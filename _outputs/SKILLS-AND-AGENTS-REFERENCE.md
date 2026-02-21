# Claude Code Superuser Pack: Skills & Agents Reference

This document catalogs all 89 skills and 11 agents available in Sean's Claude Code Superuser Pack. Use this as a reference for Claude Desktop or other contexts that need to understand the pack's capabilities.

---

## Agents (11 total)

Agents are specialized subagents that can be invoked for specific review or analysis tasks. Most are read-only (cannot edit files) to ensure they provide objective feedback.

### Domain Agents (7)

| Agent | Purpose | Restrictions |
|-------|---------|--------------|
| **checklist-validator** | Validates work against acceptance criteria and checklists. Use before marking tickets done or merging PRs. Parses criteria, gathers evidence, performs gap analysis, and provides confidence scores. | Read-only (no Edit, Write) |
| **context-gatherer** | Gathers minimal relevant context from codebase without pulling entire repo. Use before writing PRDs, tech specs, or making architectural decisions. Returns <2000 tokens of targeted context. | Read-only (no Edit, Write, Bash) |
| **doc-reviewer** | Reviews PRDs, tech specs, and documentation for completeness, clarity, and actionability. Catches gaps before stakeholders do. Provides scores for clarity, completeness, and actionability. | Read-only (no Edit, Write, Bash) |
| **data-analyst** | Analyzes data, creates visualizations, and provides insights for decision-making. Handles statistical analysis, trend identification, and report generation. | Full access |
| **security-reviewer** | Reviews code and configurations for security vulnerabilities. Checks for hardcoded secrets, auth logic issues, dependency vulnerabilities, and OWASP patterns. | Read-only (no Write, Edit, Bash) |
| **compliance-summarizer** | Reviews work for compliance with organizational policies, regulations, and standards. Performs Definition of Done validation and audit trail verification. | Read-only (no Write, Edit, Bash) |
| **game-design-advisor** | Provides game design guidance, mechanics suggestions, and creative direction for game development projects. Specializes in Phaser/React Native games, gameplay balancing, and mobile optimization. | Full access |

### Design Team Agents (4)

All design team agents are read-only to ensure objective feedback without making changes.

| Agent | Purpose | What It Checks |
|-------|---------|----------------|
| **ui-reviewer** | Reviews UI implementations for visual consistency, layout quality, spacing, color usage, and component composition. | Layout & spacing (4px/8px grid), color usage (tokens vs hardcoded), typography hierarchy, component composition, visual hierarchy |
| **accessibility-checker** | Audits UI code for WCAG 2.1 AA compliance, screen reader compatibility, keyboard navigation, color contrast, and semantic HTML. | All WCAG 2.1 AA criteria: perceivable (alt text, contrast 4.5:1), operable (keyboard nav, focus order), understandable (labels, errors), robust (valid HTML, ARIA) |
| **design-system-enforcer** | Validates that implementations conform to design system tokens, component patterns, and naming conventions. Catches design drift before it ships. | Token usage (no hardcoded colors/spacing), component patterns (naming, props, variants), composition rules (className acceptance, margin-free layouts) |
| **visual-polish-auditor** | Final-pass review for visual polish and production readiness. Checks animations, transitions, loading states, empty states, error states, and micro-interactions. | Animations (150-300ms timing, reduced-motion), loading states (skeletons), empty states (CTAs), error states (inline messages), micro-interactions (hover, focus) |

---

## Skills (89 total)

Skills are specialized knowledge modules that activate based on context matching. They provide domain expertise, code patterns, and workflows.

### Claude Mastery Skills (34)

Core Claude Code capabilities: CLI, configuration, hooks, MCP, security, and learning resources.

