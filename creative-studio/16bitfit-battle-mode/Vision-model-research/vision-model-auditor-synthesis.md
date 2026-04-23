# Vision Model Auditor — Research Synthesis & Implementation Spec
## For: 16BitFit Battle Mode Sprite Pipeline
**Created:** 2026-04-05
**Sources:** Perplexity Deep Research (Prompts 1 & 3) + Gemini Deep Research (Prompt 2)
**Purpose:** Feed this file + SOURCE-OF-TRUTH.md to Claude Code when building the VLM Auditor integration.

---

## 1. Executive Summary

Three independent deep research runs converge on one clear conclusion: **the auditor should NOT be a single vision model.** It should be a tiered pipeline where each layer uses the right tool for the job. Pixel-perfect checks (palette, alpha, baseline) stay algorithmic. Identity consistency upgrades from SSIM to **DINOv2**. And a **Vision-Language Model (VLM)** handles the tasks algorithms can't: anatomy verification, style consistency scoring, and generating natural language retry feedback for the prompt modifier.

**The winning stack:**

| Layer | Tool | Runs On | Latency | What It Does |
|-------|------|---------|---------|-------------|
| 1. Hard Gates | Sharp + custom scripts (existing) | Any machine | <100ms/frame | HF01-HF05: dimensions, alpha, corruption, color depth, file size |
| 2. Identity Scoring | **DINOv2** (replaces SSIM as primary) | Alienware GPU or MacBook CPU | <1s/frame | Cosine similarity vs anchor → 0.0-1.0 identity score |
| 3. Palette + Alpha + Baseline | Sharp + OpenCV scripts (existing) | Any machine | <200ms/frame | SF02 palette fidelity, SF05 alpha halos, baseline drift — all deterministic |
| 4. VLM Judge | **Qwen2.5-VL-7B** (local) | Alienware RTX 5080 | 2-5s/frame | HF05 anatomy, SF03 style consistency, semantic retry feedback |
| 5. Escalation Judge (optional) | **Gemini 2.5 Flash** (API) | Cloud | 2-4s/frame | Borderline cases the local model flags as uncertain |

**Why this architecture wins:**
- Layers 1-3 are instant, free, and deterministic — they handle ~80% of quality checks
- Layer 4 runs locally on hardware you already own — $0/frame
- Layer 5 is cheap ($0.0003-$0.001/frame) and only fires on edge cases
- Total per-frame audit: **3-8 seconds** (within NFR2 budget when accounting for the VLM addition)

---

## 2. Key Convergence Points (All 3 Sources Agree)

### 2.1 VLMs Cannot Replace Algorithmic Checks
All three sources are emphatic: VLMs are bad at pixel-level precision. Palette hex matching, alpha gradient analysis, baseline Y-coordinate measurement, and exact dimension verification must remain in deterministic code. A VLM asked to "count colors" or "measure pixel offset" will hallucinate. This validates the existing pipeline architecture — the Sharp-based hard gates and soft metric scripts stay exactly as built.

