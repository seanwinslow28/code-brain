# PRD template

Owned by the **Design Strategist** (seat contract, [#144](https://github.com/seanwinslow28/code-brain/issues/144)). Written first in the pipeline, from the engagement brief and relevant past ledger entries. Every downstream seat receives this artifact in full — never a summary — so it must stand alone.

**Dual-touch law:** the PRD is not done until the Evals & Evidence Architect audits and co-signs the **Evaluable success criteria** section. A success claim that cannot become a runnable test gets rewritten, not waved through. ("Users trust the answers" bounces; "≥90% of a 20-case golden set judged faithful, weekly" passes.)

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); this template is public machinery. Brevity law applies: every section reads in a breath.

```markdown
---
id: eng-001.prd
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: design-strategist
model: opus                          # baseline, or "opus→fable: <why>"
status: draft                        # draft | co-signed | audited | final
evals_cosign: pending                # pending | co-signed <date> — blocks "done"
auditor: evals-evidence-architect    # fixed by the audit cycle
---

## Problem

What hurts, for whom, and why now. One paragraph; if it needs two, the framing isn't done.

## Users

Who this serves, what they're doing when they meet it, and what they'd do without it.

## Assumptions

The user and data assumptions this design leans on — each one named, so an audit can attack it.

## Success definition

What "working" means in the user's terms. Plain language; the testable form lives below.

## Evaluable success criteria  ⟵ co-signed by Evals & Evidence

Each claim as a runnable test: metric, dataset it runs on, cadence. No thresholds here —
measurements are Evals' to design, go/no-go numbers are Ops' to set.

| # | Claim | How it's measured | Cadence |
|---|---|---|---|

## Tradeoff space

The tensions the design must resolve (speed vs cost, coverage vs precision) and which way
this PRD leans, so downstream seats inherit the priorities, not just the features.

## Non-goals

What this deliberately does not do. A missing non-goal is a scope-creep vector — name them.

## Harm check

Could any success metric reward hurting users (the "assumed resolution" class)?
State the check even when the answer is no.
```
