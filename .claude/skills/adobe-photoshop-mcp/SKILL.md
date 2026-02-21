---
name: adobe-photoshop-mcp
description: Adobe Photoshop automation and image editing via adb-mcp. Use when editing images in Photoshop, creating PSDs, working with layers and masks, assembling sprite sheets, using generative fill, batch processing photos, compositing, removing backgrounds, or manipulating images via the PS MCP server.
---

# Adobe Photoshop MCP

## Purpose

Execute Photoshop operations through the adb-mcp server's UXP plugin. Translate creative plans into small-batch MCP tool calls, verify results visually via `get_document_image`, and maintain non-destructive editing patterns throughout.

## When to Use

- Editing images or compositing in Photoshop via MCP
- Assembling sprite sheets from individual frames
- Using generative fill or AI-powered selection
- Batch processing multiple images
- Creating or modifying PSD layer structures
- Applying adjustment layers, effects, or masks
- Preparing assets for After Effects or game engines

## Examples

**Example 1: Sprite sheet assembly**
```
User: "Assemble these 12 character sprites into a 4x3 sprite sheet"
Claude: [Uses adobe-photoshop-mcp]
  1. Calculates grid: 4 columns x 3 rows at 64x64px each = 256x192 document
  2. create_document(256, 192, 72, "transparent")
  3. Loop: place_image + translate_layer for each sprite to grid position
  4. rename_layers to "Sprite_01" through "Sprite_12"
  5. group_layers into "Sheet_Root"
  6. get_document_image to verify alignment
  "Sprite sheet assembled. All 12 frames aligned to grid. Ready to export?"
```

**Example 2: Non-destructive background replacement**
```
User: "Replace the background of this product photo"
Claude: [Uses adobe-photoshop-mcp]
  1. get_document_info — confirms resolution and color mode
  2. select_subject — AI-powered subject isolation
  3. add_layer_mask_from_selection — mask instead of delete
  4. place_image (new background) → move_layer to BOTTOM
  5. get_document_image to verify composite
  "Background replaced non-destructively. Original pixels preserved under mask."
```

**Example 3: Batch adjustment with creative direction**
```
User: "The Creative Director plan says to add warm color grading to all hero images"
Claude: [Uses adobe-photoshop-mcp]
  1. get_layers — maps current layer structure
  2. add_color_balance_adjustment_layer — warm highlights (+15 red, +5 yellow)
  3. add_vibrance_adjustment_layer — boost saturation subtly (+20)
  4. get_document_image to verify against the creative brief
  "Warm grade applied as adjustment layers. Non-destructive — toggle visibility to compare."
```

## Photoshop Fundamentals

### Document Object Model

- **Hierarchy**: Application → Document → Layers/Groups → Properties (Opacity, Blend Mode, Styles)
- **Coordinate System**: 2D Cartesian. `(0,0)` is top-left. Y increases downward. All coordinates must be **integers**.
- **Layer Stack**: Z-index logic. `index: 0` is the bottom-most layer (Background). Use `move_layer` with relative positioning (UP, DOWN, TOP, BOTTOM).
- **State**: Photoshop is stateful. Selection states, active layer, and clipboard persist until explicitly changed. Clear selections after masking operations to avoid state leaking.

### Core Concepts

- **Non-Destructive Editing**: The Golden Rule. Never delete pixels — use masks. Never apply destructive adjustments — use Adjustment Layers. Never flatten unless the user explicitly says "export", "final", or "flatten".
- **Smart Objects**: Containers preserving original data. Essential for resizing without quality loss.
- **Active Selection**: Many tools (`generative_fill`, `crop`, `add_layer_mask`) require an active "marching ants" selection to function.

### Plugin Architecture

Photoshop uses a **UXP plugin** via adb-mcp with dedicated, named tool calls (not arbitrary scripting like AE/AI).

```
Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ UXP Plugin ↔ Photoshop
```

Load app-specific guidance at session start with `config://get_instructions`.

### MCP Capabilities Overview

