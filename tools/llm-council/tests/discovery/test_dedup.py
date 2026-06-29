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
