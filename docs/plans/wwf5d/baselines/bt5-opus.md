# BT5 — Systematic-Debugging Baseline: Tier-2 MBP Reachability Degradation

**Model:** Opus 4.8 (1M) · **Method:** `.claude/skills/systematic-debugging/SKILL.md` (code-brain four-phase edition) · **Mode:** diagnosis + fix spec only — no code changed, no state touched.

**Pinned symptom:** Vault Synthesizer (02:30 daily) and Knowledge Lint Tier 2 (Sun 22:00) degrade intermittently because their Tier-2 model host (Qwen served from the MacBook Pro) is unreachable; runs "succeed" with Tier-2 work silently skipped. WOL was retired as a fix path. Owner wants root cause + intent-carrying fix spec, not another patch.

---

## Phase 1 — Root Cause Investigation

### Fleet First-Check consulted (skill step 0)

The matching row in the skill's Fleet First-Checks table: *"Overnight MBP-model step fails intermittently (synthesizer, lint Tier 2, flush ≥100-msg) → Was the MBP awake? Reachability, not code — WOL retired; agents skip-and-continue by design."* **The task explicitly asks me to test this framing rather than accept it** ("skip-and-continue has papered over the gap"). I used the row to accelerate, then verified against code + manifests + a live probe — and the row's "reachability, not code / by design" verdict does **not** survive that verification. See below.

### What I traced (boundary instrumentation, per skill step 4)

I instrumented the two agents at each component boundary: dispatch (launchd plist) → agent process (Mac Mini) → routing decision (`hybrid_router`) → LLM sub-call (MBP over LAN) → result recording (manifest / `record_run`) → surfacing (`meta_agent`). Findings by boundary:

**Dispatch & host model.** Both agents' launchd plists run the agent *process* on the always-on host; the agent then reaches the MBP *over the LAN* only for the Tier-2 LLM call. The MBP is `always_on = false`, `runtime = "ollama"`, host `seans-macbook-pro.local:11434` (`config.toml:305–333`). A wake mechanism **does** exist and is not WOL: `schedule_wakes.sh` (root LaunchDaemon `com.sean.agent-fleet-wake-scheduler`, nightly 23:30) queues `pmset schedule wakeorpoweron` events at **02:25 daily** (for the 02:30 synth) and **Sun 21:55** (for the 22:00 lint) — `schedule_wakes.sh:23–30`. So the retired WOL magic-packet was **replaced** by a pmset RTC self-wake. The owner's "WOL retired, nothing wakes it" is half the picture — the live wake path is pmset self-wake, and it is *unreliable*, not *absent*.

**Synthesizer LLM call.** `run_synthesis` calls `llm_caller(prompt)` per changed file inside `try: … except Exception: continue` (`vault_synthesizer.py:1020–1024`). `llm_caller` is `_call` (`:1214–1219`), which runs `route_to_macbook(task="vault_synthesis", wake_timeout_s=90.0)`. When the MBP is asleep, `route_to_macbook` sends no packet (`wol_mac` empty), polls health to the 90 s deadline, fires `notify_wol_failure`, and raises `WOLUnavailable` (`hybrid_router.py:400–437`). `WOLUnavailable` subclasses `Exception` (`:33`), so the **per-file `except Exception` swallows it** and `continue`s. It therefore **never reaches** `main()`'s `except WOLUnavailable` handler (`:1373–1390`) that was purpose-built to write a clean `status="wol-deferred"` manifest and return. That handler is **dead code** on the production path. With every per-file call swallowed, `files_succeeded == 0` → status is promoted to `STATUS_ERROR` (`:1179–1181`).

