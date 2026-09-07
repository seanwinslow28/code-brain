---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/fragile-anchors-and-the-cost-of-hidden-dependencies.md
tags: [auto-generated, phase-6]
created: 2026-09-07
updated: 2026-09-07
---

## Definition

Legibility debt emerges when system reliability depends on opaque, environment-specific workarounds that are invisible to standard monitoring. This debt grows silently because the system appears operational while masking the fragility of its dependencies. When these hidden anchors fail, they cause catastrophic supervision failures because the root cause is not in the logic but in the unmanaged external state.

## Context

Sean's agent fleet relies on specific browser quirks and local file paths to function. This creates a high risk of silent failure where the system looks healthy but cannot perform its core tasks due to missing credentials or incompatible environments.

## Evidence

> When that session rotates there is no fallback: Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

> x/stimulus.py sweep works live today only because ~/.config/last30days/.env holds AUTH_TOKEN/CT0 written by the last30days setup wizard on 2026-06-08

## Examples

- Safari returning EPERM due to missing Full Disk Access
- Chrome throwing a JavaScript number representation error on WebKit cookie timestamps
- Reliance on ~/.config/last30days/.env for authentication tokens

## Related Concepts

[[Operational Uptime vs. Semantic Value in Agent Fleets]] [[The Illusion of Competence in Automated Systems]]
