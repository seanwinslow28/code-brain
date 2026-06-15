---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - 00_inbox/tickets.md
tags: [auto-generated, phase-6]
created: 2026-06-12
updated: 2026-06-12
---

## Definition

This mechanism addresses the tension between automated synthesis capabilities and data classification boundaries. When an agent fleet processes mixed inputs, it tends to normalize all outputs into a single public knowledge base unless explicit exclusion rules are enforced. The pattern requires a deliberate filtering layer that routes career-specific or personal-derived concepts away from public-facing indexes to prevent accidental exposure of sensitive professional strategies.

## Context

Sean's vault synthesizer currently writes job-hunt-derived concepts into the public vault/knowledge/ directory. This creates a privacy risk where professional search strategies become permanently indexed and accessible, violating the separation between his public creative output and private career activities.

## Evidence

> nightly synthesizer/flush still write job-hunt-derived concepts into the PUBLIC vault/knowledge/ + tickets.md over time

> add a privacy-aware exclusion (route career/personal-derived concepts to vault/knowledge/private/) or schedule a periodic prune pass

## Examples

- route career/personal-derived concepts to vault/knowledge/private/

## Related Concepts

[[Vault as Agent Infrastructure]] [[Cross-domain bridging]]
