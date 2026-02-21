Here is the **Test Suite for Smears & Multiples**, designed to validate the output of a 2D animation generation agent against the provided core canon.

### Part 1: The “Good” Cases (Success Scenarios)

**1\. The Ballistic Transit (Linear Smear)**

* **Description:** A character throws a punch where the fist travels from Start (Frame A) to Target (Frame C) in a single frame interval.  
* **Expected Behavior:** The agent generates a single "Elongated In-between" connecting Frame A and C. The mesh is deformed into a tube/ellipse shape.  
* **Key Parameters:** Duration \= 1 frame. Shape \= Continuous geometry from origin to target.  
* **Source:** "Smear frames... bridge the gap... typically an elongated drawing that supports the transitioning... quickly from one pose to another." 1, 2\.

**2\. The Cyclic Multiple (Wheel/Legs)**

* **Description:** A character running at high speed (cyclic motion) or a spinning wheel.  
* **Expected Behavior:** The agent uses "Multiples" (Ghosting) rather than stretching. The geometry is instanced 3–5 times along the arc in a single frame.  
* **Key Parameters:** Spacing \= Uneven (Progressive). Visibility \= Leading edge only (cull trailing edges).  
* **Source:** "Repeating movement... use the same 3 or 5 swishes... multiples will have to be spaced differently... must not follow an A-B-A pattern." 3, 2\.

**3\. The "Genndy Blur" (3D Integration)**

* **Description:** A 3D character moves \> screen width in one frame.  
* **Expected Behavior:** Agent generates sub-frames between key poses and blends them into the current frame, biasing opacity toward the final position to maintain silhouette.  
* **Key Parameters:** Blur\_Type \= Geometry blend (not pixel blur). Bias \= \>70% opacity on Leading Edge.  
* **Source:** "Add extra poses in the sub-frames and that tempered the motion blur... retained the forms and readability." 4, 5\.

**4\. The "Mini-Smear" (Head Turn)**

* **Description:** A character turns their head quickly (whip pan) but not instantaneously.  
* **Expected Behavior:** Internal features (eyes, nose, mouth) drag slightly behind the cranium rotation, or the head stretches slightly (\< 120%) for 1 frame.  
* **Key Parameters:** Stretch\_Factor \= 1.1x – 1.2x. Target \= Internal facial features.  
* **Source:** "Distort internal features... mini-smears for smaller actions." 6, 7\.

**5\. The Impact Splat (Wall Hit)**

* **Description:** A character slams into a wall at high velocity.  
* **Expected Behavior:** The agent generates a "Ken Harris Wall Splat"—the character stretches *before* impact to bridge the gap, preventing a visual disconnect between "near wall" and "on wall."  
* **Key Parameters:** Frame\_Pre\_Impact \= Elongated stretch touching the wall. Frame\_Impact \= Extreme Squash.  
* **Source:** "Stretching out its shape before the impact... prevents a noticeable gap in screen space." 8, 9\.

**6\. The Spider-Verse "Misprint" (No-Blur)**

* **Description:** High-velocity action in a comic-book style render.  
* **Expected Behavior:** Motion blur is strictly disabled. Speed is conveyed via CMYK channel offsets or "Speed Lines" (texture overlays).  
* **Key Parameters:** Motion\_Blur \= OFF. Effect \= Chromatic Aberration / Color Offset.  
* **Source:** "Avoided using blurring... utilized an effect that mimics the misprints... slight offset between colors." 10, 2\.

**7\. The "Zip" Exit**

* **Description:** A character exits the screen instantly.  
* **Expected Behavior:** A single frame drawing connecting the character's start position to the edge of the screen, tapering off (or using drybrush opacity) at the tail.  
* **Key Parameters:** Transit\_Time \= \< 3 frames. Tail\_Opacity \= Gradient/Textured fade.  
* **Source:** "Elongated drawing connecting Start \-\> End points... Zip Turn." 1, 2\.

**8\. Vibration (The "Shudder")**

* **Description:** A character is struck by a heavy object and vibrates in place.  
* **Expected Behavior:** Agent generates a "Vibrating Multiple" showing *both* the leading and trailing outlines to create a double-exposure effect.  
* **Key Parameters:** Outline\_Visibility \= Both Leading & Trailing. Offset \= \< 5 pixels.  
* **Source:** "Showing both outlines is recommended for vibrating or back-and-forth motions." 3\.

**9\. The "Noodle" (Chaos/Tumble)**

* **Description:** A character tumbles down a cliff or loses control of limbs.  
* **Expected Behavior:** Joints are removed. Limbs curve into "S" shapes or "wiggles" to convey lack of skeletal rigidity during the transit.  
* **Key Parameters:** Rigidity \= 0%. Joint\_Constraints \= Disabled.  
* **Source:** "Limbs can lose their joints altogether and even be distorted... wiggly noodle." 11, 12\.

**10\. Drybrush Trail (Vintage Style)**

