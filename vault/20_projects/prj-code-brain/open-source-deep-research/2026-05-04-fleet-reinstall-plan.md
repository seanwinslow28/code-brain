---
type: implementation-plan
date: 2026-05-05
filename-date: 2026-05-04
status: approved-pending-execution
host: Seans-Mac-mini.local
branch: feat/gemini-deep-research-v3.25.0
related:
  - "[[phase-4-night-1-2026-05-03]]"
  - "[[macmini-migration-plan-2026-05-02]]"
  - "[[2026-05-04-deep-researcher-fleet-reinstall-prompt]]"
  - "[[2026-05-04-migration-completion-handoff]]"
---

> **Note on dates:** The plan filename uses `2026-05-04` per the user's specified path. Plan execution actually happens on **2026-05-05** (verified `date` = `2026-05-05 15:33`). Smoke-test deliverable file (Sub-plan F) will be dated **2026-05-05**. The "next 02:45 cron fire" target is **02:45 on 2026-05-06**.

# SDK Agent Fleet Reinstall on Mac Mini — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline checkpointed execution) or superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore autonomous operation of the launchd-scheduled SDK agents on `Seans-Mac-mini.local` so `deep_researcher` fires at 02:45 on 2026-05-05 and processes Topic 1a from `vault/00_inbox/research-queue.md`. Surface and remove stale-plist drift in the repo. Do not re-enable any disabled agent.

**Architecture:** Symlink-based launchd installation (existing `install_schedules.sh` pattern). Surgical fixes: delete 6 stale plists from the repo, remove 1 dangling LaunchAgents symlink, run `install_schedules.sh` to load the correct active set, smoke-test `deep_researcher` end-to-end before walking away. SearXNG and LDR are already healthy on this host; no stack-level work is required.

**Tech Stack:** macOS launchd, Bash, Python 3.13 (`agents-sdk/.venv`), Docker (SearXNG), Ollama (`localhost:11434`), LDR proxy (`localhost:5050`), Obsidian vault.

---

## Diagnosis-Disagreement Note (read first)

The prior session's handoff is mostly correct but has five concrete disagreements with the actual on-host state verified at the start of this plan. Surfacing them so the plan operates against reality, not the handoff text.

| # | Prior session said | Reality on Seans-Mac-mini.local (verified 2026-05-04) | Plan impact |
|---|---|---|---|
| D1 | SearXNG runs on `:8888` | SearXNG runs on **`:8080`** (Docker container `searxng`, image `searxng/searxng:latest`, restart=`unless-stopped`, Up 30 hours, `Started: 2026-05-03T15:24:33Z`) | Sub-plan D shrinks: just verify, do not install. |
| D2 | SearXNG NOT listening | SearXNG **IS** healthy. `curl localhost:8080/search?q=qwen3&format=json` returned 20 results, HTTP 200 | Sub-plan D shrinks. |
| D3 | Repo has 12 plists | Repo has **13** plists in `agents-sdk/schedules/` | Stale-cleanup count unchanged (6) — extra plist is `gemini-researcher.plist` (intentional, gated). |
| D4 | Branch 11 commits ahead of main | Branch is **18** commits ahead | No plan impact. Surfaced for situational awareness. The repo on this Mac Mini is further along than the prior handoff captured. |
| D5 | Daily-driver morning is "active" per CLAUDE.md → load it tonight | **Updated 2026-05-05:** Sean confirmed Migration Chunks 1–4 are DONE. Commit `7a78e35` flipped `[agents.daily_driver].enabled = true`. The job-hunt-2026 operating-model artifacts exist. The daily-driver SKILL.md is repointed at job-hunt + deep-work mode. | **Sub-plan E loads 6 active plists** (5 + daily-morning). CLAUDE.md's "7 of 14 active" is correct (5 launchd + daily-morning + flush hook). |

Confirmed (matches prior session):
- `hostname` → `Seans-Mac-mini.local`
- `launchctl list | grep sean.agent` → empty
- `~/Library/LaunchAgents/` contains exactly one stale `sean.agent.*` symlink: `com.sean.agent.meeting-defender.plist` (April 18, dangling — target deleted in v3.17.0 Phase 3)
- LDR proxy on `:5050` healthy: `{"message":"API is running","status":"ok"}`
- Ollama on `:11434` healthy
- The 6 stale plists in the repo: `daily-evening`, `daily-morning-baton`, `pr-digest`, `process-inbox`, `sprint-health`, `weekly-review`
- The 2026-05-04 research file already at `vault/20_projects/research/2026-05-04-you-are-a-senior-research-analyst-specializing-in-ai-develop.md` is a **paid Gemini DR run** from 17:22 today ($2.80, per `agent-run-history.csv`). It is NOT a deep_researcher / LDR auto-fire. Topic 1a is still unprocessed.

---

## 1. Inventory & Invariants

