# Autoresearch Plan: 16BitFit Sprite Pipeline Optimization

**Date:** 2026-04-11
**Status:** DRAFT — Awaiting review before implementation

---

## Overview

Apply Karpathy's three-file autoresearch pattern to the 16BitFit sprite generation pipeline. The goal: autonomously optimize ComfyUI workflow parameters for style-consistent sprite generation using a trained LoRA, with automated scoring to keep/revert each experiment.

---

## Phase 1: LoRA Training (Prerequisite)

Before the optimization loop can run, we need a style LoRA trained on the existing sprite output.

### Dataset
- **Source:** 1020 generated frames across 12 characters (Phase 5C output)
- **Curation:** Select 30-50 best frames (clear character, clean green screen, no duplicates-per-cell)
- **Format:** PNG, nearest-neighbor upscaled to 1024x1024
- **Captioning:** WD Tagger auto-caption + prepend trigger word `16bitfit_style`
- **Folder:** `training_data/10_16bitfit_style/` (10 repeats)

### Training Config (RTX 5080, 16GB)
| Parameter | Value |
|-----------|-------|
| Framework | kohya_ss dev branch (gui-uv.bat) |
| Base model | Illustrious XL v0.1 |
| Optimizer | Adafactor (required for fused backward pass) |
| Attention | SDPA (NOT xformers) |
| Mixed precision | bf16 |
| LoRA rank | 32, alpha 32 |
| LR | 0.0005 (UNet only, text_encoder_lr=0) |
| Scheduler | cosine |
| Epochs | 10, sample every 5 |
| Batch/grad accum | 1 / 2 |
| Fused backward pass | Enabled (~10GB VRAM) |
| Expected time | 30-90 min |

### Gate
- LoRA produces recognizable 16BitFit-style sprites at strength 0.7-0.9
- X/Y/Z plot across epoch checkpoints vs. strength confirms sweet spot

---

## Phase 2: Autoresearch Loop — ComfyUI Workflow Optimization

### Three-File Mapping

| Karpathy | 16BitFit Equivalent | Location |
|----------|---------------------|----------|
| `prepare.py` (fixed) | Scoring pipeline: anchor images, CLIP+LPIPS+PQ evaluation, ComfyUI API client | `autoresearch/prepare.py` |
| `train.py` (mutable) | ComfyUI workflow JSON — the agent mutates parameter values within nodes | `autoresearch/workflow.json` |
| `program.md` (instructions) | Natural language research directions for the agent | `autoresearch/program.md` |

### The Mutable Artifact: `workflow.json`

The ComfyUI API-format workflow JSON. The agent modifies parameter values within specific nodes:

| Parameter | Node | Range | Type |
|-----------|------|-------|------|
| LoRA strength | Load LoRA | 0.5-1.2 | Continuous |
| ControlNet strength | Apply ControlNet | 0.3-1.0 | Continuous |
| IP-Adapter weight | IPAdapter Advanced | 0.3-1.0 | Continuous |
| CFG scale | KSampler | 3-12 | Continuous |
| Sampler | KSampler | euler, dpmpp_2m, dpmpp_2m_sde, euler_ancestral | Categorical |
| Steps | KSampler | 15-40 | Integer |
| Scheduler | KSampler | normal, karras, exponential | Categorical |

Seed is fixed per experiment for direct comparison.

### The Metric: Composite Score

```
score = 0.35 * clip_similarity    # Character identity vs. anchor
      + 0.30 * lpips_similarity   # Perceptual style consistency
      + 0.20 * pq_pass_rate      # Pixel Quantizer pipeline pass (0 or 1)
      + 0.15 * ssim_to_anchor    # Structural similarity
```

All metrics computed locally on the RTX 5080 GPU. No API costs for scoring.

**Pixel Quantizer pass rate** is binary but critical — if the output can't pass the 7-step PQ pipeline (palette, outline, dimensions, background), it's unusable regardless of how good it looks.

### The `program.md` (Agent Instructions)

