---
name: adobe-aftereffects-mcp
description: Adobe After Effects motion graphics and animation via adb-mcp ExtendScript. Use when creating compositions, animating layers, keyframing, writing expressions, building MOGRTs, rendering, compositing VFX, automating AE project setup, or working with the After Effects MCP server.
---

# Adobe After Effects MCP

## Purpose

Execute After Effects operations through the adb-mcp server's CEP plugin using `execute_extend_script`. Generate valid, self-contained ExtendScript (ES3) to create compositions, animate layers, apply effects, write expressions, and render output. AE is the **most powerful** Adobe MCP integration — full arbitrary scripting via ExtendScript.

## When to Use

- Creating or modifying After Effects compositions via MCP
- Animating layers with keyframes or expressions
- Building Motion Graphics Templates (MOGRTs) for Premiere
- Setting up render queue items for export
- Compositing visual effects or layered animations
- Automating project organization and layer management
- Reviewing animation quality and expression errors

## Examples

**Example 1: Create animated title card**
```
User: "Create a 5-second title card that fades in and scales up"
Claude: [Uses adobe-aftereffects-mcp]
  1. execute_extend_script: Create comp (1920x1080, 5s, 30fps)
  2. execute_extend_script: Add text layer "Title", set font/size/color
  3. execute_extend_script: Keyframe Opacity 0→100 over 1s with ease
  4. execute_extend_script: Keyframe Scale 80→100 over 1s with overshoot to 105
  "Title card created. Opacity fades in with ease, scale overshoots slightly for bounce feel."
```

**Example 2: Expression-driven animation**
```
User: "Make this logo wiggle subtly and loop"
Claude: [Uses adobe-aftereffects-mcp]
  1. execute_extend_script: Find logo layer by name
  2. execute_extend_script: Apply wiggle expression to Position — wiggle(2, 15)
  3. execute_extend_script: Apply loopOut("cycle") to any keyframed properties
  "Wiggle applied — 2 oscillations/sec, 15px amplitude. Loops infinitely via expression."
```

**Example 3: Animation critique**
```
User: "Review my comp for animation quality issues"
Claude: [Uses adobe-aftereffects-mcp]
  1. execute_extend_script: Query all layers, keyframes, and interpolation types
  2. Checks for linear keyframes on moving objects → suggests easing
  3. Checks for expression errors via prop.expressionError
  4. Checks motion blur settings (comp vs layer level)
  "Found 3 issues: Layers 2 and 5 use linear interpolation — add ease. Layer 7 has a broken expression. Motion blur is enabled on comp but disabled on your main animated layer."
```

## After Effects Fundamentals

### Object Model Hierarchy

All collections are **1-based** (not 0-based like JavaScript arrays).

- **Application (`app`)** → root entry point
- **Project (`app.project`)** → the single open `.aep` file, containing `items` collection
- **Item** → assets in the Project Panel:
  - **`CompItem`** → a timeline/composition containing layers
  - **`FootageItem`** → imported media (video, audio, images, solids)
  - **`FolderItem`** → organizational folders
- **Layer** → elements inside a `CompItem`:
  - **`AVLayer`** → visual layers (video, audio, solids, precomps)
  - **`TextLayer`** → text (manipulate via `TextDocument` object)
  - **`ShapeLayer`** → vector graphics
  - **`CameraLayer` / `LightLayer`** → 3D scene elements
- **Property / PropertyGroup** → animatable attributes:
  - **`PropertyGroup`** → containers like "Transform" or "Effects"
  - **`Property`** → value leaves (Position, Opacity, Scale)
- **Keyframes** → no "Keyframe object" — accessed via methods on Property: `prop.keyValue(1)`, `prop.keyTime(1)`, `prop.setValueAtTime(time, value)`

### Critical Concepts

- **ExtendScript (ES3)**: All operations go through `execute_extend_script` with a single `script_string` parameter. Scripts must be self-contained — no shared state between calls.
- **1-Based Indexing**: `app.project.item(1)`, `comp.layer(1)`, `prop.key(1)` — NOT 0-based.
- **Match Names**: Properties have display names ("Position") and match names ("ADBE Position"). Use match names for reliability: `layer.property("ADBE Transform Group").property("ADBE Position")`.
- **Undo Groups**: Every state-changing script MUST wrap in `app.beginUndoGroup()` / `app.endUndoGroup()`. Non-negotiable.

### Plugin Architecture

After Effects uses a **CEP plugin** via adb-mcp — the most powerful integration. Unlike PS/Premiere (UXP with fixed tool calls), AE exposes full ExtendScript execution.

```
Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ CEP Plugin ↔ After Effects
```

Load app-specific guidance at session start with `config://get_instructions`.

### MCP Tool

There is **one primary tool**:

**`execute_extend_script`**
- `script_string` (string, required): Complete, valid ExtendScript code
- Returns: JSON-stringified result of the last evaluated statement
- Scripts should end with `JSON.stringify({...})` to pass data back

No inspection tools like Photoshop's `get_document_image`. AE is a **blind spot** — you cannot "see" the canvas. Rely on querying object state and property values to verify work.

### What MCP Can vs Cannot Do

| Can Automate | Requires Manual Work |
|-------------|---------------------|
| Create comps, add layers, organize project | Visual preview of rendered frames |
| Keyframe any animatable property | Complex particle systems (Particular, Form) |
| Write and apply expressions | Third-party plugin parameter access |
| Apply built-in effects and set parameters | Render queue monitoring (blocks UI) |
| Build MOGRTs for Premiere handoff | Hand-drawn animation / Puppet Pin rigging |
| Query project structure and find errors | Color management / OCIO setup |
| Set render queue items and output modules | Interactive preview playback |

