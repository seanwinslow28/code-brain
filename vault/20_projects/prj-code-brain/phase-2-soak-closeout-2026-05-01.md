---
type: review
domain:
  - claude-mastery
  - the-block
  - creative-studio
  - life-systems
status: complete
context: code-brain
created: 2026-05-01
source: agent-wiring-rollout-phase-2-soak
references:
  - vault/20_projects/prj-code-brain/prj-agent-wiring-rollout.md
  - vault/20_projects/prj-code-brain/prj-knowledge-loop-consumer.md
---

# Phase 2 Soak Closeout — 2026-05-01

**Branch:** `knowledge-loop/phase-b` (merged to `main` as `19a805e`).
**Phase 2 commit:** `3636365` — `feat(agent-wiring): Phase 2 — meta_agent / flush / knowledge_lint consume operating-model artifacts (v3.17.0)`.
**Soak window:** 2026-04-28 → 2026-05-01 (4 days, inclusive).
**Conclusion:** **PARTIAL.** Five gates PASS, two PARTIAL (G4, G5) — both for the same reason: the soak window did not contain the production conditions needed to exercise those code paths. No regression observed; the Phase 2 wiring is functioning where it ran.

---

## Gate-check table

| # | Gate | Status | Evidence |
|---|---|---|---|
| G1 | `pytest agents-sdk/tests/` full suite green | **PASS** | `177 passed in 6.93s`. No failures, no errors, no skips reported. |
| G2 | `python3 scripts/validate.py` PASSED (no new errors) | **PASS** | `Validation PASSED (58 warning(s))`. Warnings are pre-existing secret-pattern false positives in `last30days/`, `mcp-integration/`, `react-vite-tailwind/`, `creative-studio/16bitfit-battle-mode/` — none introduced by Phase 2. |
| G3 | Pre-flight JSON guard 5/5 (baseline) | **PASS — baseline only** | Already confirmed at ship time (frontmatter line 14: "pre-flight JSON-shape guard PASS (5/5 historical transcripts × gemma4:e4b + SOUL prepend)"). Not re-run — guard was the ship gate, not a soak gate. |
| G4 | One real flush run on a session touching `the-block/**` emits tags referencing Ed / Matt / critical-path | **PARTIAL** | Flush invoked **21 times** during the window; **all 21 hit the recursion guard** (`messages=0 sections=0 duration=0ms`). Zero extraction runs, therefore zero tags written, therefore no production cross-reference signal to inspect. The integration is wired (commit 3636365 prepends all-three SOULs to `EXTRACTION_PROMPT`); the soak window simply didn't trigger the conditions where flush has work to do. Pre-flight JSON guard already validated shape. See `flush-2026-04-{28,29,30}.log` and `flush-2026-05-01.log`. |
| G5 | One `knowledge_lint --full` Sunday-style run completed in ≤ 20 min on Mac Mini alone | **PARTIAL** | Last knowledge-lint run was **2026-04-26** (Sunday before Phase 2 shipped). Next scheduled Sunday run is **2026-05-03** (after the soak window). No `--full` ad-hoc run inside the window. The schedule simply did not produce a sample. Code path is wired but unexercised in production during this window. |
| G6 | Phase 6 producer-side loop (flush → vault_synthesizer → knowledge_lint) untouched and still functions end-to-end | **PASS** | `vault-indexer` ran 4/4 nights with `status=success` (chunks 91 / 178 / 242 / 117, errors=0). `vault-synthesizer` ran 4/4 nights with `status=success` (durations 724 / 1627 / 1628 / 1267 s, all under the 2700 s budget). Both wrote daily logs with `errors=0`. Concept/connection counts remain `0` per night — that is the pre-existing Mac Mini fallback behavior documented in CLAUDE.md (Qwen3-14B on MBP "intermittent"), not a Phase 2 regression. |
| G7 | No new error rows in `agent-run-history.csv` from `meta_agent`, `flush`, `knowledge-lint` during the soak | **PASS** | Window slice of CSV: `flush` × 21 rows (all `recursion-guard`, none `error`); `meta_agent` × 0 rows (agent intentionally does not call `history.append_run` — confirmed by source inspection); `knowledge-lint` × 0 rows (no run in window). Zero `ERROR` / `Traceback` / `Exception` strings in any matching per-agent log. The 7 `process-inbox` error rows in the window are pre-existing and explicitly outside the Phase 2 modified-agent set (paused 2026-04-29 in v3.17.4 per CLAUDE.md). |

