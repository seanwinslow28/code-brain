---
name: vault-architecture
description: AI-optimized Obsidian vault structure designer. Create folder hierarchies, YAML frontmatter schemas, and note templates that work for both human navigation and AI retrieval. Use when organizing a vault, designing frontmatter schemas, creating note templates, optimizing for RAG, or restructuring an existing vault for AI workflows.
---

# AI-Optimized Vault Architecture

## Purpose

Design Obsidian vault structures that serve both human browsing and AI retrieval. Define folder hierarchies, standardized YAML frontmatter schemas, atomic note principles, MOC linking strategies, and RAG-ready templates that maximize retrieval accuracy.

## When to Use

- Setting up a new Obsidian vault for AI integration
- Restructuring an existing vault (the "500 unstructured notes" case)
- Designing YAML frontmatter schemas for AI filtering
- Creating note templates optimized for embeddings
- Building Map of Content (MOC) index notes

## Examples

**Example 1: New vault setup**
```
User: "Organize my vault for Claude Code access"
Claude: [Uses vault-architecture] Creates the NIPARAS folder structure with
CLAUDE.md, templates folder, and MOC starter notes. Sets up frontmatter
schema with type/status/tags/ai-context fields.
```

**Example 2: Retrofit existing vault**
```
User: "I have 500 unstructured notes, help me organize for AI"
Claude: [Uses vault-architecture] Scans existing notes, proposes folder
migration plan, creates batch frontmatter update script, and generates
MOC index notes by tag cluster.
```

**Example 3: Frontmatter template**
```
User: "What frontmatter should my notes have?"
Claude: [Uses vault-architecture] Outputs the standard YAML schema with
type, status, tags, keywords, related, project, and ai-context fields.
Includes a complete example note.
```

## Folder Structure: The NIPARAS Pattern

A hybrid of PARA (Tiago Forte) adapted for AI retrieval. Each folder provides clear context to both humans and AI agents.

```
Vault Root/
+-- CLAUDE.md                    # System prompt for AI agents
+-- 00_Inbox/                    # Capture point (AI monitors for processing)
+-- 01_Projects/                 # Active, time-bound initiatives
|   +-- Project-Alpha/
|   |   +-- CLAUDE.md            # Project-specific AI rules
|   |   +-- notes...
+-- 02_Areas/                    # Ongoing responsibilities (Health, Finance)
+-- 03_Resources/                # Atomic reference notes, concepts
+-- 04_Archive/                  # Completed projects, inactive items
+-- 05_System/                   # Templates, scripts, AI configuration
|   +-- Templates/
|   +-- Scripts/
+-- .claude/                     # Claude Code configuration
|   +-- commands/                # Custom slash commands
|   +-- skills/                  # Reusable AI workflows
+-- Maps/                        # MOC (Map of Content) index notes
```

Use a `MANIFEST.md` or `_Index.md` in large folders. List every file with a one-line summary so AI tools can understand folder contents without scanning thousands of tokens.

## YAML Frontmatter Schema

Apply this schema consistently across all notes. AI agents filter and categorize by these fields.

```yaml
---
# Core Identity
type: concept          # values: concept, meeting, person, project, source, journal
status: active         # values: seedling, draft, active, review, permanent, archived
created: 2024-06-15
updated: 2024-06-16

# Semantic Context
tags: [ai, knowledge-management]       # Broad categories
keywords: [vector database, embeddings] # Specific entities for search
project: "[[Project-Alpha]]"           # Link to active project
related:                               # Explicit concept relationships
  - "[[Vector Embeddings]]"
  - "[[Retrieval Augmented Generation]]"

# AI Processing Fields
ai-context:
  processed: false           # Boolean: has AI reviewed this note?
  summary: ""                # Pre-computed summary for low-cost retrieval
  next-actions: []           # AI-extracted action items
  source: ""                 # Model used (e.g., "Claude 3.5 Sonnet")
  last-run: null             # Timestamp of last AI update
---
```

