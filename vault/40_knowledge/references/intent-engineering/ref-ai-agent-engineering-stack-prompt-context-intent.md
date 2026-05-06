---
title: "Prompt Engineering, Context Engineering, and Intent Engineering — A Technical Comparison for the AI Agent Stack"
type: reference
status: processed
domain: claude-mastery
created: 2026-02-28
ai-context: "Definitive technical comparison of the three AI engineering disciplines as a layered stack — argues prompt engineering is becoming a subset of context engineering, intent engineering is OKRs/BDI/design-intent applied to autonomous agents, and the three are layers in a stack solving distinct failure modes (instruction misunderstanding / missing knowledge / wrong objective)."
tags:
  - reference
  - intent-engineering
  - context-engineering
  - prompt-engineering
  - source/pdf
  - mcp
  - claude-md
related:
  - "[[intent-engineering]]"
source-pdf: "AI-Agent-Engineering-Stack.pdf"
---

# The AI Agent Engineering Stack — Prompt, Context, Intent

The AI agent engineering stack is crystallizing around three layered disciplines:

- **Prompt engineering** — optimizes single-turn instructions
- **Context engineering** — manages the full information environment across sessions
- **Intent engineering** — aligns agent behavior to system-level goals + constraints

Short version: context engineering is real and necessary — formalized through 1,400+ research papers and endorsed by Anthropic, Karpathy, and Tobi Lütke. Intent engineering is substantively real in what it addresses (agents that optimize the wrong thing) but its intellectual lineage runs directly through OKRs, BDI agent architecture, and design intent theory. The novelty is in the application domain, not the underlying framework.

## The Three Disciplines Compared

| Dimension | Prompt Engineering | Context Engineering | Intent Engineering |
|-----------|-------------------|---------------------|-------------------|
| **Core question** | "How should I phrase this?" | "What does the model need to know?" | "What should this agent want?" |
| **Problem solved** | Ambiguity in single-turn LLM interactions | Information management across multi-turn agent sessions | Goal misalignment in autonomous agent behavior |
| **Scope** | Single interaction (stateless) | Session to system lifetime (stateful) | System lifetime (persistent) |
| **What it encodes** | Instructions, tone, format, constraints | Knowledge, tools, memory, retrieved data, message history | Objectives, outcomes, constraints, decision authority, stop rules |
| **Unit of design** | The prompt text | The full informational environment | The agent's mandate and boundaries |
| **Failure mode** | Model misinterprets the request | Model lacks information or drowns in irrelevant context | Agent optimizes the wrong thing or crosses boundaries |
| **Who practices it** | End users and developers | System architects and AI engineers | Product managers, engineering leaders, governance teams |
| **Temporal persistence** | None (one-shot) | Session-level with optional cross-session persistence | Permanent until explicitly revised |

## Prompt Engineering — "What to Do"

Crafting precise textual instructions to elicit desired behavior from an LLM in a single inference call. Operates at the level of a single interaction; stateless.

**Failure mode:** ambiguity — the model misinterprets the request, produces wrong format outputs, or makes incorrect assumptions about what's being asked.

**Current status:** prompt engineering is increasingly understood as a *subset* of context engineering rather than a standalone discipline. Anthropic's framing: "prompt engineering refers to methods for writing and organizing LLM instructions for optimal outcomes," while context engineering encompasses "the set of strategies for curating and maintaining the optimal set of tokens during LLM inference."

## Context Engineering — "What to Know"

Dynamically managing the entirety of information an LLM sees at every step of a complex task — ensuring the model has precisely the right information, at the right time, in the right format. Operates at session and system level; stateful.

The term was popularized in mid-2025 by Shopify CEO Tobi Lütke ("I really like the term 'context engineering'... it describes the core skill better"). Andrej Karpathy endorsed it, framing LLMs as CPUs and context windows as RAM, with context engineering as the operating system that loads the right data for each task.

### Three Anthropic Long-Horizon Techniques

- **Compaction** — Summarize a conversation nearing the context limit and reinitiate with the compressed summary. Claude Code preserves architectural decisions + unresolved bugs while discarding redundant tool outputs.
- **Structured note-taking** — Agents write persistent notes outside the context window (NOTES.md), pulled back in at later steps. Demonstrated by Claude playing Pokémon — precise tallies maintained across thousands of game steps.
- **Sub-agent architectures** — Specialized sub-agents handle focused tasks with clean context windows, returning only condensed summaries (~1,000–2,000 tokens) to the orchestrator.