| Skill | Purpose |
|-------|---------|
| **cli-mastery** | Keyboard shortcuts, slash commands, CLI flags, and power user workflow reference. Covers all keyboard shortcuts, permission modes, and terminal execution patterns. |
| **config-settings** | Claude Code configuration hierarchy guide. Covers Enterprise managed > Project local > Project > User settings, permission evaluation (deny > ask > allow), and settings.json structure. |
| **claude-md-optimization** | CLAUDE.md creation and optimization. Creates effective project instruction files, maintains configuration hierarchy, and avoids context bloat through modular imports. |
| **context-management** | Context window management and overflow prevention. Implements the Sawtooth compression pattern, manages handoff files, and uses `/compact` strategically. |
| **hooks-configuration** | Claude Code hooks creation and debugging. Configures PreToolUse, PostToolUse, Stop, SessionStart, UserPromptSubmit hooks. Exit code 2 = block. |
| **mcp-integration** | MCP (Model Context Protocol) server setup and debugging. Configures stdio and HTTP transports, manages user/project/managed settings hierarchy. |
| **skill-system-mastery** | Claude Code skill creation and optimization. Guides building effective SKILL.md files with proper YAML frontmatter and progressive disclosure. |
| **subagent-orchestration** | Multi-agent architecture patterns. Creates custom agents with YAML frontmatter, configures disallowedTools deny-lists, and orchestrates delegation. |
| **parallel-instances** | Multi-instance parallel Claude Code development. Orchestrates git worktrees, shared task lists, and fan-out patterns for running multiple Claude sessions. |
| **plan-and-think** | Plan Mode and Extended Thinking mastery. Plan Mode = double Shift+Tab or `/plan` (read-only exploration). Extended Thinking = single Tab (deep reasoning). Never confuse the two. |
| **verification-loops** | Quality assurance workflows. Implements TDD build-test-fix cycles, PostToolUse hooks for auto-linting, and Builder-Verifier patterns. |
| **security-hardening** | Security and permissions hardening. Configures permission hierarchies, deny/ask/allow rules, secret protection layers, and sandbox enforcement. |
| **headless-automation** | Claude Code headless mode and CI/CD integration. Covers `-p` flag for non-interactive execution, `--output-format stream-json`, GitHub Actions, and batch processing. |
| **chrome-workflows** | Chrome integration and browser-in-the-loop development. Enables visual build-verify loops with screenshots, native Chrome browsing via MCP. |
| **cursor-integration** | Hybrid workflow for Cursor IDE and Claude Code CLI. Optimizes context sharing, suggests tool selection (Micro vs Macro), and syncs configurations. |
| **troubleshooting-guide** | Diagnoses Claude Code errors and behavioral issues. Resolves MCP connection failures, permission denials, context rot, and hallucinations. |
| **changelog-navigator** | Evaluates new Claude Code features (2025-2026) for adoption. Checks version history, identifies breaking changes, and provides adoption guidance. |
| **community-navigation** | Guides to best Claude Code community resources. Compares Reddit vs Discord vs GitHub, lists notable power users, and provides etiquette guidelines. |
| **case-studies** | Real-world Claude Code success stories and workflow patterns. Provides proven "Transformation Patterns" for Product Managers, Creatives, and Developers. |
| **learning-path** | Structured progression guide from beginner to power user. Provides phase-by-phase milestones, practice exercises, and self-assessment checkpoints. |
| **learning-drill** | Generates focused practice exercises for building coding muscle memory. Uses spaced repetition for skill development. |
| **learning-accelerator** | Accelerates concept learning. Creates study plans, conducts Socratic concept drills, and converts markdown notes into Anki flashcards (CSV format). |
| **commit-checklist** | Validates commits against best practices before submission. Checks for secrets, formatting, and conventional commit patterns. |
| **safe-ops** | Ensures safe operations by checking for destructive actions and prompting for confirmation before risky commands. |
| **team-styleguide** | Enforces team coding standards and style guidelines in code reviews and edits. |
| **org-security** | Enforces organizational security policies and best practices in code and operations. |
| **org-definition-of-done** | Validates work against organizational Definition of Done criteria before marking complete. |
| **decision-doc** | Structured decision documentation. Captures context, options, and rationale so future-you understands past decisions. |
| **doc-workflows** | Documentation workflow automation. Generates READMEs, API docs, knowledge base articles, and maintains doc-as-code pipelines. |
| **git-github-workflows** | Git and GitHub workflow automation. Handles conventional commits, branch management (worktrees), PR creation, conflict resolution, and CI/CD pipelines. |
| **docker-devops** | Docker containerization and DevOps. Generates optimized multi-stage Dockerfiles, manages local development with docker-compose, and debugs container issues. |
| **prototype-scaffold** | Rapid project scaffolding for prototypes. Gets you coding in under 2 minutes with sensible defaults. |
| **python-automation** | Robust Python scripting. Generates scripts for file processing, resilient API clients, AI-powered web scraping, and scheduled tasks. |

