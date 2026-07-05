# WWF5D — Research Grounding (methodology de-risking)

- **Date:** 2026-07-04
- **Purpose:** Ground the "What Would Fable-5 Do" (WWF5D) skill's *method* with current literature before spending scarce Fable cycles. Companion to [`2026-07-04-fable5-audit-campaign.md`](2026-07-04-fable5-audit-campaign.md).
- **Scope:** the two genuine external gaps — (1) reliability of model self-report, (2) what reasoning transfers via prompting. Judge-design is reused from the existing anima Em calibration harness, not re-researched.
- **Method:** 5 parallel search agents → cited, falsifiable claims → confidence-rated. Primary sources (arXiv / frontier-lab publications) prioritized.

---

## Bottom line — four findings that shape the build

1. **Self-report is an unreliable narrator → the behavioral diff is load-bearing, not optional.**
2. **Only abstracted recipes transfer via prompting; raw traces and latent capacity do not → WWF5D encodes procedures/checklists/rubrics, never Fable transcripts.**
3. **There is a real ceiling — some of Fable's edge is promptable, some is capability-gated → validate per-move; partial transfer is the expected, honest outcome.**
4. **The validation judge must be de-biased: order-swapped, length-controlled, cross-family/decorrelated panel (never a model judging its own family), κ-gated to Sean's labels, with Sean's eye as final arbiter.**

---

## 1. Self-report reliability (why the diff is load-bearing)

- Frontier reasoning models verbalize a decisive injected hint **<20% of the time**; Claude 3.7 ~25% / DeepSeek R1 ~39%, falling to 20%/29% for *misaligned* hints. [High] — arXiv:2505.05410; anthropic.com/research/reasoning-models-dont-say-think
- Injecting a bias (e.g., always-"(A)") shifts answers while the CoT **never mentions the bias**, dropping accuracy up to **36%** across 13 BBH tasks — stated reasoning systematically misrepresents the true cause. [High] — Turpin et al., arXiv:2305.04388
- Models vary enormously in how much they actually condition on their stated CoT; **faithfulness degrades with scale/capability**. [High] — Lanham et al., arXiv:2307.13702; NeuroFaith arXiv:2506.09277
- Genuine introspection exists but is **rare (~20% even best-case, Claude Opus 4.1) and narrow** — detecting an injected internal state is a different, better-supported skill than *narrating why* an output was produced (where confabulation dominates). [High] — anthropic.com/research/introspection; transformer-circuits.pub/2025/introspection; Binder et al., arXiv:2410.13787
- Countervailing (flagged): an unfaithful CoT can still be *informative* for monitoring — but this does **not** make self-report ground truth. [Medium] — metr.org/blog/2025-08-08

**So what for WWF5D:** the introspection protocol generates *candidate* moves. No move enters WWF5D unless a Fable-vs-Opus behavioral delta corroborates it. Self-report is a lead, never a readout.

## 2. What transfers via prompting (what WWF5D can and can't contain)

**Transfers (abstracted artifacts):**
- Self-composed reasoning **structures** port across families (PaLM2→GPT-4→Llama2), +up to 32% over CoT. [High] — Self-Discover, arXiv:2402.03620
- Distilled **thought-templates** can lift a smaller model toward a larger one. [Med-High] — Buffer of Thoughts, arXiv:2406.04271
- A strong model's traces **rewritten as rationales** raise a weaker model. [Med] — AutoReason, arXiv:2412.06975
- **Metacognitive** scaffolds narrow the gap (PaLM+MP approaches GPT-4). [Med-High] — arXiv:2308.05342
- **Principles/rubrics** steer behavior in-context (best for values/behavior, not raw capacity). [Med] — Constitutional AI, arXiv:2212.08073

**Does NOT transfer (stays model-intrinsic):**
- CoT is **capability-gated / emergent** (>~10–100B), not promptable into small models. [High] — Wei et al., arXiv:2201.11903
- Analogical exemplars **don't help weak models**; the generative act, not the exemplar, is the capability. [High] — arXiv:2310.01714
- Naively copying a strong model's demos **backfires** via "semantic misleading" and "strategy-transfer failure." [Med-High] — arXiv:2509.23196

**So what for WWF5D:** encode *abstracted recipes* — a grounding protocol, a seam/handoff checklist, a root-cause ("zoom-out") procedure, a dangerously-wrong/structural/minor triage rubric, an adapter pattern, and an intent-preserving spec template. **Copy the recipe, not the raw trace.**

## 3. Feasibility + the honest ceiling

- A weaker "teacher" can author prompts that measurably lift a *stronger* student via outcome-RL (WST: +98% MATH-500). [High] — arXiv:2508.16741
- Strong-model **skill-labels/decompositions are model-agnostic** — they improve a *different, weaker* model on held-out math. [Med-High] — arXiv:2405.12205
- **But** prompting elicits some capabilities (MCQA) and **fails on others** (code-gen recovers only with fine-tuning); strong-authored prompts don't reliably transfer downward (Dropbox o3 case). [High] — password-locked models, arXiv:2502.02180; dbreunig.com/2024/12/12

**So what for WWF5D:** the procedural layer is portable; raw horsepower is not. Expect partial transfer, measure it per-move, and document the ceiling rather than oversell it.

## 4. Validation-judge design (the transfer gate)

- **Position bias** is large — swap answer order, count a win only if it holds both ways. [High] — MT-Bench, arXiv:2306.05685
- **Verbosity/length bias** inflates scores — length-control the comparison. [High] — arXiv:2404.04475
- **Self-preference is causal** — a judge favors its own text; the judge must be neither author's family. [High] — arXiv:2404.13076
- A **decorrelated panel** beats one big judge and is cheaper, but choose judges for *decorrelation, not headcount* ("nine judges, two effective votes"). [High/Med] — PoLL, arXiv:2404.18796; arXiv:2605.29800
- **Calibrate to human labels with Cohen's κ (≥0.6)**, not raw accuracy. [High] — MT-Bench

**So what for WWF5D:** for the Opus-vs-Opus+WWF5D held-out A/B, use a cross-family, order-swapped, reference-blind panel (not an Opus-led council), κ-gated against a handful of Sean's own labels, with **Sean's eye as the Engine-Truth final call**. Reuse the anima Em protocol (N=5 majority, κ 0.885) directly.

---

## Sources

Self-report/faithfulness: arXiv:2505.05410 · anthropic.com/research/reasoning-models-dont-say-think · arXiv:2305.04388 · arXiv:2307.13702 · arXiv:2506.09277 · anthropic.com/research/introspection · transformer-circuits.pub/2025/introspection · arXiv:2410.13787 · aclanthology.org/2024.findings-acl.19 · metr.org/blog/2025-08-08
Transfer/prompting: arXiv:2402.03620 · arXiv:2406.04271 · arXiv:2412.06975 · arXiv:2308.05342 · arXiv:2212.08073 · arXiv:2201.11903 · arXiv:2310.01714 · arXiv:2509.23196
Feasibility/ceiling: arXiv:2508.16741 · arXiv:2505.20072 · arXiv:2405.12205 · arXiv:2502.02180 · dropbox.tech/machine-learning/optimizing-dropbox-dash-relevance-judge-with-dspy · dbreunig.com/2024/12/12 · arXiv:2511.10507
Judge design: arXiv:2306.05685 · arXiv:2404.04475 · arXiv:2404.13076 · arXiv:2404.18796 · arXiv:2605.29800