**Knowledge Lint LLM call.** `main()` calls `run_tier2(cfg.vault_root, soul_context=…, logger=…)` **with no `llm_caller`** (`knowledge_lint.py:824–828`). `run_tier2` therefore hits `if llm_caller is None: return issues` (`:552`) after only the local staleness-regex scan and the SQL `concept_edges` fast-path. The MBP/Qwen semantic pass — LLM contradiction discovery, SOT drift, and `soul-tier-a-conflict` (`:558–598`) — **is never invoked in production, awake or asleep**. `route_to_macbook` does not appear anywhere in `knowledge_lint.py` except the docstring (`:10`). `build_soul_context` runs and its output is discarded. `main()` then calls `record_run(status="success")` unconditionally (`:843–845`).

### Reproduction / evidence (skill step 2 — gather data when not locally reproducible)

I cannot make the MBP fall asleep from here, so I gathered the historical record instead:

- **Synth manifest history, 30 runs (2026-05-23 → 06-23):** 4 nights are `status=error, model_used=none, wol_status=""` — **2026-06-06, 06-07, 06-13, 06-14**. Every other night is `ok`/`partial` with `model=qwen3-14b, wol=mbp_awake`. So ~13% full misses. **No manifest is ever `status=wol-deferred`** — empirical proof the graceful path is dead.
- **The error-night manifest is the smoking gun.** `synth-manifest-2026-06-14.json`: `run_id 2026-06-14T02:30:06` (the real 02:30 fire), `files_processed 24`, `duration_seconds 2199.53` (**~37 minutes**), `model_used none`, `status error`. 24 files × ~90 s/file poll ≈ 2160 s ≈ the observed 2199 s. This confirms every file re-polls the asleep host for the full timeout — the "skip-and-continue" turns one reachability miss into a 37-minute poll storm and (via `notify_wol_failure` per call) up to **24 Pushover pages**.
- **Weekend correlation (decisive on the *why*):** all 4 error nights are Sat/Sun (two consecutive weekends); every healthy night sampled is a weekday. The MBP is away / lid-closed / unplugged on weekends — a condition pmset self-wake **cannot** fix (off-LAN wake is meaningless; battery + closed lid suppresses scheduled wakes). Corroborated by `agents-sdk/docs/2026-06-05-mbp-away-weekend-fleet-behavior.md`.
- **Lint reports, all 8 on disk (2026-04-18 → 06-07):** `grep` for `source=llm` → **0**; for `soul-tier-a-conflict` → **0 ever**. Every contradiction line is `source=sql`. Empirical proof the LLM/MBP Tier-2 leg has never produced a single finding in production.
- **Live reachability probe (≤5 s, permitted):** Mac Mini `192.168.68.200:11434` → HTTP 200 in 32 ms (always-on host healthy). MBP `seans-macbook-pro.local` resolves to **127.0.0.1** on this checkout (I am on the MBP itself) and answers 200 — a repro gotcha: any manual synth run *on the MBP* always sees the target reachable and cannot reproduce the production gap (the Mac Mini resolves the same name to the LAN IP).

### Phase 1 Exit Gate — Evidence Block