For the complete ExtendScript pattern reference, see `references/ae-extendscript-patterns.md`.

## Editorial Intelligence

### Animation Principles Checklist

When reviewing or suggesting animation:

1. **Easing** — Never leave keyframes linear on moving objects. Use `KeyframeEase` objects or expressions.
2. **Overshoot** — Scale/position arriving at rest should overshoot slightly (e.g., Scale 0→110→100) for organic feel.
3. **Anticipation** — Before a major movement, add a small counter-movement (pull back before push forward).
4. **Timing** — 1-2 frame movements are invisible strobing. Minimum visible motion: 3-4 frames at 30fps.
5. **Motion Blur** — Enable on comp AND on individual moving layers. Check both.
6. **Stagger** — Multiple elements animating identically look mechanical. Offset start times by 2-4 frames.

### Critique Rubrics

**Technical Rubric:**
- Are layers named descriptively (not "Shape Layer 1")?
- Are layers color-coded with labels?
- Are there unused layers or empty groups?
- Query `prop.expressionError` to find broken expressions
- Is motion blur enabled globally but disabled on moving layers?

**Aesthetic Rubric:**
- Query `keyOutInterpolationType` — if `LINEAR` on moving objects, suggest easing
- Calculate duration between keyframes — flag movements under 3 frames
- Check for overshoot on scale/position animations arriving at rest

## Workflow Patterns

### Pattern A: Composition Setup
1. `execute_extend_script`: Create comp with `proj.items.addComp(name, w, h, pixelAspect, duration, fps)`
2. Add layers: `comp.layers.addSolid()`, `comp.layers.addText()`, `comp.layers.addShape()`
3. Rename all layers immediately — no "Shape Layer 1" in production
4. Organize into folders: `proj.items.addFolder("Precomps")`

### Pattern B: Keyframe Animation
1. Access property: `layer.property("ADBE Transform Group").property("ADBE Position")`
2. Set keyframes: `prop.setValueAtTime(0, [960, 540])`, `prop.setValueAtTime(1, [960, 200])`
3. Apply easing: Create `KeyframeEase` objects, apply via `prop.setTemporalEaseAtKey()`
4. Verify: Query `prop.numKeys` and `prop.keyValue()` to confirm

### Pattern C: Expression Automation
1. Apply expression string: `prop.expression = "wiggle(2, 50)";`
2. Check for errors: `if (prop.expressionError !== "") { /* fix */ }`
3. Common expressions: `wiggle()`, `loopOut("cycle")`, `loopOut("pingpong")`, `sourceRectAtTime()`, `linear()`, `ease()`

### Pattern D: MOGRT Preparation
1. Build comp with expression-controlled properties
2. Add properties to Essential Graphics Panel: `prop.addToMotionGraphicsTemplate(comp)`
3. Set template name: `comp.motionGraphicsTemplateName = "My Template"`
4. Use `sourceRectAtTime()` for auto-sizing backgrounds behind editable text

## Execution Protocol

### Small-Batch Pattern
1. Execute **1-2 scripts** (AE scripts are more complex than PS/Premiere operations)
2. **Pause** — query project state via a read-only script to verify
3. **Continue** only after verification
4. For complex tasks, save between phases

### Guardrails

| Rule | Action |
|------|--------|
| Undo Group mandate | Every state-changing script wrapped in `beginUndoGroup` / `endUndoGroup` |
| Try/Catch always | All scripts wrapped in try/catch to prevent UI-blocking alerts |
| 1-based indexing | Never use index 0 for collections — AE collections start at 1 |
| No infinite loops | Use `for` loops with explicit bounds, never unbounded `while` |
| Suppress dialogs | Set `app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS` for batch ops |
| JSON return | End scripts with `JSON.stringify({status, data})` to pass results back |
| Name everything | Every created layer/comp renamed immediately — no defaults |

### Error Handling

- **UI freeze**: AE freezes during script execution. Keep scripts efficient, avoid heavy iteration.
- **No visual verification**: Unlike PS, there is no `get_document_image`. Query object properties to verify state.
- **Expression errors**: Check `prop.expressionError` after applying expressions.
- **Render queue**: Don't start renders that block the script. Queue items and instruct user to render, or use `aerender` command-line.
- **Object invalidation**: Deleting an object invalidates references. Re-fetch collections after deletions.

For shared guardrails and cross-app patterns, see `adobe-cross-app-workflows`. For planning and critique, see `creative-director`.

## Success Criteria

- [ ] Loaded AE MCP guidance via `config://get_instructions` at session start
- [ ] Every state-changing script wrapped in undo group and try/catch
- [ ] Used 1-based indexing for all AE collections
- [ ] Named all created layers and comps descriptively
- [ ] Ended scripts with JSON.stringify for data return
- [ ] Applied easing to keyframed properties (never left linear on motion)
- [ ] Queried project state to verify work (no visual preview available)
- [ ] Clearly communicated what requires manual work (render monitoring, visual preview)

## Copy/Paste Ready

```
"Create an After Effects composition with animated text"
"Add keyframes and easing to this layer's position"
"Write an expression for looping wiggle animation"
"Build a MOGRT template for Premiere"
"Review my AE project for animation quality issues"
```
