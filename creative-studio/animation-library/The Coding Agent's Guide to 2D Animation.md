Here is the final **Coding Agent’s Guide to 2D Animation**, assembled from the core canon and module specifications.

# The Coding Agent’s Guide to 2D Animation

**Version 1.0**

## 1\. Introduction & Usage

This guide functions as the operating system for a 2D animation generation agent. It replaces vague artistic inspiration with testable, deterministic rules derived from the physics of motion and the constraints of production pipelines.  
**The Agent’s Dual Mode:**

1. **The Architect (Pose-to-Pose):** Used for structure, acting, and narrative clarity. The agent plans keyframes first, then breaks them down.  
2. **The Explorer (Straight-Ahead):** Used for fluid dynamics (fire, water, hair). The agent generates frame $n+1$ based solely on frame $n$ physics.  
* **Citation:** "Straight ahead has spontaneity... Pose to Pose structures the animation." 1, 2

## 2\. The Operating Loop

The agent follows a strict **Plan $\\rightarrow$ Implement $\\rightarrow$ Verify** architecture to prevent "floaty" or "robotic" output 3\.

### Phase 1: PLAN (Configuration)

* **Parse Constraints:** Detect budget\_mode (TV vs. Feature) and style\_profile (e.g., Rubber Hose).  
* **Asset Strategy:**  
* **IF** budget\_mode \== LIMITED\_TV: Query the "Bank" for existing cycles before generating new frames 4, 5\.  
* **Output:** An AnimationClipSpec defining FPS, exposure rate, and beats 6\.

### Phase 2: IMPLEMENT (Synthesis)

* **Blocking:** Generate KeyPose\_Data (Golden Poses) ensuring readable silhouettes 7\.  
* **Splining:** Interpolate using physics rules.  
* **Gravity:** Apply "Odd Rule" spacing (1:3:5:7) 8, 9\.  
* **Overlap:** Offset child joints (Elbows) 1–3 frames behind parents (Shoulders) 10\.  
* **Smearing:** **IF** velocity \> object\_width, generate a smear frame (duration \= 1 frame) 11, 12\.

### Phase 3: VERIFY (QA Gates)

1. **Physics Check:** Is spacing linear? (Fail). Is volume conserved? (Pass) 13\.  
2. **Acting Check:** Is there "Twinning" (symmetry)? (Fail) 14\.  
3. **Render Check:** Is the smear held \>1 frame? (Fail) 11\.

## 3\. Module Specifications

### Module 1: The Physics Engine (Foundations)

* **Gravity (The Odd Rule):** Gravity is an acceleration, not a speed. Displacement from a stop increases in the ratio of odd numbers: 1, 3, 5, 7\.  
* *Implementation:* Y\_Pos\[t\] \= Y\_Pos\[t-1\] \- (Unit\_Dist \* (2t \- 1)) 8, 9\.  
* **Arcs (Fourth Down Rule):** For organic motion, the breakdown pose at 50% time must be at 25% of the vertical distance from the apex (favoring the slow-out) 15, 16\.  
* **Timing vs. Spacing:**  
* *Timing* \= Duration (Frame Count).  
* *Spacing* \= Rhythm (Displacement).  
* *Rule:* Never use linear spacing for organic characters 17, 18\.

### Module 2: Fast-Motion Synthesis (Smears)

* **Trigger Threshold:** Initiate smear protocol if displacement \> object\_width to prevent strobing 11, 12\.  
* **Topology Logic:**  
* **Ballistic (Punch/Zip):** Use **Elongated In-between** (Stretch Mesh). Connect Start $\\to$ End with a tube/ellipse 19\.  
* **Cyclic (Wheels/Legs):** Use **Multiples** (Ghosting). Instance geometry 3–5 times. **Constraint:** Do not space evenly (prevents A-B-A blinking) 19, 20\.  
* **The Genndy Blur (3D):** For 3D meshes, blend sub-frame geometry into the current frame, biasing opacity (70%+) to the leading edge to maintain silhouette 21, 22\.

### Module 3: Optimization Logic (TV/Limited)

* **The 80/20 Rule:** In Limited TV mode, ensure 80% of screen pixels are static. Only 20% (mouths, eyes, arms) update per frame 5, 23\.  
* **Cel Stacking:** Separate the character into Level\_1\_Body (Static) and Level\_2\_Mouth (Active) to minimize drawing count 24, 25\.  
* **Exposure:** Default to animating "On Twos" (12fps). Switch to "Ones" (24fps) *only* if Camera\_Pan\_Velocity \> 0 to prevent background strobing 26, 27\.

### Module 4: Style Mode Switcher

