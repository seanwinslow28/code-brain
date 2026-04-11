# Autoresearch Plan: 16BitFit Sprite Pipeline Optimization

**Date:** 2026-04-11
**Status:** APPROVED — Ready for implementation
**Revised:** Collaboratively with Sean during Cowork session. LoRA training removed (abandoned April 8). Focus: walk cycle optimization first, then expand to all poses.

---

## Overview

Apply Karpathy's three-file autoresearch pattern to the 16BitFit sprite generation pipeline. The goal: systematically optimize sprite sheet generation — starting with walk cycles, then expanding to other animation types — through automated experimentation and scoring.

**Two phases, sequential:**
1. **Phase 0: Gemini NB2 Optimization** — Optimize the full generation approach (prompts, reference usage, sheet structure, animation principles) for the existing Gemini NB2 pipeline. Runs on Mac Mini, costs ~$0.07/experiment.
2. **Phase 1: ComfyUI Model Discovery** — Find cheaper/free alternatives to Gemini NB2 for production-grade sprite generation. Test open-source models, community LoRAs, and pre-built ComfyUI workflows on the Alienware. Runs locally for $0.

**LoRA training is NOT part of this plan.** It was abandoned on April 8 after multiple attempts produced anime-proportioned characters instead of SF2 arcade sprites. Pre-made community LoRAs may be evaluated in Phase 1 as ComfyUI workflow components, but we are not training new LoRAs.

---

## The Three-File Pattern (How It Works)

Karpathy's autoresearch has three files. The key rule: the agent can only modify ONE of them.

| File | Role | Who Can Change It |
|------|------|-------------------|
| `prepare.py` | **Scoring pipeline** — measures "was this experiment good or bad?" Returns a number. Contains anchor images, DINOv2 identity scoring, Pixel Quantizer checks, VLM walk cycle judge. | **FROZEN.** Nobody changes this during a run. Prevents the agent from "cheating" by making the test easier instead of the output better. |
| `experiment.json` | **The mutable artifact** — the thing being optimized. In Phase 0: a JSON config containing the Gemini prompt template, reference image strategy, sheet layout, and animation principle hints. In Phase 1: a ComfyUI workflow JSON with model, sampler, and adapter settings. | **AGENT ONLY.** The agent tweaks values, runs an experiment, checks the score, keeps improvements, reverts failures. |
| `program.md` | **Research directions** — plain English instructions telling the agent what to try. "First sweep CFG from 3-12, then try adding contact/passing pose descriptions." | **HUMAN ONLY.** Sean writes and updates this. The agent reads it for direction but never modifies it. |

**Why it works:** The frozen scorer prevents metric-hacking. The single mutable file keeps changes reviewable. The markdown contract lets you and the agent collaborate without stepping on each other. Every experiment is a git commit — failures revert instantly, successes form a searchable history.

---

## Scoring Pipeline (The Frozen `prepare.py`)

### Tiered Architecture

The scorer is NOT a single metric — it's a pipeline where each layer uses the right tool for the job. Fast/free checks run first and filter out ~80% of bad frames before the expensive VLM judge ever fires.

| Layer | Tool | Runs On | Cost | Speed | What It Checks |
|-------|------|---------|------|-------|----------------|
| 1. Hard Gates | Pixel Quantizer (existing) | Any machine | $0 | <100ms | Dimensions, palette compliance, alpha, background color, file integrity |
| 2. Identity | **DINOv2** (`dinov2-base`, 86M params) | Alienware GPU | $0 | <100ms | "Is this the same character?" — cosine similarity vs anchor embeddings. Replaces SSIM as primary (SSIM is brittle for animation — a 1px shift kills the score) |
| 3. Deterministic Quality | Sharp + OpenCV scripts | Any machine | $0 | <200ms | Outline weight, baseline drift, alpha halos — all pixel-math, no AI |
| 4. **VLM Walk Cycle Judge** | **Qwen2.5-VL-7B** via Ollama | Alienware RTX 5080 | $0 | 2-5s | The key layer — evaluates walk cycle quality using structured rubric + reference examples |
| 5. Escalation (borderline only) | **Gemini 2.5 Flash** via API | Cloud | ~$0.0003/frame | 2-4s | Fires only when Qwen2.5-VL flags uncertainty (~10-15% of frames) |

### What the VLM Walk Cycle Judge Evaluates

The VLM judge receives:
- The generated sprite sheet (upscaled 4x to 512×512 via nearest-neighbor — VLMs perform poorly on tiny images)
- 3 character anchor references (identity context)
- 2-3 real SF2/arcade walk cycle sprite sheets (downloaded from Spriters Resource — "this is what good looks like")
- A structured rubric based on 2D animation walk cycle principles

