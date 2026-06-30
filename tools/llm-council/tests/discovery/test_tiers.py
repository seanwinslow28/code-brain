# tests/discovery/test_tiers.py
import pytest
from council.discovery.tiers import get_tier, TIERS, _family

# IDs validated against the live OpenRouter API (FUSION_SCHEMA.md §2). Panel + judge
# must never drift outside this set (guards against a 400 from a typo'd/aliased id).
_VALIDATED_IDS = {
    "anthropic/claude-opus-4.7",
    "openai/gpt-5.5",
    "~google/gemini-pro-latest",
    "x-ai/grok-4.3",
    "deepseek/deepseek-v4-pro",
    "mistralai/mistral-medium-3-5",
}


def test_three_tiers_exist():
    assert set(TIERS) == {"quick", "standard", "deep"}


def test_family_strips_tilde_and_splits_on_slash():
    assert _family("~google/gemini-pro-latest") == "google"
    assert _family("anthropic/claude-opus-4.7") == "anthropic"
    assert _family("openai/gpt-5.5") == "openai"
    assert _family("mistralai/mistral-medium-3-5") == "mistralai"


def test_judge_family_is_disjoint_from_panel_every_tier():
    # E2 invariant: the judge must not share a model family with any panelist
    # (self-preference / self-enhancement bias — see the E2 research note).
    for name in TIERS:
        t = get_tier(name)
        panel_families = {_family(m) for m in t.panel}
        assert _family(t.judge) not in panel_families, (
            f"{name}: judge {t.judge} shares family with panel {t.panel}"
        )


def test_all_panel_and_judge_ids_are_validated():
    for name in TIERS:
        t = get_tier(name)
        for m in (*t.panel, t.judge):
            assert m in _VALIDATED_IDS, f"{name}: unvalidated model id {m!r}"


def test_quick_judge_swapped_to_disjoint_family():
    t = get_tier("quick")
    assert t.judge == "openai/gpt-5.5"
    assert t.panel == (
        "~google/gemini-pro-latest",
        "x-ai/grok-4.3",
        "deepseek/deepseek-v4-pro",
    )


def test_standard_panel_is_anthropic_free_with_opus_judge():
    t = get_tier("standard")
    assert t.panel == (
        "openai/gpt-5.5",
        "~google/gemini-pro-latest",
        "x-ai/grok-4.3",
    )
    assert t.judge == "anthropic/claude-opus-4.7"
    assert "anthropic/claude-opus-4.7" not in t.panel
    assert t.max_cost_per_run == 1.50


def test_deep_panel_excludes_anthropic_keeps_two_extra_lineages():
    t = get_tier("deep")
    assert "anthropic/claude-opus-4.7" not in t.panel
    assert "deepseek/deepseek-v4-pro" in t.panel
    assert "mistralai/mistral-medium-3-5" in t.panel
    assert t.judge == "anthropic/claude-opus-4.7"


def test_sonar_never_in_panel():
    for name in TIERS:
        panel = get_tier(name).panel
        assert not any("sonar" in m or "perplexity" in m for m in panel)


def test_deep_adds_two_more_lineages_and_confirms_cost():
    t = get_tier("deep")
    assert "deepseek/deepseek-v4-pro" in t.panel
    assert "mistralai/mistral-medium-3-5" in t.panel
    assert t.max_cost_per_run == 4.00


def test_unknown_tier_raises():
    with pytest.raises(KeyError):
        get_tier("ultra")


def test_collector_tier_gating_matches_matrix():
    q, s, d = get_tier("quick"), get_tier("standard"), get_tier("deep")
    assert (q.reviews, q.github, q.qa) == (False, False, False)   # quick stays lean
    assert (s.reviews, s.github, s.qa) == (True, True, False)     # standard: + reviews + github
    assert (d.reviews, d.github, d.qa) == (True, True, True)      # deep: + reviews + github + qa
    assert all(t.social and t.web for t in (q, s, d))             # social + web stay on everywhere


def test_supplement_blind_spot_caps_scale_by_tier():
    assert get_tier("quick").supplement_max_blind_spots == 2
    assert get_tier("standard").supplement_max_blind_spots == 4
    assert get_tier("deep").supplement_max_blind_spots == 6
