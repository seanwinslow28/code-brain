Here is the **Foundations to Implementation Rules** module for the "Coding Agent’s Guide to 2D Animation," strictly derived from the provided sources.

### Module 1: Foundations (Mechanics & Workflow)

**1\) Mental Model**

* **Concept:** Animation is not the movement of an object, but the *manipulation of time and space* to create the illusion of weight and intent.  
* **Dual Workflow:** The agent must function as both an **Architect** (Pose-to-Pose for structure) and an **Explorer** (Straight-Ahead for fluid physics).  
* **Citation:** "Straight ahead... has spontaneity... Pose to Pose is more planned... structures the animation." 1, 2\. "Timing is the objective quality... spacing is the subjective rhythm." 3\.

**2\) Rules That Become Code (Bulleted, Atomic)**

* **Workflow Selector:**  
* **IF** Asset\_Type \== "Character\_Body" OR "Rigid\_Object":  
* **THEN** use **Pose-to-Pose** (Keyframes $\\rightarrow$ Breakdowns $\\rightarrow$ In-betweens). Ensures volume consistency and narrative clarity 4-7.  
* **IF** Asset\_Type \== "Fire", "Water", "Smoke", "Hair", OR "Cloth":  
* **THEN** use **Straight-Ahead** (Frame $n \\rightarrow n+1$). Captures fluid unpredictability; ignores keyframe constraints 4, 6, 8\.  
* **Timing vs. Spacing Logic:**  
* **Timing Rule:** Calculate Total\_Frames based on Action\_Type weight (Heavy \= Slower/More Frames). Timing is objective 9, 10\.  
* **Spacing Rule:** Distribute Position\_Deltas based on physics.  
* **IF** Force \== "Gravity": Apply **Odd Rule** (spacing increases 1:3:5:7) 11-13.  
* **IF** Force \== "Internal/Organic": Apply **Cubic Easing** (Slow-In/Slow-Out) 14, 15\.  
* **Arc Constraint:**  
* **IF** Motion\_Type \== "Organic" (Human/Animal):  
* **THEN** Path\_Vector must map to a **Curved Spline** (Bézier). Linear paths are forbidden 16-18.  
* **Calculation:** For a parabolic arc, set the Breakdown pose at 50% time but only 25% vertical distance from the apex ("Fourth Down at Half Time") 12, 19\.  
* **Kinetic Chain (Successive Breaking of Joints):**  
* **Rule:** Child joints must lag parent joints.  
* **Offset:** Rotation\_Time(Elbow) \= Rotation\_Time(Shoulder) \+ Offset\_Frames 12, 20\.  
* **Anticipation Vector:**  
* **Rule:** Before moving to Target\_Pos, move to Anticipation\_Pos.  
* **Vector:** Anticipation\_Pos \= Start\_Pos \+ (-1 \* Direction\_Vector \* Magnitude) 21-23.

**3\) Parameter Defaults \+ Ranges (With Rationale)**

* **Joint Offset (Overlap):** 1–3 frames.  
* *Rationale:* Necessary to prevent "robotic" simultaneous movement; mimics the kinetic chain of force transfer 12, 24\.  
* **Anticipation Duration:**  
* *Standard:* 4–8 frames.  
* *Fast/Shock:* 1–2 frames (Invisible Anticipation).  
* *Rationale:* The audience needs time to register intent before the action occurs 22, 25, 26\.  
* **Blink Timing (Asymmetric):**  
* *Close:* 3–5 frames.  
* *Hold:* 1 frame.  
* *Open:* 4+ frames (slower than close).  
* *Rationale:* Biological data shows eyelids do not open/close linearly 27-29.  
* **Readability Floor:** Minimum 3 frames.  
* *Rationale:* Any pose held less than 3 frames is effectively invisible to the human eye 30, 31\.

**4\) Failure Modes \+ Detection Signals**

