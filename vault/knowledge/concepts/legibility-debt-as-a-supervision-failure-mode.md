---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - health/private/2026-07-26-private-findings.md
tags: [auto-generated, phase-6]
created: 2026-09-04
updated: 2026-09-04
---

## Definition

The accumulation of unstructured or hidden data that escapes automated monitoring because it resides outside the observable control plane. This debt grows when private or gitignored subtrees are used for critical context, creating blind spots where semantic decay can occur without triggering alerts. The supervisor loses visibility into the actual state of the system, relying on incomplete proxies for health.

## Context

Sean’s use of gitignored private folders for sensitive findings creates a structural blind spot. While it protects privacy, it prevents the automated linting agents from verifying the integrity of those specific insights, leading to a false sense of completeness in the public vault.

## Evidence

> LOCAL-ONLY. Gitignored (vault/health/private/). Each finding below either quotes vault/05_atlas/operating-models/ SOUL text or names a file in a gitignored subtree

> 302 finding(s) withheld from this tracked report (SOUL-derived, or about a file in a gitignored subtree).

## Examples

- Withheld findings regarding 'soul-tier-a-conflict' in accountability-gap.md
- Private-subtree findings omitted from the 2026-08-23-lint-report

## Related Concepts

[[Knowledge-Lint]] [[Operational Visibility vs. Semantic Value in Agent Fleets]]
