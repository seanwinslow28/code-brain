---
title: "Prior-Art Synthesis — What Should Change About What Gets Built First"
type: research-synthesis
status: complete
domain: [substack-studio]
tags: [pencil-and-prompt, refocus-2026-08, synthesis, prior-art, divergence, building-the-ladder, tested-library, gemini-deep-research]
created: 2026-08-05
last-updated: 2026-08-05
sources: [gemini-deep-research]
inputs: [2026-08-05-tested-mechanism-library-prior-art, 2026-08-05-divergence-mechanisms-evidence-map]
cost_usd: 5.60
ai-context: "Kickoff D step 4. Synthesis across BOTH DR reports. Findings are evidence-linked to the two reports, NOT independently verified — Topic 1 contains a known false claim, and all citations in both are opaque Google grounding-redirect URLs. This document decides nothing. The reconvene partner session (sidecar ~/.creative-harness/partner-sessions/2026-08-04-pencil-and-prompt-refocus.md) makes the calls. Written to be argued with."
---

# Prior-Art Synthesis — What Should Change About What Gets Built First

Two Gemini Deep Research runs, 2026-08-05, $5.60 total. Topic 1 = does a tested mechanism library already exist. Topic 2 = which divergence mechanisms have evidence behind them.

**Status of everything below: evidence-linked, not verified.** Both reports cite through opaque Google redirect URLs, and Topic 1 contains at least one plainly false factual claim. Treat each finding as a strong lead. Nothing here is a decision; the reconvene session decides.

---

## Finding 1 — The library bet survives, but the report's own "yes" answer is weaker than it looks

Topic 1 answers "does any library publish per-entry tested verdicts with honest failures?" with **yes**, naming Techpresso AI Academy (publishes "honest failures alongside" successes) and Aksoy Capital (1-hour retraction SLA, URL preservation, public correction logs).

Read the two examples and the "yes" thins out. Techpresso is human expert curation with no programmatic testing. Aksoy Capital is genuinely rigorous but is *algorithmic financial research*, not a prompt or technique library. Neither is a tested mechanism library in the sense the refocus means.

**What changes:** the bet is defensible, but the positioning claim must be precise. Not "nobody publishes tested verdicts" — that's falsifiable and someone will falsify it. The accurate claim is narrower and stronger: **the rigor exists but stays private, and the public artifacts have no evidence standard.**

## Finding 2 — The real white space is the *seam*, not either side of it

Topic 1's landscape splits cleanly in two. Enterprise eval infrastructure (Future AGI, Braintrust, MLflow, Langfuse, DeepEval) has serious per-entry rigor: CI/CD eval gates that block deploys, immutable version snapshots, production traces auto-converted into regression tests. All private, engineer-facing, never published as a public library. Consumer marketplaces (PromptBase, ~260k prompts, a reported $2.51B market) publish freely with no evidence standard at all — the report's phrase is that a $1.99 text string carries "no cryptographic or statistical guarantee."

Nobody has put enterprise-grade evidence discipline behind public, creative-practitioner-facing artifacts.

**What changes:** that seam is the product thesis, stated more sharply than "a tested library." It also means the credible comparison class is eval infrastructure, not prompt packs. Borrow their vocabulary — regression, gate, verdict, retraction — rather than the marketplace's.

## Finding 3 — Two of the field's most-taught divergence moves are folklore, and that is the strongest post in the pile

Topic 2 classifies **temperature/top-p tuning** and **"think outside the box" prompt directives** as practitioner folklore with negligible effect on semantic diversity. A factorial experiment across 7 foundation models and 100 open-ended questions found both produced mathematically negligible effects. Past ~1.6 temperature, outputs degrade into "slop": Self-BLEU drops (looks more diverse) while human and algorithmic creativity scores fall.

**What changes:** this is the highest-value publishable finding of the round. It is contrarian, evidence-backed, immediately testable on Sean's own fleet, and it fits the masthead exactly — the median advice *is* the convergent advice. A Building the Ladder rung that kills two moves the reader currently trusts earns more credibility than one that adds a third.

## Finding 4 — Heterogeneity, not multiplicity, is the active ingredient — and Sean already runs the infrastructure

Topic 2 is unambiguous: homogeneous multi-agent debate (many instances of one model) hits **consensus collapse** and rarely beats single-agent self-consistency while burning far more compute. Heterogeneous debate — genuinely different foundation architectures — is what forces traversal of non-overlapping semantic regions. Reported: 91% vs 82% accuracy on GSM-8K.

