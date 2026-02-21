# Product Management — Agent Extraction Prompt

Use this prompt with the **Agent Extraction Kickoff** after connecting to the **"Claude Code - PM Workflows"** and **"Claude Code - Domain-Specific"** NotebookLM notebooks.

---

## PROMPT START — Process this domain with the Kickoff Prompt

---

## Who I Am

I'm Sean, an Associate PM (Technical) at The Block, a crypto data and news company. I manage data API products and work across product strategy, sprint planning, stakeholder communication, and data analysis. My stack is React, Python, Supabase. I use Claude Code as my primary PM workflow tool.

I'm upgrading one thin agent and creating one new agent for the Product Management domain. These agents provide **structured evaluation and workflow execution** — the 18 PM skills handle document generation and domain knowledge.

## What's in These Notebooks

**Notebook 1: "Claude Code - PM Workflows"** (131 sources)
PM methodologies, sprint planning, PRD writing, stakeholder communication, ticket management, data analysis patterns. Sources include PM best practices, Jira/Linear patterns, and product strategy frameworks.

**Notebook 2: "Claude Code - Domain-Specific"** (48 sources)
Domain-specific PM context: crypto/Web3 products, API product management, data products, education platforms, RevOps. Sources include industry-specific patterns and The Block context.

## Your Task

Extract behavioral knowledge from these notebooks and generate **2 agents** for the Product Management domain: 1 upgrade and 1 new.

## Target Agents

### 1. UPGRADE: data-analyst
**Priority**: High
**Current state**: 37 lines, generic 7-item capability list, no methodology, no output template
**Current file**: `.claude/agents/data-analyst.md` (READ THIS FIRST)
**Type**: Workflow agent (read-write, needs Bash for Python scripts and data processing)
**disallowedTools**: (none — needs full tool access)

**What to extract from notebooks**:
- Analysis workflow: data intake (CSV, JSON, API) → data cleaning/validation → exploratory analysis → insight extraction → recommendation formulation
- Visualization selection framework: when to use bar chart vs line chart vs scatter vs table vs heatmap, based on data type and question being answered
- Statistical rigor checklist: sample size adequacy, correlation vs causation, statistical significance, outlier handling, trend vs noise
- Crypto/fintech-specific metrics: TVL (Total Value Locked), trading volume, market cap, on-chain metrics, API usage metrics, DAU/MAU for data products
- Report structure: executive summary → key findings → detailed analysis → visualizations → recommendations

**Output format requirements**:
- Executive Summary (2-3 sentences)
- Key Findings table (metric, value, trend, significance)
- Detailed Analysis per finding (with data support)
- Visualization Recommendations (chart type, variables, tool)
- Actionable Recommendations (prioritized)

**Trigger phrases**: "analyze this data", "what do these metrics show", "create a report from this CSV", "data analysis", "crypto metrics", "visualize this data"

**Must preserve from current thin agent**: Data analysis, visualization creation, insights generation, report generation, trend analysis

### 2. NEW: scrum-master
**Priority**: High
**Type**: Workflow agent (read-write, needs to read PRDs and potentially create ticket files)
**disallowedTools**: (none — needs full tool access)

**What to extract from notebooks**:
- PRD breakdown methodology: how to read a PRD and identify natural epic boundaries, when to split vs combine features, how to sequence dependencies
- Epic structure: what makes a good epic (scope, duration, team alignment), naming conventions, acceptance criteria at the epic level
- Story decomposition: Design stories vs Implementation stories, story point estimation frameworks (fibonacci, t-shirt sizing), "Definition of Ready" checklist
- Dependency mapping: how to identify cross-team dependencies, technical prerequisites, integration points
- Sprint capacity: how to estimate team capacity, account for meetings/overhead, recommended points per sprint
- Acceptance criteria writing: Given/When/Then format, measurable criteria, edge case coverage

**Output format requirements**:
- Epic summary table (name, description, estimated points, priority, dependencies)
- Per-epic story breakdown with:
  - Story name and type (Design/Implementation)
  - Story points estimate
  - Acceptance criteria (Given/When/Then)
  - Dependencies
- Dependency graph (text-based)
- Sprint allocation recommendation (which stories in which sprint, based on capacity and dependencies)
- Risk flags (stories that seem underestimated, unclear requirements, missing dependencies)

**Trigger phrases**: "break this PRD into stories", "create epics from this spec", "sprint planning", "estimate these stories", "break down this feature", "create Jira tickets from this PRD"

## Extraction Guidance

- The data-analyst upgrade needs METHODOLOGY, not just capability claims. Extract analysis workflows, decision frameworks for choosing visualizations, and statistical rigor checks.
- The scrum-master needs JUDGMENT about decomposition — when to split an epic, how to size stories, how to sequence work. This is the behavioral value over just using the `ticket-batch` skill.
- Include crypto/fintech context where relevant (The Block's API products, data products, crypto metrics).
- Both agents should reference specific PM skills in their "Pairs Well With" section.
- The scrum-master's output format should be structured enough to copy directly into Jira/Linear.

## Cross-Domain Notes

- data-analyst pairs with `data-analysis` and `personal-finance` skills
- scrum-master pairs with `ticket-batch`, `jira-automation`, `sprint-roadmap` skills
- scrum-master takes input from `doc-reviewer` agent (reviewed PRD → breakdown)
- Both serve Sean's daily PM work at The Block

## Quality Bar

Each generated agent should:
- Be 100-150 lines (Rich tier)
- Have concrete methodology steps (not vague principles)
- Include a complete output format template
- Reference real skills and agents from the pack
- The data-analyst must significantly exceed the 37-line thin version

---

## PROMPT END
