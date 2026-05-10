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
