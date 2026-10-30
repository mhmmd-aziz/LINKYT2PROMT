import os
import re
import tempfile
import urllib.parse
from typing import List, Dict, Any, Optional
import torch

# Ensure CUDA DLLs from PyTorch are available for CTranslate2 / Whisper on Windows
try:
    torch_lib = os.path.join(os.path.dirname(torch.__file__), "lib")
    if os.path.exists(torch_lib):
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(torch_lib)
        if torch_lib not in os.environ.get("PATH", ""):
            os.environ["PATH"] = torch_lib + os.pathsep + os.environ.get("PATH", "")
except Exception as e:
    print(f"[Warning] Failed setting torch DLL path: {e}")

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    Extracts the 11-character YouTube video ID from various URL formats or raw ID.
    """
    if not url_or_id:
        return None
    url_or_id = url_or_id.strip()
    
    # If it's already an 11-char ID
    if re.fullmatch(r"[\w-]{11}", url_or_id):
        return url_or_id
        
    parsed = urllib.parse.urlparse(url_or_id)
    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        path = parsed.path.lstrip("/")
        return path[:11] if len(path) >= 11 else None
        
    if "youtube.com" in (parsed.hostname or ""):
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/shorts/")[1][:11]
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/embed/")[1][:11]
        query = urllib.parse.parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0][:11]
            
    # Generic regex search
    match = re.search(r"(?:v=|\/|be\/|shorts\/)([\w-]{11})", url_or_id)
    if match:
        return match.group(1)
        
    return None

def fetch_video_metadata(video_id: str) -> Dict[str, Any]:
    """
    Fetches title, duration, author, thumbnail for the YouTube video using yt-dlp.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    default_meta = {
        "id": video_id,
        "url": url,
        "title": f"YouTube Video ({video_id})",
        "duration": 0,
        "author": "YouTube Creator",
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        "description": ""
    }
    
    if not yt_dlp:
        return default_meta
        
    try:
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                thumbnails = info.get("thumbnails") or []
                thumb_url = info.get("thumbnail") or (thumbnails[-1]["url"] if thumbnails else default_meta["thumbnail"])
                return {
                    "id": video_id,
                    "url": url,
                    "title": info.get("title") or default_meta["title"],
                    "duration": int(info.get("duration") or 0),
                    "author": info.get("uploader") or info.get("channel") or default_meta["author"],
                    "thumbnail": thumb_url,
                    "description": (info.get("description") or "")[:500]
                }
    except Exception as e:
        print(f"[Warning] Failed to fetch metadata with yt_dlp: {e}")
        
    return default_meta

def get_transcript_from_api(video_id: str) -> tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """
    Extracts transcript items using youtube-transcript-api.
    Compatible with both youtube-transcript-api v0.x and v1.2+.
    Returns: (transcript_items, language_code)
    """
    if not YouTubeTranscriptApi:
        return None, None
        
    try:
        transcript_list = None
        
        # 1. Try classmethod list_transcripts (v0.x)
        if hasattr(YouTubeTranscriptApi, "list_transcripts"):
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            except Exception:
                pass
                
        # 2. Try instance list or class list (v1.2+)
        if not transcript_list and hasattr(YouTubeTranscriptApi, "list"):
            try:
                transcript_list = YouTubeTranscriptApi().list(video_id)
            except Exception:
                try:
                    transcript_list = YouTubeTranscriptApi.list(video_id)
                except Exception:
                    pass

        # 3. Direct instantiation fallback
        if not transcript_list:
            try:
                api_instance = YouTubeTranscriptApi()
                if hasattr(api_instance, "list"):
                    transcript_list = api_instance.list(video_id)
            except Exception:
                pass
                
        if not transcript_list:
            print("[Info] No transcript list returned from youtube_transcript_api")
            return None, None
            
        transcript = None
        lang_code = "id"
        
        # Priority: Indonesian, English, then first available
        try:
            transcript = transcript_list.find_transcript(['id'])
            lang_code = 'id'
        except Exception:
            try:
                transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
                lang_code = 'en'
            except Exception:
                for t in transcript_list:
                    transcript = t
                    lang_code = getattr(t, "language_code", "id")
                    break
                    
        if transcript:
            fetched = transcript.fetch()
            items = []
            for item in fetched:
                # Handle both FetchedTranscriptSnippet dataclass and dict objects
                text = getattr(item, "text", None)
                if text is None and isinstance(item, dict):
                    text = item.get("text", "")
                text = str(text or "").strip().replace("\n", " ")

                start = getattr(item, "start", None)
                if start is None and isinstance(item, dict):
                    start = item.get("start", 0.0)
                start = float(start or 0.0)

                duration = getattr(item, "duration", None)
                if duration is None and isinstance(item, dict):
                    duration = item.get("duration", 0.0)
                duration = float(duration or 0.0)

                items.append({
                    "start": round(start, 2),
                    "duration": round(duration, 2),
                    "end": round(start + duration, 2),
                    "text": text
                })
            return items, lang_code
            
    except Exception as e:
        print(f"[Info] youtube-transcript-api could not get transcript directly: {e}")
        
    return None, None

