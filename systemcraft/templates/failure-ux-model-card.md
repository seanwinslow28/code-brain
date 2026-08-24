# Failure-UX spec + model card template

Owned by the **Interaction & Trust Designer** (seat contract, [#144](https://github.com/seanwinslow28/code-brain/issues/144)). Receives PRD + ADR; designs what the user experiences when the system is wrong, and what the system honestly says about itself. Two parts, one artifact: the **failure-UX spec** (behavior) and the **model card** (disclosure). Boundary call: the model card belongs to this seat as a trust-communication artifact — **Evals & Evidence supplies its numbers**, this seat writes what they mean for a user. Audited by the Design Strategist: trust surfaces honest against the PRD's users and promises.

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); this template is public machinery. Brevity law applies.

```markdown
---
id: eng-001.trust
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: interaction-trust-designer
model: sonnet
status: draft                        # draft | audited | final
auditor: design-strategist           # fixed by the audit cycle
---

# Part 1 — Failure-UX spec

## Failure inventory

Every way the system is wrong that a user can meet. An uncovered failure mode is an audit defect.

| Failure mode | What the user sees | Recovery path | Escalation |
|---|---|---|---|

Every row ends at a human or a safe stop — no escalation dead-ends.

## Trust calibration

How the design keeps user confidence matched to actual reliability: confidence display,
friction on high-stakes actions, where the system says "I don't know."
Overtrust is the failure class here, not undertrust.

## Control surfaces

What the user can steer, override, undo, or turn off — and how they find out.

# Part 2 — Model card

## What this is

Plain-language: what the system does, powered by what (numbers from the eval plan, cited not invented).

## Intended use

What it's for, who it's for.

## Out of scope

What it must not be used for. As load-bearing as intended use.

## Known limitations

Where it's weak, measured or honestly suspected — in words a user can act on, not hedges.
```
