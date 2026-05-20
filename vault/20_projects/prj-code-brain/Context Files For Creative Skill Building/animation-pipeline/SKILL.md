---
name: animation-pipeline
description: End-to-end 2D animation production pipeline with AI-assisted generation. Covers concept-to-final-render stages, ComfyUI integration for character/background generation, frame interpolation (RIFE/FILM), QA gates between pipeline stages, style profile enforcement, and asset organization. Use when asked about "animation pipeline", "production pipeline", "frame interpolation", "LoRA generation", "animation QA", "shot handoff", or "animation production".
---

# Animation Production Pipeline

## Purpose

Manage the full 2D animation production pipeline from concept through final render, with AI-assisted generation at every stage. This skill orchestrates pipeline stages, enforces quality gates between handoffs, integrates ComfyUI for asset generation, and handles frame interpolation for in-betweening. Built for someone working toward professional animation production.

## When to Use

- Setting up an animation project structure and pipeline
- Generating character/background art via ComfyUI with LoRA style refs
- Creating in-betweens with frame interpolation (RIFE/FILM)
- Running QA checks between pipeline stages
- Organizing animation assets (naming, versioning, directory structure)
- Planning shot breakdowns and timing

## Examples

**Example 1: New Animation Project Setup**
```
User: "Set up an animation pipeline for a 2-minute short"
Claude: [Uses animation-pipeline]
Creating project structure...

project_root/
├── meta/           # Shot manifests, x-sheets
├── audio/          # Dialogue tracks, phoneme maps
├── design/         # Model sheets, color palettes
├── storyboard/     # Boards, animatic exports
├── layout/         # BG lineart, camera field guides
├── assets/         # Character rigs, prop libraries
├── anim/           # Keys, breakdowns, in-betweens
├── comp/           # Compositing layers, render passes
└── output/         # Final renders

Estimated shots for 2 min @ 24fps: ~20-30 shots
Generating shot_manifest.json...
```

**Example 2: AI-Assisted Key Frame Generation**
```
User: "Generate key poses for the character walk cycle using ComfyUI"
Claude: [Uses animation-pipeline]
Queuing ComfyUI workflow with LoRA style reference...

curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": <walk_cycle_workflow.json>}'

Generating 4 key poses: Contact, Down, Passing, Up
Style LoRA: character_style_v2.safetensors (weight: 0.8)
Output: assets/characters/hero/walk_cycle/key_*.png

Running QA: palette check, silhouette clarity, volume consistency...
```

## Pipeline Stages

| # | Stage | Input | Output | QA Gate |
|:--|:------|:------|:-------|:--------|
| 1 | Script | Story concept | Formatted script | Visual density check |
| 2 | Design | Script | Model sheets, color palettes | Animatability/cost check |
| 3 | Storyboard | Script + designs | Boards, animatic | 180-degree rule, silhouette clarity |
| 4 | Audio | Script | Dialogue tracks, phoneme maps | Signal clarity, dead air check |
| 5 | Animatic | Boards + audio | Timed animatic | Pacing threshold (6 frames min, 10s max) |
| 6 | Timing/X-Sheet | Animatic | Exposure sheet, timing data | Sync offset (visual leads audio by 2 frames) |
| 7 | Layout | X-sheet + designs | BG lineart, camera field guides | Field guide validity, ground plane match |
| 8 | Animation | Layout + timing | Key frames, breakdowns | Twinning detector, hold duration |
| 9 | Cleanup | Rough animation | Clean lines | Volume conservation, line consistency |
| 10 | Ink & Paint | Clean lines | Colored frames | Palette lock, gap detection |
| 11 | Compositing | Colored layers + BG | Composited shots | Depth logic, lighting consistency |
| 12 | Final Render | Composited shots | Delivery files | Codec/bitrate spec, audio drift |

## Shot Packet Structure

Every shot uses this standardized directory and manifest:

```
SEQ01_SC03_SH01/
├── meta/
│   ├── shot_config.json    # Framerate, frame range, level stack, camera
│   └── x_sheet.json        # Exposure sheet data
├── audio/
│   ├── dialogue_master.wav
│   └── phoneme_map.json
├── layout/
│   ├── bg_lineart.png
│   └── camera_field_guide.json
├── assets/
│   ├── rig_manifest.json
│   └── model_sheets/
├── anim/
│   ├── keys/
│   ├── breakdowns/
│   └── inbetweens/
└── comp/
    ├── levels/             # L1_body, L2_mouth, BG
    └── render_pass/
```

### Shot Manifest (shot_config.json)

```json
{
  "shot_id": "SEQ01_SC03_SH01",
  "framerate_base": 24,
  "frame_range": [1, 72],
  "footage_length": "4ft 8fr",
  "level_stack": ["BG", "L1_Body", "L2_Mouth"],
  "camera_data": { "field_size": 12, "pan_velocity": 0.0 },
  "audio_sync_offset": -2,
  "style_profile": "limited_tv"
}
```

## QA Gates (Blocker vs Warning)

### Blockers (pipeline halts)

| Check | Stage | Condition |
|:------|:------|:----------|
| Framerate mismatch | Any | Shot framerate != project global |
| Missing audio | Layout → Anim | No dialogue_master.wav |
| Twinning detected | Blocking | Left limb rotation == Right limb rotation |
| Palette violation | Ink & Paint | Pixel RGB != Master Palette RGB |
| Render range mismatch | Comp | render_frame_count != x_sheet_exposure_count |

### Warnings (flagged for review, proceeds)

