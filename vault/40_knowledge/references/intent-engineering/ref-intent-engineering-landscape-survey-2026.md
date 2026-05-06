---
title: "Intent Engineering for AI Agents — Landscape Survey (Early 2026)"
type: reference
status: processed
domain: claude-mastery
created: 2026-02-28
ai-context: "Snapshot of the intent engineering landscape as of February 2026 — covers two dedicated platforms (Pathmode + Augment Intent), agent orchestration frameworks (LangGraph, CrewAI, ADK, Claude Agent SDK, Agent Teams), interoperability protocols (MCP + A2A under Linux Foundation), evaluation/observability tools (Braintrust, LangSmith, Arize AX, Langfuse), academic research (Knight Institute's autonomy levels, AgenticSE textbook), and key voices (Huryn, Nate B. Jones, IBM)."
tags:
  - reference
  - intent-engineering
  - source/pdf
  - landscape
  - pathmode
  - augment-intent
related:
  - "[[intent-engineering]]"
source-pdf: "Intent-Engineering-Landscape.pdf"
---

# Intent Engineering for AI Agents — Landscape Survey (Early 2026)

Intent engineering is emerging as a distinct discipline at the intersection of product management, software engineering, and AI agent design. Rather than telling agents *what to do* step by step, intent engineering specifies *what success looks like* — objectives, outcomes, constraints, and decision authority — so agents can reason autonomously within defined boundaries.

As of February 2026, the landscape includes:
- Two dedicated platforms (Pathmode + Augment Intent)
- A growing ecosystem of agent orchestration frameworks
- Two major interoperability protocols (MCP + A2A) under Linux Foundation governance
- Evaluation tools moving toward trace-based reasoning analysis
- Early academic formalization
- A small but vocal community of practitioners

No single standard has won, but the pieces are assembling rapidly.

## Dedicated Intent Engineering Platforms

### Pathmode

First platform purpose-built for intent engineering, turning raw user feedback (support tickets, interview quotes, analytics) into structured specifications AI coding agents can execute. Core innovation: **IntentSpec** — an open standard at intentspec.org using Markdown with YAML frontmatter and a formal JSON Schema for validation.

**The IntentSpec has five parts:**
1. Objective — The problem being solved and why it matters
2. User Goal — What the user wants to achieve
3. Outcomes — Measurable success states
4. Edge Cases — Boundary conditions and error states
5. Verification — Specific test cases and acceptance criteria

IntentSpec is explicitly open and format-agnostic: specs can be written by hand in any text editor and consumed by any LLM or agent tool. Pathmode differentiates from AGENTS.md files by offering machine-readable structure with automated CI/CD validation, rather than unstructured text with no formal verification.

In February 2026, Pathmode shipped the **Intent Compiler for Claude Code** — a zero-config MCP tool that turns Claude Code into a Socratic product thinking partner. It asks pointed questions, challenges vague language, and builds a structured intent spec through conversation. When ready, it saves an `intent.md` file and optionally exports as `.cursorrules` or `CLAUDE.md`. The MCP server (`@pathmode/mcp-server@1.2.2`) works without an API key for compiler tools; team features (dependency graphs, workspace strategy, governance) activate with a key.

**Pricing:** Free tier ($0/month starting), with subscription for team features. IntentSpec itself is fully open with no vendor lock-in.

**Claude Code compatibility:** Direct — the Intent Compiler is an MCP server designed specifically for Claude Code, and IntentSpec files work natively as CLAUDE.md context.

### Intent by Augment Code

Augment's *Intent* is a developer workspace designed as "what comes after the IDE" — a coordinated environment for orchestrating multiple AI agents. Launched in public beta in February 2026 for macOS (Windows waitlist).

Architecture works through a structured agent team:
- **Coordinator agent** uses Augment's Context Engine to understand the task and propose a plan as a spec
- **Implementor agents** execute work in parallel within isolated git worktrees
- **Verifier agent** checks results against the spec before returning work for human review

Key differentiator: the **living spec** — a specification that evolves as agents make progress. Unlike static prompts that go stale, the spec is a shared document that agents read from and update, keeping all participants aligned as plans change. Full git workflow integration means developers can go from prompt to commit to PR to merge without leaving the app.

Intent supports BYOA (Bring Your Own Agent): while optimized for Augment's own agent ("Auggie"), it also works with Claude Code, Codex, and OpenCode. Credits charged at the same rate as the Augment CLI. Augment recommends installing their Context Engine MCP for developers using other agents.

**Claude Code compatibility:** Supported as a BYOA provider. Claude Code sessions can run within Intent workspaces, benefiting from the coordinated spec and workspace isolation.

### Other Tools With Intent Positioning

