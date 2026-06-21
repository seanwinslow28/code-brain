# Kickoff Prompt — Execute fusion-discovery-council Phase 5 (subagent-driven)

Paste everything inside the fenced block into a fresh Claude Code session. **Branch off the Phase-4 tip** so the substack lens runs on the wider evidence surface: either merge `feat/fusion-discovery-council-phase4` to `main` first and branch `feat/fusion-discovery-council-phase5` off the updated `main` (recommended — Phase 4 is "Ready to merge"), or stack `feat/fusion-discovery-council-phase5` directly on `feat/fusion-discovery-council-phase4`. **Do NOT branch off plain `main`** — Phase 4 (reviews/github/qa collectors + the SSRF hardening) is not yet merged there, and Phase 5's `--segment` task threads through those collectors.

---

```
Phase 5 of fusion-discovery-council is "Substack Lens + Segment Qualifier" — the final planned phase.
It adds `--lens substack` (verified pain points → ranked post angles + a substack-value-engine handoff
brief) and `--segment` (reshape the gather queries toward a target audience). Phases 1–4 shipped:
Phase 4 widened GATHER to six tier-gated collectors (last30 + sonar + web + reviews + github + qa),
hardened the fetch path, and is green at 114 tests / 1 skipped, live-confirmed under cap. Your job:
EXECUTE Phase 5 task by task using subagent-driven development. DO NOT design — the plan carries
complete, current-file-grounded code for every task.

START HERE — read in full before doing anything:
- Plan (source of truth): docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md
  → Read its "Grounding note: PHASE 4 HAS LANDED" block FIRST. The Phase-4-landed-first deltas are
    IN FORCE (the plan's primary code already reflects all six collectors).
- Phase 4 field report (the carry-forward + known-degraded paths you must account for):
  tools/llm-council/council/docs/2026-06-21-fusion-discovery-council-phase4-field-report.md (§5–§7)
- The brief's consumer (so frame_substack emits what this skill actually reads):
  .claude/skills/substack-value-engine/SKILL.md — its Value Gate is Itch / Solution / Transfer.

EXECUTION METHOD:
- Invoke the `superpowers:subagent-driven-development` skill and follow it exactly.
- One fresh subagent per task (Tasks 1–6, IN ORDER). Run strictly sequentially — pipeline.py is
  touched by Tasks 3 + 5 and __main__.py by Tasks 4 + 5, so no parallelism. Each subagent does strict
  TDD (write failing test → run red → minimal code → run green → commit), then returns. Two-stage
  review between tasks (a spec-compliance reader + the Code Reviewer agent), each verifying against the
  real diff, not the implementer's report. Close with a whole-branch review.
- Implement what's written; don't redesign. If something genuinely doesn't work, fix minimally and
  note why in your report.

WHERE THE WORK LIVES:
- Branch `feat/fusion-discovery-council-phase5` off the Phase-4 tip (merged main, or stacked on
  feat/fusion-discovery-council-phase4). Confirm with `git branch --show-current` and confirm the
  Phase-4 collectors are present: `ls tools/llm-council/council/discovery/gather/` should show
  reviews.py, github.py, qa.py. If they're absent you branched off the wrong base — STOP and re-branch.
- All code is in `tools/llm-council/council/discovery/`. Run commands from `tools/llm-council/`.
- TEST COMMAND GOTCHA: it's `uv run --extra dev python -m pytest -v` — plain `uv run pytest` does NOT
  work (pytest is in the `dev` extra). Baseline before you start (Phase 4 landed): 114 passed, 1 skipped.

WHAT PHASE 5 SHIPS (the why, so reviews are sharp):
- Task 1: frame_substack (new frame_substack.py) — reframes each VERIFIED pain point into a PostAngle
  (hook + candidate Value-Gate Itch + Transfer + whitespace + verbatim evidence). Same scoring as
  frame_pm; NO new Fusion call (operates on post-VERIFY points), so substack costs the same as pm.
- Task 2: render_substack (new render_substack.py) — the post-angle idea ledger + the handoff brief.
  The brief pre-fills Itch (slot 1) + Transfer (slot 3) + verbatim evidence and leaves Solution (slot 2)
  for Sean — substack-value-engine runs the gate; the brief scaffolds it, never passes it.
- Task 3: pipeline lens branch — run_discovery branches on lens (substack → frame_substack +
  render_substack_*; pm → unchanged), DiscoveryResult gains brief_markdown, run_discovery gains segment.
- Task 4: CLI writes the brief to a sibling path (...-substack-brief.md) on --lens substack.
- Task 5: --segment qualifier, threaded through ALL SIX collectors (web/sonar/last30 + reviews/github/qa)
  → gather_evidence → run_discovery → CLI. Default "" = today's behavior (every existing test stays green).
- Task 6: docs reconciliation (SKILL.md, CHANGELOG, one CLAUDE.md line) + verification + one live
  substack run.

CARRY-FORWARD FROM PHASE 4 — read these or you'll trip on them:
- THE BIG ONE (Task 5): `--segment` must thread through SIX collectors, not three. Phase 4 added
  reviews/github/qa to gather_evidence's default collectors dict; the plan's Task 5 primary code now
  includes the `segment=""` param + query-shaping for each of reviews.py/github.py/qa.py and a test per
  collector. A `--segment` that only reshapes web/sonar/last30 would silently ignore half the evidence
  surface — do NOT skip the three Phase-4 collectors. The plan's Task-5 "Phase 4 has landed (MANDATORY)"
  callout spells out the exact edits.
- collect_sonar already has `fetch=None` (Phase 4 Task 6) and the orchestrator passes
  `fetch=_simple_fetch`. KEEP both when adding `segment`. sonar.py imports ONLY `extract_quotes` from
  web.py now (Phase 4 final-review M1 dropped the dead `_simple_fetch` import) — do NOT re-add it.
- last30 still yields 0 records live (upstream INCLUDE_SOURCES=null crash; degrades safely). The live
  substack run draws on Sonar + web + reviews + github + qa. Don't treat an empty last30 as a Phase-5 bug.
- The review collector under-yields (~3 records) because Brave collapses the OR'd multi-`site:` query
  (ticket M2, LOW). Correctness is fine — it's yield tuning, NOT Phase-5 scope. If you happen to be in
  reviews.py for the segment edit and want to also fix M2 (fan out to N single-`site:` queries), do it
  as a SEPARATE commit with its own test and call it out — do not silently fold it into the segment work.

NON-NEGOTIABLE CONSTRAINTS:
- The fabrication gate (verify.py) is SACRED — do not touch it. The substack lens consumes the
  ALREADY-VERIFIED pain points (post-VERIFY); every quote/URL in the brief comes from a
  VerifiedPainPoint.supporting_urls. Never re-introduce ungrounded claims.
- Python floor stays >=3.10. Reuse the council spine (client.py/budget.py); no second HTTP client or
  spend file.
- Cost integrity: Phase 5 adds NO billable call (--segment only changes query strings; the lens only
  reframes existing FusionResult output). The substack lens is the same FUSE cost as pm — caps unchanged
  ($0.50/$1.50/$4.00). Never bill a provider and record $0.
- The skill never `git add`s the vault/ directory (CLAUDE.md rule 8). Applies to runtime behavior, not
  your task commits.
- Keep the full suite green on top of each task's new tests.

TASK 6 STEP 5 IS A LIVE RUN: one `quick`-tier `--lens substack` run (~$0.36, same as pm). ASK ME before
running it. Confirm it writes BOTH the substack idea ledger AND the sibling -substack-brief.md, that the
brief's evidence quotes are real fetched-URL substrings (gate held), and that --segment shaped the
queries. The deterministic test suite is the real gate; the live run is confirmation.

DO NOT:
- Do not add demand-intent / trend-velocity / Quora / Canny collectors or the competitor-Substack
  landscape collector — all deferred (spec §13 / Phase-4 §7d).
- Do not weaken the fabrication gate, caps, or the cost-integrity rule.
- Do not re-add the dead _simple_fetch import to sonar.py (Phase 4 M1 removed it on purpose).
- Do not merge to main or open a PR unless I ask. Stay on the feature branch.

When done, give me a short Phase-5 field report: tasks completed, full test count + pass status,
validate.py result, any deviations (and why), and — if you ran the live substack run — the cost, the
verified post-angle count, confirmation that both the ledger and the brief were written, and a spot-check
that the brief's evidence quotes trace to real fetched URLs (gate held).
```

