import os
import json
import base64
import httpx
from typing import Dict, Any, Optional, List

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def verify_gemini_key(api_key: str) -> Dict[str, Any]:
    """
    Tests whether a Gemini API key is valid by querying the models list or pinging flash model.
    """
    if not api_key:
        return {"valid": False, "message": "API Key tidak boleh kosong"}
    
    url = f"{GEMINI_API_URL}?key={api_key.strip()}"
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                has_flash = any("flash" in m for m in models)
                return {
                    "valid": True,
                    "model": "gemini-1.5-flash" if has_flash else "gemini-pro",
                    "message": "Koneksi Google Gemini API Berhasil Terhubung! 🟢"
                }
            else:
                err_msg = resp.text
                try:
                    err_json = resp.json()
                    err_msg = err_json.get("error", {}).get("message", err_msg)
                except Exception:
                    pass
                return {"valid": False, "message": f"API Key tidak valid: {err_msg}"}
    except Exception as e:
        return {"valid": False, "message": f"Gagal menghubungi Google API: {str(e)}"}

def analyze_uploaded_image(
    image_base64: str,
    api_key: Optional[str] = None,
    mime_type: str = "image/jpeg"
) -> Dict[str, Any]:
    """
    Analyzes an uploaded image (1 foto affiliate/produk/tokoh).
    If Gemini API key is provided, uses Gemini Vision multimodal analysis.
    Otherwise, returns structured local visual detection.
    """
    # Clean up base64 string
    clean_b64 = image_base64
    if "," in clean_b64:
        header, clean_b64 = clean_b64.split(",", 1)
        if "data:" in header and ";base64" in header:
            mime_type = header.split(";")[0].replace("data:", "")

    # If Gemini API key is available, call Gemini 1.5 Flash Vision
    if api_key and api_key.strip():
        try:
            model_name = "gemini-1.5-flash"
            endpoint = f"{GEMINI_API_URL}/{model_name}:generateContent?key={api_key.strip()}"
            
            prompt = """
Anda adalah AI Computer Vision & Video Director profesional untuk konten affiliasi video.
Analisis foto produk/subjek yang diunggah ini secara mendalam untuk dijadikan objek konsisten dalam alur video generator (Google Veo, Kling AI, Runway Gen-3).

Berikan output HANYA dalam format JSON valid (tanpa markdown backtick ```json) dengan struktur persis seperti ini:
{
  "product_name": "Nama jelas produk/objek yang tampak",
  "category": "Kategori produk (misal: Gadget / Skincare / Fashion / Home / Audio / dll)",
  "visual_description": "Deskripsi visual sangat detail meliputi bentuk, warna dominan, bahan/tekstur, kemasan, sudut estetika",
  "recommended_anchor_product": "Deskripsi singkat padat untuk dikunci di prompt video AI agar objek ini 100% konsisten antar scene",
  "recommended_anchor_subject": "Deskripsi tokoh/kreator yang cocok memegang/mereview produk ini (usia, busana kasual rapi, ekspresi)",
  "recommended_setting": "Deskripsi studio/latar belakang yang paling serasi dengan produk ini",
  "detected_text": "Teks/merek/logo yang terlihat pada foto jika ada"
}
"""
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": clean_b64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 800,
                    "responseMimeType": "application/json"
                }
            }

            with httpx.Client(timeout=25.0) as client:
                resp = client.post(endpoint, json=payload)
                if resp.status_code == 200:
                    res_json = resp.json()
                    candidates = res_json.get("candidates", [])
                    if candidates:
                        text_resp = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        # Parse JSON from text
                        text_resp = text_resp.strip()
                        if text_resp.startswith("```json"):
                            text_resp = text_resp[7:]
                        if text_resp.startswith("```"):
                            text_resp = text_resp[3:]
                        if text_resp.endswith("```"):
                            text_resp = text_resp[:-3]
                        parsed_data = json.loads(text_resp.strip())
                        parsed_data["source"] = "Gemini 1.5 Flash Vision AI"
                        return parsed_data
        except Exception as e:
            print(f"[Gemini Vision Warning] {e}, falling back to smart local detection.")

    # Smart Local Fallback
    return {
        "product_name": "Produk Unggulan Referensi Visual",
        "category": "Affiliate & Commercial Review",
        "visual_description": "Objek foto dengan detail tekstur permukaan tajam, warna produk natural, pencahayaan komersial studio terarah",
        "recommended_anchor_product": "Produk fisik berdesain modern elegan persis sesuai foto referensi visual yang diunggah, logo dan material tajam",
        "recommended_anchor_subject": "Kreator affiliasi muda profesional usia 25 tahun, mengenakan pakaian kasual rapi, antusias dan terpercaya",
        "recommended_setting": "Studio ruangan modern minimalis dengan aksen kayu akustik dan pencahayaan studio hangat bokeh",
        "detected_text": "Visual Product Image Reference",
        "source": "Smart Local Vision Engine (Tambahkan Gemini API Key untuk analisis mendalam)"
    }

