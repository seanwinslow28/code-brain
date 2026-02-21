Here are the **Style Verification Tests**, designed to validate if a generated animation clip strictly adheres to the specific physics, timing, and rendering constraints of a chosen "Style Profile."

### 1\. Rubber Hose (1920s)

1. **Mental Model:** "Noodle" physics. No rigid joints; constant rhythmic motion synced to audio.  
2. **Measurable Indicators (Heuristics):**  
3. **Rigidity Check:** Joint\_Angle\_Sharpness must be near 0\. Limbs should form smooth curves (C or S), not angles 1, 2\.  
4. **Stasis Detection:** Idle\_Velocity \> 0\. The character must never be perfectly still; it should bounce or sway 3\.  
5. **Sync-to-Audio:** Vertical Bounce\_Frequency matches Audio\_BPM (Musical Synchronization) 4\.  
6. **Planar Constraint:** Z\_Axis\_Translation $\\approx$ 0\. Action occurs on a single flat plane 5\.  
7. **Ease Check:** Spacing\_Curve is Linear or near-Linear (constant speed, no complex easing) 3\.  
8. **Drift Signal:** "Stiff" motion. Limbs show sharp elbows/knees; character holds a static pose without bobbing.  
9. **Correction Routine:** Disable Rigid\_Joints constraints. Force Idle\_State loop to "Bob\_Cycle" synced to beat 5, 6\.

### 2\. Golden Age (Disney 1930s)

1. **Mental Model:** Volumetric realism ("Solid Drawing") with fluid mechanics ("Cushioning") and "Squash & Stretch."  
2. **Measurable Indicators (Heuristics):**  
3. **Volume Integrity:** $Scale\_X \\times Scale\_Y \\times Scale\_Z \\approx 1.0$ at all frames (±5% tolerance) 5, 7\.  
4. **Fluidity Floor:** Framerate is 24fps (Ones) or 12fps (Twos). No 8fps (Threes) allowed 8\.  
5. **Arc Compliance:** End\_Effector\_Path maps to a Bézier curve. Linear paths fail 9, 10\.  
6. **Cushioning:** Acceleration\_Graph shows non-linear spacing (Ease-in/Ease-out) at start/stops 11\.  
7. **Twinning Check:** Limb\_L\_Rot \!= Limb\_R\_Rot (Asymmetry enforced) 4, 12\.  
8. **Follow-Through:** Child\_Joint\_Delay \> 0 frames relative to parent 13\.  
9. **Drift Signal:** "Floaty" motion (Linear spacing), "Shrinking" volume, or symmetrical "Twinning."  
10. **Correction Routine:** Apply Volume\_Conservation constraint. Apply Cubic\_Ease to spacing. Offset Left\_Limb by 2 frames 4, 14\.

### 3\. Limited TV (Hanna-Barbera 1960s)

1. **Mental Model:** "Planned Animation." Economy driven. Sound drives visuals. 80% static.  
2. **Measurable Indicators (Heuristics):**  
3. **The 80/20 Rule:** Active\_Pixel\_Count \< 20% of screen area per frame 15, 16\.  
4. **Layer Separation:** Body\_Layer transform variance \== 0 while Mouth\_Layer variance \> 0 17, 6\.  
5. **Hold Duration:** Average Pose\_Hold \> 12 frames (0.5s). Action is "pose-to-pose" with few in-betweens 18, 7\.  
6. **Cycle Reuse:** Unique\_Frame\_Count / Total\_Frames ratio is low (indicating loops) 14, 19\.  
7. **Viseme Count:** Mouth\_Shape\_ID range is limited to 7–9 shapes 20, 21\.  
8. **Drift Signal:** "Full Animation." The body moves on every frame of dialogue; fluid in-betweens connect every pose.  
9. **Correction Routine:** Freeze Body\_Layer. Quantize Mouth\_Layer to standard viseme chart. Delete every 2nd frame (force Twos/Threes) 17, 18\.

### 4\. Modern Hybrid (Spider-Verse)

