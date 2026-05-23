"""Tests for lib/benchmark_scorers.py."""
import pytest
from lib.benchmark_scorers import (
    score_tool_call_json,
    compute_tokens_per_second,
    score_needle_recall,
    score_pi_gotcha_compat,
)


def test_valid_tool_call_passes():
    output = '{"name": "read_file", "arguments": {"path": "/etc/hosts"}}'
    schema = {"name": "read_file", "required": ["path"]}
    result = score_tool_call_json(output, schema)
    assert result["valid"] is True
    assert result["schema_match"] is True


def test_malformed_json_fails():
    output = '{"name": "read_file", "arguments": {path: "/x"'
    schema = {"name": "read_file", "required": ["path"]}
    result = score_tool_call_json(output, schema)
    assert result["valid"] is False


def test_wrong_tool_name_flagged():
    output = '{"name": "write_file", "arguments": {"path": "/x"}}'
    schema = {"name": "read_file", "required": ["path"]}
    result = score_tool_call_json(output, schema)
    assert result["valid"] is True
    assert result["schema_match"] is False


def test_missing_required_arg_flagged():
    output = '{"name": "read_file", "arguments": {}}'
    schema = {"name": "read_file", "required": ["path"]}
    result = score_tool_call_json(output, schema)
    assert result["valid"] is True
    assert result["schema_match"] is False


def test_tokens_per_second_basic():
    tps = compute_tokens_per_second(token_count=1024, elapsed_seconds=20.48)
    assert tps == pytest.approx(50.0, rel=1e-3)


def test_tokens_per_second_zero_elapsed_returns_zero():
    assert compute_tokens_per_second(token_count=100, elapsed_seconds=0) == 0.0


def test_needle_recall_finds_exact_string():
    response = "...the needle is BLUEFOX-9417 hidden at position 28000..."
    needle = "BLUEFOX-9417"
    result = score_needle_recall(response, needle)
    assert result["recalled"] is True


def test_needle_recall_misses_when_absent():
    response = "I cannot find the needle in this haystack."
    needle = "BLUEFOX-9417"
    result = score_needle_recall(response, needle)
    assert result["recalled"] is False


def test_pi_gotcha_compat_flags_developer_role_unsupported():
    sample_response_text = '{"error": "unknown role: developer"}'
    result = score_pi_gotcha_compat(sample_response_text, gotcha="developer_role")
    assert result["affected"] is True


def test_pi_gotcha_compat_passes_when_dev_role_handled():
    sample_response_text = '{"role": "assistant", "content": "Hello."}'
    result = score_pi_gotcha_compat(sample_response_text, gotcha="developer_role")
    assert result["affected"] is False
