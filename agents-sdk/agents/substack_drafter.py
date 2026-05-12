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
import json
from datetime import date
from pathlib import Path

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


# --- Synthesizer-dryness gate (Task C3) ---


def is_synthesizer_dry(*, health_dir: Path, threshold: int = 3) -> bool:
    """Return True iff the last `threshold` synth manifests had concepts_written == 0.

    The check is conservative: "dry" means we can't safely produce a draft.
    Edge cases all return True (dry):
      - Health directory is empty or has fewer than `threshold` manifests
      - Any manifest in the window can't be read as JSON
    If any manifest in the last `threshold` has concepts_written > 0,
    we have something to draft from → returns False (not dry).

    Args:
        health_dir: Directory containing synth-manifest-YYYY-MM-DD.json files.
            Typically `vault/health/`.
        threshold: How many of the most recent manifests to inspect.
            Default 3, configurable via [substack_drafter].synthesizer_dry_threshold
            in config.toml.

    Returns:
        bool. True = dry (skip the draft), False = wet (proceed).
    """
    manifests = sorted(health_dir.glob("synth-manifest-*.json"))
    if len(manifests) < threshold:
        return True
    recent = manifests[-threshold:]
    parsed: list[dict] = []
    for path in recent:
        try:
            parsed.append(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            return True  # unreadable manifest = treat as dry to be safe
    # All manifests readable — dry only if none had any output
    return not any(d.get("concepts_written", 0) > 0 for d in parsed)
