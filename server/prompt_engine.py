import math
from typing import List, Dict, Any, Optional

# Camera movement cycles to ensure visually dynamic, professional video rhythm
CAMERA_MOVEMENTS = [
    {"type": "Establishing Wide Shot", "motion": "Slow cinematic dolly forward, eye-level framing", "purpose": "Hook & Scene Introduction"},
    {"type": "Medium Close-Up (MCU)", "motion": "Smooth handheld subtle tracking, 50mm lens focus", "purpose": "Direct Creator Dialogue & Engagement"},
    {"type": "Macro Product Close-Up", "motion": "Slow pan across product texture, shallow depth of field (f/1.8)", "purpose": "Showcasing Affiliate Product Details"},
    {"type": "Over-the-Shoulder (OTS)", "motion": "Slight camera tilt down to screen/hands interaction", "purpose": "Demonstrating Real-world Usage"},
    {"type": "Dynamic Push-in Medium Shot", "motion": "Gentle zoom-in on subject's enthusiastic expression", "purpose": "Highlighting Key Pain Point / Benefit"},
    {"type": "Low Angle Hero Shot", "motion": "Subtle upward glide with warm rim lighting", "purpose": "Building Credibility & Confidence"},
    {"type": "Eye-Level Direct-to-Camera", "motion": "Locked off stabilized framing with soft natural motion", "purpose": "Call to Action & Affiliate Recommendation"}
]

def format_timestamp(seconds: float) -> str:
    """Formats seconds into MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def detect_subject_context(full_text: str, title: str, language: str = "id", image_context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Intelligently extracts the main affiliate subject, product, and style from image analysis, title, and transcript.
    """
    # If image analysis provided recommended anchors, prioritize them!
    if image_context:
        rec_prod = image_context.get("recommended_anchor_product") or image_context.get("product_name")
        rec_subj = image_context.get("recommended_anchor_subject")
        rec_set = image_context.get("recommended_setting")
        if rec_prod:
            return {
                "subject": rec_subj or ("Kreator affiliasi pria/wanita muda Indonesia usia 25 tahun, mengenakan pakaian kasual rapi" if language == "id" else "A charismatic 25-year-old creator in neat smart-casual attire"),
                "product": rec_prod,
                "setting": rec_set or ("Studio ruangan modern minimalis, pencahayaan studio hangat aksen bokeh" if language == "id" else "Contemporary minimalist creator studio with warm bokeh lighting"),
                "style": "Kualitas sinematik 8K, foto-realistis, pencahayaan komersial studio profesional, karakter dan produk 100% konsisten antar scene, 24fps" if language == "id" else "8K cinematic, photorealistic commercial ad grade, exact face and product continuity across all scenes, 24fps"
            }

    text_sample = (title + " " + full_text[:1000]).lower()
    
    # Defaults
    if language == "id":
        subject = "Kreator affiliasi profesional pria/wanita muda Indonesia usia 25 tahun, mengenakan pakaian kasual modern rapi"
        product = "Produk unggulan rekomendasi berkualitas tinggi dengan desain elegan dan modern"
        setting = "Studio ruangan modern minimalis, latar belakang bersih dengan pencahayaan hangat dan aksen neon lembut"
        style = "Kualitas sinematik 8K, foto-realistis, pencahayaan komersial studio profesional, tekstur kulit alami, gerakan halus 24fps"
    else:
        subject = "A 25-year-old charismatic content creator and affiliate reviewer, dressed in modern smart-casual attire"
        product = "Featured high-demand affiliate product with sleek modern minimalist packaging and branding"
        setting = "Contemporary creator studio with aesthetic wood acoustics, ambient warm lighting, and soft bokeh background"
        style = "Cinematic 8K, ultra-photorealistic, high-end commercial ad grade, 35mm lens, f/1.8 aperture, natural colors"
        
    # Check for specific affiliate product categories
    if any(k in text_sample for k in ["hp", "smartphone", "iphone", "samsung", "gadget", "unboxing", "review"]):
        if language == "id":
            product = "Smartphone flagship modern dengan bodi ramping, layar jernih menyala menampilkan tampilan antarmuka interaktif"
        else:
            product = "Premium flagship smartphone with sleek curved edges and vivid glowing display showing dynamic app UI"
    elif any(k in text_sample for k in ["skincare", "serum", "kulit", "wajah", "glowing", "beauty", "makeup"]):
        if language == "id":
            product = "Botol serum perawatan kulit estetik kaca amber transparan dengan pipet tetes elegan"
            setting = "Ruang rias estetik minimalis dengan marmer putih cerah dan pencahayaan daylight natural"
        else:
            product = "Luxury aesthetic glass dropper skincare serum bottle with premium minimalist label"
            setting = "Bright minimalist vanity studio with white marble accents and soft diffused daylight"
    elif any(k in text_sample for k in ["baju", "outfit", "fashion", "sepatu", "tas", "ootd", "jaket"]):
        if language == "id":
            product = "Pakaian fashion kasual trendi dengan bahan katun premium bertekstur rapi dan jahitan berkualitas"
        else:
            product = "Trendy premium apparel piece featuring high-grade fabric textures and contemporary tailoring"
    elif any(k in text_sample for k in ["laptop", "komputer", "pc", "keyboard", "mouse", "desk"]):
        if language == "id":
            product = "Laptop kerja tipis aluminium premium dengan keyboard backlit dan layar tajam tanpa bezel"
        else:
            product = "Sleek ultra-thin metallic productivity laptop with illuminated keyboard and bezel-less screen"

    return {
        "subject": subject,
        "product": product,
        "setting": setting,
        "style": style
    }

