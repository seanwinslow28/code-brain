# Agent Examples

These are real agents from the Claude Code Superuser Pack, representing different quality tiers. Use them to calibrate the quality bar when generating new agents.

## Example 1: Rich Review Agent (checklist-validator — 136 lines)

This is the gold standard. Note the structured validation levels, clear methodology, output template with tables, and integration guidance.

```yaml
---
name: Checklist Validator
description: Validates work against acceptance criteria before marking done
disallowedTools:
  - Edit
  - Write
---
```

Key structural elements:
- **Purpose**: Clear single-paragraph description of role
- **Validation Levels**: Quick (syntax), Standard (content), Thorough (cross-reference)
- **Validation Methodology**: Step-by-step workflow with decision points
- **Output Format**: Complete template with pass/fail table, overall status, follow-up actions
- **Integration**: Shows how to pair with doc-reviewer and ticket sources

What makes it RICH:
- Multiple operational modes (Quick/Standard/Thorough)
- Concrete criteria for each mode
- Output template includes a results table, not just prose
- References complementary agents and skills
- 136 lines of actionable content

## Example 2: Rich Review Agent (doc-reviewer — 183 lines)

The richest agent. Note the document-type-specific checklists and four review dimensions.

```yaml
---
name: Doc Reviewer
description: Reviews PRDs, tech specs, and documentation for completeness, clarity, actionability, and audience fit. Invoke when you want a quality review of written product artifacts.
disallowedTools:
  - Edit
  - Write
  - Bash
---
```

Key structural elements:
- **Four Review Dimensions**: Completeness, Clarity, Actionability, Audience Fit
- **Document-Type Checklists**: Different criteria for PRD vs Tech Spec vs Stakeholder Update
- **Severity Levels**: Critical / Important / Minor
- **Output Format**: Full review template with per-dimension scoring
- **Pairing**: References prd-generator skill and checklist-validator agent

What makes it RICH:
- Separate review criteria per document type (not one-size-fits-all)
- Concrete checklist items (not vague principles)
- Clear severity definitions
- 183 lines — the most comprehensive agent in the pack

## Example 3: Medium Review Agent (visual-polish-auditor — 85 lines)

Solid focused agent. Clear categories, concrete criteria, but less depth than Rich tier.

```yaml
---
name: Visual Polish Auditor
description: Final-pass visual quality review for animations, loading states, empty states, error states, and micro-interactions. Invoke before shipping UI to catch polish gaps.
disallowedTools:
  - Edit
  - Write
  - Bash
---
```

Key structural elements:
- **Six Polish Categories**: Animations, Loading, Empty, Error, Micro-interactions, Edge Cases
- **Performance Indicators**: What to check for each category
- **Severity**: High Impact / Medium Impact / Low Impact
- **Output Format**: Category-by-category findings with impact level

What makes it MEDIUM (not Rich):
- Categories are well-defined but criteria are less granular than doc-reviewer
- Fewer conditional workflows (no document-type branching)
- Still useful and focused — 85 lines of actionable content

## Example 4: Thin Agent (data-analyst — 37 lines) — BELOW QUALITY BAR

This is what we're upgrading. Note the generic capabilities list and lack of structured output.

```yaml
---
name: Data Analyst
description: Analyzes data, creates visualizations, and provides insights for decision-making
---
```

What makes it THIN (needs upgrade):
- Generic capability list instead of specific review dimensions
- No structured output format template
- No "How It Works" workflow steps
- No severity levels or evaluation framework
- No "Pairs Well With" references
- 37 lines — barely a skeleton

To upgrade this to Rich quality, add:
- Analysis workflow (data intake → cleaning → exploration → insight extraction)
- Visualization selection framework (when to use bar vs line vs scatter)
- Statistical rigor criteria (sample size, significance, correlation vs causation)
- Domain-specific metrics (crypto/fintech: TVL, volume, market cap)
- Complete output template with executive summary, findings table, viz recommendations

## Quality Tier Summary

| Tier | Lines | Characteristics | Examples |
|------|-------|-----------------|----------|
| Rich | 120-180+ | Multiple modes/dimensions, document-type branching, concrete checklist items, complete output template with tables | checklist-validator, doc-reviewer |
| Medium | 60-100 | Clear categories, concrete criteria, severity levels, output template | ui-reviewer, visual-polish-auditor, accessibility-checker |
| Thin (UNACCEPTABLE) | <60 | Generic capability lists, no output template, no workflow, no criteria | data-analyst (pre-upgrade), game-design-advisor (pre-upgrade) |

## Target for New Agents

All new and upgraded agents should aim for **Rich tier** (100-150 lines). The minimum acceptable quality is **Medium tier** (60+ lines with all mandatory sections).

No agent should ship below 60 lines. If you cannot reach 60 lines of actionable behavioral content, the agent may not be justified — consider whether a skill would serve the purpose better.
