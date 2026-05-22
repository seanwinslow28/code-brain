---
type: research-report
date: 2026-05-21
question: "Topic 14 — Pi extensions / plugins catalog in 2026. Enumerate every Pi extension or plugin available on the official catalog (or community equivalent) as of 2026. Rank by relevance for a solo developer running a personal autonomous-agent fleet."
topic: 14
source: gemini-deep-research-manual
tier: dr
related_supersedes: "[[2026-05-21-topic-14-pi-extensions-plugins-catalog-in-2026-enumerate-eve]]"
tags: [research, deep-research, pi.dev, gemini-dr-manual]
---

# Pi (pi.dev) Extension Catalog — Solo Developer Evaluation Report

*Assessment date: 2026-05-21 · Target reader: solo dev, ~14 launchd SDK agents + 13 Claude Code subagents, Python + TypeScript, Obsidian vault, creative + PM workflows.*

***

## 1. Catalog Landscape

### What Pi Is

Pi is a minimal, open-source, terminal-based AI coding agent created by Mario Zechner and now developed under the **Earendil Works** organization. It went viral in early 2026 after Armin Ronacher (Flask/Jinja creator) wrote publicly about using it as his primary coding agent. The core philosophy is a four-tool harness (Read, Write, Edit, Bash) with a first-class extension system that allows the agent to extend itself by writing and hot-reloading TypeScript modules. As Ronacher put it: "Pi's entire idea is that if you want the agent to do something it doesn't do yet, you don't go and download an extension — you ask the agent to extend itself."[^1][^2][^3]

The npm package was migrated from `@mariozechner/pi-coding-agent` to `@earendil-works/pi-coding-agent` in May 2026. Version `0.73.1` was the last release under the old scope; `0.74.0+` publishes under `@earendil-works`. The Homebrew formula `pi-coding-agent` is MIT-licensed and currently tracks stable `0.75.3`.[^4][^3]

### Official Package Catalog

