---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-12
updated: 2026-06-12
---

## Definition

This pattern describes the fragile dependency between an operating system's binary integrity verification (such as macOS code-signing checks) and the agent's execution environment. When a package manager upgrades a core interpreter, it alters the binary's cryptographic hash, causing the process supervisor to reject the existing launch configuration as invalid. The mechanism fails not because the logic is wrong, but because the runtime identity has shifted without updating the supervisor's cached state.

## Context

Sean's agent fleet relies on Homebrew-managed Python interpreters for execution. A routine upgrade invalidated the launchd cache for five critical jobs, causing them to be kernel-killed overnight. This creates a silent failure mode where the knowledge loop breaks because the infrastructure assumes static binary paths rather than dynamic runtime identities.

## Evidence

> the 2026-06-10 13:31 Homebrew python@3.13 reinstall (3.13.11→3.13.13_1) changed the interpreter cdhash, which invalidated launchd's cached LWCR for 5 jobs

> every fire on 2026-06-11 was kernel-killed with OS_REASON_CODESIGNING (no daily note, no overnight knowledge loop)

## Examples

- launchd's cache was stale

## Related Concepts

[[Automation Failure and Daily Note Disruption]] [[Infrastructure Status]]
