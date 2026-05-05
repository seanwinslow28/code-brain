"""Tests for agents.gemini_researcher — Phase 3 (v3.25.0).

All tests are fully mocked — no real API calls, no vault writes to production.
Mock target: scripts.gemini_dr.run (imported as run_research in the agent).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

# Ensure agents-sdk/ is on sys.path for lib imports
SDK_ROOT = Path(__file__).parent.parent
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _make_queue(tmp_path: Path, items: list[str]) -> Path:
    """Write a minimal gemini-research-queue.md with the given items."""
    queue = tmp_path / "gemini-research-queue.md"
    lines = ["---", "type: research-queue", "---", "", "## Pending", ""]
    lines += [f"- [ ] {item}" for item in items]
    lines += ["", "## Done", ""]
    queue.write_text("\n".join(lines), encoding="utf-8")
    return queue


def _make_config(tmp_path: Path, queue_path: Path, enabled: bool = True):
    """Return a mock config object."""
    log_dir = tmp_path / "90_system" / "agent-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    cfg = MagicMock()
    cfg.repo_root = tmp_path
    cfg.vault_root = tmp_path / "vault"
    cfg.log_dir = log_dir
    cfg.log_level = "INFO"
    cfg.agents = {
        "gemini_researcher": {
            "enabled": enabled,
            "queue_path": str(queue_path.relative_to(tmp_path)),
            "max_budget_usd": 0.00,
        }
    }
    return cfg


def _make_config_toml(tmp_path: Path) -> Path:
    """Write a minimal config.toml with [gemini] section for default_tier."""
    config_toml = tmp_path / "agents-sdk" / "config.toml"
    config_toml.parent.mkdir(parents=True, exist_ok=True)
    config_toml.write_text(
        '[gemini]\ndefault_tier = "dr"\n', encoding="utf-8"
    )
    return config_toml


# ─── 1. Tier marker extraction ───────────────────────────────────────────────


def test_tier_marker_dr():
    """tier: dr extracts canonical tier 'dr'."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("tier: dr What is machine learning?", "dr")
    assert tier == "dr"
    assert "What is machine learning?" in query
    assert "tier:" not in query


def test_tier_marker_dr_max():
    """tier: dr-max extracts canonical tier 'max'."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("tier: dr-max Comprehensive blockchain analysis", "dr")
    assert tier == "max"
    assert "Comprehensive blockchain analysis" in query
    assert "tier:" not in query


def test_tier_marker_max_alias():
    """tier: max extracts canonical tier 'max' (alias for dr-max)."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("tier: max Extended synthesis on AI safety", "dr")
    assert tier == "max"
    assert "Extended synthesis on AI safety" in query


def test_tier_marker_case_insensitive():
    """tier: DR is normalized to 'dr' (case-insensitive)."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("tier: DR Some research question", "dr")
    assert tier == "dr"


# ─── 2. Default tier when marker absent ──────────────────────────────────────


def test_default_tier_when_no_marker():
    """When no tier marker is present, default_tier from config is used."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("What are the practical differences between ollama modelfiles?", "dr")
    assert tier == "dr"
    # Query returned unchanged
    assert query == "What are the practical differences between ollama modelfiles?"


def test_default_tier_respects_config_default():
    """default_tier='max' propagates correctly when no marker is present."""
    from agents.gemini_researcher import _extract_tier
    tier, query = _extract_tier("Some question without a marker", "max")
    assert tier == "max"


# ─── 3. Empty queue path ─────────────────────────────────────────────────────


def test_empty_queue_exits_zero_no_api_call(tmp_path: Path):
    """Empty queue: exits 0, writes empty-queue to CSV, no gemini_dr.run call."""
    queue = tmp_path / "gemini-research-queue.md"
    queue.write_text("---\ntype: research-queue\n---\n\n## Pending\n\n## Done\n", encoding="utf-8")
    mock_config = _make_config(tmp_path, queue, enabled=True)

    run_calls = []

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger") as mock_logger,
        patch("agents.gemini_researcher.record_run") as mock_record,
        patch("agents.gemini_researcher.run_research", side_effect=lambda **kw: run_calls.append(kw) or 0) as mock_run,
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        mock_logger.return_value = MagicMock()
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    assert len(run_calls) == 0, "gemini_dr.run should not be called for empty queue"
    # record_run called with status="empty-queue"
    assert mock_record.called
    call_kwargs = mock_record.call_args
    # status is the 4th positional arg or kwarg
    args, kwargs = call_kwargs
    status = kwargs.get("status") or args[3]
    assert status == "empty-queue"


