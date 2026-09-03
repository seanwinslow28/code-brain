#!/usr/bin/env python3
"""News lane for the Content Oracle -- the week's AI news, gisted, and the listening report.

Ruled on #227 (rulings 5-8, 18 and 21), built on #239. The sweep can only see what
the author did; this lane brings in what happened in AI that week, big and small,
across five subject branches (AI news, tools, agents, system design, creativity
with AI). It is a NEWS-shaped pull on purpose -- the one place "latest on X" is
allowed -- and it feeds two things: the frame stage (a two-line gist per item) and
a listening report the author absorbs by ear through the local TTS pipeline.

    news_lane.py pull     --out DIR [--date D] [--days 7] [--branch id ...] [--search hn,youtube,web] [--dry-run]
    news_lane.py gists    --check gists.json --pull <pull.md> [--report <report.md>]
    news_lane.py template --date D --items N --out <ignored path>
    news_lane.py check    --report <path> [--gists gists.json] [--pull pull.md] [--no-resolve] [--json]
    news_lane.py preview  --report <path>
    news_lane.py render   --report <path> [--force] [--skip-check]

The lane gathers and does not judge: `pull` is a stdlib wrapper over the
last30days script on its free legs; the gists and the report are written by the
in-session model reading the pull. What the script enforces is provenance and
shape -- every gist traces to a fetched URL, every report source is tier-audited,
a figure with no tier A/B source behind it fails the check, and the report's
shape is the one the flattener can read aloud (ruling 21). `render` refuses to
run until `check` is clean.

Everything the lane writes goes to a git-ignored path and the script refuses any
other, because the report names his spikes and the cards each item spawned.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import frame_stage as fs  # noqa: E402  -- payload law, gist loader, is_ignored

REPO = HERE.parents[2]
AGENTS_SDK = REPO / "agents-sdk"
AUDIT_SCRIPT = AGENTS_SDK / "scripts" / "audit_dr_citations.py"
DOC_TO_AUDIO = AGENTS_SDK / "scripts" / "doc_to_audio.py"
VENV_PY = AGENTS_SDK / ".venv" / "bin" / "python3"
REPORTS_DIR = REPO / "creative-studio" / "content-machine" / "oracle-reports"
LAST30DAYS = Path.home() / ".claude" / "skills" / "last30days" / "scripts" / "last30days.py"

# Subject branches ruled on #227 (ruling 5). Each carries two phrasings, because
# the legs are different instruments (measured 2026-09-03, first pull): YouTube and
# the web leg answer NEWS phrasing ("latest on X", "X this week" -- required here,
# banned for anchor queries, ruling 18), while the Hacker News leg is a literal
# keyword search over the window and "this week" in the query finds nothing. HN
# gets the bare nouns; its own date filter does the rest. HN is also called through
# the last30days *library* rather than its CLI: with Reddit and X both off, the CLI
# takes a fallback path that never starts the HN search (measured the same day), and
# the library hands back the story's own URL beside the thread URL, which is the
# primary source the tier audit wants.
BRANCHES: dict[str, tuple[str, str]] = {
    #  id              (NEWS-shaped query for youtube + web,                  bare nouns for hn)
    "news":           ("latest AI news this week",                            "AI"),
    "tools":          ("new AI tools released this week",                     "AI tool"),
    "agents":         ("AI agents news this week",                            "AI agents"),
    "system-design":  ("latest on AI agent infrastructure and system design", "agent infrastructure"),
    "creativity":     ("latest on making art, music and video with AI",       "AI art"),
}
# The free legs. Reddit and X spend ScrapeCreators credits and belong to the
# anchor scan, which asks a different kind of question.
DEFAULT_SEARCH = "hn,youtube,web"
PULL_TIMEOUT_S = 300

# Ruling 21: the shape the flattener can read aloud.
WORDS_MIN, WORDS_TARGET_MAX, WORDS_HARD_CAP = 1200, 1500, 2000
ITEMS_MAX = 6
ITEM_WORDS_MAX = 250
ITEM_PARAGRAPHS = 3
LIST_MAX = 3
SPOKEN_WPM = 150            # Kokoro at speed 1.0 measured 158 on the first render (2026-09-03); 150 keeps the band conservative
DURATION_CAP_MIN = 13

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_WORD_RE = re.compile(r"[A-Za-z0-9'’\-]+")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_ITEM_HEADER_RE = re.compile(
    r"^\*\*(?P<id>[^*]+)\*\*\s*(?:\[(?P<kind>[A-Z]+)\])?\s*\(score:(?P<score>\d+)\)\s*"
    r"(?P<who>.*?)\s*\((?P<date>\d{4}-\d{2}-\d{2})\)", re.M)
_SECTION_RE = re.compile(r"^###\s+(.+?)\s*$")
_URL_RE = re.compile(r"https?://[^\s)\]>]+")
_MD_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")
_LIST_LINE_RE = re.compile(r"^\s*(?:[-*+•]|\d+[.)])\s+")
_TABLE_LINE_RE = re.compile(r"^\s*\|.*\|\s*$")

# Spoken-safe: dates and large numbers are written as words (ruling 21). Short
# numerals survive because model names carry them ("GLM 5.3") and Kokoro reads
# those correctly.
_NOT_WORDS_RES = [
    ("ISO date", re.compile(r"\b\d{4}-\d{2}-\d{2}\b")),
    ("number with thousands separator", re.compile(r"\b\d{1,3}(?:,\d{3})+\b")),
    ("four-or-more-digit number", re.compile(r"(?<![\w.])\d{4,}(?![\w.])")),
    ("percent sign", re.compile(r"\d\s*%")),
    ("currency symbol", re.compile(r"[$€£]\s?\d")),
]
# A figure is a claim that needs a source behind it: a percentage, a sum of money,
# a magnitude, a multiplier. A count under a hundred is not a figure, and neither
# is a version number.
_FIGURE_RES = [
    ("percentage", re.compile(r"\d\s*%|\bper ?cent\b", re.I)),
    ("money", re.compile(r"[$€£]\s?\d|\b(?:dollars|euros|pounds)\b", re.I)),
    ("large number", re.compile(r"\b\d{1,3}(?:,\d{3})+\b|(?<![\w.])\d{4,}(?![\w.])")),
    ("magnitude word", re.compile(r"\b(?:hundred|thousand|million|billion|trillion)s?\b", re.I)),
    ("multiplier", re.compile(
        r"\b(?:\w+-fold|(?:\w+|\d+)\s+times\s+(?:faster|cheaper|slower|more|fewer|less|larger|"
        r"smaller|higher|lower|the|as|bigger|quicker|better|worse))\b", re.I)),
]
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


# ── small helpers ────────────────────────────────────────────────────────────

def words(text: str) -> int:
    return len(_WORD_RE.findall(text))


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
_ORDINALS = {1: "first", 2: "second", 3: "third", 5: "fifth", 8: "eighth", 9: "ninth", 12: "twelfth",
             20: "twentieth", 30: "thirtieth"}


def number_words(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    raise ValueError("number_words handles 0-99")


def ordinal_words(n: int) -> str:
    if n in _ORDINALS:
        return _ORDINALS[n]
    if n < 20:
        return _ONES[n] + "th"
    tens, ones = divmod(n, 10)
    if ones == 0:
        return _ORDINALS[n]
    return _TENS[tens] + "-" + ordinal_words(ones)


def date_in_words(d: date) -> str:
    """2026-09-06 -> 'Sunday, September sixth, twenty twenty-six' (spoken-safe, ruling 21)."""
    year = f"{number_words(d.year // 100)} {number_words(d.year % 100)}" if d.year % 100 else \
        f"{number_words(d.year // 100)} hundred"
    return f"{d.strftime('%A, %B')} {ordinal_words(d.day)}, {year}"


def refuse_unless_ignored(path: Path) -> None:
    if not fs.is_ignored(path):
        raise SystemExit(f"refusing to write {path}: git does not ignore it, and the news lane's "
                         f"files name his week. Use {REPORTS_DIR} or another ignored path.")


def _load_audit():
    spec = importlib.util.spec_from_file_location("audit_dr_citations", AUDIT_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


# ── pull ─────────────────────────────────────────────────────────────────────

@dataclass
class PullItem:
    branch: str
    section: str
    id: str
    who: str
    date: str
    title: str
    url: str
    score: int


def parse_pull(text: str) -> list[PullItem]:
    """Index the last30days compact output: one row per fetched item, no transcripts."""
    items: list[PullItem] = []
    branch = "?"
    section = "?"
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# BRANCH "):
            branch = line[len("# BRANCH "):].split(" ", 1)[0].strip()
            continue
        sec = _SECTION_RE.match(line)
        if sec:
            section = sec.group(1)
            continue
        m = _ITEM_HEADER_RE.match(line)
        if not m:
            continue
        title, url = "", ""
        for follow in lines[i + 1:i + 8]:
            s = follow.strip()
            if not s:
                continue
            if s.startswith("http") and not url:
                url = s
                break
            if not title and not s.startswith(("*", "Highlights", "Insights", "http")):
                title = s
        items.append(PullItem(branch=branch, section=section, id=m.group("id"), who=m.group("who"),
                              date=m.group("date"), title=title, url=url, score=int(m.group("score"))))
    return items


def render_index(items: list[PullItem], start: date | None = None, end: date | None = None) -> str:
    """Titles and URLs only. Items dated outside the window are listed apart: the
    YouTube leg ranks by relevance and returns evergreen roundups from months ago
    whatever --days says (measured 2026-09-03), and those are not this week's news."""
    def in_window(it: PullItem) -> bool:
        if start is None or end is None:
            return True
        return start.isoformat() <= it.date <= end.isoformat()

    out = ["# News pull index -- titles and URLs only; the pull file holds the full text", ""]
    seen: set[str] = set()
    late: list[PullItem] = []
    counts: dict[str, int] = {}
    for it in items:
        if it.url in seen:
            continue
        seen.add(it.url)
        if not in_window(it):
            late.append(it)
            continue
        counts[it.branch] = counts.get(it.branch, 0) + 1
        out.append(f"- [{it.branch} / {it.section}] {it.date} · {it.who} · {it.title} · {it.url}")
    out += ["", "In window, per branch: " + (", ".join(f"{k} {v}" for k, v in counts.items()) or "none")]
    if late:
        out += ["", f"## Out of window ({len(late)}) -- the leg ignored the date filter; not this week's news", ""]
        out += [f"- [{it.branch} / {it.section}] {it.date} · {it.who} · {it.title} · {it.url}" for it in late]
    return "\n".join(out) + "\n"


