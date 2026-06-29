# council/discovery/bet.py
"""D1 — the 'proposed bet' card slot, $0 and non-fabricating.

Deterministically classifies a pain into one of five SHAPES by keyword, then emits the
matching riskiest-assumption CATEGORY + cheapest-test PATTERN. It names a structural
starting point (a real category, a test pattern) — never a fabricated specific insight.
Rendered under a 'heuristic — confirm against evidence' label with a human fill-in slot.
"""

from dataclasses import dataclass

from council.discovery.fusion import CandidatePainPoint


@dataclass(frozen=True)
class ProposedBet:
    shape: str
    riskiest_assumption: str
    cheapest_test: str


# first match wins — order = priority
_SHAPE_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("trust-gap", ("wrong", "hallucinat", "inaccurate", "unreliable", "trust", "error",
                   "made up", "made-up")),
    ("cost-pain", ("expensive", "pricing", "price", "cost", "afford", "too much", "paywall")),
    ("integration-gap", ("integrat", "api", "connect", "sync", "compat", "plugin")),
    ("workflow-friction", ("slow", "tedious", "manual", "workaround", "friction",
                           "clunky", "too many steps")),
]

_SHAPE_BETS: dict[str, tuple[str, str]] = {
    "trust-gap": (
        "that users will trust an automated correctness check enough to rely on it",
        "5 user interviews — do they describe verification/accuracy as a top-3 pain?"),
    "cost-pain": (
        "that price, not value perception, is the actual blocker to adoption",
        "a pricing-page / willingness-to-pay test against the current workaround's cost"),
    "integration-gap": (
        "that the missing integration is the deal-breaker, not a nice-to-have",
        "count how many complaints name the same target tool before building a connector"),
    "workflow-friction": (
        "that users will switch from their current workaround for a smoother flow",
        "time-on-task comparison of the current workaround vs a clickable prototype"),
    "missing-capability": (
        "that the capability is genuinely absent, not just undiscovered in existing tools",
        "a 5-tool teardown — does any competitor already solve this before you build?"),
}


def classify_pain_shape(point: CandidatePainPoint) -> str:
    hay = f"{point.title} {point.summary}".lower()
    for shape, kws in _SHAPE_KEYWORDS:
        if any(k in hay for k in kws):
            return shape
    return "missing-capability"


def propose_bet(point: CandidatePainPoint) -> ProposedBet:
    shape = classify_pain_shape(point)
    risk, test = _SHAPE_BETS[shape]
    return ProposedBet(shape=shape, riskiest_assumption=risk, cheapest_test=test)
