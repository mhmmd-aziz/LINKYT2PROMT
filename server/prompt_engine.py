import math
import re
from typing import List, Dict, Any, Optional

try:
    from server.cinematic_episodes import (
        CINEMATIC_20_SCENE_ARC,
        CINEMATIC_STORY_EPISODES,
        get_thematic_20_scene_arc,
        POLICE_CHASE_20_ARC,
        MUD_CARWASH_20_ARC
    )
except ImportError:
    try:
        from cinematic_episodes import (
            CINEMATIC_20_SCENE_ARC,
            CINEMATIC_STORY_EPISODES,
            get_thematic_20_scene_arc,
            POLICE_CHASE_20_ARC,
            MUD_CARWASH_20_ARC
        )
    except ImportError:
        CINEMATIC_20_SCENE_ARC = []
        CINEMATIC_STORY_EPISODES = []
        def get_thematic_20_scene_arc(cat): return []

def extract_car_short_name(car_name: str) -> str:
    """Extracts a short, punchy category name for a car."""
    sample = (car_name or "").lower()
    if any(k in sample for k in ["police", "polisi"]):
        return "police patrol car"
    elif any(k in sample for k in ["fire", "pemadam"]):
        return "fire rescue truck"
    elif any(k in sample for k in ["hot wheels", "balap", "racer", "speed"]):
        return "stunt racer"
    elif any(k in sample for k in ["buggy", "offroad", "jeep"]):
        return "offroad buggy"
    elif any(k in sample for k in ["monster", "truk", "truck"]):
        return "monster truck"
    return "toy car"

def adapt_transcript_dialogue_to_10s_english(raw_dialogue: str, default_dialogue: str, car_short: str) -> str:
    """
    Intelligently adapts original YouTube transcript lines into lively, continuous 22-28 word English speech.
    If the original transcript has spoken words:
    - Strips transcript artifacts ([Music], [Applause], etc.)
    - Weaves the core idea and phrases into a full 10-second continuous monologue.
    If no transcript words are present, falls back to the curated 22-28 word episode script.
    """
    if not raw_dialogue:
        return default_dialogue

    cleaned = re.sub(r'\[.*?\]', '', raw_dialogue).strip()
    cleaned = re.sub(r'\(.*?\)', '', cleaned).strip()
    words = cleaned.split()
    
    if len(words) < 2:
        return default_dialogue

    is_mostly_english = all(ord(c) < 128 for c in cleaned)
    
    # If already a high-energy monologue between 22 and 28 words
    if 22 <= len(words) <= 28 and is_mostly_english:
        return cleaned

    # Otherwise craft a dynamic blend weaving the YouTube phrase into a continuous 22-28 word speech
    core_snippet = " ".join(words[:7]).rstrip(".,!?;:")
    
    blends = [
        f"Look right here, friends! As our excitement builds: \"{core_snippet}\", our {car_short} accelerates down the orange track with unstoppable high-energy speed and cheerful power!",
        f"Listen to that action! As we shout: \"{core_snippet}\", the {car_short} drifts past the obstacles and leaps into the air with pure racing excitement and laughter!",
        f"Whoosh! Our little racer responds: \"{core_snippet}\", steering the {car_short} with confident joyful hands as the wheels spin at lightning-fast speed down the slope!",
        f"Can you believe this stunt? In the middle of: \"{core_snippet}\", our champion {car_short} handles the curve like a true hero of the grand playroom rally!"
    ]
    
    chosen = blends[len(words) % len(blends)]
    c_words = chosen.split()
    if 20 <= len(c_words) <= 32:
        return chosen
    
    return default_dialogue

# Camera movement styles designed specifically for dynamic kids toy car videos
KIDS_CAMERA_MOVEMENTS = [
    {"type": "Low-Angle Car Chase Tracking", "motion": "Camera glides smoothly along the track floor catching the rapid spinning wheels of the toy car in dynamic motion", "purpose": "Speed & Ground Action"},
    {"type": "Macro Close-Up Toy Detail", "motion": "Macro camera locks onto the glossy paintwork, expressive rounded headlights, and rubber tire treads in crisp detail", "purpose": "Toy Detail & Visual Continuity"},
    {"type": "High-Angle Playground Overview", "motion": "Camera sweeps gently overhead revealing the vibrant curving race track and colorful toy obstacles", "purpose": "Playroom Track Geometry"},
    {"type": "Dynamic 360 Spin & Jump", "motion": "Camera rotates smoothly around the toy car as it leaps off a stunt ramp in fluid slow-motion", "purpose": "Airborne Stunt Climax"},
    {"type": "Eye-Level Child Point of View (POV)", "motion": "Camera frames the toddler's joyful smiling face as playful little hands steer the toy car forward", "purpose": "Child Emotional Connection"},
    {"type": "Parallel Side-Scrolling Race Shot", "motion": "Camera tracks sideways at matching speed as the toy car speeds through a hairpin turn", "purpose": "Side-Angle Race Tension"},
    {"type": "Victory Finish & Celebration Frame", "motion": "Camera dollies in slowly as the toy car parks at the finish line with sparkling celebratory confetti", "purpose": "Triumphant Finale"}
]

# Cheerful sound effects
KIDS_SOUND_EFFECTS = [
    "[SFX: Vroom vroom engine roar, playful tire squeak 'squeeeak!', joyful toddler laughter]",
    "[SFX: Cheerful horn honk 'beep beep!', upbeat playful melody, clapping hands]",
    "[SFX: Cartoon spring bounce 'boing boing!', wind whoosh 'wuuush!', cheerful shout 'Hooray!']",
    "[SFX: Soft wooden block clatter 'clack-clack!', tire drift, playful giggle]",
    "[SFX: Friendly mini rescue siren 'wee-woo!', engine revving up, energetic child cheer]",
    "[SFX: Kinetic sand crunch 'shhhk!', tires gripping over the hill, celebratory whistle]",
    "[SFX: Triumphant victory fanfare, cartoon pop confetti 'pop pop!', joyful 'We did it!']"
]

