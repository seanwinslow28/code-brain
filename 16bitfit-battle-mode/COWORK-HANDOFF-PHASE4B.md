# Cowork Handoff Prompt — 16BitFit Battle Mode (Phase 4B: LoRA Dataset + Phase 5 Planning)

## How to Use

Copy everything below the `---` line and paste it as your first message in a new Cowork thread.

---

<role>
You are my technical project partner for 16BitFit Battle Mode — a 12-week build spanning three workstreams: (A) autonomous agent infrastructure across a three-machine network, (B) a hybrid AI sprite sheet pipeline for a 2D fighting game, and (C) an autoresearch/LoRA training system. I'm a beginner with code, so please explain your reasoning for technical choices, but keep things brief and to the point.
</role>

<context>
Before responding, read these files in this exact order:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints, three-machine topology, model routing
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference with all phase checklists, architecture decisions, and open questions
3. `16bitfit-battle-mode/phase-4-completion-summary.md` — Phase 4 results (11/11 PASS, RIFE VFI confirmed, 8 agents, LoRA infra ready)

These three files contain everything you need. Do NOT load all docs at once — use the Session Loading Guide in SOURCE-OF-TRUTH.md Part 7 to pull specific reference files only when needed for implementation tasks.
</context>

<project_status>
We have completed Phases 1-4. Here's the current state:

**Phases 1-3 (COMPLETE):** Three-machine fleet online, 7 launchd agents, hybrid sprite pipeline PROVEN VIABLE (Wan 2.2 5B scored 73.7% through Pixel Quantizer), hexagonal adapter layer with 4 atomic operations, strategy router mapping 15 animation types.

**Phase 4 (COMPLETE — 11/11 PASS):**
- RIFE VFI confirmed as primary interpolation engine (GMFSS Fortuna blocked by cupy). RIFE through Pixel Quantizer scored **87.6% overall** — higher than raw NB2 keyframes (77.7%) and Wan 2.2 (73.7%).
- Walk cycle strategy LOCKED: NB2 multi-keyframe → RIFE VFI 4x interpolation → Pixel Quantizer
- 8 autonomous agents built (3 new in Phase 4: Vault Embedding Indexer, Preserve Session, PR Digest)
- LoRA training infrastructure ready: kohya_ss config, dataset prep script, training runbook
- PixelLab v3 has a public API ($0.007-$0.016/gen, 128×128 max) — viable for pipeline integration
- Wan 2.2 + pixel animate LoRA workflows confirmed working on Alienware

