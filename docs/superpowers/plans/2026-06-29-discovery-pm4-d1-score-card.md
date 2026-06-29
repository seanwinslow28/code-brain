# Discovery PM4 + D1: Real Opportunity Score + PRD-Grade Card — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the toy opportunity score + filler card in the discovery PM/substack lenses with a research-grounded `value × confidence` composite and a PRD-grade card (who · pain-in-their-words · evidence · size · why-now · proposed bet).

**Architecture:** Two new pure modules — `scoring.py` (RICE-style `composite = 100 × value × confidence`) and `bet.py` (deterministic pain-shape → riskiest-assumption/cheapest-test heuristic). `frame_pm`/`frame_substack` compose them (threading the `EvidenceBundle` for reach/recency signals); `render.py`/`render_substack.py` render the new shapes. No new network calls, $0 API spend, verification gate untouched.

**Tech Stack:** Python 3 (stdlib only — `dataclasses`, `datetime`, `math`, `re`, `urllib.parse`), pytest, `uv`.

## Global Constraints

- **No new API spend / no network calls** — every signal comes from `VerifiedPainPoint` + `EvidenceBundle` + `FusionResult` already in memory.
- **Verification gate is sacred** — the score never invents data; cards cite only `v.supporting_urls`.
- **TDD** — write each failing test first, watch it fail, then minimal implementation.
- **Determinism** — `today` is an injectable parameter everywhere recency is computed; never call `date.today()` inside a scored helper without an override.
- **Run from** `tools/llm-council/`; tests via `uv run pytest`.
- **Tunable constants are flagged for sensitivity-testing**, not neutral defaults (composite-indicator theory).
- Commit messages end with the `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` trailer.

## File Structure

- **Create** `council/discovery/scoring.py` — `ScoreBreakdown` + `score_opportunity()` + private parse helpers + tunable constants.
- **Create** `council/discovery/bet.py` — `ProposedBet` + `classify_pain_shape()` + `propose_bet()` + shape→bet map.
- **Modify** `council/discovery/frame.py` — redesign `IdeaCard`; `frame_pm` threads `bundle`, uses scoring + bet.
- **Modify** `council/discovery/frame_substack.py` — `PostAngle.score` → `ScoreBreakdown` (drop `corroboration`); `frame_substack` threads `bundle`, uses scoring.
- **Modify** `council/discovery/render.py` — new card layout in `render_ledger`.
- **Modify** `council/discovery/render_substack.py` — read `a.score.composite` / `a.score.distinct_domains`.
- **Modify** `council/discovery/pipeline.py` — pass `bundle` + one `today` into both frame functions.
- **Create** `tests/discovery/test_scoring.py`, `tests/discovery/test_bet.py`.
- **Modify** `tests/discovery/test_frame.py`, `test_render.py`, `test_frame_substack.py`, `test_render_substack.py`.
- **Docs** `.claude/skills/fusion-discovery-council/SKILL.md`, `CHANGELOG.md`, `vault/00_inbox/tickets.md`.

---

### Task 1: `scoring.py` — the composite score (pure, isolated)

**Files:**
- Create: `council/discovery/scoring.py`
- Test: `tests/discovery/test_scoring.py`

**Interfaces:**
- Consumes: `CandidatePainPoint` (fields `intensity:int`, `recency:str`, `consensus:str`), `EvidenceBundle` (`.records` of `EvidenceRecord(source_name, url, date, quote, engagement)`).
- Produces: `ScoreBreakdown` dataclass (frozen) with fields `composite, value, confidence, importance, reach, recency, source_corroboration, consensus_ratio, intensity, engagement_sum, distinct_authors, distinct_domains, evidence_date`; and `score_opportunity(point, supporting_urls: list[str], bundle, *, today: date|None=None, value_weights=VALUE_WEIGHTS) -> ScoreBreakdown`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/discovery/test_scoring.py
from datetime import date

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint
from council.discovery.scoring import (
    ScoreBreakdown, score_opportunity, _parse_loose_date, _parse_consensus,
    CONF_FLOOR,
)

TODAY = date(2026, 6, 29)


def _bundle(*recs):
    b = EvidenceBundle()
    for r in recs:
        b.add(r)
    return b


def _pt(intensity=3, recency="2026-06", consensus="4/4 models"):
    return CandidatePainPoint("Title", "summary", quotes=["q"], urls=[],
                              intensity=intensity, recency=recency, consensus=consensus)


def test_parse_loose_date_handles_formats_and_garbage():
    assert _parse_loose_date("2026-06-15") == date(2026, 6, 15)
    assert _parse_loose_date("2026-06") == date(2026, 6, 1)
    assert _parse_loose_date("2026") == date(2026, 1, 1)
    assert _parse_loose_date("last week") is None
    assert _parse_loose_date("") is None


def test_parse_consensus_ratio():
    assert _parse_consensus("4/4 models") == 1.0
    assert _parse_consensus("3/4") == 0.75
    assert _parse_consensus("garbage") == 0.0
    assert _parse_consensus("") == 0.0


