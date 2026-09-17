---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/hidden-environmental-dependencies-create-fragile-automation-anchors.md
tags: [auto-generated, phase-6]
created: 2026-09-17
updated: 2026-09-17
---

## Definition

Legibility debt emerges when automation relies on opaque, environment-specific workarounds that are invisible to standard monitoring. This creates a state where the system appears functional but depends on manual anchors that degrade over time. The supervisor cannot detect the drift because the failure mode is external to the agent's logic, requiring human intervention to maintain the illusion of autonomy.

## Context

Sean's fleet relies on hidden environment variables and file paths to function. When these anchors break, the cost of recovery is high because the root cause is not in the code but in the unmanaged state of the host machine.

## Evidence

> sweep works live today only because ~/.config/last30days/.env holds AUTH_TOKEN/CT0 written by the last30days setup wizard on 2026-06-08

> When that session rotates there is no fallback: Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

## Examples

- The reliance on a specific .env file created by a setup wizard rather than a persistent configuration management system.
- Browser-specific failures where Safari requires Full Disk Access and Chrome throws numeric representation errors.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Operational Uptime vs. Semantic Value in Agent Fleets]]
