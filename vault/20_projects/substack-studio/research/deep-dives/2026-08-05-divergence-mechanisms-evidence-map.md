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
ai-context: "POINTER note, not the report. Full 53KB Gemini Deep Research output at vault/20_projects/research/2026-08-05-map-the-research-lineage-behind-llm-divergence-mechanisms-we.md. Topic 2 of Kickoff D. This report is materially better grounded than its Topic 1 sibling — it names datasets, metrics, effect sizes and classifications rather than vibes. VERIFICATION COMPLETE 2026-08-05 (Move C, $0): all six publishable figures resolved to primary papers and confirmed accurate AS NUMBERS, with three corrections that must travel with any published use — 91%/82% is Hegazy 2024 arXiv:2410.12853 on 2024-era models (neither cited source contains it); NoveltyBench D=16.50 vs 13.60 belongs to Bystronski et al. ACL 2026 SRW vs the G2 baseline, NOT to xRAG; and d=0.414 rests on only 2 studies with a NULL during-vs-after moderator test (p=.141), so synthesis Finding 7's masthead re-cut cannot be carried by it. All eight named frameworks confirmed real. The evidence-vs-folklore table is the single most decision-relevant artifact produced by the whole research round."
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

## Figures resolved (2026-08-05, Move C, $0)

Every publishable figure chased to its primary paper and checked **as stated in the paper**, not as paraphrased by the DR report. Method: [`audit_dr_citations.py`](../../../../../agents-sdk/scripts/audit_dr_citations.py) resolved the 48 grounding redirects, then each primary was fetched and read.

**Headline: all six numbers are real and quoted accurately. Two are attributed to the wrong source, and the masthead-critical one is far weaker than the report's framing implies.**

