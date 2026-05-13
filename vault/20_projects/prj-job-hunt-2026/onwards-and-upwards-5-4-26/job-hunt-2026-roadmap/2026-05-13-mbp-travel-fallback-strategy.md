---
type: infrastructure-spec
project: prj-job-hunt-2026
artifact: mbp-travel-fallback-strategy
created: 2026-05-13
status: trip-documented-fallback-work-deferred
sprint_epoch: 2026-05-04
companion_artifacts:
  - 2026-05-13-vault-synthesizer-retrofit-tiers.md   # eval window we're protecting on this trip
related_files:
  - agents-sdk/config.toml
  - agents-sdk/lib/hybrid_router.py
  - agents-sdk/agents/vault_synthesizer.py
  - agents-sdk/agents/job_feed.py
  - agents-sdk/agents/flush.py
ai-context: "Two-part document. PART 1 records a specific MBP-unreachable window (NY trip 2026-05-14 → 2026-05-15) so a future Claude session reviewing fleet failures from that window has context and doesn't propose remediation. PART 2 specifies the deferred fallback work Sean wants done before the NEXT trip ≥3 days. Read the Status Tracker before assuming anything is implemented."
---

# MBP Travel Fallback Strategy

> **Future Claude / future Sean reading this:** if today is between 2026-05-14 and 2026-05-16 and the fleet looks broken, that's expected — see Part 1. If today is after 2026-05-16, the trip is over and any new MBP-unreachable failures are unrelated. The fallback work in Part 2 is **not yet implemented** — check the Status Tracker.

---

## Why this exists

Sean is traveling to NY 2026-05-14 → 2026-05-15 with the MacBook Pro. The MBP hosts Qwen3-14B (LM Studio @ `192.168.68.50:1234`) for three agents — `vault_synthesizer`, `job_feed`, `flush`. When the MBP leaves the home LAN, those agents lose their preferred model and the Mac Mini-resident launchd jobs (`vault_synthesizer`, `job_feed`) will fail their health checks and either fall back, skip, or fail silently depending on agent-specific config.

This was a deliberate ship-it decision (CLAUDE.md §Agents SDK explicitly notes "succeeds only when MBP awake"), but the system has no notion of *scheduled* MBP absences — every failure looks identical to "MBP happened to be asleep." For short trips that's fine. For multi-day trips we want either (a) automatic graceful fallback or (b) a documented "trip mode" toggle. This doc captures both the specific trip and the deferred work to make trips painless.

---

## Part 1 — The 2026-05-14 → 2026-05-15 trip (CURRENT)

### Trip window

- **Depart:** Thu 2026-05-14, 8:12 AM ET (Amtrak from Boston)
- **Return:** Fri 2026-05-15, 10:00 PM ET
- **MBP location during window:** with Sean, off home LAN
- **First fully-home morning back:** Sat 2026-05-16

### Expected fleet outcomes during the window

| Agent | Fires during window | Expected behavior | Action needed |
|---|---|---|---|
| `vault_synthesizer` | Fri 5-15 02:30 AM (1 run) | Raises `WOLUnavailable` from `route_to_macbook()`, exits cleanly, logs status=fail in synth-manifest | None. Sat 02:30 picks up Thu/Fri/Sat changed-files in one batch |
| `job_feed` | Thu+Fri 8:00–11:00 AM (14 fires, 7/day) | Probe to MBP fails, scoring skipped per `fallback_disabled=true`, "Unscored — MBP was asleep" section appears in roll-up | None. Sat 8 AM fires pick up the watchlist as normal |
| `flush` (SessionEnd) | Only if Sean ends large sessions on the road | Hook tries 192.168.68.50 from the MBP itself on a foreign LAN → fails health-check → exits non-fatally. Hook count stays at 14, no extraction recorded | None. Knowledge from those sessions is lost for the trip — acceptable. Small sessions (<100 msgs) skip flush entirely |
| `knowledge_lint` | Sun 5-17 22:00 — Sean is back | Normal Mac Mini Tier-1 run; Tier-2 fires against MBP if awake | None |
| `substack_drafter` | Thu 5-14 18:00 (would fire) | Disabled by default — no fire | None |
| `daily_driver` morning | Thu+Fri 8:45 AM | Runs on Mac Mini (cloud Sonnet, MBP-independent). Morning brief surfaces "MBP was asleep at 8 AM" banner from `daily_driver.py:118` | None |

