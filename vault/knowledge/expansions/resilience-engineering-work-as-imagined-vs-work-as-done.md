---
title: "How to make `Resilience Engineering: Work-as-Imagined vs Work-as-Done` better"
type: expansion
parent: "[[resilience-engineering-work-as-imagined-vs-work-as-done]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-09
updated: 2026-06-09
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[resilience-engineering-work-as-imagined-vs-work-as-done]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “FRAM mode”: model exception handling as coupled functions, not a failed happy path.**  
   Anchor it on Erik Hollnagel’s *FRAM: The Functional Resonance Analysis Method* (2012). FRAM gives Sean a concrete way to map AP work-as-done as functions with inputs, outputs, preconditions, resources, control, and time, instead of narrating “automation fails, human intervenes.” Source: [Hollnagel FRAM](https://www.erikhollnagel.com/books/fram.html).  
   Sentence pattern to add: “The unit of analysis is not the failed transaction; it is the resonance between upstream variability and downstream control capacity.”  
   **Unlocks:** an executable AP-agent design artifact: a “function-resonance map” for duplicate checks, PO matching, bank-account changes, human queueing, SLA breach, and escalation. Current concept can say exceptions exist; FRAM lets Sean specify where variability compounds.

2. **Add “STPA / unsafe control action mode”: contradict the idea that human routing is automatically safer.**  
   Anchor it on Nancy Leveson’s *Engineering a Safer World: Systems Thinking Applied to Safety* (MIT Press, 2011). STAMP/STPA reframes safety as a control problem: accidents happen when controllers, feedback, constraints, or process models are wrong, late, missing, or contradictory. Source: [MIT Press / Google Books listing](https://books.google.com/books/about/Engineering_a_Safer_World.html?id=0gZ_7n5p8MQC).  
   Sentence pattern to add: “A human approval step is not a control unless the approver has timely feedback, authority, incentives, and a correct process model.”  
   **Unlocks:** an audit-grade AP Agent Safety Case: unsafe control actions for “approve vendor bank change,” “release payment despite duplicate suspicion,” “override tolerance breach,” and “trust OCR/vendor-master mismatch.” Current concept treats human judgment as a backstop; STPA forces Sean to design the backstop.

3. **Add “graceful extensibility / saturation mode”: measure adaptive capacity before it fails.**  
   Anchor it on David Woods’ “The Theory of Graceful Extensibility: Basic Rules That Govern Adaptive Systems” (2018) and Richard Cook’s “How Complex Systems Fail” (1998/2000). Woods gives the missing positive target: systems survive surprise by extending capacity at boundaries; Cook gives the warning that safety is continuously produced by operators, not statically embedded in components. Sources: [Woods paper listing](https://ideas.repec.org/a/spr/envsyd/v38y2018i4d10.1007_s10669-018-9708-3.html), [Cook PDF](https://worrydream.com/refs/Cook_2000_-_How_Complex_Systems_Fail.pdf).  
   Sentence pattern to add: “Exception rate is a lagging indicator; saturation shows up first as queue age, override clustering, reviewer context loss, and shrinking recovery options.”  
   **Unlocks:** a fleet/AP resilience dashboard spec: capacity margin, queue aging, reviewer load, unresolved exception classes, and “near-saturation” alerts. Current concept can recommend routing exceptions; this lets Sean define when the routing layer itself is becoming brittle.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
