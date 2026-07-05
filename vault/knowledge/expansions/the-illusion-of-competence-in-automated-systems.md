---
title: "How to make `The Illusion of Competence in Automated Systems` better"
type: expansion
parent: "[[the-illusion-of-competence-in-automated-systems]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-29
updated: 2026-06-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[the-illusion-of-competence-in-automated-systems]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Ironies of Automation” as the canonical backbone**

   **What to add:** A named subsection: **Automation Irony: the better the automation, the worse the human fallback gets.**  
   Sentence pattern: “When automation removes routine practice, it also removes the training data for human recovery.”

   **Anchor:** Lisanne Bainbridge, **“Ironies of Automation”** (1983). Bainbridge’s core point is sharper than the current concept: automation leaves humans responsible precisely for the tasks automation cannot handle, while depriving them of the practice needed to handle them.

   **What this unlocks:** A stronger **agent-fleet design principle**: every autonomous agent needs a “manual recovery curriculum,” not just monitoring.  
   Ship artifact: **`agent-recovery-drill-runbook.md`** with monthly failure drills for Daily Driver, Vault Critic, Job Feed, and Synthesizer. The current article says “retain mental models”; Bainbridge gives Sean the argument for deliberately practicing breakdowns even when the system is healthy.

2. **Add “Mode Confusion” from aviation automation**

   **What to add:** A missing facet: **the operator may not know what mode the automation is currently in, what authority it has, or what it will do next.**  
   Sentence pattern: “The failure is not that the automation stops working; the failure is that the human’s model of the automation diverges from the automation’s actual state.”

   **Anchor:** Nadine Sarter and David Woods, **“How in the World Did We Ever Get into That Mode? Mode Error and Awareness in Supervisory Control”** (1995). This is the exact canonical reference for automation surprises in complex control systems.

   **What this unlocks:** A better **observability dashboard taxonomy** for agent fleets. Sean already has health checks and manifests; this adds *mode visibility*: scheduled, skipped, fallback-disabled, partial, human-needed, stale-output, authority-escalated.  
   Ship artifact: **Agent Fleet Mode Legend** inside the daily note console or portfolio one-pager. Current concept says “monitoring”; mode confusion explains *what must be monitorable*.

3. **Add “Joint Cognitive Systems” to contradict the lone-operator framing**

   **What to add:** A contradicting framework: stop framing the issue as “human skill atrophy” alone; frame it as **human-plus-automation coordination quality**.  
   Sentence pattern: “Competence is not located in the human or the agent; it is produced by the coordination protocol between them.”

   **Anchor:** David Woods and Erik Hollnagel, **Joint Cognitive Systems: Foundations of Cognitive Systems Engineering** (2005). Also pairs well with Woods’ later resilience engineering work, but this book is the clean conceptual anchor.

   **What this unlocks:** A more mature **agent spec genre**: not “agent does task, human supervises,” but **coordination contracts**.  
   Ship artifact: **`coordination-contract.md` template** for each agent: shared state, handoff cues, authority boundary, stale-state risks, recovery owner, and “what the human must still be able to do manually.” The current concept can produce a warning essay; Joint Cognitive Systems lets Sean produce an engineering artifact for agent-human teaming.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
