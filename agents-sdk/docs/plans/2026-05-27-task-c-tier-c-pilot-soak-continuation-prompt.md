# Task C continuation prompt — Tier C pilot soak design

> Paste everything BELOW THE LINE into a fresh Claude Code session, working
> directory `/Users/seanwinslow/Code-Brain/code-brain`. The session has no
> memory of the conversation that produced Tasks A and B; this prompt is
> self-contained.

---

We're continuing Topic 20 fleet work. Tasks A (LM Studio → MBP-Ollama migration
for `vault_synthesizer` + `job_feed`) and B (MBP model cleanup, freed 38 GiB)
are complete and committed. This session has exactly one task: **scope and
execute the Tier C pilot soak — gemma4:26b @ Alienware-Ollama, 7-day passive
observation, Pattern E (manual wake) 7am–5pm window.**

# Before doing anything else

1. Confirm branch state. You should be at `c3a2a10` or a descendant
   (vault auto-commits may follow but no other code commits):
   ```
   git log --oneline origin/main..HEAD
   # expected output (top 3):
   #   c3a2a10 chore(routing): clean up Task A/B follow-ups …
   #   3812b4d feat(routing): migrate vault_synthesizer + job_feed scoring …
   #   b73cad2 data(topic-20): MBP-Ollama runtime comparison …
   ```

