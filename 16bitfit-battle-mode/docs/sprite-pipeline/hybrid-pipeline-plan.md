# Hybrid Sprite Generation Pipeline — Implementation Plan

**Status:** APPROVED — Ready for Implementation
**Date:** 2026-02-10
**Author:** Sean (synthesized from Perplexity Model Council analysis)
**Relation to Existing Docs:** This document EXTENDS the approved architecture (`architecture.md`) and epics (`epics.md`). It does NOT replace them. The existing pipeline infrastructure (Orchestrator, RetryManager, Auditor, Packer, Validator) remains the foundation. This plan adds a new generation strategy layer and a post-processing pipeline on top of it.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What Changed and Why](#2-what-changed-and-why)
3. [Architecture Update: Generation Strategy Layer](#3-architecture-update-generation-strategy-layer)
4. [Phase 0: Pixel Quantizer Prototype (GATE CHECK)](#4-phase-0-pixel-quantizer-prototype-gate-check)
5. [Phase 1: Video Model Evaluation Sprint](#5-phase-1-video-model-evaluation-sprint)
6. [Phase 2: Hybrid Pipeline End-to-End](#6-phase-2-hybrid-pipeline-end-to-end)
7. [Phase 3: Adapter Layer & Strategy Router](#7-phase-3-adapter-layer--strategy-router)
8. [Post-Processing Pipeline Specification](#8-post-processing-pipeline-specification)
9. [Video Model Landscape (Feb 2026)](#9-video-model-landscape-feb-2026)
10. [Test Matrix & Experiments](#10-test-matrix--experiments)
11. [Manifest Schema Extensions](#11-manifest-schema-extensions)
12. [New Audit Gates for Hybrid Pipeline](#12-new-audit-gates-for-hybrid-pipeline)
13. [Risk Register](#13-risk-register)
14. [Decision Log](#14-decision-log)
15. [Reference Implementations & Resources](#15-reference-implementations--resources)
16. [Glossary of New Terms](#16-glossary-of-new-terms)

---

## 1. Executive Summary

### The Problem

Our proven single-frame generation workflow (Gemini 2.0 Flash / Nano Banana Pro with dual-reference approach) works excellently for static poses but **fails at multi-frame animation sequences** — particularly walk cycles where text descriptions cannot reliably differentiate left vs. right leg positions across sequential frames. This is an inherent limitation of the image-only paradigm, not a prompt engineering problem.

### The Solution

A **Hybrid Keyframe-to-Video Pipeline** that:

1. **Generates keyframes** using our proven image model (Gemini / Nano Banana Pro) — the part that already works
2. **Interpolates motion** between keyframes using video generation models (Kling, Veo, Pika) — solving the temporal coherence problem
3. **Quantizes video output back to pixel art spec** — nearest-neighbor downscale, palette snap, outline enforcement, alpha recovery
4. **Audits, packs, and validates** using the existing pipeline infrastructure — the durable, model-agnostic asset

### The Key Insight

Video models produce "sludge" — frames that move correctly but look wrong for pixel art (anti-aliased, gradient-heavy, wrong palette). Our job is to build a **Pixel Quantizer** that converts this sludge back to clean pixel art. If the quantizer works, the hybrid pipeline is viable. If it doesn't, nothing else matters.

### Source of This Plan

This plan synthesizes findings from a **Perplexity Model Council** session (Feb 10, 2026) that ran the strategic question through Claude Opus 4.6, GPT 5.2, and Gemini 3 Pro simultaneously. All three models independently converged on the hybrid approach as the primary path forward. Key disagreements (noted where relevant) informed the phasing and risk mitigation.

---

## 2. What Changed and Why

### Before (Jan 2026 Architecture)

The approved architecture assumed a single generation strategy: **image-only, frame-by-frame** using the Gemini Generator Adapter. The `GeneratorAdapter` interface had one method:

```typescript
interface GeneratorAdapter {
  generate(ctx: GenerationContext): Promise<Result<GeneratedFrame[], SystemError>>;
}
```

This worked for the MVP scope (1 Champion × 2 moves) but hit the "temporal wall" on walk cycles.

### After (Feb 2026 — This Plan)

The generation layer now supports **three strategies** selected per-animation via the manifest:

| Strategy | When to Use | How It Works |
|----------|-------------|--------------|
| **Image-Only** | Static poses, idle, victory, single-hit attacks — any animation where frames are visually distinct enough for text/pose-reference disambiguation | Existing workflow: anchor + pose reference → Gemini → single frame. Unchanged. |
| **Hybrid Keyframe-to-Video** | Walk cycles, run cycles, complex multi-frame locomotion — any animation requiring smooth temporal coherence and correct limb ordering | Generate keyframes with image model → interpolate with video model → extract frames → quantize to pixel art → audit |
| **Motion Transfer** (experimental) | Standard locomotion animations where a canonical reference video exists | Upload reference walk cycle video + character anchor → video model transfers motion pattern onto character → extract + quantize |

### What Stays the Same

Everything downstream of frame generation is unchanged:

- **Orchestrator** — still manages the state machine
- **RetryManager** — still executes the retry ladder (with new strategy-escalation capability)
- **Auditor** — still evaluates hard gates and soft metrics (with new gates added)
- **PackerAdapter** — still wraps TexturePacker CLI
- **ValidatorAdapter** — still runs Phaser headless micro-tests
- **Manifest schema** — extended, not replaced
- **Artifact folder structure** — extended, not replaced
- **Error taxonomy** — HFxx/SFxx codes still apply, new codes added

---

## 3. Architecture Update: Generation Strategy Layer

### Updated High-Level Data Flow

```
MANIFEST (YAML)
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                   STRATEGY ROUTER                        │
│                                                          │
│  Reads: manifest.generator.strategy                      │
│  Routes to: ImageOnly | HybridKV | MotionTransfer        │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  ImageOnly    │  │  HybridKV    │  │ MotionXfer    │  │
│  │  Strategy     │  │  Strategy    │  │ Strategy      │  │
│  │              │  │              │  │ (experimental) │  │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────┘  │
│         │                 │                   │          │
│         ▼                 ▼                   ▼          │
│  ┌─────────────────────────────────────────────────┐     │
│  │         GENERATOR ADAPTER INTERFACE              │     │
│  │                                                  │     │
│  │  generateFrame(ctx)       → Frame                │     │
│  │  generateKeyframes(ctx)   → Frame[]              │     │
│  │  interpolateFrames(ctx)   → Frame[]              │     │
│  │  generateVideo(ctx)       → Video                │     │
│  │                                                  │     │
│  └─────────────────────────────────────────────────┘     │
│         │          │          │         │                 │
│  ┌──────┴──┐ ┌─────┴────┐ ┌──┴─────┐ ┌┴──────────┐     │
│  │ Gemini  │ │ Kling    │ │ Pika   │ │ Wan 2.5   │     │
│  │ Adapter │ │ Adapter  │ │ Adapter│ │ Adapter   │     │
│  └─────────┘ └──────────┘ └────────┘ └───────────┘     │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              POST-PROCESSING PIPELINE                    │
│  (NEW — only used by Hybrid and MotionTransfer)          │
│                                                          │
│  1. Frame Extraction (ffmpeg)                            │
│  2. Nearest-Neighbor Downscale (128×128 / 256×256)       │
│  3. Palette Quantization (snap to character LUT)         │
│  4. Temporal Smoothing (static region lock)              │
│  5. Outline Enforcement (bold #272929 edges)             │
│  6. Alpha Recovery (background removal + halo cleanup)   │
│  7. Baseline Registration (align feet to baseline)       │
│                                                          │
│  Output: PixelSpecFrames ready for audit                 │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              EXISTING PIPELINE (unchanged)                │
│                                                          │
│  Auditor (HF/SF gates) → RetryManager → Orchestrator     │
│       ↓                                                  │
│  TexturePacker (atlas packing)                           │
│       ↓                                                  │
│  Phaser Headless Validation (engine truth)                │
│       ↓                                                  │
│  Export: atlas.png + atlas.json                           │
└─────────────────────────────────────────────────────────┘
```

### Updated Generator Adapter Interface

The existing single-method interface expands to four atomic operations. Each adapter implements only the methods it supports. Strategy objects compose these operations.

```typescript
// src/domain/interfaces.ts — UPDATED

/**
 * Four atomic generation operations.
 * Each adapter implements only the methods its model supports.
 * Strategy objects compose these into complete workflows.
 */
interface GeneratorAdapter {
  /** Generate a single frame from reference + pose description.
   *  Used by: ImageOnly strategy, keyframe generation in Hybrid.
   *  Supported by: Gemini, FLUX, Retro Diffusion */
  generateFrame(ctx: FrameGenContext): Promise<Result<GeneratedFrame, SystemError>>;

  /** Generate multiple keyframes (batch optimization possible).
   *  Used by: Hybrid strategy to produce anchor frames.
   *  Supported by: Gemini */
  generateKeyframes?(ctx: KeyframeGenContext): Promise<Result<GeneratedFrame[], SystemError>>;

  /** Interpolate motion between two or more anchor frames → produces video.
   *  Used by: Hybrid strategy for motion interpolation.
   *  Supported by: Kling (start/end), Pika (up to 5 keyframes), Veo (first/last) */
  interpolateFrames?(ctx: InterpolationContext): Promise<Result<GeneratedVideo, SystemError>>;

  /** Generate video from a single reference image + motion description.
   *  Used by: MotionTransfer strategy.
   *  Supported by: Kling 2.6 (motion control), Wan 2.5 (I2V) */
  generateVideo?(ctx: VideoGenContext): Promise<Result<GeneratedVideo, SystemError>>;
}

/**
 * Post-processor that converts video model output back to pixel art spec.
 * This is a deterministic pipeline — no AI models involved.
 */
interface PostProcessor {
  /** Extract individual frames from video at specified timestamps or FPS */
  extractFrames(video: GeneratedVideo, config: ExtractionConfig): Promise<Result<RawFrame[], SystemError>>;

  /** Apply the full pixel art quantization pipeline to a single frame */
  quantizeFrame(frame: RawFrame, config: PixelArtConfig): Promise<Result<ProcessedFrame, SystemError>>;

  /** Apply temporal smoothing across a sequence of frames */
  temporalSmooth(frames: ProcessedFrame[], config: TemporalConfig): Promise<Result<ProcessedFrame[], SystemError>>;
}

// --- Supporting Types ---

interface FrameGenContext {
  anchor: ImagePath;              // Character anchor image
  poseRef?: ImagePath;            // Pose reference image (skeleton, sprite sheet, etc.)
  styleRefs: ImagePath[];         // Up to 6 high-fidelity style references
  guide?: ImagePath;              // Grid/baseline guide overlay
  prompt: ResolvedPrompt;         // Fully resolved prompt from template system
  targetSize: { w: number; h: number }; // 128×128 or 256×256
  attemptIndex: number;
}

interface KeyframeGenContext {
  anchor: ImagePath;
  poseRefs: ImagePath[];          // One pose ref per keyframe
  styleRefs: ImagePath[];
  prompts: ResolvedPrompt[];      // One prompt per keyframe
  keyframeIndices: number[];      // Which frame positions these keyframes represent
  targetSize: { w: number; h: number };
}

interface InterpolationContext {
  keyframes: GeneratedFrame[];    // 2-5 keyframe images
  motionPrompt: string;           // Text description of the motion
  duration: number;               // Video duration in seconds
  fps: number;                    // Target frame rate for extraction
  loop: boolean;                  // Whether animation should loop
  creativityScale?: number;       // 0-1, lower = more faithful to keyframes
}

interface VideoGenContext {
  characterRef: ImagePath;        // Character anchor
  motionRef?: VideoPath;          // Reference motion video (for Kling 2.6 motion transfer)
  motionPrompt: string;           // Text description of desired motion
  duration: number;
  fps: number;
}

interface GeneratedVideo {
  videoPath: string;              // Path to generated MP4/WebM
  duration: number;               // Actual duration in seconds
  fps: number;                    // Actual frame rate
  resolution: { w: number; h: number };
  metadata: Record<string, unknown>; // Model-specific metadata
}

interface PixelArtConfig {
  targetSize: { w: number; h: number };  // 128×128 or 256×256
  palette: HexColor[];                    // Character-specific palette
  outlineColor: HexColor;                 // Default: #272929
  outlineWeight: number;                  // Pixels, default: 2
  backgroundStrategy: 'true_alpha' | 'chroma_key';
  chromaColor?: HexColor;                 // Default: #00FF00
}

interface TemporalConfig {
  staticRegionThreshold: number;  // Pixel change below this = static (lock to mode color)
  smoothingWindow: number;        // Frames to consider for temporal smoothing
  loopable: boolean;              // If true, enforce frame 0 ≈ frame N continuity
}
```

### Strategy Pattern Implementation

Each strategy is a separate class that composes adapter methods. Adding a new strategy requires zero changes to existing adapters or the pipeline.

```typescript
// src/core/strategies/ImageOnlyStrategy.ts
class ImageOnlyStrategy implements GenerationStrategy {
  async execute(manifest: ResolvedManifest, adapter: GeneratorAdapter): Promise<Result<ProcessedFrame[], SystemError>> {
    // Existing behavior — generate each frame individually
    // Uses: adapter.generateFrame() for each frame
    // No post-processing needed (frames are already pixel art)
  }
}

// src/core/strategies/HybridKVStrategy.ts
class HybridKVStrategy implements GenerationStrategy {
  async execute(
    manifest: ResolvedManifest,
    imageAdapter: GeneratorAdapter,   // For keyframe generation (Gemini)
    videoAdapter: GeneratorAdapter,   // For interpolation (Kling/Pika/Veo)
    postProcessor: PostProcessor      // For pixel art quantization
  ): Promise<Result<ProcessedFrame[], SystemError>> {
    // 1. Generate keyframes using image adapter
    // 2. Interpolate motion using video adapter
    // 3. Extract frames from video
    // 4. Quantize each frame to pixel art spec
    // 5. Apply temporal smoothing across sequence
    // 6. Return processed frames for audit
  }
}

// src/core/strategies/MotionTransferStrategy.ts (experimental)
class MotionTransferStrategy implements GenerationStrategy {
  async execute(
    manifest: ResolvedManifest,
    videoAdapter: GeneratorAdapter,
    postProcessor: PostProcessor
  ): Promise<Result<ProcessedFrame[], SystemError>> {
    // 1. Load canonical motion reference video from library
    // 2. Generate video using motion transfer (adapter.generateVideo)
    // 3. Extract + quantize frames
    // 4. Return for audit
  }
}
```

### Strategy Router

The Orchestrator delegates to the correct strategy based on the manifest:

```typescript
// src/core/StrategyRouter.ts
class StrategyRouter {
  selectStrategy(manifest: ResolvedManifest): GenerationStrategy {
    const strategyName = manifest.generator.strategy;

    switch (strategyName) {
      case 'image_only':
        return new ImageOnlyStrategy();
      case 'hybrid_keyframe_video':
        return new HybridKVStrategy();
      case 'motion_transfer':
        return new MotionTransferStrategy();
      default:
        // Fall back to image_only
        return new ImageOnlyStrategy();
    }
  }
}
```

---

## 4. Phase 0: Pixel Quantizer Prototype (GATE CHECK)

### Why This Comes First

The entire hybrid pipeline depends on one assumption: **we can convert anti-aliased, gradient-heavy video output back to clean pixel art.** If this fails, the hybrid approach is dead regardless of which video model we use. This is a go/no-go gate check that should be completed **before any video model API integration.**

### What to Build

A standalone script (no pipeline integration yet) that:

1. Takes a 1080p video file (MP4) as input
2. Extracts frames at a specified FPS using ffmpeg
3. Downscales each frame to 128×128 using nearest-neighbor interpolation
4. Snaps every pixel to the nearest color in a provided palette lookup table (LUT)
5. Detects and enforces bold outlines (#272929)
6. Removes the background and produces clean alpha
7. Outputs individual PNG frames

### Implementation: Why Node.js + Sharp (not Python)

The existing pipeline uses **Node.js + Sharp** for all image processing (see `architecture.md` Technology Stack). While Python/OpenCV is the standard for image processing prototyping, we should build this in the same stack as the production pipeline to avoid a rewrite later. Sharp is fast enough for this work and keeps everything in one language.

For frame extraction from video, we'll use **ffmpeg via Execa** (subprocess execution), which is already in our dependency stack.

### Technical Specification

```typescript
// File: src/utils/pixel-quantizer.ts (standalone, no pipeline dependencies)

/**
 * Pixel Quantizer — converts high-res video frames to pixel art spec.
 *
 * Pipeline:
 * 1. ffmpeg extracts frames from video at target FPS
 * 2. Sharp downscales to target resolution (nearest-neighbor)
 * 3. Palette snap: each pixel → nearest color in character LUT (Euclidean distance in RGB space)
 * 4. Outline enforcement: detect edges, apply #272929 at configured weight
 * 5. Alpha recovery: remove chroma key background, clean edge fringe
 * 6. Baseline registration: detect sprite bottom edge, align to baseline
 *
 * Why Sharp for image processing:
 *   - Already in our dependency stack (architecture.md)
 *   - Native Node.js bindings (libvips) — fast enough for 128×128 frames
 *   - Avoids Python dependency for the main pipeline
 *   - raw() pixel access enables custom palette snapping
 *
 * Why ffmpeg for frame extraction:
 *   - Industry standard for video frame extraction
 *   - Called via Execa (already in dependency stack)
 *   - Supports precise timestamp-based extraction
 */
```

### Palette LUT Format

Each character has a defined palette from the character descriptions. The LUT is a simple array of hex colors:

```typescript
// Sean's palette (from Champion Character Descriptions)
const SEAN_PALETTE: HexColor[] = [
  '#F5D6C6',  // Skin — light peach
  '#C2A769',  // Hair — dirty blonde
  '#4682B4',  // Eyes — steel blue
  '#F2F0EF',  // Tank top — off white
  '#2323FF',  // Pants — neon blue
  '#F5F5F5',  // Shoes — white
  '#272929',  // Outlines — bold dark
  '#000000',  // Pure black (shadows)
  '#FFFFFF',  // Pure white (highlights)
  // Shading variants (3-4 tones per base color):
  '#D4B5A5',  // Skin shadow
  '#B89A58',  // Hair shadow
  '#3A6B94',  // Eyes shadow
  '#D4D2D0',  // Tank top shadow
  '#1A1ABF',  // Pants shadow
  '#D4D4D4',  // Shoes shadow
];
```

### Palette Snap Algorithm

For each pixel in the downscaled frame, find the nearest palette color using Euclidean distance in RGB color space:

```typescript
function snapToPalette(r: number, g: number, b: number, palette: RGB[]): RGB {
  let minDist = Infinity;
  let nearest = palette[0];

  for (const color of palette) {
    const dist = Math.sqrt(
      (r - color.r) ** 2 +
      (g - color.g) ** 2 +
      (b - color.b) ** 2
    );
    if (dist < minDist) {
      minDist = dist;
      nearest = color;
    }
  }

  return nearest;
}
```

### Success Criteria for Gate Check

The quantizer prototype passes if:

- [ ] Output frames are exactly 128×128 pixels
- [ ] Every pixel maps to a color in the character palette (zero off-palette pixels)
- [ ] Bold outlines (#272929) are visually clean and consistent (2-3px weight)
- [ ] Background is fully transparent (clean alpha, no fringe)
- [ ] Character silhouette is recognizable and not distorted by quantization
- [ ] Output is visually acceptable as "Street Fighter II style pixel art" to human review
- [ ] Processing time is ≤ 2 seconds per frame

### What Happens If It Fails

If the quantizer can't produce acceptable pixel art from video output:

- **Fallback A:** Try generating at 2× target resolution (256×256) and downscaling to 128×128 — this gives more pixel data to work with
- **Fallback B:** Add a Gemini restyle pass (using 14 reference images) between video extraction and deterministic quantization — AI assists the style conversion
- **Fallback C:** Narrow the hybrid approach to only animations where quantization artifacts are acceptable (attacks, specials) and keep image-only for locomotion with enhanced pose references
- **Fallback D (last resort):** Abandon hybrid, invest fully in image-only with skeleton/mannequin pose references for every frame

### Test Input for Prototype

You don't need a video model yet. Create test input by:

1. Taking an existing walk cycle sprite sheet (any character, any game — for testing purposes only)
2. Upscaling it to 1080p with bilinear interpolation (simulates "what video model output looks like")
3. Adding anti-aliasing and slight color drift (simulates video model artifacts)
4. Running this through the quantizer
5. Comparing output to the original pixel art

This lets you iterate on the quantizer without burning video model API credits.

---

## 5. Phase 1: Video Model Evaluation Sprint

### Prerequisites

- Phase 0 quantizer prototype passes gate check
- API access or accounts set up for target models

### Goal

Determine which video model(s) produce the best raw material for our quantizer, specifically for walk cycle interpolation with our Street Fighter II pixel art characters.

### Models to Test (Priority Order)

| Priority | Model | Key Capability | Access Method | Why Test This |
|----------|-------|----------------|---------------|---------------|
| **1** | **Pika Pikaframes 2.2** | Up to 5 keyframe interpolation | fal.ai API | Directly maps to walk cycle anchoring. Cleanest multi-keyframe API. |
| **2** | **Kling 3.0** | Start/end frame + Elements 3.0 character lock | Kling API / Ultra subscription | Character identity locking could solve drift. Launched Feb 5, 2026. |
| **3** | **Google Veo 3.1** | First/last frame transition + up to 3 reference images | Vertex AI API (Google AI Ultra sub) | Already in Google ecosystem. Best resolution quality. |
| **4** | **Kling 2.6** | Motion transfer from reference video | Kling API | Could bypass keyframe generation entirely for standard locomotion. |
| **5** | **Wan 2.5** | Image-to-video, open source | Replicate API / local (RTX 5080) | No vendor lock-in. Can run locally on your hardware. |

### Experiment: Gemini Loop Integrity Test

**Run this FIRST — takes 30 minutes, costs almost nothing, and calibrates your identity drift expectations.**

1. Generate a single Sean idle pose using proven Gemini workflow
2. Upload that SAME image as both start AND end frame to Kling (or Veo)
3. Use text prompt: "Pixel art fighting game character performing subtle idle breathing animation. Character stays in place, slight vertical bounce. No camera movement."
4. Extract frames from the resulting video
5. Run each frame through the quantizer
6. Measure identity drift (SSIM vs. the input image) across all frames

**What you learn:**
- If identity holds → the video model can maintain character consistency. Proceed to walk cycle tests.
- If identity drifts → you need tighter identity locking (Kling Elements, stronger references) before walk cycles will work.

### Experiment Matrix: Walk Cycle Tests

For each video model, test with Champion Sean walk cycle using these configurations:

| Test ID | Keyframe Count | Keyframe Source | Video Model | Post-Processing | Primary Metric |
|---------|---------------|-----------------|-------------|-----------------|----------------|
| W-01 | 4 keyframes (frames 0,2,4,6) | Gemini (proven workflow) | Pika Pikaframes 2.2 | Full quantizer | Audit pass rate |
| W-02 | 2 keyframes (start/end) | Gemini | Kling 3.0 start/end | Full quantizer | Audit pass rate |
| W-03 | 2 keyframes (start/end) | Gemini | Veo 3.1 first/last | Full quantizer | Audit pass rate |
| W-04 | 0 (motion transfer) | N/A | Kling 2.6 + reference walk video | Full quantizer | Audit pass rate |
| W-05 | 4 keyframes | Gemini | Wan 2.5 I2V (local) | Full quantizer | Audit pass rate |
| W-06 | Same as W-01 winner | Same | Same | Quantizer + Gemini restyle | Compare vs W-01 |

**Run each test 3 times** to measure variance. Grade on existing audit gates (SSIM identity, palette fidelity, baseline drift, alpha artifacts). Log everything.

### Keyframe Generation for Tests

Use the proven Gemini dual-reference approach with pose reference images. For the walk cycle, generate these 4 keyframes:

| Keyframe | Frame Position | Pose Reference | Description |
|----------|---------------|----------------|-------------|
| KF-0 | Frame 0 (Contact L) | CGTyphoon Position 1 | Left foot forward, right foot back, contact position |
| KF-1 | Frame 2 (Passing) | CGTyphoon Position 2 | Feet passing, weight transferring, mid-stride |
| KF-2 | Frame 4 (Contact R) | CGTyphoon Position 3 | Right foot forward, left foot back, mirror of KF-0 |
| KF-3 | Frame 6 (Passing) | CGTyphoon Position 4 | Feet passing (opposite direction), completing cycle |

Use the established prompt structure from `advanced-nano-banana-pro-techniques.md` with the walk cycle prompts from the Prompt Library section.

### Video Model Prompt Template

For all video model tests, use this base prompt (adapt per model's prompt conventions):

```
Pixel art fighting game character performing a walk cycle animation.
Character walks forward (right), maintaining exact appearance from reference frames.
Smooth natural walking motion with correct leg alternation.
Fixed side-view camera, no zoom, no camera movement.
Solid green (#00FF00) background.
Consistent bold dark outlines.
No anti-aliasing, no blur, no gradients.
Loop seamlessly from last frame back to first frame.
```

### Scoring Criteria

For each test, score on:

| Metric | Weight | How to Measure |
|--------|--------|----------------|
| Leg Differentiation | 30% | Visual check: do left and right legs clearly alternate correctly? Binary pass/fail per frame. |
| Identity Consistency | 25% | SSIM vs anchor image. Target ≥ 0.85 after quantization. |
| Palette Fidelity | 15% | % of pixels matching character palette after quantization. Target ≥ 90%. |
| Baseline Stability | 15% | Max pixel drift of sprite bottom edge across all frames. Target ≤ 2px (relaxed from 1px for initial testing). |
| Alpha Quality | 10% | Halo severity score after background removal. Target ≤ 0.3. |
| Style Preservation | 5% | Human judgment: does it look like SF2 pixel art after quantization? 1-5 scale. |

### Decision Gate: Phase 1 → Phase 2

Phase 1 is complete when:

- [ ] At least one video model produces walk cycle output that passes ≥ 60% of frames through audit gates after quantization
- [ ] Leg differentiation is correct in ≥ 90% of frames for the winning model
- [ ] The winning model's output can be quantized to acceptable pixel art quality
- [ ] Cost per walk cycle generation is documented (API credits + operator time)

If no model meets these criteria, revisit the quantizer (try Gemini restyle pass) or narrow scope.

---

## 6. Phase 2: Hybrid Pipeline End-to-End

### Goal

Ship one complete hybrid path from manifest to validated Phaser atlas for Champion Sean walk cycle.

### Scope

- **Character:** Sean (Champion)
- **Animation:** Walk Cycle (8 frames)
- **Strategy:** Hybrid Keyframe-to-Video (using Phase 1 winner)
- **Output:** `champion-sean-walk.png` + `champion-sean-walk.json` that loads and animates in Phaser without visible jitter

### Implementation Steps

1. **Extend manifest schema** to support `generator.strategy: 'hybrid_keyframe_video'` (see Section 11)
2. **Implement the winning video model adapter** (thin wrapper — API call + error mapping)
3. **Integrate the quantizer** into the pipeline as a PostProcessor
4. **Wire the HybridKVStrategy** into the Orchestrator via the StrategyRouter
5. **Run the full pipeline:** `pipeline run manifests/champion-sean/walk.yaml`
6. **Validate:** TexturePacker → Phaser headless → visual inspection

### Extended Artifact Folder Structure

For hybrid runs, the artifact folder adds video-specific directories:

```
runs/<run_id>/
├── manifest.lock.json
├── state.json
├── keyframes/                  # NEW — generated keyframe images
│   ├── kf_00.png
│   ├── kf_01.png
│   ├── kf_02.png
│   └── kf_03.png
├── video/                      # NEW — raw video model output
│   ├── interpolated.mp4
│   └── generation_metadata.json
├── extracted/                  # NEW — raw frames extracted from video
│   ├── raw_frame_00.png
│   ├── raw_frame_01.png
│   └── ...
├── quantized/                  # NEW — frames after pixel art quantization
│   ├── quant_frame_00.png
│   ├── quant_frame_01.png
│   └── ...
├── candidates/                 # Final candidates (same as before)
├── approved/
├── rejected/
├── audit/
├── export/
│   ├── atlas.png
│   └── atlas.json
└── validation/
```

### Retry Ladder Extension for Hybrid

The existing retry ladder (edit → re-anchor → tighten prompt → stop) extends with strategy-level escalation:

```
Hybrid Retry Ladder:
1. Re-generate video (same keyframes, different seed)
2. Adjust video model creativity/motion scale
3. Re-generate keyframes with tighter pose refs
4. Try different video model (fallback adapter)
5. Fall back to ImageOnly strategy for this animation
6. Stop with diagnostic report
```

This means the `RetryManager` needs a new escalation path: if hybrid fails N times, it can transparently switch to image-only for that specific animation without failing the entire run.

---

## 7. Phase 3: Adapter Layer & Strategy Router

### Goal

Generalize the hybrid pipeline so new video models can be integrated in < 1 day of engineering work. This is the "build the socket, not the plug" investment.

### Adapter Registry

Each adapter registers with the system and declares its capabilities:

```typescript
// src/adapters/registry.ts

interface AdapterCapabilities {
  name: string;                              // e.g., 'kling-3.0'
  type: 'image' | 'video' | 'both';
  supports: {
    generateFrame: boolean;
    generateKeyframes: boolean;
    interpolateFrames: boolean;
    generateVideo: boolean;
  };
  constraints: {
    maxKeyframes?: number;                   // e.g., Pika = 5, Kling = 2
    maxReferenceImages?: number;             // e.g., Gemini = 14, Veo = 3
    maxDuration?: number;                    // seconds
    supportsLoop?: boolean;
    supportsAlpha?: boolean;                 // true alpha output vs chroma key needed
    supportsSeed?: boolean;                  // deterministic generation
  };
  pricing: {
    costPerGeneration?: number;              // USD estimate
    costPerSecondVideo?: number;
  };
}

// Adapters self-register:
const ADAPTER_REGISTRY: Map<string, AdapterCapabilities> = new Map([
  ['gemini-flash', {
    name: 'gemini-flash',
    type: 'image',
    supports: { generateFrame: true, generateKeyframes: true, interpolateFrames: false, generateVideo: false },
    constraints: { maxReferenceImages: 14, supportsSeed: false },
    pricing: { costPerGeneration: 0.01 }
  }],
  ['pika-pikaframes', {
    name: 'pika-pikaframes',
    type: 'video',
    supports: { generateFrame: false, generateKeyframes: false, interpolateFrames: true, generateVideo: false },
    constraints: { maxKeyframes: 5, supportsLoop: true, supportsAlpha: false },
    pricing: { costPerSecondVideo: 0.05 }
  }],
  ['kling-3.0', {
    name: 'kling-3.0',
    type: 'video',
    supports: { generateFrame: false, generateKeyframes: false, interpolateFrames: true, generateVideo: true },
    constraints: { maxKeyframes: 2, maxReferenceImages: 8, supportsLoop: true, supportsAlpha: false },
    pricing: { costPerSecondVideo: 0.08 }
  }],
  // ... more adapters
]);
```

### Strategy Auto-Selection (Phase 3+)

Once telemetry data accumulates from Phases 1-2, the system can automatically select the best strategy per animation type:

```typescript
// src/core/StrategyPlanner.ts (Phase 3)

interface AnimationArchetype {
  type: 'locomotion' | 'attack' | 'reaction' | 'idle' | 'special';
  requiresLoop: boolean;
  frameCount: number;
  complexityLevel: 'low' | 'medium' | 'high';
}

function selectStrategy(archetype: AnimationArchetype, telemetry: TelemetryData): string {
  // Locomotion (walk, run) → hybrid by default
  if (archetype.type === 'locomotion') return 'hybrid_keyframe_video';

  // Low-complexity, non-looping → image-only is fine
  if (archetype.complexityLevel === 'low' && !archetype.requiresLoop) return 'image_only';

  // High frame count attacks → might benefit from hybrid
  if (archetype.frameCount >= 8) return 'hybrid_keyframe_video';

  // Default
  return 'image_only';
}
```

---

## 8. Post-Processing Pipeline Specification

### Overview

The post-processing pipeline converts raw video model output into pixel-art-spec frames ready for auditing. This is **deterministic code** — no AI models involved (unless the optional Gemini restyle pass is enabled).

### Pipeline Steps (in order)

#### Step 1: Frame Extraction

**Tool:** ffmpeg via Execa
**Input:** MP4/WebM video file
**Output:** Sequence of PNG frames

```bash
# Extract frames at specific timestamps (for precise frame selection)
ffmpeg -i input.mp4 -vf "select='eq(n\,0)+eq(n\,3)+eq(n\,6)+eq(n\,9)+eq(n\,12)+eq(n\,15)+eq(n\,18)+eq(n\,21)'" -vsync vfr frame_%03d.png

# OR extract at constant FPS (simpler, then select best frames)
ffmpeg -i input.mp4 -vf fps=24 frame_%03d.png
```

**Why ffmpeg:** Industry standard for video frame extraction. Called via Execa (already in dependency stack) for cross-platform safety. We don't need a Node.js video library — ffmpeg handles this with one subprocess call.

#### Step 2: Nearest-Neighbor Downscale

**Tool:** Sharp
**Input:** High-res frame (e.g., 1080×1080)
**Output:** Target-res frame (128×128 or 256×256)

```typescript
await sharp(inputPath)
  .resize(128, 128, { kernel: sharp.kernel.nearest })
  .toFile(outputPath);
```

**Why nearest-neighbor:** Standard resize algorithms (bilinear, bicubic) create anti-aliased intermediate colors that don't exist in pixel art. Nearest-neighbor preserves hard pixel edges. This is the standard approach for pixel art downscaling.

#### Step 3: Palette Quantization

**Tool:** Custom Sharp raw pixel manipulation
**Input:** Downscaled frame (128×128, full color)
**Output:** Frame with every pixel snapped to character palette

Process: Read raw pixel buffer → iterate each pixel → snap to nearest palette color (Euclidean distance in RGB) → write back.

**Why custom, not Sharp's built-in palette:** Sharp's `palette` option uses median-cut quantization which chooses its own colors. We need to force-snap to a specific, predetermined palette.

#### Step 4: Temporal Smoothing

**Tool:** Custom logic comparing adjacent frames
**Input:** Sequence of quantized frames
**Output:** Smoothed sequence with static region locking

Process:
1. Compare each pixel position across the frame sequence
2. If a pixel barely changes (below threshold), lock it to the **mode color** across all frames (the color it is most often)
3. This eliminates sub-pixel jitter in areas that should be static (torso, head during walk cycle)

**Reference implementation:** Sarthak Mishra's pipeline used this technique to achieve 46KB optimized sprite sheets from 1.18MB video input. The key parameters are:

- `staticThreshold`: How much a pixel can change and still be considered "static" (start with 15 in RGB distance)
- `modeColorWindow`: How many frames to consider when computing mode (all frames for short animations)

#### Step 5: Outline Enforcement

**Tool:** Custom edge detection + overlay
**Input:** Palette-quantized frame
**Output:** Frame with enforced bold outlines

Process:
1. Detect sprite edges (pixels adjacent to transparent pixels)
2. Detect internal color boundaries (adjacent pixels with different palette colors)
3. Apply #272929 outline at configured weight (2-3px)
4. Ensure outlines are consistent with the character anchor's outline style

**Why this step is needed:** Video models often soften or blur outlines during interpolation. Even after palette snapping, the outline weight may be inconsistent. This step re-applies the characteristic bold outlines of SF2-style pixel art.

#### Step 6: Alpha Recovery

**Tool:** Sharp + custom logic
**Input:** Frame (may have solid background or muddy alpha)
**Output:** Frame with clean transparency

Process depends on video model output:
- **If chroma key background (#00FF00):** Color-distance-based removal, then edge cleanup
- **If no alpha/random background:** Use foreground detection (bounding box from sprite content), mask, and clean edges

Alpha edge cleanup:
1. Find all semi-transparent pixels at sprite boundary
2. If alpha < 128, set to fully transparent
3. If alpha ≥ 128, set to fully opaque
4. This eliminates the anti-aliased fringe that video models create

#### Step 7: Baseline Registration

**Tool:** Custom sprite analysis
**Input:** Frame with clean alpha
**Output:** Frame with feet aligned to consistent baseline position

Process:
1. Detect sprite bottom edge (lowest non-transparent pixel row)
2. Compare to target baseline position (from manifest or anchor reference)
3. If offset > tolerance, shift sprite vertically within the canvas to align
4. Log the drift value for audit

**Why this matters:** Baseline drift is the #1 cause of "ice skating" animation jitter in Phaser. Even 1-2px drift between frames is visible. The quantizer should handle gross alignment; the auditor catches anything remaining.

### Optional: Gemini Restyle Pass

If deterministic quantization alone doesn't produce acceptable quality, add an AI-assisted restyle step between extraction and quantization:

```
Raw video frame (1080p)
    ↓
Gemini 3 Pro Image Edit (with up to 14 reference images):
  - Character anchor
  - Character turnaround
  - 4-6 approved keyframes as style references
  - Prompt: "Restyle this frame to match the pixel art style
    of the reference images. Bold #272929 outlines, flat cel
    shading, crisp pixels, no anti-aliasing."
    ↓
Restyled frame (still high-res, but now styled correctly)
    ↓
Deterministic quantization pipeline (steps 2-7 above)
```

This is the approach GPT 5.2 called "RestyleToPixelSpec" — treat it as an optional node you can enable/disable per manifest.

---

## 9. Video Model Landscape (Feb 2026)

This section captures the current state of video models relevant to our use case as of February 10, 2026. **This will be outdated quickly.** Update when testing reveals new capabilities or limitations.

### Kling 3.0 (Launched Feb 5, 2026)

- **Key feature:** Multi-shot storyboarding (up to 6 cuts), 15s duration, Elements 3.0 character lock via 3-8s reference video, start/end frame control
- **Why it matters:** Start/end frame + character reference could solve both temporal coherence AND identity drift
- **Access:** Ultra subscriber early access, API expected Q1 2026
- **Limitation:** API availability may lag consumer release. Test via web interface first.
- **Source:** Dzine.ai comparison, Yahoo Finance launch coverage

### Kling 2.6

- **Key feature:** Motion control via reference video transfer
- **Why it matters:** Upload a known-good walk cycle video from any source, transfer that motion onto your character. Could bypass keyframe generation entirely.
- **Access:** Kling API
- **Unique angle:** Build a library of "canonical motion" reference videos for fighting game animations

### Pika Pikaframes 2.2

- **Key feature:** Multi-keyframe interpolation with up to 5 input images
- **Why it matters:** Directly maps to our workflow. Generate 4-5 keyframes with Gemini, feed to Pika, get smooth interpolation.
- **Access:** fal.ai API (cleanest integration path)
- **Limitation:** No character identity locking beyond what the keyframes provide

### Google Veo 3.1

- **Key feature:** First/last frame transition generation, up to 3 reference images for style guidance
- **Why it matters:** You're already in the Google ecosystem (Gemini / Nano Banana Pro). Reference images can help with style consistency.
- **Access:** Vertex AI API, Google AI Ultra subscription
- **Limitation:** Reddit users report resolution mismatch — Veo generates at much higher resolution than pixel art needs, creating anti-aliased pixels that "would never work" at target resolution. Our quantizer must handle this aggressively.
- **Source:** Reddit r/aigamedev Veo 2 pixel art thread

### Wan 2.5 (Open Source)

- **Key feature:** Strong character trait restoration, I2V capabilities, runnable locally
- **Why it matters:** No vendor lock-in. Can run on your RTX 5080 via ComfyUI. No API costs for experimentation.
- **Access:** Replicate API, Higgsfield, or local installation
- **Limitation:** Lower quality than commercial models, but free for unlimited iteration

### Emerging / Monitor List

| Tool | What It Does | Why Watch It |
|------|-------------|--------------|
| **Retro Diffusion rd-animation** | Purpose-built pixel art sprite animation model | Could bypass post-processing entirely. Walk cycle model "nearly released" as of early 2026. Available on Replicate. |
| **PixelLab** | Specialized pixel art generation tool | Emerging as a potential "black box" alternative. May degrade at 256×256 (training data usually 64×64). |
| **Scenario.com** | Platform aggregating 140+ models including Kling, Veo, custom-trained | Could serve as your adapter layer before building custom integrations. |

---

## 10. Test Matrix & Experiments

### Experiment Naming Convention

All experiments follow: `{TYPE}-{NUMBER}` where TYPE is:

- `LI` = Loop Integrity tests
- `W` = Walk cycle tests
- `Q` = Quantizer tests
- `MT` = Motion transfer tests

### Phase 0 Experiments (Quantizer)

| ID | Description | Input | Expected Output | Pass Criteria |
|----|-------------|-------|-----------------|---------------|
| Q-01 | Quantize upscaled pixel art (control test) | Known pixel art walk cycle upscaled to 1080p with bilinear interpolation | 128×128 palette-locked frames | Output matches original pixel art within 95% pixel accuracy |
| Q-02 | Quantize with added anti-aliasing | Same as Q-01 but with Gaussian blur applied | 128×128 palette-locked frames | Recognizable character, clean outlines, ≤ 10% pixel error vs original |
| Q-03 | Quantize with color drift | Same as Q-01 but with hue/saturation shift | 128×128 palette-locked frames | Palette snap recovers correct colors despite drift |
| Q-04 | Alpha recovery from chroma key | 1080p frame with #00FF00 background | 128×128 with clean alpha | No green fringe, no halo, clean sprite edges |

### Phase 1 Experiments (Video Models)

| ID | Model | Keyframes | Config | Primary Question |
|----|-------|-----------|--------|------------------|
| LI-01 | Kling 3.0 | Same image × 2 (start=end) | Idle breathing prompt | Does identity hold through video generation? |
| LI-02 | Veo 3.1 | Same image × 2 (first=last) | Idle breathing prompt | Does identity hold through video generation? |
| W-01 | Pika 2.2 | 4 Gemini keyframes | Default settings | Best multi-keyframe interpolation? |
| W-02 | Kling 3.0 | 2 Gemini keyframes (start/end) | Elements 3.0 character lock | Does character lock improve output? |
| W-03 | Veo 3.1 | 2 Gemini keyframes (first/last) | 3 reference images | Does reference image support help? |
| W-04 | Kling 2.6 | 0 (motion transfer) | Reference walk video + Sean anchor | Can motion transfer bypass keyframes? |
| W-05 | Wan 2.5 | 4 Gemini keyframes | Local (RTX 5080) | Viable free/local option? |
| W-06 | Best of W-01-05 | Same as winner | Quantizer + Gemini restyle | Does AI restyle improve quality? |

### Telemetry to Capture Per Experiment

Log ALL of the following for every experiment:

```json
{
  "experiment_id": "W-01",
  "timestamp": "2026-02-15T14:30:00Z",
  "model": "pika-pikaframes-2.2",
  "strategy": "hybrid_keyframe_video",
  "keyframe_count": 4,
  "keyframe_source": "gemini-flash",
  "video_duration_s": 2.0,
  "video_resolution": "1080x1080",
  "frames_extracted": 8,
  "quantizer_version": "0.1.0",
  "restyle_enabled": false,
  "audit_results": {
    "frames_passed": 6,
    "frames_failed": 2,
    "pass_rate": 0.75,
    "leg_differentiation_correct": 7,
    "leg_differentiation_total": 8,
    "avg_ssim_vs_anchor": 0.87,
    "avg_palette_fidelity": 0.92,
    "max_baseline_drift_px": 1.5,
    "avg_alpha_halo_severity": 0.15
  },
  "cost_usd": 0.42,
  "operator_time_minutes": 15,
  "notes": "Leg ordering correct but frames 3 and 5 have palette drift after quantization"
}
```

---

## 11. Manifest Schema Extensions

### New Fields

The existing manifest schema (from `epics.md` Story 2.1) extends with these new fields:

```yaml
# manifests/champion-sean/walk.yaml — HYBRID EXAMPLE

identity:
  character: sean
  character_type: champion
  move: walk_forward
  version: v1
  frame_count: 8
  target_resolution: 128

inputs:
  anchor: assets/anchor-characters/champion-anchor-characters/Champion-Sean-anchor.png
  style_refs:
    - assets/style-refs/sean-turnaround.png
  pose_refs:
    - assets/pose-refs/walk-cycle/contact-left.png
    - assets/pose-refs/walk-cycle/passing.png
    - assets/pose-refs/walk-cycle/contact-right.png
    - assets/pose-refs/walk-cycle/passing-return.png
  guides:
    - assets/guides/guide_128.png

# --- NEW FIELDS BELOW ---

generator:
  strategy: hybrid_keyframe_video       # NEW — 'image_only' | 'hybrid_keyframe_video' | 'motion_transfer'
  strategy_fallback: image_only         # NEW — fallback if primary strategy fails N times

  # Keyframe generation config (used by hybrid strategy)
  keyframe:
    backend: gemini-flash               # Which adapter generates keyframes
    model: gemini-2.0-flash
    mode: edit_from_anchor
    keyframe_indices: [0, 2, 4, 6]      # Which frame positions are keyframes
    interpolation_frames: [1, 3, 5, 7]  # Which are interpolated from video

  # Video interpolation config (used by hybrid strategy)
  interpolation:
    backend: pika-pikaframes            # Which adapter does interpolation
    model: pika-2.2
    duration: 2.0                       # Video duration in seconds
    fps: 24                             # Video FPS (extract frames from this)
    loop: true                          # Request loopable output
    creativity_scale: 0.3               # 0-1, lower = more faithful to keyframes
    motion_prompt: >
      Pixel art fighting game character performing a smooth walk cycle.
      Character walks forward (right) with natural leg alternation.
      Fixed side-view camera. Solid green background. Bold dark outlines.

  # Motion transfer config (used by motion_transfer strategy)
  motion_transfer:
    backend: kling-2.6
    reference_video: assets/motion-refs/canonical-walk-cycle.mp4
    motion_prompt: "Walk cycle, steady pace, right-facing"

  # Existing fields (unchanged)
  prompts:
    master: "..."
    variation: "..."
    lock: "..."
    negative: "..."
  max_attempts_per_frame: 5
  seed_policy: random

# Post-processing config (NEW — only used by hybrid/motion_transfer)
post_processing:
  enabled: true
  restyle_pass: false                   # Enable Gemini restyle before quantization
  restyle_backend: gemini-flash         # Which adapter does restyling
  quantizer:
    downscale_method: nearest           # nearest | lanczos (nearest for pixel art)
    palette_source: character           # 'character' uses palette from character spec
    palette_override: []                # Optional: explicit hex color list
    outline_color: '#272929'
    outline_weight: 2                   # pixels
    background_strategy: chroma_key
    chroma_color: '#00FF00'
  temporal_smoothing:
    enabled: true
    static_threshold: 15                # RGB distance below which pixel is "static"
    mode_color_window: all              # 'all' or number of frames

auditor:
  # Existing fields (unchanged) plus:
  thresholds:
    identity_min: 0.85                  # SSIM vs anchor
    palette_min: 0.90
    alpha_artifact_max: 0.3
    baseline_drift_max: 2              # Relaxed from 1px for hybrid (tighten after tuning)
    composite_min: 0.70
    # NEW thresholds for hybrid:
    temporal_jitter_max: 0.15           # Optical flow variance across sequence
    frame_to_frame_ssim_min: 0.80       # Adjacent frame similarity floor

retry:
  # Existing fields plus:
  strategy_escalation:
    max_hybrid_failures: 3              # After 3 hybrid failures, fall back to strategy_fallback
  ladder:
    # Extended ladder for hybrid:
    - action: regenerate_video          # Re-run video model with different seed
    - action: adjust_creativity         # Lower creativity_scale by 0.1
    - action: regenerate_keyframes      # Re-generate keyframes with tighter refs
    - action: swap_video_model          # Try fallback interpolation model
    - action: fallback_image_only       # Switch to image-only for this animation
    - action: stop                      # Halt with diagnostic

export:
  # Unchanged from existing schema
  packer_flags: "--format phaser --trim-mode Trim --extrude 1 --shape-padding 2 --border-padding 2 --disable-rotation --alpha-handling ReduceBorderArtifacts --max-size 2048 --trim-sprite-names --prepend-folder-name"
  atlas_format: phaser
```

---

## 12. New Audit Gates for Hybrid Pipeline

### New Hard Gates

| Code | Gate | Threshold | Rationale |
|------|------|-----------|-----------|
| HF06 | Frame Count Match | Extracted frames == manifest.frame_count | Video model might produce wrong number of usable frames |
| HF07 | Pixel Grid Alignment | All pixels snap to integer grid after downscale | Sub-pixel artifacts from video interpolation |

### New Soft Gates

| Code | Metric | Threshold | Rationale |
|------|--------|-----------|-----------|
| SF06 | Temporal Jitter | Optical flow variance < 0.15 across sequence | Detects interpolation artifacts that per-frame audits miss. Walk cycle flow should follow a predictable sinusoidal pattern. |
| SF07 | Frame-to-Frame Continuity | SSIM between adjacent frames ≥ 0.80 | Catches "jump cuts" where video model lost coherence between frames |
| SF08 | Quantization Fidelity | ≥ 85% visual similarity between pre- and post-quantized frames | Catches cases where palette snapping destroyed important detail |

### Optical Flow Audit (SF06) — Detail

This is Claude Opus 4.6's unique contribution. For walk cycles, the magnitude of optical flow between consecutive frames should follow a **predictable sinusoidal pattern**:

- High flow at stride extremes (contact positions)
- Low flow at passing positions (legs crossing)
- Smooth transitions between high and low

If the flow pattern is erratic (spikes, drops, asymmetry), it indicates interpolation artifacts even if individual frames look acceptable.

**Implementation:** Compute optical flow magnitude between each consecutive frame pair using a simple block-matching algorithm (no need for heavy optical flow libraries at 128×128 resolution). Plot the magnitude curve. Flag if variance exceeds threshold.

---

## 13. Risk Register

| ID | Risk | Probability | Impact | Mitigation | Owner |
|----|------|-------------|--------|------------|-------|
| R1 | Quantizer destroys motion quality (over-quantization) | High | High | Invest in temporal smoothing. Lock static regions. Tune thresholds iteratively. Try 2× resolution generation + downscale. | Phase 0 |
| R2 | Video models can't maintain character identity at pixel scale | Medium | High | Kling 3.0 Elements (reference video lock). Gemini restyle pass. Fall back to image-only if needed. | Phase 1 |
| R3 | API cost blowup from retry ladders | Medium | Medium | Per-animation cost caps in manifest. Track cost-per-approved-frame. Prefer Wan 2.5 (local/free) for high-retry animations. | Phase 2 |
| R4 | Video model API deprecation / breaking changes | High | Low | Adapter pattern absorbs changes. One adapter swap, zero pipeline changes. | Phase 3 |
| R5 | Pixel grid misalignment from interpolated frames | High | Medium | Post-processing includes explicit grid-snap. Generate at 2× and downscale nearest-neighbor. | Phase 0 |
| R6 | Kling 3.0 API not available yet (web-only early access) | Medium | Medium | Test via web interface first. Pika via fal.ai is available now as primary. | Phase 1 |
| R7 | Walk cycle doesn't loop seamlessly | Medium | Medium | Use start=end frame trick where supported. Post-process: ensure frame 0 and frame N-1 are compatible. | Phase 1 |
| R8 | Outline enforcement creates visual artifacts | Medium | Low | Tune outline detection sensitivity. Compare with anchor outline weight. Manual override per character. | Phase 0 |

---

## 14. Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| 2026-02-10 | Adopt hybrid keyframe-to-video as primary generation strategy for locomotion | Model Council consensus (3/3 models). Video model first/last frame conditioning directly solves temporal coherence. | Image-only with enhanced pose refs (proven failure point). Wait-and-adapt (Gemini: "practically obsolete" given current capabilities). |
| 2026-02-10 | Keep image-only as fallback and keyframe generator | 2/3 Council models recommend (Opus, GPT 5.2). It works for static poses and generates the keyframes hybrid needs. | Abandon entirely (Gemini recommendation — too aggressive, loses proven capability). |
| 2026-02-10 | Build quantizer prototype BEFORE integrating video models | Gemini's strongest recommendation. If quantization fails, hybrid is dead regardless of video model choice. | Integrate video model first, then build quantizer (higher risk — burns API credits on possibly-unviable approach). |
| 2026-02-10 | Use Node.js + Sharp for quantizer (not Python/OpenCV) | Matches existing pipeline stack. Avoids language boundary. Sharp is fast enough for 128×128 frames. | Python/OpenCV (more image processing libraries available, but requires rewrite for production integration). |
| 2026-02-10 | Start with Pika Pikaframes via fal.ai as primary video model | Cleanest multi-keyframe API. Up to 5 keyframes = perfect for walk cycle anchoring. Available now via API. | Kling 3.0 (best features but API access uncertain). Veo 3.1 (resolution mismatch concerns). |
| 2026-02-10 | Four atomic adapter operations (not DAG render graph) | Opus's architecture — right complexity for solo developer in MVP. DAG is overengineered for current scope. | Full DAG render graph (GPT 5.2 — better for scale, too complex now). Three-stage linear pipeline (Gemini — too simple for manifest-driven needs). |
| 2026-02-10 | Extend RetryManager with strategy escalation | If hybrid fails repeatedly, transparently fall back to image-only. Prevents total run failure. | Separate retry systems per strategy (more complex). Manual strategy selection only (less resilient). |

---

## 15. Reference Implementations & Resources

### Sarthak Mishra's Video-to-Pixel-Art Pipeline

**URL:** sarthakmishra.com/blog/building-animated-sprite-hero
**Relevance:** Already-validated reference implementation for the exact post-processing challenge. Achieved 46KB sprite sheets from 1.18MB video.
**Key techniques:**
- Color quantization to 24 colors with no dithering
- Temporal smoothing via static region detection and mode-color locking
- Change threshold tuning to eliminate sub-pixel jitter

### Pika Pikaframes API via fal.ai

**URL:** blog.fal.ai/pika-api-is-now-powered-by-fal/
**Relevance:** Cleanest API for multi-keyframe interpolation (up to 5 images)

### Kling 3.0 Launch Details

**URL:** dzine.ai/blog/kling-3-0-vs-kling-2-6/
**Relevance:** Elements 3.0 character lock, multi-shot storyboarding, start/end frame

### Google Veo First/Last Frame API

**URL:** docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-first-and-last-frames
**Relevance:** Official Vertex AI documentation for first+last frame transition generation

### Retro Diffusion (Monitor)

**URL:** astropulse.itch.io/retrodiffusion (comments section for release status)
**URL:** replicate.com/blog/retro-diffusions-pixel-art-models-are-now-on-replicate
**Relevance:** Purpose-built pixel art animation. Walk cycle model "nearly released."

### CGTyphoon Walk Cycle Reference

**Relevance:** The pose reference images used for keyframe generation. Shows 5 key positions with green (current) and blue (previous) figures.

---

## 16. Glossary of New Terms

| Term | Definition |
|------|------------|
| **Hybrid Keyframe-to-Video (HybridKV)** | Generation strategy that produces keyframes with a proven image model, then uses video models to interpolate smooth motion between them. The video output is post-processed back to pixel art spec. |
| **Pixel Quantizer** | The post-processing pipeline that converts anti-aliased, gradient-heavy video model output back to clean pixel art. Includes downscaling, palette snapping, outline enforcement, alpha recovery, and baseline registration. |
| **Quantized Motion Bridge** | Gemini 3 Pro's name for the hybrid approach. The "bridge" is the video model connecting keyframes, and "quantized" refers to snapping the output back to pixel grid/palette. |
| **Motion Transfer** | Using a video model to transfer the motion pattern from a reference video onto a generated character. The reference video can be from any source (existing sprite animations, 3D renders, real video). |
| **Temporal Smoothing** | Post-processing technique that detects pixels that barely change across a frame sequence and locks them to a single consistent color, eliminating sub-pixel jitter from video interpolation. |
| **Static Region Lock** | Within temporal smoothing: pixels below the change threshold are set to their mode color (most common value) across all frames. Eliminates flicker in areas that should be still (torso, head during walk). |
| **Strategy Escalation** | Extension to the RetryManager where, after a configured number of failures with one generation strategy, the system transparently switches to a fallback strategy (e.g., hybrid → image-only). |
| **Canonical Motion Library** | A collection of reference walk cycle, attack, and movement videos used as input for motion transfer generation. These are reusable across all characters. |
| **Loop Integrity Test** | Calibration experiment: use the same image as both start and end frame with a simple motion prompt. Measures how much identity drift a video model introduces during generation. |
| **Sludge** | Informal term for raw video model output: frames that move correctly but have wrong styling for pixel art (anti-aliased edges, gradient shading, wrong palette, blurry outlines). The quantizer converts sludge to clean pixel art. |
| **RestyleToPixelSpec** | Optional pipeline node that uses an AI image editing model (Gemini) with multiple reference images to restyle video frames toward pixel art before deterministic quantization. More expensive but potentially higher quality. |

---

## Implementation Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| **Week 1** (Feb 10-16) | Phase 0 | Pixel Quantizer prototype script. Run Q-01 through Q-04 experiments. Gate check pass/fail. |
| **Week 2** (Feb 17-23) | Phase 1 | Loop Integrity tests (LI-01, LI-02). Set up API access for Pika (fal.ai) and at least one other model. |
| **Week 3** (Feb 24 - Mar 2) | Phase 1 | Walk cycle experiments W-01 through W-05. Score and compare. Select winning model. |
| **Week 4** (Mar 3-9) | Phase 1→2 | Optional W-06 (Gemini restyle). Decision gate review. Begin Phase 2 integration. |
| **Weeks 5-6** (Mar 10-23) | Phase 2 | Manifest schema extension. Video adapter implementation. Wire HybridKVStrategy into Orchestrator. |
| **Weeks 7-8** (Mar 24 - Apr 6) | Phase 2 | End-to-end run: Sean walk cycle from manifest to Phaser-validated atlas. Fix issues. Iterate. |
| **Weeks 9-12** (Apr 7-May 4) | Phase 3 | Adapter registry. Strategy auto-selection. Second character test. Telemetry dashboard. |

---

**Document Status:** COMPLETE — Ready for implementation with Claude Code.

**Next Action:** Phase 0 — Build the Pixel Quantizer prototype and run gate check experiments.
