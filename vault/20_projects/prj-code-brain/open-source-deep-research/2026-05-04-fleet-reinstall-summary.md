---
type: implementation-summary
date: 2026-05-05
filename-date: 2026-05-04
host: Seans-Mac-mini.local
branch: feat/gemini-deep-research-v3.25.0
plan: "[[2026-05-04-fleet-reinstall-plan]]"
status: complete
---

# SDK Agent Fleet Reinstall — Execution Summary

> **Plan:** [[2026-05-04-fleet-reinstall-plan]] (filename uses `2026-05-04`; execution happened on **2026-05-05** at 15:33 → 16:02 ET).

## TL;DR

7 launchd jobs are now loaded on the Mac Mini: 6 active SDK agents + 1 LDR persistent service daemon. The `deep_researcher` smoke-test for Topic 1a wrote a real 11 KB report at `2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md` in 280 s wall-clock at $0.00 cost. The next 02:45 cron is wired and will fire on **2026-05-06**.

## What changed

### Commits on `feat/gemini-deep-research-v3.25.0`

| SHA | Subject |
|---|---|
| `a8fda22` | `chore(agents-sdk): remove 6 stale launchd plists` |
| `c37d018` | `feat(agents-sdk): add LDR web daemon as persistent launchd service` |
| `23a47c1` | `chore(agents-sdk): record fleet reinstall + LDR service daemon (v3.26.1)` |

Branch is now **28 commits ahead of `main`**, all local — not pushed (per plan constraint).

### Files

**Deleted from repo (6):**
```
agents-sdk/schedules/com.sean.agent.daily-evening.plist
agents-sdk/schedules/com.sean.agent.daily-morning-baton.plist
agents-sdk/schedules/com.sean.agent.pr-digest.plist
agents-sdk/schedules/com.sean.agent.process-inbox.plist
agents-sdk/schedules/com.sean.agent.sprint-health.plist
agents-sdk/schedules/com.sean.agent.weekly-review.plist
```

**Added to repo (1):**
```
agents-sdk/schedules/com.sean.service.ldr-web.plist
```

**Symlink removed (1):**
```
~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist
```

**Doc updated (1):**
```
CHANGELOG.md — new ## [3.26.1] - 2026-05-05 section
```

CLAUDE.md and README.md unchanged: the active-agent count (7 of 14: 5 launchd + daily-morning + hook-triggered flush) remains correct.

## Currently loaded launchd jobs

```
launchctl list | grep "com.sean."
-       0       com.sean.agent.daily-morning
-       0       com.sean.agent.deep-researcher
-       0       com.sean.agent.knowledge-lint
-       0       com.sean.agent.meta-agent
-       0       com.sean.agent.vault-indexer
-       0       com.sean.agent.vault-synthesizer
63936   0       com.sean.service.ldr-web
```

`gemini-researcher` correctly skipped (default disabled, opt-in via `INSTALL_GEMINI=1`).

## Stack health

- **Ollama** `:11434` — running (`qwen3-14b-research:latest` and 5 other models available)
- **SearXNG** `:8080` — Docker container `searxng`, restart=`unless-stopped`, Up since 2026-05-03T15:24Z; returns 27 results for test query
- **LDR** `:5050` — persistent via `com.sean.service.ldr-web` plist, PID 63936, `/api/v1/health` returns `ok`, KeepAlive=true means launchd auto-respawns on crash, RunAtLoad=true means survives reboot

## What to expect at 02:45 on 2026-05-06

- `deep-researcher` fires → reads `vault/00_inbox/research-queue.md` → picks the next unchecked item, which is now **Topic 1b** (CLI-driven agentic-workflow repo audit + pinning patterns + Gemini CLI extensions). Topic 1a was consumed by today's smoke test.
- LDR proxy + SearXNG already up.
- Expected wall-clock: 5–10 min based on tonight's 280 s baseline for a similarly-shaped topic.
- Output lands at `vault/20_projects/research/2026-05-06-{slug}.md`.
- Daily-note digest will likely be `skipped-no-note` because `2026-05-06.md` doesn't exist yet at 02:45 (daily-driver morning creates it at 08:45). This is the normal pattern for cron-fired runs and is not a regression. The research file itself is the canonical artifact.

## Other agents firing tomorrow

| Time | Agent | What it does |
|------|-------|--------------|
| 02:00 | `vault-indexer` | Local Ollama `nomic-embed-text` over the vault → SQLite chunks DB |
| 02:30 | `vault-synthesizer` | Concept + connection articles via Qwen3-14B on MBP if awake; succeeds intermittently per CLAUDE.md |
| 02:45 | `deep-researcher` | Topic 1b from research-queue (see above) |
| 06:30 | `meta-agent` | Fleet health + domain-aware insights via gemma4:e4b on Mac Mini |
| 08:45 | `daily-morning` | Daily-driver morning brief — now repointed at job-hunt + deep-work signals (Step 1a) per migration commit `7a78e35` |