def transcribe_with_whisper(video_id: str, device_preference: str = "cuda") -> tuple[List[Dict[str, Any]], str]:
    """
    Fallback: Downloads audio stream (without external ffmpeg requirement)
    and transcribes using faster-whisper on GPU (CUDA) or CPU via PyAV.
    """
    if not WhisperModel or not yt_dlp:
        raise RuntimeError("faster-whisper atau yt-dlp tidak tersedia di sistem.")
        
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download raw audio without FFmpegExtractAudio postprocessor
        audio_template = os.path.join(temp_dir, "%(id)s.%(ext)s")
        ydl_opts = {
            "format": "ba/b",  # best audio stream
            "outtmpl": audio_template,
            "quiet": True,
            "no_warnings": True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
        if not files:
            raise FileNotFoundError("Gagal mengunduh audio YouTube untuk transkripsi.")
        audio_file = files[0]
        
        # Decide device with safe fallback
        use_cuda = (device_preference == "cuda" and torch.cuda.is_available())
        device = "cuda" if use_cuda else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        
        try:
            print(f"[Transcription] Menjalankan faster-whisper pada device: {device} ({compute_type})...")
            model = WhisperModel("tiny", device=device, compute_type=compute_type)
            segments, info = model.transcribe(audio_file, beam_size=5)
            
            detected_language = info.language
            items = []
            for segment in segments:
                items.append({
                    "start": round(float(segment.start), 2),
                    "duration": round(float(segment.end - segment.start), 2),
                    "end": round(float(segment.end), 2),
                    "text": segment.text.strip()
                })
            return items, detected_language
        except Exception as e:
            if device == "cuda":
                print(f"[Whisper Warning] CUDA execution error ({e}). Mengulang otomatis dengan mode CPU...")
                model = WhisperModel("tiny", device="cpu", compute_type="int8")
                segments, info = model.transcribe(audio_file, beam_size=5)
                detected_language = info.language
                items = []
                for segment in segments:
                    items.append({
                        "start": round(float(segment.start), 2),
                        "duration": round(float(segment.end - segment.start), 2),
                        "end": round(float(segment.end), 2),
                        "text": segment.text.strip()
                    })
                return items, detected_language
            raise e

def get_complete_transcript(video_id: str, device_preference: str = "cuda") -> Dict[str, Any]:
    """
    Main extraction pipeline:
    1. Fetch metadata.
    2. Try official YouTube transcripts.
    3. If none, run Whisper on GPU/CPU.
    """
    metadata = fetch_video_metadata(video_id)
    
    # Try youtube transcript api first
    items, lang = get_transcript_from_api(video_id)
    method_used = "youtube_api"
    
    if not items or len(items) == 0:
        print("[Info] Tidak ada subtitle resmi YouTube, beralih ke GPU/CPU Whisper...")
        items, lang = transcribe_with_whisper(video_id, device_preference=device_preference)
        method_used = f"whisper_{device_preference}"
        
    # Calculate duration if not present
    if metadata["duration"] == 0 and items:
        metadata["duration"] = int(items[-1]["end"])
        
    full_text = " ".join([item["text"] for item in items])
    
    return {
        "metadata": metadata,
        "language": lang or "id",
        "method": method_used,
        "items": items,
        "full_text": full_text,
        "total_segments": len(items)
    }
