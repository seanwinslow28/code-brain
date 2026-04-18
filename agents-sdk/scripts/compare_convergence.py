#!/usr/bin/env python3
"""D.4 A/B convergence harness.

Reads baseline + treatment Optuna run logs (JSON), computes trials-to-
best-fitness per night, and runs a paired Wilcoxon signed-rank test.
Gate: treatment median ≥10% lower than baseline, p < 0.1.

Usage:
    python3 scripts/compare_convergence.py \
        --baseline-dir results/baseline-week13 \
        --treatment-dir results/treatment-week16 \
        --out vault/90_system/autoresearch-convergence-ab.md

Input JSON shape (per-night file):
    {
      "date": "2026-06-19",
      "trials": [{"trial": 0, "fitness": 0.41}, ...],
      "best_fitness": 0.73,
      "articles_used": 0
    }

"trials-to-best-fitness" = index of first trial whose fitness is within
1σ of the run's best (per-run median + stdev). Baseline and treatment
must have equal night counts (paired design).
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any


def trials_to_best_fitness(trials: list[dict[str, Any]]) -> int:
    """Index of first trial whose fitness ≥ median(run) + 1σ(run).

    If σ=0 or no such trial exists, return len(trials) (no convergence).
    """
    fit = [float(t.get("fitness", 0.0)) for t in trials]
    if not fit:
        return 0
    median = statistics.median(fit)
    try:
        sigma = statistics.pstdev(fit)
    except statistics.StatisticsError:
        sigma = 0.0
    threshold = median + sigma
    for i, f in enumerate(fit):
        if f >= threshold:
            return i
    return len(fit)


def _wilcoxon_signed_rank(
    baseline: list[float],
    treatment: list[float],
) -> tuple[float, float]:
    """Paired Wilcoxon signed-rank test. Returns (W, two-sided p-value).

    Manual implementation (stdlib only) — uses the normal approximation
    because n is expected to be small (7 nights).
    """
    if len(baseline) != len(treatment):
        raise ValueError("baseline and treatment must have equal length")
    diffs = [t - b for b, t in zip(baseline, treatment) if (t - b) != 0]
    n = len(diffs)
    if n == 0:
        return (0.0, 1.0)

    # Rank |diffs| with average ranks for ties
    sorted_pairs = sorted(enumerate(diffs), key=lambda kv: abs(kv[1]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(sorted_pairs[j + 1][1]) == abs(sorted_pairs[i][1]):
            j += 1
        avg_rank = (i + j) / 2 + 1  # +1 to shift to 1-indexed
        for k in range(i, j + 1):
            ranks[sorted_pairs[k][0]] = avg_rank
        i = j + 1

    W_plus = sum(r for r, d in zip(ranks, diffs) if d > 0)
    W_minus = sum(r for r, d in zip(ranks, diffs) if d < 0)
    W = min(W_plus, W_minus)

    # Normal approximation
    mean = n * (n + 1) / 4
    var = n * (n + 1) * (2 * n + 1) / 24
    if var <= 0:
        return (W, 1.0)
    z = (W - mean) / (var ** 0.5)
    # Two-sided p via erfc
    import math
    p = math.erfc(abs(z) / (2 ** 0.5))
    return (W, p)


def _load_night_files(d: Path) -> list[dict[str, Any]]:
    files = sorted(d.glob("*.json"))
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-dir", required=True, type=Path)
    parser.add_argument("--treatment-dir", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--threshold", type=float, default=0.10)
    parser.add_argument("--p-threshold", type=float, default=0.10)
    args = parser.parse_args()

    baseline = _load_night_files(args.baseline_dir)
    treatment = _load_night_files(args.treatment_dir)
    if not baseline or not treatment:
        print("No night files in one of the directories", file=sys.stderr)
        return 2
    if len(baseline) != len(treatment):
        print(f"Night count mismatch: {len(baseline)} vs {len(treatment)}", file=sys.stderr)
        return 2

    b_conv = [trials_to_best_fitness(n.get("trials", [])) for n in baseline]
    t_conv = [trials_to_best_fitness(n.get("trials", [])) for n in treatment]

    b_med = statistics.median(b_conv)
    t_med = statistics.median(t_conv)
    improvement = (b_med - t_med) / b_med if b_med > 0 else 0.0

    _, p = _wilcoxon_signed_rank(b_conv, t_conv)

    verdict = (
        "PASS"
        if improvement >= args.threshold and p < args.p_threshold
        else "FAIL"
    )

    report = [
        f"# Autoresearch Convergence A/B — {verdict}",
        "",
        f"Nights compared: {len(b_conv)}",
        f"Baseline median trials-to-best: {b_med:.1f}",
        f"Treatment median trials-to-best: {t_med:.1f}",
        f"Improvement: {improvement * 100:.1f}% (gate ≥{args.threshold * 100:.0f}%)",
        f"Wilcoxon p: {p:.4f} (gate p<{args.p_threshold})",
        "",
        "## Per-night convergence",
        "",
        "| # | baseline | treatment |",
        "|---|----------|-----------|",
    ]
    for i, (b, t) in enumerate(zip(b_conv, t_conv)):
        report.append(f"| {i + 1} | {b} | {t} |")

    output = "\n".join(report) + "\n"
    print(output)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
