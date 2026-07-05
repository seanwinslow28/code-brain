# BT5 — Tier-2 model-host reachability: root-cause diagnosis + fix spec

- **Run**: Fable, 2026-07-05, systematic-debugging (code-brain edition, `.claude/skills/systematic-debugging/SKILL.md`)
- **Scope**: diagnosis and spec only. No fixes applied, no state changed. All probes read-only, ≤5s.
- **Pinned symptom**: Vault Synthesizer (02:30 daily) and Knowledge Lint Tier 2 (Sunday 22:00) degrade intermittently because their Tier-2 model host (MacBook Pro serving Qwen-class models) is unreachable; WOL retired; skip-and-continue has papered over the gap.
- **Machine this ran on**: `Seans-MacBook-Pro` — i.e., the Tier-2 host itself. The scheduled agents run on the Mac Mini (no `com.sean.agent.*` plists loaded here; config comment confirms Mac Mini is the always-on driver). That made local power-state and wake-daemon evidence directly inspectable.

---

## Phase 1 — Root Cause Investigation

### Fleet first-check

The skill's Fleet First-Checks table row 3 matches this symptom verbatim ("Overnight MBP-model step fails intermittently … Was the MBP awake? Reachability, not code — WOL retired; agents skip-and-continue by design"). Per the skill, the table accelerates evidence-gathering but never replaces it — and verifying it with real evidence is exactly what overturned half of it: the reachability gap is real, but "skip-and-continue by design" turns out to be false for the synthesizer (it grinds for 45 minutes and mislabels the outcome) and vacuous for lint Tier 2 (the LLM leg was never wired at all).

### What the run records actually show

**Synth manifests (`vault/health/synth-manifest-*.json`, 49 runs on this checkout, 2026-05-02 → 2026-06-23):**

| status | count |
|---|---|
| `partial` | 31 |
| `ok` | 11 |
| `error` | 5 |
| `partial-empty` | 2 |
| `wol-deferred` | **0 — never, in the entire history** |

The 5 `error` runs are the reachability misses. Every one has `model_used: "none"`, `wol_status: ""` (empty — not `"wol_deferred"`), and a duration that is the arithmetic fingerprint of a per-file 90-second poll against a dead host:

| night | weekday | files_processed | duration_s | files × ~91.6s |
|---|---|---|---|---|
| 2026-05-15 | Fri | 23 | 2783.65 | (budget-capped; ~121s/file incl. retrieval) |
| 2026-06-06 | Sat | 30 | 2743.57 | 2748 ✓ |
| 2026-06-07 | Sun | 30 | 2743.70 | 2748 ✓ |
| 2026-06-13 | Sat | 17 | 1557.62 | 1557 ✓ |
| 2026-06-14 | Sun | 24 | 2199.53 | 2198 ✓ |

91.6s/file = the 90s `wake_timeout_s` poll in `route_to_macbook` plus ~1.6s local retrieval overhead. On a down-host night the run does not skip — it polls the dead host once per changed file until the file list or the 2700s budget is exhausted, then reports `status=error`.

Contrast healthy nights: `mbp_awake` + `model_used: qwen3-14b`, e.g. 2026-06-23 (`ok`, 52 files, 45 concepts — the post-miss catch-up) and 2026-06-19/20/21 (`partial` — note 06-20/21 is a *weekend* that succeeded, so the miss pattern is host availability, not weekday). Also note every healthy night is `partial` (budget exhausted): the 45-min window is already saturated at ~5–10 min/file of real inference; there is no slack in the nightly window.

**Lint reports (`vault/health/*-lint-report.md`):** weekly Sundays 2026-05-10 → 2026-06-07, then none (06-14, 06-21 confirmed absent from the 06-21/06-23 vault syncs; later Sundays unverifiable from this checkout — last `vault/health` sync commit is `fc9c195` 2026-06-23). The 2026-06-07 report's 59 "semantic" T2 findings are **all** `source=sql` contradictions + stale-reference regex hits — both Mac-Mini-local. Zero findings have ever come from the MBP LLM leg (see Origin C below: it cannot run).

**Gap note:** the missing 2026-06-11 manifest is a separate, already-ticketed incident (brew python upgrade → launchd codesigning kill of 5 jobs; `vault/00_inbox/tickets.md` "fleet venv durable fix") — excluded from this diagnosis.

### The retirement-and-replacement history (Changed?)

