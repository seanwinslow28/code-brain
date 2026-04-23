

# Architecture Strategy for Manifest-Driven AI Sprite Sheet Pipeline

## Executive Recommendation

**Invest primarily in Option 3 (wait-and-adapt) for the *generation* layer, while aggressively pursuing Option 2 (hybrid keyframe-to-video) as your *testing* focus — and architect the adapter layer to make this a false choice.** The model landscape is shifting so fast (Kling 3.0 literally launched 4 days ago on Feb 5, 2026 [1][2]) that any hard commitment to a single generation strategy will be obsolete within a quarter. Your durable competitive advantage is the model-agnostic pipeline infrastructure — the audit gates, retry ladders, atlas packing, and headless validation — not the generation method. But "wait-and-adapt" doesn't mean "do nothing on generation." It means building the adapter layer *now* so you can run all three approaches concurrently and let empirical quality data pick the winner per animation type.

---

## I. Current Model Landscape Assessment (February 2026)

### Image Generation Models for Sprites

| Model | Strengths for Your Use Case | Limitations |
|---|---|---|
| **Gemini 2.0 Flash (Nano Banana Pro)** | Your proven workhorse. Dual-reference approach works for static poses. Available via Vertex AI. [3] | Cannot reliably differentiate sequential limb positions across frames via text description alone. |
| **Retro Diffusion rd-animation** (Replicate) | Purpose-built for pixel art sprite sheets. Grid-aligned, pixel-perfect output. Walk cycle styles available. 3+ years of pixel art specialization. [4][5] | Limited to preset animation styles (e.g., `four_angle_walking`). Smaller resolutions (48×48 typical). May not match your 128×128 SF2 aesthetic. Developer notes walk cycle model "nearly released" as of early 2026. [6] |
| **FLUX Kontext Max/Dev** | Strong character consistency across edits. Enterprise-grade prompt adherence. [7] | Not pixel-art-native. Requires post-processing. No animation-specific modes. |

### Video Generation Models for Interpolation

| Model | Key Capability | Relevance |
|---|---|---|
| **Kling 3.0** (Feb 5, 2026) | Multi-shot storyboarding (up to 6 cuts), 15s duration, Elements 3.0 character lock via 3-8s reference video, start/end frame control [1][2] | *Highest potential for your hybrid pipeline.* Start/end frame + character reference could solve the walk cycle problem directly. |
| **Kling 2.6** | Motion control via reference video transfer, start/end frame logic, strong prompt adherence [1] | Motion control feature is specifically useful — transfer a *known-good* walk cycle motion onto your generated character. |
| **Pika 2.2 (Pikaframes)** via fal.ai | Multi-keyframe interpolation (up to 5 keyframes), Pikascenes for character/wardrobe/setting control [10][11] | *Directly maps to your keyframe-to-interpolation architecture.* 5 keyframes = enough anchors for a full walk cycle. API available through fal.ai. |
| **Google Veo 2/3** | Excellent motion understanding, cinematography control, up to 4K. Veo 2 has been tested for pixel art walk cycles. [13][14] | Reddit users report resolution mismatch: Veo generates at much higher resolution than pixel art needs, creating anti-aliased/angled pixels that don't work at target resolution. "Every pixel counts" at 64-128px. [13] |
| **Wan 2.5** (Open source) | Strong character trait restoration, I2V capabilities, open source (runnable locally or via Replicate/Higgsfield) [16][17] | Open-source = no vendor lock-in. Good fallback option. Character fidelity is strong. |

### Integrated Platforms

**Scenario.com** offers a unified interface to 140+ models including Kling, Veo, and custom-trained models with workflow pipelines [18][19]. **Dzine AI** similarly aggregates Kling 3.0, Kling 2.6, Hailuo, and Nano Banana Pro [1]. These could serve as your initial adapter layer before building custom integrations.

---

## II. Architecture: The Generator Adapter Layer

### Design Pattern: Factory + Adapter + Strategy

Your adapter layer should implement three well-established patterns working together [20][21]:

