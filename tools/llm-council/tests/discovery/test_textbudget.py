"""Tests for the shared query-length clamp (council.discovery.textbudget).

A long topic (and/or --segment) composed into a provider query can exceed Brave's q-param
ceiling (~50 words / ~400 chars) or GitHub search's ~256-char limit and 422 the search — which,
pre-fix, crashed the Stage-5 backfill (2026-06-28). One shared clamp, reused by backfill +
the reviews/github collectors.
"""

from council.discovery.textbudget import clamp_words_chars


def test_clamp_trims_to_word_ceiling():
    text = " ".join(f"w{i}" for i in range(30))
    out = clamp_words_chars(text, max_words=10, max_chars=1000)
    assert len(out.split()) == 10
    assert out.startswith("w0 w1 ")


def test_clamp_trims_to_char_ceiling_on_a_word_boundary():
    out = clamp_words_chars("alpha beta gamma delta", max_words=100, max_chars=12)
    assert out == "alpha beta"      # "alpha beta g"[:12] backed off to the last whole word
    assert len(out) <= 12


def test_clamp_is_a_noop_within_both_limits():
    assert clamp_words_chars("short topic", max_words=10, max_chars=100) == "short topic"


def test_clamp_handles_a_single_overlong_word_without_a_space():
    out = clamp_words_chars("x" * 50, max_words=10, max_chars=20)
    assert len(out) <= 20
