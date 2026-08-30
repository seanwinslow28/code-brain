---
title: "How to make `Tacit Knowledge Erosion vs. Automation Scale` better"
type: expansion
parent: "[[tacit-knowledge-erosion-vs-automation-scale]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-29
updated: 2026-08-29
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[tacit-knowledge-erosion-vs-automation-scale]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Replace the “inverse relationship” with stage-specific automation debt

**Add:** A **function-allocation matrix**. Automation does not uniformly erode expertise; its effect depends on whether it automates information acquisition, analysis, decision selection, or execution. Anchor this in Parasuraman, Sheridan, and Wickens’s paper, [“A Model for Types and Levels of Human Interaction with Automation”](https://pubmed.ncbi.nlm.nih.gov/11760769/), alongside Lisanne Bainbridge’s [“Ironies of Automation”](https://www.sciencedirect.com/science/article/pii/0005109883900468).

Sentence pattern: **“Automating execution preserves diagnosis differently from automating interpretation; the debt belongs to the displaced cognitive stage, not to automation in general.”**

**Unlocks:** An **Agent Fleet Automation Allocation Review**: one page per agent mapping what it acquires, interprets, decides, and executes; which human capability each stage displaces; and which stages Sean must periodically perform manually. This turns the concept from a warning into an architecture decision tool suitable for an AI-PM portfolio case study.

## 2. Add “automation surprise”: failure may be observability loss, not skill atrophy

**Add:** **Mode awareness and automation surprise**, anchored in Nadine Sarter, David Woods, and Charles Billings’s [“Automation Surprises”](https://www.researchgate.net/publication/270960170_Automation_surprises). Their stronger claim is that operators fail because automation’s current mode, rationale, and likely next action are difficult to infer—not merely because the operator’s neural pathways weakened.

Sentence pattern: **“Before diagnosing deskilling, test whether the system made competent supervision cognitively impossible: could the operator state what the automation was doing, why, and what it would do next?”**

**Unlocks:** An **Observability Contract for Agents** requiring every scheduled agent to expose `mode`, `evidence`, `decision`, `uncertainty`, `next_action`, and `takeover_state`. Sean could ship this as an executable demo: inject a misleading-but-plausible fleet state, then measure whether he can predict and interrupt the agent before failure. That reaches agent-interface design and incident response, which the current learning-focused concept cannot.

## 3. Add a mechanism for manufacturing tacit judgment, not merely protecting it

**Add:** A **Critical Decision Method → ShadowBox loop**. Gary Klein, Roberta Calderwood, and Donald MacGregor’s [“Critical Decision Method for Eliciting Knowledge”](https://dblp.org/rec/journals/tsmc/KleinCM89.html) extracts experts’ cues, expectations, anomalies, options, and counterfactuals from difficult incidents. Klein and Joseph Borders’s [“The ShadowBox Approach to Cognitive Skills Training”](https://journals.sagepub.com/doi/10.1177/1555343416636515) converts that tacit structure into scenarios where learners rank options before seeing expert rankings and rationales.

Sentence pattern: **“Do not ask AI for critique immediately; first freeze the decision point, record cue interpretation and option ranking, then compare against an expert-derived rationale.”**

**Unlocks:** A **Systems-Judgment Scenario Pack** built from Sean’s real fleet incidents: expired credentials, fabricated research citations, off-LAN model deferral, partial council output, and failed portfolio refreshes. It could ship as a browser-based hiring demo, curriculum module, or reusable agent-evaluation benchmark—evidence that Sean can operationalize judgment rather than merely argue for preserving it.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
