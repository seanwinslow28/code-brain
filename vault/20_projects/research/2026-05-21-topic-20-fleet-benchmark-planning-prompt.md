---
type: planning-prompt
date: 2026-05-21
purpose: Paste-ready prompt for a fresh Claude Code session. Will invoke the `/writing-plans` skill to produce a thorough, executable plan for Topic 20 — pulling and benchmarking newer Ollama models (Qwen 3.5 / 3.6 / Nemotron3 / gemma4 26B-MoE) across Sean's 3-device fleet, with PC wake-on-LAN architecture for the Alienware so the desktop doesn't have to run overnight.
target_session: Fresh Claude Code session, working directory = /Users/seanwinslow/Code-Brain/code-brain
tags: [planning, topic-20, fleet-benchmark, ollama, wake-on-lan, paste-ready]
ai-context: "Paste-ready /writing-plans prompt for Topic 20 — pull and benchmark Qwen 3.5/3.6, Nemotron3, gemma4 26B-MoE across Sean's 3-device fleet with PC wake-on-LAN. The resulting plan is committed at agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md."
---

# Paste-Ready Prompt — Topic 20 Pull-and-Benchmark Plan

> **How to use:** Open a NEW Claude Code session in `/Users/seanwinslow/Code-Brain/code-brain`. Paste the fenced block below verbatim. The agent will read the required-context files, invoke the `/writing-plans` skill, and produce a complete executable plan.

---

