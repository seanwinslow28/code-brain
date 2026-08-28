"""Structural worst-case reservation bounds for council graphs."""

from decimal import ROUND_CEILING, Decimal

from council.cli import PROMPT_MAX_BYTES
from council.discovery.fusion import (
    EVIDENCE_EMBED_MAX_BYTES as FUSION_EVIDENCE_EMBED_MAX_BYTES,
    FUSION_JUDGE_MAX_TOKENS,
    TOPIC_EMBED_MAX_BYTES as FUSION_TOPIC_EMBED_MAX_BYTES,
)
from council.discovery.gather.sonar import (
    SEGMENT_EMBED_MAX_BYTES as SONAR_SEGMENT_EMBED_MAX_BYTES,
    SONAR_MAX_TOKENS,
    TOPIC_EMBED_MAX_BYTES as SONAR_TOPIC_EMBED_MAX_BYTES,
)
from council.pipeline import (
    CHAIRMAN_MAX_TOKENS,
    CROSSRANK_MAX_TOKENS,
    FANOUT_MAX_TOKENS,
    RANKING_REASONING_EMBED_MAX_BYTES,
    RESPONSE_EMBED_MAX_BYTES,
)
from council.pricing import MODEL_PRICING_PER_1K, WEB_SEARCH_PRICE_PER_CALL


COUNCIL_CHAT_ENVELOPE_BYTES = 16384
SONAR_FRAMING_BYTES = 256
FUSION_FRAMING_BYTES = 1024
MAX_WEB_SEARCH_PRICE = max(WEB_SEARCH_PRICE_PER_CALL.values())
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


def _discovery_legs(tier) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    sonar_input = (
        SONAR_TOPIC_EMBED_MAX_BYTES
        + SONAR_SEGMENT_EMBED_MAX_BYTES
        + SONAR_FRAMING_BYTES
        + COUNCIL_CHAT_ENVELOPE_BYTES
    )
    judge_input = (
        FUSION_TOPIC_EMBED_MAX_BYTES
        + FUSION_EVIDENCE_EMBED_MAX_BYTES
        + FUSION_FRAMING_BYTES
        + COUNCIL_CHAT_ENVELOPE_BYTES
    )
    sonar_leg = _call_cost(tier.sonar_model, sonar_input, SONAR_MAX_TOKENS)
    judge_leg = _call_cost(tier.judge, judge_input, FUSION_JUDGE_MAX_TOKENS)
    web_leg = (
        Decimal((len(tier.panel) + 1) * tier.max_tool_calls)
        * Decimal(str(MAX_WEB_SEARCH_PRICE))
    )
    # DISCOVERY_ALLOWANCE: Fusion panel token spend and Perplexity search count are
    # server-side and therefore client-unboundable. Sean approved max_cost_per_run as
    # the declared estimate residual for those two terms (option A, 2026-07-18).
    allowance = Decimal(str(tier.max_cost_per_run))
    return sonar_leg, judge_leg, web_leg, allowance


def _ledger_bound(amount: Decimal) -> float:
    return float(amount.quantize(_LEDGER_MICRO, rounding=ROUND_CEILING))


def discovery_worst_case_reservation(tier) -> float:
    """Bound one discovery gather+fusion run with its declared estimate residual."""
    sonar_leg, judge_leg, web_leg, allowance = _discovery_legs(tier)
    return _ledger_bound(sonar_leg + 2 * judge_leg + web_leg + allowance)


def experiment_worst_case_reservation(tier) -> float:
    """Bound gather once plus two independent fusion arms."""
    sonar_leg, judge_leg, web_leg, allowance = _discovery_legs(tier)
    return _ledger_bound(sonar_leg + 2 * (2 * judge_leg + web_leg + allowance))
