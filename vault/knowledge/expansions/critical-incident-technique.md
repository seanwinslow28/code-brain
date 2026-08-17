---
title: "How to make `Critical Incident Technique` better"
type: expansion
parent: "[[critical-incident-technique]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-17
updated: 2026-08-17
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[critical-incident-technique]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Restore the actual Critical Incident Technique

**Add:** “Flanagan mode”: CIT is not merely a promotion filter. It is a five-stage method for defining an activity’s aim, specifying observable incidents, collecting reports, classifying behaviors, and deriving practical requirements. Capture effective and ineffective behavior—not just surprising events.

**Anchor:** John C. Flanagan, [“The Critical Incident Technique” (1954)](https://www.apa.org/pubs/databases/psycinfo/critical.html).

**Sentence pattern:** “The agent was trying to ___; under ___ conditions it observed ___, did ___, and produced ___; this counts as effective/ineffective against ___.”

**Unlocks:** An executable `critical_incident` schema, labeling rubric, and synthesizer eval set. Sean could turn heterogeneous fleet traces into a comparative portfolio case study showing which behaviors reliably produce success or failure. The current concept can only decide what to retain; it cannot generate validated operating requirements.

## 2. Add Critical Decision Method replay

**Add:** “CDM replay”: after identifying an incident, reconstruct the decision through timeline sweeps and probes—first cue, changing goals, rejected options, uncertainty, time pressure, expertise used, and counterfactual outcome. A consequential choice is not useful evidence until its hidden decision model is elicited.

**Anchor:** Gary Klein, Roberta Calderwood, and Donald MacGregor, [“Critical Decision Method for Eliciting Knowledge” (1989)](https://doi.org/10.1109/21.31053).

**Sentence pattern:** “At ___ I noticed ___; I expected ___; option ___ was rejected because ___; had cue ___ been absent, I would have ___.”

**Unlocks:** A decision-interview agent spec and recruiter-ready “decision anatomy” one-pager. Applied to the fabricated-citation failure, MBP availability routing, or Pixel Quantizer gate, it would expose the cues and counterfactuals behind Sean’s architecture—not merely announce that judgment occurred. That is stronger evidence for senior-PM and agentic-engineering interviews.

## 3. Contradict the anomaly-only premise with Safety-II

**Add:** “Successful adaptation sampling”: retain a small stratified sample of difficult-but-successful ordinary runs alongside incidents. The article’s claim that routine operations are statistically insignificant is too strong; apparently routine success may conceal repeated human or agent compensation for broken assumptions.

**Anchor:** Erik Hollnagel, *Safety-I and Safety-II* (2014), especially his distinction between “work as imagined” and “work as done” and his argument that performance variability produces both success and failure. His [2014 Safety-II presentation](https://www.sintef.no/globalassets/project/hfc/documents/3-si-and-sii.pdf) makes the countercase directly.

**Sentence pattern:** “Despite ___ varying, the run succeeded because ___ adjusted ___; this adaptation is safe while ___ remains true and hazardous when ___.”

**Unlocks:** A “normal-success denominator” dashboard, resilience runbook, or Substack essay titled **The Night Nothing Broke**. It would reveal compensating mechanisms—fallbacks, retries, manual wake windows, stale-data guards—that incident-only sampling systematically erases, turning operational reliability itself into demonstrable engineering judgment.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
