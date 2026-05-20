# Adobe MCP Automation — Unified Synthesis v2
**Analyst:** Claude (for Sean Winslow) | **Date:** February 18, 2026
**Sources:** Gemini 3.0 Deep Think — 4 initial app analyses + 4 follow-up plugin/library analyses | Web research on DaVinci Resolve MCP + ButterCut

---

## 1. The Power Ranking — Where Each App Actually Stands

### Tier 1: After Effects — The Crown Jewel
**Automation depth: ~85%** of what matters is scriptable.

AE is the most powerful MCP app by a wide margin. ExtendScript gives full programmatic control over compositions, layers, keyframes, expressions, text, render queue, file I/O, cameras, and time remapping. The entire object model is exposed (Application → Project → CompItem → Layers → Properties → Keyframes), and expressions provide a second scripting layer for procedural animation, physics, looping, and rigging.

**The AI superpower:** Claude can write expressions — JavaScript math logic injected directly into layer properties. This is unique to AE in the stack.

**What's PARTIAL:** Effects (built-in yes, 3rd-party plugin UIs no), masks (track mattes yes, organic roto no), shape layers (DOM is convoluted nested groups).

**Critical constraint:** ExtendScript is ES3 — no `let`, `const`, arrow functions. Claude must write `var` everywhere.

**Plugin Ecosystem Expansion (from Gemini follow-up):**

| Tool | Type | Priority | What It Unlocks |
|------|------|----------|-----------------|
| **extendscript-es5-shim** | Polyfill | **Install immediately** | Adds `.map()`, `.filter()`, `.forEach()` to ES3 environment. Claude naturally writes modern JS; this prevents SyntaxErrors. Zero risk, pure upside. |
| **aequery** | Library | **Install immediately** | jQuery for AE. One-liner selectors instead of 20-line DOM loops. Stable despite 2022 date — AE DOM unchanged. |
| **aerender CLI** | Built-in | **Set up immediately** | Headless rendering via Python subprocess. Doesn't lock AE UI. Gotcha: `-OMtemplate` must match saved Output Module name exactly. |
| **DuAEF / Duik API** | Library | **Verify first** | Claims scriptable IK rigging via `#include "Duik_api.jsxinc"`. Test simple `Duik.Rig.arm()` call through MCP before building workflows. |
| **AEUX JSON Schema** | Bridge | **Verify first** | Generate structured JSON → AEUX script builds Shape Layers. Bypasses nightmare Shape Layer DOM. Check schema documentation quality. |
| **DuAEF Expression Library** | Reference | **Verify first** | Battle-tested bounce/physics/loop expressions. Reference bank instead of Claude inventing from scratch. |
| **Nexrender** | Renderer | **Lower priority** | Data-driven batch rendering. Great for 50 sprite variations, overkill for single jobs. |
| **Dakkshin/after-effects-mcp** | Alt MCP | **Audit patterns** | Alternative MCP server — check tool definitions for ideas to port to adb-mcp. |

**Key architecture change:** Add `beginUndoGroup()`/`endUndoGroup()` wrapper to AE MCP server as the #1 safety improvement. Without this, every individual command creates a separate undo state, making rollback impossible for multi-step operations.

---

### Tier 2: Photoshop — Strong with a Generative AI Edge
**Automation depth: ~75%** of what matters.

PS has a modern UXP API via batchPlay that handles documents, layers, masks, text, filters, file I/O, batch operations, and canvas inspection (screenshot → Claude Vision). The UXP sandbox is more restrictive than ExtendScript but the adb-mcp proxy handles file I/O externally.

**Unique advantage:** Nano Banana Pro is recordable as Photoshop Actions — Claude can trigger AI generation via `app.doAction()`. This is the only app where Claude can programmatically invoke a generative AI tool with structural/reference image control.

**What's PARTIAL:** Selections (math-based full, organic needs vision), drawing (fills/gradients fine, brush strokes poor), Smart Objects (file dialog issues), color management (Indexed Color kills Gen AI — must be last step).

**Critical architectural shift (from Gemini follow-up):**

Gemini recommends stopping Photoshop from being the generator. Use **ComfyUI as generator, Photoshop as canvas.** The reasoning: Nano Banana Pro → Actions path is brittle (Claude → MCP → proxy → UXP → doAction() → plugin → cloud → wait). ComfyUI API path is cleaner: Claude → Python MCP → HTTP POST to localhost:8188 → RTX 5080 generates locally ~2 seconds → batchPlay import to PS.

**Revised priority:** Build ComfyUI API workflow (IP-Adapter + ControlNet OpenPose) FIRST. Nano Banana becomes fallback, not primary.

**Plugin Ecosystem Expansion:**

