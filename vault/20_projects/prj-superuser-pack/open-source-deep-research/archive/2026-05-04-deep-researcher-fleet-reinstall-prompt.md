---
type: prompt-for-fresh-session
domain:
  - claude-mastery
status: ready-to-fire
context: superuser-pack
created: 2026-05-04
intended-use: Paste into a fresh Claude Code session on the Mac Mini, then activate Plan Mode (double Shift+Tab) and run /writing-plans (the superpowers:writing-plans skill) before letting Claude execute.
references:
  - vault/20_projects/prj-superuser-pack/open-source-deep-research/phase-4-night-1-2026-05-03.md
  - agents-sdk/schedules/install_schedules.sh
  - agents-sdk/AUDIT-2026-04-09-agent-downsizing.md
  - agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md
  - CLAUDE.md (auto-loaded)
---

# Prompt — Deep Researcher Fleet Reinstall (Mac Mini, 2026-05-04)

> **How to use this:** Open a fresh Claude Code session on the Mac Mini. Activate Plan Mode (`Shift+Tab` twice — must be Plan Mode, NOT Extended Thinking). Run `/writing-plans` to load the superpowers planning skill. Then paste everything below the horizontal rule. Approve the plan before letting Claude execute.

---

You are an infrastructure engineer specializing in macOS launchd, Python autonomous agents (Claude Agent SDK), and Obsidian-vault-backed personal-fleet operations. Your output will produce a written plan (via the `superpowers:writing-plans` skill) that I will review and approve before any execution. After approval, you will execute the plan with periodic checkpoints.

<context>
**Machine:** I am on `Seans-Mac-mini.local` — the always-on Mac Mini. This is the canonical host for the autonomous SDK agent fleet (per [CLAUDE.md](CLAUDE.md)). My MBP has only a test deep_researcher; the Mac Mini is the production host. Verify hostname before doing anything: `hostname` should return `Seans-Mac-mini.local`.

**Project state:** v3.25.0 of the Superuser Pack shipped yesterday (2026-05-03) on branch `feat/gemini-deep-research-v3.25.0`, 11 commits ahead of `main`, NOT pushed to remote. CLAUDE.md says 7 of 14 SDK agents are "active." The Phase 4 plan ([phase-4-night-1-2026-05-03.md](vault/20_projects/prj-superuser-pack/open-source-deep-research/phase-4-night-1-2026-05-03.md)) expected `deep_researcher` to auto-fire at 02:45 daily on the Mac Mini and process Topic 1a from `vault/00_inbox/research-queue.md` overnight.

**Life context (matters for cost decisions):** I was laid off from The Block on 2026-05-04. Severance ~1 month, separation deadline ~2026-05-11. The agent fleet is now also a job-hunt portfolio artifact (see `~/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/project_block_layoff_2026-05-04.md`). No income until severance lands. Treat any spend (Gemini API, paid services) as requiring explicit approval. The infrastructure work itself is free.
</context>

<situation>
A prior session diagnosed why Topic 1a did not auto-process overnight 2026-05-03 → 2026-05-04. The diagnosis was:

1. **`launchctl list | grep "sean.agent"` returns nothing on this Mac Mini.** Zero `sean.agent.*` jobs are loaded by launchd.
2. **`~/Library/LaunchAgents/` on this Mac Mini contains only ONE `sean.agent.*` symlink — and it's stale and dangling**: `com.sean.agent.meeting-defender.plist`, dated April 18, pointing to a target file that was deleted from the repo in v3.17.0 Phase 3 (per CLAUDE.md). No other agent plists are symlinked.
3. **The repo at `agents-sdk/schedules/*.plist` contains 12 plist files**, but per CLAUDE.md only 7 should be active (`vault_indexer`, `vault_synthesizer`, `deep_researcher`, `meta_agent`, `daily_driver` via `daily-morning.plist`, `knowledge_lint`, `flush` — note `flush` is hook-triggered, not a plist). Stale plists in the repo include: `daily-evening`, `daily-morning-baton`, `pr-digest`, `process-inbox`, `sprint-health`, `weekly-review` — most are in CLAUDE.md's "6 disabled in v3.12.3" list (per [`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`](agents-sdk/AUDIT-2026-04-09-agent-downsizing.md)).
4. **`process-inbox.plist` is unexpectedly still present in the repo** even though CLAUDE.md says process_inbox was paused 2026-04-29 (v3.17.4) pending Path B local-`gemma4:e4b` rewrite (per [`agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`](agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md)). Do NOT re-enable it.
5. **Backend stack on the Mac Mini is partially up:**
   - LDR proxy on `localhost:5050` — ✅ python3 listening (verified by `lsof -iTCP:5050 -sTCP:LISTEN`).
   - Ollama on `localhost:11434` — ✅ running, with `qwen3-14b-research:latest`, `qwen3:14b`, `gemma4:e4b`, `gemma4:26b`, `nomic-embed-text:latest`, `phi4-mini-reasoning:latest` available.
   - SearXNG on `localhost:8888` — ❌ NOT listening. The `deep_researcher` agent uses LDR + SearXNG for web search; without SearXNG, even a successfully-loaded launchd job will fail when it tries to do a web search.
