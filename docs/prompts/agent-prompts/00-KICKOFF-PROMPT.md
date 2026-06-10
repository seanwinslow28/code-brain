# Agent Extraction Kickoff Prompt

## How to Use

Open Claude Code (or Anti-Gravity IDE) in this project and specify which domain to process:

```
Read _inputs/Agent-Prompts/00-KICKOFF-PROMPT.md and process domain 2 - Product Management
```

Or process by number:

```
Read _inputs/Agent-Prompts/00-KICKOFF-PROMPT.md and process domain 3
```

Process one domain per session to stay within context limits.

---

## KICKOFF INSTRUCTIONS

You are extracting Claude Code Agents from NotebookLM notebooks using the NotebookLM MCP server. Agents define **behavioral roles** — structured review criteria, judgment frameworks, and formatted output templates. They are NOT knowledge stores (that is what Skills do).

Follow this workflow exactly. Do not skip phases or reorder steps.

---

### Phase 1: Absorb Context

Read these files to understand the agent format, behavioral patterns, and quality bar. Read them in this order:

**Agent anatomy and design patterns** (read all 4):
- `_inputs/Agent-Prompts/Agent Creator Instructions/claude-agent-anatomy.md`
- `_inputs/Agent-Prompts/Agent Creator Instructions/agent-design-patterns.md`
- `_inputs/Agent-Prompts/Agent Creator Instructions/agent-examples.md`
- `_inputs/Agent-Prompts/Agent Creator Instructions/agent-vs-skill.md`

**Quality and format requirements**:
- `_inputs/Agent-Prompts/00-DEPTH-ADDENDUM.md`

**Target extraction prompt** (match the domain number the user specified):
- `_inputs/Agent-Prompts/[NN]-[domain-name].md` (e.g., `02-product-management.md`)

**Exemplar agents** (read these to calibrate quality — these represent the bar):
- `.claude/agents/checklist-validator.md` (136 lines — gold standard: validation levels, output template, integration)
- `.claude/agents/doc-reviewer.md` (183 lines — richest agent: four review dimensions, document-type checklists)
- `.claude/agents/visual-polish-auditor.md` (85 lines — solid medium: clear categories, concrete criteria)

**For upgrade targets**, also read the current thin agent being upgraded:
- Check the extraction prompt for which agents are upgrades vs new
- Read the current thin agent file from `.claude/agents/`
- Note what it covers — the upgrade must preserve and exceed this scope

After reading all files, confirm what you absorbed:
- How many agents the extraction prompt targets (upgrades vs new)
- Which notebooks to query
- The domain context (who is Sean, what stack, what goal)

---

### Phase 2: Discover the Notebooks

1. Call `notebook_list` to find all NotebookLM notebooks
2. Match ALL notebooks listed in the extraction prompt (some domains query multiple notebooks)
3. Call `notebook_describe` on each matched notebook to get the AI-generated overview and suggested topics
4. Call `source_list_drive` on the primary notebook to list sources
5. Report what you found: notebook names, number of sources, suggested topics

If no notebook matches, stop and ask the user to verify the notebook name.

---

### Phase 3: Extract Behavioral Knowledge

This is the critical difference from skill extraction. You are extracting BEHAVIORS (how an expert would evaluate, decide, or advise), not KNOWLEDGE (facts, patterns, code).

For EACH target agent listed in the extraction prompt, run a focused extraction loop:

#### Step 3a: Broad Query
Call `notebook_query` with a behavioral breadth question:
```
What are the key workflows, decision criteria, judgment frameworks, review
processes, and evaluation methods related to [AGENT TOPIC]? I need behavioral
patterns — how an expert would evaluate, decide, or advise on this topic.
Include specific criteria they would check, severity levels they would assign,
and output formats they would use to communicate findings.
```

#### Step 3b: Deep Query
If the broad query reveals dense content, call `notebook_query` with a depth follow-up:
```
For [AGENT TOPIC], give me:
1. The specific dimensions an expert would evaluate (what categories of review)
2. Concrete criteria for each dimension (pass/fail thresholds, severity levels, scoring rubrics)
3. Common failure patterns and how to categorize them by severity
4. The output format an expert would use to communicate findings (structured templates)
5. Decision frameworks for ambiguous cases (when is something Critical vs Important?)
```

Use the `conversation_id` from Step 3a for continuity.

#### Step 3c: Source Deep Dive (when needed)
If queries reference specific sources containing evaluation frameworks, checklists, or review criteria:
- Call `source_get_content` on those sources to get the raw text
- Extract the specific evaluation dimensions, scoring rubrics, and workflow steps

#### Step 3d: Cross-Reference
Check the extraction prompt's guidance for this specific agent:
- What is the agent's role/persona?
- What dimensions should it evaluate?
- Is it a review agent (read-only), workflow agent (read-write), or advisory agent?
- What existing thin agent (if any) is being upgraded?
- What priority level is it?

Prioritize High-priority agents for deeper extraction.

---

### Phase 4: Generate Agents

For each agent, generate a `.md` file following this MANDATORY structure. Do not add, remove, or reorder sections.