### Source-of-truth ranking
1. **`agents-sdk/config.toml`** `[agents.<name>] enabled` — operational truth (today's state).
2. **`CLAUDE.md`** Active Agents table — design intent (slightly stale: cites 7 active but `daily_driver` is temporarily off).
3. **`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`** — historical justification for the 6 disabled.
4. **`agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`** — process-inbox pause history.

### Full agent inventory (14 SDK agents per CLAUDE.md)

| # | Agent | enabled in config.toml | plist in repo | symlinked now | launchctl loaded now | should be loaded after this plan | Action |
|---|---|---|---|---|---|---|---|
| 1 | `vault_indexer` | `true` | ✅ `vault-indexer.plist` | ❌ | ❌ | ✅ | INSTALL (E) |
| 2 | `vault_synthesizer` | `true` | ✅ `vault-synthesizer.plist` | ❌ | ❌ | ✅ | INSTALL (E) |
| 3 | `deep_researcher` | `true` | ✅ `deep-researcher.plist` | ❌ | ❌ | ✅ | INSTALL (E) + smoke-test (F) |
| 4 | `meta_agent` | `true` | ✅ `meta-agent.plist` | ❌ | ❌ | ✅ | INSTALL (E) |
| 5 | `knowledge_lint` | `true` | ✅ `knowledge-lint.plist` | ❌ | ❌ | ✅ | INSTALL (E) |
| 6 | `daily_driver` (morning) | **`true`** (re-enabled in `7a78e35`) | ✅ `daily-morning.plist` | ❌ | ❌ | ✅ | INSTALL (E) — fires productively at 8:45 AM 2026-05-06 |
| 7 | `flush` (hook-triggered) | `true` | n/a (not a launchd job) | n/a | n/a | n/a | n/a |
| 8 | `gemini_researcher` | `false` (intentional) | ✅ `gemini-researcher.plist` | ❌ | ❌ | ❌ | KEEP plist (gated by `INSTALL_GEMINI=1`) |
| 9 | `process_inbox` | `false` (paused) | ⚠️ `process-inbox.plist` (still in repo) | ❌ | ❌ | ❌ | DELETE plist (A) |
| 10 | `daily_driver` (evening) | `false` (disabled) | ⚠️ `daily-evening.plist` | ❌ | ❌ | ❌ | DELETE plist (A) |
| 11 | `daily_driver` (weekly) | n/a | ⚠️ `weekly-review.plist` | ❌ | ❌ | ❌ | DELETE plist (A) |
| 12 | `pr_digest` | `false` (disabled) | ⚠️ `pr-digest.plist` | ❌ | ❌ | ❌ | DELETE plist (A) |
| 13 | `sprint_health` | `false` (dormant) | ⚠️ `sprint-health.plist` | ❌ | ❌ | ❌ | DELETE plist (A) |
| 14 | `meeting_defender` | n/a (deleted v3.17.0) | ❌ (already deleted) | ⚠️ DANGLING SYMLINK | ❌ | ❌ | DELETE symlink (B) |
| — | `daily-morning-baton.plist` | n/a | ⚠️ `daily-morning-baton.plist` | ❌ | ❌ | ❌ | DELETE plist (A) |
| — | `spending_analysis` / `health_audit` / `md_to_anki` / `preserve_session` | `false` | ❌ (no plist) | n/a | n/a | n/a | n/a — manual-only |

**Net active launchd jobs after this plan: 6** (vault-indexer, vault-synthesizer, deep-researcher, meta-agent, knowledge-lint, daily-morning). Daily-driver was re-enabled in commit `7a78e35` after Chunks 1–4 of the Block-to-job-hunt migration shipped. CLAUDE.md's "7 of 14 active" is correct (the 7th is hook-triggered `flush`).

### Invariants the plan must preserve
- **Hostname check:** Each `Bash` step that touches launchd or symlinks must verify `hostname` first. No silent execution on the wrong host.
- **No paid API calls.** Gemini DR / DR Max / cloud-Sonnet runs are forbidden in this plan.
- **No git push.** No `git push origin feat/gemini-deep-research-v3.25.0`. Local commits OK.
- **No re-enabling of disabled agents.** Deletion of stale plists is the action, not flipping `enabled` flags back on.
- **No edits to `agents-sdk/agents/deep_researcher.py`.** It's the v3.23.0 soak version.
- **No `--no-verify`** on commits.
- **`launchctl print` over `launchctl list`** for spot-checks where richer output helps.

---

## 2. Sub-plan A — Stale Repo Plist Cleanup

**Goal:** Delete 6 stale plists from `agents-sdk/schedules/` so `install_schedules.sh` cannot accidentally re-install them. Net delta: 13 → 7 plists in the directory (the 5 active + `daily-morning.plist` kept-for-future + `gemini-researcher.plist` gated).

### Files to delete with citations

| Plist | Citation | Quote |
|---|---|---|
| `com.sean.agent.daily-evening.plist` | `AUDIT-2026-04-09-agent-downsizing.md` §"daily-driver (evening) — DISABLED (noisy failures)" | "0/6 success rate (April 1–9). Same `CLIConnectionError` as process-inbox. Even if fixed, the evening wrap-up is better done interactively." |
| `com.sean.agent.daily-morning-baton.plist` | Not present in CLAUDE.md active set; no `[agents.daily_driver_baton]` config block exists in `config.toml`; no run history in `agent-run-history.csv` | Orphaned plist with no config-side existence. PATH fix BUGFIX-2026-04-07 added it but it never had a corresponding agent code path turned on. |
| `com.sean.agent.pr-digest.plist` | `AUDIT-2026-04-09-agent-downsizing.md` §"pr-digest — DISABLED (unreliable, low value)" | "1/3 success rate. `gh CLI not available`. Sean's personal repos rarely have open PRs. The one successful run found nothing." |
| `com.sean.agent.process-inbox.plist` | `AUDIT-2026-04-28-process-inbox-reenable.md` + `config.toml:43-65` | "DISABLED 2026-04-29 pending Path B rewrite. Cloud-Sonnet path validated as functionally working but cost-inefficient: ~$1.50-$1.80/run for ~3 files." `enabled = false` confirmed in config.toml. |
| `com.sean.agent.sprint-health.plist` | `AUDIT-2026-04-09-agent-downsizing.md` §"sprint-health — DISABLED (never produced output)" + `config.toml:67-76` | "0/1 success. Likely the same CLIConnectionError but crashes before even logging the error. Never produced a single sprint health report." `project_key = "TBD"` since 2026-05-04 layoff. |
| `com.sean.agent.weekly-review.plist` | `AUDIT-2026-04-09-agent-downsizing.md` §"daily-driver (weekly) — DISABLED (no evidence of working)" | "No logs found in the entire audit period. Either never triggered or crashed silently." |

### KEEP-FOR-NOW

- `com.sean.agent.daily-morning.plist` — kept because `daily_driver` re-enables on 2026-05-05 PM after Chunk 2 ships. Deleting and recommitting it tomorrow is needless churn.
- `com.sean.agent.gemini-researcher.plist` — intentional, default-disabled, opt-in via `INSTALL_GEMINI=1`. Hands-off per constraints.

### Steps

- [ ] **A.1 — Confirm hostname.**

```bash
hostname
```
Expected: `Seans-Mac-mini.local`

- [ ] **A.2 — Re-confirm no stale plist is currently symlinked into LaunchAgents.** (Belt-and-suspenders. Should be true based on initial diagnosis.)

```bash
ls -la ~/Library/LaunchAgents/ | grep -E "daily-evening|daily-morning-baton|pr-digest|process-inbox|sprint-health|weekly-review"
```
Expected: empty output (no matches). If anything matches, STOP and surface — Sub-plan B's scope expands.

- [ ] **A.3 — Delete the 6 stale plists from the repo.**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git rm agents-sdk/schedules/com.sean.agent.daily-evening.plist \
       agents-sdk/schedules/com.sean.agent.daily-morning-baton.plist \
       agents-sdk/schedules/com.sean.agent.pr-digest.plist \
       agents-sdk/schedules/com.sean.agent.process-inbox.plist \
       agents-sdk/schedules/com.sean.agent.sprint-health.plist \
       agents-sdk/schedules/com.sean.agent.weekly-review.plist
```

- [ ] **A.4 — Verify post-deletion plist count is 7.**

```bash
ls agents-sdk/schedules/*.plist | wc -l
```
Expected: `7` (daily-morning, deep-researcher, gemini-researcher, knowledge-lint, meta-agent, vault-indexer, vault-synthesizer).

- [ ] **A.5 — Stage and commit (commit only, no push).** Pause here for Sean to confirm the diff is clean. This is the "review checkpoint" between A and B.

```bash
git status
git diff --cached --stat
```
Then once Sean OKs:
```bash
git commit -m "$(cat <<'EOF'
chore(agents-sdk): remove 6 stale launchd plists

Deletes plists for agents disabled per AUDIT-2026-04-09-agent-downsizing.md
(daily-evening, daily-morning-baton, pr-digest, sprint-health, weekly-review)
and AUDIT-2026-04-28-process-inbox-reenable.md (process-inbox, paused
2026-04-29 pending Path B local-gemma4:e4b rewrite).

After this commit install_schedules.sh installs only the 5 currently-active
launchd jobs + gemini-researcher (gated) + daily-morning (kept for re-enable
on 2026-05-05 after the Block-to-job-hunt Chunk 2 migration ships).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### A — Rollback

If a deletion was wrong:
```bash
git checkout HEAD~1 -- agents-sdk/schedules/com.sean.agent.<name>.plist
git commit -m "Revert: restore <name>.plist"
```
The old commit hash is recoverable via `git reflog`.

### A — Checkpoint to Sean

After A.5: report what was deleted, confirm git diff matches expected, surface any surprises (e.g., did `git rm` find all 6 files, were any missing).

---

## 3. Sub-plan B — Dangling Symlink Cleanup

**Goal:** Remove the orphaned `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` symlink. The target plist file was deleted from the repo in v3.17.0 Phase 3, leaving the symlink dangling. It's not loaded (confirmed by `launchctl list`), but it's noise that confuses future audits.

### Steps

- [ ] **B.1 — Confirm the symlink is dangling and not loaded.**

```bash
ls -la ~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist
launchctl list | grep meeting-defender || echo "NOT_LOADED"
```
Expected: symlink exists, target nonexistent, launchctl reports `NOT_LOADED`.

- [ ] **B.2 — Try `launchctl unload` defensively (no-op if not loaded).**

```bash
launchctl unload ~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist 2>&1 || true
```
Expected: harmless error or silent success. We're being polite to launchd.

- [ ] **B.3 — Remove the symlink.**

```bash
rm ~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist
```

- [ ] **B.4 — Verify gone.**

```bash
ls -la ~/Library/LaunchAgents/ | grep "sean.agent" || echo "NO_SEAN_AGENT_SYMLINKS"
```
Expected: `NO_SEAN_AGENT_SYMLINKS` (we haven't run install_schedules.sh yet).

### B — Rollback

The symlink target is already deleted from the repo in v3.17.0 Phase 3, so there's nothing to roll back to. If for some reason the symlink needs to come back: `git show v3.16.0:agents-sdk/schedules/com.sean.agent.meeting-defender.plist` to recover the historical content, then write to disk and resymlink.

### B — Checkpoint to Sean

After B.4: confirm `launchctl list | grep sean.agent` still empty and `~/Library/LaunchAgents/` contains no `sean.agent.*` entries.

---

## 4. Sub-plan C — `install_schedules.sh` Hardening (RECOMMENDATION ONLY)

**Goal:** Decide whether to harden the installer script. **Recommendation: defer the change.** Keep the install_schedules.sh behavior unchanged in this plan; document the proposed hardening in this section for future implementation.

### Current behavior

`install_schedules.sh` (lines 55-80) installs **every** `.plist` in `agents-sdk/schedules/`, with a single `INSTALL_GEMINI=1` opt-in for `gemini-researcher.plist`. After Sub-plan A removes the 6 stale plists, this becomes safe again — the directory contains exactly the right set.

### Considered hardening options

| Option | Pro | Con | Verdict |
|---|---|---|---|
| **No change** (recommended) | Zero risk; matches the existing pattern; predictable behavior; A's cleanup makes it correct | Stale plists could re-appear in future and silently re-install | **Recommended.** A's deletion is the durable fix; install_schedules.sh becomes the dumb mechanism, not the policy. |
| Read `[agents.<name>] enabled = true` from `config.toml` | Authoritative source-of-truth; one place to flip a flag | Requires TOML parser in bash (or Python helper); inverts the "plist file present == intent to install" mental model that Sean already knows | Good idea, but big enough scope for its own change. Defer. |
| Maintain explicit `ACTIVE_PLISTS` allow-list array in the script | Self-documenting; no parser needed | Same drift risk as the directory itself; just moves the list | Mid-tier idea. Defer. |
| Add a sanity check: warn if a plist has no matching `[agents.<x>] enabled = true` | Catches drift early without changing core flow | Bash-side TOML parse still needed | Future enhancement. Defer. |

### Decision

**No change to `install_schedules.sh` in this plan.** A's cleanup is the surgical fix. If Sean later wants the config-driven version, that's a small follow-up PR with its own plan and tests.

### C — Steps

- [ ] **C.1 — Document this decision in the summary file** (Step 4 of the parent task) so future audits know why this was considered and deferred.

### C — Rollback

N/A (no change made).

### C — Checkpoint

No execution work in this sub-plan. Move on to D.

---

## 5. Sub-plan D — SearXNG Verification (NOT install)

**Goal:** Confirm SearXNG is healthy on `:8080` and persists across reboot. **The prior session's port (`:8888`) was wrong; SearXNG is already running and persistent.** This sub-plan is a sanity check, not an installation.

### Background (per discovery during diagnosis)

- Container: `searxng/searxng:latest`, name `searxng`, ID `853618161fa5...`
- Port mapping: `0.0.0.0:8080->8080/tcp`
- Restart policy: `unless-stopped` ← survives reboot per [`macmini-migration-plan-2026-05-02.md`](macmini-migration-plan-2026-05-02.md) Phase 1 step 3 ("`--restart unless-stopped` matters on Mac Mini — survives reboots without manual `docker start`")
- Started: `2026-05-03T15:24:33Z`, Up 30 hours at diagnosis time
- Health probe: `curl localhost:8080/search?q=qwen3&format=json` → 20 results

### What `deep_researcher` actually uses

The agent talks to LDR proxy at `:5050`, not SearXNG directly. LDR's own SearXNG endpoint config lives in LDR's encrypted SQLCipher DB (per the migration plan §"§8 documents every gotcha hit during MBP execution — port 5000 → 5050, settings live in encrypted DB not TOML"). LDR knows where SearXNG is; we just need SearXNG to keep listening.

### Steps

- [ ] **D.1 — Confirm SearXNG container is running with correct restart policy.**

```bash
docker inspect searxng --format 'Status:{{.State.Status}} Restart:{{.HostConfig.RestartPolicy.Name}} Started:{{.State.StartedAt}}'
```
Expected: `Status:running Restart:unless-stopped Started:<recent timestamp>`. If `Status` is anything else, surface and STOP.

- [ ] **D.2 — Health-probe via LDR (the integration that actually matters).**

```bash
curl -s http://localhost:5050/api/v1/health
```
Expected: `{"message":"API is running","status":"ok",...}`. Already confirmed in diagnosis — re-run defensively before D.3.

- [ ] **D.3 — Health-probe SearXNG directly.**

```bash
curl -s "http://localhost:8080/search?q=test&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); r=d.get('results',[]); print(f'OK: {len(r)} results' if r else 'EMPTY')"
```
Expected: `OK: <N> results` where N > 0. If `EMPTY`, surface — likely a SearXNG settings issue (`search.formats: [json]` toggle).

- [ ] **D.4 — Confirm Docker Desktop auto-start is set on this Mac.** Without Docker auto-start, SearXNG dies on reboot regardless of `unless-stopped`.

```bash
defaults read /Library/LaunchDaemons/com.docker.* 2>&1 | head -20 || true
ls -la ~/Library/LaunchAgents/ | grep -i docker || echo "NO_DOCKER_LAUNCHAGENT"
osascript -e 'tell application "System Events" to get login items'
```
This is informational — if Docker is not in login items, surface to Sean as an open punch-list item. Do not auto-add it.

### D — Open question to surface (don't fix in this plan)

Is Docker Desktop set to "Start Docker Desktop when you log in" in Docker preferences? If not, after a reboot SearXNG won't be available until Sean opens Docker manually. Recommend Sean toggle that setting, but do not run `osascript` to flip it.

### D — Rollback

N/A (no changes made).

### D — Checkpoint

After D.3: report all three probes' status. If any failed, STOP and surface to Sean before proceeding to E.

---

## 6. Sub-plan E — Run `install_schedules.sh` to Load 6 Active Jobs

**Goal:** Symlink and load the 6 active launchd jobs: vault-indexer, vault-synthesizer, deep-researcher, meta-agent, knowledge-lint, **daily-morning**. Confirm `gemini-researcher` is skipped. **(E.alt and E.b are SUPERSEDED by commit `7a78e35` — daily_driver is already `enabled=true`.)**

### State

`install_schedules.sh` installs every plist in the directory (minus gemini). It does **not** read `config.toml`. After Sub-plan A leaves these 7 plists:

```
com.sean.agent.daily-morning.plist        ← loaded, fires 8:45 AM, runs productively (enabled=true per 7a78e35)
com.sean.agent.deep-researcher.plist      ← loaded, fires 02:45
com.sean.agent.gemini-researcher.plist    ← skipped (INSTALL_GEMINI not set)
com.sean.agent.knowledge-lint.plist       ← loaded, fires Sun 22:00
com.sean.agent.meta-agent.plist           ← loaded, fires 06:30
com.sean.agent.vault-indexer.plist        ← loaded, fires 02:00
com.sean.agent.vault-synthesizer.plist    ← loaded, fires 02:30
```

`launchctl list` will show **6** `sean.agent.*` jobs after the install. All six run productively at their scheduled times.

### Steps

- [ ] **E.1 — Confirm hostname.**

```bash
hostname
```
Expected: `Seans-Mac-mini.local`

- [ ] **E.2 — Confirm pre-state.**

```bash
launchctl list | grep "sean.agent" || echo "NO_SEAN_AGENT_JOBS_LOADED"
ls -la ~/Library/LaunchAgents/ | grep "sean.agent" || echo "NO_SYMLINKS"
```
Expected: both `NO_*` outputs (we haven't installed yet).

- [ ] **E.3 — `--list` dry-run via the installer's built-in.**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh --list
```
Expected output:
```
Available schedules:
  com.sean.agent.daily-morning.plist
  com.sean.agent.deep-researcher.plist
  com.sean.agent.gemini-researcher.plist  (default disabled — INSTALL_GEMINI=1 to enable)
  com.sean.agent.knowledge-lint.plist
  com.sean.agent.meta-agent.plist
  com.sean.agent.vault-indexer.plist
  com.sean.agent.vault-synthesizer.plist
```
If anything else appears (e.g., a stale plist sneaked through Sub-plan A), STOP.

- [ ] **E.4 — Run the installer (no `INSTALL_GEMINI`).**

```bash
./agents-sdk/schedules/install_schedules.sh
```
Expected output:
```
Installing agent schedules...
  Installed: com.sean.agent.daily-morning.plist
  Installed: com.sean.agent.deep-researcher.plist
  Skipping com.sean.agent.gemini-researcher.plist (default disabled — set INSTALL_GEMINI=1 to enable)
  Installed: com.sean.agent.knowledge-lint.plist
  Installed: com.sean.agent.meta-agent.plist
  Installed: com.sean.agent.vault-indexer.plist
  Installed: com.sean.agent.vault-synthesizer.plist
Done. Verify with: launchctl list | grep com.sean.agent
```

- [ ] **E.5 — Verify 6 jobs loaded** (all 6 active).

```bash
launchctl list | grep "sean.agent"
```
Expected: 6 lines, one per Installed plist above. PIDs are typically `-` (not running, scheduled).

- [ ] **E.6 — Spot-check `deep-researcher` env-vars per BUGFIX-2026-04-07.**

```bash
launchctl print gui/$(id -u)/com.sean.agent.deep-researcher | grep -A1 "PATH"
```
Expected: `PATH = "/Users/seanwinslow/.local/bin:/opt/homebrew/bin:..."` matching the v3.12.1 PATH-fix template.

### E.alt — SUPERSEDED

Branch retained for traceability. The "leave daily-morning unsymlinked" branch is moot because `daily_driver.enabled = true` is already in HEAD (commit `7a78e35`). All 6 jobs load and run productively. Skip.

### E — Rollback

If anything went wrong:
```bash
./agents-sdk/schedules/install_schedules.sh --remove
```
This unloads + removes all `sean.agent.*` symlinks, returning to pre-install state (no jobs loaded). Surface the error and stop.

### E — Checkpoint to Sean

After E.6: paste `launchctl list | grep sean.agent` output, confirm PATH spot-check matches BUGFIX template, hand off to F.

---

## 7. Sub-plan F — Smoke-Test `deep_researcher` BEFORE 02:45 Cron

**Goal:** Manually fire `deep_researcher.py --mode queue` (dry-run first, then live) to confirm the launchd-loaded agent will succeed at 02:45. The smoke test must consume Topic 1a from the queue, write a real result file, mark the queue item done, and inject the daily-note digest line.

### Pass criteria
- Dry-run returns 0 with no errors and prints the resolved Topic 1a question text.
- Live run: agent runs LDR query against `:5050`, returns within `ldr_timeout_seconds = 900`, writes a topical file to `vault/20_projects/research/2026-05-05-{slug}.md` with non-trivial body (>5 KB), and:
  - Topic 1a in `vault/00_inbox/research-queue.md` is marked `- [x]` with `→ [[...]]` backlink and timestamp.
  - Today's daily note (`vault/10_timeline/daily/2026-05-05.md`) gains a `research-digest` line.
  - `agent-run-history.csv` gains a `2026-05-05,...,deep-researcher,queue,success,0.0000,...` row.

### Fail criteria → ROLLBACK
- Dry-run errors (config load, queue parse, etc.).
- Live run wall-clock exceeds 900 s (LDR timeout).
- Live run errors mid-pipeline.
- Result file is empty or has only frontmatter + sources with no real synthesis body.
- Queue item not marked done.

### Steps

- [ ] **F.1 — Confirm hostname + Topic 1a is still the next unchecked.**

```bash
hostname
grep -m1 "^- \[ \]" /Users/seanwinslow/Code-Brain/code-brain/vault/00_inbox/research-queue.md
```
Expected: hostname Mac Mini; first match is Topic 1a (`MCP / SDK toolkit survey`). If different, STOP and surface — the queue may have changed since the plan was written.

- [ ] **F.2 — Dry-run.**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode queue --dry-run
```
Expected: prints Topic 1a's question text + LDR config, exits 0.

- [ ] **F.3 — Live run.**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/deep_researcher.py --mode queue
```
Expected: ~5–15 minute wall-clock (per 2026-05-03 baseline of 286s for an easier topic; Topic 1a is more open-ended so allow up to 900s). Exits 0. Writes `vault/20_projects/research/2026-05-05-{slug}.md` (slug auto-derived from the Topic 1a question text).

**Important:** This run should be observed live in a terminal — do NOT background it. If it hangs at >12 minutes, surface to Sean before killing it.

- [ ] **F.4 — Verify deliverables.**

```bash
ls -la vault/20_projects/research/2026-05-05-*.md
grep -c "^- \[x\] Topic 1a" vault/00_inbox/research-queue.md   # expect 1
grep "research-digest" vault/10_timeline/daily/2026-05-05.md
tail -3 vault/90_system/agent-logs/agent-run-history.csv
```
Expected:
- A 2026-05-05 file exists whose slug includes `mcp` or `sdk` or `toolkit`, size > 5 KB.
- `grep -c` returns `1`.
- Daily note contains a `research-digest` block.
- CSV last line is `2026-05-05,...,deep-researcher,queue,success,...`.

### F — Rollback (if smoke test fails)

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh --remove
launchctl list | grep sean.agent || echo "NO_JOBS_LOADED"
```
Then:
1. Surface the failure mode + raw stderr to Sean.
2. Do NOT undo Sub-plan A's repo deletions (those are independent of the launchd state).
3. Re-open the plan and decide next steps.

If the smoke test wrote a partial file, leave it on disk (don't delete) so we can analyze. If the queue item got incorrectly marked done, manually revert it:
```bash
git diff vault/00_inbox/research-queue.md   # confirm the change
git checkout HEAD -- vault/00_inbox/research-queue.md   # only if Sean approves
```

### F — Checkpoint to Sean

After F.4: paste the verification output (file size, queue grep, CSV tail). Get explicit go/no-go before proceeding to G.

---

## 8. Sub-plan G — Verify Other 4 Active Agents

**Goal:** Spot-check the env-vars and load state of the remaining loaded jobs (vault-indexer, vault-synthesizer, meta-agent, knowledge-lint). Daily-morning is intentionally inert; smoke-testing it is out of scope (it'll early-exit on `enabled=false`).

### Steps

- [ ] **G.1 — Confirm all expected jobs loaded.**

```bash
launchctl list | grep "sean.agent" | sort
```
Expected: 6 lines (vault-indexer, vault-synthesizer, deep-researcher, meta-agent, knowledge-lint, daily-morning).

- [ ] **G.2 — `launchctl print` PATH spot-check across all 4 active non-deep-researcher jobs.**

```bash
for label in vault-indexer vault-synthesizer meta-agent knowledge-lint; do
    echo "=== $label ==="
    launchctl print gui/$(id -u)/com.sean.agent.$label 2>&1 | grep -A1 "PATH" | head -3
done
```
Expected: each block prints the BUGFIX-2026-04-07 PATH string starting with `/Users/seanwinslow/.local/bin:/opt/homebrew/bin`.

- [ ] **G.3 — Spot-check `vault-indexer` is wired to fire at 02:00.**

```bash
launchctl print gui/$(id -u)/com.sean.agent.vault-indexer | grep -A2 "StartCalendarInterval"
```
Expected: `Hour = 2`, `Minute = 0`.

- [ ] **G.4 — Verify the latest run history shows pre-2026-05-04 successes** (so we know the underlying agents work; we just had no launchd jobs loaded today).

```bash
tail -20 vault/90_system/agent-logs/vault-indexer-2026-05-03.log | head -5
ls -la vault/90_system/agent-logs/vault-indexer-2026-05-03.log
```
Expected: 2026-05-03 log exists, size > 0, content shows successful run. Today's log will appear after 02:00 tomorrow.

### G — Rollback

If any spot-check fails (wrong PATH, wrong schedule):
```bash
launchctl unload ~/Library/LaunchAgents/com.sean.agent.<failing-name>.plist
rm ~/Library/LaunchAgents/com.sean.agent.<failing-name>.plist
```
Surface failure; that plist needs a fix before re-loading.

### G — Checkpoint to Sean

After G.4: paste outputs, confirm all 4 PATH spot-checks match the BUGFIX template, declare fleet healthy.

---

## 9. Documentation Updates

Per CLAUDE.md "When Modifying" mandatory rule: deletions of plist files require updates to `CHANGELOG.md`, `CLAUDE.md`, and `README.md`.

### Required updates

| File | Change | Reason |
|---|---|---|
| `CHANGELOG.md` | New entry under v3.25.x or a new patch version (`v3.25.1`?) | Records the 6 plist deletions + dangling symlink cleanup. |
| `CLAUDE.md` | **No count change required.** "Active agents (7 of 14)" remains correct (5 launchd + daily-morning + flush hook). | Active count unchanged after this plan. |
| `README.md` | **Likely no count change required.** Verify the "14 autonomous SDK agents (7 active)" line still matches; update only if the README has plist-specific text. | Same reasoning. |

### Steps

- [ ] **Doc.1 — Draft CHANGELOG entry.** Propose under a new `## [Unreleased]` section or `## [v3.25.1]`:

```markdown
## [Unreleased]

### Removed
- `agents-sdk/schedules/com.sean.agent.daily-evening.plist` — disabled per AUDIT-2026-04-09.
- `agents-sdk/schedules/com.sean.agent.daily-morning-baton.plist` — orphaned (no `[agents.daily_driver_baton]` config).
- `agents-sdk/schedules/com.sean.agent.pr-digest.plist` — disabled per AUDIT-2026-04-09.
- `agents-sdk/schedules/com.sean.agent.process-inbox.plist` — paused per AUDIT-2026-04-28.
- `agents-sdk/schedules/com.sean.agent.sprint-health.plist` — disabled per AUDIT-2026-04-09; `project_key=TBD` since 2026-05-04 layoff.
- `agents-sdk/schedules/com.sean.agent.weekly-review.plist` — disabled per AUDIT-2026-04-09.

### Fixed
- Removed dangling `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` symlink (target deleted in v3.17.0 Phase 3).

### Operational
- Reinstalled launchd schedules on Seans-Mac-mini.local. 6 active jobs loaded (vault-indexer, vault-synthesizer, deep-researcher, meta-agent, knowledge-lint, daily-morning). All run productively at their scheduled times.
```

- [ ] **Doc.2 — CLAUDE.md.** Verify the "Active agents (7 of 14)" line still matches reality (it does after this plan). No change required unless a stale plist is named in the architecture diagram or rules sections — `grep` for the 6 deleted plists in CLAUDE.md and surface any hits to Sean.

- [ ] **Doc.3 — README.md.** Same as Doc.2 — `grep` for the 6 deleted plists. Surface any hits.

- [ ] **Doc.4 — Surface the diffs to Sean for approval.** Do NOT apply yet. Present the three proposed diffs as a single message: "Here are the doc updates per the mandatory rule; OK to apply?"

- [ ] **Doc.5 — On approval, apply with Edit, then commit.**

```bash
git add CHANGELOG.md   # plus CLAUDE.md / README.md only if Doc.2/Doc.3 surfaced hits
git commit -m "$(cat <<'EOF'
chore(agents-sdk): record fleet reinstall + 6 stale plist deletions

CHANGELOG entry for the launchd reinstall on Seans-Mac-mini.local:
- Removed 6 stale plists (daily-evening, daily-morning-baton, pr-digest,
  process-inbox, sprint-health, weekly-review).
- Removed dangling com.sean.agent.meeting-defender.plist symlink.
- Loaded 6 active jobs (vault-indexer, vault-synthesizer, deep-researcher,
  meta-agent, knowledge-lint, daily-morning).
- daily-driver is enabled (re-enabled in 7a78e35); CLAUDE.md "7 of 14
  active" remains correct.

Mandatory doc-update rule per CLAUDE.md "When Modifying".

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Doc — Rollback

```bash
git revert HEAD                # safest
# OR
git checkout HEAD~1 -- CHANGELOG.md CLAUDE.md README.md
```

---

## 10. Rollback Index (consolidated)

| Sub-plan | Trigger | Rollback action |
|---|---|---|
| A | Wrong plist deleted | `git checkout HEAD~1 -- agents-sdk/schedules/com.sean.agent.<name>.plist` then commit. |
| B | Symlink should not have been removed (extremely unlikely) | Restore from `git show v3.16.0:` and re-symlink. |
| C | N/A | No change. |
| D | SearXNG broke during probe | Restart container: `docker restart searxng`. |
| E | Wrong job loaded | `launchctl unload ~/Library/LaunchAgents/com.sean.agent.<name>.plist && rm ~/Library/LaunchAgents/com.sean.agent.<name>.plist`. Or full rollback: `./agents-sdk/schedules/install_schedules.sh --remove`. |
| F | Smoke test fails | `./agents-sdk/schedules/install_schedules.sh --remove` (full unload). Surface failure to Sean. Don't push, don't paper over. |
| G | Spot-check fails on one job | Unload that one: `launchctl unload && rm` for that specific plist. Active job count drops to 4; Sean decides whether to keep going or full-rollback. |
| Doc | Doc commit was wrong | `git revert HEAD`. |

### "Confirmed-working" baseline state
- `launchctl list | grep sean.agent` → empty (no jobs loaded)
- `~/Library/LaunchAgents/` → no `sean.agent.*` symlinks
- `agents-sdk/schedules/` → contains 7 plists post-cleanup (5 active + daily-morning + gemini-researcher)
- SearXNG (`:8080`) and LDR (`:5050`) and Ollama (`:11434`) → still alive (none of this plan touches them)

This is the rollback target. F's failure path returns here.

---

## 11. Validation Checklist (run before declaring DONE)

After all sub-plans complete, before writing the summary file:

- [ ] `launchctl list | grep "sean.agent" | wc -l` returns `6`.
- [ ] `vault/20_projects/research/2026-05-05-*.md` includes a new file from this afternoon's smoke test (size > 5 KB, slug contains `mcp` or `sdk` or `toolkit`).
- [ ] Topic 1a in `vault/00_inbox/research-queue.md` is `- [x]` with timestamp + wikilink.
- [ ] Today's daily note (`vault/10_timeline/daily/2026-05-05.md`) gained a `research-digest` block.
- [ ] No paid API calls were made (no Gemini DR / DR Max / cloud-Sonnet runs in `agent-run-history.csv` from this session).
- [ ] No `git push` happened.
- [ ] `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` is gone.
- [ ] `agents-sdk/schedules/` contains exactly 7 plists.
- [ ] CHANGELOG / CLAUDE.md / README.md doc diffs applied (or explicitly skipped with reason).
- [ ] Summary file written at `vault/20_projects/prj-code-brain/open-source-deep-research/2026-05-04-fleet-reinstall-summary.md`.

---

## 12. Self-Review (against parent task spec)

| Spec requirement | Plan task |
|---|---|
| Verify hostname before action | Each sub-plan opens with hostname check (A.1, B.1 implicit via env, E.1, F.1) |
| Re-run diagnostic and surface disagreements | Top of plan ("Diagnosis-Disagreement Note") with 5 itemized findings |
| Inventory table with all 14 agents | §1 Inventory table covers all 14 + 2 supplementary rows |
| Stale-cleanup with citations | §2 Sub-plan A table with audit-doc + line-level citations |
| Dangling symlink cleanup | §3 Sub-plan B |
| install_schedules.sh hardening discussion | §4 Sub-plan C — recommendation: defer, with explicit tradeoff table |
| SearXNG handling | §5 Sub-plan D — verify rather than install (port was wrong in prior session) |
| Run installer | §6 Sub-plan E — with E.alt branch for daily-morning quirk |
| Smoke-test deep_researcher | §7 Sub-plan F with explicit pass/fail criteria + rollback |
| Verify other active agents | §8 Sub-plan G — `launchctl print` spot-checks per BUGFIX-2026-04-07 |
| Documentation updates | §9 — diffs drafted for CHANGELOG / CLAUDE.md / README.md, with Sean approval gate |
| Rollback steps for every action | §10 consolidated index |
| Hard constraint: no spend | Documented in invariants; no Gemini calls anywhere |
| Hard constraint: no push | Documented in invariants; only local commits |
| Hard constraint: don't re-enable disabled agents | Plan deletes their plists; doesn't flip enabled flags |
| Hard constraint: don't touch deep_researcher.py | No edits to agent code in this plan |

No placeholders. No "TBD" or "implement later." All commands have expected output. All sub-plans have rollback steps. All sub-plans have checkpoints back to Sean.
