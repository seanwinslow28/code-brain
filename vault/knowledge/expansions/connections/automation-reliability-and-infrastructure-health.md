---
title: "How to make `Automation Reliability and Infrastructure Health` better"
type: expansion
parent: "[[automation-reliability-and-infrastructure-health]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-25
updated: 2026-08-25
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability-and-infrastructure-health]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “service-level intent,” not infrastructure uptime

Anchor it on Chris Jones, John Wilkes, Niall Murphy, and Cody Smith’s chapter [“Service Level Objectives” in *Site Reliability Engineering*](https://sre.google/sre-book/service-level-objectives/).

The concept currently measures what machines are doing—online, offline, log present—not whether the automation delivered its promised outcome. Define each agent through a user-facing SLI/SLO:

> “By 08:45, the daily note contains a complete overnight digest on 29 of 30 mornings; deferred runs preserve queued work; stale output counts as failure.”

This reframes an offline Alienware as a capacity condition, not automatically an incident. It also introduces error budgets: reliability investment becomes justified by missed outcomes rather than generalized anxiety about redundancy.

**Unlock:** an executable **Agent Fleet Service Catalog**—one-page contracts containing promise, SLI, SLO, measurement window, error budget, owner, and remediation policy. This would be a strong portfolio artifact demonstrating PM judgment translated into operating code.

## 2. Add “gray-failure mode” and differential observability

Anchor it on Peng Huang et al.’s HotOS paper, [“Gray Failure: The Achilles’ Heel of Cloud-Scale Systems”](https://www.microsoft.com/en-us/research/publication/gray-failure-achilles-heel-cloud-scale-systems/).

Binary `ONLINE/OFFLINE` monitoring misses the dangerous middle: Ollama answers health checks but stalls inference; a model returns syntactically valid yet fabricated research; the synthesizer exits zero after producing a partial manifest; the daily note exists but lacks its fleet block. Huang’s key idea is **differential observability**: infrastructure, orchestrator, and consumer can each perceive a different system state.

Add a status vocabulary such as:

> `reachable → capable → progressing → semantically valid → consumed`

Each transition needs independent evidence. A successful process exit should never prove successful knowledge delivery.

**Unlock:** a **gray-failure detection runbook and fault-injection demo**. Sean could deliberately inject slow inference, stale output, partial manifests, and consumer-visible omissions, then show which probe catches each fault. That is considerably stronger agentic-engineering evidence than another health dashboard.

## 3. Replace “add redundancy” with “map adaptations and trade-offs”

Anchor it on Richard I. Cook’s [“How Complex Systems Fail”](https://worrydream.com/refs/Cook_2000_-_How_Complex_Systems_Fail.pdf).

Cook contradicts the article’s tidy causal story. Complex systems are usually already operating with latent failures; incidents arise from interacting conditions, and redundancy itself adds complexity and new failure modes. Sean’s fleet demonstrates this: fallback models, deferred execution, cost caps, host schedules, and manifest gates are not merely defenses—they reshape the system and can conceal degradation.

Use this incident sentence pattern:

> “The host outage was one condition; failure occurred because detection, routing, deadline, and recovery policies interacted, while normal operator adaptations stopped compensating.”

**Unlock:** a **learning-review template** that replaces root cause with contributing conditions, successful adaptations, brittle adaptations, and newly introduced trade-offs. Applied to the morning 401, MBP deferrals, or fabricated local-research citations, it could become a substantive Substack essay: **“My Agent Fleet Was Reliable Because It Was Already Partly Broken.”**

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
