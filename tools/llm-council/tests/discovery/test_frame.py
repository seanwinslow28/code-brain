from datetime import date

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame import frame_pm, IdeaCard
from council.discovery.scoring import ScoreBreakdown
from council.discovery.bet import ProposedBet

TODAY = date(2026, 6, 29)


def _vpp(title, intensity, urls, summary="summary", consensus="4/4 models"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment="PMs", recency="2026-06",
                            consensus=consensus)
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def _bundle(urls, engagement=50):
    b = EvidenceBundle()
    for i, u in enumerate(urls):
        b.add(EvidenceRecord("reddit", f"author{i}", u, "2026-06-20", f"q{i}", engagement=engagement))
    return b


def test_cards_sorted_by_composite_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3", "https://c.com/4", "https://d.com/5"])
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    bundle = _bundle(["https://a.com/1", "https://a.com/2", "https://b.com/3",
                      "https://c.com/4", "https://d.com/5"])
    cards, quote_bank = frame_pm([low, high, dropped], FusionResult(), bundle, today=TODAY)
    assert [c.title for c in cards] == ["High", "Low"]
    assert all(isinstance(c.score, ScoreBreakdown) and c.score.composite > 0 for c in cards)
    assert len(cards) == 2
    assert any("High quote" in q for q in quote_bank)


def test_card_leads_with_verbatim_quote_and_has_bet_and_why_now():
    bundle = _bundle(["https://a.com/1"])
    cards, _ = frame_pm([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(), bundle, today=TODAY)
    c = cards[0]
    assert c.lead_quote == "Slow export quote"     # leads with the verbatim quote
    assert "Slow export" in c.pain
    assert isinstance(c.bet, ProposedBet) and c.bet.shape == "workflow-friction"
    assert c.why_now                                # deterministic, non-empty
    assert c.who == "PMs"


def test_why_now_reflects_recency_state():
    bundle = _bundle(["https://a.com/1"])
    fresh = _vpp("Fresh", 3, ["https://a.com/1"])
    old = _vpp("Old", 3, ["https://a.com/1"])
    old.point.__dict__["recency"] = "2020-01"      # force an old date
    cf, _ = frame_pm([fresh], FusionResult(), bundle, today=TODAY)
    co, _ = frame_pm([old], FusionResult(), bundle, today=TODAY)
    assert "Fresh signal" in cf[0].why_now
    assert "Older signal" in co[0].why_now


from council.discovery.velocity import VelocitySignal
from council.discovery.frame import _velocity_term


class _FakeProvider:
    def __init__(self, mapping):
        self.mapping = mapping
        self.calls = 0

    def measure_batch(self, terms):
        self.calls += 1
        return {t: self.mapping.get(t) for t in terms}


def _sig(term, normalized):
    return VelocitySignal(term=term, slope=(normalized - 0.5) * 2, normalized=normalized,
                          source="pytrends", window_days=90, points=5)


def test_velocity_term_uses_title_then_topic_fallback():
    pt = CandidatePainPoint("Slow CSV Export!", "s", quotes=["q"], urls=[])
    assert _velocity_term(pt, "pm tools") == "slow csv export"
    empty = CandidatePainPoint("", "s", quotes=["q"], urls=[])
    assert _velocity_term(empty, "pm tools") == "pm tools"        # fallback


def test_why_now_leads_with_velocity_when_present():
    bundle = _bundle(["https://a.com/1"])
    prov = _FakeProvider({"rising pain": _sig("rising pain", 0.9)})
    cards, _ = frame_pm([_vpp("Rising pain", 4, ["https://a.com/1"])], FusionResult(), bundle,
                        today=TODAY, topic="pm", velocity_provider=prov, velocity_weight=0.2)
    assert prov.calls == 1                                        # exactly one batched call
    wn = cards[0].why_now
    assert "accelerating" in wn.lower() and "pytrends" in wn.lower()


def test_why_now_falls_back_to_recency_without_signal():
    bundle = _bundle(["https://a.com/1"])
    # provider returns None for this term -> graceful fallback to the recency note
    prov = _FakeProvider({})
    cards, _ = frame_pm([_vpp("No trend", 3, ["https://a.com/1"])], FusionResult(), bundle,
                        today=TODAY, topic="pm", velocity_provider=prov)
    assert "signal" in cards[0].why_now.lower()                  # the recency-style note
    assert "pytrends" not in cards[0].why_now.lower()


def test_frame_pm_without_provider_is_unchanged_default_path():
    bundle = _bundle(["https://a.com/1"])
    cards, _ = frame_pm([_vpp("X", 3, ["https://a.com/1"])], FusionResult(), bundle, today=TODAY)
    assert cards[0].score.velocity_source == "" and cards[0].why_now  # no provider -> neutral


def test_velocity_signal_never_leaks_into_evidence_or_quotes():
    bundle = _bundle(["https://a.com/1"])
    v = _vpp("Leak check", 4, ["https://a.com/1"])
    prov = _FakeProvider({"leak check": _sig("leak check", 0.9)})
    cards, _ = frame_pm([v], FusionResult(), bundle, today=TODAY, topic="pm",
                        velocity_provider=prov, velocity_weight=0.3)
    c = cards[0]
    assert c.evidence_urls == v.supporting_urls      # unchanged by velocity
    assert c.quotes == v.point.quotes                # unchanged by velocity
    assert c.score.velocity_source == "pytrends"     # signal WAS attached (to the score only)
