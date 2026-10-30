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
    high-energy, continuous 10-second ENGLISH spoken dialogues with seamless continuity
    and natural, fluid, photorealistic 3D Pixar/Disney style video prompts.
    """
    key = (api_token or "").strip()
    if not key:
        return None

    prov = provider or detect_api_provider(key)
    
    # Prompt System for DeepSeek: Continuous English Voiceover + Locked Toy Continuity
    system_prompt = f"""You are an elite YouTube Kids Toy Video Showrunner, Voiceover Scriptwriter, and AI Video Director (think Vlad and Niki, Hot Wheels Stunt Team, and Pixar Cars).

CRITICAL REQUIREMENTS:
1. SPOKEN DIALOGUE MUST BE 100% IN ENGLISH FOR EVERY SINGLE SCENE!
2. FULL 10 SECONDS OF CONTINUOUS SPEECH (NO DEAD AIR):
   - Each scene must have an energetic, engaging 22 to 28-word spoken monologue/dialogue in English that takes the entire 10 seconds to say without empty pauses!
3. SEAMLESS NARRATIVE CONTINUITY ACROSS ALL SCENES:
   - Scene 1 directly hooks the audience and revs up.
   - Scene 2 launches down the ramp following Scene 1.
   - Scene 3 drifts into the curve following Scene 2.
   - Scene 4 encounters the obstacle, and so on, building up to a dramatic climax and victory finish at the final scene!
   - Every scene must logically connect and continue from the previous one!
4. STRICT OBJECT & CHARACTER LOCKING:
   - Locked Toy Car: {anchors.get('product', 'Red and yellow cartoon monster truck with oversized rugged wheels, glossy aerodynamic body, and expressive headlights')}
   - Locked Child Character: {anchors.get('subject', 'Cheerful 4-year-old child in bright blue and orange striped playwear with an enthusiastic smiling face')}
   - Locked Play Environment: {anchors.get('setting', 'Vibrant kids playroom track filled with orange loops, mini wooden suspension bridges, and colorful stacking blocks')}
   - Locked Visual Style: {anchors.get('style', 'Cinematic 3D Pixar animation aesthetic, 8K ultra-vibrant saturated colors, warm soft playroom lighting, 24fps smooth motion')}
5. NATURAL, FLUID VIDEO PROMPTS (NO STIFF BRACKETS):
   - Write beautiful, natural cinematic scene descriptions without bracket dividers.

STORY PREMISE & YOUTUBE VISION:
{video_vision}
Video Title: {video_meta.get('title', '')}

SCENE TIMELINE ({len(scenes_data)} scenes, 10 seconds each):
{json.dumps([{'scene_index': s['scene_index'], 'time_range': s['time_range'], 'source_cue': s['dialogue']} for s in scenes_data], indent=2)}

OUTPUT FORMAT:
Respond ONLY with a valid JSON array of objects (pure JSON, no markdown formatting):
[
  {{
    "scene_index": 1,
    "english_dialogue": "Full 10-second continuous energetic English monologue (22 to 28 words) with zero dead air, engaging toddler/kid audience.",
    "story_link": "How this scene connects to the next action",
    "sound_effects": "[SFX: Vroom vroom engine revving, cheerful horn beep beep, toddler giggle]",
    "action_description": "Precise toy car movement, stunts, and child interaction during these 10 seconds",
    "video_prompt": "Cinematic 3D Pixar animation style, 8K ultra-vibrant colors. (Natural fluid description of the locked toy car stunt, child character smiling, track obstacles, sound cues, smooth camera motion, 24fps, no morphing).",
    "camera_directive": "Dynamic Low-Angle Car Tracking (Camera glides smoothly along the track floor catching wheel motion)",
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
                {"role": "system", "content": "You are a world-class kids video director and English scriptwriter. Always reply with a valid JSON array."},
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
                {"role": "system", "content": "You are a world-class kids video director and English scriptwriter. Always reply with a valid JSON array."},
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
