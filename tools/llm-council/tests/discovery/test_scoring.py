from datetime import date

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint
from council.discovery.scoring import (
    ScoreBreakdown, score_opportunity, _parse_loose_date, _parse_consensus,
    CONF_FLOOR,
)

TODAY = date(2026, 6, 29)


def _bundle(*recs):
    b = EvidenceBundle()
    for r in recs:
        b.add(r)
    return b


def _pt(intensity=3, recency="2026-06", consensus="4/4 models"):
    return CandidatePainPoint("Title", "summary", quotes=["q"], urls=[],
                              intensity=intensity, recency=recency, consensus=consensus)


def test_parse_loose_date_handles_formats_and_garbage():
    assert _parse_loose_date("2026-06-15") == date(2026, 6, 15)
    assert _parse_loose_date("2026-06") == date(2026, 6, 1)
    assert _parse_loose_date("2026") == date(2026, 1, 1)
    assert _parse_loose_date("last week") is None
    assert _parse_loose_date("") is None


def test_parse_consensus_ratio():
    assert _parse_consensus("4/4 models") == 1.0
    assert _parse_consensus("3/4") == 0.75
    assert _parse_consensus("garbage") == 0.0
    assert _parse_consensus("") == 0.0


def test_full_evidence_scores_near_max_confidence():
    urls = [f"https://d{i}.com/x" for i in range(4)]
    recs = [EvidenceRecord("reddit", f"author{i}", urls[i], "2026-06-20", "q", engagement=200)
            for i in range(4)]
    s = score_opportunity(_pt(intensity=5), urls, _bundle(*recs), today=TODAY)
    assert s.confidence > 0.95
    assert s.distinct_domains == 4
    assert s.composite == round(100 * s.value * s.confidence, 1)


def test_single_source_is_discounted_even_with_full_consensus():
    rec = EvidenceRecord("reddit", "solo", "https://one.com/x", "2026-06-20", "q", engagement=999)
    s = score_opportunity(_pt(intensity=5, consensus="4/4 models"),
                          ["https://one.com/x"], _bundle(rec), today=TODAY)
    assert s.distinct_domains == 1
    assert s.confidence < 0.8
    assert s.confidence >= CONF_FLOOR


def test_reach_is_log_damped_not_linear():
    rec_lo = EvidenceRecord("reddit", "a", "https://a.com/x", "2026-06-20", "q", engagement=10)
    rec_hi = EvidenceRecord("reddit", "a", "https://a.com/x", "2026-06-20", "q", engagement=1000)
    lo = score_opportunity(_pt(), ["https://a.com/x"], _bundle(rec_lo), today=TODAY)
    hi = score_opportunity(_pt(), ["https://a.com/x"], _bundle(rec_hi), today=TODAY)
    assert hi.reach > lo.reach
    assert hi.reach < lo.reach * 3


def test_missing_intensity_floors_at_one():
    s = score_opportunity(_pt(intensity=0), [], EvidenceBundle(), today=TODAY)
    assert s.intensity == 1
    assert s.importance == 0.2


def test_unparseable_recency_is_neutral():
    s = score_opportunity(_pt(recency="recently"), [], EvidenceBundle(), today=TODAY)
    assert s.recency == 0.5
    assert s.evidence_date == ""


def test_recency_floor_holds_for_old_evidence():
    s = score_opportunity(_pt(recency="2020-01"), [], EvidenceBundle(), today=TODAY)
    assert s.recency == 0.3


def test_sensitivity_sanity_corroborated_mid_beats_single_high():
    multi_urls = [f"https://d{i}.com/x" for i in range(4)]
    multi = score_opportunity(
        _pt(intensity=3),
        multi_urls,
        _bundle(*[EvidenceRecord("reddit", f"a{i}", multi_urls[i], "2026-06-20", "q", engagement=150)
                  for i in range(4)]),
        today=TODAY)
    single = score_opportunity(
        _pt(intensity=5),
        ["https://one.com/x"],
        _bundle(EvidenceRecord("reddit", "solo", "https://one.com/x", "2026-06-20", "q", engagement=150)),
        today=TODAY)
    assert multi.composite > single.composite
