import math
import re
from typing import List, Dict, Any, Optional

# Camera movement styles designed specifically for dynamic kids toy car videos
KIDS_CAMERA_MOVEMENTS = [
    {"type": "Low-Angle Car Chase Tracking", "motion": "Kamera meluncur rendah di permukaan lantai mengikuti laju kencang ban mobil mainan secara dinamis", "purpose": "Aksi Laju Cepat & Rasa Kecepatan"},
    {"type": "Macro Close-Up Toy Detail", "motion": "Kamera makro fokus tajam menyorot bodi mengkilap, lampu bulat lucu, dan putaran roda mobil", "purpose": "Konsistensi Detail Mainan Mobil"},
    {"type": "High-Angle Playground Overview", "motion": "Kamera melayang perlahan dari atas memperlihatkan lintasan balap warna-warni dan rintangan balok", "purpose": "Menunjukkan Rute Petualangan"},
    {"type": "Dynamic 360 Spin & Jump", "motion": "Kamera berputar dinamis saat mobil melompati tanjakan rintangan dengan gerakan slow-motion halus", "purpose": "Momen Klimaks Aksi Melompat"},
    {"type": "Eye-Level Child Point of View (POV)", "motion": "Sudut pandang mata anak setinggi lantai dengan tangan kecil ceria mengarahkan mobil meluncur", "purpose": "Keterikatan Emosional Anak-Anak"},
    {"type": "Parallel Side-Scrolling Race Shot", "motion": "Kamera bergerak menyamping dengan kecepatan konstan mengikuti balapan sengit di tikungan tajam", "purpose": "Ketegangan Balapan Ceria"},
    {"type": "Victory Podium & Celebration Frame", "motion": "Kamera dolly-in perlahan menyorot mobil mainan berhenti di garis finish dengan lampu berkedip ceria", "purpose": "Kemenangan & Garis Finish"}
]

# Kids cheerful sound effects list
KIDS_SOUND_EFFECTS = [
    "[SFX: Vroom vroom mesin mobil menderu ceria, decitan ban kartun 'squeak!', tawa riang anak]",
    "[SFX: Suara klakson tin-tin lucu 'beep beep!', musik ceria bertempo riang, tepuk tangan]",
    "[SFX: Efek lompatan kartun 'boing boing!', suara desingan angin cepat 'wuuush!', sorak 'Horeee!']",
    "[SFX: Tabrakan lembut balok kayu 'klak-kluk!', suara mobil berputar rem mendadak, tawa riang gembira]",
    "[SFX: Suara sirine mini ceria 'wiu-wiu!', deru mesin cepat, suara anak berseru 'Ayo cepat!']",
    "[SFX: Gemercik pasir mainan 'shhhk!', ban mobil menanjak bukit pasir, suara peluit finish]",
    "[SFX: Musik selebrasi kemenangan bernada riang, kembang api kartun 'pop pop!', sorak bahagia 'Kita menang!']"
]

