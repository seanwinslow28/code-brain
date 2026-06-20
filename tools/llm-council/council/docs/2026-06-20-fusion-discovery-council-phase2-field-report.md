---
title: fusion-discovery-council — Phase 2 (Harden the Slice) Field Report
date: 2026-06-20
status: complete
branch: feat/fusion-discovery-council
plan: ../../../../docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase2.md
phase1_report: 2026-06-20-fusion-discovery-council-phase1-field-report.md
---

# fusion-discovery-council — Phase 2 Field Report

**One-line:** All seven Phase-2 tasks landed green via subagent-driven TDD (implement → spec review → code-quality review per task). The hardening goals are met — the discovery slice is now genuinely multi-source, empty runs are diagnosable, and the three cost/budget-integrity gaps are closed. One real rollover blocks *live* last30 yield (an upstream plugin crash, not our code); everything else deferred is intentional Phase-3 polish.

## 1. Executive summary

Phase 1 shipped a live-validated single-source slice (Sonar only, in practice). Phase 2 was pure hardening of the existing `council/discovery/` subpackage — no new stages, no new lenses. It executed exactly to plan with no scope drift.

- **8 commits** off the plan baseline `e64f0782`; **+387 / −84** across 6 code files + 7 test/doc files.
- **Test suite: 66 → 76 passed, 1 skipped** (10 net-new tests). Discovery subpackage alone: **42 passing**. `scripts/validate.py`: **PASSED** (62 pre-existing secret-pattern warnings, none in changed files).
- **Every task passed both review stages.** Spec-compliance review found **zero** missing/extra/wrong items on all seven tasks. Code-quality review returned **approve / approve-with-nits** on every task (scores 8–9/10); all nits were Minor with safe failure modes and are catalogued in §5.
- **Method:** `superpowers:subagent-driven-development`. Fresh implementer subagent per task; two independent reviewers per task (a spec-compliance reader + the `Code Reviewer` agent), each verifying against the real code rather than the implementer's report. Tasks run strictly sequentially because of file overlap (`pipeline.py` in Tasks 2+4, `fusion.py` in Tasks 4+5).

## 2. What shipped, by commit

| Commit | Task | What |
|---|---|---|
| `08cad85` | 1 | Brave web provider (`_default_brave_search`) + `_simple_fetch` full-page fallback; `collect_web` now Exa→Brave→none. |
| `bd4add6` | 1 (review fix) | Bounded `_simple_fetch` to `text/*`/`application/xhtml` + 2 MB cap; recorded SSRF/redirect deferral comment. |
| `51c2c61` | 2 | `gather_evidence` → `(bundle, status)` tuple; per-collector `ok:/error:` status to stderr + threaded into session JSON (both empty + normal branches). |
| `b098409` | 3 | last30days collector rewrite: real plugin path first, `--emit=json` parser over `report.to_dict()`, dropped the bogus `--agent` flag, swallow bad JSON. |
| `ad4deed` | 4 | `FusionResult.cost` captures OpenRouter `usage.cost`; `_estimate_cost` prefers it, falls back to token+web estimate. |
| `8edb75e` | 5 | Fusion `>=400` raises `FusionError` with the OpenRouter error body verbatim; no retry on HTTP errors (the prompt-only retry was useless against a 400). |
| `7dea981` | 6 | Council CLI preflight → `preflight_tool(tool="council")`; council + discovery budgets now isolated **bidirectionally**. |
| `a4cc098` | 7 | Reconciled SKILL.md §2/§5, CHANGELOG, and the Phase-1 field report (RESOLVED notes on §5 + §6 items 1–4). |

**Backlog coverage (from the Phase-1 field report):**
- **Tier A** — Brave web ✅ (Task 1) · last30days path/flags/JSON parser ✅ (Task 3) · per-collector diagnosability ✅ (Task 2).
- **Tier B** — symmetric per-tool budgets ✅ (Task 6) · authoritative `usage.cost` ✅ (Task 4) · Fusion 4xx surfacing ✅ (Task 5).
- Phase-1 punch-list Important items **1–4 all closed**; Minor items 5–8 intentionally left for Phase 3.

## 3. How the execution went

Smooth. The plan was unusually complete — every task carried verbatim, current-file-grounded code and tests — so implementers mostly transcribed-and-verified rather than designed. TDD discipline held on all seven (each test confirmed red before the implementation made it green). The two-stage review was where the value showed up: it caught one self-inflicted robustness gap and surfaced (and let me correctly *reject*) a plausible-but-wrong reviewer claim.

Three execution notes worth recording:

1. **One review-driven fix.** Task 1's `_simple_fetch` shipped (per plan) as an unbounded `r.text` read. The quality reviewer flagged that a Brave result URL can point at a PDF/binary/huge page, so the same implementer added a `text/*` content-type gate + 2 MB cap (`bd4add6`). SSRF/redirect-to-metadata was consciously deferred to Phase 3 with a recorded comment — appropriate on a personal machine where the fetch target comes from Brave, not an attacker.

2. **One reviewer false-positive, verified down.** Task 3's quality reviewer rated as *Important* that the upstream `last30days.py` prepends `FIRST_RUN: true` before the JSON, which would make `json.loads` silently discard a valid first-run report. I checked the upstream source directly: the `FIRST_RUN: true` print is gated to the **`compact`** emit branch only (`output_result`, line ~2098); the `--emit=json` branch emits pure `json.dumps(...)`. The claim does not apply to our flags. No speculative parsing was added. (Lesson: adversarial review is high-value, but its findings still get verified against ground truth before acting.)

