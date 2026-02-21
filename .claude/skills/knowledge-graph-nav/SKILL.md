---
name: knowledge-graph-nav
description: Obsidian knowledge graph navigation for Claude Code. Traverse wiki-links, build multi-hop context from linked notes, discover backlinks, and navigate Map of Content structures. Use when following concept links, building project context from vault, discovering related topics, navigating MOCs, or traversing the knowledge graph.
---

# Knowledge Graph Navigation

## Purpose

Navigate Obsidian knowledge graphs from Claude Code sessions. Traverse wiki-links to build multi-hop context, discover backlinks for concept relationships, use MOC structures for topic exploration, and build project-specific context from linked notes.

## When to Use

- Following wiki-links to build deep context for a task
- Discovering what notes reference a given concept (backlinks)
- Navigating MOC (Map of Content) structures for topic clusters
- Building project-specific context from linked notes
- Finding conceptual connections between vault topics

## Examples

**Example 1: Project context gathering**
```
User: "Gather all context for Project Beta"
Claude: [Uses knowledge-graph-nav] Reads Project Beta dashboard,
follows wikilinks to Requirements, Meetings, and Specs notes,
synthesizes context from 1-hop linked notes, drafts implementation plan.
```

**Example 2: Concept discovery via backlinks**
```
User: "What notes reference Strategic Planning?"
Claude: [Uses knowledge-graph-nav] Runs grep for [[Strategic Planning]],
reads referring notes, summarizes the constraints and decisions
mentioned in those contexts.
```

**Example 3: Topic exploration via MOC**
```
User: "Explore my AI notes starting from the MOC"
Claude: [Uses knowledge-graph-nav] Reads AI MOC, selects the 3 most
relevant linked notes for the specific sub-topic, summarizes their
key insights with cross-references.
```

## Traversal Strategies

### Strategy 1: Forward Link Traversal (Context Expansion)

Read a note, identify wiki-links, then read linked notes to build context depth.

**Workflow:**
1. Read the entry note (e.g., `Project Alpha.md`)
2. Identify key wikilinks: `[[Client Requirements]]`, `[[Architecture Diagram]]`
3. Read those specific linked files
4. Synthesize the combined context

**Best Practice:** Use Plan Mode (Shift+Tab in Claude Code) for complex traversals. Claude creates a step-by-step plan before reading files, preventing unnecessary token consumption.

**Prompt Pattern:**
> "Read `Project Beta.md`. Follow all wikilinks listed under the 'Core Docs' section. Using that context, draft an implementation plan."

### Strategy 2: Backlink Discovery (Reverse Traversal)

Find all notes that reference a given concept. Obsidian stores outgoing links but not incoming ones in the file itself.

**The Grep Strategy:**

```bash
# Find all notes referencing a concept
grep -r "\[\[Neural Networks\]\]" .

# Find all notes referencing a specific project
grep -r "\[\[Project Alpha\]\]" --include="*.md" .

# Count references to identify hub concepts
grep -rl "\[\[Machine Learning\]\]" . | wc -l
```

**Prompt Pattern:**
> "Find all notes that reference [[Strategic Planning]] and summarize the key constraints mentioned in those referring contexts."

### Strategy 3: MOC-Based Navigation

MOCs act as curated routers. Point Claude at a MOC instead of asking it to search the entire vault.

**MOC Structure:**
```markdown
# Artificial Intelligence MOC

## Foundations
- [[Neural Networks]] - Architecture fundamentals
- [[Transformer Architecture]] - Attention mechanisms
- [[Vector Embeddings]] - Numerical representations

## Applications
- [[RAG Architecture]] - Retrieval augmented generation
- [[Semantic Search]] - Meaning-based retrieval

## Tools and Implementations
- [[Ollama Setup]] - Local model hosting
- [[sqlite-vec]] - Vector database
```

**Prompt Pattern:**
> "Read `AI MOC.md`, then select the three most relevant linked notes regarding 'Transformers' and summarize them."

### Strategy 4: Multi-Hop Context Building

Build progressively deeper context by following links through multiple levels.

**Depth Levels:**
| Depth | What Gets Read | Token Cost | Use Case |
| :--- | :--- | :--- | :--- |
| 0 | Entry note only | Low | Quick reference |
| 1 | Entry + directly linked notes | Medium | Standard context |
| 2 | Entry + links + links-of-links | High | Deep research |

**Prompt Pattern for Depth-2:**
> "Read `Agentic Memory.md`. For each wikilink in that note, read the linked note. For any new concepts found in those notes, read one more level. Synthesize a comprehensive overview."

**Warning:** Depth-2 traversals can consume significant context. Limit to 3-5 first-hop notes and 2-3 second-hop notes per branch.

## MCP Graph Tools

Some MCP server implementations expose specialized graph operations:

| Tool | Function | When to Use |
| :--- | :--- | :--- |
| `get_backlinks` | List incoming links | Faster than grep for large vaults |
| `guided_path` | Narrative tour through linked notes | Exploratory learning |
| `graph_traversal` | Depth-specified traversal | Automated context building |
| `get_similar_notes` | Vector similarity (Smart Connections) | Concept discovery |

**MCP Config for Graph-Capable Server:**
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/yourname/Documents/MyVault"
      }
    }
  }
}
```

## Practical Workflows

### Auto-Link New Notes

When adding a new note, automatically create bidirectional connections:

> "I am adding a new note about 'Vector Databases'. Search my vault for existing notes that mention 'embeddings', 'similarity search', or 'RAG'. Update the new note to include [[wikilinks]] to these existing concepts, and add a backlink to this new note in the 'related' section of those existing files."

### Dashboard-Based Context Loading

1. Create a dashboard note: `Project Beta.md` with links to Requirements, Meetings, and Specs
2. Ask Claude to read the dashboard and follow links for context
3. Result: Claude loads only relevant notes, not the entire vault

### Semantic Graph Traversal (Concept Discovery)

Find connections between concepts that are not explicitly linked:

1. Use Smart Connections MCP: `get_similar_notes`
2. Convert query to vector, find KNN in note embeddings
3. Return semantically related notes and their direct links

> "Find notes conceptually related to 'Agentic Memory' even if they don't use that exact term. Traverse the graph to find any parent concepts they share."

## Graph Navigation Best Practices

1. **Atomic notes**: One concept per note ensures retrieval precision. A 5,000-word file wastes context tokens when only one link is relevant
2. **CLAUDE.md rules**: Explicitly instruct link handling:
   - "When creating notes, always check for existing related topics and link them"
   - "Use `[[wikilinks]]` format, not standard markdown links"
3. **Progressive disclosure**: Start with a MOC or Dashboard, let Claude request deeper nodes as needed
4. **Anchor files**: Maintain an `ACTIVE_PROJECTS.md` or `PROGRESS.md` as a root node for work sessions
5. **Link aggressively**: Every `[[concept]]` in brackets is a traversable edge in the graph. More links mean richer context paths

## Success Criteria

- [ ] Claude can follow wiki-links from a note and read linked content
- [ ] Backlink discovery returns notes referencing a given concept
- [ ] MOC navigation provides structured topic exploration
- [ ] Multi-hop traversal builds context without exceeding token limits
- [ ] New notes are auto-linked to existing related concepts

## Copy/Paste Ready

```
"Follow the links in Project Alpha and summarize the context"
"Find all notes that reference this concept"
"Navigate my AI MOC and summarize key topics"
"Build context from my vault for this task"
"What concepts are related to agentic workflows in my vault?"
```
