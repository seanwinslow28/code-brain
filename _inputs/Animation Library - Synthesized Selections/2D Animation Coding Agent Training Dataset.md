Here is the training dataset for a 2D animation coding agent, structured into 60 instruction-output pairs across the six core modules.

### Module 1: The Physics Engine (Foundations & Mechanics)

*(Focus: Gravity, Spacing, Arcs, Weight)*  
**1\. Gravity Drop**

* **Instruction:** "Animate a bowling ball falling from a shelf (height 4ft) to the floor."  
* **PLAN:** {"mode": "PHYSICS", "force": "gravity", "fps": 24, "object\_mass": "heavy"}  
* **IMPLEMENT:** {"keys": \[1\], "spacing\_rule": "ODD\_RULE (1:3:5:7)", "path": "vertical\_linear", "squash\_impact": "minimal"}  
* **VERIFY:** {"check": "Is spacing non-linear?", "result": "PASS", "fix": "None"} \[Source: 1, 2\]

**2\. The Parabolic Jump**

* **Instruction:** "Character jumps across a gap. Make the arc feel organic."  
* **PLAN:** {"mode": "ORGANIC", "arc\_type": "parabola", "breakdown\_placement": "fourth\_down\_half\_time"}  
* **IMPLEMENT:** {"keys": \["Start", "Apex", "Land"\], "breakdown\_pos": "Apex\_Y \- 25%", "breakdown\_time": "50%"}  
* **VERIFY:** {"check": "Is path linear?", "result": "FAIL", "fix": "Apply Bezier Curve"} \[Source: 4, 11\]

**3\. Heavy Lift**

* **Instruction:** "Character lifts a heavy box from the ground."  
* **PLAN:** {"weight": "heavy", "timing": "slow", "ease": "heavy\_cushion"}  
* **IMPLEMENT:** {"duration": "24+ frames", "spacing": "extreme\_ease\_in\_out", "anticipation": "down\_before\_up"}  
* **VERIFY:** {"check": "Duration \< 16 frames?", "result": "FAIL (Too fast)", "fix": "Extend to 24 frames"} \[Source: 9, 33\]

**4\. Standard Walk Cycle**

* **Instruction:** "Generate a standard bipedal walk cycle."  
* **PLAN:** {"state\_machine": "WALK", "tempo": "12\_frames\_per\_step", "cycle": "loop"}  
* **IMPLEMENT:** {"beats": {"1": "Contact", "4": "Down", "7": "Pass", "10": "Up"}, "loop\_point": 25}  
* **VERIFY:** {"check": "Foot sliding?", "result": "PASS", "fix": "Lock foot x-translation on ground"} \[Source: 4, 39\]

**5\. Feather Fall**

* **Instruction:** "A feather drifts down to the ground."  
* **PLAN:** {"mode": "FLUID", "force": "air\_resistance", "path": "sine\_wave"}  
* **IMPLEMENT:** {"workflow": "STRAIGHT\_AHEAD", "spacing": "uniform\_slow", "rotation": "oscillating"}  
* **VERIFY:** {"check": "Is spacing Odd Rule?", "result": "FAIL (Correct)", "fix": "Ignore gravity accel"} \[Source: 25, 35\]

**6\. Fast Run**

* **Instruction:** "Character runs fast, entering from left."  
* **PLAN:** {"state\_machine": "RUN", "tempo": "fast (8 fr/step)", "lean": "forward"}  
* **IMPLEMENT:** {"beats": {"1": "Contact", "3": "Down", "5": "Pass", "7": "Up"}, "air\_time": "significant"}  
* **VERIFY:** {"check": "Both feet on ground?", "result": "FAIL (Correct for run)", "fix": "Ensure flight phase"} \[Source: 34, 41\]

**7\. Pendulum Swing**

* **Instruction:** "Animate a clock pendulum swinging."  
* **PLAN:** {"physics": "mechanical", "pivot": "top", "ease": "sine\_wave"}  
* **IMPLEMENT:** {"spacing": "extreme\_cushion\_at\_extremes", "fast\_in\_center": "true", "arc": "perfect\_circular"}  
* **VERIFY:** {"check": "Timing vs Spacing?", "result": "PASS", "fix": "Ensure slow-out/slow-in"} \[Source: 1, 3\]

**8\. Head Turn (Organic)**