def chunk_transcript_to_10s_scenes(
    transcript_items: List[Dict[str, Any]],
    total_duration_sec: float,
    scene_duration: float = 10.0,
    max_scenes: int = 60
) -> List[Dict[str, Any]]:
    """
    Splits the video duration into exact 10-second chunks (scenes).
    Collects full conversation dialogue falling in each 10-second interval.
    Enforces a strict maximum of 60 scenes (up to 10 minutes of dense prompt-to-video).
    """
    if total_duration_sec <= 0:
        if transcript_items:
            total_duration_sec = transcript_items[-1]["end"]
        else:
            total_duration_sec = 10.0
            
    # Cap total scenes to max_scenes (default 60)
    calculated_scenes = max(1, math.ceil(total_duration_sec / scene_duration))
    num_scenes = min(calculated_scenes, max_scenes)
    scenes = []
    
    for i in range(num_scenes):
        start_t = i * scene_duration
        end_t = min((i + 1) * scene_duration, total_duration_sec)
        
        # Collect all dialogue lines that intersect this time interval
        dialogue_lines = []
        for item in transcript_items:
            item_start = item.get("start", 0.0)
            item_end = item.get("end", item_start + item.get("duration", 0.0))
            
            # Check overlap: item_start < end_t and item_end > start_t
            if item_start < end_t and item_end > start_t:
                text = item.get("text", "").strip()
                if text and text not in dialogue_lines:
                    dialogue_lines.append(text)
                    
        full_scene_dialogue = " ".join(dialogue_lines).strip()
        
        scenes.append({
            "scene_index": i + 1,
            "start_time": start_t,
            "end_time": end_t,
            "time_range": f"{format_timestamp(start_t)} - {format_timestamp(end_t)}",
            "dialogue": full_scene_dialogue if full_scene_dialogue else "(Suasana visual estetik / jeda transisi tanpa percakapan)",
            "has_dialogue": bool(full_scene_dialogue)
        })
        
    return scenes

