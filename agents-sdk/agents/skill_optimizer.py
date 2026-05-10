"""skill_optimizer.py — autoresearch optimization loop for writing-voice-modes.

See docs/superpowers/specs/2026-05-09-writing-voice-modes-autoresearch-design.md.
"""
from __future__ import annotations

import json
import math
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
    sonnet_check_every_n_iterations: int = 5
    results_path: str = "data/skill-optimizer/writing-voice-modes-results.tsv"


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


RESULTS_HEADER = (
    "iteration", "timestamp", "mutation_section", "mutation_summary",
    "train_score", "holdout_score", "surprise_score",
    "criterion_substack_format_intro", "criterion_anti_pattern_overreference",
    "criterion_stylometric_distance", "criterion_signature_move_present",
    "criterion_sounds_like_sean", "criterion_no_anti_pattern_violation",
    "moving_avg", "delta_vs_best", "kept_or_reverted",
    "tripwires_triggered", "sonnet_qwen_agreement", "duration_sec", "cost_usd",
)


def write_results_row(path: Path, row: dict) -> None:
    """Append one row to results.tsv. Writes the header on first invocation."""
    write_header = not path.exists()
    with open(path, "a") as f:
        if write_header:
            f.write("\t".join(RESULTS_HEADER) + "\n")
        f.write("\t".join(str(row.get(k, "")) for k in RESULTS_HEADER) + "\n")


import datetime
import time
import yaml
from anthropic import Anthropic

from lib.skill_optimizer.structural_checks import (
    substack_format_intro,
    anti_pattern_overreference,
    stylometric_distance,
)
from lib.skill_optimizer.stylometry import load_baseline
from lib.skill_optimizer.judge_runner import JudgeRunner
from lib.skill_optimizer.mutation_guard import validate_mutation
from lib.skill_optimizer.decision import keep_or_revert, moving_average
from lib.skill_optimizer.tripwire import check_all_tripwires, IterationSnapshot

PROTECTED_LINE_RANGES = [(1, 4), (23, 69)]
PROTECTED_SECTION_HEADINGS = ("References", "Related Skills", "Copy/Paste Ready")
CRITERION_IDS = (
    "substack_format_intro", "anti_pattern_overreference", "stylometric_distance",
    "signature_move_present", "sounds_like_sean", "no_anti_pattern_violation",
)


