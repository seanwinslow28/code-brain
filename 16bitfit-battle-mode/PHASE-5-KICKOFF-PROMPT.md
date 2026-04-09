# Phase 5 Kickoff Prompt for Claude Code

## How to Use This

**Before pasting this prompt into Claude Code**, complete the manual setup checklist below. Phase 5 is the final phase — Autoresearch + Scale. The LoRA path has been abandoned; this phase focuses entirely on scaling the proven NB2 → RIFE VFI → Pixel Quantizer pipeline and building autoresearch to optimize it.

---

## YOUR MANUAL CHECKLIST (Do These First)

### Mac Mini — Remaining Phase 4 Tasks

- [ ] Install launchd plists for Vault Indexer + PR Digest:
  ```bash
  cp agents-sdk/schedules/com.sean.agent.vault-indexer.plist ~/Library/LaunchAgents/
  cp agents-sdk/schedules/com.sean.agent.pr-digest.plist ~/Library/LaunchAgents/
  launchctl load ~/Library/LaunchAgents/com.sean.agent.vault-indexer.plist
  launchctl load ~/Library/LaunchAgents/com.sean.agent.pr-digest.plist
  ```
- [x] ~~Install gh CLI and authenticate~~ — DONE

### Cross-Machine Verification

- [ ] Mac Mini online: `curl http://192.168.68.200:11434/api/tags`
- [ ] Alienware online: `curl http://192.168.68.201:11434/api/tags`
- [ ] ComfyUI running on Alienware with `--force-fp16`

### PixelLab API

- [x] ~~Sign up and get API key~~ — DONE
- [x] ~~Store key in Keychain~~ — DONE (`pixellab-key`)

---

## THE CLAUDE CODE PROMPT

Paste everything below the line into Claude Code, starting a session from the `claude-code-superuser-pack` root directory.

---

```
You are continuing the 16BitFit Battle Mode build — Phase 5 (final phase) of a 12-week project. Phases 1-4 are complete. The LoRA training path has been abandoned — Gemini NB2 keyframes are confirmed as the production image source.

<role>
You are a senior systems engineer and creative pipeline architect. Phase 5 has three parallel threads: (1) scaling the sprite pipeline to batch-produce all fighter animations, (2) building an autoresearch loop to optimize NB2 prompt templates and pipeline parameters, and (3) adding a PixelLab adapter and Meta-Agent for fleet orchestration. You write clean, typed, tested code. You follow hexagonal/ports-and-adapters architecture.
</role>

<context>
Read these files in this exact order before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference (Part 4 Phase 5 checklist is your task list)
3. `16bitfit-battle-mode/phase-4-completion-summary.md` — Phase 4 results (adapters built, RIFE confirmed, strategy router)
4. `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — Current adapter interfaces and implementations
5. `16bitfit-battle-mode/pixel-quantizer/video-eval/strategy_router.py` — Strategy map (10 IMAGE_ONLY + 5 HYBRID)
6. `16bitfit-battle-mode/docs/lora-autoresearch/autoresearch-overview.md` — Autoresearch concept (ComfyGI, Optuna, ImageReward)
7. `16bitfit-battle-mode/docs/validation/opportunity-scan.md` — ComfyGI details, Optuna TPE, quality metrics upgrade

After reading, confirm you understand: (a) the locked pipeline (NB2 → RIFE VFI → Pixel Quantizer, 87.6%), (b) the four atomic adapter operations, (c) the strategy decision map, and (d) the autoresearch architecture before proceeding.
</context>

<machine_ips>
Mac Mini LAN IP: 192.168.68.200
Alienware LAN IP: 192.168.68.201
MacBook Pro: localhost (this machine)
</machine_ips>

