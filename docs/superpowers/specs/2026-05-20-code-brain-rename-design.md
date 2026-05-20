---
title: Repo rename — Claude Code Superuser Pack → Code-Brain
date: 2026-05-20
status: approved
owner: Sean Winslow
---

# Repo rename — Claude Code Superuser Pack → Code-Brain

## Context

The repo started early-2025 as a personal toolkit for learning and mastering Claude Code. Over the past year+, it has compounded into something much larger: 118 skills, 13 Claude Code subagents, 14 hooks, 17 autonomous Agent SDK agents (8 currently active on launchd; others opt-in or manual-trigger), a 3-domain workspace, an Obsidian vault with a synthesizer-maintained knowledge graph, a local TTS pipeline, and an LLM council. The current name — *Claude Code Superuser Pack* — reads like a tutorial bundle. It under-sells what the project actually is to anyone scanning the GitHub repo for the first time.

This rename is driven by the active 8-week job-hunt sprint at [`vault/20_projects/prj-job-hunt-2026/`](../../../vault/20_projects/prj-job-hunt-2026/). The target audience for the new name is recruiters and hiring managers who land on the repo via Sean's portfolio, LinkedIn, or GitHub bio.

## Decisions

### Name

**Code-Brain** (Title-Case branding, lowercase-kebab slug).

- README H1: `# Code-Brain`
- GitHub slug: `code-brain`
- New URL: `https://github.com/seanwinslow28/code-brain`
- Local path on MBP + Mac Mini: `~/Code-Brain/code-brain`

Rationale: The parent workspace dir is already named `Code-Brain/`, so the name has been gravitating into use for months. The slug `code-brain` differentiates the repo from its parent at the path level while keeping the brand-facing name unified.

### Tagline (README subtitle)

> **One engineer's working second brain — skills, an agent fleet, and a knowledge graph that thinks back.**

Practitioner framing. Skips specific component counts (they change weekly; not worth the maintenance burden). "Thinks back" is the memorable hook.

### GitHub repo description (1-sentence blurb on repo page)

> Sean Winslow's agentic engineering practice in working form. Skills, autonomous agents, a knowledge-graph vault, and the runtime that keeps them in sync.

### GitHub topics

Replace existing with: `agentic-engineering`, `claude-code`, `claude-agent-sdk`, `second-brain`, `obsidian`, `autonomous-agents`, `personal-knowledge-management`.

### Rename scope: front-door only

Update only the surfaces a recruiter actually reads:

- `README.md` (H1 + tagline + lead paragraph)
- `CHANGELOG.md` (add v4.0.0 entry — do NOT rewrite history)
- `CLAUDE.md` (intro paragraph + "What This Repo Is" section)
- `LICENSE`, `.mcp.json`, `.claude-plugin/marketplace.json` (only if the string literally appears)
- GitHub repo description, topics, URL

Explicitly NOT touching:

- Historical CHANGELOG entries (authentic record of what the project was called when)
- `_archive/`, `_inputs/`, kickoff prompts, AUDIT docs
- 16BitFit / creative-studio internal docs that reference the old name
- Skills / agents / hooks (they use relative paths, not the project name)
- Issue / PR titles in GitHub history

### Version bump

Tag the rename as **v4.0.0** in CHANGELOG.md. Semver-appropriate: rename is a major identity change.

## Migration plan

Single rename branch on MBP → review → merge → Mac Mini follows. All changes reversible up to the merge commit.

### Phase 1 — Pre-flight (MBP)

1. `git status` clean on MBP
2. SSH to Mac Mini, confirm `git status` clean there too
3. Note current branch + any open work
4. Create rename branch: `git checkout -b rename/code-brain`

### Phase 2 — Update files in repo (MBP, on rename branch)

Front-door surface edits:

- `README.md` — replace H1, tagline, lead paragraph
- `CHANGELOG.md` — prepend v4.0.0 entry documenting the rename
- `CLAUDE.md` — update intro paragraph + first heading after the lead
- `LICENSE`, `.mcp.json`, `.claude-plugin/marketplace.json` — grep first; edit only if the literal string appears

Launchd plist path update (all 8 active plists + 2 opt-in):

```bash
sed -i '' 's|/Code-Brain/claude-code-superuser-pack/|/Code-Brain/code-brain/|g' \
  agents-sdk/schedules/*.plist
```

Verify nothing broke: `python3 scripts/validate.py`.

Commit on rename branch.

### Phase 3 — Local rename (MBP)

1. Close all editors / terminals / IDE workspaces pointing at the old path
2. `./agents-sdk/schedules/install_schedules.sh --remove` (clear old launchd symlinks)
3. `mv ~/Code-Brain/claude-code-superuser-pack ~/Code-Brain/code-brain`
4. `cd ~/Code-Brain/code-brain && ./agents-sdk/schedules/install_schedules.sh` (re-install with new paths)
5. Smoke test: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run`
6. Verify launchd: `launchctl list | grep com.sean.agent` should show all expected agents

### Phase 4 — GitHub rename

1. From `~/Code-Brain/code-brain`: `gh repo rename code-brain`
2. GitHub auto-creates a redirect — old URLs (clones, bookmarks, LinkedIn, Substack links) keep working indefinitely
3. `git remote set-url origin https://github.com/seanwinslow28/code-brain.git`
4. `gh repo edit --description "Sean Winslow's agentic engineering practice in working form. Skills, autonomous agents, a knowledge-graph vault, and the runtime that keeps them in sync."`
5. `gh repo edit --add-topic agentic-engineering --add-topic claude-code --add-topic claude-agent-sdk --add-topic second-brain --add-topic obsidian --add-topic autonomous-agents --add-topic personal-knowledge-management`
6. `git push -u origin rename/code-brain`
7. Open PR, review the front-door edits + plist sed-replace, squash-merge to `main`
8. Verify: `git clone https://github.com/seanwinslow28/code-brain.git /tmp/code-brain-test` → check README renders correctly

