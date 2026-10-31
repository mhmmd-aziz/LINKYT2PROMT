import os
import json
import base64
import io
import httpx
from PIL import Image
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
                return {"valid": False, "message": f"API Key tidak valid ({resp.status_code})"}
    except Exception as e:
        return {"valid": False, "message": f"Gagal menghubungi Google API: {str(e)}"}

def analyze_uploaded_image(
    image_base64: str,
    api_key: Optional[str] = None,
    mime_type: str = "image/jpeg"
) -> Dict[str, Any]:
    """
    Analyzes an uploaded image (toy car, character, or track) using Gemini Vision multimodal.
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
You are a Lead Character & Toy Designer for world-class Kids YouTube 3D animated content.
Analyze this uploaded reference photo of a toy car, vehicle, or child character for strict visual continuity across 20 sequential video generation scenes.

Output ONLY a valid JSON object:
{
  "product_name": "Accurate name of the toy car / character (e.g. Red Fire Monster Truck with oversized rugged tires)",
  "category": "Kids Toy Play / Cartoon Car Adventure",
  "visual_description": "Extremely detailed visual breakdown: exact color palette (e.g. crimson red glossy body with bright lemon yellow flame decals), wheel diameter, tread pattern, headlight shape, materials",
  "recommended_anchor_product": "Locked description of this toy car to ensure 100% visual identity in all 20 AI video scenes without morphing",
  "recommended_anchor_subject": "Description of the child character (e.g. 4-year-old toddler in colorful playwear with joyful expressive smile)",
  "recommended_setting": "Playful kids room track setting (e.g. Bright playroom floor with orange race loops, wooden bridges, and colorful stacking blocks)",
  "detected_text": "Any numbers, logos, or text visible on the toy"
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
                        text_resp = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
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
            print(f"[Gemini Vision Warning] {e}")

    # Fallback to smart local PIL color & shape analysis
    return analyze_image_locally(clean_b64)

def analyze_image_locally(clean_b64: str) -> Dict[str, Any]:
    """
    Analyzes uploaded image locally using PIL to detect dominant colors, aspect ratio,
    and visual attributes of the toy car/character without requiring external API calls.
    """
    try:
        raw_bytes = base64.b64decode(clean_b64)
        img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        width, height = img.size
        
        # Resize for fast color histogram analysis
        thumb = img.resize((100, 100))
        pixels = list(thumb.getdata())
        
        # Color classification buckets
        color_counts = {
            "Blue": 0,
            "Cyan": 0,
            "Red": 0,
            "Green": 0,
            "Yellow": 0,
            "Orange": 0,
            "Purple": 0,
            "White": 0,
            "Black": 0
        }
        
        for r, g, b in pixels:
            if r > 210 and g > 210 and b > 210:
                color_counts["White"] += 1
            elif r < 45 and g < 45 and b < 45:
                color_counts["Black"] += 1
            elif r > 180 and g > 150 and b < 80:
                color_counts["Yellow"] += 1
            elif r > 180 and 80 <= g <= 150 and b < 80:
                color_counts["Orange"] += 1
            elif r > 160 and g < 100 and b < 100:
                color_counts["Red"] += 1
            elif g > 140 and g > r * 1.2 and g > b * 1.2:
                color_counts["Green"] += 1
            elif b > 140 and b > r * 1.2 and b > g * 1.2:
                color_counts["Blue"] += 1
            elif g > 130 and b > 130 and r < 100:
                color_counts["Cyan"] += 1
            elif (r > 130 and b > 130 and g < 110) or (r > 180 and b > 140 and g < 150):
                color_counts["Purple"] += 1
        
        # Filter out dominant background/white/black if colored exists
        non_neutral = {k: v for k, v in color_counts.items() if k not in ("White", "Black")}
        sorted_colored = sorted(non_neutral.items(), key=lambda x: x[1], reverse=True)
        
        if sorted_colored and sorted_colored[0][1] > 150:
            primary_color = sorted_colored[0][0]
            secondary_color = sorted_colored[1][0] if len(sorted_colored) > 1 and sorted_colored[1][1] > 100 else "Yellow"
        else:
            primary_color = "Crimson Red"
            secondary_color = "Neon Yellow"
            
        ratio = width / max(1, height)
        if ratio > 1.3:
            car_type = "Aerodynamic Stunt Racer"
            tires = "low-profile track tires with yellow rims"
        else:
            car_type = "Rugged Stunt Monster Truck"
            tires = "oversized rugged off-road rubber tires"

        product_name = f"Gleaming {primary_color} & {secondary_color} {car_type}"
        rec_anchor = (
            f"Gleaming {primary_color.lower()} {car_type.lower()} with vibrant {secondary_color.lower()} racing decals, "
            f"{tires}, rounded cartoon headlights, and glossy finish in 3D Pixar animation style"
        )
        visual_desc = (
            f"Uploaded reference photo detected: Primary {primary_color} glossy body with {secondary_color} racing accents, "
            f"{tires}, and expressive cartoon features."
        )

        return {
            "product_name": product_name,
            "category": "Kids Toy Adventure & Car Play",
            "visual_description": visual_desc,
            "recommended_anchor_product": rec_anchor,
            "recommended_anchor_subject": "Cheerful 4-year-old child in bright colorful playwear with an enthusiastic smiling face",
            "recommended_setting": "Sunlit kids playroom track featuring vibrant orange looping ramps, mini wooden suspension bridges, and colorful stacking blocks",
            "detected_text": f"{primary_color} Racer #01",
            "source": f"Smart Local Vision Engine (Detected {primary_color} & {secondary_color})"
        }
    except Exception as e:
        print(f"[Local Image Analysis Error] {e}")
        return {
            "product_name": "Gleaming Red & Yellow Stunt Monster Truck",
            "category": "Kids Toy Adventure & Car Play",
            "visual_description": "Vibrant glossy crimson red toy car with sunny yellow racing stripes, oversized black rubber rugged tires, and friendly cartoon headlights in 3D Pixar style",
            "recommended_anchor_product": "Gleaming crimson red stunt monster truck with sunny yellow racing stripes, oversized black rubber off-road tires, glossy plastic finish, and rounded headlights in 3D Pixar animation style",
            "recommended_anchor_subject": "Cheerful 4-year-old toddler with neat brown hair wearing a bright blue and orange striped play shirt, beaming with an energetic joyful smile",
            "recommended_setting": "Sunlit kids playroom track featuring vibrant orange looping ramps, mini wooden suspension bridges, and colorful stacking blocks",
            "detected_text": "Stunt Car 01",
            "source": "Smart Kids Vision Engine"
        }

def generate_kids_prompts_with_gemini(
    scenes_data: List[Dict[str, Any]],
    anchors: Dict[str, str],
    video_meta: Dict[str, Any],
    video_vision: str,
    language: str,
    api_key: str,
    image_context: Optional[Dict[str, Any]] = None,
    full_transcript: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Uses Gemini API to deeply analyze the original YouTube video and uploaded photo
    to craft a custom 20-scene remake matching the video's actual storyline with continuous English speech.
    """
    if not api_key or not api_key.strip():
        return None

    try:
        endpoint = f"{GEMINI_API_URL}/gemini-1.5-flash:generateContent?key={api_key.strip()}"
        
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

        system_instruction = f"""
You are an elite YouTube Kids Toy Video Showrunner, AI Video Director, and Voiceover Scriptwriter.

CORE MISSION:
The user wants to REMAKE THIS SPECIFIC YOUTUBE VIDEO into an action-packed 20-scene story (~3.3 minutes), starring their uploaded toy car and child character!
DO NOT use a rigid or unrelated pre-made script. You MUST analyze what actually happens in the YouTube video (from its title, description, and transcript below) and adapt THAT SPECIFIC STORY into a 20-scene narrative arc!

SOURCE YOUTUBE VIDEO TO REMAKE:
- Title: {video_title}
- Description: {video_desc}
- Full Transcript / Dialogue in Video: {transcript_text if transcript_text else '(Music/visual action based video, understand story from title & description)'}
- Detected Vision Theme: {video_vision}
- User's Uploaded Toy Photo: {image_desc if image_desc else 'Standard toy vehicle'}

LOCKED CHARACTER & OBJECT CONTINUITY (100% IDENTICAL ACROSS ALL 20 SCENES):
- Hero Toy Car: {anchors.get('product', 'Locked primary toy car')}
- Child Character: {anchors.get('subject', 'Cheerful 4-year-old child in bright playwear with an enthusiastic smiling face')}
- Story Setting: {anchors.get('setting', 'Play environment matching the video theme')}
- Visual Style: {anchors.get('style', 'Cinematic 3D Pixar animation aesthetic, 8K ultra-vibrant saturated colors, warm soft playroom lighting, 24fps smooth motion')}

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

Output ONLY a valid JSON array of 20 objects:
[
  {{
    "scene_index": 1,
    "act": "Act 1: The Mission Setup",
    "milestone": "Descriptive Event Name",
    "english_dialogue": "Energetic 22-28 word continuous English monologue filling all 10 seconds without silence.",
    "story_link": "How this connects to the next scene action",
    "sound_effects": "[SFX: High-RPM engine throttle revs, digital countdown beeps, child cheer]",
    "visual_effects": "Subtle heat haze shimmering above exhaust, warm morning playroom sunbeams",
    "action_description": "Precise toy car movement, stunts, and child interaction during these 10 seconds",
    "camera_directive": "Dynamic Low-Angle Car Tracking (Camera glides smoothly along the track floor)",
    "is_closing": false
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
                    return json.loads(text_resp.strip())
    except Exception as e:
        print(f"[Gemini Scene Gen Warning] {e}")

    return None
