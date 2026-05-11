---
type: research-report
project: prj-job-hunt-2026
research_topic: eval-design-canon-2026
created: 2026-05-09
model: perplexity-research
ai-context: "Fluency primer + reference eval cases for the Week 5 vault-synthesizer evals build. All claims cited; intermediate fluency calibrated."
***

# Eval Design Canon 2026 — Fluency Primer + Reference Cases for the Vault Synthesizer

***

## 1. The 2026 Canon — What the Field Agrees On

These are the claims that triangulate across Hamel Husain / Shreya Shankar practitioner writing, Anthropic system cards, the UK AISI Inspect framework, and the Brendan Foody / Mercor practitioner stream. Use these as interview anchors.

**1. Error analysis must precede automated evaluators.** Hamel Husain states this as the most important principle in his course FAQ: "Start with error analysis, not infrastructure. Spend 30 minutes manually reviewing 20–50 LLM outputs whenever you make significant changes."  The corollary is that you cannot write meaningful evals for failure modes you haven't first observed in data. **Confidence: HIGH** — this view appears consistently in Husain's public blog posts, the course FAQ, and is corroborated by the Lenny's interview with Husain (Oct 2025).[^1][^2][^3]

**2. Generic off-the-shelf metrics create false confidence.** The Husain–Shankar course is blunt: "All you get from using these prefab evals is you don't know what what they actually do and in the best case they waste your time and in the worst case they create an illusion of confidence that is unjustified."  Anthropic's system card methodology mirrors this by domain-scoping every eval to a specific capability risk (CBRN, cyber, autonomy) rather than using general LLM benchmarks. **Confidence: HIGH.**[^2][^4]

**3. Binary pass/fail beats Likert scales for most evals.** The Husain–Shankar course FAQ recommends binary labels because "Likert scales introduce significant challenges: the difference between adjacent points is subjective and inconsistent across annotators."  Anthropic's uplift-trial rubrics use threshold-based pass/fail logic (>50%–80% success triggers escalation). **Confidence: HIGH.**[^2]

**4. LLM-as-judge requires calibration against human labels before you can trust it.** Husain's "Creating a LLM-as-a-Judge That Drives Business Results" post walks through measuring TPR/TNR against a held-out labeled set as the prerequisite for deploying an automated judge.  Both the Hamel–Shreya and Anthropic frameworks use human expert review as the ground-truth signal. **Confidence: HIGH.**[^2]

**5. Expert domain knowledge cannot be outsourced during annotation.** The Husain–Shankar "benevolent dictator" pattern — a single domain expert as the definitive pass/fail arbiter — is a consistent recommendation in course materials  and practitioner interviews. Anthropic system cards employ external domain experts (biosecurity, cybersecurity, clinical psychiatry) as an extension of this idea. **Confidence: HIGH.**[^3][^4][^2]

**6. Evals are now the primary quality signal for AI companies and ship decisions, not a post-hoc QA step.** Brendan Foody (CEO of Mercor, the fastest-growing company to $500M in 17 months by supplying expert evaluators to AI labs) articulated this directly in a September 2025 Lenny's Podcast episode: "evaluations aren't just technical benchmarks, but the new PRDs and even the sales collateral for AI companies."  **Note: This quote comes from a Lenny's Newsletter transcript of the Sept 2025 podcast episode** ([lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody](https://www.lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody), accessed 2026-05-09).  **Confidence: HIGH for the quote source; the "evals are the new PRDs" framing is attributed to Foody in this episode, not a standalone blog post.**[^5]

**7. Short-horizon evals give misleading assurance for agentic tasks.** Anthropic's April 2026 Claude Mythos Preview system card disclosed that their automated behavioral audit evaluations "struggle to emulate the kinds of long-running sessions on network-connected computers" where the most concerning behaviors emerged.  Husain's agent-eval FAQ makes the same point about multi-step agent traces requiring full-session review, not single-turn snapshots. **Confidence: HIGH — appears in multiple independent Anthropic system cards and in the Husain–Shankar course FAQ.**[^6][^2]

**Where the canon disagrees:** Hamel–Shreya recommend _against_ eval-driven development (write evals after observing errors, not before), while some platform vendors (Braintrust, Promptfoo) and CI/CD-oriented practitioners advocate test-first workflows. The defensible interview answer is: "For novel LLM products, error-first is safer because you can't predict all the failure modes in advance; test-first only makes sense when you have a well-understood constraint you know will matter (e.g., 'never mention competitors')."[^2]

***

## 2. The Hamel–Shreya Course Canon

