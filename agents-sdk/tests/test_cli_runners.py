import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from lib.cli_runners import (
    CLIResponse,
    detect_rate_cap,
    parse_codex_tokens,
    run_antigravity,
    run_codex,
)

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


def _fake_proc(stdout_bytes: bytes, stderr_bytes: bytes, returncode: int = 0):
    """Return a mocked asyncio subprocess that emits the given bytes."""
    proc = AsyncMock()
    proc.communicate = AsyncMock(return_value=(stdout_bytes, stderr_bytes))
    proc.returncode = returncode
    return proc


def test_run_codex_replays_smoke_fixture():
    stdout = (FIXTURES / "codex-out.txt").read_bytes()
    stderr = (FIXTURES / "codex-err.txt").read_bytes()

    async def go():
        fake = _fake_proc(stdout, stderr, returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=60)

    resp = asyncio.run(go())
    assert resp.cli == "codex"
    assert resp.tokens == 17182
    assert resp.exit_code == 0
    assert resp.rate_capped is False
    # The Codex stdout fixture starts with "1. **Add..."; assert we captured it.
    assert resp.text.startswith("1. **Add")
    assert resp.ok is True


def test_run_codex_timeout_returns_error_not_raise():
    async def go():
        async def slow_communicate():
            await asyncio.sleep(10)
            return (b"", b"")
        fake = AsyncMock()
        fake.communicate = slow_communicate
        fake.returncode = None
        fake.kill = MagicMock()
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=0.05)

    resp = asyncio.run(go())
    assert resp.ok is False
    assert resp.error is not None
    assert "timeout" in resp.error.lower()


def test_run_codex_rate_cap_marks_response_capped():
    async def go():
        fake = _fake_proc(b"", b"Error: rate limit exceeded", returncode=1)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.rate_capped is True
    assert resp.ok is False


def test_run_antigravity_replays_smoke_fixture():
    stdout = (FIXTURES / "gemini-out.json").read_bytes()
    stderr = (FIXTURES / "gemini-err.txt").read_bytes()

    async def go():
        fake = _fake_proc(stdout, stderr, returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)) as create:
            resp = await run_antigravity("any prompt", timeout_s=60)
            # Verify the env var was set on the subprocess call
            kwargs = create.call_args.kwargs
            assert "env" in kwargs, "env dict was not passed as kwarg to create_subprocess_exec"
            env = kwargs["env"]
            assert env.get("GEMINI_CLI_TRUST_WORKSPACE") == "true"
            return resp

    resp = asyncio.run(go())
    assert resp.cli == "antigravity"
    assert resp.exit_code == 0
    assert resp.rate_capped is False
    # The response field starts with "### 1. Surgical Cultural Synthesis"
    assert resp.text.startswith("### 1. Surgical Cultural Synthesis")
    # Token total from stats.models["gemini-3.1-pro-preview"].tokens.total
    assert resp.tokens == 15746
    assert resp.ok is True


def test_run_antigravity_malformed_json_marks_error():
    async def go():
        fake = _fake_proc(b"not json at all", b"", returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_antigravity("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.ok is False
    assert resp.error is not None
    assert "json" in resp.error.lower()


def test_run_antigravity_extracts_routed_model_from_stats():
    """Don't hardcode gemini-3.1-pro-preview — read from stats.models keys."""
    payload = {
        "session_id": "abc",
        "response": "body",
        "stats": {
            "models": {
                "gemini-4.0-pro-preview": {  # hypothetical future model
                    "tokens": {"total": 999}
                }
            }
        },
    }
    async def go():
        fake = _fake_proc(json.dumps(payload).encode(), b"", returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_antigravity("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.tokens == 999
