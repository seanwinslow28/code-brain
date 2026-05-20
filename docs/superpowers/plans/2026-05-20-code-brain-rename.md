# Code-Brain Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the repo from *Claude Code Superuser Pack* to *Code-Brain* across local working tree (MBP), GitHub, and the Mac Mini agent-fleet host — without breaking the running launchd agent fleet or any external links.

**Architecture:** Single rename branch on MBP → review → squash-merge → Mac Mini follows via SSH. All changes reversible up to the merge commit. "Front-door only" scope: only surfaces a recruiter actually reads (README, CHANGELOG, CLAUDE.md, plugin manifest) plus launchd plist paths get updated; historical CHANGELOG entries, AUDIT docs, kickoff prompts, and `_archive/` content stay untouched.

**Tech Stack:** Git, `gh` CLI, macOS `launchctl`, `sed`, SSH (Mac Mini), Python 3 (`scripts/validate.py`).

**Spec:** [docs/superpowers/specs/2026-05-20-code-brain-rename-design.md](../specs/2026-05-20-code-brain-rename-design.md)

---

## File Structure

**Files modified (front-door surfaces — committed via rename branch):**

- [README.md](../../../README.md) — H1 and tagline only; lead paragraph and body unchanged
- [CLAUDE.md](../../../CLAUDE.md) — line 3 intro only
- [CHANGELOG.md](../../../CHANGELOG.md) — line 3 (header) + new v4.0.0 entry prepended at top; historical entries unchanged
- [.claude-plugin/marketplace.json](../../../.claude-plugin/marketplace.json) — `name`, `repository.url` fields only
- [.mcp.json](../../../.mcp.json) — `obsidian-vault` `args[1]` path only (the `ldr` MCP path lives outside this repo and stays as-is)
- [agents-sdk/schedules/*.plist](../../../agents-sdk/schedules/) — all 11 plists, absolute paths updated via `sed`

**Files NOT modified (out of scope — left as authentic historical record):**

- Skills (`.claude/skills/**`), agents (`.claude/agents/**`), hooks (`.claude/hooks/**`) — use relative paths, no project-name references
- `_archive/`, `_inputs/`, `agents-sdk/AUDIT-*.md`, `agents-sdk/BUGFIX-*.md`
- `*-kickoff-prompt.md`, `*-prompt.md`, `claude-code-restructure-prompt.md`
- `creative-studio/`, `the-block/`, `life-systems/`, `vault/`, `16bitfit-battle-mode/` content
- Historical CHANGELOG entries (everything below the new v4.0.0 header)
- `evals/`, `docs/` (except this plan + the spec it implements)
- `LICENSE` (verified: no name reference)

**External surfaces modified (outside git):**

- GitHub repo name (`gh repo rename`)
- GitHub repo description (`gh repo edit --description`)
- GitHub repo topics (`gh repo edit --add-topic`)
- Local MBP directory: `~/Code-Brain/claude-code-superuser-pack` → `~/Code-Brain/code-brain`
- Mac Mini directory: same rename via SSH
- launchd schedule symlinks in `~/Library/LaunchAgents/` on both machines (re-installed by `install_schedules.sh`)

---

### Task 1: Pre-flight checks on both machines

**Files:** (none modified)

- [ ] **Step 1: Verify MBP working tree is clean**

```bash
cd ~/Code-Brain/claude-code-superuser-pack
git status
```

Expected: `nothing to commit, working tree clean` on branch `main`. If dirty, stash or commit before continuing.

- [ ] **Step 2: Verify Mac Mini working tree is clean via SSH**

```bash
ssh sean@<mac-mini-host> "cd ~/Code-Brain/claude-code-superuser-pack && git status"
```

Expected: `nothing to commit, working tree clean`. If dirty, SSH in and resolve before continuing (the rename will fail mid-sync if there are uncommitted local changes on Mac Mini).

- [ ] **Step 3: Create rename branch on MBP**

```bash
cd ~/Code-Brain/claude-code-superuser-pack
git checkout -b rename/code-brain
git status
```

Expected: `On branch rename/code-brain` and `nothing to commit, working tree clean`.

---

### Task 2: Audit current name references (sanity check)

**Files:** (none modified)

- [ ] **Step 1: Confirm exact scope of front-door surfaces**

```bash
cd ~/Code-Brain/claude-code-superuser-pack
echo "=== README.md ===" && grep -n "Claude Code Superuser Pack\|claude-code-superuser-pack" README.md | head -5
echo "=== CLAUDE.md ===" && grep -n "Claude Code Superuser Pack\|claude-code-superuser-pack" CLAUDE.md | head -5
echo "=== CHANGELOG.md ===" && grep -n "Claude Code Superuser Pack\|claude-code-superuser-pack" CHANGELOG.md | head -5
echo "=== .claude-plugin ===" && grep -n "claude-code-superuser-pack" .claude-plugin/marketplace.json
echo "=== .mcp.json ===" && grep -n "claude-code-superuser-pack" .mcp.json
echo "=== plists (path count) ===" && grep -l "claude-code-superuser-pack" agents-sdk/schedules/*.plist | wc -l
```

Expected output:
- README.md line 1 (`# Claude Code Superuser Pack`)
- CLAUDE.md (no direct reference — only `claude-code-superuser-pack` may appear in path-context, but not the title)
- CHANGELOG.md line 3 (`All notable changes to the Claude Code Superuser Pack will be documented in this file.`)
- `.claude-plugin/marketplace.json` lines for `"name"` and `"url"`
- `.mcp.json` one line: the `obsidian-vault` args path
- `agents-sdk/schedules/*.plist` count: **11** files

This is your scope confirmation. If the counts don't match, investigate before proceeding.

---

### Task 3: Update README.md (H1 + tagline)

**Files:**
- Modify: `README.md` (line 1, plus insert 2 new lines after H1)

- [ ] **Step 1: Apply the edit**

Replace:

```
# Claude Code Superuser Pack

An open-source agentic engineering practitioner's toolkit — **118** skills,
```

With:

```
# Code-Brain

> *One engineer's working second brain — skills, an agent fleet, and a knowledge graph that thinks back.*

An open-source agentic engineering practitioner's toolkit — **118** skills,
```

- [ ] **Step 2: Verify the edit**

```bash
head -5 README.md
```

Expected output:
```
# Code-Brain

> *One engineer's working second brain — skills, an agent fleet, and a knowledge graph that thinks back.*

An open-source agentic engineering practitioner's toolkit — **118** skills,
```

---

### Task 4: Update CLAUDE.md intro

**Files:**
- Modify: `CLAUDE.md` (line 3)

- [ ] **Step 1: Apply the edit**

Replace line 3:

```
This is Sean's personal command center — a second brain for Claude Code.
```

With:

```
This is Code-Brain — Sean's personal command center, a second brain built on Claude Code.
```

- [ ] **Step 2: Verify the edit**

```bash
sed -n '1,5p' CLAUDE.md
```

Expected:
```
# CLAUDE.md

This is Code-Brain — Sean's personal command center, a second brain built on Claude Code.

## What This Repo Is
```

---

### Task 5: Update CHANGELOG.md (header + new v4.0.0 entry)

**Files:**
- Modify: `CHANGELOG.md` (line 3, plus insert v4.0.0 entry block at top)

- [ ] **Step 1: Update the header line**

Replace line 3:

```
All notable changes to the Claude Code Superuser Pack will be documented in this file.
```

With:

```
All notable changes to Code-Brain (formerly *Claude Code Superuser Pack*) will be documented in this file.
```

- [ ] **Step 2: Find the first existing version header**

```bash
grep -n "^## \[" CHANGELOG.md | head -1
```

Expected: a line like `5:## [3.37.1] — 2026-05-16` (or whatever the most recent version is). Note both the line number and the exact text of that version header — you'll use it as the `old_string` anchor in the next step.

- [ ] **Step 3: Prepend the v4.0.0 entry**

Use the Edit tool with `old_string` set to the exact version-header line from Step 2 (e.g. `## [3.37.1] — 2026-05-16`) and `new_string` set to the new v4.0.0 block + a blank line + the original line. That inserts the new block immediately above the previous most-recent entry.

The new block to insert:

```markdown
## [4.0.0] — 2026-05-20

### Changed
- **Renamed the project from *Claude Code Superuser Pack* to *Code-Brain*.** The previous name described the project's origin (a toolkit for mastering Claude Code) but no longer described what it had become: a personal agentic OS, a working second brain, and a published example of agentic engineering practice. New tagline: *"One engineer's working second brain — skills, an agent fleet, and a knowledge graph that thinks back."* GitHub repo slug renamed `seanwinslow28/claude-code-superuser-pack` → `seanwinslow28/code-brain`; auto-redirect preserves all existing URLs. Local + Mac Mini directories renamed `~/Code-Brain/claude-code-superuser-pack` → `~/Code-Brain/code-brain`. Launchd plist absolute paths updated on both machines via `sed` and `install_schedules.sh` re-bootstrap. Scope was deliberately "front-door only" — README H1 + tagline + intro, CLAUDE.md intro, CHANGELOG header, `.claude-plugin/marketplace.json`, `.mcp.json` vault path, and the 11 launchd plist paths. Historical CHANGELOG entries, AUDIT docs, kickoff prompts, and `_archive/` content stay untouched as authentic record. Spec at [docs/superpowers/specs/2026-05-20-code-brain-rename-design.md](docs/superpowers/specs/2026-05-20-code-brain-rename-design.md); plan at [docs/superpowers/plans/2026-05-20-code-brain-rename.md](docs/superpowers/plans/2026-05-20-code-brain-rename.md).

```

- [ ] **Step 4: Verify**

```bash
head -3 CHANGELOG.md
echo "---"
grep -n "^## \[4.0.0\]" CHANGELOG.md
```

Expected:
```
# Changelog

All notable changes to Code-Brain (formerly *Claude Code Superuser Pack*) will be documented in this file.
---
<line-number>:## [4.0.0] — 2026-05-20
```

---

### Task 6: Update .claude-plugin/marketplace.json + .mcp.json

**Files:**
- Modify: `.claude-plugin/marketplace.json` (2 fields)
- Modify: `.mcp.json` (1 line)

- [ ] **Step 1: Edit .claude-plugin/marketplace.json**

Replace:

```json
  "name": "claude-code-superuser-pack",
```

With:

```json
  "name": "code-brain",
```

And replace:

```json
    "url": "https://github.com/seanwinslow28/claude-code-superuser-pack"
```

With:

```json
    "url": "https://github.com/seanwinslow28/code-brain"
```

- [ ] **Step 2: Edit .mcp.json (obsidian-vault path)**

Replace:

```
        "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault"
```

With:

```
        "/Users/seanwinslow/Code-Brain/code-brain/vault"
```

- [ ] **Step 3: Verify both files are syntactically valid JSON**

```bash
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))" && echo "marketplace.json OK"
python3 -c "import json; json.load(open('.mcp.json'))" && echo ".mcp.json OK"
```

Expected: both lines printed. If either fails, the JSON is malformed — re-check the edits.

- [ ] **Step 4: Verify the values changed**

```bash
grep "\"name\"\|\"url\"" .claude-plugin/marketplace.json | head -2
grep "code-brain" .mcp.json
```

Expected: name shows `code-brain`, url shows the new URL, .mcp.json shows the new path.

---

### Task 7: Update launchd plist paths (all 11 files)

**Files:**
- Modify: `agents-sdk/schedules/*.plist` (11 files)

- [ ] **Step 1: Run sed in-place across all plists**

```bash
sed -i '' 's|/Code-Brain/claude-code-superuser-pack/|/Code-Brain/code-brain/|g' agents-sdk/schedules/*.plist
```

Expected: no output (sed runs silently on success).

- [ ] **Step 2: Verify zero remaining references to the old path**

```bash
grep -l "claude-code-superuser-pack" agents-sdk/schedules/*.plist | wc -l
```

Expected: `0`. If non-zero, list which files still match and re-investigate.

- [ ] **Step 3: Verify the new path appears in all 11 plists**

```bash
grep -l "/Code-Brain/code-brain/" agents-sdk/schedules/*.plist | wc -l
```

Expected: `11`.

- [ ] **Step 4: Spot-check one plist visually**

```bash
grep "/Code-Brain/code-brain/" agents-sdk/schedules/com.sean.agent.daily-morning.plist
```

Expected: 5 lines showing python3 binary, daily_driver.py script, working directory, stdout log, stderr log — all under the new `code-brain/` path.

---

### Task 8: Validate + commit Phase 2 changes

**Files:** (none modified — verification + commit only)

- [ ] **Step 1: Run validator**

```bash
python3 scripts/validate.py
```

Expected: exit 0. The validator hard-enforces the 3-primary-domain structure (per CLAUDE.md note on v3.15.0) and skill/agent/hook counts — none of which should have changed.

- [ ] **Step 2: Review the diff before committing**

```bash
git status
git diff --stat
```

Expected files modified:
```
.claude-plugin/marketplace.json
.mcp.json
CHANGELOG.md
CLAUDE.md
README.md
agents-sdk/schedules/com.sean.agent-fleet-wake-scheduler.plist
agents-sdk/schedules/com.sean.agent.daily-morning.plist
agents-sdk/schedules/com.sean.agent.deep-researcher.plist
agents-sdk/schedules/com.sean.agent.gemini-researcher.plist
agents-sdk/schedules/com.sean.agent.knowledge-lint.plist
agents-sdk/schedules/com.sean.agent.meta-agent.plist
agents-sdk/schedules/com.sean.agent.substack-drafter.plist
agents-sdk/schedules/com.sean.agent.vault-indexer.plist
agents-sdk/schedules/com.sean.agent.vault-synthesizer.plist
agents-sdk/schedules/com.sean.job-feed.plist
agents-sdk/schedules/com.sean.service.ldr-web.plist
```

(16 files: 5 front-door + 11 plists.)

- [ ] **Step 3: Stage and commit**

```bash
git add README.md CLAUDE.md CHANGELOG.md .claude-plugin/marketplace.json .mcp.json agents-sdk/schedules/*.plist
git commit -m "$(cat <<'EOF'
rename: Claude Code Superuser Pack -> Code-Brain

Front-door surfaces only: README H1 + tagline, CLAUDE.md intro,
CHANGELOG header + v4.0.0 entry, .claude-plugin/marketplace.json
name + url, .mcp.json obsidian-vault path, and all 11 launchd
plist absolute paths (sed: claude-code-superuser-pack -> code-brain).

Historical CHANGELOG entries, AUDIT docs, kickoff prompts, and
_archive/ content unchanged.

Spec: docs/superpowers/specs/2026-05-20-code-brain-rename-design.md
Plan: docs/superpowers/plans/2026-05-20-code-brain-rename.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: commit created on `rename/code-brain` branch.

---

### Task 9: MBP local rename + relink launchd

**Files:** (none modified — filesystem operation + launchd reload)

- [ ] **Step 1: Close anything pointing at the old path**

Manual step. Close all open editors, terminals, IDE workspaces, and VSCode "recent folders" that have `~/Code-Brain/claude-code-superuser-pack` open. Failing to do this won't break the rename, but stale terminal CWDs will be confusing afterward.

Open a fresh terminal in `~` to proceed.

- [ ] **Step 2: Remove old launchd symlinks**

```bash
cd ~/Code-Brain/claude-code-superuser-pack
./agents-sdk/schedules/install_schedules.sh --remove
```

Expected: output lines like `Removed: com.sean.agent.daily-morning.plist` for each of the 8 installed schedules (the opt-in ones won't be removed if they weren't installed).

- [ ] **Step 3: Rename the directory**

```bash
cd ~
mv Code-Brain/claude-code-superuser-pack Code-Brain/code-brain
ls -la Code-Brain/ | grep code-brain
```

Expected: shows `code-brain` directory. Old name no longer present.

- [ ] **Step 4: Reinstall launchd schedules from the new path**

```bash
cd ~/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh
```

Expected: output lines like `Loaded: com.sean.agent.daily-morning.plist` for each schedule.

- [ ] **Step 5: Verify all expected agents loaded**

```bash
launchctl list | grep com.sean.agent
launchctl list | grep com.sean.service
launchctl list | grep com.sean.job-feed
launchctl list | grep com.sean.agent-fleet-wake-scheduler
```

Expected: each grep returns at least one line; total ~8 entries (more if opt-in agents are installed).

---

### Task 10: MBP smoke test (daily_driver dry run)

**Files:** (none modified)

- [ ] **Step 1: Run the daily driver in dry-run mode**

```bash
cd ~/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run
```

Expected: exit 0. Prints the prompt that would be sent to Claude. No actual API call (dry run). If exit non-zero, the agent SDK setup is broken at the new path — check the `.venv` is still functional, working dir resolution is correct, and config.toml paths.

- [ ] **Step 2: Sanity check the validator still passes from the new path**

```bash
cd ~/Code-Brain/code-brain
python3 scripts/validate.py
```

Expected: exit 0.

---

### Task 11: GitHub repo rename

**Files:** (none modified — external GitHub action)

- [ ] **Step 1: Rename the GitHub repo via gh**

```bash
cd ~/Code-Brain/code-brain
gh repo rename code-brain
```

Expected: prompt to confirm (`Rename CLAUDE-CODE-SUPERUSER-PACK to code-brain? (Y/n)`). Type `y`. Output: `✓ Renamed repository seanwinslow28/code-brain`. GitHub automatically creates a redirect from the old URL.

- [ ] **Step 2: Update local remote URL**

```bash
git remote set-url origin https://github.com/seanwinslow28/code-brain.git
git remote -v
```

Expected:
```
origin	https://github.com/seanwinslow28/code-brain.git (fetch)
origin	https://github.com/seanwinslow28/code-brain.git (push)
```

- [ ] **Step 3: Verify the rename took effect on GitHub**

```bash
gh repo view seanwinslow28/code-brain --json name,url
```

Expected: JSON with `"name": "code-brain"` and `"url": "https://github.com/seanwinslow28/code-brain"`.

- [ ] **Step 4: Verify auto-redirect works**

```bash
gh repo view seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK --json url
```

Expected: returns the new URL (`https://github.com/seanwinslow28/code-brain`), confirming GitHub's auto-redirect is active. Existing bookmarks, LinkedIn links, and Substack links pointing at the old URL continue to work.

---

### Task 12: Update GitHub description and topics

**Files:** (none modified — external GitHub action)

- [ ] **Step 1: Set the new repo description**

```bash
gh repo edit seanwinslow28/code-brain --description "Sean Winslow's agentic engineering practice in working form. Skills, autonomous agents, a knowledge-graph vault, and the runtime that keeps them in sync."
```

Expected: silent success (or a one-line success message).

- [ ] **Step 2: Add the new topic set**

```bash
gh repo edit seanwinslow28/code-brain \
  --add-topic agentic-engineering \
  --add-topic claude-code \
  --add-topic claude-agent-sdk \
  --add-topic second-brain \
  --add-topic obsidian \
  --add-topic autonomous-agents \
  --add-topic personal-knowledge-management
```

Expected: silent success per topic.

- [ ] **Step 3: Verify description and topics on the live repo**

```bash
gh repo view seanwinslow28/code-brain --json description,repositoryTopics
```

Expected: JSON showing the new description and a `repositoryTopics` array containing all 7 added topics. (Existing old topics may also still be present — that's fine; review them in the next step.)

- [ ] **Step 4: Optionally remove stale topics**

```bash
gh repo view seanwinslow28/code-brain --json repositoryTopics
```

Look at the list. If any old topic is no longer relevant (e.g. a generic `productivity` topic from the v3.0.0 era), remove with:

```bash
gh repo edit seanwinslow28/code-brain --remove-topic <stale-topic-name>
```

If all topics look fine, skip this step.

---

### Task 13: Push branch, open PR, merge to main

**Files:** (none modified — git operations)

- [ ] **Step 1: Push the rename branch**

```bash
cd ~/Code-Brain/code-brain
git push -u origin rename/code-brain
```

Expected: new branch created on origin.

- [ ] **Step 2: Create PR**

```bash
gh pr create --title "rename: Claude Code Superuser Pack -> Code-Brain" --body "$(cat <<'EOF'
## Summary
- Renames the project from *Claude Code Superuser Pack* to *Code-Brain*
- Front-door surfaces only: README H1 + tagline, CLAUDE.md intro, CHANGELOG header + new v4.0.0 entry, .claude-plugin/marketplace.json name + url, .mcp.json obsidian-vault path, and all 11 launchd plist absolute paths
- Historical CHANGELOG entries, AUDIT docs, kickoff prompts, and _archive/ content deliberately left as authentic record
- New tagline: *One engineer's working second brain — skills, an agent fleet, and a knowledge graph that thinks back.*
- GitHub repo already renamed (auto-redirect active); this PR ships the in-tree changes

## Test plan
- [x] `python3 scripts/validate.py` passes on rename branch
- [x] MBP local directory renamed `~/Code-Brain/claude-code-superuser-pack` → `~/Code-Brain/code-brain`
- [x] MBP launchd schedules re-installed via `install_schedules.sh`, `launchctl list | grep com.sean.agent` returns all expected entries
- [x] MBP `daily_driver.py --mode morning --dry-run` exits 0
- [ ] Mac Mini synced via SSH (Task 14 of plan)
- [ ] Next morning's 02:00 AM agent fleet runs cleanly on Mac Mini (Task 16 of plan)

Spec: docs/superpowers/specs/2026-05-20-code-brain-rename-design.md
Plan: docs/superpowers/plans/2026-05-20-code-brain-rename.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: PR URL printed. Open it in browser, review the diff visually one more time.

- [ ] **Step 3: Squash-merge the PR**

```bash
gh pr merge --squash --delete-branch
```

Expected: PR squash-merged into `main`, remote branch deleted.

- [ ] **Step 4: Sync local main**

```bash
git checkout main
git pull origin main
git log --oneline -3
```

Expected: top commit is the squash-merged rename commit.

---

### Task 14: Mac Mini sync via SSH

**Files:** (filesystem ops on Mac Mini only — no in-repo changes)

**Timing constraint:** Do this during the day. The 02:00–03:00 AM window has the vault-indexer (02:00), vault-synthesizer (02:30), and deep-researcher (02:45) all firing — running this overlap would corrupt an in-flight run. Run between roughly 09:00 and 23:00.

- [ ] **Step 1: SSH to Mac Mini**

```bash
ssh sean@<mac-mini-host>
```

Replace `<mac-mini-host>` with the actual hostname or IP. Confirm you land in the Mac Mini's home directory.

- [ ] **Step 2: Verify Mac Mini working tree is still clean**

```bash
cd ~/Code-Brain/claude-code-superuser-pack
git status
```

Expected: `nothing to commit, working tree clean`. If dirty (an agent may have committed something since Task 1's check), resolve before continuing.

- [ ] **Step 3: Remove old launchd symlinks on Mac Mini**

```bash
./agents-sdk/schedules/install_schedules.sh --remove
```

Expected: `Removed: ...` for each installed schedule.

- [ ] **Step 4: Update remote URL and pull renamed plists**

```bash
git remote set-url origin https://github.com/seanwinslow28/code-brain.git
git remote -v
git pull origin main
```

Expected: remote URL updated, pull succeeds, brings in the squash-merged rename commit including renamed plist paths.

- [ ] **Step 5: Rename the directory on Mac Mini**

```bash
cd ~
mv Code-Brain/claude-code-superuser-pack Code-Brain/code-brain
ls -la Code-Brain/ | grep code-brain
```

Expected: shows `code-brain` directory.

- [ ] **Step 6: Reinstall launchd schedules from new path**

```bash
cd ~/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh
```

Expected: `Loaded: ...` for each schedule.

- [ ] **Step 7: Verify launchctl loaded everything with new paths**

```bash
launchctl list | grep com.sean.agent
launchctl list | grep com.sean.service
launchctl list | grep com.sean.job-feed
launchctl list | grep com.sean.agent-fleet-wake-scheduler
```

Expected: same set of entries as on MBP (the active 8 + any opt-ins that were installed on Mac Mini). All should be loaded.

- [ ] **Step 8: Spot-check one running agent's resolved path**

```bash
launchctl print gui/$(id -u)/com.sean.agent.daily-morning | grep -E "(path|directory|program)" | head -5
```

Expected: paths point at `/Users/sean/Code-Brain/code-brain/...` (note: Mac Mini's user may be different from MBP — confirm against the actual Mac Mini username).

- [ ] **Step 9: Exit SSH**

```bash
exit
```

---

### Task 15: External cleanup checklist

**Files:** (external surfaces — outside this repo)

- [ ] **Step 1: Update LinkedIn**

Open LinkedIn → Profile → Featured/Projects → any pinned link pointing at `github.com/seanwinslow28/claude-code-superuser-pack` or `CLAUDE-CODE-SUPERUSER-PACK` → edit to use `code-brain`.

GitHub auto-redirect handles existing browser visits, but explicit URLs are cleaner for ATS scrapers and rendering previews.

- [ ] **Step 2: Update Substack bio / about page**

If the Substack "About" or bio links at the old repo URL, update to `github.com/seanwinslow28/code-brain`.

- [ ] **Step 3: Update portfolio site(s)**

Check `sw-portfolio/`, `sw-ai-pm-portfolio/`, and any deployed portfolio pages for hardcoded repo URLs. Replace.

- [ ] **Step 4: Update shell aliases / VSCode workspaces**

```bash
grep -n "claude-code-superuser-pack" ~/.zshrc ~/.bashrc ~/.zsh_aliases 2>/dev/null
```

If any matches, update them to `code-brain`. Then:

```bash
ls ~/Library/Application\ Support/Code/User/workspaceStorage/ 2>/dev/null | xargs -I {} grep -l "claude-code-superuser-pack" ~/Library/Application\ Support/Code/User/workspaceStorage/{}/workspace.json 2>/dev/null
```

Stale VSCode workspace folders will quietly disappear once the directory rename is committed — usually safe to ignore, but if a critical workspace was bookmarked, recreate it from the new path.

- [ ] **Step 5: Update Granola / Apple Notes / Obsidian quick-links**

Search any place where you've pinned the old URL or local path. The vault itself has `[[code-brain]]` wikilinks possibly nowhere — but check `vault/05_atlas/` and operating-model artifacts for absolute path references.

```bash
cd ~/Code-Brain/code-brain
grep -rn "claude-code-superuser-pack" vault/05_atlas/ 2>/dev/null | head -10
```

If matches surface, decide case-by-case whether to update (operating-model artifacts referring to the project may want to be updated; historical Granola notes capturing a meeting from when the project had the old name are fine to leave).

---

### Task 16: Next-morning verification

**Files:** (verification only — runs the morning after the migration)

- [ ] **Step 1: Confirm Mac Mini agent fleet ran cleanly overnight**

The morning after Task 14 completes, on MBP:

```bash
cd ~/Code-Brain/code-brain
ls -lt vault/daily/ | head -5
```

Expected: today's daily note exists (written by Daily Driver at 08:45 AM Mac Mini time).

- [ ] **Step 2: Check fleet activity logs**

```bash
tail -20 vault/90_system/agent-logs/agent-run-history.csv
```

Expected: rows from the overnight runs (vault-indexer, vault-synthesizer, deep-researcher) and morning runs (meta-agent, daily-driver). All should show success status.

- [ ] **Step 3: Read the daily note's Fleet Overnight Digest**

Open today's daily note in Obsidian (or `cat vault/daily/$(date +%Y-%m-%d).md`). Look for the `<!-- fleet-overnight -->` section — it should be populated with 7 lines (one per active agent) showing overnight activity.

If the section is empty or shows errors, investigate:
- Were the launchd schedules actually loaded? `launchctl list | grep com.sean.agent` on Mac Mini via SSH
- Did the agents try to write to old paths? `tail -100 vault/90_system/agent-logs/daily-morning-stderr.log`
- Did Mac Mini have any unrelated overnight issues (sleep, network)?

- [ ] **Step 4: Confirm GitHub redirect is still working from external surfaces**

```bash
curl -sI "https://github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK" | head -3
```

Expected: `HTTP/2 301` redirect to the new URL.

- [ ] **Step 5: Final sanity check — clone from new URL into /tmp**

```bash
rm -rf /tmp/code-brain-clone-test 2>/dev/null
git clone --depth 1 https://github.com/seanwinslow28/code-brain.git /tmp/code-brain-clone-test
head -5 /tmp/code-brain-clone-test/README.md
rm -rf /tmp/code-brain-clone-test
```

Expected: clone succeeds; README starts with `# Code-Brain` and the new tagline blockquote.

If all five verifications pass, the rename is complete.

---

## Success criteria (must all be true)

1. `https://github.com/seanwinslow28/code-brain` resolves and renders the new README
2. `https://github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK` returns HTTP 301 to the new URL
3. MBP: `cd ~/Code-Brain/code-brain && python3 scripts/validate.py` exits 0
4. MBP: `launchctl list | grep com.sean.agent` shows all expected agents loaded
5. Mac Mini: same two checks pass via SSH
6. Next morning's 02:00 AM agent fleet runs cleanly on Mac Mini, daily note written at 08:45 AM by Daily Driver
7. README opens with `# Code-Brain` + the practitioner tagline blockquote
8. CHANGELOG.md has a v4.0.0 entry documenting the rename
9. `.claude-plugin/marketplace.json` `name` field is `code-brain` and `repository.url` points at the new URL
10. `.mcp.json` `obsidian-vault` path resolves to the new location

## Rollback (if something breaks before merge)

```bash
# On MBP, before Task 13 squash-merge:
git checkout main
git branch -D rename/code-brain
mv ~/Code-Brain/code-brain ~/Code-Brain/claude-code-superuser-pack
cd ~/Code-Brain/claude-code-superuser-pack
./agents-sdk/schedules/install_schedules.sh --remove
./agents-sdk/schedules/install_schedules.sh
# On GitHub, if rename already happened:
gh repo rename CLAUDE-CODE-SUPERUSER-PACK
```

## Rollback (if something breaks after merge but before Mac Mini sync)

```bash
# Revert the squash-merge commit on MBP:
git revert <merge-commit-sha>
git push origin main
# Then restore local + GitHub state as above.
```

## Rollback (if something breaks on Mac Mini after Task 14)

Mac Mini's directory + launchd state is independent of MBP. Reverse on Mac Mini only:

```bash
ssh sean@<mac-mini-host>
cd ~/Code-Brain/code-brain
./agents-sdk/schedules/install_schedules.sh --remove
mv ~/Code-Brain/code-brain ~/Code-Brain/claude-code-superuser-pack
cd ~/Code-Brain/claude-code-superuser-pack
# At this point the plists in git point at the new path, so install_schedules.sh
# would re-install with the new path. Either: pull a revert commit first, OR
# manually sed the plists back on Mac Mini before re-installing:
sed -i '' 's|/Code-Brain/code-brain/|/Code-Brain/claude-code-superuser-pack/|g' agents-sdk/schedules/*.plist
./agents-sdk/schedules/install_schedules.sh
```