| Tool | Type | Priority | What It Unlocks |
|------|------|----------|-----------------|
| **Alchemist** | Inspector | **Install immediately** | Translates PS actions to batchPlay JSON. Developer tool to discover API calls and expand adb-mcp command surface. |
| **Pyxelate** | Python lib | **Install immediately** | Converts AI images to clean pixel art using Bayesian model. Better than Nearest Neighbor. `pip install pyxelate`. |
| **OpenCV/NumPy bounding box** | Python | **Build immediately** | `cv2.boundingRect()` for exact pixel coordinates. Solves sprite shimmer mathematically (Frame 1 at Y=10, Frame 4 at Y=15 = bob). |
| **ImageMagick `-remap +dither`** | CLI | **Install immediately** | `magick input.png +dither -remap gameboy.pal output.png` — mathematically forces 4-color palette. More reliable than PS Gradient Map via script. |
| **TexturePacker CLI** | CLI | **Confirmed headless** | `--format phaser --sheet hero.png --data hero.json` — removes PS from packing phase entirely. |
| **Auto-Photoshop-SD-Plugin** | Bridge | **Verify if needed** | 7.2k stars, claims Actions support. ComfyUI API path preferred. |

---

### Tier 3: Illustrator — Solid for Vector, Locked Out of AI
**Automation depth: ~65%** of what matters.

Illustrator's ExtendScript controls the DOM well: documents, artboards, shape primitives, color/styling, layers, symbols, transforms, exports, file I/O, batch operations, and selection/inspection. The agent is strong at mathematical, deterministic vector work.

**Hard wall:** Every Firefly AI feature is confirmed unscriptable — Generative Recolor, Text to Vector, Generative Shape Fill, Text to Pattern, Mockup. The Actions workaround is static and unreliable (async cloud + synchronous ExtendScript = timeouts).

**Illustrator is NOT a pixel art tool.** Use for scalable UI, vector logos, promotional art, animation model sheets — not 16BitFit sprites.

**Plugin Ecosystem Expansion (from Gemini follow-up):**

| Tool | Type | Priority | What It Unlocks |
|------|------|----------|-----------------|
| **JSON2.js** | Polyfill | **Mandatory** | Adds `JSON.parse()` and `JSON.stringify()` to ES3 environment. Without it, agent cannot pass structured data (color palettes, item stats, config arrays) into Illustrator. `#include "json2.js"` at top of every script. |
| **Recraft.ai V3 SVG** | API | **Test quality first** | Only frontier AI model that generates *mathematical SVG vectors* from text prompts (not raster traces). ~$0.08/generation. Prompt like "flat 2D RPG sword icon, pixel-perfect, 4 colors." Holy grail if quality holds up. |
| **vTracer** | Python CLI | **Install immediately** | Rust-based raster-to-vector. Free, `pip install vtracer`. Has `pixel` mode for retro art without smoothing sharp corners. 5.5k stars. |
| **SVGO** | Node.js | **Mandatory pipeline step** | Strips redundant tags/anchors from AI-generated SVGs. Reduces anchor points 50-70%. Run on EVERY imported SVG before ExtendScript touches it. |
| **Shapely** | Python lib | **Build workaround** | Headless boolean geometry. Extract paths via ExtendScript → send to Python Shapely → return clean merged SVG paths. Avoids `executeMenuCommand('Live Pathfinder Add')` GUI race conditions. |
| **Vectorizer.ai** | API | **Verify vs vTracer** | Proprietary deep learning tracer. $9.99/mo. Better for complex organic art. Test against vTracer on same input before paying. |
| **creold/illustrator-scripts** | Reference | **Index for agent** | 1k+ stars, updated 2025/2026. Definitive modern Illustrator ExtendScript bible. Agent syntax baseline. |

**Vector Generation Pipeline Rankings:**

1. **Recraft API → SVGO → Illustrator place()** — Best quality/speed for game UI. Native math-based SVG. ~$0.08/image.
2. **Local SD → vTracer (pixel mode) → Illustrator** — Best for budget + retro 16BitFit sprites. Free. Medium complexity.
3. **Midjourney/DALL-E → Vectorizer.ai → SVGO → Illustrator** — Best for complex organic art. High cost (two APIs).

**Critical operational rules:**
- Bundle all commands into a single `evalScript()` payload (Illustrator has no `beginUndoGroup()` — CEP treats entire payload as one undo state)
- Never use `app.executeMenuCommand('Live Trace Make')` — async, locks UI, terrible geometry
- Never attempt Firefly features via script — route to external APIs
- Always run SVGO before importing AI-generated SVGs

**CEP → UXP Migration Note:** Adobe is deprecating CEP in favor of UXP. Illustrator's UXP is in beta as of 2024/2025. CEP remains functional today, but will eventually break the current adb-mcp bridge. The UXP migration path is actually simpler: Python MCP hosts WebSocket, UXP plugin connects as client. Gives modern V8 JavaScript (native JSON.parse, fetch, async/await). Timeline estimate: late 2026/2027.

---

### Tier 4: Premiere Pro — Assembly & Delivery Engine
**Automation depth: ~35%** creative editing, ~90% deliverables/logistics.

