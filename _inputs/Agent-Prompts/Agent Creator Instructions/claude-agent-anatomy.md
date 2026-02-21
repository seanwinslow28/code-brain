# Claude Code Agent — Anatomy Reference

## What is an Agent?

An Agent is a single `.md` file in `.claude/agents/` that defines a specialized behavioral role Claude Code can assume. Unlike Skills (which provide domain knowledge), Agents define **judgment criteria, review workflows, and structured output formats**. They transform Claude from a general-purpose assistant into a focused specialist with a specific evaluation framework.

## Required: agent-name.md

### YAML Frontmatter (REQUIRED)

```yaml
---
name: Agent Display Name
description: What this agent does AND when to invoke it. This is the ONLY metadata Claude reads to decide whether to load the agent. Embed trigger phrases naturally.
disallowedTools:     # Optional. Deny-list only (never allow-list).
  - Edit
  - Write
  - Bash
---
```

Fields:
- `name` (required): Human-readable display name. Can include spaces (e.g., "Security Reviewer").
- `description` (required): Must say both WHAT the agent does and WHEN to invoke it. Include trigger phrases naturally embedded — this is the primary triggering mechanism.
- `disallowedTools` (optional): Deny-list of tools the agent cannot use. Include for read-only review agents. Omit entirely for agents that need full tool access. Use correct casing: `Edit`, `Write`, `Bash` (not lowercase).

### File Naming

The filename (minus `.md`) should be kebab-case and clearly indicate the agent's role:
- `security-reviewer.md` (not `SecurityReviewer.md`)
- `scrum-master.md` (not `scrummaster.md`)
- `game-design-advisor.md` (not `game_design_advisor.md`)

## Mandatory Section Order

Every agent `.md` file MUST follow this exact section order. Do NOT skip sections or invent new ones.

### 1. Heading: `# [Agent Name] Agent`

### 2. `## Purpose`
One paragraph. What this agent does and why it exists. Use imperative form. No fluff.

### 3. `## When to Use`
Bullet list of specific invocation scenarios. Start each with an action verb:
- "Invoke when you need a security audit before deployment"
- "Use after generating a PRD to break it into Epics and Stories"
- "Run during weekly reviews to analyze spending and habit data"

### 4. `## How It Works`
3-6 numbered steps showing the agent's internal workflow. This describes the agent's thinking/evaluation process, not the user's interaction steps.

```markdown
1. Read the target artifact (code, document, data file)
2. Evaluate against [specific dimensions]
3. Score each dimension on severity scale
4. Generate findings with file:line references
5. Produce structured output in the standard format
```

### 5. `## Invocation Examples`
3-5 realistic prompts a user would type to invoke this agent. Use quoted format:

```markdown
- "Act as Security Reviewer and audit the auth module"
- "Run a security review on src/api/"
- "Check this code for vulnerabilities before we deploy"
```

### 6. `## [Review/Analysis/Workflow Dimensions]`
This is the BULK of the agent (40-100 lines). The section heading should be domain-specific:
- "Review Dimensions" for review agents
- "Analysis Framework" for analytical agents
- "Breakdown Methodology" for workflow agents

Organize by DIMENSION (what the agent evaluates/decides), not by concept. Each dimension should have:
- Clear name and scope
- Specific criteria to check (pass/fail or severity-scored)
- What constitutes a finding at each severity level

### 7. `## Output Format`
Complete template in a markdown code block showing the exact structure of the agent's output. Include placeholder values that demonstrate the format:

````markdown
```
## [Review Type]: [Target Name]

### Score: [1-10]

### Findings (by severity)

#### Critical (blocks ship)
- [file:line] Description and suggested fix

#### Important (should fix)
- [file:line] Description and suggested fix

#### Minor (nice to have)
- [file:line] Description and suggested fix

### Summary
[1-2 sentence overall assessment]

Reviewed by [agent-name] agent
```
````

### 8. `## Constraints`
What the agent cannot do. Tool restrictions explained. Whether read-only or read-write. Keep to 2-4 bullet points.

### 9. `## Pairs Well With`
3-5 skills or agents that complement this one. Use backtick format:

```markdown
- `security-hardening` skill — apply fixes after this agent identifies issues
- `compliance-summarizer` agent — run after security review for policy compliance
- `checklist-validator` agent — validate acceptance criteria are met
```

## What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- Human-facing documentation or packaging notes
- Domain knowledge that belongs in Skills (facts, code patterns, reference data)
- Conceptual explanations Claude already knows

## Agents vs Skills — Quick Decision

| Need | Use |
|------|-----|
| Domain knowledge for execution | Skill |
| Structured review with criteria | Agent |
| Code patterns and templates | Skill |
| Judgment with severity scoring | Agent |
| Reference data and lookup tables | Skill |
| Multi-step behavioral workflow | Agent |
| Trigger phrases for auto-loading | Both (in description field) |

## Quality Bar

- Agent body: 60-180 lines (under 60 means too thin)
- Output Format section: MUST contain a complete template in a code block
- How It Works: MUST have 3-6 numbered steps
- Invocation Examples: MUST have 3-5 realistic prompts
- Review Dimensions: MUST have concrete criteria, not vague descriptions
- Imperative form throughout, zero emoji, clean markdown
