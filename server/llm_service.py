import os
import json
import base64
import httpx
from typing import Dict, Any, Optional, List

# Endpoints
HF_ROUTER_URL = "https://router.huggingface.co/hf-inference/models/deepseek-ai/DeepSeek-V4.1-Flash-1017/v1/chat/completions"
DEEPSEEK_OFFICIAL_URL = "https://api.deepseek.com/chat/completions"
TOKENHARBOR_URL = "https://tokenharbor.ai/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def detect_api_provider(token_or_key: str) -> str:
    """
    Detects whether the provided token is TokenHarbor (thk_live_...), HuggingFace (hf_...), DeepSeek (sk-...), or Gemini (AIza...).
    """
    token = (token_or_key or "").strip()
    if token.startswith("thk_live_") or token.startswith("thk_"):
        return "tokenharbor"
    elif token.startswith("hf_"):
        return "huggingface_deepseek"
    elif token.startswith("sk-"):
        return "deepseek_official"
    elif token.startswith("AIza"):
        return "gemini"
    return "tokenharbor" if "thk" in token else "huggingface_deepseek"

def verify_llm_key(api_key: str, provider: Optional[str] = None) -> Dict[str, Any]:
    """
    Verifies the user's API token against DeepSeek (HuggingFace), DeepSeek Official, or Gemini.
    """
    key = (api_key or "").strip()
    if not key:
        return {"valid": False, "provider": "none", "message": "Token / API Key tidak boleh kosong"}
        
    prov = provider or detect_api_provider(key)
    
    # 1. Token Harbor (tokenharbor.ai) with DeepSeek models
    if prov == "tokenharbor":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        # Try free tier first, then standard tier
        for model_name in ["deepseek-v4.1-flash:free", "deepseek-v4.1-flash", "deepseek-v4-flash:free"]:
            test_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "hi"}],
                "max_tokens": 5
            }
            try:
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(TOKENHARBOR_URL, headers=headers, json=test_payload)
                    if resp.status_code == 200:
                        return {
                            "valid": True,
                            "provider": "tokenharbor",
                            "model": model_name,
                            "message": f"Token Harbor DeepSeek-V4.1 ({model_name}) Berhasil Terhubung! 🟢"
                        }
                    elif resp.status_code == 402:
                        # balance zero, try next (free model)
                        continue
                    else:
                        err_text = resp.text
                        try:
                            err_json = resp.json()
                            err_msg = err_json.get("error", {}).get("message", err_text)
                        except Exception:
                            err_msg = err_text

                        if "email_verification_required" in err_text or "Verify your email" in err_msg:
                            return {
                                "valid": False,
                                "provider": "tokenharbor",
                                "message": "⚠️ Email belum diverifikasi di Token Harbor! Buka inbox email Anda atau buka tokenharbor.ai/dashboard untuk klik link verifikasi, lalu coba lagi."
                            }
            except Exception as e:
                return {"valid": False, "provider": "tokenharbor", "message": f"Koneksi Token Harbor gagal: {str(e)}"}

        return {"valid": False, "provider": "tokenharbor", "message": "Token Harbor tidak dapat mengakses model DeepSeek. Cek saldo atau limit akun di tokenharbor.ai/dashboard"}

    # 2. DeepSeek via Hugging Face Router
    elif prov == "huggingface_deepseek":
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
    provider: Optional[str] = None,
    image_context: Optional[Dict[str, Any]] = None,
    full_transcript: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Uses DeepSeek V4.1 Flash (Hugging Face) or DeepSeek Official API to deeply analyze
    the original YouTube video (title, description, full transcript) and uploaded toy car photo,
    and intelligently generates a 20-scene story remake matching the video's actual storyline!
    Produces full 10-second continuous English spoken dialogues (22-28 words), scene-specific SFX/VFX,
    and a heartfelt movie ending (penutup) at Scene 20.
    """
    key = (api_token or "").strip()
    if not key:
        return None

    prov = provider or detect_api_provider(key)
    
    video_title = video_meta.get("title", "")
    video_desc = video_meta.get("description", "")
    if len(video_desc) > 800:
        video_desc = video_desc[:800] + "..."
    
    transcript_text = (full_transcript or "").strip()
    if len(transcript_text) > 3000:
        transcript_text = transcript_text[:3000] + "... [transcript continues]"
        
    image_desc = ""
    if image_context:
        prod_n = image_context.get("recommended_anchor_product") or image_context.get("product_name", "")
        cat_n = image_context.get("category", "")
        vis_n = image_context.get("visual_description", "")
        image_desc = f"Uploaded User Toy Photo: {prod_n} (Category: {cat_n}). Visual Details: {vis_n}"

    # Prompt System for DeepSeek: Intelligent Video Remake + Uploaded Image Locking + Continuous 10s English Speech
    system_prompt = f"""You are an elite YouTube Kids Toy Video Director, Voiceover Scriptwriter, and AI Video Showrunner.

