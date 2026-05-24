---
title: "How to make `Personal Agentic Intent Engineering` better"
type: expansion
parent: "[[personal-agentic-intent-engineering]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[personal-agentic-intent-engineering]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “situated-intent mode,” anchored on Lucy Suchman’s _Plans and Situated Actions: The Problem of Human-Machine Communication_**

   The current concept treats intent as specifiable in advance. Suchman is the necessary contradiction: plans do not determine action; action is improvised inside local circumstances. Add a section that says: “Personal intent is not a fixed charter. It is a situated repair loop between declared purpose, tool behavior, context drift, and what the user actually does next.”

   Sentence pattern: **“When the agent followed the plan but missed the situation, the missing intent was…”**

   This unlocks a **failure-analysis genre** Sean cannot currently produce: runbooks and Substack essays about cases where the fleet executed correctly but helped badly. Artifact: `situated-intent-postmortem.md` template for nightly-agent failures, with fields for plan, circumstance, misread cue, repair rule, and new stop condition. Source: Suchman, 1987, Cambridge University Press. [Open Library](https://openlibrary.org/works/OL4962782W/Plans_and_Situated_Actions), [Google Books](https://books.google.com/books/about/Plans_and_Situated_Actions.html?id=AJ_eBJtHxmsC).

2. **Add “leverage-rank intent,” anchored on Donella Meadows’ “Leverage Points: Places to Intervene in a System”**

   The concept says agents should align with personal goals, but it lacks a way to rank where intervention belongs. Meadows gives the missing hierarchy: parameters are weak, information flows are stronger, rules/goals/paradigms are strongest. Sean’s current article risks making every agent improvement sound equally valuable.

   Sentence pattern: **“This agent changes the system at leverage level N: parameter / feedback loop / rule / goal / paradigm.”**

   This unlocks **portfolio one-pagers and architecture reviews** where Sean can prove maturity beyond “I built automations.” Artifact: a `personal-agent-leverage-map` that classifies each fleet agent by intervention level: daily-driver as information-flow intervention, knowledge-lint as rule enforcement, intent-engineering MCP as goal/paradigm infrastructure. Source: Donella Meadows, “Leverage Points: Places to Intervene in a System.” [Donella Meadows Project](https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/).

3. **Add “orientation before optimization,” anchored on John Boyd’s “Destruction and Creation” / OODA**

   The concept currently sounds like: declare intent, build agents, adapt over time. Boyd adds a sharper decision frame: the scarce capability is not automation, it is continuously destroying stale mental models and creating better orientation faster than the environment changes. This is especially relevant to Sean’s job hunt, where the terrain changes weekly.

   Sentence pattern: **“This agent is not here to decide faster; it is here to re-orient me faster by breaking model X and recombining signals Y/Z.”**

   This unlocks **decision memos and agent specs** for high-variance domains: job targeting, portfolio positioning, Substack voice calibration, sprite-pipeline model choice. Artifact: an `orientation-agent-spec.md` where every run must produce one destroyed assumption, one new discriminating signal, and one changed next action. Source: John Boyd, “Destruction and Creation” (1976), precursor to OODA. [OODA Wiki summary](https://www.ooda.wiki/wiki/Destruction_and_Creation).

## From Anti-Gravity (Gemini 3)

### 1. Situated Action (Contradicting Framework)
**WHAT:** Add "Situated Action" to argue that personal intent cannot be fully captured in an a-priori specification. Intent engineering (like your I-5 framework) assumes intent is top-down. This framework proves that human plans are actually post-hoc rationalizations of improvisational, context-dependent actions. 
**WHO/WHAT:** Lucy Suchman, *Plans and Situated Actions: The Problem of Human-Machine Communication* (1987).
**UNLOCKS:** Reversing your `intent-engineering` MCP server logic. Instead of writing a declarative "Intent Charter" before starting, you ship an `Emergent-Intent` hook. This agent watches your raw Bash history, `git` diffs, and Obsidian edits, deducing and formally specifying your intent *after* you've acted. This unlocks a high-signal Substack essay and executable demo: "Bottom-Up Intent: Why My Agents Watch Me Before They Work," contrasting enterprise OKR-style intent with IC-level emergent intent.

### 2. Coherent Extrapolated Volition (Missing Facet)
**WHAT:** Add "Coherent Extrapolated Volition" (CEV) to differentiate between your *immediate impulse* and your *actual goals*. Personal intent is notoriously drifting; CEV defines intent as what you *would* want if you "knew more, thought faster, and were more the person you wished to be."
**WHO/WHAT:** Eliezer Yudkowsky, *Coherent Extrapolated Volition* (2004).
**UNLOCKS:** A "CEV Gate" `PreToolUse` hook. When you trigger a deep-research loop on a shiny new tangent (e.g., a new local model), the CEV agent cross-references your active `job-hunt-2026` objectives. If the action contradicts your extrapolated volition, it exits with code 2 (Deny) and prints a friction-check. You ship an executable GitHub repo demonstrating "Agent as Executive Function" rather than just "Agent as Executor"—a highly marketable artifact for AI-PM roles focused on alignment.

### 3. Factored Cognition (Missing Operational Technique)
**WHAT:** Add "Factored Cognition" as the mechanical solution for evaluating whether an agent actually met your intent. You currently use an LLM Council for high-variance critique, but monolithic vibe-checks of intent are noisy. Factored Cognition breaks an ambiguous intent into microscopic, independently verifiable sub-tasks that can be reliably graded by smaller, cheaper local models.
**WHO/WHAT:** Ought (Andreas Stuhlmüller & Jungwon Byun), *Factored Cognition Primer* (and the architecture behind Elicit).
**UNLOCKS:** A complete refactor of your Vault Synthesizer's `evaluate_article_depth()` gate. Instead of a single complex prompt, you ship an orchestration script where your local Qwen3-14B evaluates isolated intent-factors (e.g., "Does this paragraph introduce a new named entity?") independently and rolls them up into a deterministic score. This unlocks a technical PRD for your intent-engineering MCP server detailing exactly how to measure intent-drift programmatically at $0/run.
