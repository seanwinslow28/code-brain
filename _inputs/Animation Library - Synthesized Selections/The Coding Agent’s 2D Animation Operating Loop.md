### The Coding Agent’s Operating Loop: 2D Animation Generation

This operating loop integrates the physics engine, style parameters, and production constraints defined in the Core Canon. It follows a strict **Plan $\\rightarrow$ Implement $\\rightarrow$ Verify** architecture to ensure all motion data adheres to the "Immutable Laws" of animation before rendering.

### Phase 1: PLAN (Configuration & constraints)

**Goal:** Convert the raw request into a structured specification (AnimationClipSpec) and select the correct operating mode (Physics vs. Style).

* **Parse Request & Context:**  
* **Input:** User text prompt, Audio track (optional), Script context.  
* **Action:** Analyze input for keywords mapping to **Style Profiles** 1\.  
* *Example:* "1930s style" $\\rightarrow$ Set Style\_ID to GOLDEN\_AGE (Enable Squash/Stretch, Cubic Easing) 2\.  
* *Example:* "TV budget" $\\rightarrow$ Set Budget\_Mode to LIMITED\_TV (Enable 80/20 Rule, Cel Stacking) 2, 3\.  
* **Action:** Analyze Audio/Timing.  
* **IF** Audio exists: Run Phoneme\_Extraction and map to Viseme Library (7–9 shapes) 4, 5\.  
* **IF** Music exists: Calculate BPM for Sync\_Source 6\.  
* **Asset Strategy (The "Bank" Check):**  
* **Logic:** Before generating new motion, query the Asset\_Library.  
* **Rule:** **IF** Budget\_Mode \== LIMITED\_TV AND Action matches a stored "Cycle" (Walk/Run) or "Take" (Reaction), **THEN** retrieve and instance the asset. Do not re-animate. 3, 7, 8\.  
* **Construct the AnimationClipSpec:**  
* **Output Artifact:** A JSON object defining the scene's immutable parameters.  
* **Data Fields:**  
* fps: 24 (default) 9\.  
* constraints.exposure\_rate: 1 (High Fidelity) or 2 (Standard/TV) 10\.  
* action\_beats: List of key moments with duration ranges (e.g., "Fast Reaction: 2–4 frames") 11, 12\.  
* physics\_mode: "Odd Rule" (Gravity) or "Linear" (Mechanical) 13, 14\.

### Phase 2: IMPLEMENT (Generation & Synthesis)

**Goal:** Generate geometry and timing data that adheres to the AnimationClipSpec.

* **Step 1: Blocking (Key Pose Generation):**  
* **Method:** Use **Pose-to-Pose** architecture for body/acting 15, 16\.  
* **Posing Rules:**  
* **Power Center:** Align root velocity origin based on character type (e.g., Chest for Hero, Hips for Heavy) 17, 18\.  
* **Line of Action:** Fit spinal joints to a C or S curve. Reject straight lines 17, 19\.  
* **Silhouette:** Ensure limbs do not occlude \>30% of the torso surface area 19, 20\.  
* **Artifact:** KeyPose\_Data (Sparse Vector3 positions/rotations at specific time indices).  
* **Step 2: Splining (Timing & Spacing):**  
* **Logic:** Interpolate between Key Poses using Spacing\_Chart logic.  
* **Gravity Rule:** **IF** Force \== Gravity, apply **Odd Rule Spacing** (1:3:5:7 ratios) to vertical descent 13, 21\.  
* **Arc Rule:** **IF** Motion \== Organic, apply "Fourth Down at Half Time" (Breakdown is 25% from apex at 50% time) 21, 22\.  
* **Offset Rule:** Delay child joints (Elbows/Wrists) by 1–3 frames relative to parents (Shoulders) for "Successive Breaking of Joints" 17, 23\.  
* **Step 3: Fast-Motion Synthesis (Smears):**  
* **Trigger:** **IF** Velocity \> Object\_Width 24, 25\.  
* **Decision:**  
* **IF** Action \== Ballistic (Punch/Zip): Generate **Elongated In-between** (Stretch Mesh) 24, 26\.  
* **IF** Action \== Cyclic (Wheel/Run): Generate **Multiples** (Ghosting) 17, 26\.  
* **Constraint:** Force Smear Duration \= **1 Frame** strictly 25, 27\.  
* **Step 4: Layer Optimization (Limited Mode only):**  
* **Logic:** **IF** Budget\_Mode \== LIMITED\_TV:  
* Freeze Body\_Layer (Static).  
* Animate Mouth\_Layer based on audio 3, 7\.  
* Ensure Moving\_Hold (drift/traceback) is applied to static layers to prevent "death by stasis" 7, 28\.

