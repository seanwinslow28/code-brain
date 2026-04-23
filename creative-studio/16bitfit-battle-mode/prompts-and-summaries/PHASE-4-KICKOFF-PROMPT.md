# Phase 4 Kickoff Prompt for Claude Code

## How to Use This

**Before pasting this prompt into Claude Code**, make sure:
1. Phase 3 is complete (10/10 tasks passed, hybrid pipeline viable at 73.7%)
2. GMFSS Fortuna node pack installed on Alienware (GMFSS itself blocked by cupy — RIFE VFI is the working fallback)
3. Sprint Health Monitor + Meeting Defender launchd plists installed on Mac Mini (7 agents total)
4. All three machines are online
5. You're starting from the `claude-code-superuser-pack` root directory

---

## YOUR MANUAL CHECKLIST (Do These First)

- [ ] Confirm machines are online:
  - `curl http://192.168.68.200:11434/api/tags` → Mac Mini
  - `curl http://192.168.68.201:11434/api/tags` → Alienware
- [ ] Confirm ComfyUI is running on the Alienware with `--listen 0.0.0.0 --port 8188 --force-fp16`
- [ ] Confirm launchd fleet on Mac Mini: `launchctl list | grep com.sean` → should show 7 agents
- [ ] Download the Wan 2.2 pixel animate LoRA on Alienware (if not already done):
  ```
  pip install huggingface-hub
  huggingface-cli download styly-agents/Wan2-2-pixel-animate --local-dir C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\wan22-pixel-animate
  ```

---

## THE CLAUDE CODE PROMPT

Paste everything below the line into Claude Code, starting a session from the `claude-code-superuser-pack` root directory.

---

