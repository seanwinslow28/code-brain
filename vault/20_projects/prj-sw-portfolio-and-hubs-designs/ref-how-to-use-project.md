---
type: project
domain: []
status: active
context: ref-how-to-use-project
energy-level: medium
ai-context: ""
review-date: 2026-03-17
created: 2026-03-03
---
# ref-how-to-use-project

## Overview
**Goal:**
**Why it matters:**
**Definition of Done:**

## Current Status
<!-- status-update -->

## Latest Commits
<!-- git-commits -->

## Key Decisions
| Date | Decision | Rationale |
|------|----------|-----------|

## Blockers
-

## Links
- **Repo:**
- **Jira:**
- **Figma:**
- **Related notes:**
What Was Done
Moved & configured:

sw-portfolio-and-hubs-designs/ now lives at the superuser pack root
Gitignored from the superuser pack (only change: .gitignore modified)
Has its own git repo with initial commit
Created:

.gitignore — protects bank CSVs, node_modules, build output
CLAUDE.md — encodes design spec rules, lists all 22 relevant skills + 6 agents + 3 hooks, maps data connections, includes session startup checklist
Verified:

Superuser pack git only sees the .gitignore change (portfolio is invisible)
Portfolio git sees all its own files as untracked (ready for first real commit)
All data paths work via ../ (107 skills, 13 agents, 7 hooks, agent logs, config.toml, finance CSVs)
How to Use It
When you're ready to work on the portfolio projects:

Open Claude Code from claude-code-superuser-pack/ (the root, not the subfolder)
Tell Claude: "Read sw-portfolio-and-hubs-designs/design-system-spec.md and sw-portfolio-and-hubs-designs/sw-portfolio-and-hubs-context.md, then help me work on [agent-control-center / life-systems-hub / sw-portfolio]"
All 107 skills, 13 agents, and 7 hooks auto-load. The portfolio CLAUDE.md layers on top with the design rules.
The one gotcha to remember: always start sessions from the superuser pack root, not the portfolio subfolder, so Claude Code finds the parent .claude/ directory with all your skills.