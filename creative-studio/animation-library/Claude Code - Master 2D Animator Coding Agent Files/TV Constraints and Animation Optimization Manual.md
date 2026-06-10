Here is the **TV Constraints & Animation Strategies Manual**, designed as a structured specification for a coding agent to optimize animation for limited budgets and high-volume production.

### Module 3: Optimization Logic (Planned Animation)

**1\) Mental Model**

* **Concept:** "Planned Animation." Unlike feature animation, where movement drives performance, TV animation is an engineering challenge where **Sound drives Visuals**. The goal is not fluid realism but "limited" efficiency: maximizing the screen time of static assets while restricting movement to essential narrative focal points.  
* **The 80/20 Heuristic:** A scene is optimized when **80%** of the screen pixels are static (held cels/backgrounds) and only **20%** contain unique frame-by-frame movement (mouths, eyes, limbs).  
* **Citation:** "Limited animation is... a necessarily strategic process of systematizing animation production... 80% static poses supporting dialogue, and 20% original movement." 1, 2, 3\.

**2\) Rules That Become Code (Bulleted, Atomic)**

* **The "Bank" First Protocol:**  
* **IF** Action\_Type is generic (e.g., "Walk," "Laugh," "Surprise Take"):  
* **THEN** Query Asset\_Library for existing cycles or poses. Do *not* generate new frames.  
* **Logic:** Reuse is the cornerstone of the "Marathon" pipeline. 3, 4, 5\.  
* **Cel Stacking (Layer Separation):**  
* **Rule:** Deconstruct Character into hierarchical layers: Level\_1\_Body (Static) $\\rightarrow$ Level\_2\_Head (Occasional Move) $\\rightarrow$ Level\_3\_Mouth/Eyes (Active).  
* **Constraint:** The Body layer must hold for $\>24$ frames (1 second) whenever possible.  
* **Citation:** "Limited animation is based on dividing a character into as many as four cel levels... body on level 1 and the mouth on top of this on level 2." 6, 3\.  
* **Audio-Driven Timing:**  
* **Input:** The audio track (dialogue) is the master timeline.  
* **Rule:** "The Timer" assigns frame counts to the X-sheet *before* animation begins. Visuals must stretch or compress to fit the audio beat, not vice versa.  
* **Citation:** "The recording of the voice actors... becomes essentially the blueprint... the exact timing of the facial animation is made to match." 7, 3\.  
* **The "Necktie" Masking Rule:**  
* **IF** separating Head from Body:  
* **THEN** Ensure character design includes a collar, necktie, or necklace to mask the seam between the moving head and static body.  
* **Citation:** "The possibly noticeable boundary between the two was obscured by giving the character neck clothing: a shirt collar and tie." 6, 3\.

**3\) "Reuse Planner" Rule Set**

* **Cycle Logic (Looping):**  
* **Trigger:** Action \== "Walk," "Run," "Rain," "Smoke."  
* **Execution:** Create 1 cycle (e.g., 12–16 frames for a walk) and loop indefinitely.  
* **Syncopation:** To avoid the "Flintstones Effect" (repetitive backgrounds), syncopate background elements (e.g., pattern 1-2-1-2) rather than rote repetition (1-1-1-1).  
* **Citation:** "Reuse walks/runs indefinitely... syncopate elements." 8, 9, 3\.  
* **Lateral Staging (The Pan):**  
* **Trigger:** Character travels long distance.  
* **Execution:** Keep Character X\_Pos static (Walk Cycle). Animate Background\_Layer translation opposite to direction of travel.  
* **Citation:** "Characters run in place against looping BG." 3, 10\.  
* **The "Muzzle" System:**  
* **Trigger:** High-volume dialogue.  
* **Execution:** Animate *only* the mouth area (muzzle). Keep the upper skull/eyes static on a separate layer. Use a "5 o'clock shadow" or line art boundary to mask the muzzle seam.  
* **Citation:** "Separate the 'muzzle' (mouth area) onto its own layer... five-o’clock shadow around their mouth." 11, 3\.

**4\) Mouth/Face Economy Guidelines**

* **Viseme Reduction (The 7-Shape Limit):**  
* **Constraint:** Map all audio phonemes to a maximum of 7–9 visual shapes (A, E, O, Closed, F/V, etc.).  
* **Logic:** Do not animate every syllable. "Moosh" minor sounds together.  
* **Citation:** "We’ve reduced the animation of speech to nine standard mouth positions... and a character has a full vocabulary." 12, 13\.  
* **Closed Mouth Priority:**  
* **Rule:** The "Closed" mouth (M, B, P) is mandatory for readability. It must hold for $\\ge 2$ frames.  
* **Citation:** "Lips fully compressed; mandatory for readability... ensure closed mouths hold for min 2 frames." 14, 3\.  
* **Blink Modulation:**  
* **Rule:** If the body is static for $\>2$ seconds, trigger a Blink or Eye\_Dart to maintain the illusion of life ("Moving Hold").  
* **Citation:** "Never leave a character dead static... use a 'moving hold' or frequent blinks." 3, 15\.

