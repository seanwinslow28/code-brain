# Claude Skill Examples

These are real-world examples of well-structured Claude Skills for reference when creating new ones.

## Example 1: Simple Workflow Skill (Jira Ticket Writer)

```yaml
---
name: jira-ticket-writer
description: Generate Jira tickets following company standards - Epics, Design Stories, and Implementation Stories for product development
---
```

```markdown
# Jira Ticket Writer

## Overview
Generate properly formatted Epics, Design Stories ([Design] prefix), and Implementation Stories ([Implementation] prefix).

## Quick Reference
| Ticket Type | Prefix | Use Case |
|-------------|--------|----------|
| Epic | None | Feature container |
| Design Story | [Design] | UI/UX work |
| Implementation Story | [Implementation] | Dev work |

## Workflow
1. Identify the feature scope from user input
2. Create Epic with summary and acceptance criteria
3. Break into Design and Implementation stories
4. Apply correct labels, components, and story point estimates
```

## Example 2: Document Processing Skill (with scripts)

```
pdf-processor/
├── SKILL.md
├── scripts/
│   ├── extract_text.py
│   ├── fill_form.py
│   └── merge_pdfs.py
└── references/
    └── form-field-types.md
```

SKILL.md frontmatter:
```yaml
---
name: pdf-processor
description: "Extract text/tables from PDFs, fill PDF forms, merge/split PDFs, add watermarks. Use when user mentions .pdf files or asks to create, edit, fill, merge, or manipulate PDFs."
---
```

## Example 3: Domain Knowledge Skill (with references)

```
crypto-research/
├── SKILL.md
└── references/
    ├── token-taxonomy.md
    ├── defi-protocols.md
    └── regulatory-framework.md
```

SKILL.md body excerpt:
```markdown
# Crypto Research Assistant

## Quick start
Analyze crypto projects using standard evaluation framework.

## Workflows
**Token analysis** → Read references/token-taxonomy.md first
**DeFi protocol review** → Read references/defi-protocols.md first
**Regulatory compliance check** → Read references/regulatory-framework.md first

## Evaluation Framework
1. Assess tokenomics (supply, distribution, utility)
2. Review smart contract architecture
3. Evaluate team and governance
4. Check regulatory status per references/regulatory-framework.md
```

## Example 4: Creative/Asset Skill (with assets)

```
brand-content/
├── SKILL.md
├── assets/
│   ├── logo.png
│   ├── brand-colors.json
│   └── slide-template.pptx
└── references/
    └── brand-voice-guide.md
```

## Anti-Patterns to Avoid

### ❌ Too verbose (wastes tokens)
```markdown
## Introduction
This skill is designed to help Claude understand how to process
PDF documents. PDF stands for Portable Document Format and was
created by Adobe in 1993...
```

### ✅ Concise (respects token budget)
```markdown
## PDF Processing
Extract text: `pdfplumber`. Fill forms: `scripts/fill_form.py`.
For field type reference, see `references/form-fields.md`.
```

### ❌ Includes human-facing docs
```
skill/
├── SKILL.md
├── README.md           ← DELETE THIS
├── INSTALLATION.md     ← DELETE THIS
├── CHANGELOG.md        ← DELETE THIS
```

### ✅ Clean structure
```
skill/
├── SKILL.md
├── references/
└── scripts/
```

### ❌ Duplicate information
SKILL.md contains the full API schema AND references/api.md contains the same schema.

### ✅ Single source of truth
SKILL.md says: "For API schema details, see references/api.md"

## Packaging for Claude.ai
1. Create the folder structure with all files
2. ZIP the skill folder
3. Rename .zip to .skill (optional — Claude accepts both)
4. Upload via Claude.ai Settings > Features > Custom Skills
5. Or use the API: POST /v1/skills with the files
