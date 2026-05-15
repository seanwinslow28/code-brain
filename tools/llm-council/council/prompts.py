"""System prompts for the three council stages.

Stage 1 (fan-out): each model receives the raw user query, no context about other models.
Stage 2 (cross-rank): each model receives the other N-1 responses with anonymized labels.
Stage 3 (chairman): one model receives the original query, all named responses, all rankings.

Lifted with attribution from karpathy/llm-council's prompts and adapted for our use cases.
"""

from typing import Iterable
import json


FANOUT_SYSTEM = """You are a member of an LLM Council. The user has posed a question to a panel \
of four frontier models, and you are one of them. Answer the user's question to the best of your \
ability. Be substantive, specific, and direct. Do not hedge unnecessarily. Your response will \
later be cross-ranked by the other council members and synthesized by a chairman."""


CROSSRANK_SYSTEM = """You are a member of an LLM Council reviewing the responses of the other \
council members to a user's question. You see anonymized responses labeled "Response A", \
"Response B", etc. — you do NOT know which model wrote which.

Rank the responses by overall quality (accuracy + insight + clarity), best first. Then briefly \
explain your ranking in 2-4 sentences.

You MUST return a single JSON object with exactly these keys:
{
  "ranking": ["A", "B", "C"],   // letters in descending quality order
  "reasoning": "string explaining the ranking"
}

Return ONLY the JSON object — no preamble, no markdown fence."""


CHAIRMAN_SYSTEM = """You are the Chairman of an LLM Council. Four other models have each \
independently answered a user's question, then cross-ranked each other's responses anonymously. \
You now see the original question, all four named responses, and all four rankings with reasoning.

Synthesize a single final response that:
1. Resolves disagreements between models (cite which model claimed what where useful)
2. Identifies points of convergence (high confidence) and divergence (low confidence)
3. Produces a direct, substantive answer to the user's original question

Be specific about which model contributed which insight. The user values seeing the lineage."""


def fanout_prompt(*, user_query: str) -> str:
    """Build the user-facing prompt for Stage 1. System prompt is FANOUT_SYSTEM."""
    return user_query


def crossrank_prompt(*, user_query: str, others: list[dict]) -> str:
    """Build the user-facing prompt for Stage 2. `others` is a list of {model_id, content} dicts
    for the OTHER N-1 council members (the judge's own response is excluded by the caller).

    Anonymizes model IDs with letters A, B, C, ... (per call — fresh mapping every cross-rank).
    """
    if not others:
        raise ValueError("crossrank_prompt requires at least one other response")
    labels = [chr(ord("A") + i) for i in range(len(others))]
    sections = "\n\n".join(
        f"=== Response {label} ===\n{o['content']}" for label, o in zip(labels, others)
    )
    return f"""The original user question:

{user_query}

You see {len(others)} other council members' responses below, anonymized:

{sections}

Return your ranking and reasoning as a JSON object per the system instructions."""


def chairman_prompt(*, user_query: str, responses: list[dict], rankings: list[dict]) -> str:
    """Build the user-facing prompt for Stage 3.

    `responses` is a list of {model_id, content}; `rankings` is a list of
    {judge_model, ranking, reasoning}.

    Unlike Stage 2, models are NAMED here — the chairman benefits from knowing lineage.
    """
    response_block = "\n\n".join(
        f"=== {r['model_id']} ===\n{r['content']}" for r in responses
    )
    ranking_block = "\n\n".join(
        f"=== {rk['judge_model']} ranked ===\n"
        f"Order (best first): {' > '.join(rk['ranking'])}\n"
        f"Reasoning: {rk['reasoning']}"
        for rk in rankings
    )
    return f"""Original user question:

{user_query}

=== Council responses (named) ===

{response_block}

=== Cross-rankings ===

{ranking_block}

Synthesize the final response per the system instructions."""
