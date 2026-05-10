"""Decision module — moving average + bootstrap CI for keep/revert.

Per the autoresearch design (Section 8.1 of the spec): only the training-set
score drives keep/revert decisions. Holdout score is for trip-wires; surprise
score is reported but not part of the decision rule.
"""
from __future__ import annotations

import random
import statistics
from typing import Sequence


def moving_average(values: Sequence[float], window: int = 3) -> float:
    """Mean of the most recent `window` values. If fewer than `window` exist, mean of all."""
    if not values:
        return 0.0
    tail = list(values)[-window:]
    return statistics.mean(tail)


def bootstrap_ci(
    binary_outcomes: Sequence[int],
    n_resamples: int = 1000,
    ci: float = 0.95,
) -> tuple[float, float]:
    """Bootstrap CI for the mean of a binary 0/1 outcome array.

    Returns (lower, upper) of the (1-ci)/2 and (1+ci)/2 percentile of the resample means.
    """
    if not binary_outcomes:
        return 0.0, 0.0
    means = []
    n = len(binary_outcomes)
    for _ in range(n_resamples):
        sample = [binary_outcomes[random.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_idx = int(((1 - ci) / 2) * n_resamples)
    hi_idx = int(((1 + ci) / 2) * n_resamples) - 1
    return means[lo_idx], means[hi_idx]


def keep_or_revert(
    current_outcomes: Sequence[int],
    best_outcomes: Sequence[int],
    n_resamples: int = 1000,
    ci: float = 0.95,
) -> tuple[str, dict]:
    """Decide keep vs revert based on bootstrap CI of (current - best) > 0.

    Returns ('keep' | 'revert', info dict with lo/hi/delta).
    """
    if not current_outcomes:
        return "revert", {"reason": "no current outcomes"}

    # Bootstrap the difference distribution by resampling each independently.
    n_cur = len(current_outcomes)
    n_best = len(best_outcomes) if best_outcomes else 0
    deltas = []
    for _ in range(n_resamples):
        cur_mean = sum(current_outcomes[random.randrange(n_cur)] for _ in range(n_cur)) / n_cur
        if n_best > 0:
            best_mean = sum(best_outcomes[random.randrange(n_best)] for _ in range(n_best)) / n_best
        else:
            best_mean = 0.0
        deltas.append(cur_mean - best_mean)
    deltas.sort()
    lo_idx = int(((1 - ci) / 2) * n_resamples)
    hi_idx = int(((1 + ci) / 2) * n_resamples) - 1
    lo, hi = deltas[lo_idx], deltas[hi_idx]
    info = {"delta_lo": lo, "delta_hi": hi, "delta_mean": statistics.mean(deltas)}
    decision = "keep" if lo > 0 else "revert"
    return decision, info
