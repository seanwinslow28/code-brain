# Phase 1 Manual Setup Guide

**Updated:** March 28, 2026
**Context:** WiFi-only until TP-Link Deco 7 Pro mesh arrives (March 29). Setup split accordingly.

---

## TODAY (March 28) — Local Setup on Each Machine

All of these steps are local installs that don't need the mesh system. Do all three machines in parallel to save time.

### Mac Mini (Always-On Orchestrator)

> **Already done:** Ollama installed, models pulled, LAN access configured (permanent via LaunchAgent plist), WiFi IP is `10.0.0.45` on `en1`. Repo already cloned at `~/Code-Brain/claude-code-superuser-pack/`. The `.venv` folder already exists in `agents-sdk/`.

| Step | Command | Claude Code can help? | Status |
|---|---|---|---|
| ~~1. Install Python 3.12~~ | — | — | **Likely done** — venv exists, which means Python was available to create it. Have Claude Code verify: `python3.12 --version` |
| ~~2. Verify Python~~ | `python3.12 --version` | **Yes** | Quick confirmation. |
| ~~3. Clone/sync repo~~ | — | — | **Done.** Repo lives at `~/Code-Brain/claude-code-superuser-pack/` on Mac Mini. |
| ~~4. Create venv~~ | — | — | **Done.** `.venv` folder exists in `agents-sdk/`. |
| 5. Install missing packages | `source .venv/bin/activate && pip install filelock toml` | **Yes** — run it for you | **Verified via Cowork audit:** `claude-agent-sdk` (v0.1.39) and `httpx` are already installed. Only `filelock` and `toml` are missing. |
| ~~6. Verify SDK import~~ | — | — | **Done.** Verified via Cowork — `ClaudeAgentOptions` imports correctly from `claude_agent_sdk`. |
| ~~7. Make OLLAMA_HOST permanent~~ | — | — | **Done.** LaunchAgent plist created in earlier session. |

> **Note:** Venv uses Python 3.13 (not 3.12 as originally spec'd). This is fine — the SDK works with 3.13.

**Tell Claude Code on Mac Mini:**
> "Install filelock and toml into the agents-sdk venv: `cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk && source .venv/bin/activate && pip install filelock toml`"

---

### MacBook Pro (Dev Machine — Where You'll Paste the Phase 1 Prompt)

> **Important: Git clone the repo here, don't rely on Google Drive sync.** Claude Code's Phase 1 prompt will write new files (keychain.py, hybrid_router.py, safety hooks) that need proper git tracking. Google Drive sync can corrupt `.git` internals when two machines sync the same repo simultaneously. Clone the repo independently on the MacBook Pro and use `git push`/`git pull` to sync changes between machines. Google Drive is great for backups and large assets, but git repos should live separately on each machine.

| Step | Command | Status |
|---|---|---|
| ~~1. Clone the superuser pack repo~~ | — | **Pending** — clone via git, not Google Drive sync |
| ~~2. Install Python 3.13~~ | `brew install python@3.13` | **Done.** Python 3.13.12 installed. |
| ~~3. Create MLX-LM venv~~ | `python3.13 -m venv ~/Code-Brain/mlx-lm-env` | **Done.** Venv at `~/Code-Brain/mlx-lm-env`. |
| ~~4. Install MLX-LM~~ | `pip install mlx-lm` (inside venv) | **Done.** MLX-LM v0.31.1 (latest). |
| ~~5. Download Qwen3-14B~~ | — | **Done.** Tested at 31 tok/s, 8.4 GB peak memory. |
| ~~6. Download Qwen2.5-Coder-32B~~ | — | **Done.** Downloaded and cached. |
| ~~7. Add mlxenv alias~~ | — | **Done.** `alias mlxenv="source ~/Code-Brain/mlx-lm-env/bin/activate"` in `~/.zshrc`. |
| ~~8. Clean up old Python 3.9 mlx-lm~~ | — | **Done.** Uninstalled, PATH removed, old model cache deleted. |
| 9. Upgrade Node.js to v22 LTS | `nvm install 22 && nvm alias default 22` | **Remaining** — v20 is end-of-life. v22 is the current Active LTS with widest compatibility. |

> **MLX-LM usage:** Run `mlxenv` to activate the venv, then `mlx_lm.chat --model mlx-community/Qwen3-14B-4bit` etc. The `hybrid_router.py` built in Phase 1 will reference this venv path in `config.toml`.

---

### Alienware (CUDA Specialist — Windows)

> **All steps complete.** Verified via Claude Code session on March 28, 2026.

| Step | Status |
|---|---|
| ~~0. Clone superuser pack repo~~ | **Done.** `C:\Users\seanw\Documents\Code-Brain\claude-code-superuser-pack`, main branch, clean. |
| ~~1. Install Ollama~~ | **Done.** Ollama v0.18.3. |
| ~~2. Set OLLAMA_HOST~~ | **Done.** `0.0.0.0:11434` via setx. |
| ~~3. Set OLLAMA_KEEP_ALIVE~~ | **Done.** `2m` via setx. |
| ~~4. Restart Ollama~~ | **Done.** |
| ~~5. Pull vision model~~ | **Done.** `qwen3-vl:8b` (note: Ollama tags this as `:8b`, not `:7b`). |
| ~~6. Verify model~~ | **Done.** Working on GPU, Q4_K_M quantization, 8.8B params. |
| ~~7. Update ComfyUI~~ | **Done.** Updated via desktop app. Launch with `--fp16-intermediates`. |
| ~~8. Firewall rule~~ | **Done.** "Ollama LAN Access" — TCP 11434 inbound, all profiles. |

> **Alienware LAN IP (current, pre-mesh):** `10.0.0.219` — this will change after Deco mesh setup tomorrow.
> **GPU:** RTX 5080, 16 GB VRAM, NVIDIA driver 581.95, CUDA 13.0.
> **Important:** Never install xformers on this machine. SDPA (default) is correct for sm_120.

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
