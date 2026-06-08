---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 40_knowledge/references/ref-system-design-114-concepts-part-3.md
tags: [auto-generated, phase-6]
created: 2026-06-08
updated: 2026-06-08
---

## Definition

This pattern describes the structural dependency where an application's deployment and operational runtime are inextricably bound to a specific vendor's proprietary infrastructure, creating a high-friction exit barrier. When developers build within a closed ecosystem, they prioritize integration with that platform's native services over portable architecture, effectively trading long-term architectural flexibility for short-term development velocity. The resulting system becomes fragile because any change in the vendor's pricing, API stability, or strategic direction forces a complete re-architecture rather than a simple configuration update.

## Context

Sean is actively evaluating 'Orchids' as an alternative to locked-in stacks like Supabase or Stripe. Understanding this coupling helps him recognize why 'one-click deployment to Vercel' and 'bring your own AI subscriptions' are not just features but critical risk mitigations for his career mobility and project longevity.

## Evidence

> You live inside their box, choose from their secret stack, and force you to start over the moment you want to use a different database, payment processor, or tool.

> Not forced to spend credits, bring your own AI subscriptions with you.

## Examples

- Forcing a switch from Supabase to a self-hosted PostgreSQL instance requires rewriting data access layers because the original code assumed Supabase-specific authentication and real-time subscriptions.
- Migrating payment logic from Stripe's hosted checkout to a custom processor requires rebuilding the entire webhook handling and reconciliation system.

## Related Concepts

[[Abstraction Layer Shift]] [[Infrastructure Status]]
