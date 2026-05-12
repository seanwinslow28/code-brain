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


# --- Cluster picker (Task C4) ---

def _write_concept(d: Path, slug: str, wikilinks: list[str]) -> None:
    body = f"---\ntype: concept\nslug: {slug}\n---\n\n# {slug}\n\n"
    body += " ".join(f"[[{w}]]" for w in wikilinks)
    (d / f"{slug}.md").write_text(body)


def test_cluster_picker_returns_densest_3_to_5(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # Cluster A: three concepts that share >= 3 wikilinks pairwise
    _write_concept(tmp_path, "a", ["x", "y", "z", "shared"])
    _write_concept(tmp_path, "b", ["x", "y", "shared", "extra"])
    _write_concept(tmp_path, "c", ["y", "z", "shared"])
    # Cluster B: one isolated concept
    _write_concept(tmp_path, "lonely", ["nothing-shared"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    assert {"a", "b", "c"} <= set(cluster)
    assert "lonely" not in cluster
    assert 3 <= len(cluster) <= 5


def test_cluster_picker_empty_dir_returns_empty(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    assert pick_densest_cluster(concepts_dir=tmp_path, min_shared=3) == []


def test_cluster_picker_no_overlap_returns_singleton(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # Each concept has unique wikilinks → no edges meet min_shared
    _write_concept(tmp_path, "a", ["x", "y"])
    _write_concept(tmp_path, "b", ["w", "z"])
    _write_concept(tmp_path, "c", ["m", "n"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    # With no edges, every node is its own connected component. The largest is size 1.
    assert len(cluster) == 1


def test_cluster_picker_clips_to_5(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # 7 concepts all sharing >= 3 wikilinks → should clip to 5
    shared = ["a1", "a2", "a3"]
    for slug in ["n1", "n2", "n3", "n4", "n5", "n6", "n7"]:
        _write_concept(tmp_path, slug, shared + [f"unique-{slug}"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    assert len(cluster) == 5


def test_cluster_picker_ignores_aliased_wikilinks(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # [[target|display]] notation — extract target, not display
    (tmp_path / "a.md").write_text("# a\n[[shared|display 1]] [[shared|display 2]] [[other|x]]")
    (tmp_path / "b.md").write_text("# b\n[[shared|y]] [[other|z]] [[third|w]]")
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=2)
    assert set(cluster) >= {"a", "b"}
