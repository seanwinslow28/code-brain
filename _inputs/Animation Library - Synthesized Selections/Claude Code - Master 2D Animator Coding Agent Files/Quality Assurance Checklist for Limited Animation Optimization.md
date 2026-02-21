Here is the **QA Checklist for Limited Animation**, designed to optimize "Planned Animation" pipelines. It focuses on maximizing economy without sacrificing narrative clarity or appeal, preventing the common "cheap" artifacts associated with budget constraints.

### Module: Limited Animation Quality Control

**1\) Mental Model**

* **Concept:** "Planned Animation" is an engineering challenge where **Sound drives Visuals**. "Cheapness" usually stems from mechanical redundancy (bad loops) or "death by stasis" (freezing the character completely).  
* **The Heuristic:** High-quality limited animation is not about moving *more*; it is about moving *less* but with perfect timing. "The pause is as important as the movement."  
* **Citation:** "Limited animation is... a necessarily strategic process... 80% static poses supporting dialogue, and 20% original movement." 1, 2\. "The pregnant pause is a staple element... the cartoon takes it almost as far as it can go." 3\.

**2\) Rules That Become Code (Bulleted, Atomic)**

* **The 80/20 Static Limit:**  
* **Rule:** If Active\_Pixels \> 20% of Total\_Pixels AND Scene\_Type \== "Dialogue", **FLAG** for review. (Economy violation).  
* **Correction:** Switch to Cel Stacking (Static Body / Active Mouth). 2, 4\.  
* **The "Alive" Hold Rule:**  
* **Rule:** If Pose\_Duration \> 24 frames (1 sec) AND Variance \== 0, **TRIGGER** "Moving Hold."  
* **Action:** Apply subtle "Traceback" or "Drift" (sub-pixel movement) to prevent the character from looking dead. 5, 6\.  
* **Background Syncopation:**  
* **Rule:** When looping backgrounds (e.g., hallway run), avoid A-A-A repetition. Use A-B-A-C or 1-2-1-2 patterns.  
* **Reason:** Hides the "Miles-long living room" effect. 7\.  
* **Audio-Visual Lead:**  
* **Rule:** Visual\_Accent\_Frame \= Audio\_Accent\_Frame \- 2\.  
* **Reason:** Visuals should precede sound by \~2 frames for maximum impact. 8\.

**3\) Parameter Defaults \+ Ranges (With Rationale)**

* **Moving Hold Drift:** 1–2% variance over 12+ frames.  
* *Rationale:* Keeps character alive without looking "shaky" or unstable. 6\.  
* **Blink Timing (Asymmetric):**  
* *Close:* 3 frames. *Hold:* 1 frame. *Open:* 4 frames.  
* *Rationale:* Symmetric blinks look robotic; asymmetry adds organic appeal even in limited styles. 9\.  
* **Dialogue Exposure:** On Twos (12fps) or Threes (8fps).  
* *Rationale:* "Chattering" mouths on Ones can look jittery against a static body. 10, 11\.

**4\) Failure Modes \+ Detection Signals**

* **Failure:** **"The Floating Head."**  
* *Signal:* Head\_Layer rotates \> 15 degrees while Body\_Layer remains static.  
* *Fix:* Ensure "Necktie/Collar" masking is present, or rotate shoulders slightly to match. 4, 12\.  
* **Failure:** **"Strobing Pans."**  
* *Signal:* Camera\_Velocity \> 0 AND Character\_Framerate \< 24fps (Ones).  
* *Fix:* If camera pans, switch character to Ones to prevent "judder" against background. 13, 14\.  
* **Failure:** **"Sliding Feet" (Foot Skate).**  
* *Signal:* Foot\_Velocity (in screen space) \!= Background\_Pan\_Velocity during contact phase.  
* *Fix:* Match cycle speed to pan speed. 15, 16\.

**5\) QA Checklist: Preventing the "Cheap" Look**

#### A. Appeal & Life Preservation

