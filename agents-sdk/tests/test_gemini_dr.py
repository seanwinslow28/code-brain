"""Tests for scripts.gemini_dr — Phase 1 (v3.25.0).

All tests are fully mocked — no real API calls, no vault writes to production.
Mock target: scripts.gemini_dr.genai.Client
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure agents-sdk/ is on sys.path for lib imports
SDK_ROOT = Path(__file__).parent.parent
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))

from scripts.gemini_dr import (
    append_ledger,
    build_topical_note,
    check_caps,
    ledger_totals,
    poll_interaction,
    predicted_cost,
    run,
    slugify,
    warn_if_approaching_cap,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def tmp_vault_dr(tmp_path: Path) -> Path:
    """Minimal vault structure for gemini_dr tests."""
    (tmp_path / "10_timeline" / "daily").mkdir(parents=True)
    (tmp_path / "20_projects" / "research").mkdir(parents=True)
    (tmp_path / "vault" / "health").mkdir(parents=True)
    (tmp_path / "90_system" / "agent-logs").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def tmp_ledger(tmp_path: Path) -> Path:
    """An empty ledger path (file does not exist yet)."""
    ledger_dir = tmp_path / "vault" / "health"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    return ledger_dir / "gemini-spend-2026-05.json"


@pytest.fixture
def gemini_cfg_default() -> dict:
    """Default [gemini] config block matching config.toml spec."""
    return {
        "agent_id_dr": "deep-research-preview-04-2026",
        "agent_id_max": "deep-research-max-preview-04-2026",
        "default_tier": "dr",
        "poll_interval_seconds": 10,
        "max_poll_seconds": 3900,
        "output_dir": "vault/20_projects/research",
        "output_anchor": "research-digest",
        "ledger_dir": "vault/health",
        "budget": {
            "max_per_task_usd": 7.00,
            "monthly_cap_usd": 20.00,
            "daily_cap_usd": 10.00,
            "dr_predicted_usd": 2.00,
            "max_predicted_usd": 5.00,
            "prediction_multiplier": 1.4,
        },
    }


# ─── 1. argparse shape ───────────────────────────────────────────────────────


def test_argparse_required_query(monkeypatch):
    """--query is required; omitting it causes SystemExit."""
    import argparse
    from scripts.gemini_dr import main

    monkeypatch.setattr(sys, "argv", ["gemini_dr.py"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0


def test_argparse_defaults(monkeypatch):
    """--tier defaults to 'dr', --dry-run defaults to False, --no-confirm defaults to False."""
    import argparse
    from scripts import gemini_dr

    # Patch run() to capture the args without executing
    captured = {}

    def mock_run(**kwargs):
        captured["tier"] = kwargs.get("tier", "dr")
        captured["dry_run"] = kwargs.get("dry_run", False)
        captured["no_confirm"] = kwargs.get("no_confirm", False)
        return 0

    monkeypatch.setattr(sys, "argv", ["gemini_dr.py", "--query", "test question"])
    monkeypatch.setattr(gemini_dr, "run", mock_run)
    gemini_dr.main()

    assert captured["tier"] == "dr"
    assert captured["dry_run"] is False
    assert captured["no_confirm"] is False


def test_argparse_tier_choices(monkeypatch):
    """--tier only accepts 'dr' or 'max'."""
    from scripts.gemini_dr import main

    monkeypatch.setattr(sys, "argv", ["gemini_dr.py", "--query", "q", "--tier", "ultra"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0


def test_argparse_dry_run_flag(monkeypatch):
    """--dry-run flag is captured correctly."""
    from scripts import gemini_dr

    captured = {}

    def mock_run(**kwargs):
        captured["dry_run"] = kwargs.get("dry_run", False)
        return 0

    monkeypatch.setattr(sys, "argv", ["gemini_dr.py", "--query", "q", "--dry-run"])
    monkeypatch.setattr(gemini_dr, "run", mock_run)
    gemini_dr.main()

    assert captured["dry_run"] is True


# ─── 2. Slug derivation ──────────────────────────────────────────────────────


def test_slug_basic():
    """Basic slug: lowercase, hyphens for spaces."""
    s = slugify("What is machine learning?")
    assert re.match(r"^[a-z0-9-]+$", s)


def test_slug_max_length():
    """Slug is capped at 60 characters."""
    long_query = "a " * 50  # 100 chars before slugify
    s = slugify(long_query)
    assert len(s) <= 60


def test_slug_all_punctuation():
    """All-punctuation input falls back to 'untitled'."""
    s = slugify("!!! ??? ###")
    assert s == "untitled"


def test_slug_valid_chars_after_unicode():
    r"""Unicode input produces a non-empty slug with only hyphens as separators.

    slugify() uses [^\w\s-] stripping (same as deep_researcher._slugify), which
    keeps unicode word characters. The slug may contain accented letters --
    that is intentional, the EM dash and punctuation are stripped but the
    letters themselves are preserved. Key invariants: no spaces, no special
    punctuation, non-empty result.
    """
    s = slugify("Héllo Wörld — café")
    assert len(s) > 0
    assert " " not in s
    assert re.match(r"^[^\s!@#$%^&*()+={}\[\]|\\:;<>,./?\"`~]+$", s), (
        f"unexpected chars in slug: {s!r}"
    )
    # Hyphens are the only separator
    assert "--" not in s


def test_slug_no_trailing_hyphen():
    """Slug does not end with a hyphen."""
    s = slugify("test-query-")
    assert not s.endswith("-")


# ─── 3. Frontmatter shape ────────────────────────────────────────────────────


def test_frontmatter_dr_source():
    """DR tier produces source: gemini-deep-research."""
    note = build_topical_note(
        query="What is photosynthesis?",
        tier="dr",
        report_text="Photosynthesis converts light to energy.",
        interaction_id="iid-001",
        agent_id="deep-research-preview-04-2026",
        wall_seconds=120,
        cost_predicted_usd=2.80,
        cost_actual_usd=None,
    )
    assert "source: gemini-deep-research\n" in note
    assert "source: gemini-deep-research-max" not in note


def test_frontmatter_max_source():
    """DR Max tier produces source: gemini-deep-research-max."""
    note = build_topical_note(
        query="Comprehensive crypto market analysis",
        tier="max",
        report_text="Detailed analysis...",
        interaction_id="iid-002",
        agent_id="deep-research-max-preview-04-2026",
        wall_seconds=300,
        cost_predicted_usd=7.00,
        cost_actual_usd=None,
    )
    assert "source: gemini-deep-research-max\n" in note


def test_frontmatter_has_required_fields():
    """Frontmatter contains all required fields."""
    note = build_topical_note(
        query="Test query",
        tier="dr",
        report_text="Body text.",
        interaction_id="iid-xyz",
        agent_id="deep-research-preview-04-2026",
        wall_seconds=60,
        cost_predicted_usd=2.80,
        cost_actual_usd=None,
    )
    assert "interaction_id: iid-xyz" in note
    assert "agent_id: deep-research-preview-04-2026" in note
    assert "wall_seconds: 60" in note
    assert "cost_usd:" in note
    assert "created:" in note


# ─── 4. Ledger append ────────────────────────────────────────────────────────


def test_ledger_append_creates_file(tmp_path: Path):
    """append_ledger creates the file if it doesn't exist."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    assert not ledger.exists()

    entry = {
        "interaction_id": "abc123",
        "agent_id": "deep-research-preview-04-2026",
        "tier": "dr",
        "cost_predicted_usd": 2.80,
        "cost_actual_usd": None,
        "cost_usd": 2.80,
        "wall_seconds": 90,
        "query": "test query",
        "created": "2026-05-03T10:00:00Z",
        "output_path": "/path/to/note.md",
    }
    append_ledger(ledger, entry)

    assert ledger.exists()
    data = json.loads(ledger.read_text())
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["interaction_id"] == "abc123"


