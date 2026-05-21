from pathlib import Path

from lib.cli_runners import CLIResponse, parse_codex_tokens

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


def test_cliresponse_holds_response_and_meta():
    r = CLIResponse(
        cli="codex",
        text="hello world",
        tokens=123,
        duration_s=1.5,
        exit_code=0,
        rate_capped=False,
        error=None,
    )
    assert r.cli == "codex"
    assert r.text == "hello world"
    assert r.tokens == 123
    assert r.ok is True


def test_cliresponse_ok_false_when_exit_nonzero():
    r = CLIResponse(cli="codex", text="", tokens=None, duration_s=0.1,
                    exit_code=1, rate_capped=False, error="boom")
    assert r.ok is False


def test_cliresponse_ok_false_when_rate_capped():
    r = CLIResponse(cli="codex", text="", tokens=None, duration_s=0.1,
                    exit_code=0, rate_capped=True, error=None)
    assert r.ok is False


def test_cliresponse_ok_false_when_error_set_with_clean_exit():
    """A2/A6 wrappers can set `error` on soft failures (e.g., malformed JSON)
    while exit_code is 0 and rate_capped is False — `ok` must still be False."""
    r = CLIResponse(cli="antigravity", text="", tokens=None, duration_s=0.1,
                    exit_code=0, rate_capped=False, error="json parse failed")
    assert r.ok is False
