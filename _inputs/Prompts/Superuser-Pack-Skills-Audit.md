# Superuser Pack Skills Audit v2.2

**Date:** February 18, 2026 | **Pack Version:** 3.8.0 | **Auditor:** Claude Code (Opus 4.6)

**Previous versions:** v2.1 (Feb 17, Phase 1-2) | v2.0 (Feb 16, pre-consolidation) | v1.0 (Feb 15, name-based)

---

## Handoff Guide for Next Agent

This is the authoritative audit document for the Claude Code Superuser Pack. Read this before doing any skill work.

### Current State

- **102 skills**, **13 agents**, **7 hooks** across 6 domain workspaces
- **Phases 1-6 are COMPLETE** (Consolidation, New Skills, Life-Systems Rewrites, Block PM Rewrites, Creative Pipeline & Career, Future Capabilities)
- Pack version: **v3.8.0**
- Validation: `python3 scripts/validate.py` → 0 errors (block-secrets narrowing reduced false positives)

### What's Done

| Phase | Version | Status | Summary |
|-------|---------|--------|---------|
| Phase 1: Consolidation | v3.3.0 | COMPLETE | 4 agents fixed, 1 bug fixed, 3 skills deleted, 7 skill pairs merged, 7 manifests updated |
| Phase 2: New Skills & Rewrites | v3.4.0 | COMPLETE | 4 new skills created, 1 rewritten, 1 merged+deleted, 4 manifests updated |
| Phase 3: Life-Systems Rewrites | v3.5.0 | COMPLETE | 4 skills rewritten with Sean's personal data (interview-driven) |
| Phase 4: Block PM Rewrites | v3.6.0 | COMPLETE | 8 skills rewritten/improved, 1 new skill created, 2 manifests updated |
| Phase 5: Creative Pipeline & Career | v3.7.0 | COMPLETE | 7 new skills, 2 new agents, 4 manifests updated |
| Phase 6: Future Capabilities | v3.8.0 | COMPLETE | 1 new skill, 2 new hooks, 1 hook narrowed |

### All Phases Complete

All 6 audit phases are done. The pack is at v3.8.0 with 102 skills, 13 agents, 7 hooks.

### Working Instructions

1. **Skills live in `.claude/skills/<name>/SKILL.md`** — this is the canonical location, auto-loaded by Claude Code
2. **Export-group manifests** (`export-groups/*/playground.json`) are metadata-only — update them when adding/removing skills
3. **Run `python3 scripts/validate.py`** after any changes to catch orphans and misconfigurations
4. **Update this audit doc** with completion status after each phase
5. **Update `CHANGELOG.md`** with version entries for each phase
6. **Update `CLAUDE.md`** skill/agent/hook counts if they change
7. **Update `MEMORY.md`** (at `/Users/seanwinslow/.claude/projects/-Users-seanwinslow-Code-Brain-claude-code-superuser-pack/memory/MEMORY.md`) with project state

### Key Files

| File | Purpose |
|------|---------|
| `SKILLS-AUDIT-v2.md` (repo root) | Mirror of this doc — keep in sync |
| `CHANGELOG.md` | Version history |
| `CLAUDE.md` | Project overview and non-negotiable rules |
| `.claude/skills/` | All 102 skills (canonical) |
| `.claude/agents/` | All 13 agents |
| `.claude/hooks/` | All 7 hooks |
| `export-groups/*/playground.json` | Export manifests (metadata-only) |
| `scripts/validate.py` | Validation script |

---

## Executive Summary

**Current inventory:** 102 skills, 13 agents, 7 hooks across 6 domain workspaces.

**All 6 audit phases are COMPLETE (v3.8.0).** The pack went from 90 skills/11 agents/5 hooks (pre-audit) to 102/13/7. All 102 skills at Q:4-5. Zero capability loss from consolidation.

**Phase 1 consolidation (v3.3.0).** 4 agents fixed, 1 bug fixed, 3 skills deleted, 7 skill pairs merged.

**Phase 2 new skills & rewrites (v3.4.0).** 4 new skills, 1 rewrite, 1 merge+delete.

**Phase 3 life-systems rewrites (v3.5.0).** 4 skills rewritten with Sean's personal data.

**Phase 4 Block PM rewrites (v3.6.0).** 8 skills rewritten/improved, 1 new skill.

**Phase 5 Creative Pipeline & Career (v3.7.0).** 7 new skills (animation-pipeline, script-writing, creative-writing, career-transition, personal-app-patterns, technical-writing, rn-architecture), 2 new agents (animation-director, code-reviewer).

**Phase 6 Future Capabilities (v3.8.0).** 1 new skill (comfyui-workflows), 2 new hooks (daily-note-appender, network-access-control), 1 hook narrowed (block-secrets.py — eliminated false positives on "keyboard", "keynote", etc.).

### What Changed Since v2.0

| Action | Count | Details |
|--------|-------|---------|
| Skills deleted (pure) | 3 | safe-ops, org-security, quick-prd |
| Skills merged (source deleted) | 7 | supabase-python, claude-md-optimization, stakeholder-brief, phaser-pattern, sprite-pipeline, learning-drill, budget-entry |
| Agents fixed | 4 | security-reviewer, compliance-summarizer (broken tool names), data-analyst, game-design-advisor (missing deny-lists) |
| Bugs fixed | 1 | python-automation `title: string` → `title: str` |
| Export-group manifests updated | 7 | Removed all references to deleted skills |
| Skill count | 99 → 90 | -10 deleted/merged source skills, +1 counting adjustment |

### What Changed Since v3.3.0

| Action | Count | Details |
|--------|-------|---------|
| Skills created (new) | 4 | daily-driver, subscription-audit, analytics-workarounds, zapier-mcp-automation |
| Skills rewritten | 1 | ai-creative-tools (hooks, env vars, HF MCP, ComfyUI scripts) |
| Skills merged + deleted | 1 | knowledge-management → vault-read-write (Synthesis Protocol + /compress) |
| Export-group manifests updated | 4 | 02-pm, 03-creative, 04-advanced, 05-life |
| Skill count | 90 → 93 | +4 new, -1 deleted |

### What Changed Since v3.4.0

| Action | Count | Details |
|--------|-------|---------|
| Skills rewritten (personalized) | 4 | health-habits, personal-finance, time-management, life-admin — all rewritten with Sean's actual data via structured interviews |
| Quality upgrades | 4 | health-habits 3→5, personal-finance 5→5 (content upgrade), time-management 4→5, life-admin 3→5 |
| Skill count | 93 | No change (rewrites only) |

### What Changed Since v3.5.0

| Action | Count | Details |
|--------|-------|---------|
| Skills rewritten (Block PM) | 4 | meeting-prep (standup/team roster/1:1s), data-analysis (GA4/Looker/Zapier MCP), stakeholder-update (merged biweekly-jira-update), jira-automation (merged the-block-jira-ticket-writer) |
| Skills improved (general) | 4 | sprint-roadmap (adapted as general PM tool with RICE/MoSCoW), commit-checklist (Q:2→5), org-definition-of-done (Q:2→5), team-styleguide (Q:1→5) |
| Skills created (new) | 1 | etf-page-creator (WordPress ETF page workflow for The Block) |
| Export-group manifests updated | 2 | 02-pm-workflows, 08-domain-specific |
| Skill count | 93 → 94 | +1 new (etf-page-creator) |