Premiere's scripting surface is the shallowest. FULL control exists only for project management, media import/organization, markers, and timeline inspection. Everything creative — Lumetri color, Essential Sound, native text, auto-captioning, Dynamic Link — is **NOT AVAILABLE** via API. Adobe sandboxes these panels at the C++ level. No third-party plugin can create ExtendScript hooks for them.

**Premiere's MCP value:** Not creative editing. It's the **Assistant Editor and Deliverables Manager.**

**Plugin Ecosystem Expansion (from Gemini follow-up):**

| Tool | Type | Priority | What It Unlocks |
|------|------|----------|-----------------|
| **Automation Blocks** | UXP Plugin | **High value ($59.99)** | Local HTTP server at `localhost:7741`. Claude sends GET requests to trigger complex, battle-tested timeline operations. Hundreds of pre-built recipes. Only invest if Premiere stays in pipeline. |
| **PySceneDetect** | Python lib | **Install immediately** | Detects scene cuts/fades in compiled video. Outputs CSV of timecodes. Agent executes razor cuts on timeline. 99% accuracy on animation hard cuts. |
| **ffmpeg-python** | Python lib | **Install immediately** | `silencedetect` for auto-trimming VO gaps, `blackdetect` for rendering glitch detection, `ebur128` for pre-export LUFS measurement. |
| **Faster-Whisper** | Python lib | **Install for captions** | 4x faster than OpenAI Whisper, half the VRAM. Generates `.srt` files. Agent imports to timeline via API. Styling gotcha: imported captions use default Arial — must manually apply Track Style. |
| **ffmpeg-normalize** | Python CLI | **Install immediately** | Batch normalize audio to -24 LUFS festival standard BEFORE importing to timeline. Solves the biggest Premiere API gap (Essential Sound). `pip install ffmpeg-normalize`. |
| **OpenTimelineIO (OTIO)** | Python lib | **Key bridge tool** | Pixar's interchange format. Export from Premiere → import to DaVinci Resolve for color/audio finishing. Adobe natively supports OTIO. |
| **pymiere** | Reference | **Read source code** | Python wrapper for Premiere ExtendScript. Study `wrappers.py` to understand Python-to-ExtendScript translation patterns. |
| **BeatEdit** | Plugin | **Manual + Agent hybrid** | Analyzes music → generates Premiere markers on beats. Manual "Analyze" click required, but agent can then read markers and snap clips to them. |

**What's confirmed NOT scriptable (no plugin can fix these):**
- Lumetri color wheels / color grading
- Essential Sound panel / audio effects / VSTs / Audio Track Mixer
- Native Speech-to-Text captions
- Dynamic Link to After Effects
- Auto-captioning

**AutoPod insight:** Adobe engineers confirmed AutoPod uses standard `trackItems` ExtendScript API. This proves that if Python MCP externally detects silence (FFmpeg), the agent CAN replicate jump-cut features for The Block social content.

---

### New Entrant: DaVinci Resolve — The Premiere Killer for Creative Automation
**Automation depth: ~80%** of creative + deliverables (with Studio version).

DaVinci Resolve's Python 3 API natively exposes everything Premiere locks away. Color nodes, Fairlight audio EQ/mixing, render queue, Fusion compositing, timeline manipulation, media management — all scriptable. With the `execute_python()` tool, Claude can run arbitrary Python code inside Resolve, making it equivalent to AE's ExtendScript power level.

**Important constraint:** Full scripting API requires **DaVinci Resolve Studio** (~$295 one-time). The free version has restricted scripting capabilities. Sean currently has the free version — MCP servers may work with limited functionality. Plan to invest in Studio once the full ecosystem understanding is in place.

**MCP Server Ecosystem (3 options):**

| Server | Stars | Strengths | Best For |
|--------|-------|-----------|----------|
| **apvlv/davinci-resolve-mcp** | ~37 | Most documented. Project mgmt, timeline, media, Fusion, `execute_python()`, `execute_lua()` | Starting point — broadest community |
| **Positronikal/davinci-mcp-professional** | — | Enterprise fork of samuelgursky's. DXT one-click install. Claims "full functionality" through v20. | Easiest install when ready |
| **Tooflex/davinci-resolve-mcp** | — | Gallery management, track control, audio adjustments, playback, project export/import. | Most audio/color features |

**What Resolve scripts that Premiere can't:**
- Color node manipulation (programmatic color grading)
- Fairlight audio EQ and mixing
- Render queue with full parameter control
- Fusion compositions (node-based compositing/VFX)
- Arbitrary Python code execution inside the application

**Current role:** Exploration and learning. Play with free version + MCP server to understand capabilities. When budget allows, invest in Studio for full pipeline integration.

---

### New Entrant: ButterCut — Editorial Intelligence Layer
**What it is:** A Claude Code skills package + Ruby library that handles the *editorial decision-making* layer that no MCP server addresses.

**Architecture:** WhisperX (word-level transcription) + frame analysis (visual content) + Claude (editorial decisions) → XML export (FCPXML/xmeml) → import into Final Cut, Premiere, OR DaVinci Resolve.

