"""Build the per-article critique prompt sent to Codex + Anti-Gravity.

Pure functions — no I/O outside the named template path read. The smoke-
tested prompt template lives at `agents-sdk/prompts/vault-critic-prompt-
template.md` and is the source of truth; this module only fills the slots.
"""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "vault-critic-prompt-template.md"
_STANDING_CONTEXT_PATH = Path(__file__).parent.parent / "prompts" / "vault-critic-standing-context.md"

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

DEFAULT_CONTEXT_LIMIT = 30


def load_standing_context(path: Path | None = None) -> str:
    """Read the always-prepended "About Sean" preamble. Empty string if absent.

    The preamble grounds Codex / Anti-Gravity in who Sean is, what he's already
    built, and what useful critique looks like for him — so recommendations stop
    being generic and start naming works he probably has not encountered.
    Returning empty-string-on-missing keeps the prompt well-formed and lets
    callers disable enrichment without code changes (delete or rename the file).
    """
    p = path or _STANDING_CONTEXT_PATH
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def extract_wikilinks_summary(article_body: str) -> str:
    """Return a comma-separated, deduped, order-preserving wikilink list.

    `[[real|Display]]` is normalized to `real`. Empty input → "(no wikilinks)"
    so the prompt template never has a dangling empty list.
    """
    seen: dict[str, None] = {}
    for target in _WIKILINK_RE.findall(article_body):
        stripped = target.strip()
        if stripped:
            seen.setdefault(stripped, None)
    if not seen:
        return "(no wikilinks)"
    return ", ".join(seen.keys())


def render_additional_context(
    *,
    repo_root: Path,
    context_files: list[Path] | None,
) -> tuple[str, list[str]]:
    """Read each context file and render it as a labeled supplemental block.

    Missing or unreadable files are skipped with a warning so a typo or stale
    path doesn't fail the run. Each file gets a `## Supporting context: <rel>`
    header so the critic can attribute recommendations back to the source.
    Returns (rendered_block, warnings); rendered_block is empty when there is
    no context to add.
    """
    if not context_files:
        return "", []
    parts: list[str] = []
    warnings: list[str] = []
    for raw in context_files:
        full = raw if raw.is_absolute() else (repo_root / raw)
        if not full.exists() or not full.is_file():
            warnings.append(f"context file missing, skipped: {raw}")
            continue
        try:
            text = full.read_text(encoding="utf-8", errors="replace").strip()
        except OSError as exc:
            warnings.append(f"context file unreadable, skipped: {raw} ({exc})")
            continue
        try:
            rel = str(full.relative_to(repo_root))
        except ValueError:
            rel = str(full)
        parts.append(f"## Supporting context: `{rel}`\n\n{text}")
    if not parts:
        return "", warnings
    return "\n" + "\n\n---\n\n".join(parts) + "\n", warnings


def build_critique_prompt(
    *,
    slug: str,
    article_body: str,
    source_path: str,
    recent_titles: list[str],
    context_limit: int = DEFAULT_CONTEXT_LIMIT,
    template_path: Path | None = None,
    include_standing_context: bool = True,
    standing_context_path: Path | None = None,
    additional_context: str = "",
) -> str:
    """Render the critique prompt for a single article.

    `recent_titles` is the recent-concepts orientation list from
    `vault/knowledge/index.md`; cap-limited to `context_limit` (default 30)
    by recency. The cap keeps the prompt under ~14K input tokens even on
    busy nights — Codex / Anti-Gravity smoke test was 13.2K input.

    `include_standing_context` (default True) prepends the "About Sean"
    preamble at `prompts/vault-critic-standing-context.md` so the CLIs have
    grounding on who Sean is before critiquing the article. Set False for
    ablation runs (e.g., comparing Round-1 outside-perspective-only output
    against the standing-context-enriched Round-2 output on the same target).
    """
    template = (template_path or _TEMPLATE_PATH).read_text(encoding="utf-8")
    body = article_body.strip()
    capped = recent_titles[:context_limit]
    if include_standing_context:
        ctx = load_standing_context(standing_context_path)
        standing_context = f"\n{ctx}\n" if ctx else ""
    else:
        standing_context = ""
    return template.format(
        slug=slug,
        article_body=body,
        source_path=source_path,
        wikilink_summary=extract_wikilinks_summary(body),
        context_limit=context_limit,
        recent_titles=", ".join(capped) if capped else "(none)",
        standing_context=standing_context,
        additional_context=additional_context,
    )
