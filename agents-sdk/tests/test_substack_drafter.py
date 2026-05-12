"""Tests for agents-sdk/agents/substack_drafter.py — voice-rotation module."""
from datetime import date
import pytest
from agents.substack_drafter import pick_voice_mode

# SPEC rotation table: 0=sean, 1=sedaris, 2=kerouac, 3=thompson, 4=vonnegut

def test_voice_mode_at_epoch():
    assert pick_voice_mode(today=date(2026, 5, 4), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_week_1():
    # 7 days after epoch → index 1 → sedaris
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4)) == "sedaris"


def test_voice_mode_week_2():
    # 14 days after epoch → index 2 → kerouac
    assert pick_voice_mode(today=date(2026, 5, 18), epoch=date(2026, 5, 4)) == "kerouac"


def test_voice_mode_week_3():
    # 21 days after epoch → index 3 → thompson
    assert pick_voice_mode(today=date(2026, 5, 25), epoch=date(2026, 5, 4)) == "thompson"


def test_voice_mode_week_4():
    # 28 days after epoch → index 4 → vonnegut
    assert pick_voice_mode(today=date(2026, 6, 1), epoch=date(2026, 5, 4)) == "vonnegut"


def test_voice_mode_wraps_at_5():
    # 35 days after epoch → index 5 → wraps to 0 → sean
    assert pick_voice_mode(today=date(2026, 6, 8), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_override_pins():
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="vonnegut") == "vonnegut"


def test_voice_mode_rejects_bad_override():
    with pytest.raises(ValueError):
        pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="hemingway")


# --- Synthesizer-dryness gate (Task C3) ---
import json
from pathlib import Path


def _write_manifest(d: Path, date_str: str, concepts: int, status: str = "ok") -> None:
    (d / f"synth-manifest-{date_str}.json").write_text(json.dumps({
        "status": status, "concepts_written": concepts, "duration_s": 12.0
    }))


def test_dryness_gate_blocks_when_last_3_are_zero(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 0)
    _write_manifest(tmp_path, "2026-05-31", 0)
    _write_manifest(tmp_path, "2026-06-01", 0)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_passes_when_last_3_have_output(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    _write_manifest(tmp_path, "2026-06-01", 7)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_passes_when_only_most_recent_3_have_output(tmp_path):
    # Even if older manifests were dry, the gate looks only at the last N.
    _write_manifest(tmp_path, "2026-05-25", 0)
    _write_manifest(tmp_path, "2026-05-26", 0)
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    _write_manifest(tmp_path, "2026-06-01", 7)
    from agents.substack_drafter import is_synthesizer_dry
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_blocks_when_one_of_last_3_is_zero(tmp_path):
    # Any single zero in the last N nights → dry. Conservative.
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 0)
    _write_manifest(tmp_path, "2026-06-01", 7)
    from agents.substack_drafter import is_synthesizer_dry
    # NOTE: spec is "exit no-op if last N have concepts_written == 0".
    # That implies ALL N must be zero. So this case is NOT dry.
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_handles_empty_dir(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    # No manifests yet → treat as dry (don't draft from nothing)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_handles_too_few_manifests(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    # Fewer than threshold manifests exist at all → treat as dry (insufficient signal)
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    # Only 2 manifests; threshold is 3 → dry
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_handles_unreadable_manifest(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    (tmp_path / "synth-manifest-2026-06-01.json").write_text("not valid json{")
    # Unreadable in the window → treat as dry to be safe
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True
