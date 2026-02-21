# Claude Agent Skill — Anatomy Reference

## What is a Skill?
A Skill is a folder of instructions, scripts, and resources that Claude loads dynamically to perform specialized tasks. Skills are read by an AI agent, not humans. They transform Claude from a general-purpose agent into a specialized one.

## Required: SKILL.md

### YAML Frontmatter (REQUIRED)
```yaml
---
name: skill-name
description: What the skill does AND when Claude should trigger it. This is the ONLY metadata Claude reads to decide whether to load the skill. Be comprehensive and specific.
---
```

Only `name` and `description` are required. The optional `compatibility` field notes environment requirements but is rarely needed.

### Markdown Body
- Loaded AFTER the skill triggers
- Should be under 500 lines
- Uses imperative/infinitive form ("Extract text..." not "This extracts...")
- Contains only information Claude doesn't already know

## Optional: Bundled Resources

### scripts/
Executable code for tasks requiring deterministic reliability or repeated execution.
- Example: `scripts/rotate_pdf.py`, `scripts/validate_schema.py`
- Benefits: Token efficient, deterministic, can be executed without reading into context
- Always test scripts before including

### references/
Documentation Claude reads as-needed to inform its process.
- Example: `references/api-docs.md`, `references/schema.md`, `references/policies.md`
- Benefits: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- If >100 lines, include a table of contents at the top
- If >10k words, include grep search patterns in SKILL.md
- Keep one level deep from SKILL.md

### assets/
Files used in the output Claude produces (never loaded into context).
- Example: `assets/logo.png`, `assets/template.pptx`, `assets/font.ttf`
- Use cases: Templates, images, icons, boilerplate code, fonts

## What NOT to Include
- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, QUICK_REFERENCE.md
- Human-facing documentation
- Setup/testing procedures
- Auxiliary context about the creation process

## Progressive Disclosure (3 Levels)
1. **Metadata (name + description)** — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (<5k words ideal)
3. **Bundled resources** — Loaded as-needed by Claude (unlimited)

## Frontmatter Description Best Practices
The description is the primary triggering mechanism. It should include:
- What the skill does
- Specific triggers/contexts for when to use it
- All "when to use" information (NOT in the body — body is only loaded after triggering)

Example:
```
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
```

## Compression Principles
- Claude is already very smart — only add context it doesn't already have
- Challenge each piece: "Does this justify its token cost?"
- Prefer concise examples over verbose explanations
- The context window is a shared resource — Skills compete for space with system prompts, conversation history, and other Skills
