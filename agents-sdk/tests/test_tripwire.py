"""Tests for tripwire module."""
import pytest
from lib.skill_optimizer.tripwire import (
    check_all_tripwires,
    IterationSnapshot,
)


def _snap(**kwargs) -> IterationSnapshot:
    defaults = dict(
        iteration=5,
        train_score=0.75,
        holdout_score=0.70,
        prior_holdout_scores=[0.72, 0.71, 0.70],
        criterion_scores={
            "substack_format_intro": 0.80,
            "anti_pattern_overreference": 0.85,
            "stylometric_distance": 0.78,
            "signature_move_present": 0.75,
            "sounds_like_sean": 0.70,
            "no_anti_pattern_violation": 0.75,
        },
        criterion_scores_iter1={
            "substack_format_intro": 0.75,
            "anti_pattern_overreference": 0.80,
            "stylometric_distance": 0.70,
            "signature_move_present": 0.70,
            "sounds_like_sean": 0.65,
            "no_anti_pattern_violation": 0.70,
        },
        stylometric_score=0.78,
        stylometric_score_baseline=0.70,
        llm_judge_score=0.73,
        llm_judge_score_baseline=0.68,
        avg_inter_run_similarity=0.45,
        avg_inter_run_similarity_baseline=0.40,
        sonnet_qwen_agreement=0.85,
        skill_md_token_count=2500,
        skill_md_token_count_baseline=2000,
        score_gain_vs_baseline=0.10,
    )
    defaults.update(kwargs)
    return IterationSnapshot(**defaults)


class TestTripwires:
    def test_no_tripwires_on_healthy_iteration(self):
        triggered = check_all_tripwires(_snap())
        assert triggered == []

    def test_train_holdout_divergence(self):
        snap = _snap(prior_holdout_scores=[0.78, 0.76, 0.72], holdout_score=0.65)
        # Drop = 0.78 - 0.65 = 0.13 over 3 iters → triggers >5pp threshold
        triggered = check_all_tripwires(snap)
        assert "train_holdout_divergence" in triggered

    def test_complexity_ratchet(self):
        snap = _snap(skill_md_token_count=3500, skill_md_token_count_baseline=2000, score_gain_vs_baseline=0.02)
        # 75% growth, 2% gain → triggers
        triggered = check_all_tripwires(snap)
        assert "complexity_ratchet" in triggered

    def test_diversity_collapse(self):
        snap = _snap(avg_inter_run_similarity=0.65, avg_inter_run_similarity_baseline=0.40)
        triggered = check_all_tripwires(snap)
        assert "diversity_collapse" in triggered

    def test_judge_disagreement(self):
        snap = _snap(sonnet_qwen_agreement=0.65)
        triggered = check_all_tripwires(snap)
        assert "judge_disagreement" in triggered

    def test_stylometric_drift(self):
        snap = _snap(stylometric_score=0.55, stylometric_score_baseline=0.75, llm_judge_score=0.80, llm_judge_score_baseline=0.65)
        triggered = check_all_tripwires(snap)
        assert "stylometric_drift" in triggered
