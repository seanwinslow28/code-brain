Here is the **Foundations Pseudocode Library**, a set of implementation-ready patterns derived from the "Foundations" and "Implementation Rules" of the provided animation canon.

### 1\. The Gravity Spacing Generator (Odd Rule)

**When to use:** Calculating the vertical position of any object falling from a stop (apex).**Mental Model:** Gravity is a constant acceleration. Displacement between frames increases in the ratio of odd numbers (1, 3, 5, 7\) relative to the first unit of fall 1, 2\.

* **Inputs:** Apex\_Pos (Y), Unit\_Dist (Distance fallen in frame 1), Frame\_Index.  
* **Outputs:** Y\_Position for current frame.  
* **Pseudocode:**  
* def calculate\_gravity\_pos(apex\_y, unit\_dist, frame\_count):  
*     \# Physics Rule: Distance \= Unit \* Frame^2 (or Odd Rule summation)  
*     total\_fall \= unit\_dist \* (frame\_count \* frame\_count)  
*     return apex\_y \- total\_fall  
* **Parameters & Defaults:**  
* Unit\_Dist: Depends on scale. At 24fps, frame 1 drop $\\approx$ 1/3 inch 3\.  
* Frame\_Rate: 24 (On Ones) or 12 (On Twos) 4\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Floaty" Motion.** Spacing is linear (1, 1, 1).  
* *Test:* if (pos\[t\] \- pos\[t-1\]) \== (pos\[t-1\] \- pos\[t-2\]): FAIL 1\.

### 2\. Anticipation → Action → Settle

**When to use:** Before *any* significant movement to signal intent and weight.**Mental Model:** "Broadcasting Intent." An object must move in the opposite direction (-Vector) before moving in the intended direction (+Vector) 5, 6\.

* **Inputs:** Start\_Pose, Target\_Pose, Intensity (0.0 to 1.0).  
* **Outputs:** Keyframe sequence Antic, Action, Overshoot, Settle.  
* **Pseudocode:**  
* def generate\_anticipation\_beat(start, target, intensity):  
*     move\_vector \= target.position \- start.position  
*     \# Antic moves opposite to main action  
*     antic\_pos \= start.position \- (move\_vector.normalize() \* intensity \* 0.2)  
*   
*     \# Duration Heuristic: Slower antic, fast action  
*     antic\_time \= start.time \+ 4\_frames  \# Standard prep  
*     action\_time \= antic\_time \+ 2\_frames \# Fast transit (zip)  
*   
*     return Keyframe(antic\_pos, antic\_time)  
* **Parameters & Defaults:**  
* Antic\_Duration: 4–8 frames (Standard), 1–2 frames (Invisible/Shock) 7\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Surprise" Motion.** Character moves without telegraphing (unless intended).  
* *Test:* Check if Vector(Start-\>Antic) is opposite to Vector(Start-\>Target) 5\.

### 3\. Overshoot & Settle (Damped Oscillation)

**When to use:** When an object comes to a stop. Prevents "robotic" stops.**Mental Model:** Extremities (hair, loose limbs) continue past the stopping point due to momentum, then return 8, 9\.

* **Inputs:** Target\_Value, Velocity\_In, Stiffness.  
* **Outputs:** Sequence of values Peak, Return.  
* **Pseudocode:**  
* def apply\_overshoot(target, velocity, stiffness):  
*     \# Calculate how far past target to go based on speed  
*     overshoot\_mag \= velocity \* (1.0 \- stiffness)  
*     peak\_val \= target \+ overshoot\_mag  
*   
*     \# Hard Accent: Bounce back immediately  
*     \# Soft Accent: Drift through  
*     if stiffness \> 0.5:   
*         return \[Frame(peak\_val, t+1), Frame(target, t+3)\]  
*     else:  
*         return \[Frame(peak\_val, t+2), Frame(target, t+6)\]  
* **Parameters & Defaults:**  
* Return\_Frames: 3–5 frames for rigid bodies, 6+ for soft bodies 10\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Dead Stop."** Curve hits value and flattens instantly.  
* *Test:* if value\_at\_stop \== previous\_value: FAIL 11\.

