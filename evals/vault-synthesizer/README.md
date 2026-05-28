# Vault Synthesizer — Eval Suite

A 10-case binary pass/fail eval suite for a local Qwen3-14B vault synthesizer
agent. Cases were grounded in 17 days of real production logs, not imagined
failure modes. Built solo over two days as a portfolio artifact during a job
search; the discipline transferred from Hamel Husain and Shreya Shankar's
canon and Anthropic's "Demystifying Agent Evals" playbook.

> **This suite ships intentionally red.** ~80% of cases fail today by design
> — each ❌ is a real production failure mode the suite catches, not a broken
> eval. The pass rate jumps after the Workstream B synthesizer fix lands. See
> `EXPLANATION.md` for the why.

## Quickstart

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/vault-synthesizer/runner.py -v
```

(Running from any other CWD breaks the `agents_sdk` import — the `cd agents-sdk`
prefix is mandatory.)

## Current baseline

**Pre-fix (Workstream A ship, 2026-05-22): 1/10 (10%).** 7 cases red by design + vs-020 passing on the static fixture parity check. Each red case named a specific failure mode the synthesizer fix needed to address. See [`traces/baseline-run-2026-05-12.md`](traces/baseline-run-2026-05-12.md) for the per-case classification.

**Post-fix (Workstream B complete, 2026-05-12): 7/10 (70%).** vs-015, vs-016, vs-017, vs-018, vs-019, vs-021 all flipped green via targeted patches to `agents-sdk/agents/vault_synthesizer.py`, `agents-sdk/lib/pushover.py`, and `agents-sdk/agents/daily_driver.py`. Three cases remain skipped with explicit `skip_reason` fields in [`cases.yaml`](cases.yaml):

**Phase 1 fleet-memory addendum (2026-05-27): 4 cases added (vs-022 to vs-025) covering memory-preamble injection and lesson-write gating. Pass-rate target after Task 11 ships: 11/14 = 79% (the three skipped cases vs-012/013/014 remain deferred).**

> **Pre-existing miscoding — vs-016 and vs-017 (tracked, not Phase 1 scope).** On the post-Phase-1 baseline both cases are red. Root cause: the empty mock retriever in `_invoke_synthesizer` collides with the Tier 1.5 thin-source gate (`_MIN_SIMILAR_FOR_LLM=2`) — the gate skips the LLM call so `STATUS_ERROR` never reaches the assertion the cases test. The 2-line fix lives in [`runner.py`](runner.py) `_invoke_synthesizer`: change `def retriever(text, top_k): return []` to return ≥2 stub similars. Filed as a separate ticket; **do not fix in the Phase 1 follow-up batch.**

- **vs-012, vs-013** — `pass_criteria` are English prose, not Python expressions; the runner has no concept-body reader path; vs-013 also needs an `age_distribution` fixture and a `cluster_link_ages_days` field on `SynthesisResult`. All three are post-Workstream-B follow-ups.
- **vs-014** — requires a live (or richly-mocked) LLM caller that returns a well-formed concept dict with >= 2 wikilinks; offline mocks can't faithfully test this output-side regression. Deferred to Workstream C live runs.

The 1 → 7 jump documents what the synthesizer fix accomplished. The three remaining skips are honest deferrals, not silent failures — each names the specific eval-mechanics or fixture-infrastructure blocker.

## The failure taxonomy

Six observed failure modes, summarized in [`failure-modes.md`](failure-modes.md):

1. Silent empty output (Mode 1)
2. Status-field misreport on per-file LLM failures (Mode 2)
3. Missing status taxonomy values (Mode 3)
4. `model_used` schema integrity (Mode 4)
5. Pushover credentials fail-quiet (Mode 5)
6. Downstream-consumer misread of healthy status (Mode 6)

The evidence behind each mode is open-coded in [`traces/coded-traces.md`](traces/coded-traces.md).

## Portfolio artifact

See [`EXPLANATION.md`](EXPLANATION.md) for the 4Q comprehension write-up.

## Sources

See [`references.md`](references.md).
