"""Tests for the flush.py --trigger argparse argument (Phase A).

Verifies that a `--trigger {session-end,pre-compact,manual}` flag flows
into `session_summary["tag"]` in the rendered daily-log block, and that
argparse rejects unknown trigger values.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from agents.flush import RoutingTier, run_flush

REPO_ROOT = Path(__file__).resolve().parents[2]
FLUSH_SCRIPT = REPO_ROOT / "agents-sdk" / "agents" / "flush.py"


def _make_transcript(path: Path, n_messages: int) -> Path:
    entries = [{"type": "file-history-snapshot", "snapshot": {}}]
    for i in range(n_messages):
        role = "user" if i % 2 == 0 else "assistant"
        content = f"m{i}" if role == "user" else [{"type": "text", "text": f"m{i}"}]
        entries.append(
            {
                "type": role,
                "uuid": f"{role[0]}{i}",
                "timestamp": f"2026-04-25T10:{i // 60:02d}:{i % 60:02d}Z",
                "message": {"role": role, "content": content},
            }
        )
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
    return path


def _fake_llm(prompt: str, tier: RoutingTier) -> dict:
    return {
        "decisions": ["D1"],
        "lessons": ["L1"],
        "actions": ["A1"],
        "patterns": ["P1"],
        "quotes": ["Q1"],
    }


def test_run_flush_default_trigger_is_session_end(tmp_path: Path) -> None:
    """Calling run_flush without specifying trigger writes tag: session-end."""
    transcript = _make_transcript(tmp_path / "t.jsonl", 20)
    result = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=_fake_llm,
    )
    assert result.status == "ok"
    daily_path = tmp_path / "vault" / "daily" / f"{result.date}.md"
    text = daily_path.read_text(encoding="utf-8")
    assert "tag: session-end" in text


def test_run_flush_trigger_pre_compact_threads_into_tag(tmp_path: Path) -> None:
    """trigger='pre-compact' shows up as `tag: pre-compact` in the daily log."""
    transcript = _make_transcript(tmp_path / "t.jsonl", 20)
    result = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=_fake_llm,
        trigger="pre-compact",
    )
    assert result.status == "ok"
    daily_path = tmp_path / "vault" / "daily" / f"{result.date}.md"
    text = daily_path.read_text(encoding="utf-8")
    assert "tag: pre-compact" in text
    assert "tag: session-end" not in text


def test_run_flush_trigger_manual_threads_into_tag(tmp_path: Path) -> None:
    """trigger='manual' shows up as `tag: manual` in the daily log."""
    transcript = _make_transcript(tmp_path / "t.jsonl", 20)
    result = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=_fake_llm,
        trigger="manual",
    )
    assert result.status == "ok"
    daily_path = tmp_path / "vault" / "daily" / f"{result.date}.md"
    text = daily_path.read_text(encoding="utf-8")
    assert "tag: manual" in text


def test_cli_accepts_known_triggers(tmp_path: Path) -> None:
    """argparse accepts the three valid --trigger values without an `invalid choice` error."""
    for trig in ("session-end", "pre-compact", "manual"):
        proc = subprocess.run(
            [sys.executable, str(FLUSH_SCRIPT), "--trigger", trig, "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={
                "PYTHONPATH": str(REPO_ROOT / "agents-sdk"),
                "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin",
            },
        )
        assert "invalid choice" not in proc.stderr.lower(), (
            f"--trigger {trig} rejected by argparse: stderr={proc.stderr!r}"
        )
        assert "unrecognized arguments" not in proc.stderr.lower(), (
            f"--trigger {trig} unrecognized by argparse: stderr={proc.stderr!r}"
        )


def test_cli_rejects_unknown_trigger() -> None:
    """argparse rejects --trigger values outside the choices set."""
    proc = subprocess.run(
        [sys.executable, str(FLUSH_SCRIPT), "--trigger", "bogus", "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={
            "PYTHONPATH": str(REPO_ROOT / "agents-sdk"),
            "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin",
        },
    )
    assert proc.returncode == 2
    assert "invalid choice" in proc.stderr.lower() or "bogus" in proc.stderr.lower()