<phase4_artifacts>
These were built in Phases 1-4 and are available for use:
- `agents-sdk/config.toml` — routing config with all 3 machines + 8 task mappings
- `agents-sdk/lib/keychain.py` — macOS Keychain credential helper
- `agents-sdk/lib/hybrid_router.py` — three-tier routing with WOL, fallback chain
- `agents-sdk/lib/baton.py` — inter-agent dependency utility
- `agents-sdk/agents/` — 8 agents: daily_driver, process_inbox, spending_analysis, sprint_health, meeting_defender, vault_indexer, preserve_session, pr_digest
- `.claude/hooks/` — loop-detector, cost-watchdog, vault-integrity (exit code 2 to block)
- `pixel-quantizer/` — 7-step Pixel Quantizer (13 tests passing)
- `pixel-quantizer/video-eval/adapters.py` — VideoModelAdapter ABC + GeminiAdapter, Wan22Adapter, RIFEAdapter, ReplicateAdapter, GMFSSAdapter (alias)
- `pixel-quantizer/video-eval/strategy_router.py` — Strategy map: 10 IMAGE_ONLY, 5 HYBRID. GenerationPlan with adapter assignments.
- `pixel-quantizer/video-eval/workflows/rife_interpolation.json` — RIFE VFI ComfyUI workflow
- `pixel-quantizer/video-eval/evaluator.py` — Evaluation harness (quantizer scoring)
- RIFE VFI tested: 87.6% through Pixel Quantizer, 0 off-palette pixels, best score in project
- Wan 2.2 14B I2V tested: dual fp8 + LightX2V 4-step LoRA, working
- NB2 > NB Pro benchmark: NB2 26% faster, comparable quality. NB2 is primary.
</phase4_artifacts>