**Walk Cycle Rubric (scored 1-5 per criterion):**

| Criterion | What It Measures | Score 1 (Fail) | Score 5 (Perfect) |
|-----------|-----------------|----------------|-------------------|
| **Leg Differentiation** | Are leg positions distinctly different across frames? | All frames show nearly identical leg positions | Clear contact, passing, up, and down poses visible |
| **Pose Progression** | Do poses follow a logical walking sequence? | Random poses with no flow | Smooth contact→down→passing→up→contact cycle |
| **Weight Shift** | Does the character's center of gravity shift naturally? | Character appears static/floating | Visible weight transfer between legs, body dips at down pose |
| **Arm Swing** | Do arms swing opposite to legs? | Arms static or identical (twinning) | Arms swing with natural offset, opposite to leg motion |
| **Character Consistency** | Same character across all frames? | Different hair/clothes/proportions between frames | Identical character with only pose changes |
| **Height Consistency** | Is the character the same height throughout? | Character grows/shrinks noticeably | Height varies only at down pose (lowest) and up pose (highest) |

**Key animation principles embedded in the rubric** (from the 2D animation principles skill):
- A correct walk cycle has 4 key poses: **Contact** (heel strike, legs spread wide), **Down** (lowest point, weight absorb), **Passing** (legs together, one vertical), **Up** (highest point, push-off)
- Left and right limbs must NOT be twinned — offset arm swing by 2+ frames
- The body should be lowest at the Down pose and highest at the Up pose
- Frame 13 (on Twos at 12fps) mirrors Frame 1 to create a seamless loop

**Composite Score:**
```
walk_score = (
    0.25 * leg_differentiation +
    0.20 * pose_progression +
    0.20 * weight_shift +
    0.15 * character_consistency +
    0.10 * arm_swing +
    0.10 * height_consistency
) / 5.0  # Normalized to 0.0-1.0
```

If any criterion scores ≤ 2, the experiment is marked FAIL regardless of composite score.

### Reference Materials (Frozen — Part of prepare.py)

| Reference Type | Purpose | Source |
|----------------|---------|--------|
| Character anchors (3 per character) | Identity verification | Existing anchor PNGs in `assets/anchors/` |
| SF2 walk cycle sprite sheets (2-3) | "What good looks like" for the VLM judge | Downloaded from Spriters Resource (Ryu, Ken, Guile walk cycles) |
| 2D walk cycle pose diagram | Key pose identification reference | Contact/Down/Passing/Up visual guide |
| Current best walk cycle | Baseline to beat | Best-scoring walk from Sean's existing output |

These references are FROZEN — the agent cannot modify or swap them. They're the standard the agent's experiments are measured against.

---

## Phase 0: Gemini NB2 Optimization

### What Gets Optimized

Phase 0 is broader than just prompt text. The agent experiments with the FULL generation approach:

| Parameter | Type | Current Value | Experiment Range | Why It Matters |
|-----------|------|---------------|------------------|----------------|
| **Prompt template** | Text | Current walk_forward prompt | Structural variations (pose-by-pose descriptions, animation terminology, contact/passing/up/down naming) | The words describing each frame's pose are the primary quality lever |
| **Reference strategy** | Categorical | 3 anchor images per call | 1 anchor, 2 anchors, 3 anchors, anchor + pose ref, anchor + walk cycle ref | More/different references may improve consistency or pose accuracy |
| **Sheet layout** | Categorical | Full sheet (all frames in one call) | Full sheet, 2-frame pairs, individual frames, keyframes-only + RIFE | Per-frame generation failed before, but 2-frame pairs might work better than full sheets for walk cycles |
| **Animation principle hints** | Text | None currently | Add contact/down/passing/up pose names, add "legs must be in distinctly different positions", add weight shift descriptions | Explicitly teaching the model animation principles through the prompt |
| **Negative prompt additions** | Text | Basic | "no text", "no labels", "exactly ONE character per cell", "legs must show different positions in each frame" | Preventing known failure modes |
| **Frame count** | Integer | 4 keyframes for HYBRID | 4, 6, 8 keyframes | More keyframes = more distinct poses for RIFE to interpolate between |

### Three-File Mapping (Phase 0)

| Karpathy | 16BitFit Phase 0 | Location |
|----------|-------------------|----------|
| `prepare.py` (frozen) | Scoring pipeline: anchor images + DINOv2 + Pixel Quantizer + VLM walk cycle judge | `autoresearch/prepare.py` |
| `experiment.json` (mutable) | Generation config: prompt template, reference strategy, sheet layout, frame count, negative prompts | `autoresearch/experiment.json` |
| `program.md` (human-written) | Research directions for the agent | `autoresearch/program.md` |

