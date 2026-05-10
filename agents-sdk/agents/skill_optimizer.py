"""skill_optimizer.py — autoresearch optimization loop for writing-voice-modes.

See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SkillOptimizerConfig:
    branch: str
    repo_root: Path
    target_skill_md: Path
    evals_path: Path
    evals_sealed_path: Path
    stylometry_baseline_path: Path
    max_iterations: int = 25
    plateau_halt_iterations: int = 3
    runs_per_prompt: int = 15
    cost_cap_usd_hard: float = 200.0
    cost_cap_usd_soft: float = 50.0


def preflight_checks(config: SkillOptimizerConfig) -> tuple[bool, str]:
    """Verify all preconditions before starting the loop."""
    # 1. Correct branch
    # Use symbolic-ref so unborn branches (no commits yet) still resolve.
    try:
        result = subprocess.run(
            ["git", "-C", str(config.repo_root), "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        current_branch = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"git symbolic-ref failed: {e.stderr}"
    if current_branch != config.branch:
        return False, f"on branch {current_branch!r}, expected {config.branch!r}"

    # 2. Required files exist
    for p, name in [
        (config.target_skill_md, "SKILL.md"),
        (config.evals_path, "evals.yaml"),
        (config.evals_sealed_path, "evals.sealed.yaml"),
        (config.stylometry_baseline_path, "stylometry_baseline.json"),
    ]:
        if not p.exists():
            return False, f"missing required file: {name} at {p}"

    # 3. Stylometry threshold has been calibrated
    baseline = json.loads(config.stylometry_baseline_path.read_text())
    if baseline.get("_threshold") is None:
        return False, "stylometric threshold not yet calibrated (run calibrate_stylometry_threshold.py)"

    return True, "ok"


def generate_outputs(
    client,
    skill_md_text: str,
    prompts: list[dict],
    runs_per_prompt: int,
    model: str = "claude-opus-4-7",
    max_tokens: int = 600,
) -> dict[str, list[dict]]:
    """Run `runs_per_prompt` generations for each prompt; return outputs keyed by prompt id.

    Each output: {"text": str, "input_tokens": int, "output_tokens": int}
    The skill_md_text is loaded as a system prompt so the generation model behaves
    as if it had loaded the writing-voice-modes skill.
    """
    outputs: dict[str, list[dict]] = {}
    for prompt in prompts:
        outputs[prompt["id"]] = []
        for _ in range(runs_per_prompt):
            msg = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=skill_md_text,
                messages=[{"role": "user", "content": prompt["prompt"]}],
            )
            outputs[prompt["id"]].append({
                "text": msg.content[0].text,
                "input_tokens": msg.usage.input_tokens,
                "output_tokens": msg.usage.output_tokens,
            })
    return outputs