Sean already operates exactly this: `llm-council` (4 vendors + chairman) and `fusion-discovery-council` (OpenRouter Fusion panel + judge). The mechanism with the strongest evidence in the entire map is one he has running infrastructure for and lived incidents about.

**What changes:** this is the strongest candidate for **rung #1**. It satisfies the value gate's Solution slot with an artifact that already exists, and it lands in the native-fleet-experience lane approved on 2026-08-04. The baseline experiment writes itself: same prompt, homogeneous panel vs heterogeneous panel, measured on semantic rather than lexical diversity.

## Finding 5 — Morphological analysis is the sleeper, and it's cheap to test

Reported gains are the most concrete numbers in either report: **+18.5% design diversity** (mean pairwise distance between embeddings), +11.4% solution-space coverage, exploration effect size *d* ≈ 1.03 across 48 participants. It works for a reason that generalizes — it's combinatorial mathematics, not psychological defixation, so the human-to-LLM port doesn't lose its mechanism.

**What changes:** strongest rung-#2 candidate. Unlike multi-agent debate it needs no fleet, so it travels to a reader with one chat window — which is the two-tier tooling rule in §4 of the project CLAUDE.md.

## Finding 6 — Human creativity frameworks port unevenly, and the split is a whole post

SCAMPER as a single-prompt scaffold is roughly redundant: it exists to break *human* physical-world fixation, and an LLM can reach the same semantic cluster if handed the coordinate directly. Six Thinking Hats works extremely well, but only when partitioning **agents** in an ensemble, not as a linear prompt. Morphological analysis works because it's combinatorics.

The reports openly conflict here — *AI EDAM* (2025) found GPT-4 with SCAMPER matched or beat the human engineering-student median; IDEAFix (2026) found SCAMPER-style prompts didn't beat a simple "give me a wild idea." Topic 2 reconciles this with a world-model-vs-probability-distribution argument that is persuasive interpretation, not measurement.

**What changes:** "which human creativity techniques survive the port, and why" is a Building the Ladder arc rather than a single rung. The conflict is a feature — publishing it with the disagreement intact is exactly the honest-failure posture the masthead promises.

## Finding 7 — The masthead thesis needs a sharper edge than "convergent output"

The homogenization meta-analysis (19 studies, 61 effect sizes) shows the effect is strongly task-dependent, and the dependency cuts against the loose version of the thesis:

- Constrained ideation: *d* = 0.70 (medium-large, significant)
- Writing & design: *d* = 0.27 (non-significant in isolation)
- Minimally-constrained divergent thinking: *d* = 0.12 (negligible)
- **Persistence after the session ends: *d* = 0.414 (significant)**

So "AI makes everyone's output the same" is weakest precisely where a casual reader assumes it's strongest — free-form creative play — and strongest on constrained, real-work ideation. The single most defensible claim is the persistence one: convergence follows the human out of the session.

**What changes:** the masthead should lead with **stickiness**, not sameness. "It doesn't just flatten this draft, it flattens the next one you write without it" is more specific, better supported, more unsettling, and much harder for a skeptic to wave off. It also implies the right unit of demonstration — measure the human's *next* unaided output, not just the model's.

## Finding 8 — Measurement is contested, and picking the metric is a load-bearing editorial decision

Lexical metrics (n-gram overlap, Self-BLEU, Distinct) are considered insufficient: output can have near-zero lexical overlap and identical conceptual content. Newer semantic approaches have their own failure — naive embedding-cosine conflates novelty with incoherence, which is why "effective semantic diversity" restricts the pool to high-quality outputs only. NoveltyBench forces novelty to a scalar and misses peripheral interventions; Genie decomposes it into an explainable vector.

Notably, under effective semantic diversity, **preference-tuned models look more diverse than base models until you restrict to high-quality outputs — then preference tuning demonstrably reduces diversity.** The metric choice flips the finding.

**What changes:** this is the hardest constraint on the tested-library product. A per-entry verdict is only as credible as its metric, and a library that ships "beat/tied/lost" without publishing *what was measured* reproduces the marketplace trust problem it exists to solve. **The library needs a published measurement protocol before it needs entries.** That is a build-order inversion: protocol first, then rung #1.

---

## Build order implied by the above

