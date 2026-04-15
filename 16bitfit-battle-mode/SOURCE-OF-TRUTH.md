# Source of Truth — Sean's Agentic Frameworks & Creative Pipeline Master Plan

**Created:** 2026-03-27 (Boston, post-move)
**Last Updated:** 2026-04-15 — Phase 5 COMPLETE. 12/12 characters, 180/180 animations, 1020 IMAGE_ONLY + 815 HYBRID frames, 0 failures, ~$12.60. Sheet→split approach LOCKED. Anchor image Golden Rule enforced. RIFE VFI connectivity fixed. Palette expanded (Sean 27, generic 38). 3 idle animations need re-gen (Marcus, Gym Bully, Procrastination Phantom). Autoresearch plan in revision. **Phase 6 PLANNED** (Gemma 4 benchmarking + Knowledge Compounding Loop). New Workstream D adds SessionEnd flush hook, Vault Synthesizer, Knowledge Lint agent, and autoresearch feedback loop. 3 new agents planned (11 total built → 14 at Phase 6 completion). Inspired by Karpathy's LLM Wiki pattern + claude-memory-compiler.
**Purpose:** Compressed reference doc for every future Claude Code / Cowork session. Feed THIS file + the specific subfolder relevant to your current task. Never dump all 28 source files at once.
**Source Files:** 28 original docs + 3 Perplexity Computer outputs in `Agentic-Frameworks-And-Autoresearch/`

---

## How to Use This Document

**For Claude Code sessions:** Copy the relevant section of this doc into your CLAUDE.md or paste it as context, then point Claude at the specific subfolder files it needs for the current build task.

**For Cowork sessions:** Reference this doc when planning or making strategic decisions. It has the "what" and "why" compressed — go to source files for implementation details.

**For Perplexity Computer:** Use for new research that extends what's here — checking for newer model releases, updated API docs, or community workarounds.

---

## Part 1: What Exists Today (Starting Position)

### Sprite Sheet Pipeline — v0.1.0 (Shipped Jan 21, 2026)

The core pipeline is built and working. It's a manifest-driven CLI (`banana gen`, `banana doctor`, etc.) in Node.js/TypeScript/Oclif that generates sprite animation frames, audits them, retries failures, packs atlas sheets, and validates in headless Phaser 3.

**What works:**
- Full 7-stage pipeline: Manifest → Choreographer → Generator → Auditor → Retry Ladder → Packer → Phaser Validator
- Gemini integration via `@google/genai` SDK (originally Nano Banana Pro / `gemini-3-pro-image-preview`)
- Hard fail gates (HF01-HF05) + soft scoring (SF01-SF05) + bounded retry ladder (max 4 attempts)
- Resume functionality, Director Mode (human-in-the-loop review), atlas export, Phaser micro-tests
- 8 epics, 67 stories, 1004+ unit tests passing, 0% retry/reject rate in E2E
- Tested with 4-frame idle + 8-frame walk (1 Champion × 2 animations MVP)

**What doesn't work:**
- Walk cycles via image-only generation fail — text prompts can't reliably differentiate left vs. right leg positions across sequential frames. This is an inherent limitation, not a prompt engineering problem.
- Only tested with 1 character. Full scope is 12 fighters × 13 animations × 4-12 frames each.

**Architecture (Hexagonal/Ports & Adapters):** Core logic never touches external tools directly. Gemini, TexturePacker, Phaser are all behind typed Adapter interfaces — swappable by design.

### Agent SDK — v3.9.0 (Feb 2026, Pre-Implementation)

The Claude Agent SDK layer is planned but not yet built beyond the existing `daily_driver.py` pattern. A comprehensive Phase 2 upgrade plan exists (synthesized from two Gemini 3 Pro Deep Think sessions), covering 15-18 autonomous agents across a 12-week timeline.

**What exists today:**
- Basic SDK integration: `agents-sdk/agents/daily_driver.py`, shared `lib/` utils, `config.toml`
- Interactive layer: `.claude/skills/`, `.claude/hooks/`, `.claude/agents/` (subagents)
- Scheduling via launchd (basic)

**What's planned (from the Phase 2 synthesis):**
- 15-18 autonomous agents (10-12 running 100% local)
- Three-machine orchestration: Mac Mini (always-on orchestrator) → MacBook Pro (heavyweight local inference) → Alienware (CUDA-specialized)
- `hybrid_router.py` with three-tier routing + WOL for Alienware
- Baton File dependency chains, Fleet State note, prompt caching scheduling
- Monthly target: $3-6 API cost + ~$4 electricity = ~$6-10 total (recalculate — Opus 4 now 67% cheaper at $5/$25 per MTok; actual cost likely lower)

---

## Part 2: The Three Workstreams

### Workstream A: Agent SDK Infrastructure (PREREQUISITE)

**Goal:** Build the autonomous agent orchestration layer on the three-machine topology.

**Key Decisions (Locked — updated March 27 per validation audit):**
- Mac Mini = always-on orchestrator (launchd host, `phi4-mini-reasoning` 3.8B, nomic-embed-text)
- MacBook Pro = heavyweight local inference (MLX-LM — 3x faster than Ollama on M4 Pro, 14B-32B models, 48GB unified)
- Alienware = CUDA-specialized (ComfyUI v0.18.2, vision QA with Qwen3-VL-7B, LoRA training)
- SDK package: `claude-agent-sdk` (renamed from `claude-code-sdk`), class: `ClaudeAgentOptions` (renamed from `ClaudeCodeOptions`)
- Agent Teams are now production-ready (no longer experimental) — use for complex multi-agent work; subagents for focused single tasks
- Credential management via macOS Keychain (not .env)
- Filelock for vault writes, vault-integrity hook, loop-detector hook, cost-watchdog hook
- Never use `dangerouslySkipPermissions` for autonomous agents
- Opus 4.6 pricing dropped to $5/$25 per MTok (67% cheaper than Opus 4.1) — now viable for more agent tasks

**Model-to-Machine Routing (UPDATED — Phase 6 additions marked):**

