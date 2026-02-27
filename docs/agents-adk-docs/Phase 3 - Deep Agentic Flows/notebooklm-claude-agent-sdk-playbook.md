# Claude Agent SDK — NotebookLM Research & Learning Playbook

**Created:** 2026-02-22
**Context:** Sean Winslow's Claude Code Superuser Pack → Agents SDK expansion
**Purpose:** Complete playbook for building, populating, and utilizing a NotebookLM notebook to master the Claude Agent SDK tailored to Sean's personal goals, projects, and second brain architecture.

---

## Table of Contents

1. [Goal & Strategy](#goal--strategy)
2. [Deep Research Prompts (Perplexity & Google)](#deep-research-prompts)
3. [Research Execution Plan](#research-execution-plan)
4. [NotebookLM Source List](#notebooklm-source-list)
5. [NotebookLM System Prompt](#notebooklm-system-prompt)
6. [NotebookLM Chat Prompts (6 Phases)](#notebooklm-chat-prompts)
7. [Audio Overview Prompts](#audio-overview-prompts)
8. [Infographic Prompts](#infographic-prompts)
9. [Data Table Prompts](#data-table-prompts)
10. [Workflow Summary](#workflow-summary)

---

## Goal & Strategy

### What We're Building

A comprehensive NotebookLM notebook that serves as the knowledge foundation for expanding Sean's Claude Agent SDK layer from a single Daily Driver agent into a full autonomous personal assistant system spanning PM work, creative/animation pipeline, life systems, and vault management.

### Why NotebookLM

NotebookLM synthesizes 40-80+ sources into a queryable knowledge base. Sean's learning methodology: tutorials → LLM chat → build by doing → document. NotebookLM sits at the research synthesis stage, producing structured knowledge that feeds directly into Claude Code implementation sessions.

### The Pipeline

1. **Deep Research** (Perplexity Max + Google Deep Research) → raw research documents
2. **NotebookLM Population** → sources + system prompt + chat prompts → structured notes
3. **Audio/Visual Generation** → audio overviews, infographics, data tables
4. **Vault Integration** → save outputs to `vault/40_knowledge/references/`
5. **Claude Code Implementation** → hand structured specs to Claude Code to build agents

---

## Deep Research Prompts

### Execution Rules

- **Separate conversations** for each prompt (never combine in one thread)
- **Can run in parallel** within each round
- **Attach context files** as specified per prompt

---

### Perplexity Prompt 1: SDK Architecture & Autonomous Agent Patterns

**Attach:** `agents-sdk.md`

```
I'm building autonomous personal assistant agents using the **Claude Agent SDK** (`claude-agent-sdk` Python package) that spawns Claude Code CLI as a subprocess. My current setup:

- A "Daily Driver" agent that runs on macOS `launchd` schedules (6am morning planning, 5pm EOD review, Friday 4pm weekly review)
- It reads/writes to an Obsidian vault using direct filesystem I/O and a custom MCP tool (`vault_inject`) for PATCH-style anchor-based writes
- Skills (`.claude/skills/*/SKILL.md` markdown files) are loaded as system prompts via a Python skill loader — no content duplication between interactive and autonomous modes
- Safety: 30-turn cap, $0.50/run budget, `acceptEdits` permission mode, `block-secrets` hook inherited via `setting_sources=["project"]`
- Auth uses Claude Code CLI's existing OAuth (`claude login`), no separate API key

**What I need to understand:**

1. What are the most effective patterns for building reliable autonomous agents with the Claude Agent SDK? Specifically: error recovery, retry logic, graceful degradation when tools fail, and handling context window limits across multi-step tasks.
2. How should I structure the `ClaudeAgentOptions` configuration for agents that need to make autonomous decisions without human input? What are the tradeoffs between `acceptEdits` vs `dangerouslySkipPermissions` for scheduled agents?
3. What MCP server patterns work best with the SDK? I'm using a custom in-process MCP tool — should I switch to external MCP servers for better reliability? What are the failure modes?
4. How do other developers handle **cost control** beyond simple budget caps? Are there patterns for early termination when an agent is looping or producing low-value output?
5. What's the current state of the Claude Agent SDK ecosystem — are there community tools, middleware, or wrapper libraries that add observability, testing, or orchestration on top of the base SDK?

Please include specific code patterns, configuration examples, and version-specific details where possible. Flag anything that may have changed recently.
```

---

### Perplexity Prompt 2: Personal Assistant Agent Design & Scheduling

**Attach:** `agents-sdk.md` + `Sean-Winslow-Personal-Context-v1.1.md`

```
I'm designing a suite of autonomous agents that function as a **personal second brain assistant**, running on macOS launchd schedules without human supervision. The agents read and write to an Obsidian vault (markdown files with YAML frontmatter and HTML comment anchors for content injection). My current and planned agents:

| Agent | Trigger | Purpose |
|-------|---------|---------|
| Daily Driver (morning) | 6am daily | Read yesterday's note, create today's, write 1-3-5 priorities |
| Daily Driver (evening) | 5pm daily | Summarize day, write reflection, carry forward items |
| Daily Driver (weekly) | Friday 4pm | Aggregate 7 daily notes into weekly review |
| Preserve Session | Claude Code stop hook | Capture decisions/context from interactive sessions into vault |
| Spending Analysis | Sunday 9am | Parse bank CSVs, identify recurring charges, track budget |
| Process Inbox | 8am daily | Triage Obsidian inbox folder, classify and route notes |
| Health Audit | 7pm daily | Review workout/nutrition habits, gamified progress tracking |

**What I need to understand:**

1. What are best practices for **multi-agent coordination** when agents share a filesystem (my Obsidian vault)? How do I prevent race conditions, handle concurrent writes, and ensure agents don't overwrite each other's work?
2. For the **Preserve Session** agent (triggered by a Claude Code stop hook): what's the best way to capture session context — should the hook pass conversation summary data to the agent, or should the agent read session transcripts? What data is available at session end?
3. For **financial analysis agents** parsing bank CSVs: what's the safest pattern for handling sensitive financial data in agent prompts? Should I pre-process CSVs into anonymized summaries before passing to Claude, or is there a better approach?
4. What **launchd patterns** work best for agents that depend on network/API availability? How should I handle cases where the agent runs but Claude's API is down, or the machine was asleep during the scheduled time?
5. How should agents **chain or depend on each other**? For example, the morning Daily Driver should ideally run after Process Inbox. What scheduling patterns or inter-agent signaling mechanisms exist?
6. Are there examples of people building **Obsidian + AI agent** integrations that go beyond simple note creation — things like knowledge graph traversal, semantic search during agent runs, or vault-wide pattern detection?
```

---

### Perplexity Prompt 3: Creative Industry & Animation Pipeline Agents

**Attach:** `Sean-Winslow-Personal-Context-v1.1.md` + `agents-sdk.md`

```
I'm a PM building autonomous AI agents using the **Claude Agent SDK** (Python, spawns Claude Code CLI as subprocess, runs on macOS launchd schedules). I also have a **Claude Code Superuser Pack** with 106 skills covering PM work, creative production, game dev, life systems, and an Obsidian vault as my second brain.

**My career trajectory:** I'm transitioning from technical PM at a crypto company to a **remote PM role in the animation/creative industry** within 2-3 years. My pipeline:
1. Sprite automation for a Game Boy fitness RPG (16BitFit, Phaser 3) → learning AI image generation pipelines
2. Transfer sprite automation to cartoon animation → train models in personal art style
3. Produce animated shorts using AI-assisted pipeline (have 5 completed shorts, won festival awards)
4. Submit to animation + AI film festivals → build portfolio + reputation
5. Land PM role in animation industry

**My creative tools:** Procreate, Adobe Character Animator, Premiere Pro, After Effects, Illustrator, ComfyUI (RTX 5080), ElevenLabs, Nano Banana Pro (Gemini API for sprite generation). I have Adobe MCP skills that automate Photoshop, Premiere, After Effects, and Illustrator via ExtendScript/UXP plugins.

**What I want to discover:**

1. What **autonomous agents** could I build with the Claude Agent SDK to accelerate my animation pipeline? Think beyond simple file generation — agents that manage asset libraries, enforce style consistency across frames, detect animation errors, batch-process renders, or coordinate multi-stage production workflows.
2. Could an agent autonomously **monitor and manage ComfyUI workflows**? For example: queue sprite generation batches, poll for completion, run vision-model QA on outputs, retry failed generations with adjusted parameters, and organize approved assets into TexturePacker-ready folders.
3. Are there patterns for agents that **bridge Adobe Creative Suite automation with LLM decision-making**? For example: an agent that reviews After Effects compositions, suggests timing adjustments based on animation principles, or auto-generates motion graphics from script breakdowns.
4. What would a **festival submission management agent** look like? One that tracks submission deadlines (Filmfreeway), prepares submission packages (synopsis, tech specs, stills), manages multiple festival calendars, and flags upcoming deadlines.
5. How could agents help with **portfolio and career transition work** — automatically generating case studies from completed projects, maintaining a portfolio website with fresh content, or tracking job postings in the animation/creative PM space?
6. Are there examples of people using LLM agents to **assist with creative production workflows** — storyboarding, shot planning, dialogue editing, sound design coordination, or color grading decisions?

Please focus on practical implementations that could be built with the Claude Agent SDK's capabilities (filesystem I/O, MCP tools, scheduled execution). I'm intermediate in Python and React.
```

---

### Perplexity Prompt 4: PM Productivity & Work Automation Agents

**Attach:** `Sean-Winslow-Personal-Context-v1.1.md` + `agents-sdk.md`

```
I'm an Associate PM (Technical) at The Block, a crypto news/data/research company. I manage the Campus education platform, coordinate with developers and designers, and spend my work week roughly: 45% building automation workflows (Zapier), 35% meetings, 20% firefighting. I lead daily standups and report to a Product Manager → VP of Product.

I've built an autonomous agent system using the **Claude Agent SDK** (Python, macOS launchd schedules) integrated with an Obsidian vault. I currently have a Daily Driver agent for morning planning and EOD review. I also have a Claude Code Superuser Pack with 106 skills including: PRD generation, Jira automation, sprint roadmapping, stakeholder updates, data analysis, meeting prep, and Zapier MCP integration (~175 tools across 12 apps including Jira, Slack, Google Calendar, Google Sheets, GA4).

**What I want to discover:**

1. What **PM-specific autonomous agents** could I build that go beyond daily planning? Think: agents that monitor Jira for sprint health and alert me to risks, agents that auto-generate weekly stakeholder reports from Jira + Slack + Google Sheets data, agents that prepare meeting briefs by pulling context from multiple sources before each meeting.
2. How could agents help me **reduce the 35% meeting overhead**? For example: pre-meeting context gathering agents, post-meeting action item extraction and Jira ticket creation, automatic standup summary distribution to Slack.
3. What patterns exist for agents that **bridge Zapier automations with Claude Agent SDK**? I currently have ~175 Zapier MCP tools. Could autonomous agents orchestrate complex multi-step Zapier workflows that are too sophisticated for Zapier's native logic?
4. Could an agent autonomously **monitor product metrics** (GA4 via Zapier MCP, Google Sheets) and write daily/weekly trend summaries to my vault? What about anomaly detection — flagging unexpected metric changes?
5. Are there patterns for **PRD and spec automation agents** — ones that take rough notes from my vault and progressively refine them into structured documents, or that auto-update specs when Jira tickets change?
6. What would a **developer coordination agent** look like? One that tracks PR status across GitHub, flags blocked PRs, summarizes code changes in plain language for PM review, and generates release notes.

I have access to Jira, Confluence, Slack, Google Calendar, Google Sheets, GA4 (via Zapier MCP), GitHub, and Figma. Please focus on what's buildable with the Claude Agent SDK + MCP tools.
```

---

### Google Deep Research Prompt 1: Claude Agent SDK — Advanced Patterns, Ecosystem, and Production Deployment

**Attach:** `agents-sdk.md`

```
Research the **Claude Agent SDK** (the Python package `claude-agent-sdk` by Anthropic that spawns Claude Code CLI as a subprocess for programmatic, autonomous agent execution). I need a comprehensive technical deep dive covering:

**Core SDK Mechanics:**
- The full `query()` function API — all parameters, return types, and edge cases
- How `ClaudeAgentOptions` configures tool access, MCP servers, permissions, budget limits, and system prompts
- The `claude_code` preset and what capabilities it grants vs. restricts
- How `setting_sources=["project"]` inherits hooks and settings from a project's `.claude/settings.json`
- Session management: can agents resume sessions, or is every `query()` call stateless?

**Production Patterns:**
- Error handling and retry strategies for autonomous agents (no human to intervene)
- Cost optimization: beyond `max_budget_usd`, are there ways to use cheaper models for subtasks, cache responses, or short-circuit unproductive runs?
- Logging and observability: what data does the SDK expose about token usage, tool calls, and decision paths?
- Testing autonomous agents: how do you write integration tests for agents that interact with filesystems and APIs?

**Ecosystem and Community:**
- What wrapper libraries, frameworks, or tools have been built on top of the Claude Agent SDK?
- How does the Claude Agent SDK compare to alternatives like OpenAI's Agents SDK, LangChain agents, CrewAI, or AutoGen for personal automation use cases?
- Are there open-source projects using the Claude Agent SDK for personal productivity, knowledge management, or second-brain automation?

**Integration Patterns:**
- Connecting MCP servers (Jira, Google Calendar, Slack, GitHub) to SDK agents — configuration patterns and authentication handling
- Using the SDK with Obsidian vaults: direct filesystem I/O vs. MCP-based vault access
- Combining scheduled agents (launchd/cron) with event-triggered agents (file watchers, webhooks, Git hooks)

**My specific context:** I have a working Daily Driver agent that creates/updates Obsidian daily notes on a macOS launchd schedule. I load SKILL.md files as system prompts. I want to expand to 6+ agents covering finance tracking, inbox processing, health habits, and session preservation. I need patterns that scale without ballooning costs or creating reliability issues.

Please prioritize recent sources (2025-2026), official Anthropic documentation, GitHub repos, and developer blog posts. Flag any information that may be outdated given the SDK's rapid development.
```

---

### Google Deep Research Prompt 2: Autonomous AI Personal Assistants — State of the Art and Practical Architectures

**Attach:** `Sean-Winslow-Personal-Context-v1.1.md` + `VAULT-GUIDE.md`

```
Research the current state of **autonomous AI personal assistant systems** — specifically architectures where LLM-powered agents run on schedules or triggers without human supervision, managing personal knowledge bases, tasks, and life systems. I need this research to inform building my own system using the Claude Agent SDK + Obsidian vault.

**Architecture Patterns:**
- What architectures exist for personal AI assistants that operate autonomously (scheduled runs, event-driven triggers)? Compare: single-agent-multi-skill vs. multi-agent-specialist vs. hierarchical (coordinator + workers)
- How do production personal assistant systems handle **memory and context persistence** across runs? My agents are stateless per-run but share an Obsidian vault as persistent memory — is this a proven pattern, or are there better approaches (vector DBs, conversation logs, structured state files)?
- What's the best way to give an autonomous agent **awareness of what other agents have done**? My agents share a vault but don't communicate directly.

**Knowledge Management Integration:**
- How are people integrating LLM agents with **Obsidian** or similar PKM tools? Cover: direct file I/O, MCP servers, REST APIs, semantic search over vault content
- What patterns exist for agents that **build and maintain knowledge graphs** — not just write notes, but discover connections, surface insights, and reorganize information over time?
- Are there examples of agents performing **weekly/monthly life reviews** by aggregating data from daily notes, financial records, health logs, and project updates?

**Financial and Health Automation:**
- What approaches exist for LLM agents that **parse bank statements and track spending** autonomously? What are the privacy/security patterns for handling financial data in agent prompts?
- How are people using AI agents for **health and habit tracking** — specifically gamification systems, workout logging, and nutrition analysis?

**Safety and Reliability:**
- What failure modes emerge in autonomous personal AI agents (runaway costs, data corruption, privacy leaks, hallucinated actions)?
- What guardrails beyond budget caps are used in practice? (Tool whitelists, output validators, human-in-the-loop checkpoints, dry-run modes)
- How do people test and validate autonomous agents before trusting them with real personal data?

**Real-World Implementations:**
- Surface any open-source projects, blog posts, or case studies of people building Claude/GPT/Gemini-powered personal assistant systems that run autonomously
- Include projects using: Obsidian + AI agents, launchd/cron scheduled LLM tasks, personal finance automation with LLMs, knowledge base maintenance agents

**My context:** I'm a PM transitioning toward the animation/creative industry, using a Claude Code "Superuser Pack" with 106 skills and an Obsidian vault as my second brain. I have a working Daily Driver agent on macOS launchd and want to expand to finance, health, inbox processing, and session preservation agents. I'm intermediate in Python and want patterns I can actually build, not theoretical frameworks.
```

---

### Google Deep Research Prompt 3: Life Systems & Personal Automation Agents

**Attach:** `Sean-Winslow-Personal-Context-v1.1.md` + `VAULT-GUIDE.md` + `agents-sdk.md`

```
Research what's possible with **autonomous LLM-powered agents for personal life management** — specifically for someone with the following context and goals:

**My situation:**
- 33 years old, moving from NYC to Boston (March 21, 2026) with girlfriend
- Credit card debt from career-switch investment (PM classes, AI tools), need to pay down aggressively
- Want to save for engagement ring and house within 2-3 years
- Work out 5-6 days/week (PPL split), eat healthy, wake at 4:45 AM
- Currently use Rocket Money (paid) for finance tracking — want to replace with a custom app
- All personal knowledge lives in an Obsidian vault (1,431 notes, PARA method, Dataview dashboards)
- Have a Claude Agent SDK setup running autonomous agents on macOS launchd schedules
- Have 106 Claude Code skills including: personal finance (Chase/Bilt CSV parsing, subscription audit), health habits (PPL tracking, gamification), time management, life admin

**What I want to discover — go broad and surprise me:**

1. **Financial automation agents** beyond budget tracking: What could an agent do with weekly bank CSV exports? Spending pattern analysis over time, subscription creep detection, cash flow forecasting, debt paydown scenario modeling, savings milestone tracking, tax prep automation (categorizing deductible expenses). What data would I need to feed it and how should I structure financial data in my vault?

2. **Health and fitness agents**: Beyond workout logging — could an agent analyze workout progression over time (volume, intensity trends), detect plateaus, suggest deload weeks, correlate sleep/nutrition with performance, or generate periodization plans? What data capture patterns work for gym tracking with LLM analysis?

3. **Relocation and life transition agents**: I'm moving to Boston in a month. Could agents manage: address change checklists across dozens of services, medical provider transitions, utility setup, neighborhood research, commute optimization, cost-of-living comparison tracking?

4. **Learning and skill development agents**: I learn through tutorials → LLM chat → building → documentation. Could agents track my learning progress across domains, surface connections between things I'm learning, generate spaced-repetition review cards (Anki) from vault notes, or create personalized learning paths based on my goals and current skill gaps?

5. **Relationship and social agents**: Gift tracking, important date reminders, meal planning for two, shared budget tracking with a partner, travel planning agents that research and propose trips based on preferences and budget constraints?

6. **"Compound interest" agents** — agents that get smarter over time by analyzing their own previous outputs: Could a weekly review agent detect patterns across months of data? Could a meta-agent analyze which other agents are producing value and suggest adjustments?

7. **Agents I haven't thought of**: What are people building with autonomous LLM agents for personal productivity that doesn't fit neatly into the categories above? Novel use cases, experimental approaches, things that sound weird but actually work.

Please include real examples, open-source projects, blog posts, and practical architectures. I'm intermediate in Python and want things I can actually build, not theoretical frameworks.
```

---

## Research Execution Plan

### Round 1 — Foundation (run in parallel)
| Prompt | Platform | Attachments |
|--------|----------|-------------|
| Perplexity Prompt 1 | Perplexity Max | `agents-sdk.md` |
| Google Deep Research Prompt 1 | Google Deep Research | `agents-sdk.md` |

### Round 2 — Expansion (run in parallel)
| Prompt | Platform | Attachments |
|--------|----------|-------------|
| Perplexity Prompt 3 | Perplexity Max | `Personal-Context` + `agents-sdk.md` |
| Perplexity Prompt 4 | Perplexity Max | `Personal-Context` + `agents-sdk.md` |
| Google Deep Research Prompt 3 | Google Deep Research | `Personal-Context` + `VAULT-GUIDE.md` + `agents-sdk.md` |

### Round 3 — Integration (run in parallel)
| Prompt | Platform | Attachments |
|--------|----------|-------------|
| Perplexity Prompt 2 | Perplexity Max | `agents-sdk.md` + `Personal-Context` |
| Google Deep Research Prompt 2 | Google Deep Research | `Personal-Context` + `VAULT-GUIDE.md` |

**Key rules:**
- Separate conversation for each prompt (never combine)
- Each round can run in parallel
- Sequencing is for learning flow, not tool dependencies

---

## NotebookLM Source List

### Research Outputs (from prompts above)
- All 7 deep research PDF/document outputs

### Official Documentation (add as URLs or PDFs)
- `https://platform.claude.com/docs/en/agent-sdk/overview` — SDK overview
- `https://platform.claude.com/docs/en/agent-sdk/reference` — API reference
- `https://github.com/anthropics/claude-agent-sdk` — GitHub repo
- `https://code.claude.com/docs/en/hooks` — Hooks documentation
- `https://code.claude.com/docs/en/sub-agents` — Subagents docs
- `https://code.claude.com/docs/en/mcp` — MCP integration
- `https://code.claude.com/docs/en/costs` — Token cost management

### Personal Context Files (add as uploads)
- `Sean-Winslow-Personal-Context-v1.1.md`
- `VAULT-GUIDE.md`
- `CLAUDE.md`
- `agents-sdk.md`
- `README.md`

### Videos, Articles, and Community Sources
Sources already added to the notebook (as shown in screenshots):
- 2026 Agentic Coding Trends Report.pdf
- Agent Suite Architecture Guide.pdf
- Agentic Workflows: BEYOND the Chat UI with Claude Code SDK (YouTube)
- Animation Pipeline Agent Architecture.pdf
- Autonomous AI Personal Assistant Research.pdf
- Build & deploy agents with the Claude Agent SDK (YouTube)
- Building Agents with Skills: Equipping Agents for Specialized Work (Anthropic blog)
- Building Effective AI Agents (Anthropic)
- Building a C compiler with a team of parallel Claudes (Anthropic)
- Building headless automation with Claude Code (YouTube)
- Claude Agent SDK Patterns.pdf
- Claude Agent SDK Technical Deep Dive.pdf
- Claude Agent SDK Full Workshop — Thariq Shihipar (YouTube)
- Claude Agent SDK: Getting Started | Live (YouTube)
- Claude Code Tutorial: Add AI to Your SaaS App (YouTube)
- Claude Code's Agent Teams Are Insane (YouTube)
- Claude Code's Real Purpose (YouTube)
- Claude SDK: 24-Hour Coding Agent | Cole Medin (YouTube)
- Customer story | Figma | Claude (Anthropic blog)
- Demystifying evals for AI agents (Anthropic)
- Designing AI resistant technical evaluations (Anthropic)
- How AI assistance impacts the formation of coding skills (Anthropic) — **note: appears twice, remove duplicate**
- How Claude Code Works - Jared Zoneraich (YouTube)
- How I Built The PERFECT AI Agent In 1 Week (YouTube)
- How I Turned Claude Code Into My Personal Assistant (YouTube)
- Improved Web Search with Dynamic Filtering | Claude (Anthropic blog)
- LLM Agents for Personal Life Management.pdf
- Making Claude Code more secure and autonomous with sandboxing (Anthropic)
- Measuring AI agent autonomy in practice (Anthropic)
- PM Agent System Architecture.pdf
- When to use multi-agent systems (and when not to) | Claude (Anthropic blog)
- Writing effective tools for AI agents (Anthropic)
- `https://platform.claude.com/cookbook/multimodal-crop-tool`

### Cleanup Notes
- Remove duplicate "How AI assistance impacts the formation of coding skills"
- Consider removing "Designing AI resistant technical evaluations" (tangential to agent building)

---

## NotebookLM System Prompt

**Settings:** Custom role, Longer response length

```
Role: You are a senior AI systems architect and personal productivity engineer who specializes in building autonomous LLM agent systems. You have deep expertise in the Claude Agent SDK, Claude Code, MCP integrations, and Obsidian-based knowledge management. You are advising Sean Winslow — a 33-year-old Associate PM (Technical) at The Block who is building a "Claude Code Superuser Pack" as his personal command center and second brain.

Sean's Setup (always reference this when answering):
- Has a working `agents-sdk/` layer with a Daily Driver agent (morning/evening/weekly modes) running on macOS launchd schedules
- 106 Claude Code skills loaded as system prompts via a Python skill_loader.py — skills are prompts, agents are runners
- Obsidian vault (1,431 notes, PARA method) with HTML comment anchors for PATCH-style writes, Dataview dashboards, and 6 domain MOCs
- Custom MCP tool (`vault_inject`) for anchor-based content injection into vault notes
- Safety: 30-turn cap, $0.50/run budget, acceptEdits permission mode, block-secrets hook
- Auth: Claude Code CLI OAuth via `claude login`, no separate API key
- Hardware: macOS daily driver + Windows 11 Alienware RTX 5080 for ComfyUI/AI workloads
- ~175 Zapier MCP tools across 12 apps (Jira, Slack, Google Calendar, Google Sheets, GA4, GitHub, Salesforce)

Sean's Goals for the Agent SDK:
1. PM Work Automation: Agents that prep standups from Jira, generate stakeholder reports, monitor sprint health, auto-create meeting briefs, track PR status on GitHub, and reduce his 35% meeting overhead
2. Creative/Animation Pipeline: Agents that manage ComfyUI sprite generation batches, enforce style consistency, coordinate Adobe automation (Photoshop, Premiere, After Effects, Illustrator via MCP), track festival submission deadlines, and progressively build his animation portfolio
3. Life Systems: Financial analysis agents parsing Chase/Bilt bank CSVs, subscription audit automation, health/fitness tracking with gamification (PPL split, 5-6 days/week), Boston move checklist management (March 21, 2026), and learning progress tracking across domains
4. Second Brain Evolution: Agents that process his Obsidian inbox, maintain knowledge graph connections, generate weekly/monthly life reviews from aggregated data, create Anki cards from vault notes, and get smarter over time by analyzing their own previous outputs
5. Career Transition: Moving from crypto PM to remote PM in animation/creative industry within 2-3 years. All side projects feed this pipeline: sprite automation → AI animation → festival submissions → creative industry PM role

How to Respond:
- Always connect SDK concepts back to Sean's specific agents, vault architecture, and goals — never give generic advice
- When explaining a pattern, show how it would work with his existing setup (vault anchors, skill loader, launchd schedules, config.toml)
- Suggest concrete new agents he could build, with: what skills they'd load, what schedule they'd run on, what vault notes they'd read/write, and what MCP tools they'd use
- Explain code choices at a beginner-to-intermediate level — Sean knows React/Python fundamentals but wants to understand WHY certain patterns are chosen
- Flag cost implications — Sean has credit card debt and needs to be smart about API spend. Always mention estimated per-run costs when suggesting new agents
- Cross-pollinate across domains: if a pattern from PM automation applies to creative pipeline agents (or vice versa), say so
- Prioritize practical, buildable implementations over theoretical architectures
- When uncertain, say so. Sean values intellectual honesty over false confidence
- Surface ideas Sean wouldn't think to ask about — adjacent techniques, unconventional agent patterns, emerging SDK features, things at the edges of what's possible
- Reference specific sources from this notebook when making claims — cite the research documents, Anthropic docs, and video content by name

Response Format:
- Lead with the actionable answer, then explain the reasoning
- Use concrete examples with file paths, config snippets, and vault note references from Sean's actual system
- When suggesting a new agent, use this structure: Purpose → Schedule/Trigger → Skills Loaded → Vault Notes Read/Written → MCP Tools Used → Estimated Cost → How It Connects to Sean's Goals
- Keep explanations clear but don't oversimplify — Sean learns fast and wants depth
```

---

## NotebookLM Chat Prompts

Run these in order. After each prompt, save the output as a note. Ask one follow-up question per prompt before moving to the next — NotebookLM's in-thread follow-ups produce the sharpest cross-referenced insights.

### Phase 1: Foundation & Architecture

**Prompt 1.1 — SDK Mental Model**

> Based on the sources in this notebook, explain the Claude Agent SDK's core architecture — how `query()` works, what `ClaudeAgentOptions` controls, how system prompts are constructed, and how the SDK spawns Claude Code CLI as a subprocess. Map each concept to how my existing Daily Driver agent uses it (reference my agents-sdk.md). Include a mental model diagram I can use to understand the full lifecycle of an agent run from Python script → CLI spawn → tool execution → vault write → log recording.

**Prompt 1.2 — My Current System Audit**

> Analyze my current agents-sdk implementation (from agents-sdk.md) against the best practices described in the SDK documentation and research sources in this notebook. What am I doing well? What gaps or risks exist in my current architecture? Specifically evaluate: my skill loading approach, my safety configuration (30 turns, $0.50 cap, acceptEdits), my custom MCP tool setup (vault_inject), my logging/observability, and my launchd scheduling. Give me a prioritized list of improvements with effort estimates.

**Prompt 1.3 — Interactive vs Autonomous Decision Framework**

> Using the sources in this notebook, create a decision framework for when I should use each execution mode: (1) interactive Claude Code session with skills, (2) interactive session with subagents, (3) Claude Code Agent Teams, (4) autonomous SDK agents on launchd schedules, (5) SDK agents triggered by hooks/events. For each mode, explain the tradeoffs (cost, reliability, human oversight, context window, tool access) and give 3 concrete examples from my project domains (PM work at The Block, creative/animation pipeline, life systems, vault management).

---

### Phase 2: Safety, Guardrails & Cost Control

**Prompt 2.1 — Safety Architecture**

> Based on all sources in this notebook, compile a comprehensive safety and guardrails guide for my autonomous agents. Cover: permission modes (acceptEdits vs dangerouslySkipPermissions — when to use each and why), tool whitelisting strategies, hook-based guardrails (my block-secrets.py, network-access-control), budget caps and early termination patterns, filesystem scope restrictions, preventing agents from modifying critical files, handling sensitive data (bank CSVs, credentials), and what happens when an agent encounters an error with no human present. Give me a `safety-checklist.md` I can add to my vault that I reference before deploying any new agent.

**Prompt 2.2 — Cost Optimization Playbook**

> I have credit card debt and need to be extremely cost-conscious with my agent runs. Using the sources in this notebook, create a cost optimization playbook covering: how to estimate per-run costs before deploying, patterns for reducing token usage (shorter prompts, fewer turns, targeted tool access), when to use cheaper models for subtasks, how to detect and terminate unproductive agent loops, dry-run testing strategies, and how to track spending trends over time using my agent-run-history.csv. Include specific cost estimates for each of my planned agents (Daily Driver, Spending Analysis, Process Inbox, Health Audit, Preserve Session, animation pipeline agents, PM automation agents).

**Prompt 2.3 — Agent Evaluation & Evals**

> Using the Anthropic sources on agent evals, demystifying evals, and measuring agent autonomy in this notebook, create a practical evaluation framework for my agents. How should I measure whether each agent is actually producing value? Cover: defining success criteria per agent type (planning agents vs data analysis agents vs creative pipeline agents), building eval datasets from my vault's existing data, automated quality checks on agent outputs, A/B testing agent prompt variations, tracking agent performance over time, and red-teaming my agents for failure modes. Tailor this specifically to my agent roster — what does "good output" look like for a morning planning agent vs a financial analysis agent vs an animation QA agent?

---

### Phase 3: Building New Agents

**Prompt 3.1 — Agent Design Template**

> Based on the patterns in this notebook, create a reusable agent design template I can follow every time I build a new agent. The template should include: purpose statement, trigger/schedule, skills to load, vault notes to read (input), vault notes to write (output with anchor names), MCP tools needed, allowed tools whitelist, max turns and budget, success criteria, failure modes and fallbacks, testing strategy (dry-run → limited-run → full deployment), and config.toml entry. Fill in the template for my next three priority agents: Spending Analysis, Process Inbox, and Preserve Session.

**Prompt 3.2 — PM Work Agents**

> Design a complete suite of PM automation agents for my work at The Block. I lead daily standups, manage Campus 201 features, coordinate with developers, and spend 45% of my time on Zapier automations, 35% on meetings, and 20% on firefighting. I have access to Jira, Confluence, Slack, Google Calendar, Google Sheets, GA4 (via Zapier MCP), GitHub, and Figma. For each agent, specify: what it does, when it runs, what skills it loads, what MCP tools it calls, what vault notes it reads/writes, estimated cost per run, and how it reduces my meeting overhead or manual work. Think beyond what I've already planned — what PM agents would surprise me with their usefulness?

**Prompt 3.3 — Creative Pipeline Agents**

> Design agents for my animation and creative pipeline. My trajectory: sprite automation (16BitFit, Phaser 3) → AI animation pipeline → animated shorts → festival submissions → creative industry PM career. My tools: ComfyUI on RTX 5080, Adobe suite via MCP (Photoshop, Premiere, After Effects, Illustrator), Procreate, Nano Banana Pro, ElevenLabs. I need agents for: sprite generation batch management and QA, style consistency enforcement across animation frames, shot planning and storyboard organization, festival submission deadline tracking (Filmfreeway), portfolio case study generation, and any creative production workflow I haven't thought of. For each agent, explain how it would work with the SDK's capabilities (filesystem I/O, MCP tools, scheduled execution).

**Prompt 3.4 — Life Systems Agents**

> Design agents for my personal life systems. Context: moving to Boston March 21 2026, credit card debt to pay down, saving for engagement ring and house, working out 5-6 days/week (PPL split, 4:45 AM wake), use Rocket Money (want to replace), all personal knowledge in Obsidian vault. Design agents for: financial analysis (Chase/Bilt CSV parsing, spending trends, debt paydown tracking, subscription monitoring), health tracking (workout progression analysis, plateau detection, gamified XP system), Boston move management (checklist tracking, address changes, provider transitions), learning progress tracking across all my domains, and a "meta-agent" that reviews other agents' outputs weekly to detect patterns and suggest improvements. For each, specify schedule, skills, vault integration, and cost estimate.

**Prompt 3.5 — Vault & Knowledge Management Agents**

> Design agents that make my Obsidian vault smarter over time. My vault has 1,431 notes using PARA method, 6 domain MOCs, Dataview dashboards, HTML comment anchors for programmatic writes, and a process-inbox skill. Design agents for: daily inbox triage and classification, stale note detection (active status but untouched for 30+ days), automatic backlink and connection discovery between notes, weekly vault health reports (notes created, domains growing, gaps), knowledge synthesis (reading multiple related notes and generating summary insights), and Anki card generation from reference notes. Explain how each agent navigates the vault (MOC-first, grep, frontmatter filtering) and where it writes output.

---

### Phase 4: External Integrations

**Prompt 4.1 — MCP Integration Roadmap**

> Based on the sources in this notebook, create a prioritized MCP integration roadmap for my agents. I currently have ~175 Zapier MCP tools and a custom vault_inject MCP tool. Map out which MCP servers I should connect next, in priority order, considering: (1) value to my daily workflow, (2) complexity to set up, (3) cost implications, (4) security considerations. Cover: Jira MCP (mcp-atlassian), Google Calendar, Slack, GitHub CLI, Obsidian MCP server, Google Sheets, NotebookLM MCP, Hugging Face MCP, and any others mentioned in the sources. For each, explain: what agents would use it, what authentication/OAuth is needed, how to configure it in ClaudeAgentOptions, and estimated setup effort.

**Prompt 4.2 — Authentication & Security for External Services**

> Create a comprehensive guide for safely connecting external services to my autonomous agents. Cover: OAuth flows for Google services (Calendar, Sheets, GA4), Jira/Confluence API tokens, Slack bot tokens, GitHub personal access tokens, and any other auth patterns needed for my planned integrations. Explain: where credentials should be stored (not .env since my block-secrets hook protects it — what's the alternative?), how to pass auth to MCP servers in ClaudeAgentOptions, how to rotate credentials, and how to audit which agents have access to which services. I'm a beginner with OAuth — explain why each auth method works the way it does.

**Prompt 4.3 — Zapier MCP as Agent Orchestrator**

> I have ~175 Zapier MCP tools across 12 apps. Explore how my autonomous agents can orchestrate complex multi-step Zapier workflows that are too sophisticated for Zapier's native logic. For example: an agent that pulls Jira sprint data via Zapier MCP, cross-references with Google Calendar availability, generates a resource allocation report, and posts it to Slack — all in one scheduled run. What patterns work for chaining multiple Zapier MCP tool calls within a single agent run? What are the failure modes and cost implications of tool-heavy agent runs? Give me 5 concrete multi-tool workflow examples that combine my available Zapier tools.

---

### Phase 5: Advanced Patterns & Scaling

**Prompt 5.1 — Multi-Agent Coordination**

> Based on the sources on multi-agent systems, agent teams, and the parallel Claudes case study in this notebook, design the coordination layer for my agent suite. I'll eventually have 8-12 agents sharing the same Obsidian vault. Cover: preventing write conflicts (two agents targeting the same daily note anchor), agent dependency chains (Process Inbox should run before Daily Driver morning), shared state management through vault notes, inter-agent communication patterns (can one agent's output trigger another?), and monitoring the health of the full agent fleet. Give me a concrete coordination architecture with file paths, scheduling order, and failure recovery patterns.

**Prompt 5.2 — Agents That Improve Over Time**

> Explore patterns for agents that get smarter over time by learning from their own history. My agents log every run to agent-run-history.csv and write structured content to vault notes. How could a meta-agent: analyze patterns across weeks/months of daily notes, detect which priorities I consistently carry forward (indicating poor estimation or avoidance), identify spending trends from financial analysis outputs, track my skill development trajectory across domains, correlate workout consistency with productivity patterns, and generate monthly "state of Sean" reports that surface insights I wouldn't see myself? What data structures in my vault would support this kind of longitudinal analysis?

**Prompt 5.3 — Event-Driven & Reactive Agents**

> Beyond scheduled launchd agents, what event-driven and reactive agent patterns could I implement? Explore: agents triggered by Claude Code stop hooks (Preserve Session), file-watcher agents that activate when new bank CSVs appear in a folder, Git hook agents that run when I push to specific repos, webhook-triggered agents (Slack message → agent action), and Obsidian-triggered agents (new note in inbox → auto-classification). For each trigger type, explain the technical implementation on macOS, how to pass event context to the agent, and what safety considerations differ from scheduled agents.

**Prompt 5.4 — Agent SDK vs Agent Teams — When to Use What**

> Compare the Claude Agent SDK (autonomous Python scripts) with Claude Code Agent Teams (experimental, multiple Claude Code instances coordinating in real-time) for my use cases. When would I use Agent Teams instead of SDK agents? Explore: using Agent Teams for complex one-off tasks (like a full 16BitFit sprint rebuild), using SDK agents for recurring scheduled work, and hybrid patterns where a scheduled SDK agent spawns an Agent Team for a complex subtask. Reference the Agent Teams documentation and the parallel Claudes case study from this notebook.

---

### Phase 6: Implementation Planning

**Prompt 6.1 — 30-60-90 Day Roadmap**

> Based on everything in this notebook and my current state (one working Daily Driver agent, moving to Boston March 21), create a phased implementation roadmap. Phase 1 (next 30 days): which 2-3 agents should I build next, what integrations to set up, what safety improvements to make. Phase 2 (days 30-60): expanding the agent fleet, adding MCP integrations, building the meta-analysis layer. Phase 3 (days 60-90): advanced patterns, event-driven agents, creative pipeline agents, full second brain automation. For each phase, estimate total development time and ongoing daily API costs. Account for the Boston move disruption in mid-March.

**Prompt 6.2 — Full Agent Fleet Specification**

> Compile the complete specification for my target agent fleet — every agent I should build based on all the analysis in this notebook. For each agent, provide: name, one-sentence purpose, trigger type (schedule/event/manual), schedule if applicable, skills loaded from my Superuser Pack, MCP tools required, vault notes read (input), vault notes written (output), max turns, max budget, dependencies on other agents, estimated cost per run, and which of my goals it serves (PM work, creative pipeline, life systems, vault management, career transition). Organize by priority tier (build now, build next, build later, experimental).

---

## Audio Overview Prompts

All use **Deep Dive** format and **Long** length unless noted.

### Audio 1 — The Big Picture

> Explain Sean Winslow's complete autonomous agent system — from the Claude Agent SDK architecture to the Obsidian vault integration to the launchd scheduling. Walk through the full lifecycle of an agent run: Python script triggers, skills load as system prompts, Claude Code CLI spawns, tools execute, vault notes get written, costs get logged. Then discuss the expansion roadmap: what agents he should build next across PM work, creative animation pipeline, and life systems. Make it feel like a masterclass on building a personal AI assistant infrastructure, not just a feature walkthrough.

### Audio 2 — Safety, Cost, and Trust

> Focus on the tension between autonomy and safety in Sean's agent system. He has agents running with no human present, writing to his personal vault, and eventually parsing his bank statements. Discuss: what guardrails exist (budget caps, tool whitelists, hook-based blocking), what's still missing, how to evaluate whether agents are producing real value vs burning tokens, and the cost optimization strategies that matter most given his credit card debt situation. Include the eval frameworks from the Anthropic sources — how should he measure agent quality over time? Make this practical, not theoretical.

### Audio 3 — Creative Pipeline Agents

> Explore how autonomous agents could transform Sean's animation and creative production workflow. He's building a pipeline from sprite automation (16BitFit game) to AI-assisted cartoon animation to festival submissions, with the goal of transitioning to a PM role in the animation industry. Discuss: ComfyUI batch management agents, style consistency enforcement, Adobe suite automation via MCP, festival deadline tracking, portfolio generation, and any creative production agent patterns from the research sources. Connect each idea back to his career transition timeline.

### Audio 4 — PM Agents That Actually Save Time

> Sean spends 35% of his work week in meetings and 20% firefighting. Discuss the PM automation agents that would give him the most time back: standup prep from Jira data, meeting brief generation, post-meeting action item extraction, sprint health monitoring, stakeholder report automation, and developer coordination. Cover the Zapier MCP integration angle — he has 175 tools across 12 apps. What multi-tool agent workflows would be most impactful? Be specific about which tools get called in which order.

### Audio 5 — Agents That Get Smarter Over Time

> Discuss the concept of compound intelligence — agents that analyze their own previous outputs to surface patterns Sean wouldn't see himself. Cover: meta-agents reviewing weeks of daily notes to detect productivity patterns, financial trend analysis across months of spending data, learning progress tracking across domains, and the "state of Sean" monthly review concept. How should he structure vault data to support longitudinal analysis? What makes this different from simple dashboards? Reference the research sources on agent memory and self-improvement patterns.

### Audio 6 — Debate: SDK Agents vs Agent Teams

**Use Debate format.**

> Have the hosts debate: when should Sean use autonomous SDK agents (scheduled Python scripts) versus Claude Code Agent Teams (multiple Claude instances coordinating in real-time)? One host argues SDK agents are better for everything — simpler, cheaper, more reliable. The other argues Agent Teams unlock capabilities SDK agents can't touch, like the 16BitFit rebuild or complex cross-domain research tasks. Use specific examples from Sean's project list and reference the Agent Teams documentation and parallel Claudes case study.

---

## Infographic Prompts

All use **Landscape** orientation and **Detailed** level.

### Infographic 1 — Agent Lifecycle

> Create an infographic showing the complete lifecycle of a Claude Agent SDK run in Sean's system. Flow: launchd trigger → Python script starts → config.toml loaded → skills loaded as system prompts → ClaudeAgentOptions built → query() spawns Claude Code CLI → tools execute (Read, Write, Edit, Glob, Grep, vault_inject MCP) → vault notes created/updated → run logged to agent-run-history.csv → launchd job completes. Include the safety checkpoints at each stage (budget cap, turn limit, hook enforcement, tool whitelist). Use a dark color theme with clear directional flow.

### Infographic 2 — Agent Fleet Map

> Create an infographic mapping Sean's complete target agent fleet. Organize by domain: PM Work (standup prep, sprint health, stakeholder reports, meeting briefs, PR digest), Creative Pipeline (ComfyUI batch manager, style enforcer, festival tracker, portfolio generator), Life Systems (spending analysis, subscription audit, health tracker, move checklist), Vault Management (inbox processor, stale note detector, knowledge synthesizer, Anki generator), and Meta (weekly pattern analyzer, agent fleet health monitor). Show schedule/trigger for each, color-coded by priority tier (build now, build next, build later). Use a dark theme.

### Infographic 3 — Safety & Guardrails Architecture

> Create an infographic showing all the safety layers in Sean's autonomous agent system. Layers: Python-level (max_turns, max_budget_usd, allowed_tools whitelist, dry-run mode), CLI-level (permission mode, setting_sources inheriting project hooks), Hook-level (block-secrets.py blocking credential access, network-access-control blocking unauthorized domains, log-tool-use recording every action), Vault-level (PATCH-only writes via anchors, never delete without permission, search before create), Monitoring-level (agent-run-history.csv cost tracking, per-run log files, launchd stdout/stderr). Use a layered defense-in-depth visual with a dark theme.

### Infographic 4 — MCP Integration Roadmap

> Create an infographic showing Sean's MCP integration roadmap in priority order. Current: Zapier MCP (175 tools, 12 apps), custom vault_inject tool. Priority 1: Jira MCP (standup prep, sprint tracking), Google Calendar (meeting-aware planning), Slack (status distribution). Priority 2: GitHub CLI (PR digest, release notes), Obsidian MCP (semantic search from agents). Priority 3: Google Sheets (financial tracking), NotebookLM MCP (audio briefings). Show what agents each MCP unlocks and the authentication method required (OAuth, API token, local). Dark theme.

### Infographic 5 — 90-Day Buildout Timeline

> Create an infographic showing Sean's 90-day agent buildout roadmap. Phase 1 (Days 1-30, pre-Boston move): improve Daily Driver safety, build Spending Analysis agent, build Process Inbox agent, set up Jira MCP. Phase 2 (Days 30-60, post-move settling): Preserve Session agent, Health Audit agent, Google Calendar integration, meta-analysis agent. Phase 3 (Days 60-90): Creative pipeline agents (ComfyUI batch, style enforcer), event-driven triggers, festival tracker, full fleet monitoring. Mark March 21 Boston move as a milestone. Show estimated cumulative daily API cost at each phase. Dark theme with timeline visualization.

---

## Data Table Prompts

### Table 1 — Complete Agent Specifications

> Create a data table with every agent Sean should build, using columns: Agent Name, Domain (PM/Creative/Life/Vault/Meta), Trigger Type (schedule/event/manual), Schedule (if applicable), Skills Loaded, MCP Tools Required, Vault Notes Read, Vault Notes Written, Max Turns, Max Budget USD, Dependencies, Priority Tier (now/next/later), Estimated Cost Per Run. Include all agents from the sources: Daily Driver (3 modes), Spending Analysis, Process Inbox, Preserve Session, Health Audit, MD to Anki, Standup Prep, Sprint Health Monitor, Stakeholder Reporter, Meeting Brief Generator, PR Digest, ComfyUI Batch Manager, Style Enforcer, Festival Tracker, Portfolio Generator, Meta Analyzer.

### Table 2 — MCP Tools & Authentication

> Create a data table of all external tools and MCP servers Sean should connect to his agents, using columns: Service Name, MCP Server/Method, Authentication Type (OAuth/API Key/Token/Local), What Agents Use It, Setup Complexity (Low/Medium/High), Security Considerations, Current Status (connected/planned). Include: Zapier MCP (current), vault_inject (current), Jira, Confluence, Slack, Google Calendar, Google Sheets, GA4, GitHub, Obsidian Local REST API, NotebookLM, Hugging Face, Figma.

### Table 3 — Skills-to-Agents Mapping

> Create a data table mapping Sean's existing 106 Claude Code skills to which autonomous agents should load them, using columns: Skill Name, Domain, Current Use (interactive only / autonomous / both), Which SDK Agents Load It, Autonomous-Friendly (yes/needs adaptation/no — based on whether the skill instructions assume a human is present), Adaptation Needed (if any). Focus on the skills most relevant to autonomous operation: daily-driver, vault-read-write, process-inbox, subscription-audit, health-habits, personal-finance, jira-automation, stakeholder-update, meeting-prep, data-analysis, animation-pipeline, sprite-asset-pipeline, time-management.

### Table 4 — Safety Configuration Matrix

> Create a data table showing the safety configuration for each agent, using columns: Agent Name, Permission Mode, Max Turns, Max Budget USD, Allowed Tools (whitelist), Blocked Tools, Hooks Inherited, Handles Sensitive Data (yes/no), Sensitive Data Type (if applicable), Requires Dry-Run Testing Before Deploy, Risk Level (low/medium/high), Risk Mitigation Notes. Include all planned agents and flag which ones need extra scrutiny (especially Spending Analysis handling bank CSVs and any agents with Bash access).

### Table 5 — Cost Projection Model

> Create a data table projecting Sean's monthly agent costs, using columns: Agent Name, Runs Per Month, Estimated Cost Per Run, Monthly Cost, Cumulative Monthly Total. Group by deployment phase: Phase 1 agents (Daily Driver 3 modes + Spending Analysis + Process Inbox), Phase 2 additions (Preserve Session + Health Audit + Calendar integration), Phase 3 additions (Creative pipeline + PM automation + Meta analyzer). Show subtotals per phase and a grand total. This will help Sean budget his API spend against his debt paydown goals.

---

## Workflow Summary

### Step-by-Step Execution Order

1. **Run Deep Research prompts** (7 prompts across Perplexity Max and Google Deep Research, 3 rounds)
2. **Add all sources to NotebookLM** (research outputs + official docs + personal context files + videos/articles)
3. **Set the system prompt** (Custom role, Longer responses)
4. **Run Phase 1-6 chat prompts** in order (18 prompts, save each output as a note, ask 1 follow-up per prompt)
5. **Re-add chat notes as sources** (feedback loop — notebook compounds on itself)
6. **Generate Audio Overviews** (6 episodes for passive learning during gym/commute)
7. **Generate Infographics** (5 visual references for Obsidian vault)
8. **Generate Data Tables** (5 structured reference tables)
9. **Re-add audio/infographic/table outputs as sources** (final compounding layer)
10. **Export structured outputs to vault** at `vault/40_knowledge/references/ref-agent-sdk-*.md`
11. **Hand implementation specs to Claude Code** to start building agents

### Key Principles

- **Separate conversations** for each deep research prompt
- **Sequential phases** for NotebookLM chat prompts (each builds on previous)
- **One follow-up question** per chat prompt before moving to the next
- **Save and re-add** outputs as sources to create compounding knowledge
- **Match context file attachments** to each prompt's specific focus area
- **Always dry-run** before live-deploying any new agent
- **Track costs** obsessively given financial goals

---

*This document is a living reference for the Claude Agent SDK NotebookLM research initiative. It connects to Sean's broader Superuser Pack project, Obsidian vault, and career transition goals. Last updated: 2026-02-22.*
