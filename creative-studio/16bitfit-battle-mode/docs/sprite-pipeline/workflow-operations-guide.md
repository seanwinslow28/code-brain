# 16BitFit Battle Mode: Complete Sprite Production Workflow Guide

**Purpose:** This is your operations manual. It tells you exactly what assets you need, what prompts to use, how the workflow flows end-to-end, and what "done" looks like at every stage.

---

## Table of Contents

1. [The Big Picture](#1-the-big-picture)
2. [Asset Count Per Fighter](#2-asset-count-per-fighter)
3. [Total Project Scope](#3-total-project-scope)
4. [The Two Generation Strategies](#4-the-two-generation-strategies)
5. [Reference Assets You Need Before Starting](#5-reference-assets-you-need-before-starting)
6. [Strategy Decision Map: Which Animations Use Which Strategy](#6-strategy-decision-map)
7. [Image-Only Workflow (Step by Step)](#7-image-only-workflow)
8. [Hybrid Keyframe-to-Video Workflow (Step by Step)](#8-hybrid-keyframe-to-video-workflow)
9. [Master Prompt Library](#9-master-prompt-library)
10. [Post-Processing: From Raw Output to Game-Ready](#10-post-processing)
11. [Sprite Sheet Assembly](#11-sprite-sheet-assembly)
12. [Quality Checklist](#12-quality-checklist)
13. [Execution Order: What to Do First](#13-execution-order)
14. [Common Failure Modes and Fixes](#14-common-failure-modes-and-fixes)
15. [Glossary of Key Terms](#15-glossary)

---

## 1. The Big Picture

Your game needs animated sprite sheets for 12 fighters (6 Champions + 6 Bosses). Each fighter has 13 combat animations. Each animation has 4–12 frames. Every frame is a 128×128 pixel art image (256×256 for bosses) in Street Fighter II style.

**The pipeline flow:**

```
Reference Assets → AI Generation → Post-Processing → Sprite Sheet Assembly → Engine Validation → Ship
```

You have two generation strategies:

- **Image-Only** — Generate each frame individually with Gemini 3 Pro Image (Nano Banana Pro). Proven to work for simple poses. Fails at walk cycles.
- **Hybrid Keyframe-to-Video** — Generate 2-4 keyframes with Gemini, interpolate the motion between them with a video model (Pika/Kling/Veo), then convert the video output back to pixel art. Solves the walk cycle problem.

The pipeline software (Node.js CLI) automates the retry logic, quality checking, and assembly. But YOU drive the generation — choosing prompts, reviewing output, and making creative calls.

---

## 2. Asset Count Per Fighter

### Champions (128×128 px, 6 characters)

| Animation | Frames | Strategy | Notes |
|-----------|--------|----------|-------|
| Idle | 4 | Image-Only | Subtle breathing bounce. Loops. |
| Walk Forward | 8 | **Hybrid** | Full walk cycle. Left/right leg alternation. Loops. |
| Walk Backward | 8 | **Hybrid** | Defensive retreat. Loops. |
| Crouch | 4 | Image-Only | Transition from standing to crouched. |
| Jump | 4 | Image-Only or Hybrid | Vertical arc: crouch → rise → peak → land. |
| Light Punch | 6 | Image-Only | Quick jab, front hand. |
| Medium Punch | 8 | Image-Only | Cross punch with body rotation. |
| Heavy Punch | 8 | Image-Only | Haymaker, full body commitment. |
| Light Kick | 6 | Image-Only | Quick front kick. |
| Heavy Kick | 8 | Image-Only or Hybrid | Roundhouse with full rotation. |
| Block | 6 | Image-Only | Arms raised, defensive absorption. |
| Take Hit | 6 | Image-Only | Recoil from impact. |
| Victory | 8 | Image-Only | Character-specific celebration. |
| Defeat | 8 | Image-Only | Falling, lying defeated. |
| **Special Move** | 12 | **Hybrid** | Character-specific signature move. Complex motion. |

**Total frames per Champion: 96 frames**
**Total frames for all 6 Champions: 576 frames**

### Bosses (256×256 px, 6 characters)

Bosses use the same animation set but at double resolution (256×256) for their larger, more imposing presence. Frame counts are identical.

**Total frames per Boss: 96 frames**
**Total frames for all 6 Bosses: 576 frames**

---

## 3. Total Project Scope

| Category | Count |
|----------|-------|
| Champions | 6 |
| Bosses | 6 |
| Animations per fighter | 15 |
| Frames per fighter | 96 |
| **Total frames (full game)** | **1,152** |
| Sprite sheets | ~180 (1 per animation per fighter, some combined) |

**MVP scope (validate the pipeline first):**

| Milestone | Scope |
|-----------|-------|
| MVP-1 | Sean × Idle (4 frames) + Walk (8 frames) = 12 frames |
| MVP-2 | Sean × All 15 animations = 96 frames |
| MVP-3 | All 6 Champions × All animations = 576 frames |
| MVP-4 | Full roster (Champions + Bosses) = 1,152 frames |

You should NOT attempt MVP-3 until MVP-1 is rock-solid and the pipeline is automated.

---

## 4. The Two Generation Strategies

### Strategy A: Image-Only (Proven, Simpler)

**How it works:** You generate each frame individually using Gemini 3 Pro Image (Nano Banana Pro) with character reference images + pose reference images. Each frame is an independent API call.

**Best for:** Poses that are distinct and describable — idle stances, punches, blocks, crouches, victory/defeat. Single-pose or short transition animations where each frame is a clear, different pose.

**Weakness:** Cannot reliably differentiate subtle sequential positions (left leg forward vs. right leg forward in walk cycles). Text descriptions alone can't communicate precise body mechanics across a frame sequence.

**Success rate expectation:** ~80-90% first-pass approval for simple animations, ~40-60% for complex ones. Retry ladder handles failures.

### Strategy B: Hybrid Keyframe-to-Video (New, For Locomotion)

**How it works:**
1. Generate 2-4 keyframes using the proven Image-Only method (these are your "anchor poses")
2. Feed those keyframes into a video model (Pika Pikaframes, Kling, or Veo) which interpolates motion between them
3. Extract individual frames from the video output
4. Run each frame through the Pixel Quantizer to convert from smooth video back to pixel art spec
5. Audit the resulting frames

**Best for:** Walk cycles, complex multi-phase movements (roundhouse kicks, special moves), any animation where frame-to-frame coherence matters more than individual frame quality.

**Weakness:** Adds pipeline complexity, video model costs, and depends on the Pixel Quantizer working (Phase 0 gate check). Video models may introduce identity drift.

**Success rate expectation:** Unknown until Phase 1 testing. Target: ≥60% frame pass rate after quantization.

---

## 5. Reference Assets You Need Before Starting

For EACH fighter, you need these reference assets prepared before generation:

### Required (Per Character)

| Asset | Description | How to Create |
|-------|-------------|---------------|
| **Anchor Image** | Single, canonical image of the character in their signature fighting stance. This is the identity lock — every other image must look like this person. | Generate with Nano Banana Pro using character description + style prompt. Hand-pick the best result. |
| **Turnaround Sheet** | 3-5 angle views of the character (front, 3/4, side, back) on a single image. Proves consistent identity across angles. | Generate with Nano Banana Pro using the anchor as reference + explicit angle prompts. |
| **Character Palette JSON** | The exact hex colors for this character (skin, hair, eyes, clothing, outlines, shadows). Used by the Pixel Quantizer. | Extract from the Character Descriptions doc. Already defined for all 12 fighters. |

### Required (Per Animation, for Image-Only)

| Asset | Description | How to Create/Find |
|-------|-------------|---------------------|
| **Pose Reference Image(s)** | Visual reference showing the exact body position for each frame. Could be a skeleton/mannequin reference, a fighting game sprite reference, or a custom stick figure. | Find online (CGTyphoon walk cycles, fighting game sprite sheets for reference). For unique poses, create simple stick figure guides. |

### Required (Per Animation, for Hybrid)

| Asset | Description | How to Create |
|-------|-------------|---------------|
| **Keyframe Images** | 2-4 individual frames generated with Image-Only strategy. These become the start/end/mid points for video interpolation. | Generate using the Image-Only workflow below. |
| **Motion Prompt** | Text description of the motion between keyframes (for the video model). | Write based on animation type. Templates provided in the prompt library below. |

### Already Created (from previous work)

You already have anchor images and turnaround sheets for all 6 Champions and 6 Bosses. These are listed in `prd.md` under `anchorAssets`. The palettes are defined in `Champion Character Descriptions - 12-31-25.md` and `Boss-Character-Descriptions.md`.

---

## 6. Strategy Decision Map

How to decide which strategy for each animation:

```
Is the animation a looping locomotion cycle (walk forward, walk backward)?
  → YES → Use Hybrid Keyframe-to-Video
  → NO ↓

Does the animation involve complex rotational motion (roundhouse kick, special move)?
  → YES → Try Image-Only first. If leg/body differentiation fails after 2 retries, escalate to Hybrid.
  → NO ↓

Is each frame a clearly distinct pose (punch wind-up → punch extension → recovery)?
  → YES → Use Image-Only
  → NO ↓

Default → Image-Only with pose references. Escalate to Hybrid if quality is unacceptable.
```

**Summary mapping:**

| Animation | Primary Strategy | Fallback |
|-----------|-----------------|----------|
| Idle | Image-Only | — |
| Walk Forward | **Hybrid** | Image-Only + skeleton refs |
| Walk Backward | **Hybrid** | Image-Only + skeleton refs |
| Crouch | Image-Only | — |
| Jump | Image-Only | Hybrid (if camera tracking fails) |
| Light Punch | Image-Only | — |
| Medium Punch | Image-Only | — |
| Heavy Punch | Image-Only | — |
| Light Kick | Image-Only | — |
| Heavy Kick | Image-Only | Hybrid (if rotation fails) |
| Block | Image-Only | — |
| Take Hit | Image-Only | — |
| Victory | Image-Only | — |
| Defeat | Image-Only | — |
| Special Move | **Hybrid** | Image-Only frame-by-frame |

---

## 7. Image-Only Workflow (Step by Step)

This is the workflow for generating frames one at a time with Gemini 3 Pro Image (Nano Banana Pro).

### Step 1: Prepare Your Inputs

For each frame you want to generate, gather:
- Character anchor image (PNG)
- Character turnaround sheet (PNG)
- Pose reference image for this specific frame (PNG or found online)

### Step 2: Write the Prompt

Use the **Dual-Reference Prompt Template** (proven to work best):

```
Generate a single full-body image of this character in the exact pose
shown in [POSITION DESCRIPTION] of the [REFERENCE NAME] image.

Apply the character's appearance from the uploaded character reference
images to match the body position of [SPECIFIC ELEMENT] in [POSITION]—
[DETAILED POSE DESCRIPTION: leg positions, arm positions, weight
distribution, torso angle].

Character faces right. Match the exact visual style: Street Fighter II
arcade aesthetic with bold #272929 dark outlines (2-3px), 3-4 tone cel
shading on face showing bone structure, top-front lighting, pixel
rendering approach. Frame size 128×128 pixels. Full body visible from
head to feet, centered in frame with consistent baseline. Clean solid
chroma key green (#00FF00) background. Maintain perfect identity
consistency with the character reference: same face structure, hair
style, muscle definition, clothing details. Output a single crisp
character image. No anti-aliasing, no gradients, no text, no
additional elements.
```

**What to attach to the prompt:**
1. Character anchor image
2. Character turnaround sheet
3. Pose reference image (the skeleton/mannequin/sprite reference for this specific frame)

### Step 3: Generate

Run the prompt through Nano Banana Pro (Gemini 3 Pro Image). The pipeline CLI handles this via `pipeline run <manifest.yaml>`.

If running manually (before the pipeline is built), use the Gemini API or AI Studio directly.

### Step 4: Review

Check the output against these criteria:
- Does it look like the same character as the anchor?
- Is the pose correct (matching the reference)?
- Are the outlines bold and clean (#272929)?
- Is the background solid chroma green (#00FF00)?
- Are proportions consistent (head size, limb length)?
- Is the character facing right?
- Is there any text, artifacts, or extra elements?

### Step 5: Retry if Needed

If the output fails, the pipeline's RetryManager follows this ladder:
1. **Edit prompt** — Rephrase the pose description, add more detail
2. **Re-anchor** — Regenerate using the anchor as a stronger reference
3. **Tighten** — Add negative prompts ("no extra limbs, no text, no background elements")
4. **Stop** — After max retries, flag for manual intervention

### Step 6: Approve and Save

Approved frames go into the run's `approved/` directory with naming convention:
```
champion-sean-walk-forward-f01.png
champion-sean-walk-forward-f02.png
...
```

---

## 8. Hybrid Keyframe-to-Video Workflow (Step by Step)

This is the workflow for animations that need frame-to-frame coherence (walk cycles, complex motions).

### Step 1: Generate Keyframes (Using Image-Only)

For a walk cycle (8 frames), generate 2-4 keyframes using the Image-Only workflow above. Choose the most important poses:

**Walk Cycle Keyframes (4 keyframes for 8-frame cycle):**
- **KF1 (Frame 0):** Contact — right foot forward, left foot pushing off
- **KF2 (Frame 2):** Passing — feet together, weight centered
- **KF3 (Frame 4):** Contact (mirror) — left foot forward, right foot pushing off
- **KF4 (Frame 6):** Passing (mirror) — feet together again

Use skeleton/mannequin references (CGTyphoon or similar) for precise leg positioning.

### Step 2: Upload Keyframes to Video Model

Feed the approved keyframes to the video model:

**Pika Pikaframes (Primary — via fal.ai API):**
- Upload up to 5 keyframes with specified timing
- Set duration: ~2 seconds
- Set creativity low (~0.3) to stay close to keyframes
- Motion prompt: "Pixel art character walking forward in a smooth cycle, maintaining consistent proportions and style"

**Kling 3.0 (Alternative):**
- Upload start frame + end frame
- Enable Elements 3.0 character lock (upload 3-8 second reference video of the character)
- Similar motion prompt

**Veo 3.1 (Alternative):**
- Upload first + last frame + up to 3 reference images
- Set style parameters for animation

### Step 3: Extract Frames from Video

Use ffmpeg to pull out individual frames at the target count:

```bash
# Extract 8 evenly-spaced frames from a 2-second video
ffmpeg -i video.mp4 -vf "select='eq(n\,0)+eq(n\,6)+eq(n\,12)+eq(n\,18)+eq(n\,24)+eq(n\,30)+eq(n\,36)+eq(n\,42)'" -vsync vfr frame_%03d.png
```

The pipeline's PostProcessor handles this automatically.

### Step 4: Run Through Pixel Quantizer

The extracted frames will look like "sludge" — correct motion but wrong art style (smooth, anti-aliased, gradients, wrong colors). The Pixel Quantizer converts them back to pixel art:

1. Downscale to 128×128 (nearest-neighbor)
2. Snap every pixel to character palette
3. Smooth temporal jitter across sequence
4. Re-apply bold outlines
5. Clean up alpha/transparency
6. Align baselines

### Step 5: Review Quantized Output

Check against the same criteria as Image-Only, plus:
- Do the legs clearly alternate left/right correctly?
- Is the motion smooth when played as an animation?
- Is the character identity consistent across all frames?
- Does the walk cycle loop cleanly (frame 0 ≈ frame 7 wrapped)?
- Are there any "melting" or morphing artifacts from video interpolation?

### Step 6: Iterate if Needed

If the output fails, the Hybrid retry ladder:
1. **Regenerate video** — Same keyframes, different seed/creativity setting
2. **Adjust creativity** — Lower creativity = closer to keyframes but potentially jerky
3. **Regenerate keyframes** — Maybe the keyframes themselves were inconsistent
4. **Swap video model** — Try a different model (Pika → Kling → Veo)
5. **Fallback to Image-Only** — Use skeleton refs for every frame individually
6. **Stop** — Flag for manual intervention

---

## 9. Master Prompt Library

### Base Style Anchor (append to every generation prompt)

```
Match the exact visual style: Street Fighter II arcade aesthetic with
bold #272929 dark outlines (2-3px), 3-4 tone cel shading, top-front
lighting, pixel rendering approach. Frame size [128×128 | 256×256]
pixels. Full body visible from head to feet, centered in frame with
consistent baseline. Clean solid chroma key green (#00FF00) background.
No anti-aliasing, no gradients, no text, no additional elements.
```

### Search Grounding Prefix (optional — invoke for style accuracy)

```
Search for Street Fighter II CPS1 arcade sprite characteristics—outline
weight, color palette limitations, shading technique, typical frame
dimensions. Apply these authentic specifications to generate this
fighting game character sprite.
```

### Negative Prompt (append when quality issues appear)

```
No extra limbs, no text labels, no watermarks, no background elements,
no props, no weapons unless specified, no duplicate characters, no
split frame, no anti-aliased edges, no soft gradients, no motion blur,
no glow effects.
```

### Animation-Specific Prompts

**Idle (4 frames):**
```
Generate a single full-body image of this character in a subtle
[FRAME: 1=neutral ready stance | 2=slight knee bend down |
3=neutral ready stance | 4=slight rise up] position.

Standing in fighting ready stance with [CHARACTER-SPECIFIC STANCE
DESCRIPTION]. Subtle weight shift suggesting breathing/readiness.
Arms in guard position, feet shoulder-width apart.

[ATTACH: Anchor + Turnaround]
[APPEND: Base Style Anchor]
```

**Walk Forward Keyframes (for Hybrid — generate 4 keyframes):**
```
Generate a single full-body image of this character in the exact pose
shown in Position [1|2|3|4] of the uploaded walk cycle reference.

[KF1: Contact pose — right foot planted forward, left leg extending
behind, arms in opposite swing to legs, torso slightly forward-leaning]

[KF2: Passing pose — feet together passing under body, weight on
right leg, left foot lifting, arms at sides]

[KF3: Contact mirror — left foot planted forward, right leg extending
behind, opposite arm swing, torso forward-leaning]

[KF4: Passing mirror — feet together again, weight transitioning,
arms at sides]

Character faces right, walking forward confidently.
[ATTACH: Anchor + Turnaround + Walk Cycle Skeleton Reference]
[APPEND: Base Style Anchor]
```

**Walk Forward Video Prompt (for video model interpolation):**
```
Pixel art character walking forward in a smooth repeating cycle.
Maintain consistent proportions, consistent outline weight, and
consistent color palette throughout. Legs alternate naturally with
clear weight transfer. Arms swing opposite to legs. Camera stays
fixed, character moves in place. Solid green background. Smooth,
steady pace.
```

**Light Punch (6 frames):**
```
Generate a single full-body image of this character in frame [N] of
a quick jab punch animation:

Frame 1: Ready stance, fists up in guard
Frame 2: Front shoulder pulling back slightly (wind-up)
Frame 3: Front arm extending forward, fist rotating, rear arm guarding
Frame 4: Full extension, fist at target height, body rotated slightly
Frame 5: Arm beginning to retract
Frame 6: Return to guard stance

[ATTACH: Anchor + Turnaround + Boxing jab reference (optional)]
[APPEND: Base Style Anchor]
```

**Heavy Kick (8 frames):**
```
Generate a single full-body image of this character in frame [N] of
a powerful roundhouse kick animation:

Frame 1: Fighting stance
Frame 2: Weight shifting to front leg, rear knee lifting
Frame 3: Hip rotation beginning, kicking leg chambered
Frame 4: Full hip rotation, leg extending outward
Frame 5: Maximum extension, foot at target height
Frame 6: Leg beginning to retract
Frame 7: Leg returning, hip de-rotating
Frame 8: Landing back in stance

[ATTACH: Anchor + Turnaround + Roundhouse kick reference]
[APPEND: Base Style Anchor]
```

**Jump (4 frames):**
```
Generate a single full-body image of this character in frame [N] of
a vertical jump:

Frame 1: Crouch preparation (knees bent, arms down)
Frame 2: Rising (legs extending, arms pulling up)
Frame 3: Peak (body fully extended, slight tuck)
Frame 4: Descending (legs tucking for landing)

[ATTACH: Anchor + Turnaround]
[APPEND: Base Style Anchor]
```

**Block (6 frames):**
```
Frame 1: Standing ready
Frame 2: Arms raising to guard
Frame 3: Full block position (forearms crossed or up in front)
Frame 4: Impact absorption (slight backward lean)
Frame 5: Recovering
Frame 6: Return to guard
```

**Take Hit (6 frames):**
```
Frame 1: Normal stance (moment of impact)
Frame 2: Head/body snapping back from hit
Frame 3: Maximum recoil
Frame 4: Stagger (off-balance)
Frame 5: Recovering balance
Frame 6: Return to stance
```

**Victory (8 frames):**
```
Character-specific celebration. Examples:
- Sean: Fist pump, flexing pose
- Mary: Dynamic kickboxing celebration move
- Marcus: Shadow boxing victory dance

Frame 1-2: Transition from fighting stance to celebration
Frame 3-6: Main celebration animation
Frame 7-8: Hold final victory pose
```

**Defeat (8 frames):**
```
Frame 1: Final hit reaction
Frame 2-3: Staggering
Frame 4-5: Falling backward/sideways
Frame 6-7: Hitting the ground
Frame 8: Lying defeated (hold)
```

### Character Palette Blocks (append to prompts)

**Sean:**
```
Character colors: light peach skin (#F5D6C6), dirty blonde messy short
hair (#C2A769), steel blue eyes (#4682B4), off-white sleeveless athletic
tank (#F2F0EF), neon blue gym pants (#2323FF), white sneakers with dark
soles (#F5F5F5 shoes, #272929 soles).
```

**Mary:**
```
Character colors: light peach skin (#F5D6C6), medium brown hair in
athletic ponytail (#6D4C41), warm brown eyes (#654321), pink athletic
tank/sports bra (#FF7BAC), purple workout shorts (#7E57C2), deep purple
headband (#9C27B0), white sneakers (#F5F5F5).
```

**Marcus:**
```
Character colors: warm brown skin (#8D5524), short black athletic hair
(#212121), dark brown eyes (#4A4A4A), dark gray athletic tank (#545454),
light gray athletic pants (#C4BEBB), white sneakers with dark soles
(#F5F5F5 shoes, #272929 soles), gold boxing gloves (#FFD700).
```

**Aria:**
```
Character colors: warm tan skin (#C68642), dark brown hair tied back
(#4B3621), dark green eyes (#06402B), magenta dance/athletic top
(#9A2257), blue flowing athletic pants (#5577AA), white flexible
shoes (#F5F5F5).
```

**Kenji:**
```
Character colors: light beige skin (#FFDBAC), black hair neatly tied
back (#212121), deep brown eyes (#4A4A4A), light gray martial arts top
(#B0BEC5), dark gray loose training pants (#424242), white minimalist
shoes (#F5F5F5).
```

**Zara:**
```
Character colors: olive beige skin (#CBB59D), dark brown hair tied
tightly (#3B2F2F), dark brown eyes (#654321), dark gray powerlifting
tank (#545454), black athletic pants (#212121), white powerlifting
shoes (#F5F5F5).
```

---

## 10. Post-Processing

Every generated frame (whether from Image-Only or Hybrid) goes through post-processing before it's considered "approved."

### For Image-Only Frames

Minimal processing needed since Gemini already outputs pixel art:

1. **Verify dimensions** — Must be exactly 128×128 (or 256×256 for bosses)
2. **Background cleanup** — Ensure chroma green is fully removed, clean alpha
3. **Palette check** — Verify all pixels are on-palette (minor drift is common)
4. **Outline check** — Verify bold outlines are present and consistent

### For Hybrid Frames (Full Quantizer Pipeline)

Heavy processing required to convert video output to pixel art:

1. Nearest-neighbor downscale (1080p → 128×128)
2. Palette quantization (snap every pixel to character LUT)
3. Temporal smoothing (lock static regions across frame sequence)
4. Outline enforcement (re-apply bold #272929 edges)
5. Alpha recovery (remove background, clean fringe)
6. Baseline registration (align feet consistently)
7. Validation report generation

---

## 11. Sprite Sheet Assembly

Once all frames for an animation are approved, they're assembled into a sprite sheet.

### Layout Rules

- **Arrangement:** Single row, left-to-right (1×N where N is frame count)
- **Frame size:** 128×128 per frame (champions) or 256×256 (bosses)
- **Padding:** 2px between frames (prevents texture bleeding in-engine)
- **Background:** Fully transparent
- **Format:** PNG (sprite sheet image) + JSON (TexturePacker atlas metadata)

### Example: Sean Walk Forward (8 frames)

```
Sheet dimensions: (128 × 8) + (2 × 7 padding) = 1038 × 128 px

[Frame0][2px][Frame1][2px][Frame2][2px]...[Frame7]
```

### Naming Convention

```
champion-sean-walk-forward.png        ← sprite sheet image
champion-sean-walk-forward.json       ← atlas metadata (TexturePacker format)
```

Frame names within the atlas JSON:
```
champion-sean-walk-forward-f00.png
champion-sean-walk-forward-f01.png
...
champion-sean-walk-forward-f07.png
```

### Assembly Tool

TexturePacker CLI handles this automatically. The pipeline's PackerAdapter wraps it:

```bash
TexturePacker \
  --format phaser \
  --data champion-sean-walk-forward.json \
  --sheet champion-sean-walk-forward.png \
  --padding 2 \
  --trim-mode None \
  --algorithm Basic \
  --max-width 2048 \
  --max-height 2048 \
  approved/champion-sean-walk-forward-f*.png
```

### Validation

After assembly, the Phaser headless validator checks:
- Atlas loads without errors
- Frame dimensions are consistent
- Animation plays without visible jitter
- Pivot points are correct
- No baseline drift between frames

---

## 12. Quality Checklist

Run this checklist on every frame before approval:

### Per-Frame Checks

- [ ] **Identity match** — Looks like the same character as the anchor
- [ ] **Correct pose** — Matches the intended frame of the animation
- [ ] **Facing right** — Character faces right (flipping is done in-engine)
- [ ] **Correct dimensions** — Exactly 128×128 (champions) or 256×256 (bosses)
- [ ] **Clean outlines** — Bold #272929 outlines, 2-3px weight, no gaps
- [ ] **On palette** — All pixel colors match the character palette
- [ ] **Clean background** — Fully transparent, no fringe or halo
- [ ] **Centered** — Character centered horizontally in frame
- [ ] **Feet visible** — Full body from head to feet, nothing cropped
- [ ] **No artifacts** — No text, extra limbs, duplications, blur, gradients

### Per-Animation Checks (after all frames approved)

- [ ] **Consistent proportions** — Head size, limb length, body width match across all frames
- [ ] **Consistent style** — Shading direction, outline weight, detail level match across frames
- [ ] **Smooth motion** — Animation reads as smooth when played at target FPS
- [ ] **Baseline alignment** — Feet hit the same vertical position across all frames (±1px)
- [ ] **Loop integrity** — For looping animations (idle, walk), frame 0 connects smoothly to the last frame
- [ ] **Correct sequence** — Frames are in the right order (the motion makes physical sense)

### Per-Sprite-Sheet Checks (after assembly)

- [ ] **Loads in Phaser** — Atlas JSON + PNG load without errors
- [ ] **Plays without jitter** — Animation plays smoothly in-engine
- [ ] **No texture bleeding** — Padding prevents neighboring frame colors from leaking
- [ ] **Correct frame naming** — Frame keys in JSON match expected naming convention

---

## 13. Execution Order: What to Do First

### Phase 0: Build the Pixel Quantizer (Week 1)

**Goal:** Prove that video output can be converted to clean pixel art.

**What to do:**
1. Give Claude Code the kickoff prompt (included as a separate document)
2. Claude Code builds the standalone quantizer script
3. Run experiments Q-01 through Q-04 with synthetic test data
4. Review results — does the output look like acceptable pixel art?

**Gate check:** If Q-01 through Q-04 pass, proceed. If they fail, explore fallbacks before investing in video model APIs.

### Phase 1: Test Video Models (Weeks 2-4)

**Goal:** Find the best video model for walk cycle interpolation.

**What to do:**
1. Generate 4 keyframes of Sean's walk cycle using Nano Banana Pro (Image-Only)
2. Run the Loop Integrity Test on at least 2 video models (use the same image as start and end frame with an idle motion prompt — measures identity drift)
3. Run walk cycle experiments W-01 through W-05 across Pika, Kling, Veo
4. Score results on: leg differentiation (30%), identity consistency (25%), palette fidelity (15%), baseline stability (15%), alpha quality (10%), style preservation (5%)
5. Select the winning model

**What you need:**
- API access to Pika (via fal.ai), Kling, and/or Veo
- 4 approved keyframe images of Sean walking
- The quantizer from Phase 0

### Phase 2: End-to-End Pipeline (Weeks 5-8)

**Goal:** Generate a complete Sean walk cycle from manifest to Phaser-validated atlas.

**What to do:**
1. Extend the pipeline manifest schema for hybrid strategy
2. Integrate the winning video model as an adapter
3. Wire the quantizer into the pipeline as a PostProcessor
4. Run: `pipeline run manifests/champion-sean/walk-forward.yaml`
5. Validate the output sprite sheet in Phaser

### Phase 3: Scale to Full Roster (Weeks 9+)

**Goal:** Generate all animations for all fighters.

**What to do:**
1. Image-Only animations first (idle, punches, kicks, block, hit, victory, defeat for Sean)
2. Then hybrid animations (walk forward, walk backward, special for Sean)
3. Then second character (validate generalization)
4. Then remaining Champions
5. Then Bosses (at 256×256)

---

## 14. Common Failure Modes and Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Character doesn't match anchor | Insufficient identity lock | Attach turnaround sheet + anchor. Add "maintain perfect identity consistency" to prompt. |
| Wrong pose / wrong limb positions | Text description ambiguity | Add pose reference image (skeleton, mannequin, or fighting game sprite). Never rely on text alone for complex poses. |
| Background not solid green | Model generates environmental elements | Add "clean solid chroma key green (#00FF00) background" explicitly. Negative prompt: "no environment, no floor, no sky." |
| Anti-aliased / soft edges | Model defaults to modern rendering | Add "crisp pixels, no anti-aliasing, no gradients." Add search grounding prefix to invoke SF2 style. |
| Text in output | Model adds labels/watermarks | Add "no text, no labels, no watermarks" to prompt. |
| Extra limbs / duplicates | Model hallucination | Simplify pose description. Add "single character only, no duplicates." |
| Walk cycle legs don't alternate | Text can't communicate L/R difference | Switch to Hybrid strategy with visual pose references. This is the core problem Hybrid solves. |
| Video output looks "melted" | Video model introduces morphing artifacts | Lower creativity/motion scale. Use more keyframes (4 instead of 2). Try different video model. |
| Quantized frames look blocky/destroyed | Palette too limited or threshold too aggressive | Add shading variants to palette. Adjust static threshold. Try 2× resolution and downscale. |
| Baseline drift (ice skating) | Frames not aligned vertically | Quantizer baseline registration step. If persistent, manually align in image editor. |
| Identity drift across frames | Video model changes character appearance | Use Kling Elements character lock. Add Gemini restyle pass. Regenerate with lower creativity. |

---

## 15. Glossary

| Term | Meaning |
|------|---------|
| **Anchor Image** | The single canonical image that defines a character's visual identity. Every other frame must match this. |
| **Turnaround Sheet** | Multi-angle views of a character proving consistent identity from different viewpoints. |
| **Keyframe** | A key pose in an animation sequence, generated with the proven Image-Only method, used as input for video interpolation. |
| **Pixel Quantizer** | Post-processing pipeline that converts smooth video output to clean pixel art (downscale → palette snap → outline → alpha → baseline). |
| **Sludge** | Raw video model output — correct motion but wrong art style (anti-aliased, gradients, wrong colors). |
| **Temporal Smoothing** | Locking barely-changing pixels to a consistent color across a frame sequence to eliminate jitter. |
| **Chroma Key** | Using a specific solid color (#00FF00 green) as the background, then removing it to create transparency. |
| **Palette LUT** | Lookup table of exact hex colors allowed for a character. The quantizer snaps every pixel to the nearest color in this table. |
| **Dual-Reference Prompting** | Attaching both a character reference (identity) and a pose reference (body position) to a generation prompt. Proven to produce the best results. |
| **Strategy Escalation** | When one generation strategy fails repeatedly, the pipeline automatically switches to a fallback (e.g., Hybrid → Image-Only). |
| **Manifest** | A YAML file that defines everything about a generation run — character, animation, frame count, strategy, quality thresholds. The pipeline's single source of truth. |
| **Atlas** | The final sprite sheet + JSON metadata file that Phaser loads. Produced by TexturePacker from approved frames. |

---

## Quick Reference Card

```
WHAT TO GENERATE PER FIGHTER:
  15 animations × 4-12 frames each = 96 total frames

PROMPT FORMULA:
  [Search Grounding (optional)] +
  [Pose Description for this specific frame] +
  [Character Palette Block] +
  [Base Style Anchor] +
  [Negative Prompt (if needed)]
  ATTACH: Anchor + Turnaround + Pose Reference

STRATEGY SELECTION:
  Walk cycles / complex motion → Hybrid
  Everything else → Image-Only

SUCCESS = frame passes all 10 per-frame checks + all 6 per-animation checks

START HERE:
  Phase 0 → Build quantizer → Test with synthetic data → Gate check
  Phase 1 → Test video models → Select winner
  Phase 2 → End-to-end Sean walk cycle
  Phase 3 → Scale to full roster
```
