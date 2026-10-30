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
    storyline premise, and child play theme.
    """
    sample = (title + " " + full_transcript[:1500]).lower()

    if any(k in sample for k in ["monster", "truk", "truck", "offroad", "lumpur", "mud"]):
        theme = "Petualangan Truk Monster Anak Melompati Rintangan & Lintasan Ekstrem Ceria"
        car_default = "Mobil Monster Truck anak warna merah menyala bergaris kuning cerah, ban off-road raksasa bergerigi hitam, bodi mengkilap bergaya animasi 3D Pixar"
        arena_default = "Arena pasir rintangan warna-warni di kamar bermain anak yang terang, dilengkapi bukit tanjakan buatan, balok susun warna-warni, dan jembatan kayu mini"
    elif any(k in sample for k in ["polisi", "police", "fire", "pemadam", "rescue", "tayo", "ambulance"]):
        theme = "Misi Penyelamatan Mobil Kota Ceria (Police & Rescue Cars Play Mission)"
        car_default = "Mobil patroli polisi anak berwarna biru-putih ceria dengan sirine mini menyala warna merah-biru dan wajah kartun tersenyum menggemaskan"
        arena_default = "Jalanan kota mini anak-anak dengan gedung kartun pastel, lampu lalu lintas mini, dan terowongan ceria"
    elif any(k in sample for k in ["race", "balap", "hot wheels", "track", "lintasan", "loop", "cepat"]):
        theme = "Kompetisi Balapan Mobil Mainan Tercepat di Lintasan Luncur Ajaib"
        car_default = "Mobil balap mainan super cepat bodi aerodinamis warna merah metalik bergaris kuning neon menyala, ban karet hitam beralur tajam"
        arena_default = "Lintasan sirkuit plastik melingkar (loop-the-loop) warna oranye-biru cerah di atas karpet bermain anak yang luas"
    elif any(k in sample for k in ["warna", "color", "learn", "belajar", "angka"]):
        theme = "Edukasi & Belajar Warna Ceria Bersama Mobil-Mobilan Warna-Warni"
        car_default = "Armada mobil mainan mini aneka warna cerah (merah, kuning, hijau, biru) berwajah kartun ramah anak bergaya 3D"
        arena_default = "Studio bermain anak bernuansa putih bersih dihiasi bola-bola mandi bola warna-warni, terowongan pelangi, dan garasi mini"
    else:
        theme = "Keseruan Anak Bermain Mobil-Mobilan di Arena Main Ceria Penuh Aksi & Suara Riang"
        car_default = "Mobil mainan anak berwarna merah menyala dengan strip kuning cerah, ban off-road besar bertekstur karet hitam, bodi 3D animasi ramah anak"
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
    """
    if total_duration_sec <= 0:
        if transcript_items:
            total_duration_sec = transcript_items[-1]["end"]
        else:
            total_duration_sec = 600.0
            
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
        
        if not full_scene_dialogue:
            fallback_sound = ["Vroom vroom! Ayo mobil merah meluncur!", "Tin tin! Ada tikungan tajam!", "Horeee melompat tinggi melewati balok!", "Wuuush kencang sekali balapannya!", "Ayo bersiap menuju garis finish!"][i % 5]
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

def build_fluid_cinematic_prompt(
    style: str,
    action: str,
    product: str,
    subject: str,
    setting: str,
    dialogue: str,
    sfx: str,
    cam_motion: str,
    language: str = "id"
) -> str:
    """
    Builds a fluid, natural, cinematic AI video prompt WITHOUT stiff bracket tags!
    Formatted specifically to deliver peak results in Google Veo, Kling AI, Runway Gen-3, Luma, and Sora.
    """
    if language == "id":
        prompt = (
            f"{style}. "
            f"{action} "
            f"Objek utama menampilkan {product} yang dipegang dan dimainkan oleh {subject} di dalam {setting}. "
            f"Kamera merekam dengan {cam_motion}. "
            f"Suasana audio dipenuhi dialog '{dialogue}' dan efek suara ceria {sfx}. "
            f"Tampilan visual 100% konsisten pada model mobil mainan, warna cat, dan tokoh anak, pencahayaan studio anak yang cerah alami, gerak stabil 24fps tanpa perubahan bentuk."
        )
    else:
        prompt = (
            f"{style}. "
            f"{action} "
            f"Featuring {product} played with excitement by {subject} inside {setting}. "
            f"Cinematic camera capture: {cam_motion}. "
            f"Audio ambiance features dialogue '{dialogue}' and playful sound effects {sfx}. "
            f"100% exact toy model, vibrant paint colors, and child character continuity across all scenes, warm natural playroom daylight, smooth 24fps motion, no morphing."
        )
    return prompt

