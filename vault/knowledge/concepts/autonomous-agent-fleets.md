---
title: "Autonomous Agent Fleets"
type: concept
sources:
  - knowledge/concepts/autonomous-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-05-23
updated: 2026-05-23
---

## Definition

A distributed architecture where multiple autonomous agents operate in coordination, each with discrete responsibilities but interdependent via shared state or output. The system's reliability depends on agents' ability to read and write consistent, persistent context — such as daily notes or task states. Failures in one agent's ability to read or write context can propagate silently, causing downstream agents to act on stale data without awareness of the error.

## Context

Sean's workflow depends on a network of autonomous agents, including launchd SDK agents and Claude Code subagents, which operate in coordination but are vulnerable to propagation of errors when one agent fails silently without updating shared context.

## Evidence

> The core philosophy is a four-tool harness (Read, Write, Edit, Bash) with a first-class extension system that allows the agent to extend itself by writing and hot-reloading TypeScript modules.

> The npm package was migrated from `@mariozechner/pi-coding-agent` to `@earendil-works/pi-coding-agent` in May 2026. Version `0.73.1` was the last release under the old scope; `0.74.0+` publishes under `@earendil-works`.

## Examples

- A Pi agent may read a daily note to determine the user’s current task and then generate code. If that agent fails silently and does not update the note, a downstream agent may execute outdated instructions without Sean's awareness.

## Related Concepts

[[Agent Health Monitoring]] [[Daily Note Generators]]
