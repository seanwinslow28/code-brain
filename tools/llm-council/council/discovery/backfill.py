# council/discovery/backfill.py
"""Stage 5 — BACKFILL (web-supplement gap-fill).

Runs after VERIFY/FRAME. Turns each blind-spot bullet from the FUSE panel into a targeted
*solution/evidence-side* web search (not a complaint search), URL-anchors every verbatim finding,
and returns a structured supplement the renderer appends as a clearly-separate ledger section. A
gap it cannot fill is marked "still open" — never papered over.

COST-INTEGRITY: this stage reuses ONLY the existing `collect_web` rail (Exa/Brave on the user's own
keys → $0 on the OpenRouter ledger) and makes NO model call in v1 — deterministic query templating +
deterministic extraction keep it free and fully testable. If a billable call is ever added here, it
MUST thread its cost into a typed failure + record_spend exactly like FusionError.cost →
DiscoveryFailed.cost_usd (see gather/__init__.py invariant). The pipeline prices the (free) web
queries at WEB_QUERY_PRICE for honest budget accounting.
"""

import os
import re
from dataclasses import dataclass, field

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.gather.web import _SENT, collect_web
from council.discovery.textbudget import BRAVE_Q_MAX_CHARS, BRAVE_Q_MAX_WORDS, clamp_words_chars
from council.discovery.verify import quote_supported_at_url


@dataclass
class BackfillItem:
    gap: str
    query: str
    findings: list[EvidenceRecord] = field(default_factory=list)
    status: str = "still open"            # "filled" | "still open"


@dataclass
class BackfillResult:
    skipped: bool = False
    skip_reason: str = ""
    items: list[BackfillItem] = field(default_factory=list)
    queries_run: int = 0                  # priced at WEB_QUERY_PRICE by the pipeline


def supplement_section(supplement: "BackfillResult | None") -> list[str]:
    """Markdown lines for the '## Web Supplement (gap-fill)' ledger section, shared by both renderers.

    Returns [] when supplement is None (stage not run / --no-supplement) so the ledger stays
    byte-identical to the pre-Stage-5 output. Kept deliberately SEPARATE from the panel's ranked
    list — these web findings never enter the FUSE-consensus ranking.
    """
    if supplement is None:
        return []
    L = ["## Web Supplement (gap-fill)\n"]
    if supplement.skipped:
        L.append(f"_supplement skipped: {supplement.skip_reason}_")
        L.append("")
        return L
    L.append("> Gap-fill **LEADS** from a solution-side web search of the blind-spot map — NOT "
             "FUSE-consensus, panel-ranked claims. Each finding is a verbatim quote at a real URL, but "
             "relevance is not yet vetted (roadmap E1). Treat as leads; verify before use.\n")
    if not supplement.items:
        L.append("_(no blind spots surfaced)_")
        L.append("")
        return L
    for it in supplement.items:
        L.append(f"### {it.gap}")
        L.append(f"- **Query:** `{it.query}`")
        if it.findings:
            L.extend(f'- "{r.quote}" — {r.url}' for r in it.findings)
        else:
            L.append("- _still open — not filled_")
        L.append("")
    return L


# Leading "meta" words that describe the *absence* of evidence — strip them so the query targets the
# subject of the gap (the solution/comparison/data we want), not the meta-observation.
_META_PREFIX = re.compile(
    r"^\s*(?:"
    r"no\s+evidence(?:\s+(?:on|that|whether|of|for|about))?"
    r"|no\s+proof(?:\s+(?:of|that))?"
    r"|no\s+data(?:\s+(?:on|about))?"
    r"|no\s+clear"
    r"|evidence(?:\s+(?:on|that|whether|of|for|about))?"
    r"|proof(?:\s+(?:of|that))?"
    r"|data(?:\s+(?:on|about))?"
    r"|lack\s+of|lacking|absence\s+of|missing"
    r"|little|limited|sparse|scarce|minimal|few"
    r"|unclear(?:\s+(?:on|whether))?|unknown|uncertain"
    r"|no"                                # bare leading "no " (e.g. "No tool head-to-head")
    r")\b[\s:,\-]*",
    re.I,
)

_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "their", "what", "when",
    "how", "why", "does", "are", "was", "were", "will", "into", "over", "under", "about",
    "they", "them", "than", "then", "also", "such", "some", "any", "all", "you", "our",
    "its", "his", "her", "not", "but", "can", "had", "has", "have", "who", "which", "whom",
    "whose", "been", "being", "very", "just", "only", "more", "most",
}


def _strip_meta_prefix(blind_spot: str) -> str:
    cur = blind_spot.strip()
    for _ in range(3):                    # handles stacked prefixes, e.g. "No clear evidence on …"
        nxt = _META_PREFIX.sub("", cur, count=1).strip()
        if nxt == cur or not nxt:
            break
        cur = nxt
    return cur or blind_spot.strip()


