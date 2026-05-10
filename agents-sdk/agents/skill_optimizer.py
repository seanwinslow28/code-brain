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


def score_outputs(
    structural_results: dict[str, list[dict[str, bool]]],
    judge_results: dict[str, list[dict[str, bool]]],
) -> dict:
    """Aggregate per-criterion scores.

    Returns {"total_passes": int, "max_score": int, "per_criterion": {id: pass_rate}, "binary_array": list[int]}.
    The binary_array is the flat list of all pass/fail outcomes for bootstrap CI.
    """
    binary_array: list[int] = []
    per_criterion_passes: dict[str, list[int]] = {}
    for prompt_id, results in structural_results.items():
        for r in results:
            for cid, passed in r.items():
                binary_array.append(1 if passed else 0)
                per_criterion_passes.setdefault(cid, []).append(1 if passed else 0)
    for prompt_id, results in judge_results.items():
        for r in results:
            for cid, passed in r.items():
                binary_array.append(1 if passed else 0)
                per_criterion_passes.setdefault(cid, []).append(1 if passed else 0)
    per_criterion = {cid: sum(vs) / len(vs) for cid, vs in per_criterion_passes.items()}
    return {
        "total_passes": sum(binary_array),
        "max_score": len(binary_array),
        "per_criterion": per_criterion,
        "binary_array": binary_array,
    }


def propose_mutation(
    optimizer_client,
    program_md: str,
    current_skill_md: str,
    recent_results: list[dict],
    worst_criteria: list[str],
    model: str = "claude-opus-4-7",
) -> tuple[str, str, str]:
    """Ask the optimizer subagent to propose ONE mutation.

    Returns (section_heading, rationale, modified_skill_md_full_text).
    Raises ValueError if the response is malformed.
    """
    user_msg = (
        f"## Current SKILL.md\n\n{current_skill_md}\n\n"
        f"## Recent results (last {len(recent_results)} iterations)\n\n"
        f"{json.dumps(recent_results, indent=2)}\n\n"
        f"## Worst-scoring criteria last iteration\n\n"
        f"{', '.join(worst_criteria)}\n\n"
        f"Propose ONE mutation. Respond with the JSON object specified in your instructions."
    )
    msg = optimizer_client.messages.create(
        model=model,
        max_tokens=8000,
        system=program_md,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = msg.content[0].text.strip()
    # Strip optional markdown fence.
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1].lstrip("json").strip()
    parsed = json.loads(raw)
    return parsed["section_heading"], parsed["rationale"], parsed["modified_skill_md_full_text"]


def git_commit_mutation(
    repo_root: Path,
    skill_md_path: Path,
    iteration: int,
    section: str,
    rationale: str,
    score_old: float,
    score_new: float,
) -> None:
    msg = (
        f"optimize(writing-voice-modes): {rationale}\n\n"
        f"Score: {score_old:.3f} → {score_new:.3f} (+{score_new-score_old:.3f})\n"
        f"Iteration: {iteration:02d}/25\n"
        f"Section mutated: {section}\n\n"
        f"🤖 Generated by skill_optimizer.py"
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "add", str(skill_md_path)],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo_root), "commit", "-m", msg],
        check=True, capture_output=True,
    )


def git_revert_skill_md(repo_root: Path, skill_md_path: Path) -> None:
    """Discard in-tree changes to the skill file."""
    subprocess.run(
        ["git", "-C", str(repo_root), "checkout", "--", str(skill_md_path)],
        check=True, capture_output=True,
    )
