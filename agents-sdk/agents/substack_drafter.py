"""Substack-Drafter agent.

Reads post-fix synthesizer output, picks a concept cluster, drafts a Substack
post in a rotating voice mode. Never publishes; drafts land in the vault for
Sean to review Friday morning.

Default-disabled at three kill-switch layers per SPEC:
  1. enabled = false in agents-sdk/config.toml [substack_drafter] (config flag)
  2. plist not installed unless INSTALL_SUBSTACK_DRAFTER=1 (opt-in launchd)
  3. --dry-run flag prints the prompt but does not call the LLM

See agents-sdk/config.toml [substack_drafter] for defaults.
"""
from __future__ import annotations
from datetime import date

# Voice rotation: 5-week cycle. Index 0 = Sean Mode (the Hybrid default per
# .claude/skills/writing-voice-modes/SKILL.md). Indices 1-4 are the signature
# variants used when a post's shape benefits from a specific signature move.
VOICE_MODES = ("sean", "sedaris", "kerouac", "thompson", "vonnegut")


def pick_voice_mode(*, today: date, epoch: date, override: str | None = None) -> str:
    """Rotate through 5 voice modes weekly. Override pins a specific mode.

    Uses absolute weeks since `epoch` (not week-of-year, which skews across year
    boundaries — some years would hit the same mode twice in a row).

    Args:
        today: The date this run is being scheduled for. The launchd plist fires
            Thursday 18:00; pass `date.today()` from the caller.
        epoch: The rotation-index-0 anchor date. Per config.toml, this is
            2026-05-04 (the Monday Sean was laid off; the sprint epoch).
        override: If provided, pins that mode for this run regardless of cycle.
            Must be one of VOICE_MODES; otherwise ValueError.

    Returns:
        One of VOICE_MODES as a string slug.

    Raises:
        ValueError: if override is not None and not in VOICE_MODES.
    """
    if override is not None:
        if override not in VOICE_MODES:
            raise ValueError(
                f"unknown voice mode: {override!r}; valid: {VOICE_MODES}"
            )
        return override
    weeks_since = (today - epoch).days // 7
    return VOICE_MODES[weeks_since % len(VOICE_MODES)]
