"""Tripwire module — six anti-Goodhart safety checks per the autoresearch design.

See Section 8.2 of the spec. Trip-wires are LOG-ONLY for iterations 1-3
(calibration phase) and HALT from iteration 4 onward — that policy is enforced
by the orchestrator, not this module.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field


@dataclass
class IterationSnapshot:
    """Everything a tripwire check might need from one iteration."""
    iteration: int
    train_score: float
    holdout_score: float
    prior_holdout_scores: list[float]  # last 3 holdout scores (most recent last)
    criterion_scores: dict[str, float]
    criterion_scores_iter1: dict[str, float]
    stylometric_score: float
    stylometric_score_baseline: float  # iter 1 stylometric score
    llm_judge_score: float
    llm_judge_score_baseline: float  # iter 1 LLM-judge avg
    avg_inter_run_similarity: float
    avg_inter_run_similarity_baseline: float  # iter 1
    sonnet_qwen_agreement: float
    skill_md_token_count: int
    skill_md_token_count_baseline: int  # iter 1
    score_gain_vs_baseline: float  # train_score - iter1.train_score


# Threshold constants — tunable via spec Section 8.2.
TRAIN_HOLDOUT_DIVERGENCE_PP = 0.05  # 5pp
CRITERION_DRIFT_RATIO = 1.5
STYLOMETRIC_DROP_PCT = 0.15
DIVERSITY_RISE_PCT = 0.20
JUDGE_AGREEMENT_FLOOR = 0.70
COMPLEXITY_TOKEN_GROWTH_PCT = 0.50
COMPLEXITY_MIN_SCORE_GAIN = 0.05


def _train_holdout_divergence(s: IterationSnapshot) -> bool:
    if len(s.prior_holdout_scores) < 1:
        return False
    earliest = max(s.prior_holdout_scores)
    return (earliest - s.holdout_score) > TRAIN_HOLDOUT_DIVERGENCE_PP


def _criterion_uneven_drift(s: IterationSnapshot) -> bool:
    if not s.criterion_scores_iter1:
        return False
    ratios = []
    for k, baseline in s.criterion_scores_iter1.items():
        if baseline == 0:
            continue
        current = s.criterion_scores.get(k, 0.0)
        ratios.append(current / baseline)
    if len(ratios) < 2:
        return False
    median = statistics.median(ratios)
    return any(r / median > CRITERION_DRIFT_RATIO for r in ratios)


def _stylometric_drift(s: IterationSnapshot) -> bool:
    if s.stylometric_score_baseline == 0:
        return False
    drop = (s.stylometric_score_baseline - s.stylometric_score) / s.stylometric_score_baseline
    llm_rising = s.llm_judge_score > s.llm_judge_score_baseline
    return drop > STYLOMETRIC_DROP_PCT and llm_rising


def _diversity_collapse(s: IterationSnapshot) -> bool:
    if s.avg_inter_run_similarity_baseline == 0:
        return False
    rise = (s.avg_inter_run_similarity - s.avg_inter_run_similarity_baseline) / s.avg_inter_run_similarity_baseline
    return rise > DIVERSITY_RISE_PCT


def _judge_disagreement(s: IterationSnapshot) -> bool:
    return s.sonnet_qwen_agreement < JUDGE_AGREEMENT_FLOOR


def _complexity_ratchet(s: IterationSnapshot) -> bool:
    if s.skill_md_token_count_baseline == 0:
        return False
    growth = (s.skill_md_token_count - s.skill_md_token_count_baseline) / s.skill_md_token_count_baseline
    return growth > COMPLEXITY_TOKEN_GROWTH_PCT and s.score_gain_vs_baseline < COMPLEXITY_MIN_SCORE_GAIN


TRIPWIRES = {
    "train_holdout_divergence": _train_holdout_divergence,
    "criterion_uneven_drift": _criterion_uneven_drift,
    "stylometric_drift": _stylometric_drift,
    "diversity_collapse": _diversity_collapse,
    "judge_disagreement": _judge_disagreement,
    "complexity_ratchet": _complexity_ratchet,
}


def check_all_tripwires(snap: IterationSnapshot) -> list[str]:
    """Return the names of any triggered tripwires."""
    return [name for name, fn in TRIPWIRES.items() if fn(snap)]
