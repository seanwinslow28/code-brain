---
title: "How to make `Corroboration Depth as a Gradient Signal` better"
type: expansion
parent: "[[corroboration-depth-as-a-gradient-signal]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-13
updated: 2026-08-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[corroboration-depth-as-a-gradient-signal]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add a “common-mode failure” correction

- **What to add:** Replace “distinct matchers imply independent evidence” with a dependency audit. Lexical, embedding, and LLM judges can share the same source text, candidate generator, ontology, or model-derived assumptions. Count *independent failure pathways*, not matcher types.
- **Anchor:** John C. Knight and Nancy Leveson, “[An Experimental Evaluation of the Assumption of Independence in Multiversion Programming](https://doi.org/10.1109/TSE.1986.6312924).” Independently implemented programs failed together substantially more often than an independence model predicted. This directly contradicts the concept’s claim that convergence necessarily lowers shared-error probability.
- **Unlock:** An executable **correlated-failure audit** for the fusion-discovery council: perturb URLs, paraphrase evidence, remove shared metadata, swap candidate generators, and measure which judges fail together. The shippable artifact is a dependency matrix—`matcher × upstream assumption × observed joint-error rate`—plus a Substack essay: **“Three Agents Agreeing Is Sometimes One Error Wearing Three Hats.”**

## 2. Replace “corroboration depth” with a risk–coverage contract

- **What to add:** Use **selective classification with a reject option**. Corroboration count becomes merely one feature in a calibrated acceptance policy. The governing question is not “How many signals agree?” but “At this threshold, what error rate do accepted cases exhibit, and what fraction of cases are deferred?”
- **Anchor:** Yonatan Geifman and Ran El-Yaniv, “[Selective Classification for Deep Neural Networks](https://proceedings.neurips.cc/paper/2017/file/4a8423d5e91fda00bb7e46540e2b0cf1-Paper.pdf).” Their formulation explicitly trades coverage for bounded selective risk rather than treating confidence as intrinsically meaningful.
- **Unlock:** A portfolio-grade **calibration harness** that plots risk–coverage curves for pain-point persistence decisions and chooses the operating point satisfying Sean’s 80% precision bar. This produces an agent spec with three outcomes—`persist`, `defer`, `reject`—and an evidence-backed one-pager explaining exactly how much automation the claimed reliability buys. The current concept cannot distinguish “high-confidence but badly calibrated” from genuinely safe automation.

## 3. Add sequential evidence accumulation and an explicit stopping rule

- **What to add:** Model each corroborator by its **likelihood ratio**, cost, and marginal information gain. After every check, choose among `accept`, `reject`, or `collect another signal`; stop when accumulated evidence crosses a predeclared boundary. This prevents five weak, redundant votes from outweighing one highly diagnostic contradiction.
- **Anchor:** Abraham Wald, *[Sequential Analysis](https://books.google.com/books?id=oVYDHHzZtdIC)*, specifically the Sequential Probability Ratio Test. Wald’s framework turns evidence gathering into a bounded decision process with explicit false-accept and false-reject tolerances.
- **Unlock:** A runnable **corroboration controller** for the discovery council: cheap URL provenance first, semantic comparison second, expensive LLM adjudication only inside the continuation region. Ship it as a runbook and trace demo showing why each case stopped, what the next check was worth, and how much compute was avoided. That converts the concept from a qualitative metaphor—“depth as gradient”—into an implementable policy for ordering checks and knowing when enough evidence is actually enough.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
