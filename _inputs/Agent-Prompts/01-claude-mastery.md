# Claude Mastery — Agent Extraction Prompt

Use this prompt with the **Agent Extraction Kickoff** after connecting to the **"Claude Code - Core Features"** and **"Claude Code - Advanced Techniques"** NotebookLM notebooks.

---

## PROMPT START — Process this domain with the Kickoff Prompt

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals, working across three domains: PM work, creative projects (React Native + Phaser game dev), and life optimization/automation. My stack is React, Python, Supabase, and I use Claude Code as my primary development tool.

I'm upgrading existing thin agents to rich quality. These agents provide **structured review and evaluation** for the Claude Mastery domain — they don't teach Claude Code features (that's what the 34 claude-mastery skills do).

## What's in These Notebooks

**Notebook 1: "Claude Code - Core Features"** (284 sources)
Core architecture and capabilities: CLI, skills system, hooks lifecycle, subagents, MCP, plugins, headless mode, permissions, configuration management. Sources include Anthropic docs, community tutorials, power user discussions, and security patterns.

**Notebook 2: "Claude Code - Advanced Techniques"** (54 sources)
Advanced patterns: Plan Mode vs Extended Thinking, multi-instance coordination, context management, verification loops, security hardening, permission hierarchies.

## Your Task

Extract behavioral knowledge from these notebooks and generate **2 upgraded agents** for the Claude Mastery domain. These agents REVIEW and EVALUATE — they don't execute or build.

## Target Agents

### 1. UPGRADE: security-reviewer
**Priority**: High
**Current state**: 51 lines, generic capability list, no review dimensions, no output template
**Current file**: `.claude/agents/security-reviewer.md` (READ THIS FIRST)
**Type**: Review agent (read-only)
**disallowedTools**: Edit, Write, Bash

**What to extract from notebooks**:
- Security review dimensions: authentication/authorization, secrets exposure, injection vulnerabilities (XSS, SQL, command), dependency risks, permission configuration
- Claude Code-specific security patterns: hook exit codes for blocking, settings.json permission rules, MCP security scope (user vs project vs managed), secrets in CLAUDE.md
- OWASP Top 10 mapping to Claude Code projects (which apply to typical React/Python/Supabase stack)
- Severity framework: what makes a finding Critical vs Important vs Minor
- Remediation patterns for common findings

**Output format requirements**:
- Overall risk assessment (Low/Medium/High/Critical)
- Findings table organized by severity with file:line references
- Remediation guidance per finding
- Summary with recommended priority actions

**Trigger phrases**: "security review", "audit this code", "check for vulnerabilities", "is this safe", "security audit"

**Must preserve from current thin agent**: Code security review, vulnerability assessment, identifying hardcoded secrets, reviewing auth logic, dependency vulnerabilities

### 2. UPGRADE: compliance-summarizer
**Priority**: Medium
**Current state**: 52 lines, generic capability list, no compliance framework, no output template
**Current file**: `.claude/agents/compliance-summarizer.md` (READ THIS FIRST)
**Type**: Review agent (read-only)
**disallowedTools**: Edit, Write, Bash

**What to extract from notebooks**:
- Compliance dimensions: settings hierarchy adherence (Enterprise > Local > Project > User), hook configuration correctness, permission rule evaluation order (Deny > Ask > Allow), DoD (Definition of Done) validation, coding standards compliance
- Claude Code configuration compliance: are hooks using correct exit codes? Are disallowedTools using deny-list pattern? Are settings.json permissions well-ordered?
- Organizational policy patterns: how to check code against team style guides, security policies, deployment requirements
- Pass/fail criteria for each compliance dimension

**Output format requirements**:
- Compliance matrix: dimension × status (Pass/Fail/Warning) table
- Failed items with specific finding and remediation
- Overall compliance score (percentage or letter grade)
- Sign-off recommendation (Compliant / Conditionally Compliant / Non-Compliant)

**Trigger phrases**: "compliance check", "policy review", "is this compliant", "audit against standards", "definition of done check"

**Must preserve from current thin agent**: Code compliance review, policy compliance checking, security policy compliance

## Extraction Guidance

- Focus on BEHAVIORAL content: evaluation criteria, severity definitions, pass/fail thresholds. NOT on explaining what Claude Code features are (that's what skills do).
- The security-reviewer should be able to audit ANY code in the project, not just Claude Code config files.
- The compliance-summarizer focuses on organizational/team standards compliance, not just security.
- Both agents must have complete Output Format templates with severity levels and placeholder values.
- Cross-reference with the permission system: hooks that enforce permissions, settings precedence, MCP security scope.

## Cross-Domain Notes

These agents serve the entire project:
- security-reviewer is invoked before any deployment or PR merge
- compliance-summarizer validates against team standards and DoD
- Both pair with `security-hardening` and `org-security` skills for remediation
- Both pair with `checklist-validator` agent for acceptance criteria validation

## Quality Bar

Each generated agent should:
- Be 100-140 lines (Rich tier)
- Have concrete, actionable review dimensions (not vague principles)
- Include a complete output format template with all severity levels
- Reference real skills and agents from the pack in "Pairs Well With"
- Cover everything the thin agent covered, plus significantly richer dimensions

---

## PROMPT END
