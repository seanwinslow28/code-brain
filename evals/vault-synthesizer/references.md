# References

## Methodology

- Anthropic — *Demystifying Agent Evals.* The 8-step playbook + 3-grader-type framework.
  Local copy: `vault/40_knowledge/references/ref-anthropic-demystifying-agent-evals.md`.
- Hamel Husain — *Field guide to LLM evals.* "Error analysis is the #1 thing nobody does."
- Shreya Shankar — *Operationalizing ML/AI eval pipelines.* Binary pass/fail > Likert.
- Nate B Jones — OB1 (Open Brain 1) project. 4Q artifact template + typed-reasoning-edges schema.

## Pre-drafted cases (sources for retained cases vs-012..vs-015 and deferred vs-001..vs-011)

- `vault/20_projects/research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md` (vs-001 → vs-015)
- `vault/20_projects/research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md` (vs-001 → vs-013)

## Error-analysis evidence (sources for new cases vs-016..vs-021)

- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-10-evals-error-analysis-real-logs.md`
- 9 manifests in `vault/health/synth-manifest-2026-05-*.json`
- 3 daily logs in `vault/90_system/agent-logs/vault-synthesizer-2026-05-*.log`
- `vault/90_system/agent-logs/vault-synthesizer-stderr.log`

## Interview-vocabulary cheat-sheet

| Interviewer phrase | What it maps to in this suite |
|---|---|
| "How do you evaluate quality?" | The 6-mode taxonomy in `failure-modes.md` is the answer template. |
| "How do you avoid LLM-as-judge cost?" | 8/10 graders here are deterministic; LLM-judge is reserved and unused at v1. |
| "What about reproducibility?" | Binary pass/fail + Python-eval'd `pass_criteria` + deterministic mocks. |
| "How did you choose cases?" | Open-coded 17 days of real logs first; pre-drafted hallucination cases deferred until production is alive. |
