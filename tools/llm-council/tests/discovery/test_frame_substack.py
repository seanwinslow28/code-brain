from datetime import date

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame_substack import frame_substack, PostAngle
from council.discovery.scoring import ScoreBreakdown

TODAY = date(2026, 6, 29)


def _bundle(urls, engagement=50):
    b = EvidenceBundle()
    for i, u in enumerate(urls):
        b.add(EvidenceRecord("reddit", f"author{i}", u, "2026-06-20", f"q{i}", engagement=engagement))
    return b


def _vpp(title, intensity, urls, summary="it breaks", segment="PMs"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment=segment, recency="2026-06",
                            consensus="4/4 models")
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def test_angles_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3", "https://c.com/4", "https://d.com/5"])
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    bundle = _bundle(["https://a.com/1", "https://a.com/2", "https://b.com/3",
                      "https://c.com/4", "https://d.com/5"])
    angles, quote_bank = frame_substack([low, high, dropped], FusionResult(), bundle, today=TODAY)
    assert [a.title for a in angles] == ["High", "Low"]
    assert all(isinstance(a, PostAngle) and isinstance(a.score, ScoreBreakdown)
               and a.score.composite > 0 for a in angles)
    assert len(angles) == 2
    assert any("High quote" in q for q in quote_bank)


def test_angle_fills_itch_transfer_and_audience_from_segment():
    bundle = _bundle(["https://a.com/1"])
    angles, _ = frame_substack([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(),
                               bundle, segment="solo founders", today=TODAY)
    a = angles[0]
    assert "Slow export" in a.itch
    assert a.transfer.lower().startswith("after reading")
    assert a.audience == "solo founders"          # CLI segment overrides the per-pain segment
    assert a.hook                                  # an open-loop hook is present


def test_whitespace_comes_from_blind_spots():
    fr = FusionResult(blind_spots=["nobody covers recovery UX", "no mobile angle"])
    bundle = _bundle(["https://a.com/1"])
    angles, _ = frame_substack([_vpp("Data loss", 5, ["https://a.com/1"])], fr, bundle, today=TODAY)
    assert "recovery UX" in angles[0].whitespace