2. Read in full (no skim):
   - [Topic 20 main synthesis](vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md) — focus on
     §Tier C scorecards, §Operating contract for Tier C, §Per-agent
     adoption recommendation, and the §Soak outcome stub at the bottom
     (the file you'll be updating when the soak completes).
   - [Topic 20 MBP-Ollama follow-up](vault/20_projects/research/2026-05-26-topic-20-mbp-ollama-runtime-comparison.md) — context only; this is the data behind Task A,
     not directly load-bearing for Task C, but provides the per-runtime
     benchmark methodology you'll mirror for soak verification.
   - [The Task A/B plan that was approved last session](/Users/seanwinslow/.claude/plans/agreed-start-with-a-valiant-rivest.md) — for the
     "Pattern E" operating contract and the verification discipline
     (median sample, not best) that carries forward to Task C.

3. Surface these auto-memory entries (most should load automatically via
   MEMORY.md; read the full body of each):
   - `project_alienware_wake_impossible.md` — **load-bearing.** Modern
     Standby on the Alienware Aurora firmware suppresses ALL non-Microsoft-
     signed wake events. WoL + Task Scheduler RTC both fail in production
     even when smoke tests look like they pass. **Pattern E (manual wake)
     is the only path. Do NOT retry remote-wake schemes.**
   - `project_alienware_hardware_specs.md` — RTX 5080 16GB VRAM (NOT 4090
     24GB), Core Ultra 9 285, 64GB DDR5-5200, Modern Standby firmware. Tier C
     model sizing must respect 16GB VRAM ceiling; gemma4:26b fits because
     its MoE 3.8B-active design plus Ollama's CPU offload keeps the working
     set under VRAM.
   - `feedback_synth_verify_against_median_not_best.md` — **load-bearing for
     soak verification.** Random-sample the median; cherry-picking the best
     output masks defects. Use `sort -R | head -2` (or equivalent), NOT
     manual selection of "the good ones".
   - `project_mbp_ollama_viable_runtime.md` — context for what changed in
     the fleet last session (Task A flipped vault_synthesizer + job_feed
     to MBP-Ollama with `qwen3.6_35b-a3b-32k`). Not directly Task C work,
     but you'll reference it when designing the script's fallback target.
   - `project_pr52_mbp_stale_checkout.md` — read the 2026-05-26 update; the
     MBP-side parallel synth schedule is verified absent today.

4. Skim the existing fleet-script patterns so the Tier C script lands in
   the right shape (NOT a deep read — quick orient):
   - [agents-sdk/scripts/benchmark_ollama_model.py](agents-sdk/scripts/benchmark_ollama_model.py) — request shape against
     Ollama. Uses `/api/chat` with `think:false` + `options.num_ctx`.
     Mirror this for any LLM call the soak script makes.
   - [agents-sdk/scripts/query.py](agents-sdk/scripts/query.py) — closest existing precedent for a
     manual-trigger CLI script that targets a local model and writes to
     vault/. Same dispatch pattern (`PYTHONPATH=. .venv/bin/python3 scripts/…`).
   - [agents-sdk/lib/hybrid_router.py](agents-sdk/lib/hybrid_router.py) — HybridRouter has health-check + fallback
     wiring but doesn't make HTTP calls itself; it returns `RoutingDecision`.
     For Task C, decide whether to route through HybridRouter (Tier C isn't
     in `[routing.task_map]` today — you'd need to add it) or do a direct
     httpx probe + fallback. **Recommended:** route through HybridRouter
     for consistency; add a `tier_c_codegen` (or similar) task to task_map.
   - [agents-sdk/scripts/run_mbp_ollama_benchmarks.sh](agents-sdk/scripts/run_mbp_ollama_benchmarks.sh) — pattern for
     orchestrator-style scripts that loop over a workload.

# State summary (verified 2026-05-26 at the end of the last session)

**Branch:** 3 commits ahead of origin/main, working tree clean except for
possible vault auto-commits.

**Alienware (RTX 5080 16GB, Pattern E manual wake, 192.168.68.201:11434):**
  Reachable when awake. 11 models installed from Topic 20 pulls:
  - `gemma4:26b` + `gemma4_26b-32k:latest` ← **PILOT TARGET**
  - `qwen3.5:27b` + `qwen3.5_27b-32k:latest` (batch-quality candidate)
  - `qwen3.5:9b` + `qwen3.5_9b-32k:latest` (high-throughput)
  - `devstral:24b-small-2505-q4_K_M` + `devstral_24b-32k:latest` (TBD Topic 21)
  - `nemotron3:33b` + `nemotron3_33b-32k:latest` (TBD Topic 21)
  - `qwen3-vl:8b` (vision)

  Disk free: ~318 GB at end of Topic 20 cleanup; no headroom concern.

**MBP (M4 Max 48GB) Ollama** at `seans-macbook-pro.local:11434`:
  - `qwen3.6_35b-a3b-32k:latest` ← PRODUCTION (Task A target)
  - `qwen3.6:35b-a3b` (base)
  - `qwen3.5:27b` + `qwen3.5_27b-32k:latest`
  - `qwen3-coder:30b` + `qwen3-coder_30b-32k:latest`
  Disk free: ~99 GiB.

  LM Studio also bound on :1234 with `qwen3-14b-4bit` loaded as co-resident
  fallback runtime. Don't touch.

**Mac Mini (M4 Pro 24GB, always-on, 192.168.68.200:11434):**
  - `gemma4:e4b` + `gemma4_e4b-16k` (production Tier B + tier-2 LLM target)
  - `qwen3:14b` / `qwen3-14b-research:latest`
  - `nomic-embed-text` (embeddings)
  - `phi4-mini-reasoning`

**Routing config** ([agents-sdk/config.toml](agents-sdk/config.toml#L274-L296)):
  - macbook_pro: runtime=ollama, port=11434, models=[qwen3.6_35b-a3b-32k,
    qwen3-coder_30b-32k, qwen3.5_27b-32k]
  - alienware: runtime=ollama, port=11434, wol_mac present but **non-
    functional** per Pattern E, models=[qwen3-vl:8b] (current list is
    sprite-QA-only; you'll likely want to expand it for Tier C tasks)
  - `[routing.task_map]` currently has `sprite_vision_qa` and
    `comfyui_orchestration` mapped to alienware. **No general-purpose
    Tier C codegen / summarization task exists yet.**

**Task A migration verification (Stage 1b) is overlapping calendar work:**
  - Tonight's 02:30 ET nightly run is the first vault_synthesizer call
    against MBP-Ollama with `qwen3.6_35b-a3b-32k`. Tomorrow morning verify:
    `vault/health/synth-manifest-<today>.json` → `model_used` field should
    be `qwen3.6_35b-a3b-32k`. Sample MEDIAN output (sort -R | head -2)
    from today's new `vault/knowledge/expansions/*.md`.
  - **Task C design work in this session is INDEPENDENT of Stage 1b** —
    Tier C doesn't touch the same code paths. But if you have time after
    landing Task C, surface the Stage 1b check too.

# The task — Task C: Tier C pilot soak

## High-level shape (from Topic 20 main report's Open Questions §Soak validation)

> Per the plan's Phase 6 pilot model, soak the new Tier C model on a
> low-stakes batch agent for 7 days before broader rollout. Pilot agent
> recommendation: a manually-triggered codegen scratchpad (not a launchd
> agent — Tier C is brand new and the 7am-5pm availability window doesn't
> suit launchd anyway).

## What needs to happen

1. **Pick the pilot workload.** Topic 20 main report suggests three
   candidates and Sean should pick which to pilot first. Plan-mode work
   should surface the question explicitly, with concrete tradeoffs:
   - **(a) Manual codegen scratchpad** — Sean throws a one-shot prompt at
     `gemma4:26b @ Alienware`, gets a response, evaluates ad-hoc. Lowest
     setup cost; no automated output corpus to verify.
   - **(b) Long-context vault article summarization** — pick N existing
     vault articles, summarize via Tier C, store outputs in a soak
     manifest. Automated quality assessment is possible (compare against
     `qwen3-14b @ Mac Mini` or the article's own existing summary).
   - **(c) Comparison runs vs Mac Mini baseline** — same prompt set goes
     to both Tier C and Mac Mini, capture both outputs side-by-side, score
     by Sean's eyeball on a random-sample median. Most rigorous for an
     adoption decision; highest setup cost.

   **Recommendation if no other guidance:** (b) — automated workload gives
   you a sample distribution to median-check, doesn't require Sean's
   attention every day, and naturally answers "is this useful for batch
   summarization?" which is what the report suggests gemma4:26b is good at.

2. **Design the manual-trigger script.** Lives at
   `agents-sdk/scripts/tier_c_soak.py` (or similar — pick a name during
   plan mode). NOT in `agents-sdk/agents/` (that's for launchd-managed
   agents). Pattern matches `scripts/query.py`. Required behavior:
   - Reachability probe: `GET http://192.168.68.201:11434/api/tags` with
     3s timeout. If down, fail fast (exit code 2, log "Alienware unreachable
     — fire WoL? No. Pattern E says Sean wakes manually. Try again
     7am-5pm.") or fall back to Mac Mini with a clearly-flagged warning.
     **Decide which during plan mode.** Recommend: fail fast + clear
     message, because the whole point of the soak is to measure Tier C,
     not its fallback path.
   - LLM call shape: `POST /api/chat` with `think:false`,
     `options.num_ctx=<workload-appropriate>`, `temperature=0.0` for
     deterministic comparison. Mirror `benchmark_ollama_model.py`.
   - Output: append a JSON record per run to a soak manifest at
     `vault/health/tier-c-soak-{YYYY-MM-DD}.jsonl` (or .json — decide
     during plan mode whether append-JSONL or rewrite-JSON is cleaner
     given the 7-day cadence). Each record: timestamp, model used, prompt
     hash, output (or output path), wall-clock latency, eval_count,
     reachability, fallback fired (true/false).
   - CLI shape: `tier_c_soak.py --workload <name>` or `--prompt <file>`,
     idempotent against the per-day manifest, prints a 1-line summary on
     success.
   - **The script DOES NOT manage launchd, DOES NOT add itself to a
     schedule, DOES NOT call `wake_alienware.py`** (which is non-
     functional anyway per Pattern E).

3. **Soak protocol for 7 days.** Decide during plan mode:
   - How many runs per day (recommend: 2–3, all within 7am–5pm window;
     spread by 1 hour minimum to avoid the same model reloading cold-warm
     in tight succession)
   - What variance signals to capture (throughput stddev, error rate,
     Mac Mini fallback events if you chose the fallback path)
   - Quality assessment cadence — recommend: median-sample two outputs
     per day (`sort -R | head -2` from that day's manifest entries) and
     ask Sean to rate "thinking-partner depth" vs the report's
     existing-output baseline.
   - Stopping conditions:
     - **Adopt:** 7 days clean, median quality matches or beats the Mac
       Mini fallback baseline, no Alienware-side errors, no Mac Mini
       fallback fires (if fail-fast) or <10% (if fallback path enabled).
     - **Rollback:** Alienware fails to wake on any 7am-5pm day, OR
       median quality below baseline on any sampling day, OR consistent
       parse failures / model-emit-thinking-tokens (signals
       qwen3.5:9b-style adapter brokenness).

4. **Update the Topic 20 main report at end of soak.** The file
   `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md`
   has a stub at the very bottom titled "Soak outcome (filled after Phase 6
   pilot, if any)" — currently just "_Pending_". Fill it with: pilot
   workload chosen, 7-day summary, adopt/rollback decision, any new
   findings. **DO NOT** `git add` this file directly — vault git ops are
   owned by the shell auto-commit hook (CLAUDE.md Rule 8 / Issue #22).
   Just edit the file; the hook will commit it.

## Plan-mode questions to settle BEFORE writing code

1. **Workload choice** — (a) codegen / (b) vault summarization / (c) A/B
   vs Mac Mini. Use AskUserQuestion; offer all three with tradeoffs.
2. **Reachability behavior** — fail fast or fall back to Mac Mini? Default
   recommend: fail fast (cleaner soak signal).
3. **HybridRouter integration** — add a Tier C task to `[routing.task_map]`
   for cleanliness, or use direct httpx probe? Default recommend:
   HybridRouter + a new task entry like `tier_c_summarize` (since
   HybridRouter already has Mac Mini fallback wiring if you ever want it).
4. **Output format** — JSONL append vs JSON rewrite per day? Default
   recommend: JSONL (line-delimited, idempotent appends, easier to median-
   sample with `shuf | head`).
5. **Daily cadence** — 1, 2, or 3 runs per day inside the 7am-5pm window?
   Default recommend: 2 (one mid-morning, one mid-afternoon — catches
   model-warm and model-cold paths).

## Acceptance criteria (for the script + the soak design, not the
   adoption verdict)

- `agents-sdk/scripts/tier_c_soak.py` runs successfully with
  `--dry-run` when Alienware is reachable; exits non-zero with a
  clear message when not reachable
- Probe shape and LLM-call shape match the Topic 20 benchmark harness
  (`/api/chat`, `think:false`, sized `num_ctx`)
- Manifest file is written under `vault/health/` and is human-readable
- Rollback documented: `git revert <script-commit>` removes the soak
  ability cleanly; manifests under `vault/health/` are vault-owned and
  stay
- 7-day calendar dates spelled out (e.g. 2026-05-26 → 2026-06-02), so
  Sean knows exactly when to check the Topic 20 main report stub

# Operating constraints (NON-NEGOTIABLE)

1. **Plan mode FIRST.** Sean said "starting in plan mode to fully scope
   out the situation and then execute". Use `/plan` or double Shift+Tab.
   Don't write any code, don't add config entries, don't pull/push
   models, until the plan file is approved.

2. **Pattern E for Alienware — manual wake only.** Do NOT call
   `wake_alienware.py`. Do NOT add WoL retry logic. Do NOT schedule the
   soak on launchd. The Alienware's Modern Standby firmware blocks all
   non-Microsoft-signed wake events; this is verified architecturally
   impossible. The script's reachability probe is the whole story —
   Alienware is either reachable (Sean has it awake) or it's not (Sean
   needs to physically wake it).

3. **Sample MEDIAN not best.** For ALL quality assessment during the
   7-day soak. Use `sort -R | head -2` or equivalent (`shuf | head -2`
   on GNU coreutils). Cherry-picking the best output is exactly the
   failure mode that masked PR #52's stale-checkout contamination at
   first; same discipline applies here.

4. **Hardware-touchpoint walk-through.** Anything that touches the
   Alienware (model pulls, removes, modelfile builds) — walk Sean
   through one question at a time, NOT in auto mode. Sean explicitly
   set this rule for the prior session and it applies to Task C too.

5. **Vault git ops** — owned by shell auto-commit hook (CLAUDE.md Rule 8 /
   Issue #22). Don't `git add vault/...` for manifest files or the
   Topic 20 report update. Edit the files; let the hook commit.

6. **LM Studio + MBP-Ollama stay co-resident.** Task A landed
   yesterday; this is not the session to touch Task A's commits or
   move launchd schedules. Tier C is additive — new task in task_map,
   new script in `scripts/`, no other changes.

7. **NOT a launchd agent.** The pilot script must be Sean-triggered.
   Don't add a plist to `agents-sdk/schedules/`. Don't add an entry to
   `install_schedules.sh`. The whole point of Pattern E + 7am-5pm
   window is that human triggers are the only reliable path.

8. **Path references** — markdown links like `[path](path#L42)`, per
   the VSCode extension contract.

# First action

After reading the synthesis docs and memory entries:

1. `git log --oneline origin/main..HEAD` to confirm at `c3a2a10` or
   descendant
2. `nc -z -w 3 192.168.68.201 11434` and `nc -z -w 3 192.168.68.200 11434`
   to confirm Alienware (if awake) and Mac Mini reachable
3. `curl -sS http://192.168.68.201:11434/api/tags | jq -r '.models[].name' | grep gemma4`
   to confirm `gemma4:26b` and `gemma4_26b-32k:latest` are both present
   on Alienware
4. Announce plan mode entry. Do discovery (read `scripts/query.py`,
   `scripts/benchmark_ollama_model.py`, `lib/hybrid_router.py`,
   `config.toml`'s task_map section). Use Explore subagents for breadth
   if needed.
5. Use AskUserQuestion on the five plan-mode settle questions (workload
   choice, reachability behavior, HybridRouter integration, output
   format, daily cadence). Present recommendations as defaults so Sean
   can approve in a few clicks.
6. Write the plan to the auto-suggested plan file path. Include:
   - **Context** section (why we're doing this)
   - Concrete config.toml additions (task_map entry, alienware models
     list expansion if needed)
   - Script structure (file path, CLI shape, ~50 lines target)
   - Soak protocol (cadence, sampling, stopping conditions)
   - 7-day calendar (e.g. 2026-05-26 start → 2026-06-02 end, soak
     verification on 2026-06-03 morning)
   - Rollback (single command)
   - Verification gates (script smoke test, first probe, first soak
     run output)
7. Call `ExitPlanMode` once the plan is complete.
8. After approval: implement, smoke-test, commit (single commit for the
   script + task_map addition). Then run the FIRST soak datapoint
   manually with Sean watching — that's both the smoke test and Day 1
   of the soak.

# Out of scope (explicit deferrals from this session)

- `knowledge_lint` Tier 2 LLM caller wiring — deferred to a follow-up
  after Task A's 1-week soak passes. **Not in Task C.**
- Topic 21 native-template rebench for `qwen3-coder:30b`,
  `devstral:24b`, `nemotron3:33b`. **Not in Task C.**
- MBP checkout drift cleanup (MBP is at `f7dc6c0`, ~3 commits behind
  main, with uncommitted vault edits). Harmless today; not blocking.
  Address when Sean next sits at the MBP.
- Removing `code_review` test fixtures from `test_hybrid_router.py` —
  the production code_review task_map entry was dropped, but the test
  uses its own self-contained fixture. Leave the tests alone unless
  Sean asks.
- Re-enabling the `gemini-deep-research` agent or `process-inbox` agent
  (both default-disabled per `[agents.*]` config). Out of fleet scope.

# What's already committed (for reference; you should not touch these)

- `b73cad2 data(topic-20): MBP-Ollama runtime comparison — qwen3.6:35b-a3b as Tier A upgrade`
- `3812b4d feat(routing): migrate vault_synthesizer + job_feed scoring from LM Studio MLX to MBP-Ollama`
- `c3a2a10 chore(routing): clean up Task A/B follow-ups — align macbook_pro models list, drop code_review, fix e2e mock`

# What's NOT yet pushed

All 3 commits above are local. Sean has not yet pushed to origin/main.
Don't push as part of Task C — that's Sean's call when he's confident in
both Task A (overnight verification) and Task C (full design landed).

# Reminder of how the prior session unfolded (very brief)

- Task A: full plan-mode pass identified that
  (i) HybridRouter does NOT make HTTP calls (each agent constructs its own
  request, so a config flip alone wouldn't work — code changes needed in
  `vault_synthesizer.py` and `job_scoring.py`),
  (ii) the MBP-side parallel synth schedule from PR #52 was verified
  ABSENT today (memory was 5 days old), and
  (iii) `knowledge_lint` Tier 2 LLM path is dormant in production (main()
  doesn't construct an llm_caller) — so it was excluded from scope.
- Task B: 5-row decision matrix → user approved deletes for `qwen3.6:27b`
  family (Ollama-broken, 25% schema) and `qwen3.5:35b-a3b` family
  (redundant w/ production). Freed 38 GiB on MBP.
- Cleanup commit dropped a stale `code_review` task_map entry, aligned
  the macbook_pro `models` list with what Ollama actually serves, and
  fixed a pre-existing test bug.

Approach Task C with the same discipline: plan first, verify state, ask
before destructive ops, sample median, fail loudly when Alienware is
unreachable rather than papering over Pattern E.

The hard architectural problems are behind us. What's left is a focused
~1 hour of plan-mode design, ~30 minutes of code + smoke test, then 7
days of calendar observation. Good luck.
