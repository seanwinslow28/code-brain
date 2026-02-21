# Agent vs Skill — Decision Framework

## The Core Distinction

**Skills = knowledge for execution.** They provide domain-specific facts, code patterns, templates, and reference data that Claude Code needs to DO things. Skills auto-load when their description matches the user's request. Claude Code is already a full-stack executor — skills give it specialized knowledge.

**Agents = structured judgment, review criteria, or behavioral workflows.** They define HOW Claude should evaluate, decide, or process something, with specific criteria and formatted output. Agents add a behavioral layer that skills cannot encode.

## The Decision Test

Ask: "What does this add that Claude Code + auto-loaded skills don't already provide?"

| If the answer is... | Then use a... |
|---------------------|---------------|
| "Domain knowledge to write code" | **Skill** |
| "Structured criteria to review code" | **Agent** |
| "A template for generating a document" | **Skill** |
| "Judgment about whether a document is good" | **Agent** |
| "Reference data for a domain" | **Skill** |
| "A multi-step workflow with formatted output" | **Agent** |
| "Code patterns and best practices" | **Skill** |
| "Severity scoring and pass/fail evaluation" | **Agent** |

## When Skills Are Sufficient

Claude Code IS the executor. When a user says "build a Phaser scene" or "write a PRD," skills auto-load and Claude executes. You do NOT need an agent for:

- **Writing code**: Claude Code + relevant skills (e.g., `phaser-game-patterns`, `react-vite-tailwind`)
- **Generating documents**: Claude Code + relevant skills (e.g., `prd-generator`, `stakeholder-update`)
- **Processing assets**: Claude Code + relevant skills (e.g., `sprite-pipeline`, `ai-creative-tools`)
- **Configuring tools**: Claude Code + relevant skills (e.g., `mcp-integration`, `hooks-configuration`)
- **General development**: Claude Code already reads, writes, debugs, tests, and deploys

Creating an agent that says "write code using these patterns" is redundant — that is literally what a skill does.

## When Agents Add Value

Agents are justified when they provide:

### 1. Structured Evaluation Framework
The agent defines WHAT to evaluate and HOW to score it. Skills cannot encode judgment criteria with severity levels.

Example: `security-reviewer` evaluates code against OWASP dimensions and scores findings as Critical/Important/Minor. The `security-hardening` skill has the remediation knowledge, but the agent has the evaluation framework.

### 2. Formatted Review Output
The agent produces a specific, structured output (report, scorecard, review document) that follows a template. Skills produce knowledge; agents produce formatted assessments.

Example: `doc-reviewer` outputs a structured review with per-dimension scores, severity-tagged findings, and document-type-specific checklists.

### 3. Multi-Step Behavioral Workflow
The agent follows a sequence of judgment steps that transform input into structured output. The workflow involves decisions about HOW to process, not just WHAT to produce.

Example: `scrum-master` reads a PRD → identifies epic boundaries → breaks into stories → estimates points → maps dependencies → produces structured ticket output. Each step involves judgment that varies by context.

### 4. Tool Restrictions for Safety
The agent needs to be explicitly prevented from certain actions. Read-only review agents should not accidentally edit the code they are reviewing.

Example: All design-team agents use `disallowedTools: [Edit, Write, Bash]` to ensure they only report findings, never modify code.

## Agents That Were Cut (and Why)

These were proposed but determined to be redundant with Claude Code + existing skills:

| Proposed Agent | Why Cut | Use Instead |
|----------------|---------|-------------|
| pm-executor | "Write PRDs and conduct research" = Claude Code + `prd-generator`, `research-synthesis`, `stakeholder-update` skills | Skills auto-load when you ask Claude to write PM artifacts |
| creative-developer | "Write Phaser and Remotion code" = Claude Code + `phaser-game-patterns`, `remotion-fundamentals` skills | Claude Code IS a developer; skills give it domain knowledge |
| asset-artist | "Generate and process sprites" = Claude Code + `sprite-pipeline`, `ai-creative-tools`, `pixel-art-retro-style` skills | Skills contain the exact workflows and tool commands |
| senior-ui-designer | "Build UI components" = Claude Code + `react-vite-tailwind`, `tailwind-advanced-patterns`, `figma-to-code-workflow` skills | Claude Code + design skills = UI builder |
| senior-developer | IS Claude Code | Claude Code is literally a senior developer |
| claude-mastery-guide | 34 claude-mastery skills auto-load for any Claude Code question | Skills cover CLI, hooks, MCP, settings, troubleshooting |

## The Hybrid Pattern

The most effective setup pairs agents with skills:

```
User asks Claude to BUILD something
  → Skills auto-load (domain knowledge for execution)
  → Claude Code builds it

User asks an Agent to REVIEW the output
  → Agent evaluates against structured criteria
  → Agent produces formatted review with severity-tagged findings

User asks Claude to FIX the issues
  → Skills auto-load again (remediation knowledge)
  → Claude Code applies fixes
```

This "Build → Review → Fix" loop is the intended workflow. Skills handle the "Build" and "Fix" steps. Agents handle the "Review" step.

## Summary

| Question | Skill | Agent |
|----------|-------|-------|
| Does it provide knowledge? | Yes | No |
| Does it define evaluation criteria? | No | Yes |
| Does it produce formatted assessments? | No | Yes |
| Does it need tool restrictions? | No | Sometimes |
| Can Claude Code + skills do this already? | N/A | If yes, don't create the agent |
| Does it have a distinct output format? | Optional | Required |
| Does it involve judgment with severity levels? | No | Yes |