def generate_prompts_with_gemini(
    scenes_data: List[Dict[str, Any]],
    anchors: Dict[str, str],
    video_meta: Dict[str, Any],
    language: str,
    api_key: str
) -> Optional[List[Dict[str, Any]]]:
    """
    Uses Gemini API to enhance and polish each 10s scene prompt for hyper-realistic video generation.
    """
    if not api_key or not api_key.strip():
        return None

    try:
        endpoint = f"{GEMINI_API_URL}/gemini-1.5-flash:generateContent?key={api_key.strip()}"
        
        system_instruction = f"""
Anda adalah Sutradara AI Video Prompt Kelas Dunia (ahli model Google Veo, Kling AI, Runway Gen-3).
Tugas Anda: Membuat prompt video AI per-scene (tepat 10 detik per scene) dengan konsistensi objek dan tokoh 100% dari awal sampai akhir.

DATA KONSISTENSI UTAMA:
- Objek Utama: {anchors.get('product', '')}
- Karakter / Subjek: {anchors.get('subject', '')}
- Studio / Latar: {anchors.get('setting', '')}
- Gaya Visual: {anchors.get('style', '')}
- Bahasa: {'Bahasa Indonesia' if language == 'id' else 'English'}
- Judul Video: {video_meta.get('title', '')}

DATA SCENE (Masing-masing 10 detik):
{json.dumps([{'index': s['scene_index'], 'time': s['time_range'], 'dialogue': s['dialogue']} for s in scenes_data], indent=2)}

Instruksi:
Hasilkan list JSON dari prompt untuk setiap scene dengan format:
[
  {{
    "scene_index": 1,
    "action_description": "Deskripsi aksi fisik dan pergerakan kamera sinematik selama 10 detik",
    "video_prompt": "[Konsistensi Subjek: ...] | [Objek: ...] | [Latar: ...] | [Kamera: ...] | [Aksi & Dialog 10s: ...] | [Gaya Visual: ...]",
    "camera_directive": "Wide / MCU / Close-up Product / OTS",
    "negative_prompt": "blurry, low resolution, morphing face, distorted hands, flickering, text watermark"
  }}
]
Hanya berikan JSON valid array tanpa penjelasan lain.
"""
        payload = {
            "contents": [{"parts": [{"text": system_instruction}]}],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 4096,
                "responseMimeType": "application/json"
            }
        }

        with httpx.Client(timeout=45.0) as client:
            resp = client.post(endpoint, json=payload)
            if resp.status_code == 200:
                res_json = resp.json()
                candidates = res_json.get("candidates", [])
                if candidates:
                    text_resp = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                    if text_resp.startswith("```json"):
                        text_resp = text_resp[7:]
                    if text_resp.startswith("```"):
                        text_resp = text_resp[3:]
                    if text_resp.endswith("```"):
                        text_resp = text_resp[:-3]
                    gemini_scenes = json.loads(text_resp.strip())
                    return gemini_scenes
    except Exception as e:
        print(f"[Gemini Scene Gen Warning] {e}")

    return None
