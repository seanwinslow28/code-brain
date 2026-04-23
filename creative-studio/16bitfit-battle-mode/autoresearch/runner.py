"""Autoresearch Phase 0 Experiment Runner.

Implements the generate -> score -> keep/revert -> log loop for Gemini
NB2 prompt optimization of walk cycle sprite sheets.

Usage:
    # Phase 0 — Gemini prompt optimization
    python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 100 --budget 7.00

    # Dry run (no API calls, mock scores)
    python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 5 --dry-run

    # Resume from where we left off
    python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 100 --resume
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import json
import logging
import shutil
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

# ─── Path Setup ──────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent  # 16bitfit-battle-mode/
SUPERUSER_ROOT = REPO_ROOT.parent.parent  # claude-code-superuser-pack/ (post-v3.15.0 nested under creative-studio/)
PQ_DIR = REPO_ROOT / "pixel-quantizer"

sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(PQ_DIR))
sys.path.insert(0, str(PQ_DIR / "video-eval"))
sys.path.insert(0, str(SUPERUSER_ROOT / "agents-sdk"))  # lib/keychain.py lives here

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("autoresearch.runner")

# ─── Constants ───────────────────────────────────────────────────────

RESULTS_DIR = SCRIPT_DIR / "results"
EXPERIMENT_CONFIG = SCRIPT_DIR / "experiment.json"
PROGRAM_FILE = SCRIPT_DIR / "program.md"
COST_PER_EXPERIMENT = 0.07  # ~$0.07 per Gemini NB2 API call
RATE_LIMIT_DELAY = 10  # Seconds between Gemini API calls

# All 12 characters: 6 champions (128×128) + 6 bosses (256×256)
CHAR_CONFIGS = {
    # Champions
    "sean": {
        "name": "Sean",
        "description": "Muscular build, blonde hair, white tank top, blue pants, white shoes",
        "tile_size": 128,
    },
    "aria": {
        "name": "Aria",
        "description": "Athletic build, dark skin, purple sports bra, black leggings, white sneakers",
        "tile_size": 128,
    },
    "kenji": {
        "name": "Kenji",
        "description": "Lean build, black spiky hair, white karate gi, black belt, bare feet",
        "tile_size": 128,
    },
    "marcus": {
        "name": "Marcus",
        "description": "Tall muscular build, dark skin, red headband, red boxing gloves, black shorts, black boots",
        "tile_size": 128,
    },
    "mary": {
        "name": "Mary",
        "description": "Petite build, red hair in ponytail, green crop top, white shorts, green sneakers",
        "tile_size": 128,
    },
    "zara": {
        "name": "Zara",
        "description": "Tall athletic build, dark skin, braided hair, yellow sports bra, black yoga pants, yellow sneakers",
        "tile_size": 128,
    },
    # Bosses
    "gym_bully": {
        "name": "Gym Bully",
        "description": "Massive muscular build, bald head, red tank top, camo shorts, heavy chains, black combat boots",
        "tile_size": 256,
    },
    "procrastination_phantom": {
        "name": "Procrastination Phantom",
        "description": "Ghostly translucent figure, hooded cloak, ethereal purple glow, floating, no visible feet",
        "tile_size": 256,
    },
    "sloth_demon": {
        "name": "Sloth Demon",
        "description": "Obese demonic figure, grey-green skin, horns, tattered brown cloth, clawed feet",
        "tile_size": 256,
    },
    "stress_titan": {
        "name": "Stress Titan",
        "description": "Enormous rocky figure, cracked magma skin, glowing red veins, stone fists, lava dripping",
        "tile_size": 256,
    },
    "training_dummy": {
        "name": "Training Dummy",
        "description": "Wooden practice dummy, circular head, cross-shaped body, spring base, red target circles",
        "tile_size": 256,
    },
    "ultimate_slump": {
        "name": "Ultimate Slump",
        "description": "Amorphous dark mass, multiple shadowy tendrils, glowing red eyes, dripping black ooze",
        "tile_size": 256,
    },
}


# ─── Experiment Config Manager ───────────────────────────────────────

class ExperimentConfig:
    """Manages the mutable experiment.json."""

    def __init__(self, path: Path = EXPERIMENT_CONFIG):
        self.path = path
        self.config = self._load()
        self._backup: dict | None = None

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        raise FileNotFoundError(f"experiment.json not found at {self.path}")

    def save(self) -> None:
        self.path.write_text(json.dumps(self.config, indent=2) + "\n")

    def backup(self) -> None:
        """Save current state for revert."""
        self._backup = copy.deepcopy(self.config)

    def revert(self) -> None:
        """Revert to last backup."""
        if self._backup:
            self.config = copy.deepcopy(self._backup)
            self.save()
            logger.info("Reverted experiment.json to previous state")

    def mutate(self, changes: dict) -> list[str]:
        """Apply changes to the generation config. Returns list of changed keys."""
        changed = []
        gen = self.config.get("generation", {})
        for key, value in changes.items():
            if key in gen and gen[key] != value:
                gen[key] = value
                changed.append(key)
            elif key not in gen:
                gen[key] = value
                changed.append(key)
        self.config["generation"] = gen
        self.config["version"] = self.config.get("version", 0) + 1
        return changed

    @property
    def prompt_template(self) -> str:
        return self.config.get("generation", {}).get("prompt_template", "")

    @property
    def generation(self) -> dict:
        return self.config.get("generation", {})


# ─── Results Logger ──────────────────────────────────────────────────

class ResultsLogger:
    """Logs experiment results to TSV and JSONL."""

    def __init__(self, results_dir: Path = RESULTS_DIR):
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.tsv_path = results_dir / "results.tsv"
        self.jsonl_path = results_dir / "experiment_log.jsonl"
        self.best_path = results_dir / "best_experiment.json"
        self.summary_path = results_dir / "summary.md"

        # Write TSV header if new file
        if not self.tsv_path.exists():
            self.tsv_path.write_text(
                "experiment_id\tround\tparams_changed\tcomposite_score\t"
                "vlm_walk_score\tdino_identity\thard_gates_pass\t"
                "cost_usd\tgeneration_time_s\ttimestamp\n"
            )

    def log_experiment(
        self,
        experiment_id: int,
        round_num: int,
        params_changed: list[str],
        score_result,
        config_snapshot: dict,
        generation_time: float,
        cost: float,
    ) -> None:
        """Log to both TSV and JSONL."""
        # TSV
        vlm_walk = self._extract_vlm_walk(score_result.vlm_scores)
        hard_pass = all(score_result.hard_gates.values()) if score_result.hard_gates else False
        tsv_line = (
            f"{experiment_id}\t{round_num}\t"
            f"{'|'.join(params_changed) if params_changed else 'baseline'}\t"
            f"{score_result.composite:.4f}\t"
            f"{vlm_walk:.4f}\t"
            f"{score_result.dino_identity:.4f}\t"
            f"{hard_pass}\t"
            f"{cost:.4f}\t"
            f"{generation_time:.1f}\t"
            f"{score_result.timestamp:.0f}\n"
        )
        with open(self.tsv_path, "a") as f:
            f.write(tsv_line)

        # JSONL
        entry = {
            "experiment_id": experiment_id,
            "round": round_num,
            "params_changed": params_changed,
            "scores": {
                "composite": score_result.composite,
                "dino_identity": score_result.dino_identity,
                "hard_gates": score_result.hard_gates,
                "deterministic": score_result.deterministic,
                "vlm_scores": score_result.vlm_scores,
                "primary_issue": score_result.primary_issue,
                "suggested_fix": score_result.suggested_fix,
                "tier_reached": score_result.tier_reached,
            },
            "config": config_snapshot,
            "cost_usd": cost,
            "generation_time_s": generation_time,
            "timestamp": score_result.timestamp,
        }
        with open(self.jsonl_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def save_best(self, config: dict, score: float) -> None:
        """Save the best experiment config."""
        self.best_path.write_text(json.dumps(
            {"best_score": score, "config": config},
            indent=2,
        ) + "\n")

    def write_summary(self, experiments: list[dict]) -> None:
        """Write end-of-run summary."""
        if not experiments:
            return

        scores = [e["composite"] for e in experiments]
        best = max(experiments, key=lambda e: e["composite"])
        worst = min(experiments, key=lambda e: e["composite"])

        summary = f"""# Autoresearch Run Summary