### What's Left To Do

All work is complete.

| Category | Count | Status |
|----------|-------|--------|
| ~~Skills needing rewrite (personal/life)~~ | ~~4~~ | ~~COMPLETE (v3.5.0)~~ |
| ~~Skills needing rewrite (Block/work)~~ | ~~8+1~~ | ~~COMPLETE (v3.6.0)~~ |
| ~~New skills to create~~ | ~~8~~ | ~~COMPLETE (v3.7.0 + v3.8.0)~~ |
| ~~New agents to create~~ | ~~2~~ | ~~COMPLETE (v3.7.0)~~ |
| ~~New hooks to create~~ | ~~2~~ | ~~COMPLETE (v3.8.0)~~ |

**Quality distribution (post-Phase 6):** 102 skills: all rated Q:4-5 (100%). Zero skills below Q:4.

---

## Phase 1 Completion Report

### Agent Fixes (4/4 DONE)

| Agent | Problem | Fix Applied |
|-------|---------|------------|
| security-reviewer | Lowercase Cursor tool names (`write`, `edit`, `search_replace`, `delete_file`, `run_terminal_cmd`) — completely non-functional | Replaced with `Edit`, `Write`, `Bash` |
| compliance-summarizer | Same broken Cursor tool names | Replaced with `Edit`, `Write`, `Bash` |
| data-analyst | No `disallowedTools` at all | Added `disallowedTools: [Edit, Write, Bash]` (user chose read-only) |
| game-design-advisor | No `disallowedTools` at all | Added `disallowedTools: [Edit, Write, Bash]` |

**Result:** 11/11 agents now properly configured (was 6/11).

### Bug Fix (1/1 DONE)

| File | Bug | Fix |
|------|-----|-----|
| `.claude/skills/python-automation/SKILL.md` | Line 64: `title: string` (JavaScript syntax in Python skill) | Changed to `title: str` |

### Pure Deletes (3/3 DONE)

| Skill Deleted | Reason | Notes |
|---------------|--------|-------|
| safe-ops | 54-line placeholder, zero unique content beyond security-hardening | Just deleted |
| org-security | 70-line generic checklist, everything covered by security-hardening | Just deleted |
| quick-prd | Near-complete overlap with prd-generator | Added 1-line "Quick Mode" note to prd-generator before deleting |

### Merges (7/7 DONE)

| Source (deleted) | Target (enhanced) | Content Transferred |
|-----------------|-------------------|-------------------|
| supabase-python | supabase-backend | Python Client section: `create_client` setup, auth patterns (`sign_up`, `sign_in_with_password`, `get_user`), database queries with filters, insert, update |
| claude-md-optimization | config-settings | 6 sections: @import system detail, monorepo/subdirectory pattern, per-section token budget table (Architecture ~25 lines, Decisions ~25, Patterns ~25, Gotchas ~20, Commands ~15), CLAUDE.md vs Skills comparison table, update cadence (/init pattern), global security CLAUDE.md template. Also changed size target from 500 → 300 lines. |
| stakeholder-brief | stakeholder-update | 3 tone templates (Formal/Investors, Casual/Internal, Urgent/Escalation), 4 verification tests (Skim, Action, Surprise, Evidence) |
| phaser-pattern | phaser-game-patterns | React Native WebView bridge (~35 lines), Game Object Container pattern (~28 lines), StateMachine class (~35 lines), LoadingScene with progress bar (~25 lines), Common Gotchas section |
| sprite-pipeline | sprite-asset-pipeline | TexturePacker CLI integration, free-tex-packer-core Node.js script, Aseprite CLI batch export, pngquant/WebP optimization, shell automation script, animation JSON format, asset directory structure, common frame rates table |
| learning-drill | learning-accelerator | 5 drill formats (Code Completion, Bug Hunt, Explain It, Speed Drill, Build From Scratch) with worked examples, 4-week React Fundamentals progression curriculum, tracking log template, 4 verification checks |
| budget-entry | personal-finance | Quick Budget Entry (bank paste, receipt text, voice/quick entry), auto-categorization YAML rules, Google Sheets/Notion integration patterns, monthly review template, verification steps (sum, category, duplicate, date checks) |

### Manifest Updates (7/7 DONE)

| Export Group | Skills Removed |
|-------------|---------------|
| 01-core-features | safe-ops, org-security |
| 02-pm-workflows | quick-prd, stakeholder-brief |
| 03-creative-projects | phaser-pattern, sprite-pipeline |
| 04-advanced-techniques | claude-md-optimization |
| 05-life-optimization | budget-entry |
| 07-technical-stack | supabase-python |
| 09-community-resources | learning-drill |

### Other Cleanup

- Deleted orphan `plugin/skills/safe-ops/` directory (flagged by validate.py)
- Updated `CLAUDE.md` skill count (99 → 90)
- Updated `MEMORY.md` with v3.3.0 state
- Updated `CHANGELOG.md` with v3.3.0 entry

### Validation Result

```
python3 scripts/validate.py → 0 errors, 10 warnings
```

All 10 warnings are false-positive secret patterns in documentation files (example API keys, placeholder URLs). No real issues.

---

## Phase 2 Completion Report

### New Skills Created (4/4 DONE)

| Skill | Domain | Export Group | Description |
|-------|--------|-------------|-------------|
| daily-driver | Life Systems | 05-life-optimization | Morning planning with 1-3-5 Rule, task type icons ([DW] Deep Work, [QW] Quick Win, etc.), EOD review protocol, mid-day check-in, weekly review, Obsidian daily note template with frontmatter |
| subscription-audit | Life Systems | 05-life-optimization | Bank/credit card CSV parsing, recurring charge detection, 9 subscription categories, 4-action decision matrix (Keep/Downgrade/Replace/Cancel), savings projections, negotiation tips |
| analytics-workarounds | Product Management | 02-pm-workflows | 4 data access patterns: GA4 via Zapier MCP, Google Sheets as Data Hub, Manual Export + Claude Analysis, BigQuery Public Datasets. Specific Zapier GA4 and Sheets tools listed. Budget note: each MCP call = 2 Zapier tasks |
| zapier-mcp-automation | Claude Mastery | 04-advanced-techniques | ~175 Zapier MCP tool patterns organized by category (Communication, PM, Data & Docs, Analytics, Storage & Compute). 4 workflow recipes with task cost estimates. Task budget optimization (batching, caching, minimizing round-trips). Budget planning table by Zapier plan tier |

### Skill Rewrite (1/1 DONE)

