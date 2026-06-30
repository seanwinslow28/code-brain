from council.discovery.fusion import CandidatePainPoint
from experiments.blind_rating import build_blind_rating


def _pt(title, summary="s", quotes=None, urls=None):
    return CandidatePainPoint(title=title, summary=summary,
                              quotes=quotes or ["q"], urls=urls or ["https://e.com/x"])


def test_key_maps_both_sets_to_distinct_arms():
    a = [_pt("Alpha pain")]
    b = [_pt("Beta pain")]
    md, key = build_blind_rating(a, b, topic="t")
    assert set(key.keys()) == {"Set 1", "Set 2"}
    assert set(key.values()) == {"A", "B"}


def test_shuffle_is_deterministic_per_topic():
    a, b = [_pt("Alpha pain")], [_pt("Beta pain")]
    _, key1 = build_blind_rating(a, b, topic="same-topic")
    _, key2 = build_blind_rating(a, b, topic="same-topic")
    assert key1 == key2


def test_markdown_hides_arm_identity_but_shows_content():
    a, b = [_pt("Alpha pain")], [_pt("Beta pain")]
    md, key = build_blind_rating(a, b, topic="t")
    assert "## Set 1" in md and "## Set 2" in md
    assert "Alpha pain" in md and "Beta pain" in md
    # no leakage of which arm is which
    assert "panel" not in md.lower() and "single" not in md.lower()
    assert "claude" not in md.lower() and "opus" not in md.lower()
    assert "Arm A" not in md and "Arm B" not in md
    assert "Rating criteria" in md