```
┌─────────────────────────────────────────────────────────┐
│                    MANIFEST (YAML/JSON)                  │
│  character: ryu_clone                                    │
│  animation: walk_cycle                                   │
│  strategy: hybrid_keyframe_video                         │
│  generator:                                              │
│    keyframe_model: gemini-flash-nano-banana               │
│    interpolation_model: kling-3.0                        │
│    fallback_interpolation: pika-pikaframes-2.2           │
│  audit:                                                  │
│    identity_threshold: 0.92                              │
│    palette_max_colors: 24                                │
│    drift_tolerance_px: 2                                 │
│    alpha_artifact_max: 0.01                              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              GENERATION STRATEGY ROUTER                  │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ ImageOnly    │  │ HybridKV     │  │ DirectVideo    │  │
│  │ Strategy     │  │ Strategy     │  │ Strategy       │  │
│  │              │  │              │  │ (future)       │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│         ▼                ▼                   ▼           │
│  ┌─────────────────────────────────────────────────┐     │
│  │         GENERATOR ADAPTER INTERFACE             │     │
│  │                                                 │     │
│  │  generateFrame(ref, pose, opts) → Frame         │     │
│  │  generateKeyframes(ref, poses[]) → Frame[]      │     │
│  │  interpolateFrames(start, end, n) → Frame[]     │     │
│  │  generateVideo(ref, motion, opts) → Video       │     │
│  │  extractFrames(video, fps) → Frame[]            │     │
│  │                                                 │     │
│  └─────────────────────────────────────────────────┘     │
│         │          │          │         │                 │
│  ┌──────┴──┐ ┌─────┴────┐ ┌──┴─────┐ ┌┴──────────┐     │
│  │ Gemini  │ │ Kling    │ │ Pika   │ │ RetroDiff │     │
│  │ Adapter │ │ Adapter  │ │ Adapter│ │ Adapter   │     │
│  └─────────┘ └──────────┘ └────────┘ └───────────┘     │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              POST-PROCESSING PIPELINE                    │
│                                                          │
│  Video Frame Extraction (ffmpeg)                         │
│       ↓                                                  │
│  Pixel Art Quantization (palette lock, 24-color max)     │
│       ↓                                                  │
│  Temporal Smoothing (static region lock)                 │
│       ↓                                                  │
│  Background Removal / Alpha Cleanup                      │
│       ↓                                                  │
│  Resolution Normalization (→ 128×128 / 256×256)          │
│       ↓                                                  │
│  Bold Outline Enforcement                                │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  AUDIT GATE BATTERY                       │
│                                                          │
│  ✓ Identity Consistency (CLIP/SSIM vs anchor)            │
│  ✓ Palette Fidelity (max color count, Euclidean dist)    │
│  ✓ Baseline Drift (centroid/bounding box stability)      │
│  ✓ Alpha Artifacts (edge bleeding, halo detection)       │
│  ✓ Frame-to-Frame Continuity (optical flow magnitude)    │
│  ✓ Pixel Grid Alignment (sub-pixel detection)            │
│                                                          │
│  FAIL → Retry Ladder (re-generate → re-interpolate →     │
│         swap model → swap strategy → flag for manual)    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              ATLAS PACKING & VALIDATION                   │
│                                                          │
│  TexturePacker CLI (MaxRects, trim, alias detection)     │
│       ↓                                                  │
│  Phaser 3 Headless Validation                            │
│  (load atlas → play animation → assert frame count,      │
│   timing, no missing frames, bounds checking)            │
│       ↓                                                  │
│  Export: .png atlas + .json metadata                     │
└─────────────────────────────────────────────────────────┘
```

### Key Adapter Interface Design Decisions

**1. Four atomic operations, not one monolithic call:**

```typescript
interface GeneratorAdapter {
  // Single frame from reference + pose description
  generateFrame(config: FrameGenConfig): Promise<GeneratedFrame>;
  
  // Multiple keyframes (batch optimization possible)
  generateKeyframes(config: KeyframeGenConfig): Promise<GeneratedFrame[]>;
  
  // Interpolate between two or more anchor frames
  interpolateFrames(config: InterpolationConfig): Promise<GeneratedFrame[]>;
  
  // Full video generation from reference + motion description
  generateVideo(config: VideoGenConfig): Promise<GeneratedVideo>;
}

interface PostProcessor {
  // Extract individual frames from video at target FPS
  extractFrames(video: GeneratedVideo, config: ExtractionConfig): Promise<RawFrame[]>;
  
  // Apply pixel art post-processing pipeline
  pixelArtify(frame: RawFrame, config: PixelArtConfig): Promise<ProcessedFrame>;
}
```

**2. Strategy objects compose adapters, not inherit from them:**

Each strategy (ImageOnly, HybridKV, DirectVideo) is a separate orchestrator that calls adapter methods in different sequences. This means adding a new strategy (e.g., "RetroOnly" using rd-animation directly) requires zero changes to existing adapters.

**3. The manifest declares intent, not implementation:**

