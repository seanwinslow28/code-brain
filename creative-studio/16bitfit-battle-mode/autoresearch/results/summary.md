# Autoresearch Run Summary

**Date:** 2026-04-12 17:11
**Total experiments:** 100
**Total cost:** $7.00

## Scores
- **Best:** 0.8448 (experiment 75)
- **Worst:** 0.5937 (experiment 78)
- **Mean:** 0.7425
- **Median:** 0.7370

## Best Configuration
```json
{
  "version": 4,
  "character": "sean",
  "animation_type": "walk_forward",
  "generation": {
    "model": "gemini-3.1-flash-image-preview",
    "prompt_template": "Generate a pixel art sprite sheet of THIS EXACT CHARACTER from the reference images. The sprite sheet must show {frame_count} frames of the 'walk_forward' animation, arranged in a {cols}x{rows} grid. Each cell is {tile_size}x{tile_size} pixels.",
    "negative_prompt": "blurry, anti-aliased, gradient, smooth shading, 3D render, realistic, photographic, watermark, text, HUD, UI elements, anime proportions, chibi, background scenery, multiple characters",
    "reference_strategy": "3_anchors",
    "sheet_layout": "full_sheet",
    "frame_count": 4,
    "include_pose_names": true,
    "include_animation_principles": true,
    "include_walk_cycle_reference": false,
    "additional_constraints": [
      "4 distinct walk cycle phases: heel strike, weight drop, leg pass, push up"
    ]
  },
  "scoring": {
    "skip_dino": false,
    "skip_vlm": false,
    "alienware_host": "192.168.68.201",
    "vlm_timeout_s": 30
  }
}
```

## Top Findings
1. Experiment 75 — score 0.8448 (changed: additional_constraints, include_animation_principles)
2. Experiment 2 — score 0.8446 (changed: additional_constraints)
3. Experiment 47 — score 0.8429 (changed: sheet_layout)
4. Experiment 20 — score 0.8428 (changed: reference_strategy)
5. Experiment 45 — score 0.8423 (changed: sheet_layout)