* **Instruction:** "Character turns head from left to right."  
* **PLAN:** {"mode": "POSE\_TO\_POSE", "arc": "dip\_down", "overlap": "nose\_trace"}  
* **IMPLEMENT:** {"path": "U\_shape\_arc", "spacing": "cushion\_start\_end", "feature\_lag": "nose\_drags\_1fr"}  
* **VERIFY:** {"check": "Linear rotation?", "result": "FAIL", "fix": "Add arc breakdown"} \[Source: 17, 33\]

**9\. Bouncing Ball (Decay)**

* **Instruction:** "Rubber ball bounces and stops."  
* **PLAN:** {"physics": "energy\_loss", "squash": "impact\_only"}  
* **IMPLEMENT:** {"height\_decay": "60%\_per\_bounce", "timing\_decay": "-2fr\_per\_bounce", "squash": "1\_frame\_contact"}  
* **VERIFY:** {"check": "Sticky squash?", "result": "FAIL", "fix": "Limit scale to 1 frame"} \[Source: 6, 2\]

**10\. Wave (Limb Chain)**

* **Instruction:** "Character waves their arm."  
* **PLAN:** {"mechanics": "kinetic\_chain", "lead": "shoulder"}  
* **IMPLEMENT:** {"offset": "Shoulder(t) \-\> Elbow(t+2) \-\> Wrist(t+4)", "path": "figure\_eight"}  
* **VERIFY:** {"check": "Joints moving simultaneously?", "result": "FAIL", "fix": "Apply offset"} \[Source: 13, 41\]

### Module 2: Fast-Motion Synthesis (Smears & Multiples)

*(Focus: Strobing, Deformation, 1-Frame Durations)*  
**11\. Super Punch**

* **Instruction:** "Character punches forward instantly."  
* **PLAN:** {"action": "ballistic", "velocity": "high", "solution": "ELONGATED\_SMEAR"}  
* **IMPLEMENT:** {"frame\_n": "Start", "frame\_n+1": "Smear\_Mesh(Stretch\_Y)", "frame\_n+2": "Impact"}  
* **VERIFY:** {"check": "Smear duration \> 1?", "result": "FAIL", "fix": "Delete extra frame"} \[Source: 8, 582\]

**12\. Spinning Wheels**

* **Instruction:** "Car wheels spinning at high speed."  
* **PLAN:** {"action": "cyclic", "solution": "MULTIPLES", "spacing": "uneven"}  
* **IMPLEMENT:** {"geometry": "Instance\_3x", "visibility": "Leading\_Edge\_Only", "pattern": "non\_ABA"}  
* **VERIFY:** {"check": "Strobing/Blinking?", "result": "PASS", "fix": "Randomize spacing"} \[Source: 10, 469\]

**13\. Zip Exit**

* **Instruction:** "Character zips off screen to the right."  
* **PLAN:** {"action": "exit", "solution": "MOTION\_TUBE", "anticipation": "opposite\_dir"}  
* **IMPLEMENT:** {"seq": \["Antic(Left)", "Zip(Stretch\_Right)", "Empty\_Frame"\], "blur": "geometry\_stretch"}  
* **VERIFY:** {"check": "Gap between A and B?", "result": "FAIL", "fix": "Elongate mesh to cover gap"} \[Source: 18, 474\]

**14\. Head Whip**

* **Instruction:** "Fast reaction head turn."  
* **PLAN:** {"action": "rotation", "solution": "MINI\_SMEAR", "target": "internal\_features"}  
* **IMPLEMENT:** {"deform": "drag\_eyes/nose", "stretch": "1.2x", "duration": "1\_frame"}  
* **VERIFY:** {"check": "Volume loss?", "result": "PASS", "fix": "None"} \[Source: 7, 471\]

**15\. Wall Impact**

* **Instruction:** "Character slams into a wall."  
* **PLAN:** {"action": "impact", "solution": "COMPRESSION\_SMEAR", "trick": "pre\_impact\_stretch"}  
* **IMPLEMENT:** {"frame\_impact-1": "Touch\_Wall\_Stretch", "frame\_impact": "Extreme\_Squash"}  
* **VERIFY:** {"check": "Visual gap?", "result": "FAIL", "fix": "Bridge gap with stretch"} \[Source: 8, 471\]

**16\. Vibrating Phone**