# Continuous 60-Scene Story Narrative Blocks in English (Each strictly 22-28 words for a FULL 10 SECONDS of continuous speech!)
STORY_ARC_ENGLISH_DIALOGUE = [
    "Welcome friends! Look at this incredible red and yellow monster truck ready at the starting gate. Let us rev the engine up together! Vroom vroom!",
    "Are you ready for the big race? Count down with me now: three, two, one, and off it zooms speeding down the giant looping ramp!",
    "Whoosh! The monster truck speeds through the first bright orange curve, tires gripping the track so smoothly as we cheer it on with excitement!",
    "Look out ahead! There is a steep wooden ramp right in front of us. He presses the pedal down and accelerates with full power!",
    "Up into the air it flies! Look at that amazing stunt jump high over the colorful building blocks before landing with a soft bouncy thump!",
    "Haha, look at that incredible move! The child giggles happily, quickly guiding the wheels smoothly forward to keep the unstoppable momentum going!",
    "Now we are zooming into the magical rainbow tunnel! The headlights glow brightly as the sound echoes in the cozy playroom with cheerful energy!",
    "Coming out of the tunnel at top speed! The shiny red body sparkles under the warm sunlit room as the little wheels spin faster and faster!",
    "Uh-oh, there is a sharp double curve coming right up! Watch how skillfully the little monster truck drifts past the miniature toy traffic cones!",
    "Safe and sound! He handled that tricky turn like a real racing champion. Give a big round of applause, friends, you are doing awesome!",
    "Wait, what is that up ahead? It is a bumpy kinetic sand hill! Let us see if those rugged oversized tires can conquer the climb!",
    "Rev that engine! The tires dig in and push upwards step by step until—yes! We reached the very top of the sandy mountain hill!",
    "Down the other side we glide! The truck cruises down effortlessly with a playful whoosh, kicking up a tiny trail of imaginary racing dust!",
    "Now we are entering the suspension bridge zone! The wooden planks rattle gently with a friendly click-clack sound under the sturdy rubber wheels!",
    "Steady as she goes across the bridge! The toddler smiles proudly, keeping two steady hands ready to guide our four-wheeled hero to safety!",
    "We made it across without a scratch! Now we hit the turbo boost lane—listen to that engine roar with pure happy energy, vroom vroom!",
    "Look at those vibrant looping tracks spinning overhead! He gears up to take on the giant 360-degree loop at breathtaking speed right now!",
    "Upside down it goes around the loop! Defying gravity with style, and coming out straight on the other side with a huge triumphant smile!",
    "Incredible stunt driving! The little boy jumps up and down with excitement, clapping his hands as the monster truck races along the rug!",
    "Ahead lies the colorful domino maze! Can our fearless red car weave through without knocking down a single block? Let us find out!",
    "Swerving left, then swerving right! Look at that nimble precision steering, zipping through the blocks with total ease and cheerful playful confidence!",
    "Woohoo, spotless maneuvering! Not even one block tipped over. That deserves a cheerful beep-beep of the horn, let us honk together!",
    "Now the track splits into two mystery lanes! Which path should we take today, friends? Let us choose the shiny golden ramp on the right!",
    "Down the golden ramp we fly! The car picks up incredible speed, gliding over the carpet like a rocket ship heading for adventure!",
    "Watch out for the soft foam obstacle course! The monster truck gently nudges a foam cube out of the way with zero damage done!",
    "Haha, that was super funny! He quickly straightens the bumper with a cheerful giggle and charges forward toward the next thrilling play zone!",
    "Look at the crowd of toy animal spectators cheering from the sidelines! The teddy bear and dinosaur are waving their paws with joy!",
    "He honks the horn friendly to say hello to all our playroom friends as the car speeds past the grandstand with pride!",
    "We are entering the water splash zone! Blue play balls bounce playfully off the rugged wheels like raindrops in a sunny cartoon puddle!",
    "Splash, splash, what a fun ride! The shiny red paint looks brighter than ever as we surge forward with unstoppable racing spirit!",
    "Halfway through the grand championship now! The car pauses momentarily for a lightning-fast pit stop to check those awesome rugged tires!",
    "Tires inspected and ready to roll! Three, two, one, back onto the track with a burst of laughter and high-energy excitement!",
    "Now we encounter the spiral staircase tower! The car begins circling the upward spiral track, spinning higher and higher with every second!",
    "Climbing up round and round! The bird's-eye camera catches the cheerful toddler watching in awe as the car nears the top balcony!",
    "At the peak of the spiral tower! A breathtaking view of the whole playroom playground before the ultimate high-speed zip-line plunge!",
    "Down the steep zip-ramp it plunges! Whooooosh! The wind catches the yellow flame decals as the car rockets across the room!",
    "A perfect four-wheel landing right on the plush playroom mat! That was the smoothest jump of the entire day, absolutely fantastic!",
    "The toddler can barely contain his joy, giggling out loud as he grabs the car and positions it for the final obstacle stretch!",
    "Look ahead, there is a mini ring of ribbons! The car accelerates with a determined engine rev, lining up perfectly with the center!",
    "Straight through the colorful ribbon ring it blasts at full speed! Colorful ribbons flutter everywhere like festive parade streamers celebrating our brave journey forward together!",
    "Now entering the nighttime glow-in-the-dark sector! The glowing track illuminates the glossy crimson red body with magical glowing neon colors!",
    "The rounded headlights pierce through the colorful glow, casting cheerful beams across the floor as the car glides like a shooting star!",
    "Back into the warm bright daylight! The cheerful toddler waves his hand, shouting enthusiastic encouragement to his favorite toy companion!",
    "Here comes the legendary seesaw bridge! The car drives onto the wooden plank, pausing gently right in the middle as it balances!",
    "Tilt! The seesaw tips smoothly forward, allowing our monster truck to roll down gently and resume full racing speed with confidence!",
    "Masterful balance and control! Every challenge on this course has been conquered with flying colors and giant happy toddler smiles!",
    "We are approaching the miniature town square! Mini pastel toy houses and friendly traffic lights line both sides of the boulevard!",
    "Cruising through the friendly town boulevard, the engine purrs happily while the wheels roll over the carpet with reassuring smoothness!",
    "Ahead lies the final mega ramp of the championship! The biggest, steepest, most thrilling incline on the entire playroom circuit!",
    "Full throttle ahead! Listen to the mighty vroom-vroom roar as the red monster truck attacks the incline with sheer enthusiasm!",
    "Over the crest it leaps! Soaring through the air in majestic slow-motion with cartoon sparkles dancing around the rugged black wheels!",
    "Touchdown! That was a flawless four-wheel landing right into the final straightaway lane, accelerating smoothly and heading straight toward the checkered finish line banners!",
    "The crowd of toy spectators goes wild with cheering! Hear the applause, the whistling, and the joyful shouting from all around the room!",
    "Only a few meters left to go! The toddler leans forward with anticipation, eyes sparkling with sheer delight and festive excitement!",
    "Here comes the final sprint! The monster truck unleashes every bit of turbo power left in its playful little battery engine!",
    "And across the finish line it zooms! The checkered flag drops as colorful cartoon confetti pops in every direction with joy!",
    "Victory is ours! The red monster truck parks proudly on the top winner's podium with headlights flashing like celebratory disco lights!",
    "The happy child jumps up in pure elation, raising his hands high in the air and shouting: Hooray, we won the championship today!",
    "What an unforgettable toy car adventure we shared together today, packed with thrilling ramp jumps, hilarious cartoon sound effects, and nonstop playful laughter with friends!",
    "Thank you so much for racing with us today, best friends! Don't forget to smile, keep playing, and see you in the next race!"
]