1. **Publish the measurement protocol** (Finding 8) — what counts as beat/tied/lost, on what metric, with what baseline. The library's credibility is bounded by this, so it cannot come second. **Upgraded 2026-08-05:** post-Move-B this is not merely a credibility gate, it is the *entire* differentiation (see amendments below).
2. **Rung #1: heterogeneous vs homogeneous panels** (Finding 4) — strongest evidence, infrastructure already exists, native to Sean's lane.
3. **Rung #2: morphological analysis** (Finding 5) — concrete effect sizes, travels to readers without a fleet.
4. **The folklore post** (Finding 3) — can run early and independently; it's the credibility opener.
5. Re-cut the masthead toward persistence (Finding 7) before the doc re-anchor ticket runs.

## Verification debt — PARTIALLY CLEARED 2026-08-05

A $0 [citation tier audit](deep-dives/2026-08-05-citation-tier-audit.md) resolved all 108 grounding-redirect URLs and classified them. **It materially changes how much of the above you can lean on. Read it before the reconvene.**

**The redirects resolve.** 108/108. DR output is cheaply auditable, and tier-auditing should become a standing pre-citation step for every future run.

**The two reports are not equally trustworthy — not close:**

| | Defensible sourcing (academic + primary) |
|---|---|
| Topic 2 (divergence evidence) | **43 / 48 = 90%** — NeurIPS, ACL, EACL, AAAI, PNAS, TACL, INFORMS, 4× Cambridge *AI EDAM*, ~15 arXiv |
| Topic 1 (library prior art) | **14 / 60 = 23%** — against 39 vendor-marketing / SEO pages |

**UPDATE — Findings 1 and 2 came OFF probation the same day.** [Move A verification](deep-dives/2026-08-05-move-a-verification-two-named-examples.md) ($0) checked both load-bearing examples directly. **Techpresso is falsified** — 50 copy-paste prompts, zero evaluation results, zero documented failures; the "honest failures" claim is not on the page. **Aksoy Capital's policy is real and accurately reported**, but `/data/retracted/`, `/retractions/` and `/corrections/` all 404 with no searchable instance, so it is an unexercised commitment — and it is algorithmic financial research, not a technique library. Net: **no prompt or technique library publishes per-entry tested verdicts with honest failures.** The claim must be restated in that precise form (see Move A note); the broad "nobody does this" version is falsifiable via Aksoy. Residual exposure is *coverage*, not these two entities — Move B must still run.

**Original probation note, retained for the record.** Both derive from Topic 1, and the audit found two disqualifying defects: nine of its sixty citations are `futureagi.com`'s own SEO marketing (Future AGI is also row 1 of the landscape matrix — a vendor ranked first using its own comparison content), and **both load-bearing examples are self-reported**. The Techpresso "honest failures" claim rests on three of Techpresso's own product pages; the Aksoy Capital retraction-SLA claim rests on Aksoy Capital's own policy pages. Zero third-party verification for the finding the product bet leans on.

The *shape* of Findings 1–2 may still be right — the seam thesis is plausible and Finding 2's split matches how the market obviously works. But it is currently unevidenced, and it must not be published until independently checked.

**Findings 3–8 stand.** All derive from Topic 2's 90%-defensible base. Individual figures still need their primary source resolved before publication, but that is a lookup against a named paper, not archaeology.

### Remaining debt — CLEARED 2026-08-05 (Moves B and C, $0 each)

