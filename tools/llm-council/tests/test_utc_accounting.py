"""UTC accounting-date and admission-month ownership regression tests."""

import contextlib
import json
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from click.testing import CliRunner

from council import budget
from council.client import ModelResponse
from council.discovery.pipeline import DiscoveryFailed, DiscoveryResult
from council.pipeline import CouncilSession


def _reserve(*, on_date: date, reserved_cost: float, run_id: str):
    return budget.check_and_reserve(
        reserved_cost=reserved_cost,
        tool="council",
        tag="utc-accounting-test",
        profile="variance",
        run_id=run_id,
        on_date=on_date,
        per_query_cap=10.0,
        tool_daily_cap=10.0,
        tool_monthly_cap=100.0,
        aggregate_daily_cap=10.0,
        aggregate_monthly_cap=100.0,
    )


@pytest.mark.parametrize(
    ("instant", "expected"),
    [
        (datetime(2026, 8, 31, 23, 30, tzinfo=timezone.utc), date(2026, 8, 31)),
        # 17:30 on August 31 in US/Pacific is already September 1 in UTC.
        (datetime(2026, 9, 1, 0, 30, tzinfo=timezone.utc), date(2026, 9, 1)),
    ],
)
def test_utc_accounting_date_returns_the_utc_calendar_day(monkeypatch, instant, expected):
    class StubDatetime:
        @classmethod
        def now(cls, tz):
            assert tz is timezone.utc
            return instant

    monkeypatch.setattr(budget, "datetime", StubDatetime)

    assert budget.utc_accounting_date() == expected


def test_utc_month_drives_daily_file_and_month_lock_path(tmp_spend_dir):
    september = date(2026, 9, 1)

    reservation = _reserve(on_date=september, reserved_cost=1.25, run_id="september-run")

    september_file = tmp_spend_dir / "council-spend-2026-09-01.json"
    assert september_file.exists()
    assert json.loads(september_file.read_text())["runs"][0]["reservation_id"] == (
        reservation.reservation_id
    )
    september_lock = budget.month_lock_path(september)
    august_lock = budget.month_lock_path(date(2026, 8, 31))
    assert september_lock.name == ".council-spend-2026-09.lock"
    assert september_lock != august_lock


def test_admission_month_owns_actuals_and_close_across_utc_rollover(tmp_spend_dir):
    august = _reserve(
        on_date=date(2026, 8, 31), reserved_cost=1.25, run_id="august-admission"
    )
    budget.mark_dispatched(august)
    september = _reserve(
        on_date=date(2026, 9, 1), reserved_cost=2.50, run_id="september-admission"
    )

    budget.record_actual(
        august,
        attempt_id="august-attempt",
        generation_id="august-generation",
        usage_cost=0.75,
        status="settled",
    )
    budget.close(august, status="settled")

    august_data = json.loads(
        (tmp_spend_dir / "council-spend-2026-08-31.json").read_text()
    )
    september_data = json.loads(
        (tmp_spend_dir / "council-spend-2026-09-01.json").read_text()
    )
    assert august_data["total"] == 1.25
    assert august_data["runs"][0]["status"] == "settled"
    assert august_data["actuals"][0]["reservation_id"] == august.reservation_id
    assert september_data["total"] == 2.5
    assert [row["reservation_id"] for row in september_data["runs"]] == [
        september.reservation_id
    ]
    assert september_data["actuals"] == []
    assert budget.strict_ledger_state(date(2026, 9, 15))["month"]["aggregate"] == Decimal(
        "2.5"
    )


def test_settlement_takes_the_admission_months_lock_not_the_current_months(
    tmp_spend_dir, monkeypatch
):
    """Review finding (Task 1, round 2): the file assertions alone would not catch a
    mutation that acquires the CURRENT month's lock while still writing the admission
    month's file — restoring the exact split-lock race residual 2 closes. Spy on the
    lock acquisition itself: every settlement-path transaction on an August-admitted
    reservation must take August's month lock and never any other month's."""
    august = _reserve(
        on_date=date(2026, 8, 31), reserved_cost=1.25, run_id="august-lock-owner"
    )
    budget.mark_dispatched(august)

    acquired: list[str] = []
    real_month_lock = budget.month_lock

    @contextlib.contextmanager
    def spying_month_lock(accounting_date, *, root=None):
        acquired.append(accounting_date.strftime("%Y-%m"))
        with real_month_lock(accounting_date, root=root):
            yield

    monkeypatch.setattr(budget, "month_lock", spying_month_lock)

    budget.record_actual(
        august,
        attempt_id="august-lock-attempt",
        generation_id="august-lock-generation",
        usage_cost=0.75,
        status="settled",
    )
    budget.close(august, status="settled")

    assert acquired == ["2026-08", "2026-08"]


