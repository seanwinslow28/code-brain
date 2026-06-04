# MBP-Away Weekend — Expected Fleet Behavior (2026-06-05 → 06-07)

**Window:** Depart Fri 2026-06-05 ~09:30, return Sun 2026-06-07 ~14:00. MacBook Pro travels with Sean → unreachable on the LAN for the whole window.

**Verdict:** No action needed. Every MBP-dependent path fails safe by design — **$0 cost, no data loss, no paid fallback**. This note exists so the deferrals read as *designed*, not *broken*, when reviewing logs / the daily-note `deferred` lines afterward.

## MBP-dependent agents and what happens

| Agent | Fires in window | Behavior (MBP unreachable) | Cost | Data loss? |
|---|---|---|---|---|
| **Vault Synthesizer** ([vault_synthesizer.py:1372](../agents/vault_synthesizer.py)) | Sat 02:30, Sun 02:30 | `route_to_macbook` polls 90s → 1 Pushover alert → raises `WOLUnavailable` → caught → writes `wol-deferred` manifest, `status=deferred`, returns 0 | $0 — no API fallback | No. Incremental; backfill catches up |
| **Job Feed** ([job_feed.py:143](../agents/job_feed.py)) | Sat ×7, Sun ×7 (all AM fires miss; back 14:00) | Feeds fetched + rules-filtered + **persisted to SQLite**; only LLM scoring leg gated on `mbp_up` → skipped, postings left `fit_score=NULL`, carried over | $0 (`fallback_disabled=true`) | No. Scored on carryover when MBP returns |
| **Knowledge Lint** ([knowledge_lint.py:480](../agents/knowledge_lint.py)) | Sun 22:00 | MBP back by ~14:00 → Tier 2 runs normally if MBP on + Ollama up. Else Tier 2 defers, Tier 1 (Mac Mini) still runs | $0 | No |
| **Flush** (SessionEnd) | interactive only | Away → few/none; small sessions route to Mac Mini `gemma4:e4b` anyway | $0 | No |

**Unaffected (Mac-Mini-local, no MBP dependency):** Vault Indexer (02:00), Deep Researcher (02:45), Vault Critic (03:30, Codex+AG), Daily Driver (08:30), Meta-Agent (08:45). All run normally.

## Why it's safe by design (not luck)

- **No paid fallback ever fires.** `route_to_macbook` *raises* `WOLUnavailable` rather than cascading to the Claude API ([hybrid_router.py:435](../lib/hybrid_router.py)); Job Feed's `fallback_disabled=true` is the same guard. These flags exist for exactly this scenario.
- **No data lost** — job postings persist unscored and carry over; synthesis is incremental.
- **No one wakes the MBP.** Config is explicit: "no agent wakes the MBP anymore" ([config.toml:409](../config.toml)). The wake-scheduler LaunchDaemon only queues the MBP's own pmset wakes, irrelevant off-LAN.
- This is the **normal degraded state**, not a new failure mode. The synthesizer already "succeeds only when MBP awake" (CLAUDE.md) and is routinely intermittent — the weekend just guarantees two misses instead of probabilistic ones.

## The only real artifact

**Two Pushover pages at 02:30 (Sat + Sun)** from the synthesizer's `notify_wol_failure`. Expected noise. Left in place deliberately — silencing would mean unloading the synth plist for the weekend (reversible if desired; not done here).

## On return (Sun 06-07 afternoon)

Nothing to do. Confirm MBP is on + Ollama running so Sun 22:00 Knowledge Lint Tier 2 and Mon's runs (synth backfill, job-feed carryover scoring) pick up cleanly.
