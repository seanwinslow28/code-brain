# Claude Skill Design Patterns

## Degrees of Freedom

Match specificity to the task's fragility:

**High freedom** (text instructions): Multiple approaches valid, decisions depend on context.
**Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation OK.
**Low freedom** (specific scripts, few params): Operations are fragile, consistency critical, specific sequence required.

Think of Claude walking a path: narrow bridge with cliffs = guardrails (low freedom), open field = many routes (high freedom).

## Progressive Disclosure Patterns

### Pattern 1: High-level guide with references
```markdown
# PDF Processing

## Quick start
Extract text with pdfplumber:
[code example]

## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```
Claude loads FORMS.md or REFERENCE.md only when needed.

### Pattern 2: Domain-specific organization
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```
User asks about sales → Claude only reads sales.md.

### Pattern 3: Framework/variant organization
```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
User chooses AWS → Claude only reads aws.md.

### Pattern 4: Conditional details
```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

## Workflow Patterns

### Sequential Workflows
```markdown
Filling a PDF form involves these steps:
1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

### Conditional Workflows
```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below
```

## Output Patterns

### Template Pattern (strict)
```markdown
ALWAYS use this exact template structure:
# [Analysis Title]
## Executive summary
[One-paragraph overview]
## Key findings
- Finding 1 with data
## Recommendations
1. Specific actionable recommendation
```

### Template Pattern (flexible)
```markdown
Here is a sensible default format, but use your best judgment:
# [Analysis Title]
## Executive summary
[Overview]
## Key findings
[Adapt sections as needed]
```

### Examples Pattern
When output quality depends on seeing examples, provide input/output pairs:
```markdown
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## Key Guidelines
- Avoid deeply nested references — keep one level deep from SKILL.md
- Structure longer reference files (>100 lines) with a table of contents
- Information should live in EITHER SKILL.md or references, not both
- Default to SKILL.md for core workflow; use references for detailed/variant-specific info
