"""Tests for lib.session_transcript — CC JSONL transcript parser."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib.session_transcript import (
    TranscriptMessage,
    extract_tool_calls,
    message_count,
    parse_transcript,
)


def _write_transcript(path: Path, entries: list[dict]) -> Path:
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def short_transcript(tmp_path: Path) -> Path:
    return _write_transcript(
        tmp_path / "short.jsonl",
        [
            {
                "type": "file-history-snapshot",
                "messageId": "x",
                "snapshot": {},
            },
            {
                "type": "user",
                "uuid": "u1",
                "timestamp": "2026-04-17T10:00:00Z",
                "message": {"role": "user", "content": "hello"},
            },
            {
                "type": "assistant",
                "uuid": "a1",
                "timestamp": "2026-04-17T10:00:05Z",
                "message": {
                    "role": "assistant",
                    "model": "claude-opus-4-7",
                    "content": [
                        {"type": "text", "text": "hi"},
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "Read",
                            "input": {"file_path": "/x"},
                        },
                    ],
                },
            },
            {
                "type": "user",
                "uuid": "u2",
                "timestamp": "2026-04-17T10:00:10Z",
                "message": {"role": "user", "content": "ok"},
            },
        ],
    )


def test_parse_jsonl_returns_messages_only(short_transcript: Path) -> None:
    msgs = parse_transcript(short_transcript)
    # 3 real messages (file-history-snapshot excluded)
    assert len(msgs) == 3
    assert all(isinstance(m, TranscriptMessage) for m in msgs)
    assert [m.role for m in msgs] == ["user", "assistant", "user"]


def test_message_count_excludes_snapshots(short_transcript: Path) -> None:
    assert message_count(short_transcript) == 3


def test_extract_tool_calls(short_transcript: Path) -> None:
    calls = extract_tool_calls(short_transcript)
    assert len(calls) == 1
    assert calls[0].name == "Read"
    assert calls[0].input == {"file_path": "/x"}
    assert calls[0].tool_use_id == "t1"


def test_parse_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        parse_transcript(tmp_path / "nope.jsonl")


def test_extract_text_content(short_transcript: Path) -> None:
    msgs = parse_transcript(short_transcript)
    assistant = next(m for m in msgs if m.role == "assistant")
    assert assistant.text == "hi"
    user = next(m for m in msgs if m.role == "user")
    assert user.text == "hello"


def test_message_count_large(tmp_path: Path) -> None:
    """Sanity check with a 200-message transcript for routing-threshold math."""
    entries = [{"type": "file-history-snapshot", "snapshot": {}}]
    for i in range(200):
        role = "user" if i % 2 == 0 else "assistant"
        msg = {"role": role, "content": f"m{i}"} if role == "user" else {
            "role": role,
            "content": [{"type": "text", "text": f"m{i}"}],
        }
        entries.append(
            {
                "type": role,
                "uuid": f"{role[0]}{i}",
                "timestamp": f"2026-04-17T10:{i // 60:02d}:{i % 60:02d}Z",
                "message": msg,
            }
        )
    path = _write_transcript(tmp_path / "big.jsonl", entries)
    assert message_count(path) == 200
