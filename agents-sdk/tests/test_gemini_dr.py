"""Tests for scripts.gemini_dr — google-genai 2.x Interactions API.

All tests are fully mocked — no real API calls, no vault writes to production.
Mock target: scripts.gemini_dr.genai.Client

Every test that reaches run() must patch BOTH ``scripts.gemini_dr.genai`` and
the credential path, and assert ``mock_genai.Client.assert_not_called()``. A
2026-06-18 regression let a stale ledger date defeat a cap refusal and fall
through to a real 65-minute Deep Research call; the guards below exist so that
cannot recur.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure agents-sdk/ is on sys.path for lib imports
SDK_ROOT = Path(__file__).parent.parent
if str(SDK_ROOT) not in sys.path:
    sys.path.insert(0, str(SDK_ROOT))

from scripts.gemini_dr import (
    _extract_report_text,
    _read_env_file_var,
    append_ledger,
    build_topical_note,
    check_caps,
    ledger_totals,
    poll_interaction,
    predicted_cost,
    resolve_api_key,
    run,
    slugify,
    warn_if_approaching_cap,
)


# ─── 2.x Interaction shape builders ──────────────────────────────────────────
#
# google-genai 2.x returns Interaction.steps — a typed union discriminated on
# `.type` — instead of the 1.x flat Interaction.outputs list. The report body
# lives in the last "model_output" step, whose .content is a list of typed
# parts (TextContent for the answer, usually a second TextContent for sources).


def _text_part(text: str):
    """A TextContent-shaped content part."""
    part = MagicMock()
    part.type = "text"
    part.text = text
    return part


def _model_output_step(*texts: str):
    """A ModelOutputStep carrying one TextContent part per argument."""
    step = MagicMock()
    step.type = "model_output"
    step.content = [_text_part(t) for t in texts]
    return step


def _thought_step(text: str = "Let me search for sources..."):
    """A ThoughtStep — text-bearing, but Gemini's internal reasoning.

    Must never appear in the report body.
    """
    step = MagicMock()
    step.type = "thought"
    step.content = [_text_part(text)]
    return step


def _user_input_step(text: str = "the original question"):
    """A UserInputStep — the echoed prompt. Must never appear in the report."""
    step = MagicMock()
    step.type = "user_input"
    step.content = [_text_part(text)]
    return step


def _search_call_step():
    """A GoogleSearchCallStep — a tool call with no text content at all."""
    step = MagicMock()
    step.type = "google_search_call"
    step.content = None
    return step


def _interaction(status: str, steps=None, output_text=None, usage=None):
    """A 2.x Interaction with the fields the helper reads."""
    interaction = MagicMock()
    interaction.status = status
    interaction.steps = steps
    interaction.output_text = output_text
    interaction.usage = usage
    return interaction


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
    """Mock returns in_progress twice, then completed with a model_output step."""
    mock_client = MagicMock()

    running_interaction = _interaction("in_progress", steps=None)
    completed_interaction = _interaction(
        "completed",
        steps=[_model_output_step("This is the research report.")],
    )

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


def test_polling_reads_steps_not_outputs():
    """2.x migration guard: the helper must read Interaction.steps.

    google-genai 2.x removed the flat ``.outputs`` list. An interaction that
    only exposes the legacy attribute must NOT yield a report — otherwise a
    future refactor could silently fall back to the dead 1.x shape.
    """
    legacy_only = MagicMock()
    legacy_only.status = "completed"
    legacy_only.steps = None
    legacy_only.output_text = None
    legacy_only.outputs = [_text_part("1.x-shaped body that must be ignored")]

    assert _extract_report_text(legacy_only) is None


def test_extract_concatenates_all_text_parts_of_model_output():
    """Regression for Phase 4 night 1 TD5, carried into the 2.x shape.

    Deep Research puts the answer and the sources block in two separate
    TextContent parts of the same model_output step. Taking content[0] alone
    would drop the sources; taking content[-1] would drop the answer.
    """
    step = _model_output_step(
        "# The Answer\n\nThis is the actual research body.",
        "**Sources:**\n1. example.com",
    )
    report_text = _extract_report_text(_interaction("completed", steps=[step]))

    assert report_text == (
        "# The Answer\n\nThis is the actual research body."
        "\n\n**Sources:**\n1. example.com"
    )


def test_extract_skips_thought_and_tool_call_steps():
    """Only model_output steps contribute — thoughts and tool calls never do."""
    steps = [
        _thought_step("internal reasoning that must not ship"),
        _search_call_step(),
        _model_output_step("# Report\n\nThe findings."),
    ]
    report_text = _extract_report_text(_interaction("completed", steps=steps))

    assert report_text == "# Report\n\nThe findings."
    assert "internal reasoning" not in report_text


def test_extract_concatenates_every_model_output_step():
    """Deep Research chunks the report across MULTIPLE model_output steps.

    Regression for the 2026-08-05 live run (interaction v1_ChdvQ): the report
    arrived as 3 model_output steps of 12160 + 6273 + 25569 chars. Keeping only
    the last dropped 42% of the body — Parts 1 through 3 — while still writing
    a long, well-formed, entirely plausible note. Silent truncation, so the
    only defence is an explicit test.
    """
    steps = [
        _user_input_step("the original question"),
        _model_output_step("# Report\n\n## Part 1\nFirst chunk."),
        _thought_step("internal reasoning"),
        _model_output_step("\n\n## Part 2\nSecond chunk."),
        _model_output_step("\n\n## Part 3\nThird chunk."),
    ]
    report_text = _extract_report_text(_interaction("completed", steps=steps))

    # Every chunk present, in order.
    assert "## Part 1" in report_text
    assert "## Part 2" in report_text
    assert "## Part 3" in report_text
    assert report_text.index("Part 1") < report_text.index("Part 2") < report_text.index("Part 3")
    # Question and reasoning still excluded.
    assert "original question" not in report_text
    assert "internal reasoning" not in report_text
    # Leading separators normalised — no blank-line runs at the seams.
    assert "\n\n\n" not in report_text
    assert report_text == (
        "# Report\n\n## Part 1\nFirst chunk."
        "\n\n## Part 2\nSecond chunk."
        "\n\n## Part 3\nThird chunk."
    )


def test_extract_does_not_prefer_output_text_over_steps():
    """output_text is NOT a whole-report aggregate — steps always win.

    On the 2026-08-05 live run output_text equalled only the FINAL chunk, so
    preferring it (or falling back to it while steps exist) truncates the
    report exactly the way the original bug did.
    """
    steps = [
        _model_output_step("# Full Report\n\nChunk one."),
        _model_output_step("\n\nChunk two."),
    ]
    interaction = _interaction(
        "completed",
        steps=steps,
        output_text="Chunk two.",  # what the real API returned: last chunk only
    )
    report_text = _extract_report_text(interaction)

    assert "Chunk one." in report_text
    assert "Chunk two." in report_text


def test_extract_falls_back_to_output_text():
    """No model_output step at all → output_text as a degraded last resort."""
    interaction = _interaction(
        "completed",
        steps=None,
        output_text="Aggregated report body.",
    )
    assert _extract_report_text(interaction) == "Aggregated report body."


def test_extract_returns_none_when_empty():
    """Nothing textual anywhere → None (run() writes '_(no report returned)_')."""
    assert _extract_report_text(_interaction("completed", steps=[])) is None


def test_polling_budget_exceeded_is_terminal():
    """2.x added 'budget_exceeded' — it must raise, not poll to the wall."""
    mock_client = MagicMock()
    exceeded = _interaction("budget_exceeded", steps=None)
    exceeded.error = "budget exhausted"
    mock_client.interactions.get.return_value = exceeded

    import logging
    logger = logging.getLogger("test")

    with patch("time.sleep"):
        with pytest.raises(RuntimeError, match="non-success state"):
            poll_interaction(
                mock_client,
                interaction_id="budget-iid",
                poll_interval=0,
                max_poll_seconds=60,
                logger=logger,
            )

    # Terminal on the FIRST poll — no spin.
    assert mock_client.interactions.get.call_count == 1


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
    """I2: warn_if_approaching_cap receives mtd + pred_cost, not just mtd.

    The ledger entry MUST be dated to the real ``date.today()`` — run() computes
    mtd/today against the live clock, so a hard-coded past date would no longer
    count as current-month spend, the daily-cap refusal would not fire, and
    execution would fall through to the real ``genai`` API call (the historical
    "pytest hangs on an unmocked Gemini DR call" bug). ``genai`` and
    ``get_credential`` are also patched as a hermetic guard so no test can ever
    reach the network even if the cap logic changes.
    """
    ledger = tmp_path / "gemini-spend-2026-05.json"
    # Pre-populate ledger so mtd > 0 (makes the test distinguishable from mtd=0).
    # Dated to today so it counts under run()'s live-clock cap math.
    existing = [{"cost_usd": 10.00, "created": f"{date.today().isoformat()}T08:00:00Z"}]
    ledger.write_text(json.dumps(existing), encoding="utf-8")

    warn_calls = []

    def capture_warn(value, _cfg, _logger):
        warn_calls.append(value)

    with (
        patch("scripts.gemini_dr._load_gemini_cfg") as mock_cfg,
        patch("scripts.gemini_dr.load_config") as mock_load_config,
        patch("scripts.gemini_dr.setup_logger") as mock_logger,
        patch("scripts.gemini_dr.record_run"),
        patch("scripts.gemini_dr.get_credential", return_value="fake-api-key"),
        patch("scripts.gemini_dr.genai") as mock_genai,
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
    # The daily-cap refusal must fire before any API call — never hit the network.
    mock_genai.Client.assert_not_called()


# ─── 19. Credential resolution: Keychain first, .env fallback ────────────────


def test_resolve_api_key_prefers_keychain(tmp_path: Path, monkeypatch):
    """Keychain slot wins over both the environment and any .env file."""
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")
    (tmp_path / ".env").write_text("GEMINI_API_KEY=dotenv-key\n", encoding="utf-8")

    with patch("scripts.gemini_dr.get_credential", return_value="keychain-key"):
        key, source = resolve_api_key(tmp_path)

    assert key == "keychain-key"
    assert source == "keychain"


def test_resolve_api_key_falls_back_to_env_var(tmp_path: Path, monkeypatch):
    """Empty Keychain → GEMINI_API_KEY from the process environment."""
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")

    with patch("scripts.gemini_dr.get_credential", return_value=None):
        key, source = resolve_api_key(tmp_path)

    assert key == "env-key"
    assert source == "env:GEMINI_API_KEY"


def test_resolve_api_key_falls_back_to_dotenv(tmp_path: Path, monkeypatch):
    """Empty Keychain and no env var → repo-root .env (fresh-machine path)."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# comment line\n"
        "OPENAI_API_KEY=some-other-key\n"
        "GEMINI_API_KEY=dotenv-key\n",
        encoding="utf-8",
    )

    with (
        patch("scripts.gemini_dr.get_credential", return_value=None),
        patch("scripts.gemini_dr.env_file_candidates", return_value=[env_file]),
    ):
        key, source = resolve_api_key(tmp_path)

    assert key == "dotenv-key"
    assert source.startswith("dotenv:")


