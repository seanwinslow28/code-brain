# Source of Truth — Sean's Agentic Frameworks & Creative Pipeline Master Plan

**Created:** 2026-03-27 (Boston, post-move)
**Last Updated:** 2026-04-02 — Phase 4 in progress. RIFE VFI confirmed as primary interpolation engine (GMFSS blocked by cupy). Walk cycle strategy locked: NB2 → RIFE VFI → Pixel Quantizer. Building memory/retrieval agents + LoRA training setup.
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

**Model-to-Machine Routing (UPDATED):**

| Task | Machine | Model | Change from Original |
|------|---------|-------|---------------------|
| Inbox triage | Mac Mini | `phi4-mini-reasoning` (3.8B) via Ollama | Was "Phi-4 7B" — that model doesn't exist |
| Vault embeddings | Mac Mini | nomic-embed-text via Ollama | No change |
| Anki cards | Mac Mini | `phi4-mini` (3.8B) via Ollama | Was "Phi-4 7B" |
| Financial analysis | MacBook Pro | **Qwen3-14B** via MLX-LM | Was DeepSeek-R1:14B — Qwen3 outperforms on MATH, LiveCodeBench |
| Code review / PR digest | MacBook Pro | **Qwen2.5-Coder-32B** via MLX-LM | Was 14B — 32B fits in 48GB via MLX, meaningfully better |
| Heavy synthesis | MacBook Pro | **Qwen3.5** (evaluate 122B MoE 10B-active or 9B) via MLX-LM | Was Qwen2.5-32B — Qwen3.5 MoE is faster + smarter |
| Sprite vision QA | Alienware | **Qwen3-VL-7B** via Ollama CUDA | Was Qwen2.5-VL — Qwen3-VL has better spatial encoding |
| ComfyUI orchestration | Alienware | N/A (REST API) | No change |

**Source files:** `Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md` (the big one — 350 lines of detailed specs), `agents-sdk.md` (SDK architecture + how interactive vs autonomous layers relate), `tech-stack-specs.md` (hardware inventory for all 3 machines), `Claude-Code-Agent-Teams.md` (Agent Teams — now production-ready with shared task lists, plan approval, display modes)

### Workstream B: Sprite Sheet Pipeline Upgrade (THE PRODUCT)

**Goal:** Evolve the working v0.1.0 pipeline into a hybrid keyframe-to-video system that solves the walk cycle problem, then scale to all 12 fighters × 13 animations.

**NON-NEGOTIABLE: Google's image generation models stay in the pipeline.** Nano Banana Pro (`gemini-3-pro-image-preview`) and/or Nano Banana 2 (`gemini-3.1-flash-image-preview`) are the proven best-in-class for single-frame sprite generation. Cost is not a concern here — quality and speed are. These models serve as both the primary image-only generator AND the keyframe generator feeding the hybrid pipeline.

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

**Video Model Candidates (UPDATED March 27 per validation audit):**
- **Pika Pikaframes 2.2** via fal.ai — CURRENT. Up to 5 keyframes, cleanest multi-keyframe API. $0.04/sec (720p).
- **Kling 3.0** — CURRENT. Elements character lock confirmed, start/end frame API viable, Multi-Shot "AI Director" feature added.
- **Kling 2.6** — CURRENT. Motion transfer from reference video confirmed working.
- **Google Veo 3.1** — UPDATE: Was "Veo 2/3" — now Veo 3.1. Native 4K, but resolution mismatch for pixel art still valid. Test last.
- ~~**Wan 2.5**~~ — CORRECTED: Wan 2.5 is NOT open source. **Wan 2.2** is the latest open-source version.
- **NEW: Retro Diffusion rd-animation** — NOW LIVE on Replicate (4.9K runs). Purpose-built pixel art sprite sheets. Could bypass Pixel Quantizer entirely. **Test immediately.**
- **NEW: LTX-2** — Open-source (Apache 2.0), 4K@50fps, NVIDIA-optimized. True open-source replacement for Wan.
- **NEW: Seedance 2.0** — ByteDance, launched Feb 7. Reference-to-video with expression/motion transfer.
- **NEW: PixelLab "Animate with Text" v3** (March 18) — Generates multi-frame animation from static sprite + text. Native pixel art output, skeleton controls, frame-extensible. Could bypass entire hybrid pipeline for 10+ animation types. **Test immediately.**
- **NEW: Ludo.ai Sprite Animator** — Combat animation presets (melee, defense, reactions), MCP API for programmatic generation, Y-offset alignment tool. **Test immediately.**
- **NEW: Wan 2.2 pixel animation LoRAs** — Community LoRAs for animating static sprites: attack cycles, walk cycles, comprehensive set (226 training clips). Runs locally on RTX 5080 = free. **Test in Phase 2.**
- **NEW: Pixverse v4.5** — First+last frame sprite sheet workflow documented by Scenario. Another adapter candidate.

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

**LoRA Training (ready to execute):**