For the complete command reference with parameters, see `references/ps-mcp-commands.md`.

**Inspection & Vision** — `get_document_info`, `get_layers`, `get_document_image` (canvas screenshot), `get_layer_image`, `get_layer_bounds`

**Creation & Composition** — `create_document`, `place_image`, `create_pixel_layer`, `create_text_layer`, `generative_fill`, `generate_image`

**Manipulation & Transformation** — `scale_layer`, `rotate_layer`, `translate_layer`, `flip_layer`, `align_content`, `group_layers`, `move_layer`, `duplicate_layer`, `delete_layer`, `rename_layers`, `set_layer_visibility`, `set_layer_opacity`, `set_layer_properties`

**Selection & Masking** — `select_subject`, `select_sky`, `select_rectangle`, `select_ellipse`, `select_polygon`, `add_layer_mask_from_selection`, `remove_layer_mask`, `remove_background`

**Styles & Adjustments** — Adjustment layers (brightness/contrast, color balance, black/white, vibrance), effects (stroke, gradient, gaussian blur, motion blur), `harmonize_layer`

## Workflow Patterns

### Pattern A: Sprite Sheet Assembly
1. Calculate grid from sprite count and dimensions
2. `create_document` with calculated size + transparent background
3. Loop: `place_image` → `translate_layer` to grid position `(col * width, row * height)`
4. `rename_layers` to sequential names
5. `group_layers` into container
6. Verify with `get_document_image`

### Pattern B: Non-Destructive Retouch
1. `get_layers` to find source image layer
2. `create_pixel_layer` named "Retouch" or "Cleanup"
3. `set_layer_properties` to set blend mode (e.g., OVERLAY for lighting)
4. Edit on the new layer — source remains untouched

### Pattern C: Smart Mockup / Background Replacement
1. `select_subject` on product/character layer
2. `add_layer_mask_from_selection` (or `invert_selection` first if isolating background)
3. `place_image` (new background) → `move_layer` to BOTTOM
4. `harmonize_layer` to match foreground lighting to new background

## Execution Protocol

### Small-Batch Pattern
1. Execute **2-3 operations**
2. **Pause** — call `get_document_image` to verify visual result
3. **Continue** only after verification passes
4. For complex tasks, save checkpoints with `save_document`

### Guardrails

| Rule | Action |
|------|--------|
| No flattening | Never `flatten_all_layers` unless user says "export", "final", or "flatten" |
| Save before risk | `save_document` before generative fill, rasterize, or batch operations |
| Name everything | Every `create_*` followed by `rename_layers` |
| Verify visually | `get_document_image` after generative or composite operations |
| Refresh after structural changes | `get_layers` after flatten, group, merge, or delete |

### Error Handling

- **Timeout on large operations**: Break generative fill or blur on 4K images into smaller regions
- **Layer ID volatility**: IDs change after flatten/group/merge. Always refresh via `get_layers` after structural changes.
- **"No subject detected"**: Fallback to `select_rectangle` with user-provided bounding box
- **Smart Object limitation**: Cannot edit Smart Object contents directly. Place content above and group, or rasterize with user approval.

For shared guardrails (naming conventions, destructive action safeguards, checkpoint behavior), see `adobe-cross-app-workflows`. For planning and critique before execution, see `creative-director`.

## Success Criteria

- [ ] Loaded Photoshop MCP guidance via `config://get_instructions` at session start
- [ ] Executed in small batches (2-3 ops → get_document_image → continue)
- [ ] Maintained non-destructive patterns (masks over erasers, adjustment layers over direct adjustments)
- [ ] All created layers named descriptively (no "Layer 1" or "copy")
- [ ] Saved document before any high-risk operation
- [ ] Refreshed layer map after structural changes
- [ ] Verified final result visually with get_document_image

## Copy/Paste Ready

```
"Edit this image in Photoshop"
"Assemble a sprite sheet from these frames"
"Use generative fill to extend this background"
"Replace the background and composite a new scene"
"Batch process these photos with consistent color grading"
```
