"""Integration-shaped tests for skill_optimizer agent."""
import subprocess
from unittest.mock import MagicMock
import pytest
from agents.skill_optimizer import (
    preflight_checks,
    SkillOptimizerConfig,
    generate_outputs,
)


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


class TestGenerateOutputs:
    def test_runs_n_generations_per_prompt(self):
        client = MagicMock()
        client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="generated text")],
            usage=MagicMock(input_tokens=100, output_tokens=200),
        )
        outputs = generate_outputs(
            client=client,
            skill_md_text="# skill body",
            prompts=[{"id": "p1", "prompt": "write x"}],
            runs_per_prompt=3,
        )
        assert len(outputs["p1"]) == 3
        assert all(o["text"] == "generated text" for o in outputs["p1"])
        assert client.messages.create.call_count == 3

    def test_returns_per_prompt_keyed_dict(self):
        client = MagicMock()
        client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="x")],
            usage=MagicMock(input_tokens=1, output_tokens=1),
        )
        outputs = generate_outputs(
            client=client,
            skill_md_text="",
            prompts=[{"id": "a", "prompt": "x"}, {"id": "b", "prompt": "y"}],
            runs_per_prompt=2,
        )
        assert set(outputs.keys()) == {"a", "b"}
        assert len(outputs["a"]) == 2 and len(outputs["b"]) == 2
