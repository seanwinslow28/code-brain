# tests/discovery/test_verify_entailment.py
from council.discovery.verify import quote_supported_at_url, _claim_sentences


def test_claim_split_keeps_decimal_versions_intact():
    # "v3.0" must not fragment into "v3." + "0" (old naive split-on-every-dot bug)
    assert _claim_sentences("We use v3.0 now") == ["We use v3.0 now"]


def test_claim_split_keeps_title_abbreviations_intact():
    # "Mr." must not become a standalone spurious fragment that then has to be entailed
    assert _claim_sentences("Mr. Smith says exports drop rows") == ["Mr. Smith says exports drop rows"]


def test_claim_split_still_splits_real_sentences():
    # genuine sentence boundaries still split (and trailing punctuation is stripped)
    assert _claim_sentences("Exports drop rows. SSO is broken too") == ["Exports drop rows", "SSO is broken too"]


class FakeScorer:
    """Deterministic stand-in for the real NLI model. Maps (premise, hypothesis) -> entailment prob."""
    def __init__(self, prob=0.0, table=None):
        self.prob, self.table, self.calls = prob, table or {}, []
    def entails(self, *, premise, hypothesis):
        self.calls.append((premise, hypothesis))
        return self.table.get(hypothesis, self.prob)


def test_substring_hit_accepts_without_consulting_scorer():
    s = FakeScorer(prob=0.0)  # would reject everything if consulted
    assert quote_supported_at_url(cited_quote="exports fail silently",
                                  fetched_text="users say exports fail silently a lot", scorer=s) is True
    assert s.calls == []  # fast-path: scorer never consulted on a substring hit


def test_paraphrase_accepted_via_nli_on_substring_miss():
    s = FakeScorer(table={"the export feature loses data": 0.92})
    assert quote_supported_at_url(cited_quote="the export feature loses data",
                                  fetched_text="reviewers report exporting silently drops rows", scorer=s) is True


def test_unsupported_claim_rejected_when_nli_low():
    s = FakeScorer(prob=0.10)
    assert quote_supported_at_url(cited_quote="it has great SSO support",
                                  fetched_text="reviewers report exporting silently drops rows", scorer=s) is False


def test_substring_never_rejects_even_if_scorer_would():
    s = FakeScorer(prob=0.0)  # scorer says reject, but substring present must still accept
    assert quote_supported_at_url(cited_quote="drops rows",
                                  fetched_text="exporting silently drops rows", scorer=s) is True


def test_scorer_none_is_substring_only_todays_behavior():
    # paraphrase, no substring, no scorer -> reject exactly as today
    assert quote_supported_at_url(cited_quote="the export feature loses data",
                                  fetched_text="exporting silently drops rows", scorer=None) is False
    # substring still accepts with no scorer
    assert quote_supported_at_url(cited_quote="drops rows",
                                  fetched_text="exporting silently drops rows", scorer=None) is True


def test_multi_sentence_claim_requires_all_supported():
    # first sentence substring-present, second neither substring nor entailed -> overall reject (AND)
    s = FakeScorer(prob=0.0)
    assert quote_supported_at_url(cited_quote="drops rows. it also lacks SSO.",
                                  fetched_text="exporting silently drops rows", scorer=s) is False


def test_entailment_at_exact_tau_boundary_accepts():
    # prob exactly == _ENTAIL_TAU (0.5). The gate uses `>=`, so the boundary ACCEPTS.
    # Pins >= vs > so a future refactor can't silently flip it (today only 0.92/0.10 tested).
    s = FakeScorer(prob=0.5)
    assert quote_supported_at_url(cited_quote="the export feature loses data",
                                  fetched_text="exporting silently drops rows", scorer=s) is True


def test_empty_inputs_reject():
    assert quote_supported_at_url(cited_quote="", fetched_text="anything", scorer=None) is False
    assert quote_supported_at_url(cited_quote="x", fetched_text="", scorer=None) is False


def test_verify_pain_points_accepts_paraphrase_with_scorer():
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.fusion import CandidatePainPoint
    from council.discovery.verify import verify_pain_points

    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exporting silently drops rows"))
    pt = CandidatePainPoint("Export loss", "s", ["the export feature loses data"], ["https://r.com/1"], intensity=5)

    # no scorer -> paraphrase not a substring -> dropped (today's behavior)
    assert verify_pain_points([pt], b)[0].verified is False

    # with scorer that entails the paraphrase -> verified
    s = FakeScorer(table={"the export feature loses data": 0.9})
    out = verify_pain_points([pt], b, scorer=s)
    assert out[0].verified is True
    assert out[0].supporting_urls == ["https://r.com/1"]