### Product Management Skills (18)

PRDs, sprints, stakeholder communication, data analysis, and PM operations.

| Skill | Purpose |
|-------|---------|
| **prd-generator** | PRD and technical specification generator with interview-driven workflow. Asks clarifying questions before writing, produces engineering-ready specifications. |
| **quick-prd** | Rapid PRD generation with smart clarifying questions. Gets you from idea to spec in under 5 minutes. |
| **tech-spec** | Generates implementation-ready technical specifications. Bridges PM requirements and engineering execution with architecture diagrams and API contracts. |
| **sprint-roadmap** | Sprint planning and roadmap management. Handles capacity calculation, story point estimation, sprint goals, backlog grooming, and priority frameworks. |
| **stakeholder-update** | Stakeholder communication generator. Creates executive summaries, status reports, weekly updates, and cross-functional briefings. |
| **stakeholder-brief** | Creates one-page stakeholder updates optimized for busy executives. TL;DR first, details on demand. |
| **data-analysis** | Data analysis and reporting for product managers. Processes CSV and JSON files, generates metrics reports, identifies trends, and creates visualizations. |
| **meeting-prep** | Generates meeting agendas, pre-reads, and post-meeting action items. Optimized for async-first teams. |
| **ticket-batch** | Batch-create Jira/Linear tickets from PRDs, meeting notes, or brain dumps. Outputs copy-paste ready tickets. |
| **jira-automation** | Jira automation for Claude Code. Creates tickets from natural language, runs bulk operations, manages sprints, and executes JQL queries via MCP. |
| **research-synthesis** | User research synthesis. Analyzes interview transcripts, extracts themes, creates personas, maps user journeys, and generates research reports. |
| **api-product-management** | API product management for data API products. Generates OpenAPI/Swagger docs, endpoint specifications, SDK scaffolding, and versioning strategies. |
| **ai-native-products** | AI-native product development patterns. Covers prompt engineering workflows, evaluation frameworks, and building AI-powered features like chatbots and assistants. |
| **crypto-web3-context** | Crypto and Web3 product context for PMs. Provides blockchain terminology (DeFi, L1/L2, TVL, MEV, staking), market data concepts, and regulatory awareness. |
| **campus-education** | Education platform and LMS development patterns. Generates course structures, lesson outlines, quiz frameworks, and progress tracking for crypto education products. |
| **revops-adops-automation** | Revenue operations and ad operations automation. Generates pipeline reports, revenue forecasts, campaign audit checklists, and pricing models. |
| **knowledge-management** | Personal Knowledge Management (PKM) and Second Brain patterns. Organizes notes, synthesizes research from multiple sources, and links related concepts. |
| **keybindings-help** | Claude Code keyboard shortcut customization. Rebinds keys, adds chord bindings, and modifies `~/.claude/keybindings.json`. |

### Creative Studio Skills (15)

Phaser games, Remotion video, pixel art, animations, and creative AI tools.