```
You are continuing the 16BitFit Battle Mode build — Phase 4 of a 12-week project. Phases 1-3 are complete: three-machine fleet is online with 7 launchd agents, 5 autonomous agents built, hybrid pipeline PROVEN VIABLE (Wan 2.2 5B scored 73.7% through Pixel Quantizer, only 4% degradation from raw NB2 keyframes). RIFE VFI confirmed as primary interpolation engine (character identity PASS, pose transitions PASS, green screen PASS). Walk cycle strategy is locked: NB2 multi-keyframe → RIFE interpolation → Pixel Quantizer.

Phase 4 has three parallel workstreams: (A) memory/retrieval agents, (B) pipeline hardening + animation quality improvements, and (C) LoRA training on the Alienware.

<role>
You are a senior systems engineer and creative pipeline architect. Phase 4 connects three workstreams: building memory/retrieval agents that make the fleet smarter (Workstream A), hardening the sprite pipeline with real quantized output and new video model configurations (Workstream B), and training a custom style LoRA to accelerate sprite generation (Workstream C). You write clean, typed, tested code. You follow hexagonal/ports-and-adapters architecture. You route tasks to the correct machine per the topology.
</role>

<context>
Read these files in this exact order before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference (Phase 4 checklist in Part 4)
3. `16bitfit-battle-mode/phase-3-completion-summary.md` — Phase 3 results: video model ranking, adapter layer, strategy router, pipeline scores
4. `16bitfit-battle-mode/docs/agent-sdk/phase-2-synthesis.md` — Agent architecture spec (Sections 7-9: Vault Embedding Indexer, Preserve Session, PR Digest specs)
5. `16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-lora-training.md` — Complete LoRA training guide for RTX 5080 (kohya_ss setup, Illustrious XL, Adafactor, SDPA)
6. `16bitfit-battle-mode/docs/lora-autoresearch/rtx5080-compatibility.md` — RTX 5080 known issues, PyTorch requirements, confirmed working configs
7. `16bitfit-battle-mode/docs/sprite-pipeline/workflow-operations-guide.md` — ComfyUI workflow patterns, prompt templates

After reading, confirm you understand:
- The RIFE VFI interpolation results (character identity PASS, some color expansion that Pixel Quantizer handles)
- The three new agents to build (Vault Embedding Indexer, Preserve Session, PR Digest)
- The LoRA training configuration (kohya_ss dev branch, Illustrious XL v0.1, Adafactor, SDPA, rank 32)
- That GMFSS Fortuna is blocked by cupy — RIFE VFI (rife49.pth) is the confirmed interpolation engine
- The walk cycle strategy: NB2 keyframes → RIFE VFI 4x interpolation → Pixel Quantizer
</context>

<machine_ips>
Mac Mini LAN IP: 192.168.68.200
Alienware LAN IP: 192.168.68.201
MacBook Pro: localhost (this machine)
</machine_ips>

<phase3_artifacts>
These were built in Phase 3 and are available for use:
- `agents-sdk/agents/sprint_health.py` — Sprint Health Monitor (Jira MCP, Friday 15:00)
- `agents-sdk/agents/meeting_defender.py` — Meeting Defender (calendar audit, draft-only, Monday 07:00)
- `agents-sdk/agents/process_inbox.py` — Process Inbox (Mac Mini, 100% local)
- `agents-sdk/agents/spending_analysis.py` — Spending Analysis (MacBook Pro, 100% local)
- `agents-sdk/lib/baton.py` — inter-agent dependency utility
- `agents-sdk/lib/keychain.py` — macOS Keychain credential helper
- `agents-sdk/lib/hybrid_router.py` — three-tier routing with WOL
- `agents-sdk/config.toml` — routing + agent configs for all 7 agents
- `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — Wan22Adapter, GMFSSAdapter (needs RIFE swap), ReplicateAdapter, GeminiAdapter
- `16bitfit-battle-mode/pixel-quantizer/video-eval/strategy_router.py` — strategy router (15 animation types: 10 IMAGE_ONLY, 5 HYBRID)
- `16bitfit-battle-mode/pixel-quantizer/video-eval/evaluator.py` — evaluation framework with scoring
- `16bitfit-battle-mode/pixel-quantizer/video-eval/workflows/wan22_i2v_pixel_animate.json` — ComfyUI Wan 2.2 I2V workflow
- `16bitfit-battle-mode/pixel-quantizer/video-eval/workflows/gmfss_fortuna_interpolation.json` — ComfyUI interpolation workflow (currently references GMFSS Fortuna — update to RIFE)
- `eval-results/keyframe-*.png` — NB2-generated keyframes (walk cycle poses, green background, 1024x1024)
- `eval-results/gmfss-test-output/rife/frame_001.png` through `frame_005.png` — RIFE interpolated frames
- `eval-results/gmfss-test-output/film/frame_001.png` through `frame_005.png` — FILM interpolated frames (backup)
- Video model ranking: Wan 2.2 5B (73.7%) > RIFE VFI (untested through full quantizer) > Wan 2.2 14B (blocked) > rd-animation (dead)
</phase3_artifacts>

