"""Tests for lib.artifact_loader — operating-model artifact reads."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from lib import artifact_loader
from lib.artifact_loader import (
    DOMAINS,
    KINDS,
    artifact_path,
    clear_cache,
    load_artifact,
    load_heartbeats,
)


@pytest.fixture(autouse=True)
def _reset_cache():
    """Every test starts with an empty module-level cache."""
    clear_cache()
    yield
    clear_cache()


class TestArtifactPath:
    def test_path_composition(self, tmp_path: Path):
        p = artifact_path("the-block", "HEARTBEAT", tmp_path)
        assert p == tmp_path / "05_atlas/operating-models/the-block/HEARTBEAT.md"

    def test_respects_custom_subpath(self, tmp_path: Path):
        p = artifact_path("life-systems", "SOUL", tmp_path, subpath="custom/path")
        assert p == tmp_path / "custom/path/life-systems/SOUL.md"


class TestLoadArtifactHappyPath:
    def test_reads_confirmed_heartbeat_and_strips_frontmatter(self, tmp_artifacts: Path):
        body = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)
        assert body is not None
        assert body.startswith("# HEARTBEAT — The Block")
        assert "Sacred first hour" in body
        # Frontmatter must be stripped
        assert "---" not in body
        assert "status:" not in body

    def test_distinct_bodies_per_domain(self, tmp_artifacts: Path):
        block = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)
        creative = load_artifact("creative-studio", "HEARTBEAT", tmp_artifacts)
        life = load_artifact("life-systems", "HEARTBEAT", tmp_artifacts)
        assert "The Block" in block
        assert "Creative Studio" in creative
        assert "Life Systems" in life

    def test_returns_body_without_stripping_when_opted_out(self, tmp_artifacts: Path):
        body = load_artifact(
            "the-block", "HEARTBEAT", tmp_artifacts, strip_frontmatter=False
        )
        assert body is not None
        assert body.startswith("---\n")
        assert "status: confirmed" in body


class TestLoadArtifactMissingFile:
    def test_missing_file_returns_none(self, tmp_path: Path):
        result = load_artifact("the-block", "HEARTBEAT", tmp_path)
        assert result is None

    def test_missing_does_not_raise(self, tmp_path: Path):
        # Explicit: any sort of missing file — no exception propagates.
        load_artifact("life-systems", "USER", tmp_path)
        load_artifact("nonexistent-domain", "HEARTBEAT", tmp_path)


class TestRequireConfirmed:
    def _rewrite_status(self, tmp_artifacts: Path, domain: str, kind: str, status: str) -> None:
        path = artifact_path(domain, kind, tmp_artifacts)
        text = path.read_text(encoding="utf-8")
        text = text.replace("status: confirmed", f"status: {status}")
        path.write_text(text, encoding="utf-8")

    def test_draft_returns_none_when_required(self, tmp_artifacts: Path):
        self._rewrite_status(tmp_artifacts, "the-block", "USER", "draft")
        result = load_artifact("the-block", "USER", tmp_artifacts)
        assert result is None

    def test_draft_returns_body_when_not_required(self, tmp_artifacts: Path):
        self._rewrite_status(tmp_artifacts, "the-block", "USER", "draft")
        result = load_artifact(
            "the-block", "USER", tmp_artifacts, require_confirmed=False
        )
        assert result is not None
        assert "USER — the-block" in result

    def test_missing_frontmatter_returns_none_when_required(self, tmp_artifacts: Path):
        path = artifact_path("life-systems", "SOUL", tmp_artifacts)
        path.write_text("# No frontmatter\n\nJust body.\n", encoding="utf-8")
        assert load_artifact("life-systems", "SOUL", tmp_artifacts) is None


class TestCaching:
    def test_cache_hit_does_not_reread(self, tmp_artifacts: Path, monkeypatch):
        first = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)

        read_calls = {"count": 0}
        original = Path.read_text

        def counting_read(self, *args, **kwargs):
            read_calls["count"] += 1
            return original(self, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", counting_read)

        second = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)
        assert second == first
        assert read_calls["count"] == 0  # cache hit, no re-read

    def test_cache_invalidates_on_mtime_change(self, tmp_artifacts: Path):
        path = artifact_path("the-block", "HEARTBEAT", tmp_artifacts)
        first = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)
        assert first is not None

        # Advance mtime past the filesystem's resolution, then rewrite.
        time.sleep(0.01)
        new_body = (
            "---\n"
            "type: operating-model\n"
            "artifact: HEARTBEAT\n"
            "domain: [the-block]\n"
            "status: confirmed\n"
            "---\n\n"
            "# HEARTBEAT — The Block (revised)\n\n"
            "New content.\n"
        )
        path.write_text(new_body, encoding="utf-8")
        os.utime(path, (time.time() + 1, time.time() + 1))

        second = load_artifact("the-block", "HEARTBEAT", tmp_artifacts)
        assert second is not None
        assert "revised" in second


class TestLoadHeartbeats:
    def test_returns_three_domains(self, tmp_artifacts: Path):
        result = load_heartbeats(tmp_artifacts)
        assert set(result.keys()) == set(DOMAINS)
        for domain in DOMAINS:
            assert result[domain] is not None

    def test_missing_domain_maps_to_none(self, tmp_artifacts: Path):
        # Remove one domain's HEARTBEAT; the other two still load.
        missing = artifact_path("creative-studio", "HEARTBEAT", tmp_artifacts)
        missing.unlink()
        result = load_heartbeats(tmp_artifacts)
        assert result["creative-studio"] is None
        assert result["the-block"] is not None
        assert result["life-systems"] is not None


class TestAllKindsReadable:
    def test_all_five_kinds_round_trip(self, tmp_artifacts: Path):
        # Sanity check: every (domain, kind) the fixture creates is loadable.
        for domain in DOMAINS:
            for kind in KINDS:
                body = load_artifact(domain, kind, tmp_artifacts)
                assert body is not None, f"failed to load {domain}/{kind}"