* **Instruction:** "Phone ringing on table."  
* **PLAN:** {"action": "vibration", "solution": "DOUBLE\_IMAGE", "blur": "none"}  
* **IMPLEMENT:** {"render": "Pos\_A \+ Pos\_B", "opacity": "50/50", "outline": "both\_edges"}  
* **VERIFY:** {"check": "One edge only?", "result": "FAIL", "fix": "Show leading & trailing"} \[Source: 3, 472\]

**17\. Running Legs (Cartoon)**

* **Instruction:** "Legs running in a blur (Roadrunner style)."  
* **PLAN:** {"action": "cyclic\_fast", "solution": "MULTIPLES", "style": "wheel"}  
* **IMPLEMENT:** {"instances": 5, "cull": "trailing\_edge", "color": "solid\_fill\_if\_fast"}  
* **VERIFY:** {"check": "Soupiness?", "result": "PASS", "fix": "Use sharp multiples"} \[Source: 15, 583\]

**18\. 3D Fast Motion (Genndy Style)**

* **Instruction:** "3D character zips across room."  
* **PLAN:** {"render": "3D", "solution": "GENNDY\_BLUR", "method": "sub\_frame\_blend"}  
* **IMPLEMENT:** {"bias": "80%\_leading\_edge", "samples": "stepped", "rig": "break\_joints"}  
* **VERIFY:** {"check": "Muddy silhouette?", "result": "FAIL", "fix": "Bias opacity forward"} \[Source: 15, 6\]

**19\. Spider-Verse Action**

* **Instruction:** "Fast jump in Spider-Verse style."  
* **PLAN:** {"style": "COMIC", "blur": "FALSE", "solution": "CMYK\_OFFSET"}  
* **IMPLEMENT:** {"framerate": "12fps", "effect": "color\_channel\_separation", "smear": "speed\_lines"}  
* **VERIFY:** {"check": "Motion blur enabled?", "result": "FAIL", "fix": "Disable blur"} \[Source: 20, 23\]

**20\. Tumble (Chaos)**

* **Instruction:** "Character falls down a cliff, tumbling."  
* **PLAN:** {"action": "chaos", "solution": "NOODLE\_LIMBS", "rigidity": "0"}  
* **IMPLEMENT:** {"joints": "disabled", "limbs": "S\_curves", "timing": "random"}  
* **VERIFY:** {"check": "Stiff knees?", "result": "FAIL", "fix": "Remove joint constraints"} \[Source: 11, 472\]

### Module 3: Optimization Logic (TV & Limited)

*(Focus: 80/20 Rule, Cel Stacking, Reuse)*  
**21\. Dialogue Scene**

* **Instruction:** "Character speaking a long sentence."  
* **PLAN:** {"budget": "TV", "technique": "CEL\_STACKING", "ratio": "80/20"}  
* **IMPLEMENT:** {"layer\_1": "Static\_Body", "layer\_2": "Mouth\_Loop", "visemes": "7\_standard"}  
* **VERIFY:** {"check": "Body moving?", "result": "FAIL", "fix": "Freeze body layer"} \[Source: 9, 126\]

**22\. Walking Pan**

* **Instruction:** "Character walking down a long hallway."  
* **PLAN:** {"technique": "REPEAT\_PAN", "bg": "loop", "char": "walk\_cycle"}  
* **IMPLEMENT:** {"char\_pos": "center\_screen", "bg\_vel": "-stride\_length", "sync": "no\_foot\_skate"}  
* **VERIFY:** {"check": "BG loop obvious?", "result": "FAIL", "fix": "Syncopate elements"} \[Source: 22, 593\]

**23\. Reaction Shot**

* **Instruction:** "Character listens to another person talking."  
* **PLAN:** {"action": "listen", "technique": "MOVING\_HOLD", "alive": "true"}  
* **IMPLEMENT:** {"pose": "static", "drift": "1%\_variance", "blink\_rate": "every\_3s"}  
* **VERIFY:** {"check": "Dead pixels?", "result": "FAIL", "fix": "Add trace-back"} \[Source: 6, 130\]

**24\. Crowd Scene**

* **Instruction:** "A crowd of people cheering in background."  
* **PLAN:** {"budget": "low", "technique": "CYCLE\_LOOPS", "framerate": "6fps (fours)"}  
* **IMPLEMENT:** {"assets": \["Cheer\_A", "Cheer\_B"\], "offset": "random\_start\_times"}  
* **VERIFY:** {"check": "Unison movement?", "result": "FAIL", "fix": "Offset start frames"} \[Source: 1, 566\]

