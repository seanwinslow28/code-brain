---
title: "How to make `Automation Infrastructure and Interview Preparation` better"
type: expansion
parent: "[[automation-infrastructure-and-interview-preparation]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-03
updated: 2026-07-03
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-infrastructure-and-interview-preparation]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Operational Readiness Review” as a missing interview-prep layer**

   Anchor it on Google SRE’s **“Non-Abstract Large System Design”** chapter in *Site Reliability Engineering* by Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy.

   Current concept says “automation infrastructure supports interview prep,” but it does not prove Sean can reason like someone trusted with production systems. Add a section that treats Code-Brain as an operated service: dependencies, failure modes, alert classes, rollback paths, runbooks, toil, and SLO-style promises.

   Sentence pattern: “This agent is not done when it runs; it is done when its failure mode is observable, bounded, and recoverable.”

   This unlocks a **portfolio runbook / interview artifact**: “Code-Brain Operational Readiness Review.” That gives Sean a concrete senior-IC signal beyond “I built agents”: he can show how he governs unattended automation.

2. **Add “Wardley Mapping for career leverage”**

   Anchor it on Simon Wardley’s **“Wardley Maps”** book / canonical online chapters, especially the doctrine around visibility, movement, and commoditization.

   The concept currently treats roadmap, portfolio, and observability as mutually reinforcing, but it lacks a strategic positioning model. Wardley Mapping would force Sean to place each artifact by user need and maturity: bespoke demo, reusable capability, commodity tooling, or proof of taste.

   Sentence pattern: “This is not a project list; it is a map of where Sean should differentiate versus where he should borrow, automate, or hide the machinery.”

   This unlocks a **job-hunt decision artifact**: a one-page “Portfolio Strategy Map” showing which projects deserve polish, which deserve only screenshots, and which should be converted into reusable infrastructure. It prevents the generic failure mode of treating every impressive system as equally worth explaining.

3. **Add “Boundary Object” as the missing PM-to-agentic-IC bridge**

   Anchor it on Susan Leigh Star and James R. Griesemer’s paper **“Institutional Ecology, ‘Translations’ and Boundary Objects”**.

   This concept says automation infrastructure helps interview preparation, but it misses the deeper claim: Sean’s strongest artifacts are not just tools; they are boundary objects between PM judgment, engineering execution, and agent governance. The observability dashboard, intent-engineering spec, and daily fleet console are artifacts different audiences can interpret differently without collapsing.

   Sentence pattern: “The artifact works because a recruiter can read it as evidence, an engineer as architecture, a PM as operating model, and an agent as executable context.”

   This unlocks a **Substack essay / portfolio one-pager**: “The Boundary Object Portfolio.” That lets Sean explain why his work is unusually legible across PM and IC hiring loops, instead of sounding like a grab bag of automations.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
