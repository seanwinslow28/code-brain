# Kickoff Prompt — Execute fusion-discovery-council Phase 4 (subagent-driven)

Paste everything inside the fenced block into a fresh Claude Code session. Branch `feat/fusion-discovery-council-phase4` off the latest `main` (the Phase 1–3 code is merged; the Phase 4/5 plans land on `main` via the plans PR — pull first so the plan doc is present).

---

```
Phase 4 of fusion-discovery-council is "Extended Collectors + Fetch Hardening" — widen Stage-1 GATHER
beyond Sonar + Brave web + last30 with three free, fabrication-gate-compatible collectors, harden the
shared fetch surface, strengthen Sonar evidence to verbatim quotes, and fold two deferred code nits.
Phases 1–3 shipped and are merged to main (93 tests green, live-confirmed $0.36 ledger). Your job:
EXECUTE Phase 4 task by task using subagent-driven development. DO NOT design — the plan carries
complete, current-file-grounded code for every task.

START HERE — read in full before doing anything:
- Plan (source of truth): docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase4.md
- Context: tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase3-field-report.md
  (§7c = the Phase-4 scope; §7b = the two code nits Task 8 folds; §7f = why Task 9 re-checks caps)
- Design spec (the §6 coverage matrix the collectors implement): docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md

EXECUTION METHOD:
- Invoke the `superpowers:subagent-driven-development` skill and follow it exactly.
- One fresh subagent per task (Tasks 1–9, IN ORDER). Run strictly sequentially — Task 1 (SSRF
  hardening of _simple_fetch) MUST precede Tasks 3/6/7 (which widen the fetch surface), and Task 2
  (TierConfig flags) MUST precede Task 7 (the orchestrator reads those flags). Each subagent does
  strict TDD (write failing test → run red → minimal code → run green → commit), then returns.
  Two-stage review between tasks (a spec-compliance reader + the Code Reviewer agent), each verifying
  against the real code, not the implementer's report.
- Implement what's written; don't redesign. If something genuinely doesn't work, fix minimally and
  note why in your report.

WHERE THE WORK LIVES:
- Create + work on `feat/fusion-discovery-council-phase4` (off the latest main, after pulling the plan).
  Confirm with `git branch --show-current`.
- All code is in `tools/llm-council/council/discovery/`. Run commands from `tools/llm-council/`.
- TEST COMMAND GOTCHA: it's `uv run --extra dev python -m pytest -v` — plain `uv run pytest` does NOT
  work (pytest is in the `dev` extra). Baseline before you start: 93 passed, 1 skipped.

WHAT PHASE 4 SHIPS (the why, so reviews are sharp):
- Task 1: SSRF/redirect allow-list in _simple_fetch — per-hop scheme + public-IP validation (blocks
  file://, loopback/private/link-local + the 169.254.169.254 cloud-metadata IP, and redirects INTO
  them). Lands first because the review-sites collector fans the fetch out across a wider URL surface.
- Task 2: TierConfig gains reviews/github/qa flags per spec §6 (standard: reviews+github; deep: +qa).
- Tasks 3–5: three new FREE, gate-compatible collectors — review sites + competitor-weakness mining
  (Brave site-targeted, 1*/2*-biased), GitHub Issues (free Search API), Stack Exchange Q&A (free API).
  Each emits a real URL + a verbatim quote so the fabrication gate stays the sole arbiter.
- Task 6: Sonar verbatim hardening — WebFetch each citation, extract a true substring (falls back to
  the synthesized sentence). Strengthens the Stage-3 gate.
- Task 7: wire the new collectors + the Sonar fetch opt-in into the gather orchestrator, tier-gated.
- Task 8: fold §7b nits — _first_json_object scans forward past a malformed leading object; last30
  timeout → module constant.
- Task 9: cost-integrity regression guard + SKILL.md/CHANGELOG reconciliation + the live cap re-check.

DESIGN DECISIONS ALREADY LOCKED (Sean, in the plan's "Design decisions locked" block — do NOT relitigate):
- 3 collectors only: reviews + competitor-weakness, GitHub Issues, Stack Exchange Q&A. DEFER
  demand-intent (autocomplete has no citable URL → dropped by VERIFY), trend-velocity (no free API),
  Quora (anti-scraping).
- FREE fetch path: Brave site-targeted search + the hardened _simple_fetch. No Firecrawl/Apify.
- Keep caps ($0.50/$1.50/$4.00); Task 9 does a mandatory live standard+deep re-check.

NON-NEGOTIABLE CONSTRAINTS:
- Python floor stays >=3.10. Reuse the council spine (client.py/budget.py); no second HTTP client or
  spend file.
- Cost integrity is the theme: never bill a provider and record $0. All Phase-4 collectors are FREE,
  so no gather-stage billing is introduced — Task 9 locks that with a regression guard + the documented
  threading recipe (gather/__init__.py) for the day a paid collector is added.
- Fabrication gate (verify.py) is SACRED — do not touch it. Every new collector record must carry a
  real fetched URL + a verbatim quote, or its evidence is (correctly) dropped by Stage 3.
- Verified model IDs only: `~google/gemini-pro-latest` (tilde), `mistralai/mistral-medium-3-5`
  (hyphen) — the bare/dotted forms 400. (Phase 4 changes no model IDs.)
- The skill never `git add`s the vault/ directory (CLAUDE.md rule 8). Applies to runtime behavior,
  not your task commits.
- Keep the full suite green on top of each task's new tests.

TASK 9 STEP 6 IS A LIVE RUN (the cap re-check): one `standard` (~$1.50 cap) + one `deep` (~$4.00 cap)
e2e to confirm the wider evidence bundle still lands under each cap. ASK ME before running it (up to
~$5.50 of real OpenRouter credit, likely less). The deterministic test suite is the real gate; the
live run is confirmation. If a tier exceeds its cap, follow the plan's bump procedure (raise that
tier's max_cost_per_run, update test_tiers.py + SKILL.md + CHANGELOG, re-run); if under cap (expected),
leave caps unchanged and record the figures.

ENV NOTE: the repo-root .env has BRAVE_API_KEY (review sites) and GITHUB_TOKEN (raises the GitHub API
rate limit; the collector degrades to unauthenticated without it). Stack Exchange needs no key. last30
is still live-blocked by the upstream INCLUDE_SOURCES=null crash — it degrades safely to []; don't
re-litigate it.

DO NOT:
- Do not build Phase 5 (substack lens + --segment) — that's the next plan
  (docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md), a separate session.
- Do not add demand-intent / trend-velocity / Quora / Canny collectors — deferred by decision.
- Do not introduce a paid scraper (Firecrawl/Apify) — the fetch path is free by decision.
- Do not weaken caps, the fabrication gate, or the cost-integrity rule.
- Do not merge to main or open a PR unless I ask. Stay on the feature branch.

When done, give me a short Phase-4 field report: tasks completed, full test count + pass status,
validate.py result, any deviations (and why), and — if you ran the live cap re-check — the standard
and deep costs, whether each was under cap, and the per-collector gather_status from each session JSON
(confirming reviews/github/qa actually fired).
```

