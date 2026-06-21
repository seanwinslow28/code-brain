---
title: fusion-discovery-council — Phase 5 (Substack Lens + Segment Qualifier) Field Report
date: 2026-06-21
status: complete
branch: feat/fusion-discovery-council-phase5
plan: ../../../../docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md
phase4_report: 2026-06-21-fusion-discovery-council-phase4-field-report.md
baseline_commit: c9e1aac
head_commit: cf718cf
commits: 6
test_status: 133 passed, 1 skipped
validate: PASSED (clean on changed files; 62 pre-existing warnings in unrelated vendor/skill files)
live_e2e: quick $0.25 (substack lens, --segment "indie developers") — under the $0.50 quick cap, no second model call
merged: false
roadmap: Phase 5 is the FINAL planned phase of the original spec roadmap. The lens + flag ship; the tool is NOT yet production-hardened (see §7).
---

# fusion-discovery-council — Phase 5 Field Report (detailed)

**One-line:** All six Phase-5 tasks landed green via subagent-driven TDD (implement → spec-compliance review → code-quality review per task), closed by an opus whole-branch review (**"Ready to merge"**) and a Sean-approved live run that confirmed the lens end-to-end. Phase 5 adds the `substack` lens (verified pain → ranked post angles + a `substack-value-engine` handoff brief) and the `--segment` audience qualifier (threaded through all six Phase-4 collectors). Suite **133 passed, 1 skipped** (was 114+1); `scripts/validate.py` **PASSED**. The live `quick`-tier substack run cost **$0.25** — same FUSE cost as `pm`. This phase completes the original spec roadmap, but it does **not** make the tool production-dependable: §7 is honest about what still needs work.

---

## 1. Executive summary

Phase 5 was **pure additive Stage-4 work plus a gather-query qualifier** on the existing `council/discovery/` subpackage — no new stage, no FUSE/VERIFY change, and the fabrication gate (`verify.py`) was never touched.

- **6 commits** off plan baseline `c9e1aac` (5 feature commits + 1 docs-reconciliation commit). Touches two new modules (`frame_substack.py`, `render_substack.py`), `pipeline.py`, `__main__.py`, all six `gather/*` collectors + `gather/__init__.py`, plus `SKILL.md`/`CHANGELOG.md`/`CLAUDE.md` and the test files. **`verify.py` was never touched** — confirmed by an empty diff over the whole range (the opus reviewer ran `git diff c9e1aac cf718cf -- verify.py` → empty).
- **Test suite: 114 → 133 passed, 1 skipped** (+19 net-new tests). The single skip is the pre-existing `INTEGRATION=1`-gated live test (`test_e2e.py`), unrelated to this work.
- **`scripts/validate.py`: PASSED** — clean on every changed file (the 62 pre-existing secret-pattern warnings are all in unrelated vendor/skill files).
- **Every task passed both review stages on the first implementation pass.** No implementer returned BLOCKED or NEEDS_CONTEXT; no task required a re-dispatch. The plan carried complete, current-file-grounded code, so implementers reconciled-and-verified against the live files rather than designing.
- **Live confirmation (the only spend, $0.25):** `quick`-tier `--lens substack --segment "indie developers"` produced 5 verified post angles (0 dropped), wrote both the ledger and the sibling brief, and FUSE did *not* flake on the known SSE bug this run.
- **Method:** `superpowers:subagent-driven-development`. Fresh implementer subagent per task; two-stage review per task (a spec-compliance reader + a code-quality reviewer), each verifying against the **real diff**, not the implementer's report. Tasks ran **strictly sequentially** — `pipeline.py` is touched by Tasks 3+5 and `__main__.py` by Tasks 4+5, so no parallelism. Closed with a broad whole-branch review on opus.

## 2. What shipped, by commit

