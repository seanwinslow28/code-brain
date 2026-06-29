from council.discovery.fusion import CandidatePainPoint
from council.discovery.dedup import (
    normalize_tokens, jaccard, pain_similarity, _point_text,
    SIM_THRESHOLD, MMR_LAMBDA,
)


def test_normalize_tokens_lowercases_strips_punct_and_stopwords():
    toks = normalize_tokens("The Export FAILS, silently!")
    assert toks == frozenset({"export", "fails", "silently"})   # "the" dropped, punct stripped


def test_jaccard_basic_and_empty():
    assert jaccard(frozenset(), frozenset()) == 0.0             # two empty => non-duplicate
    assert jaccard(frozenset({"a"}), frozenset({"a"})) == 1.0
    assert jaccard(frozenset({"a", "b"}), frozenset({"b", "c"})) == 1 / 3


def test_pain_similarity_word_reorder_is_high():
    a = "exports fail silently on conflict"
    b = "on conflict, exports silently fail"
    assert pain_similarity(a, b) == 1.0                          # same content tokens, reordered


def test_pain_similarity_distinct_pains_low():
    a = "exports fail silently"
    b = "onboarding tutorial is confusing"
    assert pain_similarity(a, b) < SIM_THRESHOLD


def test_point_text_joins_title_and_summary():
    pt = CandidatePainPoint("Export loss", "notes vanish on conflict", [], [])
    assert _point_text(pt) == "Export loss. notes vanish on conflict"


def test_constants_are_conservative():
    assert SIM_THRESHOLD == 0.5
    assert MMR_LAMBDA == 0.3


from council.discovery.verify import VerifiedPainPoint
from council.discovery.dedup import dedup_verified, MergeRecord


def _vpp(title, summary, *, urls, quotes=("q",), intensity=3, verified=True, supporting=None):
    pt = CandidatePainPoint(title, summary, list(quotes), list(urls), intensity=intensity)
    return VerifiedPainPoint(point=pt, verified=verified,
                             supporting_urls=list(supporting if supporting is not None else urls))


def test_dedup_merges_reordered_restatement_and_unions_evidence():
    a = _vpp("Exports fail silently", "exports silently fail on conflict",
             urls=["https://d1.com/a"], quotes=["exports fail silently"])
    b = _vpp("Silently failing exports", "on conflict exports fail silently",
             urls=["https://d2.com/b"], quotes=["silent export failure"])
    deduped, merges = dedup_verified([a, b])
    assert len(deduped) == 1
    merged = deduped[0]
    # union of supporting urls across both members (order-preserving, canonical first)
    assert set(merged.supporting_urls) == {"https://d1.com/a", "https://d2.com/b"}
    assert "exports fail silently" in merged.point.quotes and "silent export failure" in merged.point.quotes
    assert len(merges) == 1 and isinstance(merges[0], MergeRecord)
    assert merges[0].merged_titles                          # the absorbed title is recorded


def test_dedup_representative_is_strongest_evidence():
    weak = _vpp("Weak phrasing", "exports fail silently here",
                urls=["https://only.com/x"], intensity=5)            # 1 domain, high intensity
    strong = _vpp("Strong phrasing", "exports fail silently here",
                  urls=["https://a.com/x", "https://b.com/y"], intensity=3)   # 2 domains
    deduped, _ = dedup_verified([weak, strong])
    assert len(deduped) == 1
    assert deduped[0].point.title == "Strong phrasing"      # more distinct domains wins, not intensity


def test_dedup_does_not_merge_distinct_pains():
    a = _vpp("Export loss", "exports fail silently", urls=["https://a.com/x"])
    b = _vpp("Onboarding pain", "the onboarding tutorial confuses new users",
             urls=["https://b.com/y"])
    deduped, merges = dedup_verified([a, b])
    assert len(deduped) == 2 and merges == []


def test_dedup_bounded_no_transitive_collapse():
    # A~B and B~C are above threshold, but A~C is below it. Bounded merge-to-canonical compares each
    # point only against cluster SEEDS, so it must NOT collapse all three into one via B (the
    # transitive-closure over-merge trap). Expected: {A,B} merge on seed A; C stays separate.
    a = _vpp("export sync feature", "export sync feature", urls=["https://a.com/x"])
    b = _vpp("sync feature billing", "sync feature billing", urls=["https://b.com/y"])
    c = _vpp("feature billing invoice", "feature billing invoice", urls=["https://c.com/z"])
    deduped, _ = dedup_verified([a, b, c])
    assert len(deduped) == 2


def test_dedup_passes_unverified_through_untouched():
    good = _vpp("Real", "exports fail silently", urls=["https://a.com/x"])
    bad = _vpp("Fake", "never said", urls=["https://f.com/x"], verified=False, supporting=[])
    deduped, _ = dedup_verified([good, bad])
    assert any(not v.verified for v in deduped)              # unverified preserved


def test_dedup_injectable_similarity_fn():
    a = _vpp("totally", "different one", urls=["https://a.com/x"])
    b = _vpp("words", "entirely other", urls=["https://b.com/y"])
    deduped, _ = dedup_verified([a, b], similarity_fn=lambda x, y: 1.0)   # force everything equal
    assert len(deduped) == 1
