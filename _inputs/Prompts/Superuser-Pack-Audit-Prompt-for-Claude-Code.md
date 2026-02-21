# Superuser Pack Skills Audit — Claude Code Prompt

---

## PROMPT START

You are auditing Sean Winslow's Claude Code Superuser Pack — a personal command center repo containing skills, agents, and hooks across 6 domain workspaces. This audit was originally started in a Claude.ai conversation thread. You are continuing that work with the advantage of being able to **read every skill file directly**.

### Who Sean Is (Personal Context)

**Current role:** Associate Product Manager (Technical) at The Block (crypto news/data/research). Started November 10, 2025. Reports to a PM → VP of Product. Leads daily standups with devs and his PM manager. Work split: 45% building (Zapier automations, Campus 201 features, dev coordination), 35% meetings (Tue-Thu concentrated), 20% firefighting.

**Background:** 33 years old. 12 years as a NYC freelance creative (illustration, animation, film). Career-switched to PM in 2024 by investing in PM classes and AI tools — this worked but created credit card debt that's now a priority. Moving to Boston with girlfriend on March 21, 2026.

**Dream career (2-3 years):** Remote PM in the animation/creative industry, combining technical PM skills with animation/storytelling abilities.

**The pipeline connecting everything:**
1. Sprite automation for 16BitFit → learns AI image generation pipelines
2. Transfer sprite automation to cartoon animation → train models in personal art style
3. Produce animated shorts/series using AI-assisted pipeline
4. Submit to animation + AI film festivals → build portfolio + reputation
5. Transition to PM role in animation industry

**This is not scattered projects — it's career R&D. Every side project feeds this trajectory.**

**Creative profile:**
- Animation style: Flat 2D / frame-by-frame
- Tools: Procreate, Adobe Character Animator, Adobe Premiere Pro, After Effects (growing)
- Output: 5 animated shorts (one made entirely with Nano Banana Pro + Kling/Veo 3.1)
- Won best short comedy animation at multiple indie festivals (Filmfreeway)
- Has a full 2D animation reference library in NotebookLM, translated into a Claude Skill (`2d-animation-principles`)
- Interested in motion graphics libraries beyond Remotion, After Effects integration, ComfyUI

**Active projects:**

| Project | Status | Details |
|---------|--------|---------|
| 16BitFit | ~50% done | Game Boy fitness RPG (Phaser 3 + React Native + Vite + Tailwind + Supabase). Blocked on sprite consistency. Pipeline: anchor image → Claude Code → vision audit → post-process → TexturePacker. |
| Superuser Pack | Active | This repo. Growing rapidly with new skills including Adobe Mastery. |
| Prototypes project | Skeleton built | Vite + vanilla HTML/CSS/JS. Folders: Campus, TheBlock.co, personal. Shared UI layer + Claude Code skills for PRD→prototype. Netlify Deploy Previews. |
| Animation pipeline | R&D | Transfer sprite automation → cartoon animation → festival submissions. |
| Personal finance tracker | Idea stage | Rocket Money replacement. Desktop/laptop app. |
| Photo organizer | Idea stage | Swipe left/right UI with sound effects. |
| Gamified habit tracker | Idea stage | Fun, non-strict motivation tracker. |

**Technical environment:**
- Hardware: macOS daily driver + Windows 11 Alienware with RTX 5080 for ComfyUI/AI workloads
- IDEs: Cursor (primary), Anti-Gravity, VS Code
- Stack: React/Vite/Tailwind, React Native, Python, Supabase, Docker, Phaser 3
- AI: Claude Code (power user), Claude.ai, ChatGPT, Gemini, NotebookLM, ComfyUI, ElevenLabs
- Work: Jira, Confluence, Slack, Figma, Zapier, WordPress, Salesforce, GA4/Looker
- Knowledge: Obsidian Vault (just started, building from scratch), Has the skeleton built out from a previous Claude Code session, Apple Notes (migrating from), NotebookLM
- **NEW: Zapier MCP connected with ~175 tools across 12 apps (GA4, Gemini, Google Docs, Confluence, Jira, Gmail, Salesforce, Google Sheets, Zapier Tables, Google Calendar, Slack, Google Drive). GA4 "Run Report for a Property" confirmed working as analytics workaround.**
- **NEW: Adobe MCP — Claude Code now connected to Adobe products (Premiere Pro, Photoshop, After Effects, Illustrator via adb-mcp or similar)**

You can find the documents and more information within this file path: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/docs/

**Goals by timeframe:**

