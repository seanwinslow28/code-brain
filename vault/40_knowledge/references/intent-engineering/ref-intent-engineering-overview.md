---
title: "Intent Engineering — Overview & I-5 Framework"
type: reference
status: processed
domain: claude-mastery
created: 2026-02-28
ai-context: "Brief overview defining intent engineering as 'what to want' vs prompt engineering ('what to do') and context engineering ('what to know'); introduces I-5 framework, Action Schemas, and Claude Code implementation hooks (CLAUDE.md, subagents, default_to_action)."
tags:
  - reference
  - intent-engineering
  - source/pdf
  - i-5-framework
related:
  - "[[intent-engineering]]"
source-pdf: "Intent-Engineering-Overview.pdf"
---

# Intent Engineering — Overview

Intent Engineering is an emerging AI discipline focused on encoding high-level human goals, values, and decision-making hierarchies into structured parameters that autonomous agents can execute.

- **Prompt engineering** — tells AI *what to do*
- **Context engineering** — tells AI *what to know*
- **Intent engineering** — tells AI *what to want*

Bridges the gap between technical execution and organizational purpose; prevents agents from "blindly" optimizing the wrong metrics (e.g., ticket resolution speed at the expense of customer retention).

## Core Concepts and Frameworks

### The I-5 Framework

A 5-stage methodology for operationalizing intent:

1. **Intent** — Define leadership vision and constraints (Intent Charter).
2. **Interpretation** — Map user needs and system boundaries.
3. **Information** — Establish context and domain-specific truth anchors.
4. **Instruction** — Specify prompt layers and agent behavior.
5. **Implementation** — Execute through architecture, RAG, or APIs.

### Action Schemas

A small, explicit set of allowed actions for agents — ensures outcomes are automatable and aligned with implied human intent.

### Intent-First Engineering

A shift toward "spec-driven development," where human intent is captured in a living specification before any code is generated or actions are taken.

## Real-World Contexts

- **Enterprise management** — "OKRs for agents." Intent engineering provides the management infrastructure to align thousands of autonomous agents with company goals.
- **Software development** — Tools like Augment's *Intent* replace traditional IDEs with agent-orchestration platforms that use a "living spec" to coordinate multiple AI implementors.
- **Engineering design** — Historically, "design intent" referred to how 3D models (SOLIDWORKS) behave when dimensions change while preserving the original engineering rules.

## Core Technical Framework: 7-Part Specification

Intent engineering is the multi-component decision specification that governs an agent's behavior when explicit instructions run out.

1. **Objective & Desired Outcomes** — Qualitative purpose + observable success states.
2. **Health Metrics** — Signals that must not regress while pursuing the primary objective.
3. **Strategic Context** — System boundaries and trade-off priorities.
4. **Autonomy Boundaries** — Which decisions the agent may take alone, based on risk and "blast radius."
5. **Stop Rules** — Explicit conditions for halting, escalating, or terminating.
6. **Forbidden Actions** — Strictly off-limits actions.
7. **Constraints** — Steering guidance enforced through architecture rather than just prompts where possible.

## Implementation with Claude Code

Claude Code as a flexible "agent harness":

- **Custom Subagents** — Specialized workers for research, testing, or DevOps, transforming monolithic execution into orchestrated collaboration.
- **Persistent Context (CLAUDE.md)** — Houses intent specification, code styles, and workflow rules.
- **Proactive Action** — `<default_to_action>` system prompt instructs Claude to infer intent and implement changes by default rather than just suggesting them.

## Scaling to Enterprise Agentic Workflows

Focus shifts to **governance, auditability, and human-in-the-loop (HITL) orchestration**.

- **Orchestration Layer** — LangGraph for stateful workflows, CrewAI for role-based multi-agent collaboration. The orchestration layer matters more than model capability at scale.
- **Standardized Connectivity (MCP)** — Programmatically expose internal data, component libraries, and tools via Model Context Protocol.
- **Agentic Flow** — Multi-model router that automatically sends tasks to the most cost-effective model meeting quality requirements.
- **Evaluation Suites** — Treat agents as glass boxes. Build automated evaluation workflows that analyze "traces" (step-by-step reasoning) rather than only final outcomes.
