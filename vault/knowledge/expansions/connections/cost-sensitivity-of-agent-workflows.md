---
title: "How to make `Cost Sensitivity of Agent Workflows` better"
type: expansion
parent: "[[cost-sensitivity-of-agent-workflows]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-28
updated: 2026-08-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[cost-sensitivity-of-agent-workflows]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “cost per accepted outcome,” not cost per run.** Anchor it in Robert Kaplan and Steven Anderson’s [“Time-Driven Activity-Based Costing”](https://www.hbs.edu/faculty/Pages/item.aspx?num=15805). Their model assigns cost through capacity consumed and time per activity. Translate that into:

   `effective cost = inference + retries + review minutes + failed-run recovery + idle capacity`

   This contradicts the article’s implication that `$0 local` means economically free. An unavailable MBP, a 900-second timeout, or twenty minutes validating weak research all consume scarce capacity. This unlocks an **agent unit-economics ledger**, a **runbook for measuring cost per accepted concept/job lead/sprite**, and a portfolio essay titled *Your Free Local Model Is Not Free*.

2. **Add “tail-cost amplification” for fan-out workflows.** Anchor it in Jeffrey Dean and Luiz André Barroso’s [“The Tail at Scale”](https://research.google/pubs/the-tail-at-scale/) (*Communications of the ACM*, 2013). Their key result is architectural: when one request depends on many components, rare slowdowns become routine workflow-level failures. In Sean’s fleet, parallel critics, research panels, remote hosts, and chained nightly agents make the relevant quantity:

   `workflow cost = max branch latency + duplicate work + timeout/retry cost`

   This challenges the current article’s flat monthly accounting: averages conceal the expensive tail. Add percentile measures—p50/p95 completion time, timeout rate, retries per accepted artifact—and explicit cancellation rules for losing branches. This unlocks a **tail-budget incident runbook**, an **observability-dashboard specification**, and an executable demo showing when speculative parallel calls improve reliability versus merely multiplying spend.

3. **Add “value of computation” as the escalation policy.** Anchor it in Stuart Russell and Eric Wefald’s [“Principles of Metareasoning”](https://doi.org/10.1016/0004-3702%2891%2990015-C) and their book *Do the Right Thing: Studies in Limited Rationality*. Their framework asks whether another computation is worth performing based on its expected ability to change the eventual action—not whether budget remains available.

   Encode the decision rule as:

   `continue/escalate iff expected decision improvement × decision stakes > marginal compute + delay + review cost`

   This replaces “prioritize cheaper agents during budget constraints” with a defensible policy: spend $7 on deep research when evidence could reverse a consequential architecture or job decision; stop a free local loop when additional synthesis cannot change anything. This unlocks an **intent-engineering MCP policy primitive**, an **agent stop/escalation spec**, and a Substack argument that cost caps without value-of-information reasoning optimize thrift rather than outcomes.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