**25\. Phone Call**

* **Instruction:** "Close up on character on phone."  
* **PLAN:** {"technique": "PARTIAL\_ANIM", "focus": "mouth/eyes"}  
* **IMPLEMENT:** {"arm": "static\_holding\_phone", "mouth": "sync\_to\_audio", "eyes": "darts"}  
* **VERIFY:** {"check": "Floating head?", "result": "FAIL", "fix": "Mask neck seam"} \[Source: 2, 129\]

**26\. Shock Take (Reuse)**

* **Instruction:** "Character is shocked by news."  
* **PLAN:** {"technique": "BANK\_RETRIEVAL", "asset": "Generic\_Take\_01"}  
* **IMPLEMENT:** {"action": "reuse\_asset", "hold": "4\_seconds", "shake": "camera\_layer"}  
* **VERIFY:** {"check": "Asset mismatch?", "result": "PASS", "fix": "None"} \[Source: 3, 126\]

**27\. Driving (Interior)**

* **Instruction:** "Two characters driving in a car."  
* **PLAN:** {"technique": "MULTI\_PLANE", "char": "static\_bounce", "bg": "scroll"}  
* **IMPLEMENT:** {"layer\_1": "Car\_Interior (Static)", "layer\_2": "BG\_City (Scroll)", "cam": "vertical\_shake"}  
* **VERIFY:** {"check": "Smooth ride?", "result": "FAIL", "fix": "Add camera shake"} \[Source: 46, 593\]

**28\. Impact (Cut-Away)**

* **Instruction:** "Car crashes into wall."  
* **PLAN:** {"budget": "TV", "technique": "OMISSION", "sfx": "heavy"}  
* **IMPLEMENT:** {"frame\_n": "Pre-impact", "frame\_n+1": "White\_Frame/Zap", "frame\_n+2": "Wreckage"}  
* **VERIFY:** {"check": "Animated collision?", "result": "FAIL", "fix": "Remove frames, use FX"} \[Source: 16, 593\]

**29\. Typing**

* **Instruction:** "Character typing at a computer."  
* **PLAN:** {"technique": "CYCLE\_2\_FRAME", "layer": "arms\_only"}  
* **IMPLEMENT:** {"body": "frozen", "arms": "Frame\_A/Frame\_B\_Loop", "fps": "12"}  
* **VERIFY:** {"check": "Complex finger anim?", "result": "FAIL", "fix": "Simplify to blur"} \[Source: 4, 126\]

**30\. Zoom In**

* **Instruction:** "Camera zooms in on static building."  
* **PLAN:** {"technique": "CAMERA\_MOVE", "asset": "High\_Res\_Still"}  
* **IMPLEMENT:** {"scale": "100% \-\> 150%", "interpolation": "linear", "new\_drawings": "0"}  
* **VERIFY:** {"check": "Pixelation?", "result": "PASS", "fix": "Check asset res"} \[Source: 39, 138\]

### Module 4: Stylistic Parameters (History & Rendering)

*(Focus: Physics rules per era)*  
**31\. Rubber Hose Dance**

* **Instruction:** "Character dances in 1920s style."  
* **PLAN:** {"style": "RUBBER\_HOSE", "physics": "no\_joints", "sync": "musical\_beat"}  
* **IMPLEMENT:** {"limbs": "curved\_tubes", "idle": "bounce\_loop", "holds": "false"}  
* **VERIFY:** {"check": "Sharp elbows?", "result": "FAIL", "fix": "Curve deformers"} \[Source: 14, 105\]

**32\. Spider-Verse Swing**

* **Instruction:** "Spider-Man swings through city."  
* **PLAN:** {"style": "SPIDER\_VERSE", "framerate": "modulated", "blur": "none"}  
* **IMPLEMENT:** {"fps": "12 (Twos)", "fast\_bits": "24 (Ones)", "smear": "CMYK\_offset"}  
* **VERIFY:** {"check": "Smooth spline?", "result": "FAIL", "fix": "Step curves"} \[Source: 29, 109\]

**33\. UPA Walk**

* **Instruction:** "Character walks in 1950s modernist style."  
* **PLAN:** {"style": "UPA", "design": "flat/graphic", "depth": "none"}  
* **IMPLEMENT:** {"movement": "planar\_xy", "poses": "graphic\_shape", "framerate": "8fps (Threes)"}  
* **VERIFY:** {"check": "Perspective change?", "result": "FAIL", "fix": "Flatten Z-axis"} \[Source: 5, 107\]