def run_optimization_loop(config: SkillOptimizerConfig, dry_run: bool = False) -> None:
    """Top-level loop. See spec Section 9 for the data flow."""
    ok, reason = preflight_checks(config)
    if not ok:
        raise RuntimeError(f"preflight failed: {reason}")

    evals = yaml.safe_load(config.evals_path.read_text())
    sealed = yaml.safe_load(config.evals_sealed_path.read_text())
    baseline = load_baseline(config.stylometry_baseline_path)
    program_md = (config.repo_root / "agents-sdk/lib/skill_optimizer/program.md").read_text()
    judge_template = (config.repo_root / "agents-sdk/lib/skill_optimizer/judge_prompt.txt").read_text()

    anthropic = Anthropic()
    # Local Ollama client wrapper — implementation can use anthropic-style or direct HTTP.
    # For dry_run, both clients are mocks that return canned text/YES.
    local_client = _build_ollama_client(config) if not dry_run else _DummyClient("YES")
    sonnet_client = anthropic if not dry_run else _DummyClient("YES")
    judge = JudgeRunner(local_client=local_client, sonnet_client=sonnet_client, prompt_template=judge_template)

    results_path = config.repo_root / "agents-sdk" / config.results_path

    best_binary_array: list[int] = []
    train_scores: list[float] = []
    iter1_snapshot: Optional[dict] = None
    cumulative_cost = 0.0

    for iteration in range(1, config.max_iterations + 1):
        start = time.time()
        current_skill_md = config.target_skill_md.read_text()

        # 1. Propose mutation
        recent_rows = _read_recent_rows(results_path, n=5)
        worst = _worst_criteria(recent_rows)
        try:
            section, rationale, modified_md = propose_mutation(
                optimizer_client=anthropic,
                program_md=program_md,
                current_skill_md=current_skill_md,
                recent_results=recent_rows,
                worst_criteria=worst,
            )
        except Exception as e:
            print(f"[iter {iteration}] mutation proposal failed: {e}; skipping")
            continue

        # 2. Validate
        ok, reason = validate_mutation(
            original_lines=current_skill_md.splitlines(keepends=True),
            modified_lines=modified_md.splitlines(keepends=True),
            protected_line_ranges=PROTECTED_LINE_RANGES,
            protected_section_headings=PROTECTED_SECTION_HEADINGS,
            criterion_ids=CRITERION_IDS,
        )
        if not ok:
            print(f"[iter {iteration}] mutation rejected: {reason}; retrying")
            continue

        # 3. Apply in-memory (write to disk; will revert on bad score)
        config.target_skill_md.write_text(modified_md)

        # 4. Generate
        train_outputs = generate_outputs(anthropic, modified_md, evals["training_prompts"], config.runs_per_prompt)
        holdout_outputs = generate_outputs(anthropic, modified_md, evals["holdout_prompts"], config.runs_per_prompt)
        surprise_outputs = {}
        if iteration % 5 == 0:
            surprise_outputs = generate_outputs(anthropic, modified_md, sealed["surprise_prompts"], config.runs_per_prompt)

        # 5. Score
        structural = _run_structural_checks(train_outputs, baseline)
        judge_outputs = _run_judge(judge, train_outputs, evals, mode_anchors=_load_anchors())
        train = score_outputs(structural, judge_outputs)
        train_score = train["total_passes"] / train["max_score"]

        # Holdout score (no decision-rule role; trip-wire only)
        ho_structural = _run_structural_checks(holdout_outputs, baseline)
        ho_judge = _run_judge(judge, holdout_outputs, evals, mode_anchors=_load_anchors())
        holdout = score_outputs(ho_structural, ho_judge)
        holdout_score = holdout["total_passes"] / holdout["max_score"]

        # 6. Sonnet sample-check (every 5 iters)
        sonnet_agreement = 1.0
        if iteration % config.sonnet_check_every_n_iterations == 0:
            sonnet_agreement = _sonnet_check(judge, train_outputs, evals)

        # 7. Decide keep/revert
        train_scores.append(train_score)
        ma = moving_average(train_scores, window=3)
        decision, info = keep_or_revert(train["binary_array"], best_binary_array)

        # 8. Trip-wires
        snapshot = _build_snapshot(iteration, train_score, holdout_score, train, iter1_snapshot, sonnet_agreement, modified_md)
        triggered = check_all_tripwires(snapshot)

        # 9. Apply decision (after tripwires for logging)
        if decision == "keep":
            best_binary_array = train["binary_array"]
            git_commit_mutation(config.repo_root, config.target_skill_md, iteration, section, rationale, ma if iteration > 1 else train_score, train_score)
        else:
            git_revert_skill_md(config.repo_root, config.target_skill_md)

        # 10. Log
        write_results_row(results_path, _build_row(iteration, section, rationale, train_score, holdout_score, surprise_outputs, train, ma, info, decision, triggered, sonnet_agreement, time.time() - start, cumulative_cost))

        if iter1_snapshot is None:
            iter1_snapshot = {"train_score": train_score, "criterion_scores": train["per_criterion"], "skill_md_token_count": len(modified_md.split()), "stylometric_score": train["per_criterion"].get("stylometric_distance", 0), "llm_judge_score": _llm_judge_avg(train["per_criterion"]), "avg_inter_run_similarity": _diversity(train_outputs)}

        # 11. Halt checks
        if iteration >= 4 and triggered:
            print(f"[iter {iteration}] HALT — tripwires triggered: {triggered}")
            break
        if train_score >= 0.75 and all(v >= 0.60 for v in train["per_criterion"].values()):
            print(f"[iter {iteration}] SUCCESS — aggregate {train_score:.3f} ≥ 0.75 with all floors ≥ 0.60")
            break
        if _plateau(train_scores, n=config.plateau_halt_iterations):
            print(f"[iter {iteration}] HALT — plateau ({config.plateau_halt_iterations} iters no improvement)")
            break

    print(f"loop complete after {iteration} iterations")


# Helper function placeholders — fully implemented in Tasks 4.7, 4.8, 4.9.
# These NotImplementedError stubs let skill_optimizer.py import cleanly so other
# tests can exercise pre-flight + scoring + git ops independently.
def _build_ollama_client(config):
    raise NotImplementedError("implemented in Task 4.9")

def _read_recent_rows(path, n):
    raise NotImplementedError("implemented in Task 4.8")