| Skill | Purpose |
|-------|---------|
| **phaser-game-patterns** | Expert Phaser 3 game development for Game Boy-style 160x144 RPGs. Covers scene architecture, sprite management, input handling, and tile-based movement. |
| **phaser-pattern** | Phaser 3 game development patterns, code snippets, and architecture guidance for React Native integration. |
| **pixel-art-retro-style** | Enforces strict Game Boy retro aesthetic rules. Covers 4-color palette constraints, 8x8 grid alignment, dithering patterns, and character design. |
| **sprite-pipeline** | Automates sprite sheet generation, animation setup, and asset optimization for game development. |
| **sprite-asset-pipeline** | "Pixel Purity Pipeline" for game assets. Cleans AI-generated sprites, packs sprite sheets, and enforces strict naming conventions. |
| **2d-animation-principles** | 2D animation physics, timing, and production rules. Covers gravity spacing (Odd Rule), arcs, smear synthesis, and style mode switching. |
| **video-animation-production** | Video editing automation using FFmpeg and ImageMagick. Converts video formats, creates GIFs, burns subtitles, and generates asset files. |
| **ai-creative-tools** | Orchestrates advanced creative AI workflows using ComfyUI, ElevenLabs, and CLI integrations for generating AI art and audio. |
| **remotion-fundamentals** | Remotion project setup and core animation fundamentals. Creates video projects, registers Compositions, animates with useCurrentFrame and spring(). |
| **remotion-data-viz** | Data visualization animation patterns for Remotion. Builds animated bar charts, line charts with SVG path drawing, donut charts, and counter animations. |
| **remotion-transitions** | Scene transitions and multi-scene composition for Remotion. Uses @remotion/transitions with TransitionSeries and preset effects. |
| **remotion-typography** | Text and typography animation patterns for Remotion. Builds typewriter effects, character-by-character reveals, word stagger, and kinetic typography. |
| **remotion-social-output** | Social media format specifications for Remotion. Covers platform-specific dimensions (Instagram Reels, YouTube Shorts, TikTok) and rendering configuration. |
| **remotion-advanced** | Advanced Remotion patterns including audio-reactive video, 3D graphics with @remotion/three, and AI-generated media integration (ElevenLabs, images). |
| **remotion-troubleshooting** | Troubleshooting Remotion errors and performance optimization. Covers timeout debugging (delayRender), version compatibility, and asset path issues. |
| **remotion-claude-config** | CLAUDE.md configuration template and project conventions for Remotion. Provides ready-to-paste CLAUDE.md that enforces deterministic animations. |

### Design & UI Skills (8)

Design systems, Figma integration, animations, and visual polish.

| Skill | Purpose |
|-------|---------|
| **design-system-claude-md** | Design system encoding for CLAUDE.md. Creates and maintains design tokens, typography scales, spacing systems, and color palettes that Claude can reference. |
| **figma-to-code-workflow** | Figma-to-code conversion workflow using MCP servers. Extracts design tokens, maps Figma components to code, and maintains design fidelity. |
| **prompting-beautiful-ui** | Prompting strategies for generating polished UI. Covers spec-driven development workflow, visual description techniques, and iterative refinement. |
| **tailwind-advanced-patterns** | Advanced Tailwind CSS patterns for premium visual design. Covers gradient techniques (mesh, animated, text), glassmorphism, and layered shadow systems. |
| **animation-library-mastery** | Animation library selection for React web and React Native. Choose between Motion (Framer Motion), React Spring, GSAP, and Reanimated based on use case. |
| **micro-interaction-patterns** | Micro-interaction pattern library for UI polish. Copy-paste patterns for button feedback, form animations, navigation transitions, and scroll reveals. |
| **visual-polish-checklist** | Systematic visual quality checklist for reviewing generated UI. Covers shadow depth, gradient quality, typography refinements, and animation polish. |
| **react-native-animations** | React Native animation patterns with Reanimated 3 and Gesture Handler 2. Build native-feel interactions including draggables, bottom sheets, and spring physics. |

### Tech Stack Skills (8)

React, Supabase, Python, and development tools.

| Skill | Purpose |
|-------|---------|
| **react-vite-tailwind** | Modern frontend development. Generates React components with Tailwind utilities, sets up Vite projects, and implements state management patterns. |
| **rn-debug** | React Native debugging assistant. Diagnoses build failures, red screens, and performance issues systematically with platform-specific fixes. |
| **supabase-backend** | Supabase architecture patterns. Designs secure schemas with RLS policies, writes Deno Edge Functions, and optimizes real-time subscriptions. |
| **supabase-python** | Supabase integration in Python projects. Covers auth flows, database operations, real-time subscriptions, and storage management. |
| **python-automation** | Robust Python scripting. Generates file processing scripts, resilient API clients, AI-powered web scrapers, and scheduled task automation. |
| **docker-devops** | Docker containerization and DevOps. Generates optimized multi-stage Dockerfiles, manages docker-compose for local dev, and debugs container issues. |
| **git-github-workflows** | Git and GitHub workflow automation. Handles conventional commits, branch management, PR creation, conflict resolution, and CI/CD pipeline configuration. |
| **prototype-scaffold** | Rapid project scaffolding. Gets you coding in under 2 minutes with sensible defaults for various tech stacks. |