| Task | Machine | Model | Change from Original |
|------|---------|-------|---------------------|
| Inbox triage | Mac Mini | `phi4-mini-reasoning` (3.8B) via Ollama → **benchmark Gemma 4 27B MoE (Phase 6.A)** | Was "Phi-4 7B" — Gemma 4 MoE activates 3.8B with native function calling |
| Vault embeddings | Mac Mini | nomic-embed-text via Ollama | No change |
| Vault synthesis | MacBook Pro | **Qwen3-14B** via MLX-LM | **NEW (Phase 6.D.2)** — concept + connection article generation |
| Daily flush | Mac Mini or MacBook Pro | **phi4-mini** (simple sessions) or **Qwen3-14B** (complex sessions >100 msgs) | **NEW (Phase 6.D.1)** — session knowledge extraction |
| Knowledge Lint (Tier 1) | Mac Mini | **phi4-mini-reasoning** (3.8B) | **NEW (Phase 6.D.3)** — structural checks (broken links, orphans) |
| Knowledge Lint (Tier 2) | MacBook Pro | **Qwen3-14B** via MLX-LM | **NEW (Phase 6.D.3)** — semantic checks (contradictions, staleness) |
| Anki cards | Mac Mini | `phi4-mini` (3.8B) via Ollama | Was "Phi-4 7B" |
| Financial analysis | MacBook Pro | **Qwen3-14B** via MLX-LM → **benchmark Gemma 4 31B (Phase 6.A)** | Was DeepSeek-R1:14B — Gemma 4 31B is benchmark candidate |
| Code review / PR digest | MacBook Pro | **Qwen2.5-Coder-32B** via MLX-LM | Was 14B — 32B fits in 48GB via MLX, likely stays (Qwen's coding strength) |
| Heavy synthesis | MacBook Pro | **Qwen3.5** (evaluate 122B MoE 10B-active or 9B) via MLX-LM | Was Qwen2.5-32B — Qwen3.5 MoE is faster + smarter |
| Sprite vision QA | Alienware | **Qwen3-VL-7B** via Ollama CUDA | Was Qwen2.5-VL — Qwen3-VL has better spatial encoding |
| ComfyUI orchestration | Alienware | N/A (REST API) | No change |

**Source files:** `Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md` (the big one — 350 lines of detailed specs), `agents-sdk.md` (SDK architecture + how interactive vs autonomous layers relate), `tech-stack-specs.md` (hardware inventory for all 3 machines), `Claude-Code-Agent-Teams.md` (Agent Teams — now production-ready with shared task lists, plan approval, display modes)

### Workstream B: Sprite Sheet Pipeline Upgrade (THE PRODUCT)

**Goal:** Evolve the working v0.1.0 pipeline into a hybrid keyframe-to-video system that solves the walk cycle problem, then scale to all 12 fighters × 13 animations.

**NON-NEGOTIABLE: Google's image generation models stay in the pipeline.** Nano Banana Pro (`gemini-3-pro-image-preview`) and/or Nano Banana 2 (`gemini-3.1-flash-image-preview`) are the proven best-in-class for single-frame sprite generation. Cost is not a concern here — quality and speed are. These models serve as both the primary image-only generator AND the keyframe generator feeding the hybrid pipeline.

**Phase 5 Results — Full Roster Generation COMPLETE (2026-04-11):**

The sprite sheet→split approach replaced per-frame Gemini generation. Instead of calling Gemini once per frame (which produced inconsistent characters), ALL frames for an animation are generated as a single sprite sheet in one API call, then split programmatically. This is 5x faster, 6x cheaper, and solves character consistency. Every Gemini NB2 call MUST include 3 character reference PNGs as inline image data (the "Golden Rule") — enforced with `RuntimeError`, zero violations across 180 animations.

**15 animation types mapped:** 10 IMAGE_ONLY (idle, crouch, light_punch, medium_punch, heavy_punch, light_kick, heavy_kick, block, take_hit, victory) + 5 HYBRID (walk_forward, walk_backward, jump, defeat, special_move). IMAGE_ONLY: 4-7 frames each. HYBRID: 4-5 keyframes → RIFE 4x interpolation → 13-17 frames each.

| Character | Type | Tile | Anims | Frames | IMAGE_ONLY | HYBRID (KF) | Status |
|-----------|------|------|-------|--------|------------|-------------|--------|
| Sean | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Aria | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Kenji | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Marcus | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Mary | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Zara | champion | 128 | 15/15 | 85 | 10 | 5 | OK |
| Gym Bully | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| Procrastination Phantom | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| Sloth Demon | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| Stress Titan | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| Training Dummy | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| Ultimate Slump | boss | 256 | 15/15 | 85 | 10 | 5 | OK |
| **TOTAL** | | | **180/180** | **1,020** | **120** | **60** | **0 fail** |

**Palette:** Sean's palette expanded from 16 to 27 colors via k-means extraction (5 skin tones, 3 hair, 4 tank top, 5 pants, 3 shoes, 3 outline, 4 fixed). Generic `sf2_pixel_art` palette (38 colors) created from all 12 characters' anchor images. Outline weight 1 is the new standard (weight 2 was too aggressive at 128×128 — 77% of pixels become outline).

**Cost:** ~$12.60 total (180 Gemini API calls × ~$0.07/call). ~55 minutes generation time with 10s delays.

**RIFE VFI Results:** All 60 HYBRID animations (5 per character × 12 characters) interpolated via RIFE VFI on RTX 5080. 815 total interpolated frames, 0 failures. Root cause of earlier connectivity failure: corporate VPN (utun4) was blocking LAN access to Alienware. Fix: VPN disabled + httpx retries + pre-flight health check + Windows Firewall rule for port 8188.

**Pixel Quantizer:** Verified on 7/12 characters (Sean, Aria, Kenji, Marcus, Gym Bully, Procrastination Phantom, Sloth Demon) — 100% pass rate, 0 off-palette pixels across all tested frames.

**3 animations needing re-generation:**
1. Marcus idle — "Idle Neutral" text burned into frame_00 (Gemini prompt artifact). Fix: add "no text, no labels, no captions" to negative prompt.
2. Gym Bully idle — Multiple characters per cell. Fix: add "exactly ONE character per cell" constraint.
3. Procrastination Phantom idle — Same multi-character issue. All other animations for these characters are clean.

**Model Update (March 2026):** Nano Banana 2 (`gemini-3.1-flash-image-preview`) is now available — Flash-tier pricing ($0.50/$3.00 text, $0.0672/image output) with "pro-level visual intelligence." Benchmark both against Nano Banana Pro ($2.00/$12.00 text, $0.134/image) to determine if Flash quality is sufficient for sprite work, or if Pro remains necessary for anchor/keyframe generation while Flash handles volume.

**The Three Generation Strategies:**

| Strategy | Use Case | How It Works |
|----------|----------|--------------|
| **Image-Only** | Static poses, idle, single-hit attacks | Proven v0.1.0 workflow: anchor + pose ref → Gemini → single frame |
| **Hybrid Keyframe-to-Video** | Walk cycles, run cycles, complex locomotion | Keyframes via Gemini → video model interpolation → pixel quantizer → audit |
| **Motion Transfer** (experimental) | Standard locomotion with canonical reference | Upload reference walk video + character anchor → video model transfers motion |

**The Pixel Quantizer is the gate check.** All three council models (GPT-5.2, Claude Opus 4.6, Gemini 3 Pro) agree: if the quantizer can't convert video "sludge" back to clean pixel art, the hybrid approach is dead. Build and validate this FIRST.

**Pixel Quantizer Pipeline (7 steps):**
1. Nearest-neighbor downscale (Sharp, `kernel.nearest`) → 128×128
2. Palette quantization (force-snap to predetermined LUT, Euclidean RGB distance)
3. Temporal smoothing (mode-color locking for static regions)
4. Outline enforcement (`#272929`, 2-3px weight at sprite edges)
5. Alpha recovery (background removal + edge cleanup)
6. Grid alignment (snap to pixel grid)
7. Format validation (dimensions, alpha, palette compliance)

**Video Model Candidates (UPDATED April 2 per Phase 4 testing):**

**CONFIRMED WORKING (ranked by quality):**
- **RIFE VFI** — Frame interpolation from NB2 keyframes. 87.6% through Pixel Quantizer, 0 off-palette pixels. ~5s/clip, FREE/local. **Best quality for keyframe-anchored animation.** Uses rife49.pth via Fannovel16/ComfyUI-Frame-Interpolation.
- **Wan 2.2 14B I2V** — Dual-model (high_noise + low_noise fp8) with LightX2V 4-step LoRA. Uses WanImageToVideo node + two-stage KSamplerAdvanced + ModelSamplingSD3 shift=5.0. 640×640, 81 frames, 16fps. ~80s/clip, FREE/local. Minor foot artifacts on pixel art (Pixel Quantizer handles). **Replaces 5B model completely.**
- **PixelLab API** — Public API with Python SDK. Pay-per-use ($0.007-$0.016/gen). "Animate with Skeleton" + "Estimate Skeleton" endpoints. Max 128×128. Native pixel art output. **Viable for pipeline integration — test in Phase 5.**

**DEPRECATED/DEAD:**
- ~~**Wan 2.2 5B ti2v**~~ — DEPRECATED. Character distortion, no locomotion from single keyframe, used wrong node (Wan22ImageToVideoLatent). Replaced by 14B dual-model workflow.
- ~~**Retro Diffusion rd-animation**~~ — DEAD. 48x48, wrong character, wrong style.
- ~~**Pika Pikaframes 2.2**~~ — SCRAPPED. Jobs didn't complete, $0.20/gen minimum.

**UNTESTED (future evaluation):**
- **Kling 3.0** — Elements character lock, start/end frame API. Test if Wan 2.2 14B quality insufficient.
- **Google Veo 3.1** — Native 4K, resolution mismatch for pixel art. Test last.
- **LTX-2** — Open-source (Apache 2.0), 4K@50fps, NVIDIA-optimized.
- **Seedance 2.0** — ByteDance, reference-to-video with expression/motion transfer.
- **Ludo.ai Sprite Animator** — Combat animation presets, MCP API.
- **Pixverse v4.5** — First+last frame sprite sheet workflow.
- ~~**Wan 2.5**~~ — NOT open source. Do not use.

**CRITICAL: Wan 2.2 14B Workflow Requirements (learned from Phase 4 debugging):**
- Must use `WanImageToVideo` node (NOT `Wan22ImageToVideoLatent` — that node doesn't connect image conditioning properly)
- Must use dual 14B fp8 models: `wan2.2_i2v_high_noise_14B_fp8_scaled` + `wan2.2_i2v_low_noise_14B_fp8_scaled`
- Must use LightX2V 4-step LoRAs for each model
- Must use `ModelSamplingSD3` shift=5.0 on both models
- Must use two-stage `KSamplerAdvanced`: stage 1 (high noise, steps 0-2, adds noise) → stage 2 (low noise, steps 2-4, refines)
- Must use `wan_2.1_vae.safetensors` (NOT wan2.2_vae)
- Must use `CreateVideo` + `SaveVideo` nodes (NOT VHS_VideoCombine)
- Input images MUST have solid background (green screen). Transparent backgrounds cause dark/lifeless output.
- Pixel art walk cycles are seed-dependent — generate 3-5 seeds and pick the best one.

**Architecture: Model-agnostic adapter layer is mandatory.** The manifest declares animation intent, the system routes to the best available generator. Four atomic adapter operations: `generateFrame`, `generateKeyframes`, `interpolateFrames`, `generateVideo`. All council models converge on this.

**Full Production Scope:**
- 6 Champions (128×128) + 6 Bosses (256×256)
- 13 animations each × 4-12 frames = ~900-1,400 total frames
- Style: full-color arcade fighter (SF2/Capcom), transparent backgrounds, generate facing RIGHT

**Source files:**
- `Current-Sprite-Sheet-Pipeline-Workflow-Docs/CLAUDE.md` — Implementation rules, architecture, anti-patterns
- `Current-Sprite-Sheet-Pipeline-Workflow-Docs/README.md` — Pipeline overview, problem statement, 7-stage flow
- `Current-Sprite-Sheet-Pipeline-Workflow-Docs/Project_ Sprite-Sheet-Automation-Project_2026 — Original Workflow Summary.md` — Tech stack rationale, hexagonal architecture explanation, MVP scope
- `Current-Sprite-Sheet-Pipeline-Workflow-Docs/CHANGELOG.md` — v0.1.0 release notes (Jan 21, 2026), 1004+ tests, 67 stories
- `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/hybrid-pipeline-plan.md` — THE key doc: approved hybrid architecture, 4 phases, adapter layer spec, post-processing pipeline, video model landscape
- `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/workflow-operations-guide.md` — Full operations manual: asset counts, prompt library, step-by-step workflows for both strategies
- `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/claude-code-kickoff-prompt.md` — Ready-to-paste prompt for building the Pixel Quantizer in Claude Code
- `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/video-model-pipeline-kickoff-prompt.md` — Ready-to-paste prompt for video model research and testing
- `*SPRITE SHEET COUNCIL RESULTS/Perplexity-Final-Results-Analysis.md` — Cross-model consensus analysis (the synthesis)
- `*SPRITE SHEET COUNCIL RESULTS/Claude Opus 4.6 Thinking-response.md` — Opus's full analysis (motion transfer discovery, optical flow audit gate)
- `*SPRITE SHEET COUNCIL RESULTS/GPT-5.2 Thinking-response.md` — GPT's full analysis (DAG render graph, capability discovery)
- `*SPRITE SHEET COUNCIL RESULTS/Gemini 3 Pro-response.md` — Gemini's full analysis ("Quantized Motion Bridge")
- `*SPRITE SHEET COUNCIL RESULTS/CSV/` — 4 CSV comparison matrices (agreements, disagreements, unique findings)

### Workstream C: Autoresearch + LoRA Training (THE MULTIPLIER)

**Goal:** Apply Karpathy's autoresearch pattern to automate ComfyUI workflow optimization, and train a style LoRA to accelerate sprite generation.

**Autoresearch for ComfyUI (the big idea — UPDATED with proven components):**
Map the three-file architecture to ComfyUI: `prepare.py` = input images + evaluation function + ComfyUI API client | `train.py` equivalent = the mutable workflow JSON | `program.md` = agent instructions. **Don't build from scratch — assemble proven components:**
- **Mutation operators:** Fork from ComfyGI (arXiv:2411.14193) — validated KSampler parameter mutations achieved 50% improvement, 90% human preference
- **Search strategy:** Optuna TPE/GP sampler for parameters (converges in 50-100 trials vs 300+ random). Reserve LLM agent for prompt optimization (DSPy-style)
- **Scoring:** ImageReward ComfyUI node (ZaneA/ComfyUI-ImageReward) as primary fitness function — already proven in ComfyGI
- **Starting workflow:** Use the official NB2 Animated Sprite Sheet ComfyUI template (Mar 7, 2026) as the mutable artifact
- **Quality metrics upgrade:** Replace CLIP+SSIM+aesthetic with four-stage gate: (1) hard gates (palette, size), (2) DISTS + DINOv2 cosine for perceptual consistency, (3) CLIP + EDOKS for style/color, (4) cross-frame SSIM + DINOv2 identity. Add Qwen3-VL LLM-as-Judge for structured rubric grading with failure tags.
- ~60-120 experiments/hour on RTX 5080. Use `--force-fp16` flag for reduced VRAM.

**This depends on Workstream A infrastructure:** The Mac Mini orchestrates, the Alienware runs ComfyUI + scoring, WOL wakes the Alienware for overnight runs.

**LoRA Training — ABANDONED (April 8, 2026):**

Training Run 001 completed successfully (61 images, 3,050 steps, loss 0.080, 2h 12m on RTX 5080). 33-image ComfyUI test matrix showed the LoRA shifts Illustrious XL v2.0 toward pixel art but produces anime-proportioned characters with HUD artifacts — not the SF2 arcade aesthetic needed. Multiple prior attempts across the project also failed. **Decision: LoRA path abandoned. Gemini NB2 keyframes produce the correct style natively and score 87.6% through RIFE+Quantizer.** Training infrastructure (kohya_ss, scripts, configs) remains on Alienware if ever needed for a different use case.

| What Was Tried | Result |
|----------------|--------|
| kohya_ss dev, Illustrious XL v0.1, Adafactor, SDPA, rank 32, 61 images, 10 epochs | Loss 0.080 (healthy), but output style wrong for SF2 sprites |
| Inference on Illustrious XL v2.0, strength sweep 0.5-1.0, 3 poses | Best results at 0.9-1.0 but still anime-hybrid, not arcade pixel art |

**Critical RTX 5080 requirements:** PyTorch ≥2.7.0 stable cu128 (nightly no longer needed), CUDA 12.8+, cuDNN 9.x, NO xformers (use SDPA), kohya_ss dev branch only. ComfyUI v0.18.2+ with `--force-fp16` flag for VRAM savings.

**VRAM Budget (16GB):**

| Scenario | Available VRAM | Max Model |
|----------|---------------|-----------|
| ComfyUI active (heavy) | 4-8GB free | 7B Q4 only |
| ComfyUI inactive | Full 16GB | 14B Q4 |
| LoRA training | ~10GB (fused backward) | Fits with headroom |

**Source files:**
- `Autoresearch-ComfyUI-Overview.md` — Full autoresearch concept explanation, ComfyUI mapping, hardware fit, implementation sketch
- `LoRA Training Research - Perplexity Computer/ref-lora-training-rtx5080-sprite-pipeline.md` — THE key LoRA doc: complete training guide, RTX 5080 config, kohya_ss setup, autoresearch optimization loop
- `LoRA Training Research - Perplexity Computer/lora-guide-content.md` — Framework comparison (kohya_ss vs ai-toolkit vs SimpleTuner vs OneTrainer), dataset prep
- `LoRA Training Research - Perplexity Computer/LoRA-training-perplexity-computer-follow-up.md` — RTX 5080/5090 compatibility report, confirmed working configs, known bugs (cutlassF crash fix)
- `LoRA Training Research - Perplexity Computer/comfyui-lora-training-guide.pdf` — PDF version of the comprehensive training guide
- `LoRA Training Research - Perplexity Computer/perplexity-ui-ux-research-prompt.md` — Ready-to-paste Perplexity prompt for dashboard UI/UX research (not yet executed)

---

## Part 3: Dependency Chain

```
Workstream A (Agent SDK Infrastructure)                       [COMPLETE — Phase 1-4]
    ├── hybrid_router.py (three-machine routing)
    ├── Mac Mini as always-on orchestrator
    ├── WOL for Alienware
    ├── Safety hooks (loop-detector, cost-watchdog, vault-integrity)
    └── launchd schedules on Mac Mini
         │
         ├──────────────────────────────────────┐
         ▼                                      ▼
Workstream B (Sprite Pipeline)           Workstream D (Knowledge Compounding)  ←── NEW Phase 6
    [COMPLETE — Phase 1-4]                   ├── Gemma 4 benchmarking + model routing updates (6.A)
    ├── Pixel Quantizer ✅                    ├── SessionEnd hook → flush.py → daily logs (6.D.1)
    ├── Video model eval ✅                   ├── Vault Indexer v2 + synthesis loop (6.D.2)
    ├── Hybrid pipeline E2E ✅                ├── Knowledge Lint agent (6.D.3)
    ├── Adapter layer ✅                      └── Autoresearch feedback loop (6.D.4)
    └── Scale to full roster                       │
         │                                         │  ◄── FEEDS BACK INTO ──►
         ▼                                         │
Workstream C (Autoresearch + Scale)        ────────┘
    [IN PROGRESS — Phase 5]
    ├── ComfyGI mutation operators + Optuna TPE
    ├── ImageReward + quality metrics
    ├── Overnight runs: Mac Mini orchestrates, Alienware scores
    └── Knowledge articles from D improve next night's prompts (virtuous cycle)
```

**Key insight:** Workstreams A and B can start in parallel. The Pixel Quantizer prototype is pure Node.js/TypeScript — it doesn't need the Agent SDK at all. You can be building the quantizer on your MacBook while setting up Ollama on the Mac Mini.

---

## Part 4: Execution Timeline (Starting March 27, 2026)

### Phase 1: Foundation (Weeks 1-2 — Mar 27 - Apr 10)

**Workstream A — Three-Machine Setup:** ✅ COMPLETED March 28-30, 2026
- [x] Ollama on Mac Mini: `phi4-mini-reasoning` (3.8B) + `nomic-embed-text`. LAN access permanent via LaunchAgent plist.
- [x] MLX-LM v0.31.1 on MacBook Pro (Python 3.13 venv): `Qwen3-14B-4bit` (31 tok/s) + `Qwen2.5-Coder-32B-Instruct-4bit`.
- [x] Ollama on Alienware: `qwen3-vl:8b` (note: tagged `:8b` not `:7b`). `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_KEEP_ALIVE=2m`.
- [x] ComfyUI updated on Alienware. Launch with `--force-fp16`.
- [x] Deco 7 Pro BE63 mesh network: Mac Mini `192.168.68.200`, Alienware `192.168.68.201` (static IPs, wired to bedroom Deco).
- [x] Built `lib/hybrid_router.py` — three-tier routing with WOL, fallback chain, async health checks. 10/10 tests pass.
- [x] Built safety hooks: loop-detector (exit 2 on 3rd dup), cost-watchdog ($0.50 default), vault-integrity (filelock + anchor check).
- [x] Built `lib/keychain.py` — macOS Keychain credential helper with CLI.
- [x] Updated `config.toml` with `[routing]` section for all 3 machines + 8 task mappings.
- [x] Smoke test: 14/14 checks pass in dry-run mode.
- [ ] Audit skills for interactive language ("ask me", "confirm with user") → replace with autonomous decision criteria.
- [ ] Update all SDK imports: `claude-agent-sdk` package, `ClaudeAgentOptions` class.

**Workstream B — Pixel Quantizer Gate Check + New Tool Evaluation:**
- [x] Built Pixel Quantizer prototype at `16bitfit-battle-mode/pixel-quantizer/` — 13 unit tests pass, all 7 steps working.
- [x] Tested with 3 synthetic frames: 512x512 → 128x128, 0 off-palette pixels, <30ms total, palette-compliant.
- [x] **GATE CHECK: PASS** — algorithms are sound, architecture is solid. Caveat: needs testing with real video model output (Pika/Kling/Veo frames) to confirm with non-synthetic input.
- **NOTE:** Alpha recovery runs before palette quantization (reordered from original spec for better results — green background pixels don't get snapped to palette colors).
- **NOTE:** "Grid alignment" (Step 6 in SOT) is implemented as "Baseline Registration" (vertical sprite alignment). Standardize naming.
- [ ] Install GENKAIx PixelArt Processing Nodes in ComfyUI — test as alternative to custom quantizer steps 1-2.
- [ ] **Test Retro Diffusion rd-animation** via Replicate API — does it produce acceptable SF2-style sprites? If YES → could bypass quantizer for many animations.
- [ ] **Test PixelLab "Animate with Text" v3** — native pixel art animation output. If quality meets SF2 standard, simplifies pipeline dramatically.
- [ ] **Test Ludo.ai combat presets** via MCP API — fighting game animation presets with Y-offset alignment.
- [ ] Move Pixel Quantizer to sprite pipeline repo (`16BitFit-V3` or `16BitFit-Asset-Creation`) when available.

### Phase 2: First Agents + Video Model Testing (Weeks 3-4 — Apr 10 - Apr 24) ✅ COMPLETE (7/8 PASS, 1 DEFERRED)

**Workstream A — First Autonomous Agents:**
- [x] Skills audit: 5 interactive patterns fixed in 3 skill files (process-inbox, daily-driver, personal-finance). Zero interactive patterns remaining.
- [x] Process Inbox agent → `agents-sdk/agents/process_inbox.py`, Mac Mini, 100% local (`phi4-mini-reasoning` 3.8B), max 15 turns, $0.25 cap, baton file on success
- [x] Spending Analysis agent → `agents-sdk/agents/spending_analysis.py`, MacBook Pro, 100% local (Qwen3-14B via MLX-LM) + `lib/csv_sanitizer.py`
- [x] Baton File dependency chain: `lib/baton.py` + `com.sean.agent.daily-morning-baton.plist` (WatchPaths trigger). Process Inbox → flag → Daily Driver.
- [ ] Verify Mac Mini runs morning schedules reliably without laptop open (needs launchd plists installed on Mac Mini)

**Workstream B — Video Model Sprint:**
- [x] Video eval framework built: `pixel-quantizer/video-eval/` with hexagonal adapters (StubAdapter, GeminiAdapter, PikaAdapter + stubs). Gate check PASS with synthetic frames (64.6% overall, 100% palette).
- [x] NB2 vs NB Pro benchmark: **NB2 wins** — 26% faster (13.8s vs 18.7s avg), comparable quality. Use NB2 for volume, NB Pro for anchors. 4 keyframes saved to `eval-results/keyframe-*.png`.
- [x] ~~Pika Pikaframes 2.2~~ — DEFERRED then SCRAPPED. Jobs queued but didn't complete. $0.20/gen minimum, base64 delivery issues. **Decision: pivot to Wan 2.2 (free/local) + rd-animation (Replicate) in Phase 3.**
- [ ] Test Kling 3.0/2.6 — deferred to future phase if needed
- [ ] **Wan 2.2 + pixel animation LoRAs** — moved to Phase 3 (primary video model candidate)
- [ ] **GMFSS Fortuna** — moved to Phase 3 (local interpolation candidate)
- [x] Green screen technique documented: `background_color="#00FF00"` in KeyframeConfig, applied before video model input
- [ ] Install Sprite Smithy ($30) — still pending

### Phase 3: Pipeline Integration + PM Agents (Weeks 5-6 — Apr 24 - May 8) ✅ COMPLETE (10/10 PASS)

**Workstream A — PM Layer:**
- [x] Jira MCP: Native `claude.ai Atlassian` MCP active, 28 projects visible, sprint data accessible via JQL. No Keychain creds needed.
- [x] Sprint Health Monitor → `agents-sdk/agents/sprint_health.py`, Claude Sonnet via API, Jira MCP read-only, Friday 15:00, $0.50 cap. Dry-run PASS.
- [x] Meeting Defender → `agents-sdk/agents/meeting_defender.py`, Mac Mini (phi4-mini-reasoning) + Haiku, READ-ONLY calendar tools, NEVER auto-declines, Monday 07:00, $0.25 cap. Dry-run PASS.

**Workstream B — Hybrid Pipeline End-to-End:**
- [x] Generator adapter interface: 4 atomic ops (generateFrame, generateKeyframes, interpolateFrames, generateVideo) + strategy router mapping 15 animation types (10 IMAGE_ONLY, 5 HYBRID). All assertions pass.
- [x] ~~Wan 2.2 5B ti2v~~ — DEPRECATED in Phase 4. Used wrong node (`Wan22ImageToVideoLatent`), produced distortion and no locomotion. **Replaced by Wan 2.2 14B dual-model workflow** (WanImageToVideo + LightX2V 4-step LoRA). 14B quality significantly better.
- [x] Wan22Adapter, RIFEAdapter (was GMFSSAdapter), ReplicateAdapter — all behind `VideoModelAdapter` hexagonal interface.
- [x] End-to-end test: NB2 keyframes → Wan 2.2 5B → extract 8 frames → Pixel Quantizer → 73.7% overall. GATE CHECK PASS. Only 4% degradation from raw keyframes (77.7%).
- [x] Strategy decision map: 10 animations → IMAGE_ONLY, 5 → HYBRID. Duration mapping (1s combat, 2s locomotion). Frame counts (4-12 per type).
- [x] rd-animation via Replicate: TESTED, NOT VIABLE (48x48, wrong character, wrong style). Removed from strategy map.
- [x] ~~GMFSS Fortuna~~ → **RIFE VFI confirmed as primary interpolation engine.** GMFSS blocked by cupy dependency. RIFE VFI (rife49.pth) tested: character identity PASS, pose transitions PASS, green screen PASS. Color expansion (79K-103K unique colors) handled by Pixel Quantizer. FILM VFI available as backup (slightly more ghosting). Bonus VFI models available (AMT, CAIN, FLAVR) — untested, same node pack.
- [x] ~~Wan 2.2 14B I2V: BLOCKED~~ → **RESOLVED in Phase 4.** ComfyUI v0.3.52 fixed channel mismatch. 14B dual-model (fp8) + LightX2V 4-step LoRA now working. Uses `WanImageToVideo` node (NOT `Wan22ImageToVideoLatent`). Character animation with minor foot artifacts — Pixel Quantizer handles. Walk cycle quality is seed-dependent.

**Key findings (updated Phase 4):** (1) Wan 2.2 5B is deprecated — 14B dual-model is vastly superior. (2) RIFE VFI → Pixel Quantizer = 87.6% (best score in project). (3) Walk cycle strategy: NB2 keyframes → RIFE VFI for interpolation, Wan 2.2 14B for single-keyframe animation. (4) PixelLab has a public API — viable alternative for Phase 5.

### Phase 4: LoRA + Memory Layer (Weeks 7-8 — May 8 - May 22) ✅ COMPLETE (11/11 PASS)

**Workstream A — Retrieval & Memory:**
- [x] Vault Embedding Indexer → `agents-sdk/agents/vault_indexer.py`, Mac Mini, nomic-embed-text → SQLite, nightly 02:00, $0.00 cap. Dry-run PASS (274 vault files discovered).
- [x] Preserve Session → `agents-sdk/agents/preserve_session.py`, MacBook Pro, Qwen3-14B via MLX-LM, on-demand, $0.00 cap. Dry-run PASS (auto-detected session log).
- [x] PR Digest → `agents-sdk/agents/pr_digest.py`, MacBook Pro, Qwen2.5-Coder-32B via MLX-LM, daily 08:00, $0.00 cap. Dry-run PASS (needs `gh auth login`).

**Workstream B — Pipeline Hardening:**
- [x] RIFE VFI → full Pixel Quantizer: **87.6% overall, 96.4% palette, 0 off-palette pixels, 100% outline coverage.** Best score in project. Color expansion (79K-103K unique colors) fully cleaned.
- [x] Wan 2.2 14B I2V: Working via ComfyUI built-in template. Dual fp8 models + LightX2V 4-step LoRA. ~80s/clip. Minor pixel art artifacts (seed-dependent). Adapter updated.
- [x] Wan 2.2 5B → DEPRECATED. Wrong node, wrong architecture, distortion, no locomotion.
- [x] PixelLab v3: Public API confirmed ($0.007-$0.016/gen). Python SDK available. Skeleton-based animation. Build PixelLabAdapter in Phase 5.

**Workstream C — LoRA Training:**
- [x] kohya_ss training config: `lora-training/sprite-style-config.toml` (Adafactor, SDPA, rank 32, Illustrious XL v0.1, fused backward pass, bf16)
- [x] Dataset prep script: `lora-training/prepare_dataset.py` — nearest-neighbor upscale verified sharp, auto-captioning with trigger word
- [x] Training runbook: `lora-training/TRAINING-RUNBOOK.md` — complete step-by-step for Alienware
- [x] ~~Collect 30-50 training images~~ → Collected 61 images (36 original + 15 supplement + extras) via Gemini NB2
- [x] ~~Download Illustrious XL v0.1 + install kohya_ss dev branch on Alienware~~ → Done. kohya_ss v25.2.1, PyTorch 2.7.0+cu128.
- [x] ~~Train first style LoRA~~ → Training Run 001 complete: 3,050 steps, 2h 12m, loss 0.080. Two checkpoints (epoch 5 + 10).
- [x] ~~Test LoRA in ComfyUI pipeline~~ → 33-image test matrix on Illustrious XL v2.0. Results: recognizable characters but anime-proportioned, multi-character, HUD artifacts. Not SF2-quality.
- [x] **DECISION: LoRA path ABANDONED.** Multiple training attempts across project history produced consistently poor results for SF2-style pixel art. Gemini NB2 keyframes are confirmed superior (77.7% raw, 87.6% through RIFE+Quantizer). LoRA adds complexity for worse output. Workstream C refocused on autoresearch (ComfyUI workflow optimization) only.

### Phase 5: Autoresearch + Scale (Weeks 9-12 — May 22 - Jun 19) ✅ COMPLETE (9/9 PASS, 2026-04-11)

**Workstream B — Scale:**
- [x] Expand to full strategy decision map (15 animation types × IMAGE_ONLY/HYBRID routing)
- [x] Sheet→split approach for IMAGE_ONLY generation (replaces per-frame — 5x faster, 6x cheaper)
- [x] Full roster: 12/12 characters, 180/180 animations, 1,020 frames, 0 failures
- [x] HYBRID pipeline: 60/60 animations interpolated via RIFE VFI (815 frames)
- [x] Palette expansion: Sean 16→27, generic sf2_pixel_art 38 colors
- [x] Grid detection bug fixed (excess_penalty + size_penalty)
- [x] RIFE connectivity fixed (VPN root cause, httpx retries, pre-flight health check)
- [x] Pixel Quantizer verified on 7/12 characters (100% pass, 0 off-palette)
- [x] PixelLabAdapter built behind VideoModelAdapter interface
- [ ] Re-generate 3 problematic idle animations (Marcus text overlay, Gym Bully + Procrastination Phantom multi-character)
- [ ] Run Pixel Quantizer on full roster (remaining 5 characters)
- [ ] Autoresearch plan revision (remove LoRA, focus on Gemini prompt optimization + LoRA-free ComfyUI optimization)
- [ ] Build sprite pipeline dashboard (reference: Perplexity UI/UX research prompt already written)

**Workstream C — Autoresearch Loop (built on proven components, LoRA-free):**
- [x] Autoresearch framework built: Optuna TPE study, dry-run trials, SQLite resume, JSONL logging
- [x] ComfyUI workflow mutator: loads RIFE workflow, mutates KSampler + RIFE params, targets Alienware
- [ ] Fork ComfyGI mutation operators (checkpoint, ksampler, prompt_word, prompt_llm)
- [ ] Install ImageReward ComfyUI node as primary fitness function
- [ ] Use official NB2 Animated Sprite Sheet template as starting workflow JSON
- [ ] Implement upgraded quality metrics: DISTS + DINOv2 + EDOKS + Qwen3-VL LLM-as-Judge
- [ ] Configure overnight runs: Mac Mini orchestrates, Alienware runs ComfyUI + scoring
- [ ] Evaluate ComfyUI CacheProvider API for parallel experiments (multiple worker instances sharing model cache)
- [ ] First optimization target: find optimal NB2 prompt templates + RIFE interpolation params for each animation type (LoRA abandoned — focus on prompt + pipeline optimization)

**Workstream A — Meta:**
- [x] Meta-Agent built: fleet health monitor, 06:30 daily, $0.10 cap, dry-run PASS
- [x] Full fleet token audit: ~$15/mo current → $6/mo recommended → $0/mo possible (local inference)
- [ ] Implement prompt caching scheduling (cluster API agents in 5-min windows)

**Agent fleet status (April 9 downsizing audit):** 2 active agents (vault-indexer + daily-driver morning). 6 disabled due to CLIConnectionError and MCP headless limitations. Meta-agent built but not yet deployed. Do NOT re-enable disabled agents without Sean's explicit approval.

### Phase 6: Gemma 4 Benchmarking + Knowledge Compounding Loop (Weeks 13-16 — Jun 19 - Jul 17)

**Why this phase exists:** Phases 1-5 built agents, infrastructure, and the sprite pipeline. Phase 6 adds the meta-layer — model currency (Gemma 4 benchmarking) and a self-improving knowledge system (SessionEnd capture → vault synthesis → knowledge lint → autoresearch feedback). The core idea comes from Karpathy's LLM Wiki pattern and cole's claude-memory-compiler: your vault should be a living knowledge graph that the LLM maintains, not a static archive that the LLM searches. Phase 5's autoresearch generates experimental results nightly; Phase 6 captures those results into synthesized concept articles that feed back into the next night's autoresearch — a virtuous cycle.

**Can start in parallel with Phase 5 (Week 10+).** Gemma 4 benchmarking and SessionEnd hook have zero dependencies on autoresearch. Vault synthesis benefits from autoresearch output but doesn't require it.

**Gate Check (Phase 6 success criteria):**
- Gemma 4 benchmarks complete on all 3 routing tasks with head-to-head scoring
- At least 1 model swap approved and deployed based on winning benchmark
- SessionEnd hook active and capturing ≥3 sessions/week into daily logs
- Vault Indexer synthesis producing ≥2 concept articles + ≥1 connection article per nightly run
- Knowledge Lint detecting structural issues with ≥95% recall on synthetic test vault
- Autoresearch convergence improves ≥10% (measured by Optuna trials-to-best-fitness)

**Workstream A — Gemma 4 Model Benchmarking & Integration:**

Gemma 4 has native function calling with 6 dedicated tokens (purpose-built for agentic tool-use, not prompt-engineered like Qwen). 256K context window, fully multimodal (text/image/video/audio), outperforms Llama 4 on math/code/agentic benchmarks. The 27B MoE variant activates only 3.8B parameters (same active count as phi4-mini but from a larger model). The 31B dense variant is the benchmark target for MacBook Pro tasks.

- [ ] Download Gemma 4 27B MoE via Ollama on Mac Mini: `ollama pull gemma4:27b`. Verify function calling tokens work in test prompts. Compare startup time vs phi4-mini-reasoning.
- [ ] Download Gemma 4 31B via MLX-LM on MacBook Pro. Benchmark startup time and tok/s vs Qwen3-14B-4bit (current: 31 tok/s).
- [ ] Build benchmark harness: `agents-sdk/lib/gemma4_benchmark.py`. Framework for testing same prompt + context across multiple models with metrics: latency (p50/p95 across 10 runs), tok/s throughput, quality score (Jaccard similarity on extracted entities vs golden set).
- [ ] Create golden test sets (20 samples each): (1) Inbox triage — classify email into 5 categories + extract 3 action items via function calling. (2) Financial analysis — parse CSV row → categorize expense + suggest budget adjustment. (3) Code review — read 50-line Python snippet → identify issues + rate 1-5.
- [ ] Run 60 benchmark samples (20 per task × 3 models) on same hardware/timing. Output: `results/gemma4-benchmark-YYYY-MM-DD.json` + human-readable summary table.
- [ ] Swap decision (veto gate: if Gemma 4 quality ≥5% worse than incumbent, keep incumbent — quality over speed):
  - Expected: Gemma 4 27B MoE replaces phi4-mini-reasoning on Mac Mini for inbox triage + Anki cards
  - Possible: Gemma 4 31B replaces Qwen3-14B on MacBook Pro for financial analysis IF quality ≥99% of Qwen3-14B
  - Unlikely: Keep Qwen2.5-Coder-32B for code review (code understanding is Qwen's strength)
- [ ] Update `config.toml` `[routing]` section with new model assignments. Test all launchd agents with new routing (5/5 must pass).
- [ ] (Optional, Week 16) If Gemma 4 27B MoE is swapped into Mac Mini orchestrator role, test autoresearch loop function calling reliability. Hypothesis: native function tokens reduce prompt engineering overhead → ≥10% faster Optuna convergence. Metrics: function calls executed correctly / total attempted (target: ≥98%).

**Workstream D — Knowledge Compounding Loop (NEW WORKSTREAM):**

Four components: SessionEnd hook (capture) → Vault Indexer v2 (synthesize) → Knowledge Lint (health check) → Autoresearch feedback (virtuous cycle). All run 100% local. Together they transform the vault from a static archive into a self-maintaining knowledge graph.

*D.1 — SessionEnd Hook + Daily Flush (auto-capture session knowledge):*

Currently sessions evaporate unless you manually write notes. The existing Preserve Session agent (`preserve_session.py`) works but is on-demand only. This makes it automatic.

- [ ] Create SessionEnd hook at `.claude/hooks/session-end-flush.sh`. Hook spawns `agents-sdk/agents/flush.py` as a detached background process with the session transcript path. Guard against recursion: check `CLAUDE_INVOKED_BY` env var — if set, skip (flush.py itself may start sub-sessions).
- [ ] Build `agents-sdk/agents/flush.py` — Knowledge extraction agent. Input: session transcript. Output: appends to `vault/daily/YYYY-MM-DD.md`. Extracts 5 sections: Decisions Made, Lessons Learned, Action Items, Patterns Noticed, Key Quotes (2-3 verbatim snippets). Model: phi4-mini-reasoning on Mac Mini for speed (~5-10s per session). Route complex sessions (>100 messages) to Qwen3-14B on MacBook Pro via hybrid_router for quality.
- [ ] Daily log format:
  ```markdown
  # Daily Log — 2026-06-20

  ## Sessions
  - Claude Code: 2h 15m, 180 messages, tag: sprite-pipeline
  - Cowork: 45m, 32 messages, tag: pm-planning

  ## Decisions
  - Chose Gemma 4 27B MoE for Mac Mini inbox triage (benchmarks: 18% speedup)

  ## Lessons
  - Native function calling tokens in Gemma 4 reduce prompt engineering overhead
  - Wan 2.2 14B requires WanImageToVideo node, NOT Wan22ImageToVideoLatent

  ## Action Items
  - [ ] Deploy Gemma 4 MoE to production launchd schedule
  - [ ] Test PixelLab skeleton API on 5 animations

  ## Patterns
  - Session lengths >2h often indicate architectural clarity moment before implementation
  - Video model selection keeps hitting node/LoRA compatibility — pin ComfyUI versions

  ## Quotes
  > "RIFE VFI pipes 87.6% through Pixel Quantizer — that's our quality floor"
  ```
- [ ] Auto-trigger compile: After 6 PM, if daily log was updated since last compile, trigger Vault Synthesizer (D.2).
- [ ] Place daily logs inside vault at `vault/daily/` (not parallel structure) so MOCs can link to them and Obsidian metadata panel shows recent logs. Create `vault/daily/INDEX.md` MOC listing all logs by date.
- [ ] Filelock: flush.py acquires lock on `vault/daily/` before writing, releases after close. Uses existing `lib/filelock` from Phase 1.
- [ ] Add `vault/daily/*.md` to Vault Indexer exclusion list (don't re-embed daily logs — they feed synthesis, not search).
- Machine: Mac Mini (phi4-mini) or MacBook Pro (Qwen3-14B for complex sessions)
- Schedule: Immediate on session end, async/detached
- Cost: $0.00 (local)
- Success: Hook fires on ≥5 session closes, flush.py completes without errors, recursion guard blocks self-calls

*D.2 — Vault Indexer v2: Synthesis Loop (upgrade existing agent):*

Currently the Vault Indexer (2 AM, Mac Mini, nomic-embed-text) only creates embeddings. This upgrade adds a synthesis pass that produces concept and connection articles — the core of the "living knowledge graph."

- [ ] Update `agents-sdk/agents/vault_indexer.py`: After embedding pass, run change detection. Implement hash-based state tracking in `vault/.indexer-state.json` (`{filepath: sha256_hash, last_processed_timestamp}`). Compare hashes: changed file = hash mismatch, new file = hash not in state. Filter: exclude `vault/daily/`, `vault/.obsidian/`, `.indexer-state.json`, PDFs, media.
- [ ] Route synthesis tasks to MacBook Pro via `hybrid_router.py`. Schedule: Mac Mini detects changes at 2:15 AM → WOL wakes MacBook Pro → synthesis runs at 2:30 AM → completes by 3:15 AM. Fallback: if MacBook unreachable, defer synthesis to next night (log warning, don't block).
- [ ] Build `agents-sdk/agents/vault_synthesizer.py` — Concept + connection article generator. Model: Qwen3-14B via MLX-LM (or Gemma 4 31B if it wins Phase 6 benchmarks). Max turns: 25. Max runtime: 45 min.
- [ ] Synthesizer logic per changed file: (1) Read changed file + retrieve 5 semantically similar vault files via nomic-embed-text SQLite index. (2) Extract 2-5 key concepts via LLM. (3) For each concept: search vault for 2+ related files. If found, generate concept article at `vault/knowledge/concepts/concept-name.md`. (4) Identify cross-cutting themes across 3+ concepts → generate connection article at `vault/knowledge/connections/theme-name.md`. (5) Every article must include wikilinks to ≥2 other articles (graph requirement — no isolated nodes).
- [ ] Concept article template:
  ```yaml
  ---
  title: "Concept Name"
  type: concept
  sources: [list of 2+ source files]
  tags: [auto-generated]
  created: 2026-06-20
  updated: 2026-06-20
  ---
  ```
  Sections: Definition (2-3 sentences), Context (why it matters), Examples (2 concrete from source material), Related Concepts (wikilinked).
- [ ] Connection article template:
  ```yaml
  ---
  title: "Theme: Concept A + Concept B + Concept C"
  type: connection
  connects: [list of 3+ concepts/files]
  created: 2026-06-20
  ---
  ```
  Sections: Synthesis (1-2 sentences explaining the relationship), one thread per concept with evidence, Implications (how this informs future work).
- [ ] Auto-maintain `vault/knowledge/index.md` — master catalog with article paths, summaries, source links, date. Regenerated after each synthesis run.
- [ ] Add `[vault_indexer]` section to `config.toml`:
  ```toml
  [vault_indexer]
  enabled = true
  embedding_model = "nomic-embed-text"
  synthesis_enabled = true
  synthesis_machine = "macbook-pro"
  synthesis_model = "qwen3-14b"
  synthesis_max_minutes = 45
  exclude_paths = ["vault/daily", "vault/.obsidian", "*.pdf"]
  state_file = "vault/.indexer-state.json"
  ```
- Machine: Mac Mini (orchestrator + embeddings) → MacBook Pro (synthesis via WOL)
- Schedule: Nightly 2:00 AM (embedding) → 2:30 AM (synthesis)
- Cost: $0.00 (local)
- Success: ≥2 concept articles + ≥1 connection article per run, all articles have ≥2 wikilinks, index.md auto-updates

*D.3 — Knowledge Lint Agent (weekly health checks):*

Without health checks, knowledge rot is inevitable at 274+ vault files. This agent catches contradictions, stale info, orphan notes, and broken wikilinks before they compound.

- [ ] Build `agents-sdk/agents/knowledge_lint.py`. Two-tier checks:
  - **Tier 1 (Mac Mini, phi4-mini-reasoning, ~5 min):** Structural — broken wikilinks (regex scan `[[...]]` → verify target exists), orphan files (0 inbound links), missing YAML frontmatter in `vault/knowledge/`, file naming consistency (kebab-case enforcement).
  - **Tier 2 (MacBook Pro, Qwen3-14B, triggered only if Tier 1 finds issues OR weekly full scan):** Semantic — contradiction detection (compare claims across related articles), staleness detection (flag articles >30 days old referencing time-sensitive info like model releases or API changes), SOT drift check (does SOURCE-OF-TRUTH.md Part 1-2 align with vault articles?).
- [ ] Output: `vault/health/YYYY-MM-DD-lint-report.md` with severity levels (CRITICAL / HIGH / MEDIUM / LOW) and specific recommendations.
- [ ] Dry-run testing: Create synthetic 20-file vault with planted issues (broken links, orphans, contradictions, stale dates). Verify lint catches ≥95%.
- [ ] Update `agents-sdk/agents/daily_driver.py`: Check for lint report with CRITICAL or HIGH issues → surface in morning briefing with "Vault Health" section + deep link to full report. No issues = brief "Vault health: PASS ✓" line.
- Machine: Mac Mini (Tier 1) + MacBook Pro (Tier 2 via hybrid_router)
- Schedule: Sunday 22:00 weekly
- Cost: $0.00 (local)
- Max turns: 20 (Tier 1) + 30 (Tier 2)
- Success: ≥95% recall on synthetic test vault, report formats correctly, Daily Driver surfaces alerts

*D.4 — Knowledge → Autoresearch Feedback Loop (the virtuous cycle):*

This is the connective tissue between Phase 5 (autoresearch) and Phase 6 (knowledge compounding). Vault synthesis captures what autoresearch learns each night; the next night's autoresearch reads those articles for better-informed optimization.

- [ ] Update autoresearch orchestrator to read `vault/knowledge/concepts/` at startup (23:30, before overnight run). Filter for articles tagged `#autoresearch`, `#comfyui`, `#optimization`, `#rife`, `#pixel-quantizer`. Extract code snippets + lessons into Optuna DSPy-style optimizer prompt context.
- [ ] Log which articles were used per run (`articles_used: N` in run metadata) for traceability.
- [ ] Measure: Compare Optuna trials-to-best-fitness before and after knowledge injection. Hypothesis: ≥10% faster convergence (e.g., 45 trials vs 50 to reach same fitness score).
- [ ] The cycle: Night 1 autoresearch runs 50 Optuna trials → Morning flush captures "RIFE temporal_smoothing=0.8 beats 0.6 by 8%" → Night 2 synthesizer creates [[RIFE Interpolation Hyperparameters]] concept article → Night 3 autoresearch reads article, searches around 0.8 instead of uniform 0.5-1.0 → faster convergence → repeat.
- Machine: Mac Mini (orchestrator reads vault) + Alienware (autoresearch payload)
- Schedule: Continuous after both Phase 5 autoresearch and Phase 6 synthesis are live
- Cost: $0.00 (no new API calls — just reads vault)
- Success: `articles_used > 0` in autoresearch logs, convergence speed metric improves ≥10% in side-by-side comparison

**Phase 6 Cost & Effort Summary:**

| Category | Estimate |
|----------|----------|
| Dev hours | 45-55h (Gemma 4 setup 4h, benchmark harness 10h, SessionEnd hook 6h, Vault Indexer v2 3h, Synthesizer 12h, Knowledge Lint 14h, integration 5h) |
| Testing hours | 20-25h (benchmark runs 8h, synthetic vault testing 6h, integration 8h) |
| New agents | 3 (flush.py, vault_synthesizer.py, knowledge_lint.py) |
| New hooks | 1 (session-end-flush.sh) |
| API cost | $0.00 (all agents 100% local) |
| Electricity | ~$1-2/month (nightly WOL for MacBook Pro synthesis) |
| Monthly system cost | Unchanged: $7-10 total |

---

## Part 5: Open Questions (Updated March 27 — some resolved, new ones added)

1. ~~**Nano Banana 2 vs Pro for sprites**~~ — RESOLVED (Phase 2). NB2 wins: 26% faster, comparable quality. Use NB2 (`gemini-3.1-flash-image-preview`) for volume generation, NB Pro (`gemini-3-pro-image-preview`) reserved for anchor/hero frames.

2. ~~**Which video/animation model wins?**~~ — RESOLVED (Phase 3-5). **RIFE VFI** (rife49.pth) is the confirmed primary interpolation engine — 60/60 HYBRID animations, 815 interpolated frames, 0 failures, character identity preserved. **Production pipeline: NB2 keyframes → RIFE VFI 4x → Pixel Quantizer.** Wan 2.2 14B I2V available for single-keyframe animation (dual fp8 + LightX2V LoRA, ~80s/clip). Wan 2.2 5B DEPRECATED. GMFSS blocked by cupy. rd-animation dead. FILM VFI available as backup. PixelLab API ($0.007-$0.016/gen) viable alternative — adapter built, pending API verification.

3. ~~**Retro Diffusion rd-animation**~~ — RESOLVED. It's live on Replicate with 4.9K runs. Test immediately in Phase 1.

4. ~~**MLX vs Ollama on MacBook Pro**~~ — RESOLVED. MLX-LM benchmarks show 3x faster, lower RAM. Use MLX-LM on MacBook Pro, keep Ollama on Mac Mini.

5. **Dashboard tech stack** — STILL OPEN. Perplexity UI/UX research prompt is written but not yet run.

6. ~~**Agent Teams vs Subagents**~~ — RESOLVED. Agent Teams are now production-ready (no longer experimental). Use for complex multi-agent work; subagents for focused tasks.

7. ~~**LoRA quality for this specific art style**~~ — RESOLVED (April 8). **LoRA path abandoned.** Training Run 001 (61 images, rank 32, Illustrious XL v0.1→v2.0 inference) produced anime-proportioned characters with HUD artifacts — not SF2-quality pixel art. Multiple prior attempts also failed. Root cause: SDXL LoRA training cannot reliably learn the specific SF2 arcade sprite aesthetic from small datasets. **Decision: Gemini NB2 keyframes are the production path.** NB2→RIFE VFI→Pixel Quantizer scores 87.6% and produces the correct style natively.

8. ~~**Could PixelLab/Ludo.ai bypass the hybrid pipeline?**~~ — RESOLVED (Phase 4). rd-animation dead. **PixelLab v3 HAS a public API** with Python SDK ($0.007-$0.016/gen). "Animate with Skeleton" + "Estimate Skeleton" endpoints, max 128×128. Viable for pipeline integration — build PixelLabAdapter in Phase 5. Ludo.ai still untested. The hybrid pipeline remains primary (RIFE VFI 87.6%).

9. **NEW: Qwen3 model family evaluation** — Qwen3-14B, Qwen3-VL, Qwen3.5-122B MoE all claimed to outperform predecessors. Benchmark during Phase 1 Ollama/MLX setup.

10. **NEW: Opus 4.6 cost/benefit recalculation** — At $5/$25 per MTok with 1M context, some tasks currently planned for local 32B inference might be cheaper/better on Opus. Recalculate during Phase 1.

11. **NEW: Gas Town agent orchestrator** — Steve Yegge's tool (`brew install gastown`) provides structured multi-agent coordination for Claude Code. Evaluate if needed beyond native Agent Teams.

12. **NEW: Gemma 4 native function calling benefit for autoresearch** — Phase 6 Task A.5 will test if 6 dedicated function tokens reduce prompt engineering overhead in Optuna search. Hypothesis: ≥10% faster convergence. Benchmark required before committing.

13. **NEW: Where should daily logs live — inside vault or parallel?** Recommendation: inside `vault/daily/` for Obsidian MOC cross-linking. Requires filelock coordination with Vault Indexer. Decision point in Phase 6 Task D.1.

14. **NEW: Should flush agent run on Mac Mini (fast, phi4-mini) or MacBook Pro (quality, Qwen3-14B)?** Likely hybrid: phi4 for simple sessions, route complex sessions (>100 messages) to Qwen3-14B. Test both, measure extraction accuracy. Phase 6 Task D.1.

15. **NEW: Hermes Agent evaluation** — SKIPPED. Hermes Agent (NousResearch) solves problems already solved by our Agent SDK + hybrid_router + baton files. Its "learns about you" memory is just MEMORY.md + USER.md (2,200 + 1,375 chars) — less capable than our vault embeddings. Multi-platform gateway (Telegram/Discord/Slack) is dead weight for headless batch agents. **One idea worth stealing:** Honcho's "dialectic user modeling" as a pattern for vault synthesis — implement within existing infrastructure, not as a Hermes dependency.

16. **NEW: How to measure autoresearch convergence improvement from vault articles?** Phase 6 Task D.4 proposes comparing Optuna trial counts to best fitness. Alternative: compare final fitness scores directly. Test both metrics during Phase 5-6 overlap.

---

## Part 6: Key Numbers

| Metric | Target | Actual (Phase 5) |
|--------|--------|------------------|
| Total autonomous agents at steady state | 15-18 (Phase 6 adds 3: flush.py, vault_synthesizer.py, knowledge_lint.py → 14 total) | **2 active** (vault-indexer + daily-driver morning). 6 disabled — CLIConnectionError + MCP headless limitation. See April 9 audit. |
| Agents running 100% local | 10-12 (all 3 new Phase 6 agents are 100% local) | 1 (vault-indexer) |
| Monthly API cost | $3-8 (recalculate — Opus 4.6 now $5/$25, may be worth using more) | ~$12/mo (daily-driver morning ~$0.40/day) |
| Monthly electricity (all 3 machines) | ~$5-6 (nightly WOL for MacBook Pro synthesis adds ~$1-2) | ~$4 |
| Total monthly system cost | $7-12 | ~$16 |
| Total frames generated | ~900-1,400 | **1,835** (1,020 IMAGE_ONLY + 815 HYBRID) |
| Animations | — | **180** (15 per character × 12 characters) |
| Generation cost | — | **~$12.60** (180 Gemini calls × ~$0.07) |
| Full sprite production scope | 12 fighters × 15 animations × 4-17 frames | 12 fighters × 15 animations = 180 animations COMPLETE |
| Champion tile size | 128×128 | 128×128 |
| Boss tile size | 256×256 | 256×256 |
| Pipeline tech stack | Node.js / TypeScript / Oclif / Zod / Pino / Sharp / Puppeteer | + Python batch orchestrator |
| Agent SDK language | Python 3.10+ | Python 3.10+ |
| LoRA training time | 30-90 minutes per style (ABANDONED — Gemini NB2 is production path) | — |
| Vault knowledge articles (Phase 6 target) | ≥2 concepts + ≥1 connection per nightly synthesis run | — |
| Knowledge compounding loop | SessionEnd → flush → synthesize → lint → autoresearch feedback | — |

---

## Part 7: Session Loading Guide

When starting a new Claude Code or Cowork session, load THIS doc plus only the files relevant to your current task:

| Task | Load This Section | Load These Source Files |
|------|------------------|----------------------|
| Build hybrid_router.py | Part 2 Workstream A | `agent-sdk-upgrade-phase-2-synthesis-analysis.md` + `tech-stack-specs.md` |
| Build pixel quantizer | Part 2 Workstream B | `CLAUDE.md` + `hybrid-pipeline-plan.md` + `claude-code-kickoff-prompt.md` |
| Test video models | Part 2 Workstream B | `workflow-operations-guide.md` + `Perplexity-Final-Results-Analysis.md` |
| Train LoRA | Part 2 Workstream C | `ref-lora-training-rtx5080-sprite-pipeline.md` + `lora-guide-content.md` |
| Build autoresearch loop | Part 2 Workstream C | `Autoresearch-ComfyUI-Overview.md` |
| Set up launchd agents | Part 2 Workstream A | `agents-sdk.md` + `agent-sdk-upgrade-phase-2-synthesis-analysis.md` |
| Sprint planning / PM agents | Part 2 Workstream A | `agent-sdk-upgrade-phase-2-synthesis-analysis.md` (sections 1, 6, 9) |
| Dashboard UI design | Part 5 Q5 | `perplexity-ui-ux-research-prompt.md` |
| RTX 5080 troubleshooting | Part 2 Workstream C | `LoRA-training-perplexity-computer-follow-up.md` (compatibility report + known bugs) |
| Understand council disagreements | Part 2 Workstream B | Individual council responses (`Claude Opus 4.6 Thinking-response.md`, `GPT-5.2 Thinking-response.md`, `Gemini 3 Pro-response.md`) + CSVs |
| Review original pipeline architecture | Part 1 | `Original Workflow Summary.md` + `CLAUDE.md` + `CHANGELOG.md` |
| Agent Teams exploration | Part 2 Workstream A | `Claude-Code-Agent-Teams.md` |
| Detailed step-by-step execution | Part 4 | `16bitfit-execution-blueprint.md` (~102.5h total, exact commands per task) |
| Validate tool/model currency | Part 8 | `validation-audit-march-2026.md` |
| Find new tools/opportunities | Part 8 | `creative-tech-opportunity-scan.md` |
| Gemma 4 benchmarking | Phase 6 Workstream A | `agents-sdk/lib/gemma4_benchmark.py` + `config.toml` |
| Build SessionEnd flush hook | Phase 6 D.1 | `agents-sdk/agents/flush.py` + `.claude/hooks/session-end-flush.sh` |
| Build Vault Synthesizer | Phase 6 D.2 | `agents-sdk/agents/vault_synthesizer.py` + `agents-sdk/agents/vault_indexer.py` |
| Build Knowledge Lint agent | Phase 6 D.3 | `agents-sdk/agents/knowledge_lint.py` |
| Knowledge → autoresearch loop | Phase 6 D.4 | `vault/knowledge/concepts/` + autoresearch orchestrator |
| Autoresearch loop foundation | Part 2 Workstream C | `Autoresearch-ComfyUI-Overview.md` + `creative-tech-opportunity-scan.md` (ComfyGI, Optuna, ImageReward sections) |
| Test new sprite animation tools | Part 5 Q8 | `creative-tech-opportunity-scan.md` (PixelLab, rd-animation, Ludo.ai, Wan 2.2 LoRAs sections) |

---

## Part 8: Perplexity Computer Findings (March 27, 2026)

Three Perplexity Computer tasks were run against the full research corpus. Their outputs are companion docs to this SOT:

**`validation-audit-march-2026.md`** — Checked every tool, model, framework, and API against live March 2026 state. 9 categories, CURRENT/UPDATE NEEDED/REPLACED verdicts. Key findings: 8 critical changes (rd-animation released, Illustrious v2.0+v3.x exist, SDK breaking renames, Wan 2.5 not open source, Phi-4 naming mismatch, PyTorch stable supports sm_120, Opus 67% cheaper, Qwen3 family upgrades).

**`16bitfit-execution-blueprint.md`** — Detailed step-by-step execution manual: exact terminal commands, verification steps, decision gates, gotchas, time estimates (~102.5 hours total across 5 phases). Incorporates all validation audit updates. This is the "what to type" doc.

**`creative-tech-opportunity-scan.md`** — 60-day landscape scan. Top 5 highest-impact opportunities: (1) ComfyGI + Optuna + ImageReward as autoresearch foundation, (2) Wan 2.2 pixel animation LoRAs as local free animation path, (3) PixelLab Animate v3 as pipeline simplifier, (4) DISTS + DINOv2 + LLM-as-Judge quality metrics upgrade, (5) MLX-LM for 3x local inference speed. Also found: Ludo.ai combat presets, Sprite Smithy, GMFSS Fortuna, Flux.2 Klein consistency LoRA, A2A protocol, Gas Town orchestrator, GDC 2026 validation of agent-driven creative production.

**Important contradiction resolved:** The validation audit suggested evaluating Illustrious XL v2.0-STABLE as the new training base. The opportunity scan found community evidence that v0.1 is the correct LoRA training base — LoRAs trained on v2.0+ have reduced cross-compatibility. **Decision: Train on v0.1, infer on v2.0-STABLE or v3.x.**

---

*This document synthesizes 28 original source files + 3 Perplexity Computer outputs. Last updated: 2026-04-14. Phase 6 added (Gemma 4 + Knowledge Compounding Loop). Update this doc whenever a major decision changes or a gate check completes.*