- **OpenSpec** — Spec-driven development architecture addressing context loss in agent-driven workflows; lower visibility than Pathmode or Intent.
- **IBM's Objective-Validation Protocol** — Emerging concept articulated by Ismael Faro of IBM Research, describing a shift "from vibe coding to Objective-Validation Protocol" where users define goals, agents execute autonomously, and humans approve at critical checkpoints. IBM frames this as the foundation for an "Agentic Operating System (AOS)." Conceptual framework rather than a shipping product as of February 2026.

## Agent Orchestration Frameworks

| Framework | Intent Approach | Orchestration Model | Claude Code Compatible |
|-----------|----------------|---------------------|------------------------|
| **LangGraph** | Graph-based state machines; intent encoded in node/edge structure and state transitions | Directed graph with conditional branching | Via LangChain integrations |
| **CrewAI** | Role-based; intent expressed through agent role definitions and task descriptions | Role assignment with Flows for workflow control | Via tool integrations |
| **Google ADK** | Hierarchical delegation; intent in agent role descriptions and routing logic | Multi-agent hierarchy with LLM-driven routing | Via LiteLLM adapter |
| **Claude Agent SDK** | System prompts and tool permissions; intent as conversational context | Single agent with subagent spawning | Native — wraps Claude Code CLI |
| **Agent Teams** | Shared task list and messaging; intent set by team lead, refined through collaboration | Full mesh multi-agent with team lead | Native — experimental Claude Code feature |

### LangGraph

Models agent workflows as directed graphs where nodes represent processing steps and edges define transitions. Intent is essentially structural: the graph topology itself encodes what should happen, in what order, and under what conditions. Provides maximum control — developers can define human-in-the-loop pause/resume hooks within workflow graphs — but requires the intent to be pre-decomposed into graph logic. Best for enterprise applications requiring strict state management and audit trails.

### CrewAI

Organizational metaphor: agents are assigned roles with specific responsibilities, mimicking team structures. Intent expressed through role definitions ("You are a researcher responsible for...") and task descriptions, making it intuitive for PMs. CrewAI's Flows feature adds event-driven pipeline control alongside autonomous Crews. Trade-off: less fine-grained control over state transitions compared to LangGraph.

### Google Agent Development Kit (ADK)

Open-sourced at Cloud NEXT 2025. Multi-agent hierarchies where agents delegate tasks based on context and capability. Intent encoded through agent role descriptions and routing logic — a root agent dynamically routes requests to specialist sub-agents based on content. Combines deterministic workflow agents with LLM-driven routing; native A2A protocol support. Available in Python, Go, and Java.

### Anthropic's Claude Agent SDK

Anthropic's official Python toolkit for building agents on top of Claude Code. Released alongside Claude Sonnet 4.5; provides async streaming, custom tools via in-process MCP servers, hook system for injecting logic before/after tool execution, and fine-grained permission control. Intent is specified through system prompts, tool availability, and permission boundaries — the same infrastructure that powers Claude Code, exposed for custom development. Wraps the Claude Code CLI as a subprocess (CLI bundled in the package).

### Claude Code Agent Teams

Experimental feature coordinating multiple Claude Code sessions. One acts as **team lead** (understanding the big picture, delegating, synthesizing), while multiple **teammate sessions** operate as full independent Claude Code instances with their own context windows. Intent flows through a shared task list and direct mailbox — any teammate can message any other without routing through the lead.

Communication model is **full mesh** rather than hub-and-spoke, making Agent Teams best suited for collaborative exploration, research, debugging with competing hypotheses, and cross-layer coordination. Enabled via `experimental.agentTeams: true`. Higher token costs since each teammate is a separate Claude instance.

## Standards and Protocols

### Model Context Protocol (MCP)

Introduced by Anthropic November 2024, has rapidly become the universal standard for connecting AI models to tools, data, and applications. With 10,000+ published MCP servers and adoption across Claude, Cursor, VS Code, ChatGPT, Gemini, and Microsoft Copilot, MCP provides the connective tissue that makes intent engineering practical.

In December 2025, Anthropic donated MCP to the **Agentic AI Foundation (AAIF)** under the Linux Foundation, alongside Block's Goose and OpenAI's Agents.md. The protocol's specification (latest: 2025-06-18) defines servers exposing Resources (context/data), Prompts (templated workflows), Tools (executable functions), Sampling (server-initiated LLM interactions), Roots (filesystem boundaries), and Elicitation (user information requests).

For intent engineering, MCP serves as the **delivery mechanism** rather than the specification layer. Pathmode's IntentSpec, for example, can be delivered to agents as MCP context. **MCP enables intent but does not define it** — there is currently no intent-specific schema within the MCP specification itself.

### Agent-to-Agent Protocol (A2A)

