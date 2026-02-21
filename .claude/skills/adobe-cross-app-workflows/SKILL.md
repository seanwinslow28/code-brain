---
name: adobe-cross-app-workflows
description: Cross-app Adobe pipeline orchestration and MCP architecture reference. Use when coordinating work across multiple Adobe apps, troubleshooting MCP proxy connections, planning asset handoffs between Illustrator/Photoshop/After Effects/Premiere, debugging the adb-mcp server, or managing the animation pipeline.
---

# Adobe Cross-App Workflows

## Purpose

Orchestrate multi-app Adobe pipelines, define shared guardrails across all app skills, document the MCP architecture for troubleshooting, and manage handoffs between the Creative Director planning layer and the four execution skills.

## When to Use

- Coordinating assets across multiple Adobe apps (e.g., Illustrator vectors → After Effects animation)
- Troubleshooting MCP proxy connections or plugin errors
- Planning the order of operations for a multi-app pipeline
- Needing shared guardrails (naming conventions, checkpoint behavior, destructive action safeguards)
- Understanding the adb-mcp architecture (proxy, plugin, transport)
- Starting a cross-app workflow like the animation pipeline or social media content creation

## Examples

**Example 1: Animation pipeline**
```
User: "I have character designs in Illustrator that need to be animated in After Effects and assembled in Premiere"
Claude: [Uses adobe-cross-app-workflows] Plans the pipeline:
  1. Illustrator: Clean up layers, name groups, save as .ai with "Create PDF Compatible File" ON
  2. After Effects: Import .ai as "Composition - Retain Layer Sizes", rig with nulls, animate
  3. After Effects: Render to ProRes 422 .mov
  4. Premiere: Import rendered .mov, assemble with audio, titles, export
  Checkpoint: Verify frame rate consistency (24fps) across all apps.
  "Start with /adobe-illustrator-mcp for asset prep."
```

**Example 2: MCP troubleshooting**
```
User: "The Photoshop MCP connection keeps dropping"
Claude: [Uses adobe-cross-app-workflows] Diagnoses:
  1. Check proxy server is running (Node.js WebSocket on correct port)
  2. Verify the UXP plugin is loaded in Photoshop (Window > Plugins)
  3. Check MCP server process (Python stdio transport)
  4. Test with a simple tool call: get_document_info
  5. If timeout: restart proxy server first, then reload plugin
```

**Example 3: Social media content from existing assets**
```
User: "I need to repurpose my festival short film into TikTok and Instagram Reels"
Claude: [Uses adobe-cross-app-workflows] Plans:
  1. Premiere: Duplicate sequence, change settings to 1080x1920 (9:16)
  2. Premiere: Reframe key shots (Scale/Position in Effect Controls)
  3. After Effects: Create vertical-safe title cards with safe zone guides
  4. Premiere: Import title cards, add captions, export H.264 per platform specs
  Safe zones: Keep text out of bottom 15% (TikTok UI) and top 10% (Instagram UI)
```

## MCP Architecture Reference

### System Architecture

```
Claude Code ↔ MCP Server (Python, stdio) ↔ Proxy Server (Node.js, WebSocket) ↔ Adobe Plugin ↔ Adobe App
```

- **MCP Server**: Python process using stdio transport. One server per app (ps-mcp.py, pr-mcp.py, ae-mcp.py, ai-mcp.py).
- **Proxy Server**: Node.js WebSocket bridge. Translates MCP tool calls into plugin messages.
- **Adobe Plugin**: UXP (Photoshop, Premiere) or CEP (After Effects, Illustrator). Receives commands and executes within the host app.

### Plugin Types by App

| App | Plugin Type | Capability | Script Language |
|-----|-----------|-----------|-----------------|
| Photoshop | UXP | Rich API with dedicated tool calls | UXP DOM + BatchPlay |
| Premiere Pro | UXP | Limited API, many manual gaps | UXP DOM (async) |
| After Effects | CEP | Full scripting via execute_extend_script | ExtendScript (ES3) |
| Illustrator | CEP | Full scripting via execute_extend_script | ExtendScript (ES3) |

### Connection Troubleshooting

1. **"Connection refused"** → Proxy server not running. Start Node.js proxy on the correct port.
2. **"Plugin not found"** → UXP/CEP plugin not loaded. Check Window > Extensions (CEP) or Window > Plugins (UXP).
3. **"Timeout"** → Operation took too long. For UXP apps: check if modal dialog is blocking. For CEP apps: check if ExtendScript is in infinite loop.
4. **"Script error"** → ExtendScript syntax error (AE/AI). Check the error message for line numbers. Common: missing semicolons, 0-vs-1 indexing.
5. **"Permission denied"** → UXP sandbox restriction. User must grant folder access via manifest or Developer Tool.