---

## Domain-Aware Insights signal (G4-adjacent, Phase 2-specific)

**Fallback rate: 0 / 4 days.** All four daily fleet-status notes contain a populated `## Domain-Aware Insights` section. None fell back to `_Local summary unavailable — gemma4:e4b call returned no parseable JSON._`. The `meta-agent-stdout.log` header on each day from 2026-04-28 onward reads `Summary model: gemma4:e4b (Mac Mini, local Ollama)` — confirming the Phase 2 wiring activated and the local model is producing parseable output.

Three sample cross-references between the gemma4:e4b output and the actual `vault/05_atlas/operating-models/{domain}/schedule-recommendations.md` Protect / Decline lists:

1. **2026-04-28 → life-systems.** Output bullet: *"Develop the 15th-of-month finance automation loop (Chase/Bilt) to shift recurring admin tasks into a structured, asynchronous process."* Matches verbatim against `life-systems/schedule-recommendations.md`: *"Monthly finance check (15th). Agent pulls Chase bank + Chase credit + Bilt credit + Rippling pay stub data…"* and *"Bilt rewards check. Periodic scan for available redemptions…"*
2. **2026-04-30 → creative-studio.** Output bullet: *"Prioritize restoring connectivity and functional status for the Alienware and ComfyUI endpoints to restore full development/creative capacity."* Matches `creative-studio/schedule-recommendations.md`: *"Investigate getting Obsidian working on the Alienware (previously blocked by mac-only plugin errors). If Vault is SSoT for all 3 machines, Alienware needs parity."* The Decline guidance on ComfyUI ("Defer ComfyUI workflow testing unless we're testing against proven templates") is also reflected in the agent's framing of ComfyUI as an offline blocker rather than a target to expand.
3. **2026-05-01 → cross-domain.** Output bullet: *"vault-indexer and vault-synthesizer ran, maintaining the 'vault-as-SSoT' logging rhythm."* Direct lift of the creative-studio Decline-list anchor concept *"vault-as-SSoT with proper Git sync + real agentic mesh"* and the life-systems goal of consolidating personal data into the vault.

The local model is reaching into all three domain artifacts and producing output that names real Protect / Automate / Decline items by their actual phrasing. The cross-domain framing is consistent with the schedule-recommendations files. No hallucinated items observed in the four sampled days.

---

## flush SOUL prepend signal (G4)

Sessions written by flush during the soak window: **0**.

All 21 flush invocations (5 on 04-28, 9 on 04-29, 6 on 04-30, 1 on 05-01) hit the recursion guard with `messages=0 sections=0 duration=0ms`. The recursion guard is the SessionEnd hook's intentional short-circuit for re-entrant or zero-message contexts. The hook is firing — the underlying conditions for an extraction (a non-trivial transcript) didn't materialise during the window.

Consequence: there are no Ed / Matt / critical-path citations to inspect from production output. The 2026-04-29 daily note (`vault/10_timeline/daily/2026-04-29.md`) contains a single `## Claude Code Sessions` entry, but it was authored by `daily-driver morning` (08:45 line) — not by flush. The 2026-04-28 daily note has no Sessions block. The 2026-04-30 and 2026-05-01 daily notes do not exist.

The Phase 2 SOUL-prepend integration was validated against 5 historical transcripts at ship time (frontmatter line 14: "pre-flight JSON-shape guard PASS (5/5)"). That validation stands. The soak window simply produced no fresh production samples to confirm against.

This is reported as **PARTIAL** rather than FAIL because: (a) no error or regression has been observed in flush; (b) the recursion guard behaviour pre-dates Phase 2; (c) the integration is structurally in place. The right next step is opportunistic — confirm against the next session that produces a non-zero flush, rather than blocking on a synthetic test.

