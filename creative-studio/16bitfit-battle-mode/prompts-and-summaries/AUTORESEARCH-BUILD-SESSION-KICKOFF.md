# Claude Code Build Session: Autoresearch Phase 0 — Scoring Pipeline + Experiment Runner

**Date:** 2026-04-11
**Session Type:** Claude Code execution (NOT Cowork planning)
**Estimated Duration:** 1-2 sessions
**Owner:** Sean (beginner coder — explain technical choices clearly but briefly)

---

## What You're Building

You are building the autoresearch system for the **16BitFit Battle Mode** sprite generation pipeline. This system automatically runs experiments to improve sprite sheet quality — specifically **walk cycle animations**, which are the weakest output today.

The system follows Karpathy's three-file autoresearch pattern:
1. `prepare.py` — The **frozen scoring pipeline**. Measures experiment quality. The agent can NEVER modify this.
2. `experiment.json` — The **mutable config**. Contains prompt templates, reference strategies, and generation settings. The runner modifies this.
3. `program.md` — **Human-written research directions**. The runner reads this for strategy.

**This session builds the scoring pipeline (`prepare.py`) and the experiment runner (`runner.py`).** These are the two critical pieces. The `program.md` and `experiment.json` are already drafted in the autoresearch plan.

---

<context>
<required_reading>
Read ALL of these files before writing any code. They contain the architecture decisions, scoring rubric, existing code to integrate with, and reference material locations.

1. `16bitfit-battle-mode/prompts-and-summaries/AUTORESEARCH-PLAN.md` — **THE master plan.** Contains the full scoring pipeline design, walk cycle rubric, Phase 0 experiment structure, safety constraints, and three-file mapping. Every design decision in this build session comes from this document.

2. `16bitfit-battle-mode/Vision-model-research/vision-model-auditor-synthesis.md` — **The VLM integration spec.** Contains the tiered scoring architecture (hard gates → DINOv2 → VLM judge → escalation), the Chain-of-Rubrics prompting strategy, VLM adapter interfaces, image preprocessing requirements (4x upscale, side-by-side composition), and deployment configuration.

3. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — **Project master reference.** Read Part 2 Workstream B (sprite pipeline) and Workstream C (autoresearch). Contains the Pixel Quantizer 7-step pipeline, video model status, adapter architecture, and palette details.

4. `16bitfit-battle-mode/prompts-and-summaries/PHASE5C-SUMMARY.md` — **Latest phase results.** Contains the sheet→split approach, anchor Golden Rule, grid detection fix, palette expansion details, and the full roster generation results. Shows what the current pipeline produces and how.

5. `.claude/skills/2d-animation-principles/SKILL.md` — **Walk cycle animation rules.** Contains the 4 key walk cycle poses (Contact, Down, Passing, Up), timing on Twos, QA gates for twinning/spacing/arcs, and the physics engine rules. These principles must be embedded in the VLM scoring rubric.

6. `16bitfit-battle-mode/autoresearch/scorer.py` — **Existing scorer stub.** Has the `Scorer` class and `ScorerResult` dataclass, but uses placeholder scoring (TODOs). You will REPLACE the scoring logic with the real tiered pipeline.

7. `16bitfit-battle-mode/autoresearch/runner.py` — **Existing runner stub.** Has CLI argument parsing and calls `AutoresearchOptimizer`. You will REWRITE this to implement the Phase 0 experiment loop (generate → score → keep/revert → log).

8. `16bitfit-battle-mode/pixel-quantizer/batch/generate_sheet_split.py` — **The generation engine.** Contains `build_sheet_prompt`, `call_gemini`, `detect_grid`, `split_sheet`, `load_anchors`. Your experiment runner calls these functions to generate sprite sheets.

9. `16bitfit-battle-mode/pixel-quantizer/prompts/prompt_library.py` — **Current prompt templates.** Contains the walk_forward prompt template and all style constants (STYLE_TOKENS, GREEN_SCREEN, FACING, NEGATIVE_PROMPT). Phase 0 experiments will mutate these.