*30-90 days:*
- Second brain operational via Claude Code + Obsidian Vault
- Superuser Pack consolidated and expanded
- Subscription audit completed → cost savings
- Progress on 16BitFit sprite pipeline
- Prepare for Boston move (March 21)

*6-12 months:*
- Side projects generating income
- Visual progress tracking across all domains
- Claude Code functioning as personal assistant
- Animation pipeline prototyped
- Credit card debt reduced, savings started

*2-3 years:*
- PM role in animation/creative industry (remote)
- AI animation pipeline operational, trained on personal style
- Animated work submitted to film/AI film festivals
- Engagement ring + house savings on track

**Learning style:** Tutorials → LLM chat → build by doing → document. Uses NotebookLM for research synthesis. Decision-making: steps away, walks, lets solutions surface.

**What energizes him:** Design/media team collaboration, building automated workflows, creative brainstorming, learning new tools.

**What drains him:** Repetitive manual tasks (many already automated via skills), access limitations.

---

### What the Previous Audit Found

The first audit (conducted before you had direct file access) identified:

**8 redundancy pairs to consolidate:**
1. `prd-generator` + `quick-prd` → merge with mode flag
2. `stakeholder-update` + `stakeholder-brief` → merge into `stakeholder-comms`
3. `phaser-game-patterns` + `phaser-pattern` → merge into `phaser-game-dev`
4. `sprite-pipeline` + `sprite-asset-pipeline` → merge into unified `sprite-pipeline`
5. `learning-accelerator` duplicated in Claude Mastery + Life Systems → keep one, reference
6. `learning-drill` duplicated → keep one, reference
7. `python-automation` duplicated in Claude Mastery + Tech Stack → keep in Tech Stack
8. `docker-devops`, `git-github-workflows`, `prototype-scaffold` duplicated → keep in Tech Stack

**6 skills needing tailoring:**
- `campus-education` → add The Block Campus 201 specifics
- `revops-adops-automation` → add The Block Salesforce/WordPress workflows
- `crypto-web3-context` → add The Block product lines/API models
- `personal-finance` → customize to Sean's spending patterns, subscription audit
- `health-habits` → add Sean's 4:45 AM routine, gamification hooks
- `sprite-pipeline` → bake in specific anchor→Claude Code→vision→TexturePacker workflow, add ComfyUI branch

**12 new skills recommended (prioritized):**

*Tier 1 (Build now):* `daily-driver`, `subscription-audit`, `animation-pipeline`, `script-writing`, `technical-writing`, `creative-writing`

*Tier 2 (Build soon):* `zapier-to-claude-migration`, `analytics-workarounds`, `career-transition`, `motion-graphics-libraries`

*Tier 3 (Build when ready):* `comfyui-workflows`, `personal-app-patterns`

**2 new agents recommended:** `animation-director` (read-only, reviews animation assets), `financial-advisor` (read-only, reviews spending data)

**3 new hooks recommended:** `expense-logger` (PostToolUse), `daily-note-appender` (Stop), `project-time-tracker` (SessionStart + Stop)

**That audit was based on a skill list I provided verbally. You now have the advantage of reading every file. Things have changed since then — new skills have been added, including Adobe Mastery skills. Your audit should be fresh, comprehensive, and based on what actually exists now.**

---

### Your Audit Task

**Phase 1: Discovery (Do this first)**

1. Read the repo's `CLAUDE.md` for architecture understanding
2. List every directory in `.claude/skills/` and count total skills
3. List every file in `.claude/agents/` and count total agents
4. List every file in `.claude/hooks/` (or `shared/hooks/`) and count total hooks
5. Read the `settings.json` for configuration context
6. Scan each domain workspace directory for working files, templates, and references

**Phase 2: Deep Skill Analysis**

For EVERY skill file, read its contents and evaluate:

- **Purpose clarity:** Does the skill have a clear, focused purpose? Or is it trying to do too much?
- **Quality:** Is the content detailed and actionable, or is it surface-level placeholder text?
- **Relevance to Sean's goals:** Rate High / Medium / Low based on his career trajectory, active projects, and daily work
- **Overlap detection:** Does this skill duplicate content from another skill? Flag exact overlaps AND partial overlaps
- **Tailoring needed:** Is it generic boilerplate, or customized to Sean's specific context (The Block, his projects, his tools)?
- **Completeness:** Is the skill thorough, or does it have obvious gaps?

**Phase 3: Agent & Hook Analysis**

For each agent:
- Read the agent file
- Assess whether `disallowedTools` is properly configured (deny-list approach, not allow-list)
- Evaluate relevance to Sean's current and near-future needs
- Flag any agents that should be read-only but aren't

