import json
from datetime import date
from pathlib import Path

import pytest

from council.budget import (
    estimate_cost,
    record_spend,
    preflight,
    BudgetExceeded,
    Pricing,
)


SAMPLE_PRICING = {
    "openai/gpt-X": Pricing(prompt_per_1k=0.0050, completion_per_1k=0.0150),
    "anthropic/claude-X": Pricing(prompt_per_1k=0.0030, completion_per_1k=0.0150),
    "google/gemini-X": Pricing(prompt_per_1k=0.0025, completion_per_1k=0.0100),
    "x-ai/grok-X": Pricing(prompt_per_1k=0.0050, completion_per_1k=0.0150),
}


def test_estimate_cost_sums_per_model():
    cost = estimate_cost(
        pricing=SAMPLE_PRICING,
        per_model_tokens=[
            ("openai/gpt-X", 1000, 500),       # in_tokens, out_tokens
            ("anthropic/claude-X", 1000, 500),
        ],
    )
    # GPT-X: 1k * 0.005 + 0.5k * 0.015 = 0.005 + 0.0075 = 0.0125
    # Claude-X: 1k * 0.003 + 0.5k * 0.015 = 0.003 + 0.0075 = 0.0105
    # Total: 0.023
    assert cost == pytest.approx(0.023, abs=1e-6)


def test_estimate_cost_raises_on_unknown_model():
    with pytest.raises(KeyError):
        estimate_cost(
            pricing=SAMPLE_PRICING,
            per_model_tokens=[("unknown/model", 100, 100)],
        )


def test_record_spend_appends_atomically(tmp_spend_dir):
    today = date(2026, 5, 14)
    record_spend(amount=0.50, profile="variance", tag="test-1", on_date=today)
    record_spend(amount=0.30, profile="premium", tag="test-2", on_date=today)
    daily_file = tmp_spend_dir / "council-spend-2026-05-14.json"
    assert daily_file.exists()
    data = json.loads(daily_file.read_text())
    assert data["total"] == pytest.approx(0.80, abs=1e-6)
    assert len(data["runs"]) == 2
    assert data["runs"][0]["amount"] == 0.50
    assert data["runs"][0]["tag"] == "test-1"


def test_preflight_passes_when_under_caps(tmp_spend_dir):
    preflight(
        estimated=0.40,
        per_query_cap=0.80,
        daily_cap=5.00,
        monthly_cap=30.00,
        on_date=date(2026, 5, 14),
    )  # no exception


def test_preflight_rejects_when_over_per_query_cap(tmp_spend_dir):
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=0.90,
            per_query_cap=0.80,
            daily_cap=5.00,
            monthly_cap=30.00,
            on_date=date(2026, 5, 14),
        )
    assert "per-query" in str(exc.value).lower()


def test_preflight_rejects_when_estimated_plus_today_over_daily(tmp_spend_dir):
    today = date(2026, 5, 14)
    record_spend(amount=4.70, profile="premium", tag="prior", on_date=today)
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=0.50,  # 4.70 + 0.50 = 5.20 > 5.00 daily cap
            per_query_cap=0.80,
            daily_cap=5.00,
            monthly_cap=30.00,
            on_date=today,
        )
    assert "daily" in str(exc.value).lower()


def test_preflight_rejects_when_month_to_date_plus_estimated_over_monthly(tmp_spend_dir):
    # Spread spend across days in the same month
    from datetime import date as date_cls
    for day in (1, 2, 3, 4, 5):
        record_spend(amount=5.00, profile="premium", tag=f"day-{day}", on_date=date_cls(2026, 5, day))
    # Month-to-date = 25.00; add 6.00 → 31.00 > 30.00 monthly cap
    with pytest.raises(BudgetExceeded) as exc:
        preflight(
            estimated=6.00,
            per_query_cap=10.00,
            daily_cap=100.00,  # high so daily doesn't fire
            monthly_cap=30.00,
            on_date=date_cls(2026, 5, 6),
        )
    assert "monthly" in str(exc.value).lower()
