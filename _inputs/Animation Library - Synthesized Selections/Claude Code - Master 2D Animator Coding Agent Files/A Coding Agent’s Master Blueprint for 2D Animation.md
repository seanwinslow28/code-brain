This is the master blueprint for **“A Coding Agent’s Guide to 2D Animation,”** constructed strictly from the provided source texts.

### A) Table of Contents: The 6-Module Architecture

**1\. Foundations: The Physics Engine**

* **Focus:** Gravity, acceleration, and the "Odd Rule" of spacing 1, 2\.  
* **Core Mechanics:** The "Lead and Follow" kinetic chain (Successive Breaking of Joints) 3, 4\.  
* **State Machine:** The 4-position Walk Cycle (Contact, Down, Passing, Up) 5, 6\.  
* **Timing vs. Spacing:** Separating temporal duration from spatial rhythm 7, 8\.

**2\. Smears & Fast-Motion Readability**

* **Focus:** Handling velocity that exceeds visual persistence (preventing strobing) 9, 10\.  
* **Algorithms:** "Elongated In-betweens" (Mesh Stretch) for ballistic transits vs. "Multiples" (Ghosting) for cyclic action 11, 12\.  
* **The "Genndy Blur":** Tempering 3D motion blur with sub-frame geometry 13, 14\.  
* **Constraint:** The single-frame duration rule 15, 16\.

**3\. TV vs. Feature (Limited Animation Optimization)**

* **Focus:** "Planned Animation" as a resource management system 17, 18\.  
* **The 80/20 Heuristic:** 80% static poses / 20% movement ratio 19, 20\.  
* **Cel Stacking:** Separating "Static Body" layers from "Active Mouth/Eye" layers 21, 22\.  
* **Audio-Driven:** Prioritizing lip-sync and dialogue over body mechanics 23, 24\.

**4\. Style History (Procedural "Time Travel" Modes)**

* **Rubber Hose (1920s):** "Noodle" limbs (no joints), constant motion, and musical synchronization 25, 26\.  
* **Modernist/UPA (1950s):** Flatness, asymmetry, and "subjective space" (backgrounds reflect mood) 27, 28\.  
* **The "Spider-Verse" Hybrid:** Stepped animation (on Twos), no motion blur, and CMYK offsets 29, 30\.  
* **Anime/Modulation:** Dynamic switching between 1s, 2s, and 3s based on intensity 31, 32\.

**5\. Acting, Posing, and Clarity**

* **The Acting Engine:** "Power Centers" (velocity origins) and "Lines of Action" (force vectors) 33, 34\.  
* **Readability:** Silhouette validation and negative space management 35, 36\.  
* **Facial Logic:** Asymmetric blink timing (Fast Close $\\rightarrow$ Hold $\\rightarrow$ Slow Open) 37, 4\.  
* **Anti-Patterns:** Twinning (symmetry) detection and correction 38, 39\.

**6\. Production Pipeline (Data & Workflow)**

* **Data Structures:** The Exposure Sheet (X-Sheet) as the master timeline database 24, 40\.  
* **Workflow:** Separating "Blocking" (Storytelling Poses) from "Splining" (Interpolation) 41, 42\.  
* **Handoffs:** Defining "Blocking Poses" as sparse constraints for generative/in-betweening models 43, 44\.

### B) Shared “Animation Taxonomy” (Canonical & Agent Mapped)

