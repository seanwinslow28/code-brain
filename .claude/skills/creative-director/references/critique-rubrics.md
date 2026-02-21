# Critique Rubrics & Critique-to-Action Map

Read this reference when reviewing or critiquing work-in-progress. Use the scoring rubrics to evaluate each dimension, then use the Critique-to-Action Map to translate observations into tool-specific fixes.

## Scoring Rubric (1-4 Scale)

### A. Graphic Design / Static (Photoshop / Illustrator)

| Score | Hierarchy | Balance | Typography | Technical |
|-------|-----------|---------|------------|-----------|
| 4 | Eye travels in intended order: dominant → sub-dominant → subordinate | Composition weighted correctly (Rule of Thirds, Golden Ratio) | Readable contrast and size; legible font choice and kerning | Correct color mode and resolution for target |
| 3 | Clear primary focal point, minor competing elements | Generally balanced with minor weight issues | Readable but kerning or leading needs adjustment | Minor spec issues (e.g., 150dpi for 300dpi target) |
| 2 | Multiple elements compete for attention | Noticeable imbalance pulling eye off-center | Font size or contrast makes reading difficult | Wrong color mode or resolution for deliverable |
| 1 | No clear hierarchy; everything looks equal | Composition feels random or lopsided | Text is unreadable at intended viewing distance | Critical spec failures (RGB for print, 72dpi for large format) |

### B. Motion Design (After Effects)

| Score | Timing & Spacing | 12 Principles | Readability in Motion | Technical |
|-------|------------------|---------------|----------------------|-----------|
| 4 | Organic feel; S-curves in Graph Editor | Squash/stretch, anticipation, follow-through all present | Text readable at speed; hold times sufficient | Motion blur on; continuous rasterization where needed |
| 3 | Mostly smooth; 1-2 linear keyframes remain | Some principles applied but missing secondary motion | Most text readable; one element too fast | Motion blur on but inconsistent settings |
| 2 | Robotic feel; mostly linear interpolation | Only basic ease-in/ease-out, no secondary motion | Key text unreadable at playback speed | No motion blur; jagged edges on scaled layers |
| 1 | Instant jumps or uniform speed throughout | No easing applied; all linear keyframes | Text flashes too fast to register | Comp settings wrong (mismatched fps, wrong bit depth) |

### C. Video Editing (Premiere Pro)

| Score | Pacing | Continuity | Audio Mix | Color |
|-------|--------|------------|-----------|-------|
| 4 | Cut rhythm matches emotional beat and audio | 180-degree rule respected; eyelines consistent | Dialogue clear at -12dB; music ducked effectively | Consistent grade and white balance across shots |
| 3 | Generally good pacing with 1-2 awkward holds | Minor continuity breaks that most viewers won't notice | Dialogue audible but music slightly loud | Minor white balance variance between 1-2 shots |
| 2 | Sections drag or feel rushed; uneven rhythm | Noticeable jump cuts or axis violations | Dialogue competes with music; levels unbalanced | Visible color temperature shifts between shots |
| 1 | No sense of rhythm; cuts feel random | Major continuity errors (screen direction, eyeline) | Dialogue buried; audio peaking or too quiet | No color correction; raw footage look |

## Critique-to-Action Map

Use this table to translate critique observations into specific Adobe tool actions.

### 1. Composition & Focal Point
*"The subject gets lost." / "The framing feels unbalanced." / "No clear entry point."*

| App | Actions |
|-----|---------|
| **Photoshop** | Crop Tool (C) with Rule of Thirds overlay. Radial Gradient Fill on Multiply layer for vignette. Gaussian Blur on background layers to isolate subject. |
| **Illustrator** | Artboard Tool to resize/reframe. Scale Tool (S) to enlarge subject. Lower opacity of background textures. |
| **After Effects** | Adjust Camera Z-position/Point of Interest. Enable Depth of Field on Camera Layer. Apply Vignette to Adjustment Layer. |
| **Premiere** | Adjust Scale/Position in Effect Controls to punch in. Add Vignette in Lumetri Color. Gaussian Blur on background track. |

### 2. Visual Hierarchy
*"Everything looks equally important." / "The eye path is confusing."*

| App | Actions |
|-----|---------|
| **Photoshop** | Add Drop Shadow or Outer Glow via Layer Styles. Darken background midtones with Levels (Ctrl+L). |
| **Illustrator** | Recolor key element to complementary/accent. Add contrasting stroke. Increase negative space. |
| **After Effects** | Stagger layer start times (primary elements arrive first). Scale bump keyframes (100% → 110% → 100%). |
| **Premiere** | HSL Secondary in Lumetri to desaturate background. Mask Lumetri effect to brighten subject only. |