3. **The plan's Task-6 test had a real bug.** Its `monkeypatch.setattr(cli.date, "today", lambda: d)` raises `TypeError` (can't set attributes on the immutable built-in `date`). This was flagged to the implementer pre-emptively; they used the cleaner fix — `d = date.today()` and drop the monkeypatch, which makes the record/preflight reads agree by construction and is wall-clock-independent. The spec reviewer independently reverted `cli.py` to confirm the test is a genuine red-then-green regression guard, not a tautology.

## 4. Live status

- **Sonar (Stage 1b):** working (carried Phase 1).
- **Brave web (Stage 1b):** newly wired; `BRAVE_API_KEY` present. Unit-validated; not yet exercised end-to-end against the live API (the live e2e run is gated on spend approval — see §6).
- **last30days (Stage 1a): wired but live-blocked by an upstream bug.** Our collector targets the correct plugin path and flags, and the parser is unit-proven against the verified `report.to_dict()` schema. But a live `_subprocess_runner("project management tools")` returns **empty stdout** because the upstream `last30days.py` crashes before emitting JSON:
  ```
  AttributeError: 'NoneType' object has no attribute 'split'
    at last30days.py main(): config.get('INCLUDE_SOURCES', '').split(',')
  ```
  The plugin's config has `INCLUDE_SOURCES` set to an explicit null, so `.get(..., '')` returns `None`. **Our collector degrades safely to `[]`** (covered by `test_collect_returns_empty_on_runner_failure`) — it never crashes the pipeline — but last30 yields nothing live until this is fixed. Fix is upstream/config, not ours: set a non-null `INCLUDE_SOURCES` in `~/.config/last30days/.env`, or patch/​report the plugin. Tracked as a ticket.

Net: live GATHER currently draws on **Sonar + Brave web**; last30 will join once the upstream config is fixed. That still satisfies the Phase-2 "genuinely multi-source" goal (two independent live sources + diagnosable status when one is empty).

## 5. Rollovers (deferred, non-blocking)

None of these block Phase 2. They are the accumulated Minor review nits + the live blocker, kept honest here so they aren't lost.

**Blocker for live last30 yield (external):**
- **last30days upstream `INCLUDE_SOURCES=None` crash** — see §4. Until fixed, last30 contributes zero live evidence (safe-degraded). → ticket filed.

**Code-quality nits (Phase 3 polish; each has a safe failure mode today):**
- *Task 1 / `web.py`* — `_simple_fetch` SSRF/redirect allow-list deferred (comment recorded). `_default_brave_search` doesn't swallow its own HTTP errors (the orchestrator catches them, but the *why* is only on stderr).
- *Task 2 / `gather/__init__.py`* — return annotation is `tuple[EvidenceBundle, dict]`; could tighten to `dict[str, str]`. Optional: echo `gather_status` to the CLI console on empty runs (today it's on stderr + in the session JSON, which already meets "diagnosable"). `len(r)` assumes a sized sequence — true for all real collectors (lists), a contract note only.
- *Task 3 / `last30.py`* — no `proc.kill()` on `asyncio.TimeoutError` (a timed-out child can orphan); stderr is piped then discarded (a one-line breadcrumb would make live failures diagnosable instead of silent); `shutil.which("python3")` resolves system Python, not `sys.executable` — intended (the plugin has its own deps) but undocumented.
- *Task 4 / `pipeline.py`* — `getattr(fr, "cost", 0.0)` is defensive past need (`cost` is now a declared field); a genuine `$0.00` run falls through to the token estimate (conservative — over-records, never under).
- *Task 5 / `fusion.py`* — `error.get("message")` assumes `error` is a dict; a string-typed `error` degrades to `resp.text` via the `except` (safe). No test covers the non-JSON-body branch. 5xx is (correctly) not retried — worth a one-line "why" comment.
- *Task 6 / test* — could add a second assertion seeding a same-month prior-day discovery spend to also regression-guard the *monthly* (not just daily) cross-depletion path.

**Out of scope by design (Phase 3+ per the plan):**
- Extended tier-gated collectors (review sites + competitor-weakness mining, GitHub Issues/Canny/roadmaps, demand/intent, Q&A, trend velocity) + quote-verbatim hardening (WebFetch Sonar citations).
- The `substack` lens (`frame_substack` + handoff into `substack-value-engine`) and the `--segment` creative-signal qualifier (Phase 4).
- Phase-1 Minor punch-list items 5–8 (frame quote-bank positional pairing, Sonar verbatim WebFetch, URL escaping in render, `web_calls` in the estimate).

## 6. Recommended next step

**Live end-to-end run (plan Task 7, Step 6 — gated on spend approval).** A single `quick`-tier run (~$0.50, hard-capped) would confirm three Phase-2 wins at once against the live API: multi-source evidence (Sonar + Brave), non-error `gather_status` per collector in the session JSON, and `usage.cost`-based spend recording. Suggested:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "obsidian plugins" --lens pm --tier quick --output /tmp/p2-ledger.md
```
Expect the session JSON under `/tmp/.discovery-sessions/` to show `gather_status` like `{"sonar": "ok: …", "web": "ok: …", "last30": "error: …"}` (last30 erroring is the known upstream bug, now *visible* rather than silent — which is exactly the diagnosability Phase 2 bought).

Not run autonomously: the plan flags this as spend-gated and asks for Sean's go-ahead first.
