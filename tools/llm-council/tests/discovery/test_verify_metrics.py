from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint
from council.discovery.verify import verify_pain_points, citation_metrics
from tests.discovery.test_verify_entailment import FakeScorer


def _bundle(*recs):
    b = EvidenceBundle()
    for r in recs:
        b.add(r)
    return b


def test_metrics_none_without_scorer():
    b = _bundle(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports drop rows"))
    pt = CandidatePainPoint("Export", "s", ["exports drop rows"], ["https://r.com/1"], intensity=5)
    verified = verify_pain_points([pt], b)
    m = citation_metrics(verified, b, scorer=None)
    assert m.precision is None and m.recall is None


def test_recall_full_when_all_claims_supported():
    b = _bundle(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports silently drop rows"))
    pt = CandidatePainPoint("Export", "s", ["exports silently drop rows"], ["https://r.com/1"], intensity=5)
    s = FakeScorer(prob=0.9)
    verified = verify_pain_points([pt], b, scorer=s)
    m = citation_metrics(verified, b, scorer=s)
    assert m.recall == 1.0


def test_precision_flags_redundant_citation():
    # two citations, the claim is a verbatim substring of url1 only; url2 adds nothing -> redundant
    b = _bundle(
        EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports silently drop rows"),
        EvidenceRecord("reddit", "r", "https://r.com/2", "", "unrelated note about billing"),
    )
    pt = CandidatePainPoint("Export", "s", ["exports silently drop rows"],
                            ["https://r.com/1", "https://r.com/2"], intensity=5)
    s = FakeScorer(prob=0.0)  # no paraphrase help; rely on substring at url1
    verified = verify_pain_points([pt], b, scorer=s)
    m = citation_metrics(verified, b, scorer=s)
    assert m.precision == 0.5  # 1 of 2 citations contributes
