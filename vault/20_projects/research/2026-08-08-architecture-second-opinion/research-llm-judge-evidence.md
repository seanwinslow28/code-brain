All research complete. Here is the structured report.

# LLM-as-Judge for Production Quality Gates — Evidence Report (researched 2026-08-08)

Tags are relative to the target design: 2-model cross-vendor panel, axis-specific disagreement policies, Unknown escape, pre-registered max Needs-Review rate, Pass/Drift/Needs-Review verdicts on visual+text serial content.

## Area 1 — Judge pathologies and 2026 mitigation status

**Quantifying and Mitigating Self-Preference Bias of LLM Judges** — https://arxiv.org/html/2604.22891v2 (Apr 28, 2026)
- NEW: Measures self-preference net of style/length confounds (PIR minus Null-PIR baseline) across 20 models: 8 positive-bias, 9 *negative*-bias, 3 near zero. Claude-Sonnet-4.5 was the strongest negative-bias judge (β=−0.229); high capability does not predict fairness. Implication: don't assume self-preference is universal — measure your specific judge pair.
- CONFIRMS: Structured multi-dimensional pairwise forced-choice (5 axes, majority vote) cut self-preference 31.5% on average (up to 69.9%) with no discriminability loss — and **outperformed CoT prompting**. Implication: axis-decomposed judging is the right architecture; per-axis structure is itself a bias mitigation.

**Self-Preference Bias in LLM-as-a-Judge** — https://arxiv.org/pdf/2410.21819 (2024, mechanism baseline)
- CONFIRMS: Mechanism is perplexity familiarity — judges rate lower-perplexity (own-distribution-like) text higher. Implication: cross-vendor panels attack the root mechanism, not just the symptom.

**Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge** — https://arxiv.org/pdf/2410.02736 (2024 baseline, still-cited catalog)
- CONFIRMS: The canonical 12-bias catalog (position, verbosity, self-preference, sycophancy/authority, etc.) remains the reference frame; 2026 work refines measurement rather than retiring any of them.

**FutureAGI bias-mitigation and judge-prompting guides** — https://futureagi.com/blog/evaluating-llm-judge-bias-mitigation-2026/ and https://futureagi.com/blog/what-is-llm-judge-prompting-2026/ (2026, trade)
- CONFIRMS: 2026 production consensus: position bias handled by swap tests/order randomization; verbosity by explicit rubric language + length normalization; self-preference by cross-family judges; CoT-before-score claimed to raise agreement 10–20% (G-Eval lineage: Spearman 0.51→0.66). Implication: rubric + swap + cross-vendor is the standard defense stack — the design matches consensus.
- CHALLENGES (nuance): CoT-helps is trade-consensus, but the 2604.22891 result above found structured pairwise beat CoT for bias reduction — CoT is not the strongest mitigation anymore, structure is.

**Score compression / rubric anchoring** — https://arxiv.org/html/2603.00077v1 (Autorubric, 2026) and RULERS (Hong et al. 2026, via https://www.emergentmind.com/topics/rulers-rubric-unification-locking-and-evidence-anchored-robust-scoring)
- CONFIRMS: Score compression (mid-scale clustering) is documented; 2026 mitigation is "locked rubrics" with evidence rules mapping specific textual evidence to each level, concrete behavioral anchors at 5/3/1, JSON schemas. Confidence/authority bias shrinks but does not disappear under rubric control. Implication: categorical verdicts (Pass/Drift/Needs-Review) with evidence-anchored definitions sidestep score compression better than numeric scales.

**Reliability without Validity** — https://arxiv.org/pdf/2606.19544 (Jun 19, 2026)
- CHALLENGES: Judges can show acceptable agreement/consistency statistics while failing validity — reliability metrics alone don't certify a judge. Implication: your calibration set must test *correctness against ground truth*, not just judge-judge or judge-human agreement rates.

## Area 2 — Panel vs single judge

**Replacing Judges with Juries (PoLL)** — https://arxiv.org/abs/2404.18796 (2024, foundational)
- CONFIRMS: Panel of 3 small cross-family judges (command-r, gpt-3.5, haiku) beat single GPT-4 judge on human-correlation across 6 datasets at ~1/7 the cost; disjoint families reduce intra-model bias. Implication: 2-model cross-vendor is directionally supported; 3 families is the studied configuration.

