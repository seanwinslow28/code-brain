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
