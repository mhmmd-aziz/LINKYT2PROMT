from typing import List, Dict, Any

"""
20 & 60 Unique Cinematic Story Episodes for Kids YouTube Video Remake.
Organized into 8 Progressive Acts with:
- 100% Unique Physical Stunts and Actions per Scene (No Repetition!)
- Full 10-Second Continuous Spoken English Dialogue (22-28 words guaranteed, no dead air!)
- Scene-Specific Contextual Sound Effects (SFX) matched 1:1 to the action
- Movie-Grade Cinematic Visual Effects (VFX)
- Narrative Story Link connecting every scene sequentially
- Grand Climax & Warm Heartfelt Movie Ending (Penutup) in the Final Scene
"""

# Dedicated 20-Scene Cohesive Cinematic Story Arc for Kids YouTube Video Remake (~3.3 Minutes)
CINEMATIC_20_SCENE_ARC = [
    # --- ACT 1: THE GRAND COUNTDOWN & SPEED LAUNCH (SCENES 1-5) ---
    {
        "scene_index": 1,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Starting Grid & Countdown Rev",
        "action": "At the starting line of {setting}, {product} revs its engine with playful glowing rounded headlights, while {subject} holds the rear bumper eagerly ready for the launch countdown.",
        "dialogue": "Welcome friends to the greatest toy car rally ever! Look at our incredible {product_short} revving its engine at the starting gate! Let us count down together: three, two, one!",
        "sfx": "[SFX: High-RPM engine throttle revs 'vroom-vroom!', digital countdown beeps 'beep-beep-BEEP!', eager toddler cheer 'Let us go!']",
        "vfx": "Subtle heat haze shimmering above exhaust, warm morning playroom sunbeams, animated cartoon tachometer needle dancing",
        "story_link": "High-energy countdown building anticipation toward the opening drop",
        "is_closing": False
    },
    {
        "scene_index": 2,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Steep Ramp Launch Acceleration",
        "action": "{product} rockets down the steep orange decline at blistering speed, tires spinning with smoke puffs as {subject} cheers enthusiastically from the sideline.",
        "dialogue": "Green light! Off it rockets down the steep orange hill at lightning speed! Hold on tight, friends, this race is going to be super fast and exciting!",
        "sfx": "[SFX: Rubber tires screeching 'skrrrt!', sudden whoosh of acceleration, energetic drum beat, child laughing loudly]",
        "vfx": "Dynamic motion blur trailing behind wheels, white cartoon speed lines, soft carpet dust dispersion",
        "story_link": "High velocity descent setting up the first high-speed curve",
        "is_closing": False
    },
    {
        "scene_index": 3,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Hairpin Cone Drift",
        "action": "{product} drifts smoothly around bright miniature traffic cones, tires gripping the track edge with animated cartoon sparks dancing off the outer rail.",
        "dialogue": "Here comes the first sharp hairpin curve! Look at how smoothly our {product_short} drifts past the miniature cones without touching a single one, pure racing skill!",
        "sfx": "[SFX: Lateral tire squeal 'squeeeak!', rhythmic engine acceleration, playful horn honk 'beep beep!']",
        "vfx": "Sparks dancing along outer track rail, sweeping camera pan blur, reflective gloss shine on vehicle hood",
        "story_link": "Flawless curve exit leading into straightaway speed lane",
        "is_closing": False
    },
    {
        "scene_index": 4,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Straightaway Power Slide",
        "action": "{product} power-slides onto the open straightaway towards the toy city boulevard, glossy body panels sparkling under playroom daylight as {subject} guides the wheels.",
        "dialogue": "Straightening out with pure style and power! The shiny paint sparkles under the playroom lights as the toddler guides the wheels with joyful precision and confidence!",
        "sfx": "[SFX: Deep engine purr, rapid tire rotation sound, joyful toddler giggles, cheerful playful soundtrack]",
        "vfx": "Lens flare glint off front bumper, crisp 8K macro focus on spinning rim spokes, ambient room depth of field",
        "story_link": "Momentum carries the vehicle directly toward the neon speed sensor",
        "is_closing": False
    },
    {
        "scene_index": 5,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Neon Speed Gate Breach",
        "action": "{product} blasts through the glowing neon speed sensor arch, triggering cheerful flashing LED rainbow lights that illuminate {setting}.",
        "dialogue": "Blasting right through the neon speed gate! The sensors flash with cheerful colors as we hit top racing speed heading for the stunt obstacle arena right now!",
        "sfx": "[SFX: Digital chime 'ding-ding-ding!', turbo exhaust pop 'bam!', energetic child shout 'Super fast!']",
        "vfx": "Neon light streak reflection on vehicle body, colorful digital HUD speed rings expanding outward",
        "story_link": "Entering the aerial stunt ramp sector with maximum velocity",
        "is_closing": False
    },

    # --- ACT 2: THE AERIAL STUNT & BLOCK GAUNTLET (SCENES 6-8) ---
    {
        "scene_index": 6,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Airborne 360 Stunt Leap",
        "action": "{product} launches off the wooden ramp into mid-air, performing a breathtaking 360-degree aerial stunt jump soaring high above a colorful stack of rainbow building blocks.",
        "dialogue": "Up into the sky it launches! Look at that breathtaking aerial flight high over the towering stack of colorful rainbow blocks, defying gravity with pure magic!",
        "sfx": "[SFX: Suspension spring release 'BOING!', wind rush 'WHOOOOSH!', slow-motion heartbeat thud, child shouting 'Look at that!']",
        "vfx": "Slow-motion apex freeze at maximum height, rainbow block colors reflecting on undercarriage, floating dust motes",
        "story_link": "Gliding gracefully down toward the soft blue landing cushion",
        "is_closing": False
    },
    {
        "scene_index": 7,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Four-Wheel Cushion Landing",
        "action": "{product} makes a flawless four-wheel touchdown on the blue foam landing mat, rugged shock absorbers flexing smoothly with a gentle bounce.",
        "dialogue": "Touchdown! What a flawless four-wheel landing on the soft bounce mat! The shock absorbers flex gently and bounce right back into the race without stopping!",
        "sfx": "[SFX: Soft rubber thud 'THUMP!', suspension bounce squeak, triumphant child cheer 'Woohoo!', clapping hands]",
        "vfx": "Puff of cushion compression dust, dynamic camera shake on impact, restored 24fps motion velocity",
        "story_link": "Rolling off the mat into the building block slalom gauntlet",
        "is_closing": False
    },
    {
        "scene_index": 8,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Block Slalom Maneuver",
        "action": "{product} weaves swiftly left and right between towering pastel wooden blocks, tires kicking up imaginary cartoon dust plumes as {subject} steers eagerly.",
        "dialogue": "Left swerve, right swerve! Precision steering in action as our brave racer zips past the tall wooden towers without knocking down a single colorful piece!",
        "sfx": "[SFX: Rapid steering tire squeaks, light wooden clack resonance, toddler laughing 'Haha, made it!']",
        "vfx": "Lateral camera whip pan, stylized cartoon wind streaks behind spoiler, dynamic tilt angle",
        "story_link": "Exiting the block gauntlet directly toward the rainbow tunnel entrance",
        "is_closing": False
    },

    # --- ACT 3: THE RAINBOW TUNNEL & TRANSITION (SCENES 9-10) ---
    {
        "scene_index": 9,
        "act": "Act 3: The Rainbow Tunnel & Transition",
        "milestone": "Rainbow Tunnel Entry",
        "action": "{product} speeds into the arched entrance of the glowing rainbow tunnel, headlights illuminating the vibrant curved translucent walls with playful reflections.",
        "dialogue": "Into the magical rainbow tunnel we go! The headlights glow brightly as glowing neon colors swirl all around us, making the whole room echo with cheerful racing sounds!",
        "sfx": "[SFX: Tunnel echo reverb whoosh, humming neon LED buzz, happy horn honk 'beep-beep!']",
        "vfx": "Psychedelic rainbow light refractions dancing across car roof, atmospheric volumetric glow",
        "story_link": "Racing through the glowing subterranean section toward the sunlight exit",
        "is_closing": False
    },
    {
        "scene_index": 10,
        "act": "Act 3: The Rainbow Tunnel & Transition",
        "milestone": "Sunlight Tunnel Exit Burst",
        "action": "{product} bursts out from the tunnel portal back into the bright sunlit playroom, glossy paint sparkling as {subject} claps hands enthusiastically.",
        "dialogue": "Bursting back out into the bright sunshine at top speed! The shiny red body sparkles brilliantly under the cozy sunlit room as the little wheels roll on!",
        "sfx": "[SFX: Echo fades into crisp daylight acoustic, rapid engine throttle rev, cheerful child giggle]",
        "vfx": "Blinding lens flare bloom on tunnel exit, lens sparkle starbursts, restored vivid daylight color palette",
        "story_link": "Entering the rugged terrain obstacle zone ahead",
        "is_closing": False
    },

    # --- ACT 4: RUGGED OBSTACLE CHALLENGE (SCENES 11-12) ---
    {
        "scene_index": 11,
        "act": "Act 4: The Rugged Obstacle Challenge",
        "milestone": "Kinetic Sand Mountain Climb",
        "action": "{product} attacks the steep purple kinetic sand mountain, oversized off-road tire treads digging firmly into the textured sand as engine hums with power.",
        "dialogue": "Uh-oh, a bumpy purple sand mountain stands in our way! Watch those rugged oversized tires dig deep into the soft sand, climbing up inch by inch!",
        "sfx": "[SFX: Deep low-frequency engine chug, kinetic sand crunch 'shhhk-crunch!', determined toddler grunt 'Go, go, go!']",
        "vfx": "Particles of kinetic sand spraying from rear wheels, macro close-up depth of field on rubber treads",
        "story_link": "Reaching the summit and rolling onto the suspension bridge",
        "is_closing": False
    },
    {
        "scene_index": 12,
        "act": "Act 4: The Rugged Obstacle Challenge",
        "milestone": "Suspension Bridge Crossing",
        "action": "{product} drives carefully across the swaying wooden suspension bridge, planks clattering rhythmically as {subject} stabilizes the guide rail with gentle fingers.",
        "dialogue": "Careful now across the wooden suspension bridge! The planks rattle with a friendly click-clack sound under the sturdy rubber wheels as the toddler guides with patience!",
        "sfx": "[SFX: Wooden plank rhythmic clatter 'clack-clack-clack!', bridge rope creak, proud child whisper 'Almost across!']",
        "vfx": "Gentle rope bridge sway physics, soft wooden splinters and warm shadows beneath planks",
        "story_link": "Crossing to the opposite ledge heading toward the 360 loop",
        "is_closing": False
    },

    # --- ACT 5: THE STUNT HEIGHTS & MEGA LOOP (SCENES 13-14) ---
    {
        "scene_index": 13,
        "act": "Act 5: The Stunt Heights & Mega Loop",
        "milestone": "Vertical 360 Loop Upside-Down",
        "action": "{product} rockets upside-down through the top arch of a giant 360-degree vertical loop, child in background watching upside down with huge smiling eyes.",
        "dialogue": "Upside down it goes right through the giant looping track! Defying gravity with pure style and coming out perfectly on the other side with a huge champion smile!",
        "sfx": "[SFX: Centrifugal loop whoosh 'VRRRRR-SWOOSH!', engine crescendo, child gasping in delight 'Woooow!']",
        "vfx": "Circular motion blur following track contour, dynamic camera roll matching car inversion, speed lines",
        "story_link": "Momentum shoots car out of loop into the base of the spiral tower",
        "is_closing": False
    },
    {
        "scene_index": 14,
        "act": "Act 5: The Stunt Heights & Mega Loop",
        "milestone": "Spiral Staircase Tower Climb",
        "action": "{product} banks into the upward spiral tower, circling continuously around the colorful helix track as camera tracks from overhead in a bird's-eye sweep.",
        "dialogue": "Round and round up the dizzying spiral tower track! Climbing higher and higher toward the playroom ceiling as the little engine sings with pure energetic power!",
        "sfx": "[SFX: Rhythmic looping engine pitch climbing higher, playful carnival chime, toddler giggling]",
        "vfx": "Rotating overhead bird's-eye camera shot, spiral blur on outer rails, soft ambient room reflections",
        "story_link": "Reaching top balcony ready for the descent hazard zone",
        "is_closing": False
    },

    # --- ACT 6: HAZARDS & PRECISION SLALOM (SCENES 15-16) ---
    {
        "scene_index": 15,
        "act": "Act 6: Hazards & Precision Slalom",
        "milestone": "Water Splash Hazard Puddle",
        "action": "{product} splashes through a miniature blue water pool zone on the playroom floor, sending crystal droplets and blue plastic balls scattering cheerfully.",
        "dialogue": "Splash! Right through the sunny water splash puddle! Watch the sparkling droplets fly as our waterproof champion keeps rolling forward with unstoppable energy and bright happy spirit!",
        "sfx": "[SFX: Water splash 'SPLAAASH!', wet tire spin squeak, child laughing out loud 'Haha, so wet!']",
        "vfx": "Slow-motion water droplet spray glistening in sunlight, water ripples reflecting playroom lamps",
        "story_link": "Tires dry instantly on the rug heading straight into the standing dominoes",
        "is_closing": False
    },
    {
        "scene_index": 16,
        "act": "Act 6: Hazards & Precision Slalom",
        "milestone": "Standing Domino Maze Slalom",
        "action": "{product} weaves with masterclass precision through hundreds of upright rainbow domino tiles, grazing millimeters past them without toppling a single piece.",
        "dialogue": "Incredible precision driving through the domino maze! Swerving left and right with millimeter accuracy without toppling even one colorful domino, absolute masterclass driving skill!",
        "sfx": "[SFX: Gentle domino tile tap 'tick!', nimble tire drift, tense child intake of breath, then joyful gasp]",
        "vfx": "Ultra-shallow depth of field highlighting domino line foreground, crisp focus on razor-thin clearances",
        "story_link": "Clearing the last domino into the championship sprint lane",
        "is_closing": False
    },

    # --- ACT 7: THE GRAND DUEL & APEX STUNT (SCENES 17-18) ---
    {
        "scene_index": 17,
        "act": "Act 7: The Grand Climax & Apex Stunt",
        "milestone": "Side-by-Side Rival Duel Sprint",
        "action": "{product} races wheel-to-wheel alongside a rival miniature toy sports car, engines roaring in unison as {subject} watches with thrilling anticipation.",
        "dialogue": "It is a side-by-side sprint against the rival racer! Both cars are neck and neck, engines roaring at maximum speed as we approach the final mega ramp!",
        "sfx": "[SFX: Dual engine roar harmonize, wind shear, exciting uptempo percussion, child cheering 'Go red car, go!']",
        "vfx": "Split-frame dynamic speed lines, tire smoke puffs, synchronized motion blur across both vehicles",
        "story_link": "Our hero car hits turbo boost pulling ahead onto the ramp lip",
        "is_closing": False
    },
    {
        "scene_index": 18,
        "act": "Act 7: The Grand Climax & Apex Stunt",
        "milestone": "Mega Ramp Apex Leap",
        "action": "{product} blasts off the apex of the giant mega ramp, soaring high across the entire playroom with cartoon sparkles trailing wheels in majestic slow-motion.",
        "dialogue": "Full throttle off the mega ramp! Look at that unbelievable airborne stunt jump soaring through the sky in majestic slow-motion! The biggest jump in racing history!",
        "sfx": "[SFX: Mighty suspension spring pop, wind rush 'WHOOOOOOSH!', cinematic slow-mo bass drop, child screaming in delight]",
        "vfx": "Dramatic slow-motion apex freeze, golden volumetric sunbeams illuminating every glossy decal in 8K detail",
        "story_link": "Landing gracefully onto the finish line straightaway",
        "is_closing": False
    },

    # --- ACT 8: THE GRAND FINALE & MEMORABLE PENUTUP (SCENES 19-20) ---
    {
        "scene_index": 19,
        "act": "Act 8: The Grand Finale & Penutup",
        "milestone": "Victory Finish Line & Trophy",
        "action": "{product} crosses the checkered finish line amidst an explosion of rainbow confetti, parking proudly on the winner's podium as {subject} hoists the golden toy trophy.",
        "dialogue": "Across the finish line it zooms! The checkered flag drops and colorful confetti explodes everywhere as our champion takes first place on the winner's podium with the golden trophy!",
        "sfx": "[SFX: Checkered flag swoosh, confetti cannon pop 'POP-POP-POP!', victory fanfare trumpet, roaring child cheer 'We won!']",
        "vfx": "Thousands of glittering rainbow confetti particles drifting across screen, trophy lens flare starbursts",
        "story_link": "The warm final farewell and movie closing to viewers",
        "is_closing": False
    },
    {
        "scene_index": 20,
        "act": "Act 8: The Grand Finale & Penutup",
        "milestone": "PENUTUP: Heartfelt Movie Farewell",
        "action": "In a warm emotional close-up, {subject} holds {product} gently in two hands, looking straight into the camera lens with a loving smile and waving goodbye as the scene fades into a warm sunset glow.",
        "dialogue": "Thank you so much for joining our grand toy car adventure today, best friends! You are all champions! Keep playing, keep smiling, and see you next time! Bye-bye!",
        "sfx": "[SFX: Warm acoustic lullaby melody, child saying 'Bye-bye friends!', gentle horn beep 'beep-beep', closing applause]",
        "vfx": "Heartfelt close-up of child holding toy car and waving goodbye directly to camera, soft warm vignette fade, movie ending credits atmosphere",
        "story_link": "Grand movie ending (penutup), story complete",
        "is_closing": True
    }
]

