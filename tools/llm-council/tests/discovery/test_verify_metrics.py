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


def test_phantom_cited_url_is_a_hard_precision_miss():
    # Option (c): a url the model cited but that was NEVER fetched into the bundle is
    # unverifiable -> it counts in the precision denominator, never in the numerator.
    # This is the multi-quote edge case where the OLD semantics inflated precision to 1.0:
    # the point is verified (q1 substring-present at url1) but not all-claims-supported
    # (q2 is nowhere), so the OLD redundancy test counted BOTH the phantom and url1 as
    # "load-bearing" -> 2/2 = 1.0. Option (c) makes the phantom a hard miss -> 1/2 = 0.5.
    b = _bundle(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports silently drop rows"))
    pt = CandidatePainPoint(
        "Export", "s",
        ["silently drop rows", "it also lacks SSO"],          # q1 supported at url1, q2 nowhere
        ["https://r.com/1", "https://phantom.com/never-fetched"],
        intensity=5,
    )
    s = FakeScorer(prob=0.0)  # only substring can support; q2 has neither substring nor entailment
    verified = verify_pain_points([pt], b, scorer=s)
    assert verified[0].verified is True                        # q1 keeps the point alive
    m = citation_metrics(verified, b, scorer=s)
    assert m.precision == 0.5  # url1 contributes, phantom is a hard miss (never numerator)
