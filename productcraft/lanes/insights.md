---
lane: insights
seat: insights-analytics
updated: 2026-09-13
---
# Lane manifest — Insights & Analytics

Mandatory first read for the [Insights & Analytics seat](../bench/insights-analytics.md).
Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the
content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on
a machine that has it (degradation ladder otherwise). Follow only the pointers relevant to
the task. Seats stop at `## Reading path`; that section is the owner's.

This lane's two sources have opposite biases. Amplitude publishes method in order to sell a
tool; Kohavi publishes measured results in order to stop people fooling themselves. Read the
first for definitions and the second for whether a number can be believed.

## Choosing and defining a metric

- **North star vs. inputs: the dependent-variable rule** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a stakeholder asks the seat to move the headline metric directly, or proposes a metric the team can push on in a sprint.
- **The seven-point metric checklist** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a candidate metric arrives and needs a pass/fail gate before anyone writes instrumentation for it.
- **Writing a metric definition that survives a query** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a metric exists as a phrase everyone agrees on but no two people would compute the same way.
- **Input sets: breadth / depth / frequency / efficiency** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — proposing an input set, or saying whether an existing one is pitched too high or too low.

## Retention, lifecycle and instrumentation

- **Critical event, usage interval, and the three retention curves** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a retention figure is quoted without stating which computation produced it, or you are choosing a denominator for a new one.
- **Lifecycle states and the pulse ratio** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — active-user counts are climbing and someone needs an honest answer to whether that is growth.
- **Event taxonomy and the pre-analysis instrumentation audit** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — before running any analysis on a product whose tracking plan the seat did not design.

## Designing an experiment and its OEC

- **Seven Pitfalls to Avoid When Running Controlled Experiments on the Web (KDD 2009)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — drafting an OEC (the litmus test lives here), or ramp-up periods, bots or survey ratings are in the analysis.
- **Online Controlled Experiments and A/B Tests — encyclopedia entry (2023)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — the pre-flight checklist: twelve trust questions and six sensitivity levers, shorter than any of the papers.
- **Seven Rules of Thumb for Web Site Experimenters (KDD 2014)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — before promising a stakeholder how big a win to expect, or when someone calls a good-CTR module clearly good for users.
- **Rule #4 slowdown-experiment method** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — a feature ships slower than its control and the latency penalty needs pricing separately from the feature's effect.

## Trust: detecting a broken experiment

- **Diagnosing Sample Ratio Mismatch: A Taxonomy and Rules of Thumb (KDD 2019)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — the moment a scorecard shows an unexpected split, and when reviewing any platform's data-quality alerting.
- **Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained (KDD 2012)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — an experiment's early days appear to trend, running longer is proposed to buy power, or a metric moved that the change should not have touched.
- **A/B Testing Intuition Busters (KDD 2022)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — before quoting a p-value or a confidence number to anyone, and whenever a vendor tool or a small test is doing the persuading.

## Long horizons and platform scale

- **Pitfalls of Long-Term Online Controlled Experiments (IEEE Big Data 2016)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — before agreeing to a multi-month holdout or a post-period learning-effect measurement.
- **Online Controlled Experiments at Large Scale (KDD 2013)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — experiment volume is outgrowing the review process: interaction detection, alert thresholds, and what the platform costs.
- **Online Experimentation at Microsoft (Think Week 2009)** — [`kohavi-papers.md`](../corpus/canon/kohavi-papers.md) — an organization is arguing about whether to measure at all; the one-third success rate originates here.

## Reading these sources honestly

- **Correlation ranked as drivers** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a "what drives retention" finding is about to leave the seat, or a tool has handed back a ranked list of predictive actions.
- **Vendor composites: PES, focus metrics, metric trees** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — a stakeholder imports a vendor's packaged number, or asks why the studio will not report one.
- **Gaps and vendor-bias flags in this distillate** — [`amplitude-north-star.md`](../corpus/canon/amplitude-north-star.md) — before citing anything from the Amplitude file in a deliverable that leaves the studio.

## Book layer

Kohavi is ingested, and it is the systematic treatment the free papers argue toward.

- **Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* — ch. 3, 6, 7, 21** — [`books/trustworthy-online-controlled-experiments/`](../corpus/books/trustworthy-online-controlled-experiments/) — defining metrics, building an OEC, or deciding whether a measured result can be trusted at all.
- **Ellis & Brown, *Hacking Growth* — ch. 2, 3, 6** — [`books/hacking-growth/`](../corpus/books/hacking-growth/) — designing user surveys, finding a behavioral threshold, or diagnosing where users drop off.
- **Rumelt, *Good Strategy Bad Strategy* — ch. 2, 16** — [`books/good-strategy-bad-strategy/`](../corpus/books/good-strategy-bad-strategy/) — hunting the reframe or anomaly that turns a known situation into advantage.

**Read the Kohavi equations with care.** Every numbered equation was flattened in capture.
Where the surrounding prose named every variable the formula was reconstructed and is
labelled as a reconstruction in that chapter's OCR note. Where it did not — the
delta-method variance estimator (18.5–18.6) and the dilution formulas (20.2–20.6) — **no
formula is given at all**, by design; go to the original for those two. Table 2.1's cells
are gone though its narrative result survives, and subscript notation (Yᵀ/Yᶜ) is mangled
throughout, which is why chs. 18, 19 and 23 describe some notation in words. The *Hacking
Growth* cohort worksheet is corrupted and contradicts its own prose — its numbers come
from the narration, not the table.

## Reading path

Corpus states are as of the `updated:` date in the header.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (2020) | before you sign off on any experiment design | Apple Books | — none | ingested |
| 2 | Knaflic, *Storytelling with Data* | when a metrics plan has to be read by people who did not build it | listen | Cole Nussbaumer Knaflic · 5:43 | not in corpus |
| 3 | Bland & Osterwalder, *Testing Business Ideas* | — read on the discovery path | | | |
| 4 | Ellis & Brown, *Hacking Growth* | — read on the growth path | | | |
| 5 | Rumelt, *Good Strategy Bad Strategy* | — read on the strategy path | | | |

### Next

- Rodrigues, *Product Analytics* (2020) — metric design to causal inference end-to-end, in R; the deepest analytics text after Kohavi.
- Hubbard, *How to Measure Anything* — calibrated estimation and value of information; broader than product.
- Croll & Yoskovitz, *Lean Analytics* — six models by five stages with benchmarks; the benchmarks are 2013-stale, the frameworks hold.