**Date:** {time.strftime('%Y-%m-%d %H:%M')}
**Total experiments:** {len(experiments)}
**Total cost:** ${sum(e.get('cost', COST_PER_EXPERIMENT) for e in experiments):.2f}

## Scores
- **Best:** {max(scores):.4f} (experiment {best['id']})
- **Worst:** {min(scores):.4f} (experiment {worst['id']})
- **Mean:** {sum(scores) / len(scores):.4f}
- **Median:** {sorted(scores)[len(scores) // 2]:.4f}

## Best Configuration
```json
{json.dumps(best.get('config', {}), indent=2)}
```

## Top Findings
"""
        # Top 5 experiments
        top = sorted(experiments, key=lambda e: e["composite"], reverse=True)[:5]
        for i, exp in enumerate(top, 1):
            summary += f"{i}. Experiment {exp['id']} — score {exp['composite']:.4f}"
            if exp.get("params_changed"):
                summary += f" (changed: {', '.join(exp['params_changed'])})"
            summary += "\n"

        self.summary_path.write_text(summary)
        logger.info("Summary written to %s", self.summary_path)

    def _extract_vlm_walk(self, vlm_scores: dict) -> float:
        """Extract VLM walk composite score."""
        if not vlm_scores:
            return 0.0
        if "composite_score" in vlm_scores:
            return vlm_scores["composite_score"]
        return 0.0


# ─── Experiment Mutations (Phase 0 Strategies) ──────────────────────

def get_round_mutations(round_num: int, experiment_in_round: int, base_config: dict) -> dict:
    """Generate mutation for a specific experiment within a round.

    Phase 0 experiments are structured, not random. Each round tests
    a specific hypothesis about what improves walk cycle quality.
    """
    gen = base_config.get("generation", {})

    # Round 1: Prompt Structure (experiments 1-20)
    if round_num == 1:
        mutations = _round1_prompt_structure(experiment_in_round, gen)

    # Round 2: Reference Strategy (experiments 21-40)
    elif round_num == 2:
        mutations = _round2_reference_strategy(experiment_in_round, gen)

    # Round 3: Sheet Layout (experiments 41-60)
    elif round_num == 3:
        mutations = _round3_sheet_layout(experiment_in_round, gen)

    # Round 4: Negative Prompts + Constraints (experiments 61-80)
    elif round_num == 4:
        mutations = _round4_constraints(experiment_in_round, gen)

    # Round 5: Fine-Tuning (experiments 81-100)
    elif round_num == 5:
        mutations = _round5_fine_tuning(experiment_in_round, gen)

    else:
        mutations = {}

    return mutations


def _round1_prompt_structure(exp: int, gen: dict) -> dict:
    """Prompt structure experiments."""
    base_template = gen.get("prompt_template", "")

    if exp == 0:
        return {}  # Baseline — no changes

    if exp == 1:
        return {"include_pose_names": True}

    if exp == 2:
        return {
            "include_pose_names": True,
            "additional_constraints": [
                "Frame 1: CONTACT pose — right heel strikes ground, left leg trails behind, arms at maximum spread",
                "Frame 2: DOWN pose — body at lowest point, front knee bends absorbing weight",
                "Frame 3: PASSING pose — legs together, rear leg swings past planted leg",
                "Frame 4: UP pose — body at highest point, rear leg pushes off",
            ],
        }

    if exp == 3:
        return {"include_animation_principles": True}

    if exp == 4:
        return {
            "include_animation_principles": True,
            "additional_constraints": [
                "Each frame must show a DISTINCTLY DIFFERENT leg position",
            ],
        }

    if exp == 5:
        return {
            "include_pose_names": True,
            "include_animation_principles": True,
        }

    if exp == 6:
        return {
            "additional_constraints": [
                "walk cycle", "contact pose", "passing position",
                "weight transfer", "push-off",
            ],
        }

    if exp == 7:
        return {
            "include_pose_names": True,
            "additional_constraints": [
                "The legs MUST be in visibly different positions in every single frame",
                "No two frames should have identical leg positions",
            ],
        }

    if exp == 8:
        return {
            "include_pose_names": True,
            "include_animation_principles": True,
            "additional_constraints": [
                "Frame 1: CONTACT — front heel strikes ground, rear leg trails, legs at WIDEST spread",
                "Frame 2: PASSING — legs together, one leg swings past the other",
                "Frame 3: CONTACT — opposite leg now forward, legs at WIDEST spread",
                "Frame 4: PASSING — legs together again, opposite leg swinging past",
            ],
        }

    # Experiments 9-19: variations and combinations
    variations = [
        {"additional_constraints": ["Show 4 distinct walking poses: Contact, Down, Passing, Up"]},
        {"additional_constraints": ["Animate a walk cycle with clear weight shifting between frames"]},
        {"additional_constraints": ["Each frame must show progressively different body positions"]},
        {"include_pose_names": True, "additional_constraints": ["Arms swing OPPOSITE to legs"]},
        {"include_pose_names": True, "additional_constraints": ["Body dips DOWN at frame 2, rises UP at frame 4"]},
        {"additional_constraints": ["Classic 16-bit arcade walk animation with exaggerated leg movement"]},
        {"include_pose_names": True, "include_animation_principles": True,
         "additional_constraints": ["CRITICAL: Every frame must have a COMPLETELY DIFFERENT leg position"]},
        {"additional_constraints": ["Animate like Street Fighter 2: bold poses, clear silhouettes, readable at 128px"]},
        {"include_walk_cycle_reference": True},
        {"include_walk_cycle_reference": True, "include_pose_names": True},
        {"include_walk_cycle_reference": True, "include_animation_principles": True},
    ]
    idx = exp - 9
    if 0 <= idx < len(variations):
        return variations[idx]

    return {}


def _round2_reference_strategy(exp: int, gen: dict) -> dict:
    """Reference strategy experiments."""
    strategies = [
        {"reference_strategy": "1_anchor"},
        {"reference_strategy": "2_anchors"},
        {"reference_strategy": "3_anchors"},  # Current default
        {"reference_strategy": "3_anchors", "include_walk_cycle_reference": True},
        {"reference_strategy": "3_anchors", "include_walk_cycle_reference": True, "include_pose_names": True},
        {"reference_strategy": "2_anchors", "include_walk_cycle_reference": True},
        {"reference_strategy": "1_anchor", "include_walk_cycle_reference": True},
        {"reference_strategy": "3_anchors_plus_style"},
        {"reference_strategy": "3_anchors_plus_style", "include_pose_names": True},
        {"reference_strategy": "3_anchors", "include_walk_cycle_reference": True,
         "include_animation_principles": True},
    ]
    # Repeat last 10 with slight variations
    extended = strategies + [
        {**s, "additional_constraints": ["Legs must show distinctly different positions"]}
        for s in strategies
    ]

    if 0 <= exp < len(extended):
        return extended[exp]
    return {}


def _round3_sheet_layout(exp: int, gen: dict) -> dict:
    """Sheet layout experiments."""
    layouts = [
        {"sheet_layout": "full_sheet", "frame_count": 4},
        {"sheet_layout": "full_sheet", "frame_count": 6},
        {"sheet_layout": "full_sheet", "frame_count": 8},
        {"sheet_layout": "2_frame_pairs", "frame_count": 4},
        {"sheet_layout": "2_frame_pairs", "frame_count": 6},
        {"sheet_layout": "individual_frames", "frame_count": 4},
        {"sheet_layout": "individual_frames", "frame_count": 6},
        {"sheet_layout": "keyframes_only", "frame_count": 4},
        {"sheet_layout": "keyframes_only", "frame_count": 6},
        {"sheet_layout": "keyframes_only", "frame_count": 8},
    ]
    # With best prompt findings
    extended = layouts + [
        {**l, "include_pose_names": True, "include_animation_principles": True}
        for l in layouts
    ]

    if 0 <= exp < len(extended):
        return extended[exp]
    return {}


def _round4_constraints(exp: int, gen: dict) -> dict:
    """Negative prompt and constraint experiments."""
    constraints_list = [
        {"additional_constraints": ["legs must be in different positions in every frame"]},
        {"additional_constraints": ["no repeated poses"]},
        {"additional_constraints": ["body lowest at frame 2, highest at frame 4"]},
        {"additional_constraints": [
            "legs must be in different positions in every frame",
            "no repeated poses",
        ]},
        {"additional_constraints": [
            "body lowest at frame 2, highest at frame 4",
            "legs must be in different positions in every frame",
        ]},
        {"additional_constraints": ["exactly ONE character per cell", "no text or labels"]},
        {"additional_constraints": [
            "no repeated poses", "exactly ONE character per cell",
            "each frame shows a DIFFERENT walking phase",
        ]},
        {"additional_constraints": [
            "4 distinct walk cycle phases: heel strike, weight drop, leg pass, push up",
        ]},
    ]
    # Combine with best from previous rounds
    extended = constraints_list + [
        {**c, "include_pose_names": True, "include_animation_principles": True}
        for c in constraints_list
    ] + [
        {**c, "include_walk_cycle_reference": True}
        for c in constraints_list[:4]
    ]

    if 0 <= exp < len(extended):
        return extended[exp]
    return {}


def _round5_fine_tuning(exp: int, gen: dict) -> dict:
    """Fine-tuning experiments — small variations on best config."""
    # These will be dynamically adjusted based on best_experiment.json
    # For now, provide structural variations
    if exp == 0:
        return {}  # Re-run best config for stability check

    fine_tune = [
        {"frame_count": 4},
        {"frame_count": 6},
        {"frame_count": 8},
        # Test on walk_backward (if walk_forward improves)
        {},  # Will be customized at runtime
        {},
        {},
        {},
        {},
        {},
        {},
    ]

    # Variations 10-19: combine best findings with character generalization
    generalization = [
        {},  # Try on Aria
        {},  # Try on Kenji
        {},  # Stability re-run 1
        {},  # Stability re-run 2
        {},  # Stability re-run 3
        {},  # Max constraints combo
        {},  # Minimal constraints (ablation)
        {},  # No animation principles (ablation)
        {},  # No pose names (ablation)
        {},  # No walk reference (ablation)
    ]

    all_mutations = fine_tune + generalization
    if 0 <= exp < len(all_mutations):
        return all_mutations[exp]
    return {}


# ─── Generation Engine ──────────────────────────────────────────────

async def generate_sprite_sheet(
    config: dict,
    character: str,
    animation_type: str,
    output_dir: Path,
    dry_run: bool = False,
) -> tuple[Path | None, list[Path]]:
    """Generate a sprite sheet and split into frames.

    Returns:
        (sheet_path, frame_paths) or (None, []) on failure.
    """
    if dry_run:
        return _generate_dry_run(output_dir)

    from batch.generate_sheet_split import (
        build_sheet_prompt,
        call_gemini,
        detect_grid,
        get_grid_layout,
        load_anchors,
        split_sheet,
    )
    from prompts.prompt_library import (
        FACING,
        GREEN_SCREEN,
        NEGATIVE_PROMPT,
        STYLE_TOKENS,
        PromptLibrary,
    )

    gen = config.get("generation", {})
    prompt_lib = PromptLibrary()
    template = prompt_lib.get_template(animation_type)
    if not template:
        logger.error("Unknown animation type: %s", animation_type)
        return None, []

    # Character config
    char_config = CHAR_CONFIGS.get(character.lower(), CHAR_CONFIGS["sean"])

    # Get frame count from config (may be mutated)
    frame_count = gen.get("frame_count", len(template.keyframe_indices) or template.frame_count)
    frame_poses = template.frame_poses[:frame_count]
    if len(frame_poses) < frame_count:
        frame_poses = frame_poses + frame_poses[:frame_count - len(frame_poses)]

    cols, rows = get_grid_layout(frame_count)

    # Build prompt with experiment mutations
    base_prompt = build_sheet_prompt(animation_type, char_config, frame_poses, cols, rows)

    # Apply experiment config modifications
    extra_lines = []
    if gen.get("include_pose_names"):
        extra_lines.append(
            "Each frame shows a specific walk cycle phase: "
            "CONTACT (heel strike), DOWN (lowest point), PASSING (legs cross), UP (highest point)."
        )
    if gen.get("include_animation_principles"):
        extra_lines.append(
            "Follow 2D animation walk cycle principles: distinct leg positions in every frame, "
            "body dips at the DOWN pose, rises at the UP pose, arms swing opposite to legs."
        )
    for constraint in gen.get("additional_constraints", []):
        extra_lines.append(constraint)

    if extra_lines:
        base_prompt += "\n\nADDITIONAL REQUIREMENTS:\n" + "\n".join(f"- {l}" for l in extra_lines)

    # Load anchors (Golden Rule: always 3)
    references_dir = SCRIPT_DIR / "references"
    anchor_dir = references_dir / "anchors"

    # Find character anchor directory
    anchor_paths = []
    for category in ["champions", "bosses"]:
        char_dir = anchor_dir / category / char_config["name"]
        if char_dir.exists():
            anchor_paths = sorted([
                str(p) for p in char_dir.glob("*.png") if "anchor" in p.name.lower()
            ])[:3]
            break

    if not anchor_paths:
        logger.error("No anchors found for %s — cannot generate (Golden Rule)", character)
        return None, []

    # Determine how many anchors to send based on reference_strategy
    ref_strategy = gen.get("reference_strategy", "3_anchors")
    if ref_strategy == "1_anchor":
        anchor_paths = anchor_paths[:1]
    elif ref_strategy == "2_anchors":
        anchor_paths = anchor_paths[:2]
    # "3_anchors" and "3_anchors_plus_style" use all 3

    anchor_parts = load_anchors(anchor_paths)
    if len(anchor_parts) < 1:
        logger.error("Failed to load any anchors")
        return None, []

    # Add walk cycle reference image if requested
    if gen.get("include_walk_cycle_reference"):
        walk_ref_dir = references_dir / "walk_cycle"
        walk_refs = sorted(walk_ref_dir.glob("*.png")) if walk_ref_dir.exists() else []
        if walk_refs:
            import base64
            ref_data = walk_refs[0].read_bytes()
            ref_b64 = base64.b64encode(ref_data).decode()
            anchor_parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
            base_prompt += (
                "\n\nREFERENCE WALK CYCLE: The additional reference image shows a real arcade game "
                "walk cycle. Match the leg differentiation and pose progression quality shown."
            )

    # Add style reference if requested
    if ref_strategy == "3_anchors_plus_style":
        style_dir = references_dir / "style_standard"
        style_refs = sorted(style_dir.glob("*.png")) if style_dir.exists() else []
        if style_refs:
            import base64
            style_data = style_refs[0].read_bytes()
            style_b64 = base64.b64encode(style_data).decode()
            anchor_parts.append({"inlineData": {"mimeType": "image/png", "data": style_b64}})

    # Get API key
    try:
        from lib.keychain import get_credential
        api_key = get_credential("google-ai-key")
    except Exception:
        import os
        api_key = os.environ.get("GOOGLE_AI_KEY", "")

    if not api_key:
        logger.error("No Gemini API key found")
        return None, []

    # Generate
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        image_data = await call_gemini(anchor_parts, base_prompt, api_key)
    except Exception as e:
        logger.error("Gemini generation failed: %s", e)
        return None, []

    # Save sheet
    sheet_path = output_dir / "experiment_sheet.png"
    sheet_path.write_bytes(image_data)

    # Detect grid and split
    try:
        detected_cols, detected_rows = detect_grid(image_data, frame_count)
        frames_data = split_sheet(image_data, detected_cols, detected_rows, frame_count)
    except Exception as e:
        logger.error("Grid detection/splitting failed: %s", e)
        return sheet_path, []

    # Save individual frames
    frame_paths = []
    for i, frame_data in enumerate(frames_data):
        frame_path = output_dir / f"frame_{i:02d}.png"
        frame_path.write_bytes(frame_data)
        frame_paths.append(frame_path)

    return sheet_path, frame_paths


def _generate_dry_run(output_dir: Path) -> tuple[Path, list[Path]]:
    """Generate placeholder files for dry run."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a minimal green 128x128 PNG for each frame
    from PIL import Image

    sheet = Image.new("RGBA", (256, 256), (0, 255, 0, 255))
    # Draw a simple "character" rectangle in center of each quadrant
    for qx, qy in [(32, 32), (160, 32), (32, 160), (160, 160)]:
        for x in range(qx, qx + 64):
            for y in range(qy, qy + 64):
                if 10 < x - qx < 54 and 10 < y - qy < 54:
                    sheet.putpixel((x, y), (200, 160, 120, 255))

    sheet_path = output_dir / "experiment_sheet.png"
    sheet.save(sheet_path)

    frame_paths = []
    for i in range(4):
        frame = Image.new("RGBA", (128, 128), (0, 255, 0, 255))
        # Simple character silhouette
        for x in range(30, 98):
            for y in range(20, 108):
                frame.putpixel((x, y), (200, 160, 120, 255))
        frame_path = output_dir / f"frame_{i:02d}.png"
        frame.save(frame_path)
        frame_paths.append(frame_path)

    return sheet_path, frame_paths


# ─── Git Integration ─────────────────────────────────────────────────

def git_commit_improvement(old_score: float, new_score: float, params_changed: list[str]) -> None:
    """Auto-commit experiment.json when score improves."""
    try:
        param_str = ", ".join(params_changed) if params_changed else "baseline"
        message = f"autoresearch: score {old_score:.4f} -> {new_score:.4f} ({param_str})"
        subprocess.run(
            ["git", "add", str(EXPERIMENT_CONFIG)],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=REPO_ROOT,
            capture_output=True,
        )
        logger.info("Git commit: %s", message)
    except Exception as e:
        logger.warning("Git commit failed: %s", e)


# ─── Main Runner ─────────────────────────────────────────────────────

async def run_phase0(
    character: str,
    animation_type: str,
    max_experiments: int,
    budget: float,
    timeout_hours: float,
    dry_run: bool,
    resume: bool,
) -> None:
    """Execute the Phase 0 experiment loop."""
    from autoresearch.prepare import AutoresearchScorer

    print(f"\n{'=' * 60}")
    print(f"AUTORESEARCH Phase 0 — {character} / {animation_type}")
    print(f"Max experiments: {max_experiments} | Budget: ${budget:.2f} | Dry run: {dry_run}")
    print(f"{'=' * 60}\n")

    # Initialize
    config = ExperimentConfig()
    results_logger = ResultsLogger()
    scorer = AutoresearchScorer(
        character=character,
        animation_type=animation_type,
        skip_dino=config.config.get("scoring", {}).get("skip_dino", False),
        skip_vlm=config.config.get("scoring", {}).get("skip_vlm", False) or dry_run,
        alienware_host=config.config.get("scoring", {}).get("alienware_host", "192.168.68.201"),
        vlm_timeout=config.config.get("scoring", {}).get("vlm_timeout_s", 30),
    )

    # Determine starting experiment
    start_experiment = 0
    if resume and results_logger.jsonl_path.exists():
        lines = results_logger.jsonl_path.read_text().strip().split("\n")
        start_experiment = len(lines)
        logger.info("Resuming from experiment %d", start_experiment)

    # Track state
    best_score = 0.0
    best_config: dict = {}
    cumulative_cost = 0.0
    start_time = time.time()
    all_experiments: list[dict] = []

    for exp_id in range(start_experiment, max_experiments):
        # Safety checks
        elapsed_hours = (time.time() - start_time) / 3600
        if elapsed_hours >= timeout_hours:
            logger.info("Timeout reached (%.1fh) — stopping", elapsed_hours)
            break

        if cumulative_cost >= budget:
            logger.info("Budget exhausted ($%.2f / $%.2f) — stopping", cumulative_cost, budget)
            break

        # Determine round and experiment within round
        round_num = (exp_id // 20) + 1
        exp_in_round = exp_id % 20

        print(f"\n{'─' * 40}")
        print(f"Experiment {exp_id + 1}/{max_experiments} | Round {round_num} | Exp in round: {exp_in_round + 1}")

        # Backup current config before mutation
        config.backup()

        # Get and apply mutations
        mutations = get_round_mutations(round_num, exp_in_round, config.config)
        params_changed = config.mutate(mutations) if mutations else []
        config.save()

        if params_changed:
            print(f"  Changed: {', '.join(params_changed)}")
        else:
            print(f"  Baseline run (no changes)")

        # Generate sprite sheet
        exp_output_dir = RESULTS_DIR / f"experiment_{exp_id:04d}"
        gen_start = time.time()

        if dry_run:
            sheet_path, frame_paths = _generate_dry_run(exp_output_dir)
        else:
            sheet_path, frame_paths = await generate_sprite_sheet(
                config.config, character, animation_type, exp_output_dir, dry_run=False,
            )

        gen_time = time.time() - gen_start
        cost = COST_PER_EXPERIMENT if not dry_run else 0.0
        cumulative_cost += cost

        # Score
        if dry_run:
            score_result = scorer.score_dry_run()
        elif sheet_path and frame_paths:
            score_result = scorer.score_sheet(sheet_path, frame_paths)
        else:
            logger.warning("Generation failed — scoring as 0")
            score_result = scorer.score_dry_run()
            score_result.composite = 0.0

        print(f"  Score: {score_result.composite:.4f} (tier {score_result.tier_reached})")
        print(f"  DINOv2: {score_result.dino_identity:.4f} | Issue: {score_result.primary_issue}")

        # Log
        config_snapshot = copy.deepcopy(config.config)
        results_logger.log_experiment(
            experiment_id=exp_id,
            round_num=round_num,
            params_changed=params_changed,
            score_result=score_result,
            config_snapshot=config_snapshot,
            generation_time=gen_time,
            cost=cost,
        )

        all_experiments.append({
            "id": exp_id,
            "composite": score_result.composite,
            "config": config_snapshot,
            "params_changed": params_changed,
            "cost": cost,
        })

        # Keep or revert
        if score_result.composite > best_score:
            print(f"  NEW BEST: {best_score:.4f} -> {score_result.composite:.4f}")
            old_score = best_score
            best_score = score_result.composite
            best_config = copy.deepcopy(config.config)
            results_logger.save_best(best_config, best_score)
            if not dry_run:
                git_commit_improvement(old_score, best_score, params_changed)
        else:
            config.revert()
            if not dry_run:
                # Clean up experiment output to save disk
                shutil.rmtree(exp_output_dir, ignore_errors=True)

        # Rate limit
        if not dry_run and exp_id < max_experiments - 1:
            print(f"  Waiting {RATE_LIMIT_DELAY}s (rate limit)...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

    # Summary
    results_logger.write_summary(all_experiments)

    print(f"\n{'=' * 60}")
    print("AUTORESEARCH COMPLETE")
    print(f"  Experiments: {len(all_experiments)}")
    print(f"  Best score: {best_score:.4f}")
    print(f"  Total cost: ${cumulative_cost:.2f}")
    print(f"  Runtime: {(time.time() - start_time) / 60:.1f} minutes")
    print(f"  Results: {RESULTS_DIR}/")
    print(f"{'=' * 60}")


# ─── Best-of-N Runner ──────────────────────────────────────────────

async def run_best_of_n(
    character: str,
    animation_type: str,
    n: int,
    budget: float,
    dry_run: bool,
) -> None:
    """Generate N sprite sheets with the locked winning config, keep the best."""
    from autoresearch.prepare import AutoresearchScorer

    # Load winning config
    best_experiment_path = RESULTS_DIR / "best_experiment.json"
    if not best_experiment_path.exists():
        print("ERROR: results/best_experiment.json not found. Run Phase 0 first.")
        sys.exit(1)

    best_data = json.loads(best_experiment_path.read_text())
    locked_config = best_data["config"]
    phase0_best_score = best_data["best_score"]

    print(f"\n{'=' * 60}")
    print(f"BEST-OF-{n} — {character} / {animation_type}")
    print(f"Phase 0 best score: {phase0_best_score:.4f} | Budget: ${budget:.2f} | Dry run: {dry_run}")
    print(f"{'=' * 60}\n")

    # Budget check
    estimated_cost = n * COST_PER_EXPERIMENT
    if not dry_run and estimated_cost > budget + 0.001:
        print(f"ERROR: {n} runs would cost ~${estimated_cost:.2f}, exceeding budget ${budget:.2f}")
        sys.exit(1)

    # Initialize scorer
    scoring_cfg = locked_config.get("scoring", {})
    scorer = AutoresearchScorer(
        character=character,
        animation_type=animation_type,
        skip_dino=scoring_cfg.get("skip_dino", False),
        skip_vlm=scoring_cfg.get("skip_vlm", False) or dry_run,
        alienware_host=scoring_cfg.get("alienware_host", "192.168.68.201"),
        vlm_timeout=scoring_cfg.get("vlm_timeout_s", 30),
    )

    # Output directory
    output_base = RESULTS_DIR / "best-of-N" / f"{character}_{animation_type}"
    output_base.mkdir(parents=True, exist_ok=True)

    # Generate and score N sheets
    scores: list[float] = []
    run_dirs: list[Path] = []
    cumulative_cost = 0.0
    start_time = time.time()

    for run_idx in range(n):
        print(f"\n{'─' * 40}")
        print(f"Run {run_idx + 1}/{n}")

        run_dir = output_base / f"run_{run_idx:02d}"

        if dry_run:
            sheet_path, frame_paths = _generate_dry_run(run_dir)
            score_result = scorer.score_dry_run()
            cost = 0.0
        else:
            sheet_path, frame_paths = await generate_sprite_sheet(
                locked_config, character, animation_type, run_dir, dry_run=False,
            )
            cost = COST_PER_EXPERIMENT
            cumulative_cost += cost

            if cumulative_cost > budget:
                print(f"  Budget exceeded (${cumulative_cost:.2f} / ${budget:.2f}) — stopping early")
                break

            if sheet_path and frame_paths:
                score_result = scorer.score_sheet(sheet_path, frame_paths)
            else:
                logger.warning("Generation failed for run %d — scoring as 0", run_idx)
                score_result = scorer.score_dry_run()
                score_result.composite = 0.0

        scores.append(score_result.composite)
        run_dirs.append(run_dir)
        print(f"  Score: {score_result.composite:.4f} (tier {score_result.tier_reached})")

        # Rate limit between runs
        if not dry_run and run_idx < n - 1:
            print(f"  Waiting {RATE_LIMIT_DELAY}s (rate limit)...")
            await asyncio.sleep(RATE_LIMIT_DELAY)

    if not scores:
        print("ERROR: No runs completed.")
        return

    # Find the best run
    best_idx = int(max(range(len(scores)), key=lambda i: scores[i]))
    best_score = scores[best_idx]
    best_run_dir = run_dirs[best_idx]

    # Copy best run artifacts to the output directory
    best_sheet_src = best_run_dir / "experiment_sheet.png"
    if best_sheet_src.exists():
        shutil.copy2(best_sheet_src, output_base / "best_sheet.png")

    # Copy best frames
    for frame_src in sorted(best_run_dir.glob("frame_*.png")):
        shutil.copy2(frame_src, output_base / frame_src.name)

    # Delete non-winning run directories to save disk
    for idx, run_dir in enumerate(run_dirs):
        if idx != best_idx and run_dir.exists():
            shutil.rmtree(run_dir, ignore_errors=True)
    # Also clean up the winning run dir (artifacts are already copied)
    if best_run_dir.exists():
        shutil.rmtree(best_run_dir, ignore_errors=True)

    # Save result.json
    result = {
        "character": character,
        "animation": animation_type,
        "n": n,
        "scores": scores,
        "best_score": best_score,
        "best_run_index": best_idx,
        "phase0_best_score": phase0_best_score,
        "improvement": round(best_score - phase0_best_score, 4),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "cost_usd": round(cumulative_cost, 4),
    }
    (output_base / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"BEST-OF-{n} COMPLETE — {character} / {animation_type}")
    print(f"  Runs completed: {len(scores)}")
    print(f"  Scores: {', '.join(f'{s:.4f}' for s in scores)}")
    print(f"  Best score: {best_score:.4f} (run {best_idx + 1})")
    print(f"  Phase 0 best: {phase0_best_score:.4f}")
    improvement = best_score - phase0_best_score
    sign = "+" if improvement >= 0 else ""
    print(f"  Improvement: {sign}{improvement:.4f}")
    print(f"  Total cost: ${cumulative_cost:.2f}")
    print(f"  Runtime: {(time.time() - start_time) / 60:.1f} minutes")
    print(f"  Output: {output_base}/")
    print(f"{'=' * 60}")


# ─── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Autoresearch experiment runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 100
  python3 runner.py --phase 0 --character sean --animation walk_forward --max-experiments 5 --dry-run
  python3 runner.py --phase 0 --character sean --animation walk_forward --resume
  python3 runner.py --phase 0 --character sean --animation walk_forward --best-of 5 --budget 0.35
        """,
    )
    parser.add_argument("--phase", type=int, required=True, choices=[0, 1], help="Phase (0=Gemini, 1=ComfyUI)")
    parser.add_argument("--character", required=True, help="Character name (e.g. sean, gym_bully)")
    parser.add_argument("--animation", required=True, help="Animation type (e.g. walk_forward)")
    parser.add_argument("--max-experiments", type=int, default=100, help="Maximum experiments (default: 100)")
    parser.add_argument("--budget", type=float, default=7.00, help="Budget cap in USD (default: $7.00)")
    parser.add_argument("--timeout-hours", type=float, default=2.0, help="Max runtime in hours (default: 2.0)")
    parser.add_argument("--dry-run", action="store_true", help="No API calls, mock scores")
    parser.add_argument("--resume", action="store_true", help="Resume from last experiment")
    parser.add_argument("--best-of", type=int, default=0, dest="best_of",
                        help="Generate N sheets with locked config, keep best (0=disabled)")
    args = parser.parse_args()

    if args.phase == 1:
        print("Phase 1 (ComfyUI) is not yet implemented. Use --phase 0.")
        sys.exit(1)

    if args.best_of > 0:
        asyncio.run(run_best_of_n(
            character=args.character,
            animation_type=args.animation,
            n=args.best_of,
            budget=args.budget,
            dry_run=args.dry_run,
        ))
        return

    asyncio.run(run_phase0(
        character=args.character,
        animation_type=args.animation,
        max_experiments=args.max_experiments,
        budget=args.budget,
        timeout_hours=args.timeout_hours,
        dry_run=args.dry_run,
        resume=args.resume,
    ))


if __name__ == "__main__":
    main()
