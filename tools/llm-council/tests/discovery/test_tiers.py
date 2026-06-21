# tests/discovery/test_tiers.py
import pytest
from council.discovery.tiers import get_tier, TIERS


def test_three_tiers_exist():
    assert set(TIERS) == {"quick", "standard", "deep"}


def test_standard_panel_is_four_frontier_vendors():
    t = get_tier("standard")
    assert t.panel == (
        "anthropic/claude-opus-4.7",
        "openai/gpt-5.5",
        "~google/gemini-pro-latest",
        "x-ai/grok-4.3",
    )
    assert t.judge == "anthropic/claude-opus-4.7"
    assert t.max_cost_per_run == 1.50


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
