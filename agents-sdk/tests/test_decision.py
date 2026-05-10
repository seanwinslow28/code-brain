"""Tests for decision module."""
import random
import pytest
from lib.skill_optimizer.decision import (
    moving_average,
    bootstrap_ci,
    keep_or_revert,
)


class TestMovingAverage:
    def test_short_window(self):
        assert moving_average([0.5], window=3) == 0.5

    def test_partial_window(self):
        assert moving_average([0.5, 0.7], window=3) == pytest.approx(0.6)

    def test_full_window(self):
        result = moving_average([0.4, 0.5, 0.6, 0.7], window=3)
        assert result == pytest.approx((0.5 + 0.6 + 0.7) / 3)


class TestBootstrapCI:
    def test_returns_lower_and_upper(self):
        random.seed(42)
        binary = [1] * 80 + [0] * 20  # 80% pass rate
        lo, hi = bootstrap_ci(binary, n_resamples=500, ci=0.95)
        assert 0.7 < lo < 0.85
        assert 0.75 < hi < 0.9
        assert lo < hi

    def test_zero_data_returns_zero_zero(self):
        lo, hi = bootstrap_ci([], n_resamples=100, ci=0.95)
        assert lo == 0.0 and hi == 0.0


class TestKeepOrRevert:
    def test_keeps_when_ci_clearly_positive(self):
        random.seed(42)
        # current iteration scored 90% across 350 trials, prior best was 70%.
        current = [1] * 315 + [0] * 35
        best = [1] * 245 + [0] * 105
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "keep"

    def test_reverts_when_no_clear_improvement(self):
        random.seed(42)
        current = [1] * 250 + [0] * 100
        best = [1] * 250 + [0] * 100
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "revert"

    def test_reverts_when_current_worse(self):
        random.seed(42)
        current = [1] * 200 + [0] * 150
        best = [1] * 280 + [0] * 70
        decision, _ = keep_or_revert(current, best, n_resamples=500)
        assert decision == "revert"
