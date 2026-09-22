---
title: "Convergence Rule for Agentic Audits"
type: concept
sources:
  - knowledge/concepts/convergence-rule-for-agentic-audits.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

A convergence rule is a structural constraint imposed on agentic evaluation loops to prevent infinite escalation when no material defects are found. It functions by capping the number of repair passes, establishing a severity floor tied to critical errors, or requiring a 'holds/residual' verification pass instead of initiating a fresh audit cycle. This mechanism breaks the dependency chain where one agent's write creates a mandatory read for another, ensuring that the system can declare a clean verdict without manufacturing new issues.

## Context

Sean is investigating whether his master skill needs a per-artifact repair cap or a severity floor to stop the infinite loop in pc-eng-001. This is vital for his creative studio workflow because it allows him to trust the output of automated checks without needing to manually intervene every time the system fails to find a flaw.

## Evidence

> the ladder escalates on every material finding and has no stopping rule

> propose a convergence rule for the master skill (a per-artifact repair cap, a severity floor tied to the P0 rule, or a 'holds / residual' verification pass instead of a fresh audit)

## Examples

- Loop cap already in force for pc-eng-001 (brief § Amendment)
- raise the cap to 30 or stop at 26

## Related Concepts

[[Supervision as the New AI Edge]] [[Control Architecture as Evangelism]]
