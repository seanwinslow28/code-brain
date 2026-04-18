# Phase 6 Follow-up — Claude Code Prompt

Copy everything between the `===` lines below and paste into Claude Code (Opus 4.7, Plan Mode recommended so you can review before execution).

===

<role>
You are a senior infrastructure engineer working on Sean's autonomous agent fleet (Phase 6 of the 16bitfit-battle-mode project). You have deep familiarity with the codebase at `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/`. You value correctness over speed, write thorough tests, and never silently paper over a misconfiguration.
</role>

<context>
Phase 6 A.5 / A.6 previously completed with a "NO SWAP" verdict, but only because two benchmark tasks (`financial_analysis`, `code_review`) were blocked by an LM Studio RAM guardrail and the `inbox_triage` run used only 5 samples instead of the planned 20. Separately, an audit revealed the MacBook Pro WOL path was never fully wired — `agents-sdk/config.toml` still has `macbook_pro.host = "127.0.0.1"` with no `wol_mac`, which means the nightly 02:30 AM Vault Synthesizer would fail silently from the Mac Mini.

Sean has explicitly chosen the **full WOL path (plan §7.9 Option B)** over the always-on shortcut. The goal of this session is to wire WOL end-to-end, verify it works, then re-run the deferred Gemma 4 benchmarks at full sample size so we can make a defensible model-swap decision backed by real data.

Reference documents (load these first, in order):
1. [CLAUDE.md](../../../CLAUDE.md) — root rules
2. [16bitfit-battle-mode/CLAUDE.md](../../CLAUDE.md) — project rules
3. [docs/plans/phase6-SUPER-PLAN-2026-04-17.md](./phase6-SUPER-PLAN-2026-04-17.md) §P0.2, §7.1, §7.9
4. [agents-sdk/lib/hybrid_router.py](../../../agents-sdk/lib/hybrid_router.py) lines 343–406 (`route_to_macbook`) and 224–260 (`send_wol`)
5. [agents-sdk/config.toml](../../../agents-sdk/config.toml) lines 155–182
6. [agents-sdk/scripts/run_gemma4_benchmark.py](../../../agents-sdk/scripts/run_gemma4_benchmark.py)
7. [agents-sdk/benchmarks/results/A6-swap-decision-2026-04-17.md](../../../agents-sdk/benchmarks/results/A6-swap-decision-2026-04-17.md)
</context>

<task>
Complete two connected workstreams. **Do not proceed to Part B until Part A is verified green.** Use extended thinking for planning each part.

## Part A — Wire MacBook Pro WOL end-to-end

<part_a_steps>
1. **Read MBP MAC address.** Open `16bitfit-battle-mode/docs/plans/phase-6-plan-info/machine-MAC-addresses/macbook-pro.png` — it is a screenshot of the MBP's System Settings → Network panel. Extract the MAC address. Also open `mac-mini.png` in the same directory to record the Mac Mini's IP for reference and to cross-check Sean's LAN subnet.

2. **Determine the MBP's LAN IP.** Two options, pick the most reliable:
   - (a) Have Sean run `ipconfig getifaddr en0` on the MBP and paste it back. Use the `AskUserQuestion` tool for this — do NOT guess.
   - (b) If the screenshot clearly shows the LAN IP, use that and confirm with Sean before writing.

3. **Update `agents-sdk/config.toml`** in `[routing.machines.macbook_pro]`:
   - `host = "127.0.0.1"` → `host = "<MBP LAN IP>"`
   - Add `wol_mac = "<MBP MAC, colon-separated uppercase>"`
   - Leave `port = 1234`, `runtime = "lm-studio"` untouched
   - Add a brief inline comment noting "Phase 6 Option B — WOL path"