def test_ledger_append_idempotent_existing_entries(tmp_path: Path):
    """Existing entries are preserved when appending a new one."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    existing = [
        {
            "interaction_id": "old-001",
            "tier": "dr",
            "cost_usd": 2.80,
            "query": "old question",
            "created": "2026-05-01T08:00:00Z",
        }
    ]
    ledger.write_text(json.dumps(existing), encoding="utf-8")

    new_entry = {
        "interaction_id": "new-002",
        "agent_id": "deep-research-preview-04-2026",
        "tier": "dr",
        "cost_predicted_usd": 2.80,
        "cost_actual_usd": None,
        "cost_usd": 2.80,
        "wall_seconds": 100,
        "query": "new question",
        "created": "2026-05-03T10:00:00Z",
        "output_path": "/path/to/note.md",
    }
    append_ledger(ledger, new_entry)

    data = json.loads(ledger.read_text())
    assert len(data) == 2
    assert data[0]["interaction_id"] == "old-001"
    assert data[1]["interaction_id"] == "new-002"


def test_ledger_entry_shape(tmp_path: Path):
    """Ledger entry contains all required shape keys."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    entry = {
        "interaction_id": "shapetest-001",
        "agent_id": "deep-research-preview-04-2026",
        "tier": "dr",
        "cost_predicted_usd": 2.80,
        "cost_actual_usd": None,
        "cost_usd": 2.80,
        "wall_seconds": 75,
        "query": "shape test query",
        "created": "2026-05-03T11:00:00Z",
        "output_path": "/vault/20_projects/research/2026-05-03-shape-test.md",
    }
    append_ledger(ledger, entry)
    data = json.loads(ledger.read_text())
    e = data[0]
    for key in ("interaction_id", "agent_id", "tier", "cost_usd", "wall_seconds", "query", "created"):
        assert key in e, f"missing key: {key}"


