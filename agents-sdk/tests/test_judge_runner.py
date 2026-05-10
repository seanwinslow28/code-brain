"""Tests for judge_runner module."""
import pytest
from unittest.mock import MagicMock
from lib.skill_optimizer.judge_runner import (
    JudgeRunner,
    JudgeResult,
)


PROMPT_TEMPLATE = """You are evaluating a Substack blog post intro against ONE binary criterion.

OUTPUT TO EVALUATE:
{output}

ANCHOR SAMPLES:

Sample 1:
{anchor_1}

Sample 2:
{anchor_2}

CRITERION:
{question}

Answer YES or NO on the last line.
"""


class TestSingleJudgeCall:
    def test_returns_yes_when_model_says_yes(self):
        client = MagicMock()
        client.complete.return_value = "It does match.\nYES"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="some output",
            anchors=["anchor a", "anchor b"],
            question="does it match?",
            mode="sean",
        )
        assert result.passed is True
        assert result.raw_response == "It does match.\nYES"

    def test_returns_no_when_model_says_no(self):
        client = MagicMock()
        client.complete.return_value = "Reasoning here.\nNO"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="x", anchors=["a", "b"], question="?", mode="sean"
        )
        assert result.passed is False

    def test_treats_ambiguous_response_as_failure(self):
        client = MagicMock()
        client.complete.return_value = "Maybe.\nUNCLEAR"
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_single(
            output="x", anchors=["a", "b"], question="?", mode="sean"
        )
        assert result.passed is False
        assert "ambiguous" in result.reason.lower()


class TestEnsembleJudge:
    def test_majority_yes_passes(self):
        client = MagicMock()
        # Three calls return YES, YES, NO → majority YES.
        client.complete.side_effect = ["...\nYES", "...\nYES", "...\nNO"]
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_ensemble(
            output="x",
            anchors=["a", "b", "c", "d"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        assert result.passed is True
        assert result.yes_count == 2 and result.no_count == 1

    def test_majority_no_fails(self):
        client = MagicMock()
        client.complete.side_effect = ["...\nNO", "...\nNO", "...\nYES"]
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        result = runner.judge_ensemble(
            output="x",
            anchors=["a", "b", "c", "d"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        assert result.passed is False
        assert result.yes_count == 1 and result.no_count == 2

    def test_uses_different_anchor_orders_per_judge(self):
        client = MagicMock()
        client.complete.side_effect = ["x\nYES"] * 3
        runner = JudgeRunner(
            local_client=client,
            sonnet_client=None,
            prompt_template=PROMPT_TEMPLATE,
        )
        runner.judge_ensemble(
            output="x",
            anchors=["a1", "a2", "a3", "a4"],
            question="?",
            mode="sean",
            n_judges=3,
        )
        prompts_sent = [call.kwargs["prompt"] for call in client.complete.call_args_list]
        # The three prompts should not all be identical (anchor order differs).
        assert len(set(prompts_sent)) > 1