4. **Audit `route_to_macbook` in `lib/hybrid_router.py`.** Confirm:
   - `wakeonlan` package is actually imported (line ~235). It IS installed in `.venv` (version 3.1.0) — verify this with `.venv/bin/python3 -c "import wakeonlan; print(wakeonlan.__version__)"`.
   - The function calls `send_wol("macbook_pro")` before the health-check loop when `wol_mac` is non-empty.
   - The `wake_timeout_s` default of 60s is long enough for a sleeping MBP to wake and LM Studio to respond. **If the MBP has to boot LM Studio from a cold autostart, 60s may be tight — raise to 90s and document the change.**
   - The health check at `check_health("macbook_pro")` hits `http://<MBP-IP>:1234/v1/models` (LM Studio's OpenAI-compatible endpoint), not a hard-coded path. Fix if necessary.

5. **Update tests.** In `tests/test_route_to_macbook.py` and `tests/test_hybrid_router.py`:
   - Add a case where `wol_mac` is set → `send_wol` is called exactly once with the correct MAC.
   - Add a case where the MBP comes online after 3 health-check retries → routes successfully.
   - Add a case where the MBP never responds → raises `WOLUnavailable` and fires exactly one Pushover notification.
   - Mock `wakeonlan.send_magic_packet` and `httpx.AsyncClient.get` — do NOT make real network calls in unit tests.
   - Confirm existing tests still pass.

6. **Ask Sean to enable Wake-for-Network-Access on the MBP.** Produce a numbered checklist he can follow:
   - System Settings → Battery (or Energy Saver) → Options → "Wake for network access" = ON
   - Ensure MBP is on Ethernet OR "Wake for Wi-Fi network access" (WoWLAN) is explicitly supported — note that WoWLAN is flaky on Apple Silicon over Wi-Fi; if the MBP is on Wi-Fi, recommend a wired connection or an always-on Thunderbolt dock with Ethernet
   - Confirm the MBP and Mac Mini are on the same LAN subnet and VLAN
   - Keep LM Studio's local server toggle ON, port 1234, Gemma 4 31B + Qwen3-14B both available (JIT or preloaded per the Part B fix)
   - Disable "Put hard disks to sleep when possible" to prevent disk-sleep from masking WOL
   Use `AskUserQuestion` to have him confirm each item is done before continuing.

7. **Live end-to-end WOL verification.** This is the most important step — do not skip.
   - Have Sean manually put the MBP to sleep (Apple menu → Sleep).
   - From the Mac Mini, run:
     ```bash
     cd ~/Code-Brain/claude-code-superuser-pack
     PYTHONPATH=agents-sdk agents-sdk/.venv/bin/python3 -c "
     from lib.config import load_config
     from lib.hybrid_router import HybridRouter
     import asyncio, tomllib
     cfg = tomllib.load(open('agents-sdk/config.toml', 'rb'))
     r = HybridRouter.from_config(cfg)
     print(asyncio.run(r.route_to_macbook(task='vault_synthesis', wake_timeout_s=90)))
     "
     ```
   - Expected: MBP wakes, LM Studio responds, script prints a `RoutingDecision` with `machine='macbook_pro'`, `model='qwen3-14b'`, `reason='route_to_macbook: healthy'`.
   - If it fails: diagnose. Do not move to Part B until this works.

8. **Commit Part A.** Single commit, message: `phase6(P0.2): wire MBP WOL path — config + tests + verification`. Include the live-verification output in the commit body. Do NOT push.
</part_a_steps>

## Part B — Re-run the deferred Gemma 4 benchmarks at full sample size

<part_b_steps>
1. **Fix the LM Studio RAM guardrail in the benchmark runner.** In `agents-sdk/scripts/run_gemma4_benchmark.py`:
   - Between incumbent and challenger runs for each task, call `subprocess.run(["lms", "unload", "--all"], check=False)` to force unload.
   - Alternatively, if `lms` CLI is not on PATH, POST `{"operation": "unload"}` to `http://<MBP>:1234/api/v0/models/<model-id>` (confirm this endpoint against LM Studio docs — it may be non-standard; fall back to CLI if the API is unreliable).
   - Also add a pre-flight step: before starting any task, unload all models so the state is deterministic.
   - Add a `--no-unload` flag for debugging.

2. **Verify LM Studio model availability.** Before running, confirm via `curl http://<MBP>:1234/v1/models` that `qwen3-14b`, `qwen2.5-coder-32b-instruct`, and `gemma4-31b` are all present in the model list (even if not currently loaded). JIT-load will pick them up.

3. **Run full-sample benchmarks.** Override the earlier 5-sample smoke run with the planned 20 samples per task:
   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 scripts/run_gemma4_benchmark.py --samples 20
   ```
   - All three tasks should complete: `inbox_triage`, `financial_analysis`, `code_review`.
   - Incumbent + challenger for each.
   - Expected runtime: ~2–4 hours total given 6 runs × 20 samples.
   - Output: `agents-sdk/benchmarks/results/gemma4-benchmark-<today>.json`

4. **Apply the veto gate (plan §A.6) to each task:**
   - If Gemma 4 31B quality is ≥5 percentage points WORSE than incumbent → **KEEP incumbent**
   - If Gemma 4 31B quality is within ±5pp AND latency is ≥20% faster → **SWAP in favor of speed**
   - If Gemma 4 31B quality is ≥5pp BETTER → **SWAP**
   - Document the decision per-task with exact numbers.

5. **If any swap is approved**, edit `agents-sdk/config.toml` `[routing.task_map]`:
   - e.g., `inbox_triage = { model = "gemma4-31b", machine = "macbook_pro" }` if that wins
   - Run a 1-night regression: kick each affected agent manually and confirm no breakage. If anything errors, revert the swap and mark PARTIAL.

6. **Write `benchmarks/results/A6-swap-decision-<today>.md`** — same structure as the 2026-04-17 report. Include the full 20-sample table, veto-gate application per task, any swap decisions, and a comparison back to the 5-sample April 17 run so we understand what changed.

7. **Update docs per [CLAUDE.md](../../../CLAUDE.md) "When Modifying" rules:**
   - `CHANGELOG.md` under `[3.14.1]` — Phase 6 A.6 re-run + WOL wiring
   - `CLAUDE.md` — update routing table if any swap occurred, update agent-fleet note
   - `README.md` — only if public counts changed
   - Do NOT modify `16bitfit-battle-mode/SOURCE-OF-TRUTH.md`

8. **Run the gate check.** `python3 agents-sdk/scripts/phase6_gatecheck.py` — expect criteria 1 and 2 to flip from PARTIAL to PASS (unless all swaps lose, in which case 2 stays PARTIAL with a clean report).

9. **Commit Part B** as a separate commit: `phase6(A.6): re-run benchmarks at N=20 + apply veto gate`.
</part_b_steps>
</task>

<constraints>
- Follow [CLAUDE.md](../../../CLAUDE.md) rules. Hooks use exit code 2 to deny. Never re-enable the 6 agents disabled on 2026-04-09.
- Do not hard-code any secrets. MAC address is not secret, but verify with Sean that he's OK committing it.
- Do not push to remote. Sean reviews commits before push.
- Do not skip the live WOL verification. A passing unit test ≠ a working wake packet.
- Do not attempt Part B if Part A fails.
- Use `AskUserQuestion` for every point where you need input from Sean (IP, confirmation of settings, approval of swaps). Sean is a code beginner — when asking, briefly explain why you need the info.
- All Phase 6 code must stay 100% local ($0.00 API spend).
- Prefer native MCPs over Zapier.
- If you hit a blocker, stop and ask — do not improvise around a broken assumption.
</constraints>

<thinking_guidance>
Before acting, think through:
1. Read the reference files first. What's the exact current state of `route_to_macbook` and `config.toml`?
2. What's the smallest change to config.toml that enables WOL without breaking unit tests?
3. How do I test WOL without constantly putting Sean's MBP to sleep? (Answer: mock for unit tests, one live test at the end.)
4. For Part B — is the LM Studio `lms` CLI definitely present? If not, what's the fallback?
5. What would a sound veto-gate decision look like if Gemma 4 wins `code_review` but loses `inbox_triage`? (Per plan §A.6 + §7.1: task-by-task decision, not all-or-nothing.)

Output your plan in a `<plan>` block before executing any tool calls that modify files.
</thinking_guidance>

<deliverables>
At the end of the session, produce a single summary message containing:
1. Git status — which commits you made, no pushes
2. WOL live-test output (stdout from the Mac Mini verification command)
3. Full benchmark results table: task × model × quality × p50 latency × veto verdict
4. List of swaps applied (or "none" with reasoning)
5. Gate-check status before vs. after
6. Any open blockers or follow-ups for Sean
7. A one-paragraph plain-English explanation for Sean (who is a code beginner) of what changed in his stack and what he should watch overnight
</deliverables>

<validation>
Before reporting done, self-check:
- [ ] Does `agents-sdk/config.toml` have a non-localhost `host` AND a `wol_mac` for macbook_pro?
- [ ] Did the live WOL verification actually wake a sleeping MBP from the Mac Mini? (Not a unit test — a real wake.)
- [ ] Did `run_gemma4_benchmark.py` complete all 3 tasks × 2 models × 20 samples without RAM failures?
- [ ] Does the new A6 report cite exact 20-sample numbers, not 5-sample?
- [ ] Did you apply the veto gate per-task, not as a blanket decision?
- [ ] Are CHANGELOG.md, CLAUDE.md updated if any swap occurred?
- [ ] Did you run `python3 scripts/validate.py` and `pytest tests/ -v` — both green?
- [ ] Are the two commits distinct and unpushed?
- [ ] Did you tell Sean in plain English what to expect tonight (leave MBP sleeping is OK once WOL verified; Mac Mini always-on; synthesizer fires at 02:30 AM)?

If any box is unchecked, fix before reporting complete.
</validation>

===

## Why this prompt is structured the way it is

Brief notes on the prompt-engineering choices, so you can adapt future prompts for Claude Code:

- **Role block** primes Claude Code to think like an infra engineer, not a helpful generalist.
- **Context block** front-loads the 7 reference files in the right order so Claude Code reads them before planning — applying the "long documents at the top" rule.
- **Two distinct parts with a hard gate** prevents Claude Code from racing ahead to benchmarks while WOL is still broken.
- **Explicit AskUserQuestion directives** catch the handful of places Claude Code genuinely needs your input (MAC, IP, settings confirmation, swap approval) — otherwise it'd guess.
- **Live verification step** is specified as non-optional because WOL often passes unit tests and still fails in the real world (screen-sleep, Wi-Fi power management, subnet misconfigs).
- **Validation checklist at the end** forces Claude Code to self-audit before telling you it's done — the plan §9 pattern.
- **Separate commits** keep the WOL work rollback-able independently from the benchmark results.

## What you should do before you paste the prompt

1. **Open Claude Code with Opus 4.7** (the model strong at multi-step infra work) in Plan Mode (`Shift+Tab Shift+Tab`) so you see the plan before anything mutates.
2. **Keep the MBP awake** until Claude Code asks for the sleep-test step. After that, Claude Code will ask you to put it to sleep on demand.
3. **Have your Mac Mini accessible** — you'll paste verification command output back to Claude Code.
4. **Budget ~3–4 hours** end to end; most of that is the 20-sample benchmark runtime.
