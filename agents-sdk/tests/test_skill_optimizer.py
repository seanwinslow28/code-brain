"""Integration-shaped tests for skill_optimizer agent."""
import subprocess
from unittest.mock import MagicMock
import pytest
from agents.skill_optimizer import (
    preflight_checks,
    SkillOptimizerConfig,
    generate_outputs,
    score_outputs,
    git_commit_mutation,
    git_revert_skill_md,
    write_results_row,
    RESULTS_HEADER,
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


class TestScoreOutputs:
    def test_aggregates_structural_and_judge_scores(self):
        # Stub structural checks: every output passes substack format, fails anti-pattern.
        structural_results = {
            "p1": [
                {"substack_format_intro": True, "anti_pattern_overreference": False, "stylometric_distance": True},
                {"substack_format_intro": True, "anti_pattern_overreference": False, "stylometric_distance": True},
            ]
        }
        judge_results = {
            "p1": [
                {"signature_move_present": True, "sounds_like_sean": True, "no_anti_pattern_violation": False},
                {"signature_move_present": True, "sounds_like_sean": False, "no_anti_pattern_violation": True},
            ]
        }
        score = score_outputs(structural_results, judge_results)
        # 2 outputs x 6 criteria = 12 trials. Pass count: structural 2+0+2=4, judge 2+1+1=4 -> 8.
        assert score["total_passes"] == 8
        assert score["max_score"] == 12
        assert score["per_criterion"]["substack_format_intro"] == 1.0
        assert score["per_criterion"]["anti_pattern_overreference"] == 0.0


class TestGitOps:
    def test_revert_restores_original(self, tmp_path):
        subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "x@x.com"], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "x"], check=True)
        f = tmp_path / "skill.md"
        f.write_text("original")
        subprocess.run(["git", "-C", str(tmp_path), "add", "skill.md"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-m", "init"], check=True, capture_output=True)
        f.write_text("modified")
        git_revert_skill_md(tmp_path, f)
        assert f.read_text() == "original"


class TestResultsTSV:
    def test_writes_header_on_first_row(self, tmp_path):
        path = tmp_path / "results.tsv"
        row = {f: "" for f in RESULTS_HEADER}
        row["iteration"] = 1
        row["mutation_summary"] = "test mutation"
        write_results_row(path, row)
        contents = path.read_text()
        assert contents.split("\n")[0] == "\t".join(RESULTS_HEADER)
        assert "test mutation" in contents.split("\n")[1]

    def test_appends_without_duplicating_header(self, tmp_path):
        path = tmp_path / "results.tsv"
        for i in range(3):
            row = {f: "" for f in RESULTS_HEADER}
            row["iteration"] = i + 1
            write_results_row(path, row)
        lines = path.read_text().rstrip().split("\n")
        assert len(lines) == 4  # header + 3 rows
