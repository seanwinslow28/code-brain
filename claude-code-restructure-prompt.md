# Claude Code Restructure Prompt — Superuser Pack Reorganization

**How to use:** Open Claude Code inside your `claude-code-superuser-pack` directory. Confirm model is Opus 4.7. Enable high-effort reasoning (`ultrathink` keyword is included below). Paste everything between the triple backticks into a single message. Claude Code will enter Plan Mode on its own per the instructions.

---

```
<role>
You are a senior systems architect auditing a mature, production-grade personal Claude Code ecosystem. You have deep expertise in:

- Claude Code (CLI, skills, subagents, hooks, settings precedence)
- Claude Agent SDK (autonomous agents, launchd scheduling, MCP servers)
- Obsidian vault design (PARA, MOCs, daily notes, embeddings)
- Information architecture and taxonomy design
- Safe, additive refactoring of complex codebases

Your job is to audit this ecosystem, plan a targeted reorganization, and then execute it WITHOUT breaking any working system. You are measured on two things only: (1) the quality of your plan, and (2) whether nothing breaks after execution.

You are working for Sean Winslow, who built this ecosystem. He is experienced at product thinking but describes himself as a beginner with code. Be explicit about reasoning and trade-offs.
</role>

<reasoning_directive>
Use maximum reasoning effort for this task. ultrathink.

This is a large, interconnected system with 112 skills, 13 agents, 8 hooks, 7 domain workspaces, an Obsidian vault, and an Agent SDK layer with 5 active agents on launchd schedules. You need to understand the entire architecture before proposing changes. Rushed analysis will break something. Take the time to think deeply.
</reasoning_directive>

<mode_directive>
IMMEDIATELY enter Plan Mode before taking any action that writes, edits, or creates files. Remember: Plan Mode is double Shift+Tab (or `/plan`), NOT single Tab (that's Extended Thinking). Do all audit and discovery work in Plan Mode. Present the full plan for human approval before exiting Plan Mode. Do not execute any writes until the plan is explicitly approved.
</mode_directive>

<context>

## What This Repo Is

You are inside `claude-code-superuser-pack` — Sean's personal Claude Code command center. It is a mature ecosystem built over months of iteration. Read the root `CLAUDE.md` first; it has the authoritative architecture overview. Also read `README.md` and `CHANGELOG.md` to understand current state and history.

Key facts from the root CLAUDE.md:
- 112 skills in `.claude/skills/` (canonical location, auto-loaded)
- 13 agents in `.claude/agents/` (9 domain + 4 design team)
- 8 hooks in `.claude/hooks/`
- 7 domain workspaces: `claude-mastery/`, `product-management/`, `creative-studio/`, `life-systems/`, `design-team/`, `vault/`, `16bitfit-battle-mode/`
- Obsidian vault at `vault/` with PARA structure (`00_inbox`, `02_Areas`, `05_atlas`, `10_timeline`, `20_projects`, `30_domains`, `40_knowledge`, `50_sources`, `60_archive`, `70_apple-notes`, `90_system`)
- Agent SDK layer at `agents-sdk/` with 5 active autonomous agents on launchd schedules
- Installer at `scripts/install.sh` exports subsets to other projects via presets (`starter`, `power`, `enterprise`, `creative`)
- Validator at `scripts/validate.py` — MUST PASS after any change
- Phase 6 (Knowledge Compounding Loop) is planned: SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint → autoresearch feedback

## The Owner's Current Situation (Conversation Context)

Sean has been planning to adopt a pattern from an external project (OB1 / Open Brain by Nate B. Jones) — specifically the "Work Operating Model Activation" recipe, which runs a structured 5-layer interview and produces operating-model artifact files (`HEARTBEAT.md`, `USER.md`, `SOUL.md`, `operating-model.md`, `schedule-recommendations.md`) that downstream agents consume for persistent operational context.

After extended discussion, Sean decided:

1. **Don't adopt OB1 wholesale.** OB1 is Postgres + Supabase + MCP — architecturally incompatible with his local-first, Keychain-based, three-machine topology. He will keep his substrate and borrow only the interview pattern.

2. **Port the pattern as a single new skill** named `work-operating-model` at `.claude/skills/work-operating-model/`. The skill writes markdown artifacts to his vault, not JSON to Postgres.

3. **Run the interview three times — one per domain.** The three domains are:
   - **The Block** → his day job as a PM at The Block (crypto/ETF company). Covers PRDs, sprints, stakeholder comms, ETF page creation, bi-weekly updates, Jira/Confluence work.
   - **Creative Studio** → includes 16BitFit Battle Mode, Remotion video, pixel art, animation pipeline, creative writing.
   - **Life Systems** → finance, health, learning, tasks, time, career.

4. **Don't split the superuser pack into separate repos.** Instead, restructure INTERNALLY so each of the three domains has its own CLAUDE.md + its own operating-model bundle, while keeping all shared infrastructure (hooks, agents-sdk, vault, installer, embeddings) intact.

5. **Keep `Sean-Winslow-Full-Personal-Context-v1.1.md` as the tier-0 identity file** that sits above all three domain operating models. It will be updated to v2.0 AFTER the interviews run, not before.

## Current State Concerns

The ecosystem is not broken, but navigation is thinning:
- Root CLAUDE.md is dense and close to a readability ceiling
- No per-domain CLAUDE.md routing (except for the `16bitfit-battle-mode/` project, which already has one — use it as a reference pattern)
- No operating-model artifacts exist yet anywhere
- Sean's mental model has three clean domains but the repo doesn't surface that split

</context>

<objective>

Implement an internal restructure of the superuser pack that achieves all of the following:

1. A new skill `work-operating-model` at `.claude/skills/work-operating-model/` with a `SKILL.md` and any reference files. The skill takes a `domain` argument (`the-block`, `creative-studio`, or `life-systems`) and runs a structured 5-layer interview, writing outputs to the appropriate domain folder.

2. Three domain operating-model bundles at `vault/05_atlas/operating-models/{the-block,creative-studio,life-systems}/`, each containing placeholder files:
   - `HEARTBEAT.md` (operating rhythms)
   - `USER.md` (decision patterns)
   - `SOUL.md` (dependencies + institutional knowledge)
   - `operating-model.md` (structured profile)
   - `schedule-recommendations.md` (friction-derived schedule rules)

3. Three domain-level `CLAUDE.md` files that act as routers to the relevant skills, agents, and operating-model bundles for each domain. Location: you decide during planning — propose and justify.

4. Root `CLAUDE.md` refactored from a dense dump into a short router that points to the three domain CLAUDE.md files while still preserving architecture, commands, and non-negotiable rules.

5. All mandatory documentation updates per the root CLAUDE.md's rules: `CHANGELOG.md`, root `CLAUDE.md`, `README.md`.

6. Zero breakage: `python3 scripts/validate.py` must pass. All 5 active launchd-scheduled agents must continue to work. Installer presets must continue to export correctly. Phase 6 Knowledge Compounding Loop plans must not be disrupted.

</objective>

<proposed_restructure>

The human-approved direction (do NOT deviate without surfacing the deviation in your plan):

**Step 1 — Scaffold three domain CLAUDE.md files.** Decide location during planning. Two candidate approaches:
  - (a) Create new top-level folders `the-block/`, and add CLAUDE.md to existing `creative-studio/` and `life-systems/`.
  - (b) Place all three at `vault/05_atlas/operating-models/{domain}/CLAUDE.md` to co-locate with the artifacts.
  - (c) A hybrid: CLAUDE.md at the domain workspace root, operating-model files in the vault subfolder, with cross-links.
  - Propose the best option with reasoning. Note: `product-management/` already exists as a GENERIC PM skills workspace and should NOT be renamed — The Block is company-specific, which is different from generic PM. Plan the relationship between `the-block/` and `product-management/` explicitly.

**Step 2 — Create operating-model placeholders.** At `vault/05_atlas/operating-models/{the-block,creative-studio,life-systems}/`, create all five markdown files per domain. Use a consistent template: YAML frontmatter (domain, last_interviewed, status), a short "this file is populated by the work-operating-model skill" preamble, and section headers matching the 5-layer interview structure. Files should be EMPTY of actual content — just scaffolding.

**Step 3 — Build the `work-operating-model` skill.** Match the pattern of existing skills (examine `.claude/skills/prompt-engineering/SKILL.md` and `.claude/skills/creative-director/SKILL.md` for good reference patterns). The skill's `SKILL.md` must:
  - Use correct YAML frontmatter (name, description with trigger phrases, location)
  - Describe when to use
  - Include the 5-layer interview questions EXACTLY as provided in the `<interview_questions>` block below
  - Specify the output artifact format (what goes in each of the 5 files)
  - Include checkpointing behavior: pause after each layer, confirm, then save
  - Accept a `domain` argument to route writes to the right folder
  - Include a "before starting" section that tells the agent to read the current contents of the target folder (if they exist) and ask whether this is a fresh interview or a re-profile update

**Step 4 — Refactor root `CLAUDE.md` into a router.** Keep the non-negotiable rules section verbatim (it's load-bearing). Move domain-specific details to the three domain CLAUDE.md files. The new root CLAUDE.md should be short enough to load as context without burning the budget. Include a table that routes common task types to the correct domain.

**Step 5 — Update mandatory docs.** Per the root CLAUDE.md's "Mandatory doc updates" rule, every new Skill/Agent/Sub-Agent/Hook/Script requires updates to all three: `CHANGELOG.md`, `CLAUDE.md`, `README.md`. Follow that rule.

</proposed_restructure>

<interview_questions>

Sean has already reviewed and approved these questions. Write them VERBATIM into the skill (adjusted for the three-domain split — the questions below are the superset, with domain-specific tuning noted where relevant).

## Layer 1 — Operating Rhythms
Feeds: `HEARTBEAT.md`. Consumed by: `meeting-defender`, `daily-driver`.

1. Walk me through an ideal weekday in this domain — where are the protected creative/deep-work blocks, where are the execution/meeting blocks, where does inbox triage live?
2. Which recurring events are fixed on your calendar for this domain, and on which day/time? (For The Block: sprint ceremonies + bi-weekly Product & Engineering update cadence. For Creative Studio: any writing/recording rhythms. For Life Systems: any weekly finance/health reviews.)
3. What happens weekly in this domain that isn't on a calendar but should be?
4. What monthly/quarterly rhythms matter?
5. How do you split `swinslow@theblock.co` time vs `sean.winslow28@gmail.com` time for this domain?
6. Are there seasonal shifts? (crypto cycles, year-end, conference weeks, Boston winter)
7. What's your "sacred first hour" rule for this domain?

## Layer 2 — Recurring Decisions
Feeds: `USER.md`. Consumed by: `daily-driver`, `process-inbox`, `sprint-health`.

1. What decisions do you make 3+ times a week in this domain?
2. When you prioritize, what criteria do you actually use? Name the real ones, even if messy.
3. What's an auto-yes for this domain? An auto-no?
4. How do you decide what to invest in on a given day within this domain?
5. What decisions do you already trust an agent with? Which ones would you never delegate?
6. When you're unsure, what's your tiebreaker?
7. What does "done" usually mean in this domain?

## Layer 3 — Dependencies
Feeds: `SOUL.md` (people/tools section). Consumed by: `sprint-health`, `pr-digest`, `process-inbox`.

1. Who are your critical-path collaborators in this domain — the 3-5 people who, if unavailable, block you? What do you go to each of them for specifically?
2. Which tools does your flow collapse without?
3. Which external APIs/models are load-bearing right now?
4. For each of your three machines (Mac Mini, MacBook Pro, Alienware) — what halts if that machine is down, and for how long is that tolerable?
5. What's the single source of truth for this domain?
6. Who depends on you and on what cadence?
7. Where do you get stuck waiting on yourself — decisions only you can make that pile up?

## Layer 4 — Institutional Knowledge
Feeds: `SOUL.md` (tacit/tribal section).

1. Internal vocabulary: acronyms, project codenames, nicknames, jargon specific to this domain.
2. "Sacred cows" — decisions or conventions every proposal has to respect.
3. Unwritten communication rules.
4. "Ask X about Y" mapping — 5-10 people who are resident experts on specific topics.
5. Past landmines — decisions that got reversed, patterns that failed.
6. What would a sharp new hire need to know in week one that nobody would bother writing down?
7. Anything about you that collaborators have learned over time?

## Layer 5 — Friction
Feeds: `schedule-recommendations.md`. Consumed by: `meeting-defender`, future calendar agents.

1. What takes 20+ minutes today that should take 2?
2. Which context switches are most expensive for you in this domain?
3. What manual steps do you do every day that could be automated but haven't been?
4. What communication recurrently eats time?
5. What decisions do you delay because they're annoying?
6. What's broken in your physical/work setup affecting focus in this domain?
7. Where does Claude Code / Cowork / the agent fleet frustrate you in this domain?
8. If you had one extra hour every weekday in this domain, where would it go?

</interview_questions>

<non_negotiables>

These come from Sean's root CLAUDE.md and from the conversation. Do NOT violate them:

1. **`python3 scripts/validate.py` must pass after changes.** Run it as your final validation step.
2. **Skills live in `.claude/skills/` (canonical).** Don't put them in `export-groups/`.
3. **Agents live in `.claude/agents/` (canonical).** Don't put them in `shared/agents/`.
4. **Mandatory doc updates:** When creating a new Skill/Agent/Sub-Agent/Hook/Script, update ALL THREE: `CHANGELOG.md`, `CLAUDE.md`, `README.md`.
5. **Update `export-groups/*/playground.json` manifests** when adding/removing skills that belong to export groups. Decide whether the new skill belongs to any export group.
6. **Plan Mode vs Extended Thinking distinction:** Plan Mode = double Shift+Tab or `/plan`. Extended Thinking = single Tab. You are invoking Plan Mode.
7. **Hook blocking uses exit code 2** (not 0 or 1). Don't touch hooks unless you must.
8. **Agent tool restrictions use `disallowedTools` (deny-list), not allow-list.** Don't modify agents' allow-list patterns.
9. **Don't break the 5 active launchd agents.** They are: Vault Indexer (2:00 AM), Vault Synthesizer (2:30 AM), Daily Driver (8:45 AM), Knowledge Lint (Sunday 22:00), Flush (SessionEnd hook). Read `agents-sdk/config.toml` and the launchd plists in `agents-sdk/schedules/` to understand dependencies before moving anything.
10. **Don't re-enable the 6 agents disabled in v3.12.3.** They remain disabled per audit at `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`.
11. **Phase 6 Knowledge Compounding Loop is in flight.** Don't disrupt planning or scaffolding for it. Read any Phase 6 docs you find before making changes that touch the vault or session-end flush hook.
12. **`product-management/` is a generic PM workspace and stays as-is.** "The Block" is Sean's employer and is different from generic PM. If you create `the-block/` as a new workspace, it must coexist with `product-management/`, not replace it.
13. **Never commit changes.** Leave the working tree dirty for Sean to review and commit himself.
14. **No emojis in files** unless Sean explicitly asked for them. He didn't.

</non_negotiables>

<plan_mode_requirements>

Before exiting Plan Mode, your plan MUST include:

1. **Discovery summary** — what you read, what you learned, what surprised you.
2. **Dependency map** — a short list of which existing files/agents/hooks depend on paths you might be moving or restructuring. If nothing is being moved, say so explicitly.
3. **Explicit decisions you made during planning** — especially:
   - Where the three domain `CLAUDE.md` files will live (workspace root vs vault subfolder vs hybrid) — with reasoning
   - How `the-block/` relates to `product-management/`
   - Whether the `work-operating-model` skill belongs to any export-groups preset
   - Whether root CLAUDE.md should be split into a router + domain files, or preserved as-is with domain files appended
4. **File-by-file change list** — every file you will create, edit, or leave alone. For each, note the rationale.
5. **Risk register** — anything that could break. For each risk, your mitigation.
6. **Validation checklist** — the commands you'll run after execution to verify nothing broke. Minimum: `python3 scripts/validate.py`. Consider also: syntax-check any modified JSON/TOML, dry-run the `daily_driver.py` agent (`PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run` from `agents-sdk/`), spot-check one installer preset.
7. **Explicit statement** — "I have NOT made any writes. All work so far has been read-only exploration and planning. Awaiting approval to execute."

After Sean approves the plan, exit Plan Mode and execute in order. After execution, run the validation checklist and report results.

</plan_mode_requirements>

<examples>

## Example of a good domain CLAUDE.md structure

```markdown
# CLAUDE.md — The Block (Domain: PM work)

This is the domain context for Sean's day job at The Block. For the overall ecosystem architecture, see root `../CLAUDE.md`.

## Scope of This Domain
[what's in, what's out — one paragraph]

## Operating Model
- Heartbeat: [vault/05_atlas/operating-models/the-block/HEARTBEAT.md](../vault/05_atlas/operating-models/the-block/HEARTBEAT.md)
- User profile: [vault/05_atlas/operating-models/the-block/USER.md](...)
- Soul (people/tribal): [...]
- Full model: [...]
- Schedule rules: [...]

## Primary Skills for This Domain
| Skill | Purpose |
|---|---|
| biweekly-jira-update | Generate bi-weekly P&E status update |
| the-block-jira-ticket-writer | Generate Jira tickets per The Block standards |
| etf-page-creator | ETF page creation on WordPress |
| ... | ... |

## Primary Agents for This Domain
[list]

## Active MCPs Used in This Domain
[list]

## Non-Negotiable Rules Specific to This Domain
[domain-specific rules — e.g. never auto-post Jira tickets, ETF compliance patterns]
```

## Example of a good operating-model placeholder

```markdown
---
domain: the-block
artifact: HEARTBEAT
status: awaiting-interview
last_interviewed: null
---

# HEARTBEAT — The Block

This file captures Sean's operating rhythms for The Block domain. Populated by the `work-operating-model` skill. Consumed by `meeting-defender` and `daily-driver` agents.

## Daily Rhythm
_To be filled by interview._

## Weekly Cadence
_To be filled by interview._

## Monthly / Quarterly
_To be filled by interview._

## Seasonal Shifts
_To be filled by interview._

## Sacred Blocks
_To be filled by interview._
```

</examples>

<validation>

After execution, run this self-check:

1. Did `python3 scripts/validate.py` pass? If not, stop and report.
2. Does `ls .claude/skills/work-operating-model/SKILL.md` return the expected file?
3. Do all 15 operating-model placeholder files exist (5 files × 3 domains)?
4. Does each new CLAUDE.md load cleanly — i.e. does `cat` on it work and is the markdown valid?
5. Does the root CLAUDE.md still contain the non-negotiable rules section?
6. Do `CHANGELOG.md`, root `CLAUDE.md`, and `README.md` all reflect the new skill and structure?
7. Did you avoid touching: `.claude/hooks/`, any agent at `.claude/agents/`, `agents-sdk/agents/*.py`, `agents-sdk/schedules/*.plist`? (You should not need to touch these for this task.)
8. Did you commit anything? (You should NOT have. Working tree should be dirty.)

Report validation results verbatim. If anything failed, DO NOT attempt fixes yet — report and wait for Sean's direction.

</validation>

<final_instruction>

Begin now. Enter Plan Mode. Audit the repo. Produce the plan. Wait for approval.

Remember: ultrathink. This ecosystem has 112 skills and 13 agents that Sean has spent months tuning. Move with care.

</final_instruction>
```

---

## Prompt engineering notes (why the prompt is structured this way)

Using the 9-technique checklist from the skill:

**Clarity (T1):** Objective section spells out six concrete success criteria. Negative constraints are isolated in `<non_negotiables>` so they can't be missed.

**Examples (T2):** Included two — a good domain CLAUDE.md skeleton and a good operating-model placeholder. Both are lifted from your existing patterns so Claude Code has a concrete target shape.

**Chain of Thought (T3):** Used in two ways — (a) the `<reasoning_directive>` with the `ultrathink` keyword triggers Opus 4.7's high-effort mode, (b) the `<plan_mode_requirements>` force Claude to show its discovery + decisions + risks before writing anything.

**XML Tags (T4):** Every major component is in its own tag so Claude Code can't mix instructions with examples with constraints. Tag names match Anthropic's conventions.

**Role (T5):** Senior systems architect framing at the top. Makes output more rigorous than a default-mode response would be.

**Prefill (T6):** Not used — not an API call.

**Chain complex prompts (T7):** Enforced by Plan Mode itself — plan → approve → execute → validate is a built-in chain. The `<validation>` block creates a generate-validate loop.

**Long context (T8):** Heavy context is front-loaded; the `<final_instruction>` ("Begin now") sits at the very bottom. This is the >30% quality improvement placement pattern.

**Validation (T9):** Explicit self-check with 8 items, plus a "report verbatim, don't self-fix" rule so you see what actually happened instead of a retroactively-polished summary.

**Two domain-specific safeguards worth flagging:**
- The prompt explicitly tells Claude Code that `product-management/` is generic and `the-block/` is company-specific — this is the nuance it would otherwise collapse.
- The prompt names the 5 active launchd agents and the 6 disabled ones so Claude Code knows exactly what's load-bearing vs archived.

**File saved here:**

[View the prompt](computer:///sessions/wonderful-practical-mayer/mnt/claude-code-superuser-pack/claude-code-restructure-prompt.md)

Open Claude Code inside your superuser pack, confirm it's on Opus 4.7, paste the code block (everything between the triple backticks), and let it enter Plan Mode. Review the plan before approving — that's your quality gate.