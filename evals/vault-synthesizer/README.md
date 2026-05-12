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

**1/10 (10%) — by design.** The 7 failures are the failure modes the Workstream
B synthesizer fix needs to address. After the fix lands, target pass rate is
7+/10. See `traces/baseline-run-2026-05-12.md` for the per-case classification.

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
