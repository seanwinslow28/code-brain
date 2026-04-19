# Claude Code Kickoff Prompt: Phase 0 — Pixel Quantizer Prototype

**Instructions:** Copy everything below the line into Claude Code as your first message. Before pasting, make sure you have these files accessible in your project directory (or adjust paths accordingly).

---

## PASTE THIS INTO CLAUDE CODE ↓

You are building Phase 0 of the **16BitFit Battle Mode Hybrid Sprite Pipeline** — a standalone Pixel Quantizer prototype that converts high-resolution video frames into clean, palette-locked pixel art suitable for a Street Fighter II-style 2D fighting game.

**This is a GATE CHECK.** If this quantizer can't produce acceptable pixel art from video-like input, the entire hybrid keyframe-to-video pipeline approach is dead. Build it right, build it testable.

---

### Project Context

I'm building a manifest-driven CLI pipeline (Node.js + TypeScript + Oclif) that generates sprite sheet animations for a 2D fighting game using AI. The existing pipeline generates single frames well using Gemini 3 Pro Image, but fails at multi-frame animations (walk cycles) because text prompts can't reliably differentiate left vs. right leg positions across sequential frames.

The proposed solution: generate keyframes with the proven image model, interpolate motion between them with a video model (Pika, Kling, Veo), then **convert the video output back to pixel art**. This quantizer is that conversion step.

**The full architecture docs are at:** `hybrid-pipeline-plan.md`, `architecture.md`, and `project-context.md` in the project root. Read these before writing any code.

---

### What to Build

A standalone Node.js script called `pixel-quantizer.ts` (plus supporting modules) that does NOT integrate into the pipeline yet. It runs independently from the command line.

**Input:** A directory of PNG frames (simulating extracted video frames) at high resolution (e.g., 512×512 or 1080×1080)  
**Output:** A directory of processed PNG frames at 128×128, palette-locked, with clean transparency

### Processing Pipeline (7 steps, in order)

Each step should be its own function so we can test/skip/swap steps independently:

1. **Nearest-Neighbor Downscale**
   - Tool: Sharp
   - Resize input frames to 128×128 using `kernel: sharp.kernel.nearest`
   - Why nearest-neighbor: Standard resize (bilinear/bicubic) creates anti-aliased colors that don't exist in pixel art. Nearest-neighbor preserves hard pixel edges.

2. **Palette Quantization**
   - Tool: Custom Sharp raw pixel buffer manipulation
   - Read each pixel's RGB values from the raw buffer
   - Snap every pixel to the nearest color in a provided palette LUT using Euclidean distance in RGB space: `sqrt((r1-r2)² + (g1-g2)² + (b1-b2)²)`
   - Do NOT use Sharp's built-in `palette` option — it picks its own colors via median-cut. We need to force-snap to a specific predetermined palette.

3. **Temporal Smoothing**
   - Tool: Custom logic comparing frames in sequence
   - For each pixel position, look across all frames in the sequence
   - If a pixel barely changes (RGB distance < threshold, default 15), lock it to the **mode color** (most common value) across all frames
   - This eliminates sub-pixel jitter in areas that should be static (torso, head during walk)
   - Parameters: `staticThreshold` (default: 15), `modeColorWindow` (default: "all" frames)

4. **Outline Enforcement**
   - Detect sprite edges (pixels adjacent to transparent pixels)
   - Detect internal color boundaries (adjacent pixels with very different palette colors)
   - Apply `#272929` outline color at those edges (2-3px weight)
   - This re-applies the bold outlines that video models soften during interpolation

5. **Alpha Recovery**
   - Support two modes (configurable):
     - **Chroma key mode:** Remove `#00FF00` background via color-distance threshold, then clean edges
     - **Auto-detect mode:** Find the dominant background color, remove it
   - Alpha edge cleanup: pixels with alpha < 128 → fully transparent (0), alpha ≥ 128 → fully opaque (255)
   - No semi-transparent pixels allowed in final output