CORE MISSION:
The user has provided a YouTube video reference and an uploaded photo of their toy car.
You must REMAKE THAT EXACT YOUTUBE VIDEO into an action-packed 20-scene story (~3.3 minutes), starring the user's uploaded toy car and child character!
DO NOT use a rigid or unrelated pre-made script. You MUST analyze what actually happens in the YouTube video (from its title, description, and transcript below) and adapt THAT SPECIFIC STORY into a 20-scene narrative arc!

CRITICAL COMPLIANCE RULES FOR AI VIDEO GENERATORS (GOOGLE FLOW / VEO COMPLIANT):
1. ZERO THIRD-PARTY TRADEMARKS: Absolutely NEVER use trademark studio or brand names like "Pixar", "Disney", "Hot Wheels", "Lego", "DreamWorks", "Mattel", or "Barbie"! These trigger immediate copyright rejections in Google Flow / Veo ("penyedia konten pihak ketiga"). Instead, describe the style as "Premium 3D CGI stylized animation aesthetic, 8K ultra-vibrant saturated colors, soft golden daylight lighting, realistic glossy toy materials, 24fps smooth motion".
2. DIVERSE SETTINGS (DO NOT CONFINE TO BEDROOM / PLAYROOM): DO NOT always set the scene inside a bedroom or playroom! Adapt the environment dynamically: sunny outdoor backyard lawn with green grass and wooden bridges, miniature toy city boulevard with cartoon buildings, sandy coastal beach trail with dunes, muddy offroad track with automatic wash, or stadium grand arena.

SOURCE YOUTUBE VIDEO TO REMAKE:
- Title: {video_title}
- Description: {video_desc}
- Full Transcript / Dialogue in Video: {transcript_text if transcript_text else '(Music/visual action based video, understand story from title & description)'}
- Detected Vision Theme: {video_vision}
- User's Uploaded Toy Photo: {image_desc if image_desc else 'Standard toy vehicle'}

LOCKED CHARACTER & OBJECT CONTINUITY (100% IDENTICAL ACROSS ALL 20 SCENES):
- Hero Toy Car: {anchors.get('product', 'Locked primary toy car')}
- Child Character: {anchors.get('subject', 'Cheerful 4-year-old child in bright playwear with an enthusiastic smiling face')}
- Story Setting: {anchors.get('setting', 'Exciting adventure environment matching the video theme')}
- Visual Style: {anchors.get('style', 'Premium 3D CGI stylized animation aesthetic, 8K ultra-vibrant saturated colors, soft daylight lighting, realistic glossy toy materials, 24fps smooth motion')}

20-SCENE REMAKE STRUCTURE:
- Scene 1: Introduction of the hero toy car and setting up the core mission/challenge from the video.
- Scenes 2 to 18: Progressive obstacles, stunts, story events, and fun challenges adapted directly from the video (e.g. if police chase, follow the pursuit and roadblock; if mud/carwash, follow the mud pit and soap foam wash; if fire rescue, follow the emergency sirens, ladder, and water spray; if loop race, follow the speed challenge).
- Scene 19: Grand Climax & Mission Success (victory celebration, mission accomplished, trophy/celebration).
- Scene 20 (PENUTUP): Heartfelt Movie Farewell where the child holds the toy car, looks straight at the camera lens with a loving smile, and waves goodbye to young viewers ("Thank you so much for joining our adventure today, best friends! You are all champions! Keep playing, keep smiling, and see you next time! Bye-bye!").

SPEECH REQUIREMENTS:
- 100% IN ENGLISH FOR EVERY SINGLE SCENE!
- Continuous, high-energy speech filling the entire 10 seconds: strictly 22 to 28 words per scene (zero dead air, no short 2-word lines).

