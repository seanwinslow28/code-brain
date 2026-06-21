"""Tier configs: panel/judge/tool-budget/cost-cap per quick|standard|deep."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TierConfig:
    name: str
    panel: tuple[str, ...]      # Fusion analysis_models (tool-capable only)
    judge: str                  # Fusion judge / outer model
    max_tool_calls: int         # per-panel-model web tool-call budget
    max_cost_per_run: float
    sonar_model: str            # Stage 1b article harvester
    social: bool                # run last30days backbone
    web: bool                   # run exa/brave web collector


_STANDARD_PANEL = (
    "anthropic/claude-opus-4.7",
    "openai/gpt-5.5",
    "~google/gemini-pro-latest",
    "x-ai/grok-4.3",
)

TIERS: dict[str, TierConfig] = {
    "quick": TierConfig(
        name="quick",
        panel=("~google/gemini-pro-latest", "x-ai/grok-4.3", "deepseek/deepseek-v4-pro"),
        judge="~google/gemini-pro-latest",
        max_tool_calls=3,
        max_cost_per_run=0.50,
        sonar_model="perplexity/sonar",
        social=True,
        web=True,
    ),
    "standard": TierConfig(
        name="standard",
        panel=_STANDARD_PANEL,
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=5,
        max_cost_per_run=1.50,
        sonar_model="perplexity/sonar-reasoning-pro",
        social=True,
        web=True,
    ),
    "deep": TierConfig(
        name="deep",
        panel=_STANDARD_PANEL + ("deepseek/deepseek-v4-pro", "mistralai/mistral-medium-3-5"),
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=8,
        max_cost_per_run=4.00,
        sonar_model="perplexity/sonar-deep-research",
        social=True,
        web=True,
    ),
}


def get_tier(name: str) -> TierConfig:
    if name not in TIERS:
        raise KeyError(f"Unknown tier {name!r}. Available: {', '.join(sorted(TIERS))}")
    return TIERS[name]
