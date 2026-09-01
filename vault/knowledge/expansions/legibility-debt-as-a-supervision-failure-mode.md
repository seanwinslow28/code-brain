---
title: "How to make `Legibility Debt as a Supervision Failure Mode` better"
type: expansion
parent: "[[legibility-debt-as-a-supervision-failure-mode]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-31
updated: 2026-08-31
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[legibility-debt-as-a-supervision-failure-mode]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “proof-carrying change” mode.** Anchor it in Santiago Torres-Arias et al.’s [*in-toto: Providing Farm-to-Table Guarantees for Bits and Bytes*](https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias). The concept currently overclaims that a Git tag is a “cryptographic anchor”: a tag identifies state, but does not prove which agent produced it, which checks ran, or whether the intended workflow was followed. Sentence pattern: **“A change is trustworthy only when its identity, producer, inputs, transformations, and policy checks travel with it as verifiable evidence.”** This unlocks a **proof-carrying-commit agent specification**, an executable demo in which every nightly vault mutation emits signed provenance, and a portfolio one-pager distinguishing *history preservation* from *workflow integrity*.

2. **Add the “automation irony” as a contradiction to the capacity thesis.** Anchor it in Lisanne Bainbridge’s 1983 paper [*Ironies of Automation*](https://www.sciencedirect.com/science/article/pii/0005109883900468). Legibility debt is not merely “more output than Sean can inspect.” As routine inspection disappears, the operator’s system model and recovery skill decay—while automation leaves him only the rare, ambiguous failures requiring the deepest expertise. Sentence pattern: **“Automation does not merely exceed the supervisor’s attention; it consumes the practice by which the supervisor remains qualified to intervene.”** This unlocks a sharper **Substack argument about the deskilling of agent operators**, plus an **operator-readiness runbook**: scheduled manual replays, hidden-failure drills, and periodic reconstruction of an agent decision without consulting its summary.

3. **Add “risk-limiting audit” mode.** Anchor it in Philip B. Stark’s [*An Introduction to Risk-Limiting Audits and Evidence-Based Elections*](https://www.stat.berkeley.edu/~stark/Preprints/lhc18.pdf). The current concept diagnoses an impossible demand—inspect everything—then jumps to logs and tags. Stark supplies the missing supervisory policy: sample evidence, measure discrepancies, and escalate toward complete inspection when the evidence is insufficient. Sentence pattern: **“The goal is not total visibility; it is a precommitted upper bound on the chance of accepting a materially wrong system state.”** This unlocks an **executable fleet-audit tool and decision record**: define “materially wrong,” assign a risk limit, randomly inspect agent outputs, expand the sample after failures, and trigger a full audit above a discrepancy threshold. It converts “legibility debt” from metaphor into an operational control with an explicit stopping rule.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
