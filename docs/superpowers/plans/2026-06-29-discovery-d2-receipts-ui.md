# D2 — Receipts UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a compact two-axis "receipts" line (corroboration tier + freshness badge) under each ranked card in both discovery ledgers, via a shared deterministic helper.

**Architecture:** A new `council/discovery/receipts.py` (modeled on `whitespace.py`) exposes `receipt_line(score)` and a one-time `receipts_legend()`. Both `render.py` and `render_substack.py` import and call them. No new logic, no model call, no gate change — the data already lives on `score: ScoreBreakdown`. The receipt uses qualitative words; the existing float-bearing `Size:`/`Confidence:` detail lines stay as the audit trail.

**Tech Stack:** Python 3.11 stdlib only; pytest; `uv` for running tests. Package: `tools/llm-council/council/discovery/`.

## Global Constraints

- **$0, deterministic, hermetic.** No model call, no network, no new dependency. Pure stdlib.
- **Reuse `scoring.py` constants** — import `RECENCY_FLOOR` and `ScoreBreakdown`; do NOT define a second recency-floor constant.
- **Honesty invariants (sacred):** receipt restates only gate+scoring facts; a 1-domain card reads `single-source` (no `✓`/checkmark, no float harder than `confidence`); `undated` is NEVER rendered `fresh`; corroboration ladder caps at `well-corroborated` (no higher tier).
- **Run from `tools/llm-council/`:** `uv run pytest tests/ -q` (baseline **233 passed, 1 skipped**). Repo-root validator: `python3 scripts/validate.py`.
- **Commit trailer:** end every commit message with `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **No vault changes** on this branch.

---

### Task 1: `receipts.py` shared helper (TDD)

**Files:**
- Create: `tools/llm-council/council/discovery/receipts.py`
- Test: `tools/llm-council/tests/discovery/test_receipts.py`

**Interfaces:**
- Consumes: `council.discovery.scoring.ScoreBreakdown` (fields: `distinct_domains: int`, `recency: float`, `evidence_date: str`), `council.discovery.scoring.RECENCY_FLOOR` (= 0.3).
- Produces:
  - `receipt_line(score: ScoreBreakdown) -> str` — one markdown line starting `🧾 `, e.g. `🧾 well-corroborated · 3 independent domains  ·  fresh · evidence 2026-06-20`.
  - `receipts_legend() -> str` — one markdown blockquote line (the one-time explainer).
  - Module constants: `CORROBORATED_AT = 2`, `WELL_CORROBORATED_AT = 3`, `FRESH_AT = 0.5`.

- [ ] **Step 1: Write the failing tests**

Create `tools/llm-council/tests/discovery/test_receipts.py`:

```python
from council.discovery.receipts import receipt_line, receipts_legend
from council.discovery.scoring import ScoreBreakdown


def _score(*, distinct_domains=3, recency=0.84, evidence_date="2026-06-20"):
    return ScoreBreakdown(
        composite=62.0, value=0.7, confidence=0.86, importance=0.8, reach=0.55,
        recency=recency, source_corroboration=0.7, consensus_ratio=1.0, intensity=4,
        engagement_sum=300, distinct_sources=5, distinct_domains=distinct_domains,
        evidence_date=evidence_date)


def test_well_corroborated_three_domains():
    assert "well-corroborated · 3 independent domains" in receipt_line(_score(distinct_domains=3))


def test_corroborated_two_domains():
    line = receipt_line(_score(distinct_domains=2))
    assert "corroborated · 2 independent domains" in line
    assert "well-corroborated" not in line and "single-source" not in line


def test_single_source_one_domain_is_singular():
    line = receipt_line(_score(distinct_domains=1))
    assert "single-source · 1 domain" in line
    assert "domains" not in line          # singular noun


def test_uncorroborated_zero_domains():
    assert "uncorroborated · 0 domains" in receipt_line(_score(distinct_domains=0))


def test_caps_at_well_corroborated_no_higher_tier():
    line = receipt_line(_score(distinct_domains=5))
    assert "well-corroborated · 5 independent domains" in line
    assert "very" not in line.lower()     # no invented higher tier