def pull_commands(branches: list[str], days: int, search: str) -> list[tuple[str, str, list[str]]]:
    """(branch, leg, argv) per subprocess call: the NEWS phrasing on every leg except hn,
    which runs through the library (see hn_leg). --quick trims the youtube and web legs."""
    legs = [l.strip() for l in search.split(",") if l.strip() and l.strip() != "hn"]
    cmds = []
    for b in branches:
        if b not in BRANCHES:
            raise SystemExit(f"unknown branch {b!r}; known: {', '.join(BRANCHES)}")
        news_q, _ = BRANCHES[b]
        if legs:
            cmds.append((b, ",".join(legs), [sys.executable, str(LAST30DAYS), news_q, "--search",
                                             ",".join(legs), "--days", str(days), "--quick",
                                             "--emit=compact"]))
    return cmds


def format_hn_items(items: list[dict]) -> str:
    """The compact shape parse_pull reads, plus the thread URL on its own line."""
    lines = ["### Hacker News Stories", ""]
    if not items:
        lines.append("*No Hacker News stories in the window for this query.*")
    for i, it in enumerate(items, 1):
        eng = it.get("engagement") or {}
        pts = eng.get("points") if isinstance(eng, dict) else None
        cmt = eng.get("num_comments") if isinstance(eng, dict) else None
        score = int(round(float(it.get("relevance") or 0) * 100))
        lines.append(f"**HN{i}** (score:{score}) hn/{it.get('author', '?')} ({it.get('date', '?')}) "
                     f"[{pts if pts is not None else '?'}pts, {cmt if cmt is not None else '?'}cmt]")
        lines.append(f"  {it.get('title', '').strip()}")
        lines.append(f"  {it.get('url') or it.get('hn_url', '')}")
        if it.get("hn_url") and it.get("url") != it.get("hn_url"):
            lines.append(f"  Thread: {it['hn_url']}")
        lines.append("")
    return "\n".join(lines)


