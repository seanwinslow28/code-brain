# Lane manifest — Ops & Economics

Mandatory first read for the [Ops & Economics Modeler](../bench/ops-economics-modeler.md). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (degradation ladder otherwise). Follow only the pointers relevant to the task.

## Cost and unit economics

- **Cost & latency optimization** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — both vendors' caching mechanics, pricing levers, and latency playbooks.
- **Caching: Latency and Cost** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — when caching pays off and where it misleads.
- **Strategy: Low-Cost Cognition Trend** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — modeling against falling model-cost curves.
- **Working with Models** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — the operational cost of model choice, pinning, and migration.
- **Fine-Tuning: When and How** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — the cost side of the adaptation ladder.

## Production monitoring and drift

- **Streaming Evaluation Is Broken** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — why windowed production metrics mislead.
- **ML Monitoring Failure Taxonomy** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — classifying a production failure before responding to it.
- **Metrics and monitoring stack for AI products** — [`lennys-aakash-ai-pm.md`](../corpus/canon/lennys-aakash-ai-pm.md) — layering system, quality, and business monitoring.
- **Guardrails vs Evaluators; CI vs Production** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — wiring the CI-to-production feedback loop.
- **Data Discipline (Operational)** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — production data hygiene and drift detection habits.
- **Data Flywheels for LLM Applications** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — the evaluate→monitor→improve loop as an operating system.

## Incidents and graceful failure

- **Errors + Graceful Failure** — [`google-pair.md`](../corpus/canon/google-pair.md) — error taxonomy and recovery paths the runbook must honor.
- **GenAI (v3): Pitfalls, Second-Order Effects, Harms Taxonomy** — [`google-pair.md`](../corpus/canon/google-pair.md) — post-launch monitoring cadence and second-order effects.

## Running the operation

- **Making the Organizational Case** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — selling ongoing eval and ops investment internally.
- **Tooling, Prompts, and Infrastructure** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — vendor choices and where operational assets live.
- **Human Annotation: The Benevolent Dictator** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — the labor economics of labeling.
- **Team, Roles, and Process** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — staffing an AI product operation.
- **Why AI Projects Fail: The Missing Process** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — the continuous-improvement process a launch must fund.

## Book layer

- **Huyen, *AI Engineering* — ch. 7, 8, 9, 10** — [`books/huyen-ai-engineering/`](../corpus/books/huyen-ai-engineering/) — inference cost and latency, fine-tuning memory math, data-budget economics, observability.
- **Huyen, *Designing Machine Learning Systems* — ch. 7, 8, 9, 10** — [`books/huyen-designing-machine-learning-systems/`](../corpus/books/huyen-designing-machine-learning-systems/) — monitoring, drift, retraining cadence and freshness economics, infrastructure cost.
- **Alammar & Grootendorst, *Hands-On Large Language Models* — ch. 1, 3, 10–12** — [`books/alammar-hands-on-large-language-models/`](../corpus/books/alammar-hands-on-large-language-models/) — hardware constraints, latency economics, training-cost regimes.
- **Berryman & Ziegler, *Prompt Engineering for LLMs* — ch. 7** — [`books/berryman-prompt-engineering-for-llms/`](../corpus/books/berryman-prompt-engineering-for-llms/) — model choice criteria and token/cost/latency budgeting.
- **Nika, *Building AI-Powered Products* — ch. 2, 5, 6, 7** — [`books/nika-building-ai-powered-products/`](../corpus/books/nika-building-ai-powered-products/) — ROI and monetization, build/buy cost structure, financial metrics, tooling economics.