def test_full_evidence_scores_near_max_confidence():
    urls = [f"https://d{i}.com/x" for i in range(4)]
    recs = [EvidenceRecord("reddit", f"author{i}", urls[i], "2026-06-20", "q", engagement=200)
            for i in range(4)]
    s = score_opportunity(_pt(intensity=5), urls, _bundle(*recs), today=TODAY)
    assert s.confidence > 0.95            # 4 domains + 4/4 consensus
    assert s.distinct_domains == 4
    assert s.composite == round(100 * s.value * s.confidence, 1)


def test_single_source_is_discounted_even_with_full_consensus():
    rec = EvidenceRecord("reddit", "solo", "https://one.com/x", "2026-06-20", "q", engagement=999)
    s = score_opportunity(_pt(intensity=5, consensus="4/4 models"),
                          ["https://one.com/x"], _bundle(rec), today=TODAY)
    assert s.distinct_domains == 1
    assert s.confidence < 0.8             # corroboration illusion guarded
    assert s.confidence >= CONF_FLOOR     # halved, never zeroed


def test_reach_is_log_damped_not_linear():
    rec_lo = EvidenceRecord("reddit", "a", "https://a.com/x", "2026-06-20", "q", engagement=10)
    rec_hi = EvidenceRecord("reddit", "a", "https://a.com/x", "2026-06-20", "q", engagement=1000)
    lo = score_opportunity(_pt(), ["https://a.com/x"], _bundle(rec_lo), today=TODAY)
    hi = score_opportunity(_pt(), ["https://a.com/x"], _bundle(rec_hi), today=TODAY)
    # 100x engagement must NOT yield anywhere near 100x reach (saturation)
    assert hi.reach > lo.reach
    assert hi.reach < lo.reach * 3


def test_missing_intensity_floors_at_one():
    s = score_opportunity(_pt(intensity=0), [], EvidenceBundle(), today=TODAY)
    assert s.intensity == 1
    assert s.importance == 0.2


def test_unparseable_recency_is_neutral():
    s = score_opportunity(_pt(recency="recently"), [], EvidenceBundle(), today=TODAY)
    assert s.recency == 0.5
    assert s.evidence_date == ""


def test_recency_floor_holds_for_old_evidence():
    s = score_opportunity(_pt(recency="2020-01"), [], EvidenceBundle(), today=TODAY)
    assert s.recency == 0.3              # RECENCY_FLOOR, not ~0


def test_sensitivity_sanity_corroborated_mid_beats_single_high():
    # a well-corroborated importance-3 pain should outrank a single-source importance-5 pain
    multi_urls = [f"https://d{i}.com/x" for i in range(4)]
    multi = score_opportunity(
        _pt(intensity=3),
        multi_urls,
        _bundle(*[EvidenceRecord("reddit", f"a{i}", multi_urls[i], "2026-06-20", "q", engagement=150)
                  for i in range(4)]),
        today=TODAY)
    single = score_opportunity(
        _pt(intensity=5),
        ["https://one.com/x"],
        _bundle(EvidenceRecord("reddit", "solo", "https://one.com/x", "2026-06-20", "q", engagement=150)),
        today=TODAY)
    assert multi.composite > single.composite
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_scoring.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.scoring'`

- [ ] **Step 3: Write the implementation**

