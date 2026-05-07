---
type: research-prompt
project: prj-job-hunt-2026
target_model: gemini-deep-research
estimated_cost: ~$2
created: 2026-05-07
fire_target_date: 2026-05-29  # End of Week 4, before Week 5 deep-work focus
expected_output: vault/20_projects/research/2026-05-29-eval-design-canon-2026.md
roadmap_link: Task 6 §I (Week 5 eval fluency deep-work)
ai-context: "DR (not Max) prompt for the Week 5 eval-fluency deep-work focus. Engineered using the prompt-engineering skill — clarity + role + XML structure + scope discipline + multishot eval-case format + validation. Target output: fluency primer + 10-15 reference eval cases for the vault synthesizer."
---

# Gemini DR Prompt — Eval Design Canon 2026

> Copy everything below the `--- PROMPT START ---` line into Gemini Deep Research (standard tier — NOT Max; this topic is single-shape, not compound) or pipe via `agents-sdk/scripts/gemini_dr.py --tier dr`. Output report saves to `vault/20_projects/research/2026-05-29-eval-design-canon-2026.md`.

> **Fire timing:** End of Week 4 (target ~2026-05-29) so Week 5's eval-fluency deep-work block has grounded context to work from. Roadmap Task 6 §I.

--- PROMPT START ---

<role>
You are a senior AI PM with hands-on eval-engineering experience. You have shipped production eval suites at one or more frontier AI shops, and you have also been on the interviewer side — you know which eval-design questions reliably separate "good candidate" from "interview-stage candidate" in 2026 AI PM loops. You speak with the precision of someone who has both authored evals and judged candidates on their eval reasoning.

Your job is to produce a focused fluency primer for a 33-year-old PM (2 years experience, currently in AI-native PM job-hunt mode) who needs to (a) be conversational about eval design in interviews next month, and (b) ship a small working `evals/` directory (10-15 cases) for an existing vault-synthesizer agent. The PM does NOT need to publish an eval framework, build eval CI/CD, or produce novel eval research. Treat scope discipline as the second-most-important constraint after citation grounding.
</role>

<context>
**The PM's existing system under test:** The vault synthesizer is a nightly agent that reads ~500 daily-note + project markdown files, emits ~10-30 concept articles and ~5-15 connection articles, and (Phase D) emits typed reasoning edges (`supports` / `contradicts` / `supersedes` / `evolved_into` / `depends_on` / `related_to`) into a SQLite table. Backed by Qwen3-14B locally (intermittent — runs only when MBP is awake) with HybridRouter fallback to Sonnet 4.6. The known failure modes already surfaced in production: (1) hallucinated concepts not grounded in source notes, (2) connection articles that overstate edge confidence, (3) relation tagging drift (e.g., labeling `related_to` when `supports` would be correct).

**The PM's portfolio shape:** Already has a 14-agent SDK fleet, an MCP server in build, vault-RAG infrastructure. Beginner-to-intermediate Python coder. Strong agent-orchestration intuition. Limited prior eval-engineering experience.

**The Week 5 deliverable:** A small `evals/` directory in the Superuser Pack repo with 10-15 cases for the vault synthesizer. Goal is fluency and a working artifact, NOT a published framework. Time budget: ~6-8 hours of deep work over Week 5.

**Why this matters for the job hunt:** Brendan Foody's "evals are the new PRDs" framing has propagated into Glean AI Quality, Scale GenAI Platform, Anthropic FDE, and Sierra/Decagon agent PM roles. Eval fluency is now table-stakes for AI PM interviews — and the PM currently rates this as a working-but-shallow skill area. The fluency upgrade and the working `evals/` artifact are the same intervention.
</context>

<task>
Produce an 8-section fluency primer covering the items in <output_format>. Multi-source triangulation: prefer claims that appear in two or more independent primary sources. Where the canon disagrees (Hamel-Shreya vs. Anthropic system-card vs. UK AISI Inspect framework), surface the disagreement explicitly and recommend the most defensible default for an AI PM interview answer.

