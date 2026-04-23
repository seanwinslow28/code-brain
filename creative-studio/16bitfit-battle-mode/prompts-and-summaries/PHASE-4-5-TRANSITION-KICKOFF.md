# 16BitFit Battle Mode — Phase 4→5 Transition Kickoff Prompt

**Purpose:** Paste this entire file into a new Cowork conversation to continue the 16BitFit Battle Mode project from where we left off.

---

<role>
You are my technical project partner for 16BitFit Battle Mode — a 12-week build spanning three workstreams: (A) autonomous agent infrastructure across a three-machine network, (B) a hybrid AI sprite sheet pipeline for a 2D fighting game, and (C) an autoresearch/LoRA training system. I'm a beginner with code, so please explain your reasoning for technical choices, but keep things brief and to the point.
</role>

<context>
Before responding, read these files in this exact order:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints, three-machine topology, model routing
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference with all phase checklists, architecture decisions, and open questions
3. `16bitfit-battle-mode/phase-4-completion-summary.md` — Phase 4 results (11/11 PASS, RIFE VFI confirmed, 8 agents, LoRA infra ready)
4. `16bitfit-battle-mode/lora-output/TRAINING-RUN-001.md` — LoRA training execution results (61 images, 3050 steps, loss 0.080, 2h 12m)

These four files contain everything you need. Do NOT load all docs at once — use the Session Loading Guide in SOURCE-OF-TRUTH.md Part 7 to pull specific reference files only when needed for implementation tasks.
</context>

<project_status>
We have completed Phases 1-4 and the LoRA training. Here's the current state:

## Phases 1-3 (COMPLETE):
Three-machine fleet online, 7 launchd agents, hybrid sprite pipeline PROVEN VIABLE (Wan 2.2 5B scored 73.7% through Pixel Quantizer), hexagonal adapter layer with 4 atomic operations, strategy router mapping 15 animation types.

## Phase 4 (COMPLETE — 11/11 PASS):
- RIFE VFI confirmed as primary interpolation engine. RIFE through Pixel Quantizer scored 87.6% overall — best quality in project.
- Walk cycle strategy LOCKED: NB2 multi-keyframe → RIFE VFI 4x interpolation → Pixel Quantizer
- 8 autonomous agents built (Daily Driver, Process Inbox, Spending Analysis, Sprint Health, Meeting Defender, Vault Embedding Indexer, Preserve Session, PR Digest)
- PixelLab v3 has a public API ($0.007-$0.016/gen, 128×128 max) — viable for pipeline integration
- Wan 2.2 14B I2V confirmed working (replaced deprecated 5B model). Dual fp8 + LightX2V 4-step LoRA.

