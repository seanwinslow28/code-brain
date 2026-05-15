from council.prompts import (
    fanout_prompt,
    crossrank_prompt,
    chairman_prompt,
)


def test_fanout_prompt_includes_user_query():
    p = fanout_prompt(user_query="Write a haiku about pythons.")
    assert "Write a haiku about pythons." in p


def test_crossrank_prompt_anonymizes_with_letters():
    others = [
        {"model_id": "openai/gpt-X", "content": "Response one body."},
        {"model_id": "anthropic/claude-X", "content": "Response two body."},
        {"model_id": "google/gemini-X", "content": "Response three body."},
    ]
    p = crossrank_prompt(user_query="Q", others=others)
    # Anonymized labels A, B, C appear; real model IDs do NOT
    assert "Response A" in p
    assert "Response B" in p
    assert "Response C" in p
    assert "openai/gpt-X" not in p
    assert "anthropic/claude-X" not in p
    assert "google/gemini-X" not in p
    # All response bodies are present
    assert "Response one body." in p
    assert "Response two body." in p
    assert "Response three body." in p


def test_crossrank_prompt_requests_json_ranking():
    p = crossrank_prompt(user_query="Q", others=[
        {"model_id": "m1", "content": "c1"},
        {"model_id": "m2", "content": "c2"},
    ])
    # The prompt instructs the model to return a JSON object with `ranking` and `reasoning`
    assert "JSON" in p or "json" in p
    assert "ranking" in p
    assert "reasoning" in p


def test_chairman_prompt_includes_named_responses_and_rankings():
    responses = [
        {"model_id": "openai/gpt-X", "content": "Resp A"},
        {"model_id": "anthropic/claude-X", "content": "Resp B"},
    ]
    rankings = [
        {"judge_model": "openai/gpt-X", "ranking": ["B", "A"], "reasoning": "B was more concise."},
        {"judge_model": "anthropic/claude-X", "ranking": ["A", "B"], "reasoning": "A had better insight."},
    ]
    p = chairman_prompt(user_query="Q", responses=responses, rankings=rankings)
    # Chairman sees real model IDs (NOT anonymized — synthesis benefits from naming)
    assert "openai/gpt-X" in p
    assert "anthropic/claude-X" in p
    # Both response bodies and reasoning are present
    assert "Resp A" in p
    assert "Resp B" in p
    assert "B was more concise." in p
    assert "A had better insight." in p
