"""Integration-shaped tests for skill_optimizer agent."""
import subprocess
import pytest
from agents.skill_optimizer import preflight_checks, SkillOptimizerConfig


class TestPreflightChecks:
    def test_passes_on_correct_branch(self, tmp_path, monkeypatch):
        # Arrange a fake git repo on the expected branch.
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "autoresearch/writing-voice-modes-2026-05-09"], check=True, capture_output=True)
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        # Create stub files.
        (tmp_path / "SKILL.md").write_text("# Skill")
        (tmp_path / "evals.yaml").write_text("schema_version: 1")
        (tmp_path / "evals.sealed.yaml").write_text("schema_version: 1")
        (tmp_path / "baseline.json").write_text('{"_threshold": 5.0}')
        ok, reason = preflight_checks(config)
        assert ok, reason

    def test_fails_on_wrong_branch(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "main"], check=True, capture_output=True)
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        ok, reason = preflight_checks(config)
        assert not ok
        assert "branch" in reason.lower()

    def test_fails_when_threshold_unset(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "checkout", "-b", "autoresearch/writing-voice-modes-2026-05-09"], check=True, capture_output=True)
        (tmp_path / "SKILL.md").write_text("# Skill")
        (tmp_path / "evals.yaml").write_text("schema_version: 1")
        (tmp_path / "evals.sealed.yaml").write_text("schema_version: 1")
        (tmp_path / "baseline.json").write_text('{"_threshold": null}')
        config = SkillOptimizerConfig(
            branch="autoresearch/writing-voice-modes-2026-05-09",
            repo_root=tmp_path,
            target_skill_md=tmp_path / "SKILL.md",
            evals_path=tmp_path / "evals.yaml",
            evals_sealed_path=tmp_path / "evals.sealed.yaml",
            stylometry_baseline_path=tmp_path / "baseline.json",
        )
        ok, reason = preflight_checks(config)
        assert not ok
        assert "threshold" in reason.lower()