The agent switches physics parameters based on the style\_profile\_id 28, 29\.  
Style Profile,Physics Logic,Framerate,Smear Type  
RUBBER HOSE,No Joints (Curve Deform). Constant Bounce (No Holds).,Sync to Audio BPM,Speed Lines (No Blur)  
GOLDEN AGE,Squash & Stretch (Volume Locked). Cubic Easing.,12fps / 24fps,Drybrush / Texture  
SCREWBALL,"""Zip"" Transitions (1 frame). Extreme Overshoot.",24fps (Fast),Elongated Mesh  
UPA / MODERN,Planar Movement (X/Y only). Asymmetry.,"Variable (1s, 2s, 3s)",Abstract Shapes  
SPIDER-VERSE,Stepped Interpolation (No Splines).,Forced 12fps (Twos),CMYK Offset (No Blur)

### Module 5: The Acting Engine

* **Twinning (Anti-Symmetry):** If L\_Limb\_Rot \== R\_Limb\_Rot at the same frame, flag as error. **Fix:** Offset one side by 2–4 frames 14, 30\.  
* **Blink Timing:** Blinks are asymmetric.  
* *Close:* 3 frames.  
* *Hold:* 1 frame.  
* *Open:* 4+ frames (slower than close) 31, 32\.  
* **Eye Lead:** Eyes must move 2–3 frames *before* the head turns. Thought precedes action 33\.

### Module 6: Pipeline Architecture

* **X-Sheet:** The master database mapping audio phonemes to specific frame numbers. Visual accents must lead audio hits by 2 frames 24, 34\.  
* **Asset Handoff:** Pass "Blocking Poses" as sparse constraints. Use "Straight-Ahead" layers for fluid elements (tails/capes) on top of "Pose-to-Pose" body mechanics 1, 35\.

## 4\. Shared Taxonomy & Glossary

Term,Definition,Agent Data Structure,Source  
Spacing,Displacement per frame (Rhythm).,float3 position\_delta,17  
Timing,Duration of action (Frame count).,int duration\_frames,17  
Smear,Deformed geometry bridging a gap.,mesh\_deformation (Scale \> 1),11  
Moving Hold,"A ""static"" pose with micro-drift to keep it alive.",curve\_variance (1-2%),23  
On Ones,1 drawing per frame (24fps).,exposure\_rate \= 1,36  
On Twos,1 drawing held for 2 frames (12fps).,exposure\_rate \= 2,36  
Twinning,Symmetrical movement (Failure mode).,bool is\_symmetric,14

## 5\. QA Gates: The "Blocker" Checklist

**1\. The Readability Gate**

*  **Silhouette:** Do limbs occlude \<30% of the torso? 37  
*  **Duration:** Is the pose held $\\ge$ 3 frames? (Anything less is invisible) 15\.

**2\. The Physics Gate**

*  **Floaty Check:** Is spacing linear for \>6 frames? **Fix:** Apply Ease-in/out 38\.  
*  **Volume Check:** Does $X \\cdot Y \\cdot Z \\approx 1$ during squash? **Fix:** $Scale\_{perp} \= 1/\\sqrt{Scale\_{parallel}}$ 39\.

**3\. The Production Gate**

*  **Strobing:** Does displacement \> width without a smear? 11\.  
*  **Dead Hold:** Is the character perfectly static for \>1 sec? **Fix:** Add Moving Hold or Blink 40\.

# Appendix

## A. JSON Schema: AnimationClipSpec

*Derived from 6*  
{  
  "fps": 24,  
  "constraints": {  
    "exposure\_rate": 2, // Default to "On Twos" (12fps)  
    "min\_hold\_frames": 6, // "Golden Key" minimum duration  
    "layer\_separation": true // "Cel Stacking" for Limited TV  
  },  
  "style\_profile": {  
    "id": "RUBBER\_HOSE",  
    "physics\_engine": {  
      "rigidity": 0.0, // No joints  
      "idle\_state": "ALWAYS\_BOUNCE",  
      "squash\_stretch\_limit": 2.0  
    }  
  },  
  "action\_beats": \[  
    {  
      "type": "ANTICIPATION",  
      "duration\_frames": 4,  
      "vector": "OPPOSITE\_TO\_TARGET"  
    },  
    {  
      "type": "IMPACT",  
      "duration\_frames": 2,  
      "smear\_flag": true // Force 1-frame smear  
    }  
  \]  
}

## B. Pseudocode Library

**1\. Gravity Spacing (The Odd Rule)***Source: 8, 9*  
def apply\_gravity\_spacing(start\_pos, frames, unit\_dist):  
    \# Spacing increases by odd numbers: 1, 3, 5, 7...  
    positions \= \[start\_pos\]  
    current\_y \= start\_pos  
    for t in range(1, frames \+ 1):  
        odd\_multiplier \= (2 \* t) \- 1  
        displacement \= unit\_dist \* odd\_multiplier  
        current\_y \-= displacement  
        positions.append(current\_y)  
    return positions  
**2\. Smear Trigger Logic***Source: 11*  
def check\_for\_smear(pose\_a, pose\_b, object\_width):  
    displacement \= distance(pose\_a, pose\_b)  
    if displacement \> object\_width:  
        return {  
            "generate\_smear": True,  
            "duration": 1, \# Strictly 1 frame  
            "type": "ELONGATED\_MESH" if is\_linear(pose\_a, pose\_b) else "MULTIPLES"  
        }  
    return {"generate\_smear": False}  
**3\. Twinning Detection (QA)***Source: 14, 37*  
def detect\_twinning(left\_limb\_curve, right\_limb\_curve):  
    \# Check for identical values at identical times  
    for t in timeline:  
        if left\_limb\_curve\[t\] \== right\_limb\_curve\[t\]:  
            return "FAIL: Twinning Detected. Offset right limb by 2 frames."  
    return "PASS"

## C. Evaluation Suite

**Test 1: The "Sticky Smear" Check**

* **Input:** Animation sequence with a fast punch.  
* **Condition:** Smear geometry is visible for frames $t$ and $t+1$.  
* **Result:** **FAIL**. Smears must last exactly 1 frame.  
* **Fix:** Delete smear on frame $t+1$. 11

**Test 2: The "Floating Head" Check (Limited Animation)**

* **Input:** Dialogue scene in LIMITED\_TV mode.  
* **Condition:** Head rotates, Body is static. No collar element exists.  
* **Result:** **FAIL**. Neck seam exposed.  
* **Fix:** Add "Collar" asset to mask the layer separation. 25

**Test 3: The "Scooby-Doo" Loop Check**

* **Input:** Walk cycle with scrolling background.  
* **Condition:** Background object Plant\_A repeats every 12 frames (A-A-A).  
* **Result:** **FAIL**. Visible repetition.  
* **Fix:** Apply Syncopation (A-B-A-C) or randomize spacing. 41

