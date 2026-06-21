import asyncio
from click.testing import CliRunner
from council.discovery.__main__ import main
from council.discovery.pipeline import DiscoveryResult


def test_cli_writes_ledger(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "ledger.md"

    async def fake_run(**kw):
        return DiscoveryResult(markdown="# Idea Ledger — x\nok", cost_usd=0.42,
                               verified_count=1, dropped_count=0, session={"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "roadmap tools", "--lens", "pm", "--tier", "quick",
        "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert out.read_text().startswith("# Idea Ledger")
    assert "0.42" in res.output


def test_cli_deep_requires_confirmation(tmp_path, monkeypatch, fake_api_key):
    async def fake_run(**kw):
        return DiscoveryResult("md", 3.0, 1, 0, {"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)
    res = CliRunner().invoke(main, [
        "x", "--tier", "deep", "--output", str(tmp_path / "o.md"),
        "--skip-budget-check",
    ], input="n\n")
    assert res.exit_code != 0 or "aborted" in res.output.lower()


def test_cli_writes_substack_brief(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "2026-06-20-x-substack-idea-ledger.md"

    async def fake_run(**kw):
        return DiscoveryResult(markdown="# Substack Idea Ledger — x\n", cost_usd=0.4,
                               verified_count=1, dropped_count=0, session={"id": "s"},
                               brief_markdown="# Substack Handoff Brief — x\n- Itch: ...")
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "substack", "--tier", "quick", "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    brief = tmp_path / "2026-06-20-x-substack-brief.md"
    assert brief.exists()
    assert "Handoff Brief" in brief.read_text()
    assert "brief" in res.output.lower()


def test_cli_pm_lens_writes_no_brief(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "led.md"

    async def fake_run(**kw):
        return DiscoveryResult("# Idea Ledger — x\n", 0.4, 1, 0, {"id": "s"})  # brief_markdown="" default
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "pm", "--tier", "quick", "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert not (tmp_path / "led-brief.md").exists()


def test_cli_passes_segment_to_pipeline(tmp_path, monkeypatch, fake_api_key):
    captured = {}

    async def fake_run(**kw):
        captured.update(kw)
        return DiscoveryResult("# Idea Ledger — x\n", 0.1, 0, 0, {"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "pm", "--tier", "quick", "--segment", "designers",
        "--output", str(tmp_path / "o.md"), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert captured["segment"] == "designers"


def test_cli_records_spend_and_echoes_status_on_failure(tmp_path, monkeypatch, fake_api_key, tmp_spend_dir):
    from datetime import date
    from council import budget
    from council.discovery.pipeline import DiscoveryFailed

    async def boom(**kw):
        raise DiscoveryFailed("fuse blew up", cost_usd=0.42,
                              session={"gather_status": {"sonar": "ok: 3 records (3 found)"}})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", boom)

    res = CliRunner().invoke(main, [
        "obsidian", "--lens", "pm", "--tier", "quick", "--output", str(tmp_path / "o.md"),
    ])
    assert res.exit_code == 3
    assert "Gather status" in res.output
    assert round(budget.tool_total_for_day(date.today(), "discovery"), 2) == 0.42