**Failure mode:** retrieval failure + context pollution — the agent either lacks critical information, retrieves wrong/stale documents, or drowns in irrelevant context that degrades performance. As context windows grow, models show reduced precision for retrieval at longer contexts (n² pairwise attention) — a performance gradient, not a hard cliff.

### AgenticSE Framing

Ahmed Hassan's *Agentic Software Engineering* textbook (2026) dedicates Chapter 5 to context engineering, framing it as "managing knowledge for stochastic teammates." Core concept: "context is an interface, not a dump." Practices include seeding a minimal working set, actively managing context load during execution, quarantining exploration, and transferring clean continuity across sessions.

## Intent Engineering — "What to Want"

Structuring what an AI agent should optimize for — its objectives, success criteria, constraints, decision authority, and failure modes — in a way that survives real-world edge cases where instructions run out. Per the Product Compass framework: "Intent is what determines how an agent acts when instructions run out."

Operates at system-lifetime level. Encodes the agent's persistent mandate through a 7-part structure:

1. **Objective** — The problem to solve and why it matters (qualitative, aspirational)
2. **Desired Outcomes** — Observable states indicating success (measurable, from user perspective)
3. **Health Metrics** — What must not degrade while pursuing outcomes (guards against Goodhart's Law)
4. **Strategic Context** — The system the agent operates within
5. **Constraints** — Both steering (prompt layer) and hard (enforced in orchestration)
6. **Decision Authority** — Which decisions the agent may take autonomously vs. must escalate
7. **Stop Rules** — When to halt, escalate, or mark complete

**Failure mode:** misaligned optimization — the agent pursues a technically valid but strategically wrong objective. A customer support agent told to "resolve issues faster" with no health metrics will rush responses, tanking quality. An agent told to "reduce escalations" with no constraints will handle situations it shouldn't.

## Anthropic's MCP as Context Engineering Infrastructure

The Model Context Protocol (released by Anthropic November 2024) is the infrastructure layer that makes context engineering scalable. MCP replaces the N×M integration problem (connecting N models to M data sources via bespoke connectors) with a standardized interface.

Client-server architecture using JSON-RPC 2.0 with three core primitives: **tools** (actions), **resources** (data), **prompts** (templates). 8M+ weekly SDK downloads as of mid-2025.

Relationship to context engineering is direct: MCP delivers context to agents at runtime. Per Anthropic's engineering blog, agents using "just-in-time" context strategies maintain lightweight identifiers (file paths, stored queries, web links) and use MCP tools to dynamically load data into context at runtime, rather than pre-processing all relevant data up front. Mirrors how Claude Code uses MCP connections alongside glob and grep to navigate its environment.

## CLAUDE.md as a Persistent Context/Intent Layer

Claude Code's CLAUDE.md file bridges context engineering and intent engineering. Loaded into every session start; operates at three hierarchical levels:

- **Global** (`~/.claude/CLAUDE.md`) — Cross-project user preferences and patterns
- **Project** (repository root) — Shared team context, checked into version control
- **Local** (`CLAUDE.local.md`) — Private developer-specific notes, excluded from version control

Encodes both **context** (project structure, code style, build commands, architectural decisions, terminology) and **intent** (coding standards, patterns to avoid, escalation behaviors, testing requirements). This dual role makes CLAUDE.md a practical example of how the three disciplines collapse in implementation: the file *is* a prompt (instructions), *carries* context (project knowledge), and *embodies* intent (what the agent should optimize for within this codebase).

The emerging AGENTS.md standard attempts to consolidate tool-specific formats (CLAUDE.md, .cursorrules, etc.) into a single specification, though analysis of 466 open-source projects found "no established content structure yet" with significant variation between descriptive, prescriptive, prohibitive, explanatory, and conditional content.

## Amazon's Three-Layer Evaluation Framework

Amazon's production framework for measuring whether agents correctly understand intent operates across three layers:

| Layer | What It Evaluates | Key Metrics |
|-------|-------------------|-------------|
| **Bottom** | Foundation model performance | Model benchmarks, latency |
| **Middle** | Agent components (intent detection, reasoning, tool use, memory) | Intent correctness, tool selection accuracy, CoT grounding |
| **Upper** | End-to-end task completion + business outcomes | Goal success, safety, customer experience, cost |

Methodology uses simulation datasets of (user query, ground truth intent) pairs from anonymized historical interactions. Targets: 95% tool selection accuracy, 98% parameter extraction accuracy. A separately published Amazon paper showed that hybrid systems combining contrastively fine-tuned sentence transformers with LLMs (uncertainty-based routing) achieve "within 2% of native LLM accuracy with 50% less latency."

## Is Intent Engineering Genuinely New?

The honest answer: **the problem is real, the framework is not new, but the application domain creates genuinely new challenges.**

### Intellectual Lineage

- **OKRs and Empowered Teams** — The Product Compass framework explicitly acknowledges that intent structure "shows up in OKRs, as defined by Christina Wodtke, and in how Marty Cagan defines empowered team objectives." The objective/outcome/health-metric structure is nearly identical to a well-written OKR set with guardrail metrics.
- **BDI Agent Architecture** — Belief-Desire-Intention software model (Michael Bratman, late 1980s) has been the standard for programming intelligent agents since the 1990s. BDI separates beliefs (world knowledge — analogous to context), desires (goals — analogous to objectives), and intentions (committed plans — analogous to decision authority + stop rules). Structural parallel.
- **Design Intent in Engineering** — Manufacturing and systems engineering have used "design intent" as a governance mechanism for decades. Encoding constraints, tolerances, and acceptance criteria for non-deterministic processes is standard in civil, aerospace, and reliability engineering.

### What's Genuinely New

Three factors make the application domain meaningfully different:

1. **Agents can't ask clarifying questions the way humans can.** A human employee given vague OKRs uses social context, organizational norms, and informal conversations to fill gaps. An agent silently optimizes the wrong thing. Raises the stakes on specification completeness dramatically.
2. **Hard constraints must be enforced architecturally, not culturally.** In human organizations, many constraints are enforced through social norms, peer review, and management oversight. Intent engineering for agents requires splitting constraints into steering (encoded in prompts) and hard (enforced in orchestration code, not prompts). This is a genuine engineering discipline.
3. **The speed and scale of agent execution compresses feedback loops.** Per AgenticSE: when output explodes 100x, "the scarce resource is no longer typing; it is attention. Humans must own intent and risk boundaries." A misaligned agent can do damage at machine speed across multiple systems simultaneously.

### The Honest Assessment

Intent engineering is **existing concepts (OKRs, BDI, design intent) rigorously applied to a new class of autonomous actor that cannot rely on implicit organizational context.** The novelty is real but incremental. The term risks being dismissed as marketing if its practitioners don't acknowledge the lineage — and risks being underestimated if critics don't acknowledge that applying these frameworks to stochastic, autonomous agents requires genuine engineering discipline that doesn't yet exist in most organizations.

The most useful framing comes from the *Agentic Software Engineering* textbook, which doesn't use the term "intent engineering" at all. It calls it **"Mission Engineering"** and treats it as one of several engineering disciplines (alongside context engineering, trust engineering, coordination engineering) required to produce trustworthy software from stochastic contributors.

## Synthesis: Three Layers, One Stack

The three disciplines are not alternatives but **layers in a stack**, each solving a different class of failure:

| Layer | Solves | Without It | Implementation Artifact |
|-------|--------|------------|------------------------|
| **Prompt Engineering** | "Model doesn't understand the instruction" | Ambiguous, misformatted outputs | System prompt, few-shot examples |
| **Context Engineering** | "Model doesn't have the right information" | Hallucination, stale data, context overflow | MCP servers, RAG pipelines, CLAUDE.md, compaction strategies |
| **Intent Engineering** | "Model optimizes the wrong thing" | Misaligned autonomous behavior at scale | Mission briefs, OKR-like objective structures, hard constraint enforcement |

Prompt engineering is becoming a subset of context engineering. Context engineering is the bridge between model capability and real-world knowledge. Intent engineering is the governance layer determining whether the agent's capabilities and knowledge are directed toward the right outcomes.

**Practical implication for builders:** start with intent (what should the agent optimize?), build the context architecture (what does the agent need to know?), and let prompt engineering handle the remaining single-turn optimization within that governed framework. The teams that will build reliable agents are not the ones with the best prompts — they're the ones with the best methodology for defining agent intent and the engineering discipline to enforce it.