1. **v3.14.0** added a WOL cross-machine path (Mac Mini wakes MBP).
2. **WOL live-verify failed**: macOS Private Wi-Fi Address randomizes the MBP's MAC, so a fixed `wol_mac` never reliably hits the interface (CHANGELOG ~line 1820). WOL to the MBP is *architecturally* unreliable, not mis-tuned.
3. **v3.14.3 (2026-04-18)** retired it: `wol_mac` removed from `[routing.machines.macbook_pro]`, `wol_failure` removed from `[notifications].notify_on`, Mac Mini committed as sole always-on driver. Stated contract: "Every scheduled agent … resolves to a Mac-Mini-resident model or **tolerates a missing MBP gracefully**."
4. **2026-05-15**: a Friday-night miss (the first `error` manifest) is immediately followed by the first `schedule_wakes.sh` run that evening (wake-scheduler log starts 2026-05-15 20:59). **2026-05-22**: `com.sean.agent-fleet-wake-scheduler.plist` installed as a root LaunchDaemon on the MBP (file date May 22 09:17 in `/Library/LaunchDaemons/`). It queues 7 days of `pmset wakeorpoweron` events nightly at 23:30: `02:25 daily` (synth), `07:55/09:25/10:55 Mon–Fri` (job feed), `21:55 Sun` (lint T2), `17:55 Thu` (substack).
5. **2026-05-26**: MBP runtime swapped LM Studio→Ollama :11434; production model is now `qwen3.6_35b-a3b-32k` (the pinned symptom's "Qwen3-14B" is the historical name; the manifest's `model_used: qwen3-14b` is a stale normalization enum, `_normalize_model_name` maps any `qwen*` → `"qwen3-14b"`).

### Wake evidence (from the host itself)

- Wake queue is live now: `pmset -g sched` shows 24 queued `wakeorpoweron` events incl. 02:25 daily and 21:55 today (Sun 07-05).
- The daemon ran on every June failure night and queued the wakes (`/var/log/agent-fleet-wake-scheduler.log`: 06-05 23:42 "queued 24 … through 06-11", 06-06 23:30, 06-13 23:30, 06-14 23:30 — all present).
- The wakes genuinely fire when the machine is home: `pmset -g log` shows `Wake … rtc/HID Activity` or `DarkWake to FullWake` at exactly 02:25:00 on 07-02 (battery), 07-03 (AC), 07-04 (AC), with no re-sleep before 07:00.
- So on the June failure nights the wakes were queued and still nothing was reachable. `agents-sdk/docs/2026-06-05-mbp-away-weekend-fleet-behavior.md` supplies the missing variable for 06-06/07: **the MBP was physically away with Sean** (Fri 06-05 → Sun 06-07). Off-LAN, a local pmset wake is irrelevant — the doc itself says so. 06-13/14 (the very next weekend, same signature) is consistent with the same cause. The pmset log does not reach back to June (starts 2026-06-28), so per-night power state for June is not directly verifiable; the off-LAN doc + queued-wake log is the strongest available evidence, and no observed evidence contradicts it.
- Reachability right now (≤4s probes): MBP Ollama `localhost:11434/api/tags` → 200; `seans-macbook-pro.local:11434` → 200; Mac Mini `192.168.68.200:11434` → 200.

### The prediction-vs-reality mismatch (the buried code defect)

The 2026-06-05 away-weekend doc predicted, for each missed synth night: "`route_to_macbook` polls 90s → **1 Pushover alert** → raises `WOLUnavailable` → caught → **writes `wol-deferred` manifest, `status=deferred`, returns 0**."

Reality (both June weekends): **45-minute runs**, `status=error`, `wol_status=""`, and `notify_wol_failure` invoked **once per changed file** (~30/night, not 1). The designed deferral path exists in `main()` (`vault_synthesizer.py:1373` `except WOLUnavailable`) but is dead code: `run_synthesis` wraps each per-file `llm_caller(prompt)` in `except Exception` (`vault_synthesizer.py:1020-1024`), and `WOLUnavailable ⊂ Exception`, so the exception is swallowed per file, the loop continues to the next file, and each file re-runs the full 90s poll (`_default_llm_caller_factory._call` calls `router.route_to_macbook(task="vault_synthesis", wake_timeout_s=90.0)` **per prompt**, `vault_synthesizer.py:1214-1219`; `hybrid_router.py:369-437` polls to the deadline, fires `notify_wol_failure` at line 434, then raises). Zero `wol-deferred` manifests in 49 runs is the empirical proof.

Two aggravators: `notify_wol_failure` (`lib/pushover.py:116-133`) never consults `[notifications].notify_on` — which removed `wol_failure` in v3.14.3 — so a notification retired by config still fires, per file. And because every per-file call fails, run-level status promotion (`vault_synthesizer.py:1175-1192`, `files_succeeded == 0`) lands on `STATUS_ERROR`, making an environmental miss indistinguishable from a real code failure in the manifest, `record_run`, and everything downstream that reads them.

### The lint Tier-2 leg is not intermittent — it is unreachable

`knowledge_lint.py` `main()` (line 824) calls `run_tier2(cfg.vault_root, soul_context=…, logger=…)` with **no `llm_caller`**; `run_tier2` returns before the LLM block when `llm_caller is None` (lines 552-553). Repo-wide grep: `run_tier2(` has exactly one production call site — that one. So the LLM contradiction scan and `soul-tier-a-conflict` (the Phase-2 feature CLAUDE.md, the module docstring, and the 06-05 doc all describe as "Qwen3-14B on MBP if awake") **have never executed in production, regardless of MBP state**. Two more latent gaps sit behind the missing wiring: `_build_tier2_prompt` (lines 392-406) embeds *no article corpus* — it is instructions + SOUL context only, so even a wired caller would review nothing; and the LLM block's failure handling is `except Exception: pass` (lines 599-600). The launchd plist passes no `--full`, so Tier 2 as a whole is additionally gated on `tier1.total_issues > 0` (currently always true at 405 structural issues).

