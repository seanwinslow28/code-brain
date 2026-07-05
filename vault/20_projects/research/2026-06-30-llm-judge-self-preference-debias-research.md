---
title: "LLM-as-judge self-preference & position bias — debiasing for a synthesis/clustering judge (E2 research)"
date: 2026-06-30
project: fusion-discovery-council
feature: E2 (panel self-preference fix)
status: complete
tags: [research, llm-as-judge, evaluation-bias, fusion-discovery-council, discovery-step-d]
method: deep-research skill ($0, Anthropic subscription) — 5 angles, 19 sources fetched, 90 claims → 25 verified (19 confirmed / 6 refuted), 101 agents
---

# E2 research — judge self-preference & the debiasing toolkit

**Decision this informed:** how to fix the panel self-preference confound the Step-C gate flagged
(the FUSE judge `anthropic/claude-opus-4.7` was a *literal member* of its own panel in every tier).
Fork: **(a)** separate the judge's model family from the panel vs. **(b)** build a full
authorship-blind + order-randomized judge pipeline (replacing `openrouter:fusion`).

**Verdict: (a).** For a *synthesis/clustering* judge, family separation is the single
highest-leverage, lowest-cost lever; the full order-randomization machinery (b) buys little here
and can actively backfire. Decision made by the evidence, not by gut.

---

## Findings (per-finding confidence + sources)

### 1. Self-preference is real, directional, and significant — large in summarization (HIGH)
GPT-3.5/GPT-4/Llama-2 disproportionately favor their own outputs over other LLMs' and humans'.
Pairwise self-preference scores (>0.5 = favors own): **GPT-4 0.705 (XSUM) / 0.912 (CNN-DM)**,
GPT-3.5 0.582/0.431. In MT-Bench chat the effect is smaller/noisier (**GPT-4 +10pp**, **Claude-v1
+25pp** win-rate self-favoring; Zheng calls it "inconclusive" there). Existence + direction unanimous
across sources (3-0 on every constituent claim).
- Panickssery/Bowman/Feng, NeurIPS 2024 — https://arxiv.org/pdf/2404.13076
- Wataoka et al. 2024 — https://arxiv.org/abs/2410.21819
- Zheng et al., NeurIPS 2023 (MT-Bench) — https://arxiv.org/html/2306.05685v4

### 2. Two competing mechanism accounts → family separation wins under BOTH (HIGH; mechanism debate unsettled)
- **Recognition account** (Panickssery): self-preference strength is *linearly + causally* tied to
  self-recognition ability (fine-tuning recognition up/down moves preference proportionally).
  Out-of-the-box recognition is non-trivial — GPT-4 hits **73.5%** distinguishing its own output from
  two other LLMs + humans. ⇒ a different-family judge can't recognize the panelist's text as its own,
  removing the signal → family separation *meaningfully* reduces bias.
- **Perplexity/familiarity account** (Wataoka): judges over-reward low-perplexity (familiar) text
  "regardless of whether the outputs were self-generated." ⇒ family separation removes only one
  contributor; some familiarity bias remains.
- **Why this matters:** family separation is the only lever that helps under *either* account, so it's
  robust to the unsettled mechanism question. (The strong-form "perplexity is THE root cause" claim was
  **refuted 1-2** — both accounts treated as live.)
- https://arxiv.org/pdf/2404.13076 · https://arxiv.org/abs/2410.21819

### 3. Authorship-blinding ALONE does not eliminate self-preference (HIGH, 3-0)
Panickssery's self-preference is *measured under blinding by design* ("the identity of the alternative
source is not revealed to the evaluator") and persists, because recognition is implicit (style/structure),
not label-dependent. ⇒ blinding is cheap insurance, **not** a substitute for family separation. In our
case it's also moot: `openrouter:fusion` internalizes the panel and never exposes attribution to us to
strip (FUSION_SCHEMA §3).
- https://arxiv.org/pdf/2404.13076

### 4. Position bias is driven by the near-tie *quality gap* — the pairwise driver (HIGH)
Position bias is systematic (not chance; Repetition-Stability rules out noise) and "**strongly affected
by the quality gap between solutions**" — a parabolic curve: consistency peaks at large quality gaps and
**collapses for comparably-matched answers.** The hardest-to-judge instances are near-ties. Position
Consistency on MT-Bench: Claude-3.5-Sonnet 0.82, GPT-4 0.82, GPT-3.5 0.70.
- Shi et al., IJCNLP-AACL 2025 — https://arxiv.org/abs/2406.07791 · https://aclanthology.org/2025.ijcnlp-long.18.pdf