```
EVIDENCE
- Symptom: Two overnight agents' Tier-2 work degrades intermittently. Refined by
           evidence into TWO distinct, differently-shaped symptoms:
           (a) Synthesizer: on ~13% of nights (weekend-clustered) it burns ~37 min
               (2199s/24 files) polling an asleep MBP, pages up to 24x, and records
               status=error/model=none — NOT the clean "wol-deferred" its own docs
               and code claim. Zero knowledge produced that night.
           (b) Knowledge Lint: its MBP/Qwen "Tier 2 semantic pass" (LLM contradictions,
               SOT drift, soul-tier-a-conflict) has NEVER run in production — record_run
               is hardcoded status="success". Truly silent; not reachability-gated.
- Repro:   Not locally reproducible (cannot sleep the MBP from here; on-MBP the target
           name resolves to 127.0.0.1 and always answers). Reproduced from the record:
           synth-manifest-2026-06-{06,07,13,14}.json = error/none/2199s; all 8 lint
           reports have 0 source=llm & 0 soul-tier-a-conflict. Live probe: Mac Mini
           healthy (200/32ms); MBP 200 only because loopback on this host.
- Origin:  ARCHITECTURAL ROOT: Tier-2 work is statically bound in config.toml [routing]
           to macbook_pro (always_on=false), whose only wake path is best-effort pmset
           self-wake (schedule_wakes.sh 02:25/Sun-21:55) with power/lid/on-LAN
           preconditions that fail on a meaningful fraction of nights; the dispatch
           schedule is uncorrelated with when those hold. This surfaces through TWO
           code origins that fail to handle the miss in an intent-preserving way:
           * Origin 1 (synth): vault_synthesizer.py:1020-1024 — per-file `except
             Exception: continue` swallows WOLUnavailable, so the graceful
             wol-deferred handler at main():1373-1390 is DEAD CODE; the run instead
             re-polls 90s/file (route_to_macbook, hybrid_router.py:400-437) and lands
             STATUS_ERROR (:1179-1181).
           * Origin 2 (lint): knowledge_lint.py:824 calls run_tier2 WITHOUT an
             llm_caller, so the MBP pass is skipped at :552 unconditionally; born this
             way at commit 6ad8ce3; record_run status hardcoded "success" (:843-845).
- Owner:   Origin 1 → agents-sdk/agents/vault_synthesizer.py (run_synthesis vs main
           exception boundary) + lib/hybrid_router.py::route_to_macbook contract.
           Origin 2 → agents-sdk/agents/knowledge_lint.py::main (builds no router).
           Architectural → config.toml [routing] task_map binding + schedule_wakes.sh
           reliance on pmset self-wake.
- Changed: Origin 2 was NEVER wired (born broken, commit 6ad8ce3 introduced both
           run_tier2 and its llm_caller-less call site). Origin 1: WOL magic-packet
           retired v3.14.3 (2026-04-18, config.toml:305-311) and replaced by pmset
           self-wake; the synth's error handling was never updated to the clean
           deferral the retirement assumed, and the runtime swap to Ollama
           qwen3.6 (2026-05-26) left route_to_macbook's MBP-only contract intact.
```

All five fields are filled from observed evidence. Phase 1 is complete.

---

## Phase 2 — Pattern Analysis

**Working example in the same codebase (the correct pattern).** The fleet has already solved "reachability-sensitive scheduled work" twice, the right way — by **relocating the task off the MBP to the always-on Mac Mini**:

- `inbox_triage` and `financial_analysis` were moved to the Mac Mini precisely because "qwen3-14b @ MBP would fail whenever MBP sleeps" (`config.toml:355–366`). They accept a smaller model that scored acceptably on the golden set rather than depending on an intermittent host.
- The **Tier C batch route** (`tier_c_batch_summarize`, `config.toml:389–403`) is the reference pattern for work that *must* stay on an offline-heavy host: `fallback = "none"` → `route()` raises `RouteUnavailable` **before any side effect** (no dead wake packet, no cross-tier scan, no paid API), and a batch consumer "catches RouteUnavailable and defers to the next awake window." That is a *clean, cheap, honest* deferral that actually re-completes the work later.

**Difference-list — working pattern vs the two broken agents:**

| Dimension | Correct pattern (relocated tasks / Tier C route) | Synthesizer (Origin 1) | Knowledge Lint (Origin 2) |
|---|---|---|---|
| Miss detected | Once, up front (route pre-flight) | Per file, N times, each a full 90 s poll | N/A — never attempts the host |
| Cost of a miss | ~one health check; raises immediately | ~files × 90 s (37 min observed) + up to N pushes | zero attempt, but silent gap |
| Recorded state | `RouteUnavailable` → caller defers | `status=error` via the *wrong* path; graceful `wol-deferred` path is dead | `status="success"` unconditionally |
| Work re-completed later | Yes — consumer retries next awake window | Only implicitly (indexer state not advanced → next night, if MBP up) | Never |
| Honesty | Distinguishes down-vs-empty | Down looks like generic error | Down/absent indistinguishable from "ran, found nothing" |

