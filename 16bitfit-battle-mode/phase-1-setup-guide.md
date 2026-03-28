# Phase 1 Manual Setup Guide

**Updated:** March 28, 2026
**Context:** WiFi-only until TP-Link Deco 7 Pro mesh arrives (March 29). Setup split accordingly.

---

## TODAY (March 28) — Local Setup on Each Machine

All of these steps are local installs that don't need the mesh system. Do all three machines in parallel to save time.

### Mac Mini (Always-On Orchestrator)

> **Already done:** Ollama installed, models pulled, LAN access configured (permanent via LaunchAgent plist), WiFi IP is `10.0.0.45` on `en1`.

| Step | Command | Claude Code can help? | What it does & why |
|---|---|---|---|
| 1. Install Python 3.12 | `brew install python@3.12` | **Yes** — run it for you | The Agent SDK needs Python 3.12. Homebrew handles the install cleanly. If you don't have Homebrew, Claude Code can install that first too. |
| 2. Verify Python | `python3.12 --version` | **Yes** — run and check output | Confirms the install worked. You want to see `3.12.x`. |
| 3. Clone/sync the superuser pack repo | `cd ~/Code-Brain && git clone <your-repo-url>` (or `git pull` if already cloned) | **Yes** — can run git commands for you | Gets the agents-sdk code onto the Mac Mini. |
| 4. Create virtual environment | `cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk && python3.12 -m venv .venv` | **Yes** — run it for you | A venv is an isolated Python sandbox. Packages you install here won't conflict with system Python. Standard practice for any Python project. |
| 5. Install SDK + dependencies | `source .venv/bin/activate && pip install claude-agent-sdk filelock toml httpx` | **Yes** — run it for you | Installs four packages: the Claude Agent SDK itself, `filelock` (prevents multiple agents writing to the same file), `toml` (reads config files), `httpx` (async HTTP client for talking to other machines). |
| 6. Verify SDK | `source .venv/bin/activate && python3 -c "from claude_agent_sdk import ClaudeAgentOptions; print('OK')"` | **Yes** — run and confirm output | If it prints "OK," you're good. If it errors, the SDK didn't install correctly and Claude Code can troubleshoot. |
| 7. Make OLLAMA_HOST permanent | Already done ✅ | — | LaunchAgent plist was created in your earlier session. |

**Tell Claude Code on Mac Mini:**
> "Walk me through steps 1-6 in this order. Run each command, check the output, and move on. If anything fails, troubleshoot before continuing."

---

### MacBook Pro (Dev Machine — Where You'll Paste the Phase 1 Prompt)

| Step | Command | Claude Code can help? | What it does & why |
|---|---|---|---|
| 1. Install MLX-LM | `pip install mlx-lm` | **Yes** — run it for you | MLX-LM is Apple's framework for running LLMs on Apple Silicon. Chosen over Ollama here because MLX is optimized specifically for M-series chips and handles bigger models more efficiently on your 48GB machine. |
| 2. Download Qwen3-14B | `mlx_lm.download --model mlx-community/Qwen3-14B-4bit` | **Yes** — run it for you (will take a while) | The "heavy analysis" model. Handles financial analysis, complex synthesis. The `-4bit` means it's quantized (compressed) to fit in memory while staying capable. |
| 3. Download Qwen2.5-Coder-32B | `mlx_lm.download --model mlx-community/Qwen2.5-Coder-32B-Instruct-4bit` | **Yes** — run it for you (largest download) | Specialized for code review and programming tasks. This is the biggest model in your setup — the download may take some time. |
| 4. Quick test MLX-LM | `mlx_lm.generate --model mlx-community/Qwen3-14B-4bit --prompt "Hello" --max-tokens 20` | **Yes** — run and confirm output | If you see generated text, MLX-LM works. If it crashes, Claude Code can check your Python version and MLX install. |
| 5. Verify Node.js 20+ | `node --version` | **Yes** — check output | The Pixel Quantizer (Task 5 in the Claude Code prompt) uses Node.js/TypeScript with the Sharp image library. Needs v20+. If you're behind, Claude Code can run `brew install node` for you. |
| 6. Update superuser pack | `cd ~/Code-Brain/claude-code-superuser-pack && git pull` | **Yes** — run it for you | Makes sure you have the latest code before Phase 1. |

**Tell Claude Code on MacBook Pro:**
> "Walk me through steps 1-6. The model downloads might take a while — start them and let me know when each finishes. Verify each step before moving on."

---

### Alienware (CUDA Specialist — Windows)

