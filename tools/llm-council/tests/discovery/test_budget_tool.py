from datetime import date
from council import budget


def test_tool_totals_isolated(tmp_spend_dir):
    d = date(2026, 6, 20)
    budget.record_spend(amount=0.30, profile="standard", tag="t1", on_date=d, tool="discovery")
    budget.record_spend(amount=0.90, profile="premium", tag="t2", on_date=d, tool="council")
    assert round(budget.tool_total_for_day(d, "discovery"), 4) == 0.30
    assert round(budget.tool_total_for_day(d, "council"), 4) == 0.90


def test_preflight_tool_rejects_on_tool_daily_cap(tmp_spend_dir):
    d = date(2026, 6, 20)
    budget.record_spend(amount=9.80, profile="standard", tag="t", on_date=d, tool="discovery")
    import pytest
    with pytest.raises(budget.BudgetExceeded):
        budget.preflight_tool(
            estimated=0.50, per_query_cap=1.50, daily_cap=10.0, monthly_cap=50.0,
            on_date=d, tool="discovery",
        )
    # council budget is unaffected by discovery spend
    budget.preflight_tool(
        estimated=0.50, per_query_cap=1.00, daily_cap=10.0, monthly_cap=50.0,
        on_date=d, tool="council",
    )
