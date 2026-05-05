---
type: handoff
project: prj-job-hunt-2026
status: active
created: 2026-05-04
ai-context: "Resume-here pointer for fresh Claude Code sessions. The Block-to-job-hunt repo migration was completed 2026-05-04 evening across 13 commits on feat/gemini-deep-research-v3.25.0. This file tells the next session where the work landed and what to do next."
---

# Migration Completion + Handoff (2026-05-04)

> **Read this first if you're a fresh Claude Code session pointed at this folder.** The Block-to-job-hunt migration of the repo is **done**. The work-operating-model interview for `job-hunt-2026` is **also done** (2026-05-05; CHANGELOG v3.26.2). Don't re-run either. The next steps are the open work items the interview surfaced (see "Operating-model interview completed" section below) and the master plan's Phase 1 personal-logistics work.

## What was completed (2026-05-04 evening)

The full audit + migration ran in a single session. 13 commits on `feat/gemini-deep-research-v3.25.0`:

| # | Commit | Step |
|---|---|---|
| 1 | `badd489` | Disable daily-driver SDK agent |
| 2 | `fa1415f` | Rewire daily-driver skill for job-hunt + deep-work mode |
| 3 | `9daec0c` | work-operating-model SKILL.md — add `job-hunt-2026` as 4th domain (Path C) |
| 4 | `eddb4a1` | work-operating-model interview-questions.md — Layer 1 Q2 + Q5 |
| 5 | `c4e44ec` | Seed `vault/05_atlas/operating-models/job-hunt-2026/` (5 awaiting-interview placeholders) |
| 6 | `46e18ad` | INTERVIEW-PLAYBOOK + README — add Interview 4, archive Interview 1 |
| 7 | `4d862b9` | `git mv` the-block bundle → `vault/40_archive/operating-models-the-block-2026-05/` |
| 8 | `b0dba5e` | Step 11a — P1 sanitization sweep (Sean-Winslow-Personal-Context, intent-engineering, technical-writing, meeting-prep, the-block/CLAUDE.md banners, etc.) |
| 9 | `161adac` | Step 11b — 8 Block-themed PM skills generalized (crypto-web3-context kept) |
| 10 | `eae934c` | Step 11c — time-management skill full rewrite (5:30 AM / Track A/B/C / 5:30 PM hard stop) |
| 11 | `62563c9` | Step 11d — root CLAUDE.md/README domain table + calendar rule |
| 12 | `ac2c862` | Step 8 — DOMAINS tuple migration across 6 production files + 6 test files |
| 13 | `7a78e35` | Close-out — re-enable agent, dry-run verify, sanitize active operating-models, CHANGELOG v3.26.0, audit-plan resolutions |

## Where the work landed

- **Repo:** `feat/gemini-deep-research-v3.25.0` branch, 13 commits ahead. Not yet pushed; not yet merged to `main`. The branch was already in flight before the migration; the migration commits sit on top of the v3.25.0 Gemini DR work.
- **CHANGELOG:** `CHANGELOG.md` v3.26.0 entry has the full Added / Changed / Migration plan / Counts / Known follow-ups sections.
- **Audit plan with resolutions:** `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-audit-plan.md` — "Open Questions" section now reads "RESOLVED 2026-05-04" with all 8 resolutions inlined (including Sean's override on Q5 — full time-management rewrite vs the audit's defer-recommendation).
- **Migration plan with chunk status:** `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-05-block-to-job-hunt-migration.md` — Chunks 1-4 checkboxes ticked; Chunk 5 (MCP cleanup) deferred to ~5/11 per the plan calendar.

## State of validation gates (as of 2026-05-04 evening)

- `python3 scripts/validate.py`: **PASSED** (60 warnings, all pre-existing secret-pattern false positives in unrelated vendor/example files).
- `cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/`: **284 passed, 2 failed**. The 2 failures are pre-existing WOL test orphans in `tests/test_route_to_macbook.py` from the v3.14.3 WOL drop — unrelated to this migration. Confirmed by stash-test pre-migration.
- `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run`: **clean**. Zero `@theblock.co` references, zero `the-block` paths, zero `_(artifact unavailable)_` for the-block. **Update 2026-05-05:** the `_(artifact unavailable — fall back to general judgment for job-hunt-2026)_` line is now also gone because the `job-hunt-2026/HEARTBEAT.md` is at `status: confirmed` post-interview. 6 job-hunt + deep-work signal mentions confirm Step 1a is loading correctly.

## Operating-model interview completed (2026-05-05)

