---
title: "Privacy vs. Automation in Knowledge Management"
type: connection
connects:
  - Privacy-Aware Data Routing
  - Vault as Agent Infrastructure
  - Context Management as a Bottleneck
created: 2026-06-18
updated: 2026-06-18
---

## Synthesis

The tension arises between the desire for automated knowledge synthesis and the need to protect sensitive career data. Automated agents tend to treat all data equally, flushing it into a central repository. However, job-hunt materials are private and should not be mixed with public portfolio content. This requires a deliberate architectural decision to segregate data flows based on sensitivity, rather than relying on the agent's default behavior.

## Threads

### [[Privacy-Aware Data Routing]]

> nightly synthesizer/flush still write job-hunt-derived concepts into the PUBLIC vault/knowledge/ + tickets.md over time

### [[Vault as Agent Infrastructure]]

> The LLM council transcript crash where null content caused a TypeError, preventing the write even though the run succeeded.

### [[Context Management as a Bottleneck]]

> When a synthesizer fails silently overnight, the morning brief inherits stale context, and the user notices the staleness before the brief flags the failure.

## Implications

- Sean must configure the synthesizer to route private data to a separate directory.
- The public vault should be treated as a curated portfolio, not a raw dump of all agent outputs.