**34\. Anime Impact**

* **Instruction:** "Powerful punch impact in Anime style."  
* **PLAN:** {"style": "ANIME", "modulation": "variable", "bg": "speed\_lines"}  
* **IMPLEMENT:** {"impact\_frame": "negative\_color", "hold": "3\_frames (Tome)", "bg": "radial\_blur"}  
* **VERIFY:** {"check": "Constant FPS?", "result": "FAIL", "fix": "Modulate 1s/3s"} \[Source: 25, 117\]

**35\. Screwball Zip**

* **Instruction:** "Character runs away instantly (Tex Avery)."  
* **PLAN:** {"style": "SCREWBALL", "transition": "zip", "anticipation": "extreme"}  
* **IMPLEMENT:** {"seq": \["Antic\_deform", "Empty\_Screen", "Dust\_Cloud"\], "timing": "1\_frame\_transit"}  
* **VERIFY:** {"check": "Ease out?", "result": "FAIL", "fix": "Remove in-betweens"} \[Source: 7, 107\]

**36\. 1930s Dialogue**

* **Instruction:** "Character talks in Disney 1930s style."  
* **PLAN:** {"style": "GOLDEN\_AGE", "volume": "consistent", "acting": "sincere"}  
* **IMPLEMENT:** {"squash": "volumetric\_preserve", "fps": "24 (Ones)", "hands": "follow\_through"}  
* **VERIFY:** {"check": "Twinning?", "result": "FAIL", "fix": "Offset limbs"} \[Source: 5, 106\]

**37\. Genndy 3D**

* **Instruction:** "3D character reacts wildly."  
* **PLAN:** {"style": "GENNDY\_3D", "rig": "broken", "blur": "geo\_blend"}  
* **IMPLEMENT:** {"pose": "broken\_joints", "transition": "1\_frame", "smear": "multi\_instance"}  
* **VERIFY:** {"check": "Floaty?", "result": "FAIL", "fix": "Snap transition"} \[Source: 15, 110\]

**38\. Noir Shadow**

* **Instruction:** "Detective lights a match in shadows."  
* **PLAN:** {"style": "NOIR/GRAPHIC", "lighting": "high\_contrast", "motion": "minimal"}  
* **IMPLEMENT:** {"emphasis": "light\_shape", "movement": "slow\_ease", "fps": "12"}  
* **VERIFY:** {"check": "Too much detail?", "result": "FAIL", "fix": "Merge shadows"} \[Source: 35, 102\]

**39\. Retro Game Idle**

* **Instruction:** "16-bit character idle breathing."  
* **PLAN:** {"style": "PIXEL/RETRO", "cycle": "2\_frame\_bounce", "interp": "none"}  
* **IMPLEMENT:** {"pose\_A": "y=0", "pose\_B": "y=-1px", "fps": "4 (6fps)"}  
* **VERIFY:** {"check": "Sub-pixel move?", "result": "FAIL", "fix": "Snap to grid"} \[Source: 1, 103\]

**40\. Stop-Motion Emulation**

* **Instruction:** "3D character moving like claymation."  
* **PLAN:** {"style": "STOP\_MOTION", "fps": "12", "blur": "none"}  
* **IMPLEMENT:** {"interp": "stepped", "imperfection": "jitter\_light", "pop": "on\_contact"}  
* **VERIFY:** {"check": "Motion blur?", "result": "FAIL", "fix": "Disable"} \[Source: 22, 109\]

### Module 5: The Acting Engine (Posing & Performance)

*(Focus: Readability, Twinning, Offsets)*  
**41\. Surprise Take**

* **Instruction:** "Character is shocked by a loud noise."  
* **PLAN:** {"emotion": "SURPRISE", "pattern": "Antic \-\> Take \-\> Settle", "eyes": "lead"}  
* **IMPLEMENT:** {"squash": "down (2fr)", "stretch": "up (1fr)", "hold": "open\_mouth (12fr)"}  
* **VERIFY:** {"check": "Symmetric?", "result": "FAIL", "fix": "Offset arms 2fr"} \[Source: 10, 603\]

**42\. Sad Walk**

