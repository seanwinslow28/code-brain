# Ledger entry template

One file per **material decision**, written by the deciding seat at the moment of decision (Run phase) or by the master skill at Close. Entries are **private** (`systemcraft/ledger/`, gitignored); this template is public machinery.

A decision is *material* when it survives the engagement: someone could later ask "why is it built this way?" and this entry is the answer.

**Brevity law (Sean, ratified 2026-08-24):** an entry is a record, not an essay — every section reads in a breath. When a deeper explanation is wanted, an agent generates it on demand from the entry, its artifact, and the corpus; depth is never stored in the ledger.

```markdown
---
id: eng-001.d03                      # <engagement>.d<seq> — stable, citable
engagement: eng-001-fleet-knowledge-loop-audit
date: 2026-08-24
seat: architecture-advisor
artifact: ../artifacts/adr-001-retrieval.md   # the artifact this decision shaped
model: opus                          # baseline, or "opus→fable: milestone artifact"
status: decided                      # decided | superseded | reopened
supersedes: null                     # id of the entry this replaces, if any
publishable: no                      # no | candidate | published (Sean's per-entry call)
tags: [retrieval, cost]
---

## Decision

One sentence, active voice: what was chosen.

## Options considered

- **The winner** — one-line tradeoff.
- **The loser(s)** — one line each. The losers matter: they are what "why" is measured against.

## Why

The explain-why, one breath: why A over B, in terms a future reader can weigh.

## Evidence

Corpus pointers (lane-manifest refs), live data, incident history — what grounded this.
On a corpus-less machine: name the sources that *would* have grounded it (degradation ladder).

## Audit

Auditor seat · verdict · material defects raised and how they were resolved.
"Not yet audited" is a legal state — never a silently omitted section.

## Revisit when

Named conditions that reopen this decision (a cost threshold, a model release, a scale mark).
```
