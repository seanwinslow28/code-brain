#!/bin/bash
# SessionStart hook — inject vault/knowledge/index.md as `additionalContext`
# so each new Claude Code session starts aware of the synthesized knowledge
# graph. File-read-only; no LLM calls. Always exits 0 so a missing/broken
# index never blocks session start.
#
# Output (stdout): SessionStart hook contract
#   {
#     "hookSpecificOutput": {
#       "hookEventName": "SessionStart",
#       "additionalContext": "## Knowledge Index ... <truncated>"
#     }
#   }
#
# Test override: KNOWLEDGE_INDEX_PATH and KNOWLEDGE_INDEX_MAX_CHARS env vars.

set -u

REPO_ROOT="/Users/seanwinslow/Code-Brain/code-brain"
DEFAULT_INDEX="$REPO_ROOT/vault/knowledge/index.md"
# Raised from 15,000 on 2026-08-29 (#202 follow-up) so the whole graph
# fits: 912 articles render to 45,412 chars, and all 694 connections were
# the half that never arrived. This is a CEILING, not a cost. The hook
# injects whatever the graph renders to, so headroom above the current
# size is free until the vault grows into it. At the measured ~180
# articles/month that is roughly four months, and
# test_default_cap_keeps_headroom_over_the_tracked_index fails loudly
# before it runs out, which is the warning #202 never got.
DEFAULT_MAX_CHARS=80000

INDEX_PATH="${KNOWLEDGE_INDEX_PATH:-$DEFAULT_INDEX}"
MAX_CHARS="${KNOWLEDGE_INDEX_MAX_CHARS:-$DEFAULT_MAX_CHARS}"

# Drain stdin (Claude Code may pipe session metadata; we don't use it).
head -c 65536 >/dev/null 2>&1 || true

# Build the JSON via Python (stdlib only — robust JSON escaping for
# arbitrary index contents). On any unexpected failure, emit the empty
# stub rather than blocking session start.
python3 - "$INDEX_PATH" "$MAX_CHARS" <<'PYEOF' || cat <<'JSONFALLBACK'
import json
import json
import os
import re
import sys
from pathlib import Path

index_path = Path(sys.argv[1])
try:
    max_chars = int(sys.argv[2])
except (ValueError, IndexError):
    max_chars = 15000

HEADER = "## Knowledge Index (vault/knowledge/index.md)"
FOOTER = ("_To read any article, use the Read tool on the path shown "
          "for its section._")

EMPTY_STUB = (
    HEADER + "\n\n"
    "The knowledge index is empty - vault_synthesizer has not yet "
    "generated concept or connection articles. The producer pipeline "
    "(SessionEnd flush -> nightly synthesizer at 02:30) will populate "
    "it as you work."
)

ROW_RE = re.compile(r"^-\s*\[\[([^|\]]+?)(?:\|([^\]]*))?\]\]\s*(.*)$")


def _has_real_articles(text):
    """True if the index lists at least one wikilink or markdown link."""
    if re.search(r"\[\[[^\]]+\]\]", text):
        return True
    if re.search(r"\[[^\]\n]+\]\([^)]+\)", text):
        return True
    return False


def parse_sections(text):
    """[(title, [row, ...])] where a row is (slug, subdir, raw_line).

    A line the row pattern cannot read keeps slug=None and is emitted
    verbatim. Dropping what we fail to parse is how content goes
    missing quietly, which is the whole defect this guards against.
    """
    sections = []
    current = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.*\S)\s*$", line)
        if heading:
            current = (heading.group(1), [])
            sections.append(current)
            continue
        if not line.startswith("- "):
            continue
        if current is None:
            current = ("Index", [])
            sections.append(current)
        match = ROW_RE.match(line)
        if not match:
            current[1].append((None, None, line))
            continue
        target = match.group(1).strip()
        if target.startswith("_") or not target:
            current[1].append((None, None, line))
            continue
        parts = target.split("/")
        slug = parts[-1]
        if slug.endswith(".md"):
            slug = slug[:-3]
        subdir = "/".join(parts[:-1])
        current[1].append((slug, subdir, line))
    return [(title, rows) for title, rows in sections if rows]


def read_path_for(rows, title):
    subdirs = [sub for _, sub, _ in rows if sub]
    sub = subdirs[0] if subdirs else title.strip().lower().replace(" ", "-")
    return "vault/knowledge/" + sub.rstrip("/") + "/<slug>.md"


DATE_RE = re.compile(r"^(updated|created):\s*\"?([0-9]{4}-[0-9]{2}-[0-9]{2})",
                     re.MULTILINE)


def written_at(root, subdir, slug):
    """Newest-first sort key, from frontmatter rather than mtime.

    mtime is not a recency signal in this vault: a git checkout or a
    Mac Mini sync rewrites it, and 694 connection articles then all
    claim to have been written today. `updated:`/`created:` survive
    both. Reading 912 file heads measured 40ms against the hook's 5s
    budget. Missing or unreadable dates fall back to index order.
    """
    try:
        with open(root / subdir / (slug + ".md"), "rb") as handle:
            head = handle.read(400).decode("utf-8", "replace")
    except OSError:
        return None
    stamps = {key: value for key, value in DATE_RE.findall(head)}
    return stamps.get("updated") or stamps.get("created")


def render(sections, root, budget):
    """Fit sections into `budget` chars, announcing anything dropped."""
    out = []
    used = 0
    for title, rows in sections:
        head = "## {} ({})\nRead one at {}\n".format(
            title, len(rows), read_path_for(rows, title))
        lines = ["- {}".format(slug if slug else raw[2:].strip())
                 for slug, _, raw in rows]
        full = head + "\n".join(lines) + "\n"
        if used + len(full) <= budget:
            out.append(full)
            used += len(full)
            continue
        # Reserve the notice before deciding how many rows survive, so the
        # count it reports is always the count actually emitted.
        notice_tpl = ("_{} of {} not shown (newest kept). "
                      "Full list: vault/knowledge/index.md_\n")
        notice = notice_tpl.format(len(rows), len(rows))
        room = budget - used - len(head) - len(notice)
        if room <= 0:
            break
        order = []
        for position, (slug, subdir, raw) in enumerate(rows):
            stamp = written_at(root, subdir, slug) if slug else None
            order.append((stamp, position, slug, raw))
        dated = [entry for entry in order if entry[0] is not None]
        if dated:
            # Select by recency, then display in index order so the list
            # still reads alphabetically.
            ranked = sorted(order, key=lambda entry: (
                entry[0] is not None, entry[0] or "", -entry[1]),
                reverse=True)
        else:
            ranked = order
        kept, spent = [], 0
        for entry in ranked:
            text = "- {}\n".format(
                entry[2] if entry[2] else entry[3][2:].strip())
            if spent + len(text) > room:
                break
            kept.append(entry)
            spent += len(text)
        if not kept:
            break
        kept.sort(key=lambda entry: entry[1])
        shown = "".join("- {}\n".format(
            entry[2] if entry[2] else entry[3][2:].strip()) for entry in kept)
        out.append(head + shown + notice_tpl.format(
            len(rows) - len(kept), len(rows)))
        used = budget
        break
    return "\n".join(part.rstrip("\n") for part in out)


if not index_path.exists():
    body = EMPTY_STUB
else:
    try:
        content = index_path.read_text(encoding="utf-8")
    except OSError:
        content = ""
    if not content.strip() or not _has_real_articles(content):
        body = EMPTY_STUB
    else:
        sections = parse_sections(content)
        rendered = render(sections, index_path.parent, max_chars)
        if not rendered.strip():
            rendered = content[:max_chars]
        body = HEADER + "\n\n" + rendered + "\n\n" + FOOTER

print(json.dumps(
    {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }
))
PYEOF
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"## Knowledge Index (vault/knowledge/index.md)\n\nThe knowledge index is empty — vault_synthesizer has not yet generated concept or connection articles. The producer pipeline (SessionEnd flush → nightly synthesizer at 02:30) will populate it as you work."}}
JSONFALLBACK

exit 0
