---
title: "How to make `Comprehension Debt` better"
type: expansion
parent: "[[comprehension-debt]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-30
updated: 2026-08-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[comprehension-debt]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add a “debt or waste?” classification

Anchor it in Martin Fowler’s [“Technical Debt Quadrant”](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html). The concept currently labels every weak artifact “debt,” but debt should purchase a near-term advantage and later incur measurable interest. An auto-generated note that nobody uses is inventory waste; a misunderstood note repeatedly retrieved by agents is debt.

Add this sentence pattern:

> We accepted **[verification shortcut]** to obtain **[immediate value]**; its principal is **[repair work]**, and its interest is **[recurring decision or maintenance cost]**.

Track `retrieval_count × correction_minutes`, not output volume or rejection count alone. This unlocks a **comprehension-debt register and deletion runbook** that tells Sean whether to verify, quarantine, regenerate, or delete each artifact. It also prevents the concept from supporting its own thesis with ambiguous fleet metrics.

## 2. Add “theory loss,” which contradicts the repayment metaphor

Anchor it in Peter Naur’s [“Programming as Theory Building”](https://gwern.net/doc/cs/algorithm/1985-naur.pdf). Naur argues that the valuable product is the operator’s internal theory of how the problem is solved—not the program text or accompanying documentation. That creates a harder failure mode than debt: some artifacts cannot be “paid down” through later reading because the originating theory was never formed in Sean’s mind.

Add a **theory-bearing artifact gate**:

> Before promotion, Sean must explain what problem this artifact models, why its structure follows from that model, and what change would falsify it—without rereading the artifact.

Failure means “unowned theory,” not merely “low comprehension.” This unlocks an **agent spec for explain-back promotion**, a strong **Substack essay contrasting knowledge accumulation with theory formation**, and a portfolio claim more defensible than “I built a large vault”: Sean can demonstrate that his system preserves operator authority under automation.

## 3. Replace generic “verification” with lightweight assurance cases

Anchor it in Tim Kelly’s [*Arguing Safety—A Systematic Approach to Managing Safety Cases*](https://citeseerx.ist.psu.edu/document?doi=81d2e41a5673a8d4a0d7c78ca3d0b0ff26165991&repid=rep1&type=pdf), which systematized Goal Structuring Notation: claims decomposed through strategies into evidence, with context and assumptions made explicit.

Give promoted concepts a compact record:

```text
Claim → Supporting evidence → Inference
      → Assumptions → Defeaters → Confidence → Review trigger
```

Applied here, “accepting more marginal content” is only a claim; falling rejection counts and rising cluster counts do not establish it without denominator, policy-change, and retrieval-utility evidence.

This unlocks a **machine-checkable concept-assurance schema**, a **critic-agent specification that hunts unsupported inference edges**, and an **executable portfolio demo** where the fleet renders a confidence graph and automatically reopens concepts when evidence, assumptions, or source freshness changes.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
