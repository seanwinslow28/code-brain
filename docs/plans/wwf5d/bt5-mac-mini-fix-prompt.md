# BT5 → Phase C — MBP Tier-2 agent-fleet fix (Mac Mini handoff prompt)

**Run this in Claude Code on the Mac Mini.** The scheduled agents
(`com.sean.agent.vault-synthesizer`, `com.sean.agent.knowledge-lint`) load on the Mac Mini,
not the MBP — so the down-host simulation, the up-host byte-identical check, and especially
the ≥1-week live-fleet extinction check can only be validated where the fleet actually runs.
The MBP is the Tier-2 model *host*; the Mac Mini is the scheduler/driver. Do **not** implement
this on the MBP.

Paste everything below the line into Claude Code on the Mac Mini.

---

## Task: implement the BT5 Tier-2 reachability fix

You are implementing a root-cause fix that was already diagnosed and specced (by Fable 5 and
independently corroborated by Opus 4.8) during the WWF5D campaign. Your job is decision +
implementation, not re-diagnosis.

### Read first, in order
1. `docs/plans/wwf5d/fable-runs/bt5-fable.md` — the primary diagnosis + fix spec (three
   origins A/B/C; changes C1–C5; done-criteria; edge cases; rollout order). **This is the spec you implement.**
2. `docs/plans/wwf5d/baselines/bt5-opus.md` — Opus's independent diagnosis of the same
   problem (a second read; use it to sanity-check).
3. `docs/plans/wwf5d/fable-runs/bt5-diff.md` — where the two runs converge and split.
4. `vault/00_inbox/tickets.md` → the ticket "Fable 5 campaign **BT5 fix implementation (Phase C)**".

The two runs independently reached the same mechanical fixes — treat the convergent core
(C1, C2, C4, and C3's corpus-injection + kill-the-silent-catch) as high-confidence.

### STOP — two owner forks Sean must decide before you write any code

Present both to Sean, get an explicit decision, and record it in the ticket + a CHANGELOG
note **before** implementing. The evidence for each side is in `bt5-fable.md` (Origin C;
Phase 2 table; §Fix Spec) and `bt5-diff.md`.

**Fork 1 — lint Tier-2 LLM leg: wire it, or retire it?**
- *Wire it* (C3 as specced): `CLAUDE.md` advertises `soul-tier-a-conflict`, but the LLM leg
  was never wired into production. Wiring makes the advertised feature real (needs corpus
  injection + killing the silent `except: pass`).
- *Retire it*: sql/regex findings have carried every lint report to date; the LLM leg has
  never produced a single finding. Retiring means correcting `CLAUDE.md`/docs to stop
  advertising it and removing the dead wiring.

**Fork 2 — synthesis host binding: relocate to Mac Mini, or stay on MBP + C5 catch-up?**
- *Relocate to the always-on Mac Mini*: kills the availability problem outright — but needs a
  smaller model that must first clear `evals/vault-synthesizer/` (quality-regression risk;
  v3.14.3 deliberately kept synthesis on the MBP for capacity).
- *Stay on MBP + C5 catch-up window*: preserves MBP-class quality; accepts off-LAN misses as
  cheap, typed deferrals plus a same-day catch-up fire. (v3.14.3's per-task quality rationale
  + the "catch-up converges within days" evidence favor this; the availability pain favors relocate.)

### Implement (only after the forks are decided)

Follow `bt5-fable.md`'s Fix Spec exactly. Discipline:
- **TDD** — `verification-loops` (write the failing test first), and `verification-before-completion`
  before any "done" claim. Each change opens by citing the Origin it fixes (the spec's Phase-4 rule).
- **Rollout order** — C1+C2 together (route once per run + fail-fast circuit breaker + notify
  gate + tests) → C4 (typed-`wol-deferred` manifest truthfulness + the consumer sweep, incl.
  the substack-drafter dry-threshold) → C3 (lint wiring — its own PR, largest surface) →
  observe ≥1 real week (done-criterion 6: the live-fleet extinction histogram over new
  manifests) → decide C5 (window-widening) with Sean.
- **Also land** — the `CLAUDE.md` agents-table correction (Tier-2 model is
  `qwen3.6_35b-a3b-32k` since 2026-05-26, not Qwen3-14B; "skip-and-continue" is falsified —
  describe the new typed-deferral semantics) and, as a separate cosmetic commit, the
  `_normalize_model_name` stale-enum fix.

### Hard non-goals (from the spec — do not violate)
1. **No paid-API fallback** for `vault_synthesis` / `heavy_synthesis` / `job_scoring` / the new
   lint route. The $0 cost-integrity contract is deliberate — a miss must never bill Anthropic.
2. **Do not resurrect WOL** for the MBP (Private Wi-Fi Address MAC randomization still holds).
3. **Do not move** `vault_synthesis`/lint-T2 to Mac Mini/Alienware models **unless Fork 2 says so.**
4. **Keep exit code 0** on environmental deferral. Don't change the synthesizer's
   validation/depth-gate, retrieval tiers, prompt, budget default, the ≥2-wikilink invariant,
   index regen, FileLock, atomic manifest writes, or the "persist indexer state only on
   ok/partial" rule (that rule IS the implicit retry queue). Don't change lint Tier-1 checks,
   the report's severity buckets, exclusion dirs, or the SQL fast path.
5. **No new auto-commit mechanisms** (CLAUDE.md rule 8); don't re-enable the 6 disabled agents
   (AUDIT-2026-04-09); don't touch or remove the wake-scheduler's job-feed/substack entries.

### Done
Land per the rollout order; `python3 scripts/validate.py` green; CHANGELOG entry; the fork
decisions recorded. The real acceptance is done-criterion 6 — after ≥1 week, new manifests
show zero `status=error`+`model_used=none` misses; any misses present as `wol-deferred` with
`duration_seconds < 180`.