### Why we are NOT enabling fallbacks for this trip

1. **v3.34.0 retrofit eval window.** The Tier-1 retrofit ships its first nightly run Thu 2026-05-14 02:30 AM — *before* departure, while MBP is still home. Flipping `vault_synthesizer` to Sonnet fallback for Fri 5-15 would mix models inside the eval window and contaminate the "is the retrofit working?" signal. Sat 5-16 02:30 (MBP back home) is the proper second data point.
2. **Cost vs. recovery time.** Fri's missed synth run costs nothing; Sat catches up incrementally. A rushed code change the night before travel risks breaking the production retrofit path that already passed 62 tests.
3. **`job_feed.fallback_disabled = true` is an active design choice.** Flipping it for 2 days would cost ~$1 total — trivial money, but it implies "trip mode" which doesn't exist yet. We don't want one-off config drift; we want the work in Part 2 done properly.

### What to do if fleet status looks broken on Mon 5-18

Read this doc. The failures from Fri 5-15 and the Thu+Fri job_feed unscored sections are *known-expected*. Do not propose remediation. Sat 5-16 onward should be clean.

---

## Part 2 — Deferred fallback work (FUTURE)

Sean wants robust fallbacks built before the next trip ≥3 days. This section specifies the work; nothing here is implemented yet (see Status Tracker).

### Design goal

A single config-level "trip mode" or persistent automatic-fallback configuration such that:

- Any MBP-dependent agent that can run on a cloud model produces *something* instead of nothing during MBP-unreachable windows.
- The substitution is observable — every manifest / log row records which machine and which model produced the run, so post-trip review can identify substituted output.
- The substitution does not silently contaminate eval windows where Qwen3-14B is the controlled variable. (i.e., trip mode is a deliberate flip, not magic.)
- Cost is bounded — per-agent monthly cap on cloud spend during fallback, surfaced in the daily brief.

### Per-agent scope

#### `job_feed` — TRIVIAL (1 config line)

- **Current state:** `fallback_disabled = true` in [agents-sdk/config.toml:366](../../../../../agents-sdk/config.toml). When MBP fails health-check, `JobScoringUnavailable` is raised and survivors go to the "Unscored" section.
- **Fallback path already exists:** [`HybridRouter.route()`](../../../../../agents-sdk/lib/hybrid_router.py) already routes to `claude-sonnet-4-6` when local machines are unreachable and `fallback_to_api = true` (which is already the case).
- **Work needed:** wire a `trip_mode` config flag (or a date-window check against this doc) that flips `fallback_disabled` to `false` during planned trips. ~5 lines.
- **Estimated cost during fallback:** ~$0.30–0.50/day in Sonnet calls (10–30 postings/day, small scoring prompt).
- **Risk:** none. The scoring rubric is small and Sonnet handles it cleanly. No eval contamination because there's no held-out job_feed eval.

#### `vault_synthesizer` — REAL WORK (~30–50 lines + tests)

- **Current state:** [`_default_llm_caller_factory`](../../../../../agents-sdk/agents/vault_synthesizer.py) uses `router.route_to_macbook(task="vault_synthesis")` which is hardcoded to MBP and raises `WOLUnavailable` on failure. No API fallback.
- **Fallback path:** does NOT exist for this code path. `route()` would route it via task_map to MBP anyway; the fallback chain only kicks in after MBP fails.
- **Work needed:**
  1. Modify `_default_llm_caller_factory` to catch `WOLUnavailable`, then call `router.route("vault_synthesis")` (the general routing method which has the API fallback). ~20 lines.
  2. Plumb `decision.machine` and `decision.model` into `manifest_state` so the synth-manifest accurately records which model produced the run.
  3. Add `_normalize_model_name` mappings for `claude-sonnet-4-6` and `claude-haiku-4-5` (already in `MODEL_USED_VALUES` — good).
  4. New test fixture: MBP unreachable → API fallback → manifest records `model_used: claude-sonnet-4-6`, `wol_status: api_fallback`.
  5. **Trip-mode gate:** trip mode must explicitly enable the fallback; default off. Otherwise the fallback fires on any MBP-asleep night and contaminates eval windows silently.
