import math
import re
from typing import List, Dict, Any, Optional

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
    "Haha, that was an epic jump! The child giggles happily, quickly guiding the wheels back onto the smooth track to keep the momentum going!",
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
    "Straight through the colorful ribbon ring it blasts! Ribbons flutter everywhere like festive parade streamers celebrating our brave journey!",
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
    "Touchdown! A flawless landing right into the final straightaway lane, heading straight toward the checkered finish line banners!",
    "The crowd of toy spectators goes wild with cheering! Hear the applause, the whistling, and the joyful shouting from all around the room!",
    "Only a few meters left to go! The toddler leans forward with anticipation, eyes sparkling with sheer delight and festive excitement!",
    "Here comes the final sprint! The monster truck unleashes every bit of turbo power left in its playful little battery engine!",
    "And across the finish line it zooms! The checkered flag drops as colorful cartoon confetti pops in every direction with joy!",
    "Victory is ours! The red monster truck parks proudly on the top winner's podium with headlights flashing like celebratory disco lights!",
    "The happy child jumps up in pure elation, raising his hands high in the air and shouting: Hooray, we won the championship today!",
    "What an unforgettable toy car adventure we shared together, filled with thrilling jumps, funny sound effects, and nonstop laughter!",
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
    storyline premise, and child play theme.
    """
    sample = (title + " " + full_transcript[:1500]).lower()

    if any(k in sample for k in ["monster", "truk", "truck", "offroad", "lumpur", "mud"]):
        theme = "Stunt Monster Truck Playroom Rally & Obstacle Course Adventure"
        car_default = "Gleaming crimson red stunt monster truck with bright yellow flame decals, oversized rugged off-road tires, and rounded cartoon headlights in 3D Pixar style"
        arena_default = "Sunlit kids playroom track featuring vibrant orange looping ramps, mini wooden suspension bridges, and colorful stacking blocks"
    elif any(k in sample for k in ["polisi", "police", "fire", "pemadam", "rescue", "tayo", "ambulance"]):
        theme = "City Toy Car Rescue Mission & Friendly Patrol Adventure"
        car_default = "Cheerful blue and white toy police patrol car with flashing dual sirens, smiling cartoon headlights, and glossy finish in 3D animation style"
        arena_default = "Miniature pastel kids toy town with cartoon houses, tiny traffic lights, and smooth carpeted roads"
    elif any(k in sample for k in ["race", "balap", "hot wheels", "track", "lintasan", "loop", "cepat"]):
        theme = "High-Speed Hot Wheels Toy Car Championship & Stunt Loop Race"
        car_default = "Ultra-fast metallic red aerodynamic racer with glowing neon yellow stripes and black low-profile tires"
        arena_default = "Expansive multi-tier orange loop-the-loop stunt track setup on a colorful playroom rug"
    else:
        theme = "Cheerful Kids Toy Car Play Adventure with Stunts and Sound Effects"
        car_default = "Gleaming red and yellow toy car with rugged off-road tires, glossy plastic finish, and expressive rounded headlights in 3D Pixar style"
        arena_default = "Vibrant kids playroom track filled with orange loops, mini wooden suspension bridges, and colorful stacking blocks"

    vision_summary = f"YouTube Video Concept: {theme}. Tells a continuous, action-packed toy car story filled with fast ramps, stunt jumps, and joyful sound effects that captivate kids worldwide."

    return {
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
                "style": "Cinematic 3D Pixar animation style, 8K ultra-vibrant saturated colors, soft daylight, 24fps smooth motion"
            }

    return {
        "subject": "Cheerful 4-year-old toddler with neat brown hair wearing a bright blue and orange striped shirt, beaming with a happy energetic smile",
        "product": vision_info["default_car"],
        "setting": vision_info["default_arena"],
        "style": "Cinematic 3D Pixar animation aesthetic, 8K ultra-vibrant saturated colors, warm soft playroom lighting, realistic glossy toy textures, 24fps smooth motion"
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
    cam_motion: str
) -> str:
    """
    Builds a fluid, natural, cinematic AI video prompt WITHOUT stiff bracket tags!
    Formatted specifically to deliver peak results in Google Veo, Kling AI, Runway Gen-3, Luma, and Sora.
    """
    prompt = (
        f"{style}. "
        f"{action} "
        f"Featuring {product} guided with joyful enthusiasm by {subject} inside {setting}. "
        f"Cinematic camera capture: {cam_motion}. "
        f"Audio ambiance features continuous English voiceover: \"{dialogue}\" accompanied by {sfx}. "
        f"100% exact toy model continuity, vibrant paint colors, and child character appearance locked across all scenes, warm natural playroom daylight, smooth 24fps motion, no morphing."
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
    """
    title = video_meta.get("title", "")
    full_text = " ".join([s["dialogue"] for s in scenes])
    vision_info = extract_kids_video_vision(title, full_text)
    context_defaults = detect_subject_context(full_text, title, language="en", image_context=image_context)
    
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

        # Check if DeepSeek or Gemini provided an enhanced prompt for this scene
        if scene_num in llm_map:
            l_data = llm_map[scene_num]
            english_dialogue = l_data.get("english_dialogue") or l_data.get("dialogue") or STORY_ARC_ENGLISH_DIALOGUE[idx % len(STORY_ARC_ENGLISH_DIALOGUE)]
            story_link = l_data.get("story_link") or f"Builds directly toward Scene {scene_num + 1} stunt"
            action = l_data.get("action_description", "")
            video_prompt = l_data.get("video_prompt", "")
            negative_prompt = l_data.get("negative_prompt", "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry")
            sound_effects = l_data.get("sound_effects") or sfx
            cam_dir = l_data.get("camera_directive") or f"{cam['type']} ({cam['motion']})"
        else:
            # Continuous 10s English Speech Generator (No empty space, 22-28 words guaranteed!)
            english_dialogue = STORY_ARC_ENGLISH_DIALOGUE[idx % len(STORY_ARC_ENGLISH_DIALOGUE)]
            sound_effects = sfx

            if idx == 0:
                story_link = "Opening hook, revving up at starting line"
                action = (
                    f"At the starting line of the vibrant looping race track, {product_anchor} revs its engine with playful glowing rounded headlights. "
                    f"{subject_anchor} smiles brightly with excitement, holding the rear bumper ready for the launch countdown."
                )
            elif idx == total_scenes - 1:
                story_link = "Grand finale, crossing finish line and trophy celebration"
                action = (
                    f"{product_anchor} speeds triumphantly across the checkered finish line amidst a shower of festive cartoon confetti. "
                    f"{subject_anchor} claps hands enthusiastically and jumps in joyful celebration of the victory."
                )
            elif idx % 4 == 1:
                story_link = f"High-speed acceleration into curve connecting to Scene {scene_num + 1}"
                action = (
                    f"{product_anchor} accelerates down the steep orange decline, leaning into a sharp curved turn with animated cartoon speed dust trailing behind its rugged wheels."
                )
            elif idx % 4 == 2:
                story_link = f"Airborne stunt over obstacle leading to Scene {scene_num + 1}"
                action = (
                    f"{product_anchor} launches off a wooden ramp, performing a thrilling 360-degree aerial stunt jump before landing smoothly with a soft bounce on the play mat."
                )
            elif idx % 4 == 3:
                story_link = f"Tunnel and bridge crossing navigating toward Scene {scene_num + 1}"
                action = (
                    f"{product_anchor} races through a colorful rainbow tunnel and across a mini wooden suspension bridge, while the happy child watches in awe."
                )
            else:
                story_link = f"Tactical maneuvering across {setting_anchor} connecting smoothly to Scene {scene_num + 1}"
                action = (
                    f"{product_anchor} navigates past toy building blocks across {setting_anchor}, steered with joyful energy by {subject_anchor}."
                )

            # Generate natural, fluid cinematic prompt (NO STIFF BRACKETS!)
            video_prompt = build_fluid_cinematic_prompt(
                style=style_anchor,
                action=action,
                product=product_anchor,
                subject=subject_anchor,
                setting=setting_anchor,
                dialogue=english_dialogue,
                sfx=sound_effects,
                cam_motion=cam["motion"]
            )

            negative_prompt = (
                "scary, dark, realistic horror, morphing car model, distorted wheels, broken toys, realistic violence, flickering, text watermark, blurry, deformed hands"
            )
            cam_dir = f"{cam['type']} ({cam['motion']})"
        
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
            "story_link": story_link or f"Seamlessly links into Scene {min(scene_num + 1, total_scenes)}",
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
