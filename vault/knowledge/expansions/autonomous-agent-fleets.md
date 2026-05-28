---
title: "How to make `Autonomous Agent Fleets` better"
type: expansion
parent: "[[autonomous-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-28
updated: 2026-05-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[autonomous-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “blackboard architecture” as the missing coordination pattern.**  
   Anchor it on Barbara Hayes-Roth’s paper, [“A Blackboard Architecture for Control”](https://apps.dtic.mil/sti/pdfs/ADA143550.pdf), plus Hearsay-II as the canonical expert-system ancestor. The current concept treats fleet memory as propagation: agent A learns, agent B receives. Blackboard systems add a different frame: independent specialists opportunistically read/write a shared problem state, while control logic decides which knowledge source fires next.  
   **Unlock:** an executable demo or agent spec for `fleet_blackboard.py`: shared hypotheses, confidence, claims, contradictions, and next-action bids. This would move Sean from “memory backend selection” to “coordination substrate design.”

2. **Add STAMP/STPA: fleet failure as unsafe control, not bad memory.**  
   Anchor it on Nancy Leveson’s [*Engineering a Safer World: Systems Thinking Applied to Safety*](https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/) and STPA. The article currently says fragmentation makes collective intelligence null. STAMP would challenge that: accidents happen when control loops, feedback, constraints, and mental models are inadequate, even if every component is functioning. For agents, “memory did not propagate” is only one loss scenario. Others: stale feedback, over-broad autonomy, conflicting local objectives, invisible handoff state, or supervisors trusting a synthesized artifact without provenance.  
   **Unlock:** a fleet safety case / runbook: “Unsafe Control Actions for Code-Brain Agents.” Example sections: daily-driver writes based on incomplete overnight state; critic promotes contradiction without supersession; synthesizer accepts low-diversity clusters; meta-agent reports green health while downstream artifacts are stale.

3. **Add Boyd-style command-and-control as the contradiction to total shared memory.**  
   Anchor it on John Boyd’s [“Organic Design for Command and Control”](https://www.coljohnboyd.com/static/documents/1987-05__Boyd_John_R__Organic_Design_for_Command_and_Control__PPT-PDF.pdf). The missing move is: good fleets do not maximize shared state; they minimize explicit coordination by increasing implicit orientation, doctrine, trust, and commander’s intent. This directly contradicts the concept’s assumption that more inter-agent memory propagation is the path to compounding intelligence. Some agent state should remain local; shared memory should carry intent, constraints, deltas, and exceptions, not every lesson.  
   **Unlock:** a Substack essay or portfolio one-pager: “Agents Need Commander’s Intent, Not Chat History.” Also an `intent-engineering` artifact: a fleet intent charter separating shared doctrine, local autonomy, escalation triggers, and no-share zones.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
