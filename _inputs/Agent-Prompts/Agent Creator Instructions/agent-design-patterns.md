# Agent Design Patterns

## Agent Archetypes

Match the agent's structure to its behavioral role:

### Archetype 1: Review Agent (read-only)
**Pattern**: Evaluate an artifact against structured criteria, produce a scored report.
**disallowedTools**: Edit, Write, Bash
**Key sections**: Review Dimensions with severity levels, Output Format with scoring template.
**Examples**: security-reviewer, ui-reviewer, accessibility-checker, doc-reviewer

```markdown
## Review Dimensions

### [Dimension Name]
- Criterion 1: [what to check] — Critical if [condition], Important if [condition]
- Criterion 2: [what to check] — Score [how]
```

### Archetype 2: Workflow Agent (read-write)
**Pattern**: Execute a multi-step process that transforms input into structured output.
**disallowedTools**: (none — needs full tool access)
**Key sections**: Step-by-step methodology, decision points, output template.
**Examples**: scrum-master, life-systems-coach, vault-curator

```markdown
## Breakdown Methodology

### Step 1: Analyze Input
Read the source document. Identify [what to look for].

### Step 2: Apply Framework
For each [item], evaluate:
- [Criterion A]: determines [output property]
- [Criterion B]: determines [output property]

### Step 3: Generate Output
Produce structured [output type] following the Output Format template.
```

### Archetype 3: Advisory Agent (read-only or limited write)
**Pattern**: Provide expert judgment on decisions, trade-offs, or creative direction.
**disallowedTools**: Edit, Write (can read but not modify)
**Key sections**: Evaluation framework, decision criteria, advisory output.
**Examples**: video-director, game-design-advisor

```markdown
## Evaluation Framework

### [Aspect 1]
Consider: [factors]
Red flags: [what indicates problems]
Best practices: [what good looks like]
```

## Dimension Design

### Severity Levels (for review agents)
Use consistent severity across all review agents:

| Level | Label | Meaning | Action Required |
|-------|-------|---------|-----------------|
| 1 | Critical | Blocks ship, security risk, data loss | Must fix before merge |
| 2 | Important | Significant quality issue | Should fix in this PR |
| 3 | Minor | Polish, best practice | Fix when convenient |
| 4 | Info | Observation, suggestion | No action required |

### Scoring (for review agents)
When an overall score is appropriate:
- **1-3**: Major issues, needs significant rework
- **4-6**: Functional but notable issues
- **7-8**: Good with minor improvements
- **9-10**: Excellent, production-ready

### Criteria Specificity
BAD (too vague):
```
### Code Quality
- Check if the code is clean
- Look for problems
```

GOOD (actionable):
```
### Code Quality
- Functions exceed 50 lines → Important: extract helper functions
- More than 3 levels of nesting → Important: flatten with early returns
- No error handling on API calls → Critical: add try/catch with user-facing error
- Magic numbers without constants → Minor: extract to named constant
```

## Output Format Design

### Template Requirements
Every agent MUST have an Output Format section with a complete template. The template should:
1. Be enclosed in a markdown code block
2. Include placeholder values (not just labels)
3. Show the full structure from heading to sign-off
4. Include all severity levels even if some might be empty
5. End with a signature line: `Reviewed by [agent-name] agent`

### Table Formats (for structured data)
```markdown
| Item | Estimate | Priority | Dependencies |
|------|----------|----------|--------------|
| [Epic/Story name] | [points] SP | [P0/P1/P2] | [list] |
```

### Checklist Formats (for pass/fail reviews)
```markdown
- [x] Criterion passed
- [ ] **FAIL**: Criterion description — [remediation guidance]
```

## How It Works — Step Design

### For Review Agents
```
1. Read the target [code/document/artifact]
2. Evaluate each review dimension systematically
3. Assign severity to each finding
4. Score the overall quality
5. Generate the structured review output
```

### For Workflow Agents
```
1. Read the input [PRD/data/vault structure]
2. Identify [components/patterns/items] to process
3. Apply [framework/methodology] to each item
4. Validate [internal consistency/completeness]
5. Generate structured output in the standard format
6. Present summary with key decisions made
```

### For Advisory Agents
```
1. Read the target [composition/design/plan]
2. Evaluate against [domain-specific framework]
3. Identify strengths and concerns
4. Formulate specific, actionable recommendations
5. Present advisory report with prioritized suggestions
```

## Pairs Well With — Design

Complementary pairings follow three patterns:

### Review → Fix Pattern
Agent identifies issues, skill provides knowledge to fix them:
```
- `security-hardening` skill — apply fixes after security review identifies vulnerabilities
```

### Sequential Review Pattern
Multiple agents review the same artifact from different angles:
```
- `accessibility-checker` agent — run after UI review for WCAG compliance
```

### Upstream → Downstream Pattern
One agent's output feeds another's input:
```
- `scrum-master` agent — break the reviewed PRD into implementation stories
```

## Anti-Patterns

### Agent as Knowledge Store
BAD: Agent contains reference data, lookup tables, or code patterns.
FIX: Move knowledge to a Skill. Agent should reference the skill: "Uses patterns from `security-hardening` skill."

### Agent Without Output Format
BAD: Agent describes what it does but has no structured output template.
FIX: Every agent must produce a specific, formatted output. If you can't define the format, it's not an agent.

### Agent That Just Wraps a Skill
BAD: Agent's only behavior is "load this skill and run it."
FIX: If the skill alone does the job, you don't need the agent. Agents add judgment, criteria, scoring, or workflow steps that skills cannot encode.

### Overlapping Descriptions
BAD: Two agents with similar trigger phrases in their descriptions.
FIX: Make descriptions non-overlapping. Each agent should have a clearly distinct trigger surface.
