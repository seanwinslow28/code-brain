# NotebookLM Notebook: Claude Code + Obsidian RAG Integration

**Purpose:** Deep Research prompts and synthesis questions for building Obsidian as your ultimate second brain with Claude Code as the intelligent retriever
**Vision:** Obsidian = Storage Layer | Claude Code = RAG Agent | Bidirectional Knowledge Flow

---

## Understanding This Notebook

### The Goal
Transform Obsidian from a note-taking app into an AI-powered knowledge engine where:
- **Obsidian** stores, organizes, and links your knowledge (the vault)
- **Claude Code** retrieves, synthesizes, and acts on that knowledge (the agent)
- **MCP** bridges the two systems seamlessly
- **You** focus on thinking and creating while AI handles retrieval

### Why This Matters
Modern RAG (Retrieval-Augmented Generation) systems work best when:
1. Knowledge is structured for machine comprehension
2. Metadata enables semantic filtering
3. Bidirectional sync keeps everything current
4. The AI understands relationships between concepts

---

## SECTION 1: MCP Infrastructure & Technical Setup

### 1.1 Obsidian MCP Servers
```
Claude Code MCP servers for Obsidian vault integration 2025-2026: comparing obsidian-claude-code-mcp, mcp-obsidian, smithery mcp-obsidian, and MarkusPfundstein implementations. Focus on setup requirements, capabilities (read/write/search), transport protocols (WebSocket vs HTTP/SSE), and which server works best for RAG workflows.
```

### 1.2 RAG-Specific MCP Implementations
```
Obsidian RAG MCP servers and semantic search implementations: obsidian-rag-mcp, obsidian-elite-rag, and mcp-tools with semantic search. Cover vector embedding approaches, similarity search capabilities, and how to enable Claude Code to find semantically related notes rather than just keyword matches.
```

### 1.3 MCP Authentication & Security
```
Security considerations for connecting Claude Code to Obsidian vaults via MCP: authentication methods, API key management, file system permissions, and protecting sensitive notes from AI access. Include best practices for vault access control.
```

### 1.4 Multi-Client MCP Configurations
```
Running multiple MCP clients with Obsidian: simultaneous connections from Claude Code CLI, Claude Desktop, and other MCP-compatible tools. Cover auto-discovery, transport protocol differences, and maintaining consistent vault state across clients.
```

---

## SECTION 2: AI-Native Obsidian Plugins

### 2.1 Obsidian Claude Code Plugin
```
Obsidian Claude Code plugin deep dive: installation, configuration with Anthropic API keys or Claude Max subscription, vault-search skill with sqlite-vec embeddings, SQL queries over frontmatter metadata, and real-world usage patterns for knowledge retrieval.
```

### 2.2 Claudian Plugin Integration
```
Claudian plugin for embedding Claude as AI collaborator in Obsidian: agentic capabilities, file operations, bash execution, multi-step workflows, and how it compares to external MCP connections. Include setup guides and practical use cases.
```

### 2.3 Smart Connections & Embeddings
```
Obsidian Smart Connections plugin for AI-powered knowledge discovery: local embeddings, vector database support, finding semantically related notes, and integrating with external AI tools. Focus on making your vault searchable by meaning, not just keywords.
```

### 2.4 MCP Tools Plugin
```
Obsidian MCP Tools plugin: semantic search capabilities, Templater prompt execution integration, and custom MCP tool creation within Obsidian. Cover how this extends vault accessibility to any MCP-compatible client.
```

### 2.5 Supporting Plugins for AI Workflows
```
Essential Obsidian plugins that enhance AI integration: Templater for dynamic templates, Dataview for structured queries, QuickAdd for rapid capture, and how these plugins create hooks for AI-powered automation.
```

---

## SECTION 3: Vault Architecture for AI Retrieval

### 3.1 AI-Optimized Folder Structures
```
Obsidian vault folder structures optimized for AI retrieval 2025-2026: comparing PARA method, Zettelkasten, and hybrid approaches. Focus on structures where Claude Code can efficiently navigate, understand context, and retrieve relevant notes.
```

### 3.2 Atomic Notes for Machine Comprehension
```
Atomic note-taking principles adapted for AI consumption: single-thought entries, optimal note length for embeddings, splitting strategies for long content, and maintaining human readability while optimizing for machine retrieval.
```

### 3.3 Linking Strategies for Knowledge Graphs
```
Obsidian linking strategies that help AI understand relationships: wiki-link conventions, MOC (Maps of Content) patterns, index notes, and how Claude Code traverses your knowledge graph to find related concepts.
```

### 3.4 Consume-Curate-Create-Meta Framework
```
The Consume-Curate-Create-Meta vault organization framework: structuring knowledge flow from raw intake through processing to output, with metadata systems that track each note's lifecycle stage for AI-assisted workflows.
```

### 3.5 Project-Based Knowledge Contexts
```
Project-based knowledge management in Obsidian with AI integration: organizing project-specific notes, maintaining context across sessions, building queryable knowledge bases per project, and enabling Claude Code to access project-relevant information.
```

---

## SECTION 4: Metadata & Formatting Conventions

