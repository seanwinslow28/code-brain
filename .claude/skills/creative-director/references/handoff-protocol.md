# App Handoff Protocol (AHP)

Read this reference when transitioning from the Creative Director's strategic planning to execution in an Adobe app skill. Fill in the bracketed fields based on the interview and selected route.

## 1. Strategic Directive (The "North Star")

- **Single Objective:** [One sentence defining the primary problem. e.g., "Create a high-energy 15s Instagram Reel to drive clicks to the new RPG beta."]
- **Creative Intent:** [Mood/tone. e.g., "Gritty, noir aesthetic with neon accents; high contrast; fast-paced rhythmic editing."]
- **Target Audience:** [Psychographics. e.g., "Gen Z gamers familiar with pixel art tropes."]
- **Primary Platform:** [e.g., "Instagram Stories (9:16) & YouTube Shorts."]

## 2. Asset Audit

- **Existing Assets:**
  - [ ] Footage/Photography: [file types, e.g., .MOV ProRes 422, .PSD layers]
  - [ ] Brand Assets: [logos, color palettes, fonts]
  - [ ] Copy/Script: [finalized text doc]
- **Missing / To-Be-Created:**
  - [ ] [e.g., "Vector assets for the HUD interface need creation in Illustrator"]
  - [ ] [e.g., "Voiceover audio is pending; use scratch track"]
- **File Structure:**
  - [ ] Root Folder: `_YYMMDD_ProjectName`
  - [ ] Subfolders: `_Assets`, `_ProjectFiles`, `_Renders`, `_Ref`

## 3. Technical Specifications

- **Resolution:** [e.g., 1080x1920 (Vertical)]
- **Frame Rate:** [e.g., 24fps for cinematic, 60fps for gameplay]
- **Color Space:** [e.g., Rec.709 (Video), sRGB (Web), CMYK (Print)]
- **Safe Zones:** [e.g., "Keep text out of bottom 15% for TikTok UI"]
- **Brand Constraints:**
  - [ ] Fonts: [list allowed fonts]
  - [ ] Colors: [list hex codes]
- **Naming Convention:** `YYMMDD_ProjectName_Element_v01`

## 4. Execution Roadmap

### Phase A: Asset Prep (Illustrator / Photoshop)
1. **[Illustrator]** Create vector elements. Use Create Outlines for text if sharing files.
2. **[Photoshop]** Prep raster assets. Isolate subjects with masks. Set color profile to [sRGB/AdobeRGB].
3. **[Action]** Name layers logically (e.g., "FG_Character", "BG_Texture") for import.

### Phase B: Assembly & Motion (Premiere / After Effects)
1. **[Premiere]** Create Assembly Cut. Sync audio and visuals on timeline.
2. **[After Effects]** Import assets as "Composition - Retain Layer Sizes."
3. **[After Effects]** Animate: blocking → easing (Graph Editor) → secondary motion.

### Phase C: Finishing (Media Encoder / Photoshop)
1. **[AE/Premiere]** Color correction (Lumetri). Check for crushed blacks / clipped whites.
2. **[Media Encoder]** Render final output per platform specs.

## 5. Verification Checkpoints

- [ ] **30% (Rough):** Is timing right? Composition balanced? Share screenshot for concept review.
- [ ] **60% (Structure):** Brand colors correct? Hierarchy clear? Motion has weight (easing)?
- [ ] **90% (Polish):** Spelling? Glitches? Audio mix (-12dB to -6dB)? Color consistency?

## 6. Definition of Done

- [ ] **Technical Integrity:** No flash frames, audio peaking, or resolution mismatches.
- [ ] **Objective Met:** Asset clearly communicates the key message from Section 1.
- [ ] **Accessibility:** Text contrast meets WCAG AA (4.5:1 ratio).
- [ ] **File Hygiene:** Project organized, unused assets removed, dependencies collected.