| Skill | Problems Fixed | New Content Added |
|-------|---------------|-------------------|
| ai-creative-tools | Fake "CLAUDE.md hooks" (don't exist) → real PostToolUse hooks in settings.json format. Hardcoded `YOUR_XI_API_KEY` → `os.environ["ELEVENLABS_API_KEY"]`. No MCP integration → full HF MCP section | ComfyUI queue script (workflow JSON injection, class_type targeting, polling), ElevenLabs voice synthesis script (argparse CLI, voice name→ID lookup, multilingual_v2 model), Hugging Face MCP tools (hub_repo_search, hub_repo_details, space_search, paper_search, dynamic_space), asset index management (assets.json schema), cross-references to 4 related skills |

### Skill Merged + Deleted (1/1 DONE)

| Source (deleted) | Target (enhanced) | Content Transferred |
|-----------------|-------------------|-------------------|
| knowledge-management | vault-read-write | 4-step Multi-Source Synthesis Protocol (salient keywords → consensus → divergence → actionable takeaways + Consensus Matrix table format), `/compress` session-end context handoff command (6-step workflow: get date, read conversation, extract decisions/open loops/files modified/key terms, append to daily note) |

**Resolution process:** Used an Explore subagent to compare knowledge-management against all 6 vault skills (vault-architecture, vault-read-write, vault-automation, obsidian-mcp-setup, obsidian-semantic-search, knowledge-graph-nav). Only 2 of 6 capabilities were unique. All other content (atomic notes, cross-linking, PKM organizing, lazy prompting) was already fully covered.

### Manifest Updates (4/4 DONE)

| Export Group | Changes |
|-------------|---------|
| 02-pm-workflows | Added analytics-workarounds |
| 03-creative-projects | Added 2d-animation-principles |
| 04-advanced-techniques | Added zapier-mcp-automation |
| 05-life-optimization | Added daily-driver, subscription-audit. Removed knowledge-management. Updated version to 3.4.0 |

### Other Updates

- Updated `CLAUDE.md` skill count (90 → 93)
- Updated `MEMORY.md` with v3.4.0 state
- Updated `CHANGELOG.md` with v3.4.0 entry
- Updated `SKILLS-AUDIT-v2.md` (repo root) with full Phase 2 completion details

### Validation Result

```
python3 scripts/validate.py → 0 errors, 10 warnings
```

Same false-positive warnings as Phase 1. No new issues introduced.

---

## Phase 3 Completion Report

### Skills Rewritten (4/4 DONE)

| Skill | Quality Before | Quality After | Key Personalization Added |
|-------|---------------|---------------|--------------------------|
| health-habits | 3 | 5 | PPL split (Mon-Fri schedule), 4:45 AM anchor, 3-4 sets to failure, Apple Fitness → CSV pipeline via Shortcuts, XP/level gamification (10 levels, streak bonuses), vault daily note checkboxes, weekly summary generation, supplement stack table |
| personal-finance | 5 | 5 | Chase CSV parser (7-col format) + Bilt CSV parser (headerless quoted), $5,741/mo net income, 19 active subscriptions with keep/cancel status, 7 annual renewal dates, modified 50/30/20 budget framework, debt paydown calculator, Sean-specific regex categorization (40+ merchant patterns), anomaly detection |
| time-management | 4 | 5 | 4:45 AM → 9 PM daily structure, energy map (6 time blocks), 45/35/20 work split, Focus Day (Mon/Fri) vs Meeting Day (Tue-Thu), `/today` daily planning ritual, PEARL conflict resolution with Sean's priority hierarchy, weekly review template, Google Calendar OAuth integration plan |
| life-admin | 3 | 5 | Boston move March 21 checklist (15 items with status tracking), medical provider transition Medvidi→Aetna (7-step checklist), address change tracker (5 categories), annual subscription renewal calendar (7 dates), file organization audit workflow, Cannes France Sep 2026 trip planning template |

### Interview Process

Each skill was written after a structured interview with Sean:
1. Read existing generic SKILL.md
2. Cross-referenced personal context doc for known data
3. Asked targeted gap-filling questions (only what couldn't be inferred)
4. Sean provided answers via markdown docs + financial documents (Chase CSV, Bilt CSV, paystub PDF)
5. Rewrote skill with personalized content, keeping YAML frontmatter + section structure

### Subscription Audit Side-Product

During the personal-finance interview, a full subscription audit was conducted:
- **Cancelled during session:** OpenAI ChatGPT ($20/mo), Cursor AI ($65/mo), XAI/Grok ($30/mo)
- **Net monthly savings:** ~$115/month ($1,380/year)
- **Annual cancellation reminders set:** Meshy (Aug), Lottiefiles (Oct), LinkedIn Premium (Jan)

### Validation Result

```
python3 scripts/validate.py → 0 errors, 10 warnings
```

Same false-positive warnings as previous phases. No new issues introduced.

---

## Phase 4 Completion Report

### Context

Phase 4 was originally blocked on Sean's Claude Desktop experimentation. That work stabilized, and Sean provided premade `.skill` files (ZIP archives) with Block-specific content for meeting-prep, data-analysis, stakeholder-update (as biweekly-jira-update), jira-automation (as the-block-jira-ticket-writer), and etf-page-creator. An interactive interview established the strategy for each skill.

### Skills Rewritten — Full Block Rewrites (4/4 DONE)

| Skill | Quality Before | Quality After | Key Content Added |
|-------|---------------|---------------|-------------------|
| meeting-prep | 4 | 5 | Block standup format (3-part: yesterday/today/blockers), team roster with roles, 1:1 prep template, sprint planning workflow with Atlassian MCP JQL queries, pre-read auto-generation from Jira sprint board |
| data-analysis | 5 | 5 | Block metrics (subscriber growth, API usage, Campus enrollment), GA4 access pattern (view-only, no admin), Looker access pattern (view-only, CSV export), Zapier MCP data bridge (GA4 → Claude → Sheets), 4 data access tiers with specific tool references |
| stakeholder-update | 5 | 5 | Merged biweekly-jira-update: biweekly Jira sprint report format, cross-team visibility (PRO/GD/DE/OP projects), auto-pull from Atlassian MCP, sprint velocity tracking, blocker escalation format |
| jira-automation | 5 | 5 | Merged the-block-jira-ticket-writer: Block Jira config (instance URL, 7 project keys, component IDs, labels, issue type IDs), 4 ticket templates (Epic/Design Story/Implementation Story/Bug), PRD-to-tickets 4-step workflow, real examples (PRO-4354, PRO-3513), 8 JQL query patterns |

### New Skill Created (1/1 DONE)

| Skill | Domain | Export Group | Description |
|-------|--------|-------------|-------------|
| etf-page-creator | Product Management | 08-domain-specific | WordPress ETF page creation workflow for The Block. 4-step process (determine mode, collect data, auto-generate SEO, format output). Required fields table, external integrations (Track Insight ID, TradingView Symbol), SEO title/meta description auto-generation with examples, copy-paste checklist matching WordPress field order, validation rules |

### Skills Adapted (1/1 DONE)

| Skill | Quality Before | Quality After | Change |
|-------|---------------|---------------|--------|
| sprint-roadmap | 5 | 5 | Refocused from Block-specific to general PM tool. Sean's manager handles sprint ceremonies. Added RICE scoring (with worked example), MoSCoW method, Impact/Effort matrix, capacity calculation formula, backlog grooming with JQL, dependency mapping, release checklist |

### Skills Improved — Stub Expansion (3/3 DONE)

| Skill | Quality Before | Quality After | Content Added |
|-------|---------------|---------------|---------------|
| commit-checklist | 2 | 5 | Pre-commit validation checklist (Security/Code Quality/Completeness/Scope categories), conventional commit format with 10-type reference table, good/bad examples with explanations, multi-commit strategy, 5-step workflow with git commands |
| org-definition-of-done | 2 | 5 | DoD templates for 4 work types (Feature: 5 sections, Bug Fix, Refactor, Spike), Release DoD (Pre-Release/Deploy/Post-Release), 3-step review workflow with scored output format, customization guide for different team contexts |
| team-styleguide | 1 | 5 | Config auto-detection workflow (8 config file types), universal rules (naming table, import ordering, comment do/don't, file structure patterns), language-specific rules (TypeScript/Python/CSS-Tailwind), 3-step review workflow with PASS/WARN/FAIL format, new project setup guide, tools-by-language table |

### Manifest Updates (2/2 DONE)

| Export Group | Changes |
|-------------|---------|
| 02-pm-workflows | Added jira-automation to skills list (was already there — verified) |
| 08-domain-specific | Added etf-page-creator |

### Other Updates

- Updated `CLAUDE.md` skill count (93 → 94), product-management domain (18 → 19)
- Updated `MEMORY.md` with v3.6.0 state, Block Jira config reference
- Updated `CHANGELOG.md` with v3.6.0 entry
- Updated export-group manifests

### Validation Result

```
python3 scripts/validate.py → 94 skills, 0 errors, 10 warnings
```

Same false-positive warnings as previous phases. No new issues. Note: etf-page-creator initially added to both 02-pm-workflows and 08-domain-specific, causing a collision error. Removed from 02-pm-workflows (it's Block-specific, fits domain-specific).

---

## Deferred Items (With Reasons)

These items were intentionally set aside. Each has a specific reason and a clear path to completion.

### 1. knowledge-management Deletion — RESOLVED (v3.4.0)

**Status:** MERGED + DELETED
**Resolution:** Compared knowledge-management against all 6 vault skills. Found 2 unique items: the 4-step Synthesis Protocol (salient keywords → consensus → divergence → actionable takeaways + Consensus Matrix table format) and the `/compress` session-end context handoff command. Both merged into vault-read-write. All other content (atomic notes, cross-linking, PKM organizing, lazy prompting) was already fully covered by vault-architecture, knowledge-graph-nav, and vault-read-write. Skill deleted, removed from 05-life-optimization manifest.

### 2. Life-Systems Rewrites (4 skills) — RESOLVED (v3.5.0)

**Status:** COMPLETE
**Resolution:** Interactive interview with Sean provided all personal data needed. All 4 skills rewritten with personalized content: health-habits (PPL split, XP gamification, Apple Fitness pipeline), personal-finance (Chase+Bilt CSV parsers, debt paydown, subscription tracker), time-management (45/35/20 split, energy map, Focus/Meeting days), life-admin (Boston move checklist, medical transition, Cannes trip planning).

### 3. Block PM Rewrites (8+1 skills) — RESOLVED (v3.6.0)

**Status:** COMPLETE
**Resolution:** Interactive interview with Sean established the content strategy. Sean provided premade `.skill` files with Block-specific content. 4 skills received full Block-specific rewrites (meeting-prep, data-analysis, stakeholder-update/merged biweekly-jira-update, jira-automation/merged the-block-jira-ticket-writer). 1 new skill created (etf-page-creator). 1 skill adapted as general PM tool (sprint-roadmap with RICE/MoSCoW). 3 stub skills expanded from Q:≤2 to Q:5 (commit-checklist, org-definition-of-done, team-styleguide). All 94 skills now at Q:4-5.

### 4. ai-creative-tools Rewrite — RESOLVED (v3.4.0)

**Status:** REWRITTEN
**Resolution:** Full rewrite completed. Replaced fake "CLAUDE.md hooks" with real PostToolUse hooks in settings.json format. Removed hardcoded API keys, replaced with `os.environ` patterns. Added Hugging Face MCP integration (hub_repo_search, hub_repo_details, space_search, paper_search, dynamic_space). Added ComfyUI queue script with prompt injection and polling. Updated ElevenLabs to multilingual_v2 model with argparse CLI. Added asset index management (assets.json) and cross-references to sprite-asset-pipeline, pixel-art-retro-style, adobe-cross-app-workflows, and video-animation-production.

---

## Full Skill Inventory (Post-Phase 6)

### Claude Mastery (22 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 1 | cli-mastery | 5 | 5 | Keep |
| 2 | config-settings | 5 | 4 | Keep (absorbed claude-md-optimization in Phase 1) |
| 3 | hooks-configuration | 5 | 5 | Keep |
| 4 | mcp-integration | 5 | 5 | Keep |
| 5 | skill-system-mastery | 5 | 5 | Keep |
| 6 | subagent-orchestration | 5 | 5 | Keep |
| 7 | subagent-driven-development | 4 | 4 | Keep |
| 8 | context-management | 5 | 5 | Keep |
| 9 | plan-and-think | 5 | 5 | Keep |
| 10 | systematic-debugging | 5 | 5 | Keep |
| 11 | verification-loops | 4 | 4 | Keep |
| 12 | verification-before-completion | 5 | 5 | Keep |
| 13 | security-hardening | 5 | 4 | Keep (absorbed safe-ops + org-security in Phase 1) |
| 14 | headless-automation | 5 | 4 | Keep |
| 15 | chrome-workflows | 4 | 4 | Keep |
| 16 | parallel-instances | 4 | 3 | Keep |
| 17 | team-styleguide | 5 | 4 | ~~REWRITE~~ DONE (v3.6.0 — auto-detection, language rules, review workflow) |
| 18 | commit-checklist | 5 | 4 | ~~REWRITE~~ DONE (v3.6.0 — pre-commit validation, conventional commits, multi-commit strategy) |
| 19 | org-definition-of-done | 5 | 4 | ~~REWRITE~~ DONE (v3.6.0 — 4 DoD templates, release DoD, scored review workflow) |
| 20 | zapier-mcp-automation | 5 | 5 | NEW (Phase 2) — ~175 Zapier MCP tool patterns, task budget, recipes |
| 21 | personal-app-patterns | 5 | 5 | NEW (Phase 5) — React+Vite+Tailwind+Supabase starter patterns, auth, folder structure |
| 22 | rn-architecture | 5 | 5 | NEW (Phase 5) — Expo Router, Zustand, TanStack Query, EAS Build |

### Product Management (19 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 21 | prd-generator | 5 | 5 | Keep (absorbed quick-prd Quick Mode in Phase 1) |
| 22 | stakeholder-update | 5 | 5 | Keep (absorbed stakeholder-brief P1, merged biweekly-jira-update P4) |
| 23 | tech-spec | 5 | 4 | Keep |
| 24 | sprint-roadmap | 5 | 5 | ~~REWRITE~~ DONE (v3.6.0 — general PM tool with RICE/MoSCoW/Impact-Effort) |
| 25 | jira-automation | 5 | 5 | Keep (merged the-block-jira-ticket-writer P4 — Block config, templates, PRD workflow) |
| 26 | ticket-batch | 4 | 5 | Keep |
| 27 | data-analysis | 5 | 5 | ~~REWRITE~~ DONE (v3.6.0 — GA4/Looker/Zapier MCP, Block metrics) |
| 28 | meeting-prep | 5 | 5 | ~~REWRITE~~ DONE (v3.6.0 — standup, team roster, 1:1 prep, sprint planning) |
| 29 | decision-doc | 5 | 3 | Keep |
| 30 | doc-workflows | 4 | 3 | Keep |
| 31 | research-synthesis | 5 | 3 | Keep |
| 32 | ai-native-products | 5 | 4 | Keep |
| 33 | api-product-management | 5 | 4 | Keep |
| 34 | campus-education | 5 | 5 | Keep |
| 35 | crypto-web3-context | 5 | 5 | Keep |
| 36 | revops-adops-automation | 5 | 3 | Keep |
| 37 | analytics-workarounds | 5 | 5 | NEW (Phase 2) — GA4/Looker workarounds via Zapier MCP data bridge |
| 38 | etf-page-creator | 5 | 5 | NEW (Phase 4) — WordPress ETF page workflow for The Block |
| 39 | technical-writing | 5 | 5 | NEW (Phase 5) — API guides, system design docs, runbooks, RFCs |

### Creative Studio (25 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 40 | phaser-game-patterns | 5 | 5 | Keep (absorbed phaser-pattern in Phase 1) |
| 41 | sprite-asset-pipeline | 5 | 5 | Keep (absorbed sprite-pipeline in Phase 1) |
| 42 | pixel-art-retro-style | 5 | 5 | Keep |
| 43 | 2d-animation-principles | 5 | 5 | Keep |
| 44 | ai-creative-tools | 5 | 4 | REWRITTEN (Phase 2) — hooks, env vars, HF MCP, ComfyUI scripts |
| 45 | video-animation-production | 4 | 3 | Keep |
| 46 | creative-director | 5 | 5 | Keep |
| 47 | adobe-photoshop-mcp | 5 | 5 | Keep |
| 48 | adobe-premiere-mcp | 5 | 5 | Keep |
| 49 | adobe-aftereffects-mcp | 5 | 5 | Keep |
| 50 | adobe-illustrator-mcp | 5 | 5 | Keep |
| 51 | adobe-cross-app-workflows | 5 | 5 | Keep |
| 52 | remotion-fundamentals | 5 | 4 | Keep |
| 53 | remotion-claude-config | 5 | 4 | Keep |
| 54 | remotion-transitions | 5 | 4 | Keep |
| 55 | remotion-typography | 5 | 4 | Keep |
| 56 | remotion-data-viz | 5 | 3 | Keep |
| 57 | remotion-social-output | 5 | 4 | Keep |
| 58 | remotion-advanced | 5 | 4 | Keep |
| 59 | remotion-troubleshooting | 5 | 4 | Keep |
| 60 | animation-pipeline | 5 | 5 | NEW (Phase 5) — 12-stage pipeline, QA gates, shot packets, ComfyUI integration |
| 61 | script-writing | 5 | 5 | NEW (Phase 5) — Animated short screenplays, beat sheets, dialogue craft |
| 62 | creative-writing | 5 | 5 | NEW (Phase 5) — Blog, social media, pitch docs, artist statements |
| 63 | comfyui-workflows | 5 | 5 | NEW (Phase 6) — Workflow JSON, node patterns, LoRA/ControlNet, batch gen |

### Life Systems + Community (15 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 65 | personal-finance | 5 | 5 | Keep (absorbed budget-entry P1). DONE (v3.5.0 — Chase+Bilt parsers, debt paydown, subscription tracker, modified 50/30/20 budget) |
| 66 | personal-task-management | 4 | 4 | Keep |
| 67 | health-habits | 5 | 5 | DONE (v3.5.0 — PPL split, XP/level gamification, Apple Fitness pipeline, vault integration) |
| 68 | time-management | 5 | 5 | DONE (v3.5.0 — 45/35/20 split, energy map, Focus vs Meeting days, /today planning) |
| 69 | learning-accelerator | 4 | 4 | Keep (absorbed learning-drill in Phase 1) |
| 70 | life-admin | 5 | 5 | DONE (v3.5.0 — Boston move checklist, medical transition, address tracker, file audit, Cannes trip) |
| 71 | daily-driver | 5 | 5 | NEW (Phase 2) — Morning planning, EOD review, weekly review |
| 72 | subscription-audit | 5 | 5 | NEW (Phase 2) — Recurring expense analysis, keep/replace/cancel matrix |
| 73 | career-transition | 5 | 5 | NEW (Phase 5) — PM→Animation PM/Producer, terminology bridge, festival networking |
| 74 | learning-path | 4 | 3 | Keep |
| 75 | troubleshooting-guide | 4 | 3 | Keep |
| 76 | case-studies | 4 | 3 | Keep |
| 77 | changelog-navigator | 4 | 3 | Keep |
| 78 | community-navigation | 4 | 3 | Keep |
| 79 | zapier-chrome-automation | 4 | 4 | Keep |

### Design Team + Obsidian (14 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 80 | design-system-claude-md | 5 | 5 | Keep |
| 81 | tailwind-advanced-patterns | 5 | 5 | Keep |
| 82 | animation-library-mastery | 5 | 4 | Keep |
| 83 | prompting-beautiful-ui | 5 | 5 | Keep |
| 84 | micro-interaction-patterns | 5 | 4 | Keep |
| 85 | react-native-animations | 5 | 4 | Keep |
| 86 | visual-polish-checklist | 5 | 5 | Keep |
| 87 | figma-to-code-workflow | 5 | 5 | Keep |
| 88 | vault-architecture | 5 | 5 | Keep |
| 89 | vault-automation | 5 | 5 | Keep |
| 90 | vault-read-write | 5 | 5 | Keep (absorbed knowledge-management in Phase 2) |
| 91 | obsidian-mcp-setup | 5 | 5 | Keep |
| 92 | obsidian-semantic-search | 5 | 4 | Keep |
| 93 | knowledge-graph-nav | 5 | 5 | Keep |

### Technical Stack (10 skills)

| # | Skill | Quality | Relevance | Status |
|---|-------|---------|-----------|--------|
| 94 | react-vite-tailwind | 5 | 5 | Keep |
| 95 | supabase-backend | 5 | 5 | Keep (absorbed supabase-python in Phase 1) |
| 96 | python-automation | 5 | 4 | Keep (bug fixed in Phase 1) |
| 97 | git-github-workflows | 5 | 5 | Keep |
| 98 | docker-devops | 4 | 3 | Keep |
| 99 | cursor-integration | 5 | 5 | Keep |
| 100 | prototype-scaffold | 4 | 5 | Keep |
| 101 | rn-debug | 4 | 5 | Keep |

---

## Agent Inventory (Post-Phase 6)

| # | Agent | Quality | disallowedTools | Status |
|---|-------|---------|-----------------|--------|
| 1 | context-gatherer | 5 | `[Edit, Write, Bash]` | OK |
| 2 | doc-reviewer | 5 | `[Edit, Write, Bash]` | OK |
| 3 | checklist-validator | 4 | `[Edit, Write]` | OK (Bash intentionally allowed) |
| 4 | ui-reviewer | 5 | `[Edit, Write, Bash]` | OK |
| 5 | accessibility-checker | 5 | `[Edit, Write, Bash]` | OK |
| 6 | design-system-enforcer | 5 | `[Edit, Write, Bash]` | OK |
| 7 | visual-polish-auditor | 5 | `[Edit, Write, Bash]` | OK |
| 8 | security-reviewer | 4 | `[Edit, Write, Bash]` | FIXED in Phase 1 (was broken Cursor names) |
| 9 | compliance-summarizer | 3 | `[Edit, Write, Bash]` | FIXED in Phase 1 (was broken Cursor names) |
| 10 | data-analyst | 3 | `[Edit, Write, Bash]` | FIXED in Phase 1 (deny-list was missing) |
| 11 | game-design-advisor | 3 | `[Edit, Write, Bash]` | FIXED in Phase 1 (deny-list was missing) |
| 12 | animation-director | 5 | `[Edit, Write, Bash]` | NEW (Phase 5) — Animation QA review, pipeline compliance |
| 13 | code-reviewer | 5 | `[Edit, Write, Bash]` | NEW (Phase 5) — Architecture, patterns, performance, security |

**Security summary:** 13/13 agents properly configured (100%). Was 6/11 (55%) before Phase 1.

---

## Hook Inventory (Post-Phase 6)

| # | Hook | Trigger | Exit Codes | Quality | Known Issue |
|---|------|---------|-----------|---------|-------------|
| 1 | block-secrets.py | PreToolUse (Write\|Edit) | Correct (0/2) | 5 | Patterns narrowed in Phase 6 — no more false positives on "keyboard", "keynote", etc. |
| 2 | require-confirm-highrisk.sh | PreToolUse (Bash) | Correct (0/2) | 4 | `format` pattern matches `prettier --format` |
| 3 | log-tool-use.sh | PostToolUse (all) | Correct (0) | 3 | Fragile grep JSON parsing, no log rotation |
| 4 | format-on-edit.sh | PostToolUse (Write\|Edit) | Correct (0) | 3 | Race condition — background formatter can desync |
| 5 | run-tests-on-stop.sh | Stop | Correct (0) | 3 | Output discarded to /dev/null — failures invisible |
| 6 | daily-note-appender.sh | Stop | Correct (0) | 4 | NEW (Phase 6) — Appends session summary to Obsidian daily note |
| 7 | network-access-control.sh | PreToolUse (Bash) | Correct (0/2) | 4 | NEW (Phase 6) — Blocks non-whitelisted domains |

Hooks 6-7 added in Phase 6. Hook 1 narrowed in Phase 6. All hooks use correct exit codes.

---

## Remaining Redundancies

None. All redundancies resolved as of v3.4.0.

- knowledge-management was the last remaining redundancy. Resolved in Phase 2: unique content (Synthesis Protocol, /compress) merged into vault-read-write, then deleted.

---

## Skills Needing Rewrite or Tailoring

### Group A: Life-Systems Rewrites — COMPLETE (v3.5.0)

| Skill | Resolution |
|-------|-----------|
| health-habits | Rewritten with PPL split, 4:45 AM anchor, XP/level gamification, Apple Fitness pipeline, vault integration |
| personal-finance | Rewritten with Chase+Bilt CSV parsers, $5,741/mo net income, debt paydown calculator, modified 50/30/20 budget |
| time-management | Rewritten with 45/35/20 split, energy map, Focus Day vs Meeting Day, PEARL conflict resolution, /today planning |
| life-admin | Rewritten with Boston move checklist, medical provider transition, address change tracker, Cannes trip planning |

### Group B: Block PM Rewrites — COMPLETE (v3.6.0)

| Skill | Resolution |
|-------|-----------|
| meeting-prep | Rewritten with Block standup format, team roster, 1:1 prep template, sprint planning with Atlassian MCP |
| data-analysis | Rewritten with GA4/Looker access patterns, Zapier MCP data bridge, Block metrics |
| stakeholder-update | Merged biweekly-jira-update: biweekly sprint report, cross-team visibility, Atlassian MCP auto-pull |
| jira-automation | Merged the-block-jira-ticket-writer: Block Jira config, 4 ticket templates, PRD-to-tickets workflow |
| sprint-roadmap | Adapted as general PM tool: RICE scoring, MoSCoW, Impact/Effort matrix, capacity planning |
| commit-checklist | Expanded from stub: pre-commit validation, conventional commits, multi-commit strategy |
| org-definition-of-done | Expanded from stub: 4 DoD templates, Release DoD, scored review workflow |
| team-styleguide | Expanded from stub: config auto-detection, language rules, review workflow |
| etf-page-creator | NEW: WordPress ETF page workflow, SEO auto-generation, validation rules |

### Group C: Technical Rewrites — COMPLETE (v3.4.0)

| Skill | What Was Wrong | Resolution |
|-------|---------------|------------|
| ai-creative-tools | Outdated hook patterns, placeholder API keys | REWRITTEN — real PostToolUse hooks, env vars, HF MCP integration, ComfyUI queue script, ElevenLabs multilingual_v2 |

---

## Gap Analysis: New Skills Needed

### Tier 1 — Build Now (supports current goals) — COMPLETE

| Skill | Domain | Status | Notes |
|-------|--------|--------|-------|
| **daily-driver** | Life Systems | DONE (v3.4.0) | Morning planning, EOD review, weekly review, Obsidian integration |
| **subscription-audit** | Life Systems | DONE (v3.4.0) | CSV parsing, recurring charge detection, keep/replace/cancel matrix |
| **analytics-workarounds** | PM | DONE (v3.4.0) | GA4 via Zapier MCP, Sheets as data hub, BigQuery public datasets |
| **animation-pipeline** | Creative Studio | DONE (v3.7.0) | 12-stage pipeline, QA gates, shot packets, ComfyUI integration, frame interpolation |

### Tier 2 — Build Soon (supports near-term projects)

| Skill | Domain | Status | Notes |
|-------|--------|--------|-------|
| **script-writing** | Creative Studio | DONE (v3.7.0) | Animated short screenplays, beat sheets, dialogue craft, production handoff |
| **creative-writing** | Creative Studio | DONE (v3.7.0) | Blog, social media, pitch docs, artist statements, portfolio narratives |
| **technical-writing** | PM | DONE (v3.7.0) | API guides, system design docs, runbooks, RFCs, onboarding guides |
| **zapier-mcp-automation** | Mastery | DONE (v3.4.0) | ~175 tool patterns, task budget, 4 workflow recipes |
| **career-transition** | Life Systems | DONE (v3.7.0) | PM→Animation PM/Producer, terminology bridge, festival networking, 90-day plan |

### Tier 3 — Build When Ready (future capabilities)

| Skill | Domain | Status | Notes |
|-------|--------|--------|-------|
| **comfyui-workflows** | Creative Studio | DONE (v3.8.0) | Workflow JSON, node patterns, LoRA/ControlNet/IPAdapter, batch gen |
| **personal-app-patterns** | Tech Stack | DONE (v3.7.0) | React+Vite+Tailwind+Supabase starter patterns, auth, folder structure |
| **rn-architecture** | Tech Stack | DONE (v3.7.0) | Expo Router, Zustand, TanStack Query, EAS Build profiles |

---

## Gap Analysis: New Agents — COMPLETE (v3.7.0)

| Agent | Role | disallowedTools | Phase | Status |
|-------|------|-----------------|-------|--------|
| **animation-director** | Reviews animation assets for consistency, timing, style adherence | `[Edit, Write, Bash]` | Phase 5 | DONE |
| **code-reviewer** | General code quality review (architecture, patterns, performance) | `[Edit, Write, Bash]` | Phase 5 | DONE |

---

## Gap Analysis: New Hooks — COMPLETE (v3.8.0)

| Hook | Event | Purpose | Phase | Status |
|------|-------|---------|-------|--------|
| **daily-note-appender** | Stop | On session end, append a summary of what was accomplished to today's Obsidian daily note | Phase 6 | DONE |
| **network-access-control** | PreToolUse (Bash) | Block `curl`, `wget`, `nc` to untrusted URLs. Whitelist-based domain control. | Phase 6 | DONE |

---

## Domain Organization Review

**The 6 domains are correctly structured.** No skills are fundamentally misplaced.

| Observation | Status |
|-------------|--------|
| `2d-animation-principles` is not in any export group | RESOLVED (Phase 2) — added to `03-creative-projects` |
| `knowledge-management` superseded by vault domain | RESOLVED (Phase 2) — merged into vault-read-write, deleted |
| `learning-drill` was in wrong export group (09 instead of 05) | Resolved (Phase 1) — merged into learning-accelerator and deleted |
| `zapier-chrome-automation` was not in any export group | Resolved (Phase 1) — added to `04-advanced-techniques` alongside `chrome-workflows` |
| `etf-page-creator` placement | Resolved (Phase 4) — added to `08-domain-specific` (Block-specific) |

**The vault domain remains the architectural model:** infrastructure (obsidian-mcp-setup) to structure (vault-architecture) to search (obsidian-semantic-search) to navigation (knowledge-graph-nav) to automation (vault-automation) to operations (vault-read-write).

---

## Adobe Mastery Assessment

**Rating: 9/10 — Outstanding.** No changes since v2.0 audit. The 6 Adobe skills form a complete production-grade system.

See v2.0 audit for full details on MCP tool coverage, workflow coverage, and minor gaps (Adobe Character Animator, aerender CLI, Dynamic Link).

---

## Zapier MCP Integration Opportunities

The dedicated `zapier-mcp-automation` skill (created in Phase 2) covers general patterns. Integration status:

| Skill | Zapier Tools to Reference | Integration Pattern | Status |
|-------|--------------------------|-------------------|--------|
| jira-automation | Jira MCP (22 tools) | Zapier as fallback bridge for Atlassian MCP | DONE (P4) — references both Atlassian and Zapier MCP |
| data-analysis | GA4 Run Report, Google Sheets | Pull analytics via Zapier, analyze with Claude, output to Sheets | DONE (P4) — 4 data access tiers |
| sprint-roadmap | Jira, Google Calendar, Slack | Auto-generate sprint reports, post to Slack | DONE (P4) — JQL patterns for backlog grooming |
| meeting-prep | Google Calendar, Slack, Confluence | Pull events, generate agendas, post pre-reads | DONE (P4) — Atlassian MCP integration |
| stakeholder-update | Gmail, Slack, Google Docs | Generate update, push to multiple channels | DONE (P4) — Atlassian MCP auto-pull |
| personal-finance | Google Sheets, Zapier Tables | Write categorized transactions, generate reports | DONE (P3) — references Sheets integration |
| health-habits | Google Sheets | Log workouts/streaks to tracking sheet | DONE (P3) — references Sheets for tracking |
| time-management | Google Calendar | Pull calendar data for time audit | DONE (P3) — Google Calendar OAuth plan |

---

## Prioritized Action Plan

### Phase 1: Consolidation — COMPLETE (v3.3.0, Feb 17 2026)

All 16 items completed. See Phase 1 Completion Report above for full details.

| # | Action | Status |
|---|--------|--------|
| 1 | Fix security-reviewer deny-list | DONE |
| 2 | Fix compliance-summarizer deny-list | DONE |
| 3 | Add deny-list to data-analyst | DONE |
| 4 | Add deny-list to game-design-advisor | DONE |
| 5 | Delete safe-ops | DONE |
| 6 | Delete org-security | DONE |
| 7 | Delete quick-prd (add Quick Mode to prd-generator) | DONE |
| 8 | Merge stakeholder-brief into stakeholder-update | DONE |
| 9 | Merge supabase-python into supabase-backend | DONE |
| 10 | Merge claude-md-optimization into config-settings | DONE |
| 11 | Merge phaser-pattern into phaser-game-patterns | DONE |
| 12 | Merge sprite-pipeline into sprite-asset-pipeline | DONE |
| 13 | Merge learning-drill into learning-accelerator | DONE |
| 14 | Merge budget-entry into personal-finance | DONE |
| 15 | Fix python-automation `title: string` bug | DONE |
| 16 | Update 7 export-group manifests | DONE |

### Phase 2: New Skills & Technical Rewrites — COMPLETE (v3.4.0, Feb 17 2026)

All 9 items completed. 4 new skills created, 1 skill rewritten, 1 skill merged+deleted, 4 manifest updates.

| # | Action | Status |
|---|--------|--------|
| 17 | Create daily-driver skill | DONE |
| 18 | Create subscription-audit skill | DONE |
| 19 | Create analytics-workarounds skill | DONE |
| 20 | Rewrite ai-creative-tools (hooks, env vars, HF MCP, ComfyUI scripts) | DONE |
| 21 | Create zapier-mcp-automation skill | DONE |
| 22 | Add 2d-animation-principles to 03-creative-projects manifest | DONE |
| 23 | ~~Add zapier-chrome-automation to export group~~ | DONE (v3.3.0) |
| 24 | Resolve knowledge-management (merged Synthesis Protocol + /compress into vault-read-write, deleted) | DONE |
| 25 | ~~Add CHANGELOG 3.3.0 entry~~ | DONE (v3.3.0) |

### Phase 3: Life-Systems Rewrites — COMPLETE (v3.5.0, Feb 17 2026)

Interactive interview conducted with Sean. All 4 skills rewritten with personalized data.

| # | Action | Files | Effort | Status |
|---|--------|-------|--------|--------|
| 26 | ~~Rewrite health-habits~~ | `.claude/skills/health-habits/SKILL.md` | Medium | DONE — PPL split, 4:45 AM anchor, XP/level gamification, Apple Fitness pipeline, vault integration |
| 27 | ~~Rewrite personal-finance~~ | `.claude/skills/personal-finance/SKILL.md` | Medium | DONE — Chase+Bilt CSV parsers, $5,741/mo net income, subscription tracker, debt paydown calculator, modified 50/30/20 budget |
| 28 | ~~Rewrite time-management~~ | `.claude/skills/time-management/SKILL.md` | Medium | DONE — 45/35/20 work split, energy map, Focus Day vs Meeting Day, PEARL conflict resolution, /today daily planning |
| 29 | ~~Rewrite life-admin~~ | `.claude/skills/life-admin/SKILL.md` | Medium | DONE — Boston move checklist (March 21), medical provider transition (Medvidi→Aetna), address change tracker, file audit, Cannes trip planning |

### Phase 4: Block PM Rewrites — COMPLETE (v3.6.0, Feb 18 2026)

All 9 items completed. 4 full Block rewrites, 1 new skill, 1 adapted general tool, 3 stubs expanded to Q:5.

| # | Action | Files | Effort | Status |
|---|--------|-------|--------|--------|
| 30 | ~~Rewrite meeting-prep~~ | `.claude/skills/meeting-prep/SKILL.md` | Medium | DONE — standup, team roster, 1:1 prep, sprint planning, Atlassian MCP |
| 31 | ~~Rewrite sprint-roadmap~~ | `.claude/skills/sprint-roadmap/SKILL.md` | Medium | DONE — adapted as general PM tool (RICE, MoSCoW, Impact-Effort) |
| 32 | ~~Rewrite data-analysis~~ | `.claude/skills/data-analysis/SKILL.md` | Medium | DONE — GA4/Looker access patterns, Zapier MCP bridge, Block metrics |
| 33 | ~~Rewrite commit-checklist~~ | `.claude/skills/commit-checklist/SKILL.md` | Quick | DONE — pre-commit validation, conventional commits, multi-commit strategy |
| 34 | ~~Rewrite org-definition-of-done~~ | `.claude/skills/org-definition-of-done/SKILL.md` | Quick | DONE — 4 DoD templates (Feature/Bug/Refactor/Spike), Release DoD |
| 35 | ~~Rewrite team-styleguide~~ | `.claude/skills/team-styleguide/SKILL.md` | Medium | DONE — config auto-detection, language rules, review workflow |
| 35a | Rewrite stakeholder-update (merge biweekly-jira-update) | `.claude/skills/stakeholder-update/SKILL.md` | Medium | DONE — biweekly Jira sprint report, cross-team visibility format |
| 35b | Rewrite jira-automation (merge the-block-jira-ticket-writer) | `.claude/skills/jira-automation/SKILL.md` | Medium | DONE — Block Jira config, 4 ticket templates, PRD-to-tickets workflow |
| 35c | Create etf-page-creator | `.claude/skills/etf-page-creator/SKILL.md` | Medium | DONE — WordPress ETF page workflow, SEO auto-generation, validation |

### Phase 5: Creative Pipeline & Career Skills — COMPLETE (v3.7.0, Feb 18 2026)

All 7 items completed. 7 new skills, 2 new agents, 4 manifest updates.

| # | Action | Files | Effort | Status |
|---|--------|-------|--------|--------|
| 36 | Create animation-pipeline skill | `.claude/skills/animation-pipeline/SKILL.md` | Significant | DONE |
| 37 | Create script-writing skill | `.claude/skills/script-writing/SKILL.md` | Medium | DONE |
| 38 | Create creative-writing skill | `.claude/skills/creative-writing/SKILL.md` | Medium | DONE |
| 39 | Create technical-writing skill | `.claude/skills/technical-writing/SKILL.md` | Medium | DONE |
| 40 | Create career-transition skill | `.claude/skills/career-transition/SKILL.md` | Medium | DONE |
| 41 | Create animation-director agent | `.claude/agents/animation-director.md` | Quick | DONE |
| 42 | Create code-reviewer agent | `.claude/agents/code-reviewer.md` | Quick | DONE |

### Phase 6: Future Capabilities — COMPLETE (v3.8.0, Feb 18 2026)

All 7 items completed. 1 new skill, 2 new hooks, 1 hook narrowed, manifests updated.

| # | Action | Files | Effort | Status |
|---|--------|-------|--------|--------|
| 43 | Create comfyui-workflows skill | `.claude/skills/comfyui-workflows/SKILL.md` | Significant | DONE |
| 44 | Create personal-app-patterns skill | `.claude/skills/personal-app-patterns/SKILL.md` | Medium | DONE (Phase 5) |
| 45 | Create rn-architecture skill | `.claude/skills/rn-architecture/SKILL.md` | Medium | DONE (Phase 5) |
| 46 | Create daily-note-appender hook | `.claude/hooks/daily-note-appender.sh` | Medium | DONE |
| 47 | Create network-access-control hook | `.claude/hooks/network-access-control.sh` | Medium | DONE |
| 48 | Narrow block-secrets.py patterns | `.claude/hooks/block-secrets.py` | Quick | DONE |
| 49 | Update all export-group manifests for new skills | `export-groups/*/playground.json` | Medium | DONE |

---

## Final Skill Count

| Stage | Skills | Agents | Hooks | Status |
|-------|--------|--------|-------|--------|
| Pre-audit (v3.2.0) | 99 | 11 | 5 | Baseline |
| After Phase 1 (v3.3.0) | 90 | 11 | 5 | COMPLETE |
| After Phase 2 (v3.4.0) | 93 | 11 | 5 | COMPLETE |
| After Phase 3 (v3.5.0) | 93 | 11 | 5 | COMPLETE |
| After Phase 4 (v3.6.0) | 94 | 11 | 5 | COMPLETE |
| After Phase 5 (v3.7.0) | 101 | 13 | 5 | COMPLETE |
| **After Phase 6 (v3.8.0)** | **102** | **13** | **7** | **CURRENT** |

All 6 phases complete. 102 skills, 13 agents, 7 hooks. Every addition is a targeted, personalized skill. No stubs or duplicates.

---

## Lessons Learned During Audit

These are operational notes for future sessions working on this pack.

1. **Background subagents can only use read-only tools.** Running agents with `run_in_background: true` auto-denies any tool that requires user permission prompts. Tested in v3.8.1:

   | Tool | Background Mode | Error |
   |------|----------------|-------|
   | Read | **Works** | — |
   | Glob | **Works** | — |
   | Grep | **Works** | — |
   | Write | **Blocked** | `Permission to use Write has been auto-denied (prompts unavailable).` |
   | Edit | **Blocked** | Same mechanism as Write |
   | Bash | **Blocked** | `Permission to use Bash has been auto-denied (prompts unavailable).` |

   **Not silent** — returns an explicit error (updated from original "fails silently" note).
   **Workaround:** Use background agents for research only (Read/Glob/Grep). Capture the text output returned by the agent, then write files in the foreground parent context.
   **Pattern:** `run_in_background: true` → agent returns text → parent uses Write/Edit with the results.

2. **Read before Edit.** The Edit tool requires a recent Read of the same file. If a sibling tool call errors out, the Read may be invalidated. Always re-read before editing if there's any doubt.

3. **Sequential edits to the same file need re-reads.** After Edit modifies a file, the old content is stale. Read the file again before making a second edit to the same file.

4. **validate.py catches orphans.** It found `plugin/skills/safe-ops/` still existed after the main skill was deleted. Always run validation after deletions.

5. **Export-group manifests are metadata-only.** Skills live in `.claude/skills/`. Export groups just list skill names. When deleting a skill, update both the skill directory AND any referencing manifests.

6. **Skill YAML frontmatter format matters.** Every skill needs `name` and `description` in the YAML frontmatter between `---` delimiters. The description is what triggers skill activation — make it rich with trigger phrases.

7. **Agent deny-lists use `disallowedTools` (not allow-lists).** The YAML key is `disallowedTools` and values are the exact tool names: `Edit`, `Write`, `Bash` (capitalized).

8. **Hook exit code 2 = deny.** Not 0 or 1. Exit 0 = allow, exit 1 = error (logged but allowed), exit 2 = deny (blocks the operation).

9. **Export-group skill name collisions.** Each skill can only appear in ONE export group. validate.py catches collisions. When a skill fits multiple groups, choose the most specific one.

10. **Write tool requires Read in same context.** After context compaction, earlier reads don't count. Re-read with `limit=5` before writing to satisfy the requirement.

11. **.skill files are ZIP archives.** Premade `.skill` files from Claude Desktop have PK headers — extract with `unzip` before reading the SKILL.md inside.

---

*Updated by Claude Code (Opus 4.6) on February 19, 2026. Reflects v3.8.0 post-Phase-6 state (all phases complete).*
*Previous versions: v2.2/v3.6.0 (Phase 1-4, Feb 18), v2.1/v3.4.0 (Phase 1-2, Feb 17), v2.0 (Feb 16, pre-consolidation), v1.0 (Feb 15, initial audit) — archived in git history.*
