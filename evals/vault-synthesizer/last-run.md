# Vault Synthesizer Eval Run — 2026-05-12T20:41:48.451326+00:00

> **Read this first.** This suite ships intentionally red. Each ❌ below is a
> real production failure mode this suite catches — not a broken eval. The
> pass rate jumps after the Workstream B synthesizer fix lands. See
> `EXPLANATION.md` for the design rationale.

| ID | Category | Result | Notes |
|---|---|---|---|
| vs-014 | output-completeness | ⏸️ SKIPPED | ('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer/runner.py', 158, "Skipped: requires a live (or richly-mocked) LLM caller that returns a well-formed concept dict with >= 2 wikilinks; offline mocks can't faithfully test this output-side regression. Defer to Workstream C live runs.") |
| vs-015 | output-completeness | ✅ PASS |  |
| vs-016 | status-misreport | ✅ PASS |  |
| vs-017 | status-misreport | ✅ PASS |  |
| vs-018 | schema-integrity | ✅ PASS |  |
| vs-019 | config-fail-loud | ✅ PASS |  |
| vs-020 | index-integrity | ✅ PASS |  |
| vs-021 | downstream-consumer | ✅ PASS |  |
| vs-012 | source-attribution | ⏸️ SKIPPED | ('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer/runner.py', 158, 'Skipped: pass_criteria is English not Python; runner has no concept-body reader path; both are post-Workstream-B follow-ups') |
| vs-013 | stale-overweighting | ⏸️ SKIPPED | ('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/evals/vault-synthesizer/runner.py', 158, 'Skipped: pass_criteria is English not Python; age_distribution fixture unimplemented; result has no cluster_link_ages_days field; all three are post-Workstream-B follow-ups') |

**Baseline pass rate: 7/10 (70%) — by design.**