- **Estimated cost during fallback:** ~$3–8 per run depending on changed-files volume (the v3.34.0 prompt is ~800-char chunks × N files × concept + connection passes). For multi-day trips that's bounded.
- **Risk:** eval contamination if trip-mode is left on accidentally. Mitigation: every synth-manifest row already has `model_used`, so post-hoc filtering of mixed-model runs from eval comparisons is straightforward.

#### `flush` — LOW LIFT (already partially handled)

- **Current state:** [`agents-sdk/agents/flush.py:50`](../../../../../agents-sdk/agents/flush.py) catches `WOLUnavailable` and exits cleanly. Large sessions during MBP-unreachable windows produce no extraction.
- **Work needed:** route to a smaller cloud model (Haiku 4.5) when MBP unreachable and trip-mode on. Extraction is a small prompt — Haiku is fine. ~15 lines.
- **Estimated cost during fallback:** ~$0.05/large session on Haiku. Negligible.
- **Risk:** very low. Extraction output is informational, not load-bearing for downstream agents.

#### `substack_drafter` — ALREADY HANDLED

- **Current state:** already uses general `HybridRouter` with API fallback wired ([`agents-sdk/agents/substack_drafter.py:280`](../../../../../agents-sdk/agents/substack_drafter.py)). Default disabled — N/A unless opted in.
- **Work needed:** none. If `INSTALL_SUBSTACK_DRAFTER=1` and trip mode active, fallback should already work.

### Proposed config surface

```toml
[trip_mode]
# When active=true, MBP-dependent agents fall back to cloud models instead of
# skipping/erroring. Eval-sensitive agents (vault_synthesizer) gate on this
# explicitly so unplanned MBP-asleep nights do NOT silently swap models.
active = false
start_date = ""      # ISO date, e.g. "2026-06-15"
end_date = ""        # ISO date, inclusive
reason = ""          # short note for the manifest

# Per-agent budget caps during trip mode (separate from normal max_budget_usd
# because fallback runs spend real money on the cloud).
[trip_mode.budget_caps_usd]
vault_synthesizer = 10.00   # per run
job_feed          = 1.00    # per day total
flush             = 0.50    # per session
```

### Documentation hooks

When trip mode is implemented, the following should ALSO be wired so future-Sean is never surprised:

1. **Daily-driver morning brief** — surface "Trip mode active until {end_date}, fallback runs may appear in fleet" banner.
2. **Meta-agent** — recognize fallback runs as non-anomalous when trip mode active for that date.
3. **Knowledge-lint** — skip Tier-2 (Qwen3-14B on MBP) during trip mode, run Tier-1 only.
4. **This doc** — add a NEW Part 1 entry per trip; never overwrite. Becomes the trip log.

---

## Status Tracker

| Item | Owner | Status | Last update |
|---|---|---|---|
| **Part 1 — 2026-05-14 NY trip documentation** | Sean | done | 2026-05-13 |
| Part 2 — `job_feed` trip-mode toggle | Sean | not started | 2026-05-13 |
| Part 2 — `vault_synthesizer` API fallback + manifest plumbing | Sean | not started | 2026-05-13 |
| Part 2 — `flush` Haiku fallback path | Sean | not started | 2026-05-13 |
| Part 2 — `[trip_mode]` config surface | Sean | not started | 2026-05-13 |
| Part 2 — daily-driver banner + meta-agent recognition | Sean | not started | 2026-05-13 |

### Re-evaluation triggers

Promote Part 2 from "deferred" to "active sprint" when ANY of these fire:

- Sean schedules a trip ≥3 days where MBP is leaving the home LAN.
- v3.34.0 retrofit eval validation closes (currently the blocker on `vault_synthesizer` fallback).
- A trip happens and post-trip review shows the catch-up cost exceeded $20 worth of lost productivity (subjective threshold — "I lost a morning to investigating why job_feed had empty days").

### How to log a future trip (Part 1 pattern)

Append a new dated subsection to Part 1, do NOT overwrite the 2026-05-14 entry. Template:

```markdown
### Trip: YYYY-MM-DD → YYYY-MM-DD ({short label})

- Depart: <date> <time> ET
- Return: <date> <time> ET
- MBP location during window: with Sean, off home LAN
- Trip-mode active? yes/no (if yes: which agents, which budgets)
- Expected outcomes: <copy + tailor the table above>
- Post-trip review (filled in after return): <surprises, costs, signal lost>
```