### Vault & Knowledge Skills (6)

Obsidian knowledge management, semantic search, and vault automation.

| Skill | Purpose |
|-------|---------|
| **vault-architecture** | AI-optimized Obsidian vault structure design. Creates folder hierarchies, YAML frontmatter schemas, and note templates that work for both humans and AI. |
| **vault-read-write** | Bidirectional Obsidian vault workflows. Query vault content, create structured notes, run daily note routines, and synthesize research from vault data. |
| **vault-automation** | Obsidian automation with Templater and Dataview. Creates smart note templates, builds AI processing queues, and automates repetitive vault tasks. |
| **knowledge-graph-nav** | Obsidian knowledge graph navigation for Claude Code. Traverses wiki-links, builds multi-hop context from linked notes, and discovers backlinks. |
| **obsidian-mcp-setup** | Obsidian MCP server installation and configuration. Connects Claude Code to an Obsidian vault via Model Context Protocol and diagnoses connection issues. |
| **obsidian-semantic-search** | Semantic search and embeddings setup for Obsidian vaults. Configures local vector databases, embedding models, and hybrid search pipelines. |

### Life Systems Skills (8)

Personal finance, health, tasks, time management, and life admin.

| Skill | Purpose |
|-------|---------|
| **personal-finance** | Personal finance automation. Imports CSV bank exports, categorizes transactions via regex, and generates monthly spending reports with trends. |
| **budget-entry** | Quick expense categorization and budget tracking. Paste receipts or transactions, get categorized entries ready for your budget system. |
| **health-habits** | Health and habit tracking. Logs workouts, calculates streaks from CSV data, and visualizes fitness progress over time. |
| **personal-task-management** | Personal Task Management and GTD assistant. Prioritizes tasks using Eisenhower/Socratic matrix, conducts weekly reviews, and organizes active projects. |
| **time-management** | Time management and calendar optimization. Audits calendar exports for fragmentation, facilitates daily planning (`/today`), and recommends time-boxing. |
| **life-admin** | Life Admin automation. Automates file organization (`/organize-inbox`), handles recurring admin tasks, and plans travel/events using comparison matrices. |
| **learning-accelerator** | Learning acceleration. Creates study plans, conducts Socratic concept drills, and converts markdown notes into Anki flashcards (CSV export). |
| **learning-drill** | Generates focused practice exercises for building coding muscle memory. Uses spaced repetition principles for skill development. |

---

## Quick Reference

### Agent Invocation
```
"Use checklist-validator to verify this PR meets the acceptance criteria"
"Act as Security Reviewer and audit this authentication code"
"Use ui-reviewer to review this component for visual consistency"
```

### Skill Activation
Skills activate automatically based on context matching. Mention keywords like:
- "PRD", "product requirements" → prd-generator, quick-prd
- "sprint", "roadmap" → sprint-roadmap
- "Phaser", "game", "sprite" → phaser-game-patterns, sprite-pipeline
- "Remotion", "video" → remotion-fundamentals
- "Obsidian", "vault" → vault-architecture, vault-read-write
- "Claude Code", "hooks", "MCP" → hooks-configuration, mcp-integration

### Design Team Review Flow
For UI work, invoke design team agents in this order:
1. **ui-reviewer** - Layout, spacing, color, typography
2. **accessibility-checker** - WCAG 2.1 AA compliance
3. **design-system-enforcer** - Token and pattern compliance
4. **visual-polish-auditor** - Final production-readiness check

---

*Generated from claude-code-superuser-pack v1.0*