<key_decisions>
- LoRA path ABANDONED (April 8, 2026). Multiple training attempts produced anime-proportioned characters, not SF2 arcade sprites. Gemini NB2 generates the correct style natively.
- Production pipeline LOCKED: Gemini NB2 keyframes → RIFE VFI 4x interpolation → Pixel Quantizer
- IMAGE_ONLY strategy for: idle, crouch, light_punch, medium_punch, heavy_punch, light_kick, block, guard_break, hit_stun, knockdown
- HYBRID strategy for: walk, run, jump, special_1, victory
- NB2 for all keyframe generation (not NB Pro). NB Pro reserved for anchor/hero frames only.
- Green screen (#00FF00) on keyframes BEFORE feeding to video/interpolation models
- RIFE VFI (rife49.pth) is primary interpolation. FILM VFI is backup.
- Wan 2.2 14B is available for single-keyframe animation (seed-dependent quality)
</key_decisions>

<constraints>
CRITICAL — same constraints as all previous phases:
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Never use `dangerouslySkipPermissions`
- Credentials come from macOS Keychain via `lib/keychain.py`, not .env files
- RTX 5080 uses SDPA attention (NO xformers)
- Mac Mini runs `phi4-mini-reasoning` (3.8B), NOT "phi4" (14B)
- Alienware vision model is `qwen3-vl:8b` (NOT `qwen3-vl:7b`)
- ComfyUI on Alienware uses `--force-fp16`
- Wan 2.2 (NOT 2.5). Wan 2.5 is NOT open source.
- Sprite pipeline uses hexagonal architecture — all external tools behind Adapter interfaces
- All new adapters MUST extend VideoModelAdapter ABC from adapters.py
- Green screen (#00FF00) on keyframes BEFORE feeding to video/interpolation models
- Sprite tiles: Champions 128×128, Bosses 256×256
- Sprites generated facing RIGHT
- Full scope: 12 fighters (6 Champions + 6 Bosses) × 13 animations × 4-12 frames = ~900-1,400 total frames
- Each character has 3 anchor reference images (anchor-1, anchor-2, anchor-3) for NB2 to reference
- Anchor images path (same on all machines): `16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/`

FULL CHARACTER ROSTER:

Champions (128×128):
  - Sean: `champions/Sean/champion_sean_anchor-{1,2,3}.png` — Muscular build, blonde hair, white tank top, blue pants, white shoes
  - Aria: `champions/Aria/champion_aria_anchor-{1,2,3}.png` — Athletic build, brown hair in ponytail, purple crop top, light jeans, white shoes
  - Kenji: `champions/Kenji/champion_kenji_anchor-{1,2,3}.png` — Lean build, black hair in bun, gray gi top, dark gray pants, white shoes
  - Marcus: `champions/Marcus/champion_marcus_anchor-{1,2,3}.png` — Heavy muscular build, dark skin, short hair, gray tank top, yellow boxing gloves, gray pants, gray shoes
  - Mary: `champions/Mary/champion_mary_anchor-{1,2,3}.png` — Athletic build, brown hair in ponytail, purple headband, purple sports bra, purple shorts, gray shoes
  - Zara: `champions/Zara/champion_zara_anchor-{1,2,3}.png` — Athletic build, dark hair in low bun, dark gray tank top, dark cargo pants, white shoes

Bosses (256×256):
  - Gym Bully: `bosses/Gym Bully/boss_gym_bully_anchor-{1,2,3}.png` — Muscular build, dark hair, sunglasses, olive tank top, red wristbands, gray pants, gray shoes
  - Procrastination Phantom: `bosses/Procrastination Phantom/boss_procrastination_phantom_anchor-{1,2,3}.png` — Ghostly figure, white hoodie, blue-gray skin, glowing orange eyes, spectral tail (no legs)
  - Sloth Demon: `bosses/Sloth Demon/boss_sloth_demon_anchor-{1,2,3}.png` — Stocky beast, brown fur, gray armor plates, yellow eyes, clawed feet
  - Stress Titan: `bosses/Stress Titan/boss_stress_titan_anchor-{1,2,3}.png` — Tall armored figure, gray skin, white hair, black and orange power suit
  - Training Dummy: `bosses/Training Dummy/boss_training_dummy_anchor-{1,2,3}.png` — Wooden/leather training dummy, metal face plate, brown leather straps, bolted construction
  - Ultimate Slump: `bosses/Ultimate Slump/boss_ultimate_slump_anchor-{1,2,3}.png` — Hulking figure, pale green-gray skin, long dark hair, hunched posture, minimal clothing
</constraints>

<tasks>
Build the following. The three threads are independent — you may interleave them, but complete each task's verification before moving on.

=== THREAD 1: SCALE TO PRODUCTION ===

TASK 1: Build Batch Generation Orchestrator
- Location: `16bitfit-battle-mode/pixel-quantizer/batch/batch_orchestrator.py`
- Purpose: Takes a character manifest (JSON) and generates ALL animation frames for that character through the correct pipeline (IMAGE_ONLY or HYBRID per the strategy router)
- Character manifest schema:
  {
    "name": "Sean",
    "tile_size": 128,
    "type": "champion",
    "description": "Muscular build, blonde hair, white tank top, blue pants, white shoes",
    "anchor_images": [
      "16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/champions/Sean/champion_sean_anchor-1.png",
      "16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/champions/Sean/champion_sean_anchor-2.png",
      "16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images/champions/Sean/champion_sean_anchor-3.png"
    ],
    "animations": ["idle", "walk", "run", "light_punch", ...]
  }
- The `anchor_images` array gives NB2 multiple reference angles for better character consistency. The prompt library should reference the anchor images when building generation prompts (GeminiAdapter supports image input alongside text prompts).
- The `description` field is the text fallback when image-conditioning is not available.
- For each animation:
  - Look up strategy in DEFAULT_STRATEGY_MAP
  - Look up frame count and duration from strategy_router.py
  - If IMAGE_ONLY: call GeminiAdapter.generate_frame() for each frame with pose-specific prompts
  - If HYBRID: call GeminiAdapter.generate_keyframes() → RIFEAdapter.interpolate_frames() → Pixel Quantizer
  - Save frames to `output/{character_name}/{animation_type}/frame_XX.png`
  - Run Pixel Quantizer on all output frames
  - Score results with evaluator.py
  - Generate per-animation quality report
- Track progress: output `batch_status.json` with per-animation status (pending/in_progress/complete/failed)
- Resumable: skip animations that already have complete, passing output frames
- VERIFY: Run with `--dry-run` flag against a mock manifest with 3 animations (idle, walk, light_punch). Confirm it routes idle and light_punch to IMAGE_ONLY, walk to HYBRID, and generates correct adapter calls.

TASK 2: Build NB2 Prompt Template Library
- Location: `16bitfit-battle-mode/pixel-quantizer/prompts/prompt_library.py`
- Purpose: Structured prompt templates for each animation type, replacing ad-hoc prompt strings scattered through the codebase
- Each template gets:
  - `animation_type`: the animation name
  - `character_config`: palette, name, tile size
  - `frame_index`: which frame in the sequence (0-indexed)
  - `total_frames`: total frames for this animation
  - `strategy`: IMAGE_ONLY or HYBRID
- Returns a fully formatted prompt string with:
  - Character description (from palette/config)
  - Pose description specific to animation type AND frame index (e.g., walk frame 0 = "left foot forward", frame 4 = "right foot forward")
  - Style tokens: "SF2 pixel art, bold #272929 outlines, clean pixel edges, transparent background"
  - Green screen directive: "solid #00FF00 green background"
  - Facing: "facing right"
  - Tile size: "128x128 sprite" or "256x256 sprite"
- Include negative prompt templates
- For HYBRID animations, also generate keyframe descriptions (which specific poses to use as keyframes for RIFE interpolation — e.g., walk cycle keyframes: contact, passing, contact, passing)
- Write at least the following animation templates: idle (4 frames), walk (8 frames), run (8 frames), light_punch (6 frames), medium_punch (6 frames), heavy_punch (8 frames), light_kick (6 frames), jump (8 frames), block (4 frames), hit_stun (4 frames), knockdown (6 frames), special_1 (10 frames), victory (12 frames)
- VERIFY: Generate prompts for all 13 animation types for the "Sean" character. Print the first and last frame prompt for each. Confirm: (a) every prompt contains the trigger tokens and green screen directive, (b) walk/run/jump/special/victory route through HYBRID keyframe prompts, (c) frame descriptions actually change between frames (not duplicated)

TASK 3: Build Manifests for ALL 12 Characters
- Location: `16bitfit-battle-mode/pixel-quantizer/manifests/`
- Create one JSON manifest per character using the schema from Task 1
- Each manifest must include:
  - `name`, `tile_size` (128 for champions, 256 for bosses), `type` ("champion" or "boss")
  - `description` (text description of the character's appearance — use the descriptions from the <constraints> FULL CHARACTER ROSTER section above)
  - `anchor_images` (array of 3 paths to the character's anchor PNGs in `16BitFit-Reference-Images/`)
  - `animations` (all 13 animation types)
- File naming: `champion_sean.json`, `champion_aria.json`, `champion_kenji.json`, `champion_marcus.json`, `champion_mary.json`, `champion_zara.json`, `boss_gym_bully.json`, `boss_procrastination_phantom.json`, `boss_sloth_demon.json`, `boss_stress_titan.json`, `boss_training_dummy.json`, `boss_ultimate_slump.json`
- IMPORTANT: For non-humanoid bosses (Procrastination Phantom has no legs, Sloth Demon has clawed feet, Training Dummy is wooden), the prompt library may need character-specific overrides for walk/run/jump animations. Add a `pose_overrides` field to the manifest schema for this — e.g., Procrastination Phantom's "walk" should be described as "floating forward" not "legs striding."
- Also create `all_characters.json` — a manifest list that references all 12 character files, for running the full batch
- VERIFY: Validate all 12 manifests load correctly. Run the orchestrator in `--dry-run` mode with `champion_sean.json` AND `boss_sloth_demon.json` (one champion, one boss) to confirm both tile sizes and character types route properly.

=== THREAD 2: AUTORESEARCH LOOP ===

TASK 4: Build Autoresearch Framework
- Location: `16bitfit-battle-mode/autoresearch/`
- Purpose: Automated parameter search to find the optimal NB2 prompt + RIFE pipeline settings per animation type.

What autoresearch means (brief explanation): Instead of manually tweaking prompt words, sampler settings, or pipeline parameters and eyeballing results, we let a search algorithm (Optuna) try many combinations automatically and score each one. It's like having a robot try 100 different settings and tell you which one produced the best sprite.

Build these modules:

a) `autoresearch/search_space.py` — Defines what parameters can be mutated:
   - NB2 prompt parameters: style descriptor words (list of options), pose phrasing variants, negative prompt tokens
   - RIFE parameters: interpolation multiplier (2x, 4x, 8x), model variant (rife46, rife47, rife49)
   - Pixel Quantizer parameters: palette size (16, 24, 32 colors), outline thickness (1, 2, 3 px), temporal smoothing window (3, 5, 7 frames)
   - KSampler-equivalent parameters for ComfyUI workflows: steps (20-40), CFG (5-12)
   - Each parameter marked as categorical (pick from list) or numerical (range with step)

b) `autoresearch/scorer.py` — Fitness function that evaluates a generated sprite frame:
   - Primary: Pixel Quantizer gate check score (the existing evaluator.py pipeline: palette compliance, outline quality, character consistency, BG purity)
   - Secondary: Frame-to-frame consistency score (compare adjacent frames via SSIM + pixel identity ratio)
   - Returns a single float score (0-100) combining both, weighted 70% primary / 30% secondary
   - Log every evaluation to `autoresearch/results/experiment_log.jsonl` with full parameters + score

c) `autoresearch/optimizer.py` — Optuna TPE search wrapper:
   - Creates an Optuna study with TPE sampler (Tree-structured Parzen Estimator — this is smarter than random search because it learns which parameter regions are promising and samples more from those regions)
   - Each trial: sample parameters → generate frames via adapters → score → report to Optuna
   - Support `--max-trials N` (default 50) and `--timeout-hours H` (default 4)
   - Save best parameters to `autoresearch/results/best_params.json`
   - Resumable: Optuna's SQLite storage backend so you can stop and restart

d) `autoresearch/runner.py` — CLI entry point:
   - `python runner.py --animation-type walk --character sean --max-trials 50`
   - Connects optimizer to the real pipeline (GeminiAdapter → RIFEAdapter → Pixel Quantizer → scorer)
   - In `--dry-run` mode: uses mock adapters, doesn't call APIs
   - Outputs: best parameters, convergence plot (trials vs score), parameter importance chart