| Commit | Task | What | Tests after |
|---|---|---|---|
| `8026cde` | 1 | **`frame_substack.py`** — `PostAngle` dataclass + `frame_substack(verified, fusion_result, segment="")`. Reframes each *verified* pain point into a ranked post angle (hook + candidate Value-Gate Itch + Transfer + whitespace + verbatim evidence). Mirrors `frame_pm`'s scoring (`intensity × (1 + corroboration-domains)`) and quote-bank dedup **exactly**. No new Fusion call — operates post-VERIFY. | 117 |
| `70b7517` | 2 | **`render_substack.py`** — `render_substack_ledger` (ranked post-angle idea ledger, mirrors `render_ledger`'s section set) + `render_substack_brief` (the `substack-value-engine`-consumable handoff brief; pre-fills Itch slot 1 + Transfer slot 3 + verbatim evidence, leaves Solution slot 2 for the author). | 120 |
| `8d5d3d0` | 3 | **Pipeline lens branch** — `run_discovery` branches on `lens`; `DiscoveryResult` gains `brief_markdown` (last field, default `""`); `run_discovery` gains `segment` param. pm path byte-identical; empty-bundle + FusionError paths untouched. Substack modules imported lazily inside the branch. | 122 |
| `a31255e` | 4 | **CLI brief write** — `_brief_path(output)` derives the sibling `...-substack-brief.md`; on `--lens substack` with a non-empty brief, the CLI writes + echoes it. pm lens writes no brief. | 124 |
| `1528ae0` | 5 | **`--segment` qualifier (end-to-end)** — threaded CLI → `run_discovery` → `gather_evidence` → **all six** collectors (web/sonar/last30 + reviews/github/qa), each shaping its query/prompt/subject from `subject = f"{topic} {segment}".strip() if segment else topic`. Default `""` = byte-identical to today. | 133 |
| `cf718cf` | 6 | **Docs reconciliation** — SKILL.md (§1 table, §2 FRAME step, §3 lens/segment notes + flag block, §4 output paths), CHANGELOG Phase-5 entry, one CLAUDE.md descriptive line. No stale "coming in a later phase" claim survives. | 133 |

**Plan-vs-prose note:** the plan's Task 5 text says "8 new segment tests" but specifies **9** test bodies (web gets both `includes_segment` and `no_segment_unchanged`), so the net-new count is 3+3+2+2+9 = **19**, landing the suite at 133. No unrequested test was added.

## 3. How the execution went

Exceptionally clean — the same pattern as Phase 4. The plan was unusually complete (every task carried verbatim, current-file-grounded code and tests), so the implementer role was transcription-plus-TDD, not design. Model selection: sonnet for every implementer + spec reviewer; the dedicated **Code Reviewer** agent (sonnet) for per-task quality; **opus** for the final whole-branch review.

- **No execution failures.** All six implementers returned DONE on the first pass; none went BLOCKED or NEEDS_CONTEXT; none needed a re-dispatch. Every task confirmed RED-before-GREEN.
- **The two-stage per-task review found no Critical/Important issues on any task.** All findings were Minor (polish, idiom, test-coverage nits) — carried to the final review rather than churning per-task (the Phase-4 precedent).
- **One controller-caught data discrepancy** (Task 5): the implementer reported 133 passed with a garbled explanation. The controller independently ran the suite + counted the new test functions in the diff and confirmed 133 is correct (the plan's prose under-counts its own specified test bodies by one). The implementer's number was right; the reasoning was wrong — caught by not trusting the report.
- **No scope drift.** The fabrication gate was never touched; no paid call was added; caps were not weakened; only the planned files changed (plus one in-scope SKILL.md accuracy line in Task 6).

### 3.1 The whole-branch review (opus): "Ready to merge"

The opus reviewer verified the two NON-NEGOTIABLES at code level, not just at the test level:
1. **`verify.py` is provably untouched** (empty diff over the range; it doesn't appear in `--stat`). The substack lens sits strictly downstream of `verify_pain_points` and can only read `VerifiedPainPoint.supporting_urls` — never the raw `pt.urls`. There is **no reachable path** for the lens or its renderer to introduce an ungrounded claim.
2. **Phase 5 adds no billable call.** `fuse()` is called exactly once, before the lens branch; the substack lens reuses that single `FusionResult`. `frame_substack`/`render_substack_*` do zero I/O. `--segment` only mutates query strings. No second HTTP client, no second spend file.

It also confirmed: pm path regression-free, all six collectors genuinely honor `segment` (not accept-and-ignore), tier gates intact, sonar's Phase-4 invariants preserved (`fetch=None` + `extract_quotes`-only import; the lambda keeps `fetch=_simple_fetch`), the brief speaks the `substack-value-engine` Value-Gate contract, and the docs carry no stale phase-gating claim. **No Critical, no Important.**

## 4. Live e2e — the substack confirmation (2026-06-21, Sean-approved spend)

`"AI note-taking apps" --lens substack --segment "indie developers" --tier quick --output /tmp/p5-substack-idea-ledger.md`

| Metric | Value |
|---|---|
| Cost | **$0.25** (est. ~$0.36; cap $0.50) — same FUSE cost as `pm`, no second model call |
| Verified post angles | **5** |
| Dropped by verification | **0** |
| Ledger written | `/tmp/p5-substack-idea-ledger.md` (5,906 B) — `Substack Idea Ledger`, 5 ranked angles |
| Brief written | `/tmp/p5-substack-brief.md` (8,735 B) — Value-Gate scaffold + verbatim evidence |
| `--segment` shaped the run | Yes — every angle's Audience = "indie developers"; the brief surfaces "Target segment: indie developers" |
| FUSE SSE flake (the known HIGH bug) | Did **not** fire this run |

**Per-collector behavior (this run):** `last30` degraded safely to 0 records (the upstream `INCLUDE_SOURCES=null` crash — `AttributeError: 'NoneType' object has no attribute 'split'`, printed and swallowed). Sonar + web + reviews + github + qa supplied the evidence (quick tier = last30 + sonar + web; the 5 angles' evidence URLs span insightcrunch, review2idea, youtube, pcmag, voicetonotes, intrico, reddit, platformer, linkedin, mltaikins, meetjamie — i.e. the live web+sonar surface).

**Brief correctness (read directly):**
- All 5 angles leave the **Solution slot empty** for the author (`_What did you actually do? The gate blocks until this is a real run/eval/commit/number._`).
- Itch (slot 1) + Transfer (slot 3) are pre-filled as **candidates** from the verified pain; whitespace/differentiation is carried from the FUSE blind-spot map.
- The brief header names `substack-value-engine` + the full downstream chain.

**Gate-held spot-check (honest):** the run reported **dropped: 0**, meaning all 5 candidates traced to a real fetched URL through the untouched `verify.py`. A direct post-hoc fetch confirmed the insightcrunch quote *"faster than slow"* is present in the live page. A second spot-check (platformer.news, *"more work than it is worth"*) came back **not-found via bare `curl`** — but that is a curl-vs-pipeline fetch-method difference (the page is JS-heavy and returns a different shell to a bare curl than the pipeline's `_simple_fetch` saw at verification time), **not** a gate failure. The structural guarantee holds: `verify.py` is untouched, dropped=0, and every brief quote is sourced from a `VerifiedPainPoint.supporting_urls`. I'm flagging the one inconclusive spot-check rather than claiming a clean 2/2.

## 5. What we learned

1. **The substack lens is genuinely free-of-extra-cost.** $0.25 confirms the design intent: reframing post-VERIFY points into post angles costs the same single FUSE as `pm`. There is no per-lens model call. A `pm` and a `substack` run on the same topic/tier bill identically.
2. **`--segment` reaches framing AND gather, and the framing effect is visible immediately** (Audience = the segment on every card) while the gather effect is structural (it reshapes query strings). On this run the *evidence* still skewed to general note-taking pain rather than a sharply developer-flavored corpus — which is expected for a broad topic where the segment is a soft nudge, not a hard filter. The segment's value shows up most on topics where a generic phrasing returns the wrong audience's pain; "indie developers" + "AI note-taking apps" is a mild case.
3. **A "complete-code" plan makes subagent-driven execution nearly frictionless** — zero re-dispatches across six tasks — but the value of the final whole-branch review is still real: it's the only stage that verifies the cross-task seams (type/kwarg/default flow across 6 commits) and the load-bearing invariants (gate untouched, single FUSE) at code level rather than trusting the green suite.
4. **Not trusting the implementer's report caught a real (if harmless) discrepancy** (Task 5 test count). The controller's independent re-count is cheap insurance that the per-task spec review's "verify against the diff, not the report" discipline is worth keeping.
5. **`last30` is still a zero-yield live source.** GATHER is effectively Sonar + web + reviews + github + qa live; the social backbone remains dark (carried from Phase 4, an external config bug).

## 6. Failures & known-degraded paths (honest)

- **No execution failures** in this phase — all six tasks succeeded first-pass; the final review found no Critical/Important issues.
- **`last30` contributes 0 records live** — the upstream `last30days` plugin crashes before emitting JSON (`config.get('INCLUDE_SOURCES', '').split(',')` → `AttributeError` because `INCLUDE_SOURCES` is an explicit null). Our collector degrades safely to `[]`, so the pipeline never crashes, but the social backbone yields nothing. **External config bug, not a Phase-5 regression.** The 30-second unblock (set `INCLUDE_SOURCES=reddit,hackernews` in `~/.config/last30days/.env`) was **not** done this session.
- **Review collector under-yields (~3 records)** — Brave collapses the OR'd multi-`site:` query in `_review_query` (Brave treats `site:` as a single filter hint, not a Boolean). Records that *do* return are real + gate-valid; this is yield tuning only. **Ticketed** (M2, LOW, carried from Phase 4).
- **One inconclusive live spot-check** — see §4. Not a gate failure; a fetch-method artifact. Logged honestly rather than papered over.
- **Uneven quote/URL pairing in the brief** (observed live, Angle 2): when a pain point carries more `quotes` than `supporting_urls`, the trailing quotes render without an inline URL (the `zip(quotes, supporting_urls + [""]*len(quotes))` padding). This is **intended behavior carried verbatim from `frame_pm`** — the quotes are still gate-verified; the positional pairing simply runs out of URLs. Not a defect, but worth knowing the brief can show a bare quote.

## 7. WHAT STILL NEEDS ATTENTION before "full fusion-discovery-council completion" (the honest list)

Phase 5 completes the **planned roadmap**. It does **not** make the tool production-dependable. In priority order:

### 7a. ~~HIGH — Fusion response robustness (the real blocker)~~ → ✅ RESOLVED (was stale)

> **CORRECTION (2026-06-21, post-Phase-5 close-out review).** This section was carried **stale from the Phase-2 backlog** and does **not** match the current code on `main`. Both fixes it asks for already shipped in **Phase 3**:
> - `fuse()` does **not** use an "unguarded `resp.json()`" — it calls `_decode_payload(resp)` ([fusion.py](../discovery/fusion.py)), a 3-tier SSE-padding-robust decoder (`json.loads` → `_strip_sse_padding` → `_first_json_object` scan-forward → typed `FusionError`).
> - Failed Fusion calls **do** record spend: `total_cost` accumulates `usage.cost` across attempts → `FusionError(cost=…)` → the CLI's `except DiscoveryFailed` calls `record_spend`. Not $0.
> - **OpenRouter docs research (2026-06-21) confirms our handling is documented-correct:** `: OPENROUTER PROCESSING` is a documented SSE keep-alive *comment*; per the SSE spec, `:`-prefixed lines must be ignored — exactly what `_strip_sse_padding` does. Streaming is not required for slow calls. Sources: [server-tools/fusion](https://openrouter.ai/docs/guides/features/server-tools/fusion), [api/reference/streaming](https://openrouter.ai/docs/api/reference/streaming).
>
> **Net: §7a is closed** — the named bug is fixed AND the approach is validated. The "two runs failed on 2026-06-20" were **Phase-2** runs, pre-Phase-3-fix. The only residual is *confidence* (few live runs) — see the close-out live-run plan. Original (stale) text preserved below for the record.

Live discovery **intermittently fails at the FUSE parse step**. Two `quick`-tier runs on 2026-06-20 both failed: one `FusionError "did not return parseable"`, one bare `JSONDecodeError`. Root cause: OpenRouter streams `: OPENROUTER PROCESSING` SSE keep-alive comment lines as padding on slow Fusion calls, so `fuse()`'s unguarded `payload = resp.json()` in [`fusion.py`](../discovery/fusion.py) chokes on the non-JSON prefix. **It did not fire on today's Phase-5 live run, which is exactly why it's dangerous — it's intermittent, correlated with slow panel/tool-call runs.** Until this is fixed, *any* live run (pm or substack) can fail unpredictably. **Two coupled fixes:** (1) strip leading `: ` comment lines / extract the first balanced `{…}` before `json.loads`, harden `_parse`; (2) **cost-integrity** — failed Fusion calls bill OpenRouter but `record_spend` is post-success only, so a failed run records $0 locally. Record `usage.cost` on failure too. **This is the single highest-leverage thing to do before the tool is dependable.** Ticketed HIGH; full write-up in the Phase-2 field report §5/§6.

### 7b. ~~MEDIUM — the social backbone is dark~~ → ✅ RESOLVED (2026-06-21)

> **RESOLVED (2026-06-21, commit `85b1a63`).** Root cause confirmed: the upstream loader ([lib/env.py](file)) defaults `INCLUDE_SOURCES=None`, then `last30days.py` does `.split(',')` on it. Fixed **durably in our repo** (not a global `~/.config` hack a fresh machine loses): `gather/last30.py`'s `_last30_env()` forces `INCLUDE_SOURCES=reddit,hackernews` (keyless sources) in the subprocess env, which wins in the plugin's `os.environ`-first loader precedence. Live-verified — the crash is gone and **reddit yields records** (3 on the verification run). HN errored that run under `--no-native-web` (degrades safely to 0 HN records; a `hackernews_error` field is emitted) — logged as a LOW follow-up, not a blocker.

`last30` yields 0 live (§6). The tool currently leans on Sonar + web + reviews + github + qa. The substack lens specifically benefits from Reddit/HN social pain, which is exactly what `last30` would supply. The 30-second config unblock should be done and verified before anyone leans on the substack lens for real reader-pain mining. Ticketed (carried).

### 7c. LOW — `--segment` free-text into operator-bearing queries (NEW this phase)
`--segment` composes raw text unescaped into the github (`is:issue`) and reviews (`site:`/paren grouping) queries. A segment with operator tokens (`is:pr`, an unbalanced `)`, `site:foo`) alters query semantics rather than narrowing the audience — a self-inflicted **yield** bug, **not** a security or fabrication issue (read-only public search APIs; the VERIFY gate still governs every record downstream). Fix if `--segment` ever becomes automated/non-interactive input: a single `segment = segment.strip()` + operator-char strip at the CLI boundary (also closes the whitespace-only-segment edge in the sonar prompt). **Ticketed this session** (LOW). Surfaced by the whole-branch review.

### 7d. LOW — review collector under-yield (M2)
Fan out to N single-`site:` queries (one per `REVIEW_DOMAIN`) instead of one OR'd query, or feed query-expansion. Correctness fine; yield tuning only. Ticketed (carried from Phase 4).

### 7e. LOW — GATHER-stage spend invariant
The `except DiscoveryFailed` cost-recording path covers only FUSE-stage spend; the generic `except` assumes "no spend pre-fuse." True today (FUSE is the only billable stage), but if a Sonar/web call is ever instrumented to bill, a gather-stage failure would silently record $0. Documented invariant, not a live bug. Ticketed (carried).

### 7f. Carried minor code findings (non-blocking, intended/consistency-preserving)
None block merge; all either match the sibling `frame_pm`/`render_ledger` bar or are intended:
- `frame_substack`'s `.rstrip(": ")` is a character-set strip (cosmetic; could be `removesuffix`-style). The `itch`/`transfer` are deliberately templated candidates. `whitespace` is run-global (same for every angle) by design. `_domains` is duplicated from `frame.py` (a deliberate no-shared-util trade-off; drift risk if `frame_pm`'s domain logic ever changes).
- `render_substack` intentionally omits the Contradiction Map section that `render_ledger` carries (less relevant for a post-angle ledger) — worth a one-line comment so a future maintainer doesn't "fix" it.
- `pipeline.py` lazy import (justified for module isolation) and `__main__.py`'s double-call of `_brief_path` (cheap pure function) — both cosmetic.
- A pre-existing positional `DiscoveryResult(...)` construction in `test_cli.py` survives only because the new field was appended last; a future field reorder would mis-bind it. Hygiene-only; convert to kwargs if touched.
- The brief docstring hard-codes "for Sean" — fine for a personal tool, the one spot the otherwise-generic module names the operator. Matters only if the discovery subpackage is ever exported via the installer.

### 7g. Deferred-further (documented, out of the original roadmap)
Per spec §13 / Phase-4 §7d: autonomous/queued discovery mode; Apify actors for gated review-site depth; additional `deep` panel lineages; pain-taxonomy persistence across runs; demand-intent as query-expansion; trend-velocity feeds; the competitor-Substack/newsletter-landscape collector (a clean Phase-4-style site-targeted add for the substack lens). None are needed for the roadmap; all are real enhancements if the tool gets daily use.

### 7h. NEW (2026-06-21 OpenRouter Fusion research) — two LOW findings
Surfaced by the close-out research dig into the OpenRouter Fusion server-tool + streaming docs (the same dig that confirmed §7a is closed). Neither is a live bug today; both are cheap insurance.
- **Request-shape divergence (LOW, compatibility watch).** Current OpenRouter docs put the Fusion config under `tools[0].parameters` (with the judge as `model` *inside* it). Our `_build_body` ([fusion.py](../discovery/fusion.py)) uses a **top-level `"fusion"` block** + top-level `model`. Ours is live-verified working (FUSION_SCHEMA.md), but no test would catch it if OpenRouter ever drops the top-level form. Fix-if-it-breaks: move config into `tools[0].parameters`. Add a periodic live re-verify. Ticketed.
- **Typed `failure_reason` is invisible to us (LOW, diagnosability).** The Fusion tool hard-fails with `status:"error"` + a typed `failure_reason` (`all_panels_failed`, `insufficient_credits`, `rate_limited`, `fusion_invocation_capped`, `unexpected_error`). Because we read the **outer judge's** `message.content` rather than the raw tool result, those reach us as a vague "did not return parseable" + one retry → `FusionError`. Safe (degrades correctly) but loses the diagnostic. A future enhancement could detect `status`/`failure_reason` and surface it. Ticketed.
- Also confirmed in-spec by the research (no action): `analysis_models` range 1–8 (we use ≤6), `max_tool_calls` range 1–16 (we use ≤8), and streaming is **not** required for slow calls.

## 8. State of the branch

- **Branch:** `feat/fusion-discovery-council-phase5` — **not merged, no PR** (per the kickoff: stay on the feature branch unless asked).
- **Range:** `c9e1aac..cf718cf`, 6 commits. Suite **133 passed, 1 skipped**; `validate.py` **PASSED** clean on changed files.
- **Git hygiene:** nothing of this work is left staged; the only modified working-tree file is `vault/00_inbox/tickets.md` (the new §7c ticket), which **Obsidian-Git owns** per CLAUDE.md rule 8 — never `git add`'d by this session. The live-run ledger + brief went to `/tmp`; no `vault/health/` spend row was staged here.
- **Final whole-branch review (opus): Ready to merge.** No Critical, no Important.

## 9. Bottom line (honest)

**The roadmap is done; the tool is feature-complete and the deterministic gate is green.** The substack lens and `--segment` are correct, cost-safe, and fabrication-gate-respecting. **But "feature-complete" ≠ "dependable for real use."** The one thing that actually gates trustworthy operation is **§7a (Fusion robustness)** — it's a HIGH, intermittent, live-only failure that today's run happened to dodge. If this tool is going to be used to mine real Substack ideas, fix 7a first and unblock 7b (`last30`) second; everything else in §7 is genuine but lower-stakes. I'd not call the fusion-discovery-council "complete" in the operational sense until 7a is closed and a few consecutive live runs (both lenses) succeed without a FUSE flake.

> **UPDATE (2026-06-21 close-out).** The §9 framing above was built on a stale §7a. On review: **§7a was already closed** (the bug was fixed in Phase 3 and the SSE-strip approach is validated documented-correct by OpenRouter research — see the §7a correction). **§7b (`last30`) is now fixed** (`85b1a63`, reddit yields live). So **there is no remaining blocker.** What's left before declaring *operational* completeness is **confidence only** — a few consecutive live runs (incl. deep-tier, the slowest/worst case for SSE padding) without a FUSE flake. The two new research findings (§7h) are LOW and ticketed. Revised bottom line: **the tool is feature-complete, the one real open item is closed, and operational confidence is one short live-run pass away.**