Within each section, calibrate to "intermediate fluency" — enough depth to defend a position in a 30-minute interview, NOT enough to publish a research paper. If a section starts to drift into ML-research territory, cut it back.
</task>

<anti_hallucination_guards>
Standard discipline. The eval canon is well-documented and less likely to trigger entity fabrication than the MCP topic, but verify before citing:

1. Hamel Husain and Shreya Shankar are real practitioners with public-canon writing and a publicly-run course. Verify the course name, current cohort dates, and the 3-5 most-cited Hamel posts (URLs + dates).
2. Anthropic's eval methodology is documented in (a) public model cards, (b) the Model Spec evals project, (c) the Anthropic engineering blog. Cite specific posts/cards with URLs, not generic "Anthropic's approach."
3. The Inspect framework is real (UK AI Safety Institute / AISI). Verify current repo URL and primary maintainer affiliation.
4. Eval platforms (Braintrust, Langfuse, Langsmith, Promptfoo, Phoenix, etc.) — for each you name, link to the current repo or product page and verify it's still actively maintained as of research date.
5. Brendan Foody's "evals are the new PRDs" quote — verify the source (his post / podcast / talk) and link directly. If you cannot find the primary source, mark as "Attributed but unverified."
6. If you cite course content that is paywalled, say so explicitly — do not paraphrase paywalled material as if it were public.
</anti_hallucination_guards>

<citation_format>
GOOD:
> Hamel Husain's "Your AI Product Needs Evals" post is the canonical entry point, advocating <X> ([hamel.dev/blog/posts/evals/](https://hamel.dev/blog/posts/evals/), accessed 2026-05-29). Husain and Shankar have run the cohort-based course since <date>, with cohort enrollment publicly listed at <URL>.

ANTI-PATTERN (do not produce):
> The community canon argues that evals matter and that you should write them early.

The first contains a verifiable author + post + URL + accessed-on date. The second is unattributed folk wisdom and is forbidden.
</citation_format>

<eval_case_format>
For Section 6 (reference eval case library), use this exact shape per case. The shape is enforced because the output of this section will be consumed verbatim by Claude Code as the template for the actual `evals/` directory.

```yaml
- id: vs-001
  category: hallucination-check
  description: "Synthesizer must not invent concepts not present in source notes."
  input:
    notes:
      - "2026-04-01.md: Started reviewing the Phase 6 knowledge loop architecture."
      - "2026-04-02.md: Phase 6 has a producer side (SessionEnd flush → synthesizer) and a consumer side (SessionStart index injection)."
  expected_output:
    concepts_must_include: ["Phase 6 knowledge loop"]
    concepts_must_exclude: ["Phase 7 knowledge loop", "Phase 6.5 knowledge loop"]
  judge_type: rubric  # one of: exact-match | rubric | llm-judge
  pass_criteria: "All required concepts present; no excluded concepts present."
  failure_mode_under_test: "Hallucinated phase numbers (the Phase D edges work was once mislabeled 'Phase 5' by an early synthesizer run)."
```

Provide 10-15 cases covering the three known failure modes from <context> (hallucinated concepts, overstated edge confidence, relation-tag drift) plus 4-6 cases for failure modes the canon would predict for this kind of agent that the PM hasn't surfaced yet.
</eval_case_format>