- VERIFY: Run `python runner.py --animation-type walk --character sean --max-trials 3 --dry-run`. Confirm: (a) Optuna creates a study and samples 3 trials, (b) mock adapters are called with different parameters each trial, (c) scores are logged to experiment_log.jsonl, (d) best_params.json is written

TASK 5: Build ComfyUI Workflow Mutator (for Alienware overnight runs)
- Location: `16bitfit-battle-mode/autoresearch/workflow_mutator.py`
- Purpose: Takes a base ComfyUI workflow JSON and mutates specific node parameters for each Optuna trial
- Load the RIFE interpolation workflow from `pixel-quantizer/video-eval/workflows/rife_interpolation.json`
- Identify mutable nodes: KSampler (steps, cfg, seed), RIFE settings (multiplier, model)
- Apply parameter overrides from Optuna trial suggestion
- Output mutated workflow JSON to temp directory
- Queue the mutated workflow to ComfyUI on Alienware via REST API (`http://192.168.68.201:8188/prompt`)
- Wait for completion via WebSocket, download result images
- VERIFY: Load the RIFE workflow, mutate KSampler steps from 20→30 and cfg from 7→10, output the mutated JSON, confirm the changes are in the correct nodes

=== THREAD 3: PIXELLAB ADAPTER + META-AGENT ===