def format_timestamp(seconds: float) -> str:
    """Formats seconds into MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def extract_kids_video_vision(title: str, full_transcript: str) -> Dict[str, str]:
    """
    Analyzes the pasted YouTube video title and transcript to extract the core vision,
    storyline premise, and child play theme dynamically rather than forcing a rigid template.
    """
    sample = (title + " " + full_transcript[:3000]).lower()

    if any(k in sample for k in ["polisi", "police", "cop", "patrol", "siren", "sirine", "penjahat", "thief", "chase"]):
        story_cat = "police"
        theme = "City Police Patrol & High-Speed Pursuit Mission"
        car_default = "Cheerful blue and white toy police patrol car with flashing dual red-blue sirens and smiling cartoon headlights in premium 3D CGI stylized animation style"
        arena_default = "Miniature vibrant toy city with cartoon pastel buildings, tiny traffic lights, and paved miniature roadways"
    elif any(k in sample for k in ["mud", "muddy", "lumpur", "wash", "cuci", "sabun", "soap", "kotor"]):
        story_cat = "mud_wash"
        theme = "Messy Muddy Offroad Trail & Automatic Toy Car Wash Adventure"
        car_default = "Rugged offroad 4x4 toy truck with knobby mud tires, snorkel exhaust, and durable glossy finish in premium 3D CGI stylized animation style"
        arena_default = "Sunlit outdoor backyard dirt trail with wet gooey mud bog and a colorful automatic bubble car wash station"
    elif any(k in sample for k in ["fire", "pemadam", "damkar", "kebakaran", "rescue", "api"]):
        story_cat = "fire"
        theme = "Emergency Fire Truck Rescue & Water Cannon Mission"
        car_default = "Bright crimson red toy fire rescue truck with extendable ladder, flashing yellow beacons, and water hoses in premium 3D CGI stylized animation style"
        arena_default = "Miniature cartoon city square with building block towers, water hydrant, and rescue fire station"
    elif any(k in sample for k in ["monster", "truk", "truck", "offroad"]):
        story_cat = "monster_truck"
        theme = "Stunt Monster Truck Arena Rally & Obstacle Course Adventure"
        car_default = "Gleaming crimson red stunt monster truck with bright yellow flame decals, oversized rugged off-road tires, and rounded cartoon headlights in premium 3D CGI stylized animation style"
        arena_default = "Outdoor sunny arena with dirt mounds, wooden launch ramps, colorful flags, and cheerful obstacle gates"
    elif any(k in sample for k in ["race", "balap", "track", "lintasan", "loop", "cepat", "speed"]):
        story_cat = "stunt_race"
        theme = "High-Speed Toy Car Championship & Stunt Circuit Race"
        car_default = "Ultra-fast metallic red aerodynamic racer with glowing neon yellow stripes and black low-profile tires in premium 3D CGI stylized animation style"
        arena_default = "Expansive championship speed circuit with colorful curving tracks, neon finish gates, and stadium grandstand banners"
    else:
        story_cat = "general"
        theme = "Cheerful Kids Toy Car Adventure with Stunts and Sound Effects"
        car_default = "Gleaming glossy adventure toy car with rugged off-road tires, colorful finish, and expressive rounded headlights in premium 3D CGI stylized animation style"
        arena_default = "Sunny outdoor backyard garden trail with green grass, mini wooden suspension bridges, and colorful stepping stone obstacles"

    vision_summary = f"YouTube Video Concept: {theme}. The story follows an exciting kid toy adventure tailored from the video's actual storyline, featuring our hero vehicle."

    return {
        "story_category": story_cat,
        "vision_theme": theme,
        "vision_summary": vision_summary,
        "default_car": car_default,
        "default_arena": arena_default
    }

def detect_subject_context(
    full_text: str,
    title: str,
    language: str = "en",
    image_context: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Extracts the main kids toy car, character, and setting with strict continuity locks.
    """
    vision_info = extract_kids_video_vision(title, full_text)

    # If image analysis provided recommended anchors, prioritize the uploaded toy photo!
    if image_context:
        rec_car = image_context.get("recommended_anchor_product") or image_context.get("product_name")
        rec_subj = image_context.get("recommended_anchor_subject")
        rec_set = image_context.get("recommended_setting")
        if rec_car:
            return {
                "subject": rec_subj or "Cheerful 4-year-old child in bright blue and orange playwear with an enthusiastic smiling face",
                "product": rec_car,
                "setting": rec_set or vision_info["default_arena"],
                "style": "Premium 3D CGI stylized animation aesthetic, 8K ultra-vibrant saturated colors, soft daylight lighting, realistic glossy toy textures, 24fps smooth motion"
            }

    return {
        "subject": "Cheerful 4-year-old toddler with neat brown hair wearing a bright blue and orange striped shirt, beaming with a happy energetic smile",
        "product": vision_info["default_car"],
        "setting": vision_info["default_arena"],
        "style": "Premium 3D CGI stylized animation aesthetic, 8K ultra-vibrant saturated colors, soft daylight lighting, realistic glossy toy textures, 24fps smooth motion"
    }