✅ **DONE.** All 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/` are at `status: confirmed` (CHANGELOG v3.26.2). The agent fleet (daily-driver / meta-agent / flush.py / knowledge_lint Tier 2) will start consuming the populated bundle on next runs.

**Bundle pointers:**
- Synthesis: [[../../05_atlas/operating-models/job-hunt-2026/operating-model|operating-model.md]]
- Operating rhythms: [[../../05_atlas/operating-models/job-hunt-2026/HEARTBEAT|HEARTBEAT.md]]
- Recurring decisions: [[../../05_atlas/operating-models/job-hunt-2026/USER|USER.md]]
- Dependencies + tacit: [[../../05_atlas/operating-models/job-hunt-2026/SOUL|SOUL.md]]
- Friction → schedule rules: [[../../05_atlas/operating-models/job-hunt-2026/schedule-recommendations|schedule-recommendations.md]]

**Tier-A truths locked into SOUL.md** (knowledge_lint Tier 2 will flag contradictions):
1. Walk-away salary = $100,000/yr base; below = auto-no.
2. 5-days-in-office = non-negotiable no.
3. Agents do not message humans on Sean's behalf — drafts only.
4. Track-C MCP (intent-engineering) is the differentiator — protected, even in offer weeks.
5. Friday retro is the only mandatory ritual.

**Relocation override clauses:** Anthropic specifically OR any role with $250k+/yr base override the remote-preferred default.

**9 open work items the bundle surfaced** (these are the actual next moves):
1. **Track-C MCP cold-start chain** — name → repo → README → plan of action. Target ship 2026-05-25 means kickoff this week. Highest priority.
2. **Substack voice + build-in-public format** — both gate the public surface.
3. **Target list of 30 companies** — gates application volume in weeks 3–4.
4. **Agent-fleet audit + Mac-Mini migration** — daily-driver + deep_researcher are keepers; everything else needs an audit pass; anything depending on MBP/Alienware-awake should move to Mac Mini or retire. v3.26.1 fleet reinstall was the start, not the end.
5. **Gmail labeling pipeline** — labels (`recruiter` / `interview-loop` / `reference-request` / `network`) + threads-to-markdown pipe to `vault/30_domains/job-hunt-2026/email/`.
6. **YouTube yes/no decision.**
7. **Second portfolio artifact post-MCP-v0.**
8. **Agent Evals fluency** — needs a concrete learning loop.
9. **Enterprise-level build patterns** — bridge from local prototype to "company would trust me to ship + manage teams."

**North star for automation work** (per schedule-recommendations.md): every automation should free time toward (a) agentic-workflow + agent-harness fundamentals, (b) Agent Evals fluency, (c) enterprise-level build patterns. If a proposed automation doesn't, deprioritize it.

## What to do next (priority order)

### 1. Watch Tuesday 5/5 8:45 AM brief

The first re-enabled run with the new skill. If anything looks off (missing signals, residual Block refs, the brief isn't surfacing job-hunt status), flag it and we adjust. Brief writes to `vault/10_timeline/daily/2026-05-05.md`.

### 2. Master plan Phase 1 (Sean runs this — week 1 logistics)

These are personal logistics, not repo work. Driven by `2026-05-04-onwards-and-upwards-plan.md` Phase 1.

- File MA unemployment claim (target: 2026-05-05)
- ✅ **Severance signed and sent to Leanne 2026-05-05.** Claude review (5-flag analysis covering CIIA Section 5 non-solicit, ADEA exposure if 40+, NY forum-selection, laptop reset, FLSA representation) substituted for paid attorney review given the 2026-05-07 signing deadline. Tenure recalibrated post-CIIA review: ~6 months service starting 11/10/2025, so $8,333.33 = one month is fair, not lowball. Pending: Leanne to send fully counter-signed PDF for the file.
- **401(k) rollover — open Fidelity Rollover IRA THIS WEEK.** $1,398.70 in The Block 401(k) at Fidelity (under Justworks PEO wrap plan). Balance falls in the SECURE 2.0 mandatory force-out band ($1k–$7k → auto-roll to plan's default IRA), so pre-empt by opening Sean's own Rollover IRA at Fidelity (10 min, no funding needed). When Fidelity sends the Distribution Election Notice in 30–90 days, elect "Direct Rollover to IRA" — never a check made out to Sean. Add beneficiaries on NetBenefits while access still works. Confirm vesting in `Justworks_Wrap_Plan_SPD.pdf` — at 6 months tenure, employer match likely 0% vested. Cashing out = ~50% effective tax/penalty hit; don't.
- ACA Marketplace vs COBRA decision (deadline: ~2026-07-03 SEP — but lock by 5/18)
- Runway math at `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/runway-math.md` (file doesn't exist yet)
- Block offboarding logistics (data extraction, equipment return). **Laptop factory reset** (severance Section 8) is a parallel obligation tied to the May 5 separation date — confirm complete or in progress.
- Three Block-named skills (`the-block-jira-ticket-writer`, `etf-page-creator`, `biweekly-jira-update`) **must be scrubbed from the public Superuser Pack repo** before any LinkedIn / public push (CIIA Section 2.3 assigns them as Company Inventions). Either remove from public tree or keep the repo private until cleanup is done. Action gates the Phase 4 / Phase 3 public-announcement work.
- Confirm with Leanne in writing that no equity grants (RSUs, options, ESPP) exist beyond the 401(k) — severance Section 2(c) extinguishes any stock-related claims.

### 3. Master plan Phase 4 — Track-C MCP cold-start (target kickoff this week)

The operating-model interview surfaced this as the highest-priority self-blocking decision. The differentiator artifact is gated on a 4-step chain: **name → repo → README → plan of action.** Target ship date 2026-05-25 (per master plan Phase 4) means the kickoff happens this week, not week 2. This is the first work item the schedule-recommendations.md file will pressure you back about.

### 4. Migration Chunk 5 — MCP cleanup (deferred to ~5/11)

Per the migration plan calendar, week-2 work. Comment out Atlassian + Slack MCP server entries in your MCP config so they don't surface as auth-error tools. Verify `google-workspace` MCP queries no longer hit the Block calendar.

## What's NOT yet done (intentional, post-migration)

- ~~**Interview 4 hasn't run yet.**~~ ✅ DONE 2026-05-05 — see "Operating-model interview completed" section above.
- **Slack overnight scan stays no-op** until Sean has a personal Slack workspace wired in (no decision needed yet — `daily-driver/SKILL.md` Step 1b explicitly handles this).
- **Atlassian + Block calendar MCP cleanup** — Chunk 5 work, deferred to 5/11.
- **Branch not pushed.** Migration + v3.26.1 + v3.26.2 commits are local on `feat/gemini-deep-research-v3.25.0`. Push when ready (`git push origin feat/gemini-deep-research-v3.25.0`); the branch was already remote so there's a tracking relationship.
- **PR not opened.** Open one when ready to merge to `main` (`gh pr create`); the v3.25.0 Gemini DR work + v3.26.0 migration + v3.26.1 fleet reinstall + v3.26.2 operating-model interview ride together.
- **9 open work items from the operating-model interview** — see the "Operating-model interview completed" section above for the prioritized list. Track-C MCP cold-start (item 1) is the most time-sensitive; agent-fleet audit (item 4) is the largest-blast-radius repo work item.

## Where the agents-sdk fleet stands

- **daily-driver SDK agent:** re-enabled 2026-05-04. Next fire: Tue 5/5 8:45 AM. Skill loads creative-studio + life-systems + job-hunt-2026 HEARTBEATs (no the-block).
- **DOMAINS tuple:** `("creative-studio", "life-systems", "job-hunt-2026")` everywhere it appears in `agents-sdk/lib/` and `agents-sdk/agents/`.
- **Other 6 active SDK agents** (vault_indexer, vault_synthesizer, deep_researcher, meta_agent, knowledge_lint, flush): unchanged in scope; their domain iterations now match the new tuple.
- **the-block operating-model bundle:** archived at `vault/40_archive/operating-models-the-block-2026-05/` with a README explaining provenance. Still selectable as a domain argument to `work-operating-model` if Sean ever wants to re-run a historical interview.

## Open questions / known follow-ups for the new session

These don't block anything; just things to keep in mind.

1. **Personal Slack workspace decision** — when (if) Sean wires one up, the `daily-driver/SKILL.md` Step 1b has the historical pattern preserved for re-enable. Just swap in the new user ID.
2. **time-management skill is calibrated to job-hunt mode.** When an offer signs and Sean enters a new role, the skill should be re-rewritten for the new role's rhythms. Don't lock-in the current shape.
3. **`gemini-research-queue.md` and inbox files** show as modified/untracked in `git status`. These are unrelated to this migration — pre-existing concurrent vault writes. Don't include them in any migration-related commit.
4. **Handoff to a different machine** — if Sean works from the Mac Mini or another machine, the launchd plists for the agents-sdk fleet need to be re-installed via `agents-sdk/schedules/install_schedules.sh`. The migration didn't touch the install path.