**Exit gate met:** the concrete difference-list above is stated. The broken agents diverge from the fleet's own established pattern on every axis.

---

## Phase 3 — Hypothesis and Testing

**Hypothesis (names the Evidence-Block Origin):** *The architectural Origin — binding Tier-2 work to the non-always-on MBP with only best-effort pmset self-wake — produces the intermittent-degradation Symptom because the two consuming code origins convert a reachability miss into (1) a 37-minute per-file poll storm ending in `status=error` while the intended `wol-deferred` fast-path is unreachable dead code (synth), and (2) a permanently unwired, silently "successful" local-only subset (lint).*

**Tests applied (read-only, since this is diagnosis):**

1. *If Origin 1 is the per-file swallow, an asleep night's duration ≈ files × wake_timeout and status = error, never wol-deferred.* → **Confirmed**: 2026-06-14 = 24 files, 2199 s ≈ 24 × 90 s, `status=error`, and 0/30 manifests are `wol-deferred`.
2. *If Origin 2 is the missing `llm_caller`, no lint report ever contains an LLM-only finding kind.* → **Confirmed**: 0 `source=llm`, 0 `soul-tier-a-conflict` across all 8 reports; only `source=sql` + regex `stale-reference`.
3. *If the driver is host availability (not code that could self-heal on retry), misses cluster when the MBP is physically away.* → **Confirmed**: all 4 misses are Sat/Sun consecutive-weekend pairs; weekdays are clean. pmset self-wake is irrelevant off-LAN → matches.
4. *Counter-check the skill's "no single code root cause / purely environmental" escape hatch.* → **Rejected**: the environment (MBP asleep) is real, but two concrete code defects (dead deferral path; never-wired llm_caller) are what make the miss expensive-and-silent. This is not the canonical "truly environmental, add retry/skip" case — the skip is the bug.

**Exit gate met:** single hypothesis, confirmed by minimal read-only tests; the "environmental only" alternative explicitly tested and replaced.

---

## Phase 4 — Implementation

**Not performed. Diagnosis only, per task and per authorization.** Below is the intent-carrying fix spec for a weaker implementing model, to be executed later under separate authorization. Per the skill, any eventual fix must open by citing its Origin and land a failing test first (`verification-loops`), then `verification-before-completion` before any success claim.

---

## Root Cause — Symptom vs Cause, Made Explicit

- **Symptom (what is observed):** "Two agents' Tier-2 work degrades intermittently; runs succeed with Tier-2 silently skipped."
- **Environmental condition (the owner's/skill's first framing):** "The MBP is asleep/away, so Qwen is unreachable." *True but not the root cause* — it is the trigger, not the defect.
- **Actual root cause (what to fix):** Tier-2 work is **statically bound to a host that is structurally unavailable on a predictable fraction of dispatch times** (`macbook_pro`, `always_on=false`, weekend-away), backed only by a **best-effort pmset self-wake** whose preconditions (plugged in, lid state, on the home LAN) fail exactly when they're needed most. The two consumers then mishandle the miss:
  - the synthesizer's graceful `wol-deferred` deferral is **dead code**, so a miss becomes a 37-minute poll storm + a page-per-file + `status=error`;
  - knowledge-lint's MBP semantic pass was **never wired**, so it reports `success` while doing none of the advertised Tier-2 work.
- **Why "reachability, not code — by design" is wrong here:** the fleet's *own* documentation (`2026-06-05-mbp-away-weekend-fleet-behavior.md:11,13`) describes the intended clean behavior — a 90 s deferral, one alert, a `wol-deferred` manifest for synth; "Tier 2 runs normally if MBP on" for lint. **The code does neither.** The gap between the believed design and the wired reality is the root cause the owner sensed. "Skip-and-continue by design" describes a design that was never actually built.