### 4.1 YAML Frontmatter for AI
```
YAML frontmatter schemas optimized for AI comprehension: essential fields (type, status, tags, keywords, related), machine-readable date formats, relationship declarations, and metadata patterns that enable Claude Code to filter and understand notes.
```

### 4.2 Inline Fields & Dataview Integration
```
Obsidian inline field conventions (Key:: Value) for AI-queryable metadata: Dataview-compatible patterns, real-time status tracking, and how Claude Code can use inline fields to understand note context without parsing full content.
```

### 4.3 Tagging Strategies for Retrieval
```
Obsidian tagging strategies that optimize AI retrieval: hierarchical tags, semantic tag clusters, tag namespacing, and balancing human navigation with machine searchability. Include patterns for consistent tag vocabularies.
```

### 4.4 Heading Hierarchies & Structure
```
Markdown structural conventions for AI parsing: heading hierarchy best practices, section organization, code block tagging, and formatting patterns that help Claude Code understand document structure and extract relevant sections.
```

### 4.5 Templates for AI-Friendly Notes
```
Obsidian templates that create AI-friendly notes: Templater templates with AI-optimized frontmatter, dynamic field generation, and starter structures that ensure new notes are immediately RAG-ready.
```

---

## SECTION 5: Bidirectional Workflows

### 5.1 Querying Your Vault from Claude Code
```
Workflows for querying Obsidian vaults from Claude Code sessions: prompt patterns that reference vault content, context injection strategies, MCP search commands, and efficiently pulling relevant knowledge into AI conversations.
```

### 5.2 Writing AI Output Back to Obsidian
```
Capturing Claude Code outputs as Obsidian notes: automatic note creation from AI sessions, formatting AI responses as properly-structured markdown, timestamp and source tracking, and maintaining quality in AI-generated notes.
```

### 5.3 Batch Processing with Dataview
```
Batch processing Obsidian notes with Claude Code and Dataview: using DQL queries to identify notes needing AI processing, executing batch operations, applying consistent transformations, and updating processing status metadata.
```

### 5.4 Conversational Daily Notes
```
AI-assisted daily note workflows in Obsidian: Claude Code capturing daily insights through conversation, automatic wiki-linking to related topics, smart summarization, and building a connected daily journal.
```

### 5.5 Research Synthesis Workflows
```
Research workflows combining Claude Code web search with Obsidian storage: capturing research findings, synthesizing sources into topic notes, maintaining citation links, and building research knowledge bases.
```

---

## SECTION 6: Semantic Search & Embeddings

### 6.1 Local Embedding Solutions
```
Local embedding solutions for Obsidian RAG: sqlite-vec implementations, local vector databases, privacy-preserving embedding generation, and running semantic search entirely on your machine without cloud dependencies.
```

### 6.2 Cloud Embedding Services
```
Cloud embedding services for Obsidian semantic search: OpenAI embeddings, Claude-compatible embedding APIs, hybrid local/cloud approaches, and tradeoffs between privacy, cost, and search quality.
```

### 6.3 Similarity Search Implementation
```
Implementing similarity search in Obsidian for Claude Code retrieval: nearest-neighbor algorithms, threshold tuning for relevance, combining keyword and semantic search, and optimizing retrieval for your knowledge domain.
```

### 6.4 Embedding Update Strategies
```
Maintaining embedding freshness in Obsidian: incremental embedding updates, handling note modifications, re-indexing strategies, and keeping semantic search accurate as your vault grows and changes.
```

---

## SECTION 7: Advanced Automation Patterns

### 7.1 Templater + Claude Code Automation
```
Obsidian Templater combined with Claude Code automation: templates that trigger AI processing, dynamic content generation workflows, and building command templates that bridge Templater and MCP capabilities.
```

### 7.2 Dataview-Driven AI Processing Queues
```
Using Dataview as an AI processing queue: DQL queries identifying notes pending processing, status tracking fields, batch operation patterns, and automating AI work across your vault based on metadata conditions.
```

### 7.3 Git-Based Version Control
```
Git workflows for Obsidian vaults with AI integration: automatic commits after AI modifications, version history for AI-generated content, backup strategies, and using GitHub/GitLab for vault access from multiple machines.
```

### 7.4 Multi-Vault Architectures
```
Multi-vault Obsidian strategies with Claude Code: separating personal/work knowledge, cross-vault references, unified search across vaults, and managing multiple knowledge domains with AI assistance.
```

### 7.5 Canvas Integration
```
Obsidian Canvas combined with Claude Code: visual planning with AI assistance, spatial organization of knowledge, workflows that leverage both visual thinking and AI analysis.
```

---

## SECTION 8: Community Implementations

### 8.1 Knowledge Vault Systems
```
Complete Obsidian + Claude Code PKM implementations 2025-2026: reviewing Knowledge Vault, obsidian-claude-pkm starter kit, and Claudesidian pre-configured vaults. Focus on what makes these systems effective and how to adapt them.
```

### 8.2 Second Brain Architectures
```
Second brain architectures designed for AI augmentation: capture workflows, processing systems, retrieval patterns, and synthesis strategies. Include real implementations from power users.
```

