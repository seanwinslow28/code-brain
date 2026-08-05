---
title: "Divergence Mechanisms — Evidence vs Folklore (Kickoff D, Topic 2)"
type: research-pointer
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, divergence, mode-collapse, homogenization, multi-agent-debate, morphological-analysis, persona-forcing, creativity-metrics, gemini-deep-research, research]
created: 2026-08-05
last-updated: 2026-08-05
sources: [gemini-deep-research]
tool: "gemini_dr.py --tier dr (google-genai 2.x, agent=deep-research-preview-04-2026)"
cost_usd: 2.80
wall_seconds: 505
interaction_id: v1_ChdheFZ6YXRqc0ZMbVZfdU1QdDlmZTRBdxIXYXhWemF0anNGTG1WX3VNUHQ5ZmU0QXc
report: "[[2026-08-05-map-the-research-lineage-behind-llm-divergence-mechanisms-we]]"
related: [2026-08-05-tested-mechanism-library-prior-art, 2026-08-05-prior-art-synthesis]
ai-context: "POINTER note, not the report. Full 53KB Gemini Deep Research output at vault/20_projects/research/2026-08-05-map-the-research-lineage-behind-llm-divergence-mechanisms-we.md. Topic 2 of Kickoff D. This report is materially better grounded than its Topic 1 sibling — it names datasets, metrics, effect sizes and classifications rather than vibes — but citations are still opaque Google grounding-redirect URLs and no claim here has been independently verified. The evidence-vs-folklore table is the single most decision-relevant artifact produced by the whole research round."
---

# Divergence Mechanisms — Evidence vs Folklore

> **This is a pointer note.** Full report at [[2026-08-05-map-the-research-lineage-behind-llm-divergence-mechanisms-we]] (53KB, 48 citations). Kickoff D, Topic 2. Run 2026-08-05, DR tier, $2.80, 505s.

## Why this was commissioned

The refocus's masthead thesis is that **models produce competent-but-convergent output, and the publication demonstrates mechanisms that escape the median**. Building the Ladder ships one tested mechanism per rung.

That only works if the mechanisms have evidence behind them. This run asks which divergence-mechanism families are empirically supported and which are practitioner folklore, so the first rung isn't built on lore.

## The core table (the reason this run was worth $2.80)

The report classifies mechanism families on evidence strength × measured effect on *semantic* diversity:

| Mechanism family | Classification | Reported effect |
|---|---|---|
| Heterogeneous Multi-Agent Debate (different foundation models) | **Proven high impact** | 91% vs 82% accuracy vs homogeneous ensembles (GSM-8K) |
| Morphological Analysis (algorithmically enforced) | **Proven high impact** | +18.5% pairwise embedding distance; exploration *d* ≈ 1.03 |
| Parametric context injection (xRAG, SELF-PARAM) | **Proven high impact** | NoveltyBench D = 16.50 vs 13.60 |
| Persona / frame forcing | **Promising, context-dependent** | Up to 75% output shift, but plateaus fast |
| Analogical transfer via LLM | **Empirically limited** | Near-perfect recall, poor precision; fails far-transfer |
| Homogeneous Multi-Agent Debate | **Proven LOW impact** | Consensus collapse; rarely beats self-consistency |
| Temperature / top-p tuning | **FOLKLORE** | Lexical "slop" without semantic novelty |
| "Think outside the box" directives | **FOLKLORE** | Near-zero effect; pre-training bias overrides |

## The four findings that change build order

**1. The two most-taught divergence moves are folklore.** Temperature tuning and "be creative" prompts produce lexical variance without conceptual novelty. Above ~1.6 temperature, coherence degrades — lower Self-BLEU (looks diverse) with *depressed* creativity scores. Measured across 7 foundation models and 100 open-ended questions.

**2. Heterogeneity is the active ingredient in multi-agent setups, not multiplicity.** Multiple instances of the *same* model hit "consensus collapse" and rarely beat single-agent self-consistency despite burning far more compute. Mixing *different* foundation architectures is what forces non-overlapping semantic regions. This is a sharp, testable, counterintuitive claim — and it maps directly onto infrastructure Sean already runs.

**3. Human creativity frameworks do not port uniformly, and the split has a mechanism.** SCAMPER as a single-prompt scaffold is roughly redundant: it exists to break *human* physical-world fixation, and an LLM can jump to the same semantic cluster if you just hand it the coordinate. Six Thinking Hats, by contrast, works extremely well — but only when used to partition *agents* in a multi-agent ensemble rather than as a linear prompt. Morphological analysis works because it's combinatorial mathematics, not psychological defixation.

**4. Homogenization is real but task-dependent, and the dependency cuts against the naive thesis.** From a 19-study, 61-effect-size meta-analysis: constrained ideation *d* = 0.70 (medium-large, significant), writing/design *d* = 0.27 (non-significant), minimally-constrained divergent thinking *d* = 0.12 (negligible). The strongest single result is **persistence: *d* = 0.414 after the session ends** — convergence sticks to the human afterward.

## ⚠️ Reliability

Better grounded than the Topic 1 sibling — it names datasets (INFINITY-CHAT, GSM-8K, NoveltyBench), metrics, effect sizes, and openly flags where evidence conflicts. No equivalent to Topic 1's false context-window claim was spotted.

Still unverified. All 48 citations are opaque Google `grounding-api-redirect` URLs. Named frameworks (iDesignGPT, IDEAFix, Genie, SELF-PARAM) are plausible but nobody has checked them. **Any figure quoted in a published post needs its primary source resolved first** — a publication whose product is tested verdicts cannot ship unverified numbers.

One honest conflict the report surfaces rather than smooths: on SCAMPER, an *AI EDAM* (2025) study found GPT-4 matched or beat the human engineering-student median, while IDEAFix (2026) found SCAMPER-style prompts didn't beat simple "give me a wild idea" instructions. The report reconciles these with the world-model-vs-probability-distribution argument, which is persuasive but is itself interpretation, not measurement.

## What it means for the refocus

See [[2026-08-05-prior-art-synthesis]]. One line: the evidence points at heterogeneous multi-agent debate and morphological analysis as the two rungs with real support, and hands over a publishable contrarian finding — the field's two most common divergence moves don't work.