# Dedicated 20-Scene Police Chase & Rescue Mission Arc
POLICE_CHASE_20_ARC = [
    {
        "scene_index": 1,
        "act": "Act 1: The Precinct Alarm",
        "milestone": "Station Alarm & Siren Activation",
        "action": "At the miniature police station garage inside {setting}, dual red and blue sirens burst to life atop {product} as {subject} presses the siren button.",
        "dialogue": "Emergency alert in Toy Town, best friends! Our super brave {product_short} switches on its flashing sirens! Let us rev the engine and roll out on patrol together!",
        "sfx": "[SFX: High-pitched mini police wail 'wee-woo-wee-woo!', engine ignition roar, toddler shout 'Police to the rescue!']",
        "vfx": "Flashing red and blue LED strobe reflections on shiny toy car body, volumetric garage dust beams",
        "story_link": "Speeding out of the precinct onto the main city boulevard",
        "is_closing": False
    },
    {
        "scene_index": 2,
        "act": "Act 1: The Precinct Alarm",
        "milestone": "Garage Door Acceleration",
        "action": "{product} rockets out of the police garage bay doors onto the smooth carpet boulevard, tires chirping with sudden acceleration.",
        "dialogue": "Rolling out at top speed! The garage doors swing wide open as the little police cruiser accelerates down the smooth road to protect our toy city!",
        "sfx": "[SFX: Tire rubber chirp, rapid acceleration whoosh, exciting drum march rhythm, child giggling excitedly]",
        "vfx": "Motion blur streaks on tires, animated cartoon smoke puffs from rear bumper",
        "story_link": "Heading into the busy city intersection following dispatch",
        "is_closing": False
    },
    {
        "scene_index": 3,
        "act": "Act 2: The High-Speed Pursuit",
        "milestone": "Boulevard Traffic Weave",
        "action": "{product} weaves nimbly around parked pastel toy buses and miniature traffic lights, blue sirens flashing as {subject} steers with sharp focus.",
        "dialogue": "Look at that skillful driving! Zipping smoothly past the parked toy buses without touching a single mirror! We are hot on the trail of the runaway car!",
        "sfx": "[SFX: Nimble steering squeaks, rapid dual sirens 'wee-woo!', child whispering 'Keep your eyes on the road!']",
        "vfx": "Sweeping camera pan blur, reflective store window reflections in 8K detail",
        "story_link": "Spotting the speeding suspect vehicle turning into the market lane",
        "is_closing": False
    },
    {
        "scene_index": 4,
        "act": "Act 2: The High-Speed Pursuit",
        "milestone": "Market Lane Power Drift",
        "action": "{product} executes a high-speed power drift around a colorful fruit stand made of building blocks, keeping tires perfectly balanced on the road.",
        "dialogue": "Sharp left drift around the fruit market! Not a single pretend apple gets bumped! Look at the control our little police hero has on the steering wheel!",
        "sfx": "[SFX: Lateral tire squeal 'skrrrrt!', cheerful horn honk 'beep-beep!', toddler laughing loudly]",
        "vfx": "Cartoon speed stars sparking from outer tires, dynamic low-angle tracking shot",
        "story_link": "The suspect turns into the narrow alleyway shortcut",
        "is_closing": False
    },
    {
        "scene_index": 5,
        "act": "Act 2: The High-Speed Pursuit",
        "milestone": "Narrow Alleyway Squeeze",
        "action": "{product} accelerates down the narrow alleyway between cardboard toy buildings, mirrors folding slightly as siren echoes loudly against walls.",
        "dialogue": "Through the narrow alleyway we zoom! The sirens echo with exciting energy as we close the distance inch by inch! You can do it, little cruiser!",
        "sfx": "[SFX: Hollow alleyway echo siren reverberation, turbo engine whir, child cheering 'Faster, faster!']",
        "vfx": "Dramatic shadows between buildings, blue and red strobe pulses lighting the alley walls",
        "story_link": "Emerging onto the open playground bridge approach",
        "is_closing": False
    },
    {
        "scene_index": 6,
        "act": "Act 3: The Bridge Roadblock",
        "milestone": "Suspension Bridge Sprint",
        "action": "{product} chases the runaway car across the wooden suspension bridge, wooden planks clattering rhythmically under the rugged tires.",
        "dialogue": "Across the wooden suspension bridge at full speed! Listen to the planks rattle under our wheels as the bridge sways gently in the exciting playground breeze!",
        "sfx": "[SFX: Wooden plank rhythmic clatter 'clack-clack-clack!', siren echo over water, toddler cheering]",
        "vfx": "Soft wooden plank vibrations, water reflections shimmering beneath the bridge",
        "story_link": "Reaching the city park on the other side of the bridge",
        "is_closing": False
    },
    {
        "scene_index": 7,
        "act": "Act 3: The Bridge Roadblock",
        "milestone": "Deploying the Roadblock Cones",
        "action": "{subject} places bright neon orange cones across the path ahead, while {product} angles aggressively to create an impenetrable roadblock.",
        "dialogue": "Quick thinking! We set up a row of bright orange cones ahead! The runway has nowhere left to go as our brave police car stands ready!",
        "sfx": "[SFX: Plastic cone tap 'thump-thump!', brakes hissing to a halt, child whisper 'Stop right there!']",
        "vfx": "Bright neon orange cones glowing under playroom lighting, sharp macro focus on front grille",
        "story_link": "The suspect tries to swerve toward the sandbox hill",
        "is_closing": False
    },
    {
        "scene_index": 8,
        "act": "Act 4: The Sand Hill Stunt",
        "milestone": "Kinetic Sand Hill Chase",
        "action": "{product} powers up the steep purple kinetic sand hill, all-wheel drive tires digging deep to maintain pursuit speed.",
        "dialogue": "He is trying to escape up the sandbox mountain! But our {product_short} has all-wheel drive power! Digging into the sand and climbing right behind him!",
        "sfx": "[SFX: Low torque engine grind, sand crunch 'shhhhk-crunch!', determined toddler grunt 'Go, go!']",
        "vfx": "Kinetic sand spraying from rear wheels, macro rim detail in 8K resolution",
        "story_link": "Reaching the crest of the hill overlooking the playground plaza",
        "is_closing": False
    },
    {
        "scene_index": 9,
        "act": "Act 4: The Sand Hill Stunt",
        "milestone": "Crest Jump Descent",
        "action": "{product} leaps off the sand hill crest in a controlled four-wheel jump, landing smoothly on the soft playroom mat below.",
        "dialogue": "Over the sand hill it flies! A smooth jump through the air and a perfect four-wheel landing on the mat! Now we are right on his bumper!",
        "sfx": "[SFX: Spring bounce 'BOING!', soft mat thud 'thump!', child shouting 'Woohoo!']",
        "vfx": "Slow-motion hangtime at apex, dust motes drifting in sunbeams, shock absorbers compressing",
        "story_link": "Cornering the runaway car inside the roundabout",
        "is_closing": False
    },
    {
        "scene_index": 10,
        "act": "Act 5: The Subway Underpass",
        "milestone": "Underpass Tunnel Rush",
        "action": "{product} darts into the curved arched tunnel beneath the playroom table, headlights cutting through the dark with warm golden beams.",
        "dialogue": "Into the dark underpass tunnel! The glowing headlights illuminate the way forward while the dual sirens bounce off the ceiling with incredible superhero energy!",
        "sfx": "[SFX: Deep tunnel cavern echo, rapid engine throttle rev, cheerful child giggle]",
        "vfx": "Volumetric headlight dust beams piercing shadows, glowing dashboard gauges",
        "story_link": "Exiting the tunnel into the city town square",
        "is_closing": False
    },
    {
        "scene_index": 11,
        "act": "Act 5: The Subway Underpass",
        "milestone": "Town Square Pincer Move",
        "action": "{product} sweeps in a tight semi-circle around the town square statue, cutting off the escape angle with tactical precision.",
        "dialogue": "Swinging around the town square fountain with lightning speed! We cut off the corner and block the exit path! Perfect police maneuvering in action!",
        "sfx": "[SFX: Lateral tire squeak, loudspeaker chirp 'chirp-chirp!', toddler shouting 'Got you!']",
        "vfx": "Circular tire dust arc on rug, dynamic camera boom sweep from above",
        "story_link": "Executing the gentle stop maneuver",
        "is_closing": False
    },
    {
        "scene_index": 12,
        "act": "Act 6: The Safe Cornering",
        "milestone": "Bumper-to-Bumper Block",
        "action": "{product} pulls gently in front of the runaway car, bumper-to-bumper, bringing both vehicles safely to a complete halt.",
        "dialogue": "And stop! Safe and sound without a single scratch! The runaway car comes to a gentle halt right against our sturdy police bumper! Mission accomplished!",
        "sfx": "[SFX: Gentle plastic bumper tap 'clack!', brakes squeak, victorious child cheer 'Hooray, we did it!']",
        "vfx": "Headlights flashing playfully in synchronization, soft camera dolly in",
        "story_link": "The toy citizens and animals gather to celebrate",
        "is_closing": False
    },
    {
        "scene_index": 13,
        "act": "Act 6: The Safe Cornering",
        "milestone": "Officer High-Five",
        "action": "{subject} steps into frame, smiling from ear to ear, giving a proud high-five to the front bumper of {product}.",
        "dialogue": "Give me a high-five, partner! Our proud little officer smiles brightly, celebrating the safest and most exciting police rescue mission in toy city history!",
        "sfx": "[SFX: Crisp hand clap high-five 'SLAP!', joyful toddler laughter, playful horn honk]",
        "vfx": "Warm sunlight framing the child's smiling face, golden bokeh in background",
        "story_link": "Leading the peaceful escort back to precinct",
        "is_closing": False
    },
    {
        "scene_index": 14,
        "act": "Act 7: The Victory Parade",
        "milestone": "Escort Convoy Roll",
        "action": "{product} leads a friendly convoy of toy vehicles down the boulevard, headlights winking cheerfully like festive holiday lights.",
        "dialogue": "Now leading the friendly escort parade down the main street! All the toy animal spectators are waving their paws and cheering for our hero car!",
        "sfx": "[SFX: Cheerful parade brass melody, friendly siren chirps, crowd of toys applauding]",
        "vfx": "Colorful parade balloons floating in background, lens flare glint off police badge decal",
        "story_link": "Arriving at the city hall podium for the award",
        "is_closing": False
    },
    {
        "scene_index": 15,
        "act": "Act 7: The Victory Parade",
        "milestone": "City Hall Podium Arrival",
        "action": "{product} parks proudly atop the steps of the toy city hall, while {subject} places a shiny gold star medal on the roof.",
        "dialogue": "Here we are at city hall! Our brave cruiser earns the gold star medal of bravery! Look at how proudly the shiny star sparkles in the sunlight!",
        "sfx": "[SFX: Medal clink 'ting!', triumphant fanfare flourish, child giggling with pride]",
        "vfx": "Gold medal starburst glint, crystal clear 8K macro focus on polished police paint",
        "story_link": "The celebratory confetti explosion begins",
        "is_closing": False
    },
    {
        "scene_index": 16,
        "act": "Act 7: The Victory Parade",
        "milestone": "Rainbow Confetti Burst",
        "action": "A shower of festive rainbow confetti bursts into the air above {product}, drifting down like celebratory snowflakes across {setting}.",
        "dialogue": "Pop, pop, pop! A giant explosion of colorful confetti rains down from above celebrating our victory! What an incredible day of heroic teamwork and fun!",
        "sfx": "[SFX: Confetti popper 'POP-POP-POP!', paper flutter rustle, toddler joyful cheering]",
        "vfx": "Thousands of colorful confetti flakes floating in slow-motion, warm golden lighting",
        "story_link": "Switching sirens into celebratory disco rhythm",
        "is_closing": False
    },
    {
        "scene_index": 17,
        "act": "Act 8: The Grand Celebration & Penutup",
        "milestone": "Disco Siren Dance",
        "action": "{product} wiggles playfully on its tires while sirens flash rhythmically like disco lights, child dancing alongside happily.",
        "dialogue": "Look at the police car dancing! It wiggles its tires to the happy music while the sirens flash like a cheerful disco party for all our friends!",
        "sfx": "[SFX: Upbeat cartoon disco rhythm, rhythmic siren beeps, child giggling and dancing]",
        "vfx": "Animated cartoon musical notes floating above car, colorful neon light floor glow",
        "story_link": "Gathering around for the final group photo",
        "is_closing": False
    },
    {
        "scene_index": 18,
        "act": "Act 8: The Grand Celebration & Penutup",
        "milestone": "The Golden Sunset Glow",
        "action": "Warm late-afternoon sunlight fills {setting}, casting a golden glow over {product} and the peaceful toy city boulevard.",
        "dialogue": "The golden sun is setting over our peaceful toy city! Every street is safe, every friend is happy, and our favorite police cruiser rests with pride!",
        "sfx": "[SFX: Gentle acoustic guitar chords, engine purring softly, calm evening birdsong chime]",
        "vfx": "Warm golden hour sunset lighting, soft lens flare, gentle atmospheric dust motes",
        "story_link": "Preparing for the heartfelt movie farewell to viewers",
        "is_closing": False
    },
    {
        "scene_index": 19,
        "act": "Act 8: The Grand Celebration & Penutup",
        "milestone": "Holding the Hero Car",
        "action": "{subject} gently lifts {product} with two caring hands, cradling the toy police car with a loving, proud expression.",
        "dialogue": "Our little boy holds his favorite toy hero close to his heart! What a wonderful day of rescue adventures we shared with all our amazing friends!",
        "sfx": "[SFX: Soft child giggle, gentle chime, peaceful melodic background tune]",
        "vfx": "Macro close-up portrait of child and toy car, soft pastel bokeh background",
        "story_link": "The warm final farewell and movie closing to viewers",
        "is_closing": False
    },
    {
        "scene_index": 20,
        "act": "Act 8: The Grand Celebration & Penutup",
        "milestone": "PENUTUP: Heartfelt Movie Farewell",
        "action": "In a warm emotional close-up, {subject} looks straight into the camera lens with a loving smile and waves goodbye with one hand while holding {product}.",
        "dialogue": "Thank you so much for joining our police patrol adventure today, best friends! You are all champions! Keep playing, keep smiling, and see you next time! Bye-bye!",
        "sfx": "[SFX: Warm acoustic lullaby melody, child saying 'Bye-bye friends!', gentle horn beep 'beep-beep', closing applause]",
        "vfx": "Heartfelt close-up of child holding toy car and waving goodbye directly to camera, soft warm vignette fade, movie ending credits atmosphere",
        "story_link": "Grand movie ending (penutup), story complete",
        "is_closing": True
    }
]

