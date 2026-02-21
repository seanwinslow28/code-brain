# Phase 3 & 4 Kickoff — Skills Audit Continuation

## Instructions

Read these two documents fully before starting:

1. `@docs/Superuser-Pack-Skills-Audit.md` — The authoritative audit document. Start with the **Handoff Guide** at the top, then read the Phase 3 and Phase 4 sections of the **Prioritized Action Plan** for exact task lists.
2. `@docs/Sean-Winslow-Full-Personal-Context-v1.1.md` — Sean's personal context. This gives an overview of his life, routines, finances, work, and goals — but it's NOT enough to write complete skills on its own.

## Execution Order

**Phase 3 first, then Phase 4.** Do not start Phase 4 until Phase 3 is fully complete.

---

## Phase 3: Life-Systems Rewrites (4 skills)

These skills exist but are generic stubs. Each needs to be rewritten with Sean's actual personal data.

### Step 1: Read the Current Skills

Read all 4 current SKILL.md files to understand what exists:

- `.claude/skills/health-habits/SKILL.md`
- `.claude/skills/personal-finance/SKILL.md`
- `.claude/skills/time-management/SKILL.md`
- `.claude/skills/life-admin/SKILL.md`

### Step 2: Conduct the Phase 3 Interview

The personal context document provides a high-level overview, but to write truly useful, personalized skills, you need specifics. **Before writing anything**, interview Sean with targeted questions for each skill.

Cross-reference what you already know from the context doc against what a complete skill would need. Then ask Sean only for the **gaps** — the specific data points you can't infer.

**For health-habits, you need to know:**
- Exact gym routine: What exercises? What split (push/pull/legs, upper/lower, full body)? What does a typical workout look like?
- Tracking method: Does he currently track workouts anywhere? App, notebook, nothing?
- Meals: Are the meals in the context doc (eggs/spinach, yogurt bowls, chicken) the actual recurring meals, or just examples? Any meal prep patterns?
- Supplements or specific nutrition targets (protein grams, calories)?
- What kind of gamification does he want? XP per workout? Streak tracking? Level-ups? Visual progress?
- Weekend workouts: What does "short workout" mean specifically?
- Any injuries, limitations, or exercises to avoid?