### Phase 3: VERIFY (QA Gates & Correction)

**Goal:** Detect "failure modes" and apply automated fixes before finalizing.

* **Gate 1: Physics & Mechanics QA**  
* **Check:** **Gravity Acceleration.** Does vertical spacing follow the 1:3:5:7 Odd Rule? 29\.  
* **Check:** **Volume Conservation.** Does $Scale\\\_X \\times Scale\\\_Y \\times Scale\\\_Z \\approx 1$ during squash/stretch? 30\.  
* **Correction:** Re-calculate Y positions using $d=1/2gt^2$; Apply $1/\\sqrt{Y}$ to X/Z scales 22, 31\.  
* **Gate 2: Acting & Clarity QA**  
* **Check:** **Twinning.** Do Left/Right limbs have identical values on the same frame? 27, 32\.  
* **Check:** **Readability Floor.** Is the main pose held for $\<3$ frames? 33\.  
* **Correction:** Offset one limb by 2–4 frames; Extend hold duration to minimum 6 frames 11, 27\.  
* **Gate 3: Artifact & Render QA**  
* **Check:** **Strobing.** Does an object move \> width without a smear? 31, 34\.  
* **Check:** **Sticky Smear.** Is a deformed mesh held for $\\ge 2$ frames? 23, 35\.  
* **Check:** **Floaty Motion.** Is the spacing curve linear for $\>6$ frames? 16, 35\.  
* **Correction:** Insert Smear frame; Snap mesh back to rest pose; Apply Cubic Ease-In/Out 23, 31\.

### Artifacts Produced

Step,Artifact Name,Description / Schema  
PLAN,AnimationClipSpec,"JSON object defining fps (24), style\_profile (e.g., ""Rubber Hose""), budget\_mode (""TV""), and beats (Action list)."  
IMP,KeyPose\_Data,"Sparse set of ""Golden Poses"" (Vector3/Rotations) representing the narrative beats."  
IMP,Spacing\_Chart,"Frame-by-frame displacement values derived from physics rules (e.g., Odd Rule)."  
IMP,X\_Sheet,(Limited Mode) Exposure sheet mapping audio phonemes to specific frame numbers and mouth layers 15\.  
VER,QA\_Report,"Boolean list of pass/fail checks (e.g., Twinning\_Detected: True, Volume\_Loss: False)."

### Clarification Policy: When to Ask vs. Default

Scenario,Decision,Logic / Source  
Ambiguous Timing,Use Default,"Default to ""Normal Action"" (12–16 frames) unless ""Fast/Reaction"" (2–4 frames) is specified 11, 36."  
Missing Style,Use Default,"Default to High-Fidelity Hybrid: 24fps base, animated ""On Twos"" (12fps), Cubic Easing 37."  
Conflicting Physics,ASK User,"E.g., ""Realistic Rubber Hose."" Realism requires joints; Rubber Hose forbids them. Ask to prioritize Style or Anatomy 6, 38."  
Budget vs. Quality,ASK User,"If request asks for ""Feature Quality"" (Ones) but ""TV Budget"" (80% static). These are mutually exclusive constraints 3, 39."  
Fluid Elements,Use Default,"If asset is Fire/Water/Hair, automatically switch workflow to Straight-Ahead (ignore Pose-to-Pose) 16, 40."  
