# Depth & Format Addendum for Agents

Append this section to any of the 5 domain extraction prompts when extracting agents. It overrides default compression behavior to produce agents with enough behavioral substance to be operationally useful.

---

## ADDENDUM — Paste this after the "PROMPT END" line of any extraction prompt

---

## Output Depth Requirements

Agent extraction requires a different kind of depth than skill extraction. Skills need code patterns and reference data. Agents need **behavioral specificity** — concrete criteria, clear severity levels, complete output templates, and multi-step workflows.

### Minimum Content Per Agent

- **Agent body**: 60-180 lines minimum. Under 60 lines means you've compressed too far.
- **Review Dimensions / Analysis Framework**: The bulk section must be 40-100 lines of concrete criteria organized by dimension. Each dimension needs specific checkpoints, not vague principles.
- **Output Format**: Must contain a COMPLETE template in a code block. Include all sections, severity levels, and placeholder values. This is non-negotiable — an agent without a complete output template is incomplete.

### What "Concrete Criteria" Means

BAD (too vague):
```markdown
### Security
- Check for security issues
- Look for vulnerabilities
- Review authentication
```

GOOD (operationally useful):
```markdown
### Authentication & Authorization
- Hardcoded credentials in source → Critical: extract to environment variables
- API endpoints without auth middleware → Critical: add authentication guard
- Missing role-based access checks → Important: implement RBAC for sensitive operations
- Session tokens without expiry → Important: add token TTL (recommended: 1 hour access, 7 day refresh)
- Password stored in plaintext → Critical: use bcrypt with cost factor >= 12
```

### What "Complete Output Template" Means

BAD (too skeletal):
```markdown
## Output Format
Report findings with severity levels.
```

GOOD (complete template):
````markdown
## Output Format

```
## Security Review: [Target Name]

### Overall Risk: [Low/Medium/High/Critical]

### Findings

#### Critical (must fix before merge)
- [file:line] [Description] — Remediation: [specific fix]

#### Important (should fix in this PR)
- [file:line] [Description] — Remediation: [specific fix]

#### Minor (fix when convenient)
- [file:line] [Description] — Suggestion: [improvement]

### Summary
[2-3 sentences: overall security posture, most concerning pattern, recommended priority]

### Next Steps
1. [Most urgent action]
2. [Second priority]
3. [Longer-term improvement]

Reviewed by security-reviewer agent
```
````

### Mandatory Agent Structure

Every agent MUST follow this exact section order. Do NOT skip sections or invent new ones.

```markdown
---
name: Agent Display Name
description: What this agent does AND when to invoke it. Embed trigger phrases naturally.
disallowedTools:     # Optional. Include for read-only agents.
  - Edit
  - Write
  - Bash
---

# Agent Name Agent

## Purpose

One paragraph: what this agent does and why it exists. Imperative form.

## When to Use

Bullet list of specific invocation scenarios:
- Scenario 1
- Scenario 2
- Scenario 3

## How It Works

1. Step 1 of agent's internal workflow
2. Step 2
3. Step 3 (minimum 3 steps, maximum 6)

## Invocation Examples

- "Quoted realistic prompt 1"
- "Quoted realistic prompt 2"
- "Quoted realistic prompt 3"

## [Domain-Specific Dimensions]

The bulk of the agent (40-100 lines). Organized by evaluation dimension.

## Output Format

Complete template in a code block with placeholder values.

## Constraints

What the agent cannot do. 2-4 bullet points.

## Pairs Well With

- `skill-or-agent-name` — brief explanation of synergy
```

### Behavioral Focus

Agents must contain BEHAVIORAL content — judgment criteria, evaluation workflows, decision frameworks, severity scoring. NOT factual knowledge, code patterns, or reference data (those belong in skills).

**The test**: After generating the agent, could Claude produce a structured, actionable review of a real artifact using ONLY the criteria in this file? If the agent just says "review the code for issues" without specifying what issues to look for and how to score them, you've written a skill placeholder, not an agent.

### Output Checklist (Run Before Writing)

For EACH agent, verify:
- [ ] YAML frontmatter has `name` and `description` (description embeds trigger phrases naturally)
- [ ] `disallowedTools` present if read-only, uses correct casing (`Edit`, `Write`, `Bash`)
- [ ] Section order: Purpose > When to Use > How It Works > Invocation Examples > Dimensions > Output Format > Constraints > Pairs Well With
- [ ] How It Works has 3-6 numbered steps
- [ ] Invocation Examples has 3-5 realistic quoted prompts
- [ ] Review/Analysis Dimensions section is 40-100 lines with concrete criteria
- [ ] Output Format has a COMPLETE template in a code block (not just "report findings")
- [ ] Pairs Well With references 3-5 existing skills or agents from the pack
- [ ] Agent body is 60-180 lines (not under 60)
- [ ] Content is behavioral (judgment, criteria, scoring) not informational (facts, code, reference data)
- [ ] Imperative form throughout
- [ ] Zero emoji anywhere
- [ ] Clean markdown — no escaped characters, saveable directly as .md
- [ ] For upgrades: new version covers everything the thin version covered, plus richer dimensions

---

## END ADDENDUM