For each hook:
- Read the hook source file
- Verify exit code logic (0 = allow, 1 = error/allow, 2 = deny)
- Assess practical utility

**Phase 4: Gap Analysis**

Based on everything you've read, identify:
1. **Skills that should exist but don't** — considering Sean's goals, projects, tools, and the Adobe MCP addition
2. **Skills that should be merged** — with specific file paths and a recommended merge strategy
3. **Skills that should be deleted** — if they add no value or are completely superseded
4. **Skills that need rewriting** — if the content is too thin, too generic, or outdated
5. **Domain organization issues** — skills in the wrong domain, or domains that need restructuring
6. **Agent gaps** — agents that should exist based on Sean's workflow
7. **Hook gaps** — hooks that would automate parts of Sean's routine

**Phase 5: Prioritized Action Plan**

Organize all recommendations into a phased build order:

- **Phase 1 (This week):** Consolidations, deletions, and quick wins that reduce noise immediately
- **Phase 2 (Next 2-3 weeks):** New skills that directly support current work and projects
- **Phase 3 (Next month):** Skills that support near-term side projects and creative pipeline
- **Phase 4 (Ongoing):** Career transition skills, advanced capabilities, future-state tools

For each recommendation, include:
- What to do (merge / delete / create / rewrite / move)
- Which files are affected (exact paths)
- Why it matters to Sean's goals
- Estimated effort (quick / medium / significant)

---

### Output Format

Produce a single comprehensive markdown document with these sections:

```
# Superuser Pack Skills Audit v2.0
## Executive Summary (counts, key findings, what changed since v1.0)
## Full Skill Inventory (table: skill name | domain | file path | purpose | quality rating | relevance rating)
## Agent Inventory (table: agent name | file path | purpose | properly configured?)
## Hook Inventory (table: hook name | file path | purpose | exit codes correct?)
## Redundancies & Merges (specific file pairs with merge strategy)
## Skills Needing Rewrite or Tailoring (what's wrong, what to fix)
## Skills to Delete (why they add no value)
## Gap Analysis: New Skills Needed (prioritized with rationale)
## Gap Analysis: New Agents Needed
## Gap Analysis: New Hooks Needed
## Domain Organization Review (anything misplaced?)
## Adobe Mastery Assessment (specific review of new Adobe skills — completeness, gaps, integration opportunities)
## Zapier MCP Integration Opportunities (skills that should reference or leverage the ~175 Zapier tools now available)
## Prioritized Action Plan (phased, with file paths and effort estimates)
## Final Skill Count Projection (before → after consolidation → after additions)
```

---

### Audit Principles (How to Think About This)

1. **Every skill should earn its context window tokens.** If a skill is vague, thin, or duplicated, it's costing Sean performance. Be ruthless about consolidation.

2. **Generic ≠ useful.** A skill that says "write good PRDs" is less valuable than one that says "write PRDs for The Block's Campus education platform using their specific course structure and crypto education taxonomy." Flag anything that reads like a blog post instead of a personalized playbook.

3. **Cross-domain connections matter.** Sean's projects aren't siloed — sprite automation feeds animation pipeline feeds career transition. Skills should reference each other where relevant. Flag opportunities for cross-linking.

4. **The career trajectory is the north star.** Everything should ultimately serve: PM work at The Block (pays the bills) → creative side projects (builds the portfolio) → animation/creative industry PM role (the dream). Skills that don't connect to this pipeline deserve extra scrutiny.

5. **Adobe Mastery is new and critical.** Sean just discovered he can connect Claude Code to Adobe products. These skills are likely fresh and may need significant expansion. Evaluate them with extra attention — are they leveraging the full capabilities of the Adobe MCP? Do they cover Premiere Pro, After Effects, Photoshop, and Illustrator workflows that support both his PM work (Campus animations, content creation) and his creative pipeline (animated shorts, motion graphics)?

6. **Zapier MCP changes the game.** Sean now has ~175 Zapier tools available. Skills that previously said "manually export data" or "copy-paste from GA4" should be updated to leverage the Zapier bridge. Flag any skill that could be enhanced by Zapier MCP integration.

7. **Obsidian Vault integration.** Sean is building his second brain in Obsidian. Skills should reference vault workflows where relevant (daily notes, MOCs, project pages). The vault is still early, so note where skills should eventually connect to it.

8. **Financial awareness.** Sean is paying down credit card debt. Skills that help save money (subscription audit, free tool alternatives) or generate income (side project patterns, freelance workflows) deserve priority over nice-to-haves.

Save the output to the project root as `SKILLS-AUDIT-v2.md`.


