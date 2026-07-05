---
title: "How to make `Claude Skills` better"
type: expansion
parent: "[[claude-skills]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-01
updated: 2026-07-01
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[claude-skills]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “skill as situated routine,” not just tool output**

   Anchor it on Lucy Suchman’s *Plans and Situated Actions: The Problem of Human-Machine Communication*.

   The missing facet: the current concept treats Claude Skills as discrete automations: `etf-page-creator`, `stakeholder-update`, `jira-automation`. Suchman gives Sean a sharper frame: a skill is not merely a planned procedure, but a routine that survives contact with messy workplace context.

   Add a section like: “A Claude Skill is a situated work routine: it encodes the repeatable part of a human workflow while preserving escalation paths for the ambiguous part.”

   This unlocks a stronger portfolio artifact: a **workflow ethnography one-pager** for each skill. Instead of saying “automated WordPress ETF pages,” Sean can show: human routine observed → stable steps extracted → ambiguity boundaries preserved → measurable work removed. That reads like agentic-engineering judgment, not prompt-library maintenance.

2. **Add “job-to-be-done trigger mapping” for when a skill should exist**

   Anchor it on Clayton Christensen, Taddy Hall, Karen Dillon, and David Duncan’s *Competing Against Luck*.

   The missing facet: the concept proves that Sean shipped skills, but not that he can decide which skills deserve to exist. The JTBD frame would force each Claude Skill to name the progress event that “hires” it.

   Add a pattern like: “When [recurring business pressure] creates [manual coordination drag], users hire the skill to produce [trusted artifact] without [failure mode].”

   Example: “When ETF news requires fast publication under compliance-sensitive formatting constraints, editors hire `etf-page-creator` to produce a publishable WordPress draft without hand-copying structured market data.”

   This unlocks a **skill-prioritization rubric** or **agent backlog scoring model**. Sean can evaluate candidate skills by trigger frequency, pain intensity, trust requirement, and artifact repeatability. The current concept says “I built three.” This would let him say “I know which three should be built first.”

3. **Add “end-user programming / malleable software” as the deeper lineage**

   Anchor it on Bonnie Nardi’s *A Small Matter of Programming: Perspectives on End User Computing*.

   The missing facet: “Claude Skills” currently sounds vendor-specific. Nardi lets Sean reposition them as part of a longer history: non-programmers shaping software behavior through local, task-specific artifacts. Claude Skills become the 2026 version of spreadsheets, macros, and workplace scripts.

   Add a section like: “Claude Skills are malleable software objects: small, inspectable automations built close to the work by someone who understands both the domain and the execution substrate.”

   This unlocks a better **Substack essay** and **recruiter-facing positioning page**: “From PM artifacts to malleable agent systems.” It also gives Sean a clean contradiction to shallow AI-PM narratives. He is not just “using AI to automate tasks”; he is building local software that lets domain experts reshape workflows without waiting for platform teams.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
