---
title: "How to make `Daily Note Gener` better"
type: expansion
parent: "[[daily-note-gener]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-04
updated: 2026-06-04
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[daily-note-gener]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “situated-daily-note mode”: the note is not a plan, it is an index of what the day forced into view.**  
   Anchor it on Lucy Suchman’s [*Plans and Situated Actions*](https://books.google.com/books/about/Plans_and_Situated_Actions.html?id=AJ_eBJtHxmsC) (1987), especially the critique that plans are resources for action, not scripts action obeys.  
   Sentence pattern to add: “The daily note succeeds when it captures the gap between intended routine and situated reality: what happened, what interrupted the plan, what the agent inferred, and what the human had to repair.”  
   **Unlock:** a Substack essay or portfolio artifact on “agentic planning after contact with reality.” Right now the concept only says the agent generates a note; this lets Sean argue that the daily note is a field instrument for studying human-agent coordination.

2. **Add “daily note as cognitive artifact,” not productivity log.**  
   Anchor it on Donald Norman’s [*Things That Make Us Smart*](https://books.google.com/books/about/Things_That_Make_Us_Smart.html?id=yPKkBQAAQBAJ) (1993), specifically cognitive artifacts as external representations that change what the user can think, remember, and decide.  
   Sentence pattern to add: “A daily note is a cognitive artifact when it reduces memory load, exposes system state, and makes deferred commitments inspectable; it is clerical output when it merely summarizes yesterday.”  
   **Unlock:** an executable demo or one-page case study: “Daily Note as Fleet Console.” This would turn the concept into a design spec for the daily note UI: anchors, Dataview blocks, fleet digest, unresolved tickets, failure traces, next-action slots. Current version cannot distinguish a useful note from a pretty transcript.

3. **Add “reliability contract for personal agents”: SLO, error budget, and postmortem trigger.**  
   Anchor it on Google’s SRE chapter [“Embracing Risk”](https://sre.google/sre-book/embracing-risk/) and optionally John Allspaw’s “Blameless PostMortems and a Just Culture” lineage.  
   Sentence pattern to add: “The daily-note generator should have an SLO: note exists by 08:45 with fleet digest, open tickets, and overnight deltas. Misses spend error budget and trigger a lightweight postmortem, not vague ‘agent malfunction’ language.”  
   **Unlock:** a runbook and interview-ready artifact: “Personal Agent Fleet SLOs.” Sean could show PM-plus-IC judgment by converting a flaky automation anecdote into production operations: SLI, SLO, burn rate, alert, remediation, and stop rules. Current concept names failure but has no operational decision framework.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