The canonical catalog lives at **[https://pi.dev/packages](https://pi.dev/packages)**. It is a gallery that auto-discovers npm packages tagged with the `pi-package` keyword — no manual curation or gating is required. Any npm package declaring a `pi` manifest key in `package.json` and tagging `"pi-package"` in keywords appears automatically. There is no formal review, no approval queue, and no separate submission form. The gallery sorts by monthly downloads and displays install commands, author, license, type badge (extension / skill / package / theme / prompt), and optional video/image previews.[^5][^6]

As of 2026-05-21, the **GitHub `pi-package` topic** lists **258 public repositories**, and the official catalog spans at least 3 pages with well over 100 entries. The ecosystem is younger than six months at scale — most entries were published between February and May 2026.[^7]

### Extension System Architecture

Extensions are TypeScript modules loaded via `jiti` (no pre-compilation needed) that can: register LLM-callable tools, intercept and modify tool calls/results, add `/slash` commands, render custom TUI widgets, store persistent session state, and inject context into every prompt. They load from `~/.pi/agent/extensions/` (global) or `.pi/extensions/` (project-local). Pi packages bundle extensions, skills, prompt templates, and themes and distribute them via npm or git.[^8][^6]

> **Security note from official docs:** "Pi packages run with full system access. Extensions execute arbitrary code, and skills can instruct the model to perform any action including running executables. Review source code before installing third-party packages."[^6]

***

## 2. Full Enumeration Table

The catalog has grown well beyond 50 entries; they are organized below by functional category. All licenses marked "MIT" have been confirmed from the pi.dev package page, npm, or GitHub. "Unknown" means the catalog page existed but license metadata was absent at time of access. Downloads are approximate monthly figures as of 2026-05-21.

### 2A. Context & Token Management

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `context-mode` | MCP plugin saving ~98% context via sandboxed execution + FTS5 knowledge base; works with Claude Code, Gemini CLI, Codex CLI | MIT[^9] | `pi install npm:context-mode` | 101,600[^5] | [npm](https://pi.dev/packages/context-mode) |
| `pi-lean-ctx` | Routes bash/read/grep through lean-ctx CLI for strong token savings; optional MCP bridge | MIT | `pi install npm:pi-lean-ctx` | 8,717[^5] | [npm](https://pi.dev/packages/pi-lean-ctx) |
| `pi-simplify` | Reviews recently changed code for clarity, consistency, and maintainability | MIT | `pi install npm:pi-simplify` | 21,000[^5] | [npm](https://pi.dev/packages/pi-simplify) |
| `@spences10/pi-context` | Searchable local SQLite sidecar that keeps oversized tool output useful without flooding model context | MIT | `pi install npm:@spences10/pi-context` | 2,956[^1] | [npm](https://pi.dev/packages/@spences10/pi-context) |
| `pi-caveman` | Cuts ~75% output tokens while keeping full technical accuracy ("caveman mode") | MIT | `pi install npm:pi-caveman` | 3,602[^1] | [npm](https://pi.dev/packages/pi-caveman) |
| `pi-context-prune` | Prunes future context while preserving original tool-call history | MIT | `pi install npm:pi-context-prune` | 3,103[^1] | [npm](https://pi.dev/packages/pi-context-prune) |
| `pi-memctx` | Automatic memory context injection via Markdown packs | MIT | `pi install npm:pi-memctx` | 4,150[^1] | [npm](https://pi.dev/packages/pi-memctx) |
| `pi-continue` | Mid-turn continuation for long tool runs; compacts safely before context overflow, then resumes from structured handoff ledger | MIT | `pi install npm:pi-continue` | 3,433[^1] | [npm](https://pi.dev/packages/pi-continue) |
| `pi-agentic-compaction` | *(see pi-rtk-optimizer below)* | — | — | — | — |
| `pi-rtk-optimizer` | Optimizes RTK command rewriting and tool output compaction | MIT | `pi install npm:pi-rtk-optimizer` | 3,632[^1] | [npm](https://pi.dev/packages/pi-rtk-optimizer) |
| `pi-tool-display` | Compact tool call rendering, diff visualization, output truncation | MIT | `pi install npm:pi-tool-display` | 3,636[^1] | [npm](https://pi.dev/packages/pi-tool-display) |

### 2B. Subagent & Multi-Agent Orchestration

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-subagents` | Delegate tasks to subagents with chains, parallel execution, and TUI clarification | MIT[^5] | `pi install npm:pi-subagents` | 94,000[^5] | [npm](https://pi.dev/packages/pi-subagents) |
| `@tintinweb/pi-subagents` | Claude Code-style autonomous sub-agents for pi | MIT | `pi install npm:@tintinweb/pi-subagents` | 14,100[^5] | [npm](https://pi.dev/packages/@tintinweb/pi-subagents) |
| `@gotgenes/pi-subagents` | Friendly fork of `@tintinweb/pi-subagents` | MIT | `pi install npm:@gotgenes/pi-subagents` | 3,160[^1] | [npm](https://pi.dev/packages/@gotgenes/pi-subagents) |
| `pi-crew` | Coordinated AI teams, workflows, worktrees, and async task orchestration | MIT | `pi install npm:pi-crew` | 9,381[^5] | [npm](https://pi.dev/packages/pi-crew) |
| `@tintinweb/pi-tasks` | Claude Code-style task tracking; 7 LLM-callable tools, dependency management, persistent widget, shared task lists for multi-agent coordination | MIT[^10] | `pi install npm:@tintinweb/pi-tasks` | 77★ GH[^7] | [npm](https://libraries.io/npm/@tintinweb%2Fpi-tasks) |
| `pi-multiagent` | Adds `agent_team` delegation tool and pi-multiagent skill | MIT | `pi install npm:pi-multiagent` | 4,012[^1] | [npm](https://pi.dev/packages/pi-multiagent) |
| `pi-fast-subagent` | In-process subagent delegation with single, parallel, and background modes | MIT | `pi install npm:pi-fast-subagent` | 2,268[^1] | [npm](https://pi.dev/packages/pi-fast-subagent) |
| `pi-agent-flow` | Flow-state transition extension for Pi coding agent | MIT | `pi install npm:pi-agent-flow` | 12,500[^5] | [npm](https://pi.dev/packages/pi-agent-flow) |
| `@juicesharp/rpiv-pi` | Five-skill development workflow (research, design, plan, implement, validate) with shared subagents composing a ship-loop | MIT | `pi install npm:@juicesharp/rpiv-pi` | 13,000[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-pi) |
| `@spences10/pi-team-mode` | Local team orchestration with RPC teammates, task tracking, and mailbox coordination | MIT | `pi install npm:@spences10/pi-team-mode` | 3,541[^1] | [npm](https://pi.dev/packages/@spences10/pi-team-mode) |
| `pi-interactive-shell` | Run AI coding agents in pi TUI overlays with interactive and hands-free supervision | MIT[^2] | `pi install npm:pi-interactive-shell` | 3,473[^1] | [npm](https://pi.dev/packages/pi-interactive-shell) |

### 2C. Memory & Persistent Knowledge

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `@samfp/pi-memory` | Persistent memory that learns corrections, preferences, and patterns across sessions | MIT | `pi install npm:@samfp/pi-memory` | 10,600[^5] | [npm](https://pi.dev/packages/@samfp/pi-memory) |
| `pi-hermes-memory` | Persistent memory + FTS5 session search + secret scanning; 368 tests; ported from Hermes agent | MIT | `pi install npm:pi-hermes-memory` | 8,778[^5] | [npm](https://pi.dev/packages/pi-hermes-memory) |
| `pi-memory-md` | Letta-like memory using structured Markdown files in a git repo | MIT | `pi install npm:pi-memory-md` | 3,026[^1] | [npm](https://pi.dev/packages/pi-memory-md) |
| `pi-observational-memory` | Cache-friendly tiered compaction with observations and reflections | MIT | `pi install npm:pi-observational-memory` | 2,561[^1] | [npm](https://pi.dev/packages/pi-observational-memory) |
| `@zosmaai/pi-llm-wiki` | Self-maintaining LLM wiki with immutable source capture, automated ingestion, search, linting, and Obsidian-compatible vault | MIT | `pi install npm:@zosmaai/pi-llm-wiki` | 2,714[^1] | [npm](https://pi.dev/packages/@zosmaai/pi-llm-wiki) |
| `@0xkobold/pi-codebase-wiki` | Keeps a self-updating wiki for your code from git history and docs | Unknown | `pi install npm:@0xkobold/pi-codebase-wiki` | 2,377[^1] | [npm](https://pi.dev/packages/@0xkobold/pi-codebase-wiki) |
| `pi-gitnexus` | GitNexus knowledge graph enriching every file read and symbol lookup with call chains and execution flows | MIT[^11] | `pi install npm:pi-gitnexus` | 128★ GH[^7] | [GitHub](https://github.com/tintinweb/pi-gitnexus) |

### 2D. Obsidian & Knowledge Management

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-obsidian` | 13-tool Obsidian integration: read/write/search notes, frontmatter, backlinks, tags, Kanban boards, project dashboards, Mermaid + Canvas, daily notes | MIT[^5] | `pi install npm:pi-obsidian` | 388[^5] | [pi.dev](https://pi.dev/packages/pi-obsidian) |
| `pi-obsidian-preview` | Opens last Pi response in Obsidian for Markdown/LaTeX/Mermaid/diff rendering; includes `visual-explain` skill | MIT[^5] | `pi install npm:pi-obsidian-preview` | ~500 est. | [pi.dev](https://pi.dev/packages/pi-obsidian-preview) |
| `Pi Agent` *(Obsidian plugin)* | Chat with Pi from Obsidian sidebar using context from current note, links, backlinks, tags; Chat/Review/Edit/Agent modes | MIT[^12] | Install via Obsidian Community Plugins browser | 45 installs[^12] | [Obsidian](https://community.obsidian.md/plugins/pi-agent) |

### 2E. Web Access & Research

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-web-access` | Web search, URL fetch, GitHub repo cloning, PDF extraction, YouTube video understanding, local video analysis | MIT | `pi install npm:pi-web-access` | 52,700[^5] | [npm](https://pi.dev/packages/pi-web-access) |
| `@juicesharp/rpiv-web-tools` | Web search/fetch with pluggable providers (Brave, Tavily, Serper, Exa, Jina, Firecrawl) | MIT | `pi install npm:@juicesharp/rpiv-web-tools` | 14,900[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-web-tools) |
| `@ollama/pi-web-search` | Web search/fetch via Ollama APIs | MIT | `pi install npm:@ollama/pi-web-search` | 24,900[^5] | [npm](https://pi.dev/packages/@ollama/pi-web-search) |
| `mavam/pi-web-providers` | Routes search/content/research across Claude, Codex, Exa, Gemini, Parallel, and Valyu providers | MIT | `pi install npm:mavam/pi-web-providers` | 66★ GH[^7] | [GitHub](https://github.com/mavam/pi-web-providers) |
| `@companion-ai/feynman` | Research-first CLI agent on Pi and alphaXiv | MIT | `pi install npm:@companion-ai/feynman` | 7,078[^5] | [npm](https://pi.dev/packages/@companion-ai/feynman) |
| `@narumitw/pi-firecrawl` | Exposes Firecrawl web scraping and crawling tools | MIT | `pi install npm:@narumitw/pi-firecrawl` | 2,999[^1] | [npm](https://pi.dev/packages/@narumitw/pi-firecrawl) |
| `@apmantza/greedysearch-pi` | Headless multi-engine AI search via browser automation — no API keys needed | MIT | `pi install npm:@apmantza/greedysearch-pi` | 3,040[^1] | [npm](https://pi.dev/packages/@apmantza/greedysearch-pi) |
| `@feniix/pi-exa` | Exa API extension for web search, content fetching, and advanced search | MIT | `pi install npm:@feniix/pi-exa` | 2,695[^1] | [npm](https://pi.dev/packages/@feniix/pi-exa) |

### 2F. MCP Adapters & Provider Integrations

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-mcp-adapter` | MCP (Model Context Protocol) adapter for Pi | MIT | `pi install npm:pi-mcp-adapter` | 83,900[^5] | [npm](https://pi.dev/packages/pi-mcp-adapter) |
| `@spences10/pi-mcp` | MCP server integration exposing configured MCP tools; manages large responses | MIT | `pi install npm:@spences10/pi-mcp` | 4,623[^1] | [npm](https://pi.dev/packages/@spences10/pi-mcp) |
| `pi-llama-cpp` | llama.cpp integration; supports router and single modes | MIT | `pi install npm:pi-llama-cpp` | 2,420[^1] | [npm](https://pi.dev/packages/pi-llama-cpp) |
| `pi-cursor-sdk` | Cursor SDK provider extension adding Cursor models to pi's model picker | MIT[^7] | `pi install npm:pi-cursor-sdk` | 31★ GH[^7] | [GitHub](https://github.com/fitchmultz/pi-cursor-sdk) |
| `pi-antigravity-rotator` | Multi-account rotation proxy for Google Antigravity with per-model routing and quota tracking | Unknown | `pi install npm:pi-antigravity-rotator` | 4,794[^1] | [npm](https://pi.dev/packages/pi-antigravity-rotator) |
| `pi-free` | AI model providers for Pi with free model filtering | MIT | `pi install npm:pi-free` | 2,773[^1] | [npm](https://pi.dev/packages/pi-free) |
| `pi-gemini-acp` | Gemini ACP chat, prompt, search, and research provider | MIT | `pi install npm:pi-gemini-acp` | 2,849[^1] | [npm](https://pi.dev/packages/pi-gemini-acp) |

### 2G. Safety, Permissions & Sandboxing

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-sandbox` *(carderne)* | OS-level sandboxing with interactive permission prompts; 96★ on GitHub | MIT[^13] | `pi install npm:pi-sandbox` | 96★ GH[^7] | [GitHub](https://github.com/carderne/pi-sandbox) |
| `pi-container-sandbox` | Runs read/write/edit/bash tools inside a Docker sandbox | MIT[^14] | `pi install npm:pi-container-sandbox` | 1,287[^14] | [pi.dev](https://pi.dev/packages/pi-container-sandbox) |
| `@nqbao/pi-sandbox` | OS-level sandbox using macOS `sandbox-exec` or Linux `bubblewrap` | MIT[^15] | `pi install npm:@nqbao/pi-sandbox` | 196[^15] | [pi.dev](https://pi.dev/packages/@nqbao/pi-sandbox) |
| `@kky42/pi-sandbox` | Filesystem-aware bash enforcement with read-only, workspace-write, and full-access modes | MIT[^16] | `pi install npm:@kky42/pi-sandbox` | 127[^16] | [pi.dev](https://pi.dev/packages/@kky42/pi-sandbox) |
| `@gotgenes/pi-permission-system` | Permission enforcement extension | MIT | `pi install npm:@gotgenes/pi-permission-system` | 11,800[^5] | [npm](https://pi.dev/packages/@gotgenes/pi-permission-system) |
| `pi-permission-system` | Permission enforcement extension (community fork) | MIT | `pi install npm:pi-permission-system` | 2,257[^1] | [npm](https://pi.dev/packages/pi-permission-system) |
| `pi-supervisor` | Supervises the coding agent and steers it toward a defined outcome; 48★ | MIT[^7] | `pi install npm:pi-supervisor` | 48★ GH[^7] | [GitHub](https://github.com/tintinweb/pi-supervisor) |
| `@juicesharp/rpiv-advisor` | Requests a second opinion from a stronger reviewer model before acting | MIT | `pi install npm:@juicesharp/rpiv-advisor` | 15,900[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-advisor) |
| `pi-guardrails` *(aliou)* | Guardrails enforcement extension | MIT | `pi install npm:@aliou/pi-guardrails` | 4,808[^1] | [npm](https://pi.dev/packages/@aliou/pi-guardrails) |

### 2H. Git, Code Review & CI

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-committer` | Conventional commit automation; auto-commits on goal completion, splits diffs into logical commits via subagent | MIT[^17] | `pi install npm:pi-committer` | 1,130[^17] | [pi.dev](https://pi.dev/packages/pi-committer) |
| `pi-lens` | Real-time LSP, linters, formatters, type-checking, structural analysis | MIT | `pi install npm:pi-lens` | 19,500[^5] | [npm](https://pi.dev/packages/pi-lens) |
| `@plannotator/pi-extension` | Interactive plan review with annotations; annotate agent messages, review code/PRs | MIT | `pi install npm:@plannotator/pi-extension` | 29,100[^5] | [npm](https://pi.dev/packages/@plannotator/pi-extension) |
| `@spences10/pi-lsp` | Language Server Protocol tools: diagnostics, hovers, definitions, references, symbols | MIT | `pi install npm:@spences10/pi-lsp` | 4,359[^1] | [npm](https://pi.dev/packages/@spences10/pi-lsp) |
| `pi-review-mode` | Opens a Glimpse native review window for commenting on a frozen Git diff | MIT[^8] | `pi install npm:pi-review-mode` | ~1,000 est. | [pi.dev](https://pi.dev/packages/pi-review-mode) |
| `pi-autoresearch` | Autonomous experiment loop: run, measure, keep or discard; inspired by karpathy/autoresearch | MIT | `pi install npm:pi-autoresearch` | 3,210[^1] | [npm](https://pi.dev/packages/pi-autoresearch) |
| `pi-hashline-readmap` | Hash-anchored read/edit/grep, structural code maps, AST-grep, bash output compression | MIT | `pi install npm:pi-hashline-readmap` | 2,390[^1] | [npm](https://pi.dev/packages/pi-hashline-readmap) |
| `@ff-labs/pi-fff` | FFF-powered fuzzy file and content search | MIT | `pi install npm:@ff-labs/pi-fff` | 7,617[^5] | [npm](https://pi.dev/packages/@ff-labs/pi-fff) |

### 2I. Scheduling, Automation & Workflow

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-schedule-prompt` | Schedule recurring and one-shot agent prompts with cron-like functionality; 59★ on GitHub | MIT[^7] | `pi install npm:pi-schedule-prompt` | 3,827[^1] | [GitHub](https://github.com/tintinweb/pi-schedule-prompt) |
| `pi-agent-browser-native` | Exposes agent-browser as a native tool for browser automation; 76★ on GitHub | MIT[^7] | `pi install npm:pi-agent-browser-native` | 76★ GH[^7] | [GitHub](https://github.com/fitchmultz/pi-agent-browser-native) |
| `pi-chrome` | Lets Pi use your existing signed-in Chrome profile for browser tasks | MIT | `pi install npm:pi-chrome` | 9,502[^5] | [npm](https://pi.dev/packages/pi-chrome) |
| `pi-codex-goal` | Codex-style goal tracking and continuation; 50★ on GitHub | MIT[^7] | `pi install npm:pi-codex-goal` | 50★ GH[^7] | [GitHub](https://github.com/fitchmultz/pi-codex-goal) |
| `@narumitw/pi-goal` | Extension that keeps working on a `/goal` until the agent marks it complete | MIT | `pi install npm:@narumitw/pi-goal` | 3,132[^1] | [npm](https://pi.dev/packages/@narumitw/pi-goal) |
| `@capyup/pi-goal` | Goal mode with persistent long-running objectives, Sisyphus prompt style, autoContinue | MIT | `pi install npm:@capyup/pi-goal` | 2,372[^1] | [npm](https://pi.dev/packages/@capyup/pi-goal) |
| `pi-interview` | Interactive interview form for structured project kickoffs | MIT | `pi install npm:pi-interview` | 3,393[^1] | [npm](https://pi.dev/packages/pi-interview) |
| `@juicesharp/rpiv-todo` | Todo list for the model, rendered as a live overlay that survives `/reload` and compaction | MIT | `pi install npm:@juicesharp/rpiv-todo` | 29,900[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-todo) |
| `@os-eco/mulch-cli` | Structured expertise files that accumulate over time, live in git, work with any agent | MIT | `pi install npm:@os-eco/mulch-cli` | 4,358[^1] | [npm](https://pi.dev/packages/@os-eco/mulch-cli) |
| `pi-gsd` | "Get Shit Done" spec-driven development port | MIT | `pi install npm:pi-gsd` | 2,503[^1] | [npm](https://pi.dev/packages/pi-gsd) |
| `gentle-pi` | Senior-architect harness with SDD/OpenSpec, subagents, strict TDD, review guardrails, skill discovery | MIT | `pi install npm:gentle-pi` | 7,634[^5] | [npm](https://pi.dev/packages/gentle-pi) |
| `@runfusion/fusion` | HTTP API server, daemon, dashboard launcher, and task tooling | MIT | `pi install npm:@runfusion/fusion` | 12,000[^5] | [npm](https://pi.dev/packages/@runfusion/fusion) |
| `@linimin/pi-letscook` | Long-running completion workflows with canonical `.agent` state, role-based subagents | MIT | `pi install npm:@linimin/pi-letscook` | 4,206[^1] | [npm](https://pi.dev/packages/@linimin/pi-letscook) |

### 2J. UI, Themes & Observability

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-observability` | Live footer bar (tokens, cost, TPS, runtime, model, git stats, context usage) + `/obs` full-screen dashboard | MIT[^18] | `pi install npm:pi-observability` | ~5,000 est.[^18] | [libraries.io](https://libraries.io/npm/pi-observability) |
| `pi-cost` | Cost dashboard: overview → project → session → message with actual + estimated spend | MIT[^19] | `pi install npm:pi-cost` | ~500 est.[^19] | [pi.dev](https://pi.dev/packages/pi-cost) |
| `pi-powerline-footer` | Powerline-style status bar | MIT | `pi install npm:pi-powerline-footer` | 14,800[^5] | [npm](https://pi.dev/packages/pi-powerline-footer) |
| `pi-inspect` | Introspection dashboard: tools, prompts, skills, and the injected system prompt; 30★ | MIT[^7] | `pi install npm:pi-inspect` | 30★ GH[^7] | [GitHub](https://github.com/NikiforovAll/pi-inspect) |
| `pi-agent-dashboard` *(BlackBeltTechnology)* | Real-time multi-session browser dashboard: live chat mirroring, integrated terminal, diff viewer | MIT[^20] | `pi install npm:pi-agent-dashboard` | — | [GitHub](https://github.com/BlackBeltTechnology/pi-agent-dashboard) |
| `pi-studio` | Two-pane browser workspace with prompt/response editing, annotations, quiz, literate REPL | MIT | `pi install npm:pi-studio` | 9,111[^5] | [npm](https://pi.dev/packages/pi-studio) |
| `pi-markdown-preview` | Rendered Markdown + LaTeX preview in terminal, browser, or PDF | MIT | `pi install npm:pi-markdown-preview` | 11,300[^5] | [npm](https://pi.dev/packages/pi-markdown-preview) |
| `pi-mermaid` | Renders Mermaid diagrams as ASCII in the TUI | MIT | `pi install npm:pi-mermaid` | 3,120[^1] | [npm](https://pi.dev/packages/pi-mermaid) |
| `@ifi/oh-pi-themes` | Color themes: cyberpunk, nord, gruvbox, tokyo-night, catppuccin, and more | MIT | `pi install npm:@ifi/oh-pi-themes` | 3,127[^1] | [npm](https://pi.dev/packages/@ifi/oh-pi-themes) |
| `pi-code-previews` | Syntax-highlighted previews for pi tool calls | MIT | `pi install npm:pi-code-previews` | 2,692[^1] | [npm](https://pi.dev/packages/pi-code-previews) |
| `pi-claude-style-tools` | Claude Code-style tool rows with Ctrl+O image previews | MIT | `pi install npm:pi-claude-style-tools` | 2,807[^1] | [npm](https://pi.dev/packages/pi-claude-style-tools) |
| `pi-bar` | Footer/statusline: active model, thinking level, context pressure, progress, extension statuses | MIT | `pi install npm:pi-bar` | 4,353[^1] | [npm](https://pi.dev/packages/pi-bar) |
| `glimpseui` | Native micro-UI for scripts and agents — cross-platform WebView windows with bidirectional JSON | MIT | `pi install npm:glimpseui` | 10,500[^5] | [npm](https://pi.dev/packages/glimpseui) |
| `@spences10/pi-telemetry` | Local SQLite telemetry for runs, turns, tool calls, provider requests, usage, and latency | MIT | `pi install npm:@spences10/pi-telemetry` | 2,791[^1] | [npm](https://pi.dev/packages/@spences10/pi-telemetry) |

### 2K. User Interaction & Input

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `@juicesharp/rpiv-ask-user-question` | Structured questionnaire with typed options the model invokes instead of guessing | MIT | `pi install npm:@juicesharp/rpiv-ask-user-question` | 33,100[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-ask-user-question) |
| `pi-ask-user` | Interactive ask_user tool with searchable split-pane selection UI and multi-select | MIT | `pi install npm:pi-ask-user` | 9,864[^5] | [npm](https://pi.dev/packages/pi-ask-user) |
| `@juicesharp/rpiv-btw` | `/btw` slash command for side questions without polluting the main conversation | MIT | `pi install npm:@juicesharp/rpiv-btw` | 14,500[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-btw) |
| `pi-btw` | `/btw` parallel side conversations (community alternative) | MIT | `pi install npm:pi-btw` | 9,524[^5] | [npm](https://pi.dev/packages/pi-btw) |
| `@juicesharp/rpiv-args` | Shell-style `$1/$ARGUMENTS` placeholders and `!cmd` shell substitution expanded into skills | MIT | `pi install npm:@juicesharp/rpiv-args` | 13,500[^5] | [npm](https://pi.dev/packages/@juicesharp/rpiv-args) |
| `pi-listen` / `codexstar69/pi-listen` | Hold-to-talk voice input via Deepgram streaming STT; 61★ on GitHub | MIT[^7] | `pi install npm:pi-listen` | 61★ GH[^7] | [GitHub](https://github.com/codexstar69/pi-listen) |
| `@codexstar/pi-listen` | Voice in + out: hold-to-talk STT (Deepgram or 19 offline models) + TTS (Kitten Nano, Piper, Kokoro) | MIT | `pi install npm:@codexstar/pi-listen` | 2,263[^1] | [npm](https://pi.dev/packages/@codexstar/pi-listen) |
| `@juicesharp/rpiv-voice` | Voice dictation via `/voice` — local on-device STT with sherpa-onnx Whisper | MIT | `pi install npm:@juicesharp/rpiv-voice` | 2,639[^1] | [npm](https://pi.dev/packages/@juicesharp/rpiv-voice) |
| `@arcanemachine/pi-notify-marker` | Creates marker files on Pi events for external monitoring/notification scripts | MIT[^21] | `pi install git:github.com/arcanemachine/pi-notify-marker` | — | [GitHub](https://pi.dev/packages/@arcanemachine/pi-notify-marker) |
| `@juicesharp/rpiv-warp` | Native Warp terminal notifications via OSC 777 on Pi lifecycle events | MIT | `pi install npm:@juicesharp/rpiv-warp` | 3,153[^1] | [npm](https://pi.dev/packages/@juicesharp/rpiv-warp) |

### 2L. Visualization & Diagramming

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-k-excalidraw` | Native Excalidraw diagram preview via glimpse webview; 62★ on GitHub | MIT[^7] | `pi install npm:pi-k-excalidraw` | 62★ GH[^7] | [GitHub](https://github.com/kostyay/pi-k-excalidraw) |
| `@darkhorseprojects/pi-circuitry` | Agentic workflows on Excalidraw | MIT | `pi install npm:@darkhorseprojects/pi-circuitry` | 3,307[^1] | [npm](https://pi.dev/packages/@darkhorseprojects/pi-circuitry) |

### 2M. Mobile, Remote & Messaging

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `@llblab/pi-telegram` | Telegram runtime adapter for Pi | MIT | `pi install npm:@llblab/pi-telegram` | 7,653[^5] | [npm](https://pi.dev/packages/@llblab/pi-telegram) |
| `pi-messenger-bridge` *(tintinweb)* | Bridge for Telegram, WhatsApp, Slack, Discord; 41★ | MIT[^7] | `pi install npm:pi-messenger-bridge` | 41★ GH[^7] | [GitHub](https://github.com/tintinweb/pi-messenger-bridge) |
| `whatsapp-pi` | WhatsApp integration extension | MIT | `pi install npm:whatsapp-pi` | 3,553[^1] | [npm](https://pi.dev/packages/whatsapp-pi) |
| `pi-phone` | Phone-first remote UI: drives a real Pi session from a mobile web app via WebSocket; 48★ | MIT[^7] | `pi install npm:pi-phone` | 48★ GH[^7] | [GitHub](https://github.com/MaliNamNam/pi-phone) |
| `@jmfederico/pi-web` | Run Pi agents on your own machine/server with browser-based control | MIT[^22] | `pi install npm:@jmfederico/pi-web` | ~1,500 est. | [pi.dev](https://pi.dev/packages/@jmfederico/pi-web) |

### 2N. Document Processing & Spec Tooling

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-docparser` | Parses PDFs, Office documents, spreadsheets, and images with LiteParse | MIT | `pi install npm:pi-docparser` | 4,518[^1] | [npm](https://pi.dev/packages/pi-docparser) |
| `@feniix/pi-specdocs` | Structured spec documentation — PRDs, ADRs, and implementation plans with cross-referencing | MIT | `pi install npm:@feniix/pi-specdocs` | 2,652[^1] | [npm](https://pi.dev/packages/@feniix/pi-specdocs) |
| `pi-intercom` | *(inter-agent communication, details not fully public)* | MIT | `pi install npm:pi-intercom` | 6,957[^5] | [npm](https://pi.dev/packages/pi-intercom) |
| `agent-comms` | Cross-harness communication mesh: rooms, DMs, presence, real-time push over TCP | MIT | `pi install npm:agent-comms` | 3,376[^1] | [npm](https://pi.dev/packages/agent-comms) |

### 2O. Other / Miscellaneous

| Name | Purpose | License | Install Command | ~Downloads/mo | Source URL |
|---|---|---|---|---|---|
| `pi-convex` | Convex Cloud integration: queries, mutations, project management, best practices | MIT | `pi install npm:pi-convex` | 4,781[^1] | [npm](https://pi.dev/packages/pi-convex) |
| `ultimate-pi` | All-in-one harness: extensible skills, Obsidian knowledge layer, compressed context | MIT | `pi install npm:ultimate-pi` | 4,577[^1] | [npm](https://pi.dev/packages/ultimate-pi) |
| `pi-nvim` *(carderne)* | Bridge between pi and Neovim; 36★ | MIT[^7] | `pi install git:github.com/carderne/pi-nvim` | 36★ GH[^7] | [GitHub](https://github.com/carderne/pi-nvim) |
| `pi-tools` *(joelhooks)* | Power tools: repo autopsy, tsgo LSP, codex background loops, session reader; 64★ | MIT[^7] | `pi install npm:pi-tools` | 64★ GH[^7] | [GitHub](https://github.com/joelhooks/pi-tools) |
| `pi-sandbox` *(dot314)* | Extensions collection from w-winter; 109★ | MIT[^7] | `pi install git:github.com/w-winter/dot314` | 109★ GH[^7] | [GitHub](https://github.com/w-winter/dot314) |
| `@posthog/pi` | PostHog LLM Analytics for pi sessions | MIT | `pi install npm:@posthog/pi` | 2,544[^1] | [npm](https://pi.dev/packages/@posthog/pi) |
| `@howaboua/pi-codex-conversion` | Codex-oriented tool and prompt adapter | MIT | `pi install npm:@howaboua/pi-codex-conversion` | 8,393[^5] | [npm](https://pi.dev/packages/@howaboua/pi-codex-conversion) |
| `@narumitw/pi-retry` | Retries empty-detail provider unknown errors | MIT | `pi install npm:@narumitw/pi-retry` | 3,049[^1] | [npm](https://pi.dev/packages/@narumitw/pi-retry) |
| `pi-qmd-ledger` | Universal JSONL ledger with qmd hybrid search, tiered HITL, and dynamic context injection | MIT | `pi install npm:pi-qmd-ledger` | 3,032[^1] | [npm](https://pi.dev/packages/pi-qmd-ledger) |
| `@spences10/pi-skills` | Agent Skills management with profiles, enablement rules, GitHub search/install, and update flows | MIT | `pi install npm:@spences10/pi-skills` | 3,595[^1] | [npm](https://pi.dev/packages/@spences10/pi-skills) |

***

## 3. Top-10 Ranked for Sean's Stack

*Ranking criteria: directly addresses one or more of (a) multi-agent fleet management, (b) Obsidian vault integration, (c) token efficiency across 27 concurrent agents, (d) Python+TS codebase quality, (e) creative/PM workflow support.*

***

### #1 — `pi-obsidian`

**What it does:** Registers 13 tools that give Pi full read/write/search access to your Obsidian vault, including YAML frontmatter parsing, backlink traversal, tag analysis, Mermaid diagram creation, Obsidian Canvas generation, Kanban boards, project dashboards with Dataview queries, and three daily-note templates.[^5]

**Why it ranks first for Sean:** The Obsidian vault is the connective tissue across 16BitFit game design, The Block research, and PM operations. This extension lets every Pi session — and by extension any subagent — read and write directly into the vault without manual copy-paste. The `obsidian_create_project_dashboard` tool alone can auto-generate Gantt charts for sprint planning. It's the only extension providing native bidirectional vault access rather than just preview rendering.

**Install:**
```
pi install npm:pi-obsidian
```

**Integration notes:** Run pi from the vault root for per-project install (`cd ~/your-vault && pi install -l npm:pi-obsidian`). For global use across all projects, add `PI_OBSIDIAN_VAULT_PATH` to `~/.zshrc`. Your launchd agents can invoke Obsidian tools via the `pi --mode rpc` flag if you expose an RPC endpoint from each agent. Pair with `pi-obsidian-preview` (below) to close the write→render loop.[^5]

***

### #2 — `@tintinweb/pi-tasks`

**What it does:** Claude Code-style task tracking with 7 LLM-callable tools (`TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`, `TaskOutput`, `TaskStop`, `TaskExecute`), dependency management, a persistent visual widget, and shared file-backed task lists that multiple pi sessions can read simultaneously.[^10]

**Why it ranks here:** Managing 27 concurrent agents (14 launchd + 13 Claude Code subagents) without a shared task bus is the biggest coordination risk in the stack. `@tintinweb/pi-tasks` provides exactly that — a file-backed DAG that multiple pi sessions can read and write, with `TaskExecute` spawning tasks as subagents when `agentType` is set. The auto-cascade mode can flow through the entire task DAG without manual steering.[^10]

**Install:**
```
pi install npm:@tintinweb/pi-tasks
```

**Integration notes:** The shared task list requires all agent sessions to point at the same file path — set `taskListPath` in each agent's project settings. Combine with `@tintinweb/pi-subagents` (below) for the full orchestration layer. If a launchd agent writes a task, a Claude Code subagent can pick it up by reading the same file.

***

### #3 — `context-mode`

**What it does:** An MCP plugin that reduces context consumption by ~98% through sandboxed code execution (10 language runtimes), FTS5 knowledge base with BM25 ranking, intent-driven search, and batch execution. A 315 KB tool result becomes ~5.4 KB in context. Session time before slowdown goes from ~30 min to ~3 hours.[^9][^23]

**Why it ranks here:** With 27 agents running simultaneously, context window efficiency is the single largest operational cost driver. `context-mode` works as an extension hook in Pi — registering `tool_call` and `tool_result` interceptors — so it applies to every agent automatically when installed globally. For Python codebases especially, where test output and linter results can balloon, the FTS5 search approach lets agents query results without dumping raw stdout.[^9]

**Install:**
```
pi install npm:context-mode
```

**Integration notes:** Install globally (`~/.pi/agent/`) so all launchd agents pick it up. The SQLite database is session-scoped (ephemeral per run). For Python agents, the `execute` tool's sandboxed subprocess isolation also prevents memory leaks from bleeding across agent sessions.[^23]

***

### #4 — `pi-subagents` (nicopreme) + `@tintinweb/pi-subagents`

**What they do:** `pi-subagents` (nicopreme, 94K/mo) adds chains, parallel execution, and TUI clarification for subagent delegation. `@tintinweb/pi-subagents` adds Claude Code-style autonomous sub-agents.[^10][^5]

**Why they rank here:** These two are the foundation of Pi's multi-agent architecture. Because you're already running Claude Code subagents separately, the Pi subagent layer needs to complement, not duplicate, them. The nicopreme variant's parallel execution mode is the right fit for the creative + PM workload where tasks are independent (e.g., "draft release notes," "check analytics," "update Obsidian sprint board"). `@tintinweb/pi-subagents` is preferred if you need `TaskExecute` integration with `pi-tasks`.

**Install:**
```
pi install npm:pi-subagents          # for parallel/chains
pi install npm:@tintinweb/pi-subagents  # for Claude Code parity
```

**Integration notes:** Both extensions call `createAgentSession` from the Pi SDK internals. Your launchd agents should use the nicopreme variant for orchestration; Claude Code subagents operate independently and don't need this installed.

***

### #5 — `pi-schedule-prompt`

**What it does:** Schedules recurring and one-shot agent prompts with cron-like functionality. Fires prompts at defined intervals or times into a running or dormant Pi session.[^7]

**Why it ranks here:** You're already using launchd for agent scheduling on macOS. `pi-schedule-prompt` (59★ GitHub) complements this by allowing in-session recurring prompts — e.g., "every 30 minutes, summarize new Obsidian notes tagged `#inbox` and move them to the daily note." This avoids spinning up a new launchd job for every scheduled task and keeps the work inside the Pi session tree where it can access context.

**Install:**
```
pi install npm:pi-schedule-prompt
```

**Integration notes:** Works best for prompts that need access to the current session's context history. For fully autonomous background tasks, launchd remains better; use `pi-schedule-prompt` for in-session cadenced work like daily note synthesis or stand-up generation.

***

### #6 — `pi-obsidian-preview`

**What it does:** Opens the last Pi assistant response in Obsidian for full rendering — Markdown, LaTeX, Mermaid diagrams, callouts, code blocks, and diffs. Includes a `visual-explain` skill that instructs the agent to produce Mermaid/LaTeX-rich explanations.[^5]

**Why it ranks here:** For PM and creative work, rich rendered output matters. When an agent produces an architecture diagram or sprint plan, you want to see it rendered, not as raw Markdown in a terminal. Pairs directly with `pi-obsidian` — the write-tool creates the note, preview opens it instantly.

**Install:**
```bash
export PI_OBSIDIAN_VAULT_PATH="$HOME/your-vault"  # add to ~/.zshrc
pi install npm:pi-obsidian-preview
```

Then trigger with `/preview` in Pi, or `Ctrl+Shift+B`.

**Integration notes:** Requires `obsidian` CLI on PATH (`brew install obsidian`). When running pi from the vault root, use the per-project install with `-l` flag to avoid global side effects on agents where Obsidian isn't available.

***

### #7 — `pi-committer`

**What it does:** Conventional commit automation that auto-commits when a goal completes, splits diffs into logical commit groups via a subagent, generates messages from the diff, works across multi-repo sessions.[^17]

**Why it ranks here:** With 13 Claude Code subagents and 14 launchd agents all potentially touching the same repos, commit hygiene becomes critical. `pi-committer`'s `on_goal` trigger mode integrates with `pi-tasks` goal lifecycle — a task completing auto-commits the associated work. The multi-repo detection (via session tool-call history) is particularly valuable when agents span multiple projects simultaneously.

**Install:**
```
pi install npm:pi-committer
```

**Configuration** (`.pi-committer.toml` in project root):
```toml
[committer]
enabled = true
trigger_mode = "on_goal"
detailed_body = true
staged_commits = true
```

**Integration notes:** Set `subagent_model = "openai/gpt-4o-mini"` to save costs on commit-message generation. Exclusion patterns should include `.obsidian/workspace.json` and vault cache directories to prevent Obsidian churn from triggering spurious commits.[^17]

***

### #8 — `pi-agent-dashboard` (BlackBeltTechnology)

**What it does:** Real-time browser dashboard for multi-session pi management — spawns parallel sessions, shows live reasoning, mirrors chat, provides integrated terminal, diff viewer, and pi-flows execution. Tagline: "One browser tab to command an army of pi agents."[^20]

**Why it ranks here:** Your fleet of 14+13 agents is exactly the target use case. This dashboard gives you a unified control plane without having to tab-switch across 27 terminal sessions. The "spawn parallel sessions" feature is the key differentiator — you can launch, monitor, and steer all sessions from a single browser interface.

**Install:**
```
pi install npm:pi-agent-dashboard
```

*(See [blackbelttechnology.github.io/pi-agent-dashboard](https://blackbelttechnology.github.io/pi-agent-dashboard) for the animated tour and full install guide.)*

**Integration notes:** The dashboard uses `pi --mode rpc` subprocess architecture. Works on macOS and is accessible from phone (useful for monitoring agents while away from desk — complements `pi-phone` if you want mobile control).[^20]

***

### #9 — `pi-mcp-adapter`

**What it does:** MCP (Model Context Protocol) adapter that makes Pi-native extensions available as MCP tools and vice versa, bridging the Pi extension ecosystem with the broader MCP server ecosystem.[^5]

**Why it ranks here:** Your stack heavily uses Claude Code with MCP servers (Zapier, etc.). This adapter is the bridge that lets Pi agents consume existing MCP servers without rewriting them as Pi extensions. It's the highest-leverage interoperability layer for a mixed-harness fleet.

**Install:**
```
pi install npm:pi-mcp-adapter
```

**Integration notes:** Pairs with `@spences10/pi-mcp` for managing large responses from MCP tools. Configure in `~/.pi/agent/settings.json` so all global agents inherit MCP connectivity. Armin Ronacher specifically called out that Pi has no native MCP support by design — this adapter is the pragmatic bridge when you need both ecosystems.[^2][^1]

***

### #10 — `pi-observability`

**What it does:** Replaces the default footer with a live observability bar showing session tokens, estimated cost, live TPS, runtime, model, thinking level, git stats, and context usage. The `/obs` command opens a full-screen TUI dashboard with per-turn breakdowns and last 10 session history.[^18]

**Why it ranks here:** Cost and context pressure visibility across 27 agents isn't optional at scale. Without this, you're flying blind on which agents are burning budget and which are approaching context limits. The per-turn breakdown is critical for debugging runaway agents in your launchd fleet.

**Install:**
```
pi install npm:pi-observability
# or
pi install git:github.com/imran-vz/pi-observability
```

**Integration notes:** `/obs-toggle` lets you suppress the footer when you need a clean terminal for demo/recording work. The standalone `tps.ts` extension should be removed if previously installed — `pi-observability` now includes TPS notification to avoid duplicates.[^18]

***

## 4. Notable Gaps

**No native Obsidian bidirectional sync.** `pi-obsidian` writes notes and reads them, but there is no extension that watches the vault for changes and pushes them back into Pi's context in real time. Closest analogs: `pi-memctx` (markdown packs) and `@zosmaai/pi-llm-wiki` (Obsidian-compatible vault with automated ingestion), but neither provides live vault→agent push. A launchd watcher + Pi RPC call would need to be custom-built.[^1][^5]

**No launchd-native agent lifecycle manager.** There is no extension for managing macOS launchd `.plist` generation, agent health monitoring, or automatic restarts directly from Pi. `pi-schedule-prompt` handles in-session scheduling; `pi-agent-dashboard` handles browser-based multi-session control; but the gap between "running Pi session" and "persistent macOS service" remains manual.[^7]

**No cross-agent shared memory with vector search (production-ready).** `pi-hermes-memory` and `@pi-unipi/memory` provide per-session memory with FTS5 and vector search respectively, but neither has a well-documented multi-agent concurrent write model. For 27 agents sharing knowledge, SQLite's write locking will cause contention. No extension currently addresses a distributed memory bus (e.g., Redis-backed or S3-backed).[^1][^5]

**No TypeScript/Python polyglot project template.** For mixed-language codebases, there is no extension that scaffolds or enforces a consistent project structure across Python (uv, pytest) and TypeScript (pnpm, vitest) simultaneously. `gentle-pi` and `pi-gsd` target TypeScript/OpenSpec workflows. Python-first workflows lack an equivalent.[^5]

**No Zapier/n8n integration.** Your existing Zapier-based automation stack has no native Pi bridge. `pi-mcp-adapter` provides generic MCP connectivity, but there is no dedicated Zapier Pi extension that exposes webhook triggers or Zap execution as Pi tools. This would need to be custom-built, likely as a thin extension wrapping Zapier's REST API.

**No Jira/Linear integration.** Despite rich PM workflow tooling, no extension bridges Pi directly to Jira for reading/writing tickets. The `agent-comms` cross-harness mesh and `@spences10/pi-team-mode` handle inter-agent coordination, but external PM tool sync is absent.[^1]

**No built-in secret/credential rotation for agent fleet.** `pi-hermes-memory` includes secret scanning, but there is no extension for rotating API keys across a fleet of agents when credentials change — a real operational risk at 27-agent scale.[^5]

***

## 5. Risk Flags

### `pi-antigravity-rotator`
**Flag: Unknown license, privacy/ToS risk.** This extension provides multi-account rotation proxying for Google Antigravity (Google's AI API). No license is declared on the pi.dev catalog page. Multi-account rotation may violate Google's terms of service for AI API usage. Downloads (4,794/mo) suggest significant adoption despite no license transparency. **Recommendation: Avoid until license is clarified and ToS compliance verified.**[^1]

### `@posthog/pi`
**Flag: Telemetry by design.** This extension sends Pi session analytics to PostHog's cloud service. While PostHog is a legitimate, well-known analytics platform, this means agent turn data, tool call metadata, and potentially code snippets transit to a third-party server. If any agents process proprietary The Block research or 16BitFit game mechanics, this is a data leakage risk. **Recommendation: Only install in sandboxed/personal contexts, never in work agents.**[^1]

### `@0xkobold/pi-codebase-wiki`
**Flag: Unknown license.** The pi.dev page does not list a license for this extension. Given it reads your entire git history and codebase to build a wiki, the absence of a license is a material concern. No GitHub stars data was recoverable. **Recommendation: Inspect source before installing; do not use on proprietary repos until license is confirmed.**[^1]

### Single-maintainer risk across `juicesharp/rpiv-*` suite
**Note, not a hard flag:** The `rpiv-*` family (`rpiv-ask-user-question`, `rpiv-todo`, `rpiv-advisor`, `rpiv-web-tools`, `rpiv-btw`, `rpiv-args`, `rpiv-pi`, `rpiv-i18n`, `rpiv-warp`, `rpiv-voice`) are all published by a single author (`juicesharp`) with no disclosed backup maintainer. Combined, these account for ~143K monthly downloads. The extensions are actively maintained (all show "3h ago" updates as of 2026-05-21), but a single-maintainer bus factor exists. The `rpiv-i18n` package is a required dependency for the rest of the rpiv suite, so a single unpublish event would cascade. **Recommendation: Pin to specific versions; maintain local copies of any rpiv extensions you depend on.**[^5]

### `pi-json-tools`
**Flag: Narrow/unusual scope.** This extension is described as "Smart Recovery for Qwen Coder - Auto hallucination detection for qwen2.5-coder family." It is designed for a specific model family and may produce undefined behavior with Claude or GPT-4o. The description does not match the package name (`pi-json-tools`), suggesting the description may be inaccurate or the package was repurposed. **Recommendation: Skip unless running Qwen models.**[^1]

### `pi-agent-dashboard` (BlackBeltTechnology)
**Note: Relatively recent, corporate GitHub org, no npm listing found.** The dashboard is hosted under the `BlackBeltTechnology` GitHub organization (a Hungarian enterprise software company). The CHANGELOG is active, and the project has a dedicated website. However, there is no npm listing confirmed — install may require a git source. Review the CHANGELOG and issue tracker before deploying in a multi-agent production fleet.[^24][^25][^20]

***

## 6. Sources

| URL | Access Date | Notes |
|---|---|---|
| [https://pi.dev/packages](https://pi.dev/packages) | 2026-05-21 | Official package catalog, pages 1–3[^5][^1] |
| [https://pi.dev/docs/latest/extensions](https://pi.dev/docs/latest/extensions) | 2026-05-21 | Official extension API documentation[^8] |
| [https://pi.dev/docs/latest/packages](https://pi.dev/docs/latest/packages) | 2026-05-21 | Official packaging and submission documentation[^6] |
| [https://pi.dev/packages/pi-obsidian](https://pi.dev/packages/pi-obsidian) | 2026-05-21 | pi-obsidian full page with tool table[^5] |
| [https://pi.dev/packages/pi-obsidian-preview](https://pi.dev/packages/pi-obsidian-preview) | 2026-05-21 | pi-obsidian-preview full page[^5] |
| [https://pi.dev/packages/pi-committer](https://pi.dev/packages/pi-committer) | 2026-05-21 | pi-committer full page with config reference[^17] |
| [https://pi.dev/packages/pi-cost](https://pi.dev/packages/pi-cost) | 2026-05-21 | pi-cost page[^19] |
| [https://pi.dev/news/2026/5/7/pi-has-a-new-home](https://pi.dev/news/2026/5/7/pi-has-a-new-home) | 2026-05-21 | Official Pi → Earendil Works migration announcement[^3] |
| [https://github.com/topics/pi-package](https://github.com/topics/pi-package) | 2026-05-21 | GitHub topic page; 258 repos, sorted by stars[^7] |
| [https://community.obsidian.md/plugins/pi-agent](https://community.obsidian.md/plugins/pi-agent) | 2026-05-21 | Obsidian community Pi Agent plugin page[^12] |
| [https://libraries.io/npm/pi-observability](https://libraries.io/npm/pi-observability) | 2026-05-21 | pi-observability npm metadata + full README[^18] |
| [https://libraries.io/npm/@tintinweb%2Fpi-tasks](https://libraries.io/npm/@tintinweb%2Fpi-tasks) | 2026-05-21 | pi-tasks npm metadata + README[^10] |
| [https://github.com/tintinweb/pi-gitnexus](https://github.com/tintinweb/pi-gitnexus) | 2026-05-21 | pi-gitnexus GitHub README[^11] |
| [https://github.com/BlackBeltTechnology/pi-agent-dashboard](https://github.com/BlackBeltTechnology/pi-agent-dashboard) | 2026-05-21 | pi-agent-dashboard GitHub repo[^20] |
| [https://lucumr.pocoo.org/2026/1/31/pi/](https://lucumr.pocoo.org/2026/1/31/pi/) | 2026-05-21 | Armin Ronacher's essay on Pi architecture and philosophy[^2] |
| [https://github.com/mksglu/context-mode](https://github.com/mksglu/context-mode) | 2026-05-21 | context-mode GitHub + HN discussion[^9][^23] |
| [https://formulae.brew.sh/formula/pi-coding-agent](https://formulae.brew.sh/formula/pi-coding-agent) | 2026-05-21 | Homebrew formula confirming MIT license + current stable version[^4] |
| [https://pi.dev/packages/pi-container-sandbox](https://pi.dev/packages/pi-container-sandbox) | 2026-05-21 | pi-container-sandbox page[^14] |
| [https://pi.dev/packages/@nqbao/pi-sandbox](https://pi.dev/packages/@nqbao/pi-sandbox) | 2026-05-21 | nqbao sandbox page[^15] |

---

## References

1. [pi/packages/coding-agent/README.md at main - GitHub](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md) - Pi is a minimal terminal coding harness. Adapt pi to your workflows, not the other way around, witho...

2. [Building Pi, and what makes self-modifying software so fascinating](https://www.youtube.com/watch?v=n5f51gtuGHE) - Mario Zechner is the creator of Pi, a minimalist, self-modifying AI coding agent, that is the founda...

3. [Pi Has a New Home at Earendil · News - Pi Coding Agent](https://pi.dev/news/2026/5/7/pi-has-a-new-home) - Pi has moved to its new long-term home under the Earendil Works organization. The code now lives at ...

4. [pi-coding-agent - Homebrew Formulae](https://formulae.brew.sh/formula/pi-coding-agent) - AI agent toolkit. https://pi.dev/. License: MIT. Development: Pull requests. Formula JSON API: /api/...

5. [pi-obsidian-preview](https://pi.dev/packages/pi-obsidian-preview) - A terminal-based coding agent

6. [Eleven quick tips for writing a Bioconductor package](https://dx.plos.org/10.1371/journal.pcbi.1012856)

7. [pi-package · GitHub Topics](https://github.com/topics/pi-package) - A pi extension that brings Claude Code-style task tracking and coordination to pi. Track multi-step ...

8. [pi-review-mode - Pi Coding Agent](https://pi.dev/packages/pi-review-mode) - Pi Review Mode is a Pi extension package that adds /review . It opens a Glimpse native review window...

9. [Stop Burning Your Context Window — We Built Context Mode](https://mksg.lu/blog/context-mode) - Stop Burning Your Context Window — We Built Context Mode. MCP server that reduces Claude Code contex...

10. [@tintinweb/pi-tasks 0.4.2 on npm - Libraries.io - Libraries.io](https://libraries.io/npm/@tintinweb%2Fpi-tasks) - A pi extension that brings Claude Code-style task tracking and coordination to pi.

11. [GitNexus knowledge graph integration for the Pi coding agent - GitHub](https://github.com/tintinweb/pi-gitnexus) - GitNexus knowledge graph integration for the Pi coding agent - tintinweb/pi-gitnexus

12. [Pi Agent - Obsidian Plugin](https://community.obsidian.md/plugins/pi-agent) - Manual installation. Download the latest release and copy these files into: <vault>/.obsidian/plugin...

13. [pi-sandbox 0.3.0 on npm - Libraries.io](https://libraries.io/npm/pi-sandbox) - OS-level sandboxing for pi with interactive permission prompts

14. [pi-container-sandbox - Pi Coding Agent](https://pi.dev/packages/pi-container-sandbox) - A terminal-based coding agent

15. [nqbao/pi-sandbox · Packages - Pi Coding Agent](https://pi.dev/packages/@nqbao/pi-sandbox) - A terminal-based coding agent

16. [kky42/pi-sandbox](https://pi.dev/packages/@kky42/pi-sandbox) - A terminal-based coding agent

17. [pi-committer - Pi Coding Agent](https://pi.dev/packages/pi-committer) - A terminal-based coding agent

18. [pi-observability 1.0.1 on npm](https://libraries.io/npm/pi-observability) - Live observability dashboard for pi coding agent sessions — tokens, cost, TPS, runtime, git stats, a...

19. [pi-cost - Pi Coding Agent](https://pi.dev/packages/pi-cost) - Cost dashboard for the pi coding agent — overview → project ... git clone https://github.com/Nikifor...

20. [BlackBeltTechnology/pi-agent-dashboard: Real-time web ... - GitHub](https://github.com/BlackBeltTechnology/pi-agent-dashboard) - Real-time web dashboard for pi coding-agent sessions. Multi-session view, live chat mirroring, integ...

21. [arcanemachine/pi-notify-marker - Pi Coding Agent](https://pi.dev/packages/@arcanemachine/pi-notify-marker) - A terminal-based coding agent

22. [jmfederico/pi-web - Pi Coding Agent](https://pi.dev/packages/@jmfederico/pi-web) - Run AI coding agents on your own machine or server, keep them alive in real workspaces, and control ...

23. [Context Mode – 315 KB of MCP output becomes 5.4 KB in Claude ...](https://news.ycombinator.com/item?id=47148025) - Session time before slowdown goes from ~30 min to ~3 hours. MIT licensed, single command install: /p...

24. [CHANGELOG.md - BlackBeltTechnology/pi-agent-dashboard - GitHub](https://github.com/BlackBeltTechnology/pi-agent-dashboard/blob/develop/CHANGELOG.md) - All notable changes to pi-agent-dashboard are documented in this file. The format is based on Keep a...

25. [Issues · BlackBeltTechnology/pi-agent-dashboard - GitHub](https://github.com/BlackBeltTechnology/pi-agent-dashboard/issues) - Real-time web dashboard for pi coding-agent sessions. Multi-session view, live chat mirroring, integ...

