"""Tests for agents.flush — SessionEnd daily-log extractor."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch

import pytest

from agents.flush import (
    DAILY_LOG_TEMPLATE_HEADER,
    EXTRACTION_PROMPT,
    FlushResult,
    RoutingTier,
    append_to_daily_log,
    build_soul_prepend,
    format_daily_log_body,
    pick_routing_tier,
    run_flush,
)
from lib.artifact_loader import clear_cache


@pytest.fixture(autouse=True)
def _reset_artifact_cache():
    clear_cache()
    yield
    clear_cache()


@dataclass
class _FakeConfig:
    """Stand-in for lib.config.Config — fields the flush path touches."""

    vault_root: Path
    artifacts: dict = field(default_factory=dict)

    def artifact_config(self, name: str) -> dict:
        if not self.artifacts.get("enabled", False):
            return {}
        return self.artifacts.get("per_agent", {}).get(name, {})


def _flush_config(tmp_artifacts: Path, *, enabled: bool = True, on_demand=("SOUL",)) -> _FakeConfig:
    return _FakeConfig(
        vault_root=tmp_artifacts,
        artifacts={
            "enabled": enabled,
            "per_agent": {"flush": {"on_demand": list(on_demand)}},
        },
    )


def _make_transcript(path: Path, n_messages: int) -> Path:
    entries = [{"type": "file-history-snapshot", "snapshot": {}}]
    for i in range(n_messages):
        role = "user" if i % 2 == 0 else "assistant"
        content = f"m{i}" if role == "user" else [{"type": "text", "text": f"m{i}"}]
        entries.append(
            {
                "type": role,
                "uuid": f"{role[0]}{i}",
                "timestamp": f"2026-04-17T10:{i // 60:02d}:{i % 60:02d}Z",
                "message": {"role": role, "content": content},
            }
        )
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
    return path


def test_pick_routing_tier_short_to_mac_mini() -> None:
    assert pick_routing_tier(20) == RoutingTier.SIMPLE
    assert pick_routing_tier(99) == RoutingTier.SIMPLE


def test_pick_routing_tier_threshold_is_100() -> None:
    assert pick_routing_tier(100) == RoutingTier.COMPLEX
    assert pick_routing_tier(500) == RoutingTier.COMPLEX


def test_format_daily_log_body_has_five_sections() -> None:
    extracted = {
        "decisions": ["Chose X", "Deferred Y"],
        "lessons": ["Wan 2.2 requires WanImageToVideo node"],
        "actions": ["Test X on Y"],
        "patterns": ["Long sessions → implementation next day"],
        "quotes": ["'we ship now'"],
    }
    body = format_daily_log_body(
        session_summary={
            "tool": "claude-code",
            "duration": "2h 15m",
            "messages": 180,
            "tag": "phase-6",
        },
        extracted=extracted,
    )
    assert "## Sessions" in body
    assert "claude-code" in body
    assert "2h 15m" in body
    assert "180 messages" in body
    assert "## Decisions" in body
    assert "Chose X" in body
    assert "## Lessons" in body
    assert "## Action Items" in body
    assert "## Patterns" in body
    assert "## Quotes" in body


def test_append_to_daily_log_creates_file_if_missing(tmp_path: Path) -> None:
    daily_dir = tmp_path / "vault" / "daily"
    target = daily_dir / "2026-04-17.md"
    body = "## Sessions\n- claude-code: 1h\n"
    append_to_daily_log(target, body, lock_dir=daily_dir)

    assert target.exists()
    text = target.read_text(encoding="utf-8")
    assert text.startswith("# Daily Log — ")
    assert "## Sessions" in text


def test_append_to_daily_log_appends_to_existing(tmp_path: Path) -> None:
    daily_dir = tmp_path / "vault" / "daily"
    target = daily_dir / "2026-04-17.md"
    daily_dir.mkdir(parents=True)
    target.write_text("# Daily Log — 2026-04-17\n\n## Sessions\n- existing: 30m\n\n", encoding="utf-8")

    append_to_daily_log(target, "\n---\n## Sessions\n- new: 1h\n", lock_dir=daily_dir)

    text = target.read_text(encoding="utf-8")
    assert "existing: 30m" in text
    assert "new: 1h" in text
    # Header not duplicated
    assert text.count("# Daily Log") == 1


def test_recursion_guard_exits_cleanly(tmp_path: Path) -> None:
    """If CLAUDE_INVOKED_BY=flush is set, run_flush must short-circuit."""
    transcript = _make_transcript(tmp_path / "t.jsonl", 50)
    with patch.dict(os.environ, {"CLAUDE_INVOKED_BY": "flush"}):
        result = run_flush(
            transcript_path=transcript,
            vault_daily_dir=tmp_path / "vault" / "daily",
            llm_caller=None,
        )
    assert isinstance(result, FlushResult)
    assert result.status == "recursion-guard"
    # No daily log written
    assert not (tmp_path / "vault" / "daily" / "2026-04-17.md").exists()


def test_run_flush_happy_path_mocked_llm(tmp_path: Path) -> None:
    transcript = _make_transcript(tmp_path / "t.jsonl", 40)

    def fake_llm(prompt: str, tier: RoutingTier) -> dict:
        return {
            "decisions": ["Chose phi4-mini for triage"],
            "lessons": ["Mock LLM is useful for tests"],
            "actions": ["Wire up real LLM later"],
            "patterns": ["Tests should not hit network"],
            "quotes": ["'green is the only color'"],
        }

    result = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=fake_llm,
    )
    assert result.status == "ok"
    assert result.tier == RoutingTier.SIMPLE
    assert result.messages == 40
    daily_path = tmp_path / "vault" / "daily" / f"{result.date}.md"
    assert daily_path.exists()
    text = daily_path.read_text(encoding="utf-8")
    assert "Chose phi4-mini for triage" in text
    assert "Mock LLM is useful for tests" in text


def test_run_flush_missing_transcript_returns_error(tmp_path: Path) -> None:
    result = run_flush(
        transcript_path=tmp_path / "does_not_exist.jsonl",
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=None,
    )
    assert result.status == "error"
    assert "transcript" in result.error.lower()


# ─── Phase 2: SOUL prepend ────────────────────────────────────────────────


class TestBuildSoulPrepend:
    def test_returns_empty_when_config_is_none(self):
        assert build_soul_prepend(None) == ""

    def test_returns_empty_when_artifacts_disabled(self, tmp_artifacts: Path):
        cfg = _flush_config(tmp_artifacts, enabled=False)
        assert build_soul_prepend(cfg) == ""

    def test_returns_empty_when_no_per_agent_entry(self, tmp_artifacts: Path):
        cfg = _FakeConfig(
            vault_root=tmp_artifacts,
            artifacts={"enabled": True, "per_agent": {}},
        )
        assert build_soul_prepend(cfg) == ""

    def test_returns_empty_when_soul_not_in_on_demand(self, tmp_artifacts: Path):
        cfg = _flush_config(tmp_artifacts, on_demand=("USER",))
        assert build_soul_prepend(cfg) == ""

    def test_includes_all_three_domain_souls(self, tmp_artifacts: Path):
        block = build_soul_prepend(_flush_config(tmp_artifacts))
        assert "## SOUL — creative-studio" in block
        assert "## SOUL — life-systems" in block
        assert "## SOUL — job-hunt-2026" in block

    def test_uses_framing_markers(self, tmp_artifacts: Path):
        block = build_soul_prepend(_flush_config(tmp_artifacts))
        assert block.startswith("--- BEGIN OPERATING-MODEL SOUL CONTEXT")
        assert "--- END OPERATING-MODEL SOUL CONTEXT ---" in block
        assert block.rstrip().endswith("--- BEGIN SESSION TRANSCRIPT EXTRACTION ---")

    def test_missing_domain_soul_maps_to_unavailable(self, tmp_artifacts: Path):
        (tmp_artifacts / "05_atlas" / "operating-models" / "job-hunt-2026" / "SOUL.md").unlink()
        block = build_soul_prepend(_flush_config(tmp_artifacts))
        assert "## SOUL — job-hunt-2026\n\n[unavailable]" in block
        # Other two still load
        assert "## SOUL — creative-studio" in block


class TestRunFlushSoulPrepend:
    def test_no_config_keeps_existing_behavior(self, tmp_path: Path) -> None:
        """Phase-1 callers pass no config — prompt has NO SOUL prepend."""
        transcript = _make_transcript(tmp_path / "t.jsonl", 30)
        captured = {"prompt": ""}

        def fake_llm(prompt: str, tier: RoutingTier) -> dict:
            captured["prompt"] = prompt
            return {"decisions": ["d"], "lessons": [], "actions": [], "patterns": [], "quotes": []}

        run_flush(
            transcript_path=transcript,
            vault_daily_dir=tmp_path / "vault" / "daily",
            llm_caller=fake_llm,
        )
        assert "BEGIN OPERATING-MODEL SOUL CONTEXT" not in captured["prompt"]
        # The base prompt body must still be present and unchanged
        assert captured["prompt"].startswith(
            "You are summarizing a single Claude Code session"
        )

    def test_config_enabled_prepends_soul_above_existing_prompt(
        self, tmp_path: Path, tmp_artifacts: Path
    ) -> None:
        transcript = _make_transcript(tmp_path / "t.jsonl", 30)
        captured = {"prompt": ""}

        def fake_llm(prompt: str, tier: RoutingTier) -> dict:
            captured["prompt"] = prompt
            return {"decisions": ["d"], "lessons": [], "actions": [], "patterns": [], "quotes": []}

        cfg = _flush_config(tmp_artifacts)
        run_flush(
            transcript_path=transcript,
            vault_daily_dir=tmp_path / "vault" / "daily",
            llm_caller=fake_llm,
            config=cfg,
        )
        prompt = captured["prompt"]
        # SOUL prepend lands first
        assert prompt.startswith("--- BEGIN OPERATING-MODEL SOUL CONTEXT")
        # All three domain SOULs present
        assert "## SOUL — creative-studio" in prompt
        assert "## SOUL — life-systems" in prompt
        assert "## SOUL — job-hunt-2026" in prompt
        # And the existing prompt body lands AFTER the prepend, unchanged
        idx = prompt.find("You are summarizing a single Claude Code session")
        assert idx > 0
        assert "BEGIN SESSION TRANSCRIPT EXTRACTION" in prompt[:idx]

    def test_json_output_shape_unchanged_with_soul(self, tmp_path: Path, tmp_artifacts: Path) -> None:
        """JSON shape (5-key dict, lists) does NOT regress when SOUL is on."""
        transcript = _make_transcript(tmp_path / "t.jsonl", 30)

        def fake_llm(prompt: str, tier: RoutingTier) -> dict:
            return {
                "decisions": ["D1"],
                "lessons": ["L1"],
                "actions": ["A1"],
                "patterns": ["P1"],
                "quotes": ["Q1"],
            }

        result = run_flush(
            transcript_path=transcript,
            vault_daily_dir=tmp_path / "vault" / "daily",
            llm_caller=fake_llm,
            config=_flush_config(tmp_artifacts),
        )
        assert result.status == "ok"
        assert result.sections_written == 5
        text = (tmp_path / "vault" / "daily" / f"{result.date}.md").read_text(encoding="utf-8")
        for marker in ("D1", "L1", "A1", "P1", "Q1"):
            assert marker in text


def test_run_flush_daily_log_append_idempotent(tmp_path: Path) -> None:
    """Running flush twice on the same transcript produces two session blocks
    (append, not overwrite) and never duplicates the header."""
    transcript = _make_transcript(tmp_path / "t.jsonl", 30)

    def fake_llm(prompt: str, tier: RoutingTier) -> dict:
        return {
            "decisions": ["D1"],
            "lessons": ["L1"],
            "actions": ["A1"],
            "patterns": ["P1"],
            "quotes": ["Q1"],
        }

    r1 = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=fake_llm,
    )
    r2 = run_flush(
        transcript_path=transcript,
        vault_daily_dir=tmp_path / "vault" / "daily",
        llm_caller=fake_llm,
    )
    assert r1.status == "ok" and r2.status == "ok"
    daily_path = tmp_path / "vault" / "daily" / f"{r1.date}.md"
    text = daily_path.read_text(encoding="utf-8")
    assert text.count("# Daily Log") == 1
    assert text.count("D1") >= 2  # both runs wrote it