def chunk_transcript_to_10s_scenes(
    transcript_items: List[Dict[str, Any]],
    total_duration_sec: float,
    scene_duration: float = 10.0,
    max_scenes: int = 20
) -> List[Dict[str, Any]]:
    """
    Splits video into exact 10-second scenes (up to strictly 20 scenes).
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
                    
        raw_scene_dialogue = " ".join(dialogue_lines).strip()
        
        scenes.append({
            "scene_index": i + 1,
            "start_time": start_t,
            "end_time": end_t,
            "time_range": f"{format_timestamp(start_t)} - {format_timestamp(end_t)}",
            "dialogue": raw_scene_dialogue,
            "has_dialogue": bool(raw_scene_dialogue)
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
    vfx: str = ""
) -> str:
    """
    Builds a unified, natural, cinematic AI video prompt that embeds:
    - Premium 3D CGI stylized animation aesthetic
    - Locked toy car & child character continuity
    - 10-second physical toy action & stunt
    - FULL 10-second continuous spoken English dialogue (22-28 words, filling all 10s with no dead air!)
    - Playful sound effects (SFX) matched to physical stunt
    - Cinematic Visual Effects (VFX)
    - Cinematic camera movement
    - Strict visual continuity lock
    When copied, this single prompt gives Google Flow / Kling / Veo / Runway everything needed!
    """
    prompt = (
        f"{style}. "
        f"{action} "
        f"Featuring the locked primary toy vehicle {product}, steered with joyful energy by the child character {subject} in {setting}. "
        f"Spoken Dialogue (Full 10-Second Continuous English Speech): \"{dialogue}\" "
        f"Sound Effects (SFX): {sfx}. "
    )
    if vfx:
        prompt += f"Cinematic Visual Effects (VFX): {vfx}. "
    prompt += (
        f"Cinematic Camera: {cam_motion}. "
        f"Visual Continuity Lock: 100% exact toy vehicle model, glossy paint colors, wheel diameter, child face, and {setting} lighting strictly identical across all scenes, warm natural daylight, smooth 24fps motion, no morphing, no distortion."
    )
    return prompt

def generate_consistent_scene_prompts(
    scenes: List[Dict[str, Any]],
    video_meta: Dict[str, Any],
    language: str = "en",
    custom_subject: Optional[str] = None,
    custom_product: Optional[str] = None,
    custom_setting: Optional[str] = None,
    custom_style: Optional[str] = None,
    image_context: Optional[Dict[str, Any]] = None,
    llm_scenes: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Transforms 10-second dialogue scenes into video-ready prompts tailored for Kids YouTube Videos.
    Produces full 10s continuous English dialogues, seamless story links, and locked toy car continuity.
    Uses 60 unique progressive cinematic episodes across 8 acts with scene-specific SFX, VFX, and heartfelt penutup.
    """
    title = video_meta.get("title", "")
    full_text = " ".join([s.get("dialogue", "") for s in scenes])
    vision_info = extract_kids_video_vision(title, full_text)
    context_defaults = detect_subject_context(full_text, title, language="en", image_context=image_context)
    
    # If image_context is provided, the uploaded photo STRICTLY defines the car model and colors!
    if image_context and (image_context.get("recommended_anchor_product") or image_context.get("product_name")):
        product_anchor = image_context.get("recommended_anchor_product") or image_context.get("product_name")
        if image_context.get("recommended_anchor_subject"):
            subject_anchor = image_context.get("recommended_anchor_subject")
        else:
            subject_anchor = custom_subject or context_defaults["subject"]
            
        if image_context.get("recommended_setting"):
            setting_anchor = image_context.get("recommended_setting")
        else:
            setting_anchor = custom_setting or context_defaults["setting"]
    else:
        product_anchor = custom_product or context_defaults["product"]
        subject_anchor = custom_subject or context_defaults["subject"]
        setting_anchor = custom_setting or context_defaults["setting"]
        
    style_anchor = custom_style or context_defaults["style"]
    car_short = extract_car_short_name(product_anchor)
    
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

        ep = None
        # Fetch matching cinematic story episode template (prefer dedicated 20-scene cohesive arc based on detected video theme)
        if total_scenes <= 20:
            thematic_arc = get_thematic_20_scene_arc(vision_info.get("story_category", ""))
            if not thematic_arc:
                thematic_arc = CINEMATIC_20_SCENE_ARC
            if idx == total_scenes - 1:
                ep = thematic_arc[-1]  # Scene 20 (PENUTUP: Heartfelt Movie Farewell)
            elif idx == total_scenes - 2 and total_scenes >= 2:
                ep = thematic_arc[-2]  # Scene 19 (Victory Finish Line & Trophy)
            else:
                ep = thematic_arc[min(idx, len(thematic_arc) - 1)]
        elif CINEMATIC_STORY_EPISODES:
            # If at the end of the video, ensure we reach the grand climax & penutup
            if idx == total_scenes - 1 and total_scenes >= 2:
                ep = CINEMATIC_STORY_EPISODES[-1]  # (PENUTUP: Heartfelt Movie Farewell)
            elif idx == total_scenes - 2 and total_scenes >= 3:
                ep = CINEMATIC_STORY_EPISODES[-2]  # (Winner's Podium Trophy Ceremony)
            elif idx == total_scenes - 3 and total_scenes >= 4:
                ep = CINEMATIC_STORY_EPISODES[-3]  # (Victory Finish Line Crossing)
            else:
                ep = CINEMATIC_STORY_EPISODES[idx % len(CINEMATIC_STORY_EPISODES)]

        if ep:
            act = ep.get("act", "")
            milestone = ep.get("milestone", "")
            is_closing = ep.get("is_closing", False) or (idx == total_scenes - 1)
            vfx = ep.get("vfx", "Warm natural playroom lighting, crisp 8K macro toy details, soft 24fps motion")
            sfx = ep.get("sfx", KIDS_SOUND_EFFECTS[idx % len(KIDS_SOUND_EFFECTS)])
            story_link = ep.get("story_link", f"Leads into Scene {min(scene_num + 1, total_scenes)}")

            # Interpolate template variables
            try:
                base_action = ep["action"].format(
                    product=product_anchor,
                    product_short=car_short,
                    subject=subject_anchor,
                    setting=setting_anchor
                )
            except Exception:
                base_action = ep["action"]

            try:
                base_dialogue = ep["dialogue"].format(
                    product=product_anchor,
                    product_short=car_short,
                    subject=subject_anchor,
                    setting=setting_anchor
                )
            except Exception:
                base_dialogue = ep["dialogue"]
        else:
            act = f"Act {(idx // 8) + 1}"
            milestone = f"Scene {scene_num} Action"
            is_closing = (idx == total_scenes - 1)
            vfx = "Dynamic 24fps motion, warm soft playroom sunlight, crisp 8K focus"
            sfx = KIDS_SOUND_EFFECTS[idx % len(KIDS_SOUND_EFFECTS)]
            story_link = f"Connects into Scene {min(scene_num + 1, total_scenes)}"
            base_action = f"{product_anchor} drives through {setting_anchor} steered by {subject_anchor}."
            base_dialogue = STORY_ARC_ENGLISH_DIALOGUE[idx % len(STORY_ARC_ENGLISH_DIALOGUE)]

        # Check if DeepSeek or Gemini provided an enhanced prompt for this scene
        if scene_num in llm_map:
            l_data = llm_map[scene_num]
            english_dialogue = l_data.get("english_dialogue") or l_data.get("dialogue") or base_dialogue
            story_link = l_data.get("story_link") or story_link
            action = l_data.get("action_description") or base_action
            sound_effects = l_data.get("sound_effects") or sfx
            visual_effects = l_data.get("visual_effects") or vfx
            act = l_data.get("act") or act
            milestone = l_data.get("milestone") or milestone
            is_closing = l_data.get("is_closing", False) or (idx == total_scenes - 1)
            cam_dir = l_data.get("camera_directive") or f"{cam['type']} ({cam['motion']})"
            
            video_prompt = l_data.get("video_prompt", "")
            if not video_prompt or ("Spoken Dialogue" not in video_prompt and len(video_prompt) < 200):
                video_prompt = build_fluid_cinematic_prompt(
                    style=style_anchor,
                    action=action,
                    product=product_anchor,
                    subject=subject_anchor,
                    setting=setting_anchor,
                    dialogue=english_dialogue,
                    sfx=sound_effects,
                    cam_motion=cam["motion"],
                    vfx=visual_effects
                )
            negative_prompt = l_data.get("negative_prompt", "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry")
        else:
            # Intelligently adapt YouTube transcript dialogue if present, or use the curated 22-28 word continuous line
            raw_dialogue = scene.get("dialogue", "").strip()
            english_dialogue = adapt_transcript_dialogue_to_10s_english(raw_dialogue, base_dialogue, car_short)
            action = base_action
            sound_effects = sfx
            visual_effects = vfx
            cam_dir = f"{cam['type']} ({cam['motion']})"
            negative_prompt = (
                "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry, deformed hands"
            )

            # Build unified, natural cinematic video prompt with embedded dialogue, SFX, and VFX!
            video_prompt = build_fluid_cinematic_prompt(
                style=style_anchor,
                action=action,
                product=product_anchor,
                subject=subject_anchor,
                setting=setting_anchor,
                dialogue=english_dialogue,
                sfx=sound_effects,
                cam_motion=cam["motion"],
                vfx=visual_effects
            )
        
        # Calculate speech word count
        words = len(english_dialogue.split())
        
        processed_scenes.append({
            "scene_index": scene_num,
            "time_range": scene["time_range"],
            "start_time": scene["start_time"],
            "end_time": scene["end_time"],
            "duration_sec": round(scene["end_time"] - scene["start_time"], 1),
            "dialogue": english_dialogue,
            "english_dialogue": english_dialogue,
            "word_count": words,
            "speech_duration_est": "Full 10s Spoken",
            "act": act,
            "milestone": milestone,
            "story_link": story_link or f"Seamlessly links into Scene {min(scene_num + 1, total_scenes)}",
            "sound_effects": sound_effects,
            "visual_effects": visual_effects,
            "is_closing": is_closing,
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
        
    return processed_scenes

def generate_youtube_viral_package(
    video_meta: Dict[str, Any],
    anchors: Dict[str, str],
    scenes: List[Dict[str, Any]],
    image_context: Optional[Dict[str, Any]] = None,
    vision: Optional[Dict[str, Any]] = None,
    thumbnail_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates high-CTR viral YouTube metadata in English:
    1. 5 Hype FYP Titles optimized for kids audience algorithms.
    2. Comprehensive SEO Description with storyline synopsis, chapter timestamps, call-to-actions, and tags.
    3. Cinematic AI Thumbnail Prompts optimized for Google Gemini / Imagen 3 / Midjourney (16:9) WITH BOLD 3D EMBEDDED TEXT.
    """
    car_name = anchors.get("product", "Gleaming crimson red stunt monster truck with flame decals")
    child_name = anchors.get("subject", "Cheerful 4-year-old child with an energetic smile")
    arena_name = anchors.get("setting", "vibrant playroom track with orange looping ramps")
    orig_title = video_meta.get("title", "")
    
    # Extract short punchy car name and theme dynamically
    sample_car = (car_name + " " + orig_title).lower()
    
    if "police" in sample_car or "polisi" in sample_car or "cop" in sample_car or "patrol" in sample_car:
        car_short = "POLICE PATROL CAR"
        theme_tag = "Police"
        viral_titles = [
            f"POLICE CHASE! 🚓🚨 Can {car_short} Catch the Speedy Bandit? (Kids Toy Car Rescue)",
            f"EMERGENCY CALL! 🚨 Super {car_short} on High-Speed City Mission!",
            f"CAUGHT YOU! 🚔 {car_short} Roadblock & Stunt Pursuit for Kids!",
            f"HERO COPS! 🌟 Best {car_short} Toy City Adventure!",
            f"{car_short} ON PATROL! 🚨 Sirens & Speed Challenge!"
        ]
        default_thumb_text = "POLICE RESCUE! 🚨"
        text_options = ["POLICE RESCUE! 🚨", "STOP THIEF! 🚓", "EMERGENCY! 🚔", "CAUGHT YOU! 🛑", "MISSION WIN! 🏆"]
    elif "mud" in sample_car or "wash" in sample_car or "lumpur" in sample_car or "soap" in sample_car:
        car_short = "MUDDY 4X4 TRUCK"
        theme_tag = "CarWash"
        viral_titles = [
            f"SUPER DIRTY TRUCK WASH! 💦 {car_short} Muddy Bog Rescue & Bubble Bath!",
            f"DIRTY TO CLEAN! 🧼 Can We Wash The Messiest {car_short}?",
            f"MEGA MUDDY SPLASH! 🌊 {car_short} Extreme Offroad Carwash Adventure!",
            f"BUBBLE FOAM SHINE! ✨ Best Automatic Car Wash for Kids!",
            f"{car_short} MUD RESCUE! 🚜 Offroad Dirt Challenge!"
        ]
        default_thumb_text = "DIRTY TO CLEAN! 🧼"
        text_options = ["DIRTY TO CLEAN! 🧼", "MEGA MUD! 💦", "CAR WASH! 🫧", "BUBBLE FOAM! 🧽", "SUPER CLEAN! ✨"]
    elif "fire" in sample_car or "pemadam" in sample_car or "damkar" in sample_car:
        car_short = "FIRE RESCUE TRUCK"
        theme_tag = "FireTruck"
        viral_titles = [
            f"FIRE RESCUE MISSION! 🚒🔥 Brave {car_short} Saves The Day!",
            f"WATER CANNON SPRAY! 💦 Can {car_short} Put Out The Flames?",
            f"HERO RESCUE! 🚨 Emergency Ladder & Siren Sprint with {car_short}!",
            f"BRAVE FIREFIGHTER! 🌟 Best Toy Rescue Story for Kids!",
            f"{car_short} TO THE RESCUE! 🚒 High-Speed Emergency Call!"
        ]
        default_thumb_text = "FIRE RESCUE! 🚒"
        text_options = ["FIRE RESCUE! 🚒", "HERO TRUCK! 🚨", "SAVE THE DAY! 🔥", "WATER SPRAY! 💦", "WE DID IT! 🏆"]
    elif "tractor" in sample_car or "traktor" in sample_car or "farm" in sample_car:
        car_short = "FARM TRACTOR"
        theme_tag = "Tractor"
        viral_titles = [
            f"BUSY FARM TRACTOR! 🚜🌾 {car_short} Harvest & Field Adventure for Kids!",
            f"HEAVY WORK TRACTOR! 🌟 Can {car_short} Pull The Giant Cart?",
            f"MUDDY FARM TRAIL! 🚜 Sturdy Wheels Conquer The Farm!",
            f"FRIENDLY TRACTOR DAY! 🌾 Best Toy Farm Story!",
            f"{car_short} HARVEST FUN! 🌟 Farm Rescue Mission!"
        ]
        default_thumb_text = "BIG TRACTOR! 🚜"
        text_options = ["BIG TRACTOR! 🚜", "FARM HERO! 🌾", "HEAVY PULL! 🚜", "MUDDY TRAIL! 💦", "SUPER FUN! 🌟"]
    elif "excavator" in sample_car or "bego" in sample_car or "digger" in sample_car or "construction" in sample_car:
        car_short = "TOY EXCAVATOR"
        theme_tag = "Construction"
        viral_titles = [
            f"BIG EXCAVATOR DIGGING! 🚜🏗️ {car_short} Sand Quarry & Building Site!",
            f"DIG AND BUILD! 🧱 Can {car_short} Build The Highest Hill?",
            f"HEAVY CONSTRUCTION! 🚧 {car_short} Sandbox Rescue Mission!",
            f"BUILD TIME! 🏗️ Best Toy Construction Vehicles for Kids!",
            f"{car_short} AT WORK! 🚜 Sturdy Bucket Action!"
        ]
        default_thumb_text = "BIG DIGGER! 🚜"
        text_options = ["BIG DIGGER! 🚜", "BUILD TIME! 🏗️", "HEAVY WORK! 🧱", "SAND DIG! 🚧", "MISSION WIN! 🏆"]
    elif "monster" in sample_car or "truk" in sample_car or "truck" in sample_car:
        car_short = "MONSTER TRUCK"
        theme_tag = "MonsterTruck"
        viral_titles = [
            f"BIG WHEELS CRUSH! 🚜💥 {car_short} Extreme Arena Stunt Rally!",
            f"CRUSH CHALLENGE! ⚡ Massive {car_short} Bounces Over Obstacles!",
            f"MONSTER RALLY! 🏎️💨 {car_short} Arena Power Stunt for Kids!",
            f"UNSTOPPABLE! 🌟 Best {car_short} Adventure Story!",
            f"{car_short} POWER! 🚜 Mega Tire Action!"
        ]
        default_thumb_text = "MONSTER CRUSH! 💥"
        text_options = ["MONSTER CRUSH! 💥", "BIG TIRES! 🚜", "SMASH TIME! ⚡", "UNSTOPPABLE! 🚀", "VROOM VROOM! 🏁"]
    elif "hot wheels" in sample_car:
        car_short = "HOT WHEELS RACER"
        theme_tag = "HotWheels"
        viral_titles = [
            f"TURBO SPEED CHALLENGE! 🏎️💨 {car_short} Grand Prix Championship!",
            f"WHO WILL WIN?! 🏆 Ultimate {car_short} Speed Stunt Race for Kids!",
            f"MEGA SPEED RALLY! 🚀 {car_short} Playroom Racing Cup!",
            f"FASTEST RACER! 🌟 Best {car_short} Track Adventure!",
            f"{car_short} SPEED BOOST! ⚡ Grand Prix Winner!"
        ]
        default_thumb_text = "SUPER SPEED! ⚡"
        text_options = ["SUPER SPEED! ⚡", "WHO WILL WIN?! 🏁", "TURBO BOOST! 🚀", "VICTORY! 🏆", "GO GO GO! 🏎️"]
    elif "race" in sample_car or "balap" in sample_car or "racer" in sample_car or "speed" in sample_car:
        car_short = "SUPER RACER"
        theme_tag = "SpeedRacer"
        viral_titles = [
            f"TURBO SPEED RACE! 🏎️💨 {car_short} Playroom Championship Cup!",
            f"WHO WILL WIN? 🏆 High-Speed {car_short} Circuit Challenge!",
            f"LIGHTNING FAST! ⚡ {car_short} Grand Rally for Kids!",
            f"GOLDEN TROPHY! 🌟 Best {car_short} Racing Adventure!",
            f"{car_short} ON TRACK! 🏁 Ultimate Speed Cup!"
        ]
        default_thumb_text = "TURBO SPEED! ⚡"
        text_options = ["TURBO SPEED! ⚡", "WHO WILL WIN?! 🏁", "SUPER FAST! 🏎️", "GOLD TROPHY! 🏆", "GO GO GO! 🚀"]
    else:
        if image_context and image_context.get("product_name"):
            clean_p = re.sub(r'[^a-zA-Z0-9\s]', '', image_context.get("product_name", "")).strip().upper()
            if len(clean_p) > 3 and len(clean_p) <= 22:
                car_short = clean_p
            else:
                car_short = "HERO TOY CAR"
        else:
            car_short = "HERO TOY CAR"
        theme_tag = "ToyStory"
        viral_titles = [
            f"VROOM VROOM! 🚗💨 {car_short} Grand Playroom Adventure for Kids!",
            f"CAN WE COMPLETE THE MISSION? 🌟 {car_short} Obstacle Challenge!",
            f"SUPER FUN TOY ADVENTURE! ✨ {car_short} Action-Packed Play!",
            f"AMAZING JOURNEY! 🏆 Best {car_short} Tale for Children!",
            f"{car_short} ON THE MOVE! 🚀 High-Energy Fun!"
        ]
        default_thumb_text = "VROOM VROOM! 🚗"
        text_options = ["VROOM VROOM! 🚗", "LET'S GO! 🚀", "SUPER HERO! 🌟", "MISSION WIN! 🏆", "CAN WE DO IT?! ⚡"]

    primary_title = viral_titles[0]

    # Clean thumbnail text for rendering on image
    active_text = thumbnail_text or default_thumb_text
    clean_text = re.sub(r'[^\w\s\?!°#\-]', '', active_text).strip()
    if not clean_text:
        clean_text = default_thumb_text

    # Chapter Timestamps calculation
    chapters = []
    total_scenes = len(scenes)
    if total_scenes > 0:
        if total_scenes <= 20:
            chapter_indices = [
                (0, "🏁 Starting Line & High-Energy Engine Rev"),
                (min(2, total_scenes - 1), "🚀 Launch Down the High-Speed Ramp"),
                (min(5, total_scenes - 1), "✨ 360° Airborne Stunt Jump"),
                (min(8, total_scenes - 1), "🌈 Glowing Rainbow Tunnel Adventure"),
                (min(10, total_scenes - 1), "🔥 Bumpy Kinetic Sand Mountain & Suspension Bridge"),
                (min(12, total_scenes - 1), "🔄 The Giant 360-Degree Vertical Loop"),
                (min(14, total_scenes - 1), "💦 Water Splash Zone & Domino Slalom"),
                (min(16, total_scenes - 1), "⚡ Grand Duel & Mega Ramp Apex Leap"),
                (min(18, total_scenes - 1), "🏆 Victory Finish Line & Trophy Celebration"),
                (total_scenes - 1, "👋 Heartfelt Movie Farewell (Penutup)!")
            ]
        else:
            chapter_indices = [
                (0, "🏁 Starting Line & High-Energy Engine Rev"),
                (min(5, total_scenes - 1), "🚀 Launch Down the High-Speed Ramp"),
                (min(15, total_scenes - 1), "🔄 The Giant 360-Degree Loop Challenge"),
                (min(25, total_scenes - 1), "🌉 Narrow Wooden Suspension Bridge Crossing"),
                (min(35, total_scenes - 1), "🌪️ The Whirlwind Spiral Tower Ascent"),
                (min(45, total_scenes - 1), "🔥 Bumpy Kinetic Sand Mountain Climb"),
                (min(54, total_scenes - 1), "⚡ Ultimate Airborne Mega Ramp Jump"),
                (total_scenes - 1, "🏆 Grand Finish Line Celebration & Confetti!")
            ]
        seen_idx = set()
        for idx, label in chapter_indices:
            if idx not in seen_idx and idx < total_scenes:
                seen_idx.add(idx)
                s = scenes[idx]
                time_str = s.get("time_range", "").split(" - ")[0] if " - " in s.get("time_range", "") else format_timestamp(s.get("start_time", 0))
                chapters.append(f"{time_str} {label}")

    chapters_text = "\n".join(chapters) if chapters else "00:00 🏁 Starting Line & Grand Race\n05:00 🚀 Mega Stunt Jump\n09:30 🏆 Victory Celebration!"

    # SEO Description (Structured for high retention and watch time)
    description = (
        f"🌟 {primary_title}\n\n"
        f"In today's exciting toy adventure, join our little driver and the incredible {car_name} on an action-packed journey through {arena_name}! "
        f"Steered by a {child_name}, watch as our hero speeds through fun obstacles, navigates tricky challenges, and completes the grand mission!\n\n"
        f"Every scene is filled with cheerful sound effects, continuous spoken English voiceover, and nonstop high-energy fun "
        f"designed to inspire playful imagination for toddlers, preschoolers, and kids worldwide!\n\n"
        f"⏱️ VIDEO CHAPTERS / TIMESTAMPS:\n"
        f"{chapters_text}\n\n"
        f"✨ WHAT MAKES THIS VIDEO AWESOME:\n"
        f"• Full 10-second continuous English narrative without dead air or pauses!\n"
        f"• 100% consistent toy vehicle and character continuity throughout all 20 scenes!\n"
        f"• Vibrant 3D CGI stylized animation with rich colorful visual details!\n"
        f"• Wholesome, safe, and family-friendly entertainment for children.\n\n"
        f"👍 If you enjoyed this toy adventure, please smash the LIKE button, SHARE with your best friends, and SUBSCRIBE for daily cartoon adventures!\n"
        f"🔔 Turn on notifications so you never miss our next exciting video!\n"
        f"💬 QUESTION OF THE DAY: What was your favorite scene in today's story? Let us know in the comments below! 👇\n\n"
        f"#KidsVideo #{car_short.replace(' ', '')} #{theme_tag} #ToyCars #3DAnimation #KidsStory #FamilyFun #ToddlerFun"
    )

    tags = [
        f"{car_short.lower()}",
        f"{car_short.lower()} toy",
        f"{car_short.lower()} for kids",
        "kids toy car video",
        "toy car story",
        "3d cartoon animation",
        "preschool learning",
        "car cartoon for toddlers",
        "fun kids adventure",
        "sound effects for kids",
        "toy car adventure",
        "educational toy video",
        "stunt toy car",
        "cheerful toddler fun",
        "family friendly video",
        "kids story in english",
        "preschool adventure"
    ]

    hashtags = [
        "#KidsVideo",
        f"#{car_short.replace(' ', '')}",
        f"#{theme_tag}",
        "#ToyCars",
        "#3DAnimation",
        "#KidsStory",
        "#StoryForKids",
        "#FamilyFun"
    ]

    primary_thumbnail_prompt = (
        f"A hyper-viral, high-CTR YouTube video thumbnail in ultra-vivid, premium 3D CGI stylized animation aesthetic, 16:9 widescreen format (1280x720). "
        f"Embedded 3D Thumbnail Text: Bold, punchy 3D extruded cartoon typography prominently rendered across the top reading exactly \"{clean_text}\" in glowing sunny yellow gradient letters with thick comic black outlines, vibrant red drop shadows, and sparkling speed starbursts. "
        f"Hero Action Subject: The primary {car_name} powers through the action scene directly toward the camera lens with dynamic 3D pop-out effect, "
        f"front tires angled sharply, deep rubber treads in ultra-crisp 8K detail, ultra-glossy reflective finish with vibrant decals, and bright glowing rounded headlights. "
        f"Expressive Character Anchor: In the upper-right background, a {child_name} with huge sparkling joyful eyes, open-mouthed expression of sheer wonder, and both hands raised high in cheerful triumph. "
        f"Adventure Environment: Behind the vehicle, {arena_name} filled with vibrant cheerful scenic props and colorful details. "
        f"Lighting & Special Effects: Warm golden daylight sunlight with volumetric rays, colorful flying cartoon confetti and speed stars, dynamic motion blur on the background to emphasize motion while the vehicle and text remain razor-sharp 8K crisp focus. "
        f"Color Palette: Saturated neon orange, electric cyan blue, candy apple red, and sunshine yellow with cinematic high contrast. "
        f"Composition: Designed specifically for YouTube thumbnail algorithms: eye-catching from small mobile screens, crystal clear legible 3D title text \"{clean_text}\", zero dark muddy tones, wholesome, ultra-appealing and captivating for kids and parents."
    )

    closeup_thumbnail_prompt = (
        f"A viral kids YouTube thumbnail in premium 3D CGI stylized animation style, 16:9 widescreen ratio (1280x720). "
        f"Embedded 3D Thumbnail Text: Huge, expressive 3D embossed comic text situated at the top reading \"{clean_text}\" in glossy electric cyan and orange gradient with thick white borders and shiny cartoon reflections. "
        f"Macro eye-level portrait of a {child_name} beaming proudly with an ecstatic happy smile, holding the gleaming {car_name} right in front of the camera lens so the bumper and wheels appear huge and tactile. "
        f"The toy vehicle features pristine glossy paint, rounded friendly headlights casting warm cartoon light, and rugged tires. "
        f"The background reveals {arena_name} with warm natural daylight and soft pastel bokeh. "
        f"Ultra-saturated cheerful colors, crystal clear 8K resolution, cinematic studio lighting, high emotional connection, perfect for YouTube Kids CTR."
    )

    composition_tips = (
        "💡 Tips Promt Gemini / Imagen: Gunakan aspek rasio 16:9 (1280x720) saat generate di Google Gemini / Imagen 3 agar pas menjadi thumbnail YouTube.\n"
        f"🎯 Karakteristik Thumbnail FYP: Teks 3D tebal ('{clean_text}') di bagian atas + sudut kamera rendah (low-angle) dengan mobil mengarah ke penonton (3D pop-out effect) + ekspresi wajah anak kagum/gembira + warna neon kontras tinggi terbukti menghasilkan CTR di atas 15% pada algoritma YouTube Kids."
    )

    return {
        "viral_titles": viral_titles,
        "primary_title": primary_title,
        "description": description,
        "tags": tags,
        "hashtags": hashtags,
        "thumbnail_prompt": primary_thumbnail_prompt,
        "thumbnail_alt_prompt": closeup_thumbnail_prompt,
        "thumbnail_text": clean_text,
        "thumbnail_text_options": text_options,
        "thumbnail_composition_tips": composition_tips
    }
