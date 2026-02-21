---
type: reference
domain:
  - vault
  - claude-mastery
status: active
context: personal-finance
ai-context: "I've built out a notebook within NotebookLM called Claude Code..."
created: 2026-02-20
source: apple-notes-import
---

# I've built out a notebook within NotebookLM called Claude Code…

 I've built out a notebook within NotebookLM called Claude Code -     
   Obsidian Integration. Please provide me with a detailed prompt      
  that I can bring into Gemini 3.0 Deep Think that will have the       
  Claude Code - Obsidian Integration Notebook as a reference and       
  use it's Google Deep Think Search and synthesis capabilities to      
  search even further and help me set up the optimal Obsidian       
  Vault based on my personal context and goals. I'd also like to       
  find out what kind of plug ins and MCP's I should connect to my      
  Obsidian to truly a beautiful home for a second brain and make       
  it automate-able with Claude Code. Feel free to view the SKILLS      
  we've already created and the notebooklm-mcp to view the             
  notebook to help with the prompt 

ROLE

  You are an Obsidian vault architect and personal knowledge management (PKM) consultant. You have
  access to my NotebookLM notebook "Claude Code - Obsidian Integration" which contains my existing
  research on connecting Obsidian to Claude Code via MCP servers, vault architecture patterns,
  semantic search, Templater/Dataview automation, knowledge graph navigation, and bidirectional
  read/write workflows. Use it as your foundation, then use Deep Think Search to go significantly
  further.

  ABOUT ME (Personal Context)

  - Name: Sean Winslow
  - Location: Transitioning from Boston, MA to a new city
  - Career: Product Manager at The Block (crypto/Web3 data company), transitioning toward Animation
  Production Management/Producing
  - Daily routine: 4:45 AM waker, work split is roughly 45% PM work / 35% creative projects / 20%
  personal systems
  - Technical stack I actively use:
    - Claude Code CLI (power user — I have 102 custom skills, 13 agents, 7 hooks built)
    - React + Vite + Tailwind, Supabase, Python automation
    - Phaser 3 (Game Boy-style RPG game dev), Remotion (programmatic video), Adobe Creative Suite
  via MCP
    - React Native (mobile apps)
    - Docker, Git worktrees for parallel development
  - What I'm managing across my life:
    - Product management deliverables (PRDs, sprint planning, stakeholder updates, Jira automation,
  data analysis)
    - Creative projects (2D animation, pixel art, game dev, video production, script writing)
    - Personal finance (bank CSV imports, subscription audits, budget tracking)
    - Health & habits (workout logs, streak tracking, gamified XP system)
    - Learning acceleration (study plans, Anki flashcard generation, concept drills)
    - Life admin (move planning, file organization, recurring tasks)
    - Career transition planning (PM to animation production management)

  MY CURRENT VAULT STATE

  I have a skeleton Obsidian vault with PARA structure already scaffolded:
  vault/
  ├── 00-Inbox/          (empty)
  ├── 01-Projects/       (1 project: "Claude Code - Adobe Mastery")
  ├── 02-Areas/          (empty)
  ├── 03-Resources/      (empty)
  ├── 04-Archive/        (empty)
  ├── MOCs/              (6 Map of Content files: Home, Claude Mastery, Product Management, Creative
   Studio, Life Systems, Design Team)
  ├── Prompts/           (1 index file)
  ├── RAG/               (1 README)
  ├── Templates/         (4 templates: daily-note, idea-note, meeting-note, project-note)

  I also have 6 Claude Code skills already built for vault integration:
  1. obsidian-mcp-setup — MCP server installation (mcp-obsidian, obsidian-claude-code-mcp,
  smart-connections-mcp)
  2. obsidian-semantic-search — Local embeddings with sqlite-vec, Ollama, Smart Connections
  3. vault-architecture — NIPARAS folder structure, YAML frontmatter schema with ai-context fields
  4. vault-automation — Templater templates, Dataview queries, AI processing queues, status
  lifecycle
  5. vault-read-write — Bidirectional workflows, slash commands (/day, /research, /process-inbox,
  /compress)
  6. knowledge-graph-nav — Wiki-link traversal, backlink discovery, MOC navigation, multi-hop
  context building

  WHAT I NEED YOU TO RESEARCH AND SYNTHESIZE

  Please use Deep Think Search to investigate each of these areas thoroughly, then synthesize
  findings into an actionable blueprint.

  PART 1: Optimal Vault Architecture for My Use Case

  Given my specific domains (PM work, creative production, personal finance, health, learning,
  career transition), research and recommend:

  1. Folder structure refinement — Is PARA sufficient, or should I adopt a hybrid (PARA +
  Zettelkasten, PARA + Johnny Decimal, ACCESS method by Nick Milo)? What does the latest PKM
  community consensus say for someone managing 6+ life domains with AI integration?
  2. Frontmatter schema optimization — My current schema includes type, status, tags, keywords,
  related, ai-context fields. Research what frontmatter fields the most sophisticated Obsidian + AI
  users are using in 2025-2026. Should I add domain, energy-level, review-date, source-type, or
  other fields?
  3. Note type taxonomy — What note types should I define beyond
  concept/meeting/project/journal/resource? Research the Zettelkasten community's
  "fleeting/literature/permanent" distinction and how it maps to AI processing workflows.
  4. Daily notes best practices — Research the most effective daily note structures for someone who
  uses them as both a personal journal and an AI processing input. How should my daily notes feed
  into weekly reviews that Claude Code can automate?
  5. Cross-domain linking strategy — How should I link notes across my 6 domains? When a PM meeting
  note references a creative project deadline, what's the optimal linking pattern for both human
  navigation and AI retrieval?

  PART 2: Essential Obsidian Plugins

  Research and rank the most important Obsidian plugins for my use case. For each, explain what it
  does, why I specifically need it, and how it integrates with AI/Claude Code. Investigate at
  minimum:

  Core Infrastructure:
  - Dataview (and DataviewJS)
  - Templater
  - Local REST API (for MCP connectivity)
  - Smart Connections (for semantic search/embeddings)

  Visual & Navigation:
  - Graph Analysis / Graph View enhancements
  - Breadcrumbs (hierarchical nav)
  - Excalidraw (visual thinking, diagrams)
  - Canvas (native alternative to Excalidraw)
  - Strange New Worlds (backlink context previews)

  Productivity & Capture:
  - QuickAdd (rapid capture with templates)
  - Periodic Notes (daily/weekly/monthly note automation)
  - Tasks (task management within notes)
  - Kanban (visual board for projects)
  - Calendar (daily note navigation)

  Data & Automation:
  - Metadata Menu (frontmatter management GUI)
  - DB Folder (database-like folder views)
  - Commander (custom command palette)
  - CustomJS (custom JavaScript in vault)
  - Obsidian Git (automatic backup/versioning)

  AI-Specific:
  - Smart Connections
  - Copilot (Obsidian-native AI chat)
  - Text Generator
  - Any new 2025-2026 AI plugins I should know about

  Search which plugins have been updated recently, which are abandoned/unmaintained, and which have
  known compatibility issues. I don't want to install dead plugins.

  PART 3: MCP Servers for Obsidian + Claude Code

  Research the current MCP server ecosystem for Obsidian as of early 2026. My notebook covers three:
  1. mcp-obsidian (stdio, basic CRUD)
  2. obsidian-claude-code-mcp (WebSocket + HTTP/SSE, auto-discovery)
  3. smart-connections-mcp (semantic search via Smart Connections embeddings)

  Please investigate:
  - Are there newer/better MCP servers that have emerged since my research?
  - What is the current state of obsidian-claude-code-mcp — is it stable? Community reception?
  - Can I run multiple MCP servers simultaneously (e.g., basic CRUD + semantic search)?
  - What MCP servers outside of Obsidian should I connect to create a true second brain ecosystem?
  Consider:
    - Todoist / Linear / Jira MCP for task sync
    - Google Calendar MCP for schedule context
    - Readwise MCP for reading highlights
    - Notion MCP (if I have any Notion data to migrate)
    - Browser/web MCP for clipping and research
    - File system MCP for accessing documents outside the vault
    - Any other MCPs that would create a powerful ambient knowledge layer

  PART 4: Automation Recipes

  Design 5-7 concrete automation workflows that combine Obsidian plugins + Claude Code + MCP
  servers:

  1. Morning Briefing — Auto-generate a daily note that pulls in today's calendar, open tasks, and
  recent project updates
  2. Inbox Processing Pipeline — How captures from mobile (phone), browser, email, and voice all
  flow into 00-Inbox and get processed by Claude Code
  3. Weekly Review Automation — Claude Code reads the week's daily notes, extracts decisions/open
  loops, updates project statuses, generates a review note
  4. Research-to-Knowledge Pipeline — Web research → structured vault note with frontmatter,
  wikilinks, and MOC updates
  5. Spaced Repetition Integration — How notes flagged for learning automatically become Anki cards
  or drill prompts
  6. Financial Data Pipeline — Bank CSV → categorized transactions → monthly report note in vault
  7. Creative Project Tracker — How game dev, animation, and video projects track progress through
  vault notes

  PART 5: Making It Beautiful

  Research how to make the vault visually gorgeous and pleasant to use daily:
  - Best Obsidian themes for 2025-2026 (dark mode, readable, modern)
  - CSS snippets for custom styling (callouts, headers, status badges)
  - Icon packs and visual enhancements
  - Dashboard/homepage design patterns (the "life OS" homepage trend)
  - How to make Dataview tables and queries look good, not just functional
  - Mobile experience optimization (Obsidian on iPhone/iPad)

  PART 6: Migration & Setup Roadmap

  Given that my vault is mostly empty (just the skeleton), provide a phased rollout plan:
  - Phase 1 (Day 1): What to install and configure immediately
  - Phase 2 (Week 1): First content migration and template setup
  - Phase 3 (Weeks 2-3): Automation setup and MCP connections
  - Phase 4 (Month 1): Refinement, custom CSS, advanced workflows
  - Phase 5 (Ongoing): Maintenance habits, review cadences

  OUTPUT FORMAT

  Structure your response as a comprehensive blueprint document with:
  1. Executive Summary (1 paragraph — the "why this architecture" thesis)
  2. Architecture Decision Record (folder structure, frontmatter schema, linking strategy — with
  rationale)
  3. Plugin Stack (tiered: Essential / Recommended / Nice-to-Have, with install order)
  4. MCP Ecosystem Map (diagram of all connected services)
  5. Automation Playbook (each workflow as a numbered recipe with trigger → action → output)
  6. Visual Design Guide (theme, CSS, dashboard layout)
  7. Phased Roadmap (timeline with specific actions per phase)
  8. Open Questions (anything you couldn't fully resolve that I should test myself)

  For each recommendation, cite your sources and indicate confidence level (High/Medium/Low) based
  on how current and well-supported the information is.

  SEARCH GUIDANCE

  When doing Deep Think Search, prioritize:
  - The Obsidian community forum (forum.obsidian.md) for plugin recommendations and compatibility
  reports
  - r/ObsidianMD on Reddit for real-world user experiences
  - Nick Milo's Linking Your Thinking (LYT) community for vault architecture patterns
  - GitHub repos for MCP server status (stars, recent commits, open issues)
  - YouTube channels: Nicole van der Hoeven, Danny Hatcher, Sergio (FromSergio) for vault tours and
  plugin reviews
  - The Model Context Protocol specification and community for MCP server ecosystem updates
  - Search specifically for "Obsidian AI integration 2025" and "Obsidian Claude Code" for the most
  recent developments