6. **Current `install_schedules.sh` behavior is "install everything in `agents-sdk/schedules/*.plist`"** (with a single `INSTALL_GEMINI=1` opt-in gate for `gemini-researcher.plist`). Running it as-is on the Mac Mini today would install all 12 — including the 5–6 stale/disabled ones that should NOT be re-enabled.

**Symptom this needs to fix:** Topic 1a from [`vault/00_inbox/research-queue.md`](vault/00_inbox/research-queue.md) (the "MCP / SDK toolkit survey" topic, `tier: 0`, free local LDR run) did not get processed overnight 2026-05-03 → 2026-05-04. The next 4 unchecked LDR queue items (Topic 1b, 3, 5, 7) are also at risk. There is no `vault/20_projects/research/2026-05-04-{slug}.md` file for any auto-processed LDR topic.

**Goal:** Restore autonomous operation of the 7 active SDK agents on this Mac Mini per CLAUDE.md, starting with `deep_researcher` so Topic 1a fires at 02:45 tomorrow morning. Surface and fix the stale-plist drift in the repo. Do not re-enable any of the 6 disabled agents. Do not push the local v3.25.0 branch to GitHub. Do not fire any Gemini API call (paid).
</situation>

<your_task>
Use the `superpowers:writing-plans` skill to produce an implementation plan for restoring the SDK agent fleet on this Mac Mini. Write the plan to `vault/20_projects/prj-superuser-pack/open-source-deep-research/2026-05-04-fleet-reinstall-plan.md` (or the canonical plan location the skill recommends — follow the skill's conventions).

**Step 1 — Verify the diagnosis (do not trust the prior session blindly).**
Re-run the diagnostic commands and confirm:
- `hostname` returns `Seans-Mac-mini.local`
- `launchctl list | grep "sean.agent"` returns nothing
- `ls -la ~/Library/LaunchAgents/ | grep "sean.agent"` shows only the stale `meeting-defender` symlink
- The plists actually present in `agents-sdk/schedules/`
- LDR proxy / Ollama / SearXNG status (`lsof -iTCP:5050 / 11434 / 8888 -sTCP:LISTEN`)
- The "active vs disabled" agent map per CLAUDE.md and the AUDIT docs

If your verification disagrees with the prior diagnosis at any point, surface the disagreement BEFORE writing the plan. Don't paper over it.

**Step 2 — Write a plan with these required sections.**
Plan structure must include:

1. **Inventory & invariants** — Current state of each of the 14 SDK agents (active per CLAUDE.md vs disabled per audits); current state of each `*.plist` file in `agents-sdk/schedules/`; the LaunchAgents symlink state. Build a table with one row per agent: `name | active-per-CLAUDE.md | plist-in-repo | symlinked | launchctl-loaded | should-be-loaded`. This is the source of truth the plan operates against.

2. **Sub-plan A — Stale repo cleanup.** Decide which of the 5–6 stale plists to delete from `agents-sdk/schedules/` (`daily-evening`, `daily-morning-baton`, `pr-digest`, `process-inbox`, `sprint-health`, `weekly-review`). For each: justify deletion via the audit docs. If unsure for any one, mark it KEEP-FOR-NOW and explain why. Do NOT delete plists for agents currently active. Do NOT touch the `gemini-researcher.plist` (intentional, default-disabled, gated by `INSTALL_GEMINI=1`).

3. **Sub-plan B — Dangling symlink cleanup.** Remove the dangling `~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist` symlink.

4. **Sub-plan C — `install_schedules.sh` hardening (recommended, not required).** The current script installs every `.plist` in the schedules directory. After Sub-plan A removes stale plists, the script becomes safe again. But consider whether to harden it further — e.g., read the active list from `agents-sdk/config.toml`'s `[agents.<name>] enabled` field, or maintain an explicit allowlist in the script. Discuss tradeoffs in the plan; recommend an option but do not silently change the script's behavior in this same plan execution unless the plan explicitly approves it.

5. **Sub-plan D — SearXNG.** Determine the correct way to start SearXNG on this Mac Mini (likely a separate launchd job, a Docker compose, or a manual `python -m searxng` — research the actual setup in this repo before guessing). Add it to the plan such that it auto-starts at boot. If the repo has no SearXNG installation history, surface that as an open question rather than fabricating a setup.

6. **Sub-plan E — Run `install_schedules.sh` to load the 7 active plists.** Only after A + B + (D if SearXNG is needed by deep_researcher's first run) are complete. Verify with `launchctl list | grep "sean.agent"` that all 7 active jobs are loaded. Do NOT pass `INSTALL_GEMINI=1` (Gemini researcher is intentionally default-disabled).

7. **Sub-plan F — Smoke test deep_researcher BEFORE the 02:45 cron fires.** Run `deep_researcher.py` interactively in `--dry-run` mode (or its equivalent), then in live mode if dry-run looks clean. Confirm it picks up Topic 1a from `vault/00_inbox/research-queue.md`, queries LDR, gets a result back, writes to `vault/20_projects/research/2026-05-04-{slug}.md`, and marks the queue item done. Since SearXNG was likely down and the LDR/Ollama stack is local, the agent should produce a real (not empty) result. If the run fails, ROLL BACK the launchd install and surface the failure — do not declare success on a partial outcome.

8. **Sub-plan G — Verify the other 6 launchd-scheduled active agents are loaded** (`vault_indexer`, `vault_synthesizer`, `meta_agent`, `daily_driver` via `daily-morning.plist`, `knowledge_lint`). Spot-check one with `launchctl print` to confirm the env-vars and PATH look right (per `agents-sdk/BUGFIX-2026-04-07-launchd-path.md` — that PATH bug bit me before).

9. **Documentation updates.** Per CLAUDE.md's "When Modifying" mandatory doc updates: if any plist file is deleted or `install_schedules.sh` is modified, update CHANGELOG.md, CLAUDE.md (counts), and README.md. Generate proposed diffs and have me approve them before applying.

10. **Rollback steps.** For each sub-plan, write the rollback. Specifically:
    - If a deleted plist needs to come back: `git checkout HEAD -- agents-sdk/schedules/<name>.plist`
    - If `install_schedules.sh` was run and an unintended job was loaded: `launchctl unload ~/Library/LaunchAgents/com.sean.agent.<name>.plist && rm ~/Library/LaunchAgents/com.sean.agent.<name>.plist`
    - If smoke-test fails: confirmed-working state is "no `sean.agent.*` in launchctl, deep_researcher.plist NOT symlinked." Restore that state.

**Step 3 — After I approve the plan, execute it sub-plan by sub-plan with checkpoints.**
Pause and surface progress to me at each sub-plan boundary. Do not blast through all 10 sub-plans in one shot. After each sub-plan: report what changed, what didn't, what surprised you, what risk popped up.

**Step 4 — Final verification.**
After Sub-plan F's smoke test passes, leave a brief written summary at `vault/20_projects/prj-superuser-pack/open-source-deep-research/2026-05-04-fleet-reinstall-summary.md` capturing: what was deleted/installed/changed, what to expect at 02:45 tomorrow, what to verify the next morning, what's still on the punch list.
</your_task>

<constraints>
**Hard rules — do NOT violate without explicit approval from me:**

1. **No spend.** Do not fire any Gemini API call, paid LLM call, or any service that costs money. The local Ollama + LDR stack is free; use it freely.
2. **Do not push the v3.25.0 branch to GitHub.** It is local-only on the MBP, and the Mac Mini may have its own copy on the same branch. The push decision is mine, not yours, and it's deferred per the original handoff.
3. **Do not re-enable any of the 6 disabled SDK agents** (`daily-driver` evening, `daily-driver` weekly, `pr-digest`, `spending-analysis`, `health-audit`, `md-to-anki`, plus `process_inbox`). See [`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`](agents-sdk/AUDIT-2026-04-09-agent-downsizing.md) and [`agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`](agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md) for the history.
4. **Do not touch `agents-sdk/agents/deep_researcher.py`** — it's the v3.23.0 version in soak. The fleet-reinstall is about wiring, not agent code.
5. **Do not skip pre-commit hooks** (no `--no-verify`).
6. **Do not modify `agents-sdk/agents/*` files unless required by the plan** — and if required, surface the change explicitly in the plan and get approval before editing.
7. **No destructive `git` commands** (force push, reset --hard, branch -D) without my explicit confirmation per command.
8. **Confirm `hostname` returns `Seans-Mac-mini.local`** at the start. If you're somehow on the MBP, STOP — this plan is Mac-Mini-specific and the MBP is intentionally different.
9. **Empty queue / empty repo checks.** If during Sub-plan F the smoke test reveals the LDR queue has changed or the file paths in the plan are stale, do not silently adapt — surface and ask.

**Soft preferences:**

- Prefer minimal diffs over refactors. The goal is to restore broken infrastructure, not redesign it.
- Prefer surgical fixes per sub-plan over bundled mega-fixes that change many things at once.
- Prefer dry-run / preview / `--dry-run` flags over live runs whenever the agent supports them.
- Prefer using `launchctl print <label>` to spot-check loaded jobs instead of `launchctl list`'s less-detailed output.
- Use Plan Mode and the `superpowers:writing-plans` skill — the user (Sean) explicitly chose this workflow.
</constraints>

<deliverables>
1. **A written plan file** at `vault/20_projects/prj-superuser-pack/open-source-deep-research/2026-05-04-fleet-reinstall-plan.md` (or wherever `superpowers:writing-plans` recommends), structured per the 10 sections in `<your_task>` Step 2.
2. **A diagnosis-disagreement note** if your verification (Step 1) found anything different from the prior session's findings — embedded in the plan or surfaced inline before plan-writing.
3. **Per-sub-plan checkpoints during execution** — short progress updates at each sub-plan boundary, not a single end-of-execution summary.
4. **A summary file** at `vault/20_projects/prj-superuser-pack/open-source-deep-research/2026-05-04-fleet-reinstall-summary.md` after Sub-plan F passes.
5. **(If documentation changed) Proposed diffs to CHANGELOG.md, CLAUDE.md, README.md** — surfaced for my approval before applying.
</deliverables>

<references>
Files and paths the fresh session should consult while writing/executing the plan (in priority order):

1. **[CLAUDE.md](CLAUDE.md)** — Auto-loaded. Single source of truth for which agents are active, the architecture overview, and the non-negotiable rules (rules 6–8 are the most relevant: deny-list permissions, hook exit codes, settings precedence, vault sync owner).
2. **[`vault/20_projects/prj-superuser-pack/open-source-deep-research/phase-4-night-1-2026-05-03.md`](vault/20_projects/prj-superuser-pack/open-source-deep-research/phase-4-night-1-2026-05-03.md)** — Original handoff. Read sections "Where we are (engineering state)", "Phase 4 Stream A — current state", "Open items", and the DO/DON'T list.
3. **[`agents-sdk/schedules/install_schedules.sh`](agents-sdk/schedules/install_schedules.sh)** — The current installer; understand its flow before deciding whether to harden it.
4. **[`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`](agents-sdk/AUDIT-2026-04-09-agent-downsizing.md)** — Why the 6 agents are disabled. Authoritative.
5. **[`agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`](agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md)** — Why process_inbox is paused (cloud-Sonnet path works but cost-prohibitive).
6. **[`agents-sdk/BUGFIX-2026-04-07-launchd-path.md`](agents-sdk/BUGFIX-2026-04-07-launchd-path.md)** — The PATH-in-EnvironmentVariables requirement. Worth re-checking the plists.
7. **[`agents-sdk/config.toml`](agents-sdk/config.toml)** — `[agents.<name>] enabled` flags are the second source of truth (after CLAUDE.md). Check this before deciding which agents are active.
8. **[`vault/00_inbox/research-queue.md`](vault/00_inbox/research-queue.md)** — The LDR queue. Topic 1a is the first unchecked item and is the smoke-test target.
9. **`~/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/agents_sdk_mbp_first_pattern.md`** — The "MBP-first pattern" that explains why the Mac Mini install was deferred historically. Useful context, not a constraint.
10. **`~/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/project_block_layoff_2026-05-04.md`** — The layoff context. Relevant only for the cost-rule constraint and for understanding why the fleet matters as a portfolio artifact.
</references>

<validation>
Before declaring the plan ready for my approval, confirm in writing:

- [ ] Verified `hostname` is `Seans-Mac-mini.local`.
- [ ] Re-ran the diagnostic commands; either confirmed the prior diagnosis or surfaced the disagreement.
- [ ] Built the agent inventory table (Sub-plan inventory) with all 14 SDK agents enumerated.
- [ ] Each of the 5–6 stale plist deletions has a citation (audit doc + line/section) justifying it.
- [ ] No proposed action violates any of the 9 hard constraints.
- [ ] The plan's smoke-test step (Sub-plan F) has clear pass/fail criteria.
- [ ] Rollback steps exist for every modify/install action.
- [ ] If `install_schedules.sh` is being modified, the diff is surfaced and the change rationale is explicit.
- [ ] CHANGELOG.md / CLAUDE.md / README.md updates are drafted (or marked as "no changes needed and here's why").

After execution, before writing the summary file, confirm:

- [ ] `launchctl list | grep "sean.agent"` shows the expected 5 active jobs (`vault_indexer`, `vault_synthesizer`, `deep-researcher`, `meta-agent`, `daily-morning`, `knowledge-lint` — adjust per the actual active list).
- [ ] Smoke-test of `deep_researcher` produced a real result file at `vault/20_projects/research/2026-05-04-*.md` that contains an actual research answer (not just frontmatter + sources).
- [ ] Topic 1a in `vault/00_inbox/research-queue.md` is now marked `[x]` with timestamp + wikilink to the result.
- [ ] No paid API calls were made.
- [ ] No git push happened.
- [ ] The dangling `meeting-defender` symlink is gone.
</validation>
