---
name: 2d-animation-principles
description: 2D animation physics, timing, and production rules for coding agents. Covers gravity spacing (Odd Rule), arcs, smear synthesis, style mode switching (Rubber Hose through Spider-Verse), acting engine (twinning detection, eye lead, blink asymmetry), TV/limited optimization (80/20 rule, cel stacking), and QA gates. Use when animating characters, creating walk cycles, planning sprite animations, evaluating animation quality, implementing any 2D motion system, or reviewing animation timing and spacing.
---

# 2D Animation Principles

## Purpose

Apply deterministic, physics-based animation rules when generating or evaluating 2D animation. Replace vague artistic direction with testable constraints derived from the physics of motion and production pipeline requirements. Operate in two modes: Pose-to-Pose (structured keyframe planning for acting and mechanics) and Straight-Ahead (sequential frame generation for fluid dynamics like fire, water, hair).

## When to Use

- Animating characters in Phaser, Remotion, or any 2D framework
- Planning walk cycles, run cycles, or any looping animation
- Generating sprite sheet timing and frame counts
- Evaluating whether animation feels "floaty", "robotic", or "snappy"
- Choosing smear types for fast motion
- Adapting animation style to a specific era (Rubber Hose, Golden Age, Spider-Verse)
- Optimizing animation for TV/limited budgets (reducing drawing count)
- Reviewing animation for twinning, dead holds, or physics violations

## Examples

**Example 1: Planning a character jump**
```
User: "Animate a character jumping across a gap in my Phaser game"
Claude: [Uses 2d-animation-principles] Plans using Pose-to-Pose mode:
- 3 Key Poses: Anticipation (crouch), Apex (peak height), Landing (impact squash)
- Arc: Fourth Down Rule — breakdown at 50% time is 25% below apex
- Gravity spacing: Odd Rule (1:3:5:7) on descent
- Squash on landing: 1 frame, volume-locked (Scale_X * Scale_Y ~ 1.0)
- Total: ~18 frames on Twos (12fps effective)
```

**Example 2: Evaluating animation quality**
```
User: "This walk cycle feels off — what's wrong?"
Claude: [Uses 2d-animation-principles] Runs QA gates:
- Physics Gate: Spacing is linear for 8 frames — FAIL (apply ease-in/out)
- Acting Gate: Left and right arms swing identically — FAIL (twinning, offset by 2 frames)
- Production Gate: Character static for 36 frames between steps — FAIL (add moving hold with 1-2% drift)
```

**Example 3: Choosing a smear type**
```
User: "My character's punch looks choppy — there's a gap between the wind-up and impact"
Claude: [Uses 2d-animation-principles] Diagnoses strobing:
- Displacement > object width = smear needed
- Action is ballistic (linear punch) = use Elongated Inbetween
- Duration: strictly 1 frame
- Stretch mesh along motion vector, compress perpendicular axis
For the complete smear taxonomy (30 types), see references/smear-taxonomy.md.
```

## The Operating Loop

Every animation task follows Plan, Implement, Verify.

### Phase 1: PLAN (Configuration)

1. **Parse constraints**: Detect budget mode (TV vs Feature) and style profile (Rubber Hose, Golden Age, Spider-Verse, etc.)
2. **Asset strategy**: If budget mode is LIMITED_TV, check for existing cycles before generating new frames
3. **Audio sync**: If audio exists, extract phonemes and map to viseme library (7-9 mouth shapes). Visual accents lead audio hits by 2 frames
4. **Output**: An AnimationClipSpec defining FPS, exposure rate, style profile, and action beats

### Phase 2: IMPLEMENT (Synthesis)

1. **Blocking**: Generate Key Poses ensuring readable silhouettes (limbs occlude less than 30% of torso)
2. **Splining**: Interpolate between keys using physics rules (see Physics Engine below)
3. **Smear synthesis**: If displacement > object width, generate a smear frame (see `references/smear-taxonomy.md`)
4. **Layer optimization** (TV mode only): Separate static body from active mouth/eyes (cel stacking)

### Phase 3: VERIFY (QA Gates)

Run all three gates before finalizing. Any failure blocks output.

| Gate | Check | Fail Condition | Fix |
|------|-------|---------------|-----|
| Physics | Spacing linearity | Linear spacing for >6 frames | Apply ease-in/out |
| Physics | Volume conservation | Scale_X * Scale_Y != ~1.0 during squash | Scale_perp = 1/sqrt(Scale_parallel) |
| Physics | Arc compliance | End effector follows linear path | Add arc breakdown |
| Acting | Twinning (pose) | L_Rot == R_Rot (tolerance <5%) | Offset one side by 2-4 frames |
| Acting | Twinning (timing) | Start_Frame_L == Start_Frame_R | Offset one limb start by 2 frames |
| Acting | Dead hold | Pixel variance == 0 for >12 frames | Add moving hold (1-2% drift) |
| Acting | Eye lead | Head turns before or with eyes | Eyes move 2-3 frames before head |
| Acting | Blink asymmetry | Close duration == Open duration | Close: 3fr, Hold: 1fr, Open: 4+fr |
| Production | Strobing | Displacement > width without smear | Add appropriate smear type |
| Production | Readability | Key pose held <3 frames | Extend to minimum 6 frames |

## Physics Engine

### Gravity (The Odd Rule)

Gravity is acceleration, not speed. Displacement from a stop increases in odd number ratios: 1, 3, 5, 7.

```
Y_Pos[t] = Y_Pos[t-1] - (Unit_Dist * (2t - 1))
```

