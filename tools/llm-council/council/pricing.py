"""Fail-closed OpenRouter prices for bounded council and discovery calls.

The table must stay greater than or equal to real provider prices: a configured
price below real is a fail-closed outage because OpenRouter's ``max_price`` filter
404s every call, while a price above real merely over-reserves. Floating aliases
can rotate to pricier targets; when they do, the filter must refuse loudly until
the alias is re-probed and re-priced. Re-probe and re-price on every routing
change (the F8a.5 rule).
"""

import math


PRICING_AS_OF = "2026-07-18"

# USD per 1,000 tokens: 2026-07-18 raw OpenRouter snapshot x 1.25 margin.
MODEL_PRICING_PER_1K: dict[str, tuple[float, float]] = {
    "anthropic/claude-opus-4.7": (0.00625, 0.03125),
    "openai/gpt-5.5": (0.00625, 0.0375),
    "google/gemini-2.5-pro": (0.0015625, 0.0125),
    "x-ai/grok-4.5": (0.0025, 0.0075),
    "anthropic/claude-sonnet-4.5": (0.00375, 0.01875),
    "openai/gpt-5.4-mini": (0.0009375, 0.005625),
    "deepseek/deepseek-v4-pro": (0.00054375, 0.0010875),
    "mistralai/mistral-medium-3-5": (0.001875, 0.009375),
    "x-ai/grok-4.3": (0.0015625, 0.003125),
    "google/gemini-3.1-pro-preview": (0.0025, 0.015),
    "perplexity/sonar": (0.00125, 0.00125),
    "perplexity/sonar-reasoning-pro": (0.0025, 0.01),
    "perplexity/sonar-deep-research": (0.0025, 0.01),
    "~anthropic/claude-sonnet-latest": (0.00375, 0.01875),
    "~google/gemini-pro-latest": (0.0025, 0.015),
}

# USD per web-search request: non-null snapshot values x 1.25 margin.
WEB_SEARCH_PRICE_PER_CALL: dict[str, float] = {
    "anthropic/claude-opus-4.7": 0.0125,
    "openai/gpt-5.5": 0.0125,
    "google/gemini-2.5-pro": 0.0175,
    "x-ai/grok-4.5": 0.00625,
    "anthropic/claude-sonnet-4.5": 0.0125,
    "openai/gpt-5.4-mini": 0.0125,
    "x-ai/grok-4.3": 0.00625,
    "google/gemini-3.1-pro-preview": 0.0175,
    "perplexity/sonar": 0.00625,
    "perplexity/sonar-reasoning-pro": 0.00625,
    "perplexity/sonar-deep-research": 0.00625,
}


def _pricing_for(model: str) -> tuple[float, float]:
    if not isinstance(model, str) or not model.strip():
        raise ValueError("model must be a nonblank string")
    try:
        prices = MODEL_PRICING_PER_1K[model]
    except KeyError:
        raise KeyError(f"pricing missing for model {model!r}") from None
    if not isinstance(prices, (tuple, list)) or len(prices) != 2:
        raise ValueError(f"pricing malformed for model {model!r}")
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
        for value in prices
    ):
        raise ValueError(f"pricing malformed for model {model!r}")
    return float(prices[0]), float(prices[1])


def provider_price_policy(model: str) -> dict:
    """Return the exact fail-closed OpenRouter provider filter in USD/million."""
    prompt_per_1k, completion_per_1k = _pricing_for(model)
    return {
        "max_price": {
            "prompt": prompt_per_1k * 1000,
            "completion": completion_per_1k * 1000,
            "request": 0,
        },
        "allow_fallbacks": False,
        "require_parameters": True,
    }
