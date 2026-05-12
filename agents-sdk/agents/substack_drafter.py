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
import re
from collections import defaultdict
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


# --- Cluster picker (Task C4) ---

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def _extract_wikilinks(text: str) -> set[str]:
    """Return the set of unique wikilink targets in `text`. Strips aliases.

    `[[target|display]]` → "target".
    `[[plain]]` → "plain".
    """
    return {m.group(1).strip() for m in _WIKILINK_RE.finditer(text)}


def pick_densest_cluster(*, concepts_dir: Path, min_shared: int = 3) -> list[str]:
    """Return the slugs of the cluster with the densest wikilink overlap.

    Algorithm:
      1. Read every `.md` in `concepts_dir`; extract its outbound wikilinks.
      2. Build an undirected graph: edge a–b iff |links[a] ∩ links[b]| >= min_shared.
      3. Find the largest connected component (BFS).
      4. Return up to 5 slugs from that component (sorted alphabetically for
         determinism).

    Args:
        concepts_dir: Directory containing concept-article markdown files.
            Typically `vault/knowledge/concepts/`.
        min_shared: Minimum wikilink-overlap count for two concepts to be
            considered connected. Default 3 per SPEC.

    Returns:
        list[str] of 0 to 5 concept slugs. Empty list if `concepts_dir` is empty.
        Singleton list of one slug if no concepts share enough wikilinks
        (each concept is its own component; we still return the largest = 1).
    """
    paths = sorted(concepts_dir.glob("*.md"))
    if not paths:
        return []
    links_by_slug: dict[str, set[str]] = {}
    for p in paths:
        links_by_slug[p.stem] = _extract_wikilinks(p.read_text())

    # Build adjacency: connect a,b if |links[a] & links[b]| >= min_shared
    adj: dict[str, set[str]] = defaultdict(set)
    slugs = list(links_by_slug)
    for i, a in enumerate(slugs):
        for b in slugs[i + 1:]:
            if len(links_by_slug[a] & links_by_slug[b]) >= min_shared:
                adj[a].add(b)
                adj[b].add(a)

    # Find largest connected component (iterative BFS to avoid recursion limits)
    seen: set[str] = set()
    best: list[str] = []
    for slug in slugs:
        if slug in seen:
            continue
        stack, component = [slug], []
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            component.append(node)
            stack.extend(adj[node] - seen)
        if len(component) > len(best):
            best = component
    return sorted(best)[:5]


# --- Prompt composer (Task C5) ---

def compose_prompt(*, voice_mode: str, voice_skill_path: Path,
                   cluster_slugs: list[str], cluster_bodies: list[str],
                   reference_excerpts: list[str], word_count_target: int = 1350) -> dict[str, str]:
    """Return {'system': ..., 'user': ...} ready for HybridRouter.

    The system prompt loads writing-voice-modes/SKILL.md verbatim so the LLM
    follows the actual voice spec instead of an LLM-paraphrased version. If
    the skill file is missing (moved or renamed), the prompt degrades
    gracefully: it still names the voice mode but acknowledges the spec is
    missing rather than crashing the run.

    The user prompt asks for a word_count_target-word draft about the cluster,
    grounded in the references, with a hook in the first 2 sentences. The
    final sentence reminds the model not to publish — drafts land in the
    vault for Sean to review.

    Args:
        voice_mode: One of VOICE_MODES (sean / sedaris / kerouac / thompson / vonnegut)
        voice_skill_path: Path to .claude/skills/writing-voice-modes/SKILL.md
        cluster_slugs: List of concept slugs from pick_densest_cluster()
        cluster_bodies: Parallel list of concept article bodies (str)
        reference_excerpts: List of grounding source excerpts from similarity pull
        word_count_target: Default 1350 (midpoint of 1200-1500 SPEC range)

    Returns:
        {'system': str, 'user': str}
    """
    # System prompt — load voice spec verbatim
    try:
        voice_skill_text = voice_skill_path.read_text()
        system = (
            f"You are drafting a Substack post in {voice_mode!r} voice. "
            f"The full voice spec is below — follow its signature moves exactly.\n\n"
            f"---\n{voice_skill_text}\n---"
        )
    except (FileNotFoundError, OSError):
        # Graceful degradation: voice spec file is missing or unreadable.
        # Still produce a usable prompt; Sean will notice the draft feels
        # generic and can investigate why the spec didn't load.
        system = (
            f"You are drafting a Substack post in {voice_mode!r} voice. "
            f"The writing-voice-modes spec file at {voice_skill_path} could "
            f"not be loaded (missing or not found). Draft in your understanding "
            f"of {voice_mode!r} voice anyway; flag in the draft that the spec "
            f"was missing so Sean can investigate."
        )

    # User prompt — cluster + references + constraints
    cluster_block = "\n\n".join(
        f"## Source concept: {slug}\n\n{body}"
        for slug, body in zip(cluster_slugs, cluster_bodies)
    )
    refs_block = "\n\n".join(f"- {r}" for r in reference_excerpts) if reference_excerpts else "(no similarity-matched references available)"
    user = (
        f"Draft a {word_count_target}-word Substack post in {voice_mode} voice "
        f"about the connections between: {', '.join(cluster_slugs)}.\n\n"
        f"Ground in these sources:\n\n{refs_block}\n\n"
        f"Source concept bodies:\n\n{cluster_block}\n\n"
        f"Constraints:\n"
        f"- Hook in the first 2 sentences.\n"
        f"- Use {voice_mode}'s signature moves from the skill spec above.\n"
        f"- Cite sources by wikilink, not by URL.\n"
        f"- Do not publish to Substack — this is a draft for Sean to review.\n"
    )
    return {"system": system, "user": user}