Google's A2A protocol, announced April 2025 and contributed to the Linux Foundation in June 2025, addresses inter-agent communication — how agents discover capabilities, exchange information, and coordinate actions. Over 100 technology partners support A2A including Atlassian, Salesforce, ServiceNow, and LangChain.

A2A uses **Agent Cards** (JSON format) for capability discovery, supports task management with defined lifecycle states, and enables agent-to-agent collaboration via context and instruction sharing. Designed to complement MCP: MCP connects agents to *tools*, A2A connects agents to *each other*. Built on HTTP, SSE, and JSON-RPC.

Adoption has been slower than MCP's rapid uptake. IBM's Agent Communication Protocol (ACP), launched March 2025, has since merged with A2A under the Linux Foundation, consolidating the agent-to-agent protocol space.

### Emerging Intent Standards

No widely adopted standard specifically for intent specification as of February 2026. The closest candidates:

- **IntentSpec (Pathmode)** — Open, JSON Schema-validated, Markdown-based; the most formalized intent specification format available
- **IBM's Objective-Validation Protocol** — Conceptual framework for goal-setting and checkpoint validation
- **Agents.md (OpenAI, now in AAIF)** — Unstructured agent context files that carry intent but lack formal validation

The gap between MCP (tool connectivity) and A2A (agent communication) leaves intent specification as an unfilled layer in the protocol stack. Whether IntentSpec or a competing format fills this gap remains an open question.

## Evaluation and Observability

### Trace-Based Evaluation

Major shift from evaluating agent *outputs* to evaluating agent *reasoning*. Leading platforms now capture full decision traces — every prompt, model output, tool call, and intermediate reasoning step — enabling developers to understand not just *what* an agent did but *why*.

| Platform | Approach | Best For |
|----------|----------|----------|
| **Braintrust** | Evaluation-first with comprehensive traces; nested spans across multi-agent workflows; automated scoring | Teams needing integrated eval + observability |
| **LangSmith** | Step-by-step inspection of decision paths; run replay and comparison; tight LangChain integration | LangChain-based agent debugging |
| **Arize AX** | SDK-based "decision-level" visibility showing how internal state changes between tool calls | Mission-critical agents requiring deep reasoning visibility |
| **Langfuse** | OpenTelemetry-compatible traces with cost/latency tracking; sequential chain visualization | Teams optimizing performance and spend |

These tools collectively enable **intent alignment monitoring** — checking whether an agent's reasoning chain stays aligned with its specified objectives. Braintrust supports configurable evaluation scores that trigger alerts when quality degrades.

### Amazon's LLM Simulator for Intent Detection

Amazon developed an LLM simulator for evaluating customer service agent intent detection accuracy. Uses LLM-driven virtual customer personas to simulate diverse scenarios, then compares the agent's detected intent against ground truth from anonymized historical interactions.

Multi-layer evaluation:
- **Intent correctness** — Does the orchestration agent understand user intents correctly?
- **Task completion** — Does the agent's final response resolve the customer's issue?
- **Multi-turn coherence** — Topic adherence classification and refusal metrics
- **Tool use accuracy** — Correct tool selection, parameter accuracy, multi-turn function calling sequence

Represents a broader industry shift toward evaluating agents as complete systems rather than isolated models, with intent detection accuracy as a first-class metric.

### Instruction Adherence as a Metric

Salesforce predicts that instruction adherence will become a key reliability metric in 2026, with enterprises demanding "probabilistic adherence scores — categorized as high, low, or uncertain — to enable developers to refine their instructions accordingly." This framing treats intent specification as something that can be quantitatively measured against agent behavior, moving intent engineering from art toward measurable discipline.

## Academic Research

### "Human Delegation Behavior in Human-AI Collaboration" (arXiv:2401.04729)

Spitzer et al. (January 2024, revised January 2025), frequently cited in the intent engineering community — notably by Paweł Huryn — as evidence that providing contextual information significantly improves human-AI team performance. The study found that access to contextual information about both the AI's capabilities *and* the task domain changes delegation behavior and improves collaborative outcomes. While the paper focuses on human delegation rather than agent specification per se, the finding that **context beyond raw task specifications improves autonomous performance** has become a foundational reference.

### "Levels of Autonomy for AI Agents" (Columbia / Knight Institute)

Defines five escalating autonomy levels characterized by user roles: **Operator, Collaborator, Consultant, Approver, and Observer**. Key argument: autonomy should be a **deliberate design decision** separate from agent capability — a capable agent can still be designed to operate at low autonomy if it must consult its user before each action. Proposes **autonomy certificates** as a governance mechanism.

### *Agentic Software Engineering* Textbook

Available as a free PDF at agenticse-book.github.io. Defines Agentic Software Engineering as "the discipline of producing high-quality, reliable, trustworthy software from stochastic contributors, both AI and human." Thesis: "Success belongs to teams who set clear intent, manage risk boundaries, and demand evidence — not just those who type fastest."