# ─── 5. Cap refusal — monthly ────────────────────────────────────────────────


def test_cap_refusal_monthly(tmp_path: Path, gemini_cfg_default: dict):
    """$19.50 mtd + $2.80 predicted = $22.30 > $20.00 monthly cap → refused."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    # Populate ledger with entries totalling $19.50 in May 2026
    entries = [
        {"cost_usd": 2.80, "created": "2026-05-01T08:00:00Z"},
        {"cost_usd": 2.80, "created": "2026-05-01T09:00:00Z"},
        {"cost_usd": 2.80, "created": "2026-05-02T08:00:00Z"},
        {"cost_usd": 2.80, "created": "2026-05-02T09:00:00Z"},
        {"cost_usd": 2.80, "created": "2026-05-02T10:00:00Z"},
        {"cost_usd": 2.80, "created": "2026-05-02T11:00:00Z"},
        {"cost_usd": 1.50, "created": "2026-05-02T12:00:00Z"},
    ]
    # Total: 6 * 2.80 + 1.50 = 16.80 + 1.50 = 18.30 — let's adjust to exactly 19.50
    entries = [
        {"cost_usd": 5.00, "created": "2026-05-01T08:00:00Z"},
        {"cost_usd": 5.00, "created": "2026-05-01T09:00:00Z"},
        {"cost_usd": 5.00, "created": "2026-05-02T08:00:00Z"},
        {"cost_usd": 4.50, "created": "2026-05-02T09:00:00Z"},
    ]
    ledger.write_text(json.dumps(entries), encoding="utf-8")

    ok, msg, pred, mtd, today = check_caps("dr", gemini_cfg_default, ledger, "2026-05-03")

    assert not ok
    assert "monthly cap" in msg
    assert mtd == pytest.approx(19.50)
    assert pred == pytest.approx(2.80)


# ─── 6. Cap refusal — daily ──────────────────────────────────────────────────


def test_cap_refusal_daily_exceeded(tmp_path: Path, gemini_cfg_default: dict):
    """$9.00 today + $2.80 predicted = $11.80 > $10.00 daily cap → refused."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    entries = [
        {"cost_usd": 5.00, "created": "2026-05-03T08:00:00Z"},
        {"cost_usd": 4.00, "created": "2026-05-03T09:00:00Z"},
    ]
    ledger.write_text(json.dumps(entries), encoding="utf-8")

    ok, msg, pred, mtd, today = check_caps("dr", gemini_cfg_default, ledger, "2026-05-03")

    assert not ok
    assert "daily cap" in msg
    assert today == pytest.approx(9.00)


