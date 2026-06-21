"""Tests for headless OAuth token resolution (lib/auth.py).

Covers the durable-auth fix for the 2026-06-20 daily-driver 401: scheduled
launchd runs can't refresh the interactive `claude login` credential, so a
long-lived `claude setup-token` token (Keychain) is preferred when present.
"""

from __future__ import annotations

from lib.auth import OAUTH_TOKEN_CREDENTIAL, OAUTH_TOKEN_ENV, resolve_oauth_token


def test_returns_env_token_when_set(monkeypatch):
    monkeypatch.setenv(OAUTH_TOKEN_ENV, "tok-from-env")
    called = {"n": 0}

    def fake_get(name):  # keychain must NOT be consulted when env is set
        called["n"] += 1
        return "tok-from-keychain"

    assert resolve_oauth_token(keychain_get=fake_get) == "tok-from-env"
    assert called["n"] == 0


def test_falls_back_to_keychain_when_env_unset(monkeypatch):
    monkeypatch.delenv(OAUTH_TOKEN_ENV, raising=False)
    assert (
        resolve_oauth_token(keychain_get=lambda name: "tok-from-keychain")
        == "tok-from-keychain"
    )


def test_keychain_queried_with_expected_credential_name(monkeypatch):
    monkeypatch.delenv(OAUTH_TOKEN_ENV, raising=False)
    seen = {}

    def fake_get(name):
        seen["name"] = name
        return None

    resolve_oauth_token(keychain_get=fake_get)
    assert seen["name"] == OAUTH_TOKEN_CREDENTIAL == "claude_code_oauth_token"


def test_returns_none_when_neither_set(monkeypatch):
    monkeypatch.delenv(OAUTH_TOKEN_ENV, raising=False)
    assert resolve_oauth_token(keychain_get=lambda name: None) is None