def format_timestamp(seconds: float) -> str:
    """Formats seconds into MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def extract_kids_video_vision(title: str, full_transcript: str) -> Dict[str, str]:
    """
    Analyzes the pasted YouTube video title and transcript to extract the core vision,
    storyline premise, and child play theme (e.g. Balapan Mobil, Truk Monster, Misi Penyelamatan).
    """
    sample = (title + " " + full_transcript[:1200]).lower()

    if any(k in sample for k in ["monster", "truk", "truck", "offroad", "lumpur", "mud"]):
        theme = "Petualangan Truk Monster Anak Melompati Rintangan & Lintasan Ekstrem Ceria"
        car_default = "Mobil Monster Truck anak warna merah-oranye beroda raksasa bergerigi hitam, bodi tangguh bergaya 3D kartun ramah anak"
        arena_default = "Arena pasir rintangan warna-warni dengan bukit tanjakan buatan, balok susun warna-warni, dan jembatan kayu mini"
    elif any(k in sample for k in ["polisi", "police", "fire", "pemadam", "rescue", "tayo", "ambulance"]):
        theme = "Misi Penyelamatan Mobil Kota Ceria (Police & Rescue Cars Play Mission)"
        car_default = "Mobil patroli polisi anak berwarna biru-putih ceria dengan sirine mini menyala warna merah-biru dan wajah kartun tersenyum"
        arena_default = "Jalanan kota mini anak-anak dengan gedung kartun pastel, lampu lalu lintas mini, dan terowongan ceria"
    elif any(k in sample for k in ["race", "balap", "hot wheels", "track", "lintasan", "loop", "cepat"]):
        theme = "Kompetisi Balapan Mobil Mainan Tercepat di Lintasan Luncur Ajaib"
        car_default = "Mobil balap mainan super cepat bodi aerodinamis warna merah metalik bergaris kuning neon menyala"
        arena_default = "Lintasan sirkuit plastik melingkar (loop-the-loop) warna oranye-biru cerah di atas karpet bermain anak"
    elif any(k in sample for k in ["warna", "color", "learn", "belajar", "angka"]):
        theme = "Edukasi & Belajar Warna Ceria Bersama Mobil-Mobilan Warna-Warni"
        car_default = "Armada mobil mainan mini aneka warna cerah (merah, kuning, hijau, biru) berwajah kartun menggemaskan"
        arena_default = "Studio bermain anak bernuansa putih bersih dihiasi bola-bola mandi bola warna-warni dan garasi mini"
    else:
        theme = "Keseruan Anak Bermain Mobil-Mobilan di Arena Main Ceria Penuh Aksi & Suara Riang"
        car_default = "Mainan mobil balap anak berwarna merah menyala dengan strip kuning cerah, ban karet off-road besar, bergaya animasi 3D Pixar"
        arena_default = "Kamar bermain anak yang cerah dan estetis dengan lintasan jalanan mainan, miniatur pohon kartun, dan balok susun"

    vision_summary = f"Visi Video YouTube: {theme}. Mengisahkan keseruan petualangan mobil mainan dengan aksi cepat, lompatan rintangan, dan sound effects kartun yang disukai anak-anak."

    return {
        "vision_theme": theme,
        "vision_summary": vision_summary,
        "default_car": car_default,
        "default_arena": arena_default
    }

def detect_subject_context(
    full_text: str,
    title: str,
    language: str = "id",
    image_context: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Intelligently extracts the main kids toy car, character, and setting from image analysis, title, and transcript.
    """
    vision_info = extract_kids_video_vision(title, full_text)

    # If image analysis provided recommended anchors, prioritize the uploaded toy photo!
    if image_context:
        rec_car = image_context.get("recommended_anchor_product") or image_context.get("product_name")
        rec_subj = image_context.get("recommended_anchor_subject")
        rec_set = image_context.get("recommended_setting")
        if rec_car:
            return {
                "subject": rec_subj or ("Anak laki-laki kecil usia 4 tahun mengenakan kaos garis biru-oranye ceria, wajah gembira tertawa riang" if language == "id" else "A joyful 4-year-old child in cheerful bright playwear, laughing happily"),
                "product": rec_car,
                "setting": rec_set or vision_info["default_arena"],
                "style": "Gaya animasi 3D Pixar/Disney bertekstur ultra-realistis, warna jenuh cerah (vibrant saturated colors), pencahayaan studio anak yang hangat dan ceria, 24fps gerakan halus" if language == "id" else "Pixar/Disney 3D animation style, vibrant saturated colors, warm bright children studio lighting, ultra-clean playful textures, 24fps smooth motion"
            }

    # Defaults for Kids Video
    if language == "id":
        subject = "Anak kecil laki-laki usia 4 tahun berambut cokelat rapi mengenakan kaos garis-garis ceria biru-oranye, wajah riang gembira"
        product = vision_info["default_car"]
        setting = vision_info["default_arena"]
        style = "Gaya animasi 3D Pixar/Disney anak-anak, warna mencolok sangat cerah (vibrant saturated), tekstur mobil mainan mengkilap berkualitas tinggi, pencahayaan lembut ramah anak, gerakan halus stabil 24fps"
    else:
        subject = "A joyful 4-year-old child wearing cheerful bright casual clothes, expressive happy smiling face full of excitement"
        product = vision_info["default_car"]
        setting = vision_info["default_arena"]
        style = "Pixar/Disney 3D animation style, hyper-vibrant saturated colors, glossy toy car textures, soft warm daylight, friendly kids video aesthetic, 24fps"

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
    Splits video into exact 10-second scenes (up to strictly 60 scenes).
    Collects full spoken audio and child expressions in each 10s interval.
    """
    if total_duration_sec <= 0:
        if transcript_items:
            total_duration_sec = transcript_items[-1]["end"]
        else:
            total_duration_sec = 600.0  # 60 scenes default if full duration unknown
            
    calculated_scenes = max(1, math.ceil(total_duration_sec / scene_duration))
    num_scenes = min(calculated_scenes, max_scenes)
    scenes = []
    
    for i in range(num_scenes):
        start_t = i * scene_duration
        end_t = min((i + 1) * scene_duration, total_duration_sec)
        
        dialogue_lines = []
        for item in transcript_items:
            item_start = item.get("start", 0.0)
            item_end = item.get("end", item_start + item.get("duration", 0.0))
            
            if item_start < end_t and item_end > start_t:
                text = item.get("text", "").strip()
                if text and text not in dialogue_lines:
                    dialogue_lines.append(text)
                    
        full_scene_dialogue = " ".join(dialogue_lines).strip()
        
        # If no dialogue in this 10s chunk (very common in kids car videos), insert cheerful sound / action cue
        if not full_scene_dialogue:
            fallback_sound = ["Vroom vroom! Ayo mobil merah!", "Tin tin! Awas ada tikungan!", "Horeee melompat tinggi!", "Wuuush kencang sekali!", "Balapan semakin seru!"][i % 5]
            full_scene_dialogue = f"(Aksi seru main mobil meluncur kencang - '{fallback_sound}')"
            has_dial = False
        else:
            has_dial = True
        
        scenes.append({
            "scene_index": i + 1,
            "start_time": start_t,
            "end_time": end_t,
            "time_range": f"{format_timestamp(start_t)} - {format_timestamp(end_t)}",
            "dialogue": full_scene_dialogue,
            "has_dialogue": has_dial
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
    Transforms 10-second dialogue scenes into video-ready prompts tailored for Kids YouTube Videos.
    Ensures 100% object continuity (toy car models, colors, and characters) across up to 60 scenes.
    """
    title = video_meta.get("title", "")
    full_text = " ".join([s["dialogue"] for s in scenes])
    vision_info = extract_kids_video_vision(title, full_text)
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
        cam = KIDS_CAMERA_MOVEMENTS[idx % len(KIDS_CAMERA_MOVEMENTS)]
        sfx = KIDS_SOUND_EFFECTS[idx % len(KIDS_SOUND_EFFECTS)]
        dialogue = scene["dialogue"]

        # Check if Gemini provided an enhanced prompt for this scene
        if scene_num in gemini_map:
            g_data = gemini_map[scene_num]
            action = g_data.get("action_description", "")
            video_prompt = g_data.get("video_prompt", "")
            negative_prompt = g_data.get("negative_prompt", "")
            sound_effects = g_data.get("sound_effects") or sfx
            cam_dir = g_data.get("camera_directive") or f"{cam['type']} ({cam['motion']})"
        else:
            # Algorithmic Kids Toy Car Director Engine
            sound_effects = sfx
            if idx == 0:
                if language == "id":
                    action = f"Mobil mainan {product_anchor} bersiap di garis start lintasan, lampu depan berkedip ceria, anak kecil {subject_anchor} tersenyum gembira memegang bagian belakang mobil siap meluncurkannya."
                else:
                    action = f"The toy car {product_anchor} revs at the starting gate with playful glowing headlights, child character {subject_anchor} smiles brightly with excitement ready to launch it."
            elif idx == total_scenes - 1:
                if language == "id":
                    action = f"Mobil mainan {product_anchor} melintasi garis finish dengan selebrasi lentera kembang api kartun, anak bertepuk tangan riang melompat kegirangan merayakan kemenangan."
                else:
                    action = f"The toy car {product_anchor} crosses the checkered finish line with colorful cartoon confetti, the happy child claps hands and jumps in joyful celebration."
            elif idx % 4 == 1:
                if language == "id":
                    action = f"Mobil mainan {product_anchor} meluncur kencang di turunan lintasan, meliuk melewati tikungan tajam, debu warna-warni kartun mengepul di belakang rodanya."
                else:
                    action = f"The toy car {product_anchor} speeds down the steep ramp, drifting smoothly around a colorful curve with cartoon speed dust trails."
            elif idx % 4 == 2:
                if language == "id":
                    action = f"Mobil mainan {product_anchor} melompat tinggi melewati rintangan tanjakan balok kayu, berputar 360 derajat di udara dengan gaya akrobatik seru sebelum mendarat mulus."
                else:
                    action = f"The toy car {product_anchor} performs a high stunt jump over building blocks, spinning playfully in mid-air before a smooth bouncy landing."
            elif idx % 4 == 3:
                if language == "id":
                    action = f"Kamera menyorot mobil mainan {product_anchor} melewati terowongan pelangi dan jembatan gantung mini, anak mengamati dengan takjub sambil tertawa gembira."
                else:
                    action = f"Camera tracks the toy car {product_anchor} speeding through a rainbow tunnel and suspension bridge, while the happy toddler watches in awe."
            else:
                if language == "id":
                    action = f"Mobil mainan {product_anchor} bermanuver lincah di arena {setting_anchor}, menghindari miniatur kerucut lalu lintas dan meluncur lurus ke depan dengan penuh energi."
                else:
                    action = f"The toy car {product_anchor} maneuvers swiftly across {setting_anchor}, dodging miniature traffic cones with playful speed and agility."

            # Structured Prompt formatted for AI Video Generation Models (Veo, Kling, Runway Gen-3, Luma)
            if language == "id":
                video_prompt = (
                    f"[Gaya Visual: {style_anchor}] | "
                    f"[Objek Mobil Mainan Paten: {product_anchor}] | "
                    f"[Karakter Anak: {subject_anchor}] | "
                    f"[Arena Bermain: {setting_anchor}] | "
                    f"[Kamera: {cam['type']} - {cam['motion']}] | "
                    f"[Aksi 10 Detik: {action}] | "
                    f"[Audio & Sound Effects: '{dialogue}'. {sound_effects}] | "
                    f"[Kunci Konsistensi: Model mobil mainan, warna cat, nomor, dan karakter anak 100% konsisten persis sama antar semua scene, tanpa perubahan bentuk]"
                )
            else:
                video_prompt = (
                    f"[Visual Style: {style_anchor}] | "
                    f"[Primary Toy Car Object: {product_anchor}] | "
                    f"[Child Character: {subject_anchor}] | "
                    f"[Play Environment: {setting_anchor}] | "
                    f"[Camera Motion: {cam['type']} - {cam['motion']}] | "
                    f"[10s Action: {action}] | "
                    f"[Audio & Sound Effects: '{dialogue}'. {sound_effects}] | "
                    f"[Consistency Lock: Exact same toy car model, paint scheme, wheel texture, and child appearance across all scenes without morphing]"
                )
                
            negative_prompt = (
                "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, abrupt cuts"
            )
            cam_dir = f"{cam['type']} ({cam['motion']})"
        
        processed_scenes.append({
            "scene_index": scene_num,
            "time_range": scene["time_range"],
            "start_time": scene["start_time"],
            "end_time": scene["end_time"],
            "duration_sec": round(scene["end_time"] - scene["start_time"], 1),
            "dialogue": dialogue,
            "sound_effects": sound_effects,
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