## LoRA Training (COMPLETE — Training Run 001):
- Dataset: 61 Gemini NB2-generated images (36 original poses + 15 supplement poses + ~10 extra reference sprites). All green screen backgrounds, all 1024×1024 nearest-neighbor upscaled, all with caption .txt files using `16bitfit_style` trigger word.
- Training config: kohya_ss dev branch, Illustrious XL v0.1 base, Adafactor optimizer, SDPA attention (no xformers), rank 32, 10 epochs, bf16 mixed precision.
- Results: 3,050 steps in 2h 12m on RTX 5080. Final avg loss: 0.080 (within target 0.08-0.12). Peak VRAM: 11.4GB.
- Output: Two checkpoints — epoch 5 (163MB) and epoch 10/final (163MB). Both saved as .safetensors.
- LoRA installed to ComfyUI: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style.safetensors`
- Config corrections applied during training: (1) `train_data_dir` must point to parent `dataset/` folder, not the `10_16bitfit_style` subfolder. (2) `fused_backward_pass` removed — only works with full fine-tuning, not LoRA training via `train_network.py`.
- Sample images from training look bad — this is EXPECTED because training samples use raw Illustrious XL v0.1 with minimal sampler settings. The real test is using the LoRA in ComfyUI with a proper base model (v2.0-STABLE or v3.x).
- The source config in the superuser pack has been updated with both corrections.
</project_status>

<immediate_tasks>
These are the things we need to do now, in priority order:

## 1. Test LoRA in ComfyUI (CRITICAL NEXT STEP)
The LoRA is trained and installed in ComfyUI on the Alienware, but we haven't tested it with a proper inference setup yet. We need a Claude Code prompt for the Alienware that will:
- Load Illustrious XL v2.0-STABLE or v3.x as the base model (NOT v0.1 — that's the training base, not the inference base)
- Apply the `16bitfit_sprite_style.safetensors` LoRA at strength 0.8
- Generate test images with the `16bitfit_style` trigger word
- Compare with and without LoRA at multiple strength levels (0.5, 0.7, 0.8, 0.9, 1.0)
- Use proper sampler settings: 28 steps, CFG 7, euler sampler, negative prompts
- Key question to answer: Does the LoRA improve pixel art style consistency enough to reduce retries in production?

Relevant files on Alienware:
- LoRA: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\models\loras\16bitfit_sprite_style.safetensors` (epoch 10) and `16bitfit_sprite_style-000005.safetensors` (epoch 5)
- ComfyUI: `C:\Users\seanw\Documents\Code-Brain\ComfyUI\` (launch with `--force-fp16`)
- Training runbook (test section): `lora-training/TRAINING-RUNBOOK.md` steps 11-13

## 2. Phase 4 Remaining Manual Tasks
- Install Vault Indexer + PR Digest launchd plists on Mac Mini
- Install gh CLI and authenticate (`brew install gh && gh auth login`)
- Download Illustrious XL v2.0-STABLE or v3.x on Alienware (for inference with the LoRA)

## 3. Update SOURCE-OF-TRUTH.md
After LoRA testing, update:
- Phase 4 checklist: Mark LoRA training items as complete
- Open Question #7 (LoRA quality): Resolve based on ComfyUI test results
- Add Training Run 001 results to the appropriate section

## 4. Phase 5 Planning and Execution
Phase 5 = Autoresearch + Scale (Weeks 9-12). See SOURCE-OF-TRUTH.md Part 4:
- Expand to full roster (all 12 fighters × 13 animations)
- Batch generation: 2nd and 3rd Champions through pipeline
- Build PixelLabAdapter behind VideoModelAdapter interface
- Fork ComfyGI mutation operators for autoresearch
- Implement Optuna TPE sampler for workflow parameter search
- Sprite pipeline dashboard
- Meta-Agent / Chief of Staff

## 5. Wan 2.2 14B Workflow Documentation
The Wan 2.2 14B dual-model workflow has specific requirements learned from Phase 4 debugging (documented in SOURCE-OF-TRUTH.md). These need to be accessible for ComfyUI workflow automation in Phase 5.
</immediate_tasks>

<key_files>

| File | Purpose |
|------|---------|
| `16bitfit-battle-mode/CLAUDE.md` | Non-negotiable rules, constraints, anti-patterns |
| `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` | Master reference (always read first) |
| `16bitfit-battle-mode/phase-4-completion-summary.md` | Phase 4 results + what's left |
| `16bitfit-battle-mode/lora-output/TRAINING-RUN-001.md` | LoRA training execution log |
| `16bitfit-battle-mode/lora-training/sprite-style-config.toml` | kohya_ss config (corrected) |
| `16bitfit-battle-mode/lora-training/TRAINING-RUNBOOK.md` | Step-by-step training + testing guide |
| `16bitfit-battle-mode/lora-training/generate_dataset.py` | Gemini image gen (36 original poses) |
| `16bitfit-battle-mode/lora-training/generate_dataset_supplement.py` | Gemini image gen (15 supplement poses) |
| `16bitfit-battle-mode/lora-training/prepare_dataset.py` | Dataset upscaler + captioner |
| `16bitfit-battle-mode/lora-training/generate_image.py` | Gemini API wrapper (local copy) |

</key_files>

<constraints>
All constraints from 16bitfit-battle-mode/CLAUDE.md apply. Key ones:
- Package = `claude-agent-sdk`, class = `ClaudeAgentOptions` (NOT old names)
- Never `dangerouslySkipPermissions`
- Credentials via macOS Keychain (not .env files) for agents
- RTX 5080: SDPA only (NO xformers), `--force-fp16` with ComfyUI
- Wan 2.2 (NOT 2.5). Wan 2.5 is NOT open source.
- LoRA: Trained on Illustrious XL v0.1, INFER on v2.0-STABLE or v3.x
- LoRA: Adafactor optimizer, SDPA attention, rank 32, kohya_ss dev branch only
- RIFE VFI is the confirmed interpolation engine (NOT GMFSS Fortuna)
- Hexagonal/Ports & Adapters architecture for the sprite pipeline
- Green screen (#00FF00) on keyframes BEFORE feeding to video models
- Mac Mini IP: 192.168.68.200, Alienware IP: 192.168.68.201
- LoRA training config corrections: train_data_dir = parent `dataset/` folder; no fused_backward_pass for LoRA training
- When I need prompts for Claude Code on specific machines, write them for me — I paste those into Claude Code terminals on the Mac Mini, MacBook Pro, or Alienware
</constraints>

<instructions>
1. Read the four files listed in <context> above
2. Confirm you understand the project status, what's been built, and what's next
3. Start by writing me a Claude Code prompt for the Alienware to test the trained LoRA in ComfyUI — this is the critical next step that tells us if the LoRA actually works
4. After LoRA testing, help me update SOURCE-OF-TRUTH.md and plan Phase 5 execution
5. When I need prompts for Claude Code on specific machines, write them for me — I paste those into Claude Code terminals on the Mac Mini, MacBook Pro, or Alienware
</instructions>
