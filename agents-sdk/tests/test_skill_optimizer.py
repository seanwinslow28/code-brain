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
    _plateau,
    _llm_judge_avg,
    _diversity,
    _worst_criteria,
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


class TestPlateau:
    def test_returns_false_below_window(self):
        assert _plateau([0.7, 0.7], n=3) is False

    def test_returns_true_when_flat(self):
        assert _plateau([0.7, 0.7, 0.7], n=3) is True

    def test_returns_true_within_tolerance(self):
        # Spread of 0.003 is below the 0.005 default tolerance.
        assert _plateau([0.700, 0.701, 0.703], n=3) is True

    def test_returns_false_with_real_movement(self):
        assert _plateau([0.70, 0.75, 0.80], n=3) is False


class TestLLMJudgeAvg:
    def test_averages_only_judge_criteria(self):
        per = {
            "substack_format_intro": 1.0,        # structural — ignored
            "anti_pattern_overreference": 1.0,   # structural — ignored
            "stylometric_distance": 1.0,          # structural — ignored
            "signature_move_present": 0.6,
            "sounds_like_sean": 0.4,
            "no_anti_pattern_violation": 0.8,
        }
        assert _llm_judge_avg(per) == pytest.approx((0.6 + 0.4 + 0.8) / 3)

    def test_handles_missing_keys_as_zero(self):
        assert _llm_judge_avg({}) == 0.0


class TestDiversity:
    def test_high_similarity_when_outputs_identical(self):
        outputs = {
            "p1": [
                {"text": "the quick brown fox jumps over the lazy dog every morning"},
                {"text": "the quick brown fox jumps over the lazy dog every morning"},
            ]
        }
        assert _diversity(outputs) > 0.95

    def test_low_similarity_when_outputs_diverse(self):
        outputs = {
            "p1": [
                {"text": "the quick brown fox jumps over the lazy dog"},
                {"text": "completely unrelated prose with different vocabulary words entirely"},
            ]
        }
        assert _diversity(outputs) < 0.5

    def test_returns_zero_when_only_one_run_per_prompt(self):
        outputs = {"p1": [{"text": "only one run here"}]}
        assert _diversity(outputs) == 0.0


class TestWorstCriteria:
    def test_returns_top_n_worst_from_last_row(self):
        rows = [{
            "criterion_substack_format_intro": "0.95",
            "criterion_anti_pattern_overreference": "0.90",
            "criterion_stylometric_distance": "0.50",
            "criterion_signature_move_present": "0.70",
            "criterion_sounds_like_sean": "0.40",
            "criterion_no_anti_pattern_violation": "0.85",
        }]
        worst = _worst_criteria(rows)
        # Three lowest: sounds_like_sean (0.40), stylometric_distance (0.50), signature_move_present (0.70)
        assert worst[0] == "sounds_like_sean"
        assert worst[1] == "stylometric_distance"
        assert worst[2] == "signature_move_present"

    def test_returns_empty_for_no_rows(self):
        assert _worst_criteria([]) == []

    def test_skips_non_numeric_columns(self):
        rows = [{"criterion_substack_format_intro": "0.95", "iteration": "5"}]
        worst = _worst_criteria(rows)
        assert worst == ["substack_format_intro"]