**Who Judges the Judge? LLM Jury-on-Demand** — https://arxiv.org/pdf/2512.01786 (Dec 1, 2025)
- NEW: *Dynamic* juries (reliability-predictor-weighted, per-instance judge selection) beat both single judges and **static juries** on summarization/RAG. Implication: a fixed 2-model panel is a middle rung; per-axis reliability weighting (which your axis-specific policies approximate) is where the frontier moved.

**Hidden Measurement Error in LLM Pipelines (TEE)** — https://arxiv.org/pdf/2604.11581 (Apr 2026)
- NEW: Variance decomposition over full eval pipelines: judge disagreement contributed **43.8–44% of total variance** in a 3-judge safety-classification design — dwarfing prompt wording (4%). Implication: the judge panel is the dominant error lever; disagreement events are signal-rich and worth routing to Needs-Review rather than averaging away.

**LLM Judges Inconsistently Disagree Across Safety Criteria** — https://arxiv.org/html/2605.31381 (Jun 2, 2026)
- CONFIRMS (strongly, for your design): Disagreement is **criterion-specific** — observable criteria hit κ≈0.90 while interpretive ones (cultural sensitivity) sit near zero; cross-consistency α ranges −0.04 to 0.53 by category; 98% raw agreement can coincide with α≈0 under label imbalance. Authors explicitly recommend **criterion-specific judge selection**. Implication: axis-specific disagreement policies are exactly what this paper prescribes; also — use chance-corrected agreement (κ/α), never raw agreement, when your Pass rate is high.
- CHALLENGES: "Using diverse judges without alignment creates variability rather than reliability" — a cross-vendor panel only helps if judges are calibrated to a shared rubric per axis first.

## Area 3 — VLM judges for image comparison

**FineGRAIN** — https://arxiv.org/html/2512.02161 (Dec 1, 2025)
- CONFIRMS: VLM judges (Molmo-72B, InternVL3-78B, Pixtral-124B) average only ~74–77% accuracy detecting T2I failure modes. Good: color attribute binding (~84%), object counts (near-human with targeted prompting). Bad (<50%): text rendering (short *and* long), surreal/out-of-distribution scenes, opposite relations, anatomy/physics. Human agreement 67.4% even for the best method. Implication: for serial visual content, don't trust the judge on rendered text or unusual compositions — route those axes to deterministic checks (OCR) or Needs-Review.

**VLM Judges Can Rank but Cannot Score** — https://arxiv.org/abs/2604.25235 (Apr 28, 2026)
- NEW (key finding): "Ranking-scoring decoupling" — VLM judges order outputs well but absolute scores carry prediction intervals covering ~40% of the score range (natural images/aesthetics) to ~70% (charts/math); intervals 4.5× narrower on cleaner data. Mitigation: conformal prediction from score-token log-probs, no retraining. Implication: strong support for comparison-against-reference verdicts (Drift = comparative) over absolute quality scores; consider conformal intervals to power the Unknown escape.

