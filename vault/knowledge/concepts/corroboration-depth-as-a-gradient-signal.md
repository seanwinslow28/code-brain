---
title: "Corroboration Depth as a Gradient Signal"
type: concept
sources:
  - knowledge/concepts/corroboration-depth-as-a-gradient-signal.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

This mechanism defines the epistemic quality of a claim not by its binary truth value, but by the count and independence of corroborating domains that verify it. It establishes a tiered gradient where a single source falls below the credibility threshold, two sources constitute basic corroboration, and multiple independent sources represent the highest confidence tier. This structure allows for nuanced trust signaling in systems like D2 receipts, avoiding false positives from thin sourcing while preventing false negatives by flagging unverified claims as 'below threshold' rather than 'false'.

## Context

Sean needs to communicate evidence quality compactly in his D2 spec without overwhelming users with raw data. By mapping corroboration depth to specific tiers, he provides actionable trust signals that help users distinguish between verified facts and leads requiring further verification.

## Evidence

> a fact isn't entirely credible unless it can be verified by two sources — i.e. one source = below the corroboration threshold, two = corroborated.

> the top tier (1 = 'Credible and verified') is reserved for 'Multiple independent and trusted sources confirm'; tier 3 ('Possibly True') explicitly 'lacks corroborating evidence.'

## Examples

- A claim with one source is flagged as 'below threshold' rather than 'false', indicating a need for more data.
- A claim with multiple independent sources is elevated to the highest credibility tier, signaling high confidence to the user.

## Related Concepts

[[Citation Quality]] [[Evidence Accumulation Loop]]
