Here is the **Animation Style Profiles & Operational Logic Spec**, designed to allow a coding agent to emulate specific historical and aesthetic behaviors by swapping parameter sets.

### Module 4: Style Mode Switcher

#### 1\. Mental Model

* **Concept:** Styles are not merely aesthetic "skins" but distinct **physics and resource constraints**. "Rubber Hose" is a physics engine without joints; "Limited TV" is a compression algorithm for labor.  
* **Agent Goal:** To switch the Simulation\_Engine and Render\_Pipeline parameters to match the constraints of the target era, overriding standard realism settings.  
* **Citation:** "Styles... are sets of constraints (CPU limits, budget limits, physics logic) that a coding agent can toggle." 1\.

#### 2\. Style Specifications (The "Modes")

##### A. Mode: RUBBER\_HOSE\_1920

* **Definition:** "Noodle" physics where limbs are flexible tubes without rigid joints. Motion is constant and rhythm-driven.  
* **Parameter Presets:**  
* Joint\_Rigidity: **0.0** (Disable skeletal constraints).  
* Idle\_State: **Always\_Bounce** (Character must never be static).  
* Sync\_Source: **Audio\_BPM** (Vertical bounce frequency locks to music beat).  
* Easing: **None/Linear** (Constant speed fluid motion). 2, 3\.  
* **Authentic Motion:**  
* Limbs curve continuously (no elbows/knees). The character bobs to a musical beat even when standing still. Action occurs on a flat 2D plane (Z=0). 2, 4\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Stiff" Joints.** Sharp angles at elbows/knees.  
* *Fix:* Apply Curve\_Deformer to limb meshes; remove bone constraints. 4\.  
* *Mistake:* **"Dead" Holds.** Character stops moving completely.  
* *Fix:* Force Idle\_Loop to Bob\_Cycle synced to beat. 4\.

##### B. Mode: GOLDEN\_AGE\_1930

* **Definition:** Volumetric realism ("Solid Drawing") with "Cushioning" (fluid acceleration/deceleration).  
* **Parameter Presets:**  
* FPS: **24 (Ones)** or **12 (Twos)**.  
* Interpolation: **Cubic\_Bezier** (Ease-in/Ease-out).  
* Volume\_Lock: **True** ($X \\times Y \\times Z \\approx 1.0$).  
* Smear\_Type: **Drybrush\_Alpha** (Textured trail). 3, 5\.  
* **Authentic Motion:**  
* Weight is felt through spacing (slow-in/slow-out). Characters have anatomical solidity. Arcs are circular or parabolic. 3, 5\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Floaty" Motion.** Even spacing between keys.  
* *Fix:* Apply Cubic\_Ease to spacing curves. 5\.  
* *Mistake:* **"Shrinking" Volume.** Object scales down on one axis without compensating.  
* *Fix:* Enforce Volume\_Conservation constraint ($Scale\_{\\perp} \= 1/\\sqrt{Scale\_{\\parallel}}$). 5, 6\.

##### C. Mode: SCREWBALL\_1940

* **Definition:** Extreme exaggeration and "Staccato" timing. Physics are broken for comedic effect.  
* **Parameter Presets:**  
* Transition\_Type: **Zip** (1-frame travel time).  
* Overshoot\_Amp: **Extreme** (\> 20% past target).  
* Hold\_Type: **Dead\_Stop** (Hard accent).  
* Smear\_Geo: **Stretch\_Mesh** (Elongated in-between). 3, 7\.  
* **Authentic Motion:**  
* Fast moves happen in 1 frame (a "Zip"). Stops are sudden ("Hard Accent"). Characters deform wildly ("Takes") before settling. 3, 7\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Disney Softness."** Too much cushioning; slow transitions.  
* *Fix:* Delete in-betweens to create Zips. Increase Overshoot amplitude. 7\.

##### D. Mode: LIMITED\_TV\_1960