### 8.3 Skills & Agents for Obsidian
```
Claude Code skills and agents specifically for Obsidian workflows: note organizer agents, weekly reviewer agents, inbox processor skills, and how to create custom skills for your knowledge management needs.
```

### 8.4 Troubleshooting & Common Issues
```
Troubleshooting Claude Code + Obsidian integration: common MCP connection failures, embedding errors, sync issues, permission problems, and community resources for getting help.
```

---

## Synthesis Questions: After Importing Sources

### Architecture & Setup Questions

```
Based on sources, what's the complete technical stack for Obsidian + Claude Code RAG? List every component needed.
```

```
Create a step-by-step installation guide: MCP server → Obsidian plugins → Claude Code configuration → first successful query.
```

```
What are the minimum requirements vs full power-user setup? Compare configurations.
```

```
Which MCP server implementation is most mature and well-maintained? Analyze community activity.
```

### Vault Organization Questions

```
What vault structure best supports both human navigation AND machine retrieval? Find the balance.
```

```
Create an ideal YAML frontmatter template based on what sources recommend for AI comprehension.
```

```
What linking conventions help AI understand note relationships? Compile specific patterns.
```

```
How should atomic note length differ when optimizing for embeddings? Find the sweet spot.
```

### Workflow Questions

```
Describe the complete bidirectional workflow: thought → Obsidian → Claude retrieval → AI output → back to Obsidian.
```

```
What's the best way to reference Obsidian content in Claude Code prompts? Show exact syntax.
```

```
How do I build persistent project context that Claude can access across sessions?
```

```
What automation is possible with Templater + Dataview + Claude Code together? Map the possibilities.
```

### Plugin & Tool Questions

```
Rank all Obsidian AI plugins by: maturity, features, ease of setup, and RAG capability.
```

```
Compare local vs cloud embedding solutions: privacy, cost, quality, and setup complexity.
```

```
What can Smart Connections do that native MCP can't? Identify unique capabilities.
```

```
Which community implementations should I study first? Prioritize by relevance to RAG workflows.
```

### Knowledge Management Strategy Questions

```
How should my PKM practices change now that AI can retrieve from my vault?
```

```
What note-taking habits maximize AI retrieval quality? List behavioral changes.
```

```
How do I balance writing for myself vs writing for AI comprehension?
```

```
What's the maintenance burden of an AI-optimized vault? Is it sustainable?
```

### Source Quality Questions

```
Which sources have actual working implementations vs theoretical approaches?
```

```
Flag any outdated information (pre-2025) or deprecated plugins/methods.
```

```
If I could only follow 3 sources for setting up Obsidian + Claude RAG, which should they be?
```

```
What do sources disagree about? List contradictions and which approach seems more validated.
```

---

## Quick Start Implementation Path

### Phase 1: Foundation (Day 1)
1. Install MCP server (start with obsidian-claude-code-mcp)
2. Configure Claude Code to connect to your vault
3. Test basic read/search operations

### Phase 2: Structure (Days 2-3)
4. Implement YAML frontmatter template for all new notes
5. Add essential AI plugins (Smart Connections or MCP Tools)
6. Create folder structure following AI-optimized patterns

### Phase 3: Workflow (Days 4-5)
7. Build Templater templates for AI-friendly note creation
8. Set up Dataview queries for processing queues
9. Test bidirectional workflows (query → process → write back)

### Phase 4: Optimization (Ongoing)
10. Enable semantic search / embeddings
11. Create custom skills for your specific workflows
12. Build automation for recurring tasks

---

## Sample Note Structure for AI Retrieval

```markdown
---
title: Example Note Title
created: 2026-02-02
modified: 2026-02-02
type: reference
status: active
tags: [topic/subtopic, domain, concept]
keywords: [searchable, terms, for, AI]
related: [[Note A]], [[Note B]]
project: project-name
ai-processed: false
---

# Example Note Title

## Summary
One paragraph capturing the core insight for quick AI retrieval.

## Details
Expanded information with clear sections.

### Subsection
Specific details that AI can extract when queried.

## Related Concepts
- [[Link to Related]] - brief description of relationship
- [[Another Related]] - why this matters

## Sources
- [Source Name](URL) - what was learned

## Open Questions
- Question that needs more research?
```

This structure enables Claude Code to:
- Filter by type, status, project, tags
- Extract summaries for quick answers
- Follow links for deeper context
- Identify notes needing processing
- Understand relationships between concepts

---

## Sources

This notebook was informed by research on:
- [NotebookLM Deep Research](https://blog.google/technology/google-labs/notebooklm-deep-research-file-types/)
- [Obsidian Claude Code MCP](https://github.com/iansinnott/obsidian-claude-code-mcp)
- [Smart Connections Plugin](https://github.com/brianpetro/obsidian-smart-connections)
- [Obsidian RAG MCP Server](https://glama.ai/mcp/servers/@claudiogarza/obsidian-rag-mcp)
- [Knowledge Vault System](https://gist.github.com/naushadzaman/164e85ec3557dc70392249e548b423e9)
- [Obsidian Claude PKM Starter Kit](https://github.com/ballred/obsidian-claude-pkm)
