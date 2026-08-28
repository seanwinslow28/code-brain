# ADR template

Owned by the **Architecture Advisor** (seat contract, [#144](https://github.com/seanwinslow28/code-brain/issues/144)). Receives the PRD; produces one ADR per material architecture decision — model/pipeline choices, RAG vs fine-tune vs prompt, build-vs-buy. **Every option carries a rough cost implication** — an unpriced alternative is an audit defect. Audited by Ops & Economics: the seat that must run and pay for the choice.

Filled artifacts are **private** (`ledger/engagements/<eng-id>/artifacts/`); this template is public machinery. Brevity law applies.

```markdown
---
id: eng-001.adr-01                   # one ADR per decision; number them
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: architecture-advisor
model: opus
status: draft                        # draft | audited | final
auditor: ops-economics-modeler       # fixed by the audit cycle
---

## Decision

One sentence, active voice: what was chosen.

## Context

The PRD requirements and constraints that force this decision. Cite the PRD sections, don't restate them.

## Options

Every serious option, priced. The losers matter — they are what "why" is measured against.

| Option | How it works | Rough cost | Key risk |
|---|---|---|---|

Cost is order-of-magnitude honest ($/month, $/1K requests, eng-weeks) — precision is Ops' job later.

## Why

One breath: why the winner over the runner-up, in the PRD's own priority terms.

## Consequences

What this choice commits us to: lock-in, scale cliffs, single points of failure,
and what got simpler. Complexity must serve the product, not the résumé.

## Revisit when

Named conditions that reopen this decision (a cost threshold, a model release, a scale mark).
```
