# Lane manifest — Evals & Evidence

Mandatory first read for the [Evals & Evidence Architect](../bench/evals-evidence-architect.md). The hamel.dev distillate is this lane's interim spine until the Shankar/Husain book lands (~Oct 2026, watch-ticket standing). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (degradation ladder otherwise). Follow only the pointers relevant to the task.

## The lifecycle (start here)

- **Why Evals: The Iteration Flywheel** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — making the case that eval infrastructure is the bottleneck.
- **Error Analysis: Open and Axial Coding** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — the core method: discover which failures matter before writing any eval.
- **The Three Levels of Evaluation** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — deciding what kind of testing to build first and how often each runs.
- **Product Evals in Three Steps** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — standing up an eval program from zero.
- **The Three Gulfs and the Analyze–Measure–Improve lifecycle** — [`lennys-aakash-ai-pm.md`](../corpus/canon/lennys-aakash-ai-pm.md) — the PM-facing framing of the same loop.

## Datasets and annotation

- **Synthetic Data That Actually Works** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — bootstrapping test data pre-launch, and where synthetic misleads.
- **Human Annotation: The Benevolent Dictator** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — staffing and organizing labeling.
- **Data Collection + Evaluation** — [`google-pair.md`](../corpus/canon/google-pair.md) — dataset specs, labeler design, train/test hygiene, fairness checks.
- **Real-World Retrieval vs. Needle-in-a-Haystack** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — why synthetic benchmarks rank systems differently from real documents.
- **Data Discipline (Operational)** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — dev–prod skew and production data hygiene.

## Metrics and judges

- **Binary Pass/Fail Beats Likert Scales** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — designing any rubric or dashboard.
- **Evals: Measurement Foundations** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — choosing metric families and distrusting public benchmarks.
- **Task-Specific Evals That Work and Don't** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — picking the eval for a concrete task type.
- **Critique Shadowing: Building an LLM Judge** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — the step-by-step judge build.
- **LLM-Evaluators (LLM-as-Judge)** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — judge biases and panel designs, quantified.
- **Who Validates the Validators (EvalGen and Criteria Drift)** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — the research grounding for judge validation and criteria drift.
- **Evals & evaluation methodology** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — the vendors' own grader and failure-taxonomy guidance.

## Hygiene and hazards

- **Judge Validation, Holdouts, and Measurement Hygiene** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — before trusting any judge number.
- **Evals and Monitoring** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — eval harness patterns and metric-gaming warnings.
- **Evaluation Design Rules of Thumb** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — quick-reference judgment calls.
- **Evaluating RAG, Agents, and Multi-Turn Systems** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — when the system under eval is compound.
- **Course Map (AI Evals for Engineers & PMs)** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — sequencing the lane's own curriculum against the source course.

## Book layer

The Shankar/Husain evals book is still unpublished (~Oct 2026, watch-ticket standing); until it lands, the hamel.dev spine above plus the chapters below carry the lane.

- **Huyen, *AI Engineering* — ch. 3, 4** — [`books/huyen-ai-engineering/`](../corpus/books/huyen-ai-engineering/) — the book's strongest pair: judge discipline, eval-pipeline design and sizing, contamination.
- **Huyen, *Designing Machine Learning Systems* — ch. 4, 5, 6, 9** — [`books/huyen-designing-machine-learning-systems/`](../corpus/books/huyen-designing-machine-learning-systems/) — training-data quality, leakage prevention, baselines and slice evaluation, the test-in-production ladder.
- **Alammar & Grootendorst, *Hands-On Large Language Models* — ch. 4, 8, 12** — [`books/alammar-hands-on-large-language-models/`](../corpus/books/alammar-hands-on-large-language-models/) — classification metrics, retrieval and RAG evaluation, the generative eval stack.
- **Berryman & Ziegler, *Prompt Engineering for LLMs* — ch. 7, 10** — [`books/berryman-prompt-engineering-for-llms/`](../corpus/books/berryman-prompt-engineering-for-llms/) — logprob quality gates and the eval-first doctrine.
- **Nika, *Building AI-Powered Products* — ch. 2, 6** — [`books/nika-building-ai-powered-products/`](../corpus/books/nika-building-ai-powered-products/) — Go/No-Go gates and the product/system/AI metric blend.
