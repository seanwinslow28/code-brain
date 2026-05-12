# Vault Synthesizer Eval Run — 2026-05-12T16:14:50.553631+00:00

> **Read this first.** This suite ships intentionally red. Each ❌ below is a
> real production failure mode this suite catches — not a broken eval. The
> pass rate jumps after the Workstream B synthesizer fix lands. See
> `EXPLANATION.md` for the design rationale.

| ID | Category | Result | Notes |
|---|---|---|---|
| vs-014 | output-completeness | ❌ FAIL | ../evals/vault-synthesizer/runner.py:220: Failed |
| vs-015 | output-completeness | ❌ FAIL | ../evals/vault-synthesizer/runner.py:220: Failed |
| vs-016 | status-misreport | ❌ FAIL | ../evals/vault-synthesizer/runner.py:220: Failed |
| vs-017 | status-misreport | ❌ FAIL | ../evals/vault-synthesizer/runner.py:220: Failed |
| vs-018 | schema-integrity | ❌ FAIL | ../evals/vault-synthesizer/runner.py:220: Failed |
| vs-019 | config-fail-loud | ❌ FAIL | ../evals/vault-synthesizer/runner.py:179: Failed |
| vs-020 | index-integrity | ✅ PASS |  |
| vs-021 | downstream-consumer | ❌ FAIL | ../evals/vault-synthesizer/runner.py:159: Failed |
| vs-012 | source-attribution | ⏸️ SKIPPED | ('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer/runner.py', 153, 'Skipped: requires live synthesizer output; skipped until Workstream B') |
| vs-013 | stale-overweighting | ⏸️ SKIPPED | ('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer/runner.py', 153, 'Skipped: requires live synthesizer output; skipped until Workstream B') |

**Baseline pass rate: 1/10 (10%) — by design.**
