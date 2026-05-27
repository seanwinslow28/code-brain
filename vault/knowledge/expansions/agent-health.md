---
title: "How to make `Agent Health` better"
type: expansion
parent: "[[agent-health]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-health]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “SLO mode,” not freshness mode.**  
   **What to add:** Define agent health as a small SLO contract: `freshness`, `successful completion`, `output usefulness`, `dependency readiness`, and `downstream consumer impact`. Right now the concept treats “stale” as the main failure state; that is closer to a liveness probe than health.  
   **Anchor:** Google SRE, *Monitoring Distributed Systems* / *The Four Golden Signals* in the SRE book and workbook: latency, traffic, errors, saturation as service-centered signals, not machine-centered status. [SRE book](https://sre.google/resources/book-update/monitoring-distributed-systems/) / [SRE workbook](https://sre.google/workbook/monitoring/)  
   **Unlocks:** A portfolio-grade **Agent Fleet SLO one-pager**: “Each agent has an error budget, consumers, freshness window, and alert policy.” This lets Sean sound like he operates a reliability system, not just a cron dashboard.

2. **Add “control-loop health” from STAMP/STPA.**  
   **What to add:** Model each scheduled agent as a controller in a feedback system: controller, controlled process, sensor signal, actuator, process model, unsafe control actions. The missing question is not “did the synthesizer run?” but “what incorrect model of the world caused the fleet to keep depending on an asleep MBP?”  
   **Anchor:** Nancy Leveson, *Engineering a Safer World: Systems Thinking Applied to Safety*, especially STAMP/STPA and safety control structures. [PDF](https://maritimesafetyinnovationlab.org/wp-content/uploads/2021/04/Engineering_a_Safer_WorldNancyLeveson.pdf)  
   **Unlocks:** An **agent safety case** or **intent-engineering spec** where failures are phrased as bad control actions: “Daily Driver consumed stale synthesis without confidence demotion.” That is much stronger than “agent stale” because it creates design obligations.

3. **Add “always running degraded” from resilience engineering.**  
   **What to add:** Acknowledge that the fleet is never simply healthy or unhealthy; it is usually in some degraded-but-working state. Add a taxonomy: graceful degradation, latent failure, compensated failure, brittle dependency, near miss, and operator adaptation.  
   **Anchor:** Richard I. Cook, *How Complex Systems Fail*, especially the claim that complex systems contain latent failures and are kept safe by ongoing adaptation. [PDF](https://www.cs.jhu.edu/~huang/cs624/spring21/readings/how-complex-systems-fail.pdf)  
   **Unlocks:** A recurring **agent incident review** genre: “What silently compensated for this failure?” This would let Sean write sharper Substack/portfolio pieces about autonomous systems as socio-technical operations, not just automation reliability.

## From Anti-Gravity (Gemini 3)

### 1. Degraded Mode Operations (DMO) vs. Binary Freshness
*   **WHAT:** Your concept treats health as a binary cron-job: fresh (success) or stale (failure). This ignores the reality of multi-node agent fleets. You are missing "Degraded Mode Operations"—the intentional engineering of predictable, safe fallback states when preferred infrastructure (like your sleeping MBP) is offline.
*   **WHO/WHAT:** Dr. Richard I. Cook, *"How Complex Systems Fail"* (specifically the principle that complex systems continuously run as broken systems in degraded modes).
*   **UNLOCKS:** A **Degraded State Agent Spec**. Instead of the `meta-agent` just tagging the synthesizer as "stale," you can ship an orchestration protocol where the Mac Mini (`gemma4:e4b`) catches the MBP timeout, writes a degraded "stub" concept to the vault with `status: backfill-pending`, and alerts you. This shifts you from complaining about hardware sleep states to engineering resilient, multi-node handoffs.

### 2. Epistemic Contamination vs. Temporal Health
*   **WHAT:** Your definition explicitly states: *"A healthy agent produces output that updates the state of the vault."* This is a critical proxy failure. If local LDR times out and Qwen3-14B invents `PureMCPClient` (as it did on May 5), the vault updates, the timestamp refreshes, and the agent registers as "healthy"—but your knowledge base is poisoned. You are missing a framework for epistemic health.
*   **WHO/WHAT:** Nithya Sambasivan et al., *"Data Cascades in High-Stakes AI"* (2021 CHI Conference)—specifically the concept that undetected data debt compounds downstream.
*   **UNLOCKS:** An executable **Knowledge Lint Tier 3 Python Check**. You can ship a deterministic evaluation script that flags "high-confidence/low-grounding" artifacts (e.g., checking citation density vs. claim frequency). This allows you to write a Substack essay on "Why Cron Success is Agent Failure," demonstrating the shift from standard software observability to agentic epistemic observability.

### 3. Queue Saturation and Backpressure
*   **WHAT:** Your health metric tracks Latency (freshness) and Errors (execution success). It entirely misses Saturation—the depth of pending work. When the synthesizer is "stale" for three days, the pending work in `research-queue.md` piles up. When the MBP finally wakes, the batch size causes catastrophic context collapse or timeouts. You need a backpressure mechanism.
*   **WHO/WHAT:** Betsy Beyer et al., *"The Google SRE Book"* (Chapter 6: Monitoring Distributed Systems)—specifically the "Four Golden Signals," applied to LLM context windows rather than web traffic. 
*   **UNLOCKS:** A **Load-Shedding PRD & Implementation**. You can ship a logic update to the `meta-agent` that actively measures `research-queue.md` saturation. If pending items exceed your local 900s timeout budget, the agent automatically drops the task, routes it to Gemini DR via `gemini_dr.run`, or halts upstream generation. This moves your infrastructure from passive monitoring to active homeostatic self-healing.