| Step | Command | Claude Code can help? | What it does & why |
|---|---|---|---|
| 1. Install Ollama for Windows | Download from https://ollama.com/download/windows | **No** — manual download/installer | Same tool as Mac Mini, just the Windows version. Download and run the `.exe` installer. |
| 2. Set OLLAMA_HOST env var | System Properties → Advanced → Environment Variables → New System Variable: `OLLAMA_HOST` = `0.0.0.0:11434` | **Partially** — Claude Code can set it via `setx OLLAMA_HOST "0.0.0.0:11434"` in Command Prompt, but a restart of Ollama is still needed | Allows LAN access. By default Ollama only listens locally. `0.0.0.0` means "listen on all network interfaces" so your MacBook can reach it. |
| 3. Set OLLAMA_KEEP_ALIVE env var | Same location: `OLLAMA_KEEP_ALIVE` = `2m` | **Partially** — `setx OLLAMA_KEEP_ALIVE "2m"` works, but needs Ollama restart | Keeps models loaded in VRAM for 2 minutes after the last request, then unloads. This frees GPU memory for ComfyUI when Ollama isn't actively serving. |
| 4. Restart Ollama | Close the Ollama system tray icon → reopen | **No** — manual GUI action | Picks up the new environment variables. |
| 5. Pull vision model | `ollama pull qwen3-vl:7b` | **Yes** — run it for you | Qwen3-VL-7B is a vision-language model — it can look at images and analyze them. Your pipeline uses this for sprite quality checking ("Sprite Vision QA" in the routing table). |
| 6. Verify model | `ollama run qwen3-vl:7b "Describe this test." /bye` | **Yes** — run and confirm output | Should output some text and exit. If it errors about CUDA, Claude Code can help check your NVIDIA driver version. |
| 7. Update ComfyUI to v0.18.2+ | Depends on your install method (git pull, or ComfyUI Manager) | **Yes** — if installed via git, Claude Code can run `git pull` and check the version | Launch with `--fp16-intermediates` flag — this uses half-precision for intermediate calculations, saving VRAM. You won't need ComfyUI until Phase 2+ but better to have it ready. |

**Tell Claude Code on Alienware:**
> "Help me set the OLLAMA_HOST and OLLAMA_KEEP_ALIVE environment variables via setx, then pull the qwen3-vl:7b model and verify it works. Also check my ComfyUI version."

---

## TOMORROW (March 29) — After Deco 7 Pro Mesh Setup

### Step 1: Set Up the Mesh

Follow the TP-Link Deco app setup. Connect one Deco unit to your apartment's ethernet outlet in the living space, the other in your bedroom near your computer setup. The two units communicate wirelessly to create one unified network.

### Step 2: Assign Static IPs (Critical)

Open the **Deco app → More → Advanced → Address Reservation**. Assign fixed IPs to:

| Device | Why it needs a static IP |
|---|---|
| Mac Mini | `config.toml` hardcodes this IP for routing. If it changes after a reboot, the three-machine communication breaks silently. |
| Alienware | Same reason — the router sends traffic to it by IP. |
| MacBook Pro | Optional but recommended for consistency. |

Pick IPs outside the DHCP range (e.g., `.200`, `.201`, `.202`) so they never conflict with auto-assigned addresses. Write all three down.

### Step 3: Cross-Machine Verification (Claude Code on MacBook Can Help)

| Check | Command | What you're looking for |
|---|---|---|
| MacBook → Mac Mini | `curl http://{NEW_MINI_IP}:11434/api/tags` | JSON listing `phi4-mini-reasoning` and `nomic-embed-text` |
| MacBook → Alienware | `curl http://{NEW_ALIENWARE_IP}:11434/api/tags` | JSON listing `qwen3-vl:7b` |

**If Mac Mini fails:** Ollama might not be running, or `OLLAMA_HOST` isn't set. Claude Code on the Mini can check both.

**If Alienware fails:** Windows Firewall is the most common culprit. Claude Code on the Alienware can help you add an inbound rule for port 11434.

**Tell Claude Code on MacBook Pro:**
> "Run curl to check if I can reach Ollama on {MINI_IP}:11434 and {ALIENWARE_IP}:11434. Parse the JSON responses and confirm which models are available on each."

### Step 4: Store API Keys

If you have API keys ready (fal.ai, etc.), you can pre-store them in macOS Keychain Access manually. Claude Code will build the `keychain.py` helper in Task 2 of the Phase 1 prompt, which gives you a CLI for this going forward.

### Step 5: Paste the Phase 1 Claude Code Prompt

Before pasting into Claude Code on your MacBook Pro:

1. Replace `{REPLACE_WITH_MINI_IP}` with the Mac Mini's **new static IP** from the Deco
2. Replace `{REPLACE_WITH_ALIENWARE_IP}` with the Alienware's **new static IP** from the Deco
3. Make sure you start the Claude Code session from the `claude-code-superuser-pack` root directory

---

## Quick Reference: What Claude Code Can vs. Can't Do

| Claude Code CAN do | Claude Code CANNOT do |
|---|---|
| Run terminal commands (`brew install`, `pip install`, `git clone`, `ollama pull`, etc.) | Click GUI buttons (Ollama installer, system tray, Deco app) |
| Set environment variables via command line (`setx` on Windows, `launchctl` on Mac) | Restart GUI applications |
| Troubleshoot errors in real time | Access other machines remotely (it runs locally on each machine) |
| Verify installs and parse output | Set up the Deco mesh system (that's all in the phone app) |
| Run downloads in the background | Push through download speeds any faster |

**Key insight:** Claude Code runs locally on each machine, so you need to give it instructions separately on each one. It can't SSH from your MacBook to your Mac Mini — you'll have separate Claude Code sessions on each machine.
