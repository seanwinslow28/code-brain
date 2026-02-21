Here is the **Smears & Multiples Taxonomy and Implementation Guide**, designed as an operational specification for a 2D animation coding agent.

### Module 2: Smears & Fast-Motion Synthesis

**1\) Mental Model**

* **Concept:** Smears are not "motion blur" (a camera artifact); they are **information bridges**. They physically connect two distant points in space to prevent the brain from perceiving a gap (strobing) during high-velocity transit.  
* **The Logic:** If Displacement \> Object\_Width, the eye loses the object's continuity. The agent must fill this gap with *surrogate geometry* (a deformed mesh or multiple instances) that directs the eye along the path of action.  
* **Citation:** "Smear frames bridge the gap between individual frames... to show the path of movement, creating a smooth transition." 1, 2\.

**2\) Rules That Become Code (Bulleted, Atomic)**

* **The Strobing Trigger:**  
* **IF** distance(Pose\_A, Pose\_B) \> Object\_Width:  
* **THEN** Initiate Smear\_Protocol. Standard interpolation is insufficient. 3, 4\.  
* **Topology Selector (Smear vs. Multiple):**  
* **IF** Action\_Type \== "Ballistic" (Linear/Arc transit, e.g., Punch, Zip): Use **Elongated In-between** (Stretch Mesh). 5, 6\.  
* **IF** Action\_Type \== "Cyclic" (Rotation, e.g., Wheels, Running Legs): Use **Multiples** (Ghosting). 7, 5\.  
* **The Single-Frame Constraint:**  
* **Rule:** A smear frame must exist for exactly **1 frame** (at 24fps).  
* **Logic:** If Duration \>= 2 frames, the brain registers it as a static, deformed object ("broken model"). 8, 2\.  
* **Volume Conservation (The Thinning Rule):**  
* **Rule:** If Scale\_Y \> 1.0 (Stretched along motion vector), THEN Scale\_X and Scale\_Z must be \< 1.0.  
* **Formula:** Scale\_Perpendicular \= 1 / sqrt(Scale\_Parallel). 3, 9\.  
* **Leading Edge Visibility:**  
* **Rule:** When using Multiples, render *only* the leading edge (the side facing the direction of travel). Cull the trailing edge to avoid visual noise. 10, 5\.

**3\) Smear Type Selection Map (Action Category)**  
Action Category,Smear Type,Implementation Logic,Rationale/Source  
High-Speed Hit/Punch,Elongated In-between,Stretch mesh from Origin to Target. Shape \= Tube/Ellipse.,"Connects point A to B visually. 11, 12."  
Whip Pan / Head Turn,Mini-Smear,Deform internal features (eyes/nose) trailing the rotation.,"Maintains relative volume while showing force. 13, 14."  
Cyclic Run (Legs),Multiples (Ghosting),Instance geometry 3–5 times along arc. Uneven spacing.,"Avoids ""soupy"" look of stretching rotating limbs. 10, 15."  
Impact (Wall Splat),Compression Smear,"Scale\_Y \< 0.1, Scale\_X \> 3.0. Hold 1 frame before recoil.","Emphasizes sudden stop vs. continuous motion. 16, 17."  
Zip (Exit/Entrance),Motion Tube / Zip,Connect Start\_Pos to Edge\_Of\_Screen. Opacity gradient at tail.,"Indicates direction of departure/entry. 18, 19."  
Vibration/Shock,Double/Triple Image,Render Pos and Pos \+/- Offset on same frame. No blur.,"Simulates high-frequency oscillation. 10, 20."  
**4\) Parameter Defaults \+ Ranges**