**5\) Staging Rules for Economy**

* **Planar Restriction:**  
* **Rule:** Restrict movement to X/Y axes. Avoid Z-axis (movement toward/away from camera) as it requires new drawings for scale changes.  
* **Citation:** "All the characters move either to the left or right, rarely away from you... eliminates the need for tricky three-dimensional effects." 16, 3\.  
* **Camera As Animator:**  
* **Trigger:** Establishing shot or dramatic reveal.  
* **Action:** Use a static, high-resolution drawing. Apply Camera\_Zoom (Truck) or Camera\_Pan to simulate motion.  
* **Citation:** "Use camera movement... on static artwork to create the illusion of motion." 3, 17\.  
* **Omission (The Cut-Away):**  
* **Trigger:** Complex impact (Crash/Explosion) or difficult mechanics.  
* **Action:** Cut to a reaction shot or a "Zap/Dust" effect frame *instead* of animating the contact.  
* **Citation:** "Cut to reaction shot or 'Zap' effect frame instead of animating contact." 3\.

**6\) "Polish Budget" Allocator**

* **Strategy:** Allocate limited frame resources based on the "Hierarchy of Intensity."  
* **Tier 1: High Budget (On Ones / Unique)**  
* **Context:** Title Sequences, Stock Footage (Banked for repeated use), Extreme Emotion (Close-ups).  
* **Action:** Animate on Ones (24fps). Use full cel layers.  
* **Citation:** "Stock sequences... were used intensely... Title sequence." 18, 19\.  
* **Tier 2: Standard Budget (On Twos)**  
* **Context:** Dialogue, Walking, Standard Acting.  
* **Action:** Animate on Twos (12fps). Reuse Body layer; animate Head/Arms.  
* **Citation:** "Twos work well for most actions... half as much work." 20, 3\.  
* **Tier 3: Economy Budget (On Threes/Fours)**  
* **Context:** Holds, Slow Drifts, Background Crowds.  
* **Action:** Animate on Threes (8fps) or Fours (6fps). Use "Stop-Motion" aesthetic or "Slide Motion" (static image sliding).  
* **Citation:** "On Threes... slightly jerky, stylized... limited animation." 21, 22\.

**7\) QA Checklist**

*  **Static Ratio Check:** Is the updated pixel count $\< 20\\%$ of the screen? 2\.  
*  **Layer Integrity:** Does the head move independently of the body without revealing a gap (Necktie check)? 6\.  
*  **Bank Query:** Was the Asset Library checked for a reusable "Walk" before creating this new one? 4\.  
*  **Viseme Count:** Does the lip-sync use $\\le 9$ distinct mouth shapes? 13\.

**8\) Pseudocode / Structured Spec**  
def generate\_tv\_sequence(script\_event, asset\_library, audio\_track):  
    \# 1\. CHECK BANK (Reuse Planner)  
    if asset\_library.has\_cycle(script\_event.action\_type):  
        return asset\_library.get\_cycle(script\_event.action\_type)

    \# 2\. SETUP LAYERS (Cel Stacking)  
    layers \= {  
        "Level\_1\_Body": generate\_static\_pose(script\_event.character),  
        "Level\_2\_Head": generate\_static\_pose(script\_event.character.head),  
        "Level\_3\_Mouth": \[\]  
    }

    \# 3\. AUDIO-DRIVEN TIMING  
    phonemes \= analyze\_audio(audio\_track)  
      
    \# 4\. VISEME MAPPING (Economy)  
    for phoneme in phonemes:  
        viseme \= map\_to\_standard\_9\_shapes(phoneme) \# Moosh minor sounds  
        layers\["Level\_3\_Mouth"\].append(viseme)

    \# 5\. POLISH ALLOCATOR (Framerate)  
    if script\_event.is\_fast\_action:  
        framerate \= 1 \# On Ones  
    elif script\_event.is\_dialogue:  
        framerate \= 2 \# On Twos  
    else:  
        framerate \= 3 \# On Threes (Holds)

    \# 6\. STAGING CHECK  
    if script\_event.camera\_move\_z \> 0:  
        \# Reject Z-depth move, convert to Truck-In on static art  
        return apply\_camera\_truck(layers, audio\_track.duration)  
          
    return assemble\_x\_sheet(layers, framerate)  
