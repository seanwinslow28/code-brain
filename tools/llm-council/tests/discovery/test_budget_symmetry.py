"""Budget isolation symmetry: discovery spend must not reject a council run.

Counterpart to discovery's own per-tool budget scoping. The council CLI uses
``preflight_tool(..., tool="council")``, so a large *discovery* spend on the same
day cannot consume council's headroom (and vice versa). The aggregate ``preflight``
still exists for its own unit tests but is no longer wired into the CLI.

Red-then-green: with the old aggregate ``preflight``, $9.50 of discovery spend
exceeds council's $7 daily cap and rejects the run (exit 2). With per-tool
preflight, council's own spend is $0 and the run passes (exit 0).
"""

from datetime import date

from click.testing import CliRunner

from council import budget


def test_large_discovery_spend_does_not_reject_council_run(
    tmp_spend_dir, fake_api_key, tmp_path, monkeypatch
):
    # Approach A: use the real "today" so record_spend and the CLI's preflight_tool
    # read/write the same daily spend file regardless of wall-clock date.
    d = date.today()

    # Discovery has spent $9.50 today: well over council's $7 daily aggregate,
    # but under discovery's own $10 cap. Tagged tool="discovery".
    budget.record_spend(
        amount=9.50, profile="standard", tag="disc", on_date=d, tool="discovery"
    )

    from council import cli

    async def fake_run(**kw):
        from council.client import ModelResponse
        from council.pipeline import CouncilSession

        # Small non-zero token counts so _render_markdown + the post-run cost math
        # don't crash; empty list fields so the markdown loops render cleanly.
        return CouncilSession(
            id="sess-symmetry",
            profile=kw["profile"].name,
            tag=kw["tag"],
            user_query=kw["user_query"],
            responses=[],
            rankings=[],
            chairman_response=ModelResponse(
                model_id="chair",
                content="Synthesis.",
                tokens_in=1,
                tokens_out=1,
                latency_ms=1,
            ),
            dropped_models=[],
            ranking_failed_models=[],
            total_tokens_in=1,
            total_tokens_out=1,
            duration_ms=1,
        )

    monkeypatch.setattr(cli, "run_council", fake_run)

    prompt = tmp_path / "p.txt"
    prompt.write_text("hello")
    out = tmp_path / "o.md"

    res = CliRunner().invoke(
        cli.main,
        [
            "--profile", "variance",
            "--prompt-file", str(prompt),
            "--output", str(out),
            "--tag", "t",
        ],
    )

    assert res.exit_code == 0, res.output
    assert "Budget rejected" not in res.output


def test_prior_day_discovery_spend_does_not_deplete_council_monthly(tmp_spend_dir):
    # A large discovery spend earlier this month must not reduce council's monthly headroom.
    budget.record_spend(
        amount=30.0, profile="standard", tag="d", on_date=date(2026, 6, 10), tool="discovery"
    )
    budget.preflight_tool(
        estimated=0.50, per_query_cap=1.00, daily_cap=7.0, monthly_cap=40.0,
        on_date=date(2026, 6, 20), tool="council",
    )  # must not raise
    assert budget.tool_total_for_month(date(2026, 6, 20), "discovery") == 30.0
    assert budget.tool_total_for_month(date(2026, 6, 20), "council") == 0.0
