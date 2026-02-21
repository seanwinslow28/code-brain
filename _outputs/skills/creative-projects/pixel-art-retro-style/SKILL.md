---
name: pixel-art-retro-style
description: Enforce strict Game Boy retro aesthetic rules. Covers 4-color palette constraints, 8x8 grid alignment, dithering, and character design. Triggers on "Game Boy style", "retro aesthetic", "pixel art rules", "dithering pattern", or "palette constraints".
---

# Pixel Art & Retro Style

## Purpose

Maintain visual consistency for a Game Boy-inspired RPG. Enforce strict limitations on color, resolution, and movement to achieve an authentic retro feel rather than a generic "pixelated" look.

## When to Use

- Choosing colors for new assets (Ui, sprites, tiles)
- Designing tile maps (8x8 grid)
- Creating dithering patterns for backgrounds
- Configuring game resolution scaling
- Checking character sprite readability

## Examples

**Example 1: Palette Check**
```
User: "Suggest colors for a forest dungeon background."
Claude: [Uses pixel-art-retro-style]
Using strict Game Boy palette (Classic Green):
- Darkest (#0f380f): Trees, deep shadows, outlines
- Dark (#306230): Ground texture, bark shading
- Light (#8bac0f): Leaves, highlights on grass
- Lightest (#9bbc0f): Sky, sunbeams (sparingly)

*Note: Use dithering (checkerboard) to blend Dark and Light for the mid-tone fog effect.*
```

**Example 2: Character Design**
```
User: "How should I design the main hero sprite?"
Claude: [Uses pixel-art-retro-style]
Constraints: 16x16 pixels (4 hue tiles).
- Head: 6-8px height (exaggerated for readability)
- Body: 4-6px boxy form
- Legs: 2-4px stick or block style
- Animation: 2-frame idle, 4-frame walk
- View: Top-down or slight 3/4 angle
```

## Core Principles

### 1. The 4-Color Palette
Strictly limit all assets to these hexadecimal values. Do not use gradients or opacity.

| Role | Classic Green | Grayscale (Pocket) | Usage |
|------|---------------|--------------------|-------|
| Darkest | `#0f380f` | `#000000` | Outlines, Deep Shadows, Text |
| Dark | `#306230` | `#555555` | Primary Foreground, Shading |
| Light | `#8bac0f` | `#aaaaaa` | Background Details, Highlights |
| Lightest | `#9bbc0f` | `#ffffff` | Background "Air", UI Text |

### 2. Grid Constraints (8x8)
The world is built from 8x8 pixel tiles.
- **Backgrounds:** Must align to the 8x8 grid.
- **Metatiles:** Combine four 8x8 tiles to make a 16x16 logical block (e.g., a full bush or crate).
- **Reuse:** A single "brick" tile should be repeated; do not draw large unique backgrounds.

### 3. Dithering Techniques
Since you only have 4 colors, use dithering to create the illusion of more shades.

- **Checkerboard (50%):** Alternating pixels of Color A and B.
- **Sparse (25%):** One pixel of Color B every 4 pixels of Color A.
- **Bayer Pattern:** Use standard Bayer matrix for ordered dithering.

### 4. Visual Consistency Rules

1.  **Pixel-Perfect Movement:** Characters must snap to integer grid coordinates (E.g., `x: 10`, not `x: 10.5`). Sub-pixel movement causes "shimmering".
2.  **Uniform Pixel Density:** Never mix resolutions. A 32x32 boss sprite must use the same "pixel size" as the 8x8 grass tile.
3.  **No Rotation:** Do not rotate sprites freely. Rotate in 90-degree increments or redraw the sprite for the new angle.

### 5. Common Mistakes to Avoid

1.  **Mixels (Mixed Pixels):** Using assets with different resolutions (e.g., a high-res UI over a low-res game). Everything must share the same "pixel grid".
2.  **Sub-Pixel Movement:** Allowing sprites to float between pixels (e.g. x=10.5). This causes shimmering. Always `Math.floor()` coordinates for rendering.
3.  **Bilinear Filtering:** Failing to set `pixelArt: true` (Phaser) or `nearest` neighbor scaling. This creates blurry "smudged" art.
4.  **Color Bleeding:** Using colors outside the 4-tone palette (often happens when resizing images in standard editors that add anti-aliasing edges).


## Success Criteria

- [ ] Project uses exactly 4 colors (plus transparent)
- [ ] All tiles align to 8x8 grid boundaries
- [ ] No sub-pixel movement or rotation
- [ ] Sprites use integer scaling (2x, 3x, 4x) only
- [ ] Shadows are solid pixels or dithered, not alpha-blended

## Copy/Paste Ready

```
"Check if this sprite follows the 4-color Game Boy palette"
"Explain the 8x8 grid constraints for this tile map"
"Generate a checkerboard dithering pattern for the sky"
"Ensure character movement snaps to the pixel grid"
```