TASK 6: Build PixelLabAdapter
- Location: Add to `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py`
- Must extend VideoModelAdapter ABC (same interface as GeminiAdapter, Wan22Adapter, etc.)
- PixelLab API details:
  - Python SDK: `pip install pixellab` (or REST API fallback)
  - Key endpoints: "Animate with Skeleton" (skeleton-based animation), "Estimate Skeleton" (extract pose from image), "Generate Sprite" (single frame)
  - Max output: 128×128 (matches Champion tile size perfectly)
  - Pricing: $0.007-$0.016 per generation
  - Native pixel art output — may NOT need Pixel Quantizer post-processing
- Implement the four atomic operations:
  - `generate_frame`: Use "Generate Sprite" endpoint
  - `generate_keyframes`: Use "Generate Sprite" for each keyframe pose
  - `interpolate_frames`: Use "Animate with Skeleton" with start/end keyframes
  - `generate_video`: Use "Animate with Skeleton" with full motion sequence
- API key from Keychain: `keychain.get_credential("pixellab-key")`
- Add PixelLab to the strategy router as an alternative adapter (not replacing NB2+RIFE — available as a routing option)
- If the PixelLab Python SDK is not installable or API has changed, build a REST adapter using httpx with the documented endpoints. Mark with TODO comments for any endpoints you cannot verify.
- VERIFY: Run with `--dry-run` using a StubPixelLabAdapter that returns synthetic frames. Confirm it plugs into the strategy router and evaluation framework correctly.