**LoRA Dataset Preparation (IN PROGRESS — this is where we are):**
- Built `lora-training/slice_turnarounds.py` — slices composite turnaround sheets into individual training images. 34 source images → 130 individual crops.
- Built `lora-training/generate_dataset.py` — generates 36 new action poses using Gemini NB2 with existing character images as style references. Uses the 7-Layer Prompt Framework from image-generator-prompt-science skill + Battle Mode style cluster from 16bitfit-styles.md.
- Generation plan: 6 champions × 4 poses (fighting stance, high kick, jab punch, block) + 6 bosses × 2 poses (menacing idle, attack windup) = 36 images
- All prompts use green screen (#00FF00) backgrounds and character turnaround sheets as identity-locking references
- **NOT YET RUN** — need to test with 1-2 characters first, review quality, then run full batch

**The sliced dataset has some crops that are cut off** (fixed percentage-based cropping doesn't perfectly fit every character's spacing). Sean needs to do a quick curation pass to delete bad crops. This is expected and OK — for LoRA training, the model learns style patterns from whatever is visible, and minor edge artifacts don't significantly affect training quality. But images where the character is mostly off-frame should be removed.

**8 autonomous agents total:** Daily Driver, Process Inbox, Spending Analysis, Sprint Health Monitor, Meeting Defender, Vault Embedding Indexer, Preserve Session, PR Digest

**Key video model ranking:**
| Source | Overall Score | Gate |
|--------|-------------|------|
| RIFE VFI → Pixel Quantizer | 87.6% | PASS (best quality) |
| Raw NB2 Keyframes | 77.7% | PASS |
| Wan 2.2 5B ti2v | 73.7% | PASS |
| rd-animation (Replicate) | 0% | DEAD |
</project_status>

<immediate_tasks>
These are the things we need to do now, in this order:

**1. Test Gemini image generation (the critical next step):**
- Run `generate_dataset.py` for 1-2 characters as a test
- Review the output images — does Gemini maintain the 16BitFit pixel art style?
- If quality is good, run the full 36-image batch
- The script is at: `16bitfit-battle-mode/lora-training/generate_dataset.py`
- It uses: `gemini-pixel-image-gen` skill (scripts/generate_image.py) + `image-generator-prompt-science` skill
- Reference images for identity locking are at: `16bitfit-battle-mode/lora-training/LoRA-Training-Dataset/Sprite Sheet Reference Images/`
- Requires: GEMINI_API_KEY in environment or .env file

**2. Curate the sliced dataset:**
- Review `lora-training/sliced-dataset/` (130 images from the slicer)
- Delete any crops where the character is mostly cut off or the image is just empty background
- Keep everything that has a recognizable character in the 16BitFit style

**3. Merge + prepare final training dataset:**
- Combine best sliced images + generated images into one folder
- Run the Phase 4 `prepare_dataset.py` to nearest-neighbor upscale to 1024×1024 and generate caption .txt files
- Target: 50-80 high-quality training images

**4. LoRA training on Alienware:**
- Follow `lora-training/TRAINING-RUNBOOK.md`
- Copy dataset to Alienware, run kohya_ss (dev branch, Adafactor, SDPA, rank 32, Illustrious XL v0.1)
- Test trained LoRA in ComfyUI

**5. Phase 4 remaining manual tasks:**
- Install Vault Indexer + PR Digest launchd plists on Mac Mini
- Install gh CLI and authenticate (`brew install gh && gh auth login`)
- Review Alienware video outputs (Wan 2.2 with vs without LoRA, motion prompt experiments)
- Download Illustrious XL v0.1 on Alienware

**6. Phase 5 planning and execution:**
- After LoRA training, update SOURCE-OF-TRUTH.md and plan Phase 5
- Phase 5 = Autoresearch + Scale (Weeks 9-12): expand to full roster, batch generation, autoresearch loop, dashboard
- See SOURCE-OF-TRUTH.md Part 4 for Phase 5 checklist
</immediate_tasks>

<key_files>
| File | Purpose |
|------|---------|
| `16bitfit-battle-mode/CLAUDE.md` | Non-negotiable rules, constraints, anti-patterns |
| `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` | Master reference (always read first) |
| `16bitfit-battle-mode/phase-4-completion-summary.md` | Phase 4 results + what's left |
| `16bitfit-battle-mode/lora-training/generate_dataset.py` | Gemini image generation script (36 prompts) |
| `16bitfit-battle-mode/lora-training/slice_turnarounds.py` | Turnaround sheet slicer |
| `16bitfit-battle-mode/lora-training/prepare_dataset.py` | Dataset upscaler + captioner (from Phase 4) |
| `16bitfit-battle-mode/lora-training/TRAINING-RUNBOOK.md` | Step-by-step LoRA training guide |
| `16bitfit-battle-mode/lora-training/sprite-style-config.toml` | kohya_ss training config |
| `.claude/skills/gemini-pixel-image-gen/SKILL.md` | Gemini image generation skill |
| `.claude/skills/image-generator-prompt-science/SKILL.md` | Prompt engineering for image gen |
| `.claude/skills/image-generator-prompt-science/references/16bitfit-styles.md` | Battle Mode style definitions + color palettes |
| `16bitfit-battle-mode/PHASE-4-KICKOFF-PROMPT.md` | Phase 4 Claude Code prompt (for reference) |
</key_files>

<constraints>
All constraints from 16bitfit-battle-mode/CLAUDE.md apply. Key ones:
- Package = `claude-agent-sdk`, class = `ClaudeAgentOptions` (NOT old names)
- Never `dangerouslySkipPermissions`
- Credentials via macOS Keychain (not .env files) for agents
- RTX 5080: SDPA only (NO xformers), `--force-fp16` with ComfyUI
- Wan 2.2 (NOT 2.5). Wan 2.5 is NOT open source.
- LoRA: Train on Illustrious XL v0.1, infer on v2.0-STABLE or v3.x
- LoRA: Adafactor optimizer, SDPA attention, rank 32, kohya_ss dev branch only
- RIFE VFI is the confirmed interpolation engine (NOT GMFSS Fortuna)
- Hexagonal/Ports & Adapters architecture for the sprite pipeline
- Green screen (#00FF00) on keyframes BEFORE feeding to video models
- Mac Mini IP: 192.168.68.200, Alienware IP: 192.168.68.201
</constraints>

<instructions>
1. Read the three files listed in <context> above
2. Confirm you understand the project status, what's been built, and what's next
3. Start by helping me test the Gemini image generation — run `generate_dataset.py` for Sean first (4 images), review quality, and iterate on prompts if needed
4. After dataset generation is complete, help me with the remaining Phase 4 manual tasks and Phase 5 planning
5. When I need prompts for Claude Code on specific machines, write them for me — I paste those into Claude Code terminals on the Mac Mini, MacBook Pro, or Alienware
</instructions>
