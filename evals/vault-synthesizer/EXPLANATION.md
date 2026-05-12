---
artifact: vault-synthesizer-evals
created: 2026-05-12
ai-context: "Comprehension artifact for the vault-synthesizer eval suite. 4-question template per Nate B Jones / ADR convention."
---

# Vault Synthesizer Eval Suite — Explanation

## What is this?
A 10-case binary pass/fail eval suite for a local Qwen3-14B vault synthesizer
agent. Cases were derived from open-coding 17 days of production logs
(2026-04-24 → 2026-05-10), not from imagined failure modes. The suite catches
the failure class that production monitoring missed: silent regressions where
the agent reports success while producing zero output.

## Why this approach?
Pytest + YAML over Braintrust / Langfuse — at 10 cases, platform infra is
overhead. Code-based and rubric graders before LLM-as-judge (Hamel's cost-
economics rule). Binary pass/fail over Likert (Husain-Shankar canon — Likert
destroys inter-rater reliability). The case library is grounded in real-log
error analysis (Hamel's #1 principle), not synthetic generation.

## What would break?
(1) Synthesizer prompt drift — re-baseline required if the underlying
synthesis prompt changes structurally. (2) Mock-input fixtures going stale
as the vault evolves — quarterly refresh. (3) No active case uses LLM-judge
at v1; if vs-021 is ever promoted to LLM-judge, the model ID must be pinned
explicitly in the case YAML and a `--skip-llm-judge` flag added for offline runs.

## What did I learn?
That evals aren't really about hallucinations. The failure modes I imagined —
hallucinated phase numbers, relation-tag drift, temporal confusion — were the
easy cases. The hard case was the one nobody drafts on purpose: the
status field that says "ok" while the output is empty. Three layers of
monitoring agreed everything was fine while the system underneath them rotted
silently for nine days. Error analysis surfaces the failures imagination does
not.