* **Error: "Floaty" Motion**  
* *Signal:* Spacing\_Curve is Linear (equidistant deltas) AND Duration \> 6 frames.  
* *Citation:* "If the spacing... is the exact same distance... this is called linear spacing which is very boring... feel like it was animated by a computer." 32, 33\.  
* **Error: "Strobing"**  
* *Signal:* Displacement\_Per\_Frame \> Object\_Width.  
* *Citation:* "When the action is too fast... the object seems to disappear... bridge the gap with smears." 34, 35\.  
* **Error: "Twinning"**  
* *Signal:* Left\_Limb.Rotation \== Right\_Limb.Rotation at same Time\_Index.  
* *Citation:* "Symmetry is boring... twinning... creates a rather boring and unappealing pose." 36, 37\.

**5\) QA Checklist**

*  **Workflow Check:** Are fluid elements (hair/tails) on a separate Straight-Ahead layer? 38, 39\.  
*  **Silhouette Check:** Is the pose readable in black & white? (Negative space between limbs/torso) 27, 40\.  
*  **Volume Check:** Does Scale\_X \* Scale\_Y \* Scale\_Z remain constant during Squash/Stretch? 41, 42\.  
*  **Arc Check:** Do organic movements follow a curved path? (Detect linear translation). 16, 43\.

**6\) Minimal Pseudocode / Structured Spec**  
def generate\_motion(asset, start\_pose, end\_pose, duration):  
    \# 1\. SELECT WORKFLOW  
    if asset.is\_fluid:  
        return animate\_straight\_ahead(asset, duration) \# Physics simulation  
      
    \# 2\. POSE-TO-POSE ARCHITECTURE  
    timeline \= create\_timeline(duration)  
    timeline.set\_keyframe(0, start\_pose)  
    timeline.set\_keyframe(duration, end\_pose)  
      
    \# 3\. ANTICIPATION (Pre-action)  
    anticip\_vector \= (end\_pose.position \- start\_pose.position).invert() \* 0.2  
    anticip\_pose \= start\_pose \+ anticip\_vector  
    timeline.set\_keyframe(time=4, pose=anticip\_pose) \# Default 4 frames  
      
    \# 4\. BREAKDOWN (Arc Constraint)  
    \# Apply "Fourth Down at Half Time" for gravity arcs  
    mid\_time \= duration / 2  
    breakdown\_pose \= calculate\_arc\_breakdown(start\_pose, end\_pose, gravity=True)  
    timeline.set\_breakdown(mid\_time, breakdown\_pose)  
      
    \# 5\. SPACING (In-betweens)  
    \# Apply Ease-In/Out (Cubic) or Odd Rule (Gravity)  
    if asset.force \== "gravity":  
        apply\_spacing\_curve(timeline, type="odd\_rule\_1\_3\_5\_7")  
    else:  
        apply\_spacing\_curve(timeline, type="ease\_in\_out")  
          
    \# 6\. OVERLAP (Successive Breaking of Joints)  
    for child\_joint in asset.skeleton.children:  
        timeline.offset\_track(child\_joint, delay\_frames=2)  
          
    return timeline  
**7\) "Break the Rule" (Mode Switch Map)**  
Trigger Condition,Target Mode,Implementation Rule,Rationale / Citation  
Impact / Shock,No Easing,Remove Slow-in/Slow-out. Transition from Key A $\\rightarrow$ B in 1 frame.,"""For a gag action, we may omit some slow-out or slow-ins for shock appeal... more snap."" 18."  
High Velocity,Smear,IF Velocity \> Width: Stretch Geometry (1 frame). IF Cyclic: Use Multiples.,"""When the action is too fast... bridge the gap."" 12, 34."  
Limited / TV,Step-Modulation,Hold poses for 2s (12fps) or 3s (8fps). Freeze body layer during dialogue.,"""80% static poses / 20% movement ratio."" 44, 45."  
Stylized (Spider-Verse),Stepped,"Disable motion blur. Force Exposure \= 2\. Use ""Lines"" instead of blur.","""Avoided using blurring... used other techniques like smear frames."" 46, 47."  
Dialogue,Cel Stacking,Lock Body layer. Update only Mouth layer.,"""Dividing a character into... cel levels... body on level 1 and the mouth... on level 2."" 44."  