* **Definition:** "Planned Animation" optimized for budget. Sound drives visuals.  
* **Parameter Presets:**  
* Static\_Ratio: **0.8** (80% of pixels static).  
* Update\_Freq: **2** (Twos) or **3** (Threes).  
* Layer\_Split: **True** (Separate Body/Mouth).  
* Cycle\_Loop: **Infinite** (Reuse walks/runs). 3, 8\.  
* **Authentic Motion:**  
* Characters hold poses for seconds. Only mouths or specific limbs move. Backgrounds loop. "Necktie rule" masks head/body separation. 3, 8\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Full Animation."** Body moves constantly during dialogue.  
* *Fix:* Freeze Body\_Layer. Quantize Mouth\_Layer to 7–9 visemes. 8\.  
* *Mistake:* **"Floating Head."** Head moves independent of body, revealing gap.  
* *Fix:* Ensure collar/necktie asset masks the seam. 9\.

##### E. Mode: ANIME\_TRADITIONAL

* **Definition:** "Modulation." Dynamic framerates based on narrative intensity.  
* **Parameter Presets:**  
* FPS\_Modulation: **Dynamic** (Switch 8fps $\\leftrightarrow$ 24fps).  
* Hold\_Style: **Tome** (High-intensity stop-motion hold).  
* Smear\_Type: **Speed\_Lines** (Background radial lines).  
* Cam\_Move: **Aggressive** (Rack focus, static pans). 3, 10\.  
* **Authentic Motion:**  
* Jerky low framerates (3s) for conversation; high framerates (1s) for combat. "Slide Motion" (panning static art) used for establishing shots. 10, 11\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Western Smoothness."** Constant 24fps or 12fps.  
* *Fix:* Apply Modulation\_Controller. Reduce lip-sync to 3-step cycle (Open-Middle-Close). 10\.

##### F. Mode: MODERN\_HYBRID\_SPIDER

* **Definition:** "Stepped" 3D animation mimicking print media imperfections.  
* **Parameter Presets:**  
* Interpolation: **Stepped** (No Splines).  
* Motion\_Blur: **False** (Disabled).  
* FPS: **12 (Twos)** forced.  
* Effect: **CMYK\_Offset** (Misprint). 3, 12\.  
* **Authentic Motion:**  
* Crisp, non-blurred frames. Movement holds for 2 frames. Fast motion is conveyed via color channel offsets (misprints) or 2D "speed lines," not pixel blur. 12, 13\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Video Game Look."** Smooth 60fps interpolation or Gaussian blur.  
* *Fix:* Force Stepped\_Interpolation. Disable blur shader. Apply CMYK\_Offset based on velocity. 12\.

##### G. Mode: 3D\_GENNDY

* **Definition:** 2D "Snap" applied to 3D rigs. Geometry smears instead of blur.  
* **Parameter Presets:**  
* Rig\_Limits: **Off** (Allow bone stretching).  
* Motion\_Blur: **Geo\_Blend** (Sub-frame geometry).  
* Bias: **Leading\_Edge** (Opacity weighted to front).  
* Transition: **\< 2 Frames**. 3, 14\.  
* **Authentic Motion:**  
* Poses pop instantly (1-2 frames). Fast moves utilize "Genndy Blur" (multiple geometry instances blended in one frame). Silhouettes are pushed beyond rig limits. 14, 15\.  
* **Fake-Looking Mistakes & Fixes:**  
* *Mistake:* **"Interpolated 3D."** Slow, floaty transitions; muddy standard blur.  
* *Fix:* Snap transitions to 1 frame. Generate Sub\_Frame geometry blend. 14\.

#### 3\. Operational Rules (Global Constraints)

* **Mode-Switch Trigger:** The agent must evaluate the Context\_Input (Audio, Script, Budget) to select the correct profile.  
* *Rule:* **IF** Budget \== "Low" **THEN** LIMITED\_TV. 3, 16\.  
* *Rule:* **IF** Style \== "Comic" **THEN** MODERN\_HYBRID. 3\.  
* **Smear Logic Override:**  
* For RUBBER\_HOSE: **Disable** geometry smears. Use only speed lines. 3\.  
* For SCREWBALL: **Enable** Elongated\_Inbetween (Mesh Stretch). 3\.  
* For GENNDY\_3D: **Enable** Geo\_Blend (Sub-frame instances). 3\.  
* **Framerate Lock:**  
* MODERN\_HYBRID strictly enforces **Twos (12fps)** unless Velocity is extreme. 12, 13\.  
* LIMITED\_TV enforces **Threes (8fps)** for non-dialogue holds. 17\.

