# Lane manifest — Design Strategy

Mandatory first read for the [Design Strategist](../bench/design-strategist.md). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (degradation ladder otherwise). Follow only the pointers relevant to the task. Book-layer pointers land with Book ingestion.

## Framing and problem selection

- **User Needs + Defining Success** — [`google-pair.md`](../corpus/canon/google-pair.md) — deciding whether AI belongs in a feature at all, automate-vs-augment, and tying metrics to actions.
- **The Seven-Pattern Map** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — orienting a new LLM system design and naming which pattern class the problem belongs to.
- **Agent design patterns** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — choosing between workflow shapes and whether to build an agent at all.
- **In Defense of AI Evals** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — calibrating how much eval rigor a given product actually needs at framing time.

## Strategy and sequencing

- **Strategy: No GPUs Before PMF** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — facing a train/fine-tune/API decision.
- **Strategy: Durable Moats and Iteration** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — deciding what to build vs buy vs wait on.
- **Strategy: The Getting-Started Playbook** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — kicking off a new LLM product in the right order.
- **Strategy: Low-Cost Cognition Trend** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — roadmapping against falling model-cost curves.
- **Demos to Products (Closing Argument)** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — setting stakeholder expectations about the demo-to-product gulf.
- **The ten chapters** — [`aie-book-repo.md`](../corpus/canon/aie-book-repo.md) — the book's argument arc and its ordering of evals vs adaptation.

## Pre-mortems and harm checks

- **GenAI (v3): Pitfalls, Second-Order Effects, Harms Taxonomy** — [`google-pair.md`](../corpus/canon/google-pair.md) — running a pre-mortem or scoping the PRD's harm check.
- **Why AI Projects Fail: The Missing Process** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — diagnosing or pitching an AI project before committing to it.
- **The Five Principles (v3)** — [`google-pair.md`](../corpus/canon/google-pair.md) — quick top-of-doc framing for any design review.

## The AI-PM role and process

- **Why evals are the new core PM skill** — [`lennys-aakash-ai-pm.md`](../corpus/canon/lennys-aakash-ai-pm.md) — arguing who owns quality measurement and why the PRD carries evaluable criteria.
- **The Three Gulfs and the Analyze–Measure–Improve lifecycle** — [`lennys-aakash-ai-pm.md`](../corpus/canon/lennys-aakash-ai-pm.md) — diagnosing why an LLM product is failing before prescribing.
- **The AI-native PM operating model** — [`lennys-aakash-ai-pm.md`](../corpus/canon/lennys-aakash-ai-pm.md) — shaping team and process for AI-native building.
- **Team, Roles, and Process** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — staffing and sequencing roles on an AI product team.
- **Process Over Tools: Eval-Driven Development** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — when someone proposes a tool as the fix for a process gap.