def test_fresh_badge_when_recency_high_and_dated():
    assert "fresh · evidence 2026-06-20" in receipt_line(_score(recency=0.84, evidence_date="2026-06-20"))


def test_recent_badge_between_floor_and_fresh():
    line = receipt_line(_score(recency=0.4, evidence_date="2026-05-20"))
    assert "recent · evidence 2026-05-20" in line
    assert "fresh" not in line


def test_aging_badge_at_floor():
    assert "aging · evidence 2026-04-01" in receipt_line(_score(recency=0.3, evidence_date="2026-04-01"))


def test_undated_never_reads_fresh_even_at_neutral_recency():
    # honesty trap: unparseable date -> scoring sets recency=0.5; must NOT badge 'fresh'
    line = receipt_line(_score(recency=0.5, evidence_date=""))
    assert "undated · no parseable evidence date" in line
    assert "fresh" not in line


def test_legend_explains_depth_not_verdict():
    leg = receipts_legend()
    assert "depth" in leg and "not a verdict" in leg
    assert "single-source" in leg and "well-corroborated" in leg
    assert "freshness signal" in leg.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_receipts.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.receipts'`.

- [ ] **Step 3: Write minimal implementation**

Create `tools/llm-council/council/discovery/receipts.py`:

```python
# council/discovery/receipts.py
"""D2 — the per-card 'receipts' line: an evidence-depth gradient shared by both renderers.

Deterministic, $0, no model call. Every ranked card already passed the anti-fabrication
gate, so a binary "verified" stamp is meaningless (citation-hallucination runs 11-57% even
when links resolve). The receipt shows the GRADIENT — how deeply corroborated, how fresh —
in WORDS, never a checkmark or a raw float (those stay in the Size:/Confidence: detail lines).

Tiers are grounded in prior art (journalism's two-source rule + the NATO Admiralty
credibility scale for corroboration; the existing scoring.py recency decay for freshness).
The ladder CAPS at 'well-corroborated' (3+ domains): research (arXiv 2501.01303) finds no
trust gain from 1->5 citations, so a higher tier would manufacture false precision.
Spec: docs/superpowers/specs/2026-06-29-discovery-d2-receipts-ui-design.md.
Research: vault/20_projects/research/2026-06-29-receipts-provenance-ui-research.md.
"""

from __future__ import annotations

from council.discovery.scoring import RECENCY_FLOOR, ScoreBreakdown

# --- tunable thresholds (sensitivity-flagged, like scoring.py) ---
CORROBORATED_AT = 2        # journalism two-source rule: 2 independent sources = corroborated
WELL_CORROBORATED_AT = 3   # Admiralty "multiple independent"; ladder CAPS here (no higher tier).
                           # Distinct from (consistent with) scoring.DOMAIN_CEIL=4 score saturation.
FRESH_AT = 0.5             # mirrors frame._why_now's "Fresh signal" cutoff & scoring.RECENCY_NEUTRAL


def _corroboration(distinct_domains: int) -> str:
    n = max(int(distinct_domains), 0)
    if n >= WELL_CORROBORATED_AT:
        label = "well-corroborated"
    elif n >= CORROBORATED_AT:
        label = "corroborated"
    elif n == 1:
        label = "single-source"
    else:
        label = "uncorroborated"
    noun = "domain" if n == 1 else "domains"
    qualifier = "independent " if n >= CORROBORATED_AT else ""
    return f"{label} · {n} {qualifier}{noun}"


def _freshness(recency: float, evidence_date: str) -> str:
    # date-present gate FIRST: unparseable dates get recency=0.5 in scoring, which would
    # otherwise falsely read as 'fresh'. 'undated' is never 'fresh'.
    if not (evidence_date or "").strip():
        return "undated · no parseable evidence date"
    if recency >= FRESH_AT:
        badge = "fresh"
    elif recency > RECENCY_FLOOR:
        badge = "recent"
    else:
        badge = "aging"
    return f"{badge} · evidence {evidence_date}"


def receipt_line(score: ScoreBreakdown) -> str:
    """One compact receipts line: corroboration tier + freshness badge. Deterministic, $0."""
    return f"🧾 {_corroboration(score.distinct_domains)}  ·  {_freshness(score.recency, score.evidence_date)}"


def receipts_legend() -> str:
    """One-time explainer (NOT per-card); a D4-_CAVEAT-style markdown blockquote line."""
    return (
        "> 🧾 **Receipts** show evidence *depth*, not a verdict — every ranked item already "
        "cleared the anti-fabrication gate. **Corroboration** = independent source domains "
        "backing the pain (two-source rule: 1 = single-source, 2 = corroborated, 3+ = "
        "well-corroborated). **Freshness** = how recent the evidence is — a freshness signal, "
        "**not** proof; old pain can still be real."
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_receipts.py -q`
Expected: PASS (10 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/receipts.py tools/llm-council/tests/discovery/test_receipts.py
git commit -m "feat(discovery): D2 receipts.py — corroboration tier + freshness badge helper

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Wire receipts into both renderers (TDD)

**Files:**
- Modify: `tools/llm-council/council/discovery/render.py` (imports; `render_ledger` ranked section)
- Modify: `tools/llm-council/council/discovery/render_substack.py` (imports; `render_substack_ledger` ranked section)
- Test: `tools/llm-council/tests/discovery/test_render.py` (extend)
- Test: `tools/llm-council/tests/discovery/test_render_substack.py` (extend)

**Interfaces:**
- Consumes: `receipt_line`, `receipts_legend` from Task 1.
- Produces: no new public API — both ledger renderers now emit the legend once (when ≥1 card/angle) and a `receipt_line` under each card/angle heading.

- [ ] **Step 1: Write the failing tests (PM renderer)**

Append to `tools/llm-council/tests/discovery/test_render.py` (helpers `_score`, `_cards`, `_fr`, `_render`, and imports `IdeaCard`, `ProposedBet`, `ScoreBreakdown`, `render_ledger` already exist at top of file):

```python
def test_render_includes_receipt_line_and_legend_once():
    md = _render()
    # _score() has distinct_domains=2, recency=0.84, evidence_date="2026-06"
    assert "🧾 corroborated · 2 independent domains" in md
    assert "fresh · evidence 2026-06" in md
    assert md.count("Receipts** show evidence") == 1          # legend once, not per-card
    assert "**Size:**" in md and "**Confidence:**" in md      # detail lines kept (augment, not replace)
    assert md.index("score 68/100") < md.index("🧾") < md.index("**Who:**")  # receipt under heading


def test_render_single_source_card_reads_single_source():
    score = ScoreBreakdown(composite=40.0, value=0.5, confidence=0.6, importance=0.6,
                           reach=0.4, recency=0.4, source_corroboration=0.3, consensus_ratio=0.5,
                           intensity=3, engagement_sum=50, distinct_sources=1, distinct_domains=1,
                           evidence_date="2026-05-20")
    card = IdeaCard("Niche bug", "devs", "Niche bug: x", '"x"', ["https://b.com/1"], ['"x"'],
                    score, "Older signal", ProposedBet("s", "a", "t"))
    md = render_ledger(topic="t", lens="pm", tier="standard", cards=[card], quote_bank=[],
                       fusion_result=_fr(), cost_usd=0.1, dropped_count=0)
    assert "🧾 single-source · 1 domain" in md
    assert "well-corroborated" not in md                       # not over-stated


def test_render_empty_cards_no_receipts_no_legend():
    md = render_ledger(topic="t", lens="pm", tier="standard", cards=[], quote_bank=[],
                       fusion_result=_fr(), cost_usd=0.1, dropped_count=3)
    assert "🧾" not in md
    assert "Receipts** show evidence" not in md
    assert "No pain points survived verification" in md
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py -q`
Expected: FAIL — `🧾` not found (renderer not yet wired).

- [ ] **Step 3: Implement (PM renderer)**

In `tools/llm-council/council/discovery/render.py`, add to the import block (after the `whitespace` import):

```python
from council.discovery.receipts import receipt_line, receipts_legend
```

Replace the ranked-section opener and the per-card heading line. Change:

```python
    L.append("## Ranked Opportunities\n")
    if not cards:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    for i, c in enumerate(cards, 1):
        s = c.score
        L.append(f"### {i}. {c.title}  ·  score {s.composite:.0f}/100")
        L.append(f"- **Who:** {c.who}")
```

to:

```python
    L.append("## Ranked Opportunities\n")
    if not cards:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    else:
        L.append(receipts_legend())
        L.append("")
    for i, c in enumerate(cards, 1):
        s = c.score
        L.append(f"### {i}. {c.title}  ·  score {s.composite:.0f}/100")
        L.append(receipt_line(s))
        L.append(f"- **Who:** {c.who}")
```

- [ ] **Step 4: Run to verify PM tests pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py -q`
Expected: PASS (all, including the 3 new + existing).

- [ ] **Step 5: Write the failing tests (substack renderer)**

Append to `tools/llm-council/tests/discovery/test_render_substack.py` (helper `_angle`, imports `PostAngle`, `FusionResult`, `render_substack_ledger`, `ScoreBreakdown` already at top):

```python
def _fr_sub():
    return FusionResult(blind_spots=["nobody covers recovery UX"], contradictions=["mobile vs desktop"])


def test_substack_ledger_includes_receipt_and_legend_once():
    # _angle() has distinct_domains=1, recency=0.7, evidence_date="2026-06"
    md = render_substack_ledger(topic="export tools", tier="standard", angles=[_angle()],
                                quote_bank=[], fusion_result=_fr_sub(), cost_usd=0.42, dropped_count=2)
    assert "🧾 single-source · 1 domain" in md                 # single-source reads honestly
    assert "fresh · evidence 2026-06" in md
    assert md.count("Receipts** show evidence") == 1           # legend once
    assert md.index("score 72/100") < md.index("🧾") < md.index("**Audience:**")


def test_substack_well_corroborated_aging_angle_maps_badge():
    angle = PostAngle(
        title="Recovery UX gap", audience="founders", hook="h", itch="i", transfer="t",
        evidence_urls=["https://a.com/1", "https://b.com/1", "https://c.com/1"], quotes=["q"],
        whitespace="w",
        score=ScoreBreakdown(composite=55.0, value=0.7, confidence=0.8, importance=0.7, reach=0.5,
                             recency=0.3, source_corroboration=0.7, consensus_ratio=1.0, intensity=4,
                             engagement_sum=120, distinct_sources=3, distinct_domains=3,
                             evidence_date="2026-04-10"))
    md = render_substack_ledger(topic="t", tier="standard", angles=[angle], quote_bank=[],
                                fusion_result=_fr_sub(), cost_usd=0.1, dropped_count=0)
    assert "🧾 well-corroborated · 3 independent domains" in md
    assert "aging · evidence 2026-04-10" in md


def test_substack_empty_angles_no_receipts_no_legend():
    md = render_substack_ledger(topic="t", tier="standard", angles=[], quote_bank=[],
                                fusion_result=_fr_sub(), cost_usd=0.1, dropped_count=2)
    assert "🧾" not in md
    assert "Receipts** show evidence" not in md
    assert "No pain points survived verification" in md
```

- [ ] **Step 6: Run to verify substack tests fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render_substack.py -q`
Expected: FAIL — `🧾` not found.

- [ ] **Step 7: Implement (substack renderer)**

In `tools/llm-council/council/discovery/render_substack.py`, add to the import block (after the `whitespace` import):

```python
from council.discovery.receipts import receipt_line, receipts_legend
```

Change:

```python
    L.append("## Ranked Post Angles\n")
    if not angles:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    for i, a in enumerate(angles, 1):
        L.append(f"### {i}. {a.title}  ·  score {a.score.composite:.0f}/100")
        L.append(f"- **Audience:** {a.audience}")
```

to:

```python
    L.append("## Ranked Post Angles\n")
    if not angles:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    else:
        L.append(receipts_legend())
        L.append("")
    for i, a in enumerate(angles, 1):
        L.append(f"### {i}. {a.title}  ·  score {a.score.composite:.0f}/100")
        L.append(receipt_line(a.score))
        L.append(f"- **Audience:** {a.audience}")
```

- [ ] **Step 8: Run the full suite + validator**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: PASS — baseline 233 + 10 (Task 1) + 6 (Task 2) new = **249 passed, 1 skipped** (count approximate; all green).
Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: validator passes.

- [ ] **Step 9: Commit**

```bash
git add tools/llm-council/council/discovery/render.py tools/llm-council/council/discovery/render_substack.py tools/llm-council/tests/discovery/test_render.py tools/llm-council/tests/discovery/test_render_substack.py
git commit -m "feat(discovery): D2 wire receipts line + one-time legend into both ledgers

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Docs — SKILL.md + CHANGELOG

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§4 FRAME / output description)
- Modify: `CHANGELOG.md` (new D2 entry)

**Interfaces:** none (documentation only).

- [ ] **Step 1: Update SKILL.md §4**

Open `.claude/skills/fusion-discovery-council/SKILL.md`, find the §4 FRAME / output section that describes the ranked card fields. Add a sentence describing the receipts line, e.g.:

```markdown
Each ranked card now carries a compact **receipts line** under its heading (🧾) — a
two-axis evidence-depth gradient: **corroboration** (independent source domains: 1 =
single-source, 2 = corroborated, 3+ = well-corroborated) and **freshness** (fresh / recent
/ aging, or undated). A one-time legend above the ranked list states that receipts show
evidence *depth*, not a verdict (every card already cleared the gate), and that freshness
is a recency signal, not proof. Deterministic, $0; the precise floats stay in the Size:/
Confidence: detail lines.
```

(Match the exact heading/wording style of the surrounding §4 prose.)

- [ ] **Step 2: Update CHANGELOG.md**

Add an entry under the current/unreleased section of `CHANGELOG.md`:

```markdown
- **fusion-discovery-council D2 — receipts UI:** each ranked card in both ledgers (PM +
  substack) now shows a compact `🧾` receipts line — corroboration tier (off distinct
  independent domains; journalism two-source rule, caps at well-corroborated) + freshness
  badge (off the existing scoring recency decay; undated-never-fresh honesty gate) — plus a
  one-time legend framing receipts as evidence *depth*, not a verdict. New shared
  `council/discovery/receipts.py`; $0, deterministic, render-layer only. Closes Step B.
```

- [ ] **Step 3: Validate + commit**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: validator passes.

```bash
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md
git commit -m "docs(discovery): D2 receipts line in SKILL.md §4 + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:**
- `receipts.py` + `receipt_line` + `receipts_legend` → Task 1. ✓
- Corroboration ladder (1/2/3+, caps) → Task 1 `_corroboration` + tests. ✓
- Freshness badges + undated-first honesty gate → Task 1 `_freshness` + tests. ✓
- Reuse `RECENCY_FLOOR`, no parallel constant → Task 1 import. ✓
- Wire both renderers, legend once, receipt under heading, augment-not-replace → Task 2. ✓
- Empty/zero path no crash → Task 2 empty tests (PM + substack). ✓
- Honesty invariants (single-source reads honestly; no checkmark; caps) → Task 1 + Task 2 tests. ✓
- SKILL.md §4 + CHANGELOG → Task 3. ✓
- Full suite + validator → Task 2 Step 8, Task 3 Step 3. ✓

**Placeholder scan:** none — every step has concrete code/commands. ✓

**Type consistency:** `receipt_line(score: ScoreBreakdown) -> str` and `receipts_legend() -> str` used identically in Tasks 1 & 2; constant names `CORROBORATED_AT`/`WELL_CORROBORATED_AT`/`FRESH_AT` consistent; `ScoreBreakdown` field names (`distinct_domains`, `recency`, `evidence_date`) match `scoring.py`. ✓

**Out of scope:** `render_substack_brief` unchanged; consensus chip rejected; E3 `rank_gaps` precompute optional/skipped.
