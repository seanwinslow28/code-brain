---
title: "How to make `The Extra Hour` better"
type: expansion
parent: "[[the-extra-hour]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-01
updated: 2026-06-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[the-extra-hour]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “deliberate practice loop,” not “extra hour” as aspiration.**  
   Anchor it on K. Anders Ericsson, Ralf Krampe, and Clemens Tesch-Römer’s 1993 paper, [“The Role of Deliberate Practice in the Acquisition of Expert Performance”](https://philpapers.org/rec/ERITRO-4). Pattern: one narrow skill, immediate feedback, repeated attempts, visible error log. This unlocks a **job-hunt training artifact**: a weekly agentic-engineering drill book with scored reps like “design an eval for a failing agent,” “debug a bad tool call trace,” or “explain a fleet incident in PM language.” Current concept says “prepare more”; this would specify *what kind of reps compound*.

2. **Add “plans are resources, not controllers.”**  
   Anchor it on Lucy Suchman’s [*Plans and Situated Actions: The Problem of Human-Machine Communication*](https://openlibrary.org/books/OL7737289M/Plans_and_Situated_Actions_The_Problem_of_Human-Machine_Communication_%28Learning_in_Doing_Social_Cogn)). This directly contradicts the I-5 / intent-spec tendency to believe better specifications solve the gap. Pattern: “The plan is what the agent consults when reality breaks, not the thing that determines behavior.” This unlocks a **Substack essay or portfolio case study** about Code-Brain as situated work: agents negotiating local constraints, stale context, missing OAuth, sleeping machines, file locks, and cost caps. Current concept sounds like generic agent-prep; this would give it a sharper theory of why autonomous systems fail in the wild.

3. **Add “graceful extensibility” as the fleet standard.**  
   Anchor it on David Woods’ [“Resilience as Graceful Extensibility to Overcome Brittleness”](https://irgc.org/wp-content/uploads/2018/09/Woods-Resilience-as-Graceful-Extensibility-to-Overcome-Brittleness.pdf) and Woods/Dekker/Cook/Johannesen/Sarter’s [*Behind Human Error*](https://www.oreilly.com/library/view/behind-human-error/9781317175537/). Pattern: don’t ask “did the agent succeed?”; ask “where did the system stretch, saturate, hand off, or collapse?” This unlocks an **Agent Fleet Observability runbook** and interview-ready one-pager: incident taxonomy, saturation signals, escalation rules, and postmortems for launchd/Ollama/SDK failures. Current concept points at Agent Evals; this adds the missing resilience lens for evaluating the *whole human-agent system*.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
