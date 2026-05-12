# Vault Synthesizer Eval Run — 2026-05-12T (baseline, manually written — see anomaly note in traces/baseline-run-2026-05-12.md)

> **Read this first.** This suite ships intentionally red. Each ❌ below is a
> real production failure mode this suite catches — not a broken eval. The
> pass rate jumps after the Workstream B synthesizer fix lands. See
> `EXPLANATION.md` for the design rationale.

| ID | Category | Result | Notes |
|---|---|---|---|
| vs-014 | output-completeness | ❌ FAIL | vs-014: result.concepts_written >= 1 evaluated False |
| vs-015 | output-completeness | ❌ FAIL | vs-015: not (result.status == 'ok' and result.concepts_written == 0) evaluated False |
| vs-016 | status-misreport | ❌ FAIL | vs-016: result.status != 'ok' evaluated False |
| vs-017 | status-misreport | ❌ FAIL | vs-017: result.status == 'partial-empty' evaluated False |
| vs-018 | schema-integrity | ❌ FAIL | vs-018: result.model_used in {'qwen3-14b', 'claude-sonnet-4-6', 'claude-haiku-4-5', 'none'} evaluated False |
| vs-019 | config-fail-loud | ❌ FAIL | vs-019: PushoverConfigurationError class does not exist yet (Workstream B adds it) |
| vs-020 | index-integrity | ✅ PASS | |
| vs-021 | downstream-consumer | ❌ FAIL | vs-021: daily_driver.render_vault_health does not exist yet (Workstream B adds it) |
| vs-012 | source-attribution | ⏸️ SKIPPED | requires live synthesizer output; skipped until Workstream B |
| vs-013 | stale-overweighting | ⏸️ SKIPPED | requires live synthesizer output; skipped until Workstream B |

**Baseline pass rate: 1/10 (10%) — by design.**
