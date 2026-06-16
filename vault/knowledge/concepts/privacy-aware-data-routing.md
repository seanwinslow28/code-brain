---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-16
updated: 2026-06-16
---

## Definition

This mechanism addresses the tension between automated knowledge synthesis and data sovereignty. When an agent fleet processes mixed inputs (public project docs vs. private career strategy), a lack of explicit routing rules causes sensitive, job-hunt-derived concepts to leak into public-facing vault directories. The system treats all markdown files as equal knowledge assets unless a privacy filter explicitly distinguishes their origin, leading to accidental exposure of personal strategic data in public indexes.

## Context

Sean is actively managing his job hunt (job-hunt-2026) while maintaining a public open-source presence. The current synthesizer writes all derived concepts into the same public `vault/knowledge/` folder. This creates a risk where private career strategies or interview preparations become discoverable via public repo searches, violating the separation between his professional brand and personal job-search tactics.

## Evidence

> nightly synthesizer/flush still write job-hunt-derived concepts into the PUBLIC vault/knowledge/ + tickets.md over time

> add a privacy-aware exclusion (route career/personal-derived concepts to vault/knowledge/private/) or schedule a periodic prune pass

## Examples

- Route career/personal-derived concepts to vault/knowledge/private/
- Schedule a periodic prune pass for job-hunt data

## Related Concepts

[[Vault as Agent Infrastructure]] [[Privacy-Aware Data Routing]]
