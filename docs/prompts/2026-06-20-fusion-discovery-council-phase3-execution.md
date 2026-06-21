# Kickoff Prompt — Execute fusion-discovery-council Phase 3 (subagent-driven)

Paste everything inside the fenced block into a fresh Claude Code session opened on branch `feat/fusion-discovery-council`.

---

```
Phase 3 of fusion-discovery-council is "Live Reliability" — make live discovery runs actually
work. Phases 1 and 2 shipped and are green (76 tests), but two live e2e runs both crashed at the
Fusion response-parse step. This phase fixes that and a few bundled nits. Your job: EXECUTE Phase 3
task by task using subagent-driven development.

START HERE — read in full before doing anything:
- Plan (source of truth): docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase3.md
- Context: tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md (§5/§6 are the blockers this phase fixes)

EXECUTION METHOD:
- Invoke the `superpowers:subagent-driven-development` skill and follow it exactly.
- One fresh subagent per task (Tasks 1–6, IN ORDER — they share fusion.py and pipeline.py, so run
  strictly sequentially, no parallelism). Each does strict TDD (write failing test → run red →
  minimal code → run green → commit), then returns. Two-stage review between tasks.
- Every task carries verbatim, current-file-grounded code + tests. Implement what's written; don't
  redesign. If something genuinely doesn't work, fix minimally and note why.

WHERE THE WORK LIVES:
- Confirm you're on `feat/fusion-discovery-council` (`git branch --show-current`); if not, check it out.
- All code is in `tools/llm-council/council/discovery/`. Run commands from `tools/llm-council/`.
- TEST COMMAND GOTCHA: it's `uv run --extra dev python -m pytest -v` — plain `uv run pytest` does
  NOT work (pytest is in the `dev` extra). Baseline before you start: 76 passed, 1 skipped.

WHAT PHASE 3 FIXES (the why, so reviews are sharp):
- Task 1: OpenRouter streams ": OPENROUTER PROCESSING" SSE keep-alive padding on slow Fusion calls,
  even on non-stream requests. fuse()'s `resp.json()` chokes on it → bare JSONDecodeError crash.
  Fix = decode through the padding + tolerate prose-wrapped judge JSON.
- Tasks 2–3: a failed Fusion call BILLS OpenRouter but records $0 locally and leaves no session
  artifact. Fix = FusionError carries the incurred cost (summed across retries); on failure the
  pipeline persists the session JSON (with per-collector gather_status) and the CLI records the spend.
- Task 4: last30 subprocess — kill timed-out children + stderr breadcrumbs so silent-empty runs are
  diagnosable. Task 5: a tiny budget regression test. Task 6: docs + the live e2e payoff.

NON-NEGOTIABLE CONSTRAINTS:
- Python floor stays >=3.10. Reuse the council spine; no second HTTP client or spend file.
- Cost integrity is the theme: never bill OpenRouter and record $0. Every billable run records its cost.
- Fabrication gate (verify.py) is sacred — do not touch it.
- The skill never `git add`s the vault/ directory (CLAUDE.md rule 8). Applies to runtime behavior,
  not your task commits.
- Keep the full suite green on top of each task's new tests.

TASK 6 STEP 5 IS A LIVE RUN (the payoff): it spends ~$0.40–0.50 of real OpenRouter credit to confirm
the SSE fix makes a live `quick` run survive end-to-end. ASK ME before running it. The deterministic
test suite is the real gate; the live run is confirmation. If FUSE still fails for a *different*
reason, that's a finding — capture the new signature, don't paper over it.

DO NOT:
- Do not build Phase 4 (extended collectors) or Phase 5 (substack lens) — deferred.
- Do not add the _simple_fetch SSRF allow-list — consciously deferred to Phase 4 (low-risk: personal
  machine, Brave-sourced URLs).
- Do not merge to main or open a PR unless I ask. Stay on the feature branch.
- Do not weaken caps, the fabrication gate, or the cost-integrity rule.

When done, give me a short Phase-3 field report: tasks completed, full test count + pass status,
validate.py result, any deviations (and why), and — if you ran the live e2e — whether it produced a
real ledger, the recorded cost, and the per-collector gather_status from the session JSON.
```

---

## Notes for Sean (not part of the paste)
- Open the fresh session on `feat/fusion-discovery-council`.
- The live e2e (Task 6 Step 5) is the moment of truth — it confirms the SSE-padding fix end-to-end. The agent is told to ask before spending; ~$0.40–0.50.
- Optional 30-second unblock for last30 live yield: set `INCLUDE_SOURCES=reddit,hackernews` in `~/.config/last30days/.env` (tickets.md line 15). Independent of this code phase — do it whenever.
- After Phase 3 confirms a clean live run, the next plans are Phase 4 (extended collectors) and Phase 5 (substack lens), written against the now-proven live path.