# Dedicated 20-Scene Muddy Offroad & Automatic Car Wash Adventure Arc
MUD_CARWASH_20_ARC = [
    {
        "scene_index": 1,
        "act": "Act 1: The Dirty Trail Adventure",
        "milestone": "Dirt Trail Rollout",
        "action": "At the start of the rugged playroom trail in {setting}, {product} revs its oversized offroad tires, kicking up imaginary dust as {subject} pushes forward.",
        "dialogue": "Welcome friends! Today our awesome {product_short} is going on a super messy muddy off-road adventure! Let us count down together: three, two, one, vroom!",
        "sfx": "[SFX: Deep knobby tire hum, engine throttle rev 'vroom-vroom!', child giggling 'Let us get muddy!']",
        "vfx": "Warm morning sunlight filtering across the carpet trail, cartoon dust puffs behind wheels",
        "story_link": "Approaching the giant muddy obstacle puddle ahead",
        "is_closing": False
    },
    {
        "scene_index": 2,
        "act": "Act 1: The Dirty Trail Adventure",
        "milestone": "Approaching the Mud Bog",
        "action": "{product} accelerates down a dirt hill slope toward a giant wet brown mud puddle created with pretend slime and water.",
        "dialogue": "Look out ahead, friends! There is a giant gooey mud puddle right across the path! He speeds up and gets ready for the biggest splash ever!",
        "sfx": "[SFX: Accelerating engine whoosh, wet squelch sound, toddler shouting 'Splash incoming!']",
        "vfx": "Brown mud puddle surface reflecting the room, low-angle tracking camera following tires",
        "story_link": "Tires hit the mud puddle at full speed",
        "is_closing": False
    },
    {
        "scene_index": 3,
        "act": "Act 1: The Dirty Trail Adventure",
        "milestone": "The Giant Mud Splash",
        "action": "{product} plunges directly into the deep mud bog, sending giant arches of brown mud and watery droplets splashing high into the air.",
        "dialogue": "SPLASH! Right into the deep muddy puddle! Look at the giant brown mud arches flying everywhere! That was the funniest and messiest splash of the day!",
        "sfx": "[SFX: Enormous wet splash 'KABLOOSH!', mud splatters, toddler laughing hysterically]",
        "vfx": "Slow-motion mud droplet spray frozen in mid-air, cartoon mud droplets splattering on camera lens",
        "story_link": "Tires churning through the sticky mud pit",
        "is_closing": False
    },
    {
        "scene_index": 4,
        "act": "Act 2: The Mud Bog Battle",
        "milestone": "Spinning Mud Wheels",
        "action": "{product} spins its rugged tires deep in the thick brown mud, mud rooster tails shooting backward as the powerful motor digs in.",
        "dialogue": "The mud is so thick and sticky! The oversized tires spin with power, shooting muddy rooster tails everywhere as our little truck pushes forward with all its might!",
        "sfx": "[SFX: Wet tire spinning 'shhhk-shhhk!', deep engine groaning with torque, child cheering 'Push, push!']",
        "vfx": "Thick mud coating the wheel rims and fenders, dynamic camera shake on tire struggle",
        "story_link": "Climbing up the slippery muddy embankment",
        "is_closing": False
    },
    {
        "scene_index": 5,
        "act": "Act 2: The Mud Bog Battle",
        "milestone": "Muddy Hill Climb",
        "action": "{product} grips the slippery slope with its deep knobby treads, pulling itself out of the mud pit inch by inch to reach dry land.",
        "dialogue": "Inch by inch we climb up the slippery bank! Those rugged off-road treads never give up, and—YES! We made it out of the mud pit!",
        "sfx": "[SFX: Mud suction release 'SCHLUCK!', engine triumph roar, toddler clapping enthusiastically]",
        "vfx": "Pebbles of dried mud dropping from undercarriage, bright sunlight illuminating muddy paint",
        "story_link": "Inspecting how completely dirty the vehicle is",
        "is_closing": False
    },
    {
        "scene_index": 6,
        "act": "Act 3: Time for the Car Wash",
        "milestone": "Completely Muddy Inspection",
        "action": "Camera slowly rotates around {product}, completely covered from bumper to spoiler in funny brown cartoon mud splatters, while {subject} laughs.",
        "dialogue": "Haha, look at our truck now! It is completely covered in brown gooey mud from top to bottom! You know what that means: it is time for a car wash!",
        "sfx": "[SFX: Playful cartoon trombone slide 'wah-wah-wah!', child laughing out loud, horn beep 'beep-beep']",
        "vfx": "Thick textured 3D mud splatters covering shiny decals, comical mud eyebrows on headlights",
        "story_link": "Driving toward the automated toy car wash building",
        "is_closing": False
    },
    {
        "scene_index": 7,
        "act": "Act 3: Time for the Car Wash",
        "milestone": "Car Wash Station Arrival",
        "action": "{product} drives up the paved approach to the colorful toy car wash station with neon flashing lights and rotating foam brushes.",
        "dialogue": "Here is the ultimate automatic toy car wash! Look at the cheerful rainbow lights and colorful rotating brushes waiting to make our truck sparkle like new!",
        "sfx": "[SFX: Car wash mechanical motor hum, digital chime 'ding-ding!', child whispering 'So cool!']",
        "vfx": "Flashing neon signage reflecting off wet puddle, steam rising gently from wash entrance",
        "story_link": "Entering the wash tunnel conveyor belt",
        "is_closing": False
    },
    {
        "scene_index": 8,
        "act": "Act 4: The Pre-Rinse & Soap Bath",
        "milestone": "Water Jet Pre-Rinse",
        "action": "{product} rolls into the wash portal as high-pressure water nozzles spray warm crystal water jets, loosening the thick outer crust of mud.",
        "dialogue": "Rolling inside! Whoosh! High-pressure water jets blast from both sides, washing away the first thick layer of mud with powerful spraying water streams!",
        "sfx": "[SFX: High-pressure water spray 'PSSSHHHH-WHOOSH!', water gushing, child gasping in awe]",
        "vfx": "Streaming water droplets cascading over muddy body panels, mud melting away in brown rivulets",
        "story_link": "Moving into the foaming soap chamber",
        "is_closing": False
    },
    {
        "scene_index": 9,
        "act": "Act 4: The Pre-Rinse & Soap Bath",
        "milestone": "Foam Cannon Explosion",
        "action": "Giant overhead nozzles shower {product} in a thick blanket of pink, blue, and yellow cartoon soap foam that bubbles with rainbow reflections.",
        "dialogue": "Foam party time! Giant soap cannons explode with fluffy pink, yellow, and blue bubbles, covering the whole truck like a giant delicious ice cream sundae!",
        "sfx": "[SFX: Foam nozzle 'FOOOMPH!', popping soap bubbles 'pop-pop-pop!', toddler giggling joyfully]",
        "vfx": "Thick volumetric foam suds bubbling on roof, rainbow iridescence shining inside each soap bubble",
        "story_link": "Rolling into the giant rotating scrubber brushes",
        "is_closing": False
    },
    {
        "scene_index": 10,
        "act": "Act 5: The Scrubbing Brushes",
        "milestone": "Vertical Brush Scrub",
        "action": "Two giant spinning blue foam brushes hug the sides of {product}, scrubbing the doors and muddy wheels with cheerful swirling motions.",
        "dialogue": "Here come the giant spinning scrubber brushes! Swish, swash, swish! They spin around the sides, tickling the doors and scrubbing every speck of dirt away!",
        "sfx": "[SFX: Whirring sponge scrub 'swish-swash-swish!', motor hum, child shouting 'Tickle, tickle!']",
        "vfx": "Soap foam flying off spinning brush bristles, bright pastel foam splattering playfully",
        "story_link": "Top overhead roller brush sweeps down over hood and roof",
        "is_closing": False
    },
    {
        "scene_index": 11,
        "act": "Act 5: The Scrubbing Brushes",
        "milestone": "Overhead Roller Brush",
        "action": "A massive yellow roller brush rolls over the hood, windshield, and roof of {product}, leaving a pristine streak of sparkling red paint behind.",
        "dialogue": "Down comes the big yellow top brush rolling right over the hood and roof! Look, friends, the glossy red paint is already starting to shine through!",
        "sfx": "[SFX: Soft foam roller sound 'woosh-woosh!', squeak of clean glass, toddler cheering 'So clean!']",
        "vfx": "Revealing sparkling clean paint beneath foam, glittering starburst shines on cleaned hood",
        "story_link": "Specialized wheel scrubbers clean the tire rims",
        "is_closing": False
    },
    {
        "scene_index": 12,
        "act": "Act 6: The Wheel Scrub & Rinse",
        "milestone": "Tire Tread Wheel Scrub",
        "action": "Miniature spinning bristle pads clean each oversized tire and wheel rim, removing all the trapped mud between the deep rubber treads.",
        "dialogue": "Do not forget those awesome oversized tires! Dedicated wheel scrubbers spin against the rims, making the deep rubber treads look brand new and ready to roll!",
        "sfx": "[SFX: Bristle scrub 'chika-chika!', water squirt, child giggling 'Clean tires!']",
        "vfx": "Deep black rubber texture restored in 8K macro detail, water spray glistening on rims",
        "story_link": "Passing under the waterfall rinse arch",
        "is_closing": False
    },
    {
        "scene_index": 13,
        "act": "Act 6: The Wheel Scrub & Rinse",
        "milestone": "Waterfall Cascade Rinse",
        "action": "{product} drives through a cascading waterfall arch of crystal-pure water, washing away every last soap bubble into the drainage grate.",
        "dialogue": "Through the crystal waterfall rinse we glide! All the colorful soap bubbles wash away, revealing our gleaming champion underneath brighter than ever before!",
        "sfx": "[SFX: Heavy waterfall cascade 'SPLAAASH-RUSH!', gurgling drain, child clapping hands]",
        "vfx": "Sheets of crystal water cascading off aerodynamic curves, brilliant light refractions",
        "story_link": "Entering the giant warm air drying bay",
        "is_closing": False
    },
    {
        "scene_index": 14,
        "act": "Act 7: The Jet Blow Dryer",
        "milestone": "Warm Air Blow Dryers",
        "action": "Giant cartoon blow dryers blast warm air from all angles, sending water droplets dancing and skittering off the glossy hood of {product}.",
        "dialogue": "Whooosh! Giant warm air jet dryers roar to life! Watch the little water droplets race right off the shiny hood like tiny speed skaters heading for adventure!",
        "sfx": "[SFX: Powerful jet dryer wind 'WHOOOOOOSH!', water droplets skittering, child laughing loudly]",
        "vfx": "Dynamic air ripples blowing across glossy paint, dancing water beads atomizing into mist",
        "story_link": "Rolling onto the automated waxing buffer pads",
        "is_closing": False
    },
    {
        "scene_index": 15,
        "act": "Act 7: The Jet Blow Dryer",
        "milestone": "Diamond Wax & Polish",
        "action": "Soft velvet buffer pads buff the body panels of {product}, giving the glossy finish a mirror-like cartoon diamond shine.",
        "dialogue": "Now for the special diamond wax and polish! Soft velvet pads buff the finish until the shiny decals sparkle like stars in the midnight sky!",
        "sfx": "[SFX: Gentle buffer squeak 'rub-a-dub!', diamond sparkle chime 'TING-TING!', toddler in awe 'Ooooh!']",
        "vfx": "Glittering starburst glints reflecting off vehicle hood, ultra-deep mirror gloss reflection",
        "story_link": "Exiting the car wash tunnel into the sunny playroom",
        "is_closing": False
    },
    {
        "scene_index": 16,
        "act": "Act 8: The Sparkling Clean Finale",
        "milestone": "Car Wash Exit Portal",
        "action": "{product} rolls out of the car wash exit portal into the warm sunlit playroom, pristine, spotless, and sparkling with showroom brilliance.",
        "dialogue": "And out into the bright sunshine it rolls! Spotless, pristine, and dazzling! Not a single speck of mud left, looking completely brand new and gorgeous!",
        "sfx": "[SFX: Triumphant horn honk 'beep-beep!', joyful engine rev, toddler cheering 'Look at that shine!']",
        "vfx": "Dramatic sun glare starbursts on front bumper, warm soft lighting illuminating playroom",
        "story_link": "Victory rev on the clean carpet runway",
        "is_closing": False
    },
    {
        "scene_index": 17,
        "act": "Act 8: The Sparkling Clean Finale",
        "milestone": "Victory Carpet Sprint",
        "action": "{product} accelerates down the colorful playroom carpet with new energy, shiny tires rolling smoothly as {subject} cheers proudly.",
        "dialogue": "Off it zooms down the playroom carpet with pure joy and speed! A clean car is a fast car, and our champion is ready for the next race!",
        "sfx": "[SFX: Smooth tire roll on carpet, happy purring engine, child laughing happily]",
        "vfx": "Speed lines trailing behind shiny spoiler, crystal sharp 8K macro focus on clean flame decals",
        "story_link": "Child picks up the sparkling clean toy car",
        "is_closing": False
    },
    {
        "scene_index": 18,
        "act": "Act 8: The Sparkling Clean Finale",
        "milestone": "Close-up Clean Mirror Inspection",
        "action": "{subject} points to the mirror reflection in the shiny car door, showing their happy smiling face reflected in the glossy paintwork.",
        "dialogue": "Look in the mirror reflection on the door! You can see the happy smiling face of our little toddler reflected right in the shiny paint! How awesome is that!",
        "sfx": "[SFX: Toddler giggle, playful horn tap, cheerful acoustic melody]",
        "vfx": "Clear mirror reflection of child's smile on vehicle door panel, cinematic studio lighting",
        "story_link": "The warm final farewell and movie closing to viewers",
        "is_closing": False
    },
    {
        "scene_index": 19,
        "act": "Act 8: The Sparkling Clean Finale",
        "milestone": "Cradling the Clean Champion",
        "action": "{subject} holds {product} close with two loving hands, admiring the spotless tires and sparkling headlights with pure childlike wonder.",
        "dialogue": "Holding our shiny companion gently in two hands! From the messiest mud bog to the cleanest car wash sparkle, what an unforgettable adventure we had together today!",
        "sfx": "[SFX: Gentle chime, soft child chuckle, peaceful bedtime lullaby guitar]",
        "vfx": "Warm golden vignette around frame, soft playroom bokeh, wholesome atmosphere",
        "story_link": "Preparing for the heartfelt movie farewell to viewers",
        "is_closing": False
    },
    {
        "scene_index": 20,
        "act": "Act 8: The Sparkling Clean Finale",
        "milestone": "PENUTUP: Heartfelt Movie Farewell",
        "action": "In a warm emotional close-up, {subject} looks straight into the camera lens with a loving smile and waves goodbye with one hand while holding the sparkling {product}.",
        "dialogue": "Thank you so much for joining our messy mud and car wash adventure today, best friends! You are all champions! Keep playing, keep smiling, and see you next time! Bye-bye!",
        "sfx": "[SFX: Warm acoustic lullaby melody, child saying 'Bye-bye friends!', gentle horn beep 'beep-beep', closing applause]",
        "vfx": "Heartfelt close-up of child holding toy car and waving goodbye directly to camera, soft warm vignette fade, movie ending credits atmosphere",
        "story_link": "Grand movie ending (penutup), story complete",
        "is_closing": True
    }
]