1. **Mental Model:** "Stepped" motion (on Twos) without motion blur; print-media imperfections.  
2. **Measurable Indicators (Heuristics):**  
3. **Stepped Rate:** Frame\_Hold\_Duration \== 2 (12fps) for 90% of frames. Switch to 1 only if Velocity \> Threshold 22, 23\.  
4. **Blur Absence:** Pixel\_Motion\_Blur \== 0.0 (Disabled) 24\.  
5. **Offset Mode:** If Velocity is high, CMYK\_Channel\_Offset \> 0 (Misprint effect) 25, 26\.  
6. **Interpolation:** Curve\_Tangent \== Stepped (No splining) 22\.  
7. **Drift Signal:** "Video Game Look." Smooth 60fps interpolation or standard Gaussian motion blur.  
8. **Correction Routine:** Force Stepped\_Interpolation. Disable blur shader. Apply CMYK\_Offset shader based on velocity vector 25, 22\.

### 5\. 3D "Genndy" (Hotel Transylvania)

1. **Mental Model:** 2D "Snap" applied to 3D rigs. Geometry smears instead of blur. Broken rigs.  
2. **Measurable Indicators (Heuristics):**  
3. **Rig Breaking:** Bone\_Stretch\_Limit exceeded (\>200%) for exactly 1 frame during fast moves 27, 15\.  
4. **Smear Geometry:** Mesh\_Topology changes (elongates/multiplies) when Velocity \> Width 28, 29\.  
5. **Silhouette Bias:** Motion\_Blur\_Opacity is weighted \>70% to the "Leading Edge" 28, 1\.  
6. **Transition Speed:** Transition\_Duration (Pose A $\\to$ Pose B) $\\le$ 2 frames (Zip) 11\.  
7. **Drift Signal:** "Interpolated 3D." Slow, floaty transitions; standard pixel blur that muddies the silhouette.  
8. **Correction Routine:** Snap Transition to 1 frame. Generate Sub\_Frame geometry blend. Bias opacity to leading edge 1\.

### 6\. Anime (Traditional)

1. **Mental Model:** "Modulation." Dynamic framerates (1s/2s/3s) based on intensity. Cinematic staging.  
2. **Measurable Indicators (Heuristics):**  
3. **Modulation Variance:** Framerate switches between 8fps, 12fps, and 24fps within the same shot 30, 18\.  
4. **Hold "Tome":** High-intensity poses hold for $\\ge$ 3 frames (Stop-motion feel) 31\.  
5. **Limited Lip-Sync:** Mouth\_Cycle is 3 frames (Open-Middle-Close) loop, independent of precise phonemes 32\.  
6. **Speed Line Density:** If Velocity is high, Background\_Detail replaced by Radial\_Lines 33\.  
7. **Drift Signal:** "Western Smoothness." Constant 24fps or constant 12fps without modulation.  
8. **Correction Routine:** Apply Modulation\_Controller. Reduce lip-sync to 3-step cycle. Insert "Impact Frames" (color inversion) on hits 30, 18\.

### 7\. Screwball (Warner Bros 1940s)

1. **Mental Model:** Extreme exaggeration; Staccato timing. "Zips" and "Takes."  
2. **Measurable Indicators (Heuristics):**  
3. **Staccato Timing:** Velocity\_Graph shows sharp spikes (0 $\\to$ Max $\\to$ 0\) with minimal ease-in 11\.  
4. **Overshoot Magnitude:** Peak\_Pose exceeds Target\_Pose by \> 20% before settling 21\.  
5. **Zip Transition:** Travel\_Time between key locations \= 1 frame 11, 34\.  
6. **Smear Type:** Elongated\_Inbetween connects Start and End positions physically 26\.  
7. **Drift Signal:** "Disney Softness." Too much cushioning (slow-in/slow-out); lack of "snap."  
8. **Correction Routine:** Delete in-betweens (create Zip). Increase Overshoot amplitude. Ensure Smear\_Duration \= 1 frame 20\.

