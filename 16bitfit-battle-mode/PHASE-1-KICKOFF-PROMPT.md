# Phase 1 Kickoff Prompt for Claude Code

## How to Use This

**Before pasting this prompt into Claude Code**, complete the manual setup checklist below. Claude Code can write code but can't install software on your other machines.

---

## YOUR MANUAL SETUP CHECKLIST (Do These First)

Complete these on each machine before starting Claude Code. They take ~2-3 hours total and can all be done in parallel.

### Mac Mini (always-on orchestrator)

- [ ] Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
- [ ] Verify: `ollama --version` → expect `0.5.x`
- [ ] Pull models: `ollama pull phi4-mini-reasoning && ollama pull nomic-embed-text`
- [ ] Set LAN access: `launchctl setenv OLLAMA_HOST "0.0.0.0:11434"` → restart Ollama
- [ ] Verify LAN: from MacBook, `curl http://{MINI_IP}:11434/api/tags` → should list models
- [ ] Install Python 3.12: `brew install python@3.12`
- [ ] Clone/sync the superuser pack repo to Mac Mini
- [ ] Create venv: `cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk && python3.12 -m venv .venv`
- [ ] Install SDK: `source .venv/bin/activate && pip install claude-agent-sdk filelock toml httpx`
- [ ] Verify SDK: `python3 -c "from claude_agent_sdk import ClaudeAgentOptions; print('OK')"`
- [ ] Note the Mac Mini's LAN IP: `ipconfig getifaddr en0` → write it down

### MacBook Pro (your dev machine — where Claude Code runs)

- [ ] Install MLX-LM: `pip install mlx-lm`
- [ ] Pull models:
  ```bash
  mlx_lm.download --model mlx-community/Qwen3-14B-4bit
  mlx_lm.download --model mlx-community/Qwen2.5-Coder-32B-Instruct-4bit
  ```
- [ ] Quick test: `mlx_lm.generate --model mlx-community/Qwen3-14B-4bit --prompt "Hello" --max-tokens 20`
- [ ] Ensure Node.js 20+ is installed: `node --version`
- [ ] Ensure the superuser pack repo is up to date

### Alienware (CUDA specialist)

- [ ] Install Ollama for Windows: https://ollama.com/download/windows
- [ ] Set env vars (System Properties → Environment Variables):
  - `OLLAMA_HOST` = `0.0.0.0:11434`
  - `OLLAMA_KEEP_ALIVE` = `2m`
- [x] Pull model: `ollama pull qwen3-vl:8b` (note: Ollama tags this as 8b, not 7b)
- [x] Verify: `ollama run qwen3-vl:8b "Describe this test." /bye`
- [ ] Update ComfyUI to v0.18.2+. Launch with `--fp16-intermediates` flag
- [ ] Verify LAN: from MacBook, `curl http://{ALIENWARE_IP}:11434/api/tags` → should list model
- [ ] Note the Alienware's LAN IP → write it down

### After All Machines Are Online

- [ ] Confirm you can reach Mac Mini from MacBook: `curl http://{MINI_IP}:11434/api/tags`
- [ ] Confirm you can reach Alienware from MacBook: `curl http://{ALIENWARE_IP}:11434/api/tags`
- [ ] Store any API keys in macOS Keychain (fal.ai, etc.) — Claude Code will build the helper

---

## THE CLAUDE CODE PROMPT

Paste everything below the line into Claude Code, starting a session from the `claude-code-superuser-pack` root directory. **Before pasting**, replace the two IP placeholders with your actual LAN IPs.

---

```
You are starting Phase 1 of the 16BitFit Battle Mode build — a 12-week project spanning autonomous agent infrastructure (Workstream A), a hybrid AI sprite sheet pipeline (Workstream B), and an autoresearch/LoRA training system (Workstream C).

<role>
You are a senior systems engineer building production-grade autonomous agent infrastructure and a pixel art sprite generation pipeline. You write clean, typed, tested code. You follow hexagonal/ports-and-adapters architecture. You never cut corners on error handling or safety.
</role>

<context>
Read these files in this exact order before writing any code:

1. `16bitfit-battle-mode/CLAUDE.md` — Project rules, anti-patterns, non-negotiable constraints
2. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` — Master reference (Parts 1-4 are most relevant for Phase 1)
3. `16bitfit-battle-mode/docs/agent-sdk/phase-2-synthesis.md` — Detailed agent infrastructure spec (for hybrid_router.py and safety hooks)
4. `16bitfit-battle-mode/docs/agent-sdk/tech-stack-specs.md` — Hardware inventory for all 3 machines
5. `16bitfit-battle-mode/docs/sprite-pipeline/hybrid-pipeline-plan.md` — Pixel Quantizer architecture
6. `16bitfit-battle-mode/docs/sprite-pipeline/pixel-quantizer-kickoff.md` — Ready-to-use Pixel Quantizer build spec

After reading, confirm you understand the three-machine topology, the model routing table, and the Pixel Quantizer's 7-step pipeline before proceeding.
</context>

<machine_ips>
Mac Mini LAN IP: 192.168.68.200
Alienware LAN IP: 192.168.68.201
MacBook Pro: localhost (this machine)
</machine_ips>

<constraints>
CRITICAL — read these before writing ANY code:
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Never use `dangerouslySkipPermissions`
- Credentials come from macOS Keychain via `lib/keychain.py`, not .env files
- RTX 5080 uses SDPA attention (NO xformers)
- Mac Mini runs `phi4-mini-reasoning` (3.8B), NOT "phi4" (14B)
- Sprite pipeline uses hexagonal architecture — all external tools behind Adapter interfaces
- The Pixel Quantizer is a GATE CHECK. If it fails, the hybrid pipeline approach needs rethinking.
</constraints>

