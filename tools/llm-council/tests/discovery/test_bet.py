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
