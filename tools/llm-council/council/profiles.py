"""Council profiles — two named configurations (premium, variance)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    models: tuple[str, ...]  # 4 OpenRouter model IDs
    chairman: str            # one of `models`, or a fifth distinct model
    max_cost_per_query: float


# Model IDs and caps are sourced from model-selection-2026-05-14.md.
# Update both files together; this is the single source of truth at runtime.
PROFILES: dict[str, Profile] = {
    "premium": Profile(
        name="premium",
        models=(
            "anthropic/claude-opus-4.7",
            "openai/gpt-5.5",
            "~google/gemini-pro-latest",
            "x-ai/grok-4.20",
        ),
        chairman="anthropic/claude-opus-4.7",
        max_cost_per_query=1.00,
    ),
    "variance": Profile(
        name="variance",
        models=(
            "~anthropic/claude-sonnet-latest",
            "openai/gpt-5.4-mini",
            "deepseek/deepseek-v4-pro",
            "mistralai/mistral-medium-3-5",
        ),
        chairman="~anthropic/claude-sonnet-latest",
        max_cost_per_query=0.40,
    ),
}


def get_profile(name: str) -> Profile:
    """Return the named profile or raise KeyError with available names."""
    if name not in PROFILES:
        available = ", ".join(sorted(PROFILES))
        raise KeyError(f"Unknown profile {name!r}. Available: {available}")
    return PROFILES[name]
