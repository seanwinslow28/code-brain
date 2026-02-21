# Superuser Pack — Continue Skills Audit (Phase 2)

Read the skills audit document at `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/SKILLS-AUDIT-v2.md` to understand the full project state. This is a living audit of my Claude Code Superuser Pack (90 skills, 11 agents, 5 hooks).

**What's done:** Phase 1 consolidation is complete (v3.3.0). All merges, deletes, agent fixes, and bug fixes are finished. See the "Phase 1 Completion Report" section for details.

**What's next:** Phase 2 — "New Skills & Technical Rewrites (no blockers)". These are items #17-25 in the Prioritized Action Plan. Focus on the items that are NOT already marked DONE (#23 and #25 are done). The key items are:
- Create `daily-driver` skill
- Create `subscription-audit` skill
- Create `analytics-workarounds` skill
- Rewrite `ai-creative-tools` (fix outdated hook patterns, add MCP integration)
- Create `zapier-mcp-automation` skill
- Add `2d-animation-principles` to `03-creative-projects` export group manifest
- Resolve `knowledge-management` (compare with vault skills, decide keep or delete)

**What's deferred (DO NOT work on these):**
- **Life-systems rewrites** (health-habits, personal-finance, time-management, life-admin) — blocked on my personal data, I'll provide that in a separate session
- **Block PM rewrites** (meeting-prep, sprint-roadmap, data-analysis, commit-checklist, org-definition-of-done, team-styleguide) — I'm building these in Claude Desktop first, will merge later
- **Phases 3-6** — wait until Phase 2 is complete

**How to work:**
- Read the audit doc first for full context before doing anything
- Skills live in `.claude/skills/` (canonical location)
- Run `python3 scripts/validate.py` after changes
- Update export-group manifests when adding new skills
- Update the audit doc's action plan as you complete items
- Update `CHANGELOG.md` if the version changes

Start by reading the audit doc, then propose which Phase 2 items to tackle first and in what order.
