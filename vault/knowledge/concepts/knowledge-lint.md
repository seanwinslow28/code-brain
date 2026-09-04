---
title: "Knowledge-Lint"
type: concept
sources:
  - health/private/2026-07-12-private-findings.md
tags: [auto-generated, phase-6]
created: 2026-09-04
updated: 2026-09-04
---

## Definition

A continuous verification mechanism that compares the structural integrity of a knowledge graph against its source material and internal consistency rules. This process identifies broken references, semantic drift, and policy violations by scanning for mismatches between linked entities and their actual existence or content. The system acts as a diagnostic layer that exposes the gap between the intended architecture of the vault and its realized state, flagging issues like stale links or conflicting definitions before they compound into systemic confusion.

## Context

Sean's vault has grown to include thousands of files across multiple domains. Without automated linting, the cognitive load of maintaining referential integrity would become unmanageable, leading to 'legibility debt' where the system becomes harder to navigate than manual notes. This concept is critical for preserving the utility of the vault as a second brain.

## Evidence

> Each finding below either quotes `vault/05_atlas/operating-models/` SOUL text or names a file in a gitignored subtree — both private under CLAUDE.md rule 9.

> 1112 issues found (932 structural, 180 semantic).

> 265 finding(s) withheld from this tracked report (SOUL-derived, or about a file in a gitignored subtree).

## Examples

- broken-wikilink (T1): `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/README.md` — onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log
- soul-tier-a-conflict (T2): `knowledge/concepts/accountability-gap.md` — tier_a_item="SOUL — Creative Studio: 'Creative taste is Sean's, always. 90/10 delegation.' / 'Create for our"

## Related Concepts

[[Legibility Debt as a Supervision Failure Mode]] [[Infrastructure Fragmentation and Semantic Isolation]]
