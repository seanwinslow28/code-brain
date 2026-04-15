# Claude Code Kickoff Prompt: Best-of-N Mode for Autoresearch Runner

**Date:** 2026-04-15
**Purpose:** Paste this into a Claude Code session on your MacBook Pro to add `--best-of N` mode to the autoresearch runner.
**Context:** Phase 0 autoresearch is complete (100 experiments, best score 0.8448). The winning config is locked in `best_experiment.json`. Baseline variance spans 0.615–0.834, so generating multiple sheets with the same config and keeping the best will reliably push to 0.83+.

---

## Prompt

```
I need you to add a `--best-of N` mode to `16bitfit-battle-mode/autoresearch/runner.py`. This is a "quick win" follow-up to Phase 0 of our autoresearch — we've already found the winning config, now we want to generate N sprite sheets per character using that locked config and keep only the highest-scoring one.

### What to build

Add a new async function `run_best_of_n()` alongside the existing `run_phase0()`. It should:

1. Load the winning config from `autoresearch/results/best_experiment.json` (the `"config"` key).
2. For the given character + animation, generate N sprite sheets using that LOCKED config (no mutations).
3. Score each one using the existing `AutoresearchScorer` from `prepare.py`.
4. Keep the highest-scoring sheet, delete the rest to save disk.
5. Save results to a new subdirectory: `results/best-of-N/{character}_{animation}/` with:
   - The winning sheet as `best_sheet.png`
   - The winning frames as `frame_00.png`, `frame_01.png`, etc.
   - A `result.json` with: character, animation, N, all scores, best score, best run index, timestamp
6. Print a summary: character, N runs, scores for each, best score, improvement over Phase 0 best.

### CLI changes

Add these args to the existing argparse:
- `--best-of N` (int, default 0 — 0 means disabled, use normal phase mode)
- When `--best-of` is set, `--phase` should still be required but the runner calls `run_best_of_n()` instead of `run_phase0()`.

### Important constraints

- Respect the existing `RATE_LIMIT_DELAY` (10s) between Gemini API calls.
- Respect `--budget` (default should be $0.35 for 5 runs, but let the user override).
- Respect `--dry-run` for testing.
- The `generate_sprite_sheet()` function already handles everything — call it with the locked config.
- DO NOT modify `prepare.py` — it's frozen by design.

### char_configs gap

The `char_configs` dict at line 534 of runner.py only has 3 entries (sean, aria, kenji). It needs all 12 characters. The anchor folders tell you the names and types:

Champions (128×128 tile): Sean, Aria, Kenji, Marcus, Mary, Zara
Bosses (256×256 tile): Gym Bully, Procrastination Phantom, Sloth Demon, Stress Titan, Training Dummy, Ultimate Slump

Anchor folder paths: `autoresearch/references/anchors/champions/{Name}/` and `autoresearch/references/anchors/bosses/{Name}/`

Character descriptions for the missing 9 (use these for the `description` field):
- Marcus: "Tall muscular build, dark skin, red headband, red boxing gloves, black shorts, black boots"
- Mary: "Petite build, red hair in ponytail, green crop top, white shorts, green sneakers"
- Zara: "Tall athletic build, dark skin, braided hair, yellow sports bra, black yoga pants, yellow sneakers"
- Gym Bully: "Massive muscular build, bald head, red tank top, camo shorts, heavy chains, black combat boots"
- Procrastination Phantom: "Ghostly translucent figure, hooded cloak, ethereal purple glow, floating, no visible feet"
- Sloth Demon: "Obese demonic figure, grey-green skin, horns, tattered brown cloth, clawed feet"
- Stress Titan: "Enormous rocky figure, cracked magma skin, glowing red veins, stone fists, lava dripping"
- Training Dummy: "Wooden practice dummy, circular head, cross-shaped body, spring base, red target circles"
- Ultimate Slump: "Amorphous dark mass, multiple shadowy tendrils, glowing red eyes, dripping black ooze"

The `char_configs` key for bosses should use snake_case (e.g., `gym_bully`, `procrastination_phantom`) to match CLI input.

### Expected usage after your changes

# Test with dry run first
python3 runner.py --phase 0 --character sean --animation walk_forward --best-of 5 --dry-run

# Single character
python3 runner.py --phase 0 --character sean --animation walk_forward --best-of 5 --budget 0.35

# All 12 characters (shell loop)
for char in sean aria kenji marcus mary zara gym_bully procrastination_phantom sloth_demon stress_titan training_dummy ultimate_slump; do
    python3 runner.py --phase 0 --character "$char" --animation walk_forward --best-of 5 --budget 0.35
done

### Files to read first
- `autoresearch/runner.py` — the main file you're modifying
- `autoresearch/results/best_experiment.json` — the winning config to lock
- `autoresearch/experiment.json` — current config structure reference
- `autoresearch/prepare.py` — DO NOT MODIFY, but read to understand AutoresearchScorer interface

### Testing
After making changes, run: python3 runner.py --phase 0 --character sean --animation walk_forward --best-of 3 --dry-run
This should complete without errors and show 3 mock scores.
```