### Field Purposes

| Field | Purpose | AI Use |
| :--- | :--- | :--- |
| `type` | Categorize note kind | Filter context by type |
| `status` | Track lifecycle stage | Find draft/review items |
| `tags` | Broad categories | Group related notes |
| `keywords` | Specific entities | Precise search hits |
| `related` | Explicit links | Build context graphs |
| `ai-context.processed` | Track AI interaction | Build processing queues |
| `ai-context.summary` | Pre-computed summary | Skip full note reads |

## Atomic Note Principles for Embeddings

Atomic notes improve RAG retrieval precision. When a vector search retrieves a note, it gets only the relevant concept, not 10 pages of mixed topics.

1. **One idea per note.** "Cosine Similarity" not "Math Overview"
2. **Semantic integrity.** The note makes sense in isolation. Avoid orphaned pronouns ("It works by...") in the first paragraph. Use explicit nouns so the embedding captures the subject
3. **Descriptive titles.** "Optimization Techniques for Vector Embeddings" not "Optimization"
4. **Heading structure.** Use clear H1/H2 headers. AI models chunk by headers for retrieval
5. **Context block.** Include `ai-context.summary` in frontmatter for hybrid search (keyword + vector)

## MOC (Map of Content) Patterns

MOCs provide structured navigation that helps AI explore a domain without scanning the entire vault.

### Hub and Spoke Pattern

```markdown
# AI and Machine Learning MOC

## Core Concepts
- [[Neural Networks]] - Foundation architectures
- [[Transformer Architecture]] - Attention mechanisms
- [[Vector Embeddings]] - Numerical text representations

## Applications
- [[RAG Architecture]] - Retrieval augmented generation
- [[Semantic Search]] - Meaning-based retrieval

## Tools
- [[Ollama Setup]] - Local model hosting
- [[ChromaDB]] - Vector database
```

### AI-Generated MOC Prompt

> "Analyze all notes tagged `#AI` and create a structured Map of Content grouping them by sub-topic. Include a one-line summary for each linked note."

### Linking Best Practices

- Wrap key concepts in `[[brackets]]` aggressively. This creates graph edges that AI can traverse
- Use folder-scoped linking for ambiguous terms: `[[Projects/App/Sprint]]` vs `[[Fitness/Sprint]]`
- RAG systems can pull "1-hop neighbors" (notes directly linked) for deeper context

## Complete RAG-Ready Note Template

```markdown
---
type: concept
status: active
created: {{date}}
tags: [knowledge-management]
keywords: []
related: []
ai-context:
  processed: false
  summary: ""
  next-actions: []
---

# {{title}}

## Definition

One-paragraph definition using explicit nouns. Avoid pronouns in
the opening sentence to ensure the embedding captures the subject.

## Key Principles

1. Principle with concrete detail
2. Principle with concrete detail

## Connections

- Related to [[Concept A]] because...
- Builds on [[Concept B]] by...

## References

- Source: [[Original Source Note]]
```

## File Naming Conventions

- Use descriptive names: `vector-embedding-optimization.md` not `notes-v2.md`
- Kebab-case for consistency: `project-alpha-requirements.md`
- Prefix daily notes with date: `2024-06-15.md` in a `Daily Notes/` folder
- MOC files: prefix with `MOC -` for easy identification

## Success Criteria

- [ ] Every note has consistent YAML frontmatter with type and status fields
- [ ] Folder structure has clear separation between projects, areas, and resources
- [ ] CLAUDE.md exists at vault root with structure description
- [ ] MOC notes exist for major topic clusters
- [ ] Notes follow atomic principles (one idea per note)
- [ ] AI processing queue can be built from frontmatter fields

## Copy/Paste Ready

```
"Organize my vault for Claude Code"
"Design a frontmatter schema for AI filtering"
"Create a note template optimized for RAG"
"Build a Map of Content for my AI notes"
"Restructure my existing vault for AI workflows"
```
