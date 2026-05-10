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
    _read_recent_rows,
    _load_anchors,
    _build_row,
    _build_snapshot,
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


class TestReadRecentRows:
    def test_returns_empty_when_file_missing(self, tmp_path):
        assert _read_recent_rows(tmp_path / "missing.tsv", n=5) == []

    def test_returns_last_n_rows(self, tmp_path):
        path = tmp_path / "r.tsv"
        path.write_text("a\tb\n1\t2\n3\t4\n5\t6\n")
        rows = _read_recent_rows(path, n=2)
        assert len(rows) == 2
        assert rows[-1]["a"] == "5"

    def test_returns_all_rows_when_n_exceeds_count(self, tmp_path):
        path = tmp_path / "r.tsv"
        path.write_text("a\tb\n1\t2\n")
        rows = _read_recent_rows(path, n=10)
        assert len(rows) == 1


class TestLoadAnchors:
    def test_returns_dict_with_all_modes(self, tmp_path, monkeypatch):
        # Fake voice-samples.md with one section per mode.
        fake_samples = tmp_path / "voice-samples.md"
        fake_samples.write_text(
            "# Samples\n\n"
            "### Sedaris Sample One\n"
            "> Mundane accumulation example with enough words to count as content easily here.\n\n"
            "**Why it works:** explanation\n\n"
            "### Thompson Gonzo Example\n"
            "I DEPLOYED TO PRODUCTION at 11:47 PM and everything broke instantly afterwards.\n\n"
            "### Kerouac Beat Flow Sample\n"
            "And the ferry — the slow gray crossing — and the cold coffee in my hand.\n\n"
            "### Vonnegut Minimalist Closer\n"
            "It sounds the same as it always did. I sound different. I have begun.\n\n"
        )
        # Patch the module-level path constant.
        from agents import skill_optimizer
        monkeypatch.setattr(
            skill_optimizer,
            "_VOICE_SAMPLES_PATH",
            fake_samples,
        )
        anchors = _load_anchors()
        assert "sedaris" in anchors and len(anchors["sedaris"]) >= 1
        assert "gonzo" in anchors and len(anchors["gonzo"]) >= 1
        assert "kerouac" in anchors and len(anchors["kerouac"]) >= 1
        assert "vonnegut" in anchors and len(anchors["vonnegut"]) >= 1

    def test_pads_thin_modes_with_sean_fallback(self, tmp_path, monkeypatch):
        fake_samples = tmp_path / "voice-samples.md"
        fake_samples.write_text(
            "# Samples\n\n"
            "### Sean general voice sample\n"
            "Some Sean voice prose here that has at least thirty words so the parser keeps it.\n\n"
            "Another Sean snippet that the parser will treat as separate from above one.\n\n"
        )
        from agents import skill_optimizer
        monkeypatch.setattr(skill_optimizer, "_VOICE_SAMPLES_PATH", fake_samples)
        anchors = _load_anchors()
        # Even though no Sedaris-tagged samples exist, sedaris key is non-empty (padded).
        assert len(anchors["sedaris"]) >= 2


class TestBuildRow:
    def test_includes_all_header_fields(self):
        train_result = {
            "per_criterion": {
                "substack_format_intro": 0.9,
                "anti_pattern_overreference": 0.8,
                "stylometric_distance": 0.7,
                "signature_move_present": 0.6,
                "sounds_like_sean": 0.5,
                "no_anti_pattern_violation": 0.4,
            },
        }
        row = _build_row(
            iteration=3,
            section="### Beat Flow Mode",
            rationale="tightened jewel-center bullet",
            train_score=0.65,
            holdout_score=0.60,
            surprise_outputs={},
            train_result=train_result,
            moving_avg=0.62,
            decision_info={"delta_mean": 0.05},
            decision="keep",
            tripwires=[],
            sonnet_agreement=0.92,
            duration_sec=420.5,
            cost_usd=4.15,
        )
        for k in RESULTS_HEADER:
            assert k in row
        assert row["iteration"] == 3
        assert row["mutation_section"] == "### Beat Flow Mode"
        assert row["kept_or_reverted"] == "keep"
        assert row["tripwires_triggered"] == ""

    def test_truncates_long_rationale_to_200_chars(self):
        long_rationale = "x" * 500
        row = _build_row(
            iteration=1, section="x", rationale=long_rationale, train_score=0.5,
            holdout_score=0.5, surprise_outputs={},
            train_result={"per_criterion": {}}, moving_avg=0.5,
            decision_info={"delta_mean": 0}, decision="revert", tripwires=[],
            sonnet_agreement=1.0, duration_sec=1.0, cost_usd=0.0,
        )
        assert len(row["mutation_summary"]) == 200


class TestBuildSnapshot:
    def test_uses_current_as_baseline_when_iter1(self):
        train_result = {
            "per_criterion": {
                "stylometric_distance": 0.7,
                "signature_move_present": 0.6,
                "sounds_like_sean": 0.5,
                "no_anti_pattern_violation": 0.5,
            },
            "binary_array": [],
        }
        snap = _build_snapshot(
            iteration=1, train_score=0.6, holdout_score=0.55,
            train_result=train_result, iter1_snapshot=None,
            sonnet_agreement=0.9, skill_md_text="word " * 500,
            holdout_history=[], diversity=0.4,
        )
        # When iter1, baseline equals current.
        assert snap.score_gain_vs_baseline == 0.0
        assert snap.skill_md_token_count == snap.skill_md_token_count_baseline

    def test_carries_iter1_baseline_through(self):
        iter1 = {
            "train_score": 0.50,
            "criterion_scores": {"signature_move_present": 0.5},
            "skill_md_token_count": 400,
            "stylometric_score": 0.6,
            "llm_judge_score": 0.5,
            "avg_inter_run_similarity": 0.3,
        }
        train_result = {
            "per_criterion": {
                "stylometric_distance": 0.7,
                "signature_move_present": 0.7,
                "sounds_like_sean": 0.7,
                "no_anti_pattern_violation": 0.7,
            },
            "binary_array": [],
        }
        snap = _build_snapshot(
            iteration=5, train_score=0.70, holdout_score=0.65,
            train_result=train_result, iter1_snapshot=iter1,
            sonnet_agreement=0.85, skill_md_text="word " * 600,
            holdout_history=[0.66, 0.65, 0.64], diversity=0.4,
        )
        assert snap.score_gain_vs_baseline == pytest.approx(0.20)
        assert snap.skill_md_token_count == 600
        assert snap.skill_md_token_count_baseline == 400