```python
# council/discovery/scoring.py
"""PM4 — research-grounded opportunity score. composite = 100 * value * confidence.

value      = weighted(importance, reach, recency)   — "how big / how fresh"
confidence = independent-source corroboration + model consensus (discount multiplier)

RICE-style: confidence MULTIPLIES the value so a thin-evidence pain is discounted, not
propped up by high importance. Reach is log-damped (Reddit "hot" precedent) so one viral
post can't dominate. Constants are TUNABLE and flagged for sensitivity-testing — they
materially change rankings (composite-indicator theory); the card shows the full breakdown.
See vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import log1p
from urllib.parse import urlparse
import re

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import CandidatePainPoint

# --- tunable constants (sensitivity-test before trusting absolute values) ---
VALUE_WEIGHTS = {"importance": 0.45, "reach": 0.40, "recency": 0.15}   # sum 1.0
REACH_CEIL = 500          # engagement log-saturation point
BREADTH_CEIL = 8          # authors + domains saturation
HALFLIFE_DAYS = 30        # exponential recency decay half-life
RECENCY_FLOOR = 0.3       # anti over-correction — old durable pain isn't crushed
RECENCY_NEUTRAL = 0.5     # unparseable date
DOMAIN_CEIL = 4           # independent domains for full source credit
AUTHOR_CEIL = 5           # distinct authors for full source credit
CONF_FLOOR = 0.5          # a single-source pain is halved, never zeroed
CONF_SRC_WT = 0.7         # independent sources dominate confidence
CONF_CONSENSUS_WT = 0.3   # model agreement is a lighter, separate signal


@dataclass(frozen=True)
class ScoreBreakdown:
    composite: float            # 0-100 headline = 100 * value * confidence
    value: float                # 0-1
    confidence: float           # CONF_FLOOR-1.0
    importance: float           # 0-1
    reach: float                # 0-1
    recency: float              # 0-1
    source_corroboration: float # 0-1  independent evidence breadth
    consensus_ratio: float      # 0-1  model-panel agreement
    intensity: int
    engagement_sum: int
    distinct_authors: int
    distinct_domains: int
    evidence_date: str          # parsed date used, or ""


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _parse_loose_date(s: str) -> date | None:
    s = (s or "").strip()
    for fmt, n in (("%Y-%m-%d", 10), ("%Y-%m", 7), ("%Y", 4)):
        try:
            return datetime.strptime(s[:n], fmt).date()
        except ValueError:
            continue
    return None


def _parse_consensus(s: str) -> float:
    """'4/4 models' -> 1.0, '3/4' -> 0.75, garbage -> 0.0."""
    m = re.search(r"(\d+)\s*/\s*(\d+)", s or "")
    if not m:
        return 0.0
    num, den = int(m.group(1)), int(m.group(2))
    return _clamp(num / den) if den > 0 else 0.0


def score_opportunity(
    point: CandidatePainPoint,
    supporting_urls: list[str],
    bundle: EvidenceBundle,
    *,
    today: date | None = None,
    value_weights: dict[str, float] = VALUE_WEIGHTS,
) -> ScoreBreakdown:
    today = today or date.today()
    supp = set(supporting_urls)
    recs = [r for r in bundle.records if r.url in supp]

    # importance ← intensity (floored at 1)
    intensity = max(int(point.intensity or 0), 1)
    importance = _clamp(intensity / 5)

    # reach ← log-damped engagement + breadth (authors + domains)
    eng_sum = sum(int(r.engagement or 0) for r in recs)
    distinct_authors = len({r.source_name for r in recs if r.source_name})
    distinct_domains = len({urlparse(u).netloc for u in supporting_urls if u})
    breadth = distinct_authors + distinct_domains
    reach = _clamp(0.7 * (log1p(eng_sum) / log1p(REACH_CEIL))
                   + 0.3 * min(breadth / BREADTH_CEIL, 1.0))

    # recency ← exp decay on parsed evidence date (floored)
    d = _parse_loose_date(point.recency)
    if d is None:
        rec_dates = [pd for pd in (_parse_loose_date(r.date) for r in recs) if pd]
        d = max(rec_dates) if rec_dates else None
    if d is None:
        recency, evidence_date = RECENCY_NEUTRAL, ""
    else:
        age = max((today - d).days, 0)
        recency = max(0.5 ** (age / HALFLIFE_DAYS), RECENCY_FLOOR)
        evidence_date = d.isoformat()

    value = _clamp(value_weights["importance"] * importance
                   + value_weights["reach"] * reach
                   + value_weights["recency"] * recency)

    # confidence ← independent sources (dominant) + model consensus (light)
    source_corroboration = _clamp(0.7 * min(distinct_domains / DOMAIN_CEIL, 1.0)
                                  + 0.3 * min(distinct_authors / AUTHOR_CEIL, 1.0))
    consensus_ratio = _parse_consensus(point.consensus)
    confidence = _clamp(
        CONF_FLOOR + (1 - CONF_FLOOR) * (CONF_SRC_WT * source_corroboration
                                         + CONF_CONSENSUS_WT * consensus_ratio),
        CONF_FLOOR, 1.0)

    composite = round(100 * value * confidence, 1)
    return ScoreBreakdown(
        composite=composite, value=round(value, 4), confidence=round(confidence, 4),
        importance=round(importance, 4), reach=round(reach, 4), recency=round(recency, 4),
        source_corroboration=round(source_corroboration, 4),
        consensus_ratio=round(consensus_ratio, 4),
        intensity=intensity, engagement_sum=eng_sum, distinct_authors=distinct_authors,
        distinct_domains=distinct_domains, evidence_date=evidence_date,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_scoring.py -q`
