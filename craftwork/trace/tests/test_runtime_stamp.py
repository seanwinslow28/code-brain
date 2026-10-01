"""The eleventh rung-0 line: a Claude pass's recorded runtime matches its raw log's model stamps.

Ruled on #321 (2026-09-29): the Agent tool's `opus` / `sonnet` aliases moved from
Opus 5 / Sonnet 5 to the 5.5 generation after pc-eng-001 closed, and nothing in
the studio noticed. An alias is not a pin, so the record's `runtime:` is checked
against the model the transcript itself says answered.
"""
import json
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, run_checks
from tracekit.engagement import load_engagement

LINE = CHECK_NAMES[10]


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def stamp(eng_dir: Path, pid: str, *models: str) -> None:
    """Replace a pass's stub log with Claude Code transcript lines stamped with these models."""
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": "seat brief"}})]
    for m in models:
        lines.append(json.dumps({"type": "assistant", "message": {"model": m, "role": "assistant", "content": []}}))
    (eng_dir / "trace" / "logs" / f"{pid}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def line(eng_dir: Path):
    checks = run_checks(load_engagement(eng_dir))
    return next(c for c in checks if c.name == LINE)


def test_the_line_is_the_eleventh_and_runs_last():
    assert len(CHECK_NAMES) == 11 and LINE == "Recorded runtime matches the raw log's model stamps"


def test_stub_logs_are_unverifiable_never_passed_or_failed(eng_dir):
    c = line(eng_dir)
    assert c.ok and c.n_ok == 0
    assert c.n_unverifiable == c.n_total == 19   # 13 Opus + 6 Sonnet passes; Codex and the coordinator are out of scope
    assert any("carry no model stamp" in n for n in c.notes)
    assert any("not a Claude row" in n for n in c.notes)


def test_a_matching_stamp_verifies_the_pass(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5", "claude-opus-5")
    c = line(eng_dir)
    assert c.ok and c.n_ok == 1 and c.n_unverifiable == 18


def test_an_alias_that_moved_is_a_finding_naming_both_models(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5-5", "claude-opus-5-5")
    c = line(eng_dir)
    assert not c.ok
    assert c.findings == ["pass-01: runtime claude-opus-5 but its raw log is stamped claude-opus-5-5"]


def test_a_second_model_in_one_log_is_a_finding(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5", "claude-haiku-4-5")
    c = line(eng_dir)
    assert c.findings == ["pass-01: runtime claude-opus-5 but its raw log is stamped claude-haiku-4-5, claude-opus-5"]


def test_synthetic_stamps_are_not_models(eng_dir):
    # Claude Code writes "<synthetic>" on messages no model produced; they say nothing about the runtime.
    stamp(eng_dir, "pass-01", "claude-opus-5", "<synthetic>")
    assert line(eng_dir).n_ok == 1


def test_a_missing_log_is_unverifiable_and_named(eng_dir):
    (eng_dir / "trace" / "logs" / "pass-01.jsonl").unlink()
    c = line(eng_dir)
    assert c.ok
    assert any("no readable JSONL raw log" in n and "pass-01" in n for n in c.notes)