```yaml
animations:
  walk_cycle:
    frames: 8
    loop: true
    strategy_preference: [hybrid_keyframe_video, image_only]
    keyframe_indices: [0, 2, 4, 6]  # Which frames are "anchor" keyframes
    interpolation_frames: [1, 3, 5, 7]  # Which are interpolated
    pose_descriptions:
      0: "standing, weight on right foot, left foot forward beginning step"
      1: "mid-stride, left foot passing right, body centered"
      # ...
```

---

## III. The Three Strategies: Where to Invest Testing Time

### Strategy A: Image-Only Pipeline (20% of testing time)

**When it works:** Idle poses, single-hit attacks, special moves with distinct keyframes, victory poses — any animation where frames are visually *different enough* that text description can disambiguate them.

**Your known failure mode:** Walk cycles. Text can't reliably say "left leg is 15° further forward than frame 3." This is inherent to the text-to-image paradigm and unlikely to be solved by model improvements alone.

**Investment rationale:** You already have this working. Keep it as the fallback strategy. Your retry ladder already handles its variance. The main investment here is *expanding your pose reference library* — pre-generating or hand-crafting canonical pose reference images for each frame position, which your Gemini dual-reference approach can then match against.

**Concrete improvement:** Instead of text-only pose differentiation, generate a *skeleton pose reference* image for each frame (even a simple stick figure at the target pose) and pass it as the pose reference alongside the character anchor. This visual disambiguation may be more reliable than text for subtle positional differences.

### Strategy B: Hybrid Keyframe-to-Video (60% of testing time)

**This is where the action is.** Three specific model capabilities make this viable *right now* in Feb 2026:

1. **Pika Pikaframes 2.2** — Upload up to 5 keyframes and interpolate smooth motion between them [11]. This is *exactly* your use case. Generate frames 0, 2, 4, 6 of a walk cycle with your proven Gemini approach, feed them to Pikaframes, extract the interpolated frames 1, 3, 5, 7.

2. **Kling 3.0 Start/End Frames + Elements** — Lock character identity with a 3-8s reference video, set start and end frame images, and let the model calculate the motion path between them [1][2]. Generate your extreme poses (contact pose and passing pose) with Gemini, then have Kling fill in the breakdowns.

3. **Kling 2.6 Motion Control** — Upload a *reference video of a walk cycle* (from any source — even a generic sprite walk cycle) and transfer that motion pattern onto your character [1]. This could be the most powerful approach: maintain a library of "canonical motion" reference videos and apply them to each character.

**The critical post-processing pipeline for video-to-pixel-art:**

The proven pipeline from practitioners [23] is:

```
AI Video (MP4) 
  → ffmpeg frame extraction
  → Color quantization (force to N-color palette, no dithering)
  → Temporal smoothing (detect static regions, lock to mode color)
  → Resolution downscale to target (128×128)  
  → Grid alignment enforcement
  → Bold outline re-application
  → Alpha channel reconstruction
```

The Veo pixel art experiments on Reddit confirmed the core challenge: video models generate at much higher resolution than pixel art needs, and the intermediate pixels created by anti-aliasing "would never work" in a pixel art environment [13]. Your post-processing pipeline must be aggressive about re-quantization and grid snapping. This is non-trivial but deterministic — invest in making it robust.

**Specific test matrix to run:**

| Test | Keyframe Source | Interpolation Model | Post-Processing | Metric |
|---|---|---|---|---|
| B1 | Gemini (4 keyframes) | Pika Pikaframes 2.2 | Full pixel art pipeline | Audit pass rate |
| B2 | Gemini (2 keyframes) | Kling 3.0 start/end | Full pixel art pipeline | Audit pass rate |
| B3 | Gemini (1 keyframe) | Kling 2.6 motion transfer | Full pixel art pipeline | Audit pass rate |
| B4 | Retro Diffusion (4 keyframes) | Pika Pikaframes 2.2 | Minimal (already pixel art) | Audit pass rate |
| B5 | Gemini (4 keyframes) | Wan 2.5 I2V (open source) | Full pixel art pipeline | Audit pass rate |

Run each test across 3 animation types: walk cycle, punch, and jump. That's 15 experiments. Grade on your existing audit gates. This will tell you which combination actually works for your spec.

### Strategy C: Wait-and-Adapt Infrastructure (20% of testing time, but 60% of *engineering* time)

**This is the durable investment.** Everything below the generation layer is model-agnostic and will survive any model transition:

1. **Post-processing pipeline** — Color quantization, temporal smoothing, grid alignment, outline enforcement, alpha cleanup. This is needed by *every* generation approach and is deterministic code you control.

