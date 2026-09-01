---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

Legibility debt is the structural gap between automated production velocity and human verification capacity, where the volume of commits exceeds the operator's ability to inspect them directly. This forces reliance on indirect proofs—such as tags or audit logs—to establish trust in system state rather than direct observation. Without these cryptographic anchors, the operator cannot distinguish intentional design changes from accidental drift, leading to a loss of control over the system's history and an erosion of epistemic authority.

## Context

Sean audits the vault to ensure that deleted branches did not result in data loss, specifically resolving uncertainty created by the agent fleet's high-velocity commits. By proving that content exists in `main` or archives via tags, he mitigates the risk of silent failure propagation where automated noise masks critical state changes.

## Evidence

> the proof is now a tag rather than a branch: archive/mini-pre-b8-2026-08-28

> Content audit of that snapshot against main — 24 of its 27 commits are vault: auto-commit noise from the Obsidian-Git owner retired 2026-07-05

## Examples

- of the 65 files unique to it, 64 are byte-identical blobs on main
- the 3 real commits are all on main (da4856fb's 2026-08-11 production repairs are present verbatim

## Related Concepts

[[Epistemic Artifacts as Strategic Proof]] [[The Illusion of Competence in Automated Systems]]
