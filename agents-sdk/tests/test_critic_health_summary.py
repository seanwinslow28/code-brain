import json
from pathlib import Path

import pytest

from lib.lint_report import critic_health_summary, latest_critic_manifest


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "health").mkdir(parents=True)
    return tmp_path


def test_latest_critic_manifest_returns_most_recent(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-21.json").write_text("{}")
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text("{}")
    p = latest_critic_manifest(tmp_vault)
    assert p is not None
    assert p.name == "critic-manifest-2026-05-22.json"


def test_critic_health_summary_empty_when_no_manifest(tmp_vault):
    assert critic_health_summary(tmp_vault) == ""


def test_critic_health_summary_status_ok(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "ok",
            "articles_critiqued": 2,
            "codex_failures": 0,
            "antigravity_failures": 0,
            "duration_seconds": 87.3,
            "expansions_written": [
                "vault/knowledge/expansions/foo.md",
                "vault/knowledge/expansions/bar.md",
            ],
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "✓" in s or "ok" in s.lower()
    assert "2" in s   # articles count
    assert "expansions" in s.lower()


def test_critic_health_summary_status_partial_surfaces_failures(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "partial",
            "articles_critiqued": 1,
            "codex_failures": 1,
            "antigravity_failures": 0,
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "partial" in s.lower()
    assert "codex" in s.lower()


def test_critic_health_summary_status_success_empty(tmp_vault):
    """MBP-offline / synth-skipped night: vault_critic ran and exited cleanly."""
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "success-empty",
            "articles_critiqued": 0,
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "no articles" in s.lower() or "0 articles" in s.lower()