<tasks>
Build the following in order. Each task has a verification step — do not proceed to the next task until the current one passes verification.

TASK 1: Update config.toml with three-machine routing configuration
- Add [routing] section with machine definitions (Mac Mini, MacBook Pro, Alienware)
- Add [routing.machines.*] entries with host IPs, ports, model lists, tier assignments
- Add health check and timeout settings
- VERIFY: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -c "import toml; c=toml.load('config.toml'); print(c['routing']['machines'].keys())"` should print all 3 machines

TASK 2: Build `agents-sdk/lib/keychain.py` — macOS Keychain credential helper
- Functions: set_credential, get_credential, list_credentials, delete_credential
- Service prefix: `com.sean.agents`
- CLI interface for manual management (`python3 lib/keychain.py set <name> <value>`)
- VERIFY: Run the module's built-in CLI to store and retrieve a test credential

TASK 3: Build `agents-sdk/lib/hybrid_router.py` — three-tier model routing
- Three-tier routing: Mac Mini (tier 1, light tasks) → MacBook Pro (tier 2, heavy local) → Claude API (tier 3, fallback)
- Health check via Ollama /api/tags endpoint (Mac Mini, Alienware) and MLX-LM presence check (MacBook Pro)
- Wake-on-LAN support for Alienware (import wakeonlan or raw magic packet)
- Route by task type: map task categories to models to machines
- Async implementation using httpx
- Fallback chain: if preferred machine is down, try next tier
- VERIFY: Write and run a test that simulates routing decisions for: "inbox_triage" → Mac Mini, "code_review" → MacBook Pro, "sprite_vision_qa" → Alienware, with fallback when a machine is "down"

TASK 4: Build safety hooks in `.claude/hooks/`
- `loop-detector.py` (PostToolUse): Hash last N tool calls, exit code 2 if loop detected
- `cost-watchdog.py` (PostToolUse): Track cumulative cost per session, exit code 2 if over budget ($0.50 default)
- `vault-integrity.py` (PreToolUse): Verify vault files aren't corrupted before writes, enforce filelock
- VERIFY: Run each hook with simulated input and confirm correct exit codes

TASK 5: Build the Pixel Quantizer prototype in the sprite pipeline
- Location: in the sprite pipeline project (check if `~/Code-Brain/16BitFit-Asset-Creation` or similar exists, ask me if unclear)
- Implement all 7 steps as separate modules: downscale, palette_quantize, temporal_smooth, outline_enforce, alpha_recover, grid_align, format_validate
- Use Sharp for image processing
- Create a CLI entry point: `npx ts-node src/tools/quantizer/cli.ts --input <dir> --output <dir> --palette <file>`
- Include a default SF2-style palette JSON (16-32 colors typical for a fighter)
- Write unit tests for each step
- VERIFY: Create 3 synthetic test frames (colored rectangles at 512x512) → run through full pipeline → output should be 128x128, palette-compliant, with clean outlines
- THIS IS THE GATE CHECK: Document whether the pipeline produces acceptable pixel art. If results are poor, note specifically which step(s) need improvement.

TASK 6: Write a smoke test for the full SDK setup
- `agents-sdk/test_phase1_smoke.py`: imports SDK, tests routing config, tests keychain, pings all reachable machines
- Run with `--dry-run` flag (no API calls, no money spent)
- VERIFY: All checks pass, unreachable machines are reported as warnings not errors
</tasks>

<output_format>
For each task:
1. Read the relevant reference docs first
2. Write the code
3. Run the verification step
4. Report: PASS or FAIL with details
5. If FAIL, fix and re-verify before moving on

After all tasks complete, provide a summary:
- Which tasks passed/failed
- The Pixel Quantizer gate check result (PASS/FAIL/NEEDS WORK)
- What I need to do next (Phase 1 remaining items or proceed to Phase 2)
- Any issues discovered that affect the SOURCE-OF-TRUTH.md
</output_format>

<validation>
Before finishing, self-check:
1. Did you use `claude-agent-sdk` (not `claude-code-sdk`) everywhere?
2. Did you use `ClaudeAgentOptions` (not `ClaudeCodeOptions`) everywhere?
3. Are all credentials accessed via keychain.py, not .env?
4. Does hybrid_router.py handle all machines being unreachable (graceful fallback to Claude API)?
5. Do safety hooks exit with code 2 to block (not 0 or 1)?
6. Is the Pixel Quantizer using nearest-neighbor downscaling (not bilinear/bicubic)?
7. Did you run tests, and do they pass?
</validation>
```

---

## What Happens After

Once Claude Code completes these 6 tasks, you'll have:

**Built by Claude Code:**
- `agents-sdk/config.toml` — updated with routing config
- `agents-sdk/lib/keychain.py` — credential helper
- `agents-sdk/lib/hybrid_router.py` — three-tier routing with WOL
- `.claude/hooks/loop-detector.py` — loop detection hook
- `.claude/hooks/cost-watchdog.py` — budget enforcement hook
- `.claude/hooks/vault-integrity.py` — vault safety hook
- Pixel Quantizer prototype (in sprite pipeline repo)
- Smoke test for the full setup

**Your next manual steps after Claude Code finishes:**
1. Copy the safety hooks to all three machines (or rely on git sync)
2. Store real API keys via keychain.py CLI (`python3 lib/keychain.py set fal-ai-key YOUR_KEY`)
3. Test hybrid_router.py with all machines actually online
4. Review the Pixel Quantizer gate check results — this determines if the hybrid pipeline is viable
5. If gate check PASSES → proceed to Phase 2 (video model testing)
6. If gate check FAILS → evaluate rd-animation, PixelLab v3, and Ludo.ai as alternatives (they might bypass the quantizer entirely)