## Shared Guardrails (All App Skills)

### Naming Conventions

- **Files**: `YYMMDD_ProjectName_Element_v01`
- **Layers/Comps**: Descriptive names, no "Layer 1" or "copy"
- **Bins/Folders**: Numbered prefixes (`01_Assets`, `02_Sequences`, `03_Renders`)
- **Exports**: `[Date]_[Project]_[Codec].[ext]`

### Checkpoint Behavior

All app skills follow the **small-batch execution pattern**:

1. Execute 2-3 operations
2. Pause for verification (screenshot, get_document_image, or user confirmation)
3. Continue only after verification passes

### Destructive Action Safeguards

Before any of these operations, the skill MUST:
1. Save the project/document
2. Warn the user and get explicit confirmation

| Action | App | Guardrail |
|--------|-----|-----------|
| Flatten layers | Photoshop | Only if user says "export", "final", or "flatten" |
| Rasterize type/effects | Photoshop, Illustrator | Save backup first, confirm intent |
| Ripple delete | Premiere | Default to Lift (non-ripple), only ripple on explicit request |
| Overwrite on timeline | Premiere | Check track first, prefer new track |
| Merge/collapse layers | After Effects | Duplicate comp before merging |
| Delete unused media | All | List items first, confirm before removing |

### State Verification (Pre-Flight)

Before editing, each app skill verifies:
- **Photoshop**: `get_document_info` → resolution, color mode, saved state
- **Premiere**: `get_project_info` → active sequence, track structure
- **After Effects**: `app.project.activeItem instanceof CompItem` → valid comp selected
- **Illustrator**: `app.activeDocument` exists, `documentColorSpace` matches target

### Error Handling Strategy

All scripts (especially ExtendScript in AE/AI) must:
1. Wrap in `try/catch` with JSON return: `{"status": "error", "message": "..."}`
2. Never rely on host app UI for error display
3. Return structured status so Claude can diagnose and retry

## Cross-App Pipeline Patterns

### Pipeline 1: Vector-to-Video (Animation)

```
Illustrator (Design) → After Effects (Motion) → Premiere (Assembly)
```

1. **Illustrator**: Clean layers, name groups. Save `.ai` with "Create PDF Compatible File" ON.
2. **After Effects**: Import `.ai` as "Composition - Retain Layer Sizes". Rig, animate, render to ProRes 422.
3. **Premiere**: Import `.mov`, assemble with audio/titles, final export.

**Critical**: Frame rate must match across all apps (e.g., 24fps consistently).

### Pipeline 2: Sprite Processing (Game Assets)

```
Illustrator (Vector Design) → Photoshop (Raster Composite) → Game Engine
```

1. **Illustrator**: Design vector sprites on grid. Export PNG with `anti_aliasing=False`, integer scale.
2. **Photoshop**: Import PNGs, assemble sprite sheet (calculate grid → place_image → translate_layer).
3. **Export**: Save sprite sheet as PNG-24 with transparency for engine import.

**Critical**: All coordinates must be integers. Power-of-two texture sizes preferred.

### Pipeline 3: Social Media Content

```
After Effects (Motion Graphics) → Premiere (Assembly + Audio) → Export per Platform
```

1. **After Effects**: Create title cards, lower thirds, animated overlays.
2. **Premiere**: Import AE comps via Dynamic Link or rendered files. Add VO, music, sound effects.
3. **Export**: Platform-specific presets (TikTok: H.264, 9:16, <15s; YouTube: H.264, 16:9, 10-20Mbps).

### Pipeline 4: Festival Submission

```
Illustrator (Poster) + After Effects (Film) + Premiere (Final Assembly) → DCP/ProRes
```

1. **Illustrator**: Festival poster/laurels as vector → export high-res PNG.
2. **After Effects**: Animated title sequence, VFX shots.
3. **Premiere**: Full assembly with color grade. Export ProRes 422 HQ, PCM audio, 24fps.
4. **Specs**: Cannes/Tribeca require DCP. Use Simple DCP or similar service for final package.

## Creative Director → Execution Handoff

The `creative-director` skill generates a Technical Execution Plan and App Handoff Protocol. The handoff flow:

1. **Creative Director** completes interview and route selection
2. **Creative Director** generates execution plan with app assignments
3. **User** invokes the first app skill (e.g., `/adobe-illustrator-mcp`)
4. **App Skill** executes Phase A, pauses at checkpoint
5. **User** invokes next app skill for next phase
6. **Creative Director** reviews at 30/60/90% checkpoints

The app skills are independent — they don't call each other. The user (guided by the Creative Director's plan) is the orchestrator.

### Pipeline 5: Social Content Repurposing (16BitFit / Conference Clips)

```
Photoshop (Comp/Thumbnails) → After Effects (Motion Graphics) → Premiere (Edit + Audio) → Export per Platform
```

1. **Photoshop**: Create thumbnail comp, social safe-zone template (9:16 with 15% bottom margin for TikTok UI, 10% top for IG).
2. **After Effects**: Animate title cards, branded lower thirds, CTA overlays. Use Essential Graphics for reusability.
3. **Premiere**: Import AE comps via Dynamic Link. Cut/arrange footage, add VO, music, captions.
4. **Export**: Per platform:
   - **TikTok/Reels**: H.264, 1080x1920, <60s, <100MB
   - **YouTube Shorts**: H.264, 1080x1920, <60s
   - **Twitter/X**: H.264, 1280x720 or 1080x1080, <2:20
   - **LinkedIn**: H.264, 1920x1080, <10min

**Tip**: Create a Premiere export preset for each platform to avoid re-entering specs.

### Pipeline 6: MOGRT Production (Reusable Motion Templates)

```
After Effects (Design + Animate) → Essential Graphics Panel → Premiere (Consume Template)
```

1. **After Effects**: Design the motion graphic (lower third, title card, transition).
2. **After Effects**: Open Essential Graphics Panel (Window > Essential Graphics). Add editable properties:
   - Text layers → "Edit Properties" for copy changes in Premiere
   - Color controls → Expression-linked to dropdown or color picker
   - Duration → Linked to marker or expression slider
3. **After Effects**: Export as `.mogrt` (File > Export > Motion Graphics Template).
4. **Premiere**: Install MOGRT (Graphics > Install Motion Graphics Template). Drag onto timeline, edit text/colors in Essential Graphics panel.

**Use case**: Recurring branded elements (episode titles, sponsor cards, social CTAs) that non-AE users can customize in Premiere.

### Connection Troubleshooting (Extended)

Common failure patterns beyond basic connectivity:

| Symptom | Root Cause | Fix |
|:--------|:-----------|:----|
| Plugin loads but no response | Proxy WebSocket port mismatch | Check `PORT` env var matches proxy config |
| Commands work then suddenly stop | Adobe app modal dialog blocking | Dismiss any open dialog, then retry |
| ExtendScript returns `undefined` | Script doesn't end with return value | Ensure last line returns JSON string |
| "Object is not valid" in AE | Stale comp reference after save | Re-query `app.project.activeItem` |
| Slow response (>30s) for simple ops | Large file open in background | Close unused documents/projects |
| UXP plugin crashes on startup | Manifest version mismatch | Update `manifest.json` apiVersion to match app version |

## Known Gaps and Workarounds

### Blind Spot in CEP Apps (AE/AI)

Photoshop has `get_document_image` to let Claude "see" the canvas. After Effects and Illustrator do NOT have this. Workarounds:
- **AE**: Ask user to screenshot, or write ExtendScript to render a single frame to a temp file
- **AI**: Use `export_png` to render a proof image for visual review

### Asset Path Management

The handoff protocol defines a folder structure (`_Assets`, `_ProjectFiles`, `_Renders`). Enforce this across apps so skills can reliably find files without asking for absolute paths every time.

### BridgeTalk (Advanced)

For advanced inter-app communication, ExtendScript's `BridgeTalk` object can send commands between Adobe apps. Use `BridgeTalk.send()` to trigger actions in another app without user intervention. This is experimental and not part of the standard MCP workflow.

## Success Criteria

- [ ] Pipeline order documented with file format requirements at each handoff
- [ ] Frame rate and color space consistency verified across apps
- [ ] Naming conventions applied consistently in all apps
- [ ] Pre-flight verification run before editing in each app
- [ ] Checkpoint behavior followed (2-3 ops → pause → verify)
- [ ] Destructive actions blocked without explicit user confirmation
- [ ] MCP connection issues diagnosed using the troubleshooting guide

## Copy/Paste Ready

```
"Plan a multi-app workflow for [project]"
"The MCP connection to [app] is failing"
"How do I get assets from Illustrator into After Effects?"
"What's the pipeline for [animation / social / festival]?"
"Troubleshoot the Adobe proxy server"
```