| Figure | Status | Primary source | What the paper actually says |
|---|---|---|---|
| **91% vs 82%** (heterogeneous vs homogeneous debate, GSM-8K) | ⚠️ **Confirmed, wrong citation** | Hegazy 2024, *Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks*, [arXiv:2410.12853](https://arxiv.org/abs/2410.12853) | Verbatim: "after 4 rounds of debate, a diverse set of medium-capacity models (Gemini-Pro, Mixtral 7BX8, and PaLM 2-M) outperforms GPT-4 on the GSM-8K benchmark, scoring 91% accuracy" and "when 3 instances of Gemini-Pro are used, performance only reaches 82%." The comparison is legitimate. **But neither cited source is the paper**: cite 14 ([arXiv:2607.20429](https://arxiv.org/html/2607.20429v1), *More Is Not More*) contains no GSM-8K result at all, and cite 13 is [emergentmind.com](https://www.emergentmind.com/topics/multi-agent-debate-mad-strategies), a trade aggregator that relays Hegazy correctly. **Caveat for publication: this is a 2024 result on 2024-era models.** Do not present it as current. |
| **+18.5% / +11.4%** (iDesignGPT diversity / coverage) | ✅ **Confirmed** | Liu, Shen, Zhang, Hou, Wang, Luo & Zhang 2026, *iDesignGPT enhances conceptual design via large language model agentic workflows*, **Nature Communications**, [PMC12936183](https://pmc.ncbi.nlm.nih.gov/articles/PMC12936183/) | Verbatim: "diversity within modules rose from 0.92 to 1.09 (Δ+18.5%)" (mean pairwise distance between solutions) and convex-hull "area increase from 15.75 to 17.54 (Δ+11.4%)." Exactly as reported. |
| ***d* ≈ 1.03** (exploration, 48 participants) | ✅ **Confirmed** | Same paper as above | Verbatim: "A total of 48 participants were involved" and "The only reliable contrast was higher Exploration for iDesignGPT than human-only (*p* = 0.026, *d* ≈ 1.03)." Note the paper's own hedge: it was the **only** reliable contrast among those tested. |
| ***d* = 0.70 / 0.27 / 0.12** (homogenization by task type) | ⚠️ **Confirmed, one label is wrong** | de Rooij & Biskjaer 2026, *Does Generative AI Make Us Think Alike? A Systematic Review and Meta-Analysis of Homogenization Effects in Human–AI Co-Creation*, ECCE2026, [doi:10.31234/osf.io/rz5s4_v1](https://doi.org/10.31234/osf.io/rz5s4_v1) · [full text](https://osf.io/download/rz5s4/) | 19 studies, 61 effect sizes ✅. Overall pooled *d* = .334, 95% CI [.094, .574]. Moderator test significant, *Q*ₘ(*df* = 3) = 17.12. Constrained ideation ***d* = 0.70**, CI [.30, 1.10] ✅ significant. Divergent thinking ***d* = 0.12**, CI [−.285, .518] ✅ negligible. **The report's "writing & design *d* = 0.27" merges two separate moderator levels** that coincidentally round the same: writing *d* = 0.27, CI [−.078, .613] and visual art/design *d* = 0.27, CI [−.555, 1.088]. Both non-significant. Do not present as one category. |
| ***d* = 0.414** (persistence after session end) | ⚠️ **Number confirmed, framing does not survive** | Same meta-analysis | See below. This is the one that matters. |
| **D = 16.50 vs 13.60** (NoveltyBench diversity) | ❌ **Number confirmed, attribution wrong** | Bystroński, Han, Chawla & Kajdanowicz 2026, *Continuous Context Sampling Allows Extending Diversity Boundaries of Large Language Models*, **ACL 2026 Student Research Workshop**, pp. 1436–1450, [aclanthology.org/2026.acl-srw.126](https://aclanthology.org/2026.acl-srw.126.pdf) | Verbatim: "At *k* = 30, it achieves D = 16.50, compared to 13.60 for G2 and 13.31 for the in-context baseline." Correctly measured on the NoveltyBench curated subset via the Distinct metric ✅. **But the report credits this to xRAG, and it is not xRAG's number.** D = 16.50 is the authors' *own* continuous-context-sampling method; 13.60 is the **G2** baseline (Ruan et al. 2025). xRAG supplies only the borrowed projector, and the paper explicitly separates itself from it: "xRAG uses embedding-based conditioning to compress external documents for efficient RAG… Their goal, however, is orthogonal to ours." **Do not publish this as evidence for "parametric context injection (xRAG, SELF-PARAM)."** |

### The *d* = 0.414 problem — read before the masthead re-cut

The number is real. Verbatim from the paper:

> "The three-level meta-analysis on the data for homogenization effects after human–AI co-creation alone showed a positive pooled effect size, *d* = .414, 95% CI [.235, .593]."

Three things the DR report left out, and each one weakens Finding 7:

1. **It rests on two studies and six effect sizes.** Verbatim: "two studies (6 effect sizes) assessing effects after AI use."
2. **The during-vs-after moderator test was NOT significant.** *Q*ₘ(1) = 2.17, *p* = .141. The authors' own sentence: **"This finding offers no evidence for a difference in homogenization during and after human–AI co-creation."** So *d* = .414 is not evidence that convergence is *specifically* sticky; it is the pooled after-condition effect, statistically indistinguishable from the during-condition effect (*d* = .453).
3. **The authors hedge it explicitly.** Verbatim: "though tentative due to the small number of studies included, suggests that homogenization effects **might** persist beyond immediate human–AI co-creative engagement." The abstract's phrasing is equally soft: "Additional analyses **suggest** that homogenization **may** persist."

**Consequence for the reconvene.** Synthesis Finding 7 proposes re-cutting the masthead from "sameness" to "stickiness" on this number, and calls it "the single most defensible claim." That does not hold. It is the *most interesting* claim and among the **least** well-supported in the paper: n = 2 studies, a null moderator test, and an authorial "might."

The re-cut is not dead, but it cannot be carried by *d* = .414 alone. Honest options: state it with the n and the hedge attached (which is on-brand for a publication whose product is honest failure), demote it from thesis to open question, or make measuring persistence a rung — the experiment the field has only two studies of is exactly the gap a tested library could fill.

### Named frameworks — all eight exist as described

| Framework | Status | Primary |
|---|---|---|
| iDesignGPT | ✅ | Nature Communications 2026, [PMC12936183](https://pmc.ncbi.nlm.nih.gov/articles/PMC12936183/) |
| IDEAFix | ✅ | *IDEAFix: Evaluation Framework for Creative Defixation Prompting in LLMs*, [arXiv:2606.00875](https://arxiv.org/abs/2606.00875) (2026-05-30) |
| GENIE | ✅ | *GENIE: A Fine-Grained Measure for Novelty*, [arXiv:2606.12790](https://arxiv.org/abs/2606.12790) (2026-06-11). Confirms Finding 8: it decomposes novelty into explainable feature vectors rather than a scalar. |
| SELF-PARAM | ✅ | *Self-Updatable Large Language Models by Integrating Context into Model Parameters*, [arXiv:2410.00487](https://arxiv.org/abs/2410.00487). Verbatim: "we propose SELF-PARAM (Self-Updatable Large Language Models with Parameter Integration)." |
| xRAG | ✅ *but mis-framed* | Cheng et al. 2024, *xRAG: Extreme Context Compression for RAG with One Token*, [arXiv:2405.13792](https://arxiv.org/abs/2405.13792). Real, but it is a **context-compression** method, not a diversity method. |
| CreativityPrism | ✅ | [arXiv:2510.20091](https://arxiv.org/abs/2510.20091) (2025-10-23) |
| NoveltyBench | ✅ | Zhang et al. 2025, [arXiv:2504.05228](https://arxiv.org/abs/2504.05228) |
| INFINITY-CHAT | ✅ | Dataset in *Artificial Hivemind: The Open-Ended Homogeneity of Language Models*, [arXiv:2510.22954](https://arxiv.org/abs/2510.22954) |

### Net

Topic 2's 90%-defensible rating is earned. Every number checked was real and quoted accurately, which is a genuinely good result for a DR run. The failures are **attribution and framing**, not fabrication: two figures credited to the wrong system, one category label merged, and one effect size promoted past what its paper claims. All are catchable at $0 by reading the primary, and none would have been caught by a recency filter or a tier audit alone.

## ⚠️ Reliability

Better grounded than the Topic 1 sibling — it names datasets (INFINITY-CHAT, GSM-8K, NoveltyBench), metrics, effect sizes, and openly flags where evidence conflicts. No equivalent to Topic 1's false context-window claim was spotted.

~~Still unverified.~~ **RESOLVED 2026-08-05** — see "Figures resolved" above. All 48 redirects resolved; all six publishable figures traced to primaries and read; all eight named frameworks confirmed to exist as described. Three corrections carry forward to any published post: the 91%/82% figure is Hegazy 2024 (2024-era models, not the cited papers), the NoveltyBench D = 16.50/13.60 belongs to continuous context sampling vs the G2 baseline and **not** to xRAG, and *d* = 0.414 is a 2-study pooled effect whose during-vs-after moderator test was null.

One honest conflict the report surfaces rather than smooths: on SCAMPER, an *AI EDAM* (2025) study found GPT-4 matched or beat the human engineering-student median, while IDEAFix (2026) found SCAMPER-style prompts didn't beat simple "give me a wild idea" instructions. The report reconciles these with the world-model-vs-probability-distribution argument, which is persuasive but is itself interpretation, not measurement.

## What it means for the refocus

See [[2026-08-05-prior-art-synthesis]]. One line: the evidence points at heterogeneous multi-agent debate and morphological analysis as the two rungs with real support, and hands over a publishable contrarian finding — the field's two most common divergence moves don't work.