def generate_consistent_scene_prompts(
    scenes: List[Dict[str, Any]],
    video_meta: Dict[str, Any],
    language: str = "id",
    custom_subject: Optional[str] = None,
    custom_product: Optional[str] = None,
    custom_setting: Optional[str] = None,
    custom_style: Optional[str] = None,
    image_context: Optional[Dict[str, Any]] = None,
    gemini_scenes: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Transforms 10-second dialogue scenes into video-ready prompts with visual, subject, and object continuity.
    Seamlessly merges Gemini AI generated scene prompts if available.
    """
    title = video_meta.get("title", "")
    full_text = " ".join([s["dialogue"] for s in scenes])
    context_defaults = detect_subject_context(full_text, title, language, image_context=image_context)
    
    subject_anchor = custom_subject or context_defaults["subject"]
    product_anchor = custom_product or context_defaults["product"]
    setting_anchor = custom_setting or context_defaults["setting"]
    style_anchor = custom_style or context_defaults["style"]
    
    total_scenes = len(scenes)
    processed_scenes = []

    # Map gemini scene results by index if provided
    gemini_map = {}
    if gemini_scenes and isinstance(gemini_scenes, list):
        for gs in gemini_scenes:
            idx = gs.get("scene_index")
            if idx:
                gemini_map[idx] = gs
    
    for idx, scene in enumerate(scenes):
        scene_num = scene["scene_index"]
        cam = CAMERA_MOVEMENTS[idx % len(CAMERA_MOVEMENTS)]
        dialogue = scene["dialogue"]

        # Check if Gemini provided an enhanced prompt for this scene
        if scene_num in gemini_map:
            g_data = gemini_map[scene_num]
            action = g_data.get("action_description", "")
            video_prompt = g_data.get("video_prompt", "")
            negative_prompt = g_data.get("negative_prompt", "")
            cam_dir = g_data.get("camera_directive") or f"{cam['type']} ({cam['motion']})"
        else:
            # Algorithmic Cinematic Director Engine
            if idx == 0:
                if language == "id":
                    action = f"Subjek menatap ke arah kamera dengan senyum ramah dan antusias, mulai menyapa penonton dan memperkenalkan {product_anchor} di atas meja."
                else:
                    action = f"Subject looks towards the camera with a welcoming and energetic smile, addressing the audience while introducing {product_anchor} on the table."
            elif idx == total_scenes - 1:
                if language == "id":
                    action = f"Subjek memberikan senyum percaya diri dan gestur merekomendasikan, menunjuk ke arah tombol/link affiliate sambil mengangkat {product_anchor} sebagai rekomendasi terbaik."
                else:
                    action = f"Subject delivers an affirmative call-to-action gesture, gesturing towards the link while holding {product_anchor} proudly with high confidence."
            elif idx % 3 == 1:
                if language == "id":
                    action = f"Subjek berinteraksi langsung memegang {product_anchor}, memperlihatkan detail produk dari jarak dekat secara fokus sambil menjelaskan keunggulannya."
                else:
                    action = f"Subject handles and demonstrates {product_anchor}, showing tactile textures and build quality in close inspection while talking."
            elif idx % 3 == 2:
                if language == "id":
                    action = f"Kamera menyorot ekspresi subjek yang terpukau saat mendemonstrasikan hasil penggunaan {product_anchor}, gestur tangan mengekspresikan kepuasan."
                else:
                    action = f"Camera captures subject's impressed facial expression demonstrating the real-world utility of {product_anchor}, showing authentic satisfaction."
            else:
                if language == "id":
                    action = f"Subjek tersenyum berbicara rileks di depan kamera, tangan bergerak natural mendiskusikan manfaat praktis {product_anchor} dalam kehidupan sehari-hari."
                else:
                    action = f"Subject speaks naturally to camera with expressive hand gestures, emphasizing key benefits of {product_anchor} in everyday life."

            # Structured Prompt formatted for AI Video Generation Models (Veo, Kling, Runway Gen-3, Luma)
            if language == "id":
                video_prompt = (
                    f"[Konsistensi Subjek: {subject_anchor}] | "
                    f"[Objek Produk Utama: {product_anchor}] | "
                    f"[Latar & Ruangan: {setting_anchor}] | "
                    f"[Kamera & Gerakan: {cam['type']} - {cam['motion']}] | "
                    f"[Aksi & Dialog 10 Detik: '{dialogue}'. {action}] | "
                    f"[Gaya Visual: {style_anchor}, karakter wajah dan pakaian 100% konsisten antar scene, pencahayaan alami, gerak stabil 24fps]"
                )
            else:
                video_prompt = (
                    f"[Subject Consistency: {subject_anchor}] | "
                    f"[Primary Object/Product: {product_anchor}] | "
                    f"[Environment: {setting_anchor}] | "
                    f"[Camera: {cam['type']} - {cam['motion']}] | "
                    f"[Action & 10s Dialogue: '{dialogue}'. {action}] | "
                    f"[Visual Style: {style_anchor}, exact face & outfit continuity across all scenes, smooth 24fps motion, no morphing]"
                )
                
            negative_prompt = (
                "blurry, low resolution, morphing face, distorted hands, extra fingers, cartoon, 3d render, plastic look, "
                "flickering, unstable camera shaking, text watermark, oversaturated colors, abrupt jump cuts"
            )
            cam_dir = f"{cam['type']} ({cam['motion']})"
        
        processed_scenes.append({
            "scene_index": scene_num,
            "time_range": scene["time_range"],
            "start_time": scene["start_time"],
            "end_time": scene["end_time"],
            "duration_sec": round(scene["end_time"] - scene["start_time"], 1),
            "dialogue": dialogue,
            "action_description": action,
            "camera_directive": cam_dir,
            "camera_purpose": cam["purpose"],
            "video_prompt": video_prompt,
            "negative_prompt": negative_prompt,
            "anchors": {
                "subject": subject_anchor,
                "product": product_anchor,
                "setting": setting_anchor,
                "style": style_anchor
            }
        })
        
    return processed_scenes