<output_format>
Markdown document with this exact frontmatter:

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: eval-design-canon-2026
created: <RESEARCH_DATE>
model: gemini-deep-research
ai-context: "Fluency primer + reference eval cases for the Week 5 vault-synthesizer evals build. All claims cited; intermediate fluency calibrated."
---
```

# Eval Design Canon 2026 — Fluency Primer + Reference Cases for the Vault Synthesizer

## 1. The 2026 Canon — What the Field Agrees On
The 5-7 claims that have triangulated across Hamel-Shreya, Anthropic system cards, UK AISI Inspect, and the Brendan Foody / Sierra / Decagon practitioner stream. For each: who says it, the canonical post/card URL, the one-sentence version a candidate should be able to deliver in an interview. End with Confidence: HIGH/MEDIUM/LOW.

## 2. The Hamel-Shreya Course Canon
The 3,000-student cohort course's publicly-visible content. Top 5-10 concepts from the course (course landing page, public posts, podcast appearances). For each: the concept, the canonical link, the one-paragraph version. Cap at 10 concepts — this is fluency, not exhaustive coverage.

## 3. Anthropic's First-Party Eval Approach
- The system-card pattern (link the most recent Claude system card)
- The Model Spec evals project (link)
- The "two domain experts independently agree" North Star (link the source)
- What recurs across Anthropic's public eval work that a candidate should mirror

End with one sentence: "If asked 'how does Anthropic do evals' in an interview, the 60-second answer is _____."

## 4. Eval Platform Landscape — Build vs. Buy
Brief profiles (3-5 sentences each) of the 5-7 platforms a 2026 AI PM is expected to recognize: Braintrust, Langfuse, Langsmith, Promptfoo, Inspect, Phoenix, plus any rising entrant. For each: what it's good at, OSS vs. SaaS, current maintainer, link.

End with a concrete recommendation for the PM's situation: which platform (if any) to use for a 10-15-case `evals/` directory targeting a vault synthesizer, vs. just rolling a Python directory of YAML cases. Defend the recommendation in 3-4 sentences.

## 5. What "Intermediate Fluency" Looks Like
The 7-10 vocabulary terms a candidate should be able to use without hesitation: pass@k, LLM-as-judge, rubric vs. exact-match, golden dataset, regression vs. capability evals, etc. For each: the one-line definition + the trap interviewers set around it (e.g., "candidates often confuse 'eval' with 'benchmark'; the differentiator is _____").

Then the 5-7 design decisions a candidate should be able to defend: when to use LLM-as-judge vs. rubric, when to seed a golden dataset vs. generate one synthetically, how to size an eval set, etc.

## 6. Reference Eval Case Library — for a Vault-Synthesizer-Shaped Task
10-15 cases in the exact YAML shape from <eval_case_format>. Cover:
- 4-5 cases for **hallucinated concepts** (the most-known failure mode)
- 3-4 cases for **overstated edge confidence** (Phase D relation tagging)
- 2-3 cases for **relation-tag drift** (`related_to` vs. `supports` confusion)
- 4-6 cases for **canon-predicted failure modes** the PM hasn't surfaced yet (e.g., source-attribution loss, temporal-confusion, stale-content over-weighting)

Each case must include `failure_mode_under_test` so Claude Code can map it back to a defensible interview talking point.

## 7. The Don't-Build-This-Yet List
Scope discipline. Name 4-6 things that are TEMPTING for an enthusiastic PM to build but are out of scope for "Week 5 fluency + a working `evals/` directory":
- Eval CI/CD pipelines
- A published eval framework
- Custom eval-platform infrastructure
- Eval coverage metrics dashboards
- Cross-model eval comparison tooling
- Etc.

For each, a one-sentence "why this is post-employment Q3 work, not Week 5 work."

## 8. Sources Index
Every primary source cited above, organized by section. Include URL, accessed-on date, and a one-line summary of why this source is authoritative. Group "attributed but unverified" sources at the bottom.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Open every cited URL. Replace dead links or remove the claim.
2. **Course content**: For the Hamel-Shreya course, verify which content is publicly accessible vs. paywalled. Mark the line.
3. **Eval case shape**: Re-read Section 6. Every case must follow the YAML shape exactly. If any case is missing `failure_mode_under_test` or `pass_criteria`, fix it.
4. **Scope discipline**: Re-read Section 7. If anything in Sections 1-6 contradicts Section 7's "don't build this yet" list, surface the contradiction explicitly.
5. **Fluency calibration**: Re-read Section 5. If any vocabulary term requires more than one paragraph to define, you've drifted into ML-research depth — cut back.
6. **Word count**: Target 2,500-4,000 words. Below 2,500 means under-researched; above 4,000 means scope creep.
</validation>

--- PROMPT END ---