* **Instruction:** "Character walks sadly."  
* **PLAN:** {"emotion": "SAD", "power\_center": "hips", "line\_of\_action": "C\_curve\_down"}  
* **IMPLEMENT:** {"speed": "slow (32fr cycle)", "head": "droop", "arms": "minimal\_swing"}  
* **VERIFY:** {"check": "Chest leading?", "result": "FAIL", "fix": "Lead with hips"} \[Source: 2, 39\]

**43\. Heroic Stance**

* **Instruction:** "Hero stands triumphantly on a hill."  
* **PLAN:** {"emotion": "HEROIC", "power\_center": "chest", "staging": "low\_angle"}  
* **IMPLEMENT:** {"chest": "expanded", "legs": "wide", "cape": "wind\_sim"}  
* **VERIFY:** {"check": "Silhouette clear?", "result": "PASS", "fix": "None"} \[Source: 21, 604\]

**44\. Refusal**

* **Instruction:** "Character says 'No' firmly."  
* **PLAN:** {"action": "refuse", "lead": "eyes", "gesture": "head\_shake"}  
* **IMPLEMENT:** {"eyes": "narrow", "head": "sharp\_turn", "hands": "block\_gesture"}  
* **VERIFY:** {"check": "Eye lead?", "result": "PASS (Eyes \-2fr)", "fix": "None"} \[Source: 27, 603\]

**45\. Thinking**

* **Instruction:** "Character considers an idea."  
* **PLAN:** {"action": "thought", "technique": "EYE\_DARTS", "hold": "moving"}  
* **IMPLEMENT:** {"eyes": "look\_up\_left", "dart\_duration": "2fr", "head": "tilt\_slow"}  
* **VERIFY:** {"check": "Slow eyes?", "result": "FAIL", "fix": "Snap eyes"} \[Source: 16, 603\]

**46\. Heavy Laugh**

* **Instruction:** "Santa Claus laughing."  
* **PLAN:** {"action": "laugh", "physics": "mass\_jiggle", "lead": "belly"}  
* **IMPLEMENT:** {"shoulders": "up/down", "head": "back", "belly": "delayed\_bounce"}  
* **VERIFY:** {"check": "Volume conservation?", "result": "PASS", "fix": "None"} \[Source: 1, 606\]

**47\. Sneaking**

* **Instruction:** "Character sneaks past a sleeping guard."  
* **PLAN:** {"action": "sneak", "pose": "extreme\_crouch", "contact": "toe\_first"}  
* **IMPLEMENT:** {"stride": "long", "hold": "on\_pass\_pos", "timing": "slow\_in\_out"}  
* **VERIFY:** {"check": "Weight noise?", "result": "FAIL", "fix": "Soft contacts"} \[Source: 6, 603\]

**48\. Fear Reaction**

* **Instruction:** "Character sees a ghost."  
* **PLAN:** {"emotion": "FEAR", "pose": "retreat", "pupils": "contract"}  
* **IMPLEMENT:** {"spine": "reverse\_C", "hands": "protect\_face", "shudder": "vibration"}  
* **VERIFY:** {"check": "Pupils normal?", "result": "FAIL", "fix": "Shrink pupils"} \[Source: 35, 603\]

**49\. Pointing**

* **Instruction:** "Character points at a door."  
* **PLAN:** {"action": "gesture", "mechanics": "successive\_breaking", "arc": "hand\_path"}  
* **IMPLEMENT:** {"shoulder": "frame\_1", "elbow": "frame\_3", "wrist": "frame\_5"}  
* **VERIFY:** {"check": "Linear path?", "result": "FAIL", "fix": "Arc wrist"} \[Source: 12, 603\]

**50\. Double Take**

* **Instruction:** "Character looks, looks away, then looks back fast."  
* **PLAN:** {"pattern": "LOOK\_AWAY\_LOOK", "timing": "contrast"}  
* **IMPLEMENT:** {"look\_1": "12fr", "away": "4fr", "look\_2": "zip (2fr) \+ settle"}  
* **VERIFY:** {"check": "Even timing?", "result": "FAIL", "fix": "Sharpen contrast"} \[Source: 31, 604\]

### Module 6: Pipeline Architecture (Data & Workflow)

*(Focus: X-Sheets, Gates, Handoffs)*  
**51\. X-Sheet Generation**

* **Instruction:** "Create exposure sheet for 'Hello World' audio."  
* **PLAN:** {"task": "X\_SHEET", "input": "audio\_wav", "framerate": "24"}  
* **IMPLEMENT:** {"phonemes": \["H", "E", "L", "O", "W", "R", "L", "D"\], "frames": \[2-9\]}  
* **VERIFY:** {"check": "Closed mouth on silence?", "result": "PASS", "fix": "None"} \[Source: 16, 670\]