```markdown
---
name: Agent Display Name
description: What this agent does AND when to invoke it. Embed trigger phrases naturally — this is the ONLY field Claude reads to decide whether to load the agent.
disallowedTools:     # Include for read-only agents. Omit for agents needing full access.
  - Edit
  - Write
  - Bash
---

# Agent Name Agent

## Purpose

One paragraph explaining what this agent does and why it exists. Use imperative form. No fluff.

## When to Use

Bullet list of specific situations when this agent should be invoked:
- Situation 1
- Situation 2
- Situation 3

## How It Works

1. Agent's first workflow step
2. Agent's second workflow step
3. Agent's third workflow step
(3-6 steps showing the agent's internal evaluation/processing workflow)

## Invocation Examples

- "Realistic user prompt 1"
- "Realistic user prompt 2"
- "Realistic user prompt 3"
(3-5 realistic prompts a user would type)

## [Domain-Specific Dimensions]

The bulk of the agent (40-100 lines). Section heading should be domain-specific:
- "Review Dimensions" for review agents
- "Analysis Framework" for analytical agents
- "Breakdown Methodology" for workflow agents

Each dimension should have:
- Clear name and scope
- Specific criteria (pass/fail or severity-scored)
- What constitutes findings at each severity level

## Output Format

(Complete template in a code block with placeholder values)

## Constraints

- What the agent cannot do
- Tool restrictions if applicable
- Read-only or read-write designation

## Pairs Well With

- `skill-or-agent-name` — brief explanation of synergy
- `skill-or-agent-name` — brief explanation of synergy
- `skill-or-agent-name` — brief explanation of synergy
```

---

### Phase 5: Validate

Before writing ANY file, run this checklist against each agent. If an agent fails any item, fix it before proceeding.

- [ ] YAML frontmatter has `name` and `description` (description embeds trigger phrases naturally)
- [ ] `name` field uses proper display name with spaces (e.g., "Security Reviewer")
- [ ] Filename will be kebab-case version of name (e.g., `security-reviewer.md`)
- [ ] `disallowedTools` present for read-only agents, uses correct casing (`Edit`, `Write`, `Bash`)
- [ ] Section order: Purpose > When to Use > How It Works > Invocation Examples > Dimensions > Output Format > Constraints > Pairs Well With
- [ ] How It Works has 3-6 numbered steps showing internal workflow
- [ ] Invocation Examples has 3-5 realistic quoted prompts
- [ ] Dimensions section is 40-100 lines with concrete criteria and severity levels
- [ ] Output Format has a COMPLETE template in a code block (with all sections and placeholders)
- [ ] Pairs Well With references 3-5 real skills or agents that exist in the pack
- [ ] Agent body is 60-180 lines (not under 60)
- [ ] Content is behavioral (judgment, criteria, scoring, workflows) not informational (facts, code, reference data)
- [ ] Imperative form throughout (not "This agent does X" but "Evaluate X")
- [ ] Zero emoji anywhere — headings, body, bullet points
- [ ] Clean markdown — no escaped characters, saveable directly as .md
- [ ] For upgrades: new version covers everything the thin agent covered, plus richer dimensions and output format

---

### Phase 6: Write to Disk

Create the output directory structure:

```
_outputs/agents/[domain-name]/
├── [agent-name].md
├── [agent-name].md
└── ...
```

**Domain name mapping:**

| Domain # | Domain Name |
|----------|-------------|
| 1 | claude-mastery |
| 2 | product-management |
| 3 | creative-studio |
| 4 | life-systems |
| 5 | vault |

After writing all files, present a summary table:

| Agent Name | Lines | Status | Priority | Tool Access | Notes |
|------------|-------|--------|----------|-------------|-------|
| ... | ... | ... | ... | ... | ... |

Include:
- Total agents generated (upgrades vs new)
- Any agents that couldn't meet the 60-line minimum (and why)
- Any notebook sources that were particularly useful or surprisingly empty
- Suggested next steps: review specific agents, test invocation, iterate on thin ones

---

## Domain-to-Prompt Mapping

| # | Domain | Extraction Prompt | Notebooks | Target Agents |
|---|--------|-------------------|-----------|---------------|
| 1 | Claude Mastery | `01-claude-mastery.md` | 01, 04 | 2 (upgrades) |
| 2 | Product Management | `02-product-management.md` | 02, 08 | 2 (1 upgrade, 1 new) |
| 3 | Creative Studio | `03-creative-studio.md` | 03, 11 | 2 (1 upgrade, 1 new) |
| 4 | Life Systems | `04-life-systems.md` | 05 | 1 (new) |
| 5 | Vault | `05-vault.md` | 06 | 1 (new) |

---

## Format Rules (Quick Reference)

Internalize these before generating any agent. They are non-negotiable.

1. **YAML frontmatter**: `name` + `description` required. `disallowedTools` optional (deny-list only, correct casing).
2. **Description**: Embed trigger phrases naturally. This is the ONLY field Claude reads to decide whether to load the agent.
3. **Imperative form**: "Evaluate code for security issues" not "This agent evaluates code."
4. **No human-facing sections**: No Design Notes, Packaging Notes, README content.
5. **No emoji**: Zero. None in headings, bullet points, or body text.
6. **Behavioral content only**: Judgment criteria, evaluation workflows, severity scoring. NOT facts, code patterns, or reference data.
7. **Clean markdown**: No escaped characters. Output raw markdown saveable as .md.
8. **Filename = kebab-case name**: `security-reviewer.md` has `name: Security Reviewer`.
9. **60-180 lines**: Per agent body. Under 60 means the agent is too thin to be useful.
10. **Complete output template**: Every agent MUST have a full template in a code block in the Output Format section.

---

## Sean's Context (for agent content)

- Associate PM (Technical) at The Block (crypto data/news)
- Beginner coder learning fundamentals through Claude Code
- Stack: React, TypeScript, Python, Supabase, Expo/React Native
- Building domain-specific Claude Code agents for structured review and workflows
- Has `remotion-docs` MCP server installed globally
- The Block brand: Primary #1A1A2E, Accent #E94560, Background #0F3460, Text #FFFFFF
- Active projects: 16BitFit (Game Boy-style fitness RPG), PM portfolio, Remotion video production
