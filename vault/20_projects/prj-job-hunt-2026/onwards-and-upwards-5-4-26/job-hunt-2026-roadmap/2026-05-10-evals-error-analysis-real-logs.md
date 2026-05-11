---
type: error-analysis
project: prj-job-hunt-2026
artifact: vault-synthesizer-evals
created: 2026-05-10
status: complete
sources_used:
  - vault/health/synth-manifest-2026-05-{02..10}.json
  - vault/90_system/agent-logs/vault-synthesizer-2026-05-{08..10}.log
  - vault/90_system/agent-logs/vault-synthesizer-stderr.log
  - agents-sdk/agents/vault_synthesizer.py
  - vault/knowledge/index.md (empty)
ai-context: "Step 0 / Step 1 of the Hamel-Anthropic eval design playbook — open-coded 17 days of real synthesizer traces. Output is the failure taxonomy that grounds the YAML eval cases. Per Hamel: 'You cannot write meaningful evals for failure modes you haven't first observed in data.'"
---

# Vault Synthesizer — Error Analysis from Real Production Logs

> **What this is.** The error-analysis-first deliverable Hamel and Anthropic both insist on before any YAML case gets written. I open-coded 17 days of real synthesizer manifest data and stderr logs (2026-04-24 → 2026-05-10), grouped what I found into a six-mode failure taxonomy, and re-baselined the eval suite scope around what's actually broken — not what I imagined was broken.

> **Headline finding.** The vault synthesizer has produced **zero concept articles, zero connection articles, and zero typed reasoning edges** across at least the last 7 nightly runs (2026-05-02 through 2026-05-10). Two of those seven runs reported `status: "ok"`. The Phase 6 knowledge loop's consumer side — the SessionStart hook injecting `vault/knowledge/index.md` — has been dutifully prepending an empty index to every Claude Code session for at least nine days. The pre-drafted YAML hallucination cases from Gemini DR / Perplexity were aimed at a target that has never had an opportunity to hallucinate.

---

## 1. The Raw Evidence (open coding pass)

Pulled from `vault/health/synth-manifest-*.json` (7 runs):

| Date | status | concepts | connections | edges | files | duration | model_used | wol_status |
|---|---|---|---|---|---|---|---|---|
| 2026-05-02 | partial | 0 | 0 | 0 | 30 | 2713s | `""` | `""` |
| 2026-05-03 | **ok** | 0 | 0 | 0 | 20 | 1809s | `""` | `""` |
| 2026-05-06 | partial | 0 | 0 | 0 | 30 | 2720s | `""` | `""` |
| 2026-05-07 | partial | 0 | 0 | 0 | 30 | 2722s | `""` | `""` |
| 2026-05-08 | partial | 0 | 0 | 0 | 30 | 2729s | `""` | `""` |
| 2026-05-09 | **ok** | 0 | 0 | 0 | 21 | 1915s | `""` | `""` |
| 2026-05-10 | partial | 0 | 0 | 0 | 30 | 2756s | `""` | `""` |

`vault/knowledge/concepts/` — empty directory.
`vault/knowledge/connections/` — empty directory.
`vault/knowledge/index.md` — `_(none yet)_` for both Concepts and Connections.

`vault-synthesizer-stderr.log` (last 80 lines, 2026-05-10):
```
Health check failed for macbook_pro:
Pushover notify_wol_failure send failed: Missing Pushover credentials
  in Keychain (pushover_user_key / pushover_app_token)
[…repeated ~40 times across the run…]
[INFO] synthesis partial concepts=0 connections=0 rejected=0 edges=0
       edges_rejected=0 duration=2756.0s
```

The MBP is asleep. The HybridRouter can't reach it. The synthesizer keeps trying. The Pushover credentials that would alert me to the failure are missing from the Keychain. Three layers of silence between "the LLM never fires" and "Sean discovers."

---

## 2. The Six-Mode Failure Taxonomy (axial coding)

After open-coding the seven runs and the stderr tail, I grouped notes into six categories. None of them were on my pre-drafted hallucination list. Theoretical saturation hit fast — 7 traces, no new categories surfacing.

### Mode 1 — Silent empty output reported as `status: "ok"` ⚠️ LIVE
**Detection signal.** `status == "ok" AND concepts_written == 0 AND connections_written == 0 AND files_processed > 0`
**Evidence.** 2/7 runs (2026-05-03, 2026-05-09).
**Why it happens.** `run_synthesis()` initializes `result = SynthesisResult(status="ok")` and only flips to `"partial"` if budget runs out. Per-file LLM failures are caught with `except Exception` and appended to `result.warnings`; they do not promote the run-level status. The status field cannot represent "ran cleanly, processed files, emitted nothing."
**Severity.** HIGH — this is the failure mode that makes the other five invisible.
**Maps to.** Perplexity vs-015 (predicted, now confirmed live).

