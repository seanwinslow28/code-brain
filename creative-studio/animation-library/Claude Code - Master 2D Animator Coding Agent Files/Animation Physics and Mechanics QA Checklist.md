Here is the **QA Checklist for Module 1: Foundations**, designed for a coding agent to validate 2D/3D animation data against the core canon.

### Category A: Physics & Spacing Logic

**1\. Gravity Acceleration Check (The Odd Rule)**

* **What to check:** Vertical displacement of a falling object starting from rest.  
* **Detection:** Calculate delta Y between frames $f$ and $f+1$. Verify if ratios match the odd number sequence (1, 3, 5, 7).  
* **Pass/Fail:** **Fail** if spacing is linear (1:1:1) or random. **Pass** if spacing increases by $\\approx$ 2 units per frame (Odd Rule progression).  
* **Citation:** "For a falling object, the spacings follow... the odd numbers... 1:3:5:7." 1, 2\.

**2\. Parabolic Arc Breakdown (Fourth Down Rule)**

* **What to check:** The position of the breakdown pose (mid-point in time) for a curved trajectory.  
* **Detection:** Calculate vertical distance from Apex ($Y\_{max}$) to Ground ($Y\_{min}$). Check object $Y$ position at 50% of duration.  
* **Pass/Fail:** **Pass** if object is at $Y\_{apex} \- (0.25 \\times TotalHeight)$. **Fail** if object is at exact geometric center (linear interp).  
* **Citation:** "Place breakdown at 50% time, but only 25% of the vertical distance from the apex." 3, 4\.

**3\. Volumetric Conservation (Squash & Stretch)**

* **What to check:** Object volume stability during deformation.  
* **Detection:** Calculate $Volume \= Scale\_X \\times Scale\_Y \\times Scale\_Z$ at every frame.  
* **Pass/Fail:** **Pass** if product $\\approx 1.0$. **Fail** if volume deviates $\> 10\\%$ (object is growing/shrinking).  
* **Citation:** "Scale\_X \= 1 / sqrt(Scale\_Y)... Volume must remain constant." 5, 2\.

**4\. Velocity-Based Strobing**

* **What to check:** Discrete displacement relative to object size.  
* **Detection:** Measure distance(Position\_A, Position\_B). Compare to Object\_Width.  
* **Pass/Fail:** **Fail** if Displacement \> Width AND Smear\_Flag \== False. (Requires smear or motion blur).  
* **Citation:** "If (Position\_Frame\_B \- Position\_Frame\_A) \> Object\_Width... trigger Smear Generation." 3, 6\.

**5\. Linear Interpolation ("Floaty" Motion)**

* **What to check:** Spacing consistency on non-mechanical objects.  
* **Detection:** Analyze f-curve tangents. Check if derivative(velocity) \== 0 (constant speed) for $\> 6$ frames.  
* **Pass/Fail:** **Fail** if spacing is mathematically even. **Pass** if Ease-In or Ease-Out is detected.  
* **Citation:** "Spacing graph shows equidistant keys (Linear Interpolation)... 'Floaty' Motion." 7, 6\.

### Category B: Timing & Frame Rate

**6\. The Readability Floor**

* **What to check:** Minimum duration of a static pose or hold.  
* **Detection:** Count consecutive frames where Velocity \< Threshold.  
* **Pass/Fail:** **Fail** if Hold\_Duration \< 3 frames. **Pass** if Hold\_Duration \>= 3 (preferably 6-12).  
* **Citation:** "Every major pose must be held for \>= 3 frames to be readable by the human eye." 5, 2\.

**7\. Variable Exposure (Ones vs. Twos)**

* **What to check:** Update frequency based on action type.  
* **Detection:** Check Camera\_Velocity.  
* **Pass/Fail:** **IF** Camera\_Pan \> 0: **Fail** if animation is on Twos (causes strobing). **Pass** if forced to Ones (24fps).  
* **Citation:** "When the camera is panning... add in single inbetweens so it doesn't strobe\!" 8, 3\.

**8\. Fast Action Duration**

* **What to check:** Frame count for reaction/impact shots.  
* **Detection:** Measure duration of state Action\_Type \== "Reaction".  
* **Pass/Fail:** **Pass** if Duration is 2–4 frames. **Fail** if Duration \> 6 (feels sluggish).  
* **Citation:** "Fast Reaction/Surprise: 2–4 frames." 9, 4\.

**9\. Heavy Effort Timing**

* **What to check:** Frame count for lifting/pushing heavy mass.  
* **Detection:** Measure duration of state Action\_Type \== "Heavy\_Lift".  
* **Pass/Fail:** **Pass** if Duration is 16–24+ frames. **Fail** if Duration \< 12 (lacks weight).  
* **Citation:** "Heavy Effort: 16–24 frames." 9\.

**10\. Smear Durability**

* **What to check:** Exposure time of a deformed smear frame.  
* **Detection:** Check duration of Scale \> 1.0 (Stretch) events.  
* **Pass/Fail:** **Fail** if Duration \> 1 frame ("Sticky Smear"). **Pass** if Duration \== 1\.  
* **Citation:** "Smear\_Duration \<= 1 frame. Never hold a smear for \>= 2 frames." 3, 2\.

### Category C: Mechanics & Posing

**11\. Kinetic Chain Order (Successive Breaking of Joints)**

* **What to check:** Timing offset between parent and child joints.  
* **Detection:** Compare Start\_Time(Rotation) for Shoulder vs. Elbow vs. Wrist.  
* **Pass/Fail:** **Pass** if Time(Shoulder) \< Time(Elbow) \< Time(Wrist). **Fail** if all start at $t=0$.  
* **Citation:** "Child joints must rotate 1–3 frames later than their parent joint." 5, 2\.

