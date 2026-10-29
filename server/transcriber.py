import os
import re
import tempfile
import urllib.parse
from typing import List, Dict, Any, Optional
import torch

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
    Returns: (transcript_items, language_code)
    """
    if not YouTubeTranscriptApi:
        return None, None
        
    try:
        # Check transcript list first to find available languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try manual transcript in any language, or auto-generated
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
                # Fallback to first available generated or manual
                for t in transcript_list:
                    transcript = t
                    lang_code = t.language_code
                    break
                    
        if transcript:
            fetched = transcript.fetch()
            items = []
            for item in fetched:
                items.append({
                    "start": float(item["start"]),
                    "duration": float(item["duration"]),
                    "end": float(item["start"]) + float(item["duration"]),
                    "text": item["text"].strip()
                })
            return items, lang_code
            
    except Exception as e:
        print(f"[Info] youtube-transcript-api could not get transcript directly: {e}")
        
    return None, None

def transcribe_with_whisper(video_id: str, device_preference: str = "cuda") -> tuple[List[Dict[str, Any]], str]:
    """
    Fallback: Downloads audio and transcribes using faster-whisper with GPU (CUDA) or CPU.
    """
    if not WhisperModel or not yt_dlp:
        raise RuntimeError("faster-whisper or yt-dlp is not available for audio transcription fallback.")
        
    device = "cuda" if (device_preference == "cuda" and torch.cuda.is_available()) else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_template = os.path.join(temp_dir, "%(id)s.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
            "quiet": True,
            "no_warnings": True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        audio_file = os.path.join(temp_dir, f"{video_id}.mp3")
        if not os.path.exists(audio_file):
            files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
            if not files:
                raise FileNotFoundError("Audio download failed; no media file created.")
            audio_file = files[0]
            
        print(f"[Transcription] Running faster-whisper model on device: {device} ({compute_type})...")
        model = WhisperModel("base", device=device, compute_type=compute_type)
        segments, info = model.transcribe(audio_file, beam_size=5)
        
        detected_language = info.language
        items = []
        for segment in segments:
            items.append({
                "start": float(segment.start),
                "duration": float(segment.end - segment.start),
                "end": float(segment.end),
                "text": segment.text.strip()
            })
            
        return items, detected_language

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
        print("[Info] Falling back to GPU/CPU Whisper transcription...")
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