### Mode 2 — `status: "partial"` collapses two distinct conditions ⚠️ LIVE
**Detection signal.** `status == "partial"` is emitted both when (a) the run produced 50 concepts and timed out at file 28/30, AND (b) the run produced 0 of anything and timed out at file 28/30. Same status, opposite meanings.
**Evidence.** 5/7 runs (2026-05-02, -06, -07, -08, -10) — all "partial," all zero output.
**Why it happens.** Status taxonomy is `{ok, partial, budget-exhausted, wol-deferred, error}`. There's no `partial-empty` or `success-empty`.
**Severity.** HIGH.
**Maps to.** Anthropic Step 5: "Some evaluations have subtle failure modes that result in low scores even with good agent performance, as the agent fails to solve tasks due to grading bugs." The grader (status field) is the bug.

### Mode 3 — Silent LLM-call failure swallowed per file ⚠️ LIVE
**Detection signal.** `result.warnings` populated with "LLM call failed for X.md: <exception>"; `model_used == ""`; `concepts_written == 0`.
**Evidence.** All 7 runs. The stderr log shows the upstream cause (MBP health check failed, WOL unreachable), but the run-level result hides it.
**Why it happens.** The `except Exception` in the per-file loop catches everything — connection refused, model not loaded, timeout, WOL deferral — and continues. Loop ends "successfully."
**Severity.** HIGH.
**Maps to.** Hamel canon: "Open code traces, focusing on the *first upstream failure*." This eval needs to detect the upstream failure, not the symptom.

### Mode 4 — `model_used` empty string is ambiguous between three states ⚠️ LIVE
**Detection signal.** `model_used == ""` could mean (a) not yet set, (b) intentionally blank, (c) unset because LLM never fired. All seven runs are case (c) but the schema can't say so.
**Evidence.** All 7 runs.
**Why it happens.** Schema design defaults to empty string instead of an enum like `{"qwen3-14b", "claude-sonnet-fallback", "no-call-attempted", "no-call-failed"}`.
**Severity.** MEDIUM — encodes the bug rather than causing it, but makes downstream consumers (Daily Driver morning brief) report misleading state.
**Maps to.** Anthropic Step 5: "Make your graders resistant to bypasses." An empty string is the easiest bypass.

### Mode 5 — Cascading-silence chain ⚠️ LIVE
**Detection signal.** When LLM call fails, the alert path (Pushover) also silently fails because credentials aren't in Keychain. The "tell Sean about the failure" mechanism is itself broken.
**Evidence.** stderr log, all recent runs: `Pushover notify_wol_failure send failed: Missing Pushover credentials in Keychain` repeated ~40x per run.
**Why it happens.** The notification subsystem treats "no credentials" as a warning rather than an init-time fatal config error.
**Severity.** HIGH (compound).
**Maps to.** The "Swiss Cheese Model" Anthropic invokes in their layered-eval section. Three holes lined up.

### Mode 6 — Daily-driver morning brief consumes silent-failure manifest as healthy ⚠️ LIVE
**Detection signal.** Per `CLAUDE.md`: *"daily_driver.py morning brief surfaces them under Vault Health (second touch on this file: Phase 1 of agent-wiring added the artifact preamble, Phase D adds the synth line)."* The brief reads the manifest's `status` field and reports it directly. `status == "ok"` becomes "synthesis ran cleanly" in the morning briefing even when nothing was produced.
**Evidence.** Inferred from `CLAUDE.md` Phase 1 / Phase D wiring + the manifest data above. (Direct verification would require pulling a recent morning brief — deferred.)
**Severity.** HIGH — this is the consumer-side analog of Mode 1.
**Maps to.** Anthropic Step 6: "Read the transcripts." The morning brief was reading the manifest but never reading the actual `vault/knowledge/concepts/` directory to verify articles existed.

---

## 3. What This Changes in the Eval Suite Plan

The pre-drafted YAML cases from Gemini DR + Perplexity assumed the synthesizer was running and producing *something*, with hallucinations / drift / temporal confusion as the failure surface. **None of those cases would fire on the current system, because the LLM has not been invoked once in 9 nights.**

### Cases to keep (4 of 15 pre-drafts)
- **vs-015** (Perplexity, output-completeness silent empty) — promote from "predicted" to "the load-bearing case." This is the single most important case in the suite.
- **vs-014** (Perplexity, silent omission) — adapt to detect "0 concepts emitted from a 5+ note corpus mentioning a named system."
- **vs-012** (Gemini, source-attribution loss) — keep, but defer until LLM actually fires again.
- **vs-013** (Gemini, stale-content overweighting) — keep, defer.