SOUND EFFECTS (SFX) & VISUAL EFFECTS (VFX):
- Provide bespoke, scene-specific Sound Effects (SFX) matching the physical action of that exact scene.
- Provide movie-grade Cinematic Visual Effects (VFX) for every scene (e.g. mud splatters, water foam, speed lines, neon glow, smoke puffs, confetti).

OUTPUT FORMAT:
Respond ONLY with a valid JSON array of 20 objects (pure JSON, no markdown formatting):
[
  {{
    "scene_index": 1,
    "act": "Act 1: The Mission Setup",
    "milestone": "Descriptive Event Name",
    "english_dialogue": "Energetic 22-28 word continuous English monologue filling all 10 seconds without silence.",
    "story_link": "How this connects to the next scene action",
    "sound_effects": "[SFX: High-RPM engine throttle revs, digital countdown beeps, child cheer]",
    "visual_effects": "Subtle heat haze shimmering above exhaust, warm morning golden sunbeams",
    "action_description": "Precise toy car movement, stunts, and child interaction during these 10 seconds",
    "camera_directive": "Dynamic Low-Angle Tracking (Camera glides smoothly catching the spinning wheels in motion)",
    "is_closing": false
  }}
]
"""

    if prov == "tokenharbor":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        for target_model in ["deepseek-v4.1-flash:free", "deepseek-v4.1-flash", "deepseek-v4-flash:free"]:
            payload = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": "You are a world-class kids video director and English scriptwriter. Directly output the valid JSON array of 20 scenes without markdown or preamble."},
                    {"role": "user", "content": system_prompt}
                ],
                "temperature": 0.4,
                "max_tokens": 8192
            }
            try:
                print(f"[DeepSeek] Mengirim permintaan 20-scene ke Token Harbor (model: {target_model})...")
                with httpx.Client(timeout=120.0) as client:
                    resp = client.post(TOKENHARBOR_URL, headers=headers, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        choice = data.get("choices", [{}])[0]
                        content = choice.get("message", {}).get("content", "").strip()
                        
                        # Robust JSON array extraction
                        start_bracket = content.find('[')
                        end_bracket = content.rfind(']')
                        if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
                            clean_json = content[start_bracket:end_bracket+1]
                            parsed = json.loads(clean_json)
                            print(f"[DeepSeek] Berhasil menghasilkan {len(parsed)} scene dari Token Harbor ({target_model})! 🟢")
                            return parsed
                        else:
                            print(f"[Token Harbor] JSON array tidak ditemukan dalam output content: {content[:200]}")
                    elif resp.status_code == 402:
                        print(f"[Token Harbor] Model {target_model} membutuhkan balance, mencoba fallback free model...")
                        continue
                    else:
                        print(f"[Token Harbor Error] Status {resp.status_code}: {resp.text}")
                        if resp.status_code in (404, 400):
                            continue
            except Exception as e:
                print(f"[Token Harbor Exception] {e}")

    elif prov == "huggingface_deepseek":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "You are a world-class kids video director and English scriptwriter. Directly output the valid JSON array of 20 scenes without markdown or preamble."},
                {"role": "user", "content": system_prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 8192
        }
        try:
            print(f"[DeepSeek] Mengirim permintaan 20-scene ke Hugging Face DeepSeek-V4.1-Flash...")
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(HF_ROUTER_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    start_bracket = content.find('[')
                    end_bracket = content.rfind(']')
                    if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
                        parsed = json.loads(content[start_bracket:end_bracket+1])
                        print(f"[DeepSeek] Berhasil menghasilkan {len(parsed)} scene dari DeepSeek-V4.1-Flash! 🟢")
                        return parsed
                else:
                    print(f"[DeepSeek HF Error] Status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[HF DeepSeek-V4.1 Exception] {e}")

    elif prov == "deepseek_official":
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a world-class kids video director and English scriptwriter. Directly output the valid JSON array of 20 scenes without markdown or preamble."},
                {"role": "user", "content": system_prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 8192
        }
        try:
            print(f"[DeepSeek] Mengirim permintaan 20-scene ke Official DeepSeek API...")
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(DEEPSEEK_OFFICIAL_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    start_bracket = content.find('[')
                    end_bracket = content.rfind(']')
                    if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
                        parsed = json.loads(content[start_bracket:end_bracket+1])
                        print(f"[DeepSeek] Berhasil menghasilkan {len(parsed)} scene dari DeepSeek Official! 🟢")
                        return parsed
                else:
                    print(f"[DeepSeek Official Error] Status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[DeepSeek Official API Exception] {e}")

    return None