---

## Fix Spec (intent-carrying; for a weaker implementing model)

Scope: `agents-sdk/agents/vault_synthesizer.py`, `agents-sdk/agents/knowledge_lint.py`, and one owner decision on host binding. Do **not** implement without separate authorization. Three coordinated code fixes (A–C) resolve the mishandling; one strategic decision (D) resolves the binding.

### Global invariants — apply to every change below (what NOT to change)

- **$0/run is a hard contract.** Never add Claude API fallback for these agents (`max_budget_usd = 0.00`; weekend doc §"Why it's safe"). `route_to_macbook` must keep *raising*, never cascade to the paid API. A miss must cost $0.
- **WOL magic-packet stays retired.** Do not reintroduce `send_magic_packet`/`wol_mac` for the MBP. pmset self-wake is the sanctioned wake path.
- **Never advance indexer state on a deferred/failed synth run** (`vault_synthesizer.py:1419–1421` already gates on `ok`/`partial` — preserve this; it is the retry/backfill invariant).
- **Never touch the vault git path** (CLAUDE.md rule 8) and **do not re-enable any disabled agent**.
- **Keep manifest/report writes atomic** (tmp-then-rename, `:668–672`).
- **Test from the Mac Mini's resolution path, not on the MBP** — on the MBP `seans-macbook-pro.local` is loopback and masks the bug (observed live). Simulate unreachability by pointing the task at a dead host / forcing `MachineStatus.UNHEALTHY` via `set_machine_status`.

### Fix A — Make the synthesizer's deferral real; kill the poll storm

- **Objective:** A reachability miss costs ~one health check, records the honest `wol-deferred` state, pages at most once, and drops zero knowledge (retried next run). No 37-minute poll storm.
- **Root cause addressed:** Origin 1 — `vault_synthesizer.py:1020–1024` swallows `WOLUnavailable`, making the `main()` `wol-deferred` handler (`:1373–1390`) dead code.
- **Change (intent, not prescription):** Pre-flight MBP reachability **once**, before the per-file loop — a single `route_to_macbook`/health check. If unreachable, short-circuit to the *existing* deferral outcome: write the `status=wol-deferred` manifest, `record_run(status="deferred")`, do **not** advance indexer state, return 0. Additionally, inside the loop, `WOLUnavailable` must **not** be caught-and-continued as a generic per-file error — if the host drops mid-run, break to the same deferral outcome rather than re-polling every remaining file. Net: the graceful path that `main()` already contains becomes reachable; the dead code comes alive instead of being deleted.
- **What NOT to change:** Do not delete the `STATUS_WOL_DEFERRED` vocabulary or the `wol-deferred` manifest writer — wire *to* them. Do not change `wake_timeout_s` semantics for the legitimate single cold-wake case (a real 02:25 pmset wake may need the 90 s). Do not convert genuine per-file JSON/parse failures into run-level deferrals — only host-unreachability defers.
- **Done-criteria:** With the MBP forced UNHEALTHY, a run over N changed files completes in **≤ ~1 × wake_timeout** (not N ×), writes exactly one `status=wol-deferred` manifest, emits **at most one** page, spends $0, and leaves indexer state unadvanced (next run re-attempts the same files). A healthy run is byte-for-byte unchanged. A failing test encoding "N-file unreachable run defers once, does not poll N times" exists and passes.
- **Edge cases:** zero changed files (already returns `ok` — must not regress to `wol-deferred`); MBP reachable at pre-flight but asleep mid-run (loop-level break must still defer cleanly, not storm); MBP awake but Ollama not yet serving (cold darkwake) — treat as unreachable and defer, do not hang.

### Fix B — Resolve knowledge-lint's phantom Tier 2 (owner decision required)