def test_cap_ok_when_today_within_daily(tmp_path: Path, gemini_cfg_default: dict):
    """$5.00 today + $2.80 predicted = $7.80 < $10.00 → allowed."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    entries = [
        {"cost_usd": 5.00, "created": "2026-05-03T08:00:00Z"},
    ]
    ledger.write_text(json.dumps(entries), encoding="utf-8")

    ok, msg, pred, mtd, today = check_caps("dr", gemini_cfg_default, ledger, "2026-05-03")

    assert ok
    assert msg == ""


# ─── 7. Cap refusal — per-task ───────────────────────────────────────────────


def test_cap_refusal_per_task(tmp_path: Path, gemini_cfg_default: dict):
    """DR Max predicted=$7.00 > max_per_task_usd=$5.00 → refused."""
    cfg = {**gemini_cfg_default, "budget": {**gemini_cfg_default["budget"], "max_per_task_usd": 5.00}}
    ledger = tmp_path / "gemini-spend-2026-05.json"
    # Empty ledger — no prior spend
    ledger.write_text("[]", encoding="utf-8")

    ok, msg, pred, mtd, today = check_caps("max", cfg, ledger, "2026-05-03")

    assert not ok
    assert "per-task cap" in msg
    assert pred == pytest.approx(7.00)


# ─── 8. Polling — happy path ─────────────────────────────────────────────────


def test_polling_happy_path():
    """Mock returns in_progress twice, then completed with text."""
    mock_client = MagicMock()

    # First two calls: in_progress; third: completed with text
    running_interaction = MagicMock()
    running_interaction.status = "in_progress"
    running_interaction.outputs = None

    completed_interaction = MagicMock()
    completed_interaction.status = "completed"
    completed_text = MagicMock()
    completed_text.text = "This is the research report."
    completed_interaction.outputs = [completed_text]
    completed_interaction.usage = None

    mock_client.interactions.get.side_effect = [
        running_interaction,
        running_interaction,
        completed_interaction,
    ]

    import logging
    logger = logging.getLogger("test")

    with patch("time.sleep"):  # don't actually sleep
        status, report_text, usage = poll_interaction(
            mock_client,
            interaction_id="test-iid",
            poll_interval=0,
            max_poll_seconds=60,
            logger=logger,
        )

    assert status == "completed"
    assert report_text == "This is the research report."
    assert mock_client.interactions.get.call_count == 3


# ─── 9. Polling — timeout ────────────────────────────────────────────────────


def test_polling_timeout():
    """Mock always returns in_progress; helper raises RuntimeError after timeout."""
    mock_client = MagicMock()
    running = MagicMock()
    running.status = "in_progress"
    mock_client.interactions.get.return_value = running

    import logging
    logger = logging.getLogger("test")

    with patch("time.sleep"), patch("time.time") as mock_time:
        # Simulate time advancing past the deadline
        mock_time.side_effect = [0.0, 0.0, 100.0]  # start, deadline check, past deadline

        with pytest.raises(RuntimeError, match="timed out"):
            poll_interaction(
                mock_client,
                interaction_id="timeout-iid",
                poll_interval=0,
                max_poll_seconds=50,
                logger=logger,
            )


# ─── 10. --dry-run writes nothing ────────────────────────────────────────────


def test_dry_run_writes_nothing(tmp_path: Path):
    """--dry-run: no vault file, no ledger entry, no API call."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    output_dir = tmp_path / "research"
    output_dir.mkdir()

    with (
        patch("scripts.gemini_dr._load_gemini_cfg") as mock_cfg,
        patch("scripts.gemini_dr.load_config") as mock_load_config,
        patch("scripts.gemini_dr.get_credential") as mock_cred,
        patch("scripts.gemini_dr.genai") as mock_genai,
        patch("scripts.gemini_dr.setup_logger") as mock_logger,
        patch("scripts.gemini_dr.record_run"),
    ):
        # Minimal config setup
        mock_cfg.return_value = {
            "agent_id_dr": "deep-research-preview-04-2026",
            "agent_id_max": "deep-research-max-preview-04-2026",
            "poll_interval_seconds": 10,
            "max_poll_seconds": 3900,
            "output_dir": str(output_dir),
            "output_anchor": "research-digest",
            "ledger_dir": str(tmp_path),
            "budget": {
                "max_per_task_usd": 7.00,
                "monthly_cap_usd": 20.00,
                "daily_cap_usd": 10.00,
                "dr_predicted_usd": 2.00,
                "max_predicted_usd": 5.00,
                "prediction_multiplier": 1.4,
            },
        }
        mock_config = MagicMock()
        mock_config.repo_root = tmp_path
        mock_config.vault_root = tmp_path
        mock_config.log_dir = tmp_path / "90_system" / "agent-logs"
        mock_config.log_level = "INFO"
        (mock_config.log_dir).mkdir(parents=True, exist_ok=True)
        mock_load_config.return_value = mock_config
        mock_logger.return_value = MagicMock()
        mock_cred.return_value = "fake-api-key"

        result = run(
            query="test dry run query",
            tier="dr",
            dry_run=True,
            no_confirm=False,
            ledger_path_override=ledger,
        )

    # Exit code 0
    assert result == 0

    # No API call
    mock_genai.Client.assert_not_called()

    # No ledger created
    assert not ledger.exists()

    # No research notes written
    md_files = list(output_dir.rglob("*.md"))
    assert len(md_files) == 0


# ─── 11. WARN when mtd > 70% of monthly cap ──────────────────────────────────


