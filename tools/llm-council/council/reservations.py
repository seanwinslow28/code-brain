"""Structural worst-case reservation bounds for council graphs."""

from decimal import ROUND_CEILING, Decimal

from council.cli import PROMPT_MAX_BYTES
from council.pipeline import (
    CHAIRMAN_MAX_TOKENS,
    CROSSRANK_MAX_TOKENS,
    FANOUT_MAX_TOKENS,
    RANKING_REASONING_EMBED_MAX_BYTES,
    RESPONSE_EMBED_MAX_BYTES,
)
from council.pricing import MODEL_PRICING_PER_1K


COUNCIL_CHAT_ENVELOPE_BYTES = 16384
_LEDGER_MICRO = Decimal("0.000001")
_THOUSAND = Decimal(1000)


def _call_cost(model: str, input_bytes: int, max_tokens: int) -> Decimal:
    prompt_price, completion_price = MODEL_PRICING_PER_1K[model]
    return (
        Decimal(input_bytes) * Decimal(str(prompt_price))
        + Decimal(max_tokens) * Decimal(str(completion_price))
    ) / _THOUSAND


def council_worst_case_cost(profile) -> float:
    """Price the maximum 13-call graph as a pre-dispatch structural bound.

    The reservation is a proof-shaped pre-dispatch bound; its validity must never
    depend on measured actuals.
    """
    try:
        members = tuple(profile.models)
        chairman = profile.chairman
    except (AttributeError, TypeError) as exc:
        raise ValueError("profile must define four member models and a chairman") from exc
    if (
        len(members) != 4
        or len(set(members)) != 4
        or any(not isinstance(model, str) or not model.strip() for model in members)
    ):
        raise ValueError("council reservation requires four unique nonblank member models")
    if not isinstance(chairman, str) or not chairman.strip():
        raise ValueError("chairman model must be a nonblank string")

    fanout_in = PROMPT_MAX_BYTES + COUNCIL_CHAT_ENVELOPE_BYTES
    crossrank_in = (
        PROMPT_MAX_BYTES
        + 3 * RESPONSE_EMBED_MAX_BYTES
        + COUNCIL_CHAT_ENVELOPE_BYTES
    )
    chairman_in = (
        PROMPT_MAX_BYTES
        + 4 * RESPONSE_EMBED_MAX_BYTES
        + 4 * RANKING_REASONING_EMBED_MAX_BYTES
        + COUNCIL_CHAT_ENVELOPE_BYTES
    )
    fanout = sum(
        (_call_cost(model, fanout_in, FANOUT_MAX_TOKENS) for model in members),
        Decimal(0),
    )
    crossrank = 2 * sum(
        (_call_cost(model, crossrank_in, CROSSRANK_MAX_TOKENS) for model in members),
        Decimal(0),
    )
    chairman_cost = _call_cost(chairman, chairman_in, CHAIRMAN_MAX_TOKENS)
    return float(
        (fanout + crossrank + chairman_cost).quantize(
            _LEDGER_MICRO, rounding=ROUND_CEILING
        )
    )
