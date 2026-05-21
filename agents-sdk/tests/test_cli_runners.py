from pathlib import Path

from lib.cli_runners import CLIResponse, detect_rate_cap, parse_codex_tokens

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


def test_detect_rate_cap_codex_429_signature():
    # Anecdotal Codex rate-cap shape: "rate limit" or "quota" in stderr.
    assert detect_rate_cap("codex", "error: rate limit exceeded") is True
    assert detect_rate_cap("codex", "Error: 429 Too Many Requests") is True
    assert detect_rate_cap("codex", "your daily quota has been reached") is True


def test_detect_rate_cap_antigravity_shape():
    # Anti-Gravity surfaces quota errors as JSON-formatted stderr; the wrapper
    # also checks for "RESOURCE_EXHAUSTED" and "quota" in any case.
    assert detect_rate_cap("antigravity", "RESOURCE_EXHAUSTED: Quota exceeded") is True
    assert detect_rate_cap("antigravity", "rate limit hit, try again later") is True


def test_detect_rate_cap_negative_on_normal_stderr():
    # Smoke-test stderr was clean — no false positive.
    normal = (FIXTURES / "codex-err.txt").read_text(encoding="utf-8")
    assert detect_rate_cap("codex", normal) is False
