# Phase 6 Wrap-up — Claude Code Prompt (simple path)

Copy the prompt between the `===` lines and paste into Claude Code (Opus 4.7, Plan Mode). Run this **on the MBP**, not the Mac Mini.

===

<role>
You are finishing Phase 6 of Sean's autonomous agent fleet. Prior plans specified cross-machine WOL between Mac Mini and MacBook Pro — that approach is cancelled. Everything that needs heavyweight local inference runs on the MacBook Pro directly. No WOL, no cross-machine routing.
</role>

<context>
Read these before acting:
- [agents-sdk/config.toml](../../../../agents-sdk/config.toml) — current routing + machine config
- [agents-sdk/scripts/run_gemma4_benchmark.py](../../../../agents-sdk/scripts/run_gemma4_benchmark.py) — benchmark runner (still has the LM Studio RAM bug)
- [agents-sdk/benchmarks/results/A6-swap-decision-2026-04-17.md](../../../../agents-sdk/benchmarks/results/A6-swap-decision-2026-04-17.md) — prior 5-sample partial report
- [CHANGELOG.md](../../../CHANGELOG.md) v3.14.0 for what Phase 6 already shipped

Current state: Gemma 4 31B is loaded in LM Studio on this MBP at port 1234. Qwen3-14B and Qwen2.5-Coder-32B are also pulled. Prior benchmark was 5 samples, inbox_triage only, with Gemma 4 losing by 15pp. That was enough data to keep incumbents but not enough to close the phase.
</context>

<task>
Four things, in order. Don't advance until each is green.

1. **Revert any WOL-era changes to `agents-sdk/config.toml`.** If `[routing.machines.macbook_pro]` has anything other than `host = "127.0.0.1"`, `port = 1234`, `runtime = "lm-studio"`, and no `wol_mac`, revert it. Confirm with `git diff config.toml` before and after.

2. **Fix the LM Studio RAM bug in `scripts/run_gemma4_benchmark.py`.** Simplest fix: before each task's incumbent and challenger run, POST `{"keep_alive": 0}` to force unload via the OpenAI-compatible endpoint, OR call `subprocess.run(["lms", "unload", "--all"], check=False)`. Test both and use whichever actually works on Sean's LM Studio install. Ask Sean via `AskUserQuestion` to confirm "Just-in-Time Model Loading" is ON and "Keep models loaded" is OFF in LM Studio Developer settings — that makes the fix reliable.

3. **Run the full benchmark.** From MBP:
   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 scripts/run_gemma4_benchmark.py --samples 20
   ```
   All 3 tasks × 2 models × 20 samples. Expect ~2–3h runtime. If any task fails with RAM errors, stop and fix #2 first.

4. **Apply the veto gate per task and write `benchmarks/results/A6-swap-decision-<today>.md`:**
   - Gemma 4 ≥5pp worse → KEEP incumbent
   - Gemma 4 within ±5pp but ≥20% faster → SWAP
   - Gemma 4 ≥5pp better → SWAP
   Update `config.toml` `[routing.task_map]` only for tasks where swap wins. Report each task's verdict with exact numbers. Compare back to the April 17 5-sample numbers so we understand what changed.

5. **Move the two nightly plists from Mac Mini to MBP.** These currently live on the Mac Mini but need to run where the models are:
   - `com.sean.agent.vault-synthesizer.plist` (2:30 AM nightly)
   - `com.sean.agent.knowledge-lint.plist` (Sunday 22:00)
   Tell Sean the exact shell commands to run on his Mac Mini (unload + remove symlink) and on his MBP (install + load). Use `AskUserQuestion` to confirm when he's done each side. When MBP sleeps through a scheduled time, launchd queues and fires on next wake — this is the intended behavior, no further work needed.

6. **Update `CHANGELOG.md`** under a new `[3.14.1]` entry:
   - A.6 re-run at N=20 with per-task verdicts
   - WOL path abandoned; plists relocated to MBP
   - LM Studio RAM fix in benchmark runner
   Do NOT modify `SOURCE-OF-TRUTH.md` or `CLAUDE.md` routing table unless an actual swap occurred.

7. **Run validation.** `python3 scripts/validate.py` and `cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/ -v`. Both must be green before you report done.
</task>

<constraints>
- 100% local, $0.00 API spend.
- No cross-machine routing. No WOL. No hybrid_router changes unless a test breaks.
- Two commits: one for the benchmark fix + results, one for the plist relocation. Don't push.
- Sean is a code beginner. When you give him shell commands to run manually, explain what each one does in one line.
- If Gemma 4 loses all three tasks, that's still a clean result — commit the report and mark gate criterion #2 PARTIAL per plan §5 fallback.
</constraints>

<deliverables>
Final summary message:
1. Per-task benchmark table (N=20) with veto verdicts
2. Which swaps (if any) you applied to config.toml
3. Gate-check status (run `python3 agents-sdk/scripts/phase6_gatecheck.py`)
4. Confirmation Sean successfully moved both plists to MBP
5. One short paragraph in plain English for Sean: what changed, what to expect tonight, whether Gemma 4 is now in his stack
</deliverables>

===

## Before pasting

1. Open Claude Code **on the MBP** (not the Mac Mini) so the benchmark runs against local LM Studio
2. Plan Mode on (`Shift+Tab` twice)
3. LM Studio: keep the local server toggle ON, port 1234. Gemma 4 31B doesn't need to be preloaded — JIT handles it
4. Budget ~3 hours, mostly benchmark runtime — you can step away

## Why this version is shorter

The earlier prompt had 170+ lines because it was threading WOL wiring, MBP IP discovery, live sleep-wake verification, and cross-machine test coverage. Cutting WOL removes all of that. What's left is a straight "run the benchmark, apply the gate, move two files" sequence — which is what you wanted from the start.
