from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame_substack import frame_substack, PostAngle


def _vpp(title, intensity, urls, summary="it breaks", segment="PMs"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment=segment)
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def test_angles_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3"])   # 2 domains → higher corroboration
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    angles, quote_bank = frame_substack([low, high, dropped], FusionResult())
    assert [a.title for a in angles] == ["High", "Low"]
    assert all(isinstance(a, PostAngle) and a.score > 0 for a in angles)
    assert len(angles) == 2                       # unverified excluded
    assert any("High quote" in q for q in quote_bank)


def test_angle_fills_itch_transfer_and_audience_from_segment():
    angles, _ = frame_substack([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(),
                               segment="solo founders")
    a = angles[0]
    assert "Slow export" in a.itch
    assert a.transfer.lower().startswith("after reading")
    assert a.audience == "solo founders"          # CLI segment overrides the per-pain segment
    assert a.hook                                  # an open-loop hook is present


def test_whitespace_comes_from_blind_spots():
    fr = FusionResult(blind_spots=["nobody covers recovery UX", "no mobile angle"])
    angles, _ = frame_substack([_vpp("Data loss", 5, ["https://a.com/1"])], fr)
    assert "recovery UX" in angles[0].whitespace
