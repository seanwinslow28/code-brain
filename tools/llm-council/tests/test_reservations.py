"""Proof-shaped worst-case reservations for shipped council/discovery graphs."""

from dataclasses import replace
from types import SimpleNamespace

import pytest

from council import policy, pricing, reservations
from council.discovery.tiers import TIERS
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


@pytest.mark.parametrize(
    ("tier_name", "expected"),
    [
        ("quick", 3.232560),
        ("standard", 4.312080),
        ("deep", 7.302080),
    ],
)
def test_discovery_worst_case_reservation_pins_approved_bounds(tier_name, expected):
    assert reservations.discovery_worst_case_reservation(TIERS[tier_name]) == expected


@pytest.mark.parametrize(
    ("tier_name", "expected"),
    [
        ("quick", 6.438560),
        ("standard", 8.555680),
        ("deep", 14.535680),
    ],
)
def test_experiment_worst_case_reservation_pins_approved_bounds(tier_name, expected):
    reservation = reservations.experiment_worst_case_reservation(TIERS[tier_name])

    assert reservation == expected
    assert reservation <= 30.00


@pytest.mark.parametrize(
    "constant",
    [
        "SONAR_TOPIC_EMBED_MAX_BYTES",
        "SONAR_SEGMENT_EMBED_MAX_BYTES",
        "SONAR_FRAMING_BYTES",
        "SONAR_MAX_TOKENS",
        "FUSION_TOPIC_EMBED_MAX_BYTES",
        "FUSION_EVIDENCE_EMBED_MAX_BYTES",
        "FUSION_FRAMING_BYTES",
        "FUSION_JUDGE_MAX_TOKENS",
        "COUNCIL_CHAT_ENVELOPE_BYTES",
        "MAX_WEB_SEARCH_PRICE",
    ],
)
@pytest.mark.parametrize(
    "calculator",
    [
        reservations.discovery_worst_case_reservation,
        reservations.experiment_worst_case_reservation,
    ],
)
def test_discovery_bounds_are_monotone_in_every_shipped_constant(
    monkeypatch, constant, calculator
):
    """Review finding (Task 4 round 2, minor): a non-strict >= passes even when a
    listed constant is dropped from the formula entirely. Mutate by enough to clear
    the micro quantization (+1000 bytes/tokens; +0.001 on a per-call price) and
    require a STRICT increase, so every constant is proven load-bearing."""
    tier = TIERS["standard"]
    original = calculator(tier)

    delta = 0.001 if constant == "MAX_WEB_SEARCH_PRICE" else 1000
    monkeypatch.setattr(reservations, constant, getattr(reservations, constant) + delta)

    assert calculator(tier) > original


@pytest.mark.parametrize(
    "calculator",
    [
        reservations.discovery_worst_case_reservation,
        reservations.experiment_worst_case_reservation,
    ],
)
def test_discovery_bounds_are_monotone_in_tier_allowance(calculator):
    tier = TIERS["standard"]
    higher_allowance = replace(tier, max_cost_per_run=tier.max_cost_per_run + 1)

    assert calculator(higher_allowance) > calculator(tier)


def test_discovery_max_web_price_is_derived_from_the_pricing_registry():
    assert reservations.MAX_WEB_SEARCH_PRICE == max(
        pricing.WEB_SEARCH_PRICE_PER_CALL.values()
    )


@pytest.mark.parametrize(
    ("tier_name", "cap"),
    [("quick", 3.25), ("standard", 4.50), ("deep", 7.50)],
)
def test_discovery_tier_caps_cover_their_derived_reservations(tier_name, cap):
    assert cap >= reservations.discovery_worst_case_reservation(TIERS[tier_name])


@pytest.mark.parametrize(
    "calculator",
    [
        reservations.discovery_worst_case_reservation,
        reservations.experiment_worst_case_reservation,
    ],
)
def test_discovery_bounds_ignore_runtime_noise(calculator):
    tier = TIERS["standard"]
    noisy_tier = SimpleNamespace(
        **tier.__dict__,
        runtime_response={"tokens": 10**12, "cost": 10**12, "web_calls": 10**12},
    )

    assert calculator(noisy_tier) == calculator(tier)