| Decision | Choice | Why |
|----------|--------|-----|
| Framework | kohya_ss (dev branch, gui-uv.bat) | Best SDXL support, RTX 5080 compatible |
| Base model | Illustrious XL v0.1 (CONFIRMED — train on v0.1, infer on v2.0/v3.x) | Community consensus: LoRAs trained on v2.0+ have reduced cross-compatibility. v0.1 LoRAs work across ecosystem. |
| Optimizer | Adafactor | Required for fused backward pass (~10GB VRAM) |
| Attention | SDPA (PyTorch native) | xformers crashes on sm_120 |
| LoRA rank | 32 | Sweet spot for style LoRAs |
| Dataset | 30-50 PNGs of your art style, 1024px+ | Nearest-neighbor upscaling only |
| Training time | 30-90 minutes | 10 epochs, 10-15 repeats |

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
Workstream A (Agent SDK Infrastructure)
    ├── hybrid_router.py (three-machine routing)
    ├── Mac Mini as always-on orchestrator
    ├── WOL for Alienware
    ├── Safety hooks (loop-detector, cost-watchdog, vault-integrity)
    └── launchd schedules on Mac Mini
         │
         ▼
Workstream B (Sprite Pipeline Upgrade)  ←── CAN START IN PARALLEL (Pixel Quantizer doesn't need Agent SDK)
    ├── Phase 0: Pixel Quantizer prototype (GATE CHECK — do this first)
    ├── Phase 1: Video model evaluation sprint (test Pika, Kling, Veo)
    ├── Phase 2: Hybrid pipeline end-to-end (1 walk cycle)
    ├── Phase 3: Adapter layer + strategy router
    └── Scale to full roster
         │
         ▼
Workstream C (Autoresearch + LoRA)  ←── DEPENDS ON BOTH A AND B
    ├── LoRA training (needs Alienware set up, ComfyUI configured)
    ├── Autoresearch loop (needs Agent SDK infra + ComfyUI pipeline)
    └── Overnight optimization runs
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
- [x] Wan 2.2 5B ti2v = **primary video model**. GATE CHECK PASS: 73.7% overall, 84.0% palette. Character preserved, green screen intact, pixel art maintained. Free/local on RTX 5080.
- [x] Wan22Adapter, RIFEAdapter (was GMFSSAdapter), ReplicateAdapter — all behind `VideoModelAdapter` hexagonal interface.
- [x] End-to-end test: NB2 keyframes → Wan 2.2 5B → extract 8 frames → Pixel Quantizer → 73.7% overall. GATE CHECK PASS. Only 4% degradation from raw keyframes (77.7%).
- [x] Strategy decision map: 10 animations → IMAGE_ONLY, 5 → HYBRID. Duration mapping (1s combat, 2s locomotion). Frame counts (4-12 per type).
- [x] rd-animation via Replicate: TESTED, NOT VIABLE (48x48, wrong character, wrong style). Removed from strategy map.
- [x] ~~GMFSS Fortuna~~ → **RIFE VFI confirmed as primary interpolation engine.** GMFSS blocked by cupy dependency. RIFE VFI (rife49.pth) tested: character identity PASS, pose transitions PASS, green screen PASS. Color expansion (79K-103K unique colors) handled by Pixel Quantizer. FILM VFI available as backup (slightly more ghosting). Bonus VFI models available (AMT, CAIN, FLAVR) — untested, same node pack.
- [ ] Wan 2.2 14B I2V: BLOCKED by ComfyUI channel mismatch (WanImageToVideo = Wan 2.1 only). Monitor for ComfyUI update.

**Key finding:** Wan 2.2 5B produces pose animation (idle bounce) from single keyframe, not full locomotion. Walk cycles need multi-keyframe input + RIFE VFI interpolation as primary approach.

### Phase 4: LoRA + Memory Layer (Weeks 7-8 — May 8 - May 22)

**Workstream A — Retrieval & Memory:**
- [ ] Vault Embedding Indexer → Mac Mini nightly (nomic-embed-text → SQLite)
- [ ] Preserve Session → MacBook Pro (Qwen3-14B via MLX-LM)
- [ ] PR Digest → MacBook Pro (Qwen2.5-Coder-32B via MLX-LM)

**Workstream C — LoRA Training:**
- [ ] Set up kohya_ss dev branch on Alienware (gui-uv.bat)
- [ ] Prepare dataset: 30-50 PNGs of your art style, 1024px+, captioned
- [ ] Train first style LoRA on Illustrious XL (Adafactor, SDPA, rank 32)
- [ ] Test LoRA in ComfyUI pipeline for sprite generation quality
- [ ] Integrate LoRA into pipeline's ComfyUI adapter

### Phase 5: Autoresearch + Scale (Weeks 9-12 — May 22 - Jun 19)

**Workstream B — Scale:**
- [ ] Expand to full strategy decision map (all 13 animations × image-only/hybrid/motion-transfer)
- [ ] Begin batch generation: 2nd and 3rd Champions through pipeline
- [ ] Build sprite pipeline dashboard (reference: Perplexity UI/UX research prompt already written)

**Workstream C — Autoresearch Loop (built on proven components):**
- [ ] Fork ComfyGI mutation operators (checkpoint, ksampler, prompt_word, prompt_llm)
- [ ] Implement Optuna TPE sampler for parameter search (numerical/categorical). Reserve LLM agent for prompt optimization (DSPy-style, Tier 2).
- [ ] Install ImageReward ComfyUI node as primary fitness function
- [ ] Use official NB2 Animated Sprite Sheet template as starting workflow JSON
- [ ] Implement upgraded quality metrics: DISTS + DINOv2 + EDOKS + Qwen3-VL LLM-as-Judge
- [ ] Configure overnight runs: Mac Mini orchestrates, Alienware runs ComfyUI + scoring
- [ ] Evaluate ComfyUI CacheProvider API for parallel experiments (multiple worker instances sharing model cache)
- [ ] First optimization target: find optimal sampler/CFG/steps for your LoRA + Illustrious XL combo

**Workstream A — Meta:**
- [ ] Meta-Agent / Chief of Staff → Mac Mini orchestrates, MacBook runs summaries, Opus synthesizes
- [ ] Full fleet token audit
- [ ] Implement prompt caching scheduling (cluster API agents in 5-min windows)

---

## Part 5: Open Questions (Updated March 27 — some resolved, new ones added)

1. ~~**Nano Banana 2 vs Pro for sprites**~~ — RESOLVED (Phase 2). NB2 wins: 26% faster, comparable quality. Use NB2 (`gemini-3.1-flash-image-preview`) for volume generation, NB Pro (`gemini-3-pro-image-preview`) reserved for anchor/hero frames.

2. ~~**Which video/animation model wins?**~~ — RESOLVED (Phase 3-4). **Wan 2.2 5B ti2v** is the primary video model (73.7% gate check, free/local). **RIFE VFI** (rife49.pth) is the confirmed primary interpolation engine — character identity PASS, pose transitions PASS, green screen PASS. GMFSS Fortuna blocked by cupy. rd-animation dead (48x48, wrong style). Walk cycles: NB2 multi-keyframe → RIFE VFI 4x interpolation → Pixel Quantizer. FILM VFI available as backup. Wan 2.2 14B I2V blocked by ComfyUI compatibility — monitor for updates.

3. ~~**Retro Diffusion rd-animation**~~ — RESOLVED. It's live on Replicate with 4.9K runs. Test immediately in Phase 1.

4. ~~**MLX vs Ollama on MacBook Pro**~~ — RESOLVED. MLX-LM benchmarks show 3x faster, lower RAM. Use MLX-LM on MacBook Pro, keep Ollama on Mac Mini.

5. **Dashboard tech stack** — STILL OPEN. Perplexity UI/UX research prompt is written but not yet run.

6. ~~**Agent Teams vs Subagents**~~ — RESOLVED. Agent Teams are now production-ready (no longer experimental). Use for complex multi-agent work; subagents for focused tasks.

7. **LoRA quality for this specific art style** — STILL OPEN. But now confirmed: train on Illustrious XL v0.1, infer on v2.0-STABLE or v3.x for best results. Also evaluate Flux.2 Klein + community pixel art LoRA as fallback path.

8. **Could PixelLab/Ludo.ai bypass the hybrid pipeline?** — PARTIALLY RESOLVED. rd-animation is dead (48x48, wrong style, wrong character). PixelLab v3 and Ludo.ai still untested — evaluate in Phase 4 as potential shortcuts for simple animation types. The hybrid pipeline is proven viable regardless (73.7% gate check).

9. **NEW: Qwen3 model family evaluation** — Qwen3-14B, Qwen3-VL, Qwen3.5-122B MoE all claimed to outperform predecessors. Benchmark during Phase 1 Ollama/MLX setup.

10. **NEW: Opus 4.6 cost/benefit recalculation** — At $5/$25 per MTok with 1M context, some tasks currently planned for local 32B inference might be cheaper/better on Opus. Recalculate during Phase 1.

11. **NEW: Gas Town agent orchestrator** — Steve Yegge's tool (`brew install gastown`) provides structured multi-agent coordination for Claude Code. Evaluate if needed beyond native Agent Teams.

---

## Part 6: Key Numbers

| Metric | Target |
|--------|--------|
| Total autonomous agents at steady state | 15-18 |
| Agents running 100% local | 10-12 |
| Monthly API cost | $3-8 (recalculate — Opus 4.6 now $5/$25, may be worth using more) |
| Monthly electricity (all 3 machines) | ~$4 |
| Total monthly system cost | $6-10 |
| Full sprite production scope | 12 fighters × 13 animations × 4-12 frames = ~900-1,400 frames |
| Champion tile size | 128×128 |
| Boss tile size | 256×256 |
| Pipeline tech stack | Node.js / TypeScript / Oclif / Zod / Pino / Sharp / Puppeteer |
| Agent SDK language | Python 3.10+ |
| LoRA training time | 30-90 minutes per style |

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

*This document synthesizes 28 original source files + 3 Perplexity Computer outputs. Last updated: 2026-03-27. Update this doc whenever a major decision changes or a gate check completes.*