# ─── 4. enabled=false path ───────────────────────────────────────────────────


def test_disabled_agent_exits_zero_no_work(tmp_path: Path):
    """enabled=false: exits 0, logs warning, does not call gemini_dr.run."""
    queue = _make_queue(tmp_path, ["tier: dr What is DeFi?"])
    mock_config = _make_config(tmp_path, queue, enabled=False)

    run_calls = []

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger") as mock_logger,
        patch("agents.gemini_researcher.run_research", side_effect=lambda **kw: run_calls.append(kw) or 0),
    ):
        mock_log = MagicMock()
        mock_logger.return_value = mock_log
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    assert len(run_calls) == 0, "run_research should not be called when disabled"
    # A warning should have been logged
    assert mock_log.warning.called
    warning_msg = mock_log.warning.call_args[0][0]
    assert "disabled" in warning_msg.lower()


# ─── 5. Tier-marker passthrough to gemini_dr.run ─────────────────────────────


def test_tier_dr_max_marker_passes_max_to_run_research(tmp_path: Path):
    """Queue item with `tier: dr-max` calls run_research with tier='max'."""
    queue = _make_queue(tmp_path, ["tier: dr-max Comprehensive blockchain analysis 2026"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    captured = {}

    def fake_run_research(**kwargs):
        captured.update(kwargs)
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    assert captured.get("tier") == "max", f"Expected tier='max', got {captured.get('tier')!r}"
    assert captured.get("no_confirm") is True, "Autonomous agent must pass no_confirm=True"


def test_tier_dr_marker_passes_dr_to_run_research(tmp_path: Path):
    """Queue item with `tier: dr` calls run_research with tier='dr'."""
    queue = _make_queue(tmp_path, ["tier: dr What is machine learning?"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    captured = {}

    def fake_run_research(**kwargs):
        captured.update(kwargs)
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    assert captured.get("tier") == "dr"


# ─── 6. Mark-done rewrite ─────────────────────────────────────────────────────


def test_mark_done_rewrites_queue_line(tmp_path: Path):
    """After successful run, the `- [ ]` line becomes `- [x] ... → [[wikilink]]`."""
    queue = _make_queue(tmp_path, ["tier: dr What is Ethereum staking?"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    def fake_run_research(**kwargs):
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    content = queue.read_text(encoding="utf-8")
    # Original unchecked line must be gone
    assert "- [ ] tier: dr What is Ethereum staking?" not in content
    # Checked line must be present
    assert "- [x]" in content
    # Wikilink must be present
    assert "[[" in content and "]]" in content
    # "done" with timestamp must be present
    assert "done" in content
    # C1: wikilink must be vault-relative (no "vault/" prefix inside the brackets)
    assert "20_projects/research/" in content
    assert "vault/20_projects" not in content  # guard against repo-relative regression
    assert "[[20_projects/research/" in content  # exact vault-relative wikilink prefix


def test_mark_done_not_called_on_empty_queue(tmp_path: Path):
    """Empty queue: no lines to mark done — queue file unchanged."""
    queue = tmp_path / "gemini-research-queue.md"
    original = "---\ntype: research-queue\n---\n\n## Pending\n\n## Done\n"
    queue.write_text(original, encoding="utf-8")
    mock_config = _make_config(tmp_path, queue, enabled=True)

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    assert result == 0
    assert queue.read_text(encoding="utf-8") == original


# ─── 7. CLI --tier flag overrides queue marker (oneshot mode) ─────────────────


def test_cli_tier_flag_overrides_in_oneshot_mode(tmp_path: Path):
    """--tier max from CLI wins even in oneshot mode."""
    queue = _make_queue(tmp_path, [])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    captured = {}

    def fake_run_research(**kwargs):
        captured.update(kwargs)
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(
            mode="oneshot",
            dry_run=False,
            oneshot_query="Some question with explicit tier",
            cli_tier="max",
        )

    assert result == 0
    assert captured.get("tier") == "max", f"Expected tier='max', got {captured.get('tier')!r}"
    assert captured.get("query") == "Some question with explicit tier"


def test_cli_tier_dr_overrides_queue_marker_max(tmp_path: Path):
    """--tier dr from CLI overrides queue's `tier: max` marker in queue mode."""
    queue = _make_queue(tmp_path, ["tier: max Extended synthesis question"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    captured = {}

    def fake_run_research(**kwargs):
        captured.update(kwargs)
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False, cli_tier="dr")

    assert result == 0
    assert captured.get("tier") == "dr", (
        f"CLI --tier dr should override queue marker, got {captured.get('tier')!r}"
    )
    # I1: query must NOT contain the tier marker — raw queue item was "tier: max Extended..."
    captured_query = captured.get("query", "")
    assert "tier:" not in captured_query, (
        f"CLI --tier override must strip marker from query, got {captured_query!r}"
    )
    assert "Extended synthesis question" in captured_query, (
        f"Query should contain the question text, got {captured_query!r}"
    )


# ─── 8. no_confirm=True is always passed ─────────────────────────────────────


def test_no_confirm_true_always_passed_to_run_research(tmp_path: Path):
    """Autonomous agent always passes no_confirm=True to gemini_dr.run."""
    queue = _make_queue(tmp_path, ["tier: max Big extended question"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    captured = {}

    def fake_run_research(**kwargs):
        captured.update(kwargs)
        return 0

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=fake_run_research),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        run(mode="queue", dry_run=False)

    assert captured.get("no_confirm") is True, (
        "Autonomous agent must pass no_confirm=True to prevent DR Max hang"
    )


# ─── 9. Dry-run writes nothing ───────────────────────────────────────────────


def test_dry_run_no_api_call_no_vault_write(tmp_path: Path):
    """--dry-run: prints intent, no gemini_dr.run call, queue unchanged."""
    queue = _make_queue(tmp_path, ["tier: dr What are DeFi risks?"])
    original_content = queue.read_text(encoding="utf-8")
    mock_config = _make_config(tmp_path, queue, enabled=True)

    run_calls = []

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run"),
        patch("agents.gemini_researcher.run_research", side_effect=lambda **kw: run_calls.append(kw) or 0),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=True)

    assert result == 0
    assert len(run_calls) == 0, "Dry run must not call gemini_dr.run"
    assert queue.read_text(encoding="utf-8") == original_content, "Dry run must not modify queue"


# ─── 10. Marker-only queue line refused (m3) ─────────────────────────────────


def test_marker_only_query_refuses(tmp_path: Path):
    """Queue line with only a tier marker and no question text exits non-zero.

    A line like '- [ ] tier: dr-max' strips to an empty query — the agent
    must refuse with status='empty-query' rather than sending garbage to the API.
    """
    queue = _make_queue(tmp_path, ["tier: dr-max"])
    mock_config = _make_config(tmp_path, queue, enabled=True)

    run_calls = []

    with (
        patch("agents.gemini_researcher.load_config", return_value=mock_config),
        patch("agents.gemini_researcher.setup_logger", return_value=MagicMock()),
        patch("agents.gemini_researcher.record_run") as mock_record,
        patch("agents.gemini_researcher.run_research", side_effect=lambda **kw: run_calls.append(kw) or 0),
        patch("builtins.open", side_effect=_patch_open_for_toml(tmp_path)),
    ):
        from agents.gemini_researcher import run
        result = run(mode="queue", dry_run=False)

    # Must exit non-zero (2 = usage/guard refusal)
    assert result != 0, f"Marker-only queue item should refuse, but exited {result}"
    # Must NOT have called run_research — no API spend
    assert len(run_calls) == 0, "run_research must not be called for marker-only queue item"
    # Must have recorded status=empty-query in the CSV log
    assert mock_record.called, "record_run should be called even on refusal"
    args, kwargs = mock_record.call_args
    status = kwargs.get("status") or args[3]
    assert status == "empty-query", f"Expected status='empty-query', got {status!r}"


# ─── Helpers for config.toml mocking ─────────────────────────────────────────


def _patch_open_for_toml(tmp_path: Path):
    """Returns a side_effect function for builtins.open that intercepts config.toml reads.

    When the code opens the agents-sdk/config.toml path, we return a minimal
    [gemini] section. All other open() calls pass through to the real open().
    """
    import io
    import builtins

    real_open = builtins.open
    toml_content = '[gemini]\ndefault_tier = "dr"\n'

    def patched_open(file, mode="r", *args, **kwargs):
        file_str = str(file)
        # Intercept config.toml reads from the agent script
        if file_str.endswith("config.toml") and "b" in mode:
            return io.BytesIO(toml_content.encode("utf-8"))
        return real_open(file, mode, *args, **kwargs)

    return patched_open
