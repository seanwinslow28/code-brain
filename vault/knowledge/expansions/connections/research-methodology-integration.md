---
title: "How to make `Research Methodology Integration` better"
type: expansion
parent: "[[research-methodology-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-16
updated: 2026-06-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-methodology-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “research as competing programs,” not queue routing**

   Anchor it on Imre Lakatos, **“Falsification and the Methodology of Scientific Research Programmes”** in *Criticism and the Growth of Knowledge*.

   Current concept treats LDR vs Gemini DR as a tiering/logistics problem: which engine should handle which question. Missing is the stronger research-methodology layer: every research item should declare whether it is part of a **progressive** or **degenerating** research program.

   Add a field/pattern:

   > “This question belongs to the `X` research program. It is progressive if it predicts/produces `Y`; degenerating if it only explains failures after the fact.”

   This unlocks a **research agenda audit** artifact: a monthly Substack or vault report that says which lines of inquiry are creating new testable leverage and which are just producing nicer explanations. It would make Sean’s fleet critique generative because it would not merely summarize “what research ran”; it would decide which intellectual bets deserve more budget.

2. **Add “information foraging” as the cost model for research routing**

   Anchor it on Peter Pirolli and Stuart Card, **“Information Foraging in Information Access Environments”** and Pirolli’s book ** *Information Foraging Theory* **.

   The concept currently has tiers based on tool capability and dollar cost. What’s missing is a behavioral model of research as scent-following: patches, cues, expected yield, abandonment thresholds. Sean already has queues, citations, and local/cloud routes; he does not yet appear to have a theory for when a research agent should **stop digging**, **switch patches**, or **escalate because scent is weak but value is high**.

   Add a “scent ledger” to each research item:

   > `information_scent: strong|mixed|weak`  
   > `patch_type: canonical-source|forum-trace|repo-issue|market-map|paper-chain`  
   > `abandon_rule: stop after N low-yield hops unless a named source appears`

   This unlocks an **agent runbook** and **executable research policy**: not “Gemini for big topics,” but “use Gemini when patch switching dominates answer synthesis.” It also gives Sean a portfolio-grade artifact: a visible research router that justifies escalation by expected information gain, not vibes.

3. **Add “evidence grading by claim type,” borrowed from evidence-based medicine**

   Anchor it on Gordon Guyatt et al., **“GRADE: an emerging consensus on rating quality of evidence and strength of recommendations”** in *BMJ*.

   The current concept mentions citation quality collapse, fabricated entities, and routing rules, but it lacks a way to grade outputs by the **kind of claim** being made. A vendor docs claim, a community compatibility claim, a pricing claim, a conceptual analogy, and a career-market claim should not share one generic “citation quality” bucket.

   Add a small claim taxonomy:

   > `claim_type: factual-current|technical-compatibility|market-signal|conceptual-framework|personal-strategy`  
   > `evidence_grade: high|moderate|low|speculative`  
   > `upgrade_path: primary-docs|replication|expert-source|multi-source-agreement|personal-test`

   This unlocks a **research QA rubric** and **portfolio one-pager** Sean does not currently have: “How my agent fleet decides what it knows.” It would also sharpen the Vault Critic: instead of saying “citation weak,” it can say “this is a technical-compatibility claim supported only by community hearsay; upgrade path is a reproduction script.” That moves the system from summary to epistemic operations.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