---

## Notes for Sean (not part of the paste)
- **Branch strategy.** Phase 4 is on `feat/fusion-discovery-council-phase4` (114/1, opus whole-branch review said "Ready to merge"). Cleanest: open a PR for Phase 4 → merge to `main` → branch Phase 5 off `main`. That also carries the Phase 4 *and* Phase 5 plans onto `main`. If you'd rather not merge Phase 4 yet, stack Phase 5 directly on the Phase-4 branch — the kickoff handles both; it just forbids branching off plain `main` (where the Phase-4 collectors don't exist).
- **The one real execution risk** is the six-collector `--segment` threading (Task 5). I amended the Phase 5 plan so the reviews/github/qa edits are now primary code with a test each (not a footnote), and added a "Phase 4 has landed (MANDATORY)" callout. The whole-branch review should specifically verify all six collectors honor `segment`.
- **Plan changes I made this session** (so the diff isn't a surprise): de-hypothesized the "if Phase 4 landed" framing throughout, fixed the baseline (93 → 114), folded the three Phase-4 collectors into Task 5's primary code + tests, and noted the carried known-degraded paths (last30 dark, review under-yield). No task was added or removed; scope is unchanged.
- **Spend:** the only spend is the live substack confirmation (~$0.36, agent asks first). Substack lens is the same FUSE cost as pm — no new model call.
- **Optional 30-second unblock** (independent of this phase): set `INCLUDE_SOURCES=reddit,hackernews` in `~/.config/last30days/.env` to turn the dark `last30` source back on before the substack lens draws on the bundle (ticket in `vault/00_inbox/tickets.md`).
- **After Phase 5** lands and live-confirms, the original spec roadmap is complete. Deferred-further items (autonomous/queued mode, Apify depth, demand-intent as query-expansion, trend-velocity, the M2 review yield fix) are catalogued in the Phase-4 field report §7 and the Phase-5 plan's phasing reminder.