**For personal-finance, you need to know:**
- How many credit cards? Approximate total debt range? (He doesn't need to share exact numbers if uncomfortable — ranges are fine)
- Which bank(s)? What format do CSV exports come in? (Column names matter for the skill)
- Current subscriptions he's paying for (even a rough list helps)
- Monthly income range or budget targets?
- Does he use any budgeting method currently (envelope, 50/30/20, zero-based)?
- Specific savings goals with target amounts or timelines?
- How does he want to visualize financial progress?

**For time-management, you need to know:**
- Exact morning routine timing: 4:45 wake → coffee → gym → breakfast → side projects → work start time?
- Work hours: What time does the 8-hour block start and end?
- Meeting schedule: How many meetings per day Tue-Thu? Are Mon/Fri meeting-free?
- Deep work blocks: When does he do his best focused work?
- Energy patterns: When is he most/least productive during the day?
- How does he currently decide what to work on each day?
- Evening routine: Any wind-down habits, screen cutoff time, bedtime?

**For life-admin, you need to know:**
- Boston move: Is March 21 still the date? What specific tasks remain (utilities, address changes, forwarding mail, lease termination)?
- Recurring admin tasks: What comes up regularly? (Bills, insurance, car stuff, medical appointments?)
- What admin tasks has he already automated vs. what's still manual?
- File organization: Does he have a system or is it chaos?
- Important accounts/services that need address updates?
- Any upcoming life events besides the move (lease renewals, insurance changes, tax deadlines)?

**Present these as a structured interview** — group them by skill and make it easy for Sean to answer. Don't dump all questions at once. Start with one skill at a time.

### Step 3: Write the Skills

After collecting Sean's answers, rewrite each skill:

1. Keep the YAML frontmatter format (`name`, `description` between `---` delimiters)
2. Keep the section structure (Purpose, When to Use, Examples, Core Workflows, Success Criteria, Copy/Paste Ready)
3. Replace generic content with Sean's actual data
4. Make the `description` field rich with trigger phrases so the skill activates correctly
5. Run `python3 scripts/validate.py` after each rewrite

### Step 4: Update Documentation

After all 4 Phase 3 skills are rewritten:

1. Update `docs/Superuser-Pack-Skills-Audit.md`:
   - Mark Phase 3 items (#26-29) as DONE in the Prioritized Action Plan
   - Add a Phase 3 Completion Report section (like Phase 1 and Phase 2 reports)
   - Update skill Quality ratings in the inventory tables
   - Update the "What's Left To Do" summary
2. Update `SKILLS-AUDIT-v2.md` (repo root) to match
3. Update `CHANGELOG.md` with a new version entry
4. Run final `python3 scripts/validate.py`

---

## Phase 4: Block PM Rewrites (6 skills) — START ONLY AFTER PHASE 3 IS COMPLETE

These skills are generic enterprise boilerplate. They need The Block-specific content.

### Step 1: Read the Current Skills

Read all 6 current SKILL.md files:

- `.claude/skills/meeting-prep/SKILL.md`
- `.claude/skills/sprint-roadmap/SKILL.md`
- `.claude/skills/data-analysis/SKILL.md`
- `.claude/skills/commit-checklist/SKILL.md`
- `.claude/skills/org-definition-of-done/SKILL.md`
- `.claude/skills/team-styleguide/SKILL.md`

### Step 2: Conduct the Phase 4 Interview

Same approach as Phase 3 — read the current skills, identify what's generic, and ask Sean for Block-specific details. The context doc tells us Sean is a Technical APM at The Block, leads daily standup, and has a 45/35/20 work split — but the skills need much more.

**For meeting-prep, you need to know:**
- Standup format: How long? Who attends? What's the agenda structure? (Blockers → progress → plans?)
- Sprint planning: How often? Who facilitates? What artifacts are produced?
- Other recurring meetings Sean runs or attends?
- Does he pre-generate agendas in Slack or Confluence? What's the current flow?
- Retro format?

**For sprint-roadmap, you need to know:**
- Sprint length (1 week? 2 weeks?)
- Team size and composition (how many devs, designers, QA?)
- Velocity range (story points per sprint)?
- How are OKRs structured? Quarterly? Who sets them?
- What tools track the roadmap? (Jira board, Confluence page, Google Sheet?)
- How does Sean report sprint progress upward?

**For data-analysis, you need to know:**
- What metrics does Sean track? (Subscriber growth, API usage, Campus enrollment — anything else?)
- What tools does he have access to vs. not? (GA4/Looker access is limited — what CAN he access?)
- What reports does he produce and for whom?
- What data sources are available via Zapier MCP?
- What format do stakeholders prefer for data presentations?

**For commit-checklist, you need to know:**
- Does The Block use conventional commits? What prefix format?
- Jira ticket format: Is it always BLOCK-XXX or are there other project keys?
- Branch naming convention: feature/BLOCK-123-description? Something else?
- PR review process: How many approvals? Any CI checks?
- Any pre-commit hooks or linters the team uses?

**For org-definition-of-done, you need to know:**
- What are the actual DoD criteria at The Block? (Code review, QA, documentation, etc.)
- Jira workflow states: What are the columns/statuses? (To Do → In Progress → In Review → Done? More?)
- Are there different DoD for different issue types (bug vs feature vs spike)?
- Any compliance or security requirements?

**For team-styleguide, you need to know:**
- Frontend stack details: React version? TypeScript strict mode? Tailwind config?
- Component naming patterns: PascalCase? Barrel exports?
- File/folder structure conventions?
- Testing requirements: Jest? React Testing Library? Coverage thresholds?
- API patterns: REST? GraphQL? How are endpoints structured?
- Linting/formatting: ESLint config? Prettier?

**Present these as a structured interview, one skill at a time.** Reference the **Zapier MCP Integration Opportunities** section in the audit doc — skills like data-analysis, sprint-roadmap, and meeting-prep should incorporate specific Zapier MCP tools.

### Step 3: Write the Skills

Same process as Phase 3. Rewrite each skill with Sean's answers. Run `python3 scripts/validate.py` after each.

### Step 4: Update Documentation

Same as Phase 3's Step 4, but for Phase 4 items (#30-35).

---

## What NOT To Do

- **DO NOT** work on Phase 5 or Phase 6 — those are separate sessions
- **DO NOT** create new skills — Phase 3 and 4 are rewrites of existing skills only
- **DO NOT** modify export-group manifests — the skills already exist in the manifests
- **DO NOT** guess at Sean's personal data or work processes — always ask
- **DO NOT** start Phase 4 until Phase 3 is fully complete and documented
- **DO NOT** write a skill until you've interviewed Sean for that skill's specific data
