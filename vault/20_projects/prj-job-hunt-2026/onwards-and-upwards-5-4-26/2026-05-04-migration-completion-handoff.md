---
type: handoff
project: prj-job-hunt-2026
status: active
created: 2026-05-04
ai-context: "Resume-here pointer for fresh Claude Code sessions. The Block-to-job-hunt repo migration was completed 2026-05-04 evening across 13 commits on feat/gemini-deep-research-v3.25.0. This file tells the next session where the work landed and what to do next."
---

# Migration Completion + Handoff (2026-05-04)

> **Read this first if you're a fresh Claude Code session pointed at this folder.** The Block-to-job-hunt migration of the repo is **done**. Don't re-run any of it. The next human-in-the-loop step is the work-operating-model interview for `job-hunt-2026` (~45 min interactive).

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
- `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run`: **clean**. Zero `@theblock.co` references, zero `the-block` paths, zero `_(artifact unavailable)_` for the-block. One expected `_(artifact unavailable — fall back to general judgment for job-hunt-2026)_` line because the `job-hunt-2026/HEARTBEAT.md` is at `status: awaiting-interview` until you run the interview. 6 job-hunt + deep-work signal mentions confirm Step 1a is loading correctly.

## What to do next (priority order)

### 1. Run Interview 4 — `job-hunt-2026` operating model (~45 min interactive)

Open `vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md` → "Interview 4 — Job Hunt 2026" section → paste the **start prompt** into a fresh Claude Code session. Walk all 5 layers with checkpoints (summarize → confirm → write per layer). Skill writes 5 artifacts at `vault/05_atlas/operating-models/job-hunt-2026/`, status moves `awaiting-interview` → `draft` → `confirmed`.

Then paste the **commit prompt** to stage + commit + push the interview output. Then paste the **cross-check prompt** to verify the morning brief picks up the populated HEARTBEAT body and emits zero unavailable lines.

### 2. Watch Tuesday 5/5 8:45 AM brief

The first re-enabled run with the new skill. If anything looks off (missing signals, residual Block refs, the brief isn't surfacing job-hunt status), flag it and we adjust. Brief writes to `vault/10_timeline/daily/2026-05-05.md`.

### 3. Master plan Phase 1 (Sean runs this — week 1 logistics)

These are personal logistics, not repo work. Driven by `2026-05-04-onwards-and-upwards-plan.md` Phase 1.

- File MA unemployment claim (target: 2026-05-05)
- Severance review with MA employment attorney (deadline: ~2026-05-11)
- ACA Marketplace vs COBRA decision (deadline: ~2026-07-03 SEP — but lock by 5/18)
- Runway math at `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/runway-math.md` (file doesn't exist yet)
- Block offboarding logistics (data extraction, equipment return)

### 4. Migration Chunk 5 — MCP cleanup (deferred to ~5/11)

Per the migration plan calendar, week-2 work. Comment out Atlassian + Slack MCP server entries in your MCP config so they don't surface as auth-error tools. Verify `google-workspace` MCP queries no longer hit the Block calendar.

## What's NOT yet done (intentional, post-migration)

- **Interview 4 hasn't run yet.** Until you run it, the daily-driver morning brief gets job-hunt context from `vault/20_projects/prj-job-hunt-2026/README.md` Status section instead of from the HEARTBEAT body. That's fine — the README is populated.
- **Slack overnight scan stays no-op** until Sean has a personal Slack workspace wired in (no decision needed yet — `daily-driver/SKILL.md` Step 1b explicitly handles this).
- **Atlassian + Block calendar MCP cleanup** — Chunk 5 work, deferred to 5/11.
- **Branch not pushed.** 13 migration commits are local on `feat/gemini-deep-research-v3.25.0`. Push when ready (`git push origin feat/gemini-deep-research-v3.25.0`); the branch was already remote so there's a tracking relationship.
- **PR not opened.** Open one when ready to merge to `main` (`gh pr create`); the v3.25.0 Gemini DR work + this v3.26.0 migration ride together.

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
