# Obsidian Integration - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Obsidian Integration"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. I use Obsidian as my primary knowledge management tool and want to create a bidirectional bridge between my Obsidian vault and Claude Code — Obsidian stores and organizes knowledge, Claude Code retrieves and acts on it. My stack is React, Python, Supabase.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers **Obsidian + Claude Code integration** for AI-powered knowledge management.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Obsidian Integration") contains deep research on integrating Obsidian vaults with Claude Code: MCP server implementations (obsidian-claude-code-mcp, mcp-obsidian, obsidian-rag-mcp), AI-native Obsidian plugins (Claudian, Smart Connections, MCP Tools), vault architecture for AI retrieval, metadata conventions, bidirectional workflows, semantic search/embeddings, and advanced automation patterns. Sources include MCP server documentation, plugin guides, PKM methodology articles, and community implementations.

## Your Task

Analyze all sources in this notebook and generate **5-6 Claude Skills** that make Claude Code and Obsidian work together as an integrated knowledge system. The goal: my vault becomes an AI-queryable knowledge base that Claude Code can read from and write to.

## Target Skills to Extract

### 1. Obsidian MCP Setup & Connection
**Priority**: High
**What to extract**: Step-by-step MCP server installation (comparing obsidian-claude-code-mcp, mcp-obsidian, and obsidian-rag-mcp — recommend the most mature/reliable), configuration in Claude Code settings, authentication setup, transport protocol selection (WebSocket vs HTTP/SSE), troubleshooting connection failures, and verifying the connection works. Include the actual JSON configuration for settings.json.
**Trigger phrases**: "connect to Obsidian", "Obsidian MCP", "set up vault access", "Obsidian not connecting", "vault integration"

### 2. AI-Optimized Vault Architecture
**Priority**: High
**What to extract**: Folder structure patterns that work for both human navigation AND AI retrieval, YAML frontmatter schema optimized for Claude Code filtering (type, status, tags, keywords, related, project, ai-processed fields), atomic note principles adapted for embeddings, linking strategies that help AI traverse the knowledge graph (MOCs, index notes, wiki-link conventions), and note templates that are "RAG-ready" from creation.
**Trigger phrases**: "organize my vault", "vault structure", "frontmatter template", "note template", "optimize for AI", "vault architecture"

### 3. Bidirectional Read/Write Workflows
**Priority**: High
**What to extract**: Querying vault content from Claude Code sessions (prompt patterns, MCP search commands, context injection strategies), writing Claude Code outputs back to Obsidian (note creation, proper markdown formatting, source tracking), daily note workflows with AI assistance, research synthesis (web search → Obsidian note), and batch processing patterns (using Dataview to identify notes needing AI processing).
**Trigger phrases**: "search my vault", "find notes about", "save this to Obsidian", "update my notes", "process my inbox", "daily note"

### 4. Semantic Search & Embeddings
**Priority**: Medium
**What to extract**: Local embedding solutions (sqlite-vec, privacy-preserving options), cloud embedding services and their tradeoffs, similarity search implementation, combining keyword and semantic search, embedding update strategies as vault grows, and practical setup for a beginner. Recommend the simplest path to working semantic search.
**Trigger phrases**: "semantic search", "find related notes", "similar notes", "embeddings", "search by meaning"

### 5. Automation with Templater & Dataview
**Priority**: Medium
**What to extract**: Templater templates that create AI-friendly notes (dynamic frontmatter, date stamps, type selection), Dataview queries for AI processing queues (find notes where ai-processed: false), batch operation patterns, status tracking workflows (draft → review → processed), and combining Obsidian plugins with Claude Code MCP for automated knowledge management.
**Trigger phrases**: "Templater template", "Dataview query", "batch process notes", "automate vault", "processing queue"

### 6. Knowledge Graph Navigation
**Priority**: Lower
**What to extract**: How Claude Code can follow wiki-links to build context, MOC (Map of Content) patterns for topic clusters, using backlinks for concept discovery, building project-specific context from linked notes, and traversal strategies that help Claude Code understand the relationships between concepts in your vault.
**Trigger phrases**: "related concepts", "follow links", "knowledge graph", "topic cluster", "build context from vault"

## Extraction Guidance

- **Recommend ONE clear path**: The MCP server landscape is fragmented. Don't present all options equally — recommend the most reliable/mature option and mention alternatives briefly.
- **Privacy emphasis**: My Obsidian vault contains personal and work knowledge. Emphasize local-first approaches, especially for embeddings.
- **Beginner setup**: The setup process can be intimidating. Break it into phases: Phase 1 (basic read/write), Phase 2 (structured notes), Phase 3 (semantic search). Don't require Phase 3 to get value from Phase 1.
- **Real frontmatter schemas**: Include actual YAML frontmatter examples, not just field descriptions. Show what a complete, well-structured note looks like.
- **Dataview integration**: Include real DQL (Dataview Query Language) examples that are copy-paste ready.
- **File naming matters**: Include conventions for file naming that help both human browsing and AI search.

## Cross-Domain Notes

- **MCP Setup** connects to Core Features (MCP server integration patterns)
- **Vault Architecture** connects to Life Optimization (knowledge management methodology — this skill is the technical implementation)
- **Bidirectional Workflows** connects to PM Workflows (documentation), Community Resources (learning notes), and Life Optimization (second brain)
- **Semantic Search** connects to Advanced Techniques (context management) and Technical Stack (Python embeddings)
- **Automation** connects to Core Features (hooks, headless mode) for automated vault maintenance

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include actual configuration JSON, YAML frontmatter examples, and DQL queries
- Recommend the single best approach first, with alternatives noted
- Work incrementally — each skill provides standalone value, even without the others
- Be testable (include "verify it works" steps after setup)
- Handle the "my vault already has 500 unstructured notes" case, not just greenfield vaults

---

## PROMPT END
