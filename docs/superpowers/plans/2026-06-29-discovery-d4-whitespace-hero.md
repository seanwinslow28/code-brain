# D4 — Whitespace Map as Hero Output — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the blind-spot/whitespace map to the lead of both discovery ledgers, rendering each gap with a uniform "backfill" next-action under a deterministic "Sharpen the next run" list.

**Architecture:** A new single-purpose module `council/discovery/whitespace.py` produces the hero markdown deterministically from run metadata ($0, no model call). Both `render.py` (pm) and `render_substack.py` (substack) call its one public helper at the top of the ledger (DRY). `pipeline.py` threads the already-normalized `segment` into both renderers.

**Tech Stack:** Python 3.11+, pytest, `uv`. Run everything from `tools/llm-council/`.

## Global Constraints

- Pure presentation change: **no new API, $0, no model call.** Deterministic from run metadata only.
- **Gate sacred:** the hero is never rendered as verified claims; no fabricated confidence/precision on gaps; per-gap action is always "investigate/backfill," never "build."
- **Scope guard — do NOT touch:** `backfill.py`, `verify_supplement.py`, `scoring.py`, `frame*.py`, the gate. `## Web Supplement (gap-fill)`, `## Contradiction Map`, `## Quote Bank`, `## Cost Summary` keep their content and relative order.
- Spec: `docs/superpowers/specs/2026-06-29-discovery-d4-whitespace-hero-design.md`.
- Hero heading is exactly: `## ⭐ Whitespace Map — what this run MISSED` (em dash, ⭐).
- Test command: `cd tools/llm-council && uv run pytest tests/discovery/<file> -q`. Full suite was **195 passed, 1 skipped** after PM4.
- Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **Never** `git add` any `vault/` path (Sean commits those separately).

---

### Task 1: `whitespace.py` — drop-rate + sharpen-action logic

**Files:**
- Create: `tools/llm-council/council/discovery/whitespace.py`
- Test: `tools/llm-council/tests/discovery/test_whitespace.py`

**Interfaces:**
- Produces: `_drop_rate(verified_count: int, dropped_count: int) -> float`; `_sharpen_actions(*, has_gaps: bool, n_gaps: int, tier: str, segment: str, verified_count: int, dropped_count: int) -> list[str]`

- [ ] **Step 1: Write the failing tests**

```python
# tools/llm-council/tests/discovery/test_whitespace.py
from council.discovery.whitespace import _drop_rate, _sharpen_actions


def test_drop_rate_zero_denominator():
    assert _drop_rate(0, 0) == 0.0


def test_drop_rate_fraction():
    assert _drop_rate(4, 8) == 8 / 12


def test_rule1_backfill_present_iff_gaps():
    a = _sharpen_actions(has_gaps=True, n_gaps=3, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert any("Backfill the 3 gaps below" in x for x in a)
    b = _sharpen_actions(has_gaps=False, n_gaps=0, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert not any("Backfill the" in x for x in b)


def test_rule1_singular_gap():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert any("Backfill the 1 gap below" in x for x in a)


def test_rule2_segment_present_iff_empty():
    empty = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="",
                             verified_count=5, dropped_count=1)
    assert any("--segment" in x for x in empty)
    setseg = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                              verified_count=5, dropped_count=1)
    assert not any("--segment" in x for x in setseg)


def test_rule3_no_verified():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=0, dropped_count=3)
    assert any("nothing survived verification" in x for x in a)


def test_rule4_fires_at_50pct_not_deep():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=4, dropped_count=8)   # 67%
    assert any("Raise tier to `deep`" in x and "67%" in x for x in a)


def test_rule4_silent_below_threshold():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=51, dropped_count=49)  # 49%
    assert not any("Raise tier" in x for x in a)


def test_rule4_silent_on_deep_tier():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="deep", segment="dev",
                         verified_count=1, dropped_count=9)   # 90% but already deep
    assert not any("Raise tier" in x for x in a)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'council.discovery.whitespace'`