---

## Notes for Sean (not part of the paste)
- The Phase 4 + Phase 5 plans currently live on `feat/fusion-discovery-council-phase4-5-plans`. Merge that to `main` first (PR), then open the execution session off the updated `main` so the plan doc is present — or branch the execution session directly off the plans branch if you'd rather not merge the plans yet.
- **Recommended order: Phase 4 before Phase 5** — Phase 4 widens the evidence surface the substack lens draws on. But Phase 5 can ship independently on today's 2–3 live sources if you want the substack lens sooner (its plan grounds against today's collectors and flags the Phase-4-landed-first deltas inline).
- The live cap re-check (Task 9 Step 6) is the only spend — up to ~$5.50, likely less. The agent asks first. All new collectors are free; the only paid stage is still FUSE.
- Optional 30-second unblock for last30 live yield (independent of this phase): set `INCLUDE_SOURCES=reddit,hackernews` in `~/.config/last30days/.env` (tickets.md). Resolving it before Phase 4 turns GATHER from 2 live sources into 3 before the collector fan-out widens.
- After Phase 4 confirms caps live, run Phase 5 in its own fresh session with `docs/prompts/2026-06-20-fusion-discovery-council-phase5-execution.md` (write a sibling kickoff in that shape when you're ready, or reuse this one's structure).
