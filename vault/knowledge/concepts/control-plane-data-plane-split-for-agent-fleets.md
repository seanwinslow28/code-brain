---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/expansions/agent-ops-fdp-backup-track.md
tags: [auto-generated, phase-6]
created: 2026-06-03
updated: 2026-06-03
---

## Definition

This architectural invariant separates the agent system into two distinct layers: the control plane, which manages scheduling, authorization, and halting logic, and the data plane, where agents execute specific tasks like reading vault artifacts or generating summaries. This separation allows the control layer to remain stable and observable while the data layer handles variable workloads and transient state mutations. By isolating these concerns, operators can apply different reliability guarantees to each layer, ensuring that the decision-making logic for agent lifecycle does not become entangled with the execution logic of individual agent runs.

## Context

Sean is building a personal AI infrastructure that needs to be robust enough for professional demonstration. Currently, his agents likely mix scheduling logic with execution logic, making it difficult to diagnose failures or scale the system. Defining this split provides a clear mental model for interview whiteboard artifacts and helps structure the underlying codebase for maintainability.

## Evidence

> distinguish the control plane that schedules, routes, authorizes, observes, and halts agents from the data plane where agents actually read/write vault artifacts, run research, generate summaries, or mutate files.

> I built a local agent control plane over launchd, file manifests, cost caps, health checks, and Obsidian-Git boundaries.

## Examples

- Using launchd to manage the lifecycle of agent processes (control plane) while the agents themselves read and write to Obsidian vault files (data plane).

## Related Concepts

[[Agent Fleet Observability Dashboard]] [[Infrastructure Status]]