* **Smear Duration:** Strictly 1 frame. (Override global framerate to "On Ones"). 14, 2\.  
* **Ghost Count (Multiples):** 2–5 instances.  
* *Constraint:* Do not space evenly. Use geometric progression (close $\\rightarrow$ far) to avoid A-B-A strobing. 10\.  
* **Stretch Factor:**  
* *Cartoony:* 200%–400% of rest length. 18\.  
* *Realistic/Action:* 110%–150% (Mini-smears). 13\.  
* **Opacity Decay (Trails):** Linear fade (1.0 $\\rightarrow$ 0.0) over the length of the trail is often too soft. Prefer "Drybrush" decay (jagged alpha mask). 21, 22\.

**5\) Failure Modes \+ "No-Smear Zones"**

* **No-Smear Zone: Slow Motion.**  
* *Rule:* If Velocity \< Width, disable smears.  
* *Risk:* Looks like a "mutant limb" or glitch. Smears require speed to be felt rather than seen. 23, 14\.  
* **No-Smear Zone: The Hold.**  
* *Rule:* Never smear the final holding pose.  
* *Risk:* "Sticky Smear." The character looks melted. Snap back to solid geometry immediately. 8, 24\.  
* **Failure Mode: "The Blob" (Silhouette Collapse).**  
* *Detection:* Silhouette\_Area(Smear) \< Silhouette\_Area(Rest\_Pose).  
* *Fix:* Smear path must *add* volume/area to the path, not reduce it. Ensure the "Motion Tube" is wide enough. 25, 26\.  
* **Failure Mode: Even Spacing (Multiples).**  
* *Detection:* Distance between Instance A and B equals Distance between B and C.  
* *Fix:* Randomize or progress spacing to prevent "blinking" artifact. 10\.

**6\) QA Checklist**

*  **Duration Check:** Is the deformed mesh visible for only 1 frame? 8\.  
*  **Volume Check:** Does the smear thin out as it stretches? (Avoids growing mass). 3\.  
*  **Strobing Check:** Are there any gaps between the smear tail and the previous frame's position? (Must overlap). 24\.  
*  **Style Consistency:** If Style \== "Spider-Verse", is Motion Blur disabled? (Use CMYK offset instead). 27\.

**7\) Minimal Pseudocode / Structured Spec**  
def generate\_fast\_motion(frame\_prev, frame\_curr, velocity, object\_width, style\_id):  
    displacement \= distance(frame\_prev.pos, frame\_curr.pos)  
      
    \# THRESHOLD CHECK  
    if displacement \< object\_width:  
        return interpolate\_linear(frame\_prev, frame\_curr) \# No smear needed

    \# TYPE SELECTION  
    if is\_cyclic(frame\_curr.action):  
        \# MULTIPLES (Ghosting)  
        instances \= \[\]  
        \# Generate 3 ghosts with progressive spacing (not even)  
        for i in \[0.3, 0.6, 0.85\]:   
            pos \= lerp(frame\_prev.pos, frame\_curr.pos, i)  
            \# Render only Leading Edge for clarity \[10\]  
            ghost \= render\_geometry(pos, cull\_trailing\_edge=True)   
            instances.append(ghost)  
        return composite(instances)

    else:  
        \# ELONGATED SMEAR (Ballistic)  
        \# 1\. Calculate Stretch Vector  
        direction \= normalize(frame\_curr.pos \- frame\_prev.pos)  
        stretch\_mag \= displacement / object\_width  
          
        \# 2\. Deform Geometry  
        \# Constraint: Volume Conservation \[3\]  
        scale\_y \= stretch\_mag  
        scale\_x \= 1.0 / sqrt(scale\_y)   
          
        smear\_mesh \= deform\_mesh(frame\_curr.mesh, scale=(scale\_x, scale\_y, scale\_x), axis=direction)  
          
        \# 3\. Apply Style Filter  
        if style\_id \== "SPIDER\_VERSE":  
            \# No blur, use chromatic aberration \[27\]  
            return apply\_cmyk\_offset(smear\_mesh, velocity)  
        elif style\_id \== "GENNDY\_3D":  
            \# Blend sub-frames, bias to front \[28\]  
            return blend\_subframes(smear\_mesh, bias=0.7)  
        else:  
            return smear\_mesh  