Canonical Term,Definition & Source,Agent Concept / Data Structure  
Keyframe (Extreme),"The primary storytelling poses that define what happens. Immutable constraints 45, 6.","KeyPose\_Data (Vector3 positions, Rotations). Hard constraint."  
Breakdown (Passing Position),"The pose between keys that defines how the object moves (arc/spacing). Distinct from an in-between 46, 6.",Breakdown\_Frame (Interpolation Logic: Linear vs. Arc).  
Spacing,"The spatial displacement/rhythm between frames. Determines ""weight"" and ""speed"" 7, 47.",Displacement\_Delta (Distance per frame).  
Timing,"The temporal duration (frame count) of an action 7, 48.","Duration\_Ticks (Integer, frame count)."  
Smear (Elongated In-between),"A single frame where geometry is deformed to bridge large gaps and prevent strobing 11, 12.",Mesh\_Deformation (Scale axis \> 1.0). Event duration \= 1 frame.  
Multiple (Ghosting),"Repeating the object multiple times in a single frame to show path (used for cycles) 12, 49.",Instanced\_Geometry (Array of mesh positions in one frame).  
Moving Hold,"A pose that is technically moving (drift/traceback) to keep the character ""alive"" 50, 51.",Micro\_Interpolation (Variance \< 2% over time).  
On Ones / On Twos,"The exposure rate. ""On Ones"" \= 24 unique frames/sec. ""On Twos"" \= 1 drawing held for 2 frames 7, 52.",Update\_Frequency (1 or 2).  
Line of Action,"An imaginary vector through the main axis (Head to Foot) dictating force 34, 33.",Force\_Vector (Spline curve fitting spinal joints).  
Power Center,"The origin point of a character's movement force (e.g., Chest, Hips) 53, 54.",Velocity\_Origin (Root node for kinetic calculations).  
Blocking Pose,"Sparse, intentionally imprecise poses meant to convey ""gist"" before detailing 41, 43.",Sparse\_Constraint (Low-fidelity keyframe data).  
Twinning,"A failure mode where left/right limbs move symmetrically, creating a robotic effect 38, 55.",Symmetry\_Flag (Boolean: True if L\_Rot \== R\_Rot).

### C) The Standard "Chapter Template"

**1\. Mental Model (Short)**

* **Concept:** High-level theory, e.g., "Gravity is an acceleration curve, not a speed."  
* **Citation:** Source ID

**2\. Rules That Become Code (Bulleted, Atomic)**

* *Rule 1:* Atomic logic, e.g., "If falling, Spacing \= Odd Numbers (1, 3, 5)." 2  
* *Rule 2:* Atomic logic, e.g., "If Limb\_L \== Limb\_R, Offset time by 2 frames." 56

**3\. Parameter Defaults \+ Ranges (With Rationale)**

* *Fast Action (Reaction):* 2–4 frames 57\.  
* *Normal Action:* 12–16 frames 57\.  
* *Blink Duration:* Close (3-5fr), Closed (1fr), Open (4+fr) 4\.  
* *Smear Threshold:* Displacement \> Object Width 4\.

**4\. Failure Modes \+ Detection Signals**

* *Anti-Pattern:* "Floaty" motion (Even spacing/Linear interpolation) 58, 59\.  
* *Signal:* is\_linear(curve) \== TRUE and duration \> 6 frames.

**5\. QA Checklist**

*  Does the silhouette read clearly in black & white? 35  
*  Are joints breaking successively (offset)? 60

**6\. Minimal Pseudocode or Structured Spec**

* (Logic block defining the execution of the module).

### D) Mode Switch Map

**Decision Logic: When to Switch Animation Operating Modes**  
Trigger Condition,Target Mode,Implementation Rule,Motivation / Source  
Physics \== Gravity,Realism (The Odd Rule),Calculate Y pos using 1:3:5:7 ratio.,"""For a falling object, the spacings follow... the odd numbers."" 2, 4"  
Velocity \> Object\_Width,Smear / Fast Motion,IF Linear: Deform Mesh (Stretch). IF Cyclic: Instance Mesh (Multiple).,"""When the action is too fast... the object seems to disappear."" Prevent strobing. 9, 12"  
Camera\_Move \== True,High Fidelity (On Ones),Force update frequency to 1 frame (24fps).,"""When the camera is panning... add in single inbetweens so it doesn't strobe\!"" 61"  
Dialogue \== True,Limited (TV Mode),Lock Body layer. Update Mouth layer per phoneme chart.,"""80% static poses supporting dialogue... 20% original movement."" 19, 21"  
"Style \== ""Spider-Verse""",Stepped / Comic,"Disable motion blur. Enforce ""On Twos"" (12fps) unless high velocity.","""Avoided using blurring... used other techniques like smear frames and 2D speed lines."" 29, 62"  
Limb\_Side \== Left & Right,Asymmetry (Naturalism),Offset one side by 2–4 frames (Anti-Twinning).,"""Symmetry is boring... twinning... creates a rather boring and unappealing pose."" 39, 55"  
Asset \== Fluid/Fire,Straight-Ahead,Disable keyframe targets; generate sequentially.,"""Straight ahead animation is best for animating natural or free flowing animations."" 63"  
