# Phase 5B Validation Results

**Date:** 2026-04-09
**Character tested:** Sean (Champion, 128x128)
**Model:** gemini-3.1-flash-image-preview (NB2)

---

## Summary

Phase 5B validated the per-frame generation pipeline and identified a critical consistency fix. The Pixel Quantizer pipeline is fully functional. HYBRID interpolation via RIFE is blocked on Alienware access.

---

## Task 1: Per-Frame Consistency

### Problem
Individual API calls to Gemini produce **completely different characters** each frame. Despite sending 3 anchor reference images per request, each independent call "interprets" the anchors differently:
- Frame 0: Blue gi, yellow belt, short dreads
- Frame 1: Orange gi, black belt, medium dreads
- Frame 2: Blue gi, white belt, long dreads
- Frame 3: Blue gi, green belt, short curly hair
- **None matched the anchor** (blonde hair, white tank top, blue pants)

### Fix: Sprite Sheet → Split
Generate all frames as a **single sprite sheet** in one Gemini call, then programmatically split into individual frames. This leverages within-image consistency (proven 12/12 in Phase 5A).

### Result: **PASS**
All 4 idle frames from the sheet approach show identical character: blonde hair, white tank top, blue pants, muscular build. Matches anchor reference.

**Implementation:** `batch/generate_sheet_split.py` — supports `--approach sheet|sequential|reinforced`.

---

## Task 2: HYBRID Pipeline (Keyframes + RIFE)

### Keyframe Generation: PASS
8 walk_forward keyframes generated successfully via sprite sheet approach. Character consistency is strong across all frames with good walk cycle pose progression.

### RIFE Interpolation: PASS
- Alienware online, ComfyUI v0.3.52, PyTorch 2.11.0+cu128, RTX 5080
- 3 keyframes (frames 0, 3, 7) → 9 interpolated frames via RIFE VFI (4x multiplier)
- Processing time: <1s on RTX 5080 (near-instant)
- Output: 61KB h264-mp4 at 12fps
- Character identity: preserved throughout interpolation
- Green screen: maintained

### Bugs Fixed
The RIFEAdapter's dynamic workflow builder was missing required fields:
1. **RIFE VFI node**: Added `scale_factor` (1.0), `dtype` ("float16"), `torch_compile` (false), `batch_size` (1)
2. **VHS_VideoCombine node**: Added `loop_count` (0), `pingpong` (false), `save_output` (true); removed invalid `quality` field
3. **Output download**: VHS_VideoCombine stores output under `gifs` key, not `videos` — fixed to check both

Note: The static workflow JSON (`workflows/rife_interpolation.json`) was already correct (updated Phase 5A). The bug was only in the adapter's dynamically-built workflow (`adapters.py` lines 1128-1157).

---

## Task 3: Pixel Quantizer Pipeline

### Results

| Animation | Frames | Passed | Off-palette | Outline Coverage | BG Clean | Time |
|-----------|--------|--------|-------------|-----------------|----------|------|
| idle | 5 (4 + sheet) | 5/5 | 0 | 0.776-0.822 | All clean | 77ms |
| walk_forward | 9 (8 + sheet) | 9/9 | 0 | 0.834-0.858 | All clean | 120ms |

### Gate: **PASS**
- 100% pass rate
- 0 off-palette pixels
- Clean backgrounds
- Temporal jitter: 0