Expected: PASS (10 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/scoring.py tools/llm-council/tests/discovery/test_scoring.py
git commit -m "feat(discovery): research-grounded value×confidence opportunity score (PM4)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `bet.py` — proposed-bet heuristic (pure, isolated)

**Files:**
- Create: `council/discovery/bet.py`
- Test: `tests/discovery/test_bet.py`

**Interfaces:**
- Consumes: `CandidatePainPoint` (`title`, `summary`).
- Produces: `ProposedBet` dataclass (frozen) `shape, riskiest_assumption, cheapest_test`; `classify_pain_shape(point) -> str`; `propose_bet(point) -> ProposedBet`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/discovery/test_bet.py
from council.discovery.fusion import CandidatePainPoint
from council.discovery.bet import classify_pain_shape, propose_bet, ProposedBet


def _pt(title, summary=""):
    return CandidatePainPoint(title, summary, quotes=[], urls=[])


def test_each_shape_classified_by_keyword():
    assert classify_pain_shape(_pt("AI hallucinates fake APIs")) == "trust-gap"
    assert classify_pain_shape(_pt("Too expensive for solo devs")) == "cost-pain"
    assert classify_pain_shape(_pt("No Jira integration")) == "integration-gap"
    assert classify_pain_shape(_pt("Export is painfully slow and manual")) == "workflow-friction"
    assert classify_pain_shape(_pt("Wish it could generate diagrams")) == "missing-capability"


def test_priority_order_trust_beats_workflow():
    # contains both "slow" (workflow) and "wrong" (trust) -> trust wins (higher priority)
    assert classify_pain_shape(_pt("It's slow AND returns wrong answers")) == "trust-gap"


def test_propose_bet_returns_stable_populated_struct():
    bet = propose_bet(_pt("AI hallucinates fake APIs"))
    assert isinstance(bet, ProposedBet)
    assert bet.shape == "trust-gap"
    assert bet.riskiest_assumption and bet.cheapest_test
    # deterministic
    assert propose_bet(_pt("AI hallucinates fake APIs")) == bet


def test_default_fallback_is_missing_capability():
    bet = propose_bet(_pt("Something vague", "no matching keywords here"))
    assert bet.shape == "missing-capability"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_bet.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.bet'`

- [ ] **Step 3: Write the implementation**

```python
# council/discovery/bet.py
"""D1 — the 'proposed bet' card slot, $0 and non-fabricating.

Deterministically classifies a pain into one of five SHAPES by keyword, then emits the
matching riskiest-assumption CATEGORY + cheapest-test PATTERN. It names a structural
starting point (a real category, a test pattern) — never a fabricated specific insight.
Rendered under a 'heuristic — confirm against evidence' label with a human fill-in slot.
"""

from dataclasses import dataclass

from council.discovery.fusion import CandidatePainPoint


@dataclass(frozen=True)
class ProposedBet:
    shape: str
    riskiest_assumption: str
    cheapest_test: str


# first match wins — order = priority
_SHAPE_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("trust-gap", ("wrong", "hallucinat", "inaccurate", "unreliable", "trust", "error",
                   "made up", "made-up")),
    ("cost-pain", ("expensive", "pricing", "price", "cost", "afford", "too much", "paywall")),
    ("integration-gap", ("integrat", "api", "connect", "sync", "export", "import",
                         "compat", "plugin")),
    ("workflow-friction", ("slow", "tedious", "manual", "workaround", "friction",
                           "clunky", "too many steps")),
]

_SHAPE_BETS: dict[str, tuple[str, str]] = {
    "trust-gap": (
        "that users will trust an automated correctness check enough to rely on it",
        "5 user interviews — do they describe verification/accuracy as a top-3 pain?"),
    "cost-pain": (
        "that price, not value perception, is the actual blocker to adoption",
        "a pricing-page / willingness-to-pay test against the current workaround's cost"),
    "integration-gap": (
        "that the missing integration is the deal-breaker, not a nice-to-have",
        "count how many complaints name the same target tool before building a connector"),
    "workflow-friction": (
        "that users will switch from their current workaround for a smoother flow",
        "time-on-task comparison of the current workaround vs a clickable prototype"),
    "missing-capability": (
        "that the capability is genuinely absent, not just undiscovered in existing tools",
        "a 5-tool teardown — does any competitor already solve this before you build?"),
}


def classify_pain_shape(point: CandidatePainPoint) -> str:
    hay = f"{point.title} {point.summary}".lower()
    for shape, kws in _SHAPE_KEYWORDS:
        if any(k in hay for k in kws):
            return shape
    return "missing-capability"


def propose_bet(point: CandidatePainPoint) -> ProposedBet:
    shape = classify_pain_shape(point)
    risk, test = _SHAPE_BETS[shape]
    return ProposedBet(shape=shape, riskiest_assumption=risk, cheapest_test=test)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_bet.py -q`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/bet.py tools/llm-council/tests/discovery/test_bet.py
git commit -m "feat(discovery): deterministic proposed-bet heuristic (D1)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: redesign `IdeaCard` + `frame_pm`

**Files:**
- Modify: `council/discovery/frame.py`
- Test: `tests/discovery/test_frame.py`

**Interfaces:**
- Consumes: `score_opportunity` (Task 1), `propose_bet`/`ProposedBet` (Task 2), `ScoreBreakdown` (Task 1).
- Produces: `IdeaCard(title, who, pain, lead_quote, evidence_urls, quotes, score: ScoreBreakdown, why_now, bet: ProposedBet)`; `frame_pm(verified, fusion_result, bundle, *, today=None) -> tuple[list[IdeaCard], list[str]]`.

- [ ] **Step 1: Rewrite the test file**

```python
# tests/discovery/test_frame.py
from datetime import date

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame import frame_pm, IdeaCard
from council.discovery.scoring import ScoreBreakdown
from council.discovery.bet import ProposedBet

TODAY = date(2026, 6, 29)


def _vpp(title, intensity, urls, summary="summary", consensus="4/4 models"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment="PMs", recency="2026-06",
                            consensus=consensus)
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def _bundle(urls, engagement=50):
    b = EvidenceBundle()
    for i, u in enumerate(urls):
        b.add(EvidenceRecord("reddit", f"author{i}", u, "2026-06-20", f"q{i}", engagement=engagement))
    return b


def test_cards_sorted_by_composite_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3", "https://c.com/4", "https://d.com/5"])
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    bundle = _bundle(["https://a.com/1", "https://a.com/2", "https://b.com/3",
                      "https://c.com/4", "https://d.com/5"])
    cards, quote_bank = frame_pm([low, high, dropped], FusionResult(), bundle, today=TODAY)
    assert [c.title for c in cards] == ["High", "Low"]
    assert all(isinstance(c.score, ScoreBreakdown) and c.score.composite > 0 for c in cards)
    assert len(cards) == 2
    assert any("High quote" in q for q in quote_bank)


def test_card_leads_with_verbatim_quote_and_has_bet_and_why_now():
    bundle = _bundle(["https://a.com/1"])
    cards, _ = frame_pm([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(), bundle, today=TODAY)
    c = cards[0]
    assert c.lead_quote == "Slow export quote"     # leads with the verbatim quote
    assert "Slow export" in c.pain
    assert isinstance(c.bet, ProposedBet) and c.bet.shape == "workflow-friction"
    assert c.why_now                                # deterministic, non-empty
    assert c.who == "PMs"


def test_why_now_reflects_recency_state():
    bundle = _bundle(["https://a.com/1"])
    fresh = _vpp("Fresh", 3, ["https://a.com/1"])
    old = _vpp("Old", 3, ["https://a.com/1"])
    old.point.__dict__["recency"] = "2020-01"      # force an old date
    cf, _ = frame_pm([fresh], FusionResult(), bundle, today=TODAY)
    co, _ = frame_pm([old], FusionResult(), bundle, today=TODAY)
    assert "Fresh signal" in cf[0].why_now
    assert "Older signal" in co[0].why_now
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_frame.py -q`
Expected: FAIL — `frame_pm()` missing the `bundle` arg / `IdeaCard` has no `lead_quote`.

- [ ] **Step 3: Rewrite `frame.py`**

```python
# council/discovery/frame.py
"""Stage 4 (pm lens) — verified pain points → ranked PRD-grade opportunity cards + quote bank."""

from dataclasses import dataclass
from datetime import date

from council.discovery.bet import ProposedBet, propose_bet
from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import FusionResult
from council.discovery.scoring import ScoreBreakdown, score_opportunity
from council.discovery.verify import VerifiedPainPoint


@dataclass
class IdeaCard:
    title: str
    who: str
    pain: str               # the summary line (secondary to the quote)
    lead_quote: str         # pain in their words — the verbatim quote
    evidence_urls: list[str]
    quotes: list[str]
    score: ScoreBreakdown
    why_now: str
    bet: ProposedBet


def _why_now(score: ScoreBreakdown) -> str:
    if not score.evidence_date:
        return "Recency unknown — verify the pain is current."
    if score.recency >= 0.6:
        return f"Fresh signal — evidence dated {score.evidence_date}."
    return f"Older signal (evidence {score.evidence_date}); confirm it's still live."


def frame_pm(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
             bundle: EvidenceBundle, *, today: date | None = None) -> tuple[list[IdeaCard], list[str]]:
    today = today or date.today()
    cards: list[IdeaCard] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        score = score_opportunity(pt, v.supporting_urls, bundle, today=today)
        cards.append(IdeaCard(
            title=pt.title,
            who=pt.segment or "users",
            pain=f"{pt.title}: {pt.summary}",
            lead_quote=pt.quotes[0] if pt.quotes else "",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            score=score,
            why_now=_why_now(score),
            bet=propose_bet(pt),
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    cards.sort(key=lambda c: c.score.composite, reverse=True)
    return cards, quote_bank
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_frame.py -q`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/frame.py tools/llm-council/tests/discovery/test_frame.py
git commit -m "feat(discovery): PRD-grade IdeaCard + scored frame_pm (D1)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: new card layout in `render_ledger`

**Files:**
- Modify: `council/discovery/render.py` (the card loop, currently lines 20-27)
- Test: `tests/discovery/test_render.py`

**Interfaces:**
- Consumes: `IdeaCard` (Task 3) with `score: ScoreBreakdown`, `bet: ProposedBet`, `lead_quote`, `why_now`.
- Produces: unchanged `render_ledger(...)` signature; new per-card markdown.

- [ ] **Step 1: Update the test helpers + a card assertion**

Replace the `_cards()` helper and `test_render_includes_all_sections` in `tests/discovery/test_render.py` with:

```python
# top of file — update imports
from council.discovery.bet import ProposedBet
from council.discovery.scoring import ScoreBreakdown


def _score():
    return ScoreBreakdown(composite=68.0, value=0.83, confidence=0.82, importance=0.8,
                          reach=0.71, recency=0.84, source_corroboration=0.55,
                          consensus_ratio=1.0, intensity=4, engagement_sum=340,
                          distinct_authors=5, distinct_domains=2, evidence_date="2026-06")


def _cards():
    return [IdeaCard("Slow export", "PMs", "Slow export: it hangs", '"exports hang for minutes"',
                     ["https://a.com/1"], ['"slow"'], _score(),
                     "Fresh signal — evidence dated 2026-06",
                     ProposedBet("workflow-friction", "users won't switch", "time-on-task test"))]


def test_render_includes_all_sections():
    md = _render()
    assert "# Idea Ledger — pm tools" in md
    assert "Slow export" in md
    assert "score 68/100" in md
    assert '"exports hang for minutes"' in md          # leads with verbatim quote
    assert "**Size:**" in md and "importance 4/5" in md and "recency 0.84" in md
    assert "**Confidence:**" in md and "0.82" in md
    assert "**Why now:**" in md
    assert "Proposed bet" in md and "workflow-friction" in md and "Your call" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "no SSO talk" in md
    assert "Quote Bank" in md and "Contradiction" in md
    assert "$0.91" in md and "dropped by verification: 2" in md
```

(Note: the `IdeaCard(...)` positional order in `_cards()` must match the dataclass field order from Task 3: `title, who, pain, lead_quote, evidence_urls, quotes, score, why_now, bet`. The two `test_supplement_*` tests in this file keep working unchanged — they only exercise the supplement section, which is untouched.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_render.py -q`
Expected: FAIL — old `IdeaCard(...)` 8-arg positional call no longer matches; `score 68/100` not found.

- [ ] **Step 3: Replace the card loop in `render.py`**

Replace lines 20-27 (the `for i, c in enumerate(cards, 1):` block) with:

```python
    for i, c in enumerate(cards, 1):
        s = c.score
        L.append(f"### {i}. {c.title}  ·  score {s.composite:.0f}/100")
        L.append(f"- **Who:** {c.who}")
        L.append(f'- **Pain (their words):** {c.lead_quote}')
        L.append(f"  - {c.pain}")
        L.append("- **Evidence:** " + ", ".join(c.evidence_urls)
                 + f"  ·  {s.distinct_domains} independent domain(s)")
        L.append(f"- **Size:** importance {s.intensity}/5 · reach {s.reach:.2f} "
                 f"({s.engagement_sum} engagement, {s.distinct_authors} authors, "
                 f"{s.distinct_domains} domains) · recency {s.recency:.2f}")
        L.append(f"- **Confidence:** {s.confidence:.2f}× (sources {s.source_corroboration:.2f}, "
                 f"consensus {s.consensus_ratio:.2f})  →  value {s.value:.2f} × conf = {s.composite:.0f}/100")
        L.append(f"- **Why now:** {c.why_now}")
        L.append("- **Proposed bet** _(heuristic — confirm against evidence)_")
        L.append(f"  - Shape: {c.bet.shape}")
        L.append(f"  - Riskiest assumption: {c.bet.riskiest_assumption}")
        L.append(f"  - Cheapest test: {c.bet.cheapest_test}")
        L.append("  - _Your call: _________________________________")
        L.append("")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_render.py -q`
Expected: PASS (all tests in file)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/render.py tools/llm-council/tests/discovery/test_render.py
git commit -m "feat(discovery): PRD-grade card layout in render_ledger (D1)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: share the score in `frame_substack`

**Files:**
- Modify: `council/discovery/frame_substack.py`
- Test: `tests/discovery/test_frame_substack.py`

**Interfaces:**
- Consumes: `score_opportunity`, `ScoreBreakdown` (Task 1).
- Produces: `PostAngle` with `score: ScoreBreakdown` (field `corroboration` removed); `frame_substack(verified, fusion_result, bundle, *, segment="", today=None) -> tuple[list[PostAngle], list[str]]`.

- [ ] **Step 1: Update the test file**

In `tests/discovery/test_frame_substack.py`: add imports, a `_bundle` helper, thread `bundle`/`today`, and assert `ScoreBreakdown`:

```python
from datetime import date
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.scoring import ScoreBreakdown
# ... existing imports ...

TODAY = date(2026, 6, 29)

def _bundle(urls, engagement=50):
    b = EvidenceBundle()
    for i, u in enumerate(urls):
        b.add(EvidenceRecord("reddit", f"author{i}", u, "2026-06-20", f"q{i}", engagement=engagement))
    return b

def _vpp(title, intensity, urls, summary="it breaks", segment="PMs"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment=segment, recency="2026-06",
                            consensus="4/4 models")
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)
```

Then in each test, change the `frame_substack(...)` calls to pass the bundle + today, e.g.:

```python
def test_angles_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3", "https://c.com/4", "https://d.com/5"])
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    bundle = _bundle(["https://a.com/1", "https://a.com/2", "https://b.com/3",
                      "https://c.com/4", "https://d.com/5"])
    angles, quote_bank = frame_substack([low, high, dropped], FusionResult(), bundle, today=TODAY)
    assert [a.title for a in angles] == ["High", "Low"]
    assert all(isinstance(a, PostAngle) and isinstance(a.score, ScoreBreakdown)
               and a.score.composite > 0 for a in angles)
    assert len(angles) == 2
    assert any("High quote" in q for q in quote_bank)


def test_angle_fills_itch_transfer_and_audience_from_segment():
    bundle = _bundle(["https://a.com/1"])
    angles, _ = frame_substack([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(),
                               bundle, segment="solo founders", today=TODAY)
    a = angles[0]
    assert "Slow export" in a.itch
    assert a.transfer.lower().startswith("after reading")
    assert a.audience == "solo founders"
    assert a.hook


def test_whitespace_comes_from_blind_spots():
    fr = FusionResult(blind_spots=["nobody covers recovery UX", "no mobile angle"])
    bundle = _bundle(["https://a.com/1"])
    angles, _ = frame_substack([_vpp("Data loss", 5, ["https://a.com/1"])], fr, bundle, today=TODAY)
    assert "recovery UX" in angles[0].whitespace
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_frame_substack.py -q`
Expected: FAIL — `frame_substack()` missing `bundle`; `PostAngle` still has `corroboration`.

- [ ] **Step 3: Edit `frame_substack.py`**

Change the `PostAngle` dataclass: replace `score: float` with `score: ScoreBreakdown` and **delete** the `corroboration: int` field. Update imports and the function:

```python
# imports — replace the urlparse import block with:
from datetime import date

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import FusionResult
from council.discovery.scoring import ScoreBreakdown, score_opportunity
from council.discovery.verify import VerifiedPainPoint
```

```python
# the dataclass — score field becomes ScoreBreakdown; remove corroboration + _domains()
@dataclass
class PostAngle:
    title: str
    audience: str
    hook: str
    itch: str
    transfer: str
    evidence_urls: list[str]
    quotes: list[str]
    whitespace: str
    score: ScoreBreakdown


def frame_substack(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
                   bundle: EvidenceBundle, *, segment: str = "",
                   today: date | None = None) -> tuple[list[PostAngle], list[str]]:
    today = today or date.today()
    angles: list[PostAngle] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    whitespace = "; ".join(fusion_result.blind_spots) if fusion_result.blind_spots else ""
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        score = score_opportunity(pt, v.supporting_urls, bundle, today=today)
        angles.append(PostAngle(
            title=pt.title,
            audience=segment or pt.segment or "readers",
            hook=pt.summary or pt.title,
            itch=f"{pt.title}: {pt.summary}".rstrip(": ").strip(),
            transfer=f"After reading, the reader can address '{pt.title}' themselves.",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            whitespace=whitespace,
            score=score,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    angles.sort(key=lambda a: a.score.composite, reverse=True)
    return angles, quote_bank
```

Delete the now-unused `_domains` helper and the `urlparse` import.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_frame_substack.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/frame_substack.py tools/llm-council/tests/discovery/test_frame_substack.py
git commit -m "feat(discovery): substack lens adopts shared opportunity score (PM4)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: update `render_substack` for the shared score

**Files:**
- Modify: `council/discovery/render_substack.py` (lines 23, 27, 65)
- Test: `tests/discovery/test_render_substack.py`

**Interfaces:**
- Consumes: `PostAngle` (Task 5) with `score: ScoreBreakdown` (no `corroboration`).
- Produces: unchanged signatures; reads `a.score.composite` / `a.score.distinct_domains`.

- [ ] **Step 1: Update the `_angle()` test helper**

In `tests/discovery/test_render_substack.py`, change `_angle()` to build a `ScoreBreakdown` and drop `corroboration`:

```python
from council.discovery.scoring import ScoreBreakdown
# ...
def _angle():
    return PostAngle(
        title="Slow export", audience="solo founders", hook="exports hang for minutes",
        itch="Slow export: exports hang for minutes",
        transfer="After reading, the reader can fix slow exports.",
        evidence_urls=["https://a.com/1"], quotes=["exports hang for minutes"],
        whitespace="nobody covers recovery UX",
        score=ScoreBreakdown(composite=72.0, value=0.8, confidence=0.9, importance=0.8,
                             reach=0.6, recency=0.7, source_corroboration=0.5,
                             consensus_ratio=1.0, intensity=4, engagement_sum=100,
                             distinct_authors=2, distinct_domains=1, evidence_date="2026-06"),
    )
```

Add to `test_ledger_includes_all_sections`:
```python
    assert "score 72/100" in md
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/discovery/test_render_substack.py -q`
Expected: FAIL — `PostAngle` no longer accepts `corroboration` / `score 72/100` not found.

- [ ] **Step 3: Edit `render_substack.py`**

- Line 23: `f"### {i}. {a.title}  ·  score {a.score:.1f}"` → `f"### {i}. {a.title}  ·  score {a.score.composite:.0f}/100"`
- Line 27: `f"- **Corroboration:** {a.corroboration} source domain(s)"` → `f"- **Corroboration:** {a.score.distinct_domains} source domain(s)"`
- Line 65 (in `render_substack_brief`): `f"## Angle {i}: {a.title}  ·  score {a.score:.1f}"` → `f"## Angle {i}: {a.title}  ·  score {a.score.composite:.0f}/100"`

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/discovery/test_render_substack.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/render_substack.py tools/llm-council/tests/discovery/test_render_substack.py
git commit -m "feat(discovery): render shared composite score in substack ledger (PM4)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: wire `bundle` + `today` through `pipeline.py`

**Files:**
- Modify: `council/discovery/pipeline.py` (imports + lines ~120 and ~127)
- Test: full suite (`tests/`)

**Interfaces:**
- Consumes: `frame_pm`/`frame_substack` new signatures (Tasks 3, 5).
- Produces: end-to-end wiring — no signature change to `run_discovery`.

- [ ] **Step 1: Edit `pipeline.py`**

Add the import near the top (with the other stdlib imports):
```python
from datetime import date
```

In `run_discovery`, just before the `if lens == "substack":` branch (currently line ~116, after `brief_md = ""`), add:
```python
        today = date.today()
```

Update the two frame calls:
- `angles, quote_bank = frame_substack(verified, fr, segment=segment)` → `angles, quote_bank = frame_substack(verified, fr, bundle, segment=segment, today=today)`
- `cards, quote_bank = frame_pm(verified, fr)` → `cards, quote_bank = frame_pm(verified, fr, bundle, today=today)`

- [ ] **Step 2: Run the discovery test suite**

Run: `uv run pytest tests/discovery -q`
Expected: PASS — every discovery test green (existing `test_pipeline.py` exercises `run_discovery` end-to-end and must still pass).

- [ ] **Step 3: Run the FULL council suite**

Run: `uv run pytest tests/ -q`
Expected: PASS (all prior tests + the new scoring/bet tests; was 178 passed / 1 skipped before this work + new tests).

- [ ] **Step 4: Run the repo validator**

Run (from repo root `/Users/seanwinslow/Code-Brain/code-brain`): `python3 scripts/validate.py`
Expected: validation passes.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/pipeline.py
git commit -m "feat(discovery): thread evidence bundle + today into FRAME scoring (PM4/D1)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: docs — SKILL.md, CHANGELOG, tickets

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§2 FRAME description, §6 "what to surface")
- Modify: `CHANGELOG.md` (`[Unreleased]`)
- Modify: `vault/00_inbox/tickets.md`

- [ ] **Step 1: Update SKILL.md §2 FRAME + §6**

In the §2 FRAME stage description, note that PM-lens cards now carry a research-grounded `value × confidence` composite score (0–100) with an honest component breakdown, plus a heuristic "proposed bet" (riskiest assumption + cheapest test) the human confirms. In §6 ("what to surface"), note the bet is a labeled heuristic (not a fabricated insight) and the score breakdown is shown so the number is auditable. (Grep for the exact §2/§6 anchors: `grep -n "FRAME\|what to surface\|## " .claude/skills/fusion-discovery-council/SKILL.md`.)

- [ ] **Step 2: Add the CHANGELOG entry**

At the top of `## [Unreleased]` in `CHANGELOG.md`, add:
```markdown
### fusion-discovery-council — Step B: real opportunity score + PRD-grade card (PM4 + D1) (2026-06-29)
- **New `scoring.py`** — replaces the toy `intensity * (1 + domains)` with a research-grounded **`composite = 100 × value × confidence`** (RICE pattern). `value` = weighted importance/reach/recency; `confidence` = independent-source corroboration (dominant) + model consensus (light, separate) — so a single-source pain is discounted, never propped up by high importance. Reach is **log-damped** (Reddit "hot" precedent); recency is exp-decay, smallest weight, floored. Grounded in a deep-research pass ([vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md](vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md), 23 claims verified). Constants tunable + flagged for sensitivity-testing.
- **New `bet.py`** — deterministic pain-shape classifier (trust-gap / cost-pain / integration-gap / workflow-friction / missing-capability) → a labeled "proposed bet" (riskiest-assumption category + cheapest-test pattern) with a human fill-in slot. No fabricated insight.
- **PRD-grade card** — `IdeaCard` + `render_ledger` redesigned to who · pain-in-their-words (verbatim lead quote) · evidence + corroboration · size (auditable score components) · why-now (deterministic from recency) · proposed bet. Dropped the dead `workaround`/filler `opportunity` fields.
- **Substack lens** shares `score_opportunity` (DRY) — `PostAngle.score` is now the same `ScoreBreakdown`.
- Verification gate untouched; $0 new API spend (all signals from the in-memory bundle). Tests: new `test_scoring.py` + `test_bet.py`; updated frame/render tests. Full council suite green.
```

- [ ] **Step 3: Update tickets.md**

Mark Step B / PM4+D1 done on the roadmap ticket and note E3/D4/D2 remain in Step B. Append under the existing fusion-discovery roadmap bullet (do not create a duplicate top-level ticket).

- [ ] **Step 4: Re-run the validator**

Run (repo root): `python3 scripts/validate.py`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md vault/00_inbox/tickets.md docs/superpowers/specs/2026-06-29-discovery-pm4-d1-score-card-design.md vault/20_projects/research/2026-06-29-opportunity-scoring-frameworks-research.md
git commit -m "docs(discovery): PM4+D1 score+card — SKILL/CHANGELOG/tickets/research

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

(Vault paths `tickets.md` + the research note are staged per Sean's MBP exception — confirm with Sean before this commit. Never stage private-layer paths.)

---

## Self-Review (against the spec)

- **Spec coverage:** §1 scoring → Task 1; §2 bet → Task 2; §3 IdeaCard → Task 3; §4 render → Task 4; §5 substack → Tasks 5–6; §6 pipeline → Task 7; Docs → Task 8; Research grounding → captured in CHANGELOG + spec + vault note. ✓
- **Architecture match:** `composite = 100 × value × confidence` with confidence-as-multiplier is in Task 1's implementation and asserted by `test_single_source_is_discounted_even_with_full_consensus` + `test_sensitivity_sanity_corroborated_mid_beats_single_high`. ✓
- **Type consistency:** `ScoreBreakdown` field names used identically across Tasks 1/3/4/5/6; `frame_pm(verified, fr, bundle, *, today)` and `frame_substack(verified, fr, bundle, *, segment, today)` signatures consistent between definition (Tasks 3/5) and call site (Task 7); `ProposedBet(shape, riskiest_assumption, cheapest_test)` consistent Tasks 2/3/4. ✓
- **No placeholders:** every code step shows full code; every run step shows the command + expected result. ✓
- **Gate sacred / $0:** no task adds a network call; scoring reads only the in-memory bundle. ✓