**The workflow:**
1. Point at footage folder → ButterCut builds a "library" (transcribes audio, analyzes frames, generates visual transcripts)
2. Tell Claude what you want ("just the meetup coverage, 3-5 minutes, conversational pacing")
3. Claude makes editorial decisions (clip selection, ordering, pacing, narrative structure)
4. Export timeline XML to your NLE of choice

**Why this matters:** ButterCut handles the cognitive work — deciding *which* clips, *how* to structure them, *what* pacing to apply. MCP servers handle mechanical execution. These are complementary, not competing.

**Best use cases for Sean:**
- The Block social video rough cuts from raw footage
- Interview/podcast editing
- Transcript-based editorial assembly
- Any footage-based editing where Claude can analyze content and make selections

**Limitation:** Designed for footage-based editing. Animated shorts don't have "footage to select from" — they have AE renders that need assembly. ButterCut is strongest for The Block content, not the animation pipeline.

**Dependencies:** Ruby, Python, FFmpeg, WhisperX. Claude Code auto-installs missing pieces.

---

## 2. Cross-App Patterns — What Connects Everything

### Pattern 1: The ES3/Ancient JavaScript Constraint (AE + Illustrator)
Both use ExtendScript stuck in ECMAScript 3 (1999). No `let`/`const`, no arrow functions, template literals, destructuring, or modern array methods. Creative Director skill MUST include: *"When generating ExtendScript for AE or Illustrator, write strictly in ES3-compliant JavaScript using var."*

**Mitigation:** Install extendscript-es5-shim (AE) and JSON2.js (Illustrator) to add `.map()`, `.filter()`, `.forEach()`, `JSON.parse()`, `JSON.stringify()`. Photoshop and Premiere use UXP (modern JS) — this constraint is app-specific.

### Pattern 2: The "Blind Agent" Problem (All Apps)
The AI agent manipulates data/math, not pixels. It can't see what it's doing. Solutions by app:
- **Photoshop:** Canvas screenshot → Claude Vision inspection (verified in adb-mcp)
- **After Effects:** Render preview → media-utils-mcp frame extraction → Claude Vision
- **Illustrator:** Export temp PNG → Claude Vision
- **Premiere:** media-utils-mcp `generateImagesFromVideos` for frame sampling
- **DaVinci Resolve:** Render preview → extract frame → Claude Vision (same pattern)

Pipeline should always include a **vision verification checkpoint** after generative or layout operations.

### Pattern 3: Single-Threaded UI Blocking (All Apps)
All apps freeze during heavy scripted operations. Mitigation:
- Keep commands lightweight and batched
- Do heavy processing in Python/Node.js, send only final execution commands
- **AE:** Wrap in `beginUndoGroup()`/`endUndoGroup()`
- **Illustrator:** Bundle into single `evalScript()` payload (whole payload = one undo). Use `$.gc()` for garbage collection in loops.
- **PS:** Use `executeAsModal` to batch into single undo states
- **Premiere:** Keep timeline loops under ~500 clips

### Pattern 4: The "Actions Workaround" for AI Features
- **Photoshop + Nano Banana Pro:** VERIFIED working. Production-ready generative AI path. But ComfyUI API is now the recommended primary (cleaner pipeline, local generation on RTX 5080).
- **Illustrator + Firefly:** Poor reliability. Async cloud + synchronous ExtendScript = timeouts. NOT recommended. Route to Recraft API or vTracer instead.

### Pattern 5: The "Offload Everything" Architecture
Gemini's strongest recurring thesis across all four follow-up analyses: **treat Adobe apps as dumb renderers/assemblers/exporters.** Do all heavy computation, generation, analysis, and processing in Python/Node.js/CLI tools. Send only final placement and export commands to the apps.

This applies to:
- Vector generation → External API (Recraft, vTracer), not Illustrator Firefly
- Sprite generation → ComfyUI API, not Photoshop Nano Banana (primary)
- Audio normalization → ffmpeg-normalize, not Premiere Essential Sound
- Color enforcement → ImageMagick/Python, not Photoshop Gradient Map
- Boolean geometry → Python Shapely, not Illustrator Pathfinder
- Scene detection → PySceneDetect, not manual scrubbing
- Subtitle generation → Faster-Whisper, not Premiere Speech-to-Text
- Export matrix → FFmpeg, not Adobe Media Encoder

### Pattern 6: The Cross-App Pipeline Architecture
**Design in Illustrator → Composite in Photoshop → Animate in After Effects → Edit in Premiere/Resolve**

Handoff points:
- AI → PS: Export SVG/PNG from Illustrator, import into Photoshop
- PS → AE: Save PSD with layers, import into AE (layers preserved)
- AE → PR/Resolve: Render to ProRes/PNG sequence (NOT Dynamic Link — unscriptable)
- PR → Resolve: Export OTIO/XML for color/audio finishing
- Cross-check: media-utils-mcp validates every render between stages