### Phase 5 — Mac Mini sync (SSH from MBP)

**Timing constraint:** do this during the day. Do NOT let Phase 5 overlap the 2:00 AM agent fleet window (the synthesizer + indexer + deep-researcher all kick off between 2:00 and 2:45 AM and would fail mid-rename).

1. `ssh` to Mac Mini
2. `cd ~/Code-Brain/claude-code-superuser-pack`
3. Confirm `git status` clean (no uncommitted local work)
4. `./agents-sdk/schedules/install_schedules.sh --remove` (clear old launchd symlinks)
5. `git remote set-url origin https://github.com/seanwinslow28/code-brain.git`
6. `git pull origin main` (pulls the renamed plists)
7. `mv ~/Code-Brain/claude-code-superuser-pack ~/Code-Brain/code-brain`
8. `cd ~/Code-Brain/code-brain && ./agents-sdk/schedules/install_schedules.sh`
9. `launchctl list | grep com.sean.agent` → verify all expected agents loaded with new paths
10. Wait for the next morning's 2:00 AM fleet run, confirm via the daily note that synthesizer + indexer + deep-researcher all wrote their expected outputs

### Phase 6 — Cleanup

1. Update LinkedIn profile, Substack bio, portfolio site to use the new URL (auto-redirect handles existing browser visits, but explicit URLs are cleaner)
2. Update shell aliases in `~/.zshrc` if any reference the old path
3. Update VSCode "recent folders" / IDE workspace settings on MBP
4. Search Granola / Obsidian / Apple Notes for any pinned references to the old URL; update those

## Why rename-in-place beats fresh-clone (Mac Mini)

Considered: fresh clone the new URL into a new dir, delete the old.

Rejected because rename-in-place preserves:

- `agents-sdk/.venv/` — 30+ Python deps including the Claude Agent SDK; fresh clone forces a reinstall
- Ollama model state (qwen3-14b-research, gemma4:e4b, nomic-embed-text) — stays on the machine but a fresh clone would re-trigger model warm-up cycles on next agent run
- `vault/.vault-index.db` — SQLite index built incrementally over weeks
- `vault/90_system/agent-logs/` — historical agent run logs (committed sparingly, mostly gitignored)
- Any in-flight local work not yet pushed

The only thing rename-in-place needs that fresh-clone wouldn't is updating the launchd plists to new paths — which we already handle in Phase 2 via `sed` on the in-repo plist files, then re-running `install_schedules.sh` on the Mac Mini in Phase 5.

## Risk + rollback

| Risk | Mitigation |
|------|-----------|
| MBP rename breaks something cosmetic (broken link, missing reference) | All changes are on the rename branch until merge — `git checkout main` rolls back instantly |
| GitHub rename collides with another repo or breaks integrations | GitHub rename is reversible: `gh repo rename CLAUDE-CODE-SUPERUSER-PACK` restores the old name. Auto-redirect means old URLs stay live regardless. |
| Mac Mini launchd doesn't reload cleanly after the rename | `install_schedules.sh --remove && install_schedules.sh` is idempotent; can re-run any time |
| 2:00 AM agent fleet runs mid-rename and breaks | Hard timing rule in Phase 5: do during the day, not overlapping the 02:00–03:00 window |
| Lost a single nightly run | Acceptable — re-trigger manually next morning if needed |
| External links (LinkedIn, Substack, portfolio) break | GitHub auto-redirect handles this until Phase 6 updates them explicitly |

## Out of scope

- Renaming any sibling project in `~/Code-Brain/` (16BitFit-App, BMAD, sw-portfolio, etc.)
- Restructuring the parent workspace `~/Code-Brain/` itself
- Renaming any other GitHub repos owned by `seanwinslow28`
- Rewriting historical CHANGELOG / AUDIT / kickoff prompt content
- Touching the Obsidian vault structure
- Migrating the launchd schedule format
- Any logo / favicon / visual branding work — README typography only

## Success criteria

1. `https://github.com/seanwinslow28/code-brain` resolves and renders the new README
2. `https://github.com/seanwinslow28/CLAUDE-CODE-SUPERUSER-PACK` redirects to the new URL (GitHub-automatic)
3. MBP: `cd ~/Code-Brain/code-brain && python3 scripts/validate.py` passes
4. MBP: `launchctl list | grep com.sean.agent` shows all expected agents loaded
5. Mac Mini: same two checks pass
6. The next morning's 2:00 AM agent fleet runs without errors on Mac Mini, and the morning daily note is written by Daily Driver at 8:45 AM as normal
7. README opens with "# Code-Brain" + the practitioner tagline, and reads cleanly end-to-end
8. CHANGELOG.md has a v4.0.0 entry documenting the rename
9. No outstanding TODO / unresolved reference in the front-door surfaces

## Implementation handoff

Next step: invoke the `superpowers:writing-plans` skill to produce the step-by-step implementation plan with concrete commands, file paths, and verification checkpoints.
