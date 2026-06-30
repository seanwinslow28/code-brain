---
title: "How to make `Self-Hosted Research and Portfolio Integration` better"
type: expansion
parent: "[[self-hosted-research-and-portfolio-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-30
updated: 2026-06-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[self-hosted-research-and-portfolio-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “replayable proof packet” mode, not just “self-hosted reliability.”**  
   Anchor it on **Jon Claerbout / David Donoho’s reproducible research lineage**, especially Buckheit & Donoho, [“WaveLab and Reproducible Research”](https://statweb.stanford.edu/~wavelab/Wavelab_850/wavelab.pdf), and Roger Peng’s later framing of reproducibility as independent recomputation.  
   Pattern to add: `claim -> source inputs -> agent run -> output artifact -> replay command -> known failure modes`.  
   This unlocks a **portfolio evidence artifact**: a public “reproduce this nightly brief” page or GitHub repo where an interviewer can rerun one research loop and see the same markdown, manifest, costs, and citations. Right now the concept says “verifiable”; this would make verification executable.

2. **Add “situated-action failure critique” against the fantasy of autonomous self-sufficiency.**  
   Anchor it on **Lucy Suchman, [*Plans and Situated Actions: The Problem of Human-Machine Communication*](https://en.wikipedia.org/wiki/Lucy_Suchman)**. Suchman’s useful contradiction: plans are not execution; they are resources people use while improvising inside messy local situations.  
   Pattern to add: `when the agent plan met the actual morning / OAuth / machine-sleep / citation-quality situation, what broke, and what human judgment repaired it?`  
   This unlocks a **runbook/postmortem genre** Sean currently cannot reach: “Why my autonomous research fleet is not autonomous in the way vendors mean.” That is stronger job-market signal than “I self-host agents,” because it shows operational judgment around bounded autonomy, escalation, and repair.

3. **Add “theory-building handoff” as the missing bridge between portfolio demo and employer trust.**  
   Anchor it on **Peter Naur, [“Programming as Theory Building”](https://pages.cs.wisc.edu/~remzi/Naur.pdf)**. Naur’s point cuts directly against portfolio screenshots: the real asset is not the program text but the builder’s theory of how the system works, why it is shaped that way, and how to change it intelligently.  
   Pattern to add: `what theory does this fleet embody that another engineer would need before safely modifying it?`  
   This unlocks a **senior IC one-pager / architecture memo**: “The theory of Code-Brain: cheap nightly cognition, expensive interactive judgment.” That would let Sean explain the system as transferable engineering taste, not just a personal automation stack.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