**AI → AE direct (without Overlord):** Run ExtendScript to save specific Illustrator layers as `.ai` file → AE `app.project.importFile()` → execute "Create Shapes from Vector Layer" (Command ID `3973`). Document this exact command ID in cross-app workflows skill.

---

## 3. Reality Checks — Where Gemini Might Be Optimistic

### ComfyUI API as Primary Generator (PS Analysis)
Gemini recommends ComfyUI over Nano Banana Pro as primary. This is architecturally sound, but ComfyUI + IP-Adapter + ControlNet OpenPose is a complex setup. Test a basic ComfyUI API call from Python first before building the full pipeline. If ComfyUI proves unreliable or too complex to configure, Nano Banana Pro via Actions remains a viable fallback.

### Recraft V3 SVG Quality (Illustrator Analysis)
Gemini calls Recraft the "holy grail." The claim is it generates clean, mathematical SVG vectors. Verify with 10 test generations using game-asset-specific prompts. Check: Are paths clean? Colors accurate? Anchor points snap to integers? Under 100 anchor points per icon is good, over 500 is a problem.

### Automation Blocks HTTP API (Premiere Analysis)
The localhost:7741 HTTP server claim needs verification — confirm this is current and stable before building workflows around it. At $59.99, it's only worth investing if Premiere stays as your primary assembly tool (vs. shifting to Resolve).

### DaVinci Resolve Free Version Scripting
The MCP servers are built for Resolve Studio. The free version may have restricted API access. Test basic connectivity with the free version before assuming full functionality.

### After Effects Expression Writing
Claude *can* write expressions, but quality varies. Simple expressions (wiggle, loop, time-based) are reliable. Complex physics or IK rigs need iteration. Use DuAEF Expression Library as a reference bank instead of Claude inventing from scratch.

### Premiere Pro MOGRT Updates
`getMGTComponent()` is "notoriously buggy and async-heavy." Don't build critical workflows around dynamic MOGRT text updates without extensive testing.

---

## 4. Improving adb-mcp — What's Realistic for a Beginner Coder

### Realistic for You (Python/JS modifications to existing code)

**Add missing ExtendScript commands to AE/Illustrator MCP servers:**
Adding a new command means: (1) Write the ExtendScript (Claude Code can generate it), (2) Add tool definition in Python MCP server, (3) Wire through proxy. Copy-paste-and-modify on existing patterns.

