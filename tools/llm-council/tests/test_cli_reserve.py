"""Council CLI adoption of the locked reserve-before-dispatch lifecycle."""

import pytest
import json
from datetime import date
from types import SimpleNamespace

from click.testing import CliRunner

from council import budget, cli
from council.pipeline import DEFAULT_STAGE_BOUNDS, FanoutAbort


TODAY = date(2026, 7, 18)


def _session(tag="reserve-test"):
    return SimpleNamespace(
        tag=tag,
        id="session-1",
        duration_ms=10,
        total_tokens_in=10,
        total_tokens_out=20,
        dropped_models=[],
        ranking_failed_models=[],
        responses=[{"model_id": "member", "content": "answer"}],
        rankings=[{"judge_model": "judge", "ranking": ["A"], "reasoning": "ok"}],
        chairman_response=SimpleNamespace(model_id="chair", content="synthesis"),
    )


def _invoke(runner, prompt_file, out_file, *extra):
    return runner.invoke(
        cli.main,
        [
            "--profile",
            "variance",
            "--prompt-file",
            str(prompt_file),
            "--output",
            str(out_file),
            "--tag",
            "reserve-test",
            *extra,
        ],
    )


def _ledger(spend_dir):
    return json.loads((spend_dir / f"council-spend-{TODAY.isoformat()}.json").read_text())


def _prepare(monkeypatch, tmp_path):
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("How should this be tested?")
    out_file = tmp_path / "answer.md"
    monkeypatch.setattr(cli, "utc_accounting_date", lambda: TODAY)
    return prompt_file, out_file


class _Client:
    def __init__(self, events=None, **kwargs):
        if events is not None:
            events.append("client")

    async def aclose(self):
        pass


def test_happy_path_reserves_dispatches_records_actuals_and_settles(
    tmp_spend_dir, tmp_path, monkeypatch
):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def run_council(**kwargs):
        assert kwargs["dispatch_bounds"] is DEFAULT_STAGE_BOUNDS
        before = _ledger(tmp_spend_dir)
        assert before["runs"][0]["status"] == "dispatched"
        kwargs["on_attempt"]({"generation_id": "gen-1", "cost": 0.25})
        after = _ledger(tmp_spend_dir)
        assert after["actuals"][0]["status"] == "settled"
        kwargs["on_attempt"]({"generation_id": "gen-2", "cost": 0.50})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 0, result.output
    data = _ledger(tmp_spend_dir)
    reservation = data["runs"][0]
    assert reservation["amount"] == 5.069952
    assert reservation["status"] == "settled"
    assert data["total"] == 5.069952
    assert [(row["attempt_id"].rsplit("-", 1)[1], row["generation_id"], row["usage_cost"], row["status"], row["provenance"]) for row in data["actuals"]] == [
        ("01", "gen-1", 0.25, "settled", "authoritative"),
        ("02", "gen-2", 0.50, "settled", "authoritative"),
    ]
    assert "Actual cost: $0.7500" in result.output
    assert out_file.exists()


def test_none_cost_attempt_closes_unknown(tmp_spend_dir, tmp_path, monkeypatch):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": None, "cost": None})
        kwargs["on_attempt"]({"generation_id": "gen-known", "cost": 0.25})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 0, result.output
    data = _ledger(tmp_spend_dir)
    assert data["runs"][0]["status"] == "unknown"
    assert [row["status"] for row in data["actuals"]] == ["unknown", "settled"]
    assert [row["usage_cost"] for row in data["actuals"]] == [None, 0.25]


def test_fanout_abort_after_dispatch_closes_unknown_and_retains_debit(
    tmp_spend_dir, tmp_path, monkeypatch
):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def abort(**kwargs):
        raise FanoutAbort("fanout failed", attempts=[])

    monkeypatch.setattr(cli, "run_council", abort)

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 3
    data = _ledger(tmp_spend_dir)
    assert data["runs"][0]["amount"] == 5.069952
    assert data["runs"][0]["status"] == "unknown"
    assert data["total"] == 5.069952
    assert not out_file.exists()


def test_budget_exceeded_at_reserve_never_dispatches_or_constructs_client(
    tmp_spend_dir, tmp_path, monkeypatch
):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    budget.record_spend(
        amount=44.0, profile="prior", tag="prior", tool="council", on_date=TODAY
    )

    def no_network():
        raise AssertionError("network client constructed after refused reservation")

    monkeypatch.setattr(cli, "OpenRouterClient", no_network)
    monkeypatch.setattr(cli, "run_council", lambda **kwargs: (_ for _ in ()).throw(AssertionError()))

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 2
    assert "Budget rejected" in result.output
    assert all(row.get("kind") != "reservation" for row in _ledger(tmp_spend_dir)["runs"])


def test_force_skips_only_per_query_and_never_daily(tmp_spend_dir, tmp_path, monkeypatch):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli.reservations, "council_worst_case_cost", lambda profile: 6.0)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": "gen-force", "cost": 0.10})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)
    admitted = _invoke(CliRunner(), prompt_file, out_file, "--force")
    assert admitted.exit_code == 0, admitted.output

    monkeypatch.setattr(cli.reservations, "council_worst_case_cost", lambda profile: 40.0)
    refused = _invoke(CliRunner(), prompt_file, tmp_path / "second.md", "--force")
    assert refused.exit_code == 2
    assert "daily cap" in refused.output


def test_mark_dispatched_precedes_client_construction(
    tmp_spend_dir, tmp_path, monkeypatch
):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    events = []
    real_mark = budget.mark_dispatched

    def mark(reservation):
        real_mark(reservation)
        events.append("dispatched")

    monkeypatch.setattr(cli.budget, "mark_dispatched", mark)
    monkeypatch.setattr(cli, "OpenRouterClient", lambda **kwargs: _Client(events, **kwargs))

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": "gen-order", "cost": 0.10})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 0, result.output
    assert events == ["dispatched", "client"]


