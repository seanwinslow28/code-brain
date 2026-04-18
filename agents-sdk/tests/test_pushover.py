"""Tests for lib.pushover — Pushover push-notification helper."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from lib.pushover import (
    PushoverError,
    notify_wol_failure,
    send_push,
)


def _mock_ok_response() -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = 200
    resp.json.return_value = {"status": 1, "request": "abc"}
    resp.raise_for_status.return_value = None
    return resp


@patch("lib.pushover.get_credential")
@patch("lib.pushover.httpx.post")
def test_send_push_reads_keychain_and_posts(
    mock_post: MagicMock, mock_get_cred: MagicMock
) -> None:
    mock_get_cred.side_effect = lambda name: {
        "pushover_user_key": "USER_KEY",
        "pushover_app_token": "APP_TOKEN",
    }[name]
    mock_post.return_value = _mock_ok_response()

    send_push(title="Test", message="Hello")

    mock_post.assert_called_once()
    url = mock_post.call_args[0][0]
    assert "pushover.net" in url
    data = mock_post.call_args.kwargs["data"]
    assert data["token"] == "APP_TOKEN"
    assert data["user"] == "USER_KEY"
    assert data["title"] == "Test"
    assert data["message"] == "Hello"


@patch("lib.pushover.get_credential")
def test_send_push_missing_credentials_raises(mock_get_cred: MagicMock) -> None:
    mock_get_cred.return_value = None
    with pytest.raises(PushoverError, match="credentials"):
        send_push(title="X", message="Y")


@patch("lib.pushover.get_credential")
@patch("lib.pushover.httpx.post")
def test_send_push_http_error_raises(
    mock_post: MagicMock, mock_get_cred: MagicMock
) -> None:
    mock_get_cred.side_effect = lambda name: "FAKE"
    bad = MagicMock(spec=httpx.Response)
    bad.status_code = 500
    bad.text = "server error"
    bad.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500", request=MagicMock(), response=bad
    )
    mock_post.return_value = bad
    with pytest.raises(PushoverError):
        send_push(title="X", message="Y")


@patch("lib.pushover.send_push")
def test_notify_wol_failure_formats_body(mock_send: MagicMock) -> None:
    notify_wol_failure(task="vault_synthesis", machine="macbook_pro")
    mock_send.assert_called_once()
    kwargs = mock_send.call_args.kwargs
    assert "WOL" in kwargs["title"] or "unreachable" in kwargs["title"].lower()
    assert "vault_synthesis" in kwargs["message"]
    assert "macbook_pro" in kwargs["message"]


@patch("lib.pushover.get_credential")
@patch("lib.pushover.httpx.post")
def test_send_push_priority_passed_through(
    mock_post: MagicMock, mock_get_cred: MagicMock
) -> None:
    mock_get_cred.side_effect = lambda name: "FAKE"
    mock_post.return_value = _mock_ok_response()
    send_push(title="X", message="Y", priority=1)
    data = mock_post.call_args.kwargs["data"]
    assert data["priority"] == 1
