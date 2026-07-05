---
title: "Vault as Agent Infrastructure"
type: concept
sources:
  - knowledge/concepts/vault-as-agent-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism defines the vault not merely as a storage repository but as the active, synchronized substrate that agents consume to generate insights. It establishes a dependency where the integrity of the public-facing data directly dictates the quality and safety of agentic outputs. The infrastructure relies on git-backed synchronization to ensure that the agent's context window is always aligned with the latest verified state of Sean's knowledge base. This creates a rigid coupling between the physical file structure and the logical flow of information, where any structural change in the vault requires corresponding updates in the agent's routing logic.

## Context

Sean uses this infrastructure to manage his 'Raising Claude' Substack series, ensuring that sensitive narratives are backed up to GitHub while remaining accessible to agents through a sanitized layer. The reliance on this synchronized state means that any failure in the sync process or the sanitization script can disrupt the entire agentic workflow.

## Evidence

> Consolidated the 'Raising Claude' Substack work into this tracked (public) folder inside code-brain, so it backs up to GitHub and syncs across machines.

> The consequence is a dependency on automated verification scripts to ensure the proxy remains clean, creating a fragile system where any scrubbing failure could lead to privacy leakage or loss of context.

## Examples

- Sean's workflow is defined by a fundamental tension between the need for rich, personal data to fuel creative insights and the requirement to isolate that same data to protect privacy.
- The reliance on a 'sanitized proxy' means that any agent operating on the public data lacks access to the full nuance of the original stories.

## Related Concepts

[[Privacy-Aware Data Routing]] [[Silent Failure Propagation in Agent Fleets]]
