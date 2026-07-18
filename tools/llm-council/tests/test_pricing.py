"""Pricing-table provenance and fail-closed provider-policy guards."""

import json
from decimal import Decimal
from pathlib import Path

import pytest

from council import pricing
from council.profiles import PROFILES


SNAPSHOT_PATH = Path(pricing.__file__).with_name(
    "openrouter-pricing-snapshot-2026-07-18.json"
)
MARGIN = Decimal("1.25")
PER_1K = Decimal("1000")


def _snapshot_models() -> dict:
    return json.loads(SNAPSHOT_PATH.read_text(), parse_float=Decimal)["models"]


def test_pricing_table_covers_snapshot_at_exact_twenty_five_percent_margin():
    for model, raw in _snapshot_models().items():
        expected = (
            float(Decimal(raw["prompt"]) * PER_1K * MARGIN),
            float(Decimal(raw["completion"]) * PER_1K * MARGIN),
        )
        assert pricing.MODEL_PRICING_PER_1K[model] == expected
        assert pricing.MODEL_PRICING_PER_1K[model][0] >= float(
            Decimal(raw["prompt"]) * PER_1K
        )
        assert pricing.MODEL_PRICING_PER_1K[model][1] >= float(
            Decimal(raw["completion"]) * PER_1K
        )


def test_web_search_table_covers_exactly_snapshot_models_with_search_prices():
    expected = {
        model: float(Decimal(raw["web_search"]) * MARGIN)
        for model, raw in _snapshot_models().items()
        if raw["web_search"] is not None
    }
    assert pricing.WEB_SEARCH_PRICE_PER_CALL == expected


@pytest.mark.parametrize(
    ("alias", "target"),
    [
        ("~anthropic/claude-sonnet-latest", "anthropic/claude-sonnet-4.5"),
        ("~google/gemini-pro-latest", "google/gemini-3.1-pro-preview"),
    ],
)
def test_floating_alias_prices_equal_their_pinned_resolution_targets(alias, target):
    assert pricing.MODEL_PRICING_PER_1K[alias] == pricing.MODEL_PRICING_PER_1K[target]


def test_provider_price_policy_has_exact_fail_closed_shape_and_per_million_math():
    assert pricing.provider_price_policy("anthropic/claude-opus-4.7") == {
        "max_price": {
            "prompt": 6.25,
            "completion": 31.25,
            "request": 0,
        },
        "allow_fallbacks": False,
        "require_parameters": True,
    }


def test_provider_price_policy_rejects_unknown_model_clearly():
    with pytest.raises(KeyError, match="pricing missing.*unlisted/model"):
        pricing.provider_price_policy("unlisted/model")


@pytest.mark.parametrize(
    "malformed",
    [
        (True, 0.01),
        (0.01, float("inf")),
        (-0.01, 0.01),
        (0.01,),
        "not-a-price-pair",
    ],
)
def test_provider_price_policy_rejects_malformed_table_entries(monkeypatch, malformed):
    monkeypatch.setitem(pricing.MODEL_PRICING_PER_1K, "bad/model", malformed)
    with pytest.raises(ValueError, match="pricing malformed.*bad/model"):
        pricing.provider_price_policy("bad/model")


def test_every_profile_model_and_chairman_has_a_pricing_entry():
    configured = {
        model
        for profile in PROFILES.values()
        for model in (*profile.models, profile.chairman)
    }
    assert configured <= pricing.MODEL_PRICING_PER_1K.keys()

