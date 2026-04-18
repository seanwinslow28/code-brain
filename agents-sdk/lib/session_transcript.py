"""Parse Claude Code session transcripts (JSONL).

Transcripts live at:
    ~/.claude/projects/<slug>/<session-id>.jsonl

Each line is one JSON object with a `type` field:
    file-history-snapshot — metadata, skip
    user                  — user message
    assistant             — assistant message with content array

Assistant `message.content` is a list of blocks with their own `type`:
    text, thinking, tool_use, tool_result, redacted_thinking

This module exposes `parse_transcript`, `message_count`, and
`extract_tool_calls` for flush.py and other downstream consumers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

_MESSAGE_TYPES = frozenset({"user", "assistant"})


@dataclass
class ToolCall:
    tool_use_id: str
    name: str
    input: dict
    timestamp: str = ""


@dataclass
class TranscriptMessage:
    role: str  # "user" or "assistant"
    uuid: str
    timestamp: str
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


def _extract_text(content: object) -> str:
    """Pull the concatenated user-visible text out of a message content field.

    CC stores user messages as either a plain string or a list of blocks.
    Assistant messages are always a list of blocks.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return ""


def _extract_tool_calls_from_message(message: dict, timestamp: str) -> list[ToolCall]:
    content = message.get("content")
    if not isinstance(content, list):
        return []
    calls: list[ToolCall] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        calls.append(
            ToolCall(
                tool_use_id=block.get("id", ""),
                name=block.get("name", ""),
                input=block.get("input", {}) or {},
                timestamp=timestamp,
            )
        )
    return calls


def parse_transcript(path: Path) -> list[TranscriptMessage]:
    """Parse a JSONL transcript into a list of TranscriptMessage.

    Skips file-history-snapshot and other non-message entries.
    Malformed JSON lines are skipped (logged would be nice; not critical).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Transcript not found: {p}")

    messages: list[TranscriptMessage] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        entry_type = entry.get("type")
        if entry_type not in _MESSAGE_TYPES:
            continue

        msg = entry.get("message", {})
        timestamp = entry.get("timestamp", "")
        messages.append(
            TranscriptMessage(
                role=entry_type,
                uuid=entry.get("uuid", ""),
                timestamp=timestamp,
                text=_extract_text(msg.get("content")),
                tool_calls=_extract_tool_calls_from_message(msg, timestamp),
                raw=entry,
            )
        )
    return messages


def message_count(path: Path) -> int:
    """Count user + assistant messages (excluding snapshots and malformed lines)."""
    return len(parse_transcript(path))


def extract_tool_calls(path: Path) -> list[ToolCall]:
    """Flatten all assistant tool_use blocks across the transcript."""
    calls: list[ToolCall] = []
    for m in parse_transcript(path):
        calls.extend(m.tool_calls)
    return calls
