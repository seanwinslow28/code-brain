"""Tests for daily_driver auth-status resolution + headless OAuth env injection.

Telemetry fix: a 401 was observed 2026-06-20 as a ResultMessage with
subtype="success" and the error buried in `.result` (cost=$0, 1 turn). That
recorded a green ✓ in the fleet digest. `_resolve_status` downgrades such runs
to "error_auth" so auth failures stop masquerading as successes.
"""

from __future__ import annotations

import types

from agents.daily_driver import _resolve_status
from lib.auth import OAUTH_TOKEN_ENV


def _msg(subtype, result):
    return types.SimpleNamespace(subtype=subtype, result=result)


# --- _resolve_status ---------------------------------------------------------

def test_auth_failure_downgraded_even_when_subtype_success():
    m = _msg(
        "success",
        'Failed to authenticate. API Error: 401 {"type":"error",'
        '"error":{"type":"authentication_error",'
        '"message":"Invalid authentication credentials"}}',
    )
    assert _resolve_status(m) == "error_auth"


def test_plain_success_passes_through():
    assert _resolve_status(_msg("success", "Morning planning complete.")) == "success"


def test_none_message_is_unknown():
    assert _resolve_status(None) == "unknown"


def test_budget_cap_subtype_passes_through():
    assert (
        _resolve_status(_msg("error_max_budget_usd", "Command failed"))
        == "error_max_budget_usd"
    )


def test_none_result_text_is_safe():
    assert _resolve_status(_msg("success", None)) == "success"


# --- build_options OAuth injection ------------------------------------------

def test_build_options_injects_oauth_token_when_no_api_key(monkeypatch, tmp_config):
    from agents.daily_driver import build_options
    from lib.config import load_config

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv(OAUTH_TOKEN_ENV, "tok-headless")
    cfg = load_config(config_path=tmp_config)
    assert cfg.anthropic_api_key is None

    opts = build_options(cfg, mode="morning")
    assert opts.env.get(OAUTH_TOKEN_ENV) == "tok-headless"


def test_build_options_prefers_api_key_over_oauth(monkeypatch, tmp_config):
    from agents.daily_driver import build_options
    from lib.config import load_config

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-xyz")
    monkeypatch.setenv(OAUTH_TOKEN_ENV, "tok-headless")
    cfg = load_config(config_path=tmp_config)

    opts = build_options(cfg, mode="morning")
    assert opts.env.get("ANTHROPIC_API_KEY") == "sk-ant-xyz"
    assert OAUTH_TOKEN_ENV not in opts.env
