from pathlib import Path

from lib.cli_runners import parse_codex_tokens

FIXTURES = Path(__file__).parent / "fixtures" / "critic"


def test_parse_codex_tokens_from_real_stderr():
    stderr_text = (FIXTURES / "codex-err.txt").read_text(encoding="utf-8")
    tokens = parse_codex_tokens(stderr_text)
    assert tokens == 17182


def test_parse_codex_tokens_missing_footer_returns_none():
    assert parse_codex_tokens("no tokens used line here") is None
    assert parse_codex_tokens(None) is None  # guard against None stderr from asyncio


def test_parse_codex_tokens_handles_comma_thousands():
    # Codex prints 17,182 not 17182 in some terminals — match either.
    assert parse_codex_tokens("tokens used\n17,182\n") == 17182