<constraints>
CRITICAL — all previous constraints still apply, plus:
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Never use `dangerouslySkipPermissions`
- Credentials come from macOS Keychain via `lib/keychain.py`
- RTX 5080: SDPA only (NO xformers — crashes on sm_120). Use `--force-fp16` with ComfyUI.
- Wan 2.2 is the latest OPEN SOURCE version. Do NOT use Wan 2.5 — it is NOT open source.
- Mac Mini runs `phi4-mini-reasoning` (3.8B), NOT "phi4" (14B)
- Alienware vision model is `qwen3-vl:8b` (NOT `qwen3-vl:7b`)
- All video model adapters go behind the `VideoModelAdapter` hexagonal interface
- LoRA: Train on Illustrious XL v0.1. Infer on v2.0-STABLE or v3.x. v0.1 has best cross-compatibility.
- LoRA training: Adafactor optimizer, SDPA attention, rank 32. NO xformers.
- kohya_ss: dev branch ONLY (stable branch doesn't support RTX 5080)
- RIFE VFI is the confirmed interpolation engine (NOT GMFSS Fortuna — blocked by cupy dependency)
</constraints>

<tasks>
Build the following. Workstreams A, B, and C are independent — you may interleave them. Start with Task 0 (housekeeping), then proceed to the three workstreams.

=== TASK 0: HOUSEKEEPING (Phase 3 Carry-Forward) ===

TASK 0a: Swap GMFSSAdapter to use RIFE VFI
- In `video-eval/adapters.py`, update the GMFSSAdapter (or create a new RIFEAdapter):
  - Change the ComfyUI workflow to use "RIFE VFI" node instead of "GMFSS Fortuna VFI"
  - Set checkpoint to `rife49.pth`
  - Keep the same interface (VideoModelAdapter ABC)
  - Update the `_meta` in the workflow JSON
- Update `video-eval/workflows/gmfss_fortuna_interpolation.json` → rename to `rife_interpolation.json`
  - Replace "GMFSS Fortuna VFI" class_type with "RIFE VFI"
  - Replace checkpoint name with `rife49.pth`
- Update `strategy_router.py` if it references GMFSS by name
- VERIFY: Confirm adapter loads cleanly. If the Alienware is reachable (192.168.68.201:8188), submit a test workflow.

TASK 0b: Update SOURCE-OF-TRUTH.md
- Mark Phase 3 Task 5 (GMFSS Fortuna) as resolved: "GMFSS blocked by cupy. RIFE VFI confirmed as primary interpolation engine. Character identity PASS, pose transitions PASS, green screen PASS."
- Update Open Question #2 to note RIFE VFI as confirmed interpolation model
- Update the Video Model Ranking in the Phase 3 section
- Add note: "FILM VFI available as backup (same node pack, slightly more ghosting)"
- Add note: "Bonus VFI models available (AMT, CAIN, FLAVR, etc.) — untested, same node pack"

=== WORKSTREAM A: MEMORY & RETRIEVAL AGENTS ===

TASK 1: Build Vault Embedding Indexer Agent
- Location: `agents-sdk/agents/vault_indexer.py`
- Routes to: Mac Mini ONLY (100% local — nomic-embed-text via Ollama)
- Purpose: Index all vault markdown notes into a SQLite vector store for semantic search
- Reads: all `.md` files in the `vault/` directory tree
- Splits documents into chunks (~500 tokens each, with overlap)
- Generates embeddings via Ollama nomic-embed-text on Mac Mini (http://192.168.68.200:11434)
- Stores: vault path, chunk text, embedding vector, last-modified timestamp in SQLite
- Incremental: only re-indexes files that changed since last run (compare mtime)
- Safety: max 20 turns, $0.00 budget cap (100% local, no API cost)
- Schedule: nightly (2:00 AM via launchd)
- Output: SQLite DB at `vault/.vault-index.db` + log summary to vault
- VERIFY: Run with `--dry-run` flag. Confirm it discovers vault files and would generate embeddings.

TASK 2: Build Preserve Session Agent
- Location: `agents-sdk/agents/preserve_session.py`
- Routes to: MacBook Pro (Qwen3-14B via MLX-LM at localhost)
- Purpose: After a Claude Code session ends, summarize what was built, decisions made, and open threads — save to vault as a session note
- Input: reads the most recent Claude Code session transcript (if available via `~/.claude/` logs) OR accepts a manual summary via baton file
- Generates: structured session summary with sections: What Was Built, Key Decisions, Open Questions, Next Steps
- Output: vault note at `vault/03_Resources/Session-Logs/session-{date}-{topic}.md`
- Safety: max 10 turns, $0.00 budget cap (100% local)
- Schedule: on-demand (no fixed schedule — triggered manually or by baton file)
- VERIFY: Run with `--dry-run` flag. Confirm it can read input and would generate a vault note.

TASK 3: Build PR Digest Agent
- Location: `agents-sdk/agents/pr_digest.py`
- Routes to: MacBook Pro (Qwen2.5-Coder-32B via MLX-LM at localhost)
- Purpose: Summarize recent GitHub PRs across key repos into a daily digest
- Uses: GitHub MCP (if available) or `gh` CLI to list recent PRs
- Repos to watch: configurable list in config.toml (start with `16BitFit-V3`, `sprite-sheet-automation-2026`, `claude-code-superuser-pack`)
- Generates: markdown digest with PR title, author, status, 1-line summary, link
- Output: vault note at `vault/02_Areas/Work/pr-digest-{date}.md`
- Safety: max 15 turns, $0.00 budget cap (100% local, gh CLI doesn't cost anything)
- Schedule: daily (8:00 AM via launchd)
- Check if GitHub MCP is available. If not, fall back to `gh` CLI commands.
- VERIFY: Run with `--dry-run` flag. Confirm it can access GitHub and would list PRs.

=== WORKSTREAM B: PIPELINE HARDENING + ANIMATION QUALITY ===

TASK 4: Run RIFE Output Through Full Pixel Quantizer
- Take the 5 RIFE-interpolated frames from `eval-results/gmfss-test-output/rife/`
- Run them through the COMPLETE Pixel Quantizer pipeline (all 7 steps):
  1. Nearest-neighbor downscale → 128×128
  2. Palette quantization (force-snap to LUT)
  3. Temporal smoothing (mode-color locking)
  4. Outline enforcement (#272929, 2-3px)
  5. Alpha recovery (background removal)
  6. Grid alignment
  7. Format validation
- Score the quantized output using the evaluation framework
- Compare: raw NB2 keyframes (77.7%) vs Wan 2.2 output (73.7%) vs RIFE interpolated (this test)
- Save quantized frames to `eval-results/rife-quantized/`
- VERIFY: Report scores. Does the Pixel Quantizer clean up the RIFE color expansion (79K-103K unique colors → palette-compliant)? Are the interpolated mid-frames clean pixel art after quantization?

TASK 5: Test Wan 2.2 with Pixel Animate LoRA
- Check if the `styly-agents/Wan2-2-pixel-animate` LoRA is downloaded on the Alienware
  - Expected location: ComfyUI loras directory on the Alienware
  - If not present, document the download command for Sean to run on the Alienware
- Update the Wan 2.2 ComfyUI workflow (`workflows/wan22_i2v_pixel_animate.json`) to load the LoRA
  - LoRA strength: start at 0.85, document how to adjust
- Submit to ComfyUI on the Alienware (192.168.68.201:8188):
  - Input: NB2 keyframe (one of the existing walk cycle keyframes)
  - Prompt: "pixel art fighting game character walking forward, side view, green screen background, retro arcade style"
  - Generate 2-second clip
- Extract frames, run through Pixel Quantizer, score
- Compare against Phase 3 Wan 2.2 results (73.7% without LoRA) — does the LoRA improve quality?
- VERIFY: Report score. Does the LoRA improve animation style, motion range, or palette compliance?

TASK 6: Test Stronger Motion Prompts with Wan 2.2 5B
- The Phase 3 finding was that Wan 2.2 5B produces "idle bounce" from a single keyframe, not walk cycle locomotion
- Test with more explicit motion prompts to push for actual locomotion:
  - Prompt A: "pixel art character walking forward step by step, legs moving in walk cycle, side view scrolling, green screen, 2D arcade fighter"
  - Prompt B: "walking animation cycle, left foot forward then right foot forward, repeating stride, pixel art sprite, green background"
  - Prompt C: "character locomotion from left to right, full body walk cycle animation, pixel art style, chroma key green"
- Use the same NB2 keyframe as input for all three prompts
- For each: extract frames → Pixel Quantizer → score
- Also test with 2-keyframe input (start pose + end pose) to see if two reference points help the model understand intended motion
- VERIFY: Do any prompts produce actual locomotion rather than idle bounce? Report best prompt + score.

TASK 7: Evaluate PixelLab v3 "Animate with Text"
- Research: Check if PixelLab v3 has a public API (web search or check their docs)
- If API exists: build a `PixelLabAdapter` behind the VideoModelAdapter interface
- If no API: document how to use it manually and what the output format is
- Key question: Can PixelLab generate multi-frame animations from a static NB2 sprite + text prompt?
- If testable: run a walk cycle test and score through Pixel Quantizer
- Compare against the hybrid pipeline (NB2 → RIFE → Quantizer) — is PixelLab a viable shortcut for some animation types?
- VERIFY: Report findings. If PixelLab works, which animation types could it handle (potentially replacing the hybrid pipeline for those types)?

=== WORKSTREAM C: LoRA TRAINING ===

TASK 8: Set Up kohya_ss on Alienware
- kohya_ss must use the DEV BRANCH (stable doesn't support RTX 5080)
- Check if kohya_ss is already installed on the Alienware. If not, document the setup commands:
  ```
  git clone -b dev https://github.com/bmaltais/kohya_ss.git
  cd kohya_ss
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```
- Verify PyTorch version is ≥2.7.0 cu128+ (already installed: PyTorch 2.11.0+cu130)
- Confirm SDPA attention works (NOT xformers)
- Create a training config TOML for the sprite style LoRA:
  - Base model: Illustrious XL v0.1 (must be downloaded to Alienware)
  - Optimizer: Adafactor (required for fused backward pass, ~10GB VRAM)
  - Attention: SDPA
  - LoRA rank: 32
  - Network alpha: 16
  - Learning rate: 1e-4
  - Epochs: 10
  - Resolution: 1024
  - Batch size: 1 (VRAM constrained)
  - Mixed precision: fp16
  - Gradient checkpointing: enabled
  - Cache latents: enabled
- Save config to: `16bitfit-battle-mode/lora-training/sprite-style-config.toml`
- VERIFY: Config is valid TOML. Document any models that need downloading on the Alienware (Illustrious XL v0.1, etc.).

TASK 9: Prepare LoRA Training Dataset
- Create directory structure: `16bitfit-battle-mode/lora-training/dataset/`
- Document the dataset requirements:
  - 30-50 PNG images of the target art style (SF2-style pixel art fighters)
  - Resolution: 1024×1024 (nearest-neighbor upscale from smaller originals — NEVER bicubic/bilinear)
  - Each image needs a matching `.txt` caption file with the same name
- Create a caption template and 3-5 example captions for sprite art:
  - Example: "pixel art fighting game character, idle stance, bold outlines, flat cel shading, transparent background, SF2 style, 128x128 sprite"
- Build a simple Python script (`lora-training/prepare_dataset.py`) that:
  - Takes a directory of source PNGs
  - Nearest-neighbor upscales to 1024×1024
  - Generates caption .txt files from a template (with per-image customization hooks)
  - Validates all images are correct format/size
- VERIFY: Script runs without errors on a test image. Output images are 1024×1024 with nearest-neighbor scaling (sharp pixels, no blur).

TASK 10: Document LoRA Training Launch Procedure
- Since we can't run kohya_ss from the MacBook Pro remotely, create a step-by-step runbook:
  - `16bitfit-battle-mode/lora-training/TRAINING-RUNBOOK.md`
  - Exact commands to: activate venv, verify GPU, launch training, monitor progress
  - Expected VRAM usage (~10GB with Adafactor + gradient checkpointing)
  - Expected training time (30-90 minutes for 10 epochs)
  - How to test the trained LoRA in ComfyUI (load LoRA node → connect to checkpoint → generate test image)
  - Troubleshooting: common errors on RTX 5080 (cutlassF crash = needs SDPA, OOM = reduce batch size)
- VERIFY: Runbook is complete and references the correct paths on the Alienware.

=== TASK 11: Phase 4 Completion Summary ===

Summarize all task results (PASS/FAIL/BLOCKED):

1. RIFE adapter swap + SOT update
2. Vault Embedding Indexer (dry-run results)
3. Preserve Session agent (dry-run results)
4. PR Digest agent (dry-run results)
5. RIFE frames through full Pixel Quantizer (scores + comparison table)
6. Wan 2.2 + LoRA quality delta (score with vs without LoRA)
7. Motion prompt experiments (best prompt + score)
8. PixelLab v3 evaluation (viable/not viable + reasoning)
9. kohya_ss setup status
10. Dataset preparation script
11. Training runbook

Provide:
- Updated video model strategy recommendation
- Animation quality comparison table: IMAGE_ONLY (NB2) vs HYBRID (NB2+RIFE) vs HYBRID (NB2+Wan2.2) vs HYBRID (NB2+Wan2.2+LoRA)
- Agent fleet status (should be 8 agents after this phase: 5 from before + Vault Indexer + Preserve Session + PR Digest)
- What I need to do manually before Phase 5 (LoRA training on Alienware, dataset collection, etc.)
- Open questions for SOURCE-OF-TRUTH.md

</tasks>

<output_format>
For each task:
1. Read the relevant reference docs first
2. Write the code
3. Run the verification step
4. Report: PASS or FAIL with details
5. If FAIL, fix and re-verify before moving on

After all tasks complete, provide the Phase 4 Completion Summary (Task 11).
</output_format>

<validation>
Before finishing, self-check:
1. Did you use `claude-agent-sdk` and `ClaudeAgentOptions` everywhere?
2. Are all credentials accessed via keychain.py (no .env files)?
3. Is the Vault Embedding Indexer 100% local (Mac Mini + nomic-embed-text)?
4. Is Preserve Session 100% local (MacBook Pro + Qwen3-14B)?
5. Is PR Digest 100% local (MacBook Pro + Qwen2.5-Coder-32B)?
6. Did you swap GMFSS Fortuna → RIFE VFI in the adapter and workflow?
7. Did you use Wan 2.2 (NOT Wan 2.5) for all video model tests?
8. Did you use SDPA attention (NOT xformers) in all Alienware configs?
9. Is the LoRA training config using Illustrious XL v0.1 (NOT v2.0+)?
10. Is the LoRA training config using Adafactor optimizer + rank 32?
11. Did you run real RIFE output through the full Pixel Quantizer (not just scoring)?
12. Are all new adapters behind the VideoModelAdapter hexagonal interface?
13. Did all new agents get entries in config.toml?
14. Did you create launchd plists for Vault Indexer (nightly 2AM) and PR Digest (daily 8AM)?
</validation>
```

---

## What Happens After

Once Claude Code completes these 11 tasks, you'll have:

**Built by Claude Code:**
- RIFE VFI adapter + updated workflow (replacing GMFSS Fortuna references)
- `agents-sdk/agents/vault_indexer.py` — Vault Embedding Indexer (Mac Mini, 100% local, nightly)
- `agents-sdk/agents/preserve_session.py` — Preserve Session (MacBook Pro, 100% local, on-demand)
- `agents-sdk/agents/pr_digest.py` — PR Digest (MacBook Pro, 100% local, daily 8AM)
- RIFE frames fully quantized through Pixel Quantizer (quality comparison data)
- Wan 2.2 + LoRA quality delta (does the pixel animate LoRA help?)
- Motion prompt experiment results (best prompt for locomotion)
- PixelLab v3 viability assessment
- `lora-training/sprite-style-config.toml` — kohya_ss training config
- `lora-training/prepare_dataset.py` — dataset preparation script
- `lora-training/TRAINING-RUNBOOK.md` — step-by-step training guide for Alienware

**Your manual steps after Claude Code finishes:**
1. Collect 30-50 sprite art PNGs for LoRA training dataset
2. Run `prepare_dataset.py` to upscale and caption them
3. Copy dataset to Alienware
4. Follow TRAINING-RUNBOOK.md to train the LoRA on the Alienware
5. Test the trained LoRA in ComfyUI
6. Install Vault Indexer + PR Digest launchd plists on Mac Mini
7. If PixelLab v3 is viable → add it to the strategy router for applicable animation types
8. Proceed to Phase 5 (Autoresearch + Scale to full roster)
