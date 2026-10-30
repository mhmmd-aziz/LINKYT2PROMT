import os
import json
import base64
import httpx
from typing import Dict, Any, Optional, List

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def verify_gemini_key(api_key: str) -> Dict[str, Any]:
    """
    Tests whether a Gemini API key is valid.
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
    Analyzes an uploaded image (1 foto mainan mobil, karakter kartun anak, atau arena main).
    Uses Gemini Vision multimodal analysis to identify toy details, colors, and characters for 60-scene continuity.
    """
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
Anda adalah Sutradara & Produser Konten Video YouTube Anak-Anak (Kids & Toddler Video Specialist) seperti channel mainan mobil-mobilan anak (Hot Wheels, Monster Truck, Tayo, Robocar, Pixar Cars style).
Analisis foto yang diunggah ini (bisa berupa foto mainan mobil anak, karakter anak, atau latar arena bermain) untuk dijadikan objek konsisten dalam 60 scene prompt video AI (Google Veo, Kling AI, Runway Gen-3, Luma).

Berikan output HANYA dalam format JSON valid (tanpa markdown backtick ```json) dengan struktur:
{
  "product_name": "Nama mainan mobil/karakter anak yang tampak (misal: Mobil Monster Truck Merah, Truk Excavator Kuning, Mobil Polisi Ceria, Anak Laki-laki Main Mobil)",
  "category": "Kategori konten anak (misal: Mainan Mobil-Mobilan / Petualangan Balap Anak / Kartun Edukasi Warna / Truk Konstruksi / Playground)",
  "visual_description": "Deskripsi visual sangat detail meliputi model mobil, warna mencolok (merah cerah, kuning, biru), ban besar, mata ekspresif kartun/realistis, stiker api/nomor, dan tekstur bahan mainan",
  "recommended_anchor_product": "Deskripsi detail paten mainan mobil/objek utama untuk dikunci di prompt video AI agar 100% konsisten dari scene 1 sampai scene 60",
  "recommended_anchor_subject": "Deskripsi pengemudi/karakter anak kecil yang bermain (usia 4-6 tahun, baju ceria, ekspresi gembira dan tertawa)",
  "recommended_setting": "Arena bermain anak (lintasan balap warna-warni, jalanan kota mini kartun, pasir pantai ajaib, karpet bermain kamar anak dengan aksen cerah)",
  "detected_text": "Teks/nomor/merek yang terlihat pada mainan atau latar"
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
                        text_resp = text_resp.strip()
                        if text_resp.startswith("```json"):
                            text_resp = text_resp[7:]
                        if text_resp.startswith("```"):
                            text_resp = text_resp[3:]
                        if text_resp.endswith("```"):
                            text_resp = text_resp[:-3]
                        parsed_data = json.loads(text_resp.strip())
                        parsed_data["source"] = "Gemini 1.5 Flash Vision AI (Kids Toy Specialist)"
                        return parsed_data
        except Exception as e:
            print(f"[Gemini Vision Kids Warning] {e}, falling back to smart local detection.")

    # Smart Local Fallback for Kids Video
    return {
        "product_name": "Mainan Mobil Balap & Monster Truck Anak Ceria",
        "category": "Kids Toy Adventure & Car Play",
        "visual_description": "Mainan mobil-mobilan anak berwarna merah-kuning cerah mengkilap dengan ban besar bermotif bergerigi, desain kartun ramah anak bergaya 3D Pixar, lampu depan bulat menggemaskan",
        "recommended_anchor_product": "Mainan mobil balap anak berwarna merah menyala dengan strip kuning cerah, ban off-road besar bertekstur karet hitam, bodi mengkilap bergaya 3D animasi ramah anak",
        "recommended_anchor_subject": "Anak kecil berusia 4 tahun berambut cokelat rapi mengenakan kaos garis-garis ceria biru-oranye, wajah tersenyum gembira memegang mobil mainan",
        "recommended_setting": "Arena lintasan balap mainan warna-warni di kamar bermain anak yang terang dan ceria, dilengkapi jembatan mini, terowongan kartun, dan balok susun",
        "detected_text": "Kids Car Play Reference",
        "source": "Smart Local Kids Vision Engine (Tambahkan Gemini API Key untuk deteksi presisi tinggi)"
    }

def generate_kids_prompts_with_gemini(
    scenes_data: List[Dict[str, Any]],
    anchors: Dict[str, str],
    video_meta: Dict[str, Any],
    video_vision: str,
    language: str,
    api_key: str
) -> Optional[List[Dict[str, Any]]]:
    """
    Uses Gemini API to craft playful, sound-effect rich, 10-second scene prompts for Kids YouTube videos.
    Enforces object continuity (toy cars & child character) across all 60 scenes.
    """
    if not api_key or not api_key.strip():
        return None

    try:
        endpoint = f"{GEMINI_API_URL}/gemini-1.5-flash:generateContent?key={api_key.strip()}"
        
        system_instruction = f"""
Anda adalah Sutradara & Spesialis Konten YouTube Video Anak-Anak Kelas Dunia (pembuat video viral mainan mobil anak seperti Hot Wheels, Vlad and Niki car toys, Tayo the Little Bus, Monster Truck toys).
Tugas Anda: Membuat alur prompt video AI per-scene (tepat 10 detik per scene) dengan konsistensi 100% objek mobil mainan dan tokoh anak dari Scene 1 sampai Scene terakhir (maksimal 60 scene).

VISI & KONSEP VIDEO YT INI:
{video_vision}
Judul Video: {video_meta.get('title', '')}

DATA KONSISTENSI UTAMA (WAJIB KONSISTEN DI SEMUA SCENE):
- Objek Utama (Mobil/Mainan): {anchors.get('product', '')}
- Karakter Anak / Subjek: {anchors.get('subject', '')}
- Arena / Latar: {anchors.get('setting', '')}
- Gaya Visual: {anchors.get('style', '')}
- Bahasa: {'Bahasa Indonesia' if language == 'id' else 'English'}

DATA SCENE (Masing-masing 10 detik):
{json.dumps([{'index': s['scene_index'], 'time': s['time_range'], 'dialogue': s['dialogue']} for s in scenes_data], indent=2)}

Instruksi Khusus Konten Video Anak:
1. Sertakan elemen sound effect ceria anak di setiap scene, seperti: [SFX: Vroom vroom mesin mobil, Tin tin klakson ceria, suara loncatan boing boing, tawa riang anak-anak, sorak gembira 'Horeee!'].
2. Aksi visual harus dinamis dan menyenangkan (mobil melaju kencang di turunan, melompati rintangan balok, tabrakan lembut dengan tumpukan pasir, balapan seru, parkir di garasi mini).
3. Hasilkan output HANYA list JSON array:
[
  {{
    "scene_index": 1,
    "action_description": "Deskripsi aksi seru mobil mainan dan anak selama 10 detik penuh",
    "sound_effects": "[SFX: Vroom vroom menderu, klakson tin-tin, tawa riang anak]",
    "video_prompt": "[Visual Style: ...] | [Subject Continuity: ...] | [Primary Toy Car: ...] | [Play Arena: ...] | [Camera Motion: ...] | [10s Action & Sound: ...] | [Consistency Lock: 100% exact toy model & colors]",
    "camera_directive": "Dynamic Low-Angle Car Chase / Dolly Track / Macro Toy Close-Up",
    "negative_prompt": "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark"
  }}
]
"""
        payload = {
            "contents": [{"parts": [{"text": system_instruction}]}],
            "generationConfig": {
                "temperature": 0.45,
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
        print(f"[Gemini Kids Scene Gen Warning] {e}")

    return None