def test_council_cli_uses_utc_accounting_date_for_preflight_and_record(
    tmp_path, monkeypatch
):
    from council import cli

    sentinel = date(2040, 2, 29)
    captured = {}

    class FakeClient:
        async def aclose(self):
            return None

    async def fake_run_council(**kwargs):
        return CouncilSession(
            id="utc-session",
            profile=kwargs["profile"].name,
            tag=kwargs["tag"],
            user_query=kwargs["user_query"],
            responses=[],
            rankings=[],
            chairman_response=ModelResponse("chair", "done", 1, 1, 1),
            total_tokens_in=1,
            total_tokens_out=1,
            duration_ms=1,
        )

    monkeypatch.setattr(cli, "utc_accounting_date", lambda: sentinel)
    monkeypatch.setattr(cli, "OpenRouterClient", FakeClient)
    monkeypatch.setattr(cli, "run_council", fake_run_council)
    monkeypatch.setattr(
        cli, "preflight_tool", lambda **kwargs: captured.__setitem__("preflight", kwargs["on_date"])
    )
    monkeypatch.setattr(
        cli, "record_spend", lambda **kwargs: captured.__setitem__("record", kwargs["on_date"])
    )
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("hello")

    result = CliRunner().invoke(
        cli.main,
        [
            "--profile",
            "variance",
            "--prompt-file",
            str(prompt),
            "--output",
            str(tmp_path / "out.md"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert captured["preflight"] is sentinel
    assert captured["record"] is sentinel


def test_discovery_cli_success_uses_utc_accounting_date_for_preflight_and_record(
    tmp_path, monkeypatch
):
    import council.discovery.__main__ as discovery_cli

    sentinel = date(2040, 2, 29)
    captured = {}

    async def fake_run_discovery(**kwargs):
        return DiscoveryResult("# ledger", 0.42, 1, 0, {"id": "utc-discovery"})

    monkeypatch.setattr(discovery_cli, "utc_accounting_date", lambda: sentinel)
    monkeypatch.setattr(discovery_cli, "load_dotenv", lambda: None)
    monkeypatch.setattr(discovery_cli, "run_discovery", fake_run_discovery)
    monkeypatch.setattr(
        discovery_cli,
        "preflight_tool",
        lambda **kwargs: captured.__setitem__("preflight", kwargs["on_date"]),
    )
    monkeypatch.setattr(
        discovery_cli,
        "record_spend",
        lambda **kwargs: captured.__setitem__("record", kwargs["on_date"]),
    )

    result = CliRunner().invoke(
        discovery_cli.main,
        ["utc topic", "--tier", "quick", "--output", str(tmp_path / "ledger.md")],
    )

    assert result.exit_code == 0, result.output
    assert captured["preflight"] is sentinel
    assert captured["record"] is sentinel


def test_discovery_cli_billed_failure_uses_utc_accounting_date_for_record(
    tmp_path, monkeypatch
):
    import council.discovery.__main__ as discovery_cli

    sentinel = date(2040, 2, 29)
    captured = {}

    async def fake_run_discovery(**kwargs):
        raise DiscoveryFailed("fuse failed", cost_usd=0.42)

    monkeypatch.setattr(discovery_cli, "utc_accounting_date", lambda: sentinel)
    monkeypatch.setattr(discovery_cli, "load_dotenv", lambda: None)
    monkeypatch.setattr(discovery_cli, "run_discovery", fake_run_discovery)
    monkeypatch.setattr(
        discovery_cli,
        "preflight_tool",
        lambda **kwargs: captured.__setitem__("preflight", kwargs["on_date"]),
    )
    monkeypatch.setattr(
        discovery_cli,
        "record_spend",
        lambda **kwargs: captured.__setitem__("record", kwargs["on_date"]),
    )

    result = CliRunner().invoke(
        discovery_cli.main,
        ["utc topic", "--tier", "quick", "--output", str(tmp_path / "ledger.md")],
    )

    assert result.exit_code == 3
    assert captured["preflight"] is sentinel
    assert captured["record"] is sentinel


def test_panel_vs_single_cli_uses_utc_accounting_date_for_preflight_and_run(
    tmp_path, monkeypatch
):
    import experiments.panel_vs_single as panel_cli

    sentinel = date(2040, 2, 29)
    captured = {}

    async def fake_run_panel_vs_single(**kwargs):
        captured["run"] = kwargs["on_date"]
        return {"cost": 0.0}

    monkeypatch.setattr(panel_cli, "utc_accounting_date", lambda: sentinel)
    monkeypatch.setattr(panel_cli, "load_dotenv", lambda: None)
    monkeypatch.setattr(panel_cli, "run_panel_vs_single", fake_run_panel_vs_single)
    monkeypatch.setattr(panel_cli, "_write_artifacts", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        panel_cli,
        "preflight_tool",
        lambda **kwargs: captured.__setitem__("preflight", kwargs["on_date"]),
    )

    result = CliRunner().invoke(
        panel_cli.main,
        ["--yes", "--out", str(tmp_path / "panel-run")],
    )

    assert result.exit_code == 0, result.output
    assert captured["preflight"] is sentinel
    assert captured["run"] is sentinel


def test_gateway_sources_never_use_local_date_today():
    project_root = Path(__file__).resolve().parents[1]
    gateway_paths = (
        project_root / "council" / "cli.py",
        project_root / "council" / "discovery" / "__main__.py",
        project_root / "experiments" / "panel_vs_single.py",
        project_root / "experiments" / "panel_vs_single_core.py",
    )

    for path in gateway_paths:
        assert "date.today()" not in path.read_text(), path
