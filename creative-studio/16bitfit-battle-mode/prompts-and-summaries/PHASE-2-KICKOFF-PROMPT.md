# Phase 2 Kickoff Prompt for Claude Code

## How to Use This

**Before pasting this prompt into Claude Code**, make sure:
1. Phase 1 is complete (all 6 tasks passed, smoke test 16/16)
2. API keys are in macOS Keychain (not .env)
3. The .env file has been deleted
4. You're starting from the `claude-code-superuser-pack` root directory

---

## YOUR MANUAL CHECKLIST (Do These First)

- [ ] Delete the `.env` file from `agents-sdk/` (credentials are in Keychain now)
- [ ] Confirm all three machines are online:
  - `curl http://192.168.68.200:11434/api/tags` → Mac Mini responds
  - `curl http://192.168.68.201:11434/api/tags` → Alienware responds
- [ ] Sign up for Replicate (https://replicate.com/) if you want to test rd-animation — store key: `python3 lib/keychain.py set replicate-key YOUR_KEY`
- [ ] Sign up for Kling AI (https://klingai.com/) if you want to test Kling 3.0/2.6 — store key when available

> **Note:** Replicate and Kling are optional for Phase 2. You already have fal.ai (Pika) and Google AI (Gemini) keys stored, which are the highest-priority video model tests.

---

## THE CLAUDE CODE PROMPT

Paste everything below the line into Claude Code, starting a session from the `claude-code-superuser-pack` root directory.

---

```
You are continuing the 16BitFit Battle Mode build — Phase 2 of a 12-week project. Phase 1 is complete: three-machine fleet is online, hybrid_router.py works, safety hooks are installed, keychain.py is live, and the Pixel Quantizer gate check PASSED with synthetic frames.

<role>
You are a senior systems engineer and creative pipeline architect. Phase 2 has two parallel workstreams: building the first autonomous agents (Workstream A) and running a video model evaluation sprint (Workstream B). You write clean, typed, tested code. You follow hexagonal/ports-and-adapters architecture. You audit for safety before deploying any autonomous agent.
</role>

<context>
Read these files in this exact order before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference (Parts 1-4, focus on Phase 2 checklist)
3. `16bitfit-battle-mode/docs/agent-sdk/phase-2-synthesis.md` — Agent architecture spec (Sections 1-6 most relevant: agent fleet spec, skills audit, safety, hooks, multi-agent coordination)
4. `16bitfit-battle-mode/docs/sprite-pipeline/video-model-kickoff.md` — Video model evaluation plan and success criteria
5. `16bitfit-battle-mode/docs/validation/opportunity-scan.md` — New tools discovered (rd-animation, Ludo.ai, PixelLab, GMFSS Fortuna, Wan 2.2 LoRAs)
6. `16bitfit-battle-mode/docs/sprite-pipeline/hybrid-pipeline-plan.md` — Hybrid pipeline architecture

After reading, confirm you understand the two-workstream structure, the skills audit requirement, and the video model evaluation criteria before proceeding.
</context>

<machine_ips>
Mac Mini LAN IP: 192.168.68.200
Alienware LAN IP: 192.168.68.201
MacBook Pro: localhost (this machine)
</machine_ips>

<phase1_artifacts>
These were built in Phase 1 and are available for use:
- `agents-sdk/config.toml` — routing config with all 3 machines + 8 task mappings
- `agents-sdk/lib/keychain.py` — macOS Keychain credential helper (6 API keys stored)
- `agents-sdk/lib/hybrid_router.py` — three-tier routing with WOL, fallback chain
- `.claude/hooks/loop-detector.py` — exit code 2 on 3rd duplicate tool call
- `.claude/hooks/cost-watchdog.py` — exit code 2 when session exceeds $0.50
- `.claude/hooks/vault-integrity.py` — exit code 2 on empty anchor
- `sprite-sheet-automation-2026/src/tools/quantizer/` — Pixel Quantizer (7-step pipeline, 13 tests passing)
- Smoke test: 16/16 passing with real machine connectivity
</phase1_artifacts>

<constraints>
CRITICAL — same constraints as Phase 1, plus new ones for autonomous agents:
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Never use `dangerouslySkipPermissions` — not even for creative pipeline agents
- Credentials come from macOS Keychain via `lib/keychain.py`, not .env files
- RTX 5080 uses SDPA attention (NO xformers)
- Mac Mini runs `phi4-mini-reasoning` (3.8B), NOT "phi4" (14B)
- Alienware vision model is `qwen3-vl:8b` (NOT `qwen3-vl:7b`)
- Before building any agent, AUDIT its skill files for interactive language ("ask me", "confirm with user", "review with the user") — these will cause autonomous agents to hang and burn budget. Replace with autonomous decision criteria.
- Sprite pipeline uses hexagonal architecture — all external tools behind Adapter interfaces
- Video model tests must use the "green screen before video" technique — chroma key (#00FF00) on keyframes BEFORE feeding to video models
</constraints>

<tasks>
Build the following. Workstream A and B are independent — you may interleave them, but complete each task's verification before moving on.

=== WORKSTREAM A: FIRST AUTONOMOUS AGENTS ===

TASK 1: Skills Audit for Autonomous Operation
- Grep ALL skill files in `.claude/skills/` for interactive patterns: "ask me", "confirm with", "review with the user", "what would you like", "let me know", "would you prefer"
- For each match, document: file, line number, current text, proposed replacement
- Replace interactive prompts with autonomous decision criteria:
  - `daily-driver`: Use `vault/02_Areas/Focus.md` for focus decisions instead of asking
  - `process-inbox`: Use confidence-threshold routing (<80% confidence → tag as `#triage/human`) instead of confirming tags
  - `personal-finance`: Output structured markdown table instead of asking user to review anomalies
- VERIFY: Re-grep after changes — zero matches for interactive patterns

TASK 2: Build Process Inbox Agent
- Location: `agents-sdk/agents/process_inbox.py`
- Runs on Mac Mini, 100% local (`phi4-mini-reasoning` via Ollama at 192.168.68.200)
- Reads unprocessed inbox notes from vault, classifies and tags them
- Confidence threshold: ≥80% → auto-tag, <80% → tag as `#triage/human` for manual review
- On success: touch `~/.claude/batons/inbox_done.flag` (Baton File pattern)
- Load skill via skill_loader.py, use existing keychain.py for any credentials
- Safety: max 15 turns, $0.25 budget cap
- VERIFY: Run with `--dry-run` flag. Confirm it reads the skill, routes to Mac Mini, and would process a sample inbox note

TASK 3: Build Spending Analysis Agent
- Location: `agents-sdk/agents/spending_analysis.py`
- Runs on MacBook Pro, 100% local (Qwen3-14B via MLX-LM)
- Reads sanitized financial CSVs, analyzes spending patterns, outputs to vault
- Build `agents-sdk/lib/csv_sanitizer.py` first: strips account numbers, hashes transaction IDs, outputs clean JSON
- Output format: structured markdown table in vault, NOT interactive review
- Safety: max 20 turns, $0.25 budget cap
- VERIFY: Run with `--dry-run` and a sample CSV (create a synthetic test CSV with fake transactions)

TASK 4: Implement Baton File Dependency Chain
- Process Inbox creates `~/.claude/batons/inbox_done.flag` on success
- Daily Driver's launchd plist should use `WatchPaths` targeting that flag file
- Update `agents-sdk/schedules/` with the new plist configuration
- Build `agents-sdk/lib/baton.py` — utility for creating, checking, and cleaning up baton files
- VERIFY: Simulate the chain: create the baton file manually → confirm the WatchPaths trigger logic is correct

=== WORKSTREAM B: VIDEO MODEL EVALUATION SPRINT ===

TASK 5: Build Video Model Evaluation Framework
- Location: `sprite-sheet-automation-2026/src/tools/video-eval/` (or similar)
- Create a standardized evaluation harness that:
  - Takes a model name, keyframe images (start/end pose), and config
  - Calls the model's API to generate video
  - Extracts frames from the video output
  - Runs extracted frames through the Pixel Quantizer
  - Scores results: frame count, palette compliance, outline quality, character consistency
  - Outputs a structured evaluation report (JSON + visual grid)
- Build adapter interfaces for each video model (hexagonal architecture):
  - `PikaAdapter` — uses fal.ai API (key in Keychain as `fal-ai-key`)
  - `GeminiAdapter` — uses Google AI API for Nano Banana Pro/2 keyframe generation (key as `google-ai-key`)
  - Stub adapters for: `KlingAdapter`, `ReplicateAdapter` (rd-animation), `Wan22Adapter` (local ComfyUI)
- VERIFY: Run the framework with a mock/stub adapter that returns synthetic video frames → confirm the full evaluation pipeline (extract → quantize → score → report) works end-to-end

TASK 6: Test Nano Banana Pro vs Nano Banana 2 for Keyframe Quality
- Use the GeminiAdapter to generate test keyframes with both models:
  - Nano Banana Pro: `gemini-3-pro-image-preview`
  - Nano Banana 2: `gemini-3.1-flash-image-preview` (or current model string — verify via API)
- Generate start pose and end pose for a walk cycle using the Sean character reference:
  - Skin: #F5D6C6, Hair: #C2A769, Eyes: #4682B4, Tank Top: #F2F0EF, Pants: #2323FF, Shoes: #F5F5F5
  - Use chroma key green (#00FF00) background
  - 128×128 target, SF2 pixel art style, bold #272929 outlines
- Score both models on: palette accuracy, outline clarity, character consistency, generation speed
- VERIFY: Output a comparison report with side-by-side results

TASK 7: Test Pika Pikaframes 2.2 Video Interpolation
- Generate 3-4 keyframes with the winning Gemini model from Task 6
- Feed keyframes to Pika via fal.ai API (PikaAdapter)
- Use the "green screen before video" technique: ensure chroma key background on keyframes BEFORE sending to Pika
- Generate 1-second video clip for the walk cycle
- Extract frames from the video output
- Run extracted frames through the Pixel Quantizer
- VERIFY: Document results with the evaluation framework from Task 5. Report: did the quantizer produce acceptable pixel art from REAL video output? This is the TRUE gate check.

TASK 8: Write Phase 2 Completion Summary
- Summarize all task results (PASS/FAIL for each)
- Report the video model evaluation results — which model(s) produced usable output?
- Document the "real frame" Pixel Quantizer gate check result (from Task 7)
- List any issues that need updating in SOURCE-OF-TRUTH.md
- Recommend which video models to pursue further in Phase 3
- Identify what I need to do manually before Phase 3

</tasks>

<output_format>
For each task:
1. Read the relevant reference docs first
2. Write the code
3. Run the verification step
4. Report: PASS or FAIL with details
5. If FAIL, fix and re-verify before moving on

After all tasks complete, provide the Phase 2 Completion Summary (Task 8).
</output_format>

<validation>
Before finishing, self-check:
1. Did you audit ALL skill files for interactive patterns before building agents?
2. Did you use `claude-agent-sdk` and `ClaudeAgentOptions` everywhere?
3. Are all credentials accessed via keychain.py, not .env or hardcoded?
4. Does Process Inbox route to Mac Mini (192.168.68.200) and use phi4-mini-reasoning?
5. Does Spending Analysis route to MacBook Pro (localhost) and use Qwen3-14B via MLX-LM?
6. Do both agents respect their budget caps ($0.25 each)?
7. Does the Baton File chain work: Process Inbox success → flag file → Daily Driver triggers?
8. Are video model adapters behind proper hexagonal interfaces?
9. Did you apply "green screen before video" on keyframes before sending to Pika?
10. Did you run ALL verification steps and do they pass?
</validation>
```

---

## What Happens After

Once Claude Code completes these 8 tasks, you'll have:

**Built by Claude Code:**
- Audited skill files (interactive patterns removed)
- `agents-sdk/agents/process_inbox.py` — first autonomous agent, 100% local
- `agents-sdk/agents/spending_analysis.py` — second autonomous agent, 100% local
- `agents-sdk/lib/csv_sanitizer.py` — financial data airgap
- `agents-sdk/lib/baton.py` — inter-agent dependency utility
- Updated launchd plists with WatchPaths triggers
- Video model evaluation framework with adapter interfaces
- Nano Banana Pro vs Nano Banana 2 comparison report
- Pika interpolation test results + real-frame Pixel Quantizer gate check

**Your next manual steps after Claude Code finishes:**
1. Review the skills audit changes — make sure autonomous replacements make sense
2. Test Process Inbox with real vault inbox notes (without --dry-run, on Mac Mini)
3. Test Spending Analysis with a real bank CSV export
4. If Pika results are promising → sign up for Kling and Replicate to test more models
5. If Pika results are poor → evaluate rd-animation, PixelLab, and Ludo.ai as alternatives
6. Purchase Sprite Smithy ($30) as a reference/sanity check tool
7. Proceed to Phase 3 (Pipeline Integration + PM Agents)