6. **Baseline Registration**
   - Detect the bottom edge of the sprite (lowest non-transparent pixel row) in each frame
   - Calculate the target baseline (mode of all bottom edges, or configurable)
   - Shift sprites vertically within the 128×128 canvas so feet align to a consistent baseline
   - Log drift values per frame

7. **Validation Report**
   - After processing, generate a JSON report for each frame:
     - Dimensions (should be exactly 128×128)
     - Off-palette pixel count (should be 0)
     - Outline coverage percentage
     - Background transparency completeness
     - Baseline position
     - Processing time
   - Generate a summary report for the full sequence:
     - Total frames processed
     - Pass/fail per frame against criteria
     - Temporal jitter score (how much variance exists in static regions after smoothing)

---

### Character Palette (Sean — test character)

```typescript
const SEAN_PALETTE: string[] = [
  '#F5D6C6',  // Skin — light peach
  '#C2A769',  // Hair — dirty blonde
  '#4682B4',  // Eyes — steel blue
  '#F2F0EF',  // Tank top — off white
  '#2323FF',  // Pants — neon blue
  '#F5F5F5',  // Shoes — white
  '#272929',  // Outlines — bold dark
  '#000000',  // Pure black (shadows)
  '#FFFFFF',  // Pure white (highlights)
  // Shading variants:
  '#D4B5A5',  // Skin shadow
  '#B89A58',  // Hair shadow
  '#3A6B94',  // Eyes shadow
  '#D4D2D0',  // Tank top shadow
  '#1A1ABF',  // Pants shadow
  '#D4D4D4',  // Shoes shadow
  '#00FF00',  // Chroma key green (background — will be removed)
];
```

---

### CLI Interface

The script should be runnable like this:

```bash
# Basic usage
npx ts-node src/tools/pixel-quantizer.ts \
  --input ./test-frames/input/ \
  --output ./test-frames/output/ \
  --palette sean \
  --target-size 128

# With options
npx ts-node src/tools/pixel-quantizer.ts \
  --input ./test-frames/input/ \
  --output ./test-frames/output/ \
  --palette sean \
  --target-size 128 \
  --background-mode chroma \
  --chroma-color "#00FF00" \
  --outline-weight 2 \
  --static-threshold 15 \
  --skip-temporal \
  --verbose
```

**Flags:**
- `--input` (required): Directory of input PNG frames
- `--output` (required): Directory for processed output
- `--palette` (required): Palette name (loads from a palettes config file) or path to a JSON palette file
- `--target-size` (default: 128): Output frame dimensions (square)
- `--background-mode` (default: "chroma"): "chroma" or "auto"
- `--chroma-color` (default: "#00FF00"): Chroma key color
- `--outline-weight` (default: 2): Outline thickness in pixels
- `--outline-color` (default: "#272929"): Outline color
- `--static-threshold` (default: 15): RGB distance threshold for temporal smoothing
- `--skip-temporal`: Skip temporal smoothing (useful for single-frame testing)
- `--skip-outline`: Skip outline enforcement
- `--verbose`: Detailed per-step logging

---

### Project Structure

Place files like this (creating directories as needed):

```
src/
  tools/
    pixel-quantizer.ts          ← CLI entry point (argument parsing, orchestration)
    quantizer/
      index.ts                  ← Main pipeline function
      steps/
        downscale.ts            ← Step 1
        palette-quantize.ts     ← Step 2
        temporal-smooth.ts      ← Step 3
        outline-enforce.ts      ← Step 4
        alpha-recover.ts        ← Step 5
        baseline-register.ts    ← Step 6
        validate.ts             ← Step 7 (report generation)
      palettes/
        sean.json               ← Sean's palette LUT
        index.ts                ← Palette loader
      types.ts                  ← Shared types (QuantizerConfig, FrameReport, etc.)
test/
  tools/
    quantizer/
      palette-quantize.test.ts  ← Unit tests for palette snapping
      temporal-smooth.test.ts   ← Unit tests for temporal smoothing
      integration.test.ts       ← Full pipeline integration test
```

