---
title: "Runtime-Model Coupling and Automation Reliability"
type: connection
connects:
  - Runtime-Model Coupling
  - Automation Reliability
  - Infrastructure Status
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension between Runtime-Model Coupling and Automation Reliability reveals that 'model quality' is a misnomer; it is actually 'runtime-model pair quality.' When Sean switches runtimes, he is not just changing the inference engine but fundamentally altering the model's behavior. This creates a reliability risk where a model that works perfectly in one runtime fails silently in another, not due to a bug in the code, but due to a mismatch in inference flags. The consequence is that automation reliability cannot be guaranteed by model selection alone; it requires a matrix of runtime-model configurations to be maintained and monitored.

## Threads

### [[Runtime-Model Coupling]]

> the hypothesis ("Ollama think:false will recover capability lost to LM Studio's missing thinking-disable") is partially confirmed and partially refuted — gains range from +25 pp to -25 pp depending on the model.

### [[Automation Reliability]]

> Cross-runtime data refutes any "switch wholesale" framing; the right move is per-model runtime selection.

### [[Infrastructure Status]]

> Best Tier A upgrade candidate identified: qwen3.6:35b-a3b on MBP-Ollama at 85 % schema match, 5/5 needle recall, 30 tok/s — beats the current qwen3-14b LM Studio production baseline on every dimension.

## Implications

- Sean must maintain a configuration matrix of runtime-model pairs rather than a single 'best model' recommendation, increasing operational complexity but ensuring reliability.
- Automated testing pipelines must include runtime-switching tests to detect schema degradation that would be invisible in a single-runtime benchmark.
