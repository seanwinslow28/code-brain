"""Tests for synth-manifest write path + lib.lint_report Phase D additions."""

from __future__ import annotations

import json
from pathlib import Path

from agents.vault_synthesizer import SynthesisResult, write_synth_manifest
from lib.lint_report import latest_synth_manifest, synth_health_summary


def _result(**overrides) -> SynthesisResult:
    """SynthesisResult with sensible Phase D defaults; override per test."""
    base = dict(
        status="ok",
        files_processed=3,
        concepts_written=5,
        connections_written=2,
        rejected_count=1,
        edges_written=4,
        edges_rejected=0,
        duration_seconds=12.34,
        model_used="qwen3-14b",
        wol_status="mbp_awake",
        run_id="2026-05-01T02:31:00",
    )
    base.update(overrides)
    return SynthesisResult(**base)


# ─── write_synth_manifest ─────────────────────────────────────────────────


def test_write_synth_manifest_creates_health_dir_if_missing(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    assert not (vault / "health").exists()
    path = write_synth_manifest(vault_root=vault, result=_result(), today="2026-05-01")
    assert (vault / "health").is_dir()
    assert path == vault / "health" / "synth-manifest-2026-05-01.json"
    assert path.exists()


def test_write_synth_manifest_payload_shape(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    path = write_synth_manifest(vault_root=vault, result=_result(), today="2026-05-01")
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["run_id"] == "2026-05-01T02:31:00"
    assert data["files_processed"] == 3
    assert data["concepts_written"] == 5
    assert data["connections_written"] == 2
    assert data["edges_written"] == 4
    assert data["edges_rejected"] == 0
    assert data["rejected_count"] == 1
    assert data["duration_seconds"] == 12.34
    assert data["model_used"] == "qwen3-14b"
    assert data["wol_status"] == "mbp_awake"
    assert data["status"] == "ok"


def test_write_synth_manifest_round_trips_to_dict(tmp_path: Path) -> None:
    """JSON parses cleanly back into a dict — no float precision loss
    on the duration_seconds round + no encoding surprises."""
    vault = tmp_path / "vault"
    path = write_synth_manifest(
        vault_root=vault,
        result=_result(duration_seconds=99.999, edges_written=0),
        today="2026-05-01",
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    # round() to 2dp per write_synth_manifest contract
    assert data["duration_seconds"] == 100.0
    assert data["edges_written"] == 0


def test_write_synth_manifest_atomic_replaces_existing(tmp_path: Path) -> None:
    """Second write to the same date overwrites cleanly — no .tmp leftover."""
    vault = tmp_path / "vault"
    write_synth_manifest(
        vault_root=vault, result=_result(edges_written=1), today="2026-05-01"
    )
    write_synth_manifest(
        vault_root=vault, result=_result(edges_written=99), today="2026-05-01"
    )

    files = sorted((vault / "health").glob("synth-manifest-*"))
    # Exactly one final file, no .tmp leftover.
    assert len(files) == 1
    assert files[0].name == "synth-manifest-2026-05-01.json"

    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["edges_written"] == 99


# ─── latest_synth_manifest ────────────────────────────────────────────────


def test_latest_synth_manifest_returns_none_when_missing(tmp_path: Path) -> None:
    assert latest_synth_manifest(tmp_path) is None
    (tmp_path / "health").mkdir()
    assert latest_synth_manifest(tmp_path) is None


def test_latest_synth_manifest_picks_newest_by_name_sort(tmp_path: Path) -> None:
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-04-15.json").write_text("{}", encoding="utf-8")
    (health / "synth-manifest-2026-05-01.json").write_text("{}", encoding="utf-8")
    (health / "synth-manifest-2026-04-30.json").write_text("{}", encoding="utf-8")
    latest = latest_synth_manifest(tmp_path)
    assert latest is not None
    assert latest.name == "synth-manifest-2026-05-01.json"


# ─── synth_health_summary ─────────────────────────────────────────────────


def test_synth_health_summary_empty_when_no_manifest(tmp_path: Path) -> None:
    """Caller suppresses the line entirely on a fresh vault."""
    assert synth_health_summary(tmp_path) == ""


def test_synth_health_summary_formats_counts(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    write_synth_manifest(vault_root=vault, result=_result(), today="2026-05-01")
    msg = synth_health_summary(vault)
    assert "last synth:" in msg
    assert "5 concepts" in msg
    assert "2 connections" in msg
    assert "4 edges" in msg
    assert "1 rejected" in msg
    assert "synth-manifest-2026-05-01.json" in msg


def test_synth_health_summary_tolerates_malformed_json(tmp_path: Path) -> None:
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-05-01.json").write_text(
        "{not valid json", encoding="utf-8"
    )
    # Must NOT raise — daily-driver morning brief depends on this safety net.
    assert synth_health_summary(tmp_path) == ""


def test_synth_health_summary_tolerates_non_dict_json(tmp_path: Path) -> None:
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-05-01.json").write_text("[1, 2, 3]", encoding="utf-8")
    assert synth_health_summary(tmp_path) == ""


def test_synth_health_summary_handles_missing_keys(tmp_path: Path) -> None:
    """Manifest with partial keys still produces a sensible summary."""
    health = tmp_path / "health"
    health.mkdir()
    (health / "synth-manifest-2026-05-01.json").write_text(
        json.dumps({"concepts_written": 7}), encoding="utf-8"
    )
    msg = synth_health_summary(tmp_path)
    assert "7 concepts" in msg
    assert "0 connections" in msg
    assert "0 edges" in msg
    assert "0 rejected" in msg