### Phase 1 Exit Gate — Evidence Blocks

Three origins were traced. (A) is the system-level cause; (B) and (C) are code-level defects that turn (A)'s misses into silent/expensive/mislabeled degradation.

```
EVIDENCE — A (system): the reachability gap itself
- Symptom: Tier-2 LLM work scheduled at fixed instants (02:30 daily; Sun 22:00)
           silently doesn't happen on nights the MBP is unavailable.
           Verbatim record: synth-manifest 2026-06-06/07/13/14 + 2026-05-15 =
           status "error", model_used "none", wol_status "".
- Repro:   Deterministic given the environmental condition: any night the MBP is
           off-LAN / asleep-unwakeable at the fire instant. Reproduced 5× in
           manifests; 2026-06-06/07 documented in advance as an away-weekend
           (agents-sdk/docs/2026-06-05-mbp-away-weekend-fleet-behavior.md).
           Weekend correlation is incidental (06-20/21 weekend succeeded;
           05-15 was a Friday) — the variable is host availability.
- Origin:  Architecture: fixed-instant launchd scheduling (Mac Mini,
           com.sean.agent.vault-synthesizer.plist 02:30; …knowledge-lint.plist
           Sun 22:00) against an opportunistically-available host
           ([routing.machines.macbook_pro] always_on=false, a laptop that
           travels), with no component owning the contract "Tier-2 work
           completes within an availability window." The pmset wake-scheduler
           (installed 2026-05-22) restores availability only in the at-home
           case and has no verification or feedback loop; off-LAN it is
           explicitly irrelevant. Remote wake is architecturally impossible
           (v3.14.3: Private Wi-Fi Address MAC randomization).
- Owner:   Fleet scheduling/routing layer (agents-sdk/schedules/* +
           lib/hybrid_router.py + config.toml [routing]) — no single agent.
- Changed: v3.14.3 (2026-04-18) retired WOL and re-scoped the contract to
           "tolerates a missing MBP gracefully"; the wake-scheduler
           (2026-05-22) partially compensated; the 2026-05-26 LM Studio→Ollama
           swap changed the endpoint but not the availability model.
```

```
EVIDENCE — B (code): synthesizer's dead deferral path
- Symptom: On down-host nights: 45-min runs (duration ≈ files × 91.6s),
           status "error" (not "wol-deferred"), wol_status "" (not
           "wol_deferred"), notify_wol_failure fired ~once per file (~30/night
           vs the documented expectation of 1/run). 0 of 49 manifests ever
           carry the designed "wol-deferred" status.
- Repro:   Every down-host run (5/5 manifests match the signature exactly).
- Origin:  agents-sdk/agents/vault_synthesizer.py:1020-1024 — per-file
           `except Exception` around `llm_caller(prompt)` swallows
           WOLUnavailable, so main()'s `except WOLUnavailable`
           (vault_synthesizer.py:1373) never fires; compounded by
           per-prompt routing (vault_synthesizer.py:1214-1219 re-runs
           route_to_macbook's 90s poll for every file) and by
           lib/pushover.py:116-133 ignoring [notifications].notify_on.
- Owner:   vault_synthesizer.py (run_synthesis + _default_llm_caller_factory);
           lib/hybrid_router.py route_to_macbook (notify placement);
           lib/pushover.py (config bypass).
- Changed: Phase D (v3.20.0) added the wol-deferred manifest path at main()
           level while the LLM call lived inside the per-file loop — the
           handler was dead on arrival ("none found" for a breaking commit:
           the mismatch is original to the design, not a regression).
```

```
EVIDENCE — C (code): lint Tier-2 LLM leg never wired
- Symptom: No lint report has ever contained an LLM-sourced contradiction or
           any soul-tier-a-conflict finding (2026-06-07 report: all T2 lines
           are source=sql or stale-reference regex). CLAUDE.md + docs describe
           an MBP Qwen dependency for lint Tier 2 that never actually runs.
- Repro:   Structural — every production run. run_tier2 returns at
           knowledge_lint.py:552-553 because llm_caller is None.
- Origin:  agents-sdk/agents/knowledge_lint.py:824 — main() constructs no
           llm_caller (sole production call site, confirmed by grep). Latent
           behind it: _build_tier2_prompt (392-406) embeds no article corpus,
           and the LLM block is `except Exception: pass` (599-600).
- Owner:   knowledge_lint.py main() + _build_tier2_prompt.
- Changed: None found — the llm_caller parameter shipped test-only from the
           start; production wiring was never added.
```

