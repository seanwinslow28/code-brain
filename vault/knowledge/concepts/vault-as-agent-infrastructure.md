---
title: "Vault as Agent Infrastructure"
type: concept
sources:
  - knowledge/concepts/vault-as-agent-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-06-30
updated: 2026-06-30
---

## Definition

This concept defines the vault not merely as a storage repository but as the active runtime environment for Sean's agentic fleet, where the physical location of files dictates their accessibility and backup status. The mechanism operates on the principle that consolidation into a tracked folder enables cross-machine synchronization and GitHub backup, effectively turning the file system into a stateful memory layer for autonomous agents. This infrastructure creates a hard boundary between what is ephemeral or private and what is durable and shared with the agent fleet.

## Context

Sean needs his 'Raising Claude' Substack work to be both backed up to GitHub and accessible to his agents across machines. By consolidating this work into a tracked folder, he establishes the vault as the primary interface for his agentic workflows, ensuring that the data feeding his agents is consistent and persistent.

## Evidence

> Consolidated the 'Raising Claude' Substack work into this tracked (public) folder inside code-brain, so it backs up to GitHub and syncs across machines.

> The reliance on a 'sanitized proxy' means that any agent operating on the public data lacks access to the full nuance of the original stories.

## Examples

- Moving Substack drafts into a tracked folder to ensure they are included in GitHub backups and available to agents.
- Using gitignore rules to prevent private data from entering the public agent infrastructure.

## Related Concepts

[[Privacy-Aware Data Routing]] [[Do-Not-Promote Framing]]