*  **The Dead Hold Check:** Does any character remain *perfectly* pixel-static for \> 1 second?  
* *Fix:* Add a blink, an eye dart, or a "moving hold" (traceback/drift). 6, 17\.  
*  **Twinning Detector:** Are the character's arms or legs mirroring each other (symmetrical pose \+ symmetrical timing)?  
* *Fix:* Offset one limb by 2–4 frames or change its angle. Twinning looks robotic. 18, 19\.  
*  **Asymmetric Blinks:** Do blinks follow the "Fast Close / Slow Open" rule?  
* *Fix:* Ensure the open phase is slower than the close phase. Symmetric blinks look artificial. 9\.  
*  **Neck Connection:** If using separate head/body layers (Cel Stacking), is the seam masked by a collar or jawline?  
* *Fix:* Verify no "disconnect" pixels appear during head rotation. 12\.

#### B. Clarity & Staging

*  **Silhouette Squint Test:** Is the pose readable in pure black & white?  
* *Fix:* Create negative space between arms and torso to prevent "blobbing." 20, 21\.  
*  **Planar Movement:** Does the character move primarily on the X/Y axis?  
* *Fix:* Avoid Z-axis walks (toward camera) in limited budgets; they require too many unique drawings. 22, 23\.  
*  **Lip-Sync Anchors:** Does the mouth fully close (M, B, P phonemes) for at least 2 frames?  
* *Fix:* "Moosh" minor syllables, but ensure closed consonants are distinct to prevent "mushy" dialogue. 24, 25\.

#### C. Reuse & Repetition (The "Cheap" Detectors)

*  **Cycle Syncopation:** In a loop, do background elements repeat in a predictable 1-1-1 pattern?  
* *Fix:* Randomize spacing or use 1-2-1-2 patterns to hide the loop. 7\.  
*  **Context Mismatch:** Is a banked "stock gesture" being used in a context that doesn't match its intensity?  
* *Fix:* Ensure the "angry" stock pose isn't used for "mild annoyance." 26, 27\.  
*  **Sliding Feet:** During a walk cycle pan, do the feet "stick" to the ground?  
* *Fix:* Recalculate pan speed to match stride length ($V \= D/T$). 15, 16\.

#### D. Rhythm & Timing

*  **Contrast in Timing:** Is the motion evenly spaced (metronomic)?  
* *Fix:* Create "Fast Move \-\> Hard Stop" contrast. Avoid "floaty" even spacing. 28, 29\.  
*  **Audio Lead:** Do physical accents (hits/takes) happen 2 frames *before* the sound?  
* *Fix:* Shift animation track \-2 frames relative to audio. 8\.  
*  **Exposure Check:** Is fast action (smears/zips) on Ones (24fps) while dialogue is on Twos (12fps)?  
* *Fix:* Modulate framerate based on velocity. Fast \= Ones. 10, 14\.

**6\) Minimal Pseudocode / Structured Spec**  
def validate\_limited\_animation(shot\_data):  
    \# 1\. DEAD HOLD DETECTION  
    for character in shot\_data.characters:  
        static\_frames \= count\_consecutive\_static\_frames(character)  
        if static\_frames \> 24 and not character.has\_moving\_hold:  
            print("FAIL: Character is 'dead' for \>1 sec. Add drift/blink.")  
            return False

    \# 2\. TWINNING CHECK  
    if check\_symmetry(character.left\_arm, character.right\_arm):  
        print("FAIL: Twinning detected. Offset L/R timing by 2 frames.")  
        return False

    \# 3\. 80/20 BUDGET CHECK  
    pixel\_delta \= calculate\_pixel\_change(shot\_data)  
    if pixel\_delta \> 0.20 and shot\_data.type \== "limited\_dialogue":  
        print("WARNING: Too much movement for limited budget. Use Cel Stacking.")  
      
    \# 4\. FOOT SKATE (SLIDING)  
    if shot\_data.is\_walk\_cycle:  
        foot\_speed \= get\_foot\_speed(character)  
        pan\_speed \= get\_camera\_speed()  
        if abs(foot\_speed \- pan\_speed) \> tolerance:  
            print("FAIL: Sliding feet detected. Match pan speed to stride.")  
            return False

    return True  