def test_accounting_failure_is_loud_and_nonzero(tmp_spend_dir, tmp_path, monkeypatch):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    def fail_actual(*args, **kwargs):
        raise budget.ReservationError("actual fsync failed")

    monkeypatch.setattr(cli.budget, "record_actual", fail_actual)

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": "gen-fail", "cost": 0.10})
        raise AssertionError("callback failure was swallowed")

    monkeypatch.setattr(cli, "run_council", run_council)

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code != 0
    assert "actual fsync failed" in result.output
    assert _ledger(tmp_spend_dir)["runs"][0]["status"] == "unknown"


def test_post_dispatch_render_failure_closes_unknown(
    tmp_spend_dir, tmp_path, monkeypatch
):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": "gen-render", "cost": 0.10})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)
    monkeypatch.setattr(
        cli,
        "_render_markdown",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("render failed")),
    )

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code == 3
    assert "render failed" in result.output
    assert _ledger(tmp_spend_dir)["runs"][0]["status"] == "unknown"


def test_close_accounting_failure_is_loud(tmp_spend_dir, tmp_path, monkeypatch):
    prompt_file, out_file = _prepare(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "OpenRouterClient", _Client)

    async def run_council(**kwargs):
        kwargs["on_attempt"]({"generation_id": "gen-close", "cost": 0.10})
        return _session()

    monkeypatch.setattr(cli, "run_council", run_council)
    monkeypatch.setattr(
        cli.budget,
        "close",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            budget.ReservationError("close fsync failed")
        ),
    )

    result = _invoke(CliRunner(), prompt_file, out_file)

    assert result.exit_code != 0
    assert "Spend accounting failed: close fsync failed" in result.output


def test_skip_budget_check_option_is_removed(tmp_path):
    prompt_file = tmp_path / "prompt.md"
    prompt_file.write_text("hello")

    result = _invoke(CliRunner(), prompt_file, tmp_path / "out.md", "--skip-budget-check")

    assert result.exit_code == 2
    assert "No such option: --skip-budget-check" in result.output


def test_cli_constructs_client_with_zero_transport_retries(tmp_path, tmp_spend_dir, monkeypatch):
    """Review finding (3d round 2, dangerously-wrong): the client's default transport
    retries (up to 3 HTTP dispatches per logical call) would let billed-but-timed-out
    requests escape the 13-call reservation bound AND the settled accounting — only the
    final logical result reaches on_attempt. The council gateway therefore forbids
    transport retries, exactly like the-oracle's guarded client (max_retries=0): one
    logical call is one HTTP dispatch, so the 13-call graph bound is honest."""
    from council import cli as cli_mod

    captured = {}

    class _CtorSpy:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            raise RuntimeError("stop before network")

    monkeypatch.setattr(cli_mod, "OpenRouterClient", _CtorSpy)
    prompt = tmp_path / "p.txt"
    prompt.write_text("q")

    from click.testing import CliRunner

    result = CliRunner().invoke(
        cli_mod.main,
        ["--profile", "variance", "--prompt-file", str(prompt),
         "--output", str(tmp_path / "o.md")],
    )

    assert result.exit_code == 3
    assert captured.get("max_retries") == 0


@pytest.mark.parametrize("bad_cost", [True, -0.5, float("inf"), float("nan")])
def test_cli_closes_unknown_on_each_unusable_cost_kind(
    tmp_path, tmp_spend_dir, monkeypatch, bad_cost
):
    """Review finding (3d round 2, minor): pin every unusable-cost kind, not just None."""
    from council import cli as cli_mod

    async def fake_run_council(**kwargs):
        on_attempt = kwargs["on_attempt"]
        on_attempt({"stage": "fanout", "requested_model": "m", "generation_id": "g1",
                    "cost": 0.01, "tokens_in": 1, "tokens_out": 1,
                    "returned_model_id": "m", "finish_reason": "stop"})
        on_attempt({"stage": "chairman", "requested_model": "m", "generation_id": "g2",
                    "cost": bad_cost, "tokens_in": 1, "tokens_out": 1,
                    "returned_model_id": "m", "finish_reason": "stop"})
        from council.pipeline import CouncilSession
        from council.client import ModelResponse
        return CouncilSession(
            id="s", profile=kwargs["profile"].name, tag=kwargs["tag"],
            user_query=kwargs["user_query"], responses=[], rankings=[],
            chairman_response=ModelResponse("m", "done", 1, 1, 1),
        )

    class _Client:
        def __init__(self, **kwargs):
            pass

        async def aclose(self):
            return None

    monkeypatch.setattr(cli_mod, "OpenRouterClient", _Client)
    monkeypatch.setattr(cli_mod, "run_council", fake_run_council)
    prompt = tmp_path / "p.txt"
    prompt.write_text("q")

    from click.testing import CliRunner
    import json as json_mod

    result = CliRunner().invoke(
        cli_mod.main,
        ["--profile", "variance", "--prompt-file", str(prompt),
         "--output", str(tmp_path / "o.md")],
    )

    assert result.exit_code == 0, result.output
    day_file = next(tmp_spend_dir.glob("council-spend-*.json"))
    data = json_mod.loads(day_file.read_text())
    row = [r for r in data["runs"] if r.get("kind") == "reservation"][0]
    assert row["status"] == "unknown"
    unknown_actuals = [a for a in data["actuals"] if a["status"] == "unknown"]
    assert len(unknown_actuals) == 1 and unknown_actuals[0]["usage_cost"] is None
