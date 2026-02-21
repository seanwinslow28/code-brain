---
name: adobe-illustrator-mcp
description: Adobe Illustrator vector graphics and asset automation via adb-mcp ExtendScript. Use when creating vector art, SVG export, icon design, logo creation, artboard management, character model sheets, sprite assembly in Illustrator, path manipulation, or working with the Illustrator MCP server.
---

# Adobe Illustrator MCP

## Purpose

Execute Illustrator operations through the adb-mcp server's CEP plugin. Use `execute_extend_script` for vector creation and manipulation, plus dedicated tools for document inspection and PNG export. Illustrator handles vector assets for games, web, and print — from pixel-perfect sprites to SVG-optimized icons.

## When to Use

- Creating or editing vector art in Illustrator via MCP
- Assembling vector sprite sheets for game engines
- Batch processing icons (normalize, align, export)
- Building character model sheets with multiple poses
- Exporting SVG optimized for web or animation
- Creating logos, badges, or UI elements
- Managing artboards and multi-page layouts

## Examples

**Example 1: Vector sprite assembly for 16BitFit**
```
User: "Create a 4x3 sprite grid at 64x64px per cell"
Claude: [Uses adobe-illustrator-mcp]
  1. get_active_document_info — check workspace state
  2. execute_extend_script: Create document 256x192, add grid guides
  3. execute_extend_script: Create 12 named groups ("Sprite_01" through "Sprite_12")
  4. execute_extend_script: Position groups at grid coordinates
  5. export_png with anti_aliasing=false, horizontal_scale=400
  "Sprite grid created. 12 cells at 64x64. Exported at 4x scale with no anti-aliasing for crisp pixels."
```

**Example 2: Icon batch normalization**
```
User: "Normalize these 20 icons to 24x24 artboards, centered"
Claude: [Uses adobe-illustrator-mcp]
  1. get_documents — map all open files
  2. For each: execute_extend_script to select all → group → align to artboard center
  3. For each: execute_extend_script to resize artboard to 24x24
  4. export_png for each with artboard_clipping=true
  "20 icons normalized. All centered on 24x24 artboards and exported."
```

**Example 3: SVG export for web**
```
User: "Export this illustration as optimized SVG for the website"
Claude: [Uses adobe-illustrator-mcp]
  1. execute_extend_script: Convert all text to outlines (fontType: OUTLINEFONT)
  2. execute_extend_script: Export with SVG options — presentation attributes, precision 3, no raster embed
  "SVG exported with presentation attributes for CSS animation compatibility. Text converted to outlines for font independence."
```

## Illustrator Fundamentals

### Document Object Model

- **Application (`app`)** → root entry point
- **Document (`app.activeDocument`)** → the target for 90% of operations
  - **Layers** → containers for artwork. Index 0 is topmost/frontmost.
  - **Artboards** → exportable regions defining output boundaries
- **PageItems** → the drawable objects:
  - **`PathItem`** → basic vector shapes (rectangles, ellipses, custom bezier paths)
  - **`CompoundPathItem`** → complex shapes with holes (all paths share same style)
  - **`GroupItem`** → logical grouping of multiple items
  - **`TextFrame`** → text objects (Point Text or Area Text)

### Critical Concepts

- **Coordinate System**: Origin (0,0) is top-left of artboard. **Y-axis quirk**: Negative Y values move DOWN the canvas. `pathItems.rectangle(top, left, width, height)` uses argument order `(y, x, w, h)` — non-standard.
- **Points Unit System**: All scripting uses Points (pt). 72pt = 1 inch. For game assets: treat 1pt = 1px.
- **Color Model Enforcement**: Documents are strictly RGB or CMYK. Use `new RGBColor()` in RGB docs, `new CMYKColor()` in CMYK docs. Cross-applying causes muddy color conversion.
- **ExtendScript (ES3)**: Primary scripting via `execute_extend_script`. Self-contained, no shared state between calls.

### Plugin Architecture

Illustrator uses a **CEP plugin** via adb-mcp with both dedicated tools and ExtendScript execution.

```
Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ CEP Plugin ↔ Illustrator
```

Load app-specific guidance at session start with `config://get_instructions`.

### MCP Tools

**Information Gathering:**
- **`get_documents()`** — list all open documents with IDs, names, dimensions, layer counts
- **`get_active_document_info()`** — deep scan: artboard dimensions, layer structure, selection state

**Execution:**
- **`execute_extend_script(script_string)`** — inject raw ExtendScript (JSX) into Illustrator. Wrap in try/catch, return JSON.
- **`open_file(path)`** — open an existing `.ai` file or template

