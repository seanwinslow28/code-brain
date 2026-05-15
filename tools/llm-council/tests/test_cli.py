import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from council.cli import main
from council.client import ModelResponse


def _r(model: str, content: str) -> ModelResponse:
    return ModelResponse(model_id=model, content=content, tokens_in=10, tokens_out=10, latency_ms=10)


def test_cli_help_shows_profiles(fake_api_key):
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "premium" in result.output or "profile" in result.output.lower()


def test_cli_writes_markdown_output(fake_api_key, tmp_path, tmp_spend_dir, monkeypatch):
    prompt_file = tmp_path / "in.md"
    prompt_file.write_text("What's the best way to test async code?")
    out_file = tmp_path / "out.md"

    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    fake_responses = [
        _r("m1", "Use pytest-asyncio."),
        _r("m2", "Use anyio."),
        _r("m3", "Use trio test."),
        _r("m4", "Use unittest IsolatedAsyncioTestCase."),
        _r("m1", valid), _r("m2", valid), _r("m3", valid), _r("m4", valid),
        _r("m1", "Synthesis: pytest-asyncio is most idiomatic..."),
    ]

    with patch("council.cli.OpenRouterClient") as mock_client_cls, \
         patch("council.cli.get_profile") as mock_get_profile:
        from council.profiles import Profile
        mock_get_profile.return_value = Profile(
            name="variance", models=("m1","m2","m3","m4"), chairman="m1", max_cost_per_query=10.0,
        )
        mock_inst = MagicMock()
        mock_inst.complete = AsyncMock(side_effect=fake_responses)
        mock_inst.aclose = AsyncMock()
        mock_client_cls.return_value = mock_inst

        runner = CliRunner()
        result = runner.invoke(main, [
            "--profile", "variance",
            "--prompt-file", str(prompt_file),
            "--output", str(out_file),
            "--tag", "test-tag",
            "--skip-budget-check",
        ])

    assert result.exit_code == 0, result.output
    assert out_file.exists()
    text = out_file.read_text()
    assert "What's the best way to test async code?" in text  # original prompt
    assert "Use pytest-asyncio." in text                       # m1 response
    assert "Synthesis: pytest-asyncio is most idiomatic..." in text  # chairman
    assert "test-tag" in text                                  # tag echoed


def test_cli_exits_nonzero_on_missing_prompt_file(fake_api_key, tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "--profile", "variance",
        "--prompt-file", str(tmp_path / "missing.md"),
        "--output", str(tmp_path / "out.md"),
        "--tag", "x",
    ])
    assert result.exit_code != 0