TASK 7: Build Meta-Agent / Chief of Staff
- Location: `agents-sdk/agents/meta_agent.py`
- Purpose: Orchestrates the entire agent fleet. Runs on Mac Mini, checks health of all agents, surfaces issues, generates daily fleet status summary.
- Reads fleet state from `vault/02_Areas/Agent-Fleet/fleet-state.md` (create this if it doesn't exist)
- Checks:
  - Which agents ran in the last 24h (check baton files in `~/.claude/batons/`)
  - Which agents failed or timed out (check agent log files)
  - Mac Mini, MacBook Pro, Alienware online status (ping Ollama endpoints)
  - ComfyUI status on Alienware (check REST API)
  - Disk space on all machines (if accessible)
- Outputs:
  - Fleet status summary to vault: `vault/02_Areas/Agent-Fleet/daily-fleet-status-YYYY-MM-DD.md`
  - If any agent failed: create a baton file `~/.claude/batons/fleet_alert.flag`
- Machine: Mac Mini (phi4-mini-reasoning for summary generation)
- Schedule: Daily at 06:30 (before Daily Driver at 08:45)
- Safety: max 10 turns, $0.10 budget cap (mostly local inference)
- Create launchd plist: `agents-sdk/schedules/com.sean.agent.meta-agent.plist`
- VERIFY: Run with `--dry-run`. Confirm it checks all endpoints, generates a status template, and writes the fleet state note structure.

TASK 8: Full Fleet Token Audit
- Location: `agents-sdk/audit/token_audit.py`
- Purpose: Analyze all 9 agents (8 existing + Meta-Agent) for token usage efficiency
- For each agent: estimate prompt size (skill file + system prompt + typical context), expected output size, cost per run
- Flag any agents where prompt exceeds 4K tokens (compression opportunity)
- Flag any agents using Claude API where a local model might suffice
- Output: `agents-sdk/audit/token_audit_report.md` with per-agent breakdown and recommendations
- VERIFY: Run the audit and confirm it covers all 9 agents with reasonable estimates

TASK 9: Write Phase 5 Completion Summary
- Location: `16bitfit-battle-mode/phase-5-completion-summary.md`
- Summarize all task results (PASS/FAIL for each)
- Report: batch orchestrator working? Prompt library complete for 13 animations? Autoresearch framework functional?
- PixelLab adapter status (working or stubbed)
- Meta-Agent fleet check results
- Token audit key findings
- List any issues that need updating in SOURCE-OF-TRUTH.md
- What's needed to run the first full batch generation (Champion #1 "Sean" through all 13 animations)
- What's needed for the first overnight autoresearch run on Alienware

</tasks>

<output_format>
For each task:
1. Read the relevant reference docs first (use the Session Loading Guide in SOURCE-OF-TRUTH.md Part 7)
2. Write the code
3. Run the verification step
4. Report: PASS or FAIL with details
5. If FAIL, fix and re-verify before moving on

After all tasks complete, provide the Phase 5 Completion Summary (Task 9).
</output_format>

<validation>
Before finishing, self-check:
1. Did you use `claude-agent-sdk` and `ClaudeAgentOptions` everywhere?
2. Are all credentials accessed via keychain.py, not .env or hardcoded?
3. Does PixelLabAdapter extend VideoModelAdapter ABC?
4. Does the batch orchestrator use the strategy router's DEFAULT_STRATEGY_MAP?
5. Do prompt templates include green screen (#00FF00) directive in EVERY prompt?
6. Do prompt templates include "facing right" in EVERY prompt?
7. Does the autoresearch framework use Optuna TPE (not random search)?
8. Does the workflow mutator target the Alienware ComfyUI at 192.168.68.201:8188?
9. Does Meta-Agent route to Mac Mini (phi4-mini-reasoning)?
10. Does Meta-Agent respect its budget cap ($0.10)?
11. Are all new files in the correct directories (not scattered)?
12. Did you run ALL verification steps and do they pass?
13. Is there any reference to the LoRA path? If so, REMOVE IT — that path is abandoned.
</validation>
```

---

## What Happens After

Once Claude Code completes these 9 tasks, you'll have:

**Built by Claude Code:**
- `pixel-quantizer/batch/batch_orchestrator.py` — Batch generation engine with resumable progress
- `pixel-quantizer/prompts/prompt_library.py` — 13 animation prompt templates with per-frame pose descriptions
- `pixel-quantizer/manifests/` — 12 character manifests (6 champions + 6 bosses) + `all_characters.json`
- `autoresearch/search_space.py` — Mutable parameter definitions
- `autoresearch/scorer.py` — Fitness function (Pixel Quantizer score + frame consistency)
- `autoresearch/optimizer.py` — Optuna TPE search wrapper with SQLite persistence
- `autoresearch/runner.py` — CLI entry point for autoresearch
- `autoresearch/workflow_mutator.py` — ComfyUI workflow JSON mutator for Alienware
- `PixelLabAdapter` in adapters.py — PixelLab API behind hexagonal interface
- `agents-sdk/agents/meta_agent.py` — Fleet orchestrator / Chief of Staff
- `agents-sdk/audit/token_audit.py` — Fleet-wide token usage analysis
- Phase 5 completion summary

**Your next manual steps after Claude Code finishes:**
1. Run the first REAL batch generation with Sean: `python batch_orchestrator.py --manifest manifests/champion_sean.json` (anchor images are already in place)
2. Run a second batch with a boss to test 256×256: `python batch_orchestrator.py --manifest manifests/boss_sloth_demon.json`
3. Run the first autoresearch experiment: `python runner.py --animation-type walk --character sean --max-trials 20`
4. Install Meta-Agent launchd plist on Mac Mini:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.meta-agent.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.meta-agent.plist
   ```
5. Review the token audit report and apply any compression recommendations
6. Test PixelLabAdapter with real API (key already in Keychain)
7. Schedule first overnight autoresearch run on Alienware (Mac Mini orchestrates via hybrid_router)
8. After autoresearch finds optimal params, run full roster batch: `python batch_orchestrator.py --manifest manifests/all_characters.json`
