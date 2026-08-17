---
title: "How to make `Throughput vs. Taste Memory Tension` better"
type: expansion
parent: "[[throughput-vs-taste-memory-tension]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-15
updated: 2026-08-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[throughput-vs-taste-memory-tension]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Replace “taste memory” with pairwise preference learning

1. **Add:** A *taste tournament* based on pairwise choices. Taste is often tacit: Sean may be unable to specify why an opening works, yet can reliably choose A over B. Store comparisons plus rationales—“A wins because concrete image before abstraction”—instead of accumulating prose about his style.

2. **Anchor:** Paul Christiano et al., [“Deep Reinforcement Learning from Human Preferences”](https://proceedings.neurips.cc/paper/2017/hash/d5e2c0adad503c91f91df240d0cd4e49-Abstract.html). The transferable technique is learning an objective from comparisons rather than requiring a complete reward specification.

3. **Unlocks:** An executable **taste-evaluation harness**: generate four Substack openings, run six pairwise comparisons, infer recurring choice rules, then regression-test future drafts against a frozen “golden tournament.” This reaches measurable preference calibration; the current concept only says that signal becomes diluted.

### 2. Define taste preservation as a rate–distortion problem

1. **Add:** A *taste codec*: compression is successful when discarded memories do not change creative decisions. Do not rank a memory by similarity or recency; rank it by whether removing it changes which candidate wins. Sentence pattern: “Preserve the smallest representation that retains the decision-relevant information for task Y.”

2. **Anchor:** Naftali Tishby, Fernando Pereira, and William Bialek, [“The Information Bottleneck Method”](https://arxiv.org/abs/physics/0004057). Their framework asks how to compress an input while retaining information predictive of a target.

3. **Unlocks:** A concrete **retrieval-budget runbook and ablation benchmark**: 2K/8K/32K taste contexts × essay/sprite/portfolio tasks × ranking agreement with Sean. It could produce a portfolio one-pager titled “I Cut My Agent’s Memory by 80% Without Changing Its Creative Decisions.” The current “strict reconciliation protocol” has neither an objective function nor a falsifiable threshold.

### 3. Treat taste as something the system must revise, not merely preserve

1. **Add:** A *reflection-in-action mode*. After an output surprises Sean positively, the agent asks which existing taste rule the work violated, whether the violation should become a new rule, and which prior examples must be reinterpreted. Memory becomes a versioned hypothesis, not a stylistic constitution.

2. **Anchor:** Donald Schön, *The Reflective Practitioner*—specifically “reflection-in-action,” where practitioners reframe the problem while acting rather than merely applying stored knowledge.

3. **Unlocks:** A **taste-change decision record** and critic-agent spec with three outcomes: `conforms`, `productive_violation`, or `unresolved`. It also unlocks a sharper Substack essay: **“The Agent That Remembers Your Taste Can Prevent You From Developing Any.”** Without this counterforce, the concept mistakes perfect fidelity for creative success and risks automating Sean into a caricature of his previous work.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
