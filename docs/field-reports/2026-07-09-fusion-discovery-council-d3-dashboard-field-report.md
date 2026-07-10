# Field Report — fusion-discovery-council D3 dashboard + session-persistence fix (Item 3)

**Date:** 2026-07-09
**Branch:** `feat/discovery-d3-dashboard` (off `main` @ 34d54f0)
**Campaign:** Phase 2 "everything buildable now" — **Item 3 of 4** (the observability layer)
**Method:** brainstorming → spec → writing-plans → subagent-driven-development (fresh subagent per task, two-stage review, final whole-branch adversarial review on Fable)
**Tests:** 326 → **366 passed, 1 skipped** (+40). `python3 scripts/validate.py` PASSED (53 pre-existing warnings, none in changed files).
**Cost:** $0 (dashboard reads local files only; the smoke runs were read-only over real vault data).

## What shipped

### Slice A — the leak is fixed (persist by default)
The session store was **sparse by construction**: the empty-bundle early-return in `pipeline.py` wrote nothing even when a directory was passed, and `run_discovery()` defaulted `sessions_dir` to `None`, so every direct API/skill invocation persisted nowhere. Evidence: 5 session files on disk vs 7+ ledger days of real spend. Now:

- `sessions_dir=_UNSET` (the file's existing sentinel idiom) resolves: explicit arg > `$DISCOVERY_SESSIONS_DIR` > canonical `vault/20_projects/research/.discovery-sessions/` — guarded so a vendored checkout warns and skips instead of writing somewhere surprising. Explicit `None` still disables (tests).
- One `_write_session` helper (never raises; a failed diagnostic write can't mask the run or eat the spend record) now serves **all four** write sites, including the empty-bundle path.
- Schema additions (additive only): every payload records `segment` (the re-run affordance needs it); empty sessions gain `lens`/`tier`/`cost_usd`.
- **Hermeticity is load-bearing:** an autouse fixture pins `DISCOVERY_SESSIONS_DIR` to a per-test tmp dir, so the persist-by-default change can never leak test sessions into the real vault. Reviewers verified vault-file counts before/after full-suite runs.

### Slice B — the dashboard
`uv run python -m council.discovery.dashboard --output <path>` renders **one self-contained, zero-JS HTML artifact** (Python-built inline SVG/CSS) over session JSONs + council-spend ledgers:

- Spend vs the **$10/day + $50/mo caps** and per-run cost vs tier caps — all imported from `__main__`/`tiers.py`, never hardcoded.
- Run history with verified/dropped/merged, verify_mode, **citation precision/recall (E1)**, **velocity_mode + why_now_coverage (E4 — the §9 metric)**, cost; SVG mini-bar trends.
- Pipeline health: per-collector yield parsed from `gather_status`, FUSE success rate, failure rows with stage+error.
- **Ledger/session discrepancy flags** — on real data the dashboard shows 6 of them, making the pre-fix leak *visible* (5 ledger days with spend but no session file).
- Copy-ready **re-run commands**: shlex-quoted, absolute-pathed, `cd`-prefixed — paste-safe from any CWD, and the absolute `--output` means a re-run's session lands back in the canonical store.
- **Honesty rules:** `⚠ thin: N runs` badge under 10 runs; missing metrics render `n/a (pre-E1 run)` / `n/a (pre-E4 run)` vintage labels, never fabricated zeros; foreign files (the pm3-t0 bundle capture) and malformed JSON are skipped and named in the footer; a PM3 pain-taxonomy slot is reserved (gated on the 7/21 t1 verdict).
- **Tolerant readers, "never fatal" enforced:** malformed JSON, non-dict payloads, non-string ids, corrupt run entries, non-dict `gather_status` — all skip-and-report instead of crashing (several of these were review-caught, see below).

### Files
- **NEW:** `council/discovery/dashboard.py` (readers + aggregations + CLI), `council/discovery/dashboard_render.py`, `tests/discovery/test_dashboard.py`, `tests/discovery/test_dashboard_render.py`
- **EDIT:** `council/discovery/pipeline.py`, `tests/discovery/test_pipeline.py`, `tests/discovery/conftest.py` (hermetic fixture), `CHANGELOG.md`, `CLAUDE.md`

## Review findings caught + fixed (5 fix waves — the two-stage gate earned its keep)
1. **Task 3 (Important ×3):** the plan's "tolerant" readers crashed on non-dict spend JSON, on non-string session ids, and — after the first fix — on *mixed* string/int ids at the sort. Final shape: non-string-id records classify as foreign (stronger downstream guarantee: `session["id"]` is always `str`). Reviewer independently reproduced each crash and re-verified RED→GREEN against pre-fix code.
2. **Task 4 (Important ×2):** `rerun_command` interpolated topics into double quotes unescaped — a topic containing `"` produced a command-injection-shaped paste (`x"; touch pwned; echo "y`). Fixed with `shlex.quote` + an argv-level injection test. `collector_yield` crashed on a truthy non-dict `gather_status`.
3. **Task 6 (Important):** the CLI's default `--spend-dir` resolution branch had zero coverage — closed with a sandboxed test the reviewer mutation-checked (breaking the resolution makes it fail).
4. **Final review (Important ×2):** `load_spend` still crashed on corrupt entries *inside* `runs` (AttributeError missing from the except tuple); and the re-run affordance emitted a **relative** `--output` with no `cd` — copy-pasting it after `cd tools/llm-council` would have dumped a paid run's ledger into `tools/llm-council/vault/...` and its session outside the canonical store, quietly re-fragmenting the exact history Slice A fixes. Both fixed and re-verified by the final reviewer on the real artifact.

## Notes / carried forward
- **Ticketed follow-up (hardening bundle, non-blocking):** emit `<!doctype>`/`<meta charset>` + explicit UTF-8 on write; renderer type-fragility if a session carries string-typed numerics; day-granular discrepancy matching hides intra-day leaks (2026-06-30: 3 ledger runs, 1 session, no flag); same-topic re-runs share one suggested output filename; empty-gather sessions get a "pre-E3" vintage label though the cause is short-circuit; `DISCOVERY_SESSIONS_DIR=""` can't disable persistence (only `sessions_dir=None` can).
- **Known seam accepted as-is:** `council.budget._spend_dir()` mkdirs on resolve (pre-existing budget.py behavior, inert here) — a future budget.py ticket, not this branch's.
- The dashboard's FUSE success rate reads 100% over the 4-run real sample — true, but the thin badge is doing load-bearing work there; judgment improves as persist-by-default accumulates history.
- Item 4 (PM3 groundwork: pain-key clustering validation + persistence spec) is the campaign's remaining piece; the dashboard's PM3 slot and the now-reliable session store both feed it.
