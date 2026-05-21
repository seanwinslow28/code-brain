"""Build the per-article critique prompt sent to Codex + Anti-Gravity.

Pure functions — no I/O outside the named template path read. The smoke-
tested prompt template lives at `agents-sdk/prompts/vault-critic-prompt-
template.md` and is the source of truth; this module only fills the slots.
"""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "vault-critic-prompt-template.md"

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

DEFAULT_CONTEXT_LIMIT = 30


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


def build_critique_prompt(
    *,
    slug: str,
    article_body: str,
    source_path: str,
    recent_titles: list[str],
    context_limit: int = DEFAULT_CONTEXT_LIMIT,
    template_path: Path | None = None,
) -> str:
    """Render the critique prompt for a single article.

    `recent_titles` is the recent-concepts orientation list from
    `vault/knowledge/index.md`; cap-limited to `context_limit` (default 30)
    by recency. The cap keeps the prompt under ~14K input tokens even on
    busy nights — Codex / Anti-Gravity smoke test was 13.2K input.
    """
    template = (template_path or _TEMPLATE_PATH).read_text(encoding="utf-8")
    body = article_body.strip()
    capped = recent_titles[:context_limit]
    return template.format(
        slug=slug,
        article_body=body,
        source_path=source_path,
        wikilink_summary=extract_wikilinks_summary(body),
        context_limit=context_limit,
        recent_titles=", ".join(capped) if capped else "(none)",
    )