10. `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — **Existing adapters.** Contains RIFEAdapter, Wan22Adapter, GeminiAdapter, PixelLabAdapter behind the VideoModelAdapter interface. Reference for the hexagonal adapter pattern.
</required_reading>

<reference_materials>
These are the frozen reference images for the scoring pipeline. They live in:
`16bitfit-battle-mode/autoresearch/references/`

**Walk cycle references** (for the VLM judge — "this is what good looks like"):
- `references/walk_cycle/Walk-Cycle-Ref-1.png` — Isolated 6-frame walk cycle, large scale, clear Contact→Passing→Up progression. Best single reference.
- `references/walk_cycle/ryu-sf2-walk-crop.png` — Ryu SF2 walk cycle, cropped. Gold standard arcade fighter walk.
- `references/walk_cycle/axel-sor2-walk-crop.png` — Axel Streets of Rage 2 walk, cropped. Same 16-bit era, brawler style.

**Style references** (full character sheets for overall aesthetic evaluation):
- `references/style_standard/Arcade - Street Fighter 2 _ Super Street Fighter 2 - Fighters - Ryu.png`
- `references/style_standard/Arcade - Street Fighter 2 _ Super Street Fighter 2 - Fighters - Guile.png`

**Character anchors** (identity verification — 3 per character):
- `references/anchors/champions/Sean/champion_sean_anchor-{1,2,3}.png` — Primary test character for Phase 0.
- All 12 characters have anchors in `references/anchors/{champions,bosses}/{name}/`

**Current walk cycle output** (the baseline to beat):
- `pixel-quantizer/output/sean/walk_forward/walk_forward_sheet.png` — Current Sean walk (problematic — legs barely differentiate)
- `pixel-quantizer/output/sean/walk_forward/walk_forward_keyframes_sheet.png` — Keyframes for HYBRID
- `pixel-quantizer/output/aria/walk_forward/walk_forward_keyframes_sheet.png` — Aria walk (similar issues)
- `pixel-quantizer/output/kenji/walk_forward/walk_forward_keyframes_sheet.png` — Kenji walk (minimal leg variation)
</reference_materials>

<existing_code_to_integrate>
The autoresearch system lives at `16bitfit-battle-mode/autoresearch/`. Existing files:

| File | Status | Action |
|------|--------|--------|
| `__init__.py` | Exists | Keep |
| `scorer.py` | Stub with TODOs | **REWRITE** — Replace placeholder scoring with tiered pipeline |
| `runner.py` | Stub with basic CLI | **REWRITE** — Implement Phase 0 experiment loop |
| `optimizer.py` | Optuna wrapper | **KEEP or REFACTOR** — May not be needed for Phase 0 (structured sweeps, not Bayesian) |
| `search_space.py` | Optuna search space | **KEEP for later** — Phase 1 uses this |
| `workflow_mutator.py` | ComfyUI mutator | **KEEP for later** — Phase 1 uses this |
| `results/` | Existing logs | **KEEP** — Runner logs here |

The generation code lives at `16bitfit-battle-mode/pixel-quantizer/`. Key imports:
```python
from batch.generate_sheet_split import build_sheet_prompt, call_gemini, detect_grid, split_sheet, load_anchors
from prompts.prompt_library import PromptLibrary, STYLE_TOKENS, GREEN_SCREEN, FACING, NEGATIVE_PROMPT
```
</existing_code_to_integrate>
</context>

---

<instructions>

## Build Order (Complete Each Task Before Moving to the Next)

### Task 1: Build `prepare.py` — The Frozen Scoring Pipeline

Create `autoresearch/prepare.py` — the scoring pipeline that evaluates generated sprite sheets. This file is FROZEN during experiments. It must be a standalone module with no dependencies on the experiment config.

**Architecture (5 tiers, execute in order, short-circuit on hard failure):**

```
Generated Sprite Sheet
    ↓
[Tier 1] Hard Gates — Pixel Quantizer checks (palette, dimensions, alpha, BG)
    ↓ (FAIL = score 0, stop)
[Tier 2] Identity — DINOv2 cosine similarity vs anchor embeddings
    ↓
[Tier 3] Deterministic — Outline weight check, baseline drift, frame count validation
    ↓
