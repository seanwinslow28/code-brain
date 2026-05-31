---
artifact: code-brain-system-card
created: 2026-05-31
ai-context: "Comprehension artifact for the Code-Brain System Card. 4-question template per Nate B Jones / ADR convention. Companion to docs/CODE_BRAIN_SYSTEM_CARD.md — maps the live agent fleet to SR-11-7 materiality tiering and the EU AI Act (Art. 50/72, Annex IV), then names the gaps. Stress-tested through the premium LLM Council 2026-05-31."
---

# Code-Brain System Card — Explanation

## What is this?

A governance accounting of the autonomous agent fleet I run on my own hardware, mapped to the two frameworks enterprise AI-PM hiring managers actually care about: SR-11-7 (the Fed's model-risk-management guidance) and the EU AI Act (Regulation 2024/1689). It tiers every live component by materiality, documents the validation evidence and human-override path for each, and names — in plain sight — every place Code-Brain would not pass if it were a regulated system. It lives at `docs/CODE_BRAIN_SYSTEM_CARD.md`; the audience is a model-risk officer or a regulated-SaaS hiring manager who wants to see whether I can scope a regulation, not just recite one.

## Why this approach?

Three ways to prove regulatory-accountability fluency. **(1)** Write an abstract explainer of SR-11-7 and the EU AI Act — rejected; every candidate who skimmed the regulation can do that, and it proves nothing about judgment. **(2)** Claim conformance — map the fleet to the frameworks and assert it complies — rejected, and dangerous: the high-risk obligations (Annex IV, Articles 13/72) don't legally apply to a personal minimal-risk system, so claiming "partial compliance" is a category error a real officer flags in minutes. **(3)** Apply the frameworks to a system I actually operate, lead with an explicit applicability/scope determination that rules most of the regulation *out*, then model the discipline voluntarily and name the honest gaps — chosen. The credibility move is correctly scoping the law and tiering by materiality, not performing compliance. The accepted trade-off: leading with "almost none of this applies to me" risks reading as a dodge, so the artifact has to earn it by demonstrating the tiering work anyway.

## What would break?

- **Scope creep back into over-claiming.** The strongest temptation is to let "I mapped it to Annex IV" drift into "I substantially comply with Annex IV." Detection signal: any cell in the EU AI Act table that says "Partial" or "Substantially present" instead of "inapplicable; modeled voluntarily" — that's the artifact silently re-acquiring the category error the scope section exists to prevent. (The first draft had exactly this; the Council caught it.)
- **Inventory drift from the live fleet.** The card asserts a materiality tier per component; if an agent gets enabled/disabled (e.g., `substack_drafter` or the Judge Layer's master switch) and the card isn't updated, the tiering lies. Detection: the `status` column should match `agents-sdk/config.toml` enable flags on every read; a mismatch means the card is stale.
- **The "no training data" erasure.** Saying "no model is trained here, so training-data governance is N/A" reads as sophisticated but erases an obligation rather than satisfying it — SR-11-7 requires vendor models to be validated as if internal, and drift just moves to silent vendor point-releases. Detection: if the card ever frames inherited vendor-model risk as "not applicable, by architecture," it has reintroduced the single most damaging error a model-risk officer would flag.

## What did I learn?

The hardest part of regulatory fluency isn't knowing what a regulation requires — it's knowing when it *doesn't apply*, and being willing to lead with that. The first draft mapped the fleet to every article and quietly claimed partial conformance; a four-model adversarial review showed that the impressive move is the opposite: rule the regimes out correctly, then model them anyway as a demonstration. Correctly scoping a law you don't have to follow signals more judgment than performing compliance with one you've misread — which is exactly the instinct a fintech or regulated-SaaS PM needs in week one.