**52\. Layout Camera**

* **Instruction:** "Plan camera truck-in on character."  
* **PLAN:** {"task": "LAYOUT", "fielding": "12F \-\> 6F", "duration": "48fr"}  
* **IMPLEMENT:** {"start": "Wide\_Shot", "end": "CU", "curve": "ease\_in\_out"}  
* **VERIFY:** {"check": "Resolution limit?", "result": "PASS", "fix": "Check DPI"} \[Source: 14, 601\]

**53\. Asset Reuse Query**

* **Instruction:** "Check for existing walk cycle before animating."  
* **PLAN:** {"task": "ASSET\_MGMT", "query": "walk\_cycle\_sad", "library": "Bank"}  
* **IMPLEMENT:** {"search": "char\_A\_walk\*", "result": "Found v03"}  
* **VERIFY:** {"check": "Match angle?", "result": "PASS", "fix": "None"} \[Source: 3, 126\]

**54\. Palette Validation**

* **Instruction:** "Verify character colors for final render."  
* **PLAN:** {"task": "INK\_PAINT", "ref": "Model\_Sheet\_vFinal"}  
* **IMPLEMENT:** {"scan": "pixel\_values", "compare": "master\_palette\_RGB"}  
* **VERIFY:** {"check": "Deviation?", "result": "FAIL (Wrong Blue)", "fix": "Auto-correct"} \[Source: 25, 137\]

**55\. Scene Export Spec**

* **Instruction:** "Export for UK Broadcast."  
* **PLAN:** {"task": "DELIVERY", "standard": "PAL", "res": "1080p"}  
* **IMPLEMENT:** {"fps": "25", "audio": "-23 LUFS", "codec": "ProRes 422"}  
* **VERIFY:** {"check": "24fps artifact?", "result": "PASS (Converted)", "fix": "None"} \[Source: 8, 623\]

**56\. Twinning Check (Auto)**

* **Instruction:** "Run QA on blocking pass."  
* **PLAN:** {"task": "QA\_GATE", "filter": "TWINNING"}  
* **IMPLEMENT:** {"scan\_curves": "L\_Hand vs R\_Hand", "threshold": "Identical keys"}  
* **VERIFY:** {"check": "Symmetry found?", "result": "FAIL", "fix": "Offset R\_Hand \+2fr"} \[Source: 27, 139\]

**57\. Audio Sync Check**

* **Instruction:** "Ensure lip sync hits are correct."  
* **PLAN:** {"task": "TIMING", "rule": "AUDIO\_LEAD"}  
* **IMPLEMENT:** {"audio\_peak": "frame\_10", "mouth\_open": "frame\_8"}  
* **VERIFY:** {"check": "Visual leads audio?", "result": "PASS", "fix": "Shift \-2 frames"} \[Source: 6, 606\]

**58\. Layer Separation (Cel Stack)**

* **Instruction:** "Prepare file for limited animation output."  
* **PLAN:** {"task": "OPTIMIZATION", "structure": "CEL\_STACK"}  
* **IMPLEMENT:** {"Level\_1": "Body\_Static", "Level\_2": "Head", "Level\_3": "Mouth"}  
* **VERIFY:** {"check": "Neck seam?", "result": "FAIL", "fix": "Add collar patch"} \[Source: 9, 129\]

**59\. Silhouette Check**

* **Instruction:** "Verify readability of key poses."  
* **PLAN:** {"task": "QA\_STAGING", "method": "BINARY\_MASK"}  
* **IMPLEMENT:** {"render": "Black\_White", "measure": "negative\_space"}  
* **VERIFY:** {"check": "Limbs occluded?", "result": "FAIL", "fix": "Adjust camera/pose"} \[Source: 10, 135\]

**60\. Final Render Config**

* **Instruction:** "Render final frames for compositing."  
* **PLAN:** {"task": "RENDER", "format": "EXR\_Sequence", "passes": "Beauty+ZDepth"}  
* **IMPLEMENT:** {"resolution": "1920x1080", "samples": "High", "alpha": "Premultiplied"}  
* **VERIFY:** {"check": "Missing frames?", "result": "PASS", "fix": "Re-queue"} \[Source: 8, 623\]