- [ ] **Step 3: Write minimal implementation**

```python
# tools/llm-council/council/discovery/whitespace.py
"""D4 — the promoted '⭐ Whitespace Map' hero section, shared by both renderers.

Deterministic, $0, no model call. The whitespace map is by construction
absence-of-evidence (what the panel/evidence MISSED), so every gap's action is
"investigate/backfill" — never "build" — and no gap carries a fabricated score.
Spec: docs/superpowers/specs/2026-06-29-discovery-d4-whitespace-hero-design.md.
"""

_CAVEAT = (
    "> Gaps below = absence-of-evidence (what the panel and evidence did **not** surface), NOT "
    "verified claims or confirmed opportunities. The next move for each gap is to **investigate** "
    "it — never to build on it. Absence of a surfaced gap is not proof of full coverage."
)

_GAP_ACTION = ("   → Backfill (agent WebSearch/WebFetch, solution-side) — lands in "
               "**Web Supplement (gap-fill)** below.")


def _drop_rate(verified_count: int, dropped_count: int) -> float:
    denom = verified_count + dropped_count
    return (dropped_count / denom) if denom else 0.0


def _sharpen_actions(*, has_gaps: bool, n_gaps: int, tier: str, segment: str,
                     verified_count: int, dropped_count: int) -> list[str]:
    """Ordered 'Sharpen the next run' lines; each included only when its condition holds."""
    out: list[str] = []
    if has_gaps:
        out.append(f"Backfill the {n_gaps} gap{'s' if n_gaps != 1 else ''} below with the agent's "
                   "own WebSearch/WebFetch (solution-side) — do this first.")
    if not (segment or "").strip():
        out.append("Add `--segment <audience>` to focus the gather.")
    if verified_count == 0:
        out.append("Widen or reframe the topic — nothing survived verification.")
    rate = _drop_rate(verified_count, dropped_count)
    if tier != "deep" and rate >= 0.50:
        out.append(f"Raise tier to `deep` — thin verifiable signal (drop rate {round(rate * 100)}%).")
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py -q`
Expected: PASS (9 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/whitespace.py tools/llm-council/tests/discovery/test_whitespace.py
git commit -m "feat(discovery): D4 sharpen-action logic for whitespace hero

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `whitespace.py` — `whitespace_hero` assembler

**Files:**
- Modify: `tools/llm-council/council/discovery/whitespace.py`
- Test: `tools/llm-council/tests/discovery/test_whitespace.py`

**Interfaces:**
- Consumes: `_sharpen_actions`, `_CAVEAT`, `_GAP_ACTION` from Task 1.
- Produces: `whitespace_hero(*, blind_spots: list[str], tier: str, segment: str, verified_count: int, dropped_count: int) -> list[str]`

- [ ] **Step 1: Write the failing tests** (append to `test_whitespace.py`)

```python
from council.discovery.whitespace import whitespace_hero


def _hero(blind_spots, tier="standard", segment="dev", verified_count=5, dropped_count=1):
    return "\n".join(whitespace_hero(blind_spots=blind_spots, tier=tier, segment=segment,
                                     verified_count=verified_count, dropped_count=dropped_count))


def test_hero_heading_and_caveat_present():
    md = _hero(["no SSO talk"])
    assert "## ⭐ Whitespace Map — what this run MISSED" in md
    assert "absence-of-evidence" in md


def test_hero_per_gap_action_uniform_and_references_supplement():
    md = _hero(["no SSO talk", "no latency data"])
    assert "1. no SSO talk" in md and "2. no latency data" in md
    assert md.count("→ Backfill (agent WebSearch/WebFetch, solution-side)") == 2
    assert "Web Supplement (gap-fill)" in md


def test_hero_sharpen_list_renumbered_after_filtering():
    # segment set, verified>0, deep tier, low drop, gaps present → only rule 1 fires → "1."
    md = _hero(["g1"], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "**Sharpen the next run:**" in md
    assert "1. Backfill the 1 gap below" in md
    assert "2. " not in md.split("Gaps the panel")[0]  # no second sharpen item


def test_hero_no_sharpen_header_when_all_rules_silent():
    # gaps present(rule1 would fire) → force has_gaps but silence rule1? rule1 fires on gaps.
    # All-silent only possible with no gaps + segment set + verified>0 + low drop + deep tier:
    md = _hero([], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "**Sharpen the next run:**" not in md


def test_hero_empty_gaps_note():
    md = _hero([], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "No blind spots surfaced" in md
    assert "Backfill the" not in md


def test_hero_blank_gaps_filtered():
    md = _hero(["  ", "real gap"])
    assert "1. real gap" in md
    assert "2. " not in md.split("Gaps the panel")[1]  # only one real gap rendered
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py -q`
Expected: FAIL with `ImportError: cannot import name 'whitespace_hero'`

- [ ] **Step 3: Write minimal implementation** (append to `whitespace.py`)

```python
def whitespace_hero(*, blind_spots: list[str], tier: str, segment: str,
                    verified_count: int, dropped_count: int) -> list[str]:
    """Markdown lines for the promoted '## ⭐ Whitespace Map' hero section."""
    gaps = [g.strip() for g in (blind_spots or []) if g and g.strip()]
    L: list[str] = ["## ⭐ Whitespace Map — what this run MISSED\n"]

    def _sharpen(has_gaps: bool) -> None:
        actions = _sharpen_actions(has_gaps=has_gaps, n_gaps=len(gaps), tier=tier, segment=segment,
                                   verified_count=verified_count, dropped_count=dropped_count)
        if actions:
            L.append("**Sharpen the next run:**")
            L.extend(f"{i}. {a}" for i, a in enumerate(actions, 1))
            L.append("")

    if not gaps:
        L.append("_No blind spots surfaced — this run looks well-covered. (Absence of surfaced "
                 "gaps is not proof of full coverage.)_\n")
        _sharpen(has_gaps=False)
        return L

    L.append(_CAVEAT)
    L.append("")
    _sharpen(has_gaps=True)
    L.append("**Gaps the panel/evidence missed:**")
    for i, g in enumerate(gaps, 1):
        L.append(f"{i}. {g}")
        L.append(_GAP_ACTION)
    L.append("")
    return L
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_whitespace.py -q`
Expected: PASS (15 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/whitespace.py tools/llm-council/tests/discovery/test_whitespace.py
git commit -m "feat(discovery): D4 whitespace_hero assembler

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Wire hero into `render.py` (pm lens)

**Files:**
- Modify: `tools/llm-council/council/discovery/render.py`
- Test: `tools/llm-council/tests/discovery/test_render.py`

**Interfaces:**
- Consumes: `whitespace_hero` (Task 2).
- Produces: `render_ledger(...)` gains `segment: str = ""`; hero leads the ledger; old `## Blind-spot / Whitespace Map` block removed.

- [ ] **Step 1: Update the failing tests** in `test_render.py`

In `test_render_includes_all_sections`, replace the line:
```python
    assert "Blind-spot" in md and "no SSO talk" in md
```
with:
```python
    assert "## ⭐ Whitespace Map — what this run MISSED" in md and "no SSO talk" in md
    assert "## Blind-spot / Whitespace Map" not in md          # old buried heading removed
    assert md.index("⭐ Whitespace Map") < md.index("## Ranked Opportunities")  # hero leads
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py::test_render_includes_all_sections -q`
Expected: FAIL (no `⭐ Whitespace Map` heading yet)

- [ ] **Step 3: Edit `render.py`**

Add import near the top (with the other `from council.discovery...` imports):
```python
from council.discovery.whitespace import whitespace_hero
```

Change the signature of `render_ledger` to add `segment: str = ""` (place it after `lens: str`):
```python
def render_ledger(*, topic: str, lens: str, tier: str, segment: str = "", cards: list[IdeaCard],
                  quote_bank: list[str], fusion_result: FusionResult,
                  cost_usd: float, dropped_count: int,
                  supplement: "BackfillResult | None" = None) -> str:
```

Immediately after the two header `L.append(...)` lines (the `**Cost:**` line) and before `L.append("## Ranked Opportunities\n")`, insert:
```python
    L.extend(whitespace_hero(blind_spots=fusion_result.blind_spots, tier=tier, segment=segment,
                             verified_count=len(cards), dropped_count=dropped_count))
```

Delete this old block (currently between the ranked-cards loop and `supplement_section`):
```python
    L.append("## Blind-spot / Whitespace Map\n")
    L.extend(f"- {b}" for b in (fusion_result.blind_spots or ["_(none surfaced)_"]))
    L.append("")
```

- [ ] **Step 4: Run the render tests**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py -q`
Expected: PASS (the byte-identical and supplement tests still hold — `supplement` param unchanged; supplement still precedes Contradiction Map).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/render.py tools/llm-council/tests/discovery/test_render.py
git commit -m "feat(discovery): D4 promote whitespace hero in pm ledger

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Wire hero into `render_substack.py` (substack lens)

**Files:**
- Modify: `tools/llm-council/council/discovery/render_substack.py`
- Test: `tools/llm-council/tests/discovery/test_render_substack.py`

**Interfaces:**
- Consumes: `whitespace_hero` (Task 2).
- Produces: `render_substack_ledger(...)` gains `segment: str = ""`; hero leads the ledger; old `## Blind-spot / Whitespace Map` block removed. `render_substack_brief` untouched.

- [ ] **Step 1: Add/extend the failing test** in `test_render_substack.py`

Add to the existing "all sections" test (or create `test_substack_hero_leads`):
```python
    assert "## ⭐ Whitespace Map — what this run MISSED" in md
    assert "## Blind-spot / Whitespace Map" not in md
    assert md.index("⭐ Whitespace Map") < md.index("## Ranked Post Angles")
```
(Use the file's existing render helper / fixture for `md`.)

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render_substack.py -q`
Expected: FAIL (no hero heading yet)

- [ ] **Step 3: Edit `render_substack.py`**

Add import:
```python
from council.discovery.whitespace import whitespace_hero
```

Change `render_substack_ledger` signature to add `segment: str = ""` (after `tier: str`):
```python
def render_substack_ledger(*, topic: str, tier: str, segment: str = "", angles: list[PostAngle],
                           quote_bank: list[str], fusion_result: FusionResult,
                           cost_usd: float, dropped_count: int,
                           supplement: "BackfillResult | None" = None) -> str:
```

After the two header `L.append(...)` lines and before `L.append("## Ranked Post Angles\n")`, insert:
```python
    L.extend(whitespace_hero(blind_spots=fusion_result.blind_spots, tier=tier, segment=segment,
                             verified_count=len(angles), dropped_count=dropped_count))
```

Delete the old block:
```python
    L.append("## Blind-spot / Whitespace Map\n")
    L.extend(f"- {b}" for b in (fusion_result.blind_spots or ["_(none surfaced)_"]))
    L.append("")
```

- [ ] **Step 4: Run the substack render tests**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render_substack.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/render_substack.py tools/llm-council/tests/discovery/test_render_substack.py
git commit -m "feat(discovery): D4 promote whitespace hero in substack ledger

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Thread `segment` through `pipeline.py`

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py`

**Interfaces:**
- Consumes: `render_ledger(segment=...)`, `render_substack_ledger(segment=...)` (Tasks 3-4).

- [ ] **Step 1: Check existing pipeline tests for the old heading**

Run: `cd tools/llm-council && grep -n "Blind-spot" tests/discovery/test_pipeline.py`
If any test asserts on `## Blind-spot / Whitespace Map`, update it to `## ⭐ Whitespace Map`. (Likely none — pipeline tests assert on counts/cost.)

- [ ] **Step 2: Edit `pipeline.py`** — pass `segment` to both render calls

In the substack branch:
```python
            md = render_substack_ledger(topic=topic, tier=tier, segment=segment, angles=angles,
                                        quote_bank=quote_bank, fusion_result=fr, cost_usd=cost,
                                        dropped_count=dropped, supplement=supplement_result)
```
In the pm branch:
```python
            md = render_ledger(topic=topic, lens=lens, tier=tier, segment=segment, cards=cards,
                               quote_bank=quote_bank, fusion_result=fr, cost_usd=cost,
                               dropped_count=dropped, supplement=supplement_result)
```
(The empty-bundle early-return `render_ledger` call near the top has no cards/segment context — leave it; `segment` defaults to `""`, and `verified_count=len([])==0` correctly triggers the empty-gaps + reframe note.)

- [ ] **Step 3: Run the pipeline tests**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -q`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add tools/llm-council/council/discovery/pipeline.py tools/llm-council/tests/discovery/test_pipeline.py
git commit -m "feat(discovery): D4 thread segment into ledger renderers

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Docs + full-suite verification

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update SKILL.md** — point the three references at the new hero heading:
  - §2 stage 5: change `It reads each ledger's `## Blind-spot / Whitespace Map`` → `` `## ⭐ Whitespace Map` `` and note it now **leads** the ledger with a "Sharpen the next run" action list + per-gap backfill actions.
  - §4.1 step 2: `Open each ledger and read its `## Blind-spot / Whitespace Map`` → `` `## ⭐ Whitespace Map` (now the lead section)``.
  - §6 reporting note: update "blind-spot / whitespace map" mention to note it now leads the ledger and each gap carries a recommended next action.

- [ ] **Step 2: Add CHANGELOG.md entry** under the current unreleased/dated section:

```markdown
- **fusion-discovery-council D4 — whitespace map as hero output.** The blind-spot/whitespace map now LEADS both ledgers (pm + substack) instead of rendering last as bare bullets. Each gap renders as a statement + a uniform "→ Backfill (agent WebSearch/WebFetch)" next-action, under a deterministic "Sharpen the next run" list (4 conditional rules: backfill gaps · add `--segment` · reframe if 0 verified · raise tier when drop-rate ≥50%). New `council/discovery/whitespace.py` (shared by both renderers, $0/deterministic). Honesty-preserving: gaps labeled absence-of-evidence, never verified claims; no fabricated gap scores. Grounded in deep-research (`vault/20_projects/research/2026-06-29-whitespace-gap-map-presentation-research.md`). Spec: `docs/superpowers/specs/2026-06-29-discovery-d4-whitespace-hero-design.md`.
```

- [ ] **Step 3: Run the full council suite**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: PASS — at least the prior **195 passed, 1 skipped** plus the new whitespace tests (≈210 passed, 1 skipped).

- [ ] **Step 4: Run repo validator**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: validation passes.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md
git commit -m "docs(discovery): D4 whitespace hero — SKILL.md + CHANGELOG

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:** hero block (Tasks 2-4), 4 sharpen rules + threshold (Task 1), per-gap uniform action (Task 2), empty-gaps path (Task 2), section reorder + old heading removal (Tasks 3-4), `segment` threading (Task 5), scope guard / no backfill changes (Global Constraints), docs (Task 6), full-suite + validator (Task 6). Research findings 3/4/5/6/7 map to the caveat + per-gap action + sharpen rules. All covered.

**Placeholder scan:** none — every code/edit step shows the actual code or the exact string substitution.

**Type consistency:** `whitespace_hero(*, blind_spots, tier, segment, verified_count, dropped_count) -> list[str]` is defined in Task 2 and consumed with identical kwargs in Tasks 3-4. `_drop_rate` / `_sharpen_actions` signatures match between Task 1 definition and Task 2 use. `render_ledger`/`render_substack_ledger` gain `segment: str = ""`, consumed with `segment=segment` in Task 5.