```text
I need you to produce a thorough, executable plan for Topic 20 — pulling and benchmarking newer Ollama models on my actual hardware fleet, with a wake-on-LAN architecture for my Alienware PC so I don't have to leave it running overnight. The plan will be executed in a future session, so the level of detail matters — every step should be unambiguous, every decision pre-resolved, every command copy-pasteable.

REQUIRED READING — read these files IN ORDER before doing anything else. Do not skip any.

1. `/Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md`
   — Project conventions, fleet architecture, hardware tiers, current agent model assignments, the v3.14.3 WOL retirement note, and the operational constraints. Critical: this is what tells you about the 14-agent fleet, the HybridRouter, the launchd schedules, and the Mac-Mini-as-Ollama-host pattern.

2. `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/research/2026-05-21-topic-19-synthesis-optimal-ollama-models-pi.md`
   — The Topic 19 synthesis (baseline picks: qwen3-coder:30b for Tier A/B, devstral:24b-small-2505 for Tier C) AND the same-day correction addendum at the bottom of the file. The §Correction (2026-05-21) section names the candidate models for benchmark and explains why the prior synthesis missed them.

3. `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/research/2026-05-21-topic-16-pi-ollama-integration-chatgpt-manual.md`
   — Pi+Ollama integration recipe. Has the working models.json snippets, the `compat.supportsDeveloperRole: false` flag, the OLLAMA_HOST=0.0.0.0 setting for LAN access, and the Tailscale MagicDNS alternative.

4. `/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/config.toml`
   — Current HybridRouter routing rules, model assignments per agent, and budget caps. Tells you which agents currently call Qwen3-14B on MBP, which call gemma4:e4b on Mac Mini, and which fall back to cloud.

5. `/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md` and `/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/BUGFIX-2026-04-07-launchd-path.md`
   — Two prior decision records that document operational pitfalls Sean's hit before. The PATH bug in particular matters if any new model is invoked via launchd.

After reading those five files, invoke the `/writing-plans` skill and follow it exactly. The skill will tell you how to structure the plan, where to write it, and when to ask for clarification vs. when to proceed.

OBJECTIVE OF THE PLAN

Produce an executable plan that, in a future session, will:

A. Pull four candidate Ollama models on the correct hardware tiers.
B. Run a fixed benchmark suite on each candidate vs. the current production model for that tier.
C. Stand up a wake-on-LAN architecture so the Alienware (Tier C) can serve as a third always-on-on-demand Ollama host without being powered on 24/7.
D. Capture results in `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md` with proper frontmatter, source attribution, and decision recommendations per tier.
E. Surface the final adoption decisions: which models replace which current agents, which stay where they are, which get rejected and why.

CANDIDATE MODELS TO BENCHMARK

For each, the plan must specify which hardware tier to pull on, which Modelfile parameters to set (especially `num_ctx`), and the exact `ollama pull` command. Cross-check the sizes against the user's hardware budget before recommending pulls.

1. `qwen3.5:9b` — 6.6GB disk; Tier B (Mac Mini 24GB) primary candidate; potential drop-in replacement for Qwen3-14B currently running on the MBP via LM Studio
2. `qwen3.5:27b` — 17GB disk; Tier A or Tier B candidate; main upgrade path from `qwen3-coder:30b`
3. `qwen3.5:35b` — 24GB disk; Tier A (M4 Max MBP) primary candidate
4. `qwen3.6:35b` — 24GB disk; Tier A secondary candidate (newer, only 1.5M pulls — call out the lower confidence)
5. `nemotron3:33b` — 28GB disk; Tier C (RTX 4090 24GB VRAM, needs CPU offload OR a smaller-quant variant if one exists)
6. `gemma4:26b` (the MoE variant — 3.8B active / 25.2B total, 18GB) — Tier B candidate; benchmarks now published (LiveCodeBench v6: 77.1%, Codeforces ELO: 1718)

The CURRENT production models for comparison (what we're benchmarking AGAINST):

- Tier A (M4 Max MBP): Qwen3-14B running on LM Studio via the HybridRouter (used by vault_synthesizer, knowledge_lint, deep_researcher LDR loop, HybridRouter fallback)
- Tier B (Mac Mini 24GB): gemma4:e4b running on Ollama at localhost:11434 (used by meta_agent, flush.py, inbox_triage)
- Tier C (RTX 4090): currently UNUSED for agent fleet — this is the new tier we're standing up
- Baseline picks from the Topic 19 synthesis to also benchmark if practical: qwen3-coder:30b (Tier A/B) and devstral:24b-small-2505-q4_K_M (Tier C)

HARDWARE FLEET — CURRENT STATE

- Device 1: MacBook Pro M4 Max (Tier A) — Sean's interactive dev machine. Currently runs LM Studio with Qwen3-14B for the HybridRouter. Mobile / not always-on.
- Device 2: Mac Mini M4 Pro 24GB unified memory (Tier B) — always-on headless. Ollama running at localhost:11434, serves gemma4:e4b, nomic-embed-text (for vault indexer), and is the LAN endpoint for HybridRouter when MBP is asleep. Hardwired Ethernet to TP-Link Deco BE Pro (Deco 7 Pro) mesh router. Reachable on LAN as `mac-mini.local` or by static IP.
- Device 3: Alienware desktop with NVIDIA RTX 4090 24GB VRAM (Tier C) — currently OFF when not in interactive use. Hardwired Ethernet to the same TP-Link Deco BE Pro. Has CUDA-capable Ollama installed (verify in plan). NOT currently part of the agent fleet.

NETWORK TOPOLOGY

Both the Mac Mini and the Alienware are wired Ethernet to a TP-Link Deco BE Pro (Deco 7 Pro) mesh router. The router supports:
- Standard LAN broadcast (WoL magic packets propagate across the LAN)
- Tailscale (already in use elsewhere in the fleet for off-LAN access)
- mDNS / Bonjour for `.local` hostname resolution

The plan must specify whether to use raw LAN WoL (faster, requires both devices on the same subnet — they are) OR Tailscale wake (works off-LAN too, but Tailscale needs to be running on a sleeping/powered-off PC — verify possible) OR Wake-on-WAN via the Deco router admin UI (verify support).

THE NON-NEGOTIABLE CONSTRAINT

The Alienware MUST NOT be left powered on overnight. Sean is unemployed (post-The-Block layoff) and minimizing electricity cost matters. Two acceptable patterns:

Pattern A — On-demand WoL: Mac Mini sends a magic packet via the LAN to wake the Alienware before each scheduled agent run. The Alienware boots / wakes from sleep, runs the workload, and goes back to sleep on idle (Windows power plan or systemd-suspend, depending on OS — verify which OS is running on the Alienware in the plan).

Pattern B — Scheduled wake windows: Alienware self-wakes via Windows Task Scheduler (or equivalent) at preset times (e.g., 09:00, 13:00, 17:00 daily) and sleeps after configurable idle. Mac Mini hits the LAN endpoint during those windows, no magic-packet round-trip needed.

The plan must evaluate both patterns, recommend ONE primary, and document the fallback. Selection criteria: reliability (does it wake every time?), latency (how long from request → ready?), Sean-effort to maintain, and complexity of failure modes. Note that v3.14.3 of this repo RETIRED a prior WoL setup for the synthesizer specifically because the MBP wasn't reliably reachable — read that history before recommending. The Alienware case is different because it's stationary and Ethernet-only, but the prior retirement is signal that WoL+laptop is fragile.

BENCHMARK DIMENSIONS

For each candidate model, the plan must specify HOW to capture each dimension. Be specific about prompts, sample counts, success criteria, and capture format (where the results land in the vault).

1. Tool-calling correctness — % of tool calls that emit valid JSON matching the requested schema. Sample size ≥ 20 prompts per model. Use a fixed prompt set; the same prompts hit every model.
2. Tokens/sec (decode) — measured on a fixed 1024-token output, three runs, report mean + stddev.
3. Memory footprint — peak RSS during a typical Pi-style session (read file → edit file → bash command, repeated 5x). Use `htop`-style sampling on Mac, `Task Manager` snapshots on Windows if Alienware is Win-based.
4. Agentic-loop reliability — run a 10-step Pi session (or equivalent multi-tool loop) and count successful completions out of 10 attempts. Failure modes (truncated tool calls, schema breaks, infinite loops on edit) are reported separately.
5. Long-context degradation — feed each model a 32K-token prompt with a "needle" at the 28K mark; measure recall accuracy across 5 runs.
6. Pi-specific gotchas surfaced — does the model hit the streaming tool_call bug? The 2048-default num_ctx truncation? The compat.supportsDeveloperRole mismatch? Each gotcha is binary pass/fail.

For comparison, the same suite runs against the current production model on each tier (Qwen3-14B / gemma4:e4b / and either qwen3-coder:30b or devstral as the Topic 19 synthesis baselines if Sean wants to bring those into play too).

DELIVERABLES THE PLAN MUST SPECIFY

1. Where the final benchmark report lands: `vault/20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md` with `type: research-report`, proper frontmatter, links back to Topic 19 synthesis.
2. Where the wake-on-LAN architecture decision lands: `agents-sdk/docs/alienware-tier-c-wake-architecture-2026-05-21.md` as a decision record matching the style of existing records (see `local-tts-decision-record.md` in that folder for the template).
3. Where the benchmark scripts live: `agents-sdk/scripts/benchmark_ollama_model.py` (or equivalent — verify naming conventions match the existing scripts directory).
4. Configuration changes — which files in `agents-sdk/config.toml` get edited, what new launchd plists (if any) are needed under `agents-sdk/schedules/`, what changes to `.claude/settings.json` or hooks.
5. Rollback procedure — exactly how to undo each step if a model adoption turns out to be a regression. CLAUDE.md repeatedly emphasizes "rollback = X" — match that style.

ADDITIONAL CONTEXT — KNOWN PITFALLS

- The launchd PATH bug (see BUGFIX-2026-04-07-launchd-path.md) — any new launchd plist needs the full PATH env var or `claude` CLI won't be discoverable.
- Vault sync ownership — the shell-level auto-commit hook is the SOLE owner of vault git operations. Don't introduce a second auto-commit path even temporarily for benchmark capture (Issue #22 reference in CLAUDE.md).
- Qwen models support a `thinking` mode that can default-on and slow tool loops dramatically. Verify per-model whether thinking can be disabled per-call before recommending adoption.
- The Topic 19 synthesis correction (§Correction at the bottom of that file) explicitly flags that the prior synthesis had a methodology bias — the plan should NOT just rubber-stamp the original Tier A/B/C picks. Treat all candidates as equally viable until benchmark data lands.
- The Alienware's exact OS (Windows 11 vs Linux dual-boot vs Windows-only) is not currently documented in CLAUDE.md. The plan should include "step 0: confirm Alienware OS and current power-management state with Sean" if unknown.

WHEN TO STOP AND ASK

Per the `/writing-plans` skill conventions, ask for clarification before writing the plan if:
- The exact OS / power state of the Alienware is unknown after reading the required-context files.
- The benchmark sample size or success thresholds need product-decision input (i.e., "is 80% tool-call correctness good enough to migrate?").
- The wake-on-LAN approach surfaces a security implication Sean should weigh in on (LAN magic packets are fine; opening the Deco router admin UI for WAN-side wake might not be).

Otherwise: read the files, invoke `/writing-plans`, write the plan. Save it where the skill tells you to save it (typically `~/.claude/plans/<slug>.md`). When the plan is complete, surface the path back to Sean and STOP — execution happens in a future session, not this one.
```