### 2.2 DINOv2 Should Replace SSIM as Primary Identity Metric
This is the single biggest upgrade the research recommends. SSIM is "notoriously brittle" for generative pixel art — a perfect sprite shifted by 1px causes catastrophic SSIM score drops, creating massive false negatives. DINOv2 (Meta's self-supervised Vision Transformer) understands spatial structure, part-to-part correspondence, and pose-invariant identity matching at the patch level. It scores 64% on fine-grained similarity tasks where CLIP scores 28%.

**Implementation change:** DINOv2 cosine similarity becomes the primary SF01 identity score. SSIM remains as a secondary/validation metric, not the gating signal. The SOT already lists "DINOv2" in the Phase 5 upgraded metrics — this confirms it should be prioritized.

**How it works technically:**
1. Extract feature embeddings from the anchor image using DINOv2's frozen ViT encoder
2. Extract feature embeddings from the candidate frame
3. Compute cosine similarity between the two embedding vectors
4. Score = cosine similarity (already 0.0-1.0 range)
5. Threshold: ≥0.90 (same as current SF01 DINO target in PRD)

**Model:** `facebook/dinov2-base` (86M params) or `facebook/dinov2-small` (22M params). Runs in <500ms on CPU, <100ms on GPU. No VRAM concerns.

### 2.3 Qwen2.5-VL-7B Is the Consensus Local VLM
All three sources independently recommend Qwen2.5-VL-7B as the top choice for local deployment on your hardware:
- **Dynamic resolution** — encodes images at actual pixel scale without aggressive downsampling
- **Native multi-image input** — can compare candidate vs. reference in a single call
- **Native JSON structured output** — returns scores in parseable format without prompt gymnastics
- **Mature ecosystem** — Ollama, MLX-VLM, vLLM, llama.cpp GGUF all supported
- **Well-documented fine-tuning** — LoRA/QLoRA validated on RTX 4070 12GB (your 5080 has more headroom)
- **4-bit quantization** — ~8GB VRAM, runs at ~100-130 tok/s on RTX 5080

**Note on Qwen3-VL-7B (currently in SOT):** The SOT designates Qwen3-VL-7B for sprite vision QA. The Perplexity benchmark research confirms Qwen3-VL exists and has improved spatial encoding. However, the local deployment research found Qwen2.5-VL-7B has a dramatically more mature toolchain (MLX-VLM, Ollama, fine-tuning docs, GGUF conversions). **Recommendation: Start with Qwen2.5-VL-7B for proven tooling, upgrade to Qwen3-VL-7B when its local deployment ecosystem catches up.** Both share the same adapter interface, so swapping is trivial.

### 2.4 Gemini 2.5 Flash Is the Best Cloud Escalation Model
When the local VLM flags a frame as uncertain (e.g., anatomy score between 0.6-0.8), escalate to Gemini 2.5 Flash via API. At $0.30/1M input tokens and 206 tok/s output, it's the best accuracy-per-dollar option. Its 1M context window means you can send the anchor + candidate + style guide + full rubric in a single call. For cases requiring the deepest reasoning (o4-mini "thinks with images"), that's the nuclear option at $1.10/1M input.

### 2.5 Fine-Tuning Closes the API vs. Local Gap
The most actionable finding: a fine-tuned 8B model matched models 30x its size on specialized visual tasks. The strategy:
1. Use Gemini 2.5 Flash to label 200-500 sprite examples across quality criteria
2. Fine-tune Qwen2.5-VL-7B with QLoRA on the RTX 5080
3. The fine-tuned local model matches frontier API quality for your specific rubric
4. Total fine-tuning cost: ~$50-100 (API labeling) + ~1 day compute

This is a Phase 5+ optimization — start with zero-shot prompting, collect labeled data from production runs, then fine-tune.

### 2.6 Upscale Before VLM Analysis
128×128 sprites are below the resolution distribution all VLMs were trained on. All sources agree: **nearest-neighbor upscale to 512×512 before sending to any VLM**. This preserves sharp pixel art edges while giving the model more tokens per pixel to reason about. Additionally, composing a side-by-side image (reference left, candidate right, 4px separator) forces explicit visual comparison.

---

## 3. What the VLM Actually Evaluates

The VLM handles exactly three jobs that algorithms can't:

### 3.1 HF05: Gross Anatomy Verification (Pass/Fail)
- Is the character's silhouette anatomically correct?
- Are all limbs present (no missing arms/legs)?
- No extra appendages or catastrophic deformation?
- Is the character facing the correct direction?

**Why VLM:** Algorithms can measure silhouette area and bounding box ratios, but they can't determine if a shape is "a person" vs "a blob." The VLM provides semantic understanding of anatomy.

**Research insight (Gemini):** VLMs achieve ~82.8% accuracy on glitch detection but struggle with subtle body configuration errors. The "Beyond the Pixels" hierarchical approach improves this: decompose the check into binary sub-questions ("Is the left arm present?" → "Is the right arm present?" → "Are the legs below the torso?") rather than asking holistically.

### 3.2 SF03: Style Consistency Scoring (0.0-1.0)
- Line weight: Are outlines consistently 1-2px thick?
- Shading: Flat cel-shading (correct) vs. soft gradients (incorrect)?
- Overall aesthetic: Does it match 16-bit arcade fighter conventions?

**Why VLM:** Algorithms can detect anti-aliasing and gradient presence, but evaluating "does this look like Street Fighter II" requires semantic understanding of artistic conventions.

### 3.3 Semantic Retry Feedback (Natural Language)
When a frame fails any gate, the VLM generates specific, actionable text that maps to prompt modifications:
- "The character's left arm is missing below the elbow"
- "The outline on the legs is 3px thick instead of the expected 1px"
- "The shading uses soft gradients instead of flat cel-shading"

**Why VLM:** This is the unique capability no algorithm can replicate. The retry ladder currently uses reason codes to select strategies — the VLM adds semantic detail that makes prompt modifications targeted rather than generic.

---

## 4. Prompting Strategy: Chain-of-Rubrics (CoR)

All three sources converge on structured rubric-based prompting over holistic scoring. Here is the production prompt template:

### 4.1 Anatomy Check Prompt (HF05)
```
You are a quality assurance inspector for a 2D fighting game sprite pipeline.

REFERENCE IMAGE (left): The approved anchor sprite for this character.
CANDIDATE IMAGE (right): A newly generated animation frame to evaluate.

Perform a structural anatomy check by answering each question with YES or NO, then provide a brief justification:

1. SILHOUETTE: Is the character's overall silhouette recognizable as a humanoid fighter?
2. HEAD: Is the head present, properly positioned on the torso, and proportional?
3. LEFT ARM: Is the left arm present and attached to the torso?
4. RIGHT ARM: Is the right arm present and attached to the torso?
5. LEFT LEG: Is the left leg present and extends downward from the torso?
6. RIGHT LEG: Is the right leg present and extends downward from the torso?
7. FACING: Is the character facing RIGHT (the correct direction)?
8. PROPORTION: Are the head-to-body proportions consistent with the reference?

Respond in this exact JSON format:
{
  "silhouette": { "pass": true/false, "note": "brief explanation" },
  "head": { "pass": true/false, "note": "brief explanation" },
  "left_arm": { "pass": true/false, "note": "brief explanation" },
  "right_arm": { "pass": true/false, "note": "brief explanation" },
  "left_leg": { "pass": true/false, "note": "brief explanation" },
  "right_leg": { "pass": true/false, "note": "brief explanation" },
  "facing": { "pass": true/false, "note": "brief explanation" },
  "proportion": { "pass": true/false, "note": "brief explanation" },
  "overall_pass": true/false,
  "feedback": "If any check failed, describe WHAT is wrong and WHERE on the character."
}
```

### 4.2 Style Consistency Prompt (SF03)
```
You are a pixel art style evaluator for a 16-bit arcade fighting game (Street Fighter II aesthetic).

REFERENCE IMAGE (left): The approved anchor sprite establishing the target style.
CANDIDATE IMAGE (right): A generated frame to evaluate for style consistency.

Score each criterion from 1 (worst) to 5 (best). Provide brief reasoning BEFORE each score.

CRITERIA:
1. OUTLINE_WEIGHT: Are character outlines bold, dark (#272929), and consistently 1-2 pixels thick? (1 = no visible outlines or wildly inconsistent, 5 = perfectly consistent bold outlines)
2. SHADING_STYLE: Is shading flat/cel-shaded with hard edges? (1 = soft gradients or airbrushed, 5 = crisp flat shading matching the reference)
3. DETAIL_FIDELITY: Are costume details (belt, armor, accessories) present and matching the reference? (1 = major details missing, 5 = all details accurately recreated)
4. PIXEL_CLEANLINESS: Are pixels crisp without anti-aliasing artifacts or blurry edges? (1 = heavily anti-aliased/blurry, 5 = pixel-perfect crispness)
5. AESTHETIC_MATCH: Does the overall visual language match classic 16-bit arcade fighter conventions? (1 = looks like modern digital art, 5 = indistinguishable from authentic retro sprites)

Respond in this exact JSON format:
{
  "outline_weight": { "reasoning": "...", "score": 1-5 },
  "shading_style": { "reasoning": "...", "score": 1-5 },
  "detail_fidelity": { "reasoning": "...", "score": 1-5 },
  "pixel_cleanliness": { "reasoning": "...", "score": 1-5 },
  "aesthetic_match": { "reasoning": "...", "score": 1-5 },
  "composite_score": 0.0-1.0,
  "feedback": "If any score is 2 or below, describe specifically what needs to change."
}

SCORING RULE: composite_score = (sum of all scores) / 25.0
If ANY individual score is 2 or below, the frame should be flagged for retry regardless of composite.
```

### 4.3 Retry Feedback Prompt (on failure)
```
A sprite frame has failed quality checks. Generate specific retry guidance.

CHARACTER: {{character_name}}
ANIMATION: {{animation_name}}
FRAME: {{frame_index}}

FAILURES DETECTED:
{{failure_list}}

ALGORITHMIC DATA:
- DINOv2 identity score: {{dino_score}} (threshold: 0.90)
- Palette fidelity: {{palette_pct}}% (threshold: 90%)
- Baseline drift: {{drift_px}}px (threshold: 1px)
- Alpha halo severity: {{halo_score}} (threshold: 0.3)

Based on the failures above and the comparison images, write a concise prompt modification instruction. Be specific about:
1. WHAT is wrong (e.g., "left arm missing", "outline too thick on legs")
2. WHERE on the character (e.g., "below the elbow", "around the feet")
3. HOW to fix it in the generation prompt (e.g., "add explicit instruction for visible left forearm")

Respond in JSON:
{
  "primary_issue": "one-sentence summary of the main problem",
  "prompt_addition": "exact text to append to the generation prompt",
  "prompt_removal": "exact text to remove from the generation prompt (if applicable)",
  "confidence": "HIGH/MEDIUM/LOW",
  "escalate_to_api": true/false
}
```

---

## 5. Architecture: VLM Auditor Adapter

### 5.1 Where It Fits in the Pipeline

The VLM evaluator plugs into the existing Auditor (Epic 3) as a new evaluator alongside the existing hard gates and soft metrics. It does NOT replace them — it extends them.

```
Candidate Frame
    ↓
[1] Frame Normalization (existing — Sharp)
    ↓
[2] Hard Gate Evaluators HF01-HF04 (existing — deterministic)
    ↓  (if all pass)
[3] DINOv2 Identity Score (NEW — replaces SSIM as primary SF01)
    ↓
[4] Palette + Alpha + Baseline (existing — deterministic SF02, SF05, baseline)
    ↓
[5] VLM Anatomy Check (NEW — HF05, pass/fail)
    ↓  (if pass)
[6] VLM Style Score (NEW — SF03, 0.0-1.0)
    ↓
[7] Composite Scoring + Retry Decision (existing RetryManager)
    ↓  (if retry needed)
[8] VLM Retry Feedback (NEW — generates prompt modification)
    ↓
[RetryManager selects strategy + appends VLM feedback to prompt]
```

**Key design decision:** The VLM steps (5, 6, 8) only fire if the frame passes the fast deterministic checks (1-4). This means ~80% of obviously bad frames are rejected in <500ms without touching the VLM at all. The VLM only evaluates frames that are "close to passing" — exactly where its semantic understanding adds value.

### 5.2 Adapter Interface

Following the hexagonal architecture, the VLM is behind a typed adapter:

```typescript
// src/adapters/vlm/VlmAuditorPort.ts
interface VlmAuditorPort {
  /** HF05: Binary anatomy pass/fail with sub-checks */
  checkAnatomy(
    candidate: NormalizedFrame,
    anchor: AnchorImage,
    character: CharacterSpec
  ): Promise<AnatomyResult>;

  /** SF03: Style consistency score 0.0-1.0 */
  scoreStyle(
    candidate: NormalizedFrame,
    anchor: AnchorImage,
    styleGuide: StyleSpec
  ): Promise<StyleResult>;

  /** Generate semantic retry feedback from failure data */
  generateRetryFeedback(
    candidate: NormalizedFrame,
    anchor: AnchorImage,
    failures: AuditFailure[],
    metrics: AuditMetrics
  ): Promise<RetryFeedback>;
}

// Result types
interface AnatomyResult {
  overallPass: boolean;
  checks: Record<string, { pass: boolean; note: string }>;
  feedback: string | null;
  latencyMs: number;
}

interface StyleResult {
  compositeScore: number;  // 0.0-1.0
  scores: Record<string, { reasoning: string; score: number }>;
  feedback: string | null;
  flagForRetry: boolean;  // true if any sub-score ≤ 2
  latencyMs: number;
}

interface RetryFeedback {
  primaryIssue: string;
  promptAddition: string;
  promptRemoval: string | null;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  escalateToApi: boolean;
  latencyMs: number;
}
```

### 5.3 Adapter Implementations

Two adapter implementations, same interface:

```typescript
// Local adapter — Qwen2.5-VL-7B via Ollama REST API
// src/adapters/vlm/OllamaVlmAdapter.ts
class OllamaVlmAdapter implements VlmAuditorPort { ... }

// Cloud adapter — Gemini 2.5 Flash via @google/genai SDK
// src/adapters/vlm/GeminiVlmAdapter.ts  
class GeminiVlmAdapter implements VlmAuditorPort { ... }
```

The manifest controls which adapter is used:

```yaml
# manifest.yaml
auditor:
  vlm:
    primary: "ollama"          # "ollama" | "gemini"
    model: "qwen2.5-vl:7b-q4"
    endpoint: "http://alienware:11434"  # Ollama REST endpoint
    escalation:
      enabled: true
      model: "gemini-2.5-flash"
      trigger: "LOW_CONFIDENCE"  # escalate when VLM reports LOW confidence
    preprocessing:
      upscale_factor: 4          # 128→512 nearest-neighbor before VLM
      compose_side_by_side: true # reference|candidate in single image
    timeout_ms: 10000
```

---

## 6. DINOv2 Integration Spec

### 6.1 Why DINOv2 Over SSIM

| Metric | SSIM | DINOv2 |
|--------|------|--------|
| What it measures | Pixel-level luminance/contrast/structure | Semantic part-aware structural similarity |
| Pose sensitivity | Catastrophic — 1px shift kills score | Robust — understands same character in different pose |
| False negative rate | High for animation frames | Low — designed for pose-variant matching |
| Explainability | None (single number) | Patch-level attention maps available |
| Speed | <100ms | <500ms CPU, <100ms GPU |
| Pixel art suitability | Poor (assumes natural images) | Good (self-supervised, no domain assumptions) |

### 6.2 Implementation

```typescript
// src/adapters/identity/DinoV2Adapter.ts
// Uses @xenova/transformers (ONNX runtime) or Python subprocess

interface IdentityMetricPort {
  computeIdentityScore(
    candidate: NormalizedFrame,
    anchor: AnchorImage
  ): Promise<{ score: number; latencyMs: number }>;
}

class DinoV2Adapter implements IdentityMetricPort {
  // Model: facebook/dinov2-base (86M params, ~350MB)
  // Or: facebook/dinov2-small (22M params, ~88MB) for faster inference
  // Inference: Extract CLS token embeddings → cosine similarity
}
```

**SSIM is NOT removed** — it moves to a secondary validation role. The composite scoring weights update:

```yaml
# Updated from PRD
auditor:
  weights:
    identity_dino: 0.30    # was: identity (SSIM) 0.30
    identity_ssim: 0.05    # secondary validation
    stability: 0.30        # no change (was 0.35, rebalanced)
    palette: 0.15          # was 0.20, rebalanced
    style_vlm: 0.15        # NEW — VLM style score
    alpha: 0.05            # carved out from style 0.15
```

---

## 7. Hardware Deployment Map

### 7.1 Where Each Component Runs

| Component | Machine | Model/Tool | VRAM/RAM | Speed |
|-----------|---------|-----------|----------|-------|
| Hard gates (HF01-04) | Any (pipeline host) | Sharp scripts | <100MB | <100ms |
| DINOv2 identity | Alienware (GPU) | `dinov2-base` ONNX | ~500MB VRAM | <100ms |
| DINOv2 identity | MacBook (CPU fallback) | `dinov2-small` ONNX | ~200MB RAM | <500ms |
| Palette/Alpha/Baseline | Any (pipeline host) | Sharp + custom | <100MB | <200ms |
| VLM Judge (primary) | Alienware RTX 5080 | Qwen2.5-VL-7B Q4 via Ollama | ~8GB VRAM | 2-5s |
| VLM Judge (Mac fallback) | MacBook M4 Pro | Qwen2.5-VL-7B 4-bit via MLX-VLM | ~8GB unified | 4-8s |
| VLM Escalation | Cloud API | Gemini 2.5 Flash | N/A | 2-4s |

### 7.2 Ollama Setup (Alienware)
```bash
# Pull the model
ollama pull qwen2.5-vl:7b

# Or with specific quantization
ollama pull qwen2.5-vl:7b-q4_K_M

# Verify it runs
ollama run qwen2.5-vl:7b "Describe this image" --images test-sprite.png

# Expose to network (for pipeline on another machine)
# Set OLLAMA_HOST=0.0.0.0 in /etc/systemd/system/ollama.service
```

### 7.3 MLX-VLM Setup (MacBook — fallback)
```bash
pip install mlx-vlm

# Test inference
python -m mlx_vlm.generate \
  --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit \
  --image sprite.png \
  --prompt "Describe this sprite"

# For batch pipeline: use vllm-mlx for prefix caching (28x speedup on repeated reference images)
pip install vllm-mlx
```

### 7.4 Image Preprocessing Before VLM

```typescript
// src/adapters/vlm/preprocessing.ts
import sharp from 'sharp';

async function prepareForVlm(
  candidate: Buffer,
  anchor: Buffer,
  canvasSize: number  // 128 or 256
): Promise<Buffer> {
  const upscaleFactor = 4;  // 128→512 or 256→1024
  const targetSize = canvasSize * upscaleFactor;
  const separator = 4;  // px gap between images

  const upscaledCandidate = await sharp(candidate)
    .resize(targetSize, targetSize, { kernel: sharp.kernel.nearest })
    .toBuffer();

  const upscaledAnchor = await sharp(anchor)
    .resize(targetSize, targetSize, { kernel: sharp.kernel.nearest })
    .toBuffer();

  // Compose side-by-side: [anchor | 4px gap | candidate]
  const compositeWidth = targetSize * 2 + separator;
  return sharp({
    create: {
      width: compositeWidth,
      height: targetSize,
      channels: 4,
      background: { r: 128, g: 128, b: 128, alpha: 255 }
    }
  })
    .composite([
      { input: upscaledAnchor, left: 0, top: 0 },
      { input: upscaledCandidate, left: targetSize + separator, top: 0 }
    ])
    .png()
    .toBuffer();
}
```

---

## 8. Cost Estimates

### 8.1 Per-Frame Cost (Local Primary)

| Step | Cost | Notes |
|------|------|-------|
| Hard gates + palette + alpha + baseline | $0.00 | Runs on pipeline host CPU |
| DINOv2 identity | $0.00 | Runs on Alienware GPU |
| VLM anatomy + style (Qwen2.5-VL-7B local) | $0.00 | Runs on Alienware GPU |
| VLM retry feedback (if needed) | $0.00 | Same local model |
| **Total per frame (no escalation)** | **$0.00** | |

### 8.2 Per-Frame Cost (With API Escalation)

| Step | Cost | Notes |
|------|------|-------|
| All local steps | $0.00 | |
| Gemini 2.5 Flash escalation | ~$0.0003-$0.001 | Only fires on borderline frames |
| **Estimated escalation rate** | **~10-15%** of frames | Based on pipeline retry rates |

### 8.3 Full Roster Projection

| Scenario | Frames | Local Cost | API Escalation Cost | Total |
|----------|--------|-----------|-------------------|-------|
| MVP (1 char × 2 anims) | ~12 | $0.00 | ~$0.01 | ~$0.01 |
| v1 (1 char × 15 anims) | ~120 | $0.00 | ~$0.05 | ~$0.05 |
| Full roster (12 × 13 anims) | ~1,200 | $0.00 | ~$0.50 | ~$0.50 |

---

## 9. Manifest Configuration Additions

```yaml
# Additions to manifest.yaml schema for VLM auditor
auditor:
  # Existing hard_gates and soft_metrics unchanged

  # NEW: Identity metric configuration
  identity:
    primary: "dinov2"           # "dinov2" | "ssim" (fallback)
    model: "dinov2-base"        # "dinov2-base" (86M) | "dinov2-small" (22M)
    threshold: 0.90             # Same as existing SF01 target
    ssim_secondary: true        # Also compute SSIM as validation
    ssim_threshold: 0.85        # Same as existing

  # NEW: VLM evaluator configuration
  vlm:
    enabled: true               # Can disable for fast runs
    primary_backend: "ollama"   # "ollama" | "mlx" | "gemini"
    model: "qwen2.5-vl:7b-q4_K_M"
    endpoint: "http://localhost:11434"  # or http://alienware:11434
    checks:
      anatomy: true             # HF05 pass/fail
      style: true               # SF03 scoring
      retry_feedback: true      # Generate semantic feedback on failure
    preprocessing:
      upscale_factor: 4
      compose_side_by_side: true
      background_color: "#808080"  # Neutral gray for composition gap
    timeout_ms: 10000
    escalation:
      enabled: true
      backend: "gemini"
      model: "gemini-2.5-flash"
      trigger: "LOW_CONFIDENCE"
      max_escalations_per_run: 10  # Budget cap
```

---

## 10. Implementation Phases

### Phase A: DINOv2 Integration (Do First — Lowest Risk, Highest Impact)
1. Install `@xenova/transformers` or set up Python subprocess for ONNX inference
2. Implement `DinoV2Adapter` behind `IdentityMetricPort`
3. Run against existing approved frames — compare DINOv2 scores to SSIM scores
4. Update composite scoring weights
5. **Gate check:** DINOv2 scores correlate with visual quality better than SSIM on test frames

### Phase B: VLM Adapter (Local Ollama)
1. Install Ollama + pull `qwen2.5-vl:7b` on Alienware
2. Implement image preprocessing (upscale + side-by-side composition)
3. Implement `OllamaVlmAdapter` with anatomy prompt
4. Run against existing approved + rejected frames — validate anatomy check accuracy
5. Add style scoring prompt
6. **Gate check:** VLM correctly identifies known-bad frames (missing limbs, wrong facing) with >90% accuracy

### Phase C: Retry Feedback Loop
1. Implement retry feedback prompt
2. Wire VLM feedback into RetryManager's prompt modification logic
3. Run end-to-end: generate → audit → VLM feedback → retry with modified prompt
4. **Gate check:** Retry attempts with VLM feedback produce higher-quality frames than retries without

### Phase D: Cloud Escalation (Optional)
1. Implement `GeminiVlmAdapter` using existing `@google/genai` SDK
2. Add escalation trigger logic (confidence < threshold → escalate)
3. Wire budget cap to prevent runaway API costs
4. **Gate check:** Escalated frames get resolved with fewer total retries

### Phase E: Fine-Tuning (Phase 5+)
1. Collect 200-500 labeled examples from production pipeline runs
2. Fine-tune Qwen2.5-VL-7B with QLoRA on RTX 5080
3. Replace base model with fine-tuned checkpoint
4. **Gate check:** Fine-tuned model matches Gemini 2.5 Flash accuracy on your specific rubric

---

## 11. Open Questions for Testing

1. **Qwen2.5-VL-7B vs Qwen3-VL-7B:** The SOT lists Qwen3-VL-7B. Research shows Qwen2.5-VL has more mature local tooling. Test both on 10 sprite pairs and compare JSON output quality before committing.

2. **DINOv2 base vs small:** The 86M model is more accurate but the 22M model is faster. For 128×128 upscaled sprites, the small model may be sufficient. Benchmark both.

3. **Side-by-side vs separate images:** Research recommends composing a single side-by-side image. Test whether sending anchor and candidate as separate images to the VLM produces better or worse results.

4. **Upscale factor:** 4x (128→512) is the minimum recommendation. Test 8x (128→1024) to see if additional resolution helps the VLM, at the cost of larger payloads.

5. **Anatomy check granularity:** The current prompt has 8 sub-checks. Test whether 4 broader checks (silhouette, upper body, lower body, facing) produce more reliable results with fewer false positives.

---

## 12. Research Sources Summary

| Source | Platform | Key Contribution |
|--------|----------|-----------------|
| Prompt 1 (Benchmarks) | Perplexity Deep Research | Ranked comparison tables, latency profiles, multi-image context limits, known pixel art weaknesses |
| Prompt 2 (QA Pipeline) | Gemini Deep Research | Tiered architecture design, CoR prompting framework, DINOv2 dominance over SSIM, "Beyond the Pixels" hierarchical VLM approach, VideoGameQA-Bench findings |
| Prompt 3 (Local Deployment) | Perplexity Deep Research | Hardware-specific deployment tables, VRAM requirements, MLX-VLM vs Ollama speed comparison, fine-tuning gap closure data, vllm-mlx prefix caching |

---

*This document synthesizes 3 deep research outputs (2 Perplexity, 1 Gemini). Feed to Claude Code alongside SOURCE-OF-TRUTH.md for implementation.*
