from council.discovery.fusion import CandidatePainPoint
from council.discovery.bet import classify_pain_shape, propose_bet, ProposedBet


def _pt(title, summary=""):
    return CandidatePainPoint(title, summary, quotes=[], urls=[])


def test_each_shape_classified_by_keyword():
    assert classify_pain_shape(_pt("AI hallucinates fake APIs")) == "trust-gap"
    assert classify_pain_shape(_pt("Too expensive for solo devs")) == "cost-pain"
    assert classify_pain_shape(_pt("No Jira integration")) == "integration-gap"
    assert classify_pain_shape(_pt("Export is painfully slow and manual")) == "workflow-friction"
    assert classify_pain_shape(_pt("Wish it could generate diagrams")) == "missing-capability"


def test_priority_order_trust_beats_workflow():
    # contains both "slow" (workflow) and "wrong" (trust) -> trust wins (higher priority)
    assert classify_pain_shape(_pt("It's slow AND returns wrong answers")) == "trust-gap"


def test_propose_bet_returns_stable_populated_struct():
    bet = propose_bet(_pt("AI hallucinates fake APIs"))
    assert isinstance(bet, ProposedBet)
    assert bet.shape == "trust-gap"
    assert bet.riskiest_assumption and bet.cheapest_test
    # deterministic
    assert propose_bet(_pt("AI hallucinates fake APIs")) == bet


def test_default_fallback_is_missing_capability():
    bet = propose_bet(_pt("Something vague", "no matching keywords here"))
    assert bet.shape == "missing-capability"


def test_every_shape_has_a_bet_entry():
    from council.discovery.bet import _SHAPE_KEYWORDS, _SHAPE_BETS
    shapes = {s for s, _ in _SHAPE_KEYWORDS} | {"missing-capability"}
    assert shapes == set(_SHAPE_BETS), "every classifiable shape must have a bet"


def test_cost_pain_bet_is_about_pricing():
    bet = propose_bet(_pt("Too expensive for solo devs"))
    assert bet.shape == "cost-pain"
    assert "pric" in bet.cheapest_test.lower() or "pay" in bet.cheapest_test.lower()
