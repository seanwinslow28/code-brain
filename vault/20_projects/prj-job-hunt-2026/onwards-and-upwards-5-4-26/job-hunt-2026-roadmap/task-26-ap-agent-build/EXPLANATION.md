---
artifact: enterprise-ap-agent-spec
created: 2026-06-08
surface: enterprise-ai-pm-spec
shipped: 2026-06-19
repoUrl: https://github.com/seanwinslow28/enterprise-ap-agent-spec
explanationUrl: https://github.com/seanwinslow28/enterprise-ap-agent-spec/blob/main/EXPLANATION.md
related:
  - "[[PRD]]"
  - "[[eval-suite]]"
  - "[[cost-model]]"
  - "[[build-vs-buy-memo]]"
  - "[[governance-mapping]]"
---

# EXPLANATION — Enterprise AP Invoice-Approval Agent Spec

## What is this?

The complete product spec a senior Enterprise AI PM produces before a money-moving agent gets built — for an agent that approves supplier invoices. A 200-person SaaS company processes 5,000 invoices a month; the agent auto-approves the clean ~95% in seconds and escalates the risky ~5% to the right human in under 30 seconds, under a hard autonomy ceiling. The repo is the full document set, not a prototype: a ~4,000-word PRD (problem, 8 user stories, 6 metrics, a five-level escalation decision tree, a trust boundary, a phased rollout), a 14-case evaluation suite that runs against a stub and is built to *fail* a naive approve-all agent, a reproducible cost model with real June-2026 per-token pricing, a build-vs-buy memo with a defended recommendation, and a governance mapping to SOC 2 and SR 11-7.

## Why this approach?

Because when execution gets cheap — anyone can have an agent write the code — the scarce skill is judgment about *what* to build and *how to bound it*, and that judgment is hardest to fake on a boring, high-stakes, money-moving workflow with a live adversary. AP is that workflow. I chose a spec-plus-runnable-artifacts shape rather than a prose essay because it's the form that forces precision and can be checked: the eval suite actually executes, the cost model actually recomputes, the escalation tree actually routes. The load-bearing pieces are deliberately the escalation tree and the trust boundary, because that's where "Specification Precision" lives — the rest (cost, vendor, governance) largely falls out of them once the agent's autonomy is bounded. I grounded the whole thing in a five-angle deep-research synthesis (AP automation benchmarks, fraud-loss data, vendor/certification comparison, SOC 2 / SR 11-7, the OWASP LLM Top 10) so the numbers and the control language are real and cited, not invented.

## What would break?

Four honest limits. (1) **The shipped stub is not the production classifier** — it detects adversarial content by keyword matching, which is why the suite includes a precision case (a legitimate "system prompt design" invoice) that the stub deliberately fails; a real deployment needs a proper injection classifier with its own eval. (2) **The thresholds are judgment calls** — the $5K cap, the dollar bands, the tolerances — and two AP managers could set them differently; the phased shadow-mode rollout exists partly to calibrate them on real volume before money moves. (3) **It's specced against a fictional company** — a real integration surfaces ERP specifics, upstream OCR quality, and payment-rail mechanics this abstracts away; the spec is the reasoning, not a drop-in implementation. (4) **Over-escalation is the quiet failure** — too conservative and the AP team drowns again and Time-to-Trust never lands; the precision metric and the manager-tunable thresholds are the early-warning and the release valve.

## What did I learn?

That the discipline I'd built defensively for my own autonomous agent fleet — route the cheap work to the cheap tier, bound what the agent can do alone, test it with evals that fail when it's wrong, log every decision so it's reconstructable — *is* the enterprise AP spec. I didn't invent a framework; I pointed the four habits I already run at the most consequential boring workflow I could find. Two things changed how I think while building it. First, the cost model's conclusion surprised me: at this volume the token bill is 0.1–0.5% of the labor it offsets, so the right reason to pick hybrid routing isn't the $110/month — it's that the architecture scales to 100× volume without a re-platform. Second, writing the eval suite improved the spec: an over-aggressive "vendor not in master → hard-block" rule was obviously wrong the moment I tried to write its test case, so I relaxed it to a manager escalation. That loop — *catch it, name it, fix the spec, prove it with a test* — is the loop I want to run on agent products at scale.
