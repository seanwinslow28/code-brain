Based on the **Smears & Multiples Taxonomy** and **Implementation Guide**, here is the decision tree logic for the coding agent.

### Phase 1: The Trigger Check (Strobing Detection)

**Logic:** IF distance(Pos\_t, Pos\_t-1) \> Object\_Width THEN Initiate Smear Protocol

* **Why:** To prevent "strobing" (the wagon wheel effect). When displacement exceeds the object's width, the eye perceives the object as teleporting or disappearing rather than moving continuously 1, 2, 3\.  
* **What to Do:** Flag the frame for Smear\_Generation or Motion\_Blur\_Synthesis.  
* **What to Avoid:** Applying smears to slow movements. If displacement is small, a smear looks like a "glitch" or a "mutant limb" rather than motion 4, 5\.  
* **Citation:** 1, 2, 3, 5\.

### Phase 2: Topology Selector (Action Type)

**Logic:** IF Action\_Type \== "Cyclic" GOTO Branch A ELSE GOTO Branch B

#### Branch A: Cyclic / Repetitive Motion

*(e.g., Running legs, spinning wheels, vibrating props)*

* **Why:** Stretching geometry on a rotating or repeating object creates a "soupy" or melting look. "Multiples" (Ghosting) preserve the rigid form while indicating speed 6, 7\.  
* **What to Do:**  
* **Generate Multiples:** Instance the geometry 2–5 times along the motion path in a single frame.  
* **Leading Edge Rule:** Render ONLY the leading edge (approaching side) of the object. Cull the trailing edge to prevent visual clutter 8, 7\.  
* **Uneven Spacing:** Distribute the multiples irregularly (progressive spacing) to avoid strobing 8\.  
* **What to Avoid:**  
* **A-B-A Pattern:** Do not space multiples evenly. This creates a "blinking" effect rather than a motion trail 8\.  
* **Full Opacity:** Do not keep all instances at 100% opacity unless the style is "Pop Art." Fade trailing instances 9\.  
* **Citation:** 6, 8, 7\.

#### Branch B: Ballistic / Linear Transit

*(e.g., A punch, a zip exit, a falling anvil)*

* **Why:** The object is physically traveling from Point A to Point B. An "Elongated In-between" physically connects the two points, leading the eye across the gap 10, 11\.  
* **What to Do:**  
* **Deform Mesh:** Stretch vertices along the velocity vector.  
* **Volume Logic:** Apply Scale\_X \= 1 / sqrt(Scale\_Y) (if Y is the stretch axis). As the object lengthens, it must get thinner to preserve volumetric mass 12, 7\.  
* **What to Avoid:**  
* **Volume Loss:** Stretching the object without thinning it. This makes the character appear to grow in size 12, 13\.  
* **Citation:** 10, 11, 12\.

### Phase 3: Stylistic Renderer (The "Look" Filter)

**Logic:** SWITCH (Style\_ID)

* **Case 1: "3D Feature / Genndy Blur"**  
* **Why:** Standard mathematical motion blur makes poses muddy and transparent. "Tempering" blur with geometry retains the silhouette 14, 15\.  
* **What to Do:** Generate Sub\_Frames between the current and previous frame. Blend them into the current frame, but bias opacity (70%+) toward the "Leading Edge" (the future position) 15, 7\.  
* **What to Avoid:** Uniform Gaussian blur that erases internal details 16\.  
* **Case 2: "Spider-Verse / Comic"**  
* **Why:** To mimic print media imperfections and avoid the "softness" of digital blur 17\.  
* **What to Do:** Disable Motion Blur. Apply CMYK\_Offset (chromatic aberration) or "Speed Lines" (2D texture overlays) along the velocity vector 17, 18\.  
* **What to Avoid:** Any form of opacity blur or soft edges 17\.  
* **Case 3: "Vintage / Drybrush"**  
* **Why:** Simulates the physical brush characteristics of 1940s cel animation 6, 19\.  
* **What to Do:** Apply an Alpha\_Texture with "scratchy" or "jagged" edges trailing the object. Fade opacity non-linearly 6, 19\.  
* **What to Avoid:** Solid vector shapes; the trail must look like it is "decaying" 20\.  
* **Citation:** 15, 6, 19, 17\.

### Phase 4: Temporal Constraint (The Safety Valve)

**Logic:** SET Duration \= 1 Frame

* **Why:** Smears are a trick of the eye. If they persist longer than 1/24th of a second, the brain registers them as a static object (a "mutant" or "broken" model) rather than a burst of speed 8, 21\.  
* **What to Do:** Force the frame rate to "Ones" (24fps) for this specific frame, even if the rest of the scene is on "Twos." Immediately return to the normal model on the very next frame 21, 5\.  
* **What to Avoid:** "Sticky Smears." Holding a deformed mesh for $\\geq$ 2 frames 5, 22\.  
* **Citation:** 8, 21, 5\.

