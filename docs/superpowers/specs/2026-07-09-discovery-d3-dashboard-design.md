# D3 — Discovery Dashboard + Session-Persistence Fix (Phase 2 Item 3)

**Date:** 2026-07-09
**Status:** Approved (brainstorm with Sean, 3 decisions locked)
**Branch:** `feat/discovery-d3-dashboard`
**Cost:** $0 (no paid calls; dashboard reads local files only)

## Problem

1. **Session persistence leaks (data loss in progress).** `run_discovery()` in
   `tools/llm-council/council/discovery/pipeline.py` only persists a session JSON when the caller
   passes `sessions_dir`, and the empty-bundle early-return (`if not bundle.records:`) writes
   **nothing even when a directory was passed**. The CLI passes `sessions_dir`; direct API/skill
   callers generally don't. Result: only 5 session files exist on disk despite spend ledgers
   showing runs across 7+ days. Every un-persisted run is history we can't recover, and PM3's
   future persistent store needs this history to exist.
2. **No view over run history.** Spend vs caps, verified/dropped trend, citation precision/recall
   (E1), collector yield, and the new E4 `velocity_mode` / `why_now_coverage` (§9 why-now-coverage
   metric) all live in scattered JSONs with no way to see them together.

## Decisions (made with Sean during brainstorm)

| Decision | Choice |
|---|---|
| Slice A fix shape | **Persist by default** — `run_discovery()` resolves a default `sessions_dir` when the caller omits it; explicit `None` disables; empty-bundle path writes too |
| Dashboard home | **`council/discovery/dashboard.py`** inside the tested package, invoked `uv run python -m council.discovery.dashboard` |
| Render tech | **Python-built inline SVG + CSS** — zero JS, self-contained, deterministic, string-assertable in tests |

## Slice A — persist by default (`pipeline.py`)

### Default resolution

`sessions_dir` keeps its keyword slot; default becomes the existing `_UNSET` sentinel (same
pattern as `scorer` / `velocity_provider`):

- `_UNSET` → resolve, in order:
  1. `$DISCOVERY_SESSIONS_DIR` env var, if set (expanded to a `Path`).
  2. Canonical path `<repo-root>/vault/20_projects/research/.discovery-sessions/`, where
     `<repo-root>` is computed from `Path(__file__)` (pipeline.py sits at
     `<repo-root>/tools/llm-council/council/discovery/`). **Guard:** only use this if
     `<repo-root>/vault` exists; otherwise print a one-line stderr warning and skip persistence
     (behave as `None`). Never write to a surprising location when the package is vendored
     elsewhere.
- `None` → explicitly off (existing tests unchanged).
- `Path` → caller's choice (CLI behavior unchanged — it still passes
  `output.parent / ".discovery-sessions"`).

### Write-site unification

Extract one helper `_write_session(sessions_dir, session_id, payload)` carrying the existing
never-crash guard (failed diagnostic write → stderr, never masks the run/spend result). Use it at
all four write sites:

1. **Empty-bundle early-return** (currently writes nothing — the leak) — now persists its session dict.
2. Fuse-failure path.
3. Success path.
4. Post-fuse-failure path.

### Session schema completeness (additive only)

- Empty-bundle session gains `lens`, `tier`, and `cost_usd` (the gather cost — it's real billed
  spend today recorded only in the ledger, not the session).
- **All** session payloads gain `segment` (currently unrecorded; required to reconstruct the
  re-run command in the dashboard).

No fields are removed or renamed; existing consumers are unaffected.

## Slice B — dashboard (`council/discovery/dashboard.py`)

### Command

```
uv run python -m council.discovery.dashboard \
  [--sessions-dir PATH]   # default: canonical vault .discovery-sessions/
  [--spend-dir PATH]      # default: <repo-root>/vault/health/
  --output PATH           # the self-contained HTML file
```

stdlib + click only. No network, no JS, no CDN. $0.

### Readers (tolerant by design)

