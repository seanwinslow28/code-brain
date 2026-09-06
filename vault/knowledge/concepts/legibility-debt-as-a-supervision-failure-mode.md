---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-09-06
updated: 2026-09-06
---

## Definition

Legibility debt emerges when the structural complexity of an automated system outpaces the human operator's ability to verify its state through standard observability channels. This creates a dependency on fragile, manual workarounds—such as specific credential files or browser profiles—to maintain operational continuity. When these manual anchors fail or rotate, the system does not degrade gracefully but instead produces opaque errors that require deep forensic investigation rather than simple remediation, effectively hiding the true cost of automation from the operator until a critical failure occurs.

## Context

Sean is currently managing a complex agent fleet where the 'X' sweep relies on a stale credential file written by a setup wizard. The lack of a robust fallback mechanism means that routine session rotations can break core functionality, forcing Sean to manually intervene or accept broken states. This debt accumulates silently as he patches around these issues rather than addressing the underlying architectural fragility.

## Evidence

> When that session rotates there is no fallback: Safari returns EPERM on Cookies.binarycookies (no Full Disk Access), Firefox has no profile, and Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp

> The machine does not pick them — which sentence is the line is his judgment, and a machine guessing would fill the ledger with lines he never rat

## Examples

- Safari returns EPERM on Cookies.binarycookies due to lack of Full Disk Access
- Chrome's reader throws Value is too large to be represented as a JavaScript number on a WebKit cookie timestamp
- The loader ignores fenced blocks so the file's own example cannot arm it with a line nobody wrote

## Related Concepts

[[Operational Uptime vs. Semantic Value in Agent Fleets]] [[The Illusion of Competence in Automated Systems]]