[Tier 4] VLM Walk Cycle Judge — Qwen2.5-VL-7B via Ollama on Alienware
    ↓
[Tier 5] Escalation (optional) — Gemini 2.5 Flash API for borderline cases
    ↓
Composite Score (0.0 - 1.0)
```

**Tier 1 — Hard Gates:**
- Check each frame: correct dimensions (128×128 for champions, 256×256 for bosses), valid PNG, non-empty
- Palette compliance: all pixels within the character's palette (use `sf2_pixel_art` for non-Sean characters, `sean` for Sean)
- Background: frame must have green (#00FF00) or transparent background
- If ANY hard gate fails → return score 0.0 immediately, log failure reason

**Tier 2 — DINOv2 Identity:**
- Use `facebook/dinov2-base` (86M params) via `transformers` library
- Extract CLS token embeddings from each generated frame and from anchor image
- Cosine similarity between frame embedding and anchor embedding
- Average across all frames in the sheet
- Threshold: ≥ 0.85 considered good identity match
- This runs on GPU if available (Alienware), CPU fallback (Mac Mini) — detect automatically

**Tier 3 — Deterministic Checks:**
- Frame count matches expected (4 for walk_forward IMAGE_ONLY, 4 keyframes for HYBRID)
- Outline weight validation: dark outline pixels (#272929 or near) present but not > 50% of opaque pixels
- Character present in frame: opaque pixels (non-green, non-transparent) must be > 5% and < 80% of frame
- All frames have similar character bounding box size (no growing/shrinking > 20%)

**Tier 4 — VLM Walk Cycle Judge (THE KEY TIER):**

This is the most important tier. It evaluates what math-based metrics cannot — whether the walk cycle actually looks like walking.

**Preprocessing before sending to VLM:**
1. Upscale each frame 4x via nearest-neighbor (128→512, 256→1024) — VLMs perform poorly on tiny images
2. Compose a single comparison image: walk cycle reference (left) | 4px gray gap | generated sheet (right)
3. Also include the character's anchor-1 image (upscaled) as a separate image for identity context

**VLM Call — Qwen2.5-VL-7B via Ollama REST API:**
- Endpoint: `http://192.168.68.201:11434/api/chat` (Alienware Ollama)
- Model: `qwen2.5-vl:7b`
- Send: comparison image + anchor image + structured rubric prompt
- Timeout: 30 seconds
- Fallback: If Alienware unreachable, skip Tier 4 and log warning (don't fail the whole score)

**VLM Prompt (embed this exactly in prepare.py as a constant):**

```
You are a pixel art animation quality judge for a 16-bit arcade fighting game (Street Fighter II style).

REFERENCE IMAGE: A real arcade game walk cycle showing the gold standard for leg differentiation, weight shift, and pose progression.

GENERATED IMAGE: A sprite sheet of walk cycle frames to evaluate. Each cell is one animation frame.

ANCHOR IMAGE: The approved character design — use this to verify the generated frames show the correct character.

A correct walk cycle MUST show these 4 distinct poses across its frames:
1. CONTACT: Front heel strikes ground, rear leg trails behind. Legs at widest spread. Arms at maximum opposite swing.
2. DOWN: Body at its LOWEST point. Front leg absorbs weight, knee bends. This is the heaviest frame.
3. PASSING: Legs together, rear leg swings forward past the planted leg. Body at mid-height.
4. UP: Body at its HIGHEST point. Rear leg pushes off, front leg extends forward. This is the lightest frame.

Score each criterion from 1 (worst) to 5 (best):

1. LEG_DIFFERENTIATION: Are leg positions distinctly different across frames? (1 = all frames look the same, 5 = clear contact/passing/up/down poses visible)
2. POSE_PROGRESSION: Do poses follow a logical walking sequence? (1 = random or repeated poses, 5 = smooth contact→down→passing→up→contact cycle)
3. WEIGHT_SHIFT: Does the character's body move up and down naturally? (1 = character floats at same height, 5 = visible dip at DOWN pose and rise at UP pose)
4. ARM_SWING: Do arms swing opposite to legs? (1 = arms static or identical, 5 = natural opposite-leg arm swing with offset)
5. CHARACTER_CONSISTENCY: Is it the same character in every frame? (1 = different features between frames, 5 = identical character with only pose changes)
6. HEIGHT_CONSISTENCY: Is the character roughly the same size in all frames? (1 = character grows/shrinks noticeably, 5 = consistent size, height varies only with walk bob)

Respond in this exact JSON format:
{
  "leg_differentiation": {"score": 1-5, "reasoning": "brief explanation"},
  "pose_progression": {"score": 1-5, "reasoning": "brief explanation"},
  "weight_shift": {"score": 1-5, "reasoning": "brief explanation"},
  "arm_swing": {"score": 1-5, "reasoning": "brief explanation"},
  "character_consistency": {"score": 1-5, "reasoning": "brief explanation"},
  "height_consistency": {"score": 1-5, "reasoning": "brief explanation"},
  "composite_score": 0.0-1.0,
  "primary_issue": "one sentence describing the biggest quality problem, or 'none' if all scores >= 4",
  "suggested_fix": "one sentence describing how to improve the generation prompt, or 'none'"
}

SCORING RULE: composite_score = (sum of all scores) / 30.0
If ANY score is 1, the walk cycle fundamentally fails — composite_score should not exceed 0.3.
```

**VLM Score Weights in Composite:**
```python
walk_weights = {
    "leg_differentiation": 0.25,
    "pose_progression": 0.20,
    "weight_shift": 0.20,
    "character_consistency": 0.15,
    "arm_swing": 0.10,
    "height_consistency": 0.10,
}
```

**Tier 5 — Escalation (implement as a stub for now):**
- If VLM confidence is low (any score = 3) AND Gemini API key is available, escalate to Gemini 2.5 Flash
- For Phase 0, implement the interface but default to disabled
- Log when escalation would have fired

**Final Composite Score:**
```python
final_score = (
    0.15 * hard_gate_pass  # 1.0 if all pass, 0.0 if any fail
  + 0.20 * dino_identity   # 0.0-1.0 cosine similarity
  + 0.10 * deterministic   # 0.0-1.0 average of tier 3 checks
  + 0.55 * vlm_walk_score  # 0.0-1.0 from VLM rubric (THIS IS THE MAJORITY)
)
```

The VLM score is weighted at 55% because walk cycle quality is the primary optimization target. Hard gates are only 15% because they're binary (pass/fail) — a sheet either passes or it doesn't.

**`prepare.py` must export:**
```python
class AutoresearchScorer:
    def __init__(self, character: str, animation_type: str, alienware_host: str = "192.168.68.201")
    def score_sheet(self, sheet_path: Path, frames: list[Path]) -> ScoreResult
    def score_dry_run(self) -> ScoreResult  # For testing without generation

@dataclass
class ScoreResult:
    composite: float          # 0.0-1.0 final score
    hard_gates: dict          # Per-gate pass/fail
    dino_identity: float      # 0.0-1.0
    deterministic: dict       # Per-check scores
    vlm_scores: dict          # Per-criterion scores from VLM
    vlm_raw_response: str     # Full VLM JSON response
    primary_issue: str        # From VLM
    suggested_fix: str        # From VLM
    tier_reached: int         # 1-5, how far scoring got
    timestamp: float
```

**Implementation notes:**
- Use `Pillow` (PIL) for image manipulation (upscale, compose side-by-side)
- Use `transformers` library for DINOv2 (will auto-use GPU if available via torch)
- Use `httpx` for Ollama REST API calls (async not needed — synchronous is fine for Phase 0)
- Use `numpy` for cosine similarity computation
- Install dependencies: `pip install Pillow transformers torch httpx numpy`
- If DINOv2 model download is too large for the session, implement with a `--skip-dino` flag that defaults tier 2 to 1.0
- If Alienware/Ollama is unreachable, skip Tier 4 gracefully and return a partial score with a warning

### Task 2: Build `runner.py` — The Phase 0 Experiment Loop

Rewrite `autoresearch/runner.py` to implement the Phase 0 Gemini prompt optimization loop.

**The experiment loop:**
```
1. Load experiment.json (current best config)
2. Load program.md (research directions)
3. Parse the current round and experiment number from results log
4. For each experiment:
   a. Read the next experiment direction from program.md
   b. Mutate experiment.json (change prompt template, reference strategy, etc.)
   c. Call Gemini NB2 to generate a walk cycle sprite sheet using the mutated config
   d. Split the sheet into individual frames
   e. Score the sheet + frames using prepare.py
   f. If score > best_score: save as new best, commit experiment.json to git
   g. If score <= best_score: revert experiment.json
   h. Log everything to results.tsv and experiment_log.jsonl
   i. Wait 10s (Gemini rate limit) then repeat
5. After all experiments (or budget/timeout hit): write summary
```

**`experiment.json` structure (create the initial version):**
```json
{
  "version": 1,
  "character": "sean",
  "animation_type": "walk_forward",
  "generation": {
    "model": "gemini-2.0-flash-preview-image-generation",
    "prompt_template": "current walk_forward prompt from prompt_library.py",
    "negative_prompt": "current NEGATIVE_PROMPT constant",
    "reference_strategy": "3_anchors",
    "sheet_layout": "full_sheet",
    "frame_count": 4,
    "include_pose_names": false,
    "include_animation_principles": false,
    "include_walk_cycle_reference": false,
    "additional_constraints": []
  },
  "scoring": {
    "skip_dino": false,
    "skip_vlm": false,
    "alienware_host": "192.168.68.201",
    "vlm_timeout_s": 30
  }
}
```

**`program.md` (create this file):**
Use the research directions from the AUTORESEARCH-PLAN.md — the 5-round, 100-experiment strategy for walk_forward optimization. Copy it directly.

**CLI interface:**
```bash
# Phase 0 — Gemini prompt optimization
python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 100 --budget 7.00

# Dry run (no API calls, tests the loop with mock scores)
python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 5 --dry-run

# Resume from where we left off
python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 100 --resume
```

**Safety constraints (enforce in code):**
- Budget cap: `--budget` flag, default $7.00. Track cumulative cost (~$0.07/call). Stop when budget exceeded.
- Timeout: `--timeout-hours` flag, default 2.0. Stop when exceeded.
- Rate limit: 10-second delay between Gemini API calls.
- Revert on failure: If experiment scores lower, revert `experiment.json` to previous version.
- Git commit on improvement: Auto-commit `experiment.json` with message "autoresearch: score {old} → {new} ({param_changed})"

**Results logging:**
- `results/results.tsv` — Tab-separated: experiment_id, round, params_changed, composite_score, vlm_walk_score, dino_identity, hard_gates_pass, cost_usd, generation_time_s, timestamp
- `results/experiment_log.jsonl` — Full JSON per experiment (all scores, VLM response, config snapshot)
- `results/best_experiment.json` — Copy of experiment.json at highest score
- `results/summary.md` — Written at end of run: best score, worst score, mean, top findings

### Task 3: Create `experiment.json` — The Initial Mutable Config

Create `autoresearch/experiment.json` with the baseline config. This represents the CURRENT walk_forward generation approach — no optimizations yet. The first experiment scores this baseline; all subsequent experiments try to beat it.

Pull the current walk_forward prompt from `prompt_library.py` and the current generation settings from `generate_sheet_split.py`.

### Task 4: Create `program.md` — The Research Directions

Create `autoresearch/program.md` with the 5-round experiment strategy from the AUTORESEARCH-PLAN.md. Copy the Phase 0 `program.md` content directly — it has the 20-experiment-per-round breakdown for prompt structure, reference strategy, sheet layout, negative prompts, and fine-tuning.

### Task 5: Validate the Build

Run these checks:

1. **Dry run test:** `python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 3 --dry-run` — Should complete without errors, produce mock scores, log to results/
2. **Import test:** Verify `prepare.py` imports correctly and can instantiate `AutoresearchScorer`
3. **Scoring test:** Create a test that scores an existing sprite sheet (`pixel-quantizer/output/sean/walk_forward/walk_forward_sheet.png`) through at least Tiers 1-3 (hard gates, DINOv2, deterministic). Tier 4 (VLM) may not be available if Alienware is offline — that's OK, just verify it gracefully skips.
4. **Reference loading test:** Verify all reference images in `autoresearch/references/` load correctly
5. **File structure check:** Verify these files exist after the build:
   - `autoresearch/prepare.py` (new)
   - `autoresearch/runner.py` (rewritten)
   - `autoresearch/experiment.json` (new)
   - `autoresearch/program.md` (new)
   - `autoresearch/results/` directory exists

</instructions>

---

<rules>
## Non-Negotiable Rules

1. **`prepare.py` is FROZEN by design.** The experiment runner must NEVER import from or modify `prepare.py` beyond calling its public API. This is the core autoresearch principle — the scorer cannot be gamed.

2. **The Golden Rule still applies.** Every Gemini NB2 call MUST include 3 character anchor images as inline image data. This is enforced with `RuntimeError` in `generate_sheet_split.py`. Do not bypass it.

3. **No LoRA training.** LoRA was abandoned on April 8. Do not propose, reference, or build anything related to training LoRAs. Pre-made community LoRAs are only relevant in Phase 1 (ComfyUI), not Phase 0 (Gemini).

4. **Do not re-enable disabled agents.** Only 2 agents are active (vault-indexer, daily-driver morning). Do not create new Agent SDK agents or modify agent fleet configuration. The autoresearch runner is a standalone Python script, NOT an agent.

5. **Outline weight 1.** When running Pixel Quantizer checks, use `--outline-weight 1`. Weight 2 is too aggressive at 128×128.

6. **Sean is the test character.** All Phase 0 experiments use Sean (champion, 128×128). His anchor images are at `references/anchors/champions/Sean/`. His palette is `sean` (27 colors). Other characters use `sf2_pixel_art` palette (38 colors).

7. **Walk cycle references are FROZEN.** The three walk cycle reference images in `references/walk_cycle/` are part of the scoring pipeline. The runner must not modify, replace, or swap them.

8. **Green screen (#00FF00).** All generated sprites must have solid green backgrounds. This is non-negotiable for the pipeline.

9. **Hexagonal architecture.** Follow the existing adapter pattern (ports and adapters). The VLM scorer should be behind an interface so Qwen2.5-VL can be swapped for Gemini or another model later.

10. **Python, not TypeScript.** The autoresearch system is Python (matching the batch orchestrator and agents-sdk). The sprite pipeline is TypeScript, but the autoresearch layer sits on top and calls the Python generation code directly.
</rules>

---

<self_check>
## Post-Build Self-Check

After completing all tasks, verify:

- [ ] `prepare.py` has all 5 scoring tiers implemented (Tier 5 can be a stub)
- [ ] `prepare.py` does NOT import from or depend on `experiment.json` or `runner.py`
- [ ] `runner.py` implements the generate → score → keep/revert → log loop
- [ ] `runner.py` enforces budget cap, timeout, and rate limiting
- [ ] `runner.py` auto-reverts `experiment.json` when score decreases
- [ ] `experiment.json` contains the current baseline walk_forward config
- [ ] `program.md` contains the 5-round, 100-experiment research strategy
- [ ] VLM prompt includes all 6 walk cycle criteria with the 2D animation principles
- [ ] VLM prompt references Contact, Down, Passing, and Up poses explicitly
- [ ] Walk cycle reference images are loaded from `references/walk_cycle/` and composed side-by-side with generated output before sending to VLM
- [ ] Anchor images are loaded from `references/anchors/champions/Sean/`
- [ ] Graceful fallback if Alienware/Ollama is unreachable (skip VLM, log warning, return partial score)
- [ ] Graceful fallback if DINOv2 model can't be loaded (skip tier 2, log warning)
- [ ] Dry run mode works end-to-end without any API calls or GPU access
- [ ] No references to LoRA training as a planned or future activity
- [ ] No creation of new Agent SDK agents
- [ ] Results log to `autoresearch/results/` in both TSV and JSONL format
</self_check>