- **Session reader:** parse every `*.json` in the sessions dir; classify each file:
  - `success` — normal session dict.
  - `failure` — has `failed_stage`.
  - `empty` — has `empty: true`.
  - `foreign` — wrong shape (e.g. `pm3-t0-…json` is an evidence-bundle capture, not a session):
    skipped, listed by filename in the dashboard footer. Never crashes the build.
  - Malformed JSON → skipped + footer note.
  - Missing fields on old runs (pre-E1/E3/E4: no `citation_precision/recall`, `merged_count`,
    `velocity_mode`, `why_now_coverage`, `segment`) render as explicit `n/a (pre-E1 run)` /
    `n/a (pre-E4 run)` markers — never silently zeroed.
- **Spend reader:** `council-spend-*.json` in the spend dir; keep only runs with
  `tool == "discovery"` so council spend never pollutes discovery totals. Ledger date comes from
  the file's `date` field.

### Dashboard sections

1. **Header** — generated-at stamp, total run count, and a global `⚠ thin: N runs` badge whenever
   N < 10 (the honesty rule).
2. **Spend vs caps** — CSS bar per ledger day vs the **$10/day** cap; month-to-date total vs
   **$50/mo**; per-run cost vs its tier's `max_cost_per_run` **imported from `tiers.py`** (caps
   never hardcoded in the dashboard).
3. **Run history table** — date (from session id), topic, lens, tier, segment, evidence count,
   verified / dropped / merged, `verify_mode`, citation precision/recall, `velocity_mode`,
   `why_now_coverage`, cost. Inline-SVG mini-bars for the verified/dropped trend across runs.
4. **Pipeline health** — per-collector yield parsed from `gather_status` strings
   (`"ok: N records (M found)"` — parse defensively, unknown formats render verbatim); FUSE
   success rate = successes / (successes + failures), with each failure's `failed_stage` + error
   text shown.
5. **Re-run affordances** — per run, a copy-ready command block reconstructed from session fields:
   `uv run python -m council.discovery "<topic>" --lens <lens> --tier <tier>
   [--segment "<segment>"] --output <suggested-path>`. Runs missing `segment` (pre-fix) omit the
   flag and carry the n/a marker.
6. **PM3 slot** — visible placeholder: "Pain-taxonomy movement — lands when PM3 persistence ships
   (gated on the 7/21 t1 verdict)."

### Error handling / empty states

- Zero session files → dashboard still renders, with an honest empty state that names the Slice A
  fix and the sessions dir it looked in.
- A ledger day with discovery spend but no matching session (or vice versa) → flagged as a
  discrepancy line in Pipeline health, not papered over.

## Testing (TDD, extends the 326-passed / 1-skipped baseline)

- **Slice A:** default resolution (env var wins; canonical path when vault exists; guard→None +
  warning when it doesn't; explicit `None` stays off; explicit `Path` honored) · empty-bundle
  session now written and carries `lens`/`tier`/`cost_usd` · `segment` present in all four write
  sites' payloads · `_write_session` never raises.
- **Slice B:** reader classification (success/failure/empty/foreign/malformed) · pre-E1/E4 field
  handling (`n/a` markers, no zeros) · spend filtering (`tool=="discovery"` only) · aggregation
  math (daily totals, month-to-date, coverage) · HTML assertions (thin badge, n/a markers, re-run
  command reconstruction, footer skip-list, caps sourced from `tiers.py`).
- Suites: `cd tools/llm-council && uv run pytest tests/ -q` green; `python3 scripts/validate.py`
  PASSED (repo root).

## Out of scope

- `velocity_weight` config/env exposure — already ticketed, do not action.
- PM3 persistence itself — Item 4b spec only, gated on the 7/21 t1 verdict.
- Any paid discovery/validation run.
- Changes to the agent-fleet-observability repo.

## Success criteria (from the campaign runbook)

One command produces the self-contained HTML artifact over the real run history, honestly labeled
when thin; the `sessions_dir` decision is made (persist by default) and the leak is fixed with
tests.