**MM-JudgeBias** — https://arxiv.org/pdf/2604.18164 (Apr 24, 2026, NAVER AI)
- NEW: Benchmark for compositional biases in multimodal judges, including *unnecessary image dependencies* (judges leaning on the image when they shouldn't, and vice versa). Implication: a usable off-the-shelf benchmark to qualify your two VLM judges before shipping.

**Judging to Improve: De-biased VLM-as-3D-Judge** — https://arxiv.org/html/2606.20364v1 (Jun 2026)
- CONFIRMS: In-the-loop VLM judging exposes image overload (multi-image prompts collapse the judge into position-answering) and reference-free judging rewarding clean-but-wrong outputs. Implication: keep image counts per judgment low and always judge *against the reference*, never reference-free.

## Area 4 — Production calibration practice

**Galileo: Calibrate Your LLM Judge With Human Annotations** — https://galileo.ai/blog/calibrate-llm-judge-human-annotations (2025-26, trade) and **FutureAGI best-practices** — https://futureagi.com/blog/llm-as-judge-best-practices-2026 (2026, trade)
- CONFIRMS: Production pattern: gold-set + Cohen's kappa calibration; common trigger threshold ~75% agreement → recalibrate (prompt update, judge swap, or gold-set expansion); monthly re-runs against the calibration set; alert on kappa drops.
- CONFIRMS: Provider model updates are a documented *silent* drift source. Recommended contract: pin `judge_model_id` + `rubric_version` + `prompt_template_hash`; treat a judge model swap as an eval-suite migration, not a config change. Implication: your drift monitoring must cover the judges themselves, not just the content.

**ArgminAI: Why your LLM judge disagrees with your experts** — https://blog.argminai.com/how-to-calibrate-an-llm-judge-to-agree-with-your-experts (2026, trade)
- CONFIRMS: Judge-expert disagreement is usually rubric underspecification, fixed by iterating rubric wording against labeled disagreement cases rather than swapping models.

**reloadux: AI Uncertainty & Trust Design Framework** — https://reloadux.com/blog/ai-uncertainty-trust-design-framework/ (2026, trade)
- CONFIRMS: Threshold-based abstention (act above confidence threshold, surface for human review below) is the 2026-standard pattern — your Unknown escape is mainstream practice, and 2604.25235's conformal intervals give it a statistical footing.

## Area 5 — Judge verdicts as user-facing product output

**Evaluating the Impact of Explainable AI on Trust in AI-Assisted Code Review** — https://arxiv.org/html/2607.24601v1 (Jul 27, 2026)
- NEW (most relevant 2026 result for receipts): 34-developer within-subjects study. Detailed explanations → highest *perceived* trust (3.99/5 vs 3.41 without, p=0.0006) but **lower behavioral agreement** (77.5% vs 89.2% for terse feedback) — users scrutinize more when shown reasoning, which the authors read as calibrated rather than blind trust. Implication: rich receipts make users trust the *system* more while agreeing with individual verdicts less — that trade-off is desirable for a Needs-Review product, but expect explanations to *increase* human overrides, not reduce them.
- NEW: With no explanation at all, users stop engaging rather than complain ("wrong recommendation with no visible explanation" → silent feature abandonment, echoed in 2026 AI-UX trade coverage, e.g. https://www.designwhine.com/ux-evaluation-methods-for-ai-products-in-2026/). Implication: shipping verdicts without receipts is the worst option.

## Judge-lane design implications from the freshest evidence

- **Your axis-specific disagreement policies are the single best-supported element of the design.** The June 2026 safety-criteria paper (2605.31381) directly prescribes criterion-specific judge treatment: agreement is real on observable axes (κ up to ~0.9) and near-fictional on interpretive ones — so set per-axis disagreement policy *and* per-axis agreement targets, measured with chance-corrected κ/α, never raw agreement (98% raw can mask α≈0 at high Pass rates).
- **Prefer comparative/categorical over absolute scoring everywhere.** The April 2026 "Rank but Cannot Score" result shows VLM absolute scores carry 40–70%-of-range uncertainty while rankings hold; Drift-vs-reference verdicts and forced-choice per-axis checks (which also cut self-preference 31.5%, beating CoT) exploit exactly what judges are good at.
- **The 2-model cross-vendor panel is supported but under-powered relative to the frontier.** PoLL used 3 disjoint families; Jury-on-Demand (Dec 2025) shows reliability-weighted dynamic juries beat static ones. With 2 judges you get disagreement detection but no majority — which is fine *only because* you route disagreement to Needs-Review/Unknown; the TEE paper (44% of variance is judge disagreement) confirms those disagreement events are your highest-information samples, so log and mine them.
- **Carve out deterministic escapes for known VLM blind spots.** FineGRAIN: text rendering is <50%-accuracy territory for VLM judges (use OCR), and out-of-distribution/surreal compositions diverge from humans >50% of the time — for stylized serial content, pre-register those axes as auto-Needs-Review or tool-checked rather than judge-decided; keep images-per-judgment low and always judge against the reference (2606.20364).
- **Calibrate for validity, and treat judges as versioned dependencies.** "Reliability without Validity" (Jun 2026) warns agreement stats alone don't certify a judge — the gold-set must contain known-answer cases. Pin judge_model_id + rubric_version + prompt hash, re-run the calibration set monthly (provider updates drift silently), and expect your receipts to raise perceived trust while *increasing* user overrides (2607.24601) — budget the pre-registered Needs-Review rate to absorb human pushback, not just judge abstention.

Sources: all URLs listed inline above; primary papers are arXiv 2604.22891, 2404.18796, 2512.01786, 2604.11581, 2605.31381, 2512.02161, 2604.25235, 2604.18164, 2606.20364, 2606.19544, 2607.24601, plus trade sources FutureAGI, Galileo, ArgminAI, reloadux, Confident AI.