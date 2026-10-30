import os
import json
import base64
import httpx
from typing import Dict, Any, Optional, List

# Endpoints
HF_ROUTER_URL = "https://router.huggingface.co/hf-inference/models/deepseek-ai/DeepSeek-V4.1-Flash-1017/v1/chat/completions"
DEEPSEEK_OFFICIAL_URL = "https://api.deepseek.com/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def detect_api_provider(token_or_key: str) -> str:
    """
    Detects whether the provided token is HuggingFace (hf_...), DeepSeek (sk-...), or Gemini (AIza...).
    """
    token = (token_or_key or "").strip()
    if token.startswith("hf_"):
        return "huggingface_deepseek"
    elif token.startswith("sk-"):
        return "deepseek_official"
    elif token.startswith("AIza"):
        return "gemini"
    # Default to HuggingFace if unknown
    return "huggingface_deepseek"

def verify_llm_key(api_key: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """
    Verifies the user's API token against DeepSeek (HuggingFace), DeepSeek Official, or Gemini.
    """
    key = (api_key or "").strip()
    if not key:
        return {"valid": False, "provider": "none", "message": "Token / API Key tidak boleh kosong"}
        
    prov = provider or detect_api_provider(key)
    
    # 1. DeepSeek via Hugging Face Router
    if prov == "huggingface_deepseek":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        test_payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 5
        }
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(HF_ROUTER_URL, headers=headers, json=test_payload)
                if resp.status_code == 200:
                    return {
                        "valid": True,
                        "provider": "huggingface_deepseek",
                        "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
                        "message": "DeepSeek-V4.1-Flash (Hugging Face) Berhasil Terhubung! 🟢"
                    }
                else:
                    err_text = resp.text
                    try:
                        err_json = resp.json()
                        err_text = err_json.get("error", err_text)
                    except Exception:
                        pass
                    return {
                        "valid": False,
                        "provider": "huggingface_deepseek",
                        "message": f"Hugging Face Token tidak valid / ditolak ({resp.status_code}): {err_text}"
                    }
        except Exception as e:
            return {"valid": False, "provider": "huggingface_deepseek", "message": f"Koneksi Hugging Face gagal: {str(e)}"}

    # 2. DeepSeek Official API (api.deepseek.com)
    elif prov == "deepseek_official":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        test_payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 5
        }
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(DEEPSEEK_OFFICIAL_URL, headers=headers, json=test_payload)
                if resp.status_code == 200:
                    return {
                        "valid": True,
                        "provider": "deepseek_official",
                        "model": "deepseek-chat",
                        "message": "DeepSeek Official API Berhasil Terhubung! 🟢"
                    }
                else:
                    return {
                        "valid": False,
                        "provider": "deepseek_official",
                        "message": f"DeepSeek API Key tidak valid ({resp.status_code}): {resp.text}"
                    }
        except Exception as e:
            return {"valid": False, "provider": "deepseek_official", "message": f"Koneksi DeepSeek gagal: {str(e)}"}

    # 3. Google Gemini
    elif prov == "gemini":
        url = f"{GEMINI_API_URL}?key={key}"
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    return {
                        "valid": True,
                        "provider": "gemini",
                        "model": "gemini-1.5-flash",
                        "message": "Google Gemini API Berhasil Terhubung! 🟢"
                    }
                else:
                    return {
                        "valid": False,
                        "provider": "gemini",
                        "message": f"Gemini API Key tidak valid ({resp.status_code})"
                    }
        except Exception as e:
            return {"valid": False, "provider": "gemini", "message": f"Koneksi Gemini gagal: {str(e)}"}

    return {"valid": False, "provider": "unknown", "message": "Format API Key / Token tidak dikenali"}

def generate_scenes_with_deepseek(
    scenes_data: List[Dict[str, Any]],
    anchors: Dict[str, str],
    video_meta: Dict[str, Any],
    video_vision: str,
    language: str,
    api_token: str,
    provider: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Uses DeepSeek V4.1 Flash (Hugging Face) or DeepSeek Official API to generate
    natural, fluid, cinematic, and non-stiff 10-second scene prompts for Kids Toy Videos.
    """
    key = (api_token or "").strip()
    if not key:
        return None

    prov = provider or detect_api_provider(key)
    
    # Prompt System for DeepSeek: Direct, cinematic, storytelling prompt generation
    system_prompt = f"""You are an elite Hollywood Director and Lead Animator specializing in viral Kids YouTube Toy Videos (like Hot Wheels stunt tracks, Monster Truck rallies, Pixar Cars 3D animation, and joyful toy car play).

YOUR TASK:
Transform YouTube transcript dialogue into rich, cinematic, fluid video generation prompts (for Google Veo, Kling AI, Runway Gen-3, Luma) for each 10-second scene (up to 60 scenes).
NO STIFF BRACKETS (like [Objek: ...] or [Gaya: ...])! The prompts must be fluid, descriptive sentences detailing the exact playful action, car physics, sound effects, child reaction, and cinematic camera movement.

KEY CONTINUITY RULES (MUST BE 100% CONSISTENT IN ALL SCENES):
- Primary Toy Car: {anchors.get('product', 'Red and yellow cartoon monster truck with massive rugged tires and glossy finish')}
- Child Character / Driver: {anchors.get('subject', 'Joyful 4-year-old toddler in bright playwear with an expressive happy smile')}
- Play Environment: {anchors.get('setting', 'Bright colorful playroom with loops, ramps, wooden blocks, and toy bridges')}
- Visual Style: {anchors.get('style', 'Pixar 3D animation style, vibrant saturated colors, soft daylight, 24fps')}
- Core Story Vision: {video_vision}
- Video Title: {video_meta.get('title', '')}
- Language: {'Bahasa Indonesia' if language == 'id' else 'English'}

SCENE DATA (10-second chunks):
{json.dumps([{'index': s['scene_index'], 'time': s['time_range'], 'dialogue': s['dialogue']} for s in scenes_data], indent=2)}

OUTPUT FORMAT:
Respond ONLY with a valid JSON array of objects (no markdown code blocks, pure JSON array):
[
  {{
    "scene_index": 1,
    "action_description": "Aksi seru mobil mainan dan anak yang natural dan hidup sesuai percakapan 10 detik ini",
    "sound_effects": "[SFX: Vroom vroom mesin mobil menderu ceria, decitan ban kartun, tawa riang anak]",
    "video_prompt": "Cinematic 3D Pixar animation style, 8K ultra-vibrant colors. (Detailed natural sentence describing car stunt/movement, child smiling interaction, track features, sound effects cue [SFX: ...], exact toy car model continuity, smooth camera motion, 24fps).",
    "camera_directive": "Low-Angle Car Chase / Macro Toy Close-Up / Dynamic 360 Spin",
    "negative_prompt": "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry"
  }}
]
"""

    if prov == "huggingface_deepseek":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "You are a professional kids video prompt director. Always reply in valid JSON array."},
                {"role": "user", "content": system_prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 4096
        }
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(HF_ROUTER_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    return json.loads(content.strip())
        except Exception as e:
            print(f"[HF DeepSeek-V4.1 Error] {e}")

    elif prov == "deepseek_official":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a professional kids video prompt director. Always reply in valid JSON array."},
                {"role": "user", "content": system_prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 4096
        }
        try:
            with httpx.Client(timeout=60.0) as client:
                resp = client.post(DEEPSEEK_OFFICIAL_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    return json.loads(content.strip())
        except Exception as e:
            print(f"[DeepSeek Official API Error] {e}")

    return None