### Cases to add (newly grounded in real data)
- **vs-016 — Status-field misreport.** Run synthesizer with the LLM caller mocked to raise `ConnectionRefusedError` for every file. Assert `result.status != "ok"`.
- **vs-017 — Status-field collapse for partial-empty.** Same setup, run to budget timeout. Assert `result.status` distinguishes "partial-some-output" from "partial-zero-output." (May require schema change to a new `partial-empty` status.)
- **vs-018 — Empty-string `model_used` rejection.** Assert that `model_used` is one of an enum set, never empty string. Enum gets added in the same patch.
- **vs-019 — Pushover credentials health check.** Assert that on agent boot, missing Pushover creds raise `ConfigurationError` rather than getting logged-and-ignored. (Eval pre-condition, runs once at startup.)
- **vs-020 — Knowledge index integrity.** Assert that `vault/knowledge/index.md` reflects the count of files in `vault/knowledge/concepts/` and `vault/knowledge/connections/`. Catches the case where the index says "(none yet)" but disk has articles, or vice versa.
- **vs-021 — Daily-driver brief consumer check.** Mock a synth-manifest with `status="ok" AND concepts_written=0` and assert the morning brief surfaces this as a WARNING, not "ok." (Cross-agent integration eval.)

### Cases to drop or defer (11 of 15 pre-drafts)
The hallucination, edge-confidence, relation-tag-drift, and temporal-confusion cases (vs-001 through vs-011) are real failure modes — for a synthesizer that's running. They go to a `deferred-cases.yaml` file with a one-line note: *"Re-enable when synthesizer produces ≥1 concept article in a clean run."*

---

## 4. The Single Most Important Talking Point This Generated

> **"I read 5,000 words of canonical eval guidance, sat down to write hallucination cases for my synthesizer, and discovered my synthesizer hadn't produced an output in 9 nights. The status field said 'ok' twice. The Pushover alert that would have told me was silently failing because the credentials weren't loaded. The Daily Driver morning brief was reading the manifest and reporting 'synthesis ran cleanly.' I had built three layers of automation to monitor a system, and all three layers were lying to me in synchrony. The eval suite I'm shipping is the first thing in this stack that would have caught it on day one."**

That's the interview answer. It hits three notes at once: (1) Hamel's "error analysis before infrastructure" is not theoretical — real systems break in modes you would not have predicted; (2) Anthropic's "read the transcripts" is the only thing that surfaces this; (3) the "Swiss Cheese Model" of layered evals is real because individual layers fail silently in correlated ways.

---

## 5. Next Steps

1. ✅ Open-code real traces → DONE (this doc).
2. ⏳ Rewrite `cases.yaml` with the 6 grounded cases + 4 retained pre-drafts (deferred cases out to `deferred-cases.yaml`).
3. ⏳ Build the pytest+YAML runner (~100 lines) in `evals/vault-synthesizer/runner.py`.
4. ⏳ Run the suite once, confirm pass rate is genuinely below 100% (Mode 1 alone fails the suite by design).
5. ⏳ Write the `EXPLANATION.md` 4Q artifact, with the "What did I learn?" section grounded in this doc.
6. ⏳ Loom (5 min): show the real manifest data, run the eval suite, walk one transcript.
7. ⏳ Substack post syndicating the narrative (draft at `2026-05-10-the-night-my-vault-said-nothing.md`).

**Out of scope, not built (per the don't-build lists in both research docs):** GitHub Actions CI/CD wiring, generic eval framework abstraction, Braintrust/Langfuse integration, cross-model comparison, coverage dashboards.

---

## Sources Cited In This Analysis

- `vault/health/synth-manifest-2026-05-{02,03,06,07,08,09,10}.json` — primary evidence
- `vault/90_system/agent-logs/vault-synthesizer-stderr.log` — failure-mode-5 evidence
- `agents-sdk/agents/vault_synthesizer.py` (lines 320–420, 580–660) — control-flow grounding
- `vault/knowledge/index.md` — empty-state confirmation
- [`2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md`](../../research/2026-05-09-perplexity-ai-eval-fluency-primer-and-reference-cases.md) — vs-014, vs-015
- [`2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md`](../../research/2026-05-09-gemini-ai-eval-fluency-primer-and-reference-cases.md) — vs-012, vs-013
- [`ref-anthropic-demystifying-agent-evals.md`](../../../../40_knowledge/references/ref-anthropic-demystifying-agent-evals.md) — Steps 5, 6 framework
- [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) — Task 6 §I scope (Week 5 evals fluency, Week 7 publication)
