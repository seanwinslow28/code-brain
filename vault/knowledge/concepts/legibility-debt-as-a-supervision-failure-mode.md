---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-09-18
updated: 2026-09-18
---

## Definition

Legibility debt is a structural condition where automation efficacy depends on opaque, environment-specific state anchors that are invisible to standard monitoring systems. This creates a divergence between operational uptime and semantic value, as the system appears functional while relying on manual interventions that degrade over time. The supervisor cannot detect this drift because the failure mode exists external to the agent's logic, requiring human intervention to maintain the illusion of autonomy.

## Context

Sean's fleet relies on hidden environment variables and file paths to function correctly. When these anchors break, the cost of recovery is high because the root cause is not in the code but in the unmanaged state of the host machine. This makes the system fragile despite its apparent robustness.

## Evidence

> sweep works live today only because ~/.config/last30days/.env holds AUTH_TOKEN/CT0 written by the last30days setup wizard on 2026-06-08

> When that session rotates there is no fallback: Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

## Examples

- The reliance on a specific .env file created by a setup wizard rather than a persistent configuration management system.
- Browser-specific failures where Safari requires Full Disk Access and Chrome throws numeric representation errors.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Operational Uptime vs. Semantic Value in Agent Fleets]]