def test_resolve_api_key_none_when_nothing_set(tmp_path: Path, monkeypatch):
    """Nothing anywhere → (None, 'none') so run() can exit 2 cleanly."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with (
        patch("scripts.gemini_dr.get_credential", return_value=None),
        patch("scripts.gemini_dr.env_file_candidates", return_value=[tmp_path / "nope.env"]),
    ):
        key, source = resolve_api_key(tmp_path)

    assert key is None
    assert source == "none"


@pytest.mark.parametrize(
    "line,expected",
    [
        ("GEMINI_API_KEY=plain", "plain"),
        ('GEMINI_API_KEY="double-quoted"', "double-quoted"),
        ("GEMINI_API_KEY='single-quoted'", "single-quoted"),
        ("export GEMINI_API_KEY=exported", "exported"),
        ("GEMINI_API_KEY =  spaced  ", "spaced"),
        ("#GEMINI_API_KEY=commented", None),
        ("GEMINI_API_KEY=", None),
        ("OTHER_KEY=nope", None),
    ],
)
def test_read_env_file_var_parsing(tmp_path: Path, line: str, expected):
    """.env parsing handles quotes, export prefixes, comments, and blanks."""
    env_file = tmp_path / ".env"
    env_file.write_text(f"{line}\n", encoding="utf-8")
    assert _read_env_file_var(env_file, "GEMINI_API_KEY") == expected


def test_read_env_file_var_missing_file(tmp_path: Path):
    """A missing .env is not an error — it just yields None."""
    assert _read_env_file_var(tmp_path / "absent.env", "GEMINI_API_KEY") is None


# ─── 20. Live call shape pinned to google-genai 2.x ──────────────────────────


def test_run_success_uses_2x_create_shape(tmp_path: Path, monkeypatch):
    """End-to-end success path pins the 2.x create() kwargs and steps parsing.

    Guards the migration: `store` and `agent_config` are gone, and the report
    body comes from a model_output step. Hermetic — genai is a MagicMock, so
    no network is touched even though the cap check passes.
    """
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    ledger = tmp_path / "gemini-spend.json"
    output_dir = tmp_path / "research"
    output_dir.mkdir()

    completed = _interaction(
        "completed",
        steps=[
            _thought_step("internal reasoning"),
            _model_output_step("# Findings\n\nBody.", "**Sources:**\n1. example.com"),
        ],
    )

    with (
        patch("scripts.gemini_dr._load_gemini_cfg") as mock_cfg,
        patch("scripts.gemini_dr.load_config") as mock_load_config,
        patch("scripts.gemini_dr.setup_logger") as mock_logger,
        patch("scripts.gemini_dr.record_run"),
        patch("scripts.gemini_dr.get_credential", return_value="fake-api-key"),
        patch("scripts.gemini_dr.genai") as mock_genai,
        patch("time.sleep"),
    ):
        mock_cfg.return_value = {
            "agent_id_dr": "deep-research-preview-04-2026",
            "agent_id_max": "deep-research-max-preview-04-2026",
            "poll_interval_seconds": 0,
            "max_poll_seconds": 60,
            "output_dir": str(output_dir),
            "output_anchor": "research-digest",
            "ledger_dir": str(tmp_path),
            "budget": {
                "max_per_task_usd": 7.00,
                "monthly_cap_usd": 50.00,
                "daily_cap_usd": 20.00,
                "dr_predicted_usd": 2.00,
                "max_predicted_usd": 5.00,
                "prediction_multiplier": 1.4,
            },
        }
        mock_config = MagicMock()
        mock_config.repo_root = tmp_path
        mock_config.vault_root = tmp_path
        mock_config.log_dir = tmp_path / "90_system" / "agent-logs"
        mock_config.log_dir.mkdir(parents=True, exist_ok=True)
        mock_config.log_level = "INFO"
        mock_load_config.return_value = mock_config
        mock_logger.return_value = MagicMock()

        client = mock_genai.Client.return_value
        created = MagicMock()
        created.id = "iid-2x-001"
        client.interactions.create.return_value = created
        client.interactions.get.return_value = completed

        result = run(
            query="does the 2x shape work",
            tier="dr",
            dry_run=False,
            no_confirm=False,
            ledger_path_override=ledger,
        )

    assert result == 0

    # --- create() call shape is the validated 2.x one ---
    _, kwargs = client.interactions.create.call_args
    assert kwargs == {
        "input": "does the 2x shape work",
        "agent": "deep-research-preview-04-2026",
        "background": True,
    }, f"unexpected create() kwargs: {kwargs}"
    assert "store" not in kwargs
    assert "agent_config" not in kwargs

    # --- report body came from the model_output step, thoughts excluded ---
    notes = list(output_dir.glob("*.md"))
    assert len(notes) == 1
    body = notes[0].read_text(encoding="utf-8")
    assert "# Findings" in body
    assert "**Sources:**" in body
    assert "internal reasoning" not in body
    assert "interaction_id: iid-2x-001" in body

    # --- ledger got exactly one entry at the predicted DR cost ---
    entries = json.loads(ledger.read_text(encoding="utf-8"))
    assert len(entries) == 1
    assert entries[0]["interaction_id"] == "iid-2x-001"
    assert entries[0]["cost_usd"] == pytest.approx(2.80)
