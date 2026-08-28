---
title: "How to make `Cost-Capped Agentic Workflows and Deep Research Integration` better"
type: expansion
parent: "[[cost-capped-agentic-workflows-and-deep-research-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-27
updated: 2026-08-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[cost-capped-agentic-workflows-and-deep-research-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace “cost cap” with an Expected Value of Computation stopping policy

- **What to add:** An **EVC gate**: continue research only when the expected decision improvement from another query exceeds its monetary cost, latency, and opportunity cost. The current `$7/task` rule limits loss but cannot determine whether spending even $1—or stopping at $7—is rational.
- **Canonical anchor:** Stuart Russell and Eric Wefald, [“Principles of Metareasoning”](https://doi.org/10.1016/0004-3702(91)90015-C). Their resource-bounded-rationality framework values computation by its expected effect on the agent’s eventual external decision.
- **Operational pattern:** `Continue when P(decision changes) × value of better decision > marginal research cost; otherwise stop.`
- **What this unlocks:** An executable **research-escalation agent spec** that chooses among local search, standard Deep Research, DR Max, or termination. It also supports a strong Substack argument: **“A budget is not a strategy: agents need a price for thinking.”** Sean’s current concept can report fiscal discipline; this addition can justify resource allocation.

## 2. Make Deep Research an anytime workflow with explicit quality profiles

- **What to add:** **Anytime computation**: every research stage must produce a valid intermediate artifact whose quality improves with additional budget. Define observable performance profiles such as `source coverage`, `claim verification`, `counterevidence searched`, and `decision confidence` at $0.50, $1.50, $4, and $7.
- **Canonical anchor:** Shlomo Zilberstein, [“Using Anytime Algorithms in Intelligent Systems”](https://onlinelibrary.wiley.com/doi/abs/10.1609/aimag.v17i3.1232). Zilberstein replaces binary completion with measured result quality and treats computational allocation as a control problem.
- **Operational pattern:** `Interrupt → return the best valid dossier plus unresolved uncertainties; never return merely “budget exhausted.”`
- **What this unlocks:** A **budget-interruption runbook**, quality-versus-cost benchmark, and portfolio demo where a user moves a dollar slider and watches the evidence dossier deepen. The present concept connects a queue to a cap; it says nothing about graceful degradation, partial-result validity, or how the extra dollars improve the answer.

## 3. Add a pre-registered evidence protocol, adapted from PRISMA

- **What to add:** A **Research Protocol Manifest** written before execution: decision question, inclusion/exclusion criteria, source classes, search strings, date boundary, duplicate handling, appraisal rubric, counterevidence requirement, and amendment log. Require a source-flow ledger: discovered → screened → excluded with reason → cited.
- **Canonical anchor:** Matthew Page et al., [“The PRISMA 2020 Statement”](https://www.bmj.com/content/372/bmj.n71). Its checklist and flow diagrams make evidence selection inspectable; adapt the reporting structure without pretending product research is a medical systematic review.
- **Operational pattern:** `No synthesis claim without a traceable included source; no excluded source without a recorded reason.`
- **What this unlocks:** An **audit-grade research dossier template**, provenance-aware agent specification, and portfolio one-pager comparing reproducible Deep Research against opaque “answer generation.” The current concept proves spend control, but not epistemic control: a cheap research run can still be selectively sourced, irreproducible, or confidently wrong.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