The "AI Evals for Engineers & PMs" course runs on Maven ([maven.com/parlance-labs/evals](https://maven.com/parlance-labs/evals), accessed 2026-05-09), taught by Hamel Husain (ML engineer, 20+ years experience) and Shreya Shankar (ML systems researcher). As of the September–October 2025 cohort, the course had trained 2,000+ engineers and PMs, including teams at OpenAI and Anthropic. Maven lists it as the top-grossing course on the platform. The next cohort is scheduled for September 7–October 2, 2026.[^7][^8][^9][^10]

**Publicly accessible course content** includes the course landing page, Husain's blog posts at hamel.dev, the free course FAQ posted publicly at [hamel.dev/blog/posts/evals-faq/](https://hamel.dev/blog/posts/evals-faq/), and a 51-page AI Evals FAQ PDF released publicly in September 2025. The 150+ page course reader and live sessions are **paywalled**.[^11][^2]

The 10 core concepts from publicly accessible content:

**1. Three levels of evaluation (Unit Tests → Human/Model Eval → A/B Testing).** Level 1 = assertions (fast, cheap, run on every change). Level 2 = human and LLM-judge review of traces. Level 3 = A/B with real users, only for mature products. Cost and cadence increase at each level. ([hamel.dev/blog/posts/evals/](https://hamel.dev/blog/posts/evals/), published 2024-03-29)[^12][^1]

**2. Error analysis via open coding → axial coding.** The canonical process adapted from qualitative research: (a) open code 30–50 traces (expert notes any issues, focusing on first upstream failure); (b) axial code by grouping similar notes into a failure taxonomy; (c) iterate to theoretical saturation (~20 traces without a new category = stop, but review at least 100 total). An LLM can assist with axial coding only after the human has done the initial open coding.[^2]

**3. The benevolent dictator pattern.** For most small/medium teams, appoint one domain expert as the definitive quality arbiter. This person makes the final pass/fail call, eliminates annotation conflict, and can incorporate input but drives the process. Multiple annotators are only required for multinational/multi-domain deployments. Inter-annotator agreement (Cohen's Kappa) must be measured when you have multiple annotators.[^2]

**4. The LLM-as-judge alignment loop.** Seven-step process: (1) identify domain expert; (2) create trace dataset; (3) expert makes pass/fail judgments with critiques; (4) fix data errors; (5) build judge iteratively; (6) perform error analysis on judge failures; (7) create specialized sub-judges if needed. Measure alignment using TPR and TNR on a held-out labeled set, not raw agreement (which is unreliable when classes are imbalanced).[^2]

**5. Binary pass/fail is the right default.** Likert scales create annotator inconsistency and require larger sample sizes to detect statistical differences. Binary forces clarity. For gradual progress tracking, decompose into multiple binary sub-checks rather than using a scale.[^2]

**6. Custom annotation tools outperform off-the-shelf platforms for most teams.** Build a domain-specific viewer in hours using Gradio, Streamlit, or an AI coding assistant. The key feature: all context (trace + CRM result + email sent + database update) on one screen. Generic tools can't render domain-specific outcomes.  (_Exception: teams with 50+ distributed annotators needing enterprise access control._)[^2]

**7. Never use generic similarity metrics (BERTScore, ROUGE, cosine) as quality signals.** These are useful only for retrieval evaluation (semantic closeness) and diversity measurement, not for judging whether the output achieves the business goal.[^2]

**8. Spend 60–80% of development time on error analysis and evaluation, not on features.** This is the stated calibration from Husain across multiple contexts. If you're passing 100% of your evals, you're not challenging the system enough; a 70% pass rate might indicate a meaningful evaluation.[^2]

**9. Synthetic data generation via structured dimensions → tuples → queries.** Define dimensions (e.g., topic type × user mood × query complexity), create tuples manually first (20 by hand), then scale with two-step generation: LLM generates tuples, then a separate prompt converts tuples to natural language queries. Cross-product then filter is more thorough; direct LLM generation is faster but misses rare scenarios.[^2]

**10. Evals should reflect business outcomes, not technical metrics.** "Has an appointment been made?" is a better eval than "Did the tool call succeed?" The domain expert should evaluate actual outcomes visible on screen, not intermediate system states.[^2]

***

## 3. Anthropic's First-Party Eval Approach

**The system-card pattern.** Anthropic publishes a system card for every major model release. The current list (including Claude Opus 4.1, Sonnet 4, Sonnet 3.7) is at [anthropic.com/system-cards](https://www.anthropic.com/system-cards) (accessed 2026-05-09). Each card documents: (1) safety evaluation results against Anthropic's Responsible Scaling Policy (RSP) domains — CBRN, cyber, autonomy; (2) alignment assessment; (3) model welfare findings. For the Claude Opus 4 / Sonnet 4 card (May 2025, updated July 2025), the full PDF is at [anthropic.com/claude-4-system-card](https://www.anthropic.com/claude-4-system-card).[^13][^4]

**The multi-stage independent review structure.** Anthropic's standard ASL determination process involves: (1) Frontier Red Team (FRT) evaluates the model and writes a capabilities report; (2) Alignment Stress Testing (AST) team independently reviews and critiques the FRT report; (3) both reports go to the Responsible Scaling Officer, CEO, Board, and Long-Term Benefit Trust.  External experts — Apollo Research (alignment), SecureBio / Deloitte (biosecurity), Carnegie Mellon (cyber), UK and US AI Safety Institutes (CBRN/autonomy) — provide independent third-party assessments.  This is not literally "two domain experts independently agree" as a single quoted standard, but the structure always requires _at least_ internal-team independence (FRT + AST) plus external expert validation before a deployment decision.[^4]

**What recurs across Anthropic's public eval work:** (a) automated evaluations are treated as insufficient alone — human expert review (red-teaming, uplift trials, multi-turn conversations) is always required for high-stakes capability thresholds; (b) evals are run on multiple training snapshots iteratively, not just the final model; (c) helpful-only snapshots (safety training removed) are evaluated to understand the "capability ceiling" independently of safety training; (d) Anthropic has publicly acknowledged that short-horizon evals gave misleading assurance for long-running agentic tasks (Mythos Preview system card, April 2026); (e) evaluation criteria can drift as capabilities improve, requiring frequent re-baselining.[^6]

**The 60-second interview answer:** "Anthropic structures evals around their Responsible Scaling Policy — automated benchmarks and expert red-teaming across CBRN, cyber, and autonomy domains, run on multiple model snapshots. Internal Frontier Red Team findings are independently reviewed by the Alignment Stress Testing team, then validated by external domain experts. Thresholds are conservative and precautionary: if they can't rule out an ASL-3 risk, they deploy at ASL-3 anyway. Short-horizon automated evals are supplemented with long-running agentic sessions because benchmark results and real deployment behavior can diverge significantly."

***

## 4. Eval Platform Landscape — Build vs. Buy

| Platform | Type | Best for | Maintainer | Link |
|---|---|---|---|---|
| **Braintrust** | SaaS (free tier: 1M spans, 10K runs/mo) | Eval-gated CI/CD workflows, prompt versioning, regression testing; "eval-driven development culture" | Braintrust Data (private) | [braintrust.dev](https://www.braintrust.dev) [^14] |
| **Langfuse** | OSS + cloud | Tracing, debugging, annotation queues; infrastructure-savvy teams who want self-hosted observability | Langfuse GmbH | [langfuse.com](https://langfuse.com) [^15] |
| **LangSmith** | SaaS (closed source) | Teams deep in the LangChain/LangGraph ecosystem; rapid prototyping with native tracing | LangChain Inc. | [smith.langchain.com](https://smith.langchain.com) [^16] |
| **Promptfoo** | OSS CLI (MIT) | Test-driven prompt engineering, CI/CD integration, red-teaming; YAML-based, runs locally; acquired by OpenAI March 2026, still MIT-licensed | OpenAI / promptfoo maintainers | [github.com/promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) [^17][^18] |
| **Inspect (UK AISI)** | OSS (Python) | Frontier capability and safety evals; multi-turn dialog, tool-use, model-graded evals; safety-institute-grade rigor | UK AI Security Institute | [github.com/UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) [^19][^20] |
| **Arize Phoenix** | OSS (Elastic License 2.0) + managed (Arize AX) | OpenTelemetry-based tracing, LLM-as-judge, self-hosted; framework-agnostic (LlamaIndex, LangChain, LiteLLM, etc.) | Arize AI | [phoenix.arize.com](https://phoenix.arize.com) [^21][^22] |
| **Latitude** | SaaS | Auto-generation of eval prompts (GEPA), issue lifecycle tracking, eval quality measurement; rising entrant 2026 | Latitude.so | [latitude.so](https://latitude.so) [^23] |

**Recommendation for the vault synthesizer (10–15 cases, Week 5):** Start with a **plain Python directory of YAML cases with a minimal pytest runner** rather than any of the above platforms. Here is why: (1) a 10–15-case eval set does not benefit from the observability, CI/CD, or collaboration features of a SaaS platform; (2) your vault synthesizer runs locally on an intermittent MBP with a SQLite backend — a cloud platform adds unnecessary round-trip complexity; (3) the deliverable's primary value is the interview talking point (you built working evals from first principles), not the platform choice. If you want a local OSS runner for the CI/CD story, **Promptfoo** is the right add — it is YAML-native, runs entirely locally, and is MIT-licensed. Braintrust is the right next step post-employment when you want eval-gated deployments and team dashboards.[^14][^17]

***

## 5. What "Intermediate Fluency" Looks Like

### Core Vocabulary

**Pass@k** — The probability that at least one of *k* independent samples is correct for a given task. Used heavily for code generation benchmarks (HumanEval, AIME). The formula is an unbiased estimator, not a simple success-rate count. **Interviewer trap:** candidates confuse pass@k with "pass on the k-th attempt." The differentiator: pass@k estimates the probability of _at least one_ correct answer in k draws; it does not mean trying k times sequentially.[^24]

**LLM-as-judge** — Using an LLM to score or pass/fail the outputs of another LLM (or the same LLM). Requires calibration against human labels (measured by TPR/TNR, not raw accuracy) before the judge can be trusted. **Interviewer trap:** candidates claim their LLM judge is "validated" just because it agrees with humans most of the time. The differentiator: imbalanced classes make raw agreement a misleading metric; measure precision and recall separately.[^2]

**Rubric vs. exact-match** — Exact-match checks a specific string/structure (cheap, deterministic). Rubric uses a set of criteria to grade free-form output (usually via LLM-as-judge, requires calibration). **Trap:** using rubric where exact-match would suffice wastes resources and introduces variability.

**Golden dataset** — A hand-curated set of traces with human labels (pass/fail + critique), used to validate automated judges and as regression anchors. **Trap:** calling any labeled dataset "golden." A golden dataset requires domain-expert review, documented pass/fail criteria, and periodic refresh.

**Regression eval vs. capability eval** — A regression eval checks that a fix doesn't break existing behavior; a capability eval establishes a new baseline ("can the model do X at all?"). **Trap:** candidates use these interchangeably. The differentiator: you run regression evals after every code change; you run capability evals when setting up a new eval suite or evaluating a new model.

**Eval (product-specific) vs. benchmark (public)** — A benchmark measures a model's general capability against a public dataset (MMLU, HumanEval, AIME). An eval is domain-specific to your product and measures whether your system achieves your business goal. **Trap:** the most common mistake: conflating a model's benchmark score with whether your specific AI product works for your users.[^2]

**Trace** — The complete record of all messages, tool calls, retrieved documents, and intermediate steps for one user session or request. The unit of analysis in error analysis; not just the final output. **Trap:** evaluating only final outputs and ignoring intermediate failures (e.g., a hallucinated retrieval step that corrupts a correct-looking final answer).

**Hallucination (grounded vs. open-domain)** — For synthesizer agents operating over a specific document corpus, hallucination means generating concepts or claims not grounded in the source notes — distinct from creative confabulation. **Trap:** treating "hallucination" as a single failure mode; for RAG/synthesis agents it always has a grounding definition.

**Criteria drift** — The phenomenon where evaluation criteria shift as you review more outputs (the model's behavior reveals requirements you hadn't articulated). Husain cites this as a core reason why automated prompt optimization can't replace error analysis.[^2]

### Key Design Decisions

**When to use LLM-as-judge vs. rubric vs. exact-match.** Use exact-match for deterministic outputs (relation tag values, concept IDs, JSON schema conformance). Use a rubric for structured criteria with multiple sub-dimensions. Use LLM-as-judge for subjective free-form quality criteria that can't be captured by a rule — but only after calibrating against 50–100 human-labeled examples. In practice, start with exact-match and rubric; add LLM-as-judge only for persistent failures that simpler checks miss.

**Golden dataset: seed from production vs. generate synthetically.** Use production data as soon as you have any — it captures actual distribution. Use synthetic data to bootstrap when you have no users yet, or to stress-test known failure modes. The Husain structured dimensions method (dimensions → tuples → queries) is the most reliable synthetic approach. For the vault synthesizer, synthetic inputs based on real note templates are appropriate.[^2]

**Eval set size.** The Husain heuristic: review at least 100 traces before declaring a failure taxonomy stable. For an automated eval suite, 10–15 well-designed cases covering your known failure modes is a legitimate starting point that can grow — as long as each case is grounded in an observed failure, not an imagined one.

**Binary vs. scored.** Start binary. If you need finer granularity (e.g., "partially hallucinated"), decompose into multiple binary sub-checks rather than introducing a scale.

**How to size a regression suite.** Include at minimum: one case per known failure mode, one case per major feature path, and at least two adversarial edge cases. For 10–15 cases covering a three-failure-mode synthesizer, 4–5 per category is appropriate.

***

## 6. Reference Eval Case Library — for a Vault-Synthesizer-Shaped Task

```yaml
# evals/vault-synthesizer-cases.yaml
# 10–15 eval cases for the Phase D vault synthesizer.
# Judge types: exact-match | rubric | llm-judge
# Category tags align to known + canon-predicted failure modes.

- id: vs-001
  category: hallucination-check
  description: "Synthesizer must not generate concept articles for phases not present in source notes."
  input:
    notes:
      - "2026-04-01.md: Started reviewing the Phase 6 knowledge loop architecture."
      - "2026-04-02.md: Phase 6 has a producer side (SessionEnd flush → synthesizer) and a consumer side (SessionStart index injection)."
  expected_output:
    concepts_must_include: ["Phase 6 knowledge loop"]
    concepts_must_exclude: ["Phase 7 knowledge loop", "Phase 6.5 knowledge loop", "Phase 5 knowledge loop"]
  judge_type: rubric
  pass_criteria: "All required concepts present; no excluded concepts present in any emitted article."
  failure_mode_under_test: "Hallucinated phase numbers (the Phase D edges work was mislabeled 'Phase 5' in an early run)."

- id: vs-002
  category: hallucination-check
  description: "Synthesizer must not invent agent names not present in source notes."
  input:
    notes:
      - "2026-04-10.md: SessionWatcher detects MBP wake event and triggers the nightly synthesizer."
      - "2026-04-11.md: Ran a manual synthesizer trigger; output landed in vault/concepts/."
  expected_output:
    concepts_must_include: ["SessionWatcher"]
    concepts_must_exclude: ["SessionMonitor", "WakeDetector", "ContextCollector"]
  judge_type: exact-match
  pass_criteria: "Emitted articles reference 'SessionWatcher' and do not reference any excluded agent aliases."
  failure_mode_under_test: "Hallucinated agent aliases — synthesizer renames entities slightly when paraphrasing source notes."

- id: vs-003
  category: hallucination-check
  description: "A concept article body must cite at least one source note filename."
  input:
    notes:
      - "2026-04-15.md: HybridRouter falls back to Sonnet 4.6 when Qwen3-14B is unavailable."
      - "2026-04-16.md: HybridRouter logs fallback events to hybrid_router.log."
  expected_output:
    every_concept_article_cites_at_least_one_source: true
  judge_type: rubric
  pass_criteria: "Each emitted concept article includes at least one in-text or footnote reference to a source note filename (e.g., '2026-04-15.md')."
  failure_mode_under_test: "Source-attribution loss — synthesizer generates plausible-sounding concept articles that cannot be traced back to any specific note."

- id: vs-004
  category: hallucination-check
  description: "Synthesizer must not emit concept articles for undocumented tool names."
  input:
    notes:
      - "2026-04-20.md: Built a Zapier zap to push Jira ticket completions to a Slack channel."
      - "2026-04-21.md: Zapier trigger confirmed working; no issues."
  expected_output:
    concepts_must_exclude: ["Make.com", "n8n", "Activepieces", "Tray.io"]
  judge_type: exact-match
  pass_criteria: "No concept article references an automation tool other than Zapier when Zapier is the only tool mentioned in source notes."
  failure_mode_under_test: "Category-level hallucination — synthesizer substitutes a similar-category tool for the one actually mentioned."

- id: vs-005
  category: hallucination-check
  description: "Synthesizer must not create a concept article for a project referenced only in passing."
  input:
    notes:
      - "2026-04-25.md: Quick note — might explore 16BitFit gamification mechanics later this quarter."
  expected_output:
    concepts_must_exclude: ["16BitFit gamification system", "16BitFit mechanics spec"]
  judge_type: rubric
  pass_criteria: "Synthesizer does not emit a full concept article for 16BitFit; may emit at most a single-sentence connection mention if relevant."
  failure_mode_under_test: "Thin-source hallucination — synthesizer expands a passing mention into a full concept article."

- id: vs-006
  category: overstated-edge-confidence
  description: "A connection article between two sparsely-documented concepts must not claim a 'strong' or 'definitive' relationship."
  input:
    notes:
      - "2026-03-05.md: Thinking about how the vault RAG pipeline might connect to the MCP server design."
  expected_output:
    connection_article_confidence_markers_must_not_include: ["definitively", "strongly connected", "directly causes", "proven relationship"]
    connection_article_must_include_hedging: true
  judge_type: llm-judge
  pass_criteria: "Connection article uses hedged language (e.g., 'may relate to', 'suggests a possible link', 'warrants further investigation') and does not claim certainty from a single note."
  failure_mode_under_test: "Overstated edge confidence — synthesizer asserts a strong directional relationship from a single exploratory note."

- id: vs-007
  category: overstated-edge-confidence
  description: "A 'supports' relation edge must require at least two corroborating source notes."
  input:
    notes:
      - "2026-03-10.md: RAG injection on SessionStart seems to be helping context continuity."
    edges_emitted:
      - subject: "RAG injection"
        relation: "supports"
        object: "context continuity"
        source_note_count: 1
  expected_output:
    edge_must_be_downgraded_to_related_to_if_single_source: true
  judge_type: rubric
  pass_criteria: "A 'supports' edge is only emitted when at least two source notes corroborate the relationship; with a single note, the relation should be 'related_to'."
  failure_mode_under_test: "Overstated edge confidence — 'supports' tag applied based on a single positive observation in one note."

- id: vs-008
  category: overstated-edge-confidence
  description: "Phase D relation edges must include a confidence score; low-evidence edges must have low confidence."
  input:
    notes:
      - "2026-03-15.md: The synthesizer output format might evolve as the Phase D schema matures."
    edges_emitted:
      - subject: "synthesizer output format"
        relation: "evolved_into"
        object: "Phase D schema"
        confidence: 0.9
  expected_output:
    confidence_must_be_below_threshold: 0.5
  judge_type: exact-match
  pass_criteria: "Edge emitted from a speculative single-note observation has confidence < 0.5."
  failure_mode_under_test: "Confidence score inflation — synthesizer assigns high confidence to edges grounded in speculative language."

- id: vs-009
  category: relation-tag-drift
  description: "When a note provides evidence that A causes or leads to B, relation tag must be 'supports', not 'related_to'."
  input:
    notes:
      - "2026-04-03.md: Turning on the Phase 6 knowledge loop directly improved session continuity in two consecutive tests."
    expected_edge:
      subject: "Phase 6 knowledge loop"
      relation: "supports"
      object: "session continuity"
  expected_output:
    relation_tag_must_equal: "supports"
    relation_tag_must_not_equal: "related_to"
  judge_type: exact-match
  pass_criteria: "Emitted relation tag is 'supports', not 'related_to', given directional causal evidence in the note."
  failure_mode_under_test: "Relation-tag drift — synthesizer defaults to 'related_to' when 'supports' is warranted because the relationship is directional."

- id: vs-010
  category: relation-tag-drift
  description: "When one note explicitly revises a prior design decision, relation tag must be 'supersedes'."
  input:
    notes:
      - "2026-04-05.md: Replaced the old flat-file concept store with the new SQLite edges table. The old approach is retired."
    expected_edge:
      subject: "SQLite edges table"
      relation: "supersedes"
      object: "flat-file concept store"
  expected_output:
    relation_tag_must_equal: "supersedes"
    relation_tag_must_not_equal: ["evolved_into", "related_to", "depends_on"]
  judge_type: exact-match
  pass_criteria: "Emitted relation tag is 'supersedes'; 'evolved_into' is acceptable only if the object is explicitly described as a predecessor, not a retired approach."
  failure_mode_under_test: "Supersedes vs. evolved_into confusion — synthesizer uses 'evolved_into' when the note clearly indicates replacement and retirement."

- id: vs-011
  category: relation-tag-drift
  description: "A 'contradicts' edge must only be emitted when two notes make incompatible claims about the same subject."
  input:
    notes:
      - "2026-02-10.md: Qwen3-14B handles long context reliably."
      - "2026-04-12.md: Qwen3-14B truncated a 4K-token note; HybridRouter fallback triggered."
    expected_edge:
      subject: "2026-02-10 Qwen3 reliability claim"
      relation: "contradicts"
      object: "2026-04-12 Qwen3 truncation observation"
  expected_output:
    relation_tag_must_equal: "contradicts"
  judge_type: rubric
  pass_criteria: "Synthesizer correctly identifies the two notes as making incompatible empirical claims about the same model behavior and emits a 'contradicts' edge."
  failure_mode_under_test: "Contradicts suppression — synthesizer avoids emitting 'contradicts' edges because the tag feels aggressive, defaulting to 'related_to'."

- id: vs-012
  category: temporal-confusion
  description: "Synthesizer must prefer the most recent note when two notes make conflicting claims about the same system state."
  input:
    notes:
      - "2026-01-15.md: Using LangChain for orchestration."
      - "2026-04-20.md: Migrated away from LangChain; now using direct Anthropic SDK calls."
  expected_output:
    active_system_description_must_reference: "direct Anthropic SDK calls"
    active_system_description_must_not_reference: ["LangChain", "LangChain orchestration"]
  judge_type: rubric
  pass_criteria: "Concept article describing current orchestration reflects the April note, not the January note; January note may appear in a 'superseded by' historical context."
  failure_mode_under_test: "Temporal confusion — synthesizer treats all notes as equally current and produces contradictory or stale concept articles."

- id: vs-013
  category: stale-content-overweighting
  description: "A concept article synthesizing from 10+ notes must not draw its primary claims disproportionately from the oldest notes."
  input:
    notes:
      - "2026-01-01.md: Initial vault architecture uses flat files."
      - "2026-01-15.md: Considering SQLite for the edge store."
      - "2026-02-01.md: SQLite chosen for Phase D edges."
      - "2026-03-01.md: Phase D schema finalized."
      - "2026-04-01.md: Phase D edges live in production."
  expected_output:
    concept_article_primary_claims_must_reflect_most_recent_state: true
  judge_type: llm-judge
  pass_criteria: "The concept article's lead paragraph and primary claims reflect the April/March state (SQLite, Phase D edges in production), not the January flat-file state. January context may appear only as historical background."
  failure_mode_under_test: "Stale-content over-weighting — synthesizer gives equal weight to all notes and produces a concept article that describes an intermediate or superseded system state as current."

- id: vs-014
  category: output-completeness
  description: "For a corpus of 5+ notes mentioning a named system, synthesizer must emit at least one concept article."
  input:
    notes:
      - "2026-04-01.md: HybridRouter initialized."
      - "2026-04-02.md: HybridRouter routing logic tested."
      - "2026-04-03.md: HybridRouter fallback to Sonnet triggered."
      - "2026-04-04.md: HybridRouter latency logged."
      - "2026-04-05.md: HybridRouter config reviewed."
  expected_output:
    concepts_must_include: ["HybridRouter"]
  judge_type: exact-match
  pass_criteria: "At least one concept article with 'HybridRouter' as the primary subject is emitted."
  failure_mode_under_test: "Silent omission — synthesizer fails to emit a concept article for a well-documented system component, leaving it invisible in the knowledge graph."

- id: vs-015
  category: output-completeness
  description: "When a synthesizer run produces 0 concept articles from a 20-note corpus, it must emit an error or explanation, not silent success."
  input:
    notes:
      - "2026-04-06.md: [20 notes describing varied project work — see test fixture notes_fixture_20.md]"
  expected_output:
    minimum_concepts_emitted: 1
    or_error_message_present: true
  judge_type: rubric
  pass_criteria: "Either at least 1 concept article is emitted, or the synthesizer output includes a diagnostic message explaining why no articles were generated. Silent empty output is a failure."
  failure_mode_under_test: "Silent empty output — synthesizer returns a null/empty result set without any error signal, masking a runtime failure as apparent success."
```

***

## 7. The Don't-Build-This-Yet List

Scope discipline is the second-most-important constraint after citation grounding. Each of the following is a real temptation for an engaged PM doing eval work — and each is post-employment Q3 work.

**1. Eval CI/CD pipelines.** Wiring evals into GitHub Actions with pass-rate gates on every commit is the right long-term posture but requires stable prompt versioning, a reproducible test harness, and a deployment workflow — none of which the vault synthesizer has yet. Build the eval cases first; the CI wrapper is an afternoon task once the cases are stable.

**2. A published eval framework or methodology doc.** Writing a general-purpose framework ("here's how to eval any synthesis agent") is a research output, not a portfolio artifact. The portfolio value comes from the working evals/ directory tied to a specific system with known failure modes.

**3. Custom eval-platform infrastructure.** Deploying Langfuse self-hosted, building Braintrust CI/CD integrations, or setting up an OpenTelemetry trace pipeline for the vault synthesizer is a week of infrastructure work. None of it is needed for 10–15 YAML eval cases run locally.

**4. Cross-model eval comparison tooling.** Building a harness that compares Qwen3-14B vs. Sonnet 4.6 eval results with statistical significance tests is the right question for a team with multiple deployed models and a stable eval baseline — not Week 5. Run the evals against one model first.

**5. Eval coverage metrics dashboards.** Building a dashboard that tracks pass-rate trends over time (eval coverage %, failure-mode frequency, regression delta) is post-employment tooling. For Week 5, a simple pytest output or a Markdown results log is sufficient.

**6. An inter-annotator agreement study.** Computing Cohen's Kappa across multiple annotators makes sense when you have multiple domain experts and ambiguous rubrics. For a solo vault synthesizer eval suite where you are the domain expert, you are the benevolent dictator — formal IAA measurement is scope creep.

***

## 8. Sources Index

### Section 1 — 2026 Canon

| Source | URL | Accessed | Authority |
|---|---|---|---|
| Hamel Husain, LLM Evals FAQ (hamel.dev) | [hamel.dev/blog/posts/evals-faq/](https://hamel.dev/blog/posts/evals-faq/) | 2026-05-09 | Primary author, 700+ student course FAQ; most comprehensive public statement of the Husain–Shankar canon. |
| Brendan Foody on Lenny's Podcast (Sept 2025) | [lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody](https://www.lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody) | 2026-05-09 | CEO of Mercor (AI-labs' primary eval supplier); source of "evals are the new PRDs" framing. |
| Anthropic, Claude Opus 4 / Sonnet 4 System Card (May 2025) | [anthropic.com/claude-4-system-card](https://www.anthropic.com/claude-4-system-card) | 2026-05-09 | Anthropic's primary public documentation of its eval methodology and ASL determination process. |
| Anthropic, System Cards index | [anthropic.com/system-cards](https://www.anthropic.com/system-cards) | 2026-05-09 | Full list of Anthropic system cards by model and date. |
| Claude Mythos Preview System Card coverage | [wavespeed.ai/blog/posts/claude-mythos-preview-system-card-findings/](https://wavespeed.ai/blog/posts/claude-mythos-preview-system-card-findings/) | 2026-05-09 | Third-party analysis of the April 2026 Mythos card; cites the short-horizon eval limitation. |
| UK AI Security Institute, inspect_ai GitHub | [github.com/UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | 2026-05-09 | Official OSS eval framework from UK AISI; primary documentation at inspect.aisi.org.uk. |
| UK AISI, Announcing Inspect Evals (Nov 2024) | [aisi.gov.uk/blog/inspect-evals](https://www.aisi.gov.uk/blog/inspect-evals) | 2026-05-09 | UK government blog post confirming AISI as maintainer and open-source date (May 2024). |

### Section 2 — Hamel–Shreya Course Canon

| Source | URL | Accessed | Authority |
|---|---|---|---|
| Maven course landing page | [maven.com/parlance-labs/evals](https://maven.com/parlance-labs/evals) | 2026-05-09 | Official course page; confirms instructors, next cohort dates, and course description. |
| Hamel Husain, "Your AI Product Needs Evals" (2024-03-29) | [hamel.dev/blog/posts/evals/](https://hamel.dev/blog/posts/evals/) | 2026-05-09 | Canonical entry-point post; case study of Lucy at Rechat; defines three levels of evaluation. |
| Hamel Husain, blog index | [hamel.dev](https://hamel.dev) | 2026-05-09 | Confirms post date of "Your AI Product Needs Evals" as 2024-03-29. |
| AI Evals FAQ PDF (Sept 2025, publicly free) | [drive.google.com/file/d/1y447t7zN1m11ObIvNNo7mVdWCjAicoyQ/view](https://drive.google.com/file/d/1y447t7zN1m11ObIvNNo7mVdWCjAicoyQ/view) | 2026-05-09 | 51-page publicly released FAQ from 1,500+ student course; free, not paywalled. |
| Simon Willison, link to Evals FAQ (July 2025) | [simonwillison.net/2025/Jul/3/faqs-about-ai-evals/](https://simonwillison.net/2025/Jul/3/faqs-about-ai-evals/) | 2026-05-09 | Confirms public release of FAQ and course history. |
| Aakash Gupta interview: Maven top-grossing (Jan 2026) | [news.aakashg.com/p/hamel-shreya-podcast-2](https://www.news.aakashg.com/p/hamel-shreya-podcast-2) | 2026-05-09 | Confirms Maven top-grossing status and training of OpenAI/Anthropic teams. |

### Section 3 — Anthropic Eval Approach

_(See Section 1 sources above; same primary sources apply.)_

### Section 4 — Eval Platforms

| Source | URL | Accessed | Authority |
|---|---|---|---|
| Braintrust product page | [braintrust.dev](https://www.braintrust.dev) | 2026-05-09 | Official product; confirms free tier (1M spans, 10K eval runs). |
| Langfuse | [langfuse.com](https://langfuse.com) | 2026-05-09 | Official OSS platform; actively maintained by Langfuse GmbH. |
| Promptfoo GitHub (canonical) | [github.com/promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 2026-05-09 | MIT-licensed CLI; acquired by OpenAI March 2026 per DataCamp tutorial. |
| Promptfoo tutorial (OpenAI acquisition confirmation) | [datacamp.com/tutorial/promptfoo-tutorial](https://www.datacamp.com/tutorial/promptfoo-tutorial) | 2026-05-09 | Confirms OpenAI acquisition March 2026 and 350K+ developer user base. |
| Arize Phoenix GitHub | [github.com/arize-ai/phoenix](https://github.com/arize-ai/phoenix) | 2026-05-09 | OSS (Elastic License 2.0); maintained by Arize AI. |
| UK AISI inspect_ai | [github.com/UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | 2026-05-09 | Official AISI framework; documented at inspect.aisi.org.uk. |
| Latitude platform comparison (May 2026) | [latitude.so/blog/best-ai-agent-evaluation-platforms-2026-comprehensive-comparison](https://latitude.so/blog/best-ai-agent-evaluation-platforms-2026-comprehensive-comparison) | 2026-05-09 | Useful 2026 platform comparison; vendor-produced, so read with that lens. |

### Section 5 — Fluency Vocabulary

| Source | URL | Accessed | Authority |
|---|---|---|---|
| pass@k definition (Lee Hanchung blog) | [leehanchung.github.io/blogs/2025/09/08/pass-at-k/](https://leehanchung.github.io/blogs/2025/09/08/pass-at-k/) | 2026-05-09 | Clear practitioner explanation of pass@k as an unbiased estimator. |
| Husain evals FAQ (binary vs. Likert) | [hamel.dev/blog/posts/evals-faq/](https://hamel.dev/blog/posts/evals-faq/) | 2026-05-09 | As above. |

### Attributed but Unverified

- **"Evals are the new PRDs" as a standalone Foody blog post or tweet.** The phrase appears in the September 2025 Lenny's Podcast transcript ([lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody](https://www.lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody)) but could not be verified as originating in a standalone Foody post. Cite as: "Foody, Sept 2025 Lenny's Podcast."
- **Anthropic "two domain experts independently agree" as a quoted standard.** This framing circulates in AI PM community summaries of Anthropic's eval methodology but does not appear verbatim in any system card reviewed. The correct citation is the FRT + AST dual-review structure in the Claude Opus 4 system card. Do not use the "two experts" shorthand in an interview without acknowledging it is a summary, not a direct Anthropic quote.

---

## References

1. [Evals – Hamel's Blog](https://hamel.dev/notes/llm/evals/) - In this lesson, Shreya Shankar and Hamel Husain walk through the process of error analysis from… You...

2. [LLM Evals: Everything You Need to Know – Hamel's Blog](https://hamel.dev/blog/posts/evals-faq/) - A comprehensive guide to LLM evals, drawn from questions asked in our popular course on AI Evals. Co...

3. [A systematic approach to improving your AI products | Hamel Husain ...](https://www.lennysnewsletter.com/p/evals-error-analysis-and-better-prompts) - Watch now | 🎙️ How to build better AI products through data-driven error analysis, evaluation framew...

4. [[PDF] System Card: Claude Opus 4 & Claude Sonnet 4 - Anthropic](https://www.anthropic.com/claude-4-system-card) - This system card introduces Claude Opus 4 and Claude Sonnet 4, two new hybrid reasoning large langua...

5. [Brendan Foody (CEO of Mercor) - Lenny's Newsletter](https://www.lennysnewsletter.com/p/experts-writing-ai-evals-brendan-foody) - Listen now | Mercor's founder on growing from $1M to $500M in 17 months, why evals are the biggest b...

6. [What Is Inside Claude Mythos Preview? Dissecting the System Card ...](https://kenhuangus.substack.com/p/what-is-inside-claude-mythos-preview) - One of the most honest parts of this system card is where Anthropic documents failure modes in its o...

7. [AI Evals For Engineers & PMs by Hamel Husain and ... - Maven](https://maven.com/parlance-labs/evals) - If you're an engineer or PM building any AI product and struggling to know whether your system is ac...

8. [Why AI evals are the hottest new skill for product builders - YouTube](https://www.youtube.com/watch?v=BsWxPI9UM4c) - Hamel Husain and Shreya Shankar teach the world's most popular course on AI evals and have trained o...

9. [AI Evals | Maven | Unlock your career growth](https://maven.com/courses/for-product-managers/evals) - Cohort-based courses. Guided programs to get real results. AI Evals For ... Hamel Husain ML Engineer...

10. [AI Evals Masterclass with Hamel & Shreya - by Aakash Gupta](https://www.news.aakashg.com/p/hamel-shreya-podcast-2) - Their Maven course is the top-grossing course on the platform. Today, they're walking you through th...

11. [I got permission to publish a new AI Evals FAQ (Sep, 2025). It's ...](https://x.com/sh_reya/status/1968104766132908089) - @HamelHusain and @sh_reya run the world's No. 1 AI Evals course. Together with top AI architects and...

12. [Hamel Husain's Blog – Hamel's Blog - Hamel Husain](https://hamel.dev) - Notes on applied AI engineering, machine learning, and data science.

13. [Model system cards - Anthropic](https://www.anthropic.com/system-cards) - Model System Cards. System cards document the capabilities, safety evaluations, and responsible depl...

14. [5 best AI evaluation tools for AI systems in production (2026) - Articles](https://www.braintrust.dev/articles/best-ai-evaluation-tools-2026) - Braintrust is the best AI evaluation tool for most teams because it connects production traces, toke...

15. [Comparing LLM Evaluation Platforms: Top Frameworks for 2025](https://arize.com/llm-evaluation-platforms-top-frameworks/) - Here, we zero in on five platforms teams ask about most often and that lead in adoption and market s...

16. [Top LLM Evaluation Platforms: In Depth Comparison : r/AI_Agents](https://www.reddit.com/r/AI_Agents/comments/1pa02zc/top_llm_evaluation_platforms_in_depth_comparison/) - Top LLM evaluation platforms comparison. Arize Phoenix vs Langfuse comparison. Open source LLM obser...

17. [Promptfoo Tutorial: A Hands-On Guide to LLM Evaluation](https://www.datacamp.com/tutorial/promptfoo-tutorial) - Build reliable AI apps faster by turning ad-hoc prompt checks into structured LLM evaluations with P...

18. [Promptfoo Tutorial 2026: LLM Evaluations and Testing ... - Noqta](https://noqta.tn/en/tutorials/promptfoo-llm-evals-testing-ai-apps-2026) - Stop shipping LLM apps blind. Learn how to use Promptfoo to evaluate prompts, compare models, run re...

19. [UKGovernmentBEIS/inspect_ai: Inspect: A framework for ... - GitHub](https://github.com/UKGovernmentBEIS/inspect_ai) - A framework for large language model evaluations created by the UK AI Security Institute. Inspect pr...

20. [Announcing Inspect Evals | AISI Work - AI Security Institute](https://www.aisi.gov.uk/blog/inspect-evals) - Inspect Evals are built on top of Inspect AI, an open-source evaluation framework created by the UK ...

21. [Home - Phoenix - Arize AI](https://phoenix.arize.com) - Arize Phoenix is an open-source LLM tracing & evaluation platform. Seamlessly instrument, experiment...

22. [Arize-ai/phoenix: AI Observability & Evaluation - GitHub](https://github.com/arize-ai/phoenix) - Phoenix is an open-source AI observability platform designed for experimentation, evaluation, and tr...

23. [Best AI Agent Evaluation Platforms in 2026 - Latitude.so](https://latitude.so/blog/best-ai-agent-evaluation-platforms-2026-comprehensive-comparison) - Braintrust's free tier (1M spans/month, 10K eval runs) is the best starting point for eval-driven de...

24. [Statistics for AI/ML, Part 4: pass@k and Unbiased Estimator](https://leehanchung.github.io/blogs/2025/09/08/pass-at-k/) - The pass@ k metric is a fundamental evaluation tool in LLM benchmarks, but its meaning is often misu...