def test_warn_approaching_cap(gemini_cfg_default: dict):
    """Emits a warning when mtd > 70% of $20.00 = $14.00."""
    # mtd = $15.00 — should trigger warning
    mock_logger = MagicMock()
    warn_if_approaching_cap(15.00, gemini_cfg_default, mock_logger)
    mock_logger.warning.assert_called_once()
    call_args = mock_logger.warning.call_args[0][0]
    assert "monthly cap" in call_args.lower() or "month" in call_args.lower()


def test_no_warn_below_threshold(gemini_cfg_default: dict):
    """No warning when mtd is below 70% threshold."""
    mock_logger = MagicMock()
    warn_if_approaching_cap(5.00, gemini_cfg_default, mock_logger)
    mock_logger.warning.assert_not_called()


# ─── 12. predicted_cost math ─────────────────────────────────────────────────


def test_predicted_cost_dr(gemini_cfg_default: dict):
    """DR predicted = $2.00 * 1.4 = $2.80."""
    assert predicted_cost("dr", gemini_cfg_default) == pytest.approx(2.80)


def test_predicted_cost_max(gemini_cfg_default: dict):
    """Max predicted = $5.00 * 1.4 = $7.00."""
    assert predicted_cost("max", gemini_cfg_default) == pytest.approx(7.00)


# ─── 13. Missing ledger treated as $0 ────────────────────────────────────────


def test_missing_ledger_zero_totals(tmp_path: Path, gemini_cfg_default: dict):
    """Missing ledger file treated as $0 mtd / $0 today — caps pass."""
    ledger = tmp_path / "does-not-exist.json"
    assert not ledger.exists()

    ok, msg, pred, mtd, today = check_caps("dr", gemini_cfg_default, ledger, "2026-05-03")

    assert ok
    assert mtd == 0.0
    assert today == 0.0


# ─── 14. DR Max without --no-confirm is refused ──────────────────────────────


def test_dr_max_requires_no_confirm_flag(tmp_path: Path):
    """DR Max without --no-confirm exits with code 2 (usage error)."""
    with (
        patch("scripts.gemini_dr._load_gemini_cfg") as mock_cfg,
        patch("scripts.gemini_dr.load_config") as mock_load_config,
        patch("scripts.gemini_dr.setup_logger") as mock_logger,
        patch("scripts.gemini_dr.record_run"),
    ):
        mock_cfg.return_value = {
            "agent_id_dr": "deep-research-preview-04-2026",
            "agent_id_max": "deep-research-max-preview-04-2026",
            "poll_interval_seconds": 10,
            "max_poll_seconds": 3900,
            "output_dir": "vault/20_projects/research",
            "output_anchor": "research-digest",
            "ledger_dir": "vault/health",
            "budget": {
                "max_per_task_usd": 7.00,
                "monthly_cap_usd": 20.00,
                "daily_cap_usd": 10.00,
                "dr_predicted_usd": 2.00,
                "max_predicted_usd": 5.00,
                "prediction_multiplier": 1.4,
            },
        }
        mock_config = MagicMock()
        mock_config.repo_root = tmp_path
        mock_config.vault_root = tmp_path
        mock_config.log_dir = tmp_path / "90_system" / "agent-logs"
        (mock_config.log_dir).mkdir(parents=True, exist_ok=True)
        mock_config.log_level = "INFO"
        mock_load_config.return_value = mock_config
        mock_logger.return_value = MagicMock()

        result = run(
            query="some max query",
            tier="max",
            dry_run=False,
            no_confirm=False,  # No confirm → should refuse
        )

    assert result == 2


# ─── 15. Cap order: per-task checked before daily/monthly ────────────────────


def test_cap_order_per_task_first(tmp_path: Path, gemini_cfg_default: dict):
    """Per-task cap is evaluated first — even with $0 mtd, per-task refusal fires."""
    cfg = {**gemini_cfg_default, "budget": {**gemini_cfg_default["budget"], "max_per_task_usd": 1.00}}
    ledger = tmp_path / "empty-ledger.json"
    # No prior spend

    ok, msg, pred, mtd, today = check_caps("dr", cfg, ledger, "2026-05-03")

    # DR predicted = $2.80 > max_per_task = $1.00
    assert not ok
    assert "per-task cap" in msg


# ─── 16. C1: cost_actual_usd=0.0 is treated as $0, not fallen through ────────