**12\. Twinning Detection**

* **What to check:** Symmetry in limb positioning and timing.  
* **Detection:** Compare Left\_Arm.Keyframe vs. Right\_Arm.Keyframe.  
* **Pass/Fail:** **Fail** if L\_Value \== R\_Value AND L\_Time \== R\_Time. **Pass** if offset by $\\ge 2$ frames.  
* **Citation:** "Flag if Left/Right limbs have identical values; apply offset." 10, 7\.

**13\. Anticipation Vector**

* **What to check:** Direction of movement prior to main action.  
* **Detection:** Calculate vector $V\_1$ (Start $\\rightarrow$ Antic) and $V\_2$ (Antic $\\rightarrow$ Target).  
* **Pass/Fail:** **Pass** if $dot\\\_product(V\_1, V\_2) \< 0$ (Opposite directions).  
* **Citation:** "Before moving... in direction V, it must first move in direction \-V." 2\.

**14\. Silhouette Validity**

* **What to check:** Visual clarity of the pose.  
* **Detection:** Calculate Visible\_Surface\_Area of torso vs. limbs.  
* **Pass/Fail:** **Fail** if limbs occlude $\> 30\\%$ of torso (Blob effect).  
* **Citation:** "Check Visible\_Surface\_Area to ensure limbs are not occluding the torso." 10, 11\.

**15\. Arc Trajectories**

* **What to check:** Spatial path of end-effectors (wrists/noses).  
* **Detection:** Fit positions to a curve.  
* **Pass/Fail:** **Fail** if path is Linear (Straight line). **Pass** if path matches Bézier/Spline curve.  
* **Citation:** "Spatial paths for organic objects must map to Bézier curves; Linear paths are rejected." 5\.

**16\. Overshoot Geometry**

* **What to check:** Stop position relative to target.  
* **Detection:** Check peak value vs. final resting value.  
* **Pass/Fail:** **Pass** if Peak\_Val extends past Rest\_Val before returning.  
* **Citation:** "Extremities... overshoot more than solid masses." 9\.

**17\. Power Center Consistency**

* **What to check:** Velocity origin point.  
* **Detection:** Identify the root node initiating translation.  
* **Pass/Fail:** **Pass** if root matches character definition (e.g., Chest for Hero, Hips for Heavy).  
* **Citation:** "The origin point of a character's movement force." 12, 13\.

### Category D: Walk Cycle State Machine

**18\. Contact State**

* **What to check:** Foot position at Frame 1 (or cycle start).  
* **Detection:** Heel\_Y \== Ground\_Y. Legs at maximum extension.  
* **Pass/Fail:** **Fail** if knee is bent $\> 10^\\circ$ on forward leg.  
* **Citation:** "Contact: Leading heel strikes ground." 2, 14\.

**19\. Down State (Recoil)**

* **What to check:** Lowest vertical position.  
* **Detection:** Check Head\_Y at Frame 4 (standard march).  
* **Pass/Fail:** **Pass** if Head\_Y \< Contact\_Head\_Y.  
* **Citation:** "Down (Recoil): Lowest hip height, weight absorbs." 2\.

**20\. Passing State**

* **What to check:** Leg crossover.  
* **Detection:** Check Frame 7\.  
* **Pass/Fail:** **Pass** if Free\_Leg\_Z \== Stance\_Leg\_Z (Crossing point).  
* **Citation:** "Passing: Free leg crosses support leg; hips rise." 2\.

**21\. Up State (Push-off)**

* **What to check:** Highest vertical position.  
* **Detection:** Check Frame 10\.  
* **Pass/Fail:** **Pass** if Head\_Y is at maximum.  
* **Citation:** "Up (High Point): Highest hip height; push-off." 2\.

### Category E: Workflow & Pipeline

**22\. Dead Hold Prevention (Moving Hold)**

* **What to check:** Value variance during a "hold".  
* **Detection:** Analyze curves during State \== Hold.  
* **Pass/Fail:** **Fail** if variance \== 0.0. **Pass** if variance \> 0 (Traceback/Drift).  
* **Citation:** "Character curves are perfectly flat... without a 'Moving Hold'... to maintain life." 7, 15\.

**23\. Blink Asymmetry**

* **What to check:** Duration of eyelid opening vs. closing.  
* **Detection:** Duration\_Close vs Duration\_Open.  
* **Pass/Fail:** **Pass** if Close \< Open (e.g., 3fr vs 6fr). **Fail** if Close \== Open (Robotic).  
* **Citation:** "Close (3–5 frames)... Open (4 frames, slower than closing)." 5, 2\.

**24\. Workflow Selection (Fluid vs. Rigid)**

* **What to check:** Algorithm used based on asset type.  
* **Detection:** Check Asset\_Tag.  
* **Pass/Fail:** **IF** Asset \== Cloth/Fire: **Fail** if using Pose-to-Pose. **Pass** if using Straight-Ahead.  
* **Citation:** "Switch to Straight-Ahead generation for fluid elements." 16, 14\.

**25\. Limited Animation Efficiency (80/20 Rule)**

* **What to check:** Percentage of screen pixels updating.  
* **Detection:** Calculate delta pixels between frames.  
* **Pass/Fail:** **Fail** if Update\_% \> 20% (for Limited/TV mode). **Pass** if Update\_% \<= 20%.  
* **Citation:** "80% of screen pixels must be static... only 20%... may update." 3, 17\.