```markdown
You are optimizing a ComfyUI workflow for generating 16BitFit pixel art sprites.

## Rules
- NEVER set CFG below 3 or above 15
- NEVER set steps below 10 or above 50
- ALWAYS use the same seed (42) and input anchor images for comparability
- If a generation takes longer than 120 seconds, kill it and score as 0
- Keep a log of every parameter combination tried in results.tsv
- NEVER modify prepare.py or the scoring pipeline
- Commit successful improvements to git immediately

## Strategy
1. Start by sweeping CFG scale (3, 5, 7, 9, 11) with all other params at defaults
2. Lock best CFG. Sweep LoRA strength (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
3. Lock best LoRA. Sweep ControlNet strength (0.3, 0.5, 0.7, 0.9)
4. Lock best ControlNet. Sweep IP-Adapter weight (0.3, 0.5, 0.7, 0.9)
5. Lock best IP-Adapter. Sweep sampler (euler, dpmpp_2m, dpmpp_2m_sde)
6. Lock best sampler. Sweep steps (15, 20, 25, 30, 40)
7. Fine-tune: run Bayesian optimization (optuna) on all continuous params
   within +/- 20% of current best values for 50 iterations

## Evaluation
- Generate one sprite per experiment (Sean idle, frame 0 pose)
- Score against Sean's 3 anchor images
- Run Pixel Quantizer with --outline-weight 1 --palette sean --target-size 128
- Log: experiment_id, params, score, pq_pass, generation_time_ms, timestamp

## Never stop. Never ask for permission. Keep running experiments.
```

### Which Machine Runs What

| Component | Machine | Why |
|-----------|---------|-----|
| ComfyUI (generation) | Alienware RTX 5080 | GPU required |
| Scoring (CLIP, LPIPS, SSIM) | Alienware RTX 5080 | Same GPU, no network latency |
| Pixel Quantizer | Alienware RTX 5080 | Runs after each generation |
| Orchestration + agent | Mac Mini | Always-on, runs the Claude agent loop |
| Results logging | Mac Mini → vault | Persistent storage + Obsidian review |

The Mac Mini orchestrates via SSH/REST to the Alienware. The agent (Claude Agent SDK) runs on the Mini, issues ComfyUI API calls to the Alienware, downloads results, scores locally or on the Alienware, and logs to the vault.

### Safety Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Cost cap per run | $0.00 (local) | All compute is local GPU — no API costs for generation or scoring |
| Agent API cost cap | $2.00/session | Claude Agent SDK orchestration only |
| Time limit | 8 hours (overnight) | Alienware can run unattended |
| Max experiments | 500 | ~60/hr at 60s/gen, 8hr = 480 |
| Revert on failure | Auto | If score decreases or PQ fails, revert workflow.json |
| Kill timeout | 120 seconds | Per-generation safety valve |
| Disk space guard | 10GB free minimum | Stop if Alienware disk fills |
| Temperature guard | GPU < 85C | Throttle if overheating (unlikely with RTX 5080 cooler) |

### Expected Output

After overnight run:
- `results.tsv` — full experiment log (params, scores, timing)
- `workflow_best.json` — highest-scoring workflow configuration
- `samples/` — generated sprites from top-10 experiments
- Git history of every improvement commit

---

## Phase 0 (Quick Win): Gemini Prompt Optimization

Before the full LoRA+ComfyUI loop, we can run a lighter version using the existing Gemini pipeline:

| Karpathy | Gemini Equivalent |
|----------|-------------------|
| `prepare.py` | Anchor images + Pixel Quantizer scoring |
| `train.py` | Prompt template (the text sent to Gemini) |
| `program.md` | "Mutate the prompt template. Generate a sprite sheet. Score it." |

**Pros:** Runs now (no Alienware needed), fast iterations, improves the existing pipeline.
**Cons:** API costs (~$0.07/call), limited parameter space (just prompt text), less impactful than LoRA approach.

**Metric:** Pixel Quantizer pass rate + visual consistency score (CLIP similarity to anchor).

This could run as a first experiment to validate the autoresearch scaffolding before investing in LoRA training.

---

## Implementation Order

1. **Build scoring pipeline** (`prepare.py`) — CLIP + LPIPS + SSIM + PQ wrapper
2. **Phase 0** — Gemini prompt optimization (validate the loop pattern)
3. **LoRA training** — Curate dataset, train on Alienware
4. **Build ComfyUI workflow** — LoRA + ControlNet + IP-Adapter chain
5. **Phase 2** — Full autoresearch loop on ComfyUI workflow
6. **Extract reusable scaffolding** — Generic `autoresearch-loop/` in superuser pack

---

## Open Questions (for review)

1. **ControlNet pose source:** Should we use OpenPose skeletons from the Gemini-generated keyframes, or hand-draw pose references?
2. **Multi-character generalization:** Train one LoRA on all 12 characters, or per-character LoRAs?
3. **Optuna vs. grid search:** The docs suggest Bayesian optimization. Is optuna installed on the Alienware, or should we start with simple grid sweep?
4. **Vision LLM scoring:** Should we add a Claude API call as a "subjective quality" judge (adds cost but captures things CLIP/LPIPS miss)?
5. **When to run Phase 0 vs. skip to Phase 2:** Is the Gemini prompt experiment worth the API cost, or jump straight to LoRA?
