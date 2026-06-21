# fusion-discovery-council — Phase 5 (Substack Lens + Segment Qualifier) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `--lens substack` framing (verified pain points → ranked post angles + a `substack-value-engine`-consumable handoff brief) and the `--segment` qualifier (reshape gather queries toward a target audience), without touching FUSE/VERIFY or the fabrication gate.

**Architecture:** Additive Stage-4 work + a gather-query qualifier on the existing `tools/llm-council/council/discovery/` subpackage. The `substack` lens reframes the **same verified pain points** that `frame_pm` consumes — no new Fusion call, so it ships on today's 2–3 live GATHER sources at the same per-run cost as `pm`. A new `frame_substack.py` produces `PostAngle`s (hook + candidate Value-Gate Itch + Transfer + verbatim evidence); a new `render_substack.py` renders both the post-angle idea ledger and the handoff brief; `pipeline.run_discovery` branches on `lens`; the CLI writes the brief to a sibling path. `--segment` threads a free-text audience qualifier through `run_discovery → gather_evidence → collectors`, shaping each collector's query (default `""` = today's behavior, so every existing test stays green).

**Tech Stack:** Python ≥3.10, `httpx` (async), `click`, `rich`, `pytest` + `pytest-asyncio` + `pytest-httpx`. Source-of-truth docs: the [spec](2026-06-20-fusion-discovery-council-design.md) (§4 `--lens`/`--segment`, §5 substack lens, §9 output), the [Phase 3 field report](../../../tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase3-field-report.md) §7d, and the [`substack-value-engine` SKILL.md](../../../.claude/skills/substack-value-engine/SKILL.md) (the brief's consumer — Value Gate: Itch / Solution / Transfer).

## Global Constraints

- Python floor stays `>=3.10`. Co-located subpackage; **reuse the council spine (`client.py`, `budget.py`)** — do **not** add a second HTTP client or a second spend file.
- **Run all commands from `tools/llm-council/`.** The test command is **`uv run --extra dev python -m pytest -v`** — plain `uv run pytest` does NOT work (pytest lives in the `dev` extra). Baseline **with Phase 4 landed: 114 passed, 1 skipped** (Phase 4 added +21 tests; field report `2026-06-21-fusion-discovery-council-phase4-field-report.md`); every task must keep the full suite green (no regressions) on top of its new tests.
- **The fabrication gate (`verify.py`) is SACRED — never weaken it.** The substack lens consumes the **already-verified** pain points (post-VERIFY); it must never re-introduce ungrounded claims. Every quote/URL in the brief comes from a `VerifiedPainPoint.supporting_urls`.
- The skill **never** `git add`s the `vault/` directory (CLAUDE.md rule 8 — Obsidian-Git owns vault commits). The CLI **writes** the ledger + brief and stops there.
- Verified OpenRouter model IDs (live 2026-06-20): `~google/gemini-pro-latest` (tilde = floating alias; bare form 400s), `mistralai/mistral-medium-3-5` (hyphen; dotted form 400s), plus `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, all Sonar variants. (Phase 5 changes no model IDs.)
- Caps unchanged: per-run quick **$0.50** / standard **$1.50** / deep **$4.00**; discovery daily **$10** / monthly **$50** (tagged `tool="discovery"`), isolated from council's $7/$40. The substack lens is the same FUSE cost as `pm` (no new model call), so caps need no change.
- **Cost-integrity theme: never bill a provider and record $0.** Phase 5 adds no billable call (`--segment` only changes query strings; the lens only reframes existing FusionResult output).
- No new skill/agent/script **file** is created (the lens + flag live inside the existing CLI/skill), so **no CLAUDE.md/README count-table change is required** — only a CHANGELOG entry, a SKILL.md surface update, and one descriptive CLAUDE.md line tweak (Task 6).

---

## Grounding note: PHASE 4 HAS LANDED (2026-06-21) — apply the deltas below

This plan was originally drafted against pre-Phase-4 `main`. **Phase 4 is now complete** (branch `feat/fusion-discovery-council-phase4`, 114 passed/1 skipped, both tiers live-confirmed under cap; field report `tools/llm-council/council/docs/2026-06-21-fusion-discovery-council-phase4-field-report.md`). Execute Phase 5 on top of Phase 4 (it draws on the wider evidence surface). The Phase-4-landed-first notes throughout this plan are therefore **IN FORCE, not optional** — the primary code in Task 5 now reflects all six collectors.

**What Phase 4 changed that Phase 5 must account for:**
- GATHER now runs **last30 + sonar + web + reviews + github + qa** (tier-gated: quick = last30+sonar+web; standard adds reviews+github; deep adds qa). `--segment` (Task 5) must thread through **all six** collectors, not three — the substack lens benefits from the wider bundle.
- `collect_sonar` already has a `fetch=None` param (Phase 4 Task 6) and the orchestrator passes `fetch=_simple_fetch` — **keep both** when adding `segment`. `sonar.py` now imports only `extract_quotes` from `web.py` (Phase 4 final-review M1 dropped the dead `_simple_fetch` import) — do **not** re-add it.
- The substack lens itself (Tasks 1–4) is fully independent of which collectors exist — it operates on post-VERIFY pain points, so those tasks apply verbatim.

> **Known-degraded, carried from Phase 4 (don't be surprised live):** `last30` still yields **0 records** (upstream `INCLUDE_SOURCES=null` crash; degrades safely). The review collector **under-yields (~3 records)** because Brave collapses the OR'd multi-`site:` query — correctness is fine, it's yield-tuning only (ticket M2, LOW). Neither blocks Phase 5; the live substack run draws on Sonar + web + reviews + github + qa.

---

## Background: what the brief must contain (read before Task 1)

The handoff brief is consumed by the [`substack-value-engine`](../../../.claude/skills/substack-value-engine/SKILL.md) skill, whose core primitive is the **Value Gate** — three slots that must all be filled or the piece is BLOCKED:

1. **Itch** — the specific, real, *first-person* problem the author actually had (checkable: a named tool, a dated incident, a real cost).
2. **Solution** — what the author actually did about it (a run, eval, number, commit, failed attempt).
3. **Transfer** — one sentence: "After reading, the reader can ___."

Discovery mines **other users'** pain from evidence. It can honestly pre-fill a **candidate Itch** (the real, checkable user pain) and a **candidate Transfer** (the capability a post would hand the reader), plus the **verbatim evidence** that proves the pain is real. It **must not** fabricate the first-person Itch or the Solution — those stay for Sean to fill, and `substack-value-engine` runs the gate. The brief therefore *scaffolds* the gate; it does not pass it. Chain it feeds: `substack-value-engine → storytelling-architecture → writing-voice-modes → writing-critique → writing-humanity-pass`.

---

## File Structure (touched in this plan)

```
tools/llm-council/council/discovery/frame_substack.py    # CREATE: PostAngle + frame_substack (Task 1)
tools/llm-council/council/discovery/render_substack.py   # CREATE: render_substack_ledger + render_substack_brief (Task 2)
tools/llm-council/council/discovery/pipeline.py          # MODIFY: lens branch + DiscoveryResult.brief_markdown + segment param (Tasks 3, 5)
tools/llm-council/council/discovery/__main__.py          # MODIFY: write brief on substack lens + --segment flag (Tasks 4, 5)
tools/llm-council/council/discovery/gather/__init__.py   # MODIFY: thread segment into collectors (Task 5)
tools/llm-council/council/discovery/gather/web.py        # MODIFY: segment in query (Task 5)
tools/llm-council/council/discovery/gather/sonar.py      # MODIFY: segment in prompt (Task 5)
tools/llm-council/council/discovery/gather/last30.py     # MODIFY: segment composed into subject (Task 5)
.claude/skills/fusion-discovery-council/SKILL.md         # MODIFY: substack lens + --segment ship (Task 6)
CHANGELOG.md                                             # MODIFY: Phase 5 entry (Task 6)
CLAUDE.md                                                # MODIFY: one descriptive line (Task 6)
tools/llm-council/tests/discovery/*                      # new + updated tests per task
```

**Sequencing note (file overlap):** `pipeline.py` is touched by Task 3 (lens branch + `segment` param on `run_discovery`) and Task 5 (passing `segment` into the gather call); `__main__.py` by Task 4 (brief write) and Task 5 (`--segment` flag). Run tasks **sequentially** in order. Tasks 1–4 deliver the substack lens; Task 5 adds `--segment`; Task 6 reconciles docs + verifies.

---

## Task 1: `PostAngle` + `frame_substack`

**Files:**
- Create: `tools/llm-council/council/discovery/frame_substack.py`
- Test: `tools/llm-council/tests/discovery/test_frame_substack.py` (new)

**Interfaces:**
- Produces: `@dataclass PostAngle(title, audience, hook, itch, transfer, evidence_urls, quotes, whitespace, score, corroboration)` and `frame_substack(verified: list[VerifiedPainPoint], fusion_result: FusionResult, segment: str = "") -> tuple[list[PostAngle], list[str]]` (ranked angles + quote bank). Mirrors `frame_pm`'s scoring (`intensity × (1 + corroboration-domains)`) and quote-bank dedup exactly, so behavior is consistent across lenses.

**Context:** Spec §4/§5 — the substack lens reframes each *verified* pain point into a post angle. `frame_substack` consumes the same `VerifiedPainPoint` list `frame_pm` does (post-VERIFY), so no new Fusion call. It pre-fills the Value-Gate **candidate Itch** and **candidate Transfer** + the **whitespace** differentiation (from the blind-spot map), and never invents the first-person itch or the solution.

- [ ] **Step 1: Write the failing tests**

Create `tests/discovery/test_frame_substack.py`:

```python
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame_substack import frame_substack, PostAngle


def _vpp(title, intensity, urls, summary="it breaks", segment="PMs"):
    pt = CandidatePainPoint(title, summary, quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment=segment)
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def test_angles_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3"])   # 2 domains → higher corroboration
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    angles, quote_bank = frame_substack([low, high, dropped], FusionResult())
    assert [a.title for a in angles] == ["High", "Low"]
    assert all(isinstance(a, PostAngle) and a.score > 0 for a in angles)
    assert len(angles) == 2                       # unverified excluded
    assert any("High quote" in q for q in quote_bank)


def test_angle_fills_itch_transfer_and_audience_from_segment():
    angles, _ = frame_substack([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult(),
                               segment="solo founders")
    a = angles[0]
    assert "Slow export" in a.itch
    assert a.transfer.lower().startswith("after reading")
    assert a.audience == "solo founders"          # CLI segment overrides the per-pain segment
    assert a.hook                                  # an open-loop hook is present


def test_whitespace_comes_from_blind_spots():
    fr = FusionResult(blind_spots=["nobody covers recovery UX", "no mobile angle"])
    angles, _ = frame_substack([_vpp("Data loss", 5, ["https://a.com/1"])], fr)
    assert "recovery UX" in angles[0].whitespace
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_frame_substack.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.frame_substack'`.

- [ ] **Step 3: Implement**

Create `council/discovery/frame_substack.py`:

```python
# council/discovery/frame_substack.py
"""Stage 4 (substack lens) — verified pain points → ranked post angles + a
substack-value-engine handoff brief.

A post angle reframes a *verified* user pain point (the same gate-survived points
frame_pm consumes — no new Fusion call) into the raw material the Substack writing
chain needs: a hook (open loop), a candidate Value-Gate Itch, a Transfer promise, the
whitespace differentiation, and the verbatim evidence that proves the pain is real. It
does NOT write prose and does NOT invent the author's first-person itch or solution —
those slots stay for substack-value-engine to gate.
"""

from dataclasses import dataclass
from urllib.parse import urlparse

from council.discovery.fusion import FusionResult
from council.discovery.verify import VerifiedPainPoint


@dataclass
class PostAngle:
    title: str               # working post title / angle
    audience: str            # who feels the pain (CLI --segment, else the per-pain segment)
    hook: str                # the open-loop / half-told problem
    itch: str                # candidate Value-Gate Itch (the real, checkable problem)
    transfer: str            # Value-Gate Transfer: "After reading, the reader can ___"
    evidence_urls: list[str]
    quotes: list[str]
    whitespace: str          # angle differentiation (from the blind-spot/whitespace map)
    score: float
    corroboration: int


def _domains(urls: list[str]) -> int:
    return len({urlparse(u).netloc for u in urls if u})


def frame_substack(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
                   segment: str = "") -> tuple[list[PostAngle], list[str]]:
    angles: list[PostAngle] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    whitespace = "; ".join(fusion_result.blind_spots) if fusion_result.blind_spots else ""
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        corr = _domains(v.supporting_urls)
        score = float(pt.intensity or 1) * (1 + corr)
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
            corroboration=corr,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    angles.sort(key=lambda a: a.score, reverse=True)
    return angles, quote_bank
```

- [ ] **Step 4: Run the frame tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_frame_substack.py -v`
Expected: PASS (3 tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/frame_substack.py tests/discovery/test_frame_substack.py
git commit -m "feat(discovery): frame_substack — verified pain points → ranked post angles"
```

---

## Task 2: `render_substack` (post-angle ledger + handoff brief)

**Files:**
- Create: `tools/llm-council/council/discovery/render_substack.py`
- Test: `tools/llm-council/tests/discovery/test_render_substack.py` (new)

**Interfaces:**
- Produces: `render_substack_ledger(*, topic, tier, angles, quote_bank, fusion_result, cost_usd, dropped_count) -> str` (the ranked post-angle idea ledger — mirrors `render_ledger`'s section set) and `render_substack_brief(*, topic, segment, angles) -> str` (the Value-Gate-scaffolded handoff brief consumed by `substack-value-engine`).

**Context:** Spec §9 — the substack lens writes **both** an idea ledger (ranked, lens-framed, with blind-spot/quote-bank/cost sections) **and** a handoff brief. The brief pre-fills Itch (slot 1) + Transfer (slot 3) + verbatim evidence and leaves Solution (slot 2) for Sean.

- [ ] **Step 1: Write the failing tests**

Create `tests/discovery/test_render_substack.py`:

```python
from council.discovery.frame_substack import PostAngle
from council.discovery.fusion import FusionResult
from council.discovery.render_substack import render_substack_ledger, render_substack_brief


def _angle():
    return PostAngle(
        title="Slow export", audience="solo founders", hook="exports hang for minutes",
        itch="Slow export: exports hang for minutes", transfer="After reading, the reader can fix slow exports.",
        evidence_urls=["https://a.com/1"], quotes=["exports hang for minutes"],
        whitespace="nobody covers recovery UX", score=8.0, corroboration=1,
    )


def test_ledger_includes_all_sections():
    fr = FusionResult(blind_spots=["nobody covers recovery UX"], contradictions=["mobile vs desktop"])
    md = render_substack_ledger(topic="export tools", tier="standard", angles=[_angle()],
                                quote_bank=['"exports hang for minutes" — https://a.com/1'],
                                fusion_result=fr, cost_usd=0.42, dropped_count=2)
    assert "# Substack Idea Ledger — export tools" in md
    assert "Slow export" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "recovery UX" in md
    assert "Quote Bank" in md
    assert "$0.42" in md and "dropped by verification: 2" in md


def test_brief_scaffolds_value_gate_and_keeps_evidence():
    md = render_substack_brief(topic="export tools", segment="solo founders", angles=[_angle()])
    assert "Substack Handoff Brief — export tools" in md
    assert "substack-value-engine" in md          # names the consumer + chain
    assert "Itch" in md and "Solution" in md and "Transfer" in md
    assert "solo founders" in md                   # target segment surfaced
    assert '"exports hang for minutes"' in md      # verbatim evidence carried into the brief
    assert "https://a.com/1" in md


def test_brief_handles_no_angles():
    md = render_substack_brief(topic="x", segment="", angles=[])
    assert "No verified pain points" in md
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_render_substack.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.render_substack'`.

- [ ] **Step 3: Implement**

Create `council/discovery/render_substack.py`:

```python
# council/discovery/render_substack.py
"""Render the substack-lens artifacts: a ranked post-angle idea ledger and a
substack-value-engine handoff brief."""

from council.discovery.frame_substack import PostAngle
from council.discovery.fusion import FusionResult


def render_substack_ledger(*, topic: str, tier: str, angles: list[PostAngle],
                           quote_bank: list[str], fusion_result: FusionResult,
                           cost_usd: float, dropped_count: int) -> str:
    L: list[str] = []
    L.append(f"# Substack Idea Ledger — {topic}\n")
    L.append(f"- **Lens:** `substack`  **Tier:** `{tier}`  **Post angles:** {len(angles)}")
    L.append(f"- **Cost:** ${cost_usd:.2f}  ·  Pain points dropped by verification: {dropped_count}\n")

    L.append("## Ranked Post Angles\n")
    if not angles:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    for i, a in enumerate(angles, 1):
        L.append(f"### {i}. {a.title}  ·  score {a.score:.1f}")
        L.append(f"- **Audience:** {a.audience}")
        L.append(f"- **Hook:** {a.hook}")
        L.append(f"- **Transfer:** {a.transfer}")
        L.append(f"- **Corroboration:** {a.corroboration} source domain(s)")
        L.append("- **Evidence:** " + ", ".join(a.evidence_urls))
        L.append("")

    L.append("## Blind-spot / Whitespace Map\n")
    L.extend(f"- {b}" for b in (fusion_result.blind_spots or ["_(none surfaced)_"]))
    L.append("")
    L.append("## Quote Bank\n")
    L.extend(f"- {q}" for q in (quote_bank or ["_(empty)_"]))
    L.append("")
    L.append("## Cost Summary\n")
    L.append(f"- Approx cost: ${cost_usd:.2f}")
    L.append(f"- Pain points dropped by verification: {dropped_count}")
    return "\n".join(L)


def render_substack_brief(*, topic: str, segment: str, angles: list[PostAngle]) -> str:
    """A handoff brief consumable by the substack-value-engine skill.

    Pre-fills the candidate Itch + Transfer (Value-Gate slots 1 & 3) and the verbatim
    evidence; leaves Solution (slot 2) for Sean — the gate BLOCKS until that is a real,
    first-person artifact. Chain: substack-value-engine → storytelling-architecture →
    writing-voice-modes → writing-critique → writing-humanity-pass.
    """
    L: list[str] = []
    L.append(f"# Substack Handoff Brief — {topic}\n")
    L.append("> Feed this into `substack-value-engine`. Each angle pre-fills the Value-Gate **Itch**")
    L.append("> and **Transfer** from real evidence; you supply the **Solution** (what you actually did).")
    L.append("> The gate BLOCKS any angle whose Itch isn't genuinely yours or whose Solution isn't a real")
    L.append("> artifact. Chain: substack-value-engine → storytelling-architecture → writing-voice-modes →")
    L.append("> writing-critique → writing-humanity-pass.\n")
    if segment:
        L.append(f"- **Target segment:** {segment}\n")
    if not angles:
        L.append("_No verified pain points — no angles to brief. Widen the topic or raise the tier._")
        return "\n".join(L)
    for i, a in enumerate(angles, 1):
        L.append(f"## Angle {i}: {a.title}  ·  score {a.score:.1f}")
        L.append(f"- **Audience:** {a.audience}")
        L.append(f"- **Hook (open loop):** {a.hook}")
        L.append(f"- **Itch (Value-Gate slot 1 — candidate, verify it's genuinely yours):** {a.itch}")
        L.append("- **Solution (slot 2 — you fill):** _What did you actually do? The gate blocks until this is a real run/eval/commit/number._")
        L.append(f"- **Transfer (slot 3 — candidate):** {a.transfer}")
        if a.whitespace:
            L.append(f"- **Whitespace / differentiation:** {a.whitespace}")
        L.append("- **Evidence (proof the pain is real):**")
        if a.quotes:
            for q, u in zip(a.quotes, a.evidence_urls + [""] * len(a.quotes)):
                L.append(f'  - "{q}"' + (f" — {u}" if u else ""))
        else:
            L.append("  - _(no verbatim quotes captured)_")
        L.append("")
    return "\n".join(L)
```

- [ ] **Step 4: Run the render tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_render_substack.py -v`
Expected: PASS (4 tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/render_substack.py tests/discovery/test_render_substack.py
git commit -m "feat(discovery): render substack post-angle ledger + value-gate handoff brief"
```

---

## Task 3: Pipeline lens branch + `DiscoveryResult.brief_markdown` + `segment` param

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py` (add)

**Interfaces:**
- Changed: `DiscoveryResult` gains `brief_markdown: str = ""` (last field, default — existing positional constructions stay valid). `run_discovery` gains a `segment: str = ""` keyword param (used by framing now; threaded into gather in Task 5). When `lens == "substack"`, it calls `frame_substack` + `render_substack_ledger` (primary markdown) + `render_substack_brief` (→ `brief_markdown`); otherwise `frame_pm` + `render_ledger` (unchanged). `verified_count` becomes the count of the lens's cards/angles.

**Context:** Today `run_discovery` always calls `frame_pm`/`render_ledger`, so `--lens substack` currently produces a `pm`-framed ledger. This task makes the lens real on the framing side. The empty-bundle and fuse-failure paths are unchanged (no angles to frame); the substack lens differs only on the success path.

- [ ] **Step 1: Write the failing test**

Add to `tests/discovery/test_pipeline.py`:

```python
@pytest.mark.asyncio
async def test_substack_lens_produces_angles_ledger_and_brief():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/x", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "notes vanish on conflict", ["exports fail silently"],
                               ["https://r.com/1"], intensity=5, segment="power users"),
        ], blind_spots=["nobody covers recovery UX"], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="substack", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert "Substack Idea Ledger" in res.markdown
    assert "Export loss" in res.markdown
    assert res.verified_count == 1
    assert res.brief_markdown                                   # the brief is produced
    assert "Itch" in res.brief_markdown
    assert "exports fail silently" in res.brief_markdown        # verbatim evidence carried into the brief


@pytest.mark.asyncio
async def test_pm_lens_produces_no_brief():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/x", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert "Idea Ledger — sync apps" in res.markdown
    assert res.brief_markdown == ""
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_pipeline.py::test_substack_lens_produces_angles_ledger_and_brief -v`
Expected: FAIL — the markdown is the `pm`-framed `# Idea Ledger — sync apps` (no `Substack Idea Ledger`) and `DiscoveryResult` has no `brief_markdown`.

- [ ] **Step 3: Implement the lens branch**

In `council/discovery/pipeline.py`, add `brief_markdown` to `DiscoveryResult`:

```python
@dataclass
class DiscoveryResult:
    markdown: str
    cost_usd: float
    verified_count: int
    dropped_count: int
    session: dict
    brief_markdown: str = ""
```

Add `segment: str = ""` to the `run_discovery` signature (place it after `api_key`):

```python
async def run_discovery(*, topic: str, lens: str, tier: str, api_key: str, segment: str = "",
                        gather_fn=None, fuse_fn=None, sessions_dir: Path | None = None) -> DiscoveryResult:
```

Replace the success-path framing/render block (from `verified = verify_pain_points(...)` down to the `render_ledger(...)` call) with a lens branch:

```python
    verified = verify_pain_points(fr.pain_points, bundle)
    dropped = sum(1 for v in verified if not v.verified)
    cost = _estimate_cost(fr, tcfg)

    brief_md = ""
    if lens == "substack":
        from council.discovery.frame_substack import frame_substack
        from council.discovery.render_substack import render_substack_ledger, render_substack_brief
        angles, quote_bank = frame_substack(verified, fr, segment=segment)
        md = render_substack_ledger(topic=topic, tier=tier, angles=angles, quote_bank=quote_bank,
                                    fusion_result=fr, cost_usd=cost, dropped_count=dropped)
        brief_md = render_substack_brief(topic=topic, segment=segment, angles=angles)
        verified_count = len(angles)
    else:
        cards, quote_bank = frame_pm(verified, fr)
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=cards, quote_bank=quote_bank,
                           fusion_result=fr, cost_usd=cost, dropped_count=dropped)
        verified_count = len(cards)
```

Update the `session` dict's `verified` field and the final return to use `verified_count` + carry `brief_md`:

```python
    session = {
        "id": session_id, "topic": topic, "lens": lens, "tier": tier,
        "evidence_count": len(bundle.records), "verified": verified_count,
        "dropped": dropped, "cost_usd": cost,
        "gather_status": gather_status,
        "blind_spots": fr.blind_spots, "contradictions": fr.contradictions,
    }
    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(session, indent=2))

    return DiscoveryResult(markdown=md, cost_usd=cost, verified_count=verified_count,
                           dropped_count=dropped, session=session, brief_markdown=brief_md)
```

> The existing `frame_pm` / `render_ledger` imports at the top of `pipeline.py` stay; the substack modules are imported lazily inside the branch to keep the `pm` path's import graph unchanged.

- [ ] **Step 4: Run the pipeline tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_pipeline.py -v`
Expected: PASS (existing pipeline tests — `test_pipeline_end_to_end_drops_unverified` still asserts `verified_count == 1` on the `pm` path — plus the 2 new lens tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/pipeline.py tests/discovery/test_pipeline.py
git commit -m "feat(discovery): pipeline substack-lens branch + brief_markdown + segment param"
```

---

## Task 4: CLI writes the handoff brief on the substack lens

**Files:**
- Modify: `tools/llm-council/council/discovery/__main__.py`
- Test: `tools/llm-council/tests/discovery/test_cli.py` (add)

**Interfaces:**
- Produces (new): `_brief_path(output: Path) -> Path` — the brief's sibling path. On `--lens substack`, after writing the ledger to `--output`, the CLI also writes `result.brief_markdown` to `_brief_path(output)` and echoes it. The `pm` lens writes no brief (`brief_markdown == ""`).

**Context:** Spec §9 — the substack lens "additionally writes a handoff brief." The ledger goes to the `--output` path (`...-substack-idea-ledger.md` per convention); the brief lands at the sibling `...-substack-brief.md`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_cli.py`:

```python
def test_cli_writes_substack_brief(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "2026-06-20-x-substack-idea-ledger.md"

    async def fake_run(**kw):
        return DiscoveryResult(markdown="# Substack Idea Ledger — x\n", cost_usd=0.4,
                               verified_count=1, dropped_count=0, session={"id": "s"},
                               brief_markdown="# Substack Handoff Brief — x\n- Itch: ...")
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "substack", "--tier", "quick", "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    brief = tmp_path / "2026-06-20-x-substack-brief.md"
    assert brief.exists()
    assert "Handoff Brief" in brief.read_text()
    assert "brief" in res.output.lower()


def test_cli_pm_lens_writes_no_brief(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "led.md"

    async def fake_run(**kw):
        return DiscoveryResult("# Idea Ledger — x\n", 0.4, 1, 0, {"id": "s"})  # brief_markdown="" default
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "pm", "--tier", "quick", "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert not (tmp_path / "led-brief.md").exists()
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_cli.py::test_cli_writes_substack_brief -v`
Expected: FAIL — no brief file is written (the CLI only writes `result.markdown`).

- [ ] **Step 3: Implement**

In `council/discovery/__main__.py`, add the helper above `main`:

```python
def _brief_path(output: Path) -> Path:
    """Sibling path for the substack handoff brief: drop a trailing '-idea-ledger', add '-brief'."""
    stem = output.stem
    if stem.endswith("-idea-ledger"):
        stem = stem[: -len("-idea-ledger")]
    return output.with_name(f"{stem}-brief{output.suffix}")
```

In `main`, replace the success-path write block:

```python
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.markdown)
    if not skip_budget_check:
        record_spend(amount=result.cost_usd, profile=tier, tag=f"discovery-{lens}",
                     on_date=date.today(), tool="discovery")
    console.print(f"[green]Idea ledger written:[/green] {output}")
    console.print(f"[dim]Verified ideas: {result.verified_count} · dropped: {result.dropped_count} · ${result.cost_usd:.2f}[/dim]")
```

with (adds the brief write for the substack lens):

```python
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.markdown)
    if lens == "substack" and result.brief_markdown:
        brief = _brief_path(output)
        brief.write_text(result.brief_markdown)
    if not skip_budget_check:
        record_spend(amount=result.cost_usd, profile=tier, tag=f"discovery-{lens}",
                     on_date=date.today(), tool="discovery")
    console.print(f"[green]Idea ledger written:[/green] {output}")
    if lens == "substack" and result.brief_markdown:
        console.print(f"[green]Substack handoff brief written:[/green] {_brief_path(output)}")
    console.print(f"[dim]Verified ideas: {result.verified_count} · dropped: {result.dropped_count} · ${result.cost_usd:.2f}[/dim]")
```

- [ ] **Step 4: Run the CLI tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_cli.py -v`
Expected: PASS (existing CLI tests — `test_cli_writes_ledger`, deep-confirm, failure-spend — plus the 2 new brief tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/__main__.py tests/discovery/test_cli.py
git commit -m "feat(discovery): CLI writes substack handoff brief to sibling path"
```

---

## Task 5: `--segment` qualifier (end-to-end)

**Files:**
- Modify: `tools/llm-council/council/discovery/__main__.py` (add `--segment` flag → `run_discovery`)
- Modify: `tools/llm-council/council/discovery/pipeline.py` (pass `segment` into the gather call)
- Modify: `tools/llm-council/council/discovery/gather/__init__.py` (thread `segment` into all six collectors)
- Modify: `tools/llm-council/council/discovery/gather/web.py` (`collect_web` segment in query)
- Modify: `tools/llm-council/council/discovery/gather/sonar.py` (`collect_sonar` segment in prompt)
- Modify: `tools/llm-council/council/discovery/gather/last30.py` (`collect_last30` segment composed into subject)
- Modify: `tools/llm-council/council/discovery/gather/reviews.py` (`collect_reviews` segment in subject) — **Phase 4 collector**
- Modify: `tools/llm-council/council/discovery/gather/github.py` (`collect_github` segment in query) — **Phase 4 collector**
- Modify: `tools/llm-council/council/discovery/gather/qa.py` (`collect_qa` segment in query) — **Phase 4 collector**
- Test: `tests/discovery/test_gather_web.py`, `test_gather_sonar.py`, `test_gather_last30.py`, `test_gather_reviews.py`, `test_gather_github.py`, `test_gather_qa.py`, `test_pipeline.py`, `test_cli.py` (add)

**Interfaces:**
- `collect_web(*, topic, segment="", search=..., fetch=..., max_results=8)`, `collect_sonar(*, api_key, topic, model, timeout=120.0, segment="", fetch=None)`, `collect_last30(topic, runner=_subprocess_runner, segment="")`, `collect_reviews(*, topic, segment="", search=..., fetch=..., max_results=8)`, `collect_github(*, topic, segment="", search=..., max_results=8)`, `collect_qa(*, topic, segment="", search=..., max_results=8)` each gain a `segment: str = ""` param that shapes their query when non-empty (default `""` = today's behavior). `gather_evidence(*, topic, tier, api_key, segment="", collectors=None)` threads `segment` into all six default collector lambdas. `run_discovery` passes its `segment` into `gather(...)`. The CLI adds `--segment` (default `""`).

**Context:** Spec §4 + Phase-1 run-#2 insight (the blind-spot map proved generic "creatives" returns developer pain). `--segment developer|creative|pm|<free text>` reshapes the gather queries toward a target audience so the evidence comes from where that audience actually posts. Default `""` keeps every existing collector test green.

> **Phase 4 has landed (MANDATORY scope for this task):** there are **six** collectors to thread `segment` through, not three. Step 3 below now includes the `reviews`/`github`/`qa` edits as primary code (each gains a `segment=""` param + query-shaping mirroring `collect_web`), and Step 1 includes a test for each. A `--segment` that only reshapes web/sonar/last30 would silently ignore half the evidence surface — do not skip the three Phase-4 collectors.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_gather_web.py`:

```python
@pytest.mark.asyncio
async def test_collect_web_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_web(topic="note apps", segment="designers", search=search, fetch=None)
    assert "designers" in captured["q"] and "note apps" in captured["q"]


@pytest.mark.asyncio
async def test_collect_web_no_segment_unchanged():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_web(topic="note apps", search=search, fetch=None)
    assert captured["q"] == "note apps user complaints problems frustrations 2026"
```

Add to `tests/discovery/test_gather_sonar.py`:

```python
@pytest.mark.asyncio
async def test_collect_sonar_includes_segment_in_prompt(httpx_mock):
    import json as _json
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "a claim about it here."}}],
        "citations": ["https://a.com/1"], "usage": {},
    })
    await collect_sonar(api_key="k", topic="note apps", model="perplexity/sonar",
                        segment="developers", fetch=None)
    body = _json.loads(httpx_mock.get_requests()[0].content)
    assert "developers" in body["messages"][0]["content"]
```

Add to `tests/discovery/test_gather_last30.py`:

```python
@pytest.mark.asyncio
async def test_collect_last30_composes_segment_into_subject():
    seen = {}
    async def runner(subject):
        seen["s"] = subject
        return "{}"
    await collect_last30("pm tools", runner=runner, segment="enterprise")
    assert seen["s"] == "pm tools enterprise"
```

Add to `tests/discovery/test_gather_reviews.py` (Phase 4 collector):

```python
@pytest.mark.asyncio
async def test_collect_reviews_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_reviews(topic="crm", segment="nonprofits", search=search, fetch=None)
    assert "crm" in captured["q"] and "nonprofits" in captured["q"]
    assert "site:g2.com" in captured["q"]   # still site-targeted
```

Add to `tests/discovery/test_gather_github.py` (Phase 4 collector):

```python
@pytest.mark.asyncio
async def test_collect_github_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_github(topic="auth", segment="mobile devs", search=search)
    assert "auth" in captured["q"] and "mobile devs" in captured["q"]
    assert "is:issue" in captured["q"]
```

Add to `tests/discovery/test_gather_qa.py` (Phase 4 collector):

```python
@pytest.mark.asyncio
async def test_collect_qa_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_qa(topic="docker", segment="data engineers", search=search)
    assert "docker" in captured["q"] and "data engineers" in captured["q"]
```

Add to `tests/discovery/test_pipeline.py`:

```python
@pytest.mark.asyncio
async def test_run_discovery_passes_segment_to_gather():
    seen = {}
    async def gather_fn(**kw):
        seen.update(kw)
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
    await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                        segment="developers", gather_fn=gather_fn)
    assert seen["segment"] == "developers"
```

Add to `tests/discovery/test_cli.py`:

```python
def test_cli_passes_segment_to_pipeline(tmp_path, monkeypatch, fake_api_key):
    captured = {}

    async def fake_run(**kw):
        captured.update(kw)
        return DiscoveryResult("# Idea Ledger — x\n", 0.1, 0, 0, {"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "x", "--lens", "pm", "--tier", "quick", "--segment", "designers",
        "--output", str(tmp_path / "o.md"), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert captured["segment"] == "designers"
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py::test_collect_web_includes_segment_in_query tests/discovery/test_gather_reviews.py::test_collect_reviews_includes_segment_in_query tests/discovery/test_gather_github.py::test_collect_github_includes_segment_in_query tests/discovery/test_gather_qa.py::test_collect_qa_includes_segment_in_query tests/discovery/test_pipeline.py::test_run_discovery_passes_segment_to_gather tests/discovery/test_cli.py::test_cli_passes_segment_to_pipeline -v`
Expected: FAIL — `collect_web()`/`collect_reviews()`/`collect_github()`/`collect_qa()`/`run_discovery()` reject the `segment` kwarg, and the CLI has no `--segment` option.

- [ ] **Step 3: Implement the threading**

In `council/discovery/gather/web.py`, add `segment` to `collect_web` and shape the query (replace the signature line and the `query = ...` line):

```python
async def collect_web(*, topic: str, segment: str = "", search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
```
```python
    subject = f"{topic} {segment}".strip() if segment else topic
    query = f"{subject} user complaints problems frustrations 2026"
```

In `council/discovery/gather/sonar.py`, add `segment` to `collect_sonar` and inject it into the prompt (replace the signature line and the user-message `content`):

```python
async def collect_sonar(*, api_key: str, topic: str, model: str, timeout: float = 120.0, segment: str = "", fetch=None) -> list[EvidenceRecord]:
    seg = f" specifically from the perspective of {segment}" if segment else ""
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"What are the most recent, specific user complaints and unmet needs about {topic}{seg}? "
                       f"Quote real users where possible. Cite sources.",
        }],
    }
```

> Phase 4 already added the `fetch=None` param to `collect_sonar` (Task 6) and the verbatim-fetch loop in its body — the signature above keeps `fetch=None` and adds `segment` alongside it. This is a **targeted edit**: replace only the signature line and the user-message `content` block; leave the verbatim-fetch loop intact. Do **not** touch the import — `sonar.py` imports only `extract_quotes` from `web.py` (Phase 4 M1 removed the dead `_simple_fetch` import).

In `council/discovery/gather/last30.py`, add `segment` to `collect_last30` and compose the subject (replace the signature line and the `text = await runner(topic)` line):

```python
async def collect_last30(topic: str, runner=_subprocess_runner, segment: str = "") -> list[EvidenceRecord]:
    subject = f"{topic} {segment}".strip() if segment else topic
    try:
        text = await runner(subject)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
```

In `council/discovery/gather/reviews.py`, add `segment` to `collect_reviews` and shape the subject before building the site-targeted query (replace the signature line; insert the subject line before `results = await search(...)` and use it):

```python
async def collect_reviews(*, topic: str, segment: str = "", search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
```
```python
    subject = f"{topic} {segment}".strip() if segment else topic
    results = await search(_review_query(subject))
```

In `council/discovery/gather/github.py`, add `segment` to `collect_github` and compose the subject into the issue query (replace the signature line and the `items = await search(...)` line):

```python
async def collect_github(*, topic: str, segment: str = "", search=..., max_results: int = 8) -> list[EvidenceRecord]:
```
```python
    subject = f"{topic} {segment}".strip() if segment else topic
    items = await search(f"{subject} in:title,body is:issue")
```

In `council/discovery/gather/qa.py`, add `segment` to `collect_qa` and compose the subject into the search term (replace the signature line and the `items = await search(topic)` line):

```python
async def collect_qa(*, topic: str, segment: str = "", search=..., max_results: int = 8) -> list[EvidenceRecord]:
```
```python
    subject = f"{topic} {segment}".strip() if segment else topic
    items = await search(subject)
```

In `council/discovery/gather/__init__.py`, add `segment` to `gather_evidence` and thread it into **all six** collector lambdas (replace the signature + the default `collectors` dict):

```python
async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str, segment: str = "",
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t, segment=segment)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model, segment=segment, fetch=_simple_fetch)),
            "web": (lambda t: collect_web(topic=t, segment=segment)) if tier.web else None,
            "reviews": (lambda t: collect_reviews(topic=t, segment=segment)) if tier.reviews else None,
            "github": (lambda t: collect_github(topic=t, segment=segment)) if tier.github else None,
            "qa": (lambda t: collect_qa(topic=t, segment=segment)) if tier.qa else None,
        }
```

> The `sonar` lambda keeps `fetch=_simple_fetch` (Phase 4 Task 7) and now also passes `segment=segment`. The `reviews`/`github`/`qa` entries + their tier gates already exist from Phase 4 — only `segment=segment` is added. Leave the imports (`collect_reviews`/`collect_github`/`collect_qa`/`_simple_fetch`) as Phase 4 left them.

In `council/discovery/pipeline.py`, pass `segment` into the gather call (replace the gather line):

```python
    gather = gather_fn or gather_evidence
    bundle, gather_status = await gather(topic=topic, tier=tcfg, api_key=api_key, segment=segment)
```

In `council/discovery/__main__.py`, add the `--segment` option and pass it to `run_discovery`:

```python
@click.option("--segment", default="", help="Reshape gather queries toward an audience (e.g. developer, creative, pm).")
```

(add this option decorator alongside the others, and add `segment` to the `main(...)` signature), then update the `run_discovery(...)` call:

```python
        result = asyncio.run(run_discovery(
            topic=topic, lens=lens, tier=tier, api_key=api_key, segment=segment, sessions_dir=sessions_dir,
        ))
```

- [ ] **Step 4: Run the affected tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py tests/discovery/test_gather_sonar.py tests/discovery/test_gather_last30.py tests/discovery/test_gather_reviews.py tests/discovery/test_gather_github.py tests/discovery/test_gather_qa.py tests/discovery/test_pipeline.py tests/discovery/test_cli.py -v`
Expected: PASS (existing collector/pipeline/CLI tests — all default `segment=""` → unchanged behavior — plus the 8 new segment tests, one per collector + pipeline + CLI). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/__main__.py council/discovery/pipeline.py council/discovery/gather/__init__.py council/discovery/gather/web.py council/discovery/gather/sonar.py council/discovery/gather/last30.py council/discovery/gather/reviews.py council/discovery/gather/github.py council/discovery/gather/qa.py tests/discovery/test_gather_web.py tests/discovery/test_gather_sonar.py tests/discovery/test_gather_last30.py tests/discovery/test_gather_reviews.py tests/discovery/test_gather_github.py tests/discovery/test_gather_qa.py tests/discovery/test_pipeline.py tests/discovery/test_cli.py
git commit -m "feat(discovery): --segment qualifier reshapes gather queries across all six collectors"
```

---

## Task 6: Docs reconciliation + final verification + live confirmation

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md`
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md` (one descriptive line)

**Interfaces:** none (docs + final gate).

**Context:** The substack lens + `--segment` now ship; the skill surface still says substack is "coming in a later phase." Reconcile the docs, run the full gate, and live-confirm one substack run.

- [ ] **Step 1: Update SKILL.md — substack lens + segment now ship**

In `.claude/skills/fusion-discovery-council/SKILL.md`:

In the §1 table row, change:

```
| "Find me Substack ideas grounded in real reader pain" | Phase 2 (see lens note) — `pm` lens ships now |
```

to:

```
| "Find me Substack ideas grounded in real reader pain" | Yes — `--lens substack` emits a post-angle ledger + a substack-value-engine handoff brief |
```

In §3, replace the `--lens` note:

```
**`--lens`** — `pm` frames verified pain into ranked PM opportunities and **is the only lens shipping in Phase 1**. `substack` (framing the same evidence as newsletter/essay ideas) is **coming in a later phase** — do not present it as working.
```

with:

```
**`--lens`** — `pm` (default) frames verified pain into ranked PM opportunities. `substack` reframes the same verified pain into ranked post angles and additionally writes a **handoff brief** consumable by the `substack-value-engine` skill (chain: substack-value-engine → storytelling-architecture → writing-voice-modes → writing-critique → writing-humanity-pass). The brief pre-fills the Value-Gate Itch + Transfer + verbatim evidence and leaves the Solution slot for you.

**`--segment`** — optional free-text audience qualifier (e.g. `developer`, `creative`, `pm`) that reshapes the gather queries toward where that audience posts. Use it when a generic topic returns the wrong segment's pain (e.g. generic "creatives" returns developer pain).
```

In §3's flag block, add the `--segment` line under `--tier`:

```
--segment  <audience>        reshape gather queries toward a target audience (optional)
```

Update the §4 "Output path convention" and add the brief path:

```
vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md
```

Add directly below it:

```
On `--lens substack`, a sibling brief is also written:

vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-substack-brief.md
```

In §2, change the FRAME step (4.) to acknowledge both lenses:

```
4. **FRAME** — Apply the lens (`pm` in Phase 1) to turn each *verified* pain point into a ranked, evidence-linked opportunity, and render the **idea ledger** markdown.
```

to:

```
4. **FRAME** — Apply the lens to each *verified* pain point: `pm` → ranked, evidence-linked opportunity cards; `substack` → ranked post angles + a substack-value-engine handoff brief. Render the **idea ledger** markdown (+ the brief for substack).
```

- [ ] **Step 2: Add a CHANGELOG entry**

Add a dated entry under the latest `CHANGELOG.md` heading:

```markdown
### fusion-discovery-council Phase 5 — substack lens + segment qualifier (2026-06-20)
- `--lens substack` ships: reframes verified pain points into ranked post angles (`frame_substack`) and writes a `substack-value-engine`-consumable handoff brief (pre-fills the Value-Gate Itch + Transfer + verbatim evidence; leaves Solution for the author). Renders a `Substack Idea Ledger` + a sibling `-substack-brief.md`. No new Fusion call — same per-run cost as `pm`.
- `--segment <audience>` reshapes the gather queries (all six collectors: web/sonar/last30 + reviews/github/qa) toward a target audience, fixing the "generic 'creatives' returns developer pain" failure mode. Default empty = unchanged behavior.
- Plan: docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md.
```

- [ ] **Step 3: Update the CLAUDE.md descriptive line**

In `CLAUDE.md`, the fusion-discovery-council entry describes the pipeline as ending `→ FRAME (pm lens → idea ledger)`. Update that fragment to reflect both lenses:

```
FRAME (pm lens → idea ledger)
```

to:

```
FRAME (pm lens → idea ledger; substack lens → post-angle ledger + substack-value-engine handoff brief)
```

(This is a one-line accuracy tweak, not a count-table change — no new skill/agent/script was added.)

- [ ] **Step 4: Full verification gate**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run --extra dev python -m pytest -v
cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py
```

Expected: pytest fully green (baseline + all new Phase-5 tests passed, 1 skipped); `validate.py` passes (pre-existing secret-pattern warnings only, none in changed files).

- [ ] **Step 5: Live confirmation (ask Sean before spending) — one substack run**

Confirm the lens end-to-end on today's live sources (cost is the same as `pm`):

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "AI note-taking apps" --lens substack --segment "indie developers" --tier quick \
  --output /tmp/p5-substack-idea-ledger.md
```

Expected: writes `/tmp/p5-substack-idea-ledger.md` (a `Substack Idea Ledger` with ranked post angles) **and** `/tmp/p5-substack-brief.md` (the handoff brief with Itch/Solution/Transfer slots + verbatim evidence). Verify the brief's evidence quotes are real fetched-URL substrings (gate held) and the segment shaped the queries. Record the cost (should be ≈ the `quick` `pm` figure, ~$0.36).

- [ ] **Step 6: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md CLAUDE.md
git commit -m "docs(discovery): Phase 5 — substack lens + --segment surface reconciliation"
```

> The vault is intentionally **not** staged (CLAUDE.md rule 8 — Obsidian-Git owns vault commits). The live-run ledger + brief go to `/tmp`; any spend-ledger row written to `vault/health/` is left for Obsidian-Git, never `git add`-ed here.

---

## Self-Review (completed during plan authoring)

**Spec coverage (§4 `--lens`/`--segment`, §5 substack lens, §9 output + Phase-3 §7d):**
- `frame_substack()` → Task 1 ✅ (verified pain → post angles + hooks + value-promise/Transfer + candidate Itch; consumes post-VERIFY points, no new Fusion call).
- Handoff brief consumable by `substack-value-engine` → Tasks 2 + 4 ✅ (brief scaffolds Itch/Solution/Transfer per the skill's Value Gate, names the chain, carries verbatim evidence; written to the spec §9 sibling path).
- Wire `--lens substack` through `__main__.py` + a render variant → Tasks 3 + 4 ✅ (pipeline lens branch + `render_substack_*`).
- `--segment` qualifier reshaping gather queries → Task 5 ✅ (all six collectors: web/sonar/last30 + reviews/github/qa, threaded via gather_evidence + run_discovery + CLI; Phase-1 run-#2 insight addressed).
- Output path per §9 (ledger + brief where the chain expects) → Task 4 ✅ (`...-substack-idea-ledger.md` + `...-substack-brief.md` under `vault/20_projects/research/`).

**Placeholder scan:** every code/test step carries complete code grounded in the real current files (re-read 2026-06-20) and the real `substack-value-engine` Value-Gate contract. No TBD/TODO. The one live step (Task 6 Step 5) is a gated, Sean-approved confirmation with the deterministic unit tests as the real gate.

**Type consistency:** `PostAngle` (Task 1) is consumed by `render_substack_*` (Task 2) and `pipeline` (Task 3) with matching field names (`title/audience/hook/itch/transfer/evidence_urls/quotes/whitespace/score/corroboration`); `frame_substack(verified, fusion_result, segment="")` signature matches its pipeline call; `DiscoveryResult.brief_markdown` (Task 3, default `""`) is read by the CLI (Task 4) and defaults keep existing positional `DiscoveryResult(...)` constructions valid; `run_discovery`'s `segment` param (Task 3) is populated by the CLI + threaded to `gather_evidence` (Task 5); `_brief_path` (Task 4) is defined before use. `collect_web/collect_sonar/collect_last30/gather_evidence` all gain `segment: str = ""` (Task 5) — default empty preserves every existing call site and test.

**Cross-phase consistency (Phase 4 landed):** Task 5 threads `segment` through **all six** collectors (web/sonar/last30 + reviews/github/qa), with `collect_sonar` keeping its Phase-4 `fetch=None` param and the orchestrator keeping `fetch=_simple_fetch`. `sonar.py`'s import is left as Phase 4's M1 fix left it (`extract_quotes` only). The substack-lens tasks (1–4) are collector-agnostic (post-VERIFY) and apply verbatim.

---

## Phasing reminder

This plan is **Phase 5 (substack lens + segment qualifier)** only. It is the final planned phase of the original spec's roadmap. **Phase 4 has landed**, so it runs on top of the wider evidence surface (reviews/github/qa) and `--segment` reshapes all six collectors. After it lands and a live substack run confirms the lens + brief:
- **Future (deferred, per spec §13):** autonomous/queued discovery mode; Apify actors for gated review-site depth; additional `deep` lineages; pain-taxonomy persistence across runs; the competitor-Substack/newsletter-landscape collector (spec §6, substack-lens-specific — defers cleanly as a Phase-4-style site-targeted collector).
