# Daily Driver — Eval Suite

A binary pass/fail eval suite for the autonomous morning daily-driver agent.
Mirrors the [`evals/vault-synthesizer/`](../vault-synthesizer/) structure.

> **Phase 1 scope: fleet-memory wiring only.** Two cases (dd-001, dd-002)
> verify that the daily_driver builds correct SDK options when fleet-memory
> is enabled vs. disabled. Production-grounded morning-brief failure modes
> land in Phase 2 once traces accumulate.

## Quickstart

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/daily-driver/runner.py -v
```

(Running from any other CWD breaks the `agents` import — the `cd agents-sdk`
prefix is mandatory, same as the synth eval.)

## Current baseline

**Phase 1 ship (2026-05-27 plan): 2/2 (100%).** Both cases assert wiring
shape and pass against the implementation built in Tasks 9 and 10. Cases
are pre-emptive (guarding the wiring against drift), not regression-driven
— there's no production failure to point to yet.

## Forward roadmap

[`deferred-cases.yaml`](deferred-cases.yaml) lists 4 named-but-not-runnable
cases (dd-003 through dd-006) for Phase 2:

- **dd-003** Morning-brief shape (`## Morning Focus`, 1-3-5 structure)
- **dd-004** Vault Health propagation (success-empty → WARNING)
- **dd-005** MBP-asleep fallback signaling
- **dd-006** Fleet-memory retrieval — does the model actually reference
  stored lessons in its brief?

Each blocked on accumulating traces, not on test infrastructure.

## Sources

- Eval pattern lifted from [`evals/vault-synthesizer/`](../vault-synthesizer/)
- Underlying agent: [`agents-sdk/agents/daily_driver.py`](../../agents-sdk/agents/daily_driver.py)
- Fleet-memory plan: [`agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md`](../../agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md)
