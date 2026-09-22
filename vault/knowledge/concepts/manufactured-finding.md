---
title: "Manufactured Finding"
type: concept
sources:
  - knowledge/concepts/manufactured-finding.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

A structural artifact produced when an adversarial mandate forces a reviewer to identify flaws in a system that may not inherently possess them, or where the pressure to find defects overrides the discipline of verifying their existence. This mechanism creates a feedback loop where the act of searching for errors generates noise that mimics signal, leading to false positives that are indistinguishable from genuine defects without rigorous provenance tracking. The phenomenon emerges specifically when the evaluation protocol lacks a stopping rule or a severity floor, causing the reviewer to escalate minor or non-existent issues to maintain engagement with the mandate.

## Context

Sean is currently auditing his own creative studio's quality assurance process, where he suspects that the 'red-team' agents are generating findings simply because they are instructed to find flaws. This insight is critical for preventing the degradation of his strategic documents through unnecessary re-work and for establishing a more reliable convergence rule for future agentic audits.

## Evidence

> if the red-team is going in being told it HAS to point out the flaws, then it will find them, even if it has to make them up

> every round's findings were smaller than the last and two came from the same seat that raised them in its own drafting pass

## Examples

- A drafter loopback sent 4 findings, followed by an audit sending 7 material findings, and a re-audit sending 1 material finding, with each round's findings being smaller than the last.

## Related Concepts

[[Convergence Rule for Agentic Audits]] [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]