def hn_leg(query: str, start: date, end: date) -> str:
    """Hacker News through the last30days library: Algolia search over the window, free."""
    scripts_dir = str(LAST30DAYS.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    try:
        from lib import hackernews  # type: ignore[import-not-found]
        raw = hackernews.search_hackernews(query, start.isoformat(), end.isoformat())
        items = hackernews.parse_hackernews_response(raw, query=query)
    except Exception as exc:  # noqa: BLE001 -- a failed leg is a line in the pull, not a crash
        return f"### Hacker News Stories\n\n**ERROR:** {type(exc).__name__}: {exc}\n"
    items = [it for it in items if start.isoformat() <= str(it.get("date", "")) <= end.isoformat()]
    return format_hn_items(items)


def run_pull(run_date: date, days: int, branches: list[str], search: str, out_dir: Path,
             dry_run: bool) -> tuple[Path, Path]:
    pull_path = out_dir / f"{run_date.isoformat()}-pull.md"
    index_path = out_dir / f"{run_date.isoformat()}-pull-index.md"
    start = run_date - timedelta(days=days)
    want_hn = "hn" in [l.strip() for l in search.split(",")]
    cmds = pull_commands(branches, days, search)
    if dry_run:
        for b in branches:
            if want_hn:
                print(f"[{b} / hn] library search {BRANCHES[b][1]!r} {start} .. {run_date}")
            for cb, leg, cmd in cmds:
                if cb == b:
                    print(f"[{b} / {leg}] {' '.join(cmd[2:])}")
        return pull_path, index_path
    if not LAST30DAYS.exists():
        raise SystemExit(f"last30days not found at {LAST30DAYS}")
    refuse_unless_ignored(pull_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    parts = [f"# News pull -- {run_date.isoformat()} (window {start.isoformat()} to {run_date.isoformat()}, legs {search})", ""]
    for b in branches:
        if want_hn:
            hn_q = BRANCHES[b][1]
            print(f"[{b} / hn] {hn_q!r} ...", file=sys.stderr, flush=True)
            parts += [f"# BRANCH {b} -- leg hn -- query: {hn_q}", "", hn_leg(hn_q, start, run_date), ""]
        for cb, leg, cmd in cmds:
            if cb != b:
                continue
            print(f"[{b} / {leg}] {cmd[2]!r} ...", file=sys.stderr, flush=True)
            try:
                done = subprocess.run(cmd, capture_output=True, text=True, timeout=PULL_TIMEOUT_S,
                                      cwd=LAST30DAYS.parent.parent)
                body = strip_ansi(done.stdout)
                if done.returncode != 0:
                    body += f"\n\n(last30days exited {done.returncode})\n{strip_ansi(done.stderr)[-2000:]}"
            except subprocess.TimeoutExpired:
                body = f"(last30days timed out after {PULL_TIMEOUT_S}s)"
            parts += [f"# BRANCH {b} -- leg {leg} -- query: {cmd[2]}", "", body, ""]
    text = "\n".join(parts)
    pull_path.write_text(text, encoding="utf-8")
    items = parse_pull(text)
    index_path.write_text(render_index(items, start, run_date), encoding="utf-8")
    inside = sum(1 for i in items if start.isoformat() <= i.date <= run_date.isoformat())
    print(f"→ {pull_path} ({words(text)} words)\n→ {index_path} ({len(items)} items, {inside} in window)",
          file=sys.stderr)
    return pull_path, index_path


# ── gists ────────────────────────────────────────────────────────────────────

def _norm_url(u: str) -> str:
    return u.strip().rstrip("/").rstrip(".,;")


def check_gists(gists_path: Path, pull_text: str | None, report_text: str | None = None) -> list[str]:
    """Shape, privacy, and provenance. Every gist must trace to a fetched URL (the pull)
    or to a source the report's audited fence carries -- a gist with no fetched URL
    behind it is an invention, and it would become a card's Evidence line."""
    problems: list[str] = []
    try:
        gists = fs.load_gists(gists_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [f"gists file: {exc}"]
    if len(gists) > fs.GIST_MAX_ITEMS:
        problems.append(f"{len(gists)} gists; the frame stage caps at {fs.GIST_MAX_ITEMS}")
    known: set[str] = set()
    for text in (pull_text, report_text):
        if text:
            known.update(_norm_url(u) for u in _URL_RE.findall(text))
    for i, g in enumerate(gists):
        for fname, val in (("happened", g.happened), ("can_now", g.can_now)):
            if len(val) > fs.GIST_FIELD_MAX:
                problems.append(f"gist {i}.{fname} is {len(val)} chars; cap is {fs.GIST_FIELD_MAX}")
            for name, pattern in fs.FORBIDDEN:
                hit = pattern.search(val)
                if hit:
                    problems.append(f"gist {i}.{fname}: {name} ({hit.group(0)[:24]!r})")
            if _URL_RE.search(val):
                problems.append(f"gist {i}.{fname} carries a URL; sources ride on 'source' only")
        if not g.source:
            problems.append(f"gist {i} has no source; a gist with no fetched URL behind it is an invention")
        elif known and _norm_url(g.source) not in known:
            problems.append(f"gist {i} source is not in the pull or the report's sources: {g.source}")
    return problems


# ── report ───────────────────────────────────────────────────────────────────

@dataclass
class Item:
    number: int
    title: str
    lines: list[str] = field(default_factory=list)

    @property
    def body(self) -> str:
        return "\n".join(self.lines)

    @property
    def paragraphs(self) -> list[str]:
        paras, cur = [], []
        for line in self.lines:
            if line.strip():
                cur.append(line.strip())
            elif cur:
                paras.append(" ".join(cur))
                cur = []
        if cur:
            paras.append(" ".join(cur))
        return paras


@dataclass
class Report:
    preamble: list[str]
    items: list[Item]
    sources: dict[int, list[tuple[str, str]]]
    has_sources_section: bool
    has_fence: bool
    fence_is_last: bool

    @property
    def body_words(self) -> int:
        return words("\n".join(self.preamble)) + sum(words(i.body) for i in self.items)


def parse_report(text: str) -> Report:
    text = _FRONTMATTER_RE.sub("", text, count=1)
    lines = text.splitlines()
    preamble: list[str] = []
    items: list[Item] = []
    sources_lines: list[str] = []
    has_sources = False
    in_sources = False
    cur: Item | None = None
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
            if title.lower().rstrip(":") == "sources":
                has_sources, in_sources, cur = True, True, None
                continue
            in_sources = False
            cur = Item(number=len(items) + 1, title=title)
            items.append(cur)
            continue
        if in_sources:
            sources_lines.append(line)
        elif cur is None:
            preamble.append(line)
        else:
            cur.lines.append(line)
    src_text = "\n".join(sources_lines)
    audit = _load_audit()
    sources: dict[int, list[tuple[str, str]]] = {}
    for idx, label, url in audit.parse_plain_sources(src_text):
        sources.setdefault(idx, []).append((label, url))
    fence_is_last = False
    if has_sources:
        headings = [l for l in lines if l.startswith("## ")]
        fence_is_last = headings[-1][3:].strip().lower().rstrip(":") == "sources"
    return Report(preamble=preamble, items=items, sources=sources,
                  has_sources_section=has_sources, has_fence="```" in src_text,
                  fence_is_last=fence_is_last)


def _list_runs(lines: list[str]) -> int:
    longest = run = 0
    for line in lines:
        if _LIST_LINE_RE.match(line):
            run += 1
            longest = max(longest, run)
        elif line.strip():
            run = 0
    return longest


def lint_report(rep: Report) -> tuple[list[str], list[str]]:
    """Ruling 21 made mechanical. Errors block the render; warnings are read aloud."""
    errors: list[str] = []
    warnings: list[str] = []
    n = len(rep.items)
    if n == 0:
        errors.append("no items: an item is one `##` heading followed by three paragraphs")
    if n > ITEMS_MAX:
        errors.append(f"{n} items; at most {ITEMS_MAX} -- the rest are cards, not narration")
    if not rep.has_sources_section:
        errors.append("no `## Sources` section")
    elif not rep.has_fence:
        errors.append("the Sources list must sit inside a code fence, so it is spoken once as "
                      "'Code block omitted' instead of six URLs read aloud")
    elif not rep.fence_is_last:
        errors.append("`## Sources` must be the last section")
    for it in rep.items:
        tag = f"item {it.number} ({it.title[:40]!r})"
        paras = it.paragraphs
        if len(paras) != ITEM_PARAGRAPHS:
            errors.append(f"{tag}: {len(paras)} paragraphs; the shape is exactly {ITEM_PARAGRAPHS} "
                          "(what happened with its source in the sentence; what it can now do; "
                          "the card or two it spawned)")
        w = words(it.body)
        if w > ITEM_WORDS_MAX:
            errors.append(f"{tag}: {w} words; an item over {ITEM_WORDS_MAX} is a piece, not a brief")
        if any(_TABLE_LINE_RE.match(l) for l in it.lines):
            errors.append(f"{tag}: table -- the flattener reads rows as comma lists")
        if any(l.strip().startswith("```") for l in it.lines):
            errors.append(f"{tag}: code fence in the body -- only the Sources list is fenced")
        if any(l.startswith("#") for l in it.lines):
            errors.append(f"{tag}: sub-heading -- one `##` per item, nothing deeper")
        if _URL_RE.search(it.body):
            errors.append(f"{tag}: raw URL in the narration -- name the source in the sentence and "
                          "put the URL in the Sources fence")
        if _MD_LINK_RE.search(it.body):
            warnings.append(f"{tag}: markdown link -- the flattener drops the URL and keeps the text; "
                            "make sure the source is named in the sentence")
        run = _list_runs(it.lines)
        if run > LIST_MAX:
            errors.append(f"{tag}: a list of {run}; at most {LIST_MAX}")
        for name, pattern in _NOT_WORDS_RES:
            hit = pattern.search(it.body)
            if hit:
                errors.append(f"{tag}: {name} {hit.group(0)!r} -- write dates and large numbers as words")
        if it.number not in rep.sources:
            errors.append(f"{tag}: no line numbered {it.number} in the Sources fence")
    for idx in rep.sources:
        if idx > n or idx < 1:
            errors.append(f"Sources fence names item {idx}, but there are {n} items")
    total = rep.body_words
    if total > WORDS_HARD_CAP:
        errors.append(f"{total} words; hard cap is {WORDS_HARD_CAP} (about {DURATION_CAP_MIN} minutes)")
    elif total < WORDS_MIN or total > WORDS_TARGET_MAX:
        warnings.append(f"{total} words; the band is {WORDS_MIN}-{WORDS_TARGET_MAX} "
                        f"(about {total // SPOKEN_WPM} minutes at {SPOKEN_WPM} words a minute)")
    return errors, warnings


def figure_sentences(text: str) -> list[tuple[str, str]]:
    out = []
    for sentence in _SENTENCE_SPLIT_RE.split(" ".join(text.split())):
        for name, pattern in _FIGURE_RES:
            if pattern.search(sentence):
                out.append((name, sentence.strip()))
                break
    return out


def audit_report(rep: Report, resolve: bool = True) -> tuple[list[str], list[str], list[dict]]:
    """Ruling 8 and 21: tier every source, and a figure with no tier A/B source behind
    it is dropped from the narration -- the check fails until it is."""
    audit = _load_audit()
    flat = [(idx, label, url) for idx, rows in sorted(rep.sources.items()) for label, url in rows]
    rows = audit.audit_urls(flat, resolve_urls=resolve)
    by_item: dict[int, list[dict]] = {}
    for r in rows:
        by_item.setdefault(r["idx"], []).append(r)
    errors: list[str] = []
    warnings: list[str] = []
    record: list[dict] = []
    for it in rep.items:
        srcs = by_item.get(it.number, [])
        tiers = [r["tier"] for r in srcs]
        citable = any(audit.is_citable(t) for t in tiers)
        figures = figure_sentences(it.body)
        tag = f"item {it.number} ({it.title[:40]!r})"
        for r in srcs:
            if r["tier"].startswith("X"):
                warnings.append(f"{tag}: source did not resolve: {r['url']}")
        if figures and not citable:
            for kind, sentence in figures:
                errors.append(f"{tag}: {kind} with no tier A/B source behind it -- drop it from the "
                              f"narration or cite the primary source: {sentence[:160]!r}")
        if not citable and srcs:
            warnings.append(f"{tag}: every source is tier C/D ({', '.join(tiers)}); "
                            "the item may run, but no figure may")
        record.append({"item": it.number, "title": it.title, "tiers": tiers,
                       "citable": citable, "figures": len(figures), "words": words(it.body)})
    return errors, warnings, record


def check_report(report_path: Path, gists_path: Path | None, pull_path: Path | None,
                 resolve: bool) -> dict:
    text = report_path.read_text(encoding="utf-8")
    rep = parse_report(text)
    errors, warnings = lint_report(rep)
    a_err, a_warn, record = audit_report(rep, resolve=resolve)
    errors += a_err
    warnings += a_warn
    pull_text = pull_path.read_text(encoding="utf-8") if pull_path else None
    if pull_text:
        fetched = {_norm_url(u) for u in _URL_RE.findall(pull_text)}
        for idx, rows in rep.sources.items():
            for _, url in rows:
                if _norm_url(url) not in fetched:
                    warnings.append(f"item {idx}: source not in the pull -- confirm it is the primary "
                                    f"behind a fetched item: {url}")
    if gists_path:
        errors += check_gists(gists_path, pull_text, text)
    return {"report": str(report_path), "items": len(rep.items), "words": rep.body_words,
            "minutes_estimate": round(rep.body_words / SPOKEN_WPM, 1),
            "errors": errors, "warnings": warnings, "record": record}


def print_check(result: dict) -> None:
    print(f"{result['report']}: {result['items']} items, {result['words']} words "
          f"(~{result['minutes_estimate']} min at {SPOKEN_WPM} wpm)")
    for r in result["record"]:
        print(f"  item {r['item']}: {r['words']} words · tiers {r['tiers'] or ['none']} · "
              f"{'citable' if r['citable'] else 'no A/B source'} · figures {r['figures']}")
    for w in result["warnings"]:
        print(f"  warn: {w}")
    for e in result["errors"]:
        print(f"  FAIL: {e}")
    print("check: " + ("clean" if not result["errors"] else f"{len(result['errors'])} failure(s)"))


# ── template / preview / render ──────────────────────────────────────────────

def template_text(run_date: date, items: int, days: int = 7) -> str:
    window_start = run_date - timedelta(days=days)
    head = [
        "---",
        "type: oracle-report",
        f"date: {run_date.isoformat()}",
        f"window: {window_start.isoformat()} to {run_date.isoformat()}",
        f"items: {items}",
        "status: draft",
        "---",
        "",
        f"# The week in AI, {date_in_words(run_date)}",
        "",
        "<one short paragraph, optional: what kind of week it was. No numbers.>",
        "",
    ]
    for i in range(1, items + 1):
        head += [
            f"## <item {i} title -- spoken as the section title>",
            "",
            "<What happened, with the source named in the sentence. Dates and large numbers as "
            "words. A figure only if a tier A or B source is behind it.>",
            "",
            "<What it can now do that it could not last week.>",
            "",
            "<The one or two experiment cards it spawned, one line each: do this, expect that.>",
            "",
        ]
    head += ["## Sources", "", "```text"]
    for i in range(1, items + 1):
        head.append(f"{i}. <title> -- https://<primary source for item {i}>")
    head += ["```", ""]
    return "\n".join(head)


def preview_text(report_path: Path) -> str:
    """Exactly what the flattener will hand the synthesizer, one line per element."""
    code = (
        "import sys; from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "from lib.markdown_to_speech import preprocess, Segment, SectionBreak\n"
        "for e in preprocess(Path(sys.argv[2]).read_text(encoding='utf-8')):\n"
        "    print(('[H%d] ' % e.level) + e.title if isinstance(e, SectionBreak) else '    ' + e.text)\n"
    )
    py = VENV_PY if VENV_PY.exists() else Path(sys.executable)
    done = subprocess.run([str(py), "-c", code, str(AGENTS_SDK), str(report_path)],
                          capture_output=True, text=True, timeout=60)
    if done.returncode != 0:
        raise SystemExit(f"preview failed: {done.stderr[-800:]}")
    return done.stdout


def render_report(report_path: Path, force: bool) -> dict:
    report_path = report_path.resolve()   # doc_to_audio runs with cwd=agents-sdk
    if not VENV_PY.exists():
        raise SystemExit(f"agents-sdk venv missing at {VENV_PY}; run agents-sdk/scripts/install_tts_models.sh")
    cmd = [str(VENV_PY), str(DOC_TO_AUDIO), "--source", str(report_path), "--json"]
    if force:
        cmd.append("--force")
    env = dict(os.environ, PYTHONPATH=str(AGENTS_SDK))
    done = subprocess.run(cmd, capture_output=True, text=True, cwd=AGENTS_SDK, env=env, timeout=1800)
    if done.returncode != 0:
        raise SystemExit(f"doc_to_audio failed ({done.returncode}): {done.stderr[-1200:]}")
    last = [l for l in done.stdout.splitlines() if l.strip().startswith("{")]
    payload = json.loads(last[-1]) if last else {"status": "unknown", "raw": done.stdout[-500:]}
    text = report_path.read_text(encoding="utf-8")
    payload["words"] = parse_report(text).body_words
    if payload.get("duration_sec"):
        payload["minutes"] = round(payload["duration_sec"] / 60, 2)
        payload["words_per_minute"] = round(payload["words"] / (payload["duration_sec"] / 60))
        payload["under_cap"] = payload["duration_sec"] / 60 < DURATION_CAP_MIN
    return payload


# ── CLI ──────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pull", help="run the NEWS-shaped queries on the free legs; write pull + index")
    p.add_argument("--out", type=Path, default=REPORTS_DIR, help="ignored directory (default oracle-reports/)")
    p.add_argument("--date", type=date.fromisoformat, default=date.today())
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--branch", action="append", help="branch id (repeatable); default all five")
    p.add_argument("--search", default=DEFAULT_SEARCH, help=f"last30days legs (default {DEFAULT_SEARCH})")
    p.add_argument("--dry-run", action="store_true", help="print the queries; fetch nothing")

    g = sub.add_parser("gists", help="validate a gists.json: shape, privacy, provenance")
    g.add_argument("--check", type=Path, required=True)
    g.add_argument("--pull", type=Path)
    g.add_argument("--report", type=Path)

    t = sub.add_parser("template", help="write the report skeleton to an ignored path")
    t.add_argument("--date", type=date.fromisoformat, default=date.today())
    t.add_argument("--items", type=int, default=ITEMS_MAX)
    t.add_argument("--days", type=int, default=7)
    t.add_argument("--out", type=Path, help=f"default {REPORTS_DIR}/<date>-oracle-report.md")

    c = sub.add_parser("check", help="lint the shape and tier-audit the sources; exit 2 on failure")
    c.add_argument("--report", type=Path, required=True)
    c.add_argument("--gists", type=Path)
    c.add_argument("--pull", type=Path)
    c.add_argument("--no-resolve", action="store_true", help="classify written URLs; no network")
    c.add_argument("--json", action="store_true")

    v = sub.add_parser("preview", help="print exactly what the flattener will speak")
    v.add_argument("--report", type=Path, required=True)

    r = sub.add_parser("render", help="check, then render to MP3 via doc_to_audio.py")
    r.add_argument("--report", type=Path, required=True)
    r.add_argument("--gists", type=Path)
    r.add_argument("--pull", type=Path)
    r.add_argument("--force", action="store_true")
    r.add_argument("--skip-check", action="store_true", help="render even if the check fails (not for a real week)")

    args = ap.parse_args(argv)

    if args.cmd == "pull":
        run_pull(args.date, args.days, args.branch or list(BRANCHES), args.search, args.out, args.dry_run)
        return 0

    if args.cmd == "gists":
        pull_text = args.pull.read_text(encoding="utf-8") if args.pull else None
        report_text = args.report.read_text(encoding="utf-8") if args.report else None
        problems = check_gists(args.check, pull_text, report_text)
        for pr in problems:
            print(f"  FAIL: {pr}")
        print("gists: " + ("clean" if not problems else f"{len(problems)} problem(s)"))
        return 0 if not problems else 2

    if args.cmd == "template":
        out = args.out or REPORTS_DIR / f"{args.date.isoformat()}-oracle-report.md"
        refuse_unless_ignored(out)
        if out.exists():
            raise SystemExit(f"{out} exists; not overwriting a report")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(template_text(args.date, args.items, args.days), encoding="utf-8")
        print(f"→ {out}")
        return 0

    if args.cmd == "check":
        result = check_report(args.report, args.gists, args.pull, resolve=not args.no_resolve)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_check(result)
        return 0 if not result["errors"] else 2

    if args.cmd == "preview":
        sys.stdout.write(preview_text(args.report))
        return 0

    if args.cmd == "render":
        if not args.skip_check:
            result = check_report(args.report, args.gists, args.pull, resolve=True)
            print_check(result)
            if result["errors"]:
                print("render refused: fix the check first (or --skip-check for a throwaway).", file=sys.stderr)
                return 2
        payload = render_report(args.report, args.force)
        print(json.dumps(payload, indent=2))
        if payload.get("status") == "ok" and not payload.get("under_cap", True):
            print(f"over the {DURATION_CAP_MIN}-minute cap: cut items, not sentences.", file=sys.stderr)
            return 2
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
