# PM Workflows - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - PM Workflows"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto data/news company (The Block). I'm a beginner coder learning fundamentals, working across three domains: PM work, creative projects (React Native + Phaser game dev), and life optimization/automation. My stack is React, Python, Supabase, and I use Claude Code as my primary development tool.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers my **core PM workflows** and how Claude Code can accelerate them.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - PM Workflows") contains deep research on using Claude Code for product management tasks: Jira automation, PRD/spec generation, stakeholder communication, data analysis, sprint planning, roadmap generation, documentation workflows, and PM-specific patterns. Sources include PM practitioner guides, Jira integration tutorials, template examples, and community workflows.

## Your Task

Analyze all sources in this notebook and generate **6-7 Claude Skills** that make Claude Code a PM power tool. These skills should help me do my daily PM job faster and at higher quality, even as a beginner coder.

## Target Skills to Extract

### 1. Jira Automation
**Priority**: High
**What to extract**: MCP server setup for Jira, ticket creation from natural language, bulk ticket creation/updates, JQL query patterns, sprint management commands, ticket templates (bug report, feature request, tech debt, spike), linking tickets, and batch operations. Include specific Jira field mappings and common JQL queries for a technical PM.
**Trigger phrases**: "create Jira ticket", "update Jira", "bulk tickets", "sprint planning", "JQL query", "Jira template"

### 2. PRD & Technical Spec Generator
**Priority**: High
**What to extract**: Interview-style clarifying question workflow (ask before writing), PRD template structure (problem, goals, user stories, requirements, success metrics, constraints, timeline), technical spec format, spec validation checklist, engineering-ready quality criteria. The skill should guide Claude through a structured conversation before generating the document.
**Trigger phrases**: "write a PRD", "create a spec", "product requirements", "technical specification", "feature spec"

### 3. Stakeholder Communication
**Priority**: High
**What to extract**: Templates for different audience levels (executive summary, technical deep-dive, cross-functional update), status report formats, weekly/monthly update structures, "what happened / what's next / blockers" pattern, presentation slide outlines, tailoring language for technical vs non-technical stakeholders.
**Trigger phrases**: "stakeholder update", "status report", "executive summary", "leadership update", "weekly update", "present to"

### 4. Data Analysis & Reporting
**Priority**: Medium
**What to extract**: CSV/JSON processing patterns, metrics analysis workflows, trend identification, report generation (weekly metrics, monthly reviews, quarterly business reviews), chart/visualization recommendations, integration patterns with analytics tools (GA4, Looker), and skills for a non-data-scientist to do meaningful analysis.
**Trigger phrases**: "analyze this data", "create a report", "metrics review", "data analysis", "CSV", "trend analysis"

### 5. Sprint & Roadmap Planning
**Priority**: Medium
**What to extract**: Sprint planning automation (capacity calculation, story point estimation assistance, sprint goal formulation), roadmap generation from backlog, backlog grooming workflows, prioritization frameworks (RICE, MoSCoW, impact/effort), dependency mapping, and release planning patterns.
**Trigger phrases**: "sprint planning", "roadmap", "backlog grooming", "prioritize", "release plan", "capacity planning"

### 6. Documentation Workflows
**Priority**: Medium
**What to extract**: README generation, API documentation, knowledge base article creation, doc maintenance/update workflows, doc-driven development patterns, keeping docs in sync with code changes, and documentation review checklists.
**Trigger phrases**: "write documentation", "update docs", "README", "knowledge base", "API docs", "document this"

### 7. User Research Synthesis
**Priority**: Lower
**What to extract**: Interview transcript analysis, theme extraction, insight synthesis, persona creation from research data, user journey mapping, research report generation, and patterns for turning qualitative data into actionable product decisions.
**Trigger phrases**: "analyze interviews", "user research", "synthesize feedback", "persona", "user journey", "research findings"

## Extraction Guidance

- **Beginner-friendly**: I'm not a senior PM with 10 years of experience. Skills should guide me through processes, not assume I know the right questions to ask.
- **Interview-style workflows**: For PRDs and specs, the skill should prompt Claude to ASK ME questions before generating — not just dump a template. The clarifying conversation IS the value.
- **Templates with flexibility**: Include templates but make them adaptable. Different projects need different depth.
- **Crypto/fintech context**: Where relevant, include examples from crypto/fintech PM work (token economics, on-chain metrics, regulatory considerations, market data).
- **Real Jira patterns**: Include actual JQL queries, field names, and workflow states — not generic descriptions.
- **Output quality markers**: Each skill should specify what "done well" looks like for its output.

## Cross-Domain Notes

- **Jira skill** connects to Technical Stack (API integration) and Core Features (MCP setup)
- **PRD skill** connects to Creative Projects (game design docs) and Domain Specific (crypto product specs)
- **Data Analysis** connects to Life Optimization (personal finance analysis) and Technical Stack (Python scripts)
- **Stakeholder Communication** connects to Domain Specific (crypto industry language)
- **Documentation** connects to Obsidian Integration (knowledge base) and Core Features (CLAUDE.md patterns)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Guide me through a process, not just generate output — the workflow matters as much as the result
- Include concrete templates with placeholder variables I can fill in
- Be immediately usable for real PM work at a crypto company
- Handle the "80% case" well — not every edge case, but the most common PM scenarios
- Include validation/review steps so I catch issues before sending to stakeholders or engineering

---

## PROMPT END