### Observation: Dark Quantized Output
The quantized sprites appear very dark — the outline color (#272929) dominates due to aggressive palette snapping. The 16-color Sean palette may need:
- More mid-tone skin colors (between skin and skin_shadow)
- More clothing mid-tones (between tank_top and tank_top_shadow)
- A lighter outline option for internal details vs. silhouette edges

This is a palette refinement issue, not a pipeline failure. The 7-step pipeline (downscale → alpha → palette → temporal → outline → grid → validate) is working correctly.

---

## Task 4: Consistency Approach Comparison

Tested on `light_punch` (6 frames) for Sean:

| Criteria | Sheet → Split (A) | Sequential Conditioning (B) |
|----------|-------------------|---------------------------|
| Character consistency | Excellent | Excellent |
| Hair/outfit match | Blonde, white tank, blue pants | Blonde, white tank, blue pants |
| Pose quality | Good — subtle variation | Excellent — dynamic, impact VFX |
| Animation readability | Moderate | Strong (clear wind-up → extend → retract) |
| Generation time | 22.9s (1 call) | 123.0s (6 calls) |
| Cost multiplier | 1x | ~6x (growing context per frame) |
| Output resolution | ~344x384 per cell | ~768x768 per frame |

### Winner: Sheet → Split (Default)
5x faster, 6x cheaper, and character consistency is equivalent. The lower per-cell resolution is acceptable because the Pixel Quantizer downscales to 128x128 anyway.

### Runner-up: Sequential Conditioning (Fallback)
Superior pose quality and resolution. Use for:
- Animations needing maximum pose expressiveness (special_move, heavy attacks)
- Debugging sheet splitting issues
- When sheet approach produces too-similar poses

### Not Tested: Reinforced Prompts (Approach C)
Individual per-frame calls with enhanced prompts. Given that the original per-frame approach (with standard prompts + anchors) produced completely inconsistent characters, prompt reinforcement alone is unlikely to solve the fundamental issue. The anchors are necessary but not sufficient for cross-call consistency.

---

## Recommended Approach for Full Roster

### Default Pipeline (IMAGE_ONLY animations)
1. Generate all frames as sprite sheet (1 Gemini API call per animation)
2. Auto-detect grid layout (Gemini sometimes produces more cells than requested)
3. Split into individual frames
4. Run Pixel Quantizer (128x128 for champions, 256x256 for bosses)

### HYBRID Pipeline (when Alienware is online)
1. Generate keyframes via sprite sheet approach
2. Upload to Alienware ComfyUI for RIFE interpolation
3. Download interpolated frames
4. Run Pixel Quantizer on interpolated frames

### Estimated Cost for Full Roster
- 12 characters × 15 animations = 180 animations
- Sheet approach: 180 API calls (1 per animation)
- At ~$0.07 per NB2 call with 3 anchor images: ~$12.60 total
- Time: ~20s per animation → ~1 hour total (with rate limiting delays)

---

## Issues to Fix Before Autoresearch Run

1. ~~**RIFE workflow validation**~~ — DONE. Fixed 3 bugs in RIFEAdapter dynamic workflow builder. RIFE confirmed working.
2. **Grid detection** — `generate_sheet_split.py` now includes auto-detection for Gemini's variable grid output
3. **Palette refinement** — Sean's 16-color palette produces dark quantized output; needs mid-tone expansion
4. **Batch orchestrator update** — Integrate sheet → split approach as the default for IMAGE_ONLY strategy (currently uses per-frame calls that produce inconsistent characters)
5. **RIFEAdapter integration** — Wire the fixed adapter into the batch orchestrator's HYBRID path so `--resume` re-runs failed HYBRID animations

---

## Files Created/Modified

| File | Action | Purpose |
|------|--------|---------|
| `batch/generate_sheet_split.py` | Created | Sheet → split + sequential + reinforced approaches |
| `output/sean/idle/` | Regenerated | 4 consistent frames via sheet approach |
| `output/sean/idle_quantized/` | Created | Pixel Quantizer output (128x128, on-palette) |
| `output/sean/walk_forward/` | Generated | 8 walk cycle frames via sheet approach |
| `output/sean/walk_forward_quantized/` | Created | Pixel Quantizer output |
| `output/sean/light_punch/` | Generated | 6 frames via sheet approach (Task 4 comparison) |
| `output/sean/light_punch_sequential/` | Generated | 6 frames via sequential conditioning (Task 4 comparison) |