---

## Phase 2 — Pattern Analysis

The fleet has already solved "scheduled work against an intermittently-available host" twice, deliberately. The broken agents differ from the working patterns on every load-bearing dimension:

| Dimension | job_feed (working) | tier_c_batch route (working) | vault_synthesizer (broken) | knowledge_lint T2-LLM (broken) |
|---|---|---|---|---|
| Availability model | 7 fires across 8:00–11:00 window; wake-scheduler queues 07:55/09:25/10:55 wakes to raise hit rate | Pattern-E documented window (7am–5pm manual wake); consumers defer to next window | Single fixed instant 02:30 (wake at 02:25 helps only at-home case) | Single fixed instant Sun 22:00 |
| Host check | Explicit pre-probe, once per run: `_probe_mbp`, 2s timeout (job_feed.py:55-56,111) | Health-check inside route(); `fallback="none"` raises `RouteUnavailable` **before any side effect** (hybrid_router.py:326-330) | 90s poll **per file**, re-entered up to N times per run | None (leg unreachable) |
| On miss | LLM leg skipped this fire; postings persist unscored (`fit_score=NULL`), carried over; `complete` flag records truth (job_feed.py:167-168) | Caller catches RouteUnavailable, defers; "healthy idle outcome, not an error" | Grinds 45 min, labels run `error`, ~N pushes | Silent absence, `except: pass` |
| Cost integrity | `fallback_disabled=true` — never cloud | `fallback="none"` — never cloud, never dead WoL | route_to_macbook never falls back (good) but wastes the whole budget | n/a |
| Truthful record | `mbp_up` in report + `complete` flag | RouteUnavailable is a distinct, typed outcome | `error` conflates environment with code failure; `wol-deferred` enum exists but unreachable | Report can't distinguish "no semantic issues" from "scan never ran" |

Also relevant: `financial_analysis` was **re-routed to the Mac Mini** in v3.14.3 precisely because "qwen3-14b @ MBP would fail whenever MBP sleeps" — the third pattern (move work to the always-on host) was applied per-task where a Mac-Mini-class model sufficed. It was *not* applied to vault_synthesis/lint-T2 because those need MBP-class capacity — a deliberate quality decision, which is why the availability problem persists for exactly these two.

**Exit gate — difference list:** the broken pair (1) fire once at an instant instead of converging over a window, (2) probe per-file mid-work (or never) instead of once up-front, (3) burn budget on a known-down host instead of failing fast pre-side-effect, (4) record the miss as `error`/nothing instead of a typed deferral, (5) notify per-file against retired config instead of once-or-never, (6) (lint only) the dependent leg was never wired at all.

---

## Phase 3 — Hypothesis and Testing

**Hypothesis (names Origin A):** Fixed-instant scheduling against the opportunistically-available MBP (Origin A) produces the intermittent, silent Tier-2 degradation (Symptom A) because no component owns completion-within-a-window: when the instant misses the availability window, the only behaviors available are the consumers' own degradation paths, and those paths are defective (Origins B, C) — expensive, mislabeled, or structurally absent.

Read-only tests run against the hypothesis (no state changed):

| # | Test | Prediction if hypothesis true | Result |
|---|---|---|---|
| 1 | Duration arithmetic on all 5 `error` manifests | duration ≈ files × (90s poll + ε) | ✓ 91.6s/file exact on all 4 June nights |
| 2 | Grep 49 manifests for `wol-deferred` | 0 hits (B: dead path) | ✓ 0 hits |
| 3 | Wake-scheduler log on failure nights | wakes queued yet miss happened (wake ≠ reachable) | ✓ queued 06-05/06/13/14 |
| 4 | pmset -g log at 02:25 recent nights | RTC wakes fire when home | ✓ FullWake 07-02/03/04 |
| 5 | Away-weekend doc vs 06-06/07 manifests | doc predicts `wol-deferred`+1 page; manifests show `error`+45min | ✓ mismatch confirmed (B) |
| 6 | Weekend-only counter-check | if availability (not weekday) drives it, some weekends succeed | ✓ 06-20/21 weekend `partial`/`mbp_awake`; 05-15 Friday missed |
| 7 | grep `run_tier2(` production call sites | exactly one, no llm_caller (C) | ✓ knowledge_lint.py:824 only |
| 8 | 2026-06-07 lint report T2 provenance | all findings sql/regex, none LLM | ✓ 59/59 |
| 9 | Live probes (all three endpoints, ≤4s) | reachable now (MBP awake) → gap is availability-timing, not config/DNS | ✓ all 200; mDNS name resolves |

No competing hypothesis survives: "wake-scheduler not installed" — refuted (installed 05-22, root:wheel, log current). "Wakes not queued on failure nights" — refuted (log). "Wrong host/port after the Ollama swap" — refuted (probes 200 on the exact configured mDNS name+port; healthy manifests post-05-26 exist). "Code error in the LLM call path" — refuted (healthy nights produce articles; error nights never reach an LLM). "launchd/codesigning kill" — separate incident, different signature (no manifest at all vs error manifest), already ticketed.

