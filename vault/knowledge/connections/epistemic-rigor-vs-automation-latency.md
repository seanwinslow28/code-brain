---
title: "Epistemic Rigor vs. Automation Latency"
type: connection
connects:
  - Gemini Deep Research
  - Research Agents
  - Deep Research Queue
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension lies between the need for 'anti-bias structure' in complex research and the 'compound question in, cited synthesis out' simplicity of automated agents. Gemini Deep Research is optimized for speed and breadth, but Sean's job-hunt and product strategy require 'adversarial disconfirmation' and 'hypothesis competition.' When these modes are conflated, the agent produces confident but epistemically shallow outputs. This forces Sean to manually inject 'tasking doctrine' into the agent's prompt, effectively breaking the automation loop he is trying to build. The consequence is that the agent becomes a 'report generator' rather than a 'thinking partner,' requiring Sean to perform the cognitive labor of structuring the inquiry himself.

## Threads

### [[Gemini Deep Research]]

> Compound research does not just need more horsepower; it needs anti-bias structure.

> Before Gemini DR runs, classify whether the task requires evidence collection, hypothesis competition, adversarial disconfirmation, or estimate calibration.

### [[Research Agents]]

> The current concept treats Gemini DR as a report generator: compound question in, cited synthesis out.

### [[Deep Research Queue]]

> Add a mode like: “Before Gemini DR runs, classify whether the task requires evidence collection, hypothesis competition, adversarial disconfirmation, or estimate calibration.”

## Implications

- Sean must implement a pre-flight classifier in his agent fleet to route queries to different reasoning scaffolds, adding latency but improving epistemic quality.
- The 'Deep Research Queue' cannot be a simple FIFO list; it must be a priority queue weighted by epistemic risk, not just complexity.
- Automated 'red-team contradiction runs' require a different prompt template than 'market map runs,' necessitating a modular agent architecture.