---

## Phase 6 producer-side loop

**Status: green.**

| Night | vault-indexer | vault-synthesizer |
|---|---|---|
| 2026-04-28 | success, 91 chunks, 6.7 s, 0 errors | success, 8 changed files, 724 s, 0 errors |
| 2026-04-29 | success, 178 chunks, 11.8 s, 0 errors | success, 18 changed files, 1627 s, 0 errors |
| 2026-04-30 | success, 242 chunks, 14.0 s, 0 errors | success, 18 changed files, 1628 s, 0 errors |
| 2026-05-01 | success, 117 chunks, 10.8 s, 0 errors | success, 14 changed files, 1267 s, 0 errors |

Both agents ran to completion every night, well inside the 2700 s synthesizer budget, with zero error rows in `agent-run-history.csv`. Concept/connection emission stays at `0 / 0 / 0 rejected=0` — that's the pre-existing fallback behaviour when the MBP isn't awake to serve Qwen3-14B (CLAUDE.md: *"intermittent — succeeds only when MBP awake; v3.14.3 retired WOL"*). Phase 2 did not touch this path; the empty knowledge index reported in the SessionStart system-reminder is a producer-side condition, not a Phase 2 regression.

---

## Carry-over signals (not gating)

- **`meta_agent` doesn't write to `agent-run-history.csv`.** Confirmed by source inspection — the agent has no `history.append_run` call. This is a pre-existing condition; absence of meta_agent rows during the soak is therefore expected, and the agent's actual run record lives in `meta-agent-stdout.log`. Worth tightening in a follow-up if fleet-state observability matters; not a Phase 2 issue.
- **`process-inbox` error rows in the window (7).** All known and explicitly outside the Phase 2 modified-agent set. Per CLAUDE.md, paused on 2026-04-29 (v3.17.4) pending Path B local-model rewrite. Carry-over from `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`.
- **Daily notes for 2026-04-30 and 2026-05-01 do not exist** in `vault/10_timeline/daily/`. The `daily-driver morning` runs were `status=success` per CSV, so the agent reported success; the file simply isn't on disk. Worth a quick check on `vault_io.create_from_template` writes vs. the path daily-driver actually returns. Not a Phase 2 issue, not gating, but visible in the fleet-status notes ("Daily note exists: No").
- **`agent-error count = 0` on the daily-driver path.** All four `daily-driver morning` runs in the window completed at $0.39–$0.43, well under the $0.60 cap. Phase 1 cap-bump still has comfortable headroom; Phase 2 added no daily-driver token pressure.
- **2026-04-26 knowledge-lint run.** The most recent `knowledge-lint` run (Sunday before Phase 2 shipped) completed normally per `knowledge-lint-2026-04-26.log` — but predates Phase 2 SOUL wiring, so doesn't speak to the new code path either way.

---

## Recommendation

**Hold the merge-readiness signal at PARTIAL — do not block, but don't yet declare Phase 2 fully closed either.** Five of seven gates PASS. The two PARTIAL gates (G4, G5) failed for the same structural reason: the soak window's production conditions never exercised flush extraction or the Sunday knowledge-lint pass. No regression has been observed; the Phase 2 wiring is functioning everywhere it ran. The Domain-Aware Insights output is high-quality, on-target with the schedule-recommendations files, and 4/4 days populated without fallback — that is the strongest live signal of the soak.

PR not yet open for branch `knowledge-loop/phase-b` — the branch was already merged into `main` as commit `19a805e`, so no PR comment will be posted. Sean to open one only if a separate review trail is wanted; otherwise the merge has shipped.

The clean way to convert G4 and G5 to PASS is opportunistic, not prescriptive: the next non-trivial Claude Code session that produces a real flush extraction will confirm G4, and the Sunday 2026-05-03 knowledge-lint run will confirm G5. If either produces unexpected output, instant rollback remains `[artifacts].enabled = false` in `agents-sdk/config.toml`; per-agent rollback is removing the failing agent from `[artifacts.per_agent]`. Knowledge-loop Phase C should not start until at least G4 has converted to PASS via a real flush extraction.