**Exit gate:** hypothesis confirmed. This is the skill's §"When Investigation Reveals No Single Code Root Cause" *pattern* — an environmental availability condition — **but not its conclusion**: the investigation completed and found that the environmental condition was already known and accepted, while the actual defects are (a) an unowned completion contract and (b) two broken degradation paths. Those are code/design, and fixable.

---

## Root cause (symptom vs cause, explicit)

**Symptom** (what the owner sees): two scheduled agents intermittently "succeed" with their Tier-2 model work silently skipped; on bad nights the synthesizer's manifest says `error`, and lint's semantic scan yields nothing — correlated with whether the MBP happened to be awake.

**Root cause** (where the behavior is born): **the fleet schedules Tier-2 LLM work at fixed wall-clock instants against a host whose availability is opportunistic, and no component owns the contract "this work completes within an availability window, and a miss is a cheap, typed, visible outcome."** After WOL's architecturally-forced retirement (Private Wi-Fi MAC randomization, v3.14.3), host availability became best-effort (pmset self-wakes cover only the at-home case, with no verification loop and nothing addressing off-LAN travel). Each consumer was left to improvise a degradation path, and both improvisations are defective:

- **Synthesizer (Origin B)**: the designed typed-deferral path (`WOLUnavailable` → `wol-deferred` manifest → 1 notification → exit 0) is dead code — the per-file `except Exception` swallows it — so a miss instead costs the full 45-minute budget (90s poll × every changed file), fires a retired-by-config notification per file, and is recorded as `status=error`, indistinguishable from a real failure. 0/49 manifests ever said `wol-deferred`; 5/5 misses said `error`.
- **Lint Tier 2 (Origin C)**: the MBP-dependent LLM leg was never wired into production (`main()` passes no `llm_caller`), its prompt contains no corpus to review, and its error path is `except: pass`. Its degradation isn't intermittent — it is total and permanent, masked by the sql/regex findings that share the "T2" label.

The pinned symptom statement therefore needs two corrections which are themselves findings: lint Tier 2 does not "call Qwen3-14B when the MBP is awake" (it never calls anything), and "skip-and-continue" flatters the synthesizer (it poll-grinds and mislabels). Also cosmetic-but-misleading: since 2026-05-26 the Tier-2 model is `qwen3.6_35b-a3b-32k` (Ollama :11434), and the manifest's `model_used: "qwen3-14b"` is a stale normalization enum.

---

## Fix spec (intent-carrying; for a weaker implementing model)

> **Status: SPEC ONLY. Do not implement without separate authorization.**
> Every change below opens by citing the Origin it fixes, per the skill's Phase-4 rule. Follow `verification-loops` (failing test first) and run `verification-before-completion` before claiming done.

### Objective

When the Tier-2 host is unavailable, a scheduled Tier-2 run must **fail fast (≤ ~2 min), record a typed deferral truthfully, notify at most once, and leave the work queued for the next opportunity** — and lint's Tier-2 LLM leg must actually exist so "MBP awake" can matter for it at all. When the host **is** available, behavior must be byte-for-byte what it is today. The environmental fact that a traveling laptop is sometimes off-LAN is **accepted, not fought**: no wake mechanism can fix off-LAN, so the design goal is convergence-over-window plus honest misses, at $0.

### Non-goals / what NOT to change (hard constraints)

1. **No paid-API fallback** for `vault_synthesis`, `heavy_synthesis`, `job_scoring`, or the new lint route. The $0 cost-integrity contract is deliberate and repeatedly reaffirmed (`fallback_disabled=true`, `fallback="none"`, RouteUnavailable docstring). A miss must never bill Anthropic.
2. **Do not resurrect WOL for the MBP.** Retired for an architectural reason (Private Wi-Fi Address MAC randomization) that still holds. Leave `send_wol`, its tests, and the Alienware WOL path alone.
3. **Do not move `vault_synthesis`/lint-T2 to Mac Mini or Alienware models.** Mac Mini hosts sub-Tier-2 models (quality decision made per-task in v3.14.3, e.g. `financial_analysis` — a per-task call, not a blanket one); Alienware is Pattern-E offline overnight.
4. **Do not change** the synthesizer's validation/depth-gate semantics, retrieval tiers, prompt, budget default, the ≥2-wikilink invariant, index regeneration, FileLock usage, atomic tmp-then-rename manifest writes, or the "persist indexer state only on ok/partial" rule (that rule IS the implicit retry queue — on a deferral the state must continue not to advance).
5. **Do not change** lint Tier 1 checks, the report format's severity buckets, exclusion dirs, or the SQL fast path / dedupe rule.
6. **Keep exit code 0** on environmental deferral (launchd semantics; matches current design intent).
7. **No new auto-commit mechanisms, no cron/launchd additions on the vault-commit path** (CLAUDE.md rule 8); do not re-enable the 6 disabled agents (AUDIT-2026-04-09); do not touch the wake-scheduler's job-feed/substack wake entries.
8. **Do not remove the wake-scheduler.** It demonstrably works for the at-home case (pmset log: FullWake at 02:25) and job_feed depends on its morning wakes.