- ~~Resolve primary sources for every publicly quoted figure~~ → **DONE.** [Figures resolved](deep-dives/2026-08-05-divergence-mechanisms-evidence-map.md#figures-resolved-2026-08-05-move-c-0). All six real and quoted accurately; three corrections carry forward (see Finding 7 update below and Finding 4's date caveat). All eight named frameworks confirmed to exist.
- ~~Independently verify Techpresso and Aksoy Capital~~ → **DONE** ([Move A](deep-dives/2026-08-05-move-a-verification-two-named-examples.md)).
- ~~Replace Topic 1 with a named-candidate falsification pass~~ → **DONE** ([Move B](deep-dives/2026-08-05-move-b-candidate-falsification.md)). Also discharges refocus-ticket item 2 (Executive Circle competitive checks).
- Drop the `$2.51B` market-size figure and the `10–30× creative diversity` claim unless independently sourced — the first traces to SEO content, the second to `springboards.ai`'s own blog. **Still open; simplest fix is not to use them.**

---

## Post-verification amendments — READ BEFORE THE RECONVENE

Two of the eight findings changed materially once the primaries were read. Both changes are the round working as designed: caught at $0, before publication.

### Amendment to Findings 1–2 — the white space is CUMULATION, not testing

[Move B](deep-dives/2026-08-05-move-b-candidate-falsification.md) checked twelve named candidates directly. Eleven are clean NOs with URLs behind each: Anthropic's prompt library, DAIR.AI, promptingguide.ai, LangSmith Hub, PromptHub, PromptLayer, Braintrust, DSPy, OpenAI Cookbook, awesome-chatgpt-prompts, and HF `finephrase`. LangSmith states the standard's absence outright: its hub prompts are **"user-generated and unverified."**

The twelfth is the finding. The Executive Circle pass surfaced **Nate Jones** — the incumbent the project CLAUDE.md already names — running a real controlled experiment on 2026-07-15: 742-word brief vs 5,197-word method, three runs each, two blind scorers, and a binary delivery contract. His richer artifact scored better on content (19.67 vs 17.5 / 20) and **failed delivery two runs out of three**. He publishes the loss, refuses to over-claim from it, and ships an evidence-labelling vocabulary (`VERIFIED` / `INFERRED` / `INACCESSIBLE` / `NOT_EXPOSED`).

**So "we publish tested verdicts with honest failures" is no longer a differentiator.** It is falsified as a novelty claim by the nearest competitor in Sean's exact lane.

What survives, and it is narrower and better: **nobody makes it cumulative.** Nate's rigor is per-post and inconsistent (the same author's "I Tested OpenAI's 200 Prompt Templates" publishes zero measurements). The rigor exists in three places and none of them accumulate — private enterprise eval tooling, out-of-domain financial retraction discipline, and one-off practitioner experiments. A per-entry, versioned, retractable library against a *published* measurement protocol does not exist.

**This makes Finding 8 load-bearing rather than merely prudent.** The measurement protocol is not a credibility prerequisite for the library; it *is* the differentiation. A library of verdicts without a published protocol is Nate's posts with worse distribution.

### Amendment to Finding 7 — the masthead re-cut cannot be carried by *d* = 0.414

The number is real (95% CI [.235, .593]) but three facts the DR report omitted break the framing:

1. It rests on **two studies, six effect sizes**.
2. The during-vs-after moderator test was **not significant** (*Q*ₘ(1) = 2.17, *p* = .141). The authors' own words: *"This finding offers no evidence for a difference in homogenization during and after human–AI co-creation."*
3. The authors hedge: persistence *"might"* occur, *"tentative due to the small number of studies."*

Finding 7 called persistence "the single most defensible claim." It is closer to the least defensible of the four task-type figures. Also: the report's "writing & design *d* = 0.27" silently merges two separate moderator levels (writing 0.27, visual art/design 0.27) with very different confidence intervals.

The stickiness re-cut is not dead. But it must either ship with the n and the hedge attached, drop from thesis to open question, or become a rung — *"the field has two studies on whether this sticks; here is a third"* is a strong Building the Ladder move and fits the masthead better than borrowing a number that cannot hold the weight.

### Smaller corrections that travel with any published post

- **Finding 4's 91%/82%** is real but comes from **Hegazy 2024** ([arXiv:2410.12853](https://arxiv.org/abs/2410.12853)), not from either cited source, and it is a **2024 result on 2024-era models** (Gemini-Pro, PaLM 2-M, Mixtral 7B×8 vs GPT-4). Do not present it as current. The mechanism claim stands; the number needs its date.
- **The NoveltyBench D = 16.50 vs 13.60 figure is not xRAG's.** It belongs to continuous context sampling (ACL 2026 SRW) measured against the **G2** baseline. The paper explicitly calls xRAG's goal "orthogonal to ours." Drop it from any "parametric context injection" claim.
- **Findings 3, 5, 6 and 8 are unamended.** iDesignGPT's +18.5% / +11.4% / *d* ≈ 1.03 / 48 participants all confirmed verbatim in **Nature Communications**.

### The methodological lesson (worth a post on its own)

Query shape determined source tier. A research-shaped question pulled 88% academic sources; a market-shaped question pulled 65% vendor marketing — same model, same tier, same day, same recency instruction. And the bad sources were not *stale*, they were aggressively fresh 2026 marketing, which recency filters cannot catch.

A publication whose product is *tested verdicts with honest failures* cannot ship unverified numbers in the post announcing it. Clearing this debt is part of rung #1, not a chore after it.
