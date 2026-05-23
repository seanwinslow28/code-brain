---
title: "Automation Reliability"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/2026-05-10-the-night-my-vault-said-nothing.md
tags: [auto-generated, phase-6]
created: 2026-05-23
updated: 2026-05-23
---

## Definition

The invariant that automation systems must not only function but also report their status truthfully. When an agent fails silently, it creates a hidden dependency between the user's decision-making and the system's internal health. This is especially concerning when the system's output is used as a foundation for subsequent actions, including content generation and strategic planning.

## Context

For Sean, this is critical because his daily decision-making relies on the status of his agents. If automation fails silently, it creates a feedback loop where decisions are made based on false assumptions about system health.

## Evidence

> There is a moment, somewhere around the eighth night that an automated system has been quietly producing nothing while reporting that everything is fine, when you start to wonder which of you is the real problem.

> The theme of all of it, repeated until it became a kind of liturgy, was this: evals are the new PRDs.

## Examples

- The vault synthesizer failed to produce output for nine consecutive nights while still publishing status reports as 'ok'.
- The system's ability to self-report its health is insufficient if it cannot detect or announce internal failure modes.

## Related Concepts

[[Agent Health Monitoring]] [[Eval Vocabulary]]