* **Description:** An object moves fast in a 1940s/vintage aesthetic context.  
* **Expected Behavior:** The trail is not a solid vector shape but a textured alpha mask (simulating dry bristles) that fades non-linearly.  
* **Key Parameters:** Texture \= Scratchy/Jagged. Fill \= Non-solid.  
* **Source:** "Swishes (done with drybrush) indicate arcs... orchestration of thick/thin lines." 13, 14\.

### Part 2: The "Bad" Cases (Failure Modes)

**1\. The "Sticky" Smear**

* **Description:** A distorted smear frame remains on screen for 2 or more frames.  
* **Why it Fails:** The human eye has time to focus on the distortion, registering it as a "mutant" or broken model rather than a blur.  
* **Fix:** Force Smear\_Duration to exactly **1 frame**. If the action is slower, remove the smear and use standard in-betweens.  
* **Source:** "If a smear lasts too long, the viewer starts perceiving it as a static detail... stick movement." 15, 16\.

**2\. The "Sausage" (Volume Increase)**

* **Description:** An object stretches along the motion vector (Y-axis) but maintains its original X and Z width.  
* **Why it Fails:** The object appears to gain mass/grow in size, breaking physical believability.  
* **Fix:** Apply Volumetric Conservation: If Scale\_Y \> 1.0, then Scale\_X \= 1/sqrt(Scale\_Y).  
* **Source:** "If we stretched the ball out... but didn't compensate... the body itself would be expanding gaining mass." 17, 18\.

**3\. The "Blinking" Multiple (A-B-A Spacing)**

* **Description:** A cyclic action (spinning wheel) uses multiples spaced evenly apart.  
* **Why it Fails:** Even spacing creates a stroboscopic "blinking" effect where the eye tracks the gap rather than the motion.  
* **Fix:** Use uneven or progressive spacing (e.g., Fibonacci or log scale) for the ghosts.  
* **Source:** "They must not follow an A-B-A pattern because then they would appear blinking." 3\.

**4\. The "Ghost" Limb (Slow Motion Smear)**

* **Description:** A smear is triggered when Displacement \< Object\_Width.  
* **Why it Fails:** At slow speeds, the smear looks like a graphical glitch or a "mutant limb" because the eye can track the object without help.  
* **Fix:** Set a trigger threshold: IF Velocity \< Width THEN Disable\_Smear.  
* **Source:** "If you use these tricks to slow a movement you end up with a mutant limb." 7, 16\.

**5\. The "Muddy" Blur (Standard Motion Blur)**

* **Description:** Using standard Gaussian/Pixel motion blur on a 2D or Cel-Shaded character.  
* **Why it Fails:** It reduces the visual impact of the pose, creating a "muddy" or transparent image that loses silhouette clarity.  
* **Fix:** Use "Genndy Blur" (geometry tempering) or "Smear Frames" (solid shapes) instead of opacity blur.  
* **Source:** "Motion blur was basically my enemy because it blurs all these great drawings away." 19, 20\.

**6\. The "Soupy" Cycle**

* **Description:** Using elastic deformation (stretching) on a rotating object like a running leg or wheel.  
* **Why it Fails:** Stretching a rotating object destroys its rigid structure, making it look like liquid or "soup."  
* **Fix:** Switch algorithm to **Multiples** (Ghosting) for cyclic/rotational action.  
* **Source:** "Repeating movement... use the same 3 or 5 swishes multiples... stretching looks soupy." 3, 21\.

**7\. The "Double Vision" (Trailing Edge)**

* **Description:** A multiple shows both the front (leading) and back (trailing) outlines of a moving object.  
* **Why it Fails:** It creates visual clutter and confuses the directionality of the volume.  
* **Fix:** Render *only* the leading edge (approaching side). Cull the back face/trailing edge.  
* **Source:** "Multiples often only show the outline of one side... An approaching element has the front outline visible." 3\.

**8\. The "Gap" (Strobing)**

* **Description:** An object moves a large distance, and the smear geometry does not physically touch the previous frame's position.  
* **Why it Fails:** The eye perceives a gap, breaking the continuity of the path (strobing).  
* **Fix:** Ensure the Smear/Elongation physically overlaps or connects Point A and Point B.  
* **Source:** "Bridge the gap... if there’s a noticeable gap in screen space... it looks weird." 9, 22\.

**9\. The "Broken" Silhouette**

* **Description:** A smear frame is generated, but the resulting shape is unrecognizable or obscures the character's line of action.  
* **Why it Fails:** Animation depends on clear silhouettes; a messy smear confuses the brain about what the object is.  
* **Fix:** Run a Silhouette\_Check: Does the smeared mass still convey the "gist" of the character's form?  
* **Source:** "Retain the forms and readability of the character's shape during fast actions." 23, 2\.

**10\. Twinning in Smears**

* **Description:** Both arms/legs smear identically and symmetrically in the same frame.  
* **Why it Fails:** Creates a "dead" or robotic appearance, even in fast motion.  
* **Fix:** Offset the timing of one limb's smear by 1 frame or vary the shape of the smear on the secondary limb.  
* **Source:** "Avoid symmetry... Twinning... creates a rather boring and unappealing pose." 24, 25\.