def generate_consistent_scene_prompts(
    scenes: List[Dict[str, Any]],
    video_meta: Dict[str, Any],
    language: str = "id",
    custom_subject: Optional[str] = None,
    custom_product: Optional[str] = None,
    custom_setting: Optional[str] = None,
    custom_style: Optional[str] = None,
    image_context: Optional[Dict[str, Any]] = None,
    llm_scenes: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Transforms 10-second dialogue scenes into video-ready prompts tailored for Kids YouTube Videos.
    Seamlessly incorporates DeepSeek V4.1 Flash / Gemini LLM generated prompts when available,
    or uses dynamic keyword-driven local director engine (never stiff templates!).
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

    # Map LLM scene results by index if provided
    llm_map = {}
    if llm_scenes and isinstance(llm_scenes, list):
        for ls in llm_scenes:
            idx = ls.get("scene_index")
            if idx:
                llm_map[idx] = ls
    
    for idx, scene in enumerate(scenes):
        scene_num = scene["scene_index"]
        cam = KIDS_CAMERA_MOVEMENTS[idx % len(KIDS_CAMERA_MOVEMENTS)]
        sfx = KIDS_SOUND_EFFECTS[idx % len(KIDS_SOUND_EFFECTS)]
        dialogue = scene["dialogue"]

        # Check if DeepSeek or Gemini provided an enhanced prompt for this scene
        if scene_num in llm_map:
            l_data = llm_map[scene_num]
            action = l_data.get("action_description", "")
            video_prompt = l_data.get("video_prompt", "")
            negative_prompt = l_data.get("negative_prompt", "")
            sound_effects = l_data.get("sound_effects") or sfx
            cam_dir = l_data.get("camera_directive") or f"{cam['type']} ({cam['motion']})"
        else:
            # Dynamic Contextual Kids Toy Director Engine (Adapts to actual dialogue keywords!)
            d_lower = dialogue.lower()
            sound_effects = sfx

            # 1. Start scene
            if idx == 0:
                action = (
                    f"Di garis start arena lintasan balap, mobil mainan {product_anchor} bersiap meluncur dengan lampu bulat yang menyala ceria. "
                    f"Anak kecil {subject_anchor} tersenyum antusias memegang bagian belakang mobil sambil bersiap menghitung mundur peluncuran."
                )
                sound_effects = "[SFX: Vroom vroom menderu pelan bersiap, klakson tin-tin lucu 'beep beep!', tawa antusias anak]"
            # 2. Finish celebration scene
            elif idx == total_scenes - 1 or "finish" in d_lower or "menang" in d_lower:
                action = (
                    f"Mobil mainan {product_anchor} melesat cepat menembus pita garis finish diiringi semburan kembang api kartun ceria. "
                    f"Anak {subject_anchor} bertepuk tangan gembira dan melompat senang merayakan kemenangan balapan yang seru."
                )
                sound_effects = "[SFX: Sorak sorai kemenangan 'Horeee kita menang!', musik riang ceria, tepuk tangan meriah]"
            # 3. Crash / Bump / Stunt keyword
            elif any(k in d_lower for k in ["tabrak", "jatuh", "rusak", "opps", "oops", "awas", "hati-hati"]):
                action = (
                    f"Mobil mainan {product_anchor} meluncur sedikit oleng dan menabrak balok susun empuk warna-warni, terbalik perlahan dengan lucu tanpa kerusakan. "
                    f"Tangan mungil anak {subject_anchor} segera meraih mobil mainan sambil tertawa geli dan menegakkannya kembali."
                )
                sound_effects = "[SFX: Suara tabrakan kartun 'klak-kluk!', decitan rem lucu, tawa geli anak-anak]"
            # 4. Jump / Ramp / Fly keyword
            elif any(k in d_lower for k in ["lompat", "jump", "terbang", "tinggi", "tanjakan"]):
                action = (
                    f"Mobil mainan {product_anchor} melesat kencang di tanjakan oranye lalu melompat tinggi berputar 360 derajat di udara dengan aksi akrobatik mengagumkan. "
                    f"Kamera menangkap momen terbang lambat (slow motion) sebelum mobil mendarat mulus di atas karpet empuk."
                )
                sound_effects = "[SFX: Efek lompatan pegas kartun 'boing boing!', desingan angin cepat 'wuuush!', seruan takjub 'Waaah!']"
            # 5. Speed / Race / Fast keyword
            elif any(k in d_lower for k in ["cepat", "kencang", "balap", "race", "speed", "ngebut"]):
                action = (
                    f"Mobil mainan {product_anchor} memacu kecepatan maksimal di lintasan lurus, debu animasi kartun mengepul ceria di belakang rodanya. "
                    f"Anak {subject_anchor} menyemangati dengan mata berbinar-binar penuh kegembiraan."
                )
                sound_effects = "[SFX: Deru mesin kencang vroom-vroom!, desisan angin meluncur cepat, sorak semangat 'Ayo cepat!']"
            # 6. Curve / Drift / Loop keyword
            elif any(k in d_lower for k in ["tikungan", "loop", "putar", "belok", "drift"]):
                action = (
                    f"Mobil mainan {product_anchor} bermanuver lincah melewati lintasan melingkar (loop-the-loop) dan tikungan tajam warna-warni dengan presisi mulus. "
                    f"Bodi mobil yang mengkilap memantulkan cahaya studio anak yang hangat dan cerah."
                )
                sound_effects = "[SFX: Decitan ban kartun di tikungan 'squeeeak!', efek putaran melingkar ceria, tawa riang]"
            # Default progressive scenes
            else:
                action = (
                    f"Mobil mainan {product_anchor} menjelajahi arena {setting_anchor}, melintasi terowongan warna-warni mini dan jembatan kayu. "
                    f"Anak {subject_anchor} dengan ceria mengarahkan jalurnya dengan imajinasi petualangan yang menyenangkan."
                )

            # Generate natural, fluid cinematic prompt (NO STIFF BRACKETS!)
            video_prompt = build_fluid_cinematic_prompt(
                style=style_anchor,
                action=action,
                product=product_anchor,
                subject=subject_anchor,
                setting=setting_anchor,
                dialogue=dialogue,
                sfx=sound_effects,
                cam_motion=cam["motion"],
                language=language
            )

            negative_prompt = (
                "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry, deformed hands"
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