- **Objective:** Knowledge Lint's reported state must match what it actually did. Either the MBP semantic pass runs (and defers honestly when it can't), or it is retired and the docs corrected — but it must never again report `success` for work it never performed.
- **Root cause addressed:** Origin 2 — `knowledge_lint.py:824` calls `run_tier2` with no `llm_caller`; `record_run` hardcodes `status="success"` (`:843`).
- **Change — the spec surfaces the fork; it does not silently pick one:**
  - **Option B1 (wire it):** In `main()`, build a `HybridRouter` + `llm_caller` mirroring `vault_synthesizer._default_llm_caller_factory` (task `vault_synthesis`), pre-flight MBP reachability (reuse Fix A's helper), and pass `llm_caller` into `run_tier2` **only when reachable**. When unreachable, record the LLM leg as *deferred* in the report and in `record_run` notes — not silently absent. This is the only way `soul-tier-a-conflict` (CLAUDE.md HIGH) ever fires.
  - **Option B2 (retire it):** If the SQL fast-path + regex staleness (which have carried every report for months) are sufficient, delete the dead `llm_caller` branch (`:552–601`) and the `build_soul_context` call, correct the docstring (`:10`) and CLAUDE.md so documented behavior matches reality, and drop `soul-tier-a-conflict` from advertised capabilities.
- **What NOT to change:** Tier-1 structural checks and the SQL `concept_edges` contradiction fast-path are correct and must run every week regardless of MBP state and regardless of B1/B2. Do not add API fallback (B1's miss defers, never pays).
- **Done-criteria:** `record_run` no longer emits a bare `status="success"` when the intended semantic leg didn't run — the run's state string distinguishes *ran-LLM* / *deferred-LLM* / *no-LLM-by-design*. If B1: a reachable run produces at least one `source=llm` or `soul-tier-a-conflict` line in a fresh report (grep-verifiable), and an unreachable run records the leg as deferred. If B2: no code path references a never-called `llm_caller`, and docs no longer claim an MBP Tier-2 pass.
- **Edge cases:** launchd runs `knowledge_lint.py` with **no args** → `--full` is false → Tier 2 only runs when Tier 1 found issues; ensure the LLM leg (B1) or its removal (B2) behaves correctly on a clean-Tier-1 week too. Sunday 22:00 is after the documented weekend return (~14:00), so B1 will usually find the MBP up — but must still defer cleanly on a long-away weekend.

### Fix C — Make the reachability outcome first-class and observable

- **Objective:** A silent skip becomes structurally impossible: every run's record distinguishes *produced* / *ran-empty* / *did-not-run-unreachable*, and `meta_agent` surfaces "deferred/unreachable" as its own state — visible without paging, never mislabeled "healthy" or buried as generic "error."
- **Root cause addressed:** the surfacing half of both origins (`vault_synthesizer` error-vs-deferred conflation; `knowledge_lint` hardcoded success).
- **Change:** Reuse the synthesizer's existing status taxonomy; add the equivalent to knowledge-lint. Ensure `meta_agent.check_agent_health` (`meta_agent.py:130–209`) maps a deferred/unreachable run to a distinct, surfaced status rather than folding it into `healthy` (lint today) or `error` (synth today). Update the honest-but-vague `meta_agent` machine labels ("MBP (when awake)", "Mac Mini / MBP") to reflect the resolved binding after Fix D.
- **What NOT to change:** don't invent a new notification channel; a deferral should be *visible in the daily fleet note*, not a new page.
- **Done-criteria:** on a simulated miss, the daily fleet note shows the agent as "deferred (host unreachable)", not "healthy" and not an undifferentiated "error"; on a healthy run, unchanged.

### Fix D — Resolve the binding at the source (strategic; owner chooses)

- **Objective:** Stop depending on an intermittent host for scheduled Tier-2 work. This is the durable "resolve, not paper over" the owner asked for; A–C make the *miss* clean, D reduces *misses to ~zero*.
- **Root cause addressed:** the architectural Origin itself (static bind to `always_on=false` MBP).
- **The tradeoff the spec must NOT hide:**
  - **D1 — relocate to the always-on Mac Mini** (fleet precedent: `inbox_triage`, `financial_analysis`, `config.toml:355–366`). Move `vault_synthesis` (and lint Tier-2, if B1) to a Mac-Mini-served model. Cost: the Mac Mini likely can't hold qwen3.6-35b — requires validating a smaller model's synthesis/contradiction quality on the existing eval suite (`evals/vault-synthesizer/`). Benefit: the weekend-away failure mode disappears entirely, because the runner *is* the model host.
  - **D2 — harden + monitor the pmset self-wake** (keep the MBP binding). Verify the wake LaunchDaemon is installed/loaded and `pmset -g sched` shows the 02:25/Sun-21:55 wakes; gate on AC power (scheduled wakes are battery-suppressed); add a post-wake readiness gate (wait for Ollama-serving, bounded); and add a **catch-up re-dispatch** so a missed night's Tier-2 work actually completes when the MBP is next confirmed up (not merely "retried if it happens to be up"). Cost: cannot fix the off-LAN weekend case at all (pmset wake is meaningless when the laptop is in another city) — so D2 leaves the weekend misses that dominate the evidence.
- **Recommendation carried (not decided):** the evidence — misses are weekend/off-LAN, which D2 structurally cannot address, and the fleet has twice chosen relocation for exactly this reason — points to **D1** as the durable fix, contingent on a smaller model clearing the eval bar. Put this decision to the owner; do not silently pick.
- **Done-criteria (if D1):** no `task_map` entry for synthesis/lint-Tier-2 points at `macbook_pro`; the eval suite passes at the chosen model; a simulated weekend (MBP off-LAN) yields a normal `ok` run, not a deferral. **(if D2):** `pmset -g sched` verified populated; a battery/off-LAN night defers cleanly via Fix A/B and re-completes via the catch-up dispatch on next confirmed uptime.

### Secondary finding (fold into whichever fix touches notifications)

`notify_wol_failure` (`pushover.py:116–133`) sends **unconditionally** — it never consults `[notifications] notify_on`, from which `wol_failure` was deliberately removed (`config.toml:415–417`) on the belief that "no agent wakes the MBP anymore." The documented intent (no WOL-failure pages) is therefore **not enforced in code**: today every asleep synth night pages once *per changed file*. Fix A collapses this to ≤1 page/run; additionally, `notify_wol_failure` should honor `notify_on` so the config's stated intent is real. **Do not** silence it globally without the owner's call — just make code and config agree.

---

## Verification handoff (Phase 4 discipline, for the eventual implementer)

Per this skill's chosen chain: each fix's first line of explanation must cite its Origin ("Fixes Origin 1: …" / "Fixes Origin 2: …"). Land a **failing test first** via `verification-loops` (e.g. "24-file unreachable synth run defers once in ≤~90 s and does not advance indexer state"; "reachable lint run emits ≥1 `source=llm` finding" or B2's "no dead llm_caller path remains"). Run `verification-before-completion` — exercise a simulated-unreachable run and confirm the manifest/report state with your own eyes — before any "fixed" claim. If three fix attempts fail (each revealing new coupling), stop and escalate to `zoom-out-and-think`, do not ship a silent Fix #4.

---

## Evidence read — appendix (every file/artifact consulted)

**Skill**
- `.claude/skills/systematic-debugging/SKILL.md` — method followed.

**Pinned starting read set**
- `agents-sdk/agents/vault_synthesizer.py` — per-file `except` swallow (1020–1024), `_call`/`route_to_macbook` (1214–1219), dead `wol-deferred` handler (1373–1390), status promotion (1175–1192), indexer-state gate (1419–1421).
- `agents-sdk/agents/knowledge_lint.py` — `run_tier2` no-`llm_caller` call site (824–828), `llm_caller is None` early return (552), hardcoded `record_run(status="success")` (843–845), stale docstring (10).
- `agents-sdk/lib/hybrid_router.py` — `route_to_macbook` poll/notify/raise (369–437), `WOLUnavailable`/`RouteUnavailable` contracts (33–50), `send_wol` (236–269).
- `agents-sdk/config.toml` — MBP machine block (305–333), `task_map` synthesis→MBP (375–377), Tier C `fallback="none"` (389–403), `notify_on` minus `wol_failure` (415–417), agent schedules (118–135).

**Followed-the-evidence reads**
- `agents-sdk/lib/pushover.py` — `notify_wol_failure` unconditional send (116–133); `notify_on` not consulted.
- `agents-sdk/agents/meta_agent.py` — `check_agent_health` CSV status mapping (130–209), machine labels "MBP (when awake)"/"Mac Mini / MBP" (54–60).
- `agents-sdk/schedules/com.sean.agent.knowledge-lint.plist` — Sun 22:00, runs `knowledge_lint.py` with **no args** (no `--full`).
- `agents-sdk/schedules/com.sean.agent.vault-synthesizer.plist` — 02:30 daily.
- `agents-sdk/schedules/com.sean.agent-fleet-wake-scheduler.plist` — root LaunchDaemon, 23:30, runs `schedule_wakes.sh`.
- `agents-sdk/scripts/schedule_wakes.sh` — pmset `wakeorpoweron` at 02:25 daily + Sun 21:55 (the pmset self-wake that replaced WOL).
- `agents-sdk/docs/2026-06-05-mbp-away-weekend-fleet-behavior.md` — the prior mental model; its synth "wol-deferred / 1 alert" and lint "Tier 2 runs if MBP on" claims are disproven by the manifest/report evidence here.

**Empirical artifacts (health manifests + reports)**
- `vault/health/synth-manifest-*.json` ×30 (2026-05-23 → 06-23) — status/model/wol/duration history; 4 error nights all Sat/Sun; `wol-deferred` never observed.
- `vault/health/synth-manifest-2026-06-14.json` (full) — error/none/2199.53s/24 files, `run_id 02:30:06` — the poll-storm smoking gun.
- `vault/health/*lint-report*.md` ×8 (2026-04-18 → 06-07) — 0 `source=llm`, 0 `soul-tier-a-conflict`, all contradictions `source=sql`.

**Git history**
- `git log -S "run_tier2("` on `knowledge_lint.py` — introducing commit `6ad8ce3` created both `run_tier2` and its `llm_caller`-less call site (born unwired).
- `git log` on `knowledge_lint.py` — no later commit ever added an `llm_caller` at the call site.

**Grep sweeps**
- `run_tier2` / `route_to_macbook` / `llm_caller` callers across `agents-sdk` — production `run_tier2` call has no `llm_caller` (only tests pass one); `route_to_macbook` used by `vault_synthesizer` + `flush` (adjacent, out of scope), absent from `knowledge_lint` except docstring.
- `schedule_wakes|pmset|wake-scheduler` sweep — surfaced the wake LaunchDaemon, `install_schedules.sh:38`, and the 06-05 weekend doc.

**Live probes (≤5 s, read-only)**
- `curl -m5 http://192.168.68.200:11434/api/tags` → 200 / 32 ms (Mac Mini healthy).
- `curl -m5 http://seans-macbook-pro.local:11434/api/tags` → 200, but name resolves to `127.0.0.1` on this MBP checkout (loopback → repro gotcha, not a LAN reachability signal).
- `date` weekday checks — confirmed all 4 error nights fall on Sat/Sun; sampled healthy nights on weekdays.

**Not read (parallel-run isolation, per task):** `docs/plans/wwf5d/baselines/`, `docs/plans/wwf5d/fable-runs/`.
