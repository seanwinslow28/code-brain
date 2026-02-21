---
title: Prompts Index
created: "2026-02-08"
tags: [moc, prompts]
status: active
---

# Prompts Library

Reusable prompt packages organized by domain. These can be turned into skills, sub-agents, or just copy-pasted into conversations.

## How to Use
1. Find a prompt below that fits your need
2. Copy it into a Claude Code conversation, or
3. Turn it into a skill: copy to `.claude/skills/{name}/SKILL.md` with frontmatter
4. Turn it into an agent: copy to `.claude/agents/{name}.md` with frontmatter

## By Domain

### Claude Code
- (Add prompts for meta-tasks, debugging, configuration)

### Product Management
- (Add prompts for PRD writing, stakeholder comms, analysis)

### Creative Studio
- (Add prompts for game design, video production, art direction)

### Life Systems
- (Add prompts for financial analysis, habit tracking, learning plans)

### Design
- (Add prompts for design reviews, accessibility audits, component specs)

## Prompt Template
```markdown
---
title: Prompt Name
created: YYYY-MM-DD
tags: [prompt, domain-tag]
domain: which-domain
---

## Context
When to use this prompt.

## Prompt
The actual prompt text.

## Variables
- `{variable}`: What to replace it with

## Example Output
What good output looks like.
```