### The `program.md` (Agent Instructions — Phase 0)

```markdown
You are optimizing Gemini NB2 sprite sheet generation for walk_forward animations.
The goal: produce walk cycles where legs show distinctly different positions across frames,
following the Contact→Down→Passing→Up progression of real arcade fighter walk cycles.

## Rules
- NEVER modify prepare.py or the scoring pipeline
- ALWAYS use the same character (Sean) and seed for comparability
- ALWAYS include 3 anchor images (Golden Rule — enforced with RuntimeError)
- Log every experiment to results.tsv: experiment_id, params_changed, scores, generation_time, timestamp
- Commit successful improvements to git immediately
- If score decreases, revert experiment.json and try next direction
- Budget: ~$0.07 per experiment. Stop after 100 experiments or $7 total.

## Strategy (work through in order)

### Round 1: Prompt Structure (experiments 1-20)
1. Baseline: run current prompt, record score
2. Add explicit pose names per frame: "Frame 1: Contact pose — right heel strikes ground,
   left leg trails behind, arms at maximum spread"
3. Try pose-by-pose prompt (describe each frame separately) vs. sheet-level prompt
4. Add animation terminology: "walk cycle", "contact pose", "passing position",
   "weight transfer", "push-off"
5. Try adding "each frame must show a DISTINCTLY DIFFERENT leg position"

### Round 2: Reference Strategy (experiments 21-40)
6. Test with 1 anchor vs 2 vs 3 (is more always better?)
7. Add a reference walk cycle sprite sheet alongside anchors
8. Add a pose reference diagram showing contact/passing/up/down positions
9. Test anchor + style ref (full SF2 sprite sheet from another character)

### Round 3: Sheet Layout (experiments 41-60)
10. Try 2-frame pair generation (generate frames 1-2, then 3-4, etc.)
11. Try individual frame generation with heavy anchor conditioning
12. Try generating 6 keyframes instead of 4 for HYBRID walk cycles
13. Try 8 keyframes (more distinct poses for RIFE to interpolate)

### Round 4: Negative Prompts + Constraints (experiments 61-80)
14. Add "legs must be in different positions in every frame"
15. Add "no repeated poses"
16. Add 2D animation principle constraints: "body lowest at frame 2, highest at frame 4"
17. Test combination of best findings from Rounds 1-3

### Round 5: Fine-Tuning Best Configuration (experiments 81-100)
18. Take the best-scoring configuration and make small variations
19. Try the winning approach on walk_backward
20. Try on a second character (Aria) to confirm generalization
```

### Cost and Timeline (Phase 0)

| Metric | Value |
|--------|-------|
| Cost per experiment | ~$0.07 (one Gemini NB2 API call) |
| Experiments planned | 100 |
| Total estimated cost | ~$7.00 |
| Time per experiment | ~15-20s (API call + scoring) |
| Total runtime | ~30-45 minutes for 100 experiments |
| Can run unattended | Yes — standalone Python script |

---

## Phase 1: ComfyUI Model Discovery

### Goal

Find a local, free (or much cheaper) alternative to Gemini NB2 for production-grade sprite generation. If this pipeline is going to be a product, paying $0.07 per animation isn't sustainable at scale. The Alienware RTX 5080 is sitting there — let's use it.

### What Gets Tested

| Category | Examples | Why |
|----------|----------|-----|
| **Open-source image models** | Illustrious XL, Pony Diffusion, PixArt-Σ, Flux.1 | Base models that might produce pixel art with the right workflow |
| **Community LoRAs** (pre-made, NOT trained by us) | Pixel art LoRAs on CivitAI, sprite-specific LoRAs | Community has trained pixel art LoRAs on larger datasets than we could |
| **Pre-built ComfyUI workflows** | NB2 Animated Sprite Sheet template, community sprite workflows | Proven workflows with optimized node configurations |
| **IP-Adapter + ControlNet** (no LoRA) | IP-Adapter for character identity, ControlNet for pose guidance | Achieves style transfer without training — uses anchor images directly |
| **Sampler/scheduler settings** | CFG scale, steps, sampler choice, scheduler | Same model can produce very different results with different settings |

### Three-File Mapping (Phase 1)

| Karpathy | 16BitFit Phase 1 | Location |
|----------|-------------------|----------|
| `prepare.py` (frozen) | Same scoring pipeline as Phase 0 (reused entirely) | `autoresearch/prepare.py` |
| `experiment.json` (mutable) | ComfyUI workflow JSON — the agent mutates model selection, LoRA weights, IP-Adapter strength, ControlNet settings, sampler params | `autoresearch/workflow.json` |
| `program.md` (human-written) | Research directions for ComfyUI experiments | `autoresearch/program_comfyui.md` |