2. **Audit gate battery** — Identity consistency, palette fidelity, baseline drift, alpha artifacts. Add a new gate: **frame-to-frame optical flow magnitude** — for walk cycles, the optical flow between consecutive frames should follow a predictable sinusoidal pattern. Anomalous flow = interpolation artifact.

3. **Retry ladder with strategy escalation** — Current: retry same model. Add: swap interpolation model → swap generation strategy → flag for manual review. The retry ladder should be able to fall back from HybridKV to ImageOnly transparently.

4. **TexturePacker CLI integration** — Already well-supported for automation. Use MaxRects packing, enable trim (transparent area removal) and alias detection (identical frame dedup). TexturePacker's smart-update hash system means re-running only rebuilds when sprites change [24][25].

5. **Phaser 3 headless validation** — Load the generated atlas + JSON metadata, create the animation, assert: correct frame count, no missing frames, bounding box within expected dimensions, animation plays without visual glitches. Phaser supports `addSpriteSheetFromAtlas` for testing atlas-based animations programmatically [26][27].

6. **Telemetry and model comparison dashboards** — Log every generation attempt: model used, strategy, prompt hash, audit pass/fail per gate, latency, cost. This data becomes your decision engine for which models to promote to production.

---

## IV. Recommended Phasing

### Phase 1: Foundation (Now → March 2026)

- **Ship the adapter interface** with Gemini (image-only) and one video model (start with Pika Pikaframes via fal.ai — cleanest API for keyframe interpolation [11]).
- **Build the post-processing pipeline** end-to-end: video extraction → pixel art conversion → audit → TexturePacker → Phaser validation.
- **Run the B1 and B2 test matrix** to get your first empirical data on hybrid pipeline quality.
- **Implement the manifest schema** with strategy declarations per animation type.

### Phase 2: Model Expansion (March → April 2026)

- **Add Kling 3.0 adapter** (likely available via API by then, currently Ultra subscriber early access [2]).
- **Add Kling 2.6 motion control adapter** — build a reference motion video library for canonical fighting game animations.
- **Add Retro Diffusion rd-animation adapter** via Replicate API [4] — test whether purpose-built pixel art animation bypasses the post-processing bottleneck entirely.
- **Run full test matrix** (B1-B5) and promote best-performing combinations per animation type.

### Phase 3: Intelligence (May → June 2026)

- **Implement strategy auto-selection** — the manifest declares animation *type*, the system picks the best strategy based on accumulated quality telemetry.
- **Build the retry ladder with cross-strategy fallback** — if hybrid fails audit 3 times, automatically attempt image-only with enriched pose references.
- **Evaluate Kling 3.0 Omni's multi-shot storyboard** for generating entire animation sequences as a single request (6 shots = 6 keyframes of a complex animation) [1].
- **Re-evaluate the landscape** — by Q2 2026, new models will exist that we can't predict today. Your adapter layer should be able to integrate a new model in < 1 day of engineering work.

---

## V. Key Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Video-to-pixel-art post-processing destroys motion quality | High | High | Invest heavily in temporal smoothing. Lock static regions. Use the Sarthak Mishra pattern [23]: color quantization + mode-color static masking + change threshold tuning. |
| Video models can't maintain character identity at pixel art scale | Medium | High | Kling 3.0 Elements (reference video lock) + aggressive post-processing palette lock should help. If identity drifts, fall back to image-only with manual pose references. |
| API cost blowup from retry ladders | Medium | Medium | Set per-animation cost caps in manifest. Track cost-per-approved-frame metric. Prefer Wan 2.5 (open source, self-hostable) for high-retry animations. |
| Model API deprecation / breaking changes | High | Low (if adapter layer exists) | The entire point of the adapter pattern. One adapter swap, zero pipeline changes. |
| Pixel grid misalignment from interpolated frames | High | Medium | Post-processing must include explicit grid-snap pass. Quantize to nearest pixel grid, then re-apply outlines. Consider generating at 2× target resolution and downscaling with nearest-neighbor. |

---

## VI. Bottom Line

**Don't pick one strategy. Architect for all three and let data decide.**

Your unique value isn't in calling AI APIs — anyone can do that. It's in the **quality enforcement pipeline** that turns unreliable AI output into production-ready game assets. Every hour spent on audit gates, temporal smoothing, palette enforcement, and headless validation compounds in value regardless of which model generates the raw frames.

The hybrid keyframe-to-video approach (Strategy B) is the most promising for walk cycles *today*, particularly Pika Pikaframes 2.2 (5-keyframe interpolation) and Kling 3.0 (start/end frame + character lock). But the model that solves this best in June 2026 may not exist yet. Build the socket, not the plug.