def _worst_criteria(rows: list[dict]) -> list[str]:
    """Return the 3 criterion names with the lowest scores in the most recent row."""
    if not rows:
        return []
    last = rows[-1]
    scored = []
    for k, v in last.items():
        if not k.startswith("criterion_"):
            continue
        try:
            scored.append((float(v), k.removeprefix("criterion_")))
        except (ValueError, TypeError):
            continue
    scored.sort()  # ascending — worst (lowest) first
    return [name for _, name in scored[:3]]

def _run_structural_checks(outputs, baseline):
    raise NotImplementedError("implemented in Task 4.9")

def _run_judge(judge, outputs, evals, mode_anchors):
    raise NotImplementedError("implemented in Task 4.9")

def _load_anchors():
    raise NotImplementedError("implemented in Task 4.8")

def _sonnet_check(judge, outputs, evals):
    raise NotImplementedError("implemented in Task 4.9")

def _build_snapshot(*args, **kwargs):
    raise NotImplementedError("implemented in Task 4.8")

def _build_row(*args, **kwargs):
    raise NotImplementedError("implemented in Task 4.8")

def _llm_judge_avg(per_criterion: dict[str, float]) -> float:
    """Mean of just the LLM-judge criteria (excludes structural)."""
    keys = ("signature_move_present", "sounds_like_sean", "no_anti_pattern_violation")
    vals = [per_criterion.get(k, 0.0) for k in keys]
    return sum(vals) / len(vals) if vals else 0.0


def _char_trigram_bag(text: str) -> dict[str, int]:
    text = text.lower()
    bag: dict[str, int] = {}
    for i in range(len(text) - 2):
        tri = text[i : i + 3]
        bag[tri] = bag.get(tri, 0) + 1
    return bag


def _cosine(a: dict[str, int], b: dict[str, int]) -> float:
    common = set(a.keys()) & set(b.keys())
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def _diversity(outputs: dict[str, list[dict]]) -> float:
    """Average inter-run cosine similarity over character trigrams.

    Higher = more similar (entropy collapse — a tripwire signal). Returns 0.0
    when no prompt has at least 2 runs to compare.
    """
    sims = []
    for _prompt_id, runs in outputs.items():
        if len(runs) < 2:
            continue
        bags = [_char_trigram_bag(r["text"]) for r in runs]
        for i in range(len(bags)):
            for j in range(i + 1, len(bags)):
                sims.append(_cosine(bags[i], bags[j]))
    return sum(sims) / len(sims) if sims else 0.0


def _plateau(scores: list[float], n: int = 3, tol: float = 0.005) -> bool:
    """True when the last `n` scores are within `tol` of each other (no improvement)."""
    if len(scores) < n:
        return False
    tail = scores[-n:]
    return max(tail) - min(tail) <= tol


class _DummyClient:
    """Echo client for dry-run mode."""
    def __init__(self, fixed_response: str = "YES"):
        self._r = fixed_response
        self.messages = self
    def create(self, **kwargs):
        return type("M", (), {"content": [type("C", (), {"text": self._r})()], "usage": type("U", (), {"input_tokens": 100, "output_tokens": 200})()})()
    def complete(self, **kwargs):
        return f"reasoning\n{self._r}"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--config-path", default="agents-sdk/config.toml")
    args = ap.parse_args()
    # Load config from TOML — caller fills in repo_root etc.
    import tomllib
    repo_root = Path(__file__).resolve().parents[2]
    cfg_data = tomllib.load(open(repo_root / args.config_path, "rb"))["agents"]["skill_optimizer"]
    config = SkillOptimizerConfig(
        branch=cfg_data["branch"],
        repo_root=repo_root,
        target_skill_md=repo_root / cfg_data["target_skill_md"],
        evals_path=repo_root / cfg_data["evals_path"],
        evals_sealed_path=repo_root / cfg_data["evals_sealed_path"],
        stylometry_baseline_path=repo_root / "agents-sdk" / cfg_data["stylometry_baseline_path"],
        max_iterations=cfg_data.get("max_iterations", 25),
        plateau_halt_iterations=cfg_data.get("plateau_halt_iterations", 3),
        runs_per_prompt=cfg_data.get("runs_per_prompt", 15),
        cost_cap_usd_hard=cfg_data.get("cost_cap_usd_hard", 200.0),
        cost_cap_usd_soft=cfg_data.get("cost_cap_usd_soft", 50.0),
        sonnet_check_every_n_iterations=cfg_data.get("sonnet_check_every_n_iterations", 5),
        results_path=cfg_data.get("results_path", "data/skill-optimizer/writing-voice-modes-results.tsv"),
    )
    run_optimization_loop(config, dry_run=args.dry_run)