### 5. Order-swap mitigation is NOT reliably beneficial — it can backfire (HIGH, 3-0)
The textbook fix (call judge twice, swap order, win only if preferred both ways) was the only single-call
strategy to *significantly help* any model on MT-Bench (Gemini Flash **+4.7pp**, p=0.004) — but on LLMBar
**adversarial** data it **hurt all models 4–11pp** (GPT-4o −11.1pp) because tie-resolution "discards
correct verdicts... where one response is unambiguously better."
- "Judging the Judges," arXiv:2604.23178 — https://arxiv.org/html/2604.23178
- ⚠️ Two *other* claims from this same paper ("position bias is now negligible ≤0.04") were **refuted 0-3**.
  Read it narrowly: "swap has real downside," NOT "bias is gone."

### 6. For a synthesis/clustering judge the position-bias confound is materially smaller (MEDIUM — extrapolation)
A clustering/synthesis judge groups findings into themes; it isn't making A-vs-B preference picks, so the
dominant position-bias driver (near-tie quality gap) doesn't directly transfer. **But this is inference**
— every position-bias paper studies pairwise/list-wise comparison; **none studies a synthesis judge**
(hence MEDIUM). And the attempt to prove "pointwise scoring is broadly more bias-robust than pairwise" was
**refuted twice** — so do *not* assume a synthesis judge is bias-free. Self-preference can still leak via
implicit recognition (over-quoting same-family phrasing) or perplexity (favoring fluent findings).
- https://aclanthology.org/2025.ijcnlp-long.18.pdf · https://arxiv.org/abs/2406.07791 · https://arxiv.org/pdf/2404.13076

### 7. PoLL — disjoint-family juries show less intra-model bias (HIGH, supporting)
"Replacing Judges with Juries" (Verga et al.): a Panel of LLM evaluators composed of *disjoint model
families* exhibits less intra-model bias than a single large judge while correlating better with humans.
Corroborates disjointness as the right bar. (We keep a single judge for now; PoLL is the future direction
if the council ever needs a jury.)
- https://arxiv.org/abs/2404.18796

### Refuted (kept for honesty)
- "Perplexity is THE root cause of self-preference" — 1-2 (mechanism is unsettled, not settled).
- "Position bias in modern judges is negligible (≤0.04)" — 0-3.
- "Pointwise scoring is broadly more bias-robust than pairwise" — 0-3 / 1-2 (don't over-claim synthesis safety).

---

## How this changed the build

1. **Killed option (b).** The full authorship-blind + order-randomized pipeline targets *position* bias,
   whose dominant driver (near-tie pairwise quality gaps) is largely absent for a synthesis judge — and
   order-swap can *erase* decisive correct judgments (−4 to −11pp). Building it would be over-engineering
   *and* a potential regression. Rejected.

2. **Locked option (a) = family separation as the one lever.** It's the only fix that helps under both
   unsettled mechanism accounts. Implemented as a single enforceable invariant: **for every tier, the
   judge's model family ∉ the set of panel families.**

3. **Shape = (a1) "keep the strong judge, drop its family from the panel"** for standard/deep — keep the
   proven Opus judge, remove Opus from those panels (standard 4→3 families, deep 6→5; both stay fully
   cross-vendor vs the judge). For `quick` (judge was `~google/gemini`, panel had no anthropic), keep the
   3-model panel and swap the judge to a disjoint family (`openai/gpt-5.5`; `mistralai/mistral-medium-3-5`
   as the budget-safe alternative).

4. **Dropped authorship-blinding plumbing.** Finding 3 + FUSION_SCHEMA §3: blinding is insufficient *and*
   unreachable through the opaque fusion tool. Family separation does the work.

5. **No paid verification re-run.** Research + the Step-C gate already justify the change, which is
   config-only and regression-guarded by the invariant test. (A judge-swap variant of the Step-C harness
   remains available if empirical before/after is ever wanted.)

## Open questions (not blocking E2; logged for later)
- Does self-preference manifest in a *clustering* judge as over-quoting / theme-naming favoring same-family
  phrasing? No study tests this; a cheap internal A/B (same- vs cross-family judge on identical findings)
  would close the gap.
- Which mechanism dominates for *our* models (Opus / GPT-5.x / Gemini / Grok)? Determines whether family
  separation is near-complete or partial mitigation.
- Could the *input order* of panel findings bias which get clustered as "primary" themes (a primacy effect
  distinct from pairwise position bias)? If ever a concern, a lightweight finding-shuffle — not a full p!
  permutation pipeline — would be the minimal mitigation.
