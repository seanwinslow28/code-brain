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