If spacing between frames is constant (linear), the motion looks "floaty". This is the most common physics failure.

### Arcs (Fourth Down Rule)

For organic motion, the breakdown pose at 50% time must be at 25% of the vertical distance from the apex. This creates the slow-out feel at the top of a jump or throw.

### Timing vs Spacing

- **Timing** = duration (frame count). "How long does the action take?"
- **Spacing** = rhythm (displacement per frame). "How does the speed change within that duration?"
- Never use linear spacing for organic characters. Always ease in and out.

### Follow-Through and Overlap

Child joints lag behind parent joints. Offset hierarchy:

```
Shoulder (t) -> Elbow (t+2) -> Wrist (t+4) -> Fingers (t+6)
```

For complete timing defaults, JSON schemas, and pseudocode patterns, see `references/timing-spacing.md`.

## Style Mode Switcher

Switch physics parameters based on the target style. Each style overrides interpolation, smear type, and framerate.

| Style | FPS | Interpolation | Smear Type | Squash/Stretch |
|-------|-----|---------------|------------|----------------|
| Rubber Hose (1920s) | Sync to BPM | Linear (constant) | Speed lines | High (rubber) |
| Golden Age (1930s) | 24 (Ones) or 12 (Twos) | Cubic bezier | Drybrush texture | Moderate (volume locked) |
| Screwball (1940s) | 24 (Ones) for zips | Zip (1-frame transit) | Elongated mesh | Extreme (volume broken) |
| Limited TV (1960s) | 12 (Twos) or 8 (Threes) | Step (hold-to-pop) | Abstract blur | Low (muzzle only) |
| Spider-Verse | 12 (Twos) forced | Stepped (no splines) | CMYK offset | Low (rigid) |
| Genndy 3D | 24 (Ones) | Snappy (sharp curves) | Geo blend (sub-frame) | Extreme (cartoony) |

For the full parameter override matrix and per-style verification tests, see `references/style-profiles.md`.

## Acting Engine

### Twinning Detection

If left and right limbs have identical rotation or timing, the character looks robotic. Always offset one side.

- **Pose twinning**: L_Limb_Rot == R_Limb_Rot at same frame. Fix: offset angle.
- **Timing twinning**: Both limbs start moving on same frame. Fix: offset start by 2 frames.

### The Acting Beat Pattern

Every significant action follows: Thought, Anticipation, Action, Overshoot, Settle.

1. **Thought**: Eyes move to target 2-3 frames before head turns. Processing pause: 6-12 frames.
2. **Anticipation**: Move opposite to intended direction. Duration: 4-8 frames (standard), 1-2 frames (shock).
3. **Action**: The main movement. Use Ones for fast, Twos for normal.
4. **Overshoot**: Extremities pass the target. Return: 3-5 frames (rigid), 6+ frames (soft).
5. **Settle**: Decelerate into final pose with dampened oscillation or ease-out.

### Duration Defaults (at 24fps)

| Action Type | Frame Range | Example |
|-------------|-------------|---------|
| Fast reaction | 2-4 frames | Surprise, impact, shock |
| Normal gesture | 8-12 frames | Conversation, pointing |
| Heavy effort | 16-24 frames | Lifting, pushing |
| Golden key hold | 6-12 frames | Readable attitude pose |
| Readability floor | 3 frames minimum | Anything less is invisible |

## TV/Limited Optimization

When budget mode is LIMITED_TV:

- **80/20 Rule**: 80% of screen pixels must be static. Only 20% (mouths, eyes, arms) update per frame.
- **Cel Stacking**: Separate character into Level_1_Body (static) and Level_2_Mouth (active). Mask seam with collar/necktie.
- **Exposure**: Default to Twos (12fps). Switch to Ones only if camera pans (prevents background strobing).
- **Bank First**: Query asset library for existing cycles before generating new frames.
- **Moving Holds**: If pose holds >24 frames, add 1-2% drift to prevent "dead" look.
- **Background Syncopation**: Use A-B-A-C patterns, not A-A-A repetition (prevents "Flintstones Effect").

## Walk Cycle Reference

Standard bipedal walk cycle on Twos (12fps):

| Frame | Pose | Notes |
|-------|------|-------|
| 1 | Contact | Heel strike, arms at extremes |
| 4 | Down | Lowest point, weight absorb |
| 7 | Passing | Vertical leg, arms cross center |
| 10 | Up | Highest point, push-off |
| 13 | Contact (mirror) | Opposite leg, loop start |

For curated instruction-output examples across all 6 modules, see `references/training-examples.md`.

## Success Criteria

- [ ] Gravity uses Odd Rule spacing (1:3:5:7), not linear
- [ ] Volume is conserved during squash/stretch (Scale_X * Scale_Y ~ 1.0)
- [ ] No twinning: left/right limbs offset in pose and timing
- [ ] Smears last exactly 1 frame (never held longer)
- [ ] Key poses held minimum 3 frames (6+ for narrative beats)
- [ ] Style profile parameters match the target era
- [ ] TV mode: active pixels under 20% of screen area
- [ ] Eyes lead head turns by 2-3 frames
- [ ] Arcs follow Fourth Down Rule (breakdown at 25% from apex at 50% time)

## Copy/Paste Ready

```
"Animate this character walking"
"Plan a jump animation for my Phaser sprite"
"What smear type should I use for a fast punch?"
"Review this animation — why does it feel floaty?"
"Set up timing for a surprise reaction"
"How many frames for a walk cycle on Twos?"
"Adapt this animation to Spider-Verse style"
"Optimize this animation for TV budget"
```
