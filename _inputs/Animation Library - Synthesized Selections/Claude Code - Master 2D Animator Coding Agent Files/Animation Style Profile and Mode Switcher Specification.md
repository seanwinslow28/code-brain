Here is the **Style Mode Switcher** specification, derived strictly from the "Animation Style Profiles" and related operational logic sources.

### Module: Style Mode Switcher

#### 1\. Style Profile Registry (style\_profile\_id)

*Definitions derived from the Style Profiles Data Table 1\.*

* **RUBBER\_HOSE\_1920**: "Noodle" physics. Limbs are flexible tubes without joints. Motion is constant (bouncing/swaying) and synchronized to musical beats. No holds.  
* **GOLDEN\_AGE\_1930**: Volumetric realism. Anatomical construction with "cushion" easing (slow-in/slow-out). Prioritizes "sincerity" and fluid mechanics on Ones or Twos.  
* **SCREWBALL\_1940**: Extreme exaggeration. "Staccato" timing (Fast Move $\\to$ Hard Stop). Uses "Zips" and violent distortions. Breaking anatomical limits for comedy.  
* **MODERNIST\_UPA\_1950**: Graphic flatness. Rejects perspective for 2D design. Limited motion ("popping" between poses) on variable framerates (3s/4s). Backgrounds reflect psychology ("Subjective Space").  
* **LIMITED\_TV\_1960**: "Planned Animation" economy. Audio-driven. Separates "Static Body" from "Moving Mouth." Heavy use of loops, cycles, and lateral pans to save drawings.  
* **ANIME\_TRADITIONAL**: Modulation. Dynamic switching between framerates (1s, 2s, 3s) based on intensity. Cinematic camera angles and symbolic effects (speed lines).  
* **GENNDY\_3D\_MODERN**: "Broken Rig" 3D. Pushing 3D models to 2D limits (non-physical deformation). Uses "Genndy Blur" (geometry blends) instead of motion blur.  
* **SPIDER\_VERSE\_HYBRID**: Stepped 3D. Animates on Twos (12fps) to mimic hand-drawn aesthetics. Motion blur is disabled in favor of CMYK offsets or speed lines.

#### 2\. Parameter Override Matrix

*This table dictates how the physics and rendering engines reconfigure when a style is selected.*  
Parameter,RUBBER\_HOSE,GOLDEN\_AGE,SCREWBALL,LIMITED\_TV,SPIDER\_VERSE,GENNDY\_3D,Source  
FPS / Update Rate,Sync\_to\_BPM (Musical),24 (Ones) or 12 (Twos),24 (Ones) for Zips,12 (Twos) or 8 (Threes),12 (Twos) Forced,24 (Ones),"1, 2"  
Interpolation,Linear (Constant Speed),Cubic\_Bezier (Ease In/Out),Zip (1-frame transit),Step (Hold $\\to$ Pop),Step (No Splining),Snappy (Sharp curves),"1, 3"  
Rigidity / Joints,0.0 (No joints/bones),1.0 (Solid volume),0.5 (Flexible/Breakable),1.0 (Rigid/Hinged),1.0 (Solid),0.0 (Broken Rig),1  
Idle State,Always\_Bounce (No holds),Moving\_Hold (Drift),Dead\_Stop (Hard hold),Static (Frozen),Stepped\_Hold,Moving\_Hold,"1, 4"  
Smear Tech,None (Speed Lines only),Drybrush\_Alpha (Textured),Elongated\_Mesh (Stretch),Abstract\_Blur (Symbol),CMYK\_Offset (No Blur),Geo\_Blend (Sub-frame),"1, 5"  
Squash/Stretch,High (Rubber),Moderate (Volume Locked),Extreme (Volume Broken),Low (Muzzle only),Low (Rigid),Extreme (Cartoony),"1, 6"  
Line of Action,Curved (Hose),S-Curve (Flow),Sharp/Angular,Planar/Flat,Graphic/Comic,Silhouette-driven,"1, 7"

#### 3\. Mode-Switch Rules (Decision Logic)

*The agent executes this logic tree to determine the active style\_profile\_id.*

* **IF** Audio\_Track contains Rhythmic\_Music AND Script\_Tone \== "Surreal/Happy":  
* **SET** Style \= **RUBBER\_HOSE\_1920**.  
* *Rule:* Enforce "Musical Sync" (bobbing to the beat). Disable holds; character must remain in constant motion 1\.  
* **IF** Budget \== "Low" OR Pipeline \== "Series/Episodic":  
* **SET** Style \= **LIMITED\_TV\_1960**.  
* *Rule:* Apply "80/20 Static Ratio." Lock body layers; animate only mouth/eyes. Use standardized mouth charts (7-9 visemes) 1, 8\.  
* **IF** Render\_Target \== "Comic\_Book\_Look" OR Aesthetic \== "Hand-Drawn\_3D":  
* **SET** Style \= **SPIDER\_VERSE\_HYBRID**.  
* *Rule:* Disable Motion Blur. Force Frame Rate to "Twos" (12fps). Use CMYK color offsets for fast motion velocity 1, 2\.  
* **IF** Action\_Type \== "Slapstick" AND Intensity \== "High":  
* **SET** Style \= **SCREWBALL\_1940**.  
* *Rule:* Use "Zips" (1-frame transitions). Anticipation and Overshoot must be extreme (breaking anatomical limits) 1\.  
* **IF** Design\_Philosophy \== "Graphic/Abstract" AND Perspective \== "Flat":  
* **SET** Style \= **MODERNIST\_UPA\_1950**.  
* *Rule:* Restrict camera to Planar moves (X/Y panning only). Backgrounds must reflect "Subjective Space" (mood) rather than geography 1, 9\.  
* **IF** Rig\_Type \== "3D" AND Motion\_Feel \== "Snappy/2D":  
* **SET** Style \= **GENNDY\_3D\_MODERN**.  
* *Rule:* Apply "Genndy Blur" (blend sub-frames into current frame). Bias opacity to the leading edge. Break rig joints to achieve silhouette 1, 6\.

