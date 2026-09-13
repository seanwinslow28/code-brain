"""Tests for the keychain CLI, in particular `set --stdin`.

Filed 2026-09-13: installing the headless `claude setup-token` credential kept
failing with `zsh: parse error near '\\n'` because `set` took the secret as an
argv, so the shell had to parse it. A truncated 34-character token sat in the
Keychain for months looking healthy and returning 401. The stdin path keeps the
secret off the command line (and out of `~/.zsh_history`) entirely.
"""

from __future__ import annotations

import io

import pytest

from lib import keychain

TOKEN = "sk-ant-oat01-" + "A" * 80


@pytest.fixture
def stored(monkeypatch):
    """Capture set_credential calls instead of touching the real Keychain."""
    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(keychain, "set_credential", lambda n, v: calls.append((n, v)))
    return calls


def _stdin(monkeypatch, text: str) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO(text))


def test_set_stdin_stores_value_from_stdin(stored, monkeypatch, capsys):
    _stdin(monkeypatch, TOKEN + "\n")
    keychain._cli(["set", "--stdin", "claude_code_oauth_token"])
    assert stored == [("claude_code_oauth_token", TOKEN)]
    assert TOKEN not in capsys.readouterr().out  # never echo the secret


def test_set_stdin_reports_length_so_truncation_is_visible(stored, monkeypatch, capsys):
    _stdin(monkeypatch, TOKEN + "\n")
    keychain._cli(["set", "--stdin", "claude_code_oauth_token"])
    assert f"{len(TOKEN)} chars" in capsys.readouterr().out


def test_set_argv_also_reports_length(stored, capsys):
    keychain._cli(["set", "claude_code_oauth_token", TOKEN])
    assert stored == [("claude_code_oauth_token", TOKEN)]
    assert f"{len(TOKEN)} chars" in capsys.readouterr().out


def test_set_stdin_strips_only_the_trailing_newline(stored, monkeypatch):
    _stdin(monkeypatch, TOKEN + "\r\n")
    keychain._cli(["set", "--stdin", "tok"])
    assert stored == [("tok", TOKEN)]


def test_set_stdin_preserves_interior_characters(stored, monkeypatch):
    value = "a-b_c.d/e+f=g"
    _stdin(monkeypatch, value + "\n")
    keychain._cli(["set", "--stdin", "tok"])
    assert stored == [("tok", value)]


def test_set_stdin_rejects_empty_input(stored, monkeypatch):
    _stdin(monkeypatch, "\n")
    with pytest.raises(SystemExit) as exc:
        keychain._cli(["set", "--stdin", "tok"])
    assert exc.value.code != 0
    assert stored == []


def test_set_stdin_rejects_an_interior_newline(stored, monkeypatch):
    # Pasting a whole terminal transcript instead of just the token is exactly
    # how the 34-character truncation happened. Refuse rather than store junk.
    _stdin(monkeypatch, f"Your token is:\n{TOKEN}\n")
    with pytest.raises(SystemExit) as exc:
        keychain._cli(["set", "--stdin", "tok"])
    assert exc.value.code != 0
    assert stored == []


def test_set_stdin_rejects_a_positional_value(stored, monkeypatch):
    _stdin(monkeypatch, TOKEN + "\n")
    with pytest.raises(SystemExit) as exc:
        keychain._cli(["set", "--stdin", "tok", TOKEN])
    assert exc.value.code != 0
    assert stored == []


def test_set_without_stdin_flag_still_requires_a_value(stored):
    with pytest.raises(SystemExit) as exc:
        keychain._cli(["set", "tok"])
    assert exc.value.code != 0
    assert stored == []


def test_usage_line_mentions_the_stdin_form(capsys):
    with pytest.raises(SystemExit):
        keychain._cli([])
    assert "--stdin" in capsys.readouterr().out
