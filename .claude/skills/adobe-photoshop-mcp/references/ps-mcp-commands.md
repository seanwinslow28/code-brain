# Photoshop MCP Command Reference

Read this when you need exact parameter details for a specific Photoshop MCP tool call. The main SKILL.md provides the overview; this file has the complete command list.

## Inspection & Vision

### get_document_info
Returns metadata: resolution, color mode (RGB/CMYK), bit depth, saved state, dimensions.
Use as pre-flight check before editing.

### get_layers
Returns full JSON tree of the layer stack: IDs, names, types, nesting, visibility, opacity, blend modes.
**Always call after structural changes** (flatten, group, merge, delete) — layer IDs change.

### get_document_image
Returns a JPEG of the current canvas state. This is how Claude "sees" the work.
Use after every 2-3 operations for visual verification.

### get_layer_image
Returns a JPEG of a specific layer in isolation (by layer ID).
Use to inspect individual elements without other layers visible.

### get_layer_bounds
Returns pixel coordinates `(left, top, right, bottom)` of a layer's content bounds.
Use for calculating positions in sprite sheet assembly or alignment tasks.

## Creation & Composition

### create_document
- `width` (int): Width in pixels
- `height` (int): Height in pixels
- `resolution` (int): PPI (72 for web, 300 for print)
- `fill` (string): "white", "black", or "transparent"
- `name` (string): Document name

### place_image
- `file_path` (string): Path to PNG/JPG file
- `layer_id` (int, optional): Target layer to place above
Imports external file as a new layer. Follow with `translate_layer` for positioning.

### create_pixel_layer
Creates an empty raster layer. Use for non-destructive retouching workflows.
Follow immediately with `rename_layers`.

### create_text_layer
- `text` (string): Text content
- `font_size` (int): Size in points
- `color` (object): RGB color values
Creates a new text layer. Follow with `translate_layer` for positioning.

### generative_fill
- `prompt` (string): Text description of desired content
Requires an **active selection** (marching ants). Uses Adobe Firefly to generate content within the selected area.
**Save document before calling.** May timeout on large selections.

### generate_image
- `prompt` (string): Text description
Generates a new image using Adobe Firefly AI.

## Manipulation & Transformation

### scale_layer
- `layer_id` (int): Target layer
- `width` (float): Scale percentage for width
- `height` (float): Scale percentage for height

### rotate_layer
- `layer_id` (int): Target layer
- `angle` (float): Rotation in degrees

### translate_layer
- `layer_id` (int): Target layer
- `x` (int): Horizontal offset in pixels
- `y` (int): Vertical offset in pixels
**Coordinates must be integers.**

### flip_layer
- `layer_id` (int): Target layer
- `direction` (string): "horizontal" or "vertical"

### align_content
- `layer_ids` (array): Layers to align
- `alignment` (string): Alignment type (left, center, right, top, middle, bottom)

### group_layers
- `layer_ids` (array): Layers to group
- `name` (string): Group name

### move_layer
- `layer_id` (int): Target layer
- `position` (string): "UP", "DOWN", "TOP", "BOTTOM"
Relative positioning within the layer stack.

### duplicate_layer
- `layer_id` (int): Layer to duplicate

### delete_layer
- `layer_id` (int): Layer to remove
**Destructive operation.** Consider hiding (`set_layer_visibility`) instead.

### rename_layers
- `layer_ids` (array): Layers to rename
- `names` (array): New names (same length as layer_ids)
**Call after every create operation.** No "Layer 1" or "copy" names in production files.

### set_layer_visibility
- `layer_id` (int): Target layer
- `visible` (bool): Show or hide

### set_layer_opacity
- `layer_id` (int): Target layer
- `opacity` (float): 0-100 percentage

### set_layer_properties
- `layer_id` (int): Target layer
- `blend_mode` (string): Blend mode name (NORMAL, MULTIPLY, SCREEN, OVERLAY, etc.)

## Selection & Masking

### select_subject
AI-powered Neural Engine selection. Automatically detects and selects the main subject.
May return "No subject detected" — fallback to `select_rectangle`.

### select_sky
AI-powered sky detection and selection.

### select_rectangle / select_ellipse / select_polygon
- `bounds` (object): Geometric bounds for the selection
Manual selection shapes for precise control.

### add_layer_mask_from_selection
Converts the current active selection into a layer mask on the active layer.
**Preferred over erasing** — non-destructive, editable, reversible.

### remove_layer_mask
Removes the mask from a layer. Ask for confirmation first.

### remove_background
AI-powered one-click background removal. Creates a mask automatically.

## Styles & Adjustments

### Adjustment Layers
Non-destructive adjustments that affect all layers below:
- `add_brightness_contrast_adjustment_layer`
- `add_color_balance_adjustment_layer`
- `add_black_and_white_adjustment_layer`
- `add_vibrance_adjustment_layer`

### Effects
- `add_stroke_layer_style` — outline effect
- `create_gradient_layer_style` — gradient overlay
- `apply_gaussian_blur` — blur effect (may timeout on 4K)
- `apply_motion_blur` — directional blur

### harmonize_layer
Matches the color and lighting of a foreground layer to a background layer.
Essential for realistic compositing after background replacement.

## Document Management

### save_document
Save the current document state. **Call before high-risk operations.**

### flatten_all_layers
**DESTRUCTIVE. Never call unless user explicitly says "export", "final", or "flatten".**
Merges all layers into a single background layer. Cannot be undone after save.
