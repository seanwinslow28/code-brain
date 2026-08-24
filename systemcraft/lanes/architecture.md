# Lane manifest — Architecture

Mandatory first read for the [Architecture Advisor](../bench/architecture-advisor.md). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (degradation ladder otherwise). Follow only the pointers relevant to the task. Book-layer pointers land with Book ingestion.

## System shape: prompts, flows, agents

- **Agent design patterns** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — single vs multi-agent, workflow patterns, and their cost profiles.
- **Workflow and Flow Engineering** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — deciding between one big prompt, a flow, or an agent.
- **Context engineering** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — any design touching context budgets, compaction, memory, or long-horizon agents.
- **Tool use & tool design** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — designing or reviewing an agent's tool surface.

## RAG vs fine-tune vs prompt

- **RAG and Retrieval** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — designing or auditing a retrieval system, and the RAG-vs-fine-tune call.
- **RAG: Retrieval-Augmented Generation** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — hybrid search, embedding choices, and measuring retrieval upstream.
- **RAG & retrieval** — [`openai-anthropic-docs.md`](../corpus/canon/openai-anthropic-docs.md) — vendor-documented retrieval architectures and their measured trade-offs.
- **Fine-Tuning: When and How** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — deciding fine-tune vs prompt vs RAG, and the adaptation ladder.
- **Prompting Fundamentals** — [`applied-llms.md`](../corpus/canon/applied-llms.md) / [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — writing or debugging the prompt layer before reaching for heavier machinery.

## Production plumbing

- **Guardrails: Output Quality Control** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — layering output checks into the pipeline.
- **Guardrails vs Evaluators; CI vs Production** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — placing checks in the request path vs async.
- **Caching: Latency and Cost** — [`eugeneyan.md`](../corpus/canon/eugeneyan.md) — when caching pays off and where it's dangerous.
- **Traces and Looking at Data** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — defining logging and observability requirements.
- **Working with Models** — [`applied-llms.md`](../corpus/canon/applied-llms.md) — choosing, pinning, and migrating models.

## Compound systems

- **Evaluating RAG, Agents, and Multi-Turn Systems** — [`hamel-evals.md`](../corpus/canon/hamel-evals.md) — architecting a compound system so it stays evaluable.
- **Research Line: Data Systems for LLM Pipelines** — [`sh-reya.md`](../corpus/canon/sh-reya.md) — pipeline decomposition and cost/quality co-optimization, with academic backing.
- **resources.md chapter-by-chapter pointers** — [`aie-book-repo.md`](../corpus/canon/aie-book-repo.md) — citation quarry for primary sources per architecture topic.