Good candidates:
- AE: `beginUndoGroup`/`endUndoGroup` wrapper (safety critical, #1 priority)
- AE: Render queue automation commands
- AE: Expression application tools
- Illustrator: Batch artboard export with custom naming
- Illustrator: Color palette enforcement (sweep all paths, snap to legal colors)

**Add Python pipeline tools to MCP server:**
These don't touch Adobe APIs at all — pure Python processing:
- Pyxelate pixel art conversion
- ImageMagick palette enforcement via subprocess
- OpenCV bounding box shimmer detection
- ffmpeg-normalize audio preprocessing
- PySceneDetect scene boundary detection
- vTracer raster-to-vector conversion

**Add media-utils-mcp pre-flight checks:**
Pure Python + ffprobe. Add custom validation rules (e.g., "reject any file not matching 24.00fps and ProRes 422").

**Improve error handling in proxy:**
Timeout extensions for long operations (Nano Banana generations) — straightforward config change.

### Needs Expertise (Defer)

- Expanding Premiere Pro's UXP DOM surface (Adobe limitation)
- Making Illustrator's AI features scriptable (Adobe deliberately blocks)
- Building custom UXP panels with deep batchPlay integration
- Fixing WebSocket payload size limits for large data transfers

### The Gemini-as-Architect, Claude-as-Builder Pattern
Use Gemini 3.0 Deep Think to: (1) Design ExtendScript logic, (2) Specify MCP tool structure, (3) Identify edge cases. Then use Claude Code to: (1) Write and test code, (2) Modify MCP server files, (3) Debug against running Adobe apps. Division of labor: Gemini has deep context from notebooks, Claude Code iterates rapidly with actual codebase.

---

## 5. Creative Director Skill Enhancement Plan

### Capability-Aware Routing Table

| Task Type | Primary App | Why | Fallback |
|-----------|-------------|-----|----------|
| Sprite generation/consistency | ComfyUI API (primary) | Local generation on RTX 5080, cleaner pipeline | Photoshop (Nano Banana via Actions) |
| Sprite sheet assembly/packing | TexturePacker CLI | Headless, Phaser 3 format native | After Effects OR Photoshop |
| Sprite post-processing | Python (Pyxelate + ImageMagick + OpenCV) | External tools, no Adobe dependency | Photoshop batchPlay |
| Vector UI/icons/logos | Illustrator | Native vector DOM, math precision | Recraft API → SVGO → Illustrator |
| Vector generation (AI) | Recraft API (quality) or vTracer (free) | Illustrator Firefly is unscriptable | External API always |
| Character model sheets | Illustrator (structure) + Human (drawing) | Agent builds guides, human draws | — |
| 2D animation rigging | After Effects | Expressions + parenting + keyframes | Duik API (if verified) |
| Motion graphics | After Effects | Full keyframe/expression control | — |
| Video editing (creative) | Premiere Pro (HUMAN) | API too shallow for creative decisions | DaVinci Resolve (when Studio acquired) |
| Video assembly/rough cut | Premiere Pro (AGENT) or ButterCut | Timeline placement + clip sequencing | ButterCut for footage-based |
| Editorial intelligence | ButterCut | Transcript analysis, clip selection, pacing | Manual selection |
| Festival exports | FFmpeg Master-to-Matrix | 100% stable CLI, better than AME presets | Premiere `encodeSequence()` |
| Pre-flight validation | media-utils-mcp | External tool, no app dependency | — |
| Color grading | Premiere Pro (HUMAN) today | Lumetri unscriptable | DaVinci Resolve (when Studio acquired) |
| Audio mixing/normalization | ffmpeg-normalize (pre-import) | Normalizes to -24 LUFS before timeline | DaVinci Resolve Fairlight (when Studio acquired) |
| Subtitle generation | Faster-Whisper → SRT import | Premiere Speech-to-Text unscriptable | — |
| Scene detection | PySceneDetect | 99% accuracy on animation hard cuts | — |
| Generative AI (vector) | External API → Illustrator place() | All Illustrator AI features unscriptable | — |
| Palette enforcement | ImageMagick (primary) or Illustrator sweep | Mathematical color snapping | Photoshop Gradient Map |
| Boolean geometry (vector) | Python Shapely → Illustrator | Avoids GUI race conditions | — |

### Limitation Awareness
The skill should never promise what the MCP can't deliver:

1. Never suggest Lumetri color grading via script — flag as manual (or route to Resolve when available)
2. Never suggest Essential Sound automation — use ffmpeg-normalize pre-import instead
3. Never suggest Dynamic Link between AE and Premiere — use hard renders
4. Never suggest Illustrator AI features as automatable — use external API workaround
5. Never use Illustrator's native Live Trace — route to vTracer or Vectorizer.ai
6. Never use Illustrator Pathfinder via executeMenuCommand — route to Python Shapely
7. Always include vision verification checkpoints after generative operations
8. Always specify ES3 constraints when planning AE/Illustrator scripts
9. Always run SVGO on AI-generated SVGs before Illustrator import
10. Always normalize audio via ffmpeg-normalize BEFORE importing to any timeline

### Enhanced Handoff Protocol
When the Creative Director hands off to an execution skill, the handoff document includes:

1. Which app handles this task (from routing table)
2. What the MCP can vs. can't do for this specific task
3. Where human intervention is required
4. What verification method to use (canvas screenshot, frame extraction, media probe)
5. What file format to use at each handoff point
6. Estimated execution time (15-45 sec generative, near-instant deterministic)
7. What Python preprocessing is needed before the app sees the file
8. What external tools run between app handoffs

---

## 6. Revised 16BitFit Sprite Pipeline

### Old Approach
Photoshop does everything (generation + post-processing + packing).

### New Approach — Specialized Tools for Each Phase

| Step | Tool | What It Does | Adobe Involved? |
|------|------|-------------|-----------------|
| 1 | **Claude Code** (Python MCP) | Orchestration, coordinates all steps | No |
| 2 | **Photoshop UXP** | Grid setup, skeleton import, final assembly | Yes |
| 3 | **ComfyUI REST API** | IP-Adapter + ControlNet OpenPose sprite generation on RTX 5080 | No |
| 4 | **Pyxelate** (Python) | Clean pixel art downscaling (Bayesian model) | No |
| 5 | **ImageMagick CLI** | Strict 4-color Game Boy palette enforcement | No |
| 6 | **OpenCV/NumPy** (Python) | Bounding box shimmer detection (mathematical) | No |
| 7 | **TexturePacker CLI** | Phaser 3 atlas packing with JSON metadata | No |

Steps 3-7 run in Python with no PS involvement until final assembly. Architecturally cleaner than routing through UXP.

### The Critical Test (Changed)
~~Step 3 of old pipeline (Nano Banana Actions) was the bottleneck.~~
**New critical test:** Build ComfyUI API workflow with IP-Adapter + ControlNet OpenPose and test from Python script. If this produces consistent sprites across 16 frames, the full revised pipeline is viable. If not, fall back to Nano Banana Pro Actions approach.

### The Indexed Color Trap (Still Applies)
Gen AI features do NOT work in Indexed Color mode. Pipeline must do ALL generative work in RGB, apply color crunch (ImageMagick or Gradient Map) as the absolute final step before export.

---

## 7. Animated Shorts Pipeline — The Hybrid Architecture

### For Production (Current Setup — Free Resolve)

1. **After Effects** (via adb-mcp) → Render individual scenes/shots as ProRes or PNG sequences
2. **PySceneDetect** (Python) → Auto-detect scene boundaries if rendering long masters
3. **ffmpeg-normalize** (Python) → Batch normalize all audio to -24 LUFS
4. **Faster-Whisper** (Python) → Generate SRT subtitles if needed
5. **Premiere Pro** (via adb-mcp) → Rough assembly, clip ordering, MOGRT application, SRT import
6. **Premiere Pro** (HUMAN) → Color grading (Lumetri), audio mixing (Essential Sound), creative polish
7. **FFmpeg Master-to-Matrix** (Python) → One ProRes master export → spawn all festival/social variants

### For Production (Future — Resolve Studio)

1. **After Effects** (via adb-mcp) → Render individual scenes/shots
2. **PySceneDetect** (Python) → Scene boundary detection
3. **ffmpeg-normalize** (Python) → Audio normalization
4. **Faster-Whisper** (Python) → Subtitle generation
5. **Premiere Pro** OR **ButterCut** → Rough assembly and clip ordering
6. **OTIO export** → Bridge to DaVinci Resolve
7. **DaVinci Resolve** (via MCP) → Color grading (scriptable nodes), audio mixing (Fairlight), Fusion compositing
8. **Resolve render** OR **FFmpeg Master-to-Matrix** → Final deliverables

### For The Block Social Content

1. **ButterCut** → Analyze footage, build rough cut from transcripts, export XML
2. **Premiere Pro** → Import XML, apply MOGRTs, refine
3. **FFmpeg** → Export variants for each platform (9:16 TikTok, 1080p YouTube, etc.)

---

## 8. The FFmpeg Power Tools — NLE-Agnostic, Build Now

These Python/CLI tools work regardless of which NLE you use. High ROI, zero Adobe API risk.

### Master-to-Matrix Exporter (Impact: 10/10, Feasibility: 10/10)
Export one ProRes 422 HQ master from any NLE. Python/FFmpeg spawns all variants in parallel:
- Crop 9:16 for TikTok/Reels
- Scale to 1080p for festival submission
- Apply strict bitrate limit for FilmFreeway
- Burn in Whisper-generated subtitles headlessly

FFmpeg's `libx264` encoder is often superior to AME's H.264 at low bitrates, and 100% stable via CLI.

### Pre-Mix Audio Normalizer (Impact: 9/10, Feasibility: 10/10)
Audio rejection is the #1 festival QC failure. `ffmpeg-normalize` batch-normalizes dialogue and SFX WAVs to exactly -24 LUFS BEFORE import to any timeline. Solves the biggest Premiere API gap.

### Pre-Flight QC Suite (Impact: 8/10, Feasibility: 10/10)
- `silencedetect` → Find gaps in voiceover for auto-trimming
- `blackdetect` → Catch 1-frame rendering glitches from AE
- `ebur128` → Measure exact LUFS of final mix before festival export
- PySceneDetect → CSV of timecodes for automated scene splitting

### Audio Pipeline (slhck/ffmpeg-normalize)
1.8k+ stars. The best Python wrapper for LUFS normalization. Install: `pip install ffmpeg-normalize`.

---

## 9. What's Missing — Gaps to Fill

1. **ComfyUI → Photoshop integration testing.** The architectural shift to ComfyUI as primary generator is the biggest change from v1. Needs hands-on validation before committing the pipeline.

2. **DaVinci Resolve free version API limitations.** Unknown what exactly is restricted. Test with the MCP server to discover boundaries before planning Resolve-dependent workflows.

3. **ButterCut skill integration with Code-Brain.** ButterCut has its own Claude Code skills. Evaluate whether to use them standalone or port patterns into your creative-studio domain.

4. **Error recovery and checkpointing.** What happens when step 3 fails on frame 7 of 16? Pipeline needs state saving after each successful frame for resume-on-failure.

5. **Version control for generated assets.** Output folder structure with version numbering for comparing sprite sheet iterations.

6. **Adobe Character Animator.** Listed as a current tool, part of 2D animation workflow, but has no MCP support and wasn't covered by Gemini. Gap in the automation story.

7. **Cost analysis of external APIs.** Recraft (~$0.08/call), Vectorizer.ai ($9.99/mo), Automation Blocks ($59.99 one-time). For batch operations, these add up. Factor into financial picture.

8. **FilmFreeway has no public API.** Must manually maintain `festivals.json` spec sheet for Claude to read festival export requirements.

9. **Faster-Whisper caption styling.** SRT import uses default Arial. Manual Track Style application required. No workaround exists.

---

## 10. Recommended Next Steps (Prioritized)

### Immediate (This Week)
1. **Build ComfyUI API workflow** — IP-Adapter + ControlNet OpenPose, test from Python script on Alienware RTX 5080. This is now the critical test for the sprite pipeline.
2. **Install AE foundations** — extendscript-es5-shim, aequery, set up aerender CLI
3. **Install PS foundations** — Alchemist for batchPlay discovery
4. **Install Illustrator foundations** — JSON2.js (mandatory for all scripts)
5. **Install Python pipeline tools** — `pip install pyxelate vtracer ffmpeg-normalize ffmpeg-python pyscenedetect`
6. **Clone ButterCut** — `git clone https://github.com/barefootford/buttercut.git` and review skills structure
7. **Update creative-director.md** — Add routing table and limitation rules from Section 5

### Short-Term (Next 2 Weeks)
8. **Add beginUndoGroup wrapper** to AE MCP server (safety critical, #1 adb-mcp improvement)
9. **Add ES3 constraint** to both AE and Illustrator skill files
10. **Build FFmpeg Master-to-Matrix exporter** — NLE-agnostic, immediately useful
11. **Install ffmpeg-normalize** and test on short film audio files
12. **Test DaVinci Resolve free version** with apvlv/davinci-resolve-mcp — discover API boundaries
13. **Test Recraft V3** — 10 game-asset prompts, evaluate SVG quality
14. **Build Pyxelate + ImageMagick + OpenCV pipeline** in Python MCP server
15. **Update adobe-cross-app-workflows.md** — Add verified handoff formats, OTIO bridge, and all new tool integrations

### Medium-Term (Weeks 3-4)
16. **Build full revised sprite pipeline** (if ComfyUI test passes) or Nano Banana fallback
17. **Expand AE MCP commands** using Gemini-as-Architect, Claude-as-Builder pattern
18. **Create Pipeline Test Suite** — Simple test operations for each app verifying MCP connection
19. **Evaluate ButterCut integration** — Use standalone or port patterns into Code-Brain
20. **Add SVGO to Node.js proxy** as automatic SVG preprocessing step

### Decision Points
- **After ComfyUI test:** ComfyUI primary or Nano Banana Pro primary for sprite generation?
- **After Resolve free test:** How much capability do you actually get? Is Studio investment justified now or defer?
- **After Recraft test:** Recraft API or vTracer for vector generation pipeline?
- **After Automation Blocks evaluation:** Worth $59.99 if Premiere stays in pipeline, or is Resolve replacing it?

---

## 11. GitHub Repos — Master Reference

### After Effects
| Repo | Stars | Purpose |
|------|-------|---------|
| ExtendScript/extendscript-es5-shim | — | ES5 polyfill for AE ExtendScript |
| docsforadobe/aequery | — | jQuery for AE DOM |
| RxLaboratory/Duik | — | Scriptable IK rigging API |
| google/AEUX | — | JSON → Shape Layer builder |
| RxLaboratory/DuAEF_ExpressionLib | — | Battle-tested expression reference |
| inlife/nexrender | — | Data-driven batch rendering |
| Dakkshin/after-effects-mcp | — | Alternative AE MCP server |

### Photoshop
| Repo | Stars | Purpose |
|------|-------|---------|
| jardicc/alchemist | — | batchPlay JSON inspector |
| sedthh/pyxelate | — | Python pixel art converter |
| AbdullahAlfaraj/Auto-Photoshop-StableDiffusion-Plugin | 7.2k | SD bridge (verify if needed) |
| loonghao/photoshop-python-api-mcp-server | — | Windows COM alternative |

### Illustrator
| Repo | Stars | Purpose |
|------|-------|---------|
| creold/illustrator-scripts | 1k+ | Definitive ExtendScript reference (2025/2026) |
| visioncortex/vtracer | 5.5k | Rust/Python raster-to-vector |
| joshbduncan/AiCommandPalette | — | Undocumented executeMenuCommand dictionary |
| david-t-martel/adobe-mcp | — | Alternative Illustrator MCP |
| krVatsal/illustrator-mcp | — | Windows COM alternative |

### Premiere Pro / Video
| Repo | Stars | Purpose |
|------|-------|---------|
| SYSTRAN/faster-whisper | — | Optimized Whisper for subtitle generation |
| Breakthrough/PySceneDetect | — | Scene cut detection |
| kkroening/ffmpeg-python | — | FFmpeg filters in Python |
| slhck/ffmpeg-normalize | 1.8k | LUFS audio normalization |
| qmasingarbe/pymiere | 250+ | Python Premiere wrapper (study source) |
| AcademySoftwareFoundation/OpenTimelineIO | — | Pixar's editorial interchange format |
| BigUncle/Fast-Whisper-MCP-Server | — | Ready-made Whisper MCP server |
| barefootford/buttercut | 51 | Claude Code video editing skills + Ruby XML library |

### DaVinci Resolve
| Repo | Stars | Purpose |
|------|-------|---------|
| apvlv/davinci-resolve-mcp | 37 | Primary MCP server — broadest coverage |
| Positronikal/davinci-mcp-professional | — | Enterprise fork, DXT install |
| Tooflex/davinci-resolve-mcp | — | Most audio/color features |

### Core Infrastructure
| Repo | Stars | Purpose |
|------|-------|---------|
| mikechambers/adb-mcp | — | Base Adobe MCP server (PS, PR, AE, AI) |

---

*This document lives in Obsidian Vault at `Projects/Adobe-MCP/unified-synthesis-v2.md` and should be imported as a source into the Integration Hub NotebookLM notebook. Update as tools are tested and pipeline decisions are made.*