### Changes

**C1 — Synthesizer: route once per run, fail fast, resurrect the typed deferral. (Fixes Origin B; mitigates A's cost.)**
In `agents-sdk/agents/vault_synthesizer.py`: resolve the routing decision **once per run, before the per-file loop** — not per prompt. Concretely: in `main()` (or at the top of the LLM phase), perform a single bounded reachability/route resolution (reuse `route_to_macbook(task="vault_synthesis", wake_timeout_s=90.0)` — one 90s window total per run, aligned with the 02:25 pmset wake). On `WOLUnavailable`: take the **existing** deferral path (write `wol-deferred` manifest via the existing `except WOLUnavailable` block, `record_run status="deferred"`, exit 0). The per-file `llm_caller` then reuses the already-resolved decision (pass the `RoutingDecision` into the caller factory; keep the HTTP call per file). Result: down-host run cost drops from ~2700s to ≤~95s, one manifest, correct status, indexer state untouched (work re-queues automatically — this already works: see 06-23 catch-up, 52 files/45 concepts).
*Also required:* a mid-run host-loss circuit breaker — if K=2 consecutive per-file LLM calls fail with connection-class errors, re-probe once (≤5s); if down, stop the loop and finish with the existing `partial`/`partial-empty` promotion plus a `warnings` entry `"host lost mid-run after N files"`. Do NOT re-enter a 90s poll per remaining file.
*Keep*: `WOLUnavailable ⊂ Exception` per-file catch may remain for other exception types, but `WOLUnavailable` must be either impossible there (decision pre-resolved) or re-raised distinctly — never counted as an ordinary per-file failure.

**C2 — Notification honesty: at most one per run, and respect config. (Fixes Origin B's page-storm; closes the v3.14.3 config bypass.)**
`notify_wol_failure` currently fires inside `route_to_macbook` per invocation and ignores `[notifications].notify_on` (which removed `wol_failure` in v3.14.3). Move the notify decision to the caller (agent level, once per run) **or** gate `notify_wol_failure` on the config list; either way the invariant is: **≤1 notification per scheduled run for host-unreachable**, and whether it sends at all is controlled by `notify_on` (add a `host_unreachable` event name to config if Sean wants the single page; otherwise it stays silent and the manifest + morning brief carry the signal). Do not touch `notify_agent_error` / `notify_gate_check_fail` / job-feed push paths.

**C3 — Lint: wire the Tier-2 LLM leg for real. (Fixes Origin C.)**
In `agents-sdk/agents/knowledge_lint.py` `main()`: construct a production `llm_caller` using the same probe-first routing as C1 (add a dedicated task_map key `lint_tier2 = { model = "qwen3.6_35b-a3b-32k", machine = "macbook_pro" }` in `config.toml` rather than borrowing `vault_synthesis`, so per-task routing stays observable; same model, same host). Three sub-requirements a naive implementation will miss:
   - **Corpus injection**: `_build_tier2_prompt` currently contains *no article content*. The caller must supply the material to review — inject `knowledge/concepts/*.md` bodies (or title+Definition sections) in token-budgeted batches sized for the 32K-context variant; multiple LLM calls per run are acceptable within a bounded Tier-2 time budget (~15 min per the module docstring). Without this, C3 ships a scan that reviews nothing.
   - **Honest deferral**: if the host probe fails, the report must say so — add a line in the report body (e.g. `_Tier-2 LLM scan: deferred (host unreachable)._`) and a log/record_run note, instead of silence. Similarly distinguish "Tier 2 skipped by gate (tier1 clean, no --full)" from "ran without LLM" in the report footer.
   - **Kill the silent catch**: replace the LLM block's `except Exception: pass` with a logged warning plus the same report line ("Tier-2 LLM scan: failed — <exc class>"), so scan failures stop masquerading as clean scans.
   Preserve: the SQL-vs-LLM dedupe rule, SOUL context assembly, severity mapping, and the existing JSON response contract.

**C4 — Manifest/status truthfulness. (Fixes A's observability; prevents B's mislabeling from recurring.)**
Keep the existing `wol-deferred` enum value for continuity (consumers and Phase-D changelog already know it; renaming is out of scope). Reserve `error` for genuine code/LLM failures — after C1, a down-host night must produce `wol-deferred`, never `error` with `model_used="none"`. Add to the synth manifest: `host_probe: "ok" | "unreachable" | "lost-mid-run"` and probe latency. Verify (read, don't redesign) that manifest consumers — `lib/fleet_summary.py`, meta-agent, substack_drafter's `synthesizer_dry_threshold`, daily-driver brief — handle `wol-deferred` sanely; the substack drafter's "last N manifests had concepts_written == 0" no-op check should treat deferral nights as non-dry (deferrals are not evidence the synthesizer is dry). Optional cosmetic (separate commit): extend `MODEL_USED_VALUES`/`_normalize_model_name` so `qwen3.6_35b-a3b-32k` stops reporting as `qwen3-14b`.

**C5 (optional, Phase 2) — Widen the window instead of praying at the instant. (Mitigates A directly.)**
Only after C1–C4 are verified: add **one** catch-up fire for the synthesizer (e.g. 09:30, after the 07:55 job-feed wake window when the MBP is typically awake/in use) gated on "today's manifest says `wol-deferred`", with a reduced `--budget-seconds` (e.g. 1200) so it can't collide with the interactive day; and for lint, a Monday-morning catch-up under the same gate pattern. Same-day manifest collision: the catch-up run must suffix its manifest (follow vault_critic's `-manual-HHMMSS` precedent), and only the consumer-facing "latest" resolution may prefer the richer run. This is optional because C1's cheap-miss + the existing implicit re-queue already converge within days; take it only if the owner wants same-day convergence.
*(Alternative considered and rejected: an MBP-side `caffeinate` hold after the 02:25 wake. July pmset evidence shows the machine already stays up after RTC wakes at home, and the documented misses were off-LAN, where no amount of staying awake helps. Revisit only if post-C4 manifests ever show `host_probe: unreachable` while the pmset log proves the machine was awake at home.)*

### Done criteria (all verifiable, evidence before assertion)

1. **Failing tests first** (per `verification-loops`): a test that stubs an unreachable host and asserts today's broken behavior (45-min-shaped loop / swallowed `WOLUnavailable` / `status=error`) fails after the fix in the right direction — i.e., new asserts: run completes < 3 min sim-time, manifest `status="wol-deferred"`, `wol_status="wol_deferred"`, indexer state file NOT rewritten, ≤1 notify call recorded.
2. Down-host simulation (point `macbook_pro.host` at a black-hole IP or stub `check_health`): synthesizer exits 0 in ≤ ~2 min wall, writes exactly one `wol-deferred` manifest, `record_run status="deferred"`, zero or one notification depending on `notify_on`.
3. Up-host run: byte-identical behavior to today on the happy path (manifest fields other than the new `host_probe` unchanged; existing tests green — the 2 pre-existing WOL test orphans in `tests/test_route_to_macbook.py` may stay red as documented in CHANGELOG v3.29.x).
4. Mid-run loss simulation: after K=2 connection failures + failed re-probe, loop stops; status is `partial`/`partial-empty` with the `host lost mid-run` warning; remaining files did NOT each burn a 90s poll.
5. Lint with host up (`--full` or seeded tier1 issue): report contains an LLM-tier section whose findings can only come from the wired caller (use the synthetic-vault contradiction pair as the fixture); `soul-tier-a-conflict` reachable end-to-end at least in the harness. With host down: report contains the explicit deferral line. With the LLM erroring: report contains the failure line — `grep -c "Tier-2 LLM" report` ≥ 1 in all three cases.
6. **Extinction check on live fleet** (the real-world acceptance): after ≥1 week of nightly runs, `python3 -c` histogram over new manifests shows zero instances of the old miss signature (`status=error` + `model_used=none`); any misses present as `wol-deferred` with `duration_seconds < 180`.
7. `python3 scripts/validate.py` passes; CHANGELOG entry added; the CLAUDE.md agents-table line for synthesizer/lint updated to describe the new deferral semantics (it currently asserts "skip-and-continue", which this diagnosis falsified).

### Edge cases the implementer must handle

- **No changed files + host down**: don't mark `wol-deferred` — there was no Tier-2 work to defer; keep today's early-return (`ok`, index regen only). Probe only when there is work.
- **Host up at probe, Ollama model not pulled** (`/api/tags` lists tags — the route decision doesn't verify the specific model): first real call 404s. That is an `error`-class outcome (real failure), not a deferral — but the circuit breaker must still stop the loop after K repeats.
- **mDNS quirks**: `seans-macbook-pro.local` resolution failure, TCP refusal, and timeout are all "unreachable" for the probe; log which one (they discriminate off-LAN vs awake-but-Ollama-down for future diagnosis).
- **Probe race with the 02:25 wake**: agent fires 02:30:05; keep the single 90s poll window (not a bare one-shot 3s check) so a slow wake/Wi-Fi reassociation doesn't produce a false miss. Never shrink the wake→fire gap below 5 min if schedules move.
- **DST / clock skew**: launchd `StartCalendarInterval` and pmset both use local wall time — a schedule change must move wake and fire together.
- **Concurrent runs** (nightly + optional C5 catch-up, or a manual run): FileLock already serializes writes; manifests must not clobber (suffix rule in C5); `record_run` CSV appends are already per-machine.
- **Pushover creds missing**: `ensure_credentials_or_raise` already fails loud at startup — keep; C2 must not reintroduce a silent-notify path.
- **Lint gate interplay**: Tier 2 only runs when `tier1.total_issues > 0` or `--full`; today tier1 is never 0 (405 issues), but if it ever goes clean the report must say Tier 2 was gate-skipped rather than implying a clean semantic scan.
- **Old-schema manifests** (pre-2026-05-13, e.g. 05-02…05-11) lack `model_used`/`wol_status`; any consumer/histogram code must tolerate missing keys.

### Rollout order

C1+C2 together (one PR: routing hoist + breaker + notify gate + tests) → C4 (manifest field + consumer verification) → C3 (lint wiring, its own PR — largest surface, includes prompt-corpus design) → observe one real week (done-criterion 6) → decide C5 with the owner.

---

## Phase 4 — Implementation

**Not entered.** Per the task pin: diagnosis and spec only; implementation requires separate authorization. The spec above carries the Phase-4 obligations forward (each change cites its Origin; failing-test-first; `verification-before-completion` before any "done" claim).

---

## Appendix — Evidence read

Repo files (read in full unless noted):

1. `.claude/skills/systematic-debugging/SKILL.md` — the method followed
2. `agents-sdk/agents/vault_synthesizer.py` (pinned)
3. `agents-sdk/agents/knowledge_lint.py` (pinned)
4. `agents-sdk/lib/hybrid_router.py` (pinned)
5. `agents-sdk/config.toml` (pinned)
6. `agents-sdk/schedules/install_schedules.sh`
7. `agents-sdk/lib/pushover.py`
8. `agents-sdk/schedules/com.sean.agent-fleet-wake-scheduler.plist`
9. `agents-sdk/schedules/com.sean.agent.vault-synthesizer.plist`
10. `agents-sdk/schedules/com.sean.agent.knowledge-lint.plist`
11. `agents-sdk/scripts/schedule_wakes.sh`
12. `agents-sdk/docs/2026-06-05-mbp-away-weekend-fleet-behavior.md` — the away-weekend prediction doc
13. `agents-sdk/agents/flush.py` (lines 205–280 — `_default_llm_caller` routing comparison)
14. `agents-sdk/agents/job_feed.py` (grep excerpts — probe-first pattern, lines 55–56, 111, 148–168, 217–286)
15. `agents-sdk/lib/fleet_summary.py` (grep excerpt — status badge handling)
16. `agents-sdk/agents/meta_agent.py` (grep excerpt — ACTIVE_AGENTS, synth display row)
17. `CHANGELOG.md` (grep excerpts — v3.14.0/v3.14.3 WOL history lines ~1717–1820, Phase-D manifest lines ~1279–1287, WOL test-orphan notes)
18. `vault/health/synth-manifest-*.json` — all 49 files field-extracted; ~25 individually inspected (2026-05-02…2026-06-23)
19. `vault/health/` directory listing (manifest + lint-report inventory)
20. `vault/health/2026-06-07-lint-report.md` (head + T2 provenance count)
21. `vault/90_system/agent-logs/` listing + `agent-run-history.csv` (full)
22. `vault/00_inbox/tickets.md` (`## Todo` section — codesigning incident ticket; no existing ticket for this problem)
23. `CLAUDE.md` (project instructions, in-context) + auto-memory `MEMORY.md` (machine-identity note)

System/host evidence (read-only, ≤5s each):

24. `scutil --get LocalHostName` → `Seans-MacBook-Pro` (this machine = the Tier-2 host)
25. `ls ~/Library/LaunchAgents` + `launchctl list | grep com.sean` → no agent plists loaded here (agents run on Mac Mini)
26. `ls /Library/LaunchDaemons | grep sean` → wake-scheduler installed root:wheel, dated 2026-05-22
27. `pmset -g sched` → 24 queued wakes (02:25 daily, 21:55 Sun, 07:55/09:25/10:55 weekdays, 17:55 Thu)
28. `pmset -g custom` → sleep 5 / standby 1 / hibernatemode 3 / womp 1 (both power sources)
29. `/var/log/agent-fleet-wake-scheduler.log` (head, tail, June greps) — first run 2026-05-15 20:59; 55 runs; queued on all June failure nights
30. `pmset -g log` (filtered) — RTC wakes fired 02:25 on 07-02/03/04; log retention starts 2026-06-28
31. `curl -m 4` probes: `localhost:11434/api/tags` ✓, `seans-macbook-pro.local:11434/api/tags` ✓, `192.168.68.200:11434/api/tags` ✓
32. `git log -- vault/health` (sync freshness: last 2026-06-23 `fc9c195`) + `git log -1 HEAD`
33. Weekday computation for manifest dates (python `datetime`)
34. Repo greps: `llm_caller` (production call sites), `run_tier2(`, `wol|pmset|schedule_wakes` in CHANGELOG/docs, `mbp|probe|fallback` in job_feed/flush

Isolation honored: `docs/plans/wwf5d/baselines/` and `docs/plans/wwf5d/fable-runs/` were not read; `docs/plans/wwf5d/fable-session-driver.md` was not read.