### Parameters the Agent Can Mutate

| Parameter | Node | Range | Type |
|-----------|------|-------|------|
| Base model checkpoint | Load Checkpoint | Illustrious XL, Pony, PixArt-Σ, Flux.1 | Categorical |
| Community LoRA | Load LoRA | Top-rated pixel art LoRAs from CivitAI | Categorical |
| LoRA strength | Load LoRA | 0.3-1.0 | Continuous |
| IP-Adapter weight | IPAdapter Advanced | 0.3-1.0 | Continuous |
| ControlNet strength | Apply ControlNet | 0.3-1.0 | Continuous |
| CFG scale | KSampler | 3-12 | Continuous |
| Sampler | KSampler | euler, dpmpp_2m, dpmpp_2m_sde, euler_ancestral | Categorical |
| Steps | KSampler | 15-40 | Integer |
| Scheduler | KSampler | normal, karras, exponential | Categorical |

Seed is fixed per experiment for direct comparison.

### Cost and Timeline (Phase 1)

| Metric | Value |
|--------|-------|
| Cost per experiment | $0.00 (all local GPU) |
| Experiments planned | 200-500 |
| Time per experiment | ~30-120s depending on model/steps |
| Total runtime | 4-8 hours (overnight on Alienware) |
| Can run unattended | Yes — standalone Python script on Mac Mini orchestrating Alienware via REST |

---

## Which Machine Runs What

| Component | Machine | Why |
|-----------|---------|-----|
| Experiment orchestration | Mac Mini | Always-on, runs the Python script |
| Gemini API calls (Phase 0) | Mac Mini → Gemini API | HTTP calls, no GPU needed |
| ComfyUI generation (Phase 1) | Alienware RTX 5080 | GPU required, REST API at 192.168.68.201:8188 |
| DINOv2 identity scoring | Alienware RTX 5080 | Same GPU, no network latency |
| Pixel Quantizer | Alienware RTX 5080 | Runs after each generation |
| VLM judge (Qwen2.5-VL-7B) | Alienware RTX 5080 via Ollama | Local inference, $0/frame |
| VLM escalation (Gemini 2.5 Flash) | Mac Mini → Gemini API | Borderline cases only (~10-15%) |
| Results logging | Mac Mini → vault | Persistent storage + Obsidian review |
| Morning summary | Daily-driver agent (existing) | Reads results log, writes digest to daily note |

---

## Safety Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Phase 0 API budget | $7.00 per run (100 experiments) | ~$0.07/call × 100 |
| Phase 1 compute cost | $0.00 (local GPU) | All inference on Alienware |
| VLM escalation budget | $0.50 per run | Gemini 2.5 Flash is cheap but cap it anyway |
| Time limit | 8 hours (Phase 1 overnight) | Alienware can run unattended |
| Max experiments per run | 500 | ~60/hr at 60s/gen, 8hr = 480 |
| Revert on failure | Automatic | If score decreases, revert experiment.json to previous best |
| Kill timeout | 120 seconds | Per-generation safety valve |
| Disk space guard | 10GB free minimum | Stop if Alienware disk fills |
| Temperature guard | GPU < 85°C | Throttle if overheating |
| Git commit on improvement | Automatic | Every score increase = committed workflow.json |

---

## Orchestration Architecture

### Now: Standalone Python Script (Reliable)

```
Mac Mini                          Alienware RTX 5080
┌─────────────────────┐          ┌──────────────────────┐
│ autoresearch/        │          │ ComfyUI (Phase 1)    │
│   runner.py          │──REST──▶│ Ollama (Qwen2.5-VL)  │
│   prepare.py (frozen)│◀──────── │ DINOv2 (scoring)     │
│   experiment.json    │          │ Pixel Quantizer       │
│   program.md         │          └──────────────────────┘
│   results.tsv        │
│   best_experiment.json│
└─────────────────────┘
         │
         ▼
  vault/daily note (results summary)
```

**How to run:**
```bash
# Phase 0 — Gemini prompt optimization (walk_forward, 100 experiments)
cd autoresearch && python3 runner.py --phase 0 --animation walk_forward --character sean --max-experiments 100

# Phase 1 — ComfyUI model discovery (walk_forward, overnight)
cd autoresearch && python3 runner.py --phase 1 --animation walk_forward --character sean --max-experiments 500 --timeout-hours 8
```

