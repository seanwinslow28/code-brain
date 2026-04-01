# Phase 3 Kickoff Prompt for Claude Code

## How to Use This

**Before pasting this prompt into Claude Code**, make sure:
1. Phase 2 is complete (7/8 tasks passed, Pika deferred)
2. The `.env` file has been deleted from `agents-sdk/`
3. New launchd plists are installed on Mac Mini (process-inbox + daily-morning-baton)
4. All three machines are online
5. You have a Replicate API key stored: `python3 lib/keychain.py set replicate-key YOUR_KEY`

---

## YOUR MANUAL CHECKLIST (Do These First)

- [ ] Delete `.env` from `agents-sdk/` if not done already
- [ ] Install launchd plists on Mac Mini — copy `agents-sdk/schedules/com.sean.agent.process-inbox.plist` and `com.sean.agent.daily-morning-baton.plist` to Mac Mini, then run `install_schedules.sh`
- [ ] Sign up for Replicate (https://replicate.com/) and store key: `python3 lib/keychain.py set replicate-key YOUR_KEY`
- [ ] Confirm machines are online:
  - `curl http://192.168.68.200:11434/api/tags` → Mac Mini
  - `curl http://192.168.68.201:11434/api/tags` → Alienware
- [ ] Verify ComfyUI launches on the Alienware with `--fp16-intermediates` flag

---

## THE CLAUDE CODE PROMPT

Paste everything below the line into Claude Code, starting a session from the `claude-code-superuser-pack` root directory.

---

```
You are continuing the 16BitFit Battle Mode build — Phase 3 of a 12-week project. Phase 1 (infrastructure) and Phase 2 (first agents + evaluation framework) are complete. The three-machine fleet is online, two autonomous agents are built, and the Pixel Quantizer gate check PASSED with synthetic frames. NB2 (Gemini Flash) won the keyframe benchmark (26% faster, comparable quality). Pika was scrapped — too expensive and unreliable.

Phase 3 focuses on two things: testing the FREE/LOCAL video models (Wan 2.2 LoRAs on the Alienware + rd-animation via Replicate) and building the PM-layer agents. The video model tests will determine whether the hybrid pipeline actually works with real video output.

<role>
You are a senior systems engineer and creative pipeline architect. Phase 3 has two parallel workstreams: PM-layer autonomous agents (Workstream A) and video model testing with hybrid pipeline integration (Workstream B). You write clean, typed, tested code. You follow hexagonal/ports-and-adapters architecture. You test video model output through the Pixel Quantizer to validate real-world results.
</role>

<context>
Read these files in this exact order before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference (Phase 3 checklist in Part 4)
3. `16bitfit-battle-mode/docs/agent-sdk/phase-2-synthesis.md` — Agent architecture (Section 1: agent fleet spec for Sprint Health Monitor + Meeting Defender)
4. `16bitfit-battle-mode/docs/sprite-pipeline/hybrid-pipeline-plan.md` — Hybrid pipeline architecture (4 atomic operations, strategy router, adapter interfaces)
5. `16bitfit-battle-mode/docs/validation/opportunity-scan.md` — Wan 2.2 LoRAs (Section 6), GMFSS Fortuna (Section 2), rd-animation + Ludo.ai (Section 1)
6. `16bitfit-battle-mode/docs/sprite-pipeline/workflow-operations-guide.md` — ComfyUI workflow patterns
7. `16bitfit-battle-mode/phase-2-completion-summary.md` — What was built in Phase 2 (video-eval framework, adapters, keyframe results)

After reading, confirm you understand:
- The 4 atomic adapter operations (generateFrame, generateKeyframes, interpolateFrames, generateVideo)
- The Wan 2.2 LoRA pipeline: static sprite → Wan 2.2 I2V + pixel animation LoRA → extract frames → Pixel Quantizer
- The rd-animation pipeline: anchor image → Replicate API → pixel art animation output (may bypass quantizer)
- The Sprint Health Monitor and Meeting Defender agent specs
</context>

<machine_ips>
Mac Mini LAN IP: 192.168.68.200
Alienware LAN IP: 192.168.68.201
MacBook Pro: localhost (this machine)
</machine_ips>

<phase2_artifacts>
These were built in Phase 2 and are available for use:
- `agents-sdk/agents/process_inbox.py` — Process Inbox agent (Mac Mini, 100% local)
- `agents-sdk/agents/spending_analysis.py` — Spending Analysis agent (MacBook Pro, 100% local)
- `agents-sdk/lib/baton.py` — inter-agent dependency utility
- `agents-sdk/lib/csv_sanitizer.py` — financial data airgap
- `16bitfit-battle-mode/pixel-quantizer/video-eval/` — evaluation framework with hexagonal adapters
- `16bitfit-battle-mode/pixel-quantizer/video-eval/adapters.py` — GeminiAdapter (working), PikaAdapter (scrapped), stubs for Kling/Replicate/Wan22
- `eval-results/keyframe-*.png` — NB2-generated keyframes (walk cycle start/mid/end poses, green background)
- Skills audited: zero interactive patterns remaining
</phase2_artifacts>

<constraints>
CRITICAL — all previous constraints still apply, plus:
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Never use `dangerouslySkipPermissions`
- Credentials come from macOS Keychain via `lib/keychain.py`
- RTX 5080: SDPA only (NO xformers — crashes on sm_120). Use `--fp16-intermediates` with ComfyUI.
- Wan 2.2 is the latest OPEN SOURCE version. Do NOT use Wan 2.5 — it is NOT open source.
- Mac Mini runs `phi4-mini-reasoning` (3.8B), NOT "phi4" (14B)
- Alienware vision model is `qwen3-vl:8b` (NOT `qwen3-vl:7b`)
- All video model adapters go behind the `VideoModelAdapter` hexagonal interface
- Use "green screen before video" technique — chroma key (#00FF00) on keyframes BEFORE feeding to video models
- 1-second clips for combat animations, 2-second clips for walk cycles
</constraints>

<tasks>
Build the following. Workstream A and B are independent — you may interleave them.

=== WORKSTREAM A: PM-LAYER AGENTS ===

TASK 1: Set up mcp-atlassian with Keychain credentials
- Check if the Jira MCP (mcp-atlassian or claude.ai Atlassian) is already configured
- If credentials are needed, retrieve from Keychain or guide me on what to store
- Verify the MCP can reach Jira and list projects
- VERIFY: Run a test query against Jira (list projects or get a recent issue)

TASK 2: Build Sprint Health Monitor Agent
- Location: `agents-sdk/agents/sprint_health.py`
- Routes to: Mac Mini → Claude Sonnet via API (needs Jira MCP for data access)
- Reads current sprint from Jira, analyzes velocity, flags at-risk stories
- Outputs sprint health report to vault
- Safety: max 15 turns, $0.50 budget cap (needs API for Jira access)
- Trigger: runs on-demand or weekly (Friday 3:00 PM via launchd)
- VERIFY: Run with `--dry-run` flag. Confirm it can read sprint data from Jira.

TASK 3: Build Meeting Defender Agent
- Location: `agents-sdk/agents/meeting_defender.py`
- Routes to: Mac Mini for pre-classification (phi4-mini-reasoning), Claude Haiku for synthesis
- Reads calendar for the upcoming week, identifies meetings that could be declined
- Drafts Slack DMs for declinable meetings (NEVER auto-declines — drafts only)
- Output: markdown table in vault with meeting name, recommendation (keep/decline/shorten), draft message
- Safety: max 10 turns, $0.25 budget cap
- Trigger: Weekly (Monday 7:00 AM via launchd)
- VERIFY: Run with `--dry-run` flag. Confirm it reads calendar events and generates recommendations.

=== WORKSTREAM B: VIDEO MODEL TESTING + HYBRID PIPELINE ===

TASK 4: Set up Wan 2.2 on Alienware via ComfyUI
- Build a ComfyUI workflow JSON for Wan 2.2 image-to-video with LoRA support
- The workflow should:
  - Accept a static sprite image as input (the NB2 keyframes from Phase 2)
  - Load a pixel animation LoRA (styly-agents/Wan2-2-pixel-animate, 2.3GB)
  - Generate a 1-2 second video clip
  - Use chroma key green (#00FF00) background preservation
- Download the LoRA: `styly-agents/Wan2-2-pixel-animate` from HuggingFace (https://huggingface.co/styly-agents/Wan2-2-pixel-animate)
- Also download the CivitAI attack LoRA if accessible: https://civitai.com/models/2085866
- Build the `Wan22Adapter` in `video-eval/adapters.py` — calls ComfyUI REST API on the Alienware (192.168.68.201:8188)
- VERIFY: Submit the workflow to ComfyUI via REST API, confirm it queues successfully. If ComfyUI isn't running, document the exact launch command for the Alienware.

TASK 5: Set up GMFSS Fortuna Frame Interpolation in ComfyUI
- Install the ComfyUI-Frame-Interpolation node pack (Fannovel16/ComfyUI-Frame-Interpolation) on the Alienware
- Build a ComfyUI workflow that takes 3-4 keyframes and interpolates between them using GMFSS Fortuna
- This is the LOCAL, FREE alternative to Pika for the interpolation step
- Build a `GMFSSAdapter` in `video-eval/adapters.py`
- VERIFY: Test with the NB2 keyframes from Phase 2 — does GMFSS produce smooth interpolation?

TASK 6: Build rd-animation Adapter (Replicate)
- Implement the `ReplicateAdapter` in `video-eval/adapters.py`
- Uses Replicate API (key in Keychain as `replicate-key`) to call Retro Diffusion rd-animation
- rd-animation generates pixel art animations directly — may bypass the Pixel Quantizer entirely
- Input: anchor image + animation description
- Output: animated sprite frames
- VERIFY: Run a test generation with the Sean character anchor. Document quality results.

TASK 7: Build Generator Adapter Interface (4 Atomic Operations)
- Location: in the sprite pipeline project (`sprite-sheet-automation-2026/`)
- Implement the typed adapter interfaces from the hybrid pipeline plan:
  - `generateFrame` — single frame from anchor + pose ref (image-only strategy)
  - `generateKeyframes` — 3-5 keyframes for video interpolation (hybrid strategy)
  - `interpolateFrames` — video model fills between keyframes (Wan 2.2 or GMFSS)
  - `generateVideo` — motion transfer from reference video (experimental, stub for now)
- Wire adapters: GeminiAdapter for generateFrame/generateKeyframes, Wan22Adapter for interpolateFrames, ReplicateAdapter as alternative
- Build a strategy router that selects image-only vs hybrid per animation type based on manifest config
- VERIFY: Run the full hybrid pipeline end-to-end with stub/mock data. Confirm the router selects the correct strategy.

TASK 8: Run Real Video Model Tests Through Pixel Quantizer
- This is the TRUE gate check — real video output through the full pipeline
- Test 1: NB2 keyframes → Wan 2.2 + pixel animate LoRA → extract frames → Pixel Quantizer → score
- Test 2: NB2 keyframes → GMFSS Fortuna interpolation → extract frames → Pixel Quantizer → score
- Test 3: rd-animation via Replicate → evaluate output directly (may not need quantizer)
- For each test, use the evaluation framework from Phase 2 to score: palette compliance, outline quality, character consistency, background removal
- Apply green screen technique: chroma key on keyframes BEFORE feeding to video models
- Use 2-second clips for walk cycle, 1-second for combat
- VERIFY: Document results for each model. Which produces the best output? Does the Pixel Quantizer handle real video "sludge"?

TASK 9: End-to-End Hybrid Pipeline Test (1 Champion Walk Cycle)
- Run the FULL pipeline for one complete animation:
  1. Generate keyframes with NB2 (GeminiAdapter) — walk cycle start/mid/end poses
  2. Interpolate with the BEST video model from Task 8
  3. Extract frames (target: 8 frames for walk cycle)
  4. Run through Pixel Quantizer (all 7 steps)
  5. Audit frames (palette, outline, dimensions, alpha)
  6. Pack into atlas sheet (if existing packer is available)
  7. Validate in headless Phaser (if validator is available)
- If packer/validator aren't wired up yet, stop after step 5 and document
- VERIFY: Does the walk cycle look like SF2-quality pixel art? Are left/right legs correctly differentiated? Is the animation smooth?

TASK 10: Phase 3 Completion Summary
- Summarize all task results (PASS/FAIL)
- Video model ranking: which model(s) produced the best sprite animation output?
- Real-frame Pixel Quantizer gate check: PASS/FAIL/NEEDS WORK for each model
- Hybrid pipeline viability assessment: is the keyframe → video → quantize approach working?
- Compare: hybrid pipeline vs rd-animation (does rd-animation bypass the need for the quantizer?)
- List issues for SOURCE-OF-TRUTH.md
- Recommend the video model strategy going forward
- What I need to do manually before Phase 4

</tasks>

<output_format>
For each task:
1. Read the relevant reference docs first
2. Write the code
3. Run the verification step
4. Report: PASS or FAIL with details
5. If FAIL, fix and re-verify before moving on

After all tasks complete, provide the Phase 3 Completion Summary (Task 10).
</output_format>

<validation>
Before finishing, self-check:
1. Did you use `claude-agent-sdk` and `ClaudeAgentOptions` everywhere?
2. Are all credentials accessed via keychain.py?
3. Does Sprint Health Monitor use Jira MCP for data access?
4. Does Meeting Defender ONLY draft messages (never auto-decline)?
5. Are Wan 2.2 and GMFSS workflows targeting the Alienware (192.168.68.201)?
6. Did you use Wan 2.2 (NOT Wan 2.5)?
7. Did you apply green screen BEFORE feeding keyframes to video models?
8. Are all video adapters behind the VideoModelAdapter hexagonal interface?
9. Did you run real video output through the Pixel Quantizer (not just synthetic frames)?
10. Does the strategy router correctly select image-only vs hybrid per animation type?
</validation>
```

---

## What Happens After

Once Claude Code completes these 10 tasks, you'll have:

**Built by Claude Code:**
- Jira MCP connection verified
- `agents-sdk/agents/sprint_health.py` — Sprint Health Monitor (Jira-connected)
- `agents-sdk/agents/meeting_defender.py` — Meeting Defender (calendar audit, draft-only)
- Wan 2.2 ComfyUI workflow with pixel animation LoRAs on Alienware
- GMFSS Fortuna interpolation workflow on Alienware
- `Wan22Adapter`, `GMFSSAdapter`, `ReplicateAdapter` — all behind hexagonal interfaces
- Generator adapter interface (4 atomic operations) in sprite pipeline
- Strategy router (image-only vs hybrid per animation)
- Real video model test results + Pixel Quantizer gate check with actual video output
- End-to-end hybrid pipeline test: 1 Champion walk cycle

**Your next manual steps after Claude Code finishes:**
1. Review the video model test results — which model won?
2. Review the walk cycle output — does it look like SF2 pixel art?
3. Install Sprint Health Monitor + Meeting Defender launchd plists on Mac Mini
4. Test Meeting Defender with your real calendar
5. If hybrid pipeline works → proceed to Phase 4 (LoRA training + scale to full roster)
6. If hybrid pipeline fails but rd-animation works → pivot to rd-animation as primary path
7. If both fail → evaluate PixelLab v3 and Ludo.ai MCP as alternative approaches
