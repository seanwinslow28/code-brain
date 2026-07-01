# tests/discovery/test_verify_entailment.py
from council.discovery.verify import quote_supported_at_url


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


def test_empty_inputs_reject():
    assert quote_supported_at_url(cited_quote="", fetched_text="anything", scorer=None) is False
    assert quote_supported_at_url(cited_quote="x", fetched_text="", scorer=None) is False