### Future: Agent SDK Wrapper (When SDK Bug Is Fixed)

The standalone script is designed as clean modules (experiment loop, scoring, logging). When the CLIConnectionError in `claude-agent-sdk` v0.1.56 is fixed in a future release, the same modules get wrapped in an agent that adds:
- Natural language experiment summaries ("walk cycles improve 23% when prompts name contact/passing poses explicitly")
- Adaptive strategy changes mid-run ("CFG sweeps plateaued — switching to prompt structure experiments")
- `program.md` hypothesis updates based on observed patterns
- Morning digest integration with daily-driver agent

**Do NOT build the agent wrapper until:** (1) SDK transport bug is fixed, AND (2) Sean explicitly approves adding a new agent to the fleet.

---

## Implementation Order

1. **Build scoring pipeline** (`prepare.py`) — Hard gates + DINOv2 + Pixel Quantizer + VLM walk cycle judge
2. **Collect reference materials** — Download 2-3 SF2 walk cycle sprite sheets, create walk cycle pose diagram
3. **Build experiment runner** (`runner.py`) — The loop: load config → generate → score → keep/revert → log
4. **Phase 0: Run Gemini prompt optimization** — 100 experiments on walk_forward, ~45 minutes, ~$7
5. **Apply Phase 0 findings to walk_backward** — Confirm learnings generalize
6. **Phase 1: Set up ComfyUI workflows** — Install community LoRAs, configure IP-Adapter + ControlNet
7. **Phase 1: Run ComfyUI model discovery** — 200-500 experiments overnight, $0
8. **Compare Phase 0 vs Phase 1 winners** — Best Gemini config vs best ComfyUI config, pick the production path
9. **Expand to other animation types** — Apply the winning approach to idle, attacks, etc.
10. **Extract reusable scaffolding** — Generic `autoresearch-loop/` pattern for the superuser pack

---

## Expected Output

After each run:
- `results.tsv` — full experiment log (experiment_id, params_changed, all scores, generation_time, timestamp)
- `best_experiment.json` — highest-scoring configuration
- `samples/` — generated sprite sheets from top-10 experiments
- `summary.md` — human-readable summary of findings (written by daily-driver agent or manually)
- Git history of every improvement commit

---

## Open Questions (Resolved)

| # | Question | Resolution |
|---|----------|------------|
| 1 | LoRA training? | **ABANDONED.** Removed from plan entirely. Community pre-made LoRAs may be tested in Phase 1. |
| 2 | Which scoring approach? | **Tiered: Hard gates → DINOv2 → VLM judge → Gemini escalation.** Walk cycle specific rubric. |
| 3 | Which VLM for judging? | **Qwen2.5-VL-7B locally via Ollama** (mature tooling), Gemini 2.5 Flash for escalation. |
| 4 | What reference materials? | **Anchor images + real SF2 walk cycles + 2D animation pose diagrams.** All frozen. |
| 5 | Agent vs script? | **Standalone script now, agent later** when SDK bug is fixed. Daily-driver summarizes results. |
| 6 | When to start? | **Now, with walk cycles.** Don't fix existing sprites first — autoresearch may improve them. |
| 7 | ComfyUI goal? | **Find cheaper/free alternative to NB2 for production.** Not a refinement step — a replacement candidate. |
| 8 | Optuna vs grid search? | **Start with structured sweeps (program.md directions), add Optuna for Phase 1 fine-tuning.** |

---

## Deferred Tasks (Not Part of This Plan)

These are tracked but NOT started until autoresearch produces results:

1. **Re-generate 3 idle animations** — Marcus (text overlay), Gym Bully + Procrastination Phantom (multi-character). May benefit from autoresearch findings.
2. **Run Pixel Quantizer on remaining 5 characters** — Sean, Aria, Kenji, Marcus, Gym Bully, Procrastination Phantom, Sloth Demon verified. Remaining: Mary, Zara, Stress Titan, Training Dummy, Ultimate Slump.
3. **Full sprite visual review** — Sean wants to personally review all sprites. Deferred until autoresearch shows whether walk cycles can be improved.
4. **Agent SDK wrapper** — Wrap the experiment loop in a Claude Agent SDK agent for learning/documentation. Blocked on SDK transport bug fix.
5. **Fine-tune Qwen2.5-VL-7B** — Collect 200-500 labeled examples from autoresearch runs, QLoRA fine-tune on RTX 5080 to match Gemini 2.5 Flash accuracy on the walk cycle rubric. Phase 5+ optimization.

---

*This plan was collaboratively designed by Sean and Claude during a Cowork session on 2026-04-11. It replaces the previous draft which included LoRA training (abandoned April 8).*