def get_thematic_20_scene_arc(category: str) -> List[Dict[str, Any]]:
    """Returns the dedicated 20-scene story arc matching the detected video theme."""
    cat = (category or "").lower()
    if any(k in cat for k in ["police", "polisi", "patrol", "cop"]):
        return POLICE_CHASE_20_ARC
    elif any(k in cat for k in ["mud", "lumpur", "wash", "cuci"]):
        return MUD_CARWASH_20_ARC
    return CINEMATIC_20_SCENE_ARC

CINEMATIC_STORY_EPISODES = [
    # --- ACT 1: THE GRAND COUNTDOWN & LAUNCH (SCENES 1-5) ---
    {
        "scene_index": 1,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Starting Grid & Countdown Rev",
        "action": "At the starting line of {setting}, {product} revs its engine with playful glowing rounded headlights, while {subject} holds the rear bumper eagerly ready for the launch countdown.",
        "dialogue": "Welcome friends to the greatest toy car rally ever! Look at our incredible {product_short} revving its engine at the starting gate! Let us count down together: three, two, one!",
        "sfx": "[SFX: High-RPM engine throttle revs 'vroom-vroom!', digital countdown beeps 'beep-beep-BEEP!', eager toddler cheer 'Let us go!']",
        "vfx": "Subtle heat haze shimmering above exhaust, warm morning playroom sunbeams, animated cartoon tachometer needle dancing",
        "story_link": "High-energy countdown building anticipation toward the opening drop",
        "is_closing": False
    },
    {
        "scene_index": 2,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Steep Ramp Launch Acceleration",
        "action": "{product} rockets down the steep orange decline at blistering speed, tires spinning with smoke puffs as {subject} cheers enthusiastically from the sideline.",
        "dialogue": "Green light! Off it rockets down the steep orange hill at lightning speed! Hold on tight, friends, this race is going to be super fast and exciting!",
        "sfx": "[SFX: Rubber tires screeching 'skrrrt!', sudden whoosh of acceleration, energetic drum beat, child laughing loudly]",
        "vfx": "Dynamic motion blur trailing behind wheels, white cartoon speed lines, soft carpet dust dispersion",
        "story_link": "High velocity descent setting up the first high-speed curve",
        "is_closing": False
    },
    {
        "scene_index": 3,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Hairpin Cone Drift",
        "action": "{product} drifts smoothly around bright miniature traffic cones, tires gripping the track edge with animated cartoon sparks dancing off the outer rail.",
        "dialogue": "Here comes the first sharp hairpin curve! Look at how smoothly our {product_short} drifts past the miniature cones without touching a single one, pure racing skill!",
        "sfx": "[SFX: Lateral tire squeal 'squeeeak!', rhythmic engine acceleration, playful horn honk 'beep beep!']",
        "vfx": "Sparks dancing along outer track rail, sweeping camera pan blur, reflective gloss shine on vehicle hood",
        "story_link": "Flawless curve exit leading into straightaway speed lane",
        "is_closing": False
    },
    {
        "scene_index": 4,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Straightaway Power Slide",
        "action": "{product} power-slides onto the open straightaway towards the toy city boulevard, glossy body panels sparkling under playroom daylight as {subject} guides the wheels.",
        "dialogue": "Straightening out with pure style and power! The shiny paint sparkles under the playroom lights as the toddler guides the wheels with joyful precision and confidence!",
        "sfx": "[SFX: Deep engine purr, rapid tire rotation sound, joyful toddler giggles, cheerful playful soundtrack]",
        "vfx": "Lens flare glint off front bumper, crisp 8K macro focus on spinning rim spokes, ambient room depth of field",
        "story_link": "Momentum carries the vehicle directly toward the neon speed sensor",
        "is_closing": False
    },
    {
        "scene_index": 5,
        "act": "Act 1: The Grand Countdown & Launch",
        "milestone": "Neon Speed Gate Breach",
        "action": "{product} blasts through the glowing neon speed sensor arch, triggering cheerful flashing LED rainbow lights that illuminate {setting}.",
        "dialogue": "Blasting right through the neon speed gate! The sensors flash with cheerful colors as we hit top racing speed heading for the stunt obstacle arena right now!",
        "sfx": "[SFX: Digital chime 'ding-ding-ding!', turbo exhaust pop 'bam!', energetic child shout 'Super fast!']",
        "vfx": "Neon light streak reflection on vehicle body, colorful digital HUD speed rings expanding outward",
        "story_link": "Entering the aerial stunt ramp sector with maximum velocity",
        "is_closing": False
    },

    # --- ACT 2: THE STUNT RAMP & BUILDING BLOCK GAUNTLET (SCENES 6-12) ---
    {
        "scene_index": 6,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Wooden Ramp Approach",
        "action": "Camera tracks at ground level as {product} charges toward a steep wooden launch ramp, front bumper lowering aggressively as engine power surges.",
        "dialogue": "Look ahead, friends! The giant wooden jump ramp is right in front of us! He presses down on the pedal to gain maximum speed for the jump!",
        "sfx": "[SFX: Engine roaring at peak pitch, suspension tightening under acceleration, child gasping in eager anticipation]",
        "vfx": "Low-angle ground camera looking upward, dramatic sun glare over ramp lip, tire track marks on wood",
        "story_link": "Tires hit the ramp lip preparing for airborne liftoff",
        "is_closing": False
    },
    {
        "scene_index": 7,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Airborne 360 Stunt Leap",
        "action": "{product} launches into mid-air, performing a breathtaking 360-degree aerial stunt jump soaring high above a colorful stack of rainbow building blocks.",
        "dialogue": "Up into the sky it launches! Look at that breathtaking aerial flight high over the towering stack of colorful rainbow blocks, defying gravity with pure magic!",
        "sfx": "[SFX: Suspension spring release 'BOING!', wind rush 'WHOOOOSH!', slow-motion heartbeat thud, child shouting 'Look at that!']",
        "vfx": "Slow-motion apex freeze at maximum height, rainbow block colors reflecting on undercarriage, floating dust motes",
        "story_link": "Gliding gracefully down toward the soft blue landing cushion",
        "is_closing": False
    },
    {
        "scene_index": 8,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Four-Wheel Cushion Landing",
        "action": "{product} makes a flawless four-wheel touchdown on the blue foam landing mat, rugged shock absorbers flexing smoothly with a gentle bounce.",
        "dialogue": "Touchdown! What a flawless four-wheel landing on the soft bounce mat! The shock absorbers flex gently and bounce right back into the race without stopping!",
        "sfx": "[SFX: Soft rubber thud 'THUMP!', suspension bounce squeak, triumphant child cheer 'Woohoo!', clapping hands]",
        "vfx": "Puff of cushion compression dust, dynamic camera shake on impact, restored 24fps motion velocity",
        "story_link": "Rolling off the mat straight into the foam cube obstacle",
        "is_closing": False
    },
    {
        "scene_index": 9,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Foam Cube Barrier Breach",
        "action": "{product} plows cheerfully through a wall of soft foam cubes, sending colorful lightweight blocks tumbling gently to either side of the track.",
        "dialogue": "Direct hit on the soft foam obstacle course! The cubes tumble harmlessly to the sides like colorful pillow feathers as our brave hero pushes right through!",
        "sfx": "[SFX: Soft foam block tumbling 'thud-thud-pop!', engine growl, hilarious toddler chuckles, energetic horn honk]",
        "vfx": "Slow-motion floating foam blocks tumbling in foreground, vehicle headlights shining through the gaps",
        "story_link": "Clearing the foam barrier into the precision domino slalom",
        "is_closing": False
    },
    {
        "scene_index": 10,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Domino Slalom Weave",
        "action": "{product} weaves with nimble precision through a standing domino maze, tires swerving left and right without knocking down a single colorful piece.",
        "dialogue": "Now for the ultimate test of balance: weaving in and out of the domino maze without tipping over a single one! Steady hands guide our champion!",
        "sfx": "[SFX: Rapid tire swishing left-and-right, soft wooden click-clack resonance, child holding breath then giggling]",
        "vfx": "Z-axis camera tracking between domino pillars, sharp macro focus on rubber tire tread blocks",
        "story_link": "Exiting the domino maze toward the canyon bridge",
        "is_closing": False
    },
    {
        "scene_index": 11,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Suspension Bridge Crossing",
        "action": "{product} carefully crosses a narrow wooden suspension bridge elevated above the playroom rug, wooden slats rattling gently under rubber tires.",
        "dialogue": "Carefully crossing the high suspension bridge! The wooden slats rattle with a friendly song as the little boy guides our four-wheeled hero across safely!",
        "sfx": "[SFX: Rhythmic wooden plank clatter 'clack-clack-clack!', bridge ropes creaking, gentle engine hum, child humming]",
        "vfx": "Overhead aerial drone view looking down into the playroom rug, soft golden lighting filtering through bridge cables",
        "story_link": "Safely touching solid track preparing for turbo lane",
        "is_closing": False
    },
    {
        "scene_index": 12,
        "act": "Act 2: The Aerial Stunt Arena",
        "milestone": "Turbo Boost Pad Activation",
        "action": "{product} hits the glowing neon turbo pad, electric cyan and orange speed streaks igniting behind its rear wheels as it surges ahead.",
        "dialogue": "We crossed the bridge! Now hitting the neon turbo booster strip! Feel that sudden surge of power rocketing our vehicle straight ahead with pure energy!",
        "sfx": "[SFX: Electric charging whine, futuristic warp whoosh 'ZOOOOM!', child screaming with delight 'Faster, faster!']",
        "vfx": "Electric cyan and orange particle trail behind rear wheels, speed distortion lines radiating across frame",
        "story_link": "Supercharged speed propels the vehicle into the rainbow tunnel",
        "is_closing": False
    },

    # --- ACT 3: THE MAGICAL RAINBOW TUNNEL & LOOPS (SCENES 13-20) ---
    {
        "scene_index": 13,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Rainbow Arched Entrance",
        "action": "{product} plunges into the glowing rainbow tunnel, multi-colored arches illuminating the glossy roof with vibrant pink and green reflections.",
        "dialogue": "Plunging headfirst into the magical rainbow tunnel! The colorful arches light up the glossy roof with dazzling pink and green glow reflections everywhere we look!",
        "sfx": "[SFX: Cavernous echoing engine roar inside tunnel, rhythmic tire click-clack, child whispering in awe 'So pretty!']",
        "vfx": "Psychedelic rainbow color reflections sweeping across glossy hood, high-contrast tunnel lighting",
        "story_link": "Diving deeper into the resonant tunnel corridor",
        "is_closing": False
    },
    {
        "scene_index": 14,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Echoing Subterranean Sprint",
        "action": "Inside the tunnel, {product} speeds along the polished reflective floor, rounded headlights casting bright volumetric beams through light mist.",
        "dialogue": "Listen to that engine sound echo inside! The headlights pierce through the colorful mist as the wheels grip the polished track with absolute confidence!",
        "sfx": "[SFX: Resonant acoustic echo, throaty exhaust rumble, playful horn echo 'beep-beep-beep!', child laughing]",
        "vfx": "Mirror-like floor reflections, headlight volumetric light cones cutting through soft atmospheric haze",
        "story_link": "Approaching the sparkling crystal obstacle cluster",
        "is_closing": False
    },
    {
        "scene_index": 15,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Glowing Crystal Detour",
        "action": "{product} swerves around glittering toy crystal stalagmites, glowing sparkles dancing across the windshield and bodywork in 3D Pixar style.",
        "dialogue": "Watch out for the sparkling toy crystal stalagmites! With nimble precision, our driver swerves smoothly around the glittering gems like a playful little starship!",
        "sfx": "[SFX: Crystal chime 'ting-ting-ting!', smooth tire drift, child clapping happily in amazement]",
        "vfx": "Prismatic crystal lens flares, glowing sparkle particles dancing across windshield and body",
        "story_link": "Angling up toward the corkscrew helix wall",
        "is_closing": False
    },
    {
        "scene_index": 16,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Corkscrew Helix Wall Climb",
        "action": "{product} rides along the curved vertical tunnel wall, executing an upward corkscrew helix with camera rotating alongside to match its tilt.",
        "dialogue": "Climbing the corkscrew spiral wall! The car tilts on two wheels, defying gravity as it spins upward toward the bright sunlight exit above us!",
        "sfx": "[SFX: Centrifugal tire groaning grip, climbing engine strain, upbeat cartoon trumpet fanfare, child cheering]",
        "vfx": "Dynamic 360-degree rotational camera roll matching vehicle tilt, spiral motion blur",
        "story_link": "Breaking through the tunnel portal into bright sunlight",
        "is_closing": False
    },
    {
        "scene_index": 17,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Sunlit Portal Breakthrough",
        "action": "{product} bursts out of the tunnel mouth into brilliant afternoon playroom daylight, sunbeams washing over the glossy paintwork.",
        "dialogue": "Bursting out of the tunnel back into the warm sunshine! Fresh playroom daylight floods over the gleaming body as we accelerate with pure joy and smiles!",
        "sfx": "[SFX: Sound opening up into bright daylight acoustics, wind whoosh, joyful toddler sigh 'Ahhh, we made it!']",
        "vfx": "Dramatic brightness transition from dark tunnel to radiant sunlight, golden sun lens flare",
        "story_link": "Speeding toward the giant banked stadium turn",
        "is_closing": False
    },
    {
        "scene_index": 18,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Banked Stadium Velodrome Turn",
        "action": "{product} rides high on a 45-degree banked velodrome curve, centrifugal momentum pressing the tires firmly into the vibrant orange track.",
        "dialogue": "Leaning hard into the banked stadium curve! The car rides high on the curved wall, using centrifugal momentum to gain even greater velocity right now!",
        "sfx": "[SFX: High-speed centrifugal track friction 'shhh-whirr!', engine humming at peak revs, child laughing]",
        "vfx": "Tilted horizon line camera angle, dynamic speed streaks along orange curved barrier",
        "story_link": "Leveling out heading straight for the 360 vertical loop",
        "is_closing": False
    },
    {
        "scene_index": 19,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Vertical 360 Loop Upside-Down",
        "action": "{product} rockets upside-down through the top arch of a giant 360-degree vertical loop, child in background watching upside down with huge smiling eyes.",
        "dialogue": "Here is the legendary giant loop! Upside down at the very peak! The car hangs in mid-air, defying physics with pure racing bravery and excitement!",
        "sfx": "[SFX: Gravity-defying vertical whoosh 'WHOOOOSH!', metallic loop hum, ecstatic child shout 'We are upside down!']",
        "vfx": "Slow-motion freeze at top apex showing child face watching upside down, speed lines wrapping in circle",
        "story_link": "Exiting the loop with explosive forward momentum",
        "is_closing": False
    },
    {
        "scene_index": 20,
        "act": "Act 3: The Rainbow Tunnel",
        "milestone": "Loop Exit Straightaway Sprint",
        "action": "{product} shoots out of the vertical loop onto the straightaway, leveling out smoothly with sparkling speed lines dancing along its fenders.",
        "dialogue": "Exiting the loop straight as an arrow! The crowd of toy friends goes wild as our four-wheeled champion glides smoothly onto the straightaway track!",
        "sfx": "[SFX: Smooth transition from plastic track to plush carpet 'whump-whirrr', celebratory whistle, child cheering]",
        "vfx": "Soft carpet fiber micro-details, glistening paint finish under room lighting, dust motes",
        "story_link": "Transitioning toward the rugged sand and water expedition zone",
        "is_closing": False
    },

    # --- ACT 4: THE MUD, SAND & WATER ADVENTURE (SCENES 21-30) ---
    {
        "scene_index": 21,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Kinetic Sand Dune Climb",
        "action": "{product} enters the bumpy golden kinetic sand terrain, rugged oversized tires digging in with visible tread traction as it attacks the hill.",
        "dialogue": "Entering the kinetic sand off-road expedition! The rugged tire treads dig deep into the soft golden sand, climbing step by step with relentless power!",
        "sfx": "[SFX: Sand crunching under heavy treads 'shhhk-shhhk-crunch!', low-gear torque rumble, child cheering encouragement]",
        "vfx": "Sand particles spraying playfully from rear tires, macro focus on deep tire tread ridges",
        "story_link": "Approaching the dune summit ready for the plunge",
        "is_closing": False
    },
    {
        "scene_index": 22,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Sand Dune Crest Plunge",
        "action": "{product} pauses for a split-second at the sand ridge summit before sliding down the steep slope with a joyful whoosh into the valley.",
        "dialogue": "We reached the very top of the sand dune! Pausing for a split second before zooming down the other side with thrilling joy and laughter!",
        "sfx": "[SFX: Engine revving at crest, sand sliding whoosh 'shwoooop!', child squealing in delight]",
        "vfx": "Miniature sand avalanche tumbling downward, warm golden hour playroom lighting",
        "story_link": "Carpet straightaway leads directly toward the blue ball-pit pool",
        "is_closing": False
    },
    {
        "scene_index": 23,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Plastic Ball Pit Splashdown",
        "action": "{product} plunges into a blue plastic ball-pit pool, sending colorful lightweight spheres splashing in slow-motion in every direction.",
        "dialogue": "Look out below, it is the blue plastic ball pit! Splash! A colorful wave of lightweight balls bounces in all directions playfully and cheerfully!",
        "sfx": "[SFX: Plastic ball clatter 'clack-clack-clatter!', bouncing ball sounds 'boing-boing!', contagious toddler laughter]",
        "vfx": "Colorful blue, yellow, and red balls bouncing in slow-motion across screen in 3D depth",
        "story_link": "Surfing across the shiny blue play mat",
        "is_closing": False
    },
    {
        "scene_index": 24,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Hydroplane Water Mat Surf",
        "action": "{product} glides across the glossy water play mat, imaginary cartoon droplets scattering like diamonds in the cheerful daylight.",
        "dialogue": "Gliding across the shiny blue water mat! Droplets of imaginary splash sparkle like cartoon diamonds as the vehicle surfs forward smoothly without stopping!",
        "sfx": "[SFX: Wet tire hydroplane 'swoooosh!', bubbly water splash 'splish-splash!', child giggling happily]",
        "vfx": "Glossy water surface reflections, animated cartoon splash droplets with rainbow prismatic fringes",
        "story_link": "Guiding the vehicle into the mini toy car wash station",
        "is_closing": False
    },
    {
        "scene_index": 25,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Foam Bubble Car Wash Station",
        "action": "{product} passes between rotating soft sponge rollers, rainbow soap bubbles popping playfully against its glossy fenders.",
        "dialogue": "Time for a lightning-fast car wash! Soft sponge rollers spin around the hood, tickling the headlights and washing away all the dust playfully!",
        "sfx": "[SFX: Soft sponge swishing 'squeegee-squeegee!', soapy bubbles popping 'pop-pop-pop!', playful music box chime]",
        "vfx": "Floating iridescent soap bubbles catching room light, soft foam suds wiping off in real-time",
        "story_link": "Emerging sparkling clean into the miniature construction zone",
        "is_closing": False
    },
    {
        "scene_index": 26,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Gleaming Paint Reveal",
        "action": "{product} emerges from the car wash with pristine, ultra-glossy paint gleaming under the sun as {subject} gives an enthusiastic double thumbs-up.",
        "dialogue": "Emerging from the wash sparkling cleaner than ever! The glossy finish shines like brand new as our proud little driver gives two enthusiastic thumbs up!",
        "sfx": "[SFX: Cartoon sparkle chime 'ting-ting-twinkle!', engine purr, child singing a cheerful melody]",
        "vfx": "Star-shaped specular glints pinging off polished hood and chrome rim covers",
        "story_link": "Heading into the miniature toy construction zone",
        "is_closing": False
    },
    {
        "scene_index": 27,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Toy Construction Site Detour",
        "action": "{product} drives through a toy construction zone with miniature yellow dump trucks and friendly cranes waving mechanical booms.",
        "dialogue": "Navigating through the toy construction site! Friendly yellow dump trucks and mini cranes wave their mechanical arms as we speed past with polite honks!",
        "sfx": "[SFX: Construction ratchets 'click-clack!', friendly horn honks, engine hum, child saying 'Hello trucks!']",
        "vfx": "Miniature construction barriers, tiny orange warning cones, detailed toy mechanical linkages",
        "story_link": "Weaving through the yellow safety barrel slalom",
        "is_closing": False
    },
    {
        "scene_index": 28,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Safety Barrel Slalom",
        "action": "{product} slaloms with fast steering inputs around yellow toy safety barrels, tires squeaking playfully on the smooth playroom floor.",
        "dialogue": "Swerving left, then swerving right through the detour zone! Nimble steering keeps our vehicle right on track without missing a single beat or obstacle!",
        "sfx": "[SFX: Sharp steering tire squeaks, rapid throttle bursts, child making playful motor sounds 'brrr-brrr!']",
        "vfx": "Fast left-to-right camera whip pans, cartoon motion trails around bumpers",
        "story_link": "Approaching the wooden seesaw balance test",
        "is_closing": False
    },
    {
        "scene_index": 29,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Tilting Seesaw Bridge",
        "action": "{product} balances on the pivot point of a wooden seesaw plank before it gently tips downward, allowing a smooth roll forward.",
        "dialogue": "Driving onto the wooden seesaw bridge! Creeping slowly to the center until—tilt! The plank gently pivots forward, letting us roll onward with confidence!",
        "sfx": "[SFX: Wooden creak, see-saw pivot 'thunk!', child holding breath then cheering 'Yes, it tipped!']",
        "vfx": "Slow deliberate camera balance shot, realistic wood grain textures, shadow shifting smoothly",
        "story_link": "Pulling in for the quick halfway pit stop check",
        "is_closing": False
    },
    {
        "scene_index": 30,
        "act": "Act 4: Sand & Water Expedition",
        "milestone": "Mid-Race Pit Stop Check",
        "action": "At the halfway mark, {subject} lovingly checks the tire treads of {product} and wipes the cartoon windshield clean before giving the go-ahead.",
        "dialogue": "Quick pit stop at the halfway mark! Little toddler fingers check the tires and give the windshield a loving wipe. All systems ready for action!",
        "sfx": "[SFX: Toy pneumatic wrench sound 'whirrr-clack!', child giggling 'All ready!', horn double beep]",
        "vfx": "Loving close-up of child hands gently inspecting the toy car, warm emotional framing",
        "story_link": "All set to tackle the monumental spiral tower",
        "is_closing": False
    },

    # --- ACT 5: THE SPIRAL TOWER & HIGH-ALTITUDE DESCENT (SCENES 31-40) ---
    {
        "scene_index": 31,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Spiral Base Entry",
        "action": "{product} enters the base of a towering multi-tier spiral ramp, beginning its circular upward climb as camera pans upward in awe.",
        "dialogue": "Beginning the climb up the monumental spiral tower! Round and round the track circles, rising higher and higher above the bedroom floor with energy!",
        "sfx": "[SFX: Rhythmic upward spiral hum, tires gripping curved rails, cheerful upbeat accordion tune]",
        "vfx": "High-angle vertical camera looking down spiral helix, gradual elevation increase",
        "story_link": "Winding upward toward level two balcony",
        "is_closing": False
    },
    {
        "scene_index": 32,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Tower Level 2 Ascent",
        "action": "Camera orbits around the tower exterior as {product} rounds level two, engine singing cheerfully as it ascends towards the ceiling.",
        "dialogue": "Reaching level two of the tower! The bird's-eye camera captures our colorful vehicle winding effortlessly upward with tireless racing determination and joy!",
        "sfx": "[SFX: Steady engine cadence, child cheering 'Higher and higher!', soft background play chimes]",
        "vfx": "Sweeping circular camera pan rotating around exterior of tower, depth blur below",
        "story_link": "Passing the cheering stuffed animal gallery",
        "is_closing": False
    },
    {
        "scene_index": 33,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Stuffed Animal Spectator Gallery",
        "action": "On the adjacent bookshelf, plush teddy bears and toy dinosaurs wave miniature checkered flags as {product} climbs past with a friendly horn.",
        "dialogue": "Look at the stuffed animal crowd cheering from the bookshelf grandstand! The teddy bear and plush dinosaur are waving flags with pure joy and smiles!",
        "sfx": "[SFX: Cheerful spectator cheering murmurs, squeaky toy honk, child shouting 'Look at Mr. Bear!']",
        "vfx": "Soft textured stuffed animals in background smiling, colorful miniature flags waving",
        "story_link": "Nearing the panoramic observation platform at the peak",
        "is_closing": False
    },
    {
        "scene_index": 34,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Tower Peak Panoramic Balcony",
        "action": "{product} arrives at the top observation balcony, pausing against the wide window overlooking the entire sprawling playroom track below.",
        "dialogue": "We made it to the very summit balcony of the tower! What a spectacular panoramic view of the entire playroom race track below our wheels!",
        "sfx": "[SFX: Gentle wind whisper, majestic brass fanfare, toddler gasping in pure awe 'We are so high!']",
        "vfx": "Expansive wide-angle overview of whole playroom world, sun rays streaming through window",
        "story_link": "Locking onto the downhill high-speed zipline rail",
        "is_closing": False
    },
    {
        "scene_index": 35,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Zipline Track Plunge",
        "action": "{product} locks into the downhill zipline descent, rocketing down the high-velocity cable across the bedroom with cartoon speed blurs.",
        "dialogue": "Locking into the downhill zipline track! Three, two, one, and swooooosh! Rocketing down the steep cable with unbelievable cartoon speed and excitement!",
        "sfx": "[SFX: High-pitched zipline cable whir 'ZRRRRRRR!', wind rushing past ears, child yelling with joy]",
        "vfx": "Extreme motion blur streaks, camera zooming backward at matching velocity, speed lines",
        "story_link": "Approaching the soft pillow landing zone",
        "is_closing": False
    },
    {
        "scene_index": 36,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Pillow Cushion Touchdown",
        "action": "{product} deploys cartoon air brakes, landing softly on plush decorative pillows with a playful wiggle before rolling onto the carpet.",
        "dialogue": "Deploying the invisible cartoon air brakes! The vehicle touches down softly onto the plush foam pillows with a delightful bouncy wiggle and laughter!",
        "sfx": "[SFX: Air brake hiss 'Psssshhhh!', soft pillow landing 'FLUMP!', child giggling enthusiastically]",
        "vfx": "Pillow foam flexing gently, microscopic fabric threads in crisp 8K detail, smooth stop",
        "story_link": "Popping a wheelie onto the open floor track",
        "is_closing": False
    },
    {
        "scene_index": 37,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Front Wheelie Acceleration",
        "action": "{product} pops a playful front-wheel wheelie, accelerating down the carpet on its two rear tires with {subject} cheering proudly.",
        "dialogue": "Popping a playful front-wheel wheelie as we accelerate back onto the main course! The front wheels lift into the air with pure racing style!",
        "sfx": "[SFX: Rear tire burnout chirp, engine roar, child cheering 'Wheels up, let us roll!']",
        "vfx": "Low-angle perspective showing undercarriage, tiny cartoon smoke puffs from rear wheels",
        "story_link": "Entering the darkened glow-in-the-dark sector",
        "is_closing": False
    },
    {
        "scene_index": 38,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Blacklight Glow Track Entry",
        "action": "{product} enters the under-bed blacklight sector, track glowing in fluorescent neon green and body flame decals glowing electric yellow.",
        "dialogue": "Entering the nighttime glow sector of the room! The track glows in vivid neon green and purple under the playful blacklight ambiance of adventure!",
        "sfx": "[SFX: Futuristic synth pulse, gentle electrical hum, child whispering excitedly 'It glows!']",
        "vfx": "UV blacklight glow illumination, vehicle flame decals glowing neon yellow, bioluminescence",
        "story_link": "Switching on the high-beam headlights",
        "is_closing": False
    },
    {
        "scene_index": 39,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Headlight Beam Illumination",
        "action": "{product} switches on dual rounded headlights, piercing the dark glow corridor with warm golden beams that illuminate the way ahead.",
        "dialogue": "Our bright rounded headlights turn on, casting two friendly golden beams across the glowing track like a friendly superhero racing through the magical night!",
        "sfx": "[SFX: Headlight click 'click-snap!', warm beam hum, cheerful melody, playful horn beep]",
        "vfx": "Volumetric light cones illuminating dust motes, realistic lens flare, high contrast shadows",
        "story_link": "Emerging from the shadow sector back into golden afternoon daylight",
        "is_closing": False
    },
    {
        "scene_index": 40,
        "act": "Act 5: The Spiral Sky Tower",
        "milestone": "Golden Hour Daylight Return",
        "action": "{product} re-emerges into the warm afternoon sunbeams streaming through the curtains, paint glistening with radiant reflections.",
        "dialogue": "Back into the brilliant golden daylight! The afternoon sun warms the colorful track as our driver smiles with unstoppable racing enthusiasm and joy!",
        "sfx": "[SFX: Sunlit acoustic expansion, energetic guitar strum, child laughing with renewed vigor]",
        "vfx": "Warm golden-hour daylight wash, shimmering dust particles, crystal-clear car reflections",
        "story_link": "A companion vehicle enters the adjacent lane for the duel",
        "is_closing": False
    },

    # --- ACT 6: THE DUEL & OBSTACLE GAUNTLET (SCENES 41-50) ---
    {
        "scene_index": 41,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Companion Car Entry",
        "action": "A friendly companion toy car pulls into the parallel lane alongside {product}, both drivers exchanging friendly smiling glances before accelerating.",
        "dialogue": "Look over there, a friendly companion toy car pulls up into the neighboring lane! A friendly side-by-side match race is on right now, friends!",
        "sfx": "[SFX: Dual engine harmonies, friendly greeting horn 'beep-beep', child saying 'Race you to the finish!']",
        "vfx": "Side-by-side tracking camera, dual shadows racing across track surface",
        "story_link": "Side-by-side battle accelerating down the straight",
        "is_closing": False
    },
    {
        "scene_index": 42,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Wheel-to-Wheel Dual Race",
        "action": "Both toy vehicles race wheel-to-wheel down twin orange tracks, neither yielding an inch as miniature tires rotate in synchronized speed.",
        "dialogue": "Neck and neck down the twin straightaways! Both cars matching speed with thrilling precision, neither giving an inch of room in this playful duel!",
        "sfx": "[SFX: Twin engine roars at synchronized RPM, tires spinning in unison, child clapping excitedly]",
        "vfx": "Dynamic split-screen feel in single frame, speed lines framing both vehicles",
        "story_link": "Approaching the tight chicane curve",
        "is_closing": False
    },
    {
        "scene_index": 43,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Chicane Overtake Maneuver",
        "action": "{product} takes the inside line of the S-bend chicane, executing a polite bumper tap and surging into the lead with a triumphant horn honk.",
        "dialogue": "Navigating the chicane with expert skill! A polite tap of the bumpers and our hero pulls ahead into the lead with a big happy smile!",
        "sfx": "[SFX: Harmless plastic bumper tap 'bop!', tire chirp, child shouting 'Nice pass!']",
        "vfx": "Soft plastic collision vibration, smooth overtaking arc, camera tracking lead car",
        "story_link": "Sprinting forward toward the paper ribbon gate",
        "is_closing": False
    },
    {
        "scene_index": 44,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Paper Ribbon Gate Breakthrough",
        "action": "{product} bursts through a paper ribbon banner, streamers fluttering over the windshield in festive celebration of the lead.",
        "dialogue": "Blasting through the ribbon gate! Multi-colored paper streamers flutter over the hood like festive confetti celebrating our courageous journey forward with friends!",
        "sfx": "[SFX: Paper ribbon fluttering 'rustle-rustle-flutter!', engine acceleration, joyful toddler cheer]",
        "vfx": "Slow-motion paper streamers draping over windshield and drifting away in aerodynamic wake",
        "story_link": "Approaching the swinging foam pendulum obstacle",
        "is_closing": False
    },
    {
        "scene_index": 45,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Swinging Pendulum Timing",
        "action": "Ahead, a soft foam pendulum clock swings rhythmically across the track as {subject} leans forward, timing the acceleration perfectly.",
        "dialogue": "Approaching the swinging soft pendulum obstacle! Timing is everything right now. The toddler lines up the trajectory with total focus and patience!",
        "sfx": "[SFX: Clock tick-tock 'tick-tock-whoosh!', engine revving in rhythm, child whispering 'Wait for it...']",
        "vfx": "Swinging foam pendulum casting moving shadow across track, intense cinematic focus",
        "story_link": "Executing the split-second throttle punch",
        "is_closing": False
    },
    {
        "scene_index": 46,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Under-Pendulum Slide",
        "action": "{product} punches the throttle, ducking underneath the swinging pendulum with pinpoint timing as it clears the hazard without a scratch.",
        "dialogue": "Now! Stepping on the gas and sliding underneath with split-second perfection! We made it through with flying colors and zero bumps or scratches!",
        "sfx": "[SFX: Sudden turbo surge 'WHOOSH!', pendulum swinging past behind, child screaming in victory]",
        "vfx": "Camera dipping low beneath pendulum, speed blur trails, relieved child smile",
        "story_link": "Hitting the magnetic accelerator strip",
        "is_closing": False
    },
    {
        "scene_index": 47,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Magnetic Spark Accelerator",
        "action": "{product} crosses the magnetic accelerator strip, electric blue spark particles dancing around its wheel hubs as velocity doubles.",
        "dialogue": "Crossing the magnetic booster lane! Energy crackles with playful electric blue sparks, propelling our champion forward with astonishing speed and confidence!",
        "sfx": "[SFX: Electric crackle 'bzzzzt-ziiiip!', cartoon warp sound, child laughing 'Super power!']",
        "vfx": "Glowing blue electrical arc particles dancing around wheel hubs and chassis",
        "story_link": "Approaching the tabletop garage jump",
        "is_closing": False
    },
    {
        "scene_index": 48,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Tabletop Garage Jump",
        "action": "{product} launches off a tabletop crest soaring directly over the miniature toy parking garage in majestic slow motion.",
        "dialogue": "Launching off the tabletop crest directly over the miniature toy garage! Soaring through the air in majestic cinematic slow motion with total grace!",
        "sfx": "[SFX: High-altitude air whoosh, suspension spring release, child gasping with wide joyful eyes]",
        "vfx": "Bird's-eye downward perspective showing tiny toy town below, dramatic slow-motion",
        "story_link": "Lining up landing on the final straightaway",
        "is_closing": False
    },
    {
        "scene_index": 49,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Final Sector Touchdown",
        "action": "{product} lands cleanly on all four wheels at the entrance of the final sector, shock absorbers absorbing impact with zero bounce.",
        "dialogue": "Four wheels hit the final straightaway track at exactly the same time! Perfect shock absorption, steering straight toward the ultimate climax of the championship!",
        "sfx": "[SFX: Solid track impact 'THUMP!', suspension settling smoothly, child shouting 'Great landing!']",
        "vfx": "Camera stabilizing instantly on touchdown, forward momentum preserved, gleaming chrome",
        "story_link": "Unleashing the final turbo reserve for the mega ramp",
        "is_closing": False
    },
    {
        "scene_index": 50,
        "act": "Act 6: The Rival Duel & Gauntlet",
        "milestone": "Final Turbo Unleashed",
        "action": "{product} unleashes its final reserve of turbo energy, dual exhausts spitting golden cartoon sparkles as it screams toward the mega ramp.",
        "dialogue": "Unleashing the very last reserves of turbo energy! The little engine hums with heroic power as we head into the final championship stretch together!",
        "sfx": "[SFX: Turbo whistle reaching crescendo, engine roaring with joyful pride, child pumping fist]",
        "vfx": "Golden cartoon sparkles ejecting from rear exhausts, vibrant saturated color glow",
        "story_link": "The colossal mega ramp looms ahead for the finale",
        "is_closing": False
    },

    # --- ACT 7: THE MEGA RAMP & 360 APEX CLIMAX (SCENES 51-57) ---
    {
        "scene_index": 51,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Mega Ramp Incline Approach",
        "action": "Camera looks up from floor level at the towering mega ramp rising toward the ceiling as {product} charges the base with full determination.",
        "dialogue": "There it is, friends: the legendary Mega Ramp! The tallest, steepest, most thrilling incline on the whole playroom circuit! Ready for greatness together!",
        "sfx": "[SFX: Dramatic orchestral buildup, heavy engine idle rumbling, child gasping in awe 'The biggest ramp!']",
        "vfx": "Low-angle heroic worm's-eye camera emphasizing the immense height of orange ramp",
        "story_link": "Tires hit the steep ramp incline at full throttle",
        "is_closing": False
    },
    {
        "scene_index": 52,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Steep Mega Ramp Climb",
        "action": "{product} accelerates up the near-vertical orange incline, tires biting into the surface as engine revs reach their thrilling peak.",
        "dialogue": "Charging up the steep incline with full throttle! Tires digging into the textured plastic ramp, climbing straight toward the playroom ceiling with unstoppable force!",
        "sfx": "[SFX: Engine working at full power 'VROOOOM!', track vibration, toddler cheering enthusiastically]",
        "vfx": "Camera tracking alongside steep climb, dynamic motion blur below",
        "story_link": "Reaching the ramp lip for the ultimate launch",
        "is_closing": False
    },
    {
        "scene_index": 53,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Rocket Launch Liftoff",
        "action": "{product} launches off the mega ramp lip, soaring into the air like a rocket against the sunlit playroom window with {subject} jumping in excitement.",
        "dialogue": "Liftoff! The car separates from the ramp, blasting into the air like a magnificent cartoon rocket! Look at how high it flies right now!",
        "sfx": "[SFX: Colossal launch whoosh 'BOOOOOM-WHOOSH!', wind howling, child jumping up shouting 'Fly, car, fly!']",
        "vfx": "Slow-motion freeze framing the car suspended against sunlit playroom window",
        "story_link": "Entering the 360-degree matrix rotation apex",
        "is_closing": False
    },
    {
        "scene_index": 54,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Matrix 360 Apex Rotation",
        "action": "Camera rotates a full 360 degrees around {product} suspended at the jump apex in mid-air, volumetric sunbeams illuminating every glossy decal in 8K.",
        "dialogue": "A full 360-degree matrix camera rotation in mid-air! Every glossy detail of the car and every sparkle on the toddler's face captured in 8K!",
        "sfx": "[SFX: Cinematic bullet-time whoosh, peaceful harp glissando, child smiling with wonder]",
        "vfx": "360-degree camera rotation around vehicle suspended in mid-air, volumetric god rays",
        "story_link": "Beginning the graceful descent toward the finish line track",
        "is_closing": False
    },
    {
        "scene_index": 55,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Glide Slope Descent",
        "action": "{product} dips its front wheels gracefully, aligning with the downward landing slope with aerodynamic perfection.",
        "dialogue": "Beginning the smooth downward descent! The nose dips gracefully, aligning with the curved landing track with absolute laser precision and balance!",
        "sfx": "[SFX: Wind pitch descending, engine revving gently to match landing speed, child smiling proudly]",
        "vfx": "Gentle downward camera tilt tracking the glide slope, soft atmospheric depth blur",
        "story_link": "Touchdown on the final home stretch track",
        "is_closing": False
    },
    {
        "scene_index": 56,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Masterful Ramp Landing",
        "action": "{product} touches down on the landing ramp with a solid, satisfying thud, suspension compressing and releasing into full acceleration.",
        "dialogue": "Touchdown! What an unbelievable landing! Not a wobble, not a scratch! The greatest stunt jump in the history of toy car racing!",
        "sfx": "[SFX: Satisfying solid landing 'CLACK-THUD!', suspension compression, child screaming with pure joy]",
        "vfx": "Puff of landing dust, camera shock absorbing impact, vehicle accelerating instantly",
        "story_link": "Sprinting the final meters toward the checkered flag",
        "is_closing": False
    },
    {
        "scene_index": 57,
        "act": "Act 7: The Mega Ramp Climax",
        "milestone": "Checkered Flag Approach",
        "action": "Ahead, checkered flags flutter wildly as {product} charges toward the finish line with spectators and toys cheering in celebration.",
        "dialogue": "Only ten meters to the finish line! The checkered flags are waving wildly in the breeze as the crowd cheers with roaring excitement and pride!",
        "sfx": "[SFX: Roaring crowd applause, whistles, horn honking in celebration, engine sprinting at max speed]",
        "vfx": "Chequered flags framing both sides of screen, golden confetti already drifting down",
        "story_link": "Crossing the line for the grand victory",
        "is_closing": False
    },

    # --- ACT 8: THE GRAND FINALE & MEMORABLE MOVIE ENDING (PENUTUP) (SCENES 58-60) ---
    {
        "scene_index": 58,
        "act": "Act 8: The Grand Finale & Penutup",
        "milestone": "Victory Finish Line Crossing",
        "action": "{product} zooms triumphantly across the checkered finish line as a massive shower of festive rainbow confetti bursts into the air and banner drops.",
        "dialogue": "And across the finish line it zooms! The checkered flag drops as a giant shower of colorful confetti explodes into the air with pure joy!",
        "sfx": "[SFX: Checkered flag swoosh, confetti cannon explosion 'POP-POP-POP!', roaring toddler cheer 'We won the race!']",
        "vfx": "Thousands of rainbow confetti particles filling screen, slow-motion victory tape snapping, golden light",
        "story_link": "Pulling onto the highest step of the winner's podium",
        "is_closing": False
    },
    {
        "scene_index": 59,
        "act": "Act 8: The Grand Finale & Penutup",
        "milestone": "Winner's Podium Trophy Ceremony",
        "action": "{product} parks proudly atop the winner's podium with headlights flashing rhythmically like disco lights as {subject} hoists a golden toy trophy high.",
        "dialogue": "Our champion takes the top spot on the winner's podium! Headlights flash like disco lights while our proud little boy raises the golden trophy high!",
        "sfx": "[SFX: Triumphant brass victory fanfare, disco horn beeps, child laughing and hugging the toy car tightly]",
        "vfx": "Golden trophy shining with lens flare starbursts, sparkling disco headlight reflections, celebratory balloons",
        "story_link": "The warm final farewell and movie closing to viewers",
        "is_closing": False
    },
    {
        "scene_index": 60,
        "act": "Act 8: The Grand Finale & Penutup",
        "milestone": "PENUTUP: Heartfelt Movie Farewell",
        "action": "In a warm emotional close-up, {subject} holds {product} gently in two hands, looking straight into the camera lens with a loving smile and waving goodbye as the scene fades into a warm sunset glow.",
        "dialogue": "Thank you so much for joining our grand toy car adventure today, best friends! You are all champions! Keep playing, keep smiling, and see you next time! Bye-bye!",
        "sfx": "[SFX: Warm acoustic lullaby melody, child saying 'Bye-bye friends!', gentle horn beep 'beep-beep', closing applause]",
        "vfx": "Heartfelt close-up of child holding toy car and waving goodbye directly to camera, soft warm vignette fade, movie ending credits atmosphere",
        "story_link": "Grand movie ending (penutup), story complete",
        "is_closing": True
    }
]

