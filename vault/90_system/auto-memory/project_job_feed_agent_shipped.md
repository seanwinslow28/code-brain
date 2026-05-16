---
name: Job-feed agent v1 shipped
description: SDK agent #8 — daily PM/APM role discovery — merged to main 2026-05-11 via PR #33. Replaces "where do I find job postings" friction for Sean's active job hunt.
type: project
originSessionId: 463d778b-c715-4316-8874-5e33f0957a9f
---
Job-feed agent v1 shipped 2026-05-11 (PR #33 merged). Polls 4 free public feeds (RemoteOK, HN "Who's Hiring", web3.career, WeWorkRemotely) + ~40-company ATS watchlist (Greenhouse/Lever/Ashby auto-detect). Rules-filter → Qwen3-14B-on-MBP scoring with `fallback_disabled=true` (no cloud egress) → standalone SQLite at `vault/.job-feed.db` → daily Markdown roll-up at `vault/20_projects/prj-job-hunt-2026/job-feed/<today>.md`. Daily-driver morning brief surfaces top 3 fits.

**Why:** Sean was laid off from The Block 2026-05-04; this agent is the daily discovery layer for his active job hunt. $0/run cost integrity is non-negotiable per his post-layoff budget.

**How to apply:**
- If Sean asks "did I see anything good today" or "what did the job feed find" → check `vault/20_projects/prj-job-hunt-2026/job-feed/<today>.md`
- If he asks to update a posting's status (applied / passed / reviewed) → `PYTHONPATH=agents-sdk agents-sdk/.venv/bin/python3 agents-sdk/scripts/update_status.py <db_id> <status>`
- If he asks to edit the watchlist → `vault/20_projects/prj-job-hunt-2026/job-feed/watchlist.yaml` (user-editable, re-read on every run; no code change needed)
- If he asks why a posting isn't there → query `vault/.job-feed.db` for `source_role_id` to see if it was rules-rejected (with reason) or never fetched
- If the agent appears broken → check `vault/health/job-feed-manifest-<today>.json` for failed pollers + run-by-run state

**Activation gates as of 2026-05-11 merge:**
- launchd schedule: plist at `agents-sdk/schedules/com.sean.job-feed.plist`. Run `agents-sdk/schedules/install_schedules.sh` to actually load it (Sean's call — would schedule 7 fires 8:00–11:00 AM ET starting next day).
- web3.career token: `python3 agents-sdk/lib/keychain.py set web3career_token <token>` (optional; adapter skips cleanly without it).
- MBP-awake dependency: scoring only fires when MBP is reachable during 8–11 AM ET window. MBP-asleep → postings persist with `fit_score=NULL` and carry over to the next run.

**First live-run results (2026-05-11, MBP asleep):** 3922 fetched, 160 rules-passed, 3762 rules-rejected (95.9%), 0 scored. One ATS poll silently failed (`elevenlabs` — empty error in manifest). Roll-up + DB + manifest all wrote correctly. Partial-path verified end-to-end.

**Total scope shipped:** 25 commits, ~2,100 LOC across 7 new lib modules (`job_types`, `job_sources`, `job_rules`, `job_db`, `job_scoring`, `job_renderer` + watchlist parser), 1 agent entrypoint, 1 CLI helper, 1 launchd plist, 1 watchlist seed (~48 companies). +105 new tests (240 baseline → 414 after merge, of which ~69 are job-feed specific and the rest came from skill_optimizer landing on main during the same period). Spec at `docs/superpowers/specs/2026-05-09-job-feed-agent-design.md`. Plan at `docs/superpowers/plans/2026-05-11-job-feed-agent.md`.
