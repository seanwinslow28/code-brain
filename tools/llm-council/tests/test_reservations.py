"""Proof-shaped worst-case reservations for the shipped council graph."""

from types import SimpleNamespace

import pytest

from council import policy, reservations
from council.profiles import PROFILES


@pytest.mark.parametrize(
    ("profile_name", "expected"),
    [
        ("premium", 11.189760),
        ("variance", 5.069952),
        ("interview_grader", 12.456960),
    ],
)
def test_council_worst_case_cost_pins_approved_bounds(profile_name, expected):
    assert reservations.council_worst_case_cost(PROFILES[profile_name]) == expected


@pytest.mark.parametrize(
    "constant",
    [
        "PROMPT_MAX_BYTES",
        "RESPONSE_EMBED_MAX_BYTES",
        "RANKING_REASONING_EMBED_MAX_BYTES",
        "FANOUT_MAX_TOKENS",
        "CROSSRANK_MAX_TOKENS",
        "CHAIRMAN_MAX_TOKENS",
    ],
)
def test_council_bound_is_monotone_in_every_shipped_constant(monkeypatch, constant):
    profile = PROFILES["premium"]
    original = reservations.council_worst_case_cost(profile)

    monkeypatch.setattr(reservations, constant, getattr(reservations, constant) + 1)

    assert reservations.council_worst_case_cost(profile) >= original


def test_council_bound_is_independent_of_runtime_responses():
    profile = PROFILES["premium"]
    profile_with_runtime_noise = SimpleNamespace(
        models=profile.models,
        chairman=profile.chairman,
        runtime_response={"tokens": 10**12, "cost": 10**12, "content": "x" * 1000},
    )

    assert reservations.council_worst_case_cost(profile_with_runtime_noise) == (
        reservations.council_worst_case_cost(profile)
    )


@pytest.mark.parametrize(
    "profile",
    [
        SimpleNamespace(models=("a", "b", "c"), chairman="a"),
        SimpleNamespace(models=("a", "b", "c", "c"), chairman="a"),
        SimpleNamespace(models=("a", "b", "c", " "), chairman="a"),
        SimpleNamespace(models=("a", "b", "c", "d"), chairman=" "),
    ],
)
def test_council_bound_refuses_malformed_profiles(profile):
    with pytest.raises(ValueError):
        reservations.council_worst_case_cost(profile)


def test_every_profile_has_bound_headroom_and_an_enumerated_cap():
    enumerated = set(policy.load_policy()["tools"]["council"]["per_query_caps"])

    for profile in PROFILES.values():
        assert profile.max_cost_per_query >= reservations.council_worst_case_cost(profile)
        assert profile.max_cost_per_query in enumerated
