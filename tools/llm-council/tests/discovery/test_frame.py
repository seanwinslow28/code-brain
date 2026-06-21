from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame import frame_pm


def _vpp(title, intensity, urls):
    pt = CandidatePainPoint(title, "summary", quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment="PMs")
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def test_cards_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3"])  # 2 domains → higher corroboration
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    cards, quote_bank = frame_pm([low, high, dropped], FusionResult())
    assert [c.title for c in cards] == ["High", "Low"]
    assert all(c.score > 0 for c in cards)
    assert len(cards) == 2                       # unverified excluded
    assert any("High quote" in q for q in quote_bank)


def test_opportunity_line_references_pain():
    cards, _ = frame_pm([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult())
    assert "Slow export" in cards[0].pain
    assert cards[0].opportunity