## Verification commands to run tomorrow morning

```bash
# Did everything fire?
tail -3 vault/90_system/agent-logs/agent-run-history.csv
ls -la vault/20_projects/research/2026-05-06-*.md
ls -la vault/90_system/agent-logs/vault-indexer-2026-05-06.log
grep -c "^- \[ \]" vault/00_inbox/research-queue.md   # should be one fewer than yesterday

# LDR daemon survived overnight?
launchctl list | grep com.sean.service.ldr-web   # PID column should be a number, not -

# Daily-driver brief landed?
cat vault/10_timeline/daily/2026-05-06.md | head -50
```

## What surprised me during execution

1. **The prior session's diagnosis port (`:8888`) was wrong.** SearXNG runs on `:8080` per the migration plan. Sub-plan D shrunk from "install SearXNG" to "verify and confirm Docker auto-start."
2. **The repo was already further along than the prompt said.** The user prompt described 11 commits ahead of main and `daily_driver.enabled=false`; reality at session start was 18 commits and Sean's `7a78e35` had already re-enabled daily_driver. By the time I committed Sub-plan A, the branch was 25+ ahead. I updated the plan inline before executing.
3. **LDR was the actual silent gap, not the launchd plists.** Even with all 6 SDK agents loaded, the 02:45 cron would have failed if LDR happened to be down — and LDR was being started by hand from a foreground terminal that exited overnight. Building `com.sean.service.ldr-web.plist` with `KeepAlive=true` is the durable fix and turns LDR into a fleet-grade dependency.
4. **`ldr-web --help` doesn't print help — it starts the server.** A small footgun. The bash 2-min timeout cleaned up after the inadvertent foreground start.
5. **`launchctl print` shows two `PATH` entries per job** (inherited launchd-default + user-supplied EnvironmentVariables override). The user-supplied one wins at exec time. Spot-checking with a too-narrow grep made it look like the BUGFIX-2026-04-07 PATH was missing — it wasn't.

## Punch list (open items, not blockers for tonight)

- **`install_schedules.sh` final-echo line** still says `Verify with: launchctl list | grep com.sean.agent` — should probably say `com.sean\.` to also surface the service. Not changed in this plan to keep the script untouched per Sub-plan C's recommendation. Trivial follow-up.
- **Docker Desktop auto-start at login** — not verified during this run. If Docker is not in macOS Login Items, SearXNG will be unavailable on reboot until Sean opens Docker manually. Recommend toggling "Start Docker Desktop when you log in" in Docker preferences.
- **Daily-note digest skip pattern at 02:45** — research files land successfully but the digest line gets skipped because the day's note doesn't yet exist. Could be addressed by either creating the note skeleton at 02:00 (extend `vault-indexer` or a new tiny job) or by having `deep-researcher` create the file lazily when missing. Out of scope for this plan; flag for future thought.
- **One leftover ldr-mcp-wrapper.py instances** — 6 idle wrapper PIDs from interactive sessions earlier today are still running (`9:06AM`, `10:31AM`, `3:10PM`). Harmless but a tidy-up opportunity (`pkill -f ldr-mcp-wrapper`).
- **Topic 1b auto-fire tomorrow** — Topic 1b's question text references repos at GitHub URLs and asks the LDR run to fetch maintenance-signal data. SearXNG can return search results but won't run `git log` against private/recent commits. Topic 1b's quality may be uneven; expect a partial-fidelity report.

## Validation checklist (final)

- [x] `launchctl list | grep "sean.agent" | wc -l` returns `6` (active SDK agents).
- [x] `launchctl list | grep "sean.service" | wc -l` returns `1` (LDR daemon).
- [x] `vault/20_projects/research/2026-05-05-*.md` includes the smoke-test file (11,284 bytes, contains `mcp` + `sdk` + `toolkit` in slug).
- [x] Topic 1a in `vault/00_inbox/research-queue.md` is `- [x]` with timestamp + wikilink (verified via `grep -c "^- \[x\] Topic 1a"` returns 1, `grep -c "^- \[ \] Topic 1a"` returns 0).
- [x] CSV row `2026-05-05,16:02:01,deep-researcher,queue,success,0.0000,...` recorded.
- [x] No paid API calls (`agent-run-history.csv` shows the smoke test at $0.00; no Gemini calls in this session).
- [x] No `git push` happened.
- [x] `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` is gone.
- [x] `agents-sdk/schedules/` contains 8 plists (7 agent + 1 service).
- [x] CHANGELOG.md updated with v3.26.1 entry.
- [x] CLAUDE.md and README.md verified — no count change required.
- [x] LDR persistent across reboot (`KeepAlive=true`, `RunAtLoad=true`).
- [ ] Daily-note digest pattern note logged for future thought (above).

## Resume-here

Tomorrow morning, run the verification commands above. If anything in the punch list bites, surface it and decide whether to address inline or defer.