def test_ledger_totals_zero_actual_not_falsy():
    """C1: cost_actual_usd=0.0 (free/cancelled run) sums as $0, not $2.80.

    The old `or`-chain treated 0.0 as falsy and fell through to cost_predicted_usd,
    overcounting spend. Explicit is-not-None checks fix this.
    """
    entries = [
        {
            "cost_actual_usd": 0.0,       # free run (e.g. cancelled before billing)
            "cost_predicted_usd": 2.80,   # would have been $2.80 if it ran
            "created": "2026-05-03T10:00:00Z",
        }
    ]
    mtd, today = ledger_totals(entries, "2026-05-03")
    assert mtd == pytest.approx(0.0), f"Expected $0 mtd, got ${mtd}"
    assert today == pytest.approx(0.0), f"Expected $0 today, got ${today}"


# ─── 17. C2: tmp file is cleaned up when write_text raises ───────────────────


def test_append_ledger_tmp_cleaned_on_write_error(tmp_path: Path, monkeypatch):
    """C2: .tmp file does not persist when write_text raises (e.g. disk full)."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    entry = {
        "interaction_id": "tmp-leak-test",
        "tier": "dr",
        "cost_predicted_usd": 2.80,
        "cost_actual_usd": None,
        "cost_usd": 2.80,
        "created": "2026-05-03T10:00:00Z",
    }

    original_write_text = Path.write_text

    def raising_write_text(self, *args, **kwargs):
        # Only raise for .tmp files to simulate disk-full on the tmp write
        if self.suffix == ".tmp":
            raise OSError("Simulated disk full")
        return original_write_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", raising_write_text)

    with pytest.raises(OSError, match="Simulated disk full"):
        append_ledger(ledger, entry)

    tmp_path_candidate = ledger.with_suffix(".tmp")
    assert not tmp_path_candidate.exists(), ".tmp file leaked after write_text failure"


# ─── 18. I2: run() passes mtd + pred_cost to warn_if_approaching_cap ─────────


def test_run_warn_called_with_mtd_plus_pred(tmp_path: Path):
    """I2: warn_if_approaching_cap receives mtd + pred_cost, not just mtd."""
    ledger = tmp_path / "gemini-spend-2026-05.json"
    # Pre-populate ledger so mtd > 0 (makes the test distinguishable from mtd=0)
    existing = [{"cost_usd": 10.00, "created": "2026-05-03T08:00:00Z"}]
    ledger.write_text(json.dumps(existing), encoding="utf-8")

    warn_calls = []

    def capture_warn(value, _cfg, _logger):
        warn_calls.append(value)

    with (
        patch("scripts.gemini_dr._load_gemini_cfg") as mock_cfg,
        patch("scripts.gemini_dr.load_config") as mock_load_config,
        patch("scripts.gemini_dr.setup_logger") as mock_logger,
        patch("scripts.gemini_dr.record_run"),
        patch("scripts.gemini_dr.warn_if_approaching_cap", side_effect=capture_warn),
    ):
        mock_cfg.return_value = {
            "agent_id_dr": "deep-research-preview-04-2026",
            "agent_id_max": "deep-research-max-preview-04-2026",
            "poll_interval_seconds": 10,
            "max_poll_seconds": 3900,
            "output_dir": "vault/20_projects/research",
            "output_anchor": "research-digest",
            "ledger_dir": "vault/health",
            "budget": {
                "max_per_task_usd": 7.00,
                "monthly_cap_usd": 20.00,
                "daily_cap_usd": 10.00,
                "dr_predicted_usd": 2.00,
                "max_predicted_usd": 5.00,
                "prediction_multiplier": 1.4,
            },
        }
        mock_config = MagicMock()
        mock_config.repo_root = tmp_path
        mock_config.vault_root = tmp_path
        mock_config.log_dir = tmp_path / "90_system" / "agent-logs"
        (mock_config.log_dir).mkdir(parents=True, exist_ok=True)
        mock_config.log_level = "INFO"
        mock_load_config.return_value = mock_config
        mock_logger.return_value = MagicMock()

        # This will hit the daily cap (10.00 + 2.80 > 10.00) and return exit 1,
        # but warn_if_approaching_cap is called before the cap-refusal branch.
        run(
            query="warn threshold test",
            tier="dr",
            dry_run=False,
            no_confirm=False,
            ledger_path_override=ledger,
        )

    assert len(warn_calls) == 1, "warn_if_approaching_cap should be called exactly once"
    # DR predicted = $2.00 * 1.4 = $2.80; mtd = $10.00 → expected arg = $12.80
    assert warn_calls[0] == pytest.approx(12.80), (
        f"Expected warn called with mtd+pred=$12.80, got ${warn_calls[0]}"
    )