| Check | Stage | Condition |
|:------|:------|:----------|
| Floaty motion | Animation | Linear spacing detected (no ease in/out) |
| 80/20 rule violation | Animation (TV) | >20% pixel change in dialogue shot |
| Dead hold | Animation | Golden pose held < 6 frames |
| Dead air | Audio | Silence > 2 seconds without SFX |

## AI-Assisted Generation with ComfyUI

### Character Generation with LoRA

```bash
# Queue a character pose generation
curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d @workflow_character_pose.json

# Workflow targets:
# - class_type: "KSampler" → set seed, steps, cfg
# - class_type: "LoraLoader" → load style LoRA
# - class_type: "CLIPTextEncode" → inject prompt
```

### Style LoRA Workflow

1. **Train LoRA** on model sheets (10-20 reference images)
2. **Apply** at weight 0.7-0.85 for consistency without rigidity
3. **QA check** each generated frame against master palette
4. **Post-process** with pngquant for palette reduction if pixel art

### Background Generation

```bash
# Generate layout background
# Use ControlNet with lineart for precise composition
# Input: layout/bg_lineart.png (hand-drawn or rough)
# Output: layout/bg_colored.png (AI-colored, style-matched)
```

## Frame Interpolation (In-Betweening)

### RIFE (Real-Time Intermediate Flow Estimation)

```bash
# Generate in-betweens from key frames
python -m rife.inference_video \
  --img anim/keys/ \
  --exp 2 \
  --output anim/inbetweens/

# exp=1: 1 in-between (doubles frame count)
# exp=2: 3 in-betweens (quadruples frame count)
# exp=3: 7 in-betweens (8x frame count)
```

### FILM (Frame Interpolation for Large Motion)

```bash
# Better for large motion between keys
python -m film.interpolate \
  --input_frames anim/keys/ \
  --output_frames anim/inbetweens/ \
  --times_to_interpolate 2
```

### When to Use Which

| Tool | Best For | Limitation |
|:-----|:---------|:-----------|
| RIFE | Small-medium motion, real-time preview | Artifacts on large movements |
| FILM | Large motion, high quality | Slower processing |
| Manual | Complex acting, overlapping action | Time-intensive |

## Style Profiles

Define per-project to enforce consistency:

```json
{
  "profile_name": "limited_tv",
  "framerate": 24,
  "exposure": "twos_and_threes",
  "max_detail_lines": 80,
  "palette_colors": 32,
  "hold_minimum_frames": 6,
  "pixel_change_budget": 0.20,
  "lora_weight": 0.8,
  "lora_model": "style_v2.safetensors"
}
```

| Profile | Exposure | Detail Budget | Use Case |
|:--------|:---------|:-------------|:---------|
| feature_film | Ones | 200+ lines | High-budget, full animation |
| limited_tv | Twos/Threes | 80 lines | TV series, web series |
| limited_indie | Threes/Fours | 50 lines | Short films, festival entries |
| pixel_art | Ones (low res) | N/A | Game sprites, retro style |

## Asset Organization

### Naming Convention

`{SequenceID}_{SceneID}_{ShotID}_{Layer}_{FrameNumber}.{ext}`

Example: `SEQ02_SC05_SH01_L1Body_0024.png`

### Common Frame Rates

| Standard | FPS | Exposure | Frames/Foot |
|:---------|:----|:---------|:-----------|
| Film | 24 | Ones (24 drawings/sec) | 16 |
| TV (on twos) | 24 | Twos (12 drawings/sec) | 16 |
| Web/Indie | 24 | Threes (8 drawings/sec) | 16 |
| Game (pixel) | 12 | Ones (12 drawings/sec) | N/A |

## Success Criteria

- [ ] Project uses standardized shot packet structure
- [ ] QA gates run between every pipeline stage
- [ ] Blockers halt the pipeline; warnings flag for review
- [ ] Style profile enforced across all generated assets
- [ ] Frame interpolation produces clean in-betweens
- [ ] Asset naming follows convention consistently
- [ ] Shot manifests contain all required metadata fields

## Related Skills (Stage Cross-Reference)

Each pipeline stage maps to one or more specialized skills:

| Stage | Skill | What It Covers |
|:------|:------|:---------------|
| 1. Script | `script-writing` | Screenplay format, shot descriptions, dialogue |
| 2. Design | `pixel-art-retro-style`, `creative-director` | Style rules (pixel art) or creative direction (general) |
| 3-5. Storyboard → Animatic | `creative-director` | Visual planning, pacing critique, route selection |
| 6. Timing/X-Sheet | `2d-animation-principles` | Exposure timing, physics rules, spacing charts |
| 7. Layout | `adobe-illustrator-mcp`, `adobe-photoshop-mcp` | BG lineart (vector) or raster compositing |
| 8. Animation | `2d-animation-principles` | Easing, overlap, squash/stretch, timing |
| 9-10. Cleanup → Ink & Paint | `sprite-asset-pipeline` | Clean lines, palette enforcement, gap detection |
| 11. Compositing | `adobe-aftereffects-mcp`, `adobe-cross-app-workflows` | Layer compositing, effects, multi-app handoff |
| 12. Final Render | `video-animation-production`, `remotion-*` skills | FFmpeg rendering or Remotion programmatic video |
| AI Generation | `ai-creative-tools`, `comfyui-workflows` | ComfyUI workflows, LoRA training, HF models |
| Project Planning | `creative-director` | Interview, route selection, critique rubrics |

## Copy/Paste Ready

```
"Set up an animation pipeline for my short film"
"Generate character key frames with ComfyUI"
"Run QA checks on this shot"
"Create in-betweens from my key frames"
"Set up the style profile for this project"
"Organize my animation assets"
"Break down this scene into shots"
```