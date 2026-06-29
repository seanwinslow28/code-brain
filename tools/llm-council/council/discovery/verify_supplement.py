# council/discovery/verify_supplement.py
"""Anti-fabrication backstop for the AGENT-driven Web Supplement (2026-06-28 pivot).

The orchestrating Claude Code session writes the `## Web Supplement (gap-fill)` section by hand,
using WebSearch/WebFetch on the Anthropic subscription ($0). The agent judges *relevance* natively
— the hard, subjective part it does best. This module re-checks the cheap, objective part: is each
cited quote actually VERBATIM at its URL? It routes every quote through the one shared
anti-fabrication primitive (`verify.quote_supported_at_url`), so the brand's gate guarantee
survives the move off the deterministic in-CLI backfill. Trust, but verify.

CLI: `python -m council.discovery.verify_supplement <ledger.md>` — exits non-zero if any cited
quote is not verbatim at its URL (so it can gate a run). Read-only; it never rewrites the ledger —
on a miss it tells you to demote that item to "still open — not filled".
"""

import asyncio
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import click
from rich.console import Console

from council.discovery.gather.web import _simple_fetch
from council.discovery.verify import quote_supported_at_url

console = Console()


@dataclass(frozen=True)
class SupplementFinding:
    gap: str
    quote: str
    url: str


@dataclass(frozen=True)
class SupplementVerdict:
    finding: SupplementFinding
    supported: bool
    reason: str


_SECTION_RE = re.compile(r"^##\s+web supplement", re.I)
_GAP_RE = re.compile(r"^###\s+(.*)$")
_LIST_RE = re.compile(r"^\s*[-*]\s+(.*)$")
_URL_RE = re.compile(r"https?://[^\s)>\]]+")
_QUOTE_CHARS = "\"'“”‘’"      # straight + curly quotes
_SEP_CHARS = "—–-·:"               # em/en dash, hyphen, middle dot, colon


def _clean_quote(text: str) -> str:
    """Strip the trailing quote→URL separator and wrapping quotes down to the cited text.

    Two strip passes so a legacy multi-quote line (`"" · "real quote"` from the deprecated in-CLI
    backfill) doesn't leak its leading empty-quote + middot into the parsed quote — pass one peels
    the outer `""`, pass two peels the exposed ` · "` before the real quote.
    """
    t = text.strip().strip(_SEP_CHARS + " \t").strip(_QUOTE_CHARS)
    t = t.strip(_SEP_CHARS + " \t").strip(_QUOTE_CHARS).strip()
    return re.sub(r"\s+", " ", t)


def parse_supplement(markdown: str) -> list[SupplementFinding]:
    """Extract (gap, quote, url) findings from a ledger's `## Web Supplement (gap-fill)` section.

    Scoped strictly to that section (the next `## ` heading ends it). Skips the blockquote intro,
    `**Query:**` lines, and `still open — not filled` lines (which carry no URL). Each finding line
    is `- "<verbatim quote>" — <URL>`; parsing keys off the first URL on the line, so a quote that
    contains internal quote characters still parses.
    """
    findings: list[SupplementFinding] = []
    in_section = False
    gap = ""
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if _SECTION_RE.match(line):
            in_section, gap = True, ""
            continue
        if not in_section:
            continue
        if line.startswith("## "):           # any other H2 ends the supplement section
            break
        m_gap = _GAP_RE.match(line)
        if m_gap:
            gap = m_gap.group(1).strip()
            continue
        m_list = _LIST_RE.match(line)
        if not m_list:
            continue
        item = m_list.group(1).strip()
        if item.lower().lstrip("*").startswith("query:"):
            continue
        url_m = _URL_RE.search(item)
        if not url_m:                         # e.g. "still open — not filled"
            continue
        url = url_m.group(0).rstrip(".,;)")
        quote = _clean_quote(item[: url_m.start()])
        if not quote:
            continue
        findings.append(SupplementFinding(gap=gap, quote=quote, url=url))
    return findings


async def audit_supplement(markdown: str, *, fetch=None) -> list[SupplementVerdict]:
    """Re-fetch each finding's URL and confirm the cited quote appears verbatim there."""
    fetch = fetch or _simple_fetch
    verdicts: list[SupplementVerdict] = []
    for f in parse_supplement(markdown):
        text = await fetch(f.url)
        if not text:
            verdicts.append(SupplementVerdict(
                f, False, "fetch failed or returned empty (unreachable, non-HTML, or SSRF-blocked)"))
        elif quote_supported_at_url(cited_quote=f.quote, fetched_text=text):
            verdicts.append(SupplementVerdict(f, True, "verbatim quote found at URL"))
        else:
            verdicts.append(SupplementVerdict(
                f, False, "quote not found at URL (verbatim mismatch — demote to 'still open')"))
    return verdicts


@click.command()
@click.argument("ledger", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(ledger: Path):
    """Verify every cited quote in a ledger's Web Supplement is verbatim at its URL.

    Exit 0 = all findings verbatim-supported (or no supplement to check); exit 1 = at least one
    quote is not verbatim at its URL — demote each flagged item to "still open — not filled".
    """
    verdicts = asyncio.run(audit_supplement(ledger.read_text()))
    if not verdicts:
        console.print("[dim]No Web Supplement findings to verify.[/dim]")
        return
    unsupported = [v for v in verdicts if not v.supported]
    for v in verdicts:
        tag = "[green]✓ verbatim[/green]" if v.supported else "[red]✗ UNSUPPORTED[/red]"
        console.print(f"{tag}  {v.finding.url}")
        console.print(f"    {v.finding.quote[:100]}")
        if not v.supported:
            console.print(f"    [yellow]{v.reason}[/yellow]")
    supported = len(verdicts) - len(unsupported)
    console.print(f"\n[bold]{supported}/{len(verdicts)} verbatim-supported[/bold]")
    if unsupported:
        console.print(f"[red]{len(unsupported)} unsupported — demote each to "
                      f"'still open — not filled' in the ledger.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