Frames itself as "the missing manual that did not come with your agentic coding tools, including Claude Code." Addresses four pillars of engineering (people, process, tools, artifacts) rather than just coding techniques. Emphasizes that intent specification is necessary precisely because AI teammates are stochastic — they fail with some probability, requiring constraint-based engineering to achieve trusted reliability.

### Intent-Based System Design and Operation (arXiv:2502.05984)

February 2025 paper proposing intent as a new abstraction within the context of system design and operation, encoding functional and operational requirements at a high level to automate design, implementation, operation, and evolution of systems. Broader than AI agent intent engineering but formalizes many of the same concepts.

## Community and Discourse

### Key Voices

**Paweł Huryn** — Most systematic voice on intent engineering for AI agents. Product Compass newsletter (119K+ subscribers) published "The Intent Engineering Framework for AI Agents" in January 2026, defining the seven-element structure. His framing — "context without intent is noise" — has become a touchstone for the community. Huryn's formulation bridges product management (OKRs, empowered teams) with agent engineering, drawing explicitly on arXiv:2401.04729 and concepts from military *Auftragstaktik* (commander's intent). Emphasizes that intent engineering is not about more detailed instructions, but about giving agents the reasoning framework to handle unknowns.

**Nate B. Jones** — Substack newsletter ("Nate's Substack" / "AI News & Strategy Daily") focused on AI strategy and practical implementation. Content covers agent UI surfaces, intent-state-outcome loops, and predictions around memory breakthroughs and long-running agents. Emphasizes execution over tooling; published guides on agent architecture, multi-agent orchestration, and context engineering.

**The Agentic SE Book authors** (agenticse-book.github.io) — Contribute the academic engineering perspective, arguing that intent clarity is the foundation of trustworthy agentic development.

**IBM researchers** (particularly Ismael Faro and Maryam Ashoori) — Shaping the enterprise perspective with concepts like the Objective-Validation Protocol and predictions about 2026 as "the year of operating AI agents at scale."

### Newsletters and Communities

| Resource | Focus | Author/Org |
|----------|-------|-----------|
| The Product Compass | Intent engineering frameworks, context engineering, AI PM | Paweł Huryn |
| Nate's Substack | AI strategy, agent architecture, practical playbooks | Nate B. Jones |
| r/AugmentCodeAI | Agent orchestration, Intent workspace discussion | Reddit community |
| ClaudeFast blog | Claude Code Agent Teams guides, team orchestration patterns | Community guides |
| IBM Think / IBM Research Blog | Super agents, ACP/A2A protocol development, enterprise agentic AI | IBM |

### Forming Reading List

Canonical reading list not yet established, but the emerging syllabus:
- Huryn's "Intent Engineering Framework for AI Agents" and "Context Engineering" posts
- arXiv:2401.04729 on contextual information in human-AI delegation
- "Levels of Autonomy for AI Agents" (Columbia/Knight)
- *Agentic Software Engineering* textbook
- IntentSpec documentation at intentspec.org
- Anthropic's MCP specification
- Amazon's agent evaluation blog on intent detection with LLM simulators
- arXiv:2502.05984 on intent-based system design

## Landscape Assessment

### What Exists Today

The intent engineering landscape in early 2026 is fragmented but directional. Two dedicated platforms (Pathmode + Augment Intent) have shipped products, one open standard (IntentSpec) is available with CI/CD validation, one conceptual framework (Huryn's 7-element structure) provides a practitioner vocabulary. The protocol stack (MCP for tools, A2A for agents) is maturing under Linux Foundation governance but lacks an intent-specific layer.

### What's Missing

- **No universal intent schema** — IntentSpec is the closest, but adoption beyond Pathmode's ecosystem is nascent
- **No runtime intent enforcement** — Most intent specifications operate at the prompt layer; hard enforcement remains a custom engineering problem
- **No cross-framework intent portability** — An IntentSpec written for Claude Code doesn't automatically work as a CrewAI crew definition or a LangGraph state machine
- **Limited evaluation tooling for intent alignment** — Trace-based tools monitor reasoning but don't systematically compare agent behavior against intent specifications
- **Sparse academic formalization** — The concept is referenced in industry but has no dedicated peer-reviewed research program

### Trajectory

The convergence of trends suggests intent engineering will solidify rapidly: the shift from "vibe coding" to structured development (IBM's framing), the maturation of agent orchestration frameworks needing better specification inputs, the growing observability stack that can measure intent adherence, and the professional community forming around Huryn's framework and Pathmode's tools.

For anyone building with Claude Code today, the practical action: adopt IntentSpec files (`intent.md`) as project artifacts alongside CLAUDE.md, and treat intent specification as a first-class product skill rather than an afterthought.