### 3. Color Harmony
*"Colors are clashing." / "Palette feels disjointed." / "Mood doesn't match."*

| App | Actions |
|-----|---------|
| **Photoshop** | Gradient Map adjustment layer to unify tones. Hue/Saturation to shift specific channels. |
| **Illustrator** | Edit Colors > Recolor Artwork to specific Harmony Rule. Global Edit swatches to unify. |
| **After Effects** | Lumetri Curves to align RGB channels. Tint Effect to map blacks/whites to brand palette. |
| **Premiere** | Color Wheels: push Shadows (teal) and Highlights (orange). Color Match in Lumetri to align shots. |

### 4. Typography
*"Text is hard to read." / "Too many fonts." / "Kerning feels sloppy."*

| App | Actions |
|-----|---------|
| **Photoshop** | Character Panel: adjust Tracking and Kerning. Layer Style Stroke or Drop Shadow for contrast. |
| **Illustrator** | Set Leading to 1.2-1.5x font size. Create Outlines to tweak letter nodes. |
| **After Effects** | Animate Menu > add Tracking animator. Drop Shadow: Effect > Perspective > Drop Shadow. |
| **Premiere** | Essential Graphics: Responsive Design - Time for intro/outro. Stroke/Shadow via appearance tab. |

### 5. Pacing & Rhythm
*"It drags in the middle." / "Cuts feel jarring." / "Motion is monotonous."*

| App | Actions |
|-----|---------|
| **After Effects** | Time Remapping (Cmd+Opt+T) to speed ramp. Graph Editor: Hold keyframes for stop-motion. Vary keyframe spacing. |
| **Premiere** | Ripple Edit (B) to trim to music beats. Rate Stretch (R) to speed/slow clips. Remix Tool to retime music. |

### 6. Animation Timing & Easing
*"Movement feels robotic." / "Stops too abruptly." / "Lacks weight."*

| App | Actions |
|-----|---------|
| **After Effects** | Easy Ease (F9) for basic smoothing. Graph Editor bezier handles for S-curves. Add overshoot keyframes past target. |
| **Premiere** | Right-click keyframe > Ease In/Out for temporal interpolation. Change spatial to Linear to fix boomerang paths. |

### 7. Lighting & Shadows
*"Lighting feels flat." / "Shadows don't match." / "Subject isn't grounded."*

| App | Actions |
|-----|---------|
| **Photoshop** | Curves/Levels per layer. Paint shadows on Multiply layer, highlights on Overlay. Gradient Fill for light source. |
| **Illustrator** | Gradient Mesh for 3D shading. Drop Shadow: Effect > Stylize (keep global light consistent). |
| **After Effects** | Add Point/Parallel/Spot lights with Cast Shadows. Adjust Specular and Metal material properties. |
| **Premiere** | Lumetri Exposure and Contrast. Shadow/Highlight effect. Mask to create pool of light. |

### 8. Audio Balance
*"Dialogue is hard to hear." / "Music is overpowering." / "Mix sounds muddy."*

| App | Actions |
|-----|---------|
| **After Effects** | Keyframe Audio Levels (L). Pan with Stereo Mixer. (Ideally send to Premiere/Audition.) |
| **Premiere** | Essential Sound: tag types, Auto-Duck music against dialogue. Parametric EQ: cut <100Hz on dialogue. |

### 9. Edge Control & Masking
*"The cutout looks fake." / "Edges are too sharp/soft." / "Matte lines are jittery."*

| App | Actions |
|-----|---------|
| **Photoshop** | Select and Mask: Shift Edge (negative) to remove halos, Feather to soften. Defringe: Layer > Matting. |
| **Illustrator** | Clipping Mask (Cmd+7) for clean crops. Pathfinder Trim/Divide for overlapping edges. |
| **After Effects** | Increase Mask Feather. Simple Choker effect. Alpha Matte for clean reveals. |
| **Premiere** | Feather mask edge in Effect Controls. Ultra Key: adjust Choke and Soften for green screen. |

### 10. Export Quality
*"Footage looks pixelated." / "Colors look washed out." / "File size is too huge."*

| App | Actions |
|-----|---------|
| **Photoshop** | Export As PNG-24 (transparency) or JPG @ 80% (web). Convert to sRGB for web. |
| **Illustrator** | SVG for web; 300ppi PNG for print. Anti-aliasing: Type Optimized for text. |
| **After Effects** | ProRes 422 for master; H.264 for web. Set 16/32 bpc to fix banding. |
| **Premiere** | Media Encoder High Bitrate (10-20Mbps for 1080p). Render at Maximum Depth. VBR 2-Pass. |