---

### Dependencies

Use only packages already in the project stack (or standard additions):

- **Sharp** — image processing (already in stack)
- **Execa** — subprocess execution for ffmpeg if needed (already in stack)
- **yargs** or **commander** — CLI arg parsing for this standalone tool (lightweight, not Oclif since this isn't a pipeline command yet)
- **Pino** — logging (already in stack)

Do NOT add Python, OpenCV, or any non-Node.js dependencies.

---

### Test Data Generation

Before testing with real video output, create synthetic test input:

**Experiment Q-01: Control test (upscaled pixel art)**
1. Find or create a small pixel art sprite (128×128)
2. Upscale it to 512×512 using nearest-neighbor (Sharp)
3. Run it through the quantizer
4. Output should be identical (or nearly identical) to the original
5. This validates the pipeline doesn't destroy clean input

**Experiment Q-02: Anti-aliased input**
1. Take the same pixel art sprite
2. Upscale to 512×512 using bilinear interpolation (adds anti-aliasing)
3. Run through quantizer
4. Output should still be clean pixel art (tests palette snapping on smooth gradients)

**Experiment Q-03: Color-drifted input**
1. Take the upscaled sprite from Q-02
2. Shift all colors by random ±10-20 in each RGB channel (simulates video model color drift)
3. Run through quantizer
4. Output should snap back to correct palette colors

**Experiment Q-04: Simulated video sequence**
1. Create 4-8 slightly different frames (manually shift sprite 1-2px per frame, add slight wobble)
2. Add anti-aliasing and color drift to all frames
3. Run the full pipeline including temporal smoothing
4. Output should have smooth, consistent sprites without jitter

Write a script `src/tools/generate-test-data.ts` that creates these test inputs automatically from a single source sprite PNG.

---

### Success Criteria (Gate Check)

The quantizer passes Phase 0 if:

- [ ] Output frames are exactly 128×128 pixels
- [ ] Every pixel maps to a palette color (zero off-palette pixels)
- [ ] Bold outlines (#272929) are visually clean and consistent (2-3px weight)
- [ ] Background is fully transparent (clean alpha, no fringe)
- [ ] Character silhouette is recognizable and not distorted
- [ ] Processing time ≤ 2 seconds per frame
- [ ] Q-01 through Q-04 experiments produce acceptable results to human review

---

### What Happens If It Fails

If experiments fail, try these in order:

1. **Try 2× resolution:** Generate at 256×256 target instead of 128×128 — more pixel data to work with
2. **Tune thresholds:** Adjust static threshold, outline detection sensitivity, alpha threshold
3. **Add intermediate step:** Consider a Gemini restyle pass between downscale and palette quantization (documented in `hybrid-pipeline-plan.md` Section 8 as "optional RestyleToPixelSpec")
4. **Narrow scope:** Accept hybrid only for certain animation types
5. **Abandon hybrid:** If nothing works, invest in image-only with enhanced pose references

---

### Code Style Requirements

Follow the project conventions from `project-context.md`:

- TypeScript strict mode
- `kebab-case.ts` for filenames
- `camelCase` for variables and functions
- All functions return typed results
- Pino for logging (structured JSON)
- Each step function should be pure: takes input path(s) + config, returns output path(s) + metrics
- No global state

---

### Your First Task

1. Read `hybrid-pipeline-plan.md` (Sections 4 and 8 especially), `architecture.md`, and `project-context.md`
2. Scaffold the directory structure above
3. Implement the palette quantization step first (Step 2) — it's the core algorithm everything depends on
4. Write the test data generator
5. Run Q-01 to validate the basic pipeline
6. Build remaining steps one by one
7. Run Q-02 through Q-04
8. Generate the validation report

Ask me questions if anything is unclear, but prefer making reasonable assumptions and documenting them over blocking on decisions.