### 4\. Successive Breaking of Joints (Offset/Overlap)

**When to use:** Animating limbs, tails, or spinal chains.**Mental Model:** Kinetic Chain. Force travels Root $\\rightarrow$ Shoulder $\\rightarrow$ Elbow $\\rightarrow$ Wrist. Child joints must lag behind parents 12, 13\.

* **Inputs:** Joint\_Hierarchy (List), Base\_Curve.  
* **Outputs:** Offset curves for child joints.  
* **Pseudocode:**  
* def apply\_joint\_offset(hierarchy, delay\_frames=2):  
*     for i, joint in enumerate(hierarchy):  
*         if i \== 0: continue \# Root stays  
*   
*         \# Child joint copies parent curve but shifts in time  
*         parent\_curve \= hierarchy\[i-1\].get\_rotation\_curve()  
*         offset \= i \* delay\_frames  
*   
*         joint.set\_curve(parent\_curve.shifted\_by(offset))  
* **Parameters & Defaults:**  
* Delay: 1–3 frames per joint. (2 frames is standard "Twos" overlap) 14\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Twinning" / "Stiff."** All joints rotate simultaneously.  
* *Test:* if Rotation\_Start\_Time(Elbow) \== Rotation\_Start\_Time(Shoulder): FAIL 15\.

### 5\. Arc Enforcement (Fourth Down at Half Time)

**When to use:** Calculating the breakdown position for curved motion (organic).**Mental Model:** "Fourth Down at Half Time." At 50% of the duration, the object is only 25% down from the apex (vertical), creating a parabolic arc 16, 17\.

* **Inputs:** Start\_Pos, End\_Pos, Apex\_Height, Duration.  
* **Outputs:** Breakdown\_Pos (The "Half-time" key).  
* **Pseudocode:**  
* def get\_arc\_breakdown(apex\_y, ground\_y):  
*     total\_height \= apex\_y \- ground\_y  
*     \# Rule: At half time, we are only 1/4 down the total height  
*     breakdown\_y \= apex\_y \- (total\_height \* 0.25)  
*     return breakdown\_y  
* **Parameters & Defaults:**  
* Arc\_Bias: Organic \= Parabolic; Mechanical \= Linear 18\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Linear/Mechanical."** Midpoint is exactly (Start \+ End) / 2\.  
* *Test:* if breakdown\_pos is on\_linear\_vector(start, end): FAIL 19\.

### 6\. Volume Preserving Squash & Stretch

**When to use:** Deforming characters on impact or acceleration.**Mental Model:** Volumetric Integrity. $X \\times Y \\times Z \= Constant$. If Y stretches, X and Z must squash 20, 21\.

* **Inputs:** Scale\_Y (Stretch factor).  
* **Outputs:** Scale\_X, Scale\_Z.  
* **Pseudocode:**  
* def preserve\_volume(scale\_y):  
*     \# Inverse square root ensures volume \= 1.0  
*     \# Formula: scale\_x \= 1 / sqrt(scale\_y)  
*     scale\_x \= 1.0 / math.sqrt(scale\_y)  
*     scale\_z \= scale\_x   
*     return (scale\_x, scale\_y, scale\_z)  
* **Parameters & Defaults:**  
* Max\_Stretch: 2.0 (Cartoony) vs 1.1 (Realistic) 22\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Shrinking/Growing."** Object scales in one axis only.  
* *Test:* if (sx \* sy \* sz) \< 0.9 or \> 1.1: FAIL 23\.

### 7\. Asymmetric Blink Timing

**When to use:** Generating facial idle animations or reactions.**Mental Model:** A blink is not a sine wave. Closing is fast (muscle flex); opening is slow (relaxation/adhesion) 24, 25\.