# Clamp with margin under Brave's q-param ceiling (textbudget.BRAVE_Q_MAX_*); exceeding it 422s the
# search and (pre-fix) crashed the whole post-FUSE pipeline (observed 2026-06-28 deep run).
_MAX_QUERY_WORDS = BRAVE_Q_MAX_WORDS - 10   # 40
_MAX_QUERY_CHARS = BRAVE_Q_MAX_CHARS - 40   # 360


def _supplement_query(blind_spot: str, topic: str, segment: str) -> str:
    """Solution/evidence-side query for a blind-spot gap. Deliberately NOT the complaint query.

    Clamped under Brave's q-param ceiling: the topic head is kept intact (most on-subject), the gap is
    trimmed to the remaining word budget, then "2026" is appended. The shared `clamp_words_chars` is
    the final safety net (also catches a topic head that alone exceeds the word ceiling).
    """
    gap = _strip_meta_prefix(blind_spot)
    head = " ".join(p for p in (topic.strip(), segment.strip()) if p)
    budget = max(4, _MAX_QUERY_WORDS - len(head.split()) - 1)   # -1 reserves a slot for "2026"
    gap = " ".join(gap.split()[:budget])
    q = " ".join(p for p in (head, gap, "2026") if p)
    return clamp_words_chars(q, max_words=_MAX_QUERY_WORDS, max_chars=_MAX_QUERY_CHARS)


def _keywords(query: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z]+", query.lower()) if len(w) >= 4 and w not in _STOPWORDS}


def _make_relevant_extractor(query: str, *, min_overlap: int = 2, limit: int = 3):
    """Permissive verbatim extractor: pull sentences overlapping >=2 distinct query keywords.

    Unlike Stage 1's complaint-only regex, this surfaces solutions, comparisons, and data — the
    content that actually fills a gap. Still verbatim (sentences lifted unchanged from fetched text).
    """
    kws = _keywords(query)

    def extract(text: str) -> list[str]:
        out: list[str] = []
        if not kws:
            return out
        for sent in _SENT.findall(text):
            low = sent.lower()
            if sum(1 for k in kws if k in low) >= min_overlap:
                out.append(sent.strip())
            if len(out) >= limit:
                break
        return out

    return extract


async def run_backfill(*, blind_spots: list[str], bundle: EvidenceBundle, topic: str, segment: str,
                       tier, search=..., fetch=...) -> BackfillResult:
    # Graceful degradation: with no injected search AND no web-search key, skip honestly. (collect_web
    # returns [] for BOTH "no key" and "found nothing", so the explicit check here is what lets us emit
    # the distinct "skipped" note instead of a wall of "still open".)
    if search is ... and not (os.environ.get("EXA_API_KEY") or os.environ.get("BRAVE_API_KEY")):
        return BackfillResult(skipped=True,
                              skip_reason="no web-search key configured (set EXA_API_KEY or BRAVE_API_KEY)")

    cap = getattr(tier, "supplement_max_blind_spots", 2)
    gaps = [g for g in (blind_spots or []) if g and g.strip()][:cap]
    supp = EvidenceBundle()               # within-supplement dedup (cross-gap) via existing _dedup_key
    items: list[BackfillItem] = []
    queries_run = 0

    for gap in gaps:
        query = _supplement_query(gap, topic, segment)
        extractor = _make_relevant_extractor(query)
        try:
            recs = await collect_web(topic=topic, segment=segment, query=query, extract=extractor,
                                     source_type="web-supplement", search=search, fetch=fetch)
        except Exception:
            # A search/fetch backend error (e.g. a Brave 422) degrades this gap to "still open" rather
            # than crashing the pipeline post-FUSE (SKILL.md §8 "supplement never crashes"). The failed
            # query is not cost-counted (queries_run is only incremented on a successful collect_web).
            items.append(BackfillItem(gap=gap, query=query, findings=[], status="still open"))
            continue
        queries_run += 1
        findings: list[EvidenceRecord] = []
        for r in recs:
            if bundle.has_url(r.url):      # already a Stage-1 evidence URL → don't re-surface
                continue
            # Anti-fabrication gate, routed through the single shared chokepoint (verify.py). In v1 this
            # is SAFE BY CONSTRUCTION: r.quote was deterministically extracted verbatim from the page at
            # r.url, so it is trivially supported — the supplement cannot fabricate a quote. The real,
            # un-vetted failure mode is RELEVANCE (keyword overlap can surface an on-keyword/off-topic
            # sentence); roadmap E1 upgrades quote_supported_at_url to atomic-claim + NLI entailment and
            # this stage inherits that relevance vetting for free. Until E1, the section is labeled LEADS.
            if not quote_supported_at_url(cited_quote=r.quote, fetched_text=r.quote):
                continue
            if not supp.add(r):            # dedup against other gaps' findings (url + quote)
                continue
            findings.append(r)
        items.append(BackfillItem(gap=gap, query=query, findings=findings,
                                  status="filled" if findings else "still open"))

    return BackfillResult(skipped=False, items=items, queries_run=queries_run)