---

## What this prompt will produce

The fresh Claude Code session will:

1. Read the 5 required-context files (CLAUDE.md, Topic 19 synthesis + correction, Topic 16 Pi+Ollama, agents-sdk/config.toml, the two prior decision records).
2. Invoke the `/writing-plans` skill, which will guide it through structured planning (objectives, decisions, work breakdown, rollback, success criteria).
3. Likely ask you 1–3 clarifying questions about the Alienware (its OS, current power state, whether you want raw WoL vs Tailscale vs Deco-router-WoL).
4. Save the plan to `~/.claude/plans/<slug>.md` (the `/writing-plans` skill chooses the path).
5. Surface the plan path back to you and stop.

You then review the plan, approve / revise, and execute it in a third session (the execution session). That gives you three sharp checkpoints: research → plan → execute, with you in control at each transition.

## Why a fresh session and not this one

Two reasons. First, this session is already thick with context (Pi research, the 8-file processing, the synthesis correction). The `/writing-plans` skill works best in a clean context where it can fully drive the agenda. Second, this gives you a clean handoff — the planning prompt above is self-contained and reproducible. If the first attempt produces a weak plan, you can re-run it with adjustments. If it works, the plan stands on its own as a vault artifact.

## My quick recommendation on the wake-on-LAN question (the plan will dig deeper)

Based on what I know about your topology:

**Pattern A (on-demand WoL) is probably right.** Both Mac Mini and Alienware are Ethernet to the same Deco — magic packets are dead-simple over wired LAN and require zero router cooperation. Mac Mini sends `wakeonlan <Alienware-MAC>` (or the Python equivalent in your agent), waits ~30s for the box to come up, runs the workload, the Alienware sleeps on idle.

**Pattern B (scheduled self-wake) is a good fallback** if WoL ever turns flaky, but adds the constraint of "workloads must align with wake windows."

**Avoid Pattern C (always-on with display off)** — that's the option Sean is explicitly ruling out.

The plan should still evaluate all three formally and document the choice with a one-paragraph decision record. Don't pre-decide — let the planning session weigh it with full context.