* **Inputs:** Start\_Frame.  
* **Outputs:** Keyframes for Eyelid\_Open\_Pct.  
* **Pseudocode:**  
* def generate\_blink(start\_f):  
*     \# Close Fast (3 frames)  
*     keys.add(time=start\_f, val=1.0) \# Open  
*     keys.add(time=start\_f+3, val=0.0) \# Closed  
*   
*     \# Hold Closed (1 frame)  
*     keys.add(time=start\_f+4, val=0.0)  
*   
*     \# Open Slow (4-6 frames)  
*     keys.add(time=start\_f+9, val=1.0) \# Open  
* **Parameters & Defaults:**  
* Close: 3 frames. Open: 4-6 frames 25\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Robot Blink."** Close duration \== Open duration.  
* *Test:* if duration\_close \== duration\_open: FAIL.

### 8\. Smear / Strobing Detection

**When to use:** High-velocity movements (fast pans, punches).**Mental Model:** If displacement \> Object Width, the eye sees a gap (strobing). Fill it with a smear 26, 27\.

* **Inputs:** Pos\_Current, Pos\_Next, Object\_Width.  
* **Outputs:** Smear\_Flag (Boolean) or Scale\_Stretch\_Vector.  
* **Pseudocode:**  
* def check\_strobing(p1, p2, width):  
*     displacement \= distance(p1, p2)  
*     if displacement \> width:  
*         \# Trigger Smear Geometry or Multiple  
*         return True   
*     return False  
* **Parameters & Defaults:**  
* Smear\_Duration: STRICTLY 1 frame 27\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Sticky Smear."** Smear held \> 1 frame.  
* *Test:* if is\_smear and duration \> 1: FAIL 28\.

### 9\. Moving Hold (The "Alive" State)

**When to use:** When a character is "still" or listening.**Mental Model:** "Traceback." No living character is perfectly static. Use a "Moving Hold" to drift between two nearly identical poses 29, 30\.

* **Inputs:** Pose\_A, Duration.  
* **Outputs:** Pose\_B (Micro-offset).  
* **Pseudocode:**  
* def generate\_moving\_hold(pose\_a, duration):  
*     \# Create Pose B with \< 5% variance  
*     pose\_b \= pose\_a \+ random\_drift(0.02)   
*   
*     \# Linear interpolate very slowly  
*     return interpolate(pose\_a, pose\_b, duration, curve="linear")  
* **Parameters & Defaults:**  
* Drift\_Amount: 1-2% variance.  
* Min\_Duration: 12 frames (for readability) 31\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Dead Hold."** Values remain exactly constant.  
* *Test:* if variance(curve) \== 0 for \> 12 frames: FAIL 32\.

### 10\. Walk Cycle State Machine

**When to use:** Procedural locomotion.**Mental Model:** Four distinct states define a step. Contact (heel), Down (weight), Pass (cross), Up (push) 33\.

* **Inputs:** Stride\_Length, Cycle\_Frames.  
* **Outputs:** Key poses at specific intervals.  
* **Pseudocode:**  
* def get\_walk\_pose(frame, cycle\_len=24):  
*     \# Standard 24-frame cycle (12 frames per step)  
*     phase \= frame % cycle\_len  
*   
*     if phase \== 1: return "CONTACT" \# Heel strike  
*     if phase \== 4: return "DOWN"    \# Lowest Y, Squash  
*     if phase \== 7: return "PASS"    \# Leg crossing  
*     if phase \== 10: return "UP"     \# Highest Y, Push off  
*     \# Repeat for other leg (frames 13-24)  
* **Parameters & Defaults:**  
* Standard\_March: 12 frames per step (2 steps/sec) 33\.  
* Cartoon\_Run: 6 or 8 frames per step 34\.  
* **Failure Modes \+ Tests:**  
* *Failure:* **"Sliding."** Feet move while on ground.  
* *Test:* if state in \[DOWN, PASS, UP\] and Foot\_Velocity \!= 0: FAIL.