**Export:**
- **`export_png(path, ...)`** — export active document to PNG:
  - `path` (required): save location
  - `transparency` (bool, default: true)
  - `anti_aliasing` (bool, default: true) — set false for pixel art
  - `artboard_clipping` (bool, default: true)
  - `horizontal_scale` / `vertical_scale` (int): percentage (e.g., 400 for 4x)
  - `export_type`: "PNG24" or "PNG8"

### What MCP Can vs Cannot Do

| Can Automate | Requires Manual Work |
|-------------|---------------------|
| Create/manipulate paths, shapes, text | Gradient mesh editing |
| Group, layer, and organize artwork | Complex pathfinder operations (some) |
| Apply colors, strokes, transformations | Live Paint, Image Trace fine-tuning |
| Export PNG and SVG programmatically | Symbol spraying and editing |
| Manage artboards | Perspective grid drawing |
| Batch process files | Pattern editing inside Pattern Mode |

For the complete ExtendScript pattern reference, see `references/ai-extendscript-patterns.md`.

## Workflow Patterns

### Pattern A: Vector Sprite Assembly
1. `get_active_document_info` to check workspace
2. `execute_extend_script`: Create document, set coordinate system
3. `execute_extend_script`: Draw shapes at grid positions using integer coordinates (no sub-pixel)
4. `execute_extend_script`: Name and group each sprite cell
5. `export_png` with `anti_aliasing=false` for pixel-perfect output

### Pattern B: Icon Batch Processing
1. `get_documents` to map workspace
2. For each file: `execute_extend_script` to unlock layers, select all, group, align to artboard center
3. Clean: remove hidden items and empty text frames
4. `export_png` per file with `artboard_clipping=true`

### Pattern C: Model Sheet Generation
1. `execute_extend_script`: Create artboards for each pose (`doc.artboards.add(rect)`)
2. `execute_extend_script`: Add labeled text frames ("Front View", "Side View", "Iso View")
3. `execute_extend_script`: Create named groups per view ("Pose_Front", "Pose_Side")
4. Organize: one group per artboard, consistent naming

### Pattern D: SVG Export Optimization
1. `execute_extend_script` with `ExportOptionsSVG`:
   - `cssProperties = SVGCSSPropertyLocation.PRESENTATIONATTRIBUTES` (best for CSS animation)
   - `fontType = SVGFontType.OUTLINEFONT` (converts text to shapes)
   - `coordinatePrecision = 3` (balance file size vs precision)
   - `embedRasterImages = false` (keep SVG light)

## Execution Protocol

### Small-Batch Pattern
1. Execute **2-3 operations**
2. **Pause** — call `get_active_document_info` to verify document state
3. **Continue** only after verification
4. Save periodically for batch operations

### Guardrails

| Rule | Action |
|------|--------|
| Coordinate normalization | Set `app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM` at script start |
| No infinite loops | Use `for` loops with explicit bounds (`doc.pageItems.length`), never unbounded `while` |
| Suppress dialogs | Set `app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS` for batch ops |
| Integer coordinates for sprites | Round all positions to integers — sub-pixel values cause anti-aliasing fuzz |
| Color model match | Check `doc.documentColorSpace` before creating color objects |
| Name everything | Every created group/path/text named immediately |
| Try/catch + JSON return | All scripts wrapped, end with `JSON.stringify()` |

### Error Handling

- **Modal dialog hang**: "Missing Font" or "Color Profile" dialogs freeze scripts. Suppress with `DONTDISPLAYALERTS`.
- **Object invalidation**: Deleting items invalidates variable references. Re-fetch collections after deletion.
- **Y-axis confusion**: Test coordinates with simple shapes first. Negative Y = down on canvas.
- **Parameter order**: `pathItems.rectangle(y, x, w, h)` — not the standard `(x, y, w, h)`.
- **Modern features**: Gradient Mesh, Repeat Grids lack full scripting. Use `app.executeMenuCommand()` workarounds or manual steps.

For shared guardrails and cross-app patterns, see `adobe-cross-app-workflows`. For planning and critique, see `creative-director`.

## Success Criteria

- [ ] Loaded Illustrator MCP guidance via `config://get_instructions` at session start
- [ ] Set coordinate system to artboard coordinates in scripts
- [ ] Used correct color model matching document color space
- [ ] Integer coordinates for pixel-art/sprite workflows (no sub-pixel)
- [ ] Named all created elements descriptively
- [ ] Wrapped scripts in try/catch with JSON return
- [ ] Used `for` loops with explicit bounds (no `while` loops)
- [ ] Verified document state with `get_active_document_info` between batches

## Copy/Paste Ready

```
"Create vector sprites in Illustrator for the game"
"Export this as optimized SVG for the website"
"Batch normalize these icons to 24x24"
"Build a character model sheet with front/side/iso views"
"Set up artboards for a multi-page icon set"
```
