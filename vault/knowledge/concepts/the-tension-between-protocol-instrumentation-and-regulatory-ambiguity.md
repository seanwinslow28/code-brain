---
title: "The Tension Between Protocol Instrumentation and Regulatory Ambiguity"
type: concept
sources:
  - 20_projects/substack-studio/06-stop-building-agents/post.md
tags: [auto-generated, phase-6]
created: 2026-06-23
updated: 2026-06-23
---

## Definition

A structural conflict where the need for precise, deterministic routing rules (protocol) clashes with the ambiguous, probabilistic nature of LLM outputs (regulatory ambiguity). When agents are tasked with complex ecosystem mapping, they lack a hard constraint to verify existence, leading them to invent protocols that satisfy the syntactic structure of the request without adhering to semantic truth. This tension forces a shift from trusting agent autonomy to enforcing deterministic validation layers, as the cost of maintaining 'agent-shaped solutions for automation-shaped jobs' becomes unsustainable.

## Context

Sean is building an 'Agent-or-Automation Advisor' to solve this exact problem. He recognizes that his current fleet uses agents where simple routing rules would suffice, leading to maintenance burdens and hallucinations. This concept defines the core architectural pivot: moving from probabilistic agents to deterministic routers to eliminate the ambiguity that causes fabrication.

## Evidence

> The fix was a deterministic route, not a smarter agent; the hook pivot for Post 6 'Stop Building Agents' is that the maintenance burden kills automations with LLM nodes.

> I ran a tool on my own fleet and it told me 9 of my 14 agents are automations in a trench coat.

## Examples

- Sean's decision to pivot from 'The Day My Research Agent Invented Microsoft' to 'Stop Building Agents' reflects the realization that better models don't fix bad architectures.
- The creation of the 'Agent-or-Automation Advisor' build spec as a direct response to the fleet audit revealing excessive agent usage.

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Automation Reliability]]
