# 12-Week Execution Blueprint
## Sean's Agentic Frameworks & Creative Pipeline

**Created:** March 27, 2026
**Scope:** Three-machine orchestration, autonomous agent fleet, hybrid sprite pipeline, LoRA training, autoresearch
**Hardware:** Mac Mini M4 Pro (24GB) · MacBook Pro M4 Pro (48GB) · Alienware Aurora RTX 5080 (16GB VRAM)
**Starting Position:** Post-move, fresh setups needed on all machines

---

## Master Timeline

| Phase | Weeks | Focus | Est. Hours |
|-------|-------|-------|------------|
| **Phase 1** | 1-2 (Mar 27 - Apr 10) | Foundation: hardware setup, networking, safety hooks, pixel quantizer | ~24h |
| **Phase 2** | 3-4 (Apr 10 - Apr 24) | First agents, video model evaluation, Retro Diffusion test | ~19.5h |
| **Phase 3** | 5-6 (Apr 24 - May 8) | Pipeline integration, PM agents, end-to-end hybrid test | ~19.5h |
| **Phase 4** | 7-8 (May 8 - May 22) | LoRA training, memory agents, vault embedding indexer | ~17.5h |
| **Phase 5** | 9-12 (May 22 - Jun 19) | Autoresearch loop, pipeline scaling, meta-agent, fleet optimization | ~22h |
| **Total** | | | **~102.5h** |

## Critical Updates from Validation Audit (March 27, 2026)

These changes have been incorporated throughout the blueprint:

1. **Phi-4 is actually 14B** — Mac Mini tasks use `phi4-mini-reasoning` (3.8B), not "Phi-4 7B"
2. **PyTorch stable cu128** — No longer need nightly builds for RTX 5080 sm_120 support
3. **Claude Agent SDK** — Package renamed from `claude-code-sdk` to `claude-agent-sdk`; `ClaudeAgentOptions` replaces `ClaudeCodeOptions`
4. **Illustrious XL v2.0-STABLE** — Replaces v0.1 as the LoRA base model
5. **Retro Diffusion rd-animation** — Now live on Replicate; could bypass hybrid pipeline for standard animations
6. **Wan 2.5 NOT open source** — Wan 2.2 is latest open-source; LTX-2 is the alternative
7. **Opus 4.6 price drop** — 67% cheaper ($5/$25 per MTok), viable for more agent tasks
8. **Qwen3 family** — Qwen3-14B outperforms DeepSeek-R1:14B; evaluate during Phase 1 benchmarking
9. **ComfyUI v0.18.2** — Built-in NanoBanana2 API node for direct Gemini image generation
10. **Ollama v0.5.x** — Blackwell compilation, structured outputs, improved model scheduling

## Non-Negotiable Constraints

- **Gemini image models** (Nano Banana Pro / Nano Banana 2) remain the primary image generators
- **RTX 5080**: CUDA 12.8+, PyTorch stable cu128, SDPA (NO xformers), kohya_ss dev branch
- **Credential management** via macOS Keychain (not .env files)
- **Never use `dangerouslySkipPermissions`** for autonomous agents

## Updated Model-to-Machine Routing

| Task | Machine | Model | Pull Command |
|------|---------|-------|-------------|
| Inbox triage | Mac Mini | phi4-mini-reasoning (3.8B) | `ollama pull phi4-mini-reasoning` |
| Vault embeddings | Mac Mini | nomic-embed-text | `ollama pull nomic-embed-text` |
| Meeting pre-classification | Mac Mini | phi4-mini-reasoning (3.8B) | (already pulled) |
| Financial analysis | MacBook Pro | Qwen3:14b via MLX | `mlx_lm.download --model mlx-community/Qwen3-14B-4bit` |
| Code review / PR digest | MacBook Pro | Qwen2.5-Coder:32b via MLX | `mlx_lm.download --model mlx-community/Qwen2.5-Coder-32B-Instruct-4bit` |
| Heavy synthesis | MacBook Pro | Qwen2.5:32b via MLX | `mlx_lm.download --model mlx-community/Qwen2.5-32B-Instruct-4bit` |
| Sprite vision QA | Alienware | qwen2.5-vl:7b via Ollama CUDA | `ollama pull qwen2.5-vl:7b` |
| ComfyUI orchestration | Alienware | N/A (REST API) | N/A |

---

# 16BitFit Battle Mode — Execution Blueprint: Phases 1-2

**Author:** Sean Winslow
**Created:** 2026-03-27
**Scope:** Weeks 1-4 (March 27 – April 24, 2026)
**Status:** ACTIVE

---

## Reading Guide

This blueprint covers **Phase 1 (Foundation)** and **Phase 2 (First Agents + Video Model Testing)**. Every task includes exact commands, full config files, complete code implementations, and verification steps. You should be able to execute every step by copying and pasting.

**Machine Legend:**
- **Mac Mini** = Mac Mini M4 Pro (24GB unified, 12-core CPU, macOS) — always-on orchestrator
- **MacBook Pro** = MacBook Pro M4 Pro (48GB unified, 14-core CPU, macOS) — heavyweight local inference
- **Alienware** = Alienware Aurora (Intel Ultra 9, 64GB DDR5, RTX 5080 16GB, Windows 11) — CUDA-specialized

**Critical Constraints (memorize these):**
- Gemini image models (Nano Banana Pro and Nano Banana 2) are **NON-NEGOTIABLE** in the sprite pipeline
- RTX 5080 commands use **CUDA 12.8+** and **PyTorch stable cu128** (NOT nightly)
- Use `phi4-mini` or `phi4-mini-reasoning` (3.8B) for Mac Mini — NOT "Phi-4 7B" (Phi-4 is 14B, too big)
- Package name is `claude-agent-sdk` (NOT `claude-code-sdk`)
- Class name is `ClaudeAgentOptions` (NOT `ClaudeCodeOptions`)
- Ollama v0.5.x on all machines
- ComfyUI v0.18.2 on Alienware
- **Never install xformers on RTX 5080** — use SDPA (PyTorch native attention)

---

## PHASE 1: FOUNDATION (Weeks 1-2, Mar 27 – Apr 10)

**Goal:** All three machines online with Ollama, models pulled, LAN routing working, safety hooks deployed, and the Pixel Quantizer prototype passing gate checks.

**Phase 1 Task Map:**

```
Parallel Track A (Agent Infra):     Parallel Track B (Sprite Pipeline):
1.1 Mac Mini Ollama ──┐              1.10 Pixel Quantizer (MacBook Pro)
1.2 Mac Mini SDK ─────┤                    │
1.3 MacBook Pro MLX ──┤              (independent — no dependencies)
1.4 Alienware Ollama ─┤
1.5 Alienware ComfyUI ┤
                       │
1.6 Networking ────────┤
1.7 hybrid_router.py ─┤
1.8 Safety Hooks ──────┤
1.9 Keychain Helper ───┘
```

---

### 1.1 Mac Mini: Ollama Installation and Model Setup — 1.5h

**Depends on:** None — can start immediately
**Can parallel with:** 1.3, 1.4, 1.5, 1.10
**Machine:** Mac Mini

**Steps:**

1. **Install Ollama via the official install script**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **Why:** This installs Ollama CLI and the background service. On macOS, it also installs the Ollama.app which manages the service automatically.

   **Verify:**
   ```bash
   ollama --version
   # Expected: ollama version 0.5.x
   ```

2. **Pull the phi4-mini-reasoning model (3.8B parameters)**

   ```bash
   ollama pull phi4-mini-reasoning
   ```

   **Why:** This is the lightweight reasoning model for the Mac Mini. At 3.8B parameters (~2.5GB at Q4), it fits easily in 24GB unified memory and leaves headroom for other tasks. Do NOT use "phi4" (which is the full 14B model) — it would consume too much of the Mac Mini's memory.

   **Verify:**
   ```bash
   ollama run phi4-mini-reasoning "What is 2+2? Reply in one word."
   # Expected: "Four" or similar short response
   # Then type /bye to exit
   ```

3. **Pull the nomic-embed-text model for embeddings**

   ```bash
   ollama pull nomic-embed-text
   ```

   **Why:** This tiny embedding model (<500MB) generates vector embeddings for the Vault Embedding Indexer agent. It runs on the always-on Mac Mini so embeddings can be generated nightly without waking other machines.

   **Verify:**
   ```bash
   curl http://localhost:11434/api/embeddings -d '{
     "model": "nomic-embed-text",
     "prompt": "test embedding"
   }'
   # Expected: JSON response with an "embedding" array of 768 floats
   ```

4. **Configure OLLAMA_HOST for LAN access via launchd environment**

   By default, Ollama only listens on `127.0.0.1:11434` (localhost). To allow other machines on your LAN to connect, you need to set it to `0.0.0.0:11434`.

   On macOS, the Ollama app runs as a launchd service. Set the environment variable using `launchctl`:

   ```bash
   # Set the environment variable for the current user session
   launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
   ```

   **Why:** `launchctl setenv` makes the variable available to all processes launched by launchd for the current user session, including the Ollama app.

   To make this **persist across reboots**, create a Launch Agent that sets the variable at login:

   ```bash
   cat > ~/Library/LaunchAgents/com.sean.ollama-env.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sean.ollama-env</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/launchctl</string>
        <string>setenv</string>
        <string>OLLAMA_HOST</string>
        <string>0.0.0.0:11434</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
PLIST
   ```

   Load it immediately:

   ```bash
   launchctl load ~/Library/LaunchAgents/com.sean.ollama-env.plist
   ```

   **Verify the env is set:**
   ```bash
   launchctl getenv OLLAMA_HOST
   # Expected: 0.0.0.0:11434
   ```

5. **Create a launchd plist to auto-start Ollama on boot**

   If you installed Ollama via the `curl` script, Ollama.app is installed and auto-starts when you log in. However, since the Mac Mini is a headless always-on server, you want Ollama available even before you log in. Create a global Launch Daemon:

   ```bash
   sudo cat > /Library/LaunchDaemons/com.sean.ollama-server.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sean.ollama-server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_HOST</key>
        <string>0.0.0.0:11434</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama-server.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama-server.stderr.log</string>
</dict>
</plist>
PLIST
   ```

   **Important:** If the Ollama.app is already managing the service, you may get a port conflict. In that case, either:
   - Remove Ollama.app from Login Items (System Settings → General → Login Items) and use only this daemon, OR
   - Skip this step and rely on Ollama.app (which auto-starts at user login)

   For a headless Mac Mini, the Launch Daemon approach is more reliable because it starts at boot, before any user logs in.

   Load the daemon:
   ```bash
   sudo launchctl load /Library/LaunchDaemons/com.sean.ollama-server.plist
   ```

   **Verify:**
   ```bash
   curl http://localhost:11434/api/tags
   # Expected: JSON with models list including phi4-mini-reasoning and nomic-embed-text
   ```

6. **Verify models load and respond**

   ```bash
   # Test phi4-mini-reasoning
   curl http://localhost:11434/api/generate -d '{
     "model": "phi4-mini-reasoning",
     "prompt": "Summarize the concept of hexagonal architecture in one sentence.",
     "stream": false
   }' | python3 -m json.tool

   # Test nomic-embed-text
   curl http://localhost:11434/api/embeddings -d '{
     "model": "nomic-embed-text",
     "prompt": "sprite animation pipeline"
   }' | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Embedding dimensions: {len(d[\"embedding\"])}')"
   # Expected: Embedding dimensions: 768
   ```

   **Verify:** Both return valid JSON responses without errors.

7. **Verify LAN access from another machine**

   From your MacBook Pro (or any other machine on the same network), find the Mac Mini's IP address first:

   ```bash
   # ON THE MAC MINI — find its IP
   ipconfig getifaddr en0
   # Example output: 192.168.1.100
   ```

   Then from the MacBook Pro:
   ```bash
   # ON THE MACBOOK PRO — test LAN access
   curl http://192.168.1.100:11434/api/tags
   # Expected: Same JSON response with models list
   ```

   **Verify:** You get a valid response. If you get "Connection refused," check that `OLLAMA_HOST` is set to `0.0.0.0:11434` and that the Ollama service was restarted after setting it.

**Gotchas:**
- If Ollama was already running when you set `OLLAMA_HOST`, you need to restart it. Quit Ollama.app from the menu bar and reopen it, or `sudo launchctl unload/load` the daemon.
- The `ollama pull` command requires Ollama to be running (`ollama serve` or via the app). If you get "connection refused," start the service first.
- `phi4-mini-reasoning` is different from `phi4-mini`. The reasoning variant has chain-of-thought training. Either works; reasoning is preferred for agent tasks.

---

### 1.2 Mac Mini: Python Environment and Agent SDK Setup — 1h

**Depends on:** 1.1 (Ollama must be running for SDK tests)
**Can parallel with:** 1.3, 1.4, 1.5, 1.10
**Machine:** Mac Mini

**Steps:**

1. **Install Python 3.12+ via Homebrew**

   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python 3.12
   brew install python@3.12
   ```

   **Why:** macOS ships with a system Python that shouldn't be modified. Homebrew gives you a clean, up-to-date Python installation.

   **Verify:**
   ```bash
   python3.12 --version
   # Expected: Python 3.12.x
   ```

2. **Create a virtual environment for the agents-sdk**

   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   **Why:** Virtual environments isolate your agent dependencies from the system Python and other projects.

   **Verify:**
   ```bash
   which python3
   # Expected: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3
   ```

3. **Install claude-agent-sdk and dependencies**

   ```bash
   pip install claude-agent-sdk
   pip install filelock toml httpx
   ```

   **Why:**
   - `claude-agent-sdk` — the core SDK that spawns Claude Code CLI as a subprocess
   - `filelock` — prevents concurrent vault writes from corrupting files
   - `toml` — reads `config.toml` configuration
   - `httpx` — async HTTP client for communicating with Ollama endpoints on other machines

   **Verify:**
   ```bash
   pip show claude-agent-sdk
   # Expected: Name: claude-agent-sdk, Version: 0.1.50 (or later)

   python3 -c "from claude_agent_sdk import ClaudeAgentOptions; print('SDK imported successfully')"
   ```

4. **Verify SDK works with a minimal test script**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/test_sdk_smoke.py`:

   ```python
   #!/usr/bin/env python3
   """Smoke test: verify claude-agent-sdk is installed and importable."""

   import asyncio
   from claude_agent_sdk import query, ClaudeAgentOptions


   async def main():
       # Dry-run test: build options but don't execute
       # This verifies the SDK is importable and option construction works
       options = ClaudeAgentOptions(
           max_turns=3,
           system_prompt="You are a helpful assistant. Reply briefly.",
       )
       print(f"✓ ClaudeAgentOptions created successfully")
       print(f"  max_turns: {options.max_turns}")
       print(f"  SDK smoke test PASSED")

       # Uncomment below to actually call Claude (costs money):
       # result = await query(
       #     prompt="Say 'hello world' and nothing else.",
       #     options=options,
       # )
       # for message in result:
       #     if hasattr(message, 'content'):
       #         print(f"  Claude response: {message.content}")


   if __name__ == "__main__":
       asyncio.run(main())
   ```

   Run it:
   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 test_sdk_smoke.py
   # Expected: ✓ ClaudeAgentOptions created successfully
   #           SDK smoke test PASSED
   ```

   **Why:** This confirms the SDK is properly installed and importable without spending any API credits.

5. **Set up macOS Keychain credential helper**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/keychain.py`:

   ```python
   #!/usr/bin/env python3
   """
   macOS Keychain credential helper.

   Stores and retrieves API keys and tokens using macOS Keychain
   instead of .env files. This is more secure because:
   1. Credentials are encrypted at rest by the OS
   2. They don't appear in git history even accidentally
   3. The block-secrets.py hook can't accidentally expose them
   4. They persist across reboots without dotfiles

   Usage:
       from lib.keychain import get_credential, set_credential

       # Store a credential (run once during setup)
       set_credential("jira-api-token", "your-token-here")

       # Retrieve in agent code
       token = get_credential("jira-api-token")
   """

   import subprocess
   import sys
   from typing import Optional

   # All credentials use this service name prefix for organization
   SERVICE_PREFIX = "com.sean.agents"


   def set_credential(name: str, value: str, account: str = "sean") -> bool:
       """Store a credential in macOS Keychain.

       Args:
           name: Credential identifier (e.g., "jira-api-token", "github-pat", "fal-ai-key")
           value: The secret value to store
           account: Keychain account name (default: "sean")

       Returns:
           True if successful, False otherwise
       """
       service = f"{SERVICE_PREFIX}.{name}"

       # Delete existing entry if it exists (security command errors if duplicate)
       subprocess.run(
           ["security", "delete-generic-password", "-s", service, "-a", account],
           capture_output=True,  # Suppress "item not found" error
       )

       result = subprocess.run(
           [
               "security", "add-generic-password",
               "-s", service,        # Service name
               "-a", account,        # Account name
               "-w", value,          # Password (the secret)
               "-U",                 # Update if exists
           ],
           capture_output=True,
           text=True,
       )

       if result.returncode != 0:
           print(f"ERROR: Failed to store credential '{name}': {result.stderr}", file=sys.stderr)
           return False

       print(f"✓ Credential '{name}' stored in Keychain (service: {service})")
       return True


   def get_credential(name: str, account: str = "sean") -> Optional[str]:
       """Retrieve a credential from macOS Keychain.

       Args:
           name: Credential identifier (e.g., "jira-api-token")
           account: Keychain account name (default: "sean")

       Returns:
           The secret value, or None if not found
       """
       service = f"{SERVICE_PREFIX}.{name}"

       result = subprocess.run(
           [
               "security", "find-generic-password",
               "-s", service,
               "-a", account,
               "-w",                 # Output only the password
           ],
           capture_output=True,
           text=True,
       )

       if result.returncode != 0:
           return None

       return result.stdout.strip()


   def list_credentials(account: str = "sean") -> list[str]:
       """List all agent credentials stored in Keychain.

       Returns:
           List of credential names (without the service prefix)
       """
       result = subprocess.run(
           ["security", "dump-keychain"],
           capture_output=True,
           text=True,
       )

       credentials = []
       for line in result.stdout.split("\n"):
           if f'"{SERVICE_PREFIX}.' in line and "svce" in line:
               # Extract the service name after the prefix
               start = line.index(f'"{SERVICE_PREFIX}.') + len(f'"{SERVICE_PREFIX}.')
               end = line.index('"', start)
               credentials.append(line[start:end])

       return sorted(set(credentials))


   def delete_credential(name: str, account: str = "sean") -> bool:
       """Delete a credential from macOS Keychain.

       Args:
           name: Credential identifier
           account: Keychain account name

       Returns:
           True if deleted, False if not found
       """
       service = f"{SERVICE_PREFIX}.{name}"

       result = subprocess.run(
           ["security", "delete-generic-password", "-s", service, "-a", account],
           capture_output=True,
           text=True,
       )

       return result.returncode == 0


   # CLI interface for manual credential management
   if __name__ == "__main__":
       import argparse

       parser = argparse.ArgumentParser(description="Manage agent credentials in macOS Keychain")
       subparsers = parser.add_subparsers(dest="command", help="Command to run")

       # set command
       set_parser = subparsers.add_parser("set", help="Store a credential")
       set_parser.add_argument("name", help="Credential name (e.g., jira-api-token)")
       set_parser.add_argument("value", help="Secret value to store")

       # get command
       get_parser = subparsers.add_parser("get", help="Retrieve a credential")
       get_parser.add_argument("name", help="Credential name")

       # list command
       subparsers.add_parser("list", help="List all stored credentials")

       # delete command
       del_parser = subparsers.add_parser("delete", help="Delete a credential")
       del_parser.add_argument("name", help="Credential name")

       args = parser.parse_args()

       if args.command == "set":
           set_credential(args.name, args.value)
       elif args.command == "get":
           val = get_credential(args.name)
           if val:
               print(val)
           else:
               print(f"Credential '{args.name}' not found", file=sys.stderr)
               sys.exit(1)
       elif args.command == "list":
           creds = list_credentials()
           if creds:
               print("Stored credentials:")
               for c in creds:
                   print(f"  • {c}")
           else:
               print("No credentials found")
       elif args.command == "delete":
           if delete_credential(args.name):
               print(f"✓ Deleted '{args.name}'")
           else:
               print(f"Credential '{args.name}' not found", file=sys.stderr)
       else:
           parser.print_help()
   ```

6. **Add initial credentials to the Keychain**

   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk

   # Store your API keys (replace with real values)
   .venv/bin/python3 lib/keychain.py set jira-api-token "YOUR_JIRA_API_TOKEN"
   .venv/bin/python3 lib/keychain.py set github-pat "YOUR_GITHUB_PAT"
   .venv/bin/python3 lib/keychain.py set fal-ai-key "YOUR_FAL_AI_API_KEY"
   .venv/bin/python3 lib/keychain.py set google-genai-key "YOUR_GOOGLE_GENAI_API_KEY"

   # Verify they're stored
   .venv/bin/python3 lib/keychain.py list
   # Expected:
   # Stored credentials:
   #   • fal-ai-key
   #   • github-pat
   #   • google-genai-key
   #   • jira-api-token

   # Test retrieval
   .venv/bin/python3 lib/keychain.py get jira-api-token
   # Expected: your token value
   ```

   **Why this is better than .env files:**
   - `.env` files are plaintext on disk — one bad `git add .` and your secrets are in version history forever
   - The `block-secrets.py` hook prevents agents from reading `.env`, but that means agents can't get credentials either. Keychain bypasses this because the credential retrieval happens in Python before the agent runs.
   - macOS Keychain encrypts secrets at rest using your login keychain password
   - Credentials persist across reboots and are backed up via Time Machine (encrypted)

**Gotchas:**
- If you get `security: SecKeychainItemCreateFromContent: The specified item already exists in the keychain`, the `-U` flag should handle this, but you can manually delete first: `security delete-generic-password -s "com.sean.agents.NAME" -a sean`
- The `security` command is macOS-only. This helper won't work on Linux or Windows — that's fine since only the Mac Mini and MacBook Pro run agent scripts.

---

### 1.3 MacBook Pro: Ollama + MLX Installation and Benchmarking — 2h

**Depends on:** None — can start immediately
**Can parallel with:** 1.1, 1.2, 1.4, 1.5, 1.10
**Machine:** MacBook Pro

**Steps:**

1. **Install Ollama**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **Verify:**
   ```bash
   ollama --version
   # Expected: ollama version 0.5.x
   ```

2. **Pull models via Ollama**

   ```bash
   ollama pull qwen3:14b
   ollama pull qwen2.5-coder:14b
   ```

   **Why:** Qwen3:14b is the updated reasoning model that outperforms DeepSeek-R1:14b (per the March 2026 audit). Qwen2.5-Coder:14b is the code-specialized model for PR Digest and code review tasks.

   **Verify:**
   ```bash
   ollama list
   # Expected: Both models listed with their sizes (~9-10GB each)

   ollama run qwen3:14b "Explain the adapter pattern in 2 sentences."
   # Expected: Coherent response about the adapter design pattern
   # Type /bye to exit
   ```

3. **Configure OLLAMA_HOST for LAN access**

   ```bash
   launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
   ```

   Create the persistent plist (same pattern as Mac Mini):

   ```bash
   cat > ~/Library/LaunchAgents/com.sean.ollama-env.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sean.ollama-env</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/launchctl</string>
        <string>setenv</string>
        <string>OLLAMA_HOST</string>
        <string>0.0.0.0:11434</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
PLIST

   launchctl load ~/Library/LaunchAgents/com.sean.ollama-env.plist
   ```

   **Restart Ollama** (quit from menu bar and reopen, or):
   ```bash
   pkill -f "Ollama" && sleep 2 && open -a Ollama
   ```

   **Verify LAN access from Mac Mini:**
   ```bash
   # ON MAC MINI — replace with MacBook Pro's actual IP
   curl http://192.168.1.101:11434/api/tags
   ```

4. **Install MLX and mlx-lm**

   ```bash
   # Create a separate venv for MLX work (keeps it clean)
   python3 -m venv ~/mlx-env
   source ~/mlx-env/bin/activate

   pip install mlx mlx-lm
   ```

   **Why:** MLX is Apple's native ML framework optimized for unified memory on Apple Silicon. For 14B+ models, MLX can deliver significantly faster token generation than Ollama because it's designed specifically for the shared GPU/CPU memory architecture.

   **Verify:**
   ```bash
   python3 -c "import mlx; print(f'MLX version: {mlx.__version__}')"
   # Expected: MLX version: 0.29.x

   python3 -c "import mlx_lm; print('mlx-lm imported successfully')"
   ```

5. **Download models via mlx-lm from HuggingFace**

   ```bash
   source ~/mlx-env/bin/activate

   # Download Qwen3-14B in MLX format from the mlx-community
   python3 -m mlx_lm.generate \
     --model mlx-community/Qwen3-14B-4bit \
     --prompt "Hello, world!" \
     --max-tokens 50
   ```

   **Why:** The `mlx-community` org on HuggingFace hosts pre-quantized MLX-format models. The first run downloads the model (~8-9GB); subsequent runs use the cached version.

   **Verify:**
   ```bash
   # Check that the model was downloaded to the HuggingFace cache
   ls ~/.cache/huggingface/hub/ | grep -i qwen
   # Expected: models--mlx-community--Qwen3-14B-4bit (or similar)
   ```

   Also download the coder model:
   ```bash
   python3 -m mlx_lm.generate \
     --model mlx-community/Qwen2.5-Coder-14B-Instruct-4bit \
     --prompt "Write a Python hello world" \
     --max-tokens 50
   ```

6. **Benchmark Ollama vs MLX for the 14B model**

   Create `~/benchmark-ollama-vs-mlx.py`:

   ```python
   #!/usr/bin/env python3
   """
   Benchmark: Ollama vs MLX for 14B model inference on MacBook Pro M4 Pro.

   Measures tokens/sec for a standard prompt to determine which backend
   should be primary for MacBook Pro tasks.

   Usage:
       source ~/mlx-env/bin/activate
       python3 ~/benchmark-ollama-vs-mlx.py
   """

   import time
   import subprocess
   import json
   import statistics
   from typing import NamedTuple


   class BenchmarkResult(NamedTuple):
       backend: str
       model: str
       tokens_per_sec: float
       total_tokens: int
       time_to_first_token_ms: float
       total_time_sec: float


   STANDARD_PROMPT = (
       "Explain the hexagonal architecture pattern (ports and adapters) "
       "in the context of a TypeScript CLI application. Include code examples "
       "for an adapter interface and a concrete implementation. "
       "Be thorough but concise — aim for about 300 words."
   )

   NUM_RUNS = 3  # Average over 3 runs for stability


   def benchmark_ollama(model: str = "qwen3:14b") -> list[BenchmarkResult]:
       """Benchmark Ollama's inference speed."""
       results = []
       print(f"\n{'='*60}")
       print(f"Benchmarking Ollama — {model}")
       print(f"{'='*60}")

       for run in range(NUM_RUNS):
           print(f"  Run {run + 1}/{NUM_RUNS}...", end=" ", flush=True)

           start = time.perf_counter()

           result = subprocess.run(
               [
                   "curl", "-s", "http://localhost:11434/api/generate",
                   "-d", json.dumps({
                       "model": model,
                       "prompt": STANDARD_PROMPT,
                       "stream": False,
                       "options": {"num_predict": 512},
                   }),
               ],
               capture_output=True,
               text=True,
           )

           total_time = time.perf_counter() - start

           try:
               data = json.loads(result.stdout)
               eval_count = data.get("eval_count", 0)
               eval_duration_ns = data.get("eval_duration", 1)
               prompt_eval_duration_ns = data.get("prompt_eval_duration", 0)

               tokens_per_sec = eval_count / (eval_duration_ns / 1e9) if eval_duration_ns > 0 else 0
               ttft_ms = prompt_eval_duration_ns / 1e6

               br = BenchmarkResult(
                   backend="Ollama",
                   model=model,
                   tokens_per_sec=round(tokens_per_sec, 2),
                   total_tokens=eval_count,
                   time_to_first_token_ms=round(ttft_ms, 1),
                   total_time_sec=round(total_time, 2),
               )
               results.append(br)
               print(f"{br.tokens_per_sec} tok/s ({br.total_tokens} tokens in {br.total_time_sec}s)")

           except (json.JSONDecodeError, KeyError) as e:
               print(f"ERROR: {e}")

       return results


   def benchmark_mlx(model: str = "mlx-community/Qwen3-14B-4bit") -> list[BenchmarkResult]:
       """Benchmark MLX's inference speed."""
       results = []
       print(f"\n{'='*60}")
       print(f"Benchmarking MLX — {model}")
       print(f"{'='*60}")

       for run in range(NUM_RUNS):
           print(f"  Run {run + 1}/{NUM_RUNS}...", end=" ", flush=True)

           start = time.perf_counter()

           result = subprocess.run(
               [
                   "python3", "-m", "mlx_lm.generate",
                   "--model", model,
                   "--prompt", STANDARD_PROMPT,
                   "--max-tokens", "512",
               ],
               capture_output=True,
               text=True,
           )

           total_time = time.perf_counter() - start

           # Parse MLX output for token count and speed
           output = result.stdout + result.stderr
           tokens_per_sec = 0.0
           total_tokens = 0

           for line in output.split("\n"):
               if "tok/s" in line.lower() or "tokens/s" in line.lower():
                   # MLX typically prints something like "Prompt: X tok/s, Generation: Y tok/s"
                   parts = line.split()
                   for i, part in enumerate(parts):
                       if "tok/s" in part.lower() or "tokens/s" in part.lower():
                           try:
                               tokens_per_sec = float(parts[i - 1].replace(",", ""))
                           except (ValueError, IndexError):
                               pass
               if "tokens" in line.lower() and ("generated" in line.lower() or "total" in line.lower()):
                   for part in line.split():
                       try:
                           total_tokens = int(part)
                           break
                       except ValueError:
                           pass

           # Fallback: estimate from total time if parsing fails
           if tokens_per_sec == 0 and total_time > 0:
               # Rough estimate: count words in output * 1.3 for tokens
               word_count = len(result.stdout.split())
               total_tokens = int(word_count * 1.3)
               tokens_per_sec = total_tokens / total_time if total_time > 0 else 0

           br = BenchmarkResult(
               backend="MLX",
               model=model,
               tokens_per_sec=round(tokens_per_sec, 2),
               total_tokens=total_tokens,
               time_to_first_token_ms=0,  # MLX doesn't report TTFT separately
               total_time_sec=round(total_time, 2),
           )
           results.append(br)
           print(f"{br.tokens_per_sec} tok/s ({br.total_tokens} tokens in {br.total_time_sec}s)")

       return results


   def print_summary(ollama_results: list[BenchmarkResult], mlx_results: list[BenchmarkResult]):
       """Print comparison summary and decision recommendation."""
       print(f"\n{'='*60}")
       print("BENCHMARK SUMMARY")
       print(f"{'='*60}")

       if ollama_results:
           avg_ollama = statistics.mean(r.tokens_per_sec for r in ollama_results)
           print(f"  Ollama average: {avg_ollama:.1f} tok/s")
       else:
           avg_ollama = 0
           print("  Ollama: NO RESULTS")

       if mlx_results:
           avg_mlx = statistics.mean(r.tokens_per_sec for r in mlx_results)
           print(f"  MLX average:    {avg_mlx:.1f} tok/s")
       else:
           avg_mlx = 0
           print("  MLX: NO RESULTS")

       if avg_ollama > 0 and avg_mlx > 0:
           ratio = avg_mlx / avg_ollama
           print(f"\n  MLX/Ollama ratio: {ratio:.2f}x")
           print(f"\n  {'─'*40}")

           if ratio >= 2.0:
               print(f"  ✅ DECISION: USE MLX as primary for MacBook Pro tasks")
               print(f"     MLX is {ratio:.1f}x faster — significant advantage.")
               print(f"     Keep Ollama installed for LAN API compatibility.")
           elif ratio >= 1.3:
               print(f"  ⚠️  DECISION: USE MLX as primary, Ollama as LAN fallback")
               print(f"     MLX is {ratio:.1f}x faster — moderate advantage.")
           else:
               print(f"  ℹ️  DECISION: USE OLLAMA as primary (simpler LAN integration)")
               print(f"     MLX advantage ({ratio:.1f}x) is not significant enough")
               print(f"     to justify the complexity of two inference backends.")


   if __name__ == "__main__":
       print("MacBook Pro M4 Pro — Ollama vs MLX Benchmark")
       print(f"Prompt: {STANDARD_PROMPT[:80]}...")
       print(f"Max tokens: 512")
       print(f"Runs per backend: {NUM_RUNS}")

       ollama_results = benchmark_ollama()
       mlx_results = benchmark_mlx()
       print_summary(ollama_results, mlx_results)
   ```

   Run the benchmark:
   ```bash
   source ~/mlx-env/bin/activate
   python3 ~/benchmark-ollama-vs-mlx.py
   ```

   **Why:** This gives you hard numbers to make the MLX vs Ollama decision. The benchmark runs each backend 3 times and averages to account for warmup effects.

   **Verify:** Both backends produce valid output and you get a clear recommendation.

**Decision Gate:** If MLX is 2x+ faster than Ollama for 14B models, use MLX as the primary inference backend for MacBook Pro tasks. Keep Ollama running for LAN API compatibility (the hybrid_router.py connects to Ollama's HTTP API). When the MacBook Pro needs to serve inference to the Mac Mini, it uses Ollama; for local heavy tasks, it uses MLX directly.

**Gotchas:**
- The first MLX run downloads the model (~8-9GB). Subsequent runs use the cache.
- MLX requires macOS 13.5+ and an Apple Silicon Mac. Your M4 Pro qualifies.
- Both Ollama and MLX can run simultaneously — they don't conflict. Ollama uses its own model cache, MLX uses HuggingFace's cache.

---

### 1.4 Alienware: Ollama with CUDA Setup — 1.5h

**Depends on:** None — can start immediately
**Can parallel with:** 1.1, 1.2, 1.3, 1.10
**Machine:** Alienware (Windows 11)

**Steps:**

1. **Download and install Ollama for Windows**

   Open **PowerShell as Administrator** and run:

   ```powershell
   # Option A: PowerShell one-liner
   irm https://ollama.com/install.ps1 | iex

   # Option B: Download installer manually from https://ollama.com/download/windows
   # and run OllamaSetup.exe
   ```

   **Why:** Ollama on Windows natively supports CUDA acceleration. It will auto-detect your RTX 5080.

   **Verify (open a NEW PowerShell window):**
   ```powershell
   ollama --version
   # Expected: ollama version 0.5.x
   ```

2. **Pull the vision model**

   ```powershell
   # Try Qwen3-VL first (if available in Ollama library)
   ollama pull qwen3-vl:7b

   # If qwen3-vl:7b is not available yet, fall back to:
   ollama pull qwen2.5-vl:7b
   ```

   **Why:** The vision model is used for sprite QA — it analyzes generated sprite frames for quality, palette compliance, and anatomy checks. The 7B size fits in the RTX 5080's 16GB VRAM alongside ComfyUI when it's in a light workflow state.

   **Verify:**
   ```powershell
   ollama list
   # Expected: qwen2.5-vl:7b (or qwen3-vl:7b) listed with ~5GB size
   ```

3. **Set environment variables persistently**

   Open **PowerShell as Administrator**:

   ```powershell
   # Allow LAN access (listen on all interfaces)
   [Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "User")

   # Auto-unload models after 2 minutes of inactivity
   # This frees VRAM back to ComfyUI
   [Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "2m", "User")

   # Apply to current session too
   $env:OLLAMA_HOST = "0.0.0.0:11434"
   $env:OLLAMA_KEEP_ALIVE = "2m"
   ```

   **Why:** `OLLAMA_HOST=0.0.0.0:11434` allows the Mac Mini's hybrid_router.py to send inference requests over the LAN. `OLLAMA_KEEP_ALIVE=2m` is critical for the RTX 5080's 16GB VRAM budget — after 2 minutes of no requests, Ollama unloads the model from VRAM, giving 100% GPU memory back to ComfyUI. Without this, a loaded 7B model would permanently consume ~5GB of your 16GB.

   **Restart Ollama** (close from system tray and reopen, or restart the service):
   ```powershell
   # Stop Ollama service
   Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
   # Start it again (it runs as a background process on Windows)
   Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
   ```

4. **Configure Windows Firewall to allow port 11434 on private network**

   Open **PowerShell as Administrator**:

   ```powershell
   # Create inbound firewall rule for Ollama
   New-NetFirewallRule `
     -DisplayName "Ollama LAN Access" `
     -Direction Inbound `
     -Protocol TCP `
     -LocalPort 11434 `
     -Action Allow `
     -Profile Private `
     -Description "Allow LAN machines to access Ollama API on port 11434"

   # Verify the rule was created
   Get-NetFirewallRule -DisplayName "Ollama LAN Access" | Format-Table DisplayName, Enabled, Direction, Action
   # Expected: Ollama LAN Access  True  Inbound  Allow
   ```

   **Why:** Windows Firewall blocks incoming connections by default. The `-Profile Private` flag means this rule only applies on private networks (your home LAN), not public Wi-Fi.

5. **Verify CUDA acceleration is working**

   ```powershell
   # Run the vision model with a test prompt
   ollama run qwen2.5-vl:7b "Describe what you see in this prompt: a pixel art fighter character."

   # While it's running, check GPU utilization in a separate PowerShell:
   nvidia-smi
   # Expected: Ollama process visible in the process list, GPU utilization > 0%
   ```

   You can also check Ollama's logs for CUDA detection:
   ```powershell
   # Ollama logs are typically in %LOCALAPPDATA%\Ollama\logs
   Get-Content "$env:LOCALAPPDATA\Ollama\logs\server.log" -Tail 20
   # Look for lines mentioning "cuda" or "GPU" or "NVIDIA"
   ```

   **Verify:** `nvidia-smi` shows Ollama using the GPU, and the model responds in a few seconds (not minutes — minutes would indicate CPU fallback).

**Gotchas:**
- If Ollama falls back to CPU inference, ensure your NVIDIA drivers are up to date: `nvidia-smi` should show driver version 570+ for RTX 5080.
- The `OLLAMA_KEEP_ALIVE=2m` is per-model. If you run two models, both get the 2-minute timer independently.
- After setting environment variables, you MUST restart Ollama for them to take effect. Closing the PowerShell window is not enough — close Ollama from the system tray.

---

### 1.5 Alienware: ComfyUI Fresh Install for RTX 5080 — 2.5h

**Depends on:** None — can start immediately (but easier after 1.4 confirms CUDA works)
**Can parallel with:** 1.1, 1.2, 1.3, 1.10
**Machine:** Alienware (Windows 11)

**Steps:**

1. **Install Python 3.12 and Git for Windows (if not already installed)**

   ```powershell
   # Check if Python is installed
   python --version
   # If not installed, download from https://www.python.org/downloads/
   # IMPORTANT: Check "Add Python to PATH" during installation

   # Check if Git is installed
   git --version
   # If not installed, download from https://git-scm.com/download/win
   ```

2. **Clone ComfyUI v0.18.2**

   ```powershell
   cd C:\
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   git checkout v0.18.2
   ```

   **Why:** v0.18.2 includes the built-in NanoBanana2 API node and is the validated stable version for RTX 5080.

   **Verify:**
   ```powershell
   git log --oneline -1
   # Expected: commit hash with v0.18.2 tag
   ```

3. **Create Python virtual environment and install PyTorch with CUDA 12.8**

   ```powershell
   cd C:\ComfyUI
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Install PyTorch stable with CUDA 12.8 support
   # THIS IS THE CORRECT COMMAND — NOT nightly, NOT cu124
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
   ```

   **Why:** The RTX 5080 uses the Blackwell architecture (sm_120) which requires CUDA 12.8+. PyTorch stable ≥2.7.0 with cu128 now supports sm_120 natively — you no longer need nightly builds.

   **Verify CUDA works:**
   ```powershell
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
   # Expected:
   # CUDA available: True
   # CUDA version: 12.8
   # GPU: NVIDIA GeForce RTX 5080
   ```

   **CRITICAL CHECK — verify xformers is NOT installed:**
   ```powershell
   pip list | Select-String "xformers"
   # Expected: NO OUTPUT (empty). If xformers appears, uninstall it immediately:
   # pip uninstall xformers -y
   ```

4. **Install ComfyUI dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

5. **Install ComfyUI Manager**

   ```powershell
   cd C:\ComfyUI\custom_nodes
   git clone https://github.com/ltdrdata/ComfyUI-Manager.git
   ```

   **Why:** ComfyUI Manager provides a UI for installing and managing custom nodes, models, and updates.

6. **Install required custom nodes**

   ```powershell
   cd C:\ComfyUI\custom_nodes

   # IP-Adapter Plus — for style transfer and character consistency
   git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus.git

   # ControlNet Auxiliary Preprocessors — for OpenPose, depth, etc.
   git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git

   # Comfyroll Custom Nodes — utility nodes for workflows
   git clone https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes.git

   # Install each node's requirements
   cd ComfyUI_IPAdapter_plus && pip install -r requirements.txt 2>$null; cd ..
   cd comfyui_controlnet_aux && pip install -r requirements.txt 2>$null; cd ..
   cd ComfyUI_Comfyroll_CustomNodes && pip install -r requirements.txt 2>$null; cd ..
   ```

7. **Download required models**

   ```powershell
   cd C:\ComfyUI

   # Illustrious XL v2.0-STABLE (updated base model per audit)
   # Download from HuggingFace — ~7GB
   Invoke-WebRequest -Uri "https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0/resolve/main/Illustrious-XL-v2.0-STABLE.safetensors" `
     -OutFile "models\checkpoints\Illustrious-XL-v2.0-STABLE.safetensors"

   # ControlNet OpenPose for SDXL
   Invoke-WebRequest -Uri "https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0/resolve/main/control-lora-openposeXL2-rank256.safetensors" `
     -OutFile "models\controlnet\control-lora-openposeXL2-rank256.safetensors"

   # IP-Adapter for SDXL
   Invoke-WebRequest -Uri "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors" `
     -OutFile "models\ipadapter\ip-adapter-plus_sdxl_vit-h.safetensors"

   # CLIP Vision model (required by IP-Adapter)
   # Create directory if needed
   New-Item -ItemType Directory -Path "models\clip_vision" -Force
   Invoke-WebRequest -Uri "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors" `
     -OutFile "models\clip_vision\CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
   ```

   **Why:** Illustrious XL v2.0-STABLE is the updated base model specifically designed for 2D illustration (per the March 2026 audit). The ControlNet, IP-Adapter, and CLIP Vision models are needed for the sprite generation workflows that maintain character consistency.

   **Note:** These are large downloads (7GB+ for the base model). If you have a slow connection, consider downloading overnight.

8. **Add training directories to Windows Defender exclusion list**

   Open **PowerShell as Administrator**:

   ```powershell
   # Exclude ComfyUI directories from Windows Defender real-time scanning
   # This prevents Defender from scanning every generated image, which slows things dramatically
   Add-MpPreference -ExclusionPath "C:\ComfyUI"
   Add-MpPreference -ExclusionPath "C:\ComfyUI\output"
   Add-MpPreference -ExclusionPath "C:\ComfyUI\temp"
   Add-MpPreference -ExclusionPath "C:\ComfyUI\models"

   # Verify exclusions were added
   Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
   # Expected: All four paths listed
   ```

   **Why:** Windows Defender's real-time scanning intercepts every file write. During ComfyUI generation and LoRA training, this creates thousands of file writes per minute. Without exclusions, Defender can slow operations by 30-50%.

9. **Launch ComfyUI and verify it works**

   ```powershell
   cd C:\ComfyUI
   .\venv\Scripts\Activate.ps1

   # Start ComfyUI with LAN access enabled
   python main.py --listen 0.0.0.0 --port 8188
   ```

   Open a browser and navigate to `http://localhost:8188`

   **Verify:**
   - The ComfyUI interface loads without errors
   - ComfyUI Manager appears in the sidebar
   - No Python errors in the terminal about CUDA or missing modules

10. **Test image generation**

    In the ComfyUI UI:
    1. Load the default workflow (drag the default workflow JSON or use Queue Prompt with the default nodes)
    2. Set the checkpoint to `Illustrious-XL-v2.0-STABLE.safetensors`
    3. Set a simple prompt: "pixel art fighter character, SF2 style, transparent background"
    4. Click "Queue Prompt"
    5. Verify an image generates without errors

    **Verify from another machine via REST API:**
    ```bash
    # FROM MAC MINI — replace IP with Alienware's actual IP
    curl http://192.168.1.102:8188/system_stats
    # Expected: JSON response with GPU info and queue status
    ```

11. **Configure REST API access**

    ComfyUI's REST API is automatically available at `http://0.0.0.0:8188` when you start with `--listen 0.0.0.0`. You also need a Windows Firewall rule:

    Open **PowerShell as Administrator**:
    ```powershell
    New-NetFirewallRule `
      -DisplayName "ComfyUI LAN Access" `
      -Direction Inbound `
      -Protocol TCP `
      -LocalPort 8188 `
      -Action Allow `
      -Profile Private `
      -Description "Allow LAN machines to access ComfyUI REST API on port 8188"
    ```

**Decision Gate:** N/A — ComfyUI must work. If CUDA verification fails, check your NVIDIA driver version (`nvidia-smi`). You need driver 570+ for RTX 5080.

**Gotchas:**
- **Do NOT install xformers.** The RTX 5080 uses SDPA (Scaled Dot Product Attention, built into PyTorch). If you see `cutlassF` errors at any point, xformers snuck in — check with `pip list | Select-String xformers` and uninstall.
- If ComfyUI crashes with a CUDA out-of-memory error on the first generation, make sure Ollama has unloaded its model (wait 2 minutes after your last `ollama run` command, or restart Ollama).
- The `--listen 0.0.0.0` flag is required for LAN access. Without it, ComfyUI only listens on localhost.
- Model downloads via `Invoke-WebRequest` can be slow. An alternative is to use a browser to download from HuggingFace and manually place files in the correct directories.

---

### 1.6 Three-Machine Networking — 1.5h

**Depends on:** 1.1, 1.3, 1.4 (all three machines need Ollama running)
**Can parallel with:** 1.10
**Machine:** All three (primarily configured from Mac Mini)

**Steps:**

1. **Assign static IPs or DHCP reservations**

   The best approach is DHCP reservations in your router. This way, each machine always gets the same IP via DHCP without changing any machine settings.

   Log into your router admin page (typically `192.168.1.1`) and create reservations:

   | Machine | MAC Address | Reserved IP | How to Find MAC |
   |---------|-------------|-------------|-----------------|
   | Mac Mini | `(find below)` | 192.168.1.100 | `ifconfig en0 \| grep ether` |
   | MacBook Pro | `(find below)` | 192.168.1.101 | `ifconfig en0 \| grep ether` |
   | Alienware | `(find below)` | 192.168.1.102 | PowerShell: `Get-NetAdapter \| Select Name,MacAddress` |

   **Find MAC addresses:**

   On **Mac Mini**:
   ```bash
   ifconfig en0 | grep ether
   # Example: ether a8:b1:c2:d3:e4:f5
   ```

   On **MacBook Pro**:
   ```bash
   ifconfig en0 | grep ether
   ```

   On **Alienware** (PowerShell):
   ```powershell
   Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object Name, MacAddress
   # Use the Ethernet adapter's MAC address for WOL
   ```

   **Why:** Static IPs ensure the hybrid_router.py config never breaks when machines get different IPs from DHCP.

   **Alternative if you can't access router:** Set static IPs on each machine directly.

   Mac Mini static IP (if needed):
   ```bash
   # System Settings → Network → Ethernet → Details → TCP/IP
   # Set "Configure IPv4" to "Manually"
   # IP: 192.168.1.100, Subnet: 255.255.255.0, Router: 192.168.1.1
   ```

2. **Test connectivity between all machines**

   From **Mac Mini**:
   ```bash
   # Test MacBook Pro Ollama
   curl -s http://192.168.1.101:11434/api/tags | python3 -m json.tool
   # Expected: JSON with qwen3:14b and qwen2.5-coder:14b

   # Test Alienware Ollama
   curl -s http://192.168.1.102:11434/api/tags | python3 -m json.tool
   # Expected: JSON with qwen2.5-vl:7b

   # Test Alienware ComfyUI
   curl -s http://192.168.1.102:8188/system_stats | python3 -m json.tool
   # Expected: JSON with GPU info
   ```

   From **Alienware** (PowerShell):
   ```powershell
   # Test Mac Mini Ollama
   Invoke-RestMethod -Uri "http://192.168.1.100:11434/api/tags"
   # Expected: Models list with phi4-mini-reasoning

   # Test MacBook Pro Ollama
   Invoke-RestMethod -Uri "http://192.168.1.101:11434/api/tags"
   ```

3. **Configure Wake-on-LAN for Alienware**

   The Alienware should be asleep most of the time to save power. The Mac Mini wakes it via magic packet when CUDA tasks are needed.

   **On Alienware — BIOS/UEFI settings:**
   1. Restart the Alienware and press F2 during boot to enter BIOS
   2. Navigate to Power Management or Power Options
   3. Find "Wake on LAN" or "Wake on LAN/WLAN" → set to **Enabled**
   4. Save and exit BIOS

   **On Alienware — Windows Device Manager:**
   1. Open Device Manager (Win+X → Device Manager)
   2. Expand "Network adapters"
   3. Right-click your Ethernet adapter → Properties
   4. **Advanced tab:** Find "Wake on Magic Packet" → set to **Enabled**
   5. **Power Management tab:** Check all three boxes:
      - "Allow the computer to turn off this device to save power"
      - "Allow this device to wake the computer"
      - "Only allow a magic packet to wake the computer"

   **On Alienware — Windows Power Settings:**
   ```powershell
   # Disable Fast Startup (interferes with WOL)
   powercfg /h off

   # Verify
   powercfg /a
   # Look for "S4 (Hibernate)" and "S5 (Soft Off)" states
   ```

   **Why:** Fast Startup puts the PC in a hybrid shutdown/hibernate state that some network adapters can't wake from. Disabling it ensures clean Wake-on-LAN behavior.

4. **Install wakeonlan on Mac Mini**

   ```bash
   brew install wakeonlan
   ```

5. **Test WOL: send magic packet from Mac Mini**

   First, put the Alienware to sleep (Start → Power → Sleep).

   Then from the **Mac Mini**:
   ```bash
   # Replace with Alienware's actual MAC address (found in step 1)
   wakeonlan -i 192.168.1.255 AA:BB:CC:DD:EE:FF
   ```

   **Why:** The `-i 192.168.1.255` flag sends the magic packet to the broadcast address of your subnet, ensuring it reaches the sleeping Alienware.

   Wait 15-30 seconds, then verify:
   ```bash
   ping -c 3 192.168.1.102
   # Expected: replies within 1-2 seconds (machine is awake)
   ```

   **Troubleshooting if WOL doesn't work:**
   - Verify BIOS setting is enabled (most common issue)
   - Ensure you're using the Ethernet adapter's MAC address, not Wi-Fi
   - The Alienware must be in Sleep (S3) or Soft Off (S5) — not Hibernate (S4)
   - Try the broadcast address: `wakeonlan -i 255.255.255.255 AA:BB:CC:DD:EE:FF`
   - Some routers block broadcast packets — try from a machine on the same switch

6. **Create a network health check script**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/network-test.sh` on the **Mac Mini**:

   ```bash
   #!/bin/bash
   # network-test.sh — Check all three machines and their services
   # Usage: ./scripts/network-test.sh

   set -euo pipefail

   # Configure IPs (update these to match your actual IPs)
   MAC_MINI_IP="192.168.1.100"
   MACBOOK_IP="192.168.1.101"
   ALIENWARE_IP="192.168.1.102"

   RED='\033[0;31m'
   GREEN='\033[0;32m'
   YELLOW='\033[0;33m'
   NC='\033[0m' # No Color

   check_ping() {
       local name="$1"
       local ip="$2"
       if ping -c 1 -W 2 "$ip" &>/dev/null; then
           echo -e "  ${GREEN}✓${NC} $name ($ip) — ONLINE"
           return 0
       else
           echo -e "  ${RED}✗${NC} $name ($ip) — OFFLINE"
           return 1
       fi
   }

   check_ollama() {
       local name="$1"
       local ip="$2"
       local response
       response=$(curl -s --connect-timeout 3 "http://$ip:11434/api/tags" 2>/dev/null || echo "FAIL")
       if [[ "$response" != "FAIL" ]] && echo "$response" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
           local models
           models=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>/dev/null)
           echo -e "  ${GREEN}✓${NC} $name Ollama — RUNNING (models: $models)"
           return 0
       else
           echo -e "  ${RED}✗${NC} $name Ollama — NOT RESPONDING"
           return 1
       fi
   }

   check_comfyui() {
       local ip="$1"
       local response
       response=$(curl -s --connect-timeout 3 "http://$ip:8188/system_stats" 2>/dev/null || echo "FAIL")
       if [[ "$response" != "FAIL" ]] && echo "$response" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
           echo -e "  ${GREEN}✓${NC} Alienware ComfyUI — RUNNING"
           return 0
       else
           echo -e "  ${YELLOW}⚠${NC} Alienware ComfyUI — NOT RESPONDING (may need manual start)"
           return 1
       fi
   }

   echo "============================================"
   echo "  Three-Machine Network Health Check"
   echo "  $(date '+%Y-%m-%d %H:%M:%S')"
   echo "============================================"
   echo ""

   echo "PING TEST:"
   check_ping "Mac Mini" "$MAC_MINI_IP"
   check_ping "MacBook Pro" "$MACBOOK_IP"
   check_ping "Alienware" "$ALIENWARE_IP"

   echo ""
   echo "OLLAMA STATUS:"
   check_ollama "Mac Mini" "$MAC_MINI_IP"
   check_ollama "MacBook Pro" "$MACBOOK_IP"
   check_ollama "Alienware" "$ALIENWARE_IP"

   echo ""
   echo "COMFYUI STATUS:"
   check_comfyui "$ALIENWARE_IP"

   echo ""
   echo "============================================"
   ```

   Make it executable:
   ```bash
   chmod +x ~/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/network-test.sh
   ```

   Run it:
   ```bash
   ./scripts/network-test.sh
   ```

   **Verify:** The script reports status for all three machines. Green checkmarks for online services, red X for offline ones. The MacBook Pro will show offline when the laptop lid is closed — that's expected.

**Gotchas:**
- If you're on Wi-Fi, the IPs may differ between Ethernet and Wi-Fi. Use Ethernet for all stationary machines (Mac Mini, Alienware) for reliability.
- The MacBook Pro will not be reachable when the lid is closed (Sleep mode). This is by design — the hybrid_router.py handles this gracefully.

---

### 1.7 hybrid_router.py Implementation — 4h

**Depends on:** 1.1, 1.3, 1.4, 1.6 (all machines online and networked)
**Can parallel with:** 1.10
**Machine:** Mac Mini (where the file lives and runs)

**Steps:**

1. **Create the routing configuration**

   Add this section to `~/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml`:

   ```toml
   # ─── Three-Machine Routing Configuration ───

   [routing]
   # Health check interval in seconds
   health_check_interval = 30
   # Timeout for health check pings (seconds)
   health_check_timeout = 3
   # Timeout for inference requests (seconds)
   inference_timeout = 120
   # Claude API fallback (requires ANTHROPIC_API_KEY or claude login)
   enable_api_fallback = true
   api_fallback_model = "claude-sonnet-4-20250514"

   [routing.machines.mac_mini]
   name = "Mac Mini"
   host = "192.168.1.100"
   port = 11434
   always_on = true
   models = ["phi4-mini-reasoning", "nomic-embed-text"]
   max_model_size = "7B"

   [routing.machines.macbook_pro]
   name = "MacBook Pro"
   host = "192.168.1.101"
   port = 11434
   always_on = false
   models = ["qwen3:14b", "qwen2.5-coder:14b"]
   max_model_size = "32B"

   [routing.machines.alienware]
   name = "Alienware"
   host = "192.168.1.102"
   port = 11434
   always_on = false
   models = ["qwen2.5-vl:7b"]
   max_model_size = "14B"
   wol_mac = "AA:BB:CC:DD:EE:FF"  # Replace with actual MAC
   wol_broadcast = "192.168.1.255"
   wol_wait_seconds = 45

   # Model-to-machine routing preferences
   # Format: model_pattern = "preferred_machine, fallback_machine, ..."
   [routing.model_map]
   "phi4-mini-reasoning" = "mac_mini"
   "nomic-embed-text" = "mac_mini"
   "qwen3:14b" = "macbook_pro, mac_mini"
   "qwen2.5-coder:14b" = "macbook_pro"
   "qwen2.5-vl:7b" = "alienware"
   "qwen3-vl:7b" = "alienware"
   ```

2. **Implement hybrid_router.py**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/hybrid_router.py`:

   ```python
   #!/usr/bin/env python3
   """
   hybrid_router.py — Three-tier routing for the multi-machine agent fleet.

   Routes inference requests to the optimal machine based on model requirements,
   machine availability, and VRAM constraints. Includes health checking,
   Wake-on-LAN for the Alienware, and Claude API fallback.

   Routing order:
     1. Preferred machine (from model_map in config.toml)
     2. Secondary machine (fallback in model_map)
     3. Any available machine that has the model
     4. Claude API fallback (if enabled)

   Usage:
       from lib.hybrid_router import HybridRouter

       router = HybridRouter.from_config("config.toml")
       response = await router.generate("qwen3:14b", "Explain adapters.")
       response = await router.embed("nomic-embed-text", "sprite pipeline")
   """

   import asyncio
   import hashlib
   import json
   import logging
   import subprocess
   import time
   from dataclasses import dataclass, field
   from enum import Enum
   from pathlib import Path
   from typing import Any, Optional

   import httpx
   import toml

   logger = logging.getLogger("hybrid_router")


   class MachineStatus(Enum):
       ONLINE = "online"
       OFFLINE = "offline"
       WAKING = "waking"
       UNKNOWN = "unknown"


   @dataclass
   class MachineConfig:
       name: str
       host: str
       port: int
       always_on: bool
       models: list[str]
       max_model_size: str
       wol_mac: Optional[str] = None
       wol_broadcast: Optional[str] = None
       wol_wait_seconds: int = 45
       status: MachineStatus = MachineStatus.UNKNOWN
       last_health_check: float = 0.0
       loaded_models: list[str] = field(default_factory=list)

       @property
       def base_url(self) -> str:
           return f"http://{self.host}:{self.port}"


   @dataclass
   class RoutingResult:
       success: bool
       machine: Optional[str]
       model: str
       response: Any = None
       error: Optional[str] = None
       fallback_used: bool = False
       latency_ms: float = 0.0


   class HybridRouter:
       """Three-tier inference router with health checking and WOL."""

       def __init__(
           self,
           machines: dict[str, MachineConfig],
           model_map: dict[str, list[str]],
           health_check_interval: int = 30,
           health_check_timeout: int = 3,
           inference_timeout: int = 120,
           enable_api_fallback: bool = True,
           api_fallback_model: str = "claude-sonnet-4-20250514",
       ):
           self.machines = machines
           self.model_map = model_map
           self.health_check_interval = health_check_interval
           self.health_check_timeout = health_check_timeout
           self.inference_timeout = inference_timeout
           self.enable_api_fallback = enable_api_fallback
           self.api_fallback_model = api_fallback_model
           self._client = httpx.AsyncClient(timeout=inference_timeout)
           self._health_client = httpx.AsyncClient(timeout=health_check_timeout)

       @classmethod
       def from_config(cls, config_path: str = "config.toml") -> "HybridRouter":
           """Load router configuration from config.toml."""
           config = toml.load(config_path)
           routing = config.get("routing", {})

           machines = {}
           for key, mc in routing.get("machines", {}).items():
               machines[key] = MachineConfig(
                   name=mc["name"],
                   host=mc["host"],
                   port=mc["port"],
                   always_on=mc.get("always_on", False),
                   models=mc.get("models", []),
                   max_model_size=mc.get("max_model_size", "7B"),
                   wol_mac=mc.get("wol_mac"),
                   wol_broadcast=mc.get("wol_broadcast"),
                   wol_wait_seconds=mc.get("wol_wait_seconds", 45),
               )

           model_map = {}
           for model, targets in routing.get("model_map", {}).items():
               if isinstance(targets, str):
                   model_map[model] = [t.strip() for t in targets.split(",")]
               else:
                   model_map[model] = targets

           return cls(
               machines=machines,
               model_map=model_map,
               health_check_interval=routing.get("health_check_interval", 30),
               health_check_timeout=routing.get("health_check_timeout", 3),
               inference_timeout=routing.get("inference_timeout", 120),
               enable_api_fallback=routing.get("enable_api_fallback", True),
               api_fallback_model=routing.get("api_fallback_model", "claude-sonnet-4-20250514"),
           )

       async def health_check(self, machine_key: str) -> MachineStatus:
           """Check if a machine's Ollama instance is responding."""
           machine = self.machines[machine_key]
           now = time.time()

           # Cache health check results for the configured interval
           if (
               now - machine.last_health_check < self.health_check_interval
               and machine.status != MachineStatus.UNKNOWN
           ):
               return machine.status

           try:
               response = await self._health_client.get(
                   f"{machine.base_url}/api/tags"
               )
               if response.status_code == 200:
                   data = response.json()
                   machine.loaded_models = [
                       m["name"] for m in data.get("models", [])
                   ]
                   machine.status = MachineStatus.ONLINE
                   machine.last_health_check = now
                   logger.debug(
                       f"Health check {machine.name}: ONLINE "
                       f"(models: {machine.loaded_models})"
                   )
                   return MachineStatus.ONLINE
           except (httpx.ConnectError, httpx.TimeoutException, httpx.ConnectTimeout):
               pass
           except Exception as e:
               logger.warning(f"Health check {machine.name}: unexpected error: {e}")

           machine.status = MachineStatus.OFFLINE
           machine.last_health_check = now
           logger.debug(f"Health check {machine.name}: OFFLINE")
           return MachineStatus.OFFLINE

       async def health_check_all(self) -> dict[str, MachineStatus]:
           """Check health of all machines in parallel."""
           tasks = {
               key: self.health_check(key) for key in self.machines
           }
           results = {}
           for key, task in tasks.items():
               results[key] = await task
           return results

       async def wake_machine(self, machine_key: str) -> bool:
           """Send Wake-on-LAN magic packet to a machine."""
           machine = self.machines[machine_key]
           if not machine.wol_mac:
               logger.warning(f"No WOL MAC configured for {machine.name}")
               return False

           logger.info(f"Sending WOL magic packet to {machine.name} ({machine.wol_mac})")
           machine.status = MachineStatus.WAKING

           try:
               cmd = ["wakeonlan"]
               if machine.wol_broadcast:
                   cmd.extend(["-i", machine.wol_broadcast])
               cmd.append(machine.wol_mac)

               subprocess.run(cmd, check=True, capture_output=True, text=True)
           except FileNotFoundError:
               logger.error("wakeonlan not installed. Run: brew install wakeonlan")
               return False
           except subprocess.CalledProcessError as e:
               logger.error(f"WOL failed: {e.stderr}")
               return False

           # Wait for machine to boot and Ollama to start
           logger.info(
               f"Waiting {machine.wol_wait_seconds}s for {machine.name} to wake..."
           )
           await asyncio.sleep(machine.wol_wait_seconds)

           # Check if it's actually up
           status = await self.health_check(machine_key)
           if status == MachineStatus.ONLINE:
               logger.info(f"{machine.name} is now ONLINE after WOL")
               return True

           # Retry once with shorter wait
           logger.info(f"{machine.name} not ready yet, waiting 15s more...")
           await asyncio.sleep(15)
           status = await self.health_check(machine_key)
           success = status == MachineStatus.ONLINE
           if success:
               logger.info(f"{machine.name} is now ONLINE after WOL (retry)")
           else:
               logger.error(f"{machine.name} failed to wake after WOL")
           return success

       def _resolve_routing(self, model: str) -> list[str]:
           """Determine the ordered list of machines to try for a model."""
           # Check explicit model map first
           if model in self.model_map:
               return self.model_map[model]

           # Check partial matches (e.g., "qwen3" matches "qwen3:14b")
           for pattern, targets in self.model_map.items():
               if pattern in model or model in pattern:
                   return targets

           # Fallback: try all machines in order (mac_mini → macbook_pro → alienware)
           return list(self.machines.keys())

       async def _try_generate(
           self, machine_key: str, model: str, prompt: str, **kwargs
       ) -> Optional[dict]:
           """Attempt to generate on a specific machine."""
           machine = self.machines[machine_key]

           status = await self.health_check(machine_key)
           if status != MachineStatus.ONLINE:
               # If machine has WOL and is offline, try waking it
               if machine.wol_mac and status == MachineStatus.OFFLINE:
                   if not await self.wake_machine(machine_key):
                       return None
               else:
                   return None

           try:
               payload = {
                   "model": model,
                   "prompt": prompt,
                   "stream": False,
                   **kwargs,
               }
               response = await self._client.post(
                   f"{machine.base_url}/api/generate",
                   json=payload,
               )
               if response.status_code == 200:
                   return response.json()
               else:
                   logger.warning(
                       f"Generate failed on {machine.name}: HTTP {response.status_code}"
                   )
                   return None
           except (httpx.ConnectError, httpx.TimeoutException) as e:
               logger.warning(f"Generate failed on {machine.name}: {e}")
               machine.status = MachineStatus.OFFLINE
               return None

       async def generate(
           self, model: str, prompt: str, **kwargs
       ) -> RoutingResult:
           """
           Route a generation request through the three-tier chain.

           Args:
               model: Ollama model name (e.g., "qwen3:14b")
               prompt: The prompt to send
               **kwargs: Additional Ollama API parameters (temperature, num_predict, etc.)

           Returns:
               RoutingResult with response data or error
           """
           start = time.perf_counter()
           route = self._resolve_routing(model)

           for machine_key in route:
               if machine_key not in self.machines:
                   logger.warning(f"Unknown machine in route: {machine_key}")
                   continue

               logger.info(
                   f"Trying {self.machines[machine_key].name} for {model}..."
               )
               result = await self._try_generate(machine_key, model, prompt, **kwargs)

               if result is not None:
                   latency = (time.perf_counter() - start) * 1000
                   return RoutingResult(
                       success=True,
                       machine=machine_key,
                       model=model,
                       response=result,
                       latency_ms=latency,
                   )

           # All local machines failed — try Claude API fallback
           if self.enable_api_fallback:
               logger.warning(
                   f"All local machines failed for {model}. "
                   f"Falling back to Claude API ({self.api_fallback_model})."
               )
               try:
                   # Use claude-agent-sdk for API fallback
                   from claude_agent_sdk import query, ClaudeAgentOptions

                   options = ClaudeAgentOptions(
                       max_turns=1,
                       system_prompt="You are a helpful assistant.",
                   )
                   api_result = await query(prompt=prompt, options=options)
                   latency = (time.perf_counter() - start) * 1000

                   return RoutingResult(
                       success=True,
                       machine="claude_api",
                       model=self.api_fallback_model,
                       response={"response": str(api_result)},
                       fallback_used=True,
                       latency_ms=latency,
                   )
               except Exception as e:
                   logger.error(f"Claude API fallback failed: {e}")

           latency = (time.perf_counter() - start) * 1000
           return RoutingResult(
               success=False,
               machine=None,
               model=model,
               error=f"All machines and API fallback failed for model {model}",
               latency_ms=latency,
           )

       async def embed(
           self, model: str, text: str
       ) -> RoutingResult:
           """Route an embedding request."""
           start = time.perf_counter()
           route = self._resolve_routing(model)

           for machine_key in route:
               if machine_key not in self.machines:
                   continue

               machine = self.machines[machine_key]
               status = await self.health_check(machine_key)
               if status != MachineStatus.ONLINE:
                   continue

               try:
                   response = await self._client.post(
                       f"{machine.base_url}/api/embeddings",
                       json={"model": model, "prompt": text},
                   )
                   if response.status_code == 200:
                       latency = (time.perf_counter() - start) * 1000
                       return RoutingResult(
                           success=True,
                           machine=machine_key,
                           model=model,
                           response=response.json(),
                           latency_ms=latency,
                       )
               except (httpx.ConnectError, httpx.TimeoutException):
                   continue

           latency = (time.perf_counter() - start) * 1000
           return RoutingResult(
               success=False,
               machine=None,
               model=model,
               error=f"No machine available for embedding model {model}",
               latency_ms=latency,
           )

       async def fleet_status(self) -> dict:
           """Get current status of all machines and loaded models."""
           statuses = await self.health_check_all()
           return {
               key: {
                   "name": machine.name,
                   "status": statuses[key].value,
                   "host": f"{machine.host}:{machine.port}",
                   "models_available": machine.models,
                   "models_loaded": machine.loaded_models,
                   "always_on": machine.always_on,
                   "has_wol": machine.wol_mac is not None,
               }
               for key, machine in self.machines.items()
           }

       async def close(self):
           """Close HTTP clients."""
           await self._client.aclose()
           await self._health_client.aclose()


   # ─── CLI interface for testing ───

   async def _cli_main():
       import argparse

       parser = argparse.ArgumentParser(description="Test the hybrid router")
       parser.add_argument("--config", default="config.toml", help="Config file path")
       parser.add_argument("--status", action="store_true", help="Show fleet status")
       parser.add_argument("--model", help="Model to use for generation")
       parser.add_argument("--prompt", help="Prompt for generation test")
       parser.add_argument("--wake", help="Wake a specific machine (e.g., alienware)")

       args = parser.parse_args()

       logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
       router = HybridRouter.from_config(args.config)

       try:
           if args.status:
               status = await router.fleet_status()
               print(json.dumps(status, indent=2))

           elif args.wake:
               success = await router.wake_machine(args.wake)
               print(f"Wake {'succeeded' if success else 'FAILED'}")

           elif args.model and args.prompt:
               result = await router.generate(args.model, args.prompt)
               if result.success:
                   print(f"Machine: {result.machine}")
                   print(f"Latency: {result.latency_ms:.0f}ms")
                   print(f"Fallback: {result.fallback_used}")
                   print(f"Response: {result.response.get('response', '')[:500]}")
               else:
                   print(f"FAILED: {result.error}")

           else:
               parser.print_help()
       finally:
           await router.close()


   if __name__ == "__main__":
       asyncio.run(_cli_main())
   ```

3. **Write unit tests**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_hybrid_router.py`:

   ```python
   """Tests for hybrid_router.py — routing logic, health checks, WOL."""

   import asyncio
   import json
   import pytest
   from unittest.mock import AsyncMock, MagicMock, patch
   from lib.hybrid_router import (
       HybridRouter,
       MachineConfig,
       MachineStatus,
       RoutingResult,
   )


   @pytest.fixture
   def sample_machines():
       return {
           "mac_mini": MachineConfig(
               name="Mac Mini",
               host="192.168.1.100",
               port=11434,
               always_on=True,
               models=["phi4-mini-reasoning", "nomic-embed-text"],
               max_model_size="7B",
           ),
           "macbook_pro": MachineConfig(
               name="MacBook Pro",
               host="192.168.1.101",
               port=11434,
               always_on=False,
               models=["qwen3:14b", "qwen2.5-coder:14b"],
               max_model_size="32B",
           ),
           "alienware": MachineConfig(
               name="Alienware",
               host="192.168.1.102",
               port=11434,
               always_on=False,
               models=["qwen2.5-vl:7b"],
               max_model_size="14B",
               wol_mac="AA:BB:CC:DD:EE:FF",
               wol_broadcast="192.168.1.255",
               wol_wait_seconds=5,  # Short for testing
           ),
       }


   @pytest.fixture
   def sample_model_map():
       return {
           "phi4-mini-reasoning": ["mac_mini"],
           "nomic-embed-text": ["mac_mini"],
           "qwen3:14b": ["macbook_pro", "mac_mini"],
           "qwen2.5-coder:14b": ["macbook_pro"],
           "qwen2.5-vl:7b": ["alienware"],
       }


   @pytest.fixture
   def router(sample_machines, sample_model_map):
       return HybridRouter(
           machines=sample_machines,
           model_map=sample_model_map,
           health_check_interval=0,  # No caching for tests
           health_check_timeout=1,
           inference_timeout=5,
           enable_api_fallback=False,
       )


   class TestRouteResolution:
       def test_exact_model_match(self, router):
           route = router._resolve_routing("phi4-mini-reasoning")
           assert route == ["mac_mini"]

       def test_model_with_fallback(self, router):
           route = router._resolve_routing("qwen3:14b")
           assert route == ["macbook_pro", "mac_mini"]

       def test_unknown_model_returns_all(self, router):
           route = router._resolve_routing("llama3:70b")
           assert set(route) == {"mac_mini", "macbook_pro", "alienware"}

       def test_vision_model_routes_to_alienware(self, router):
           route = router._resolve_routing("qwen2.5-vl:7b")
           assert route == ["alienware"]


   class TestMachineConfig:
       def test_base_url(self, sample_machines):
           assert sample_machines["mac_mini"].base_url == "http://192.168.1.100:11434"

       def test_wol_config(self, sample_machines):
           assert sample_machines["alienware"].wol_mac == "AA:BB:CC:DD:EE:FF"
           assert sample_machines["mac_mini"].wol_mac is None


   class TestHealthCheck:
       @pytest.mark.asyncio
       async def test_online_machine(self, router):
           mock_response = MagicMock()
           mock_response.status_code = 200
           mock_response.json.return_value = {
               "models": [{"name": "phi4-mini-reasoning"}]
           }

           with patch.object(router._health_client, "get", return_value=mock_response):
               status = await router.health_check("mac_mini")

           assert status == MachineStatus.ONLINE
           assert "phi4-mini-reasoning" in router.machines["mac_mini"].loaded_models

       @pytest.mark.asyncio
       async def test_offline_machine(self, router):
           import httpx
           with patch.object(
               router._health_client, "get",
               side_effect=httpx.ConnectError("refused")
           ):
               status = await router.health_check("macbook_pro")

           assert status == MachineStatus.OFFLINE


   class TestFleetStatus:
       @pytest.mark.asyncio
       async def test_fleet_status_structure(self, router):
           mock_response = MagicMock()
           mock_response.status_code = 200
           mock_response.json.return_value = {"models": []}

           with patch.object(router._health_client, "get", return_value=mock_response):
               status = await router.fleet_status()

           assert "mac_mini" in status
           assert "macbook_pro" in status
           assert "alienware" in status
           assert status["mac_mini"]["always_on"] is True
           assert status["alienware"]["has_wol"] is True
   ```

4. **Test the router manually**

   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   source .venv/bin/activate

   # Check fleet status
   PYTHONPATH=. python3 lib/hybrid_router.py --config config.toml --status

   # Test generation routing
   PYTHONPATH=. python3 lib/hybrid_router.py --config config.toml \
     --model phi4-mini-reasoning \
     --prompt "What is the adapter pattern?"

   # Run unit tests
   PYTHONPATH=. python3 -m pytest tests/test_hybrid_router.py -v
   ```

   **Verify:** Fleet status shows Mac Mini online, generation returns a response, all unit tests pass.

**Gotchas:**
- The config.toml IPs must match your actual network. Update them after completing task 1.6.
- The Claude API fallback requires either `ANTHROPIC_API_KEY` environment variable or `claude login` completed.
- The WOL feature requires `wakeonlan` to be installed on the Mac Mini (`brew install wakeonlan`).

---

### 1.8 Safety Hooks Implementation — 3h

**Depends on:** 1.2 (Python environment set up)
**Can parallel with:** 1.7, 1.10
**Machine:** Mac Mini

**Steps:**

1. **Create loop-detector.py**

   Create `~/Code-Brain/claude-code-superuser-pack/.claude/hooks/loop-detector.py`:

   ```python
   #!/usr/bin/env python3
   """
   loop-detector.py — PostToolUse hook

   Detects when an agent is stuck in a loop by hashing the last N tool calls.
   If hash(call[n]) == hash(call[n-2]), the agent is repeating the same
   sequence and should be killed to prevent budget waste.

   Hook Type: PostToolUse
   Trigger: After every tool call
   Action: Exits with code 2 (BLOCK) if loop detected
   """

   import hashlib
   import json
   import os
   import sys
   from pathlib import Path

   # Sliding window size: compare last 3 tool calls
   WINDOW_SIZE = 3
   # State file to persist across tool calls within the same run
   STATE_FILE = Path("/tmp/claude-loop-detector-state.json")


   def hash_tool_call(tool_name: str, tool_input: str) -> str:
       """Create a hash of a tool call for comparison."""
       content = f"{tool_name}:{tool_input}"
       return hashlib.sha256(content.encode()).hexdigest()[:16]


   def load_state() -> list[str]:
       """Load the sliding window of recent tool call hashes."""
       if STATE_FILE.exists():
           try:
               data = json.loads(STATE_FILE.read_text())
               # Check if state is from the current process (same agent run)
               if data.get("pid") == os.getppid():
                   return data.get("hashes", [])
           except (json.JSONDecodeError, KeyError):
               pass
       return []


   def save_state(hashes: list[str]):
       """Save the sliding window state."""
       STATE_FILE.write_text(json.dumps({
           "pid": os.getppid(),
           "hashes": hashes[-WINDOW_SIZE * 2:],  # Keep 2x window for comparison
       }))


   def check_for_loop(hashes: list[str]) -> bool:
       """
       Detect if the agent is in a loop.

       Returns True if the last WINDOW_SIZE hashes match the WINDOW_SIZE
       hashes before them (i.e., the agent is repeating a 3-step sequence).
       """
       if len(hashes) < WINDOW_SIZE * 2:
           return False

       recent = hashes[-WINDOW_SIZE:]
       previous = hashes[-WINDOW_SIZE * 2:-WINDOW_SIZE]

       return recent == previous


   def main():
       # Read hook input from stdin
       try:
           hook_input = json.loads(sys.stdin.read())
       except json.JSONDecodeError:
           # Can't parse input — allow the call to proceed
           sys.exit(0)

       tool_name = hook_input.get("tool_name", "unknown")
       tool_input = json.dumps(hook_input.get("tool_input", {}), sort_keys=True)

       # Hash this call
       call_hash = hash_tool_call(tool_name, tool_input)

       # Load and update state
       hashes = load_state()
       hashes.append(call_hash)

       # Check for loop
       if check_for_loop(hashes):
           print(
               json.dumps({
                   "decision": "block",
                   "reason": (
                       f"LOOP DETECTED: The last {WINDOW_SIZE} tool calls are identical "
                       f"to the {WINDOW_SIZE} before them. Agent appears stuck. "
                       f"Tool sequence hash: {call_hash}"
                   ),
               })
           )
           # Clean up state file
           STATE_FILE.unlink(missing_ok=True)
           sys.exit(2)

       # Save updated state and allow
       save_state(hashes)
       sys.exit(0)


   if __name__ == "__main__":
       main()
   ```

2. **Create cost-watchdog.py**

   Create `~/Code-Brain/claude-code-superuser-pack/.claude/hooks/cost-watchdog.py`:

   ```python
   #!/usr/bin/env python3
   """
   cost-watchdog.py — PreRun hook

   Reads agent-run-history.csv and blocks agent launch if daily fleet
   spend exceeds the configured limit (default: $2.00/day).

   This prevents runaway costs from misconfigured or looping agents.

   Hook Type: PreRun (before agent starts)
   Action: Exits with code 2 (BLOCK) if daily spend exceeds limit
   """

   import csv
   import json
   import sys
   from datetime import date
   from pathlib import Path

   # Configuration
   DAILY_SPEND_LIMIT = 2.00  # USD
   HISTORY_FILE = Path.home() / "Code-Brain" / "claude-code-superuser-pack" / \
       "vault" / "90_system" / "agent-logs" / "agent-run-history.csv"


   def get_today_spend() -> float:
       """Sum all costs from today's agent runs."""
       if not HISTORY_FILE.exists():
           return 0.0

       today_str = date.today().isoformat()
       total = 0.0

       with open(HISTORY_FILE, "r") as f:
           reader = csv.DictReader(f)
           for row in reader:
               if row.get("date", "") == today_str:
                   try:
                       cost = float(row.get("cost_usd", "0"))
                       total += cost
                   except ValueError:
                       pass

       return total


   def main():
       today_spend = get_today_spend()

       if today_spend >= DAILY_SPEND_LIMIT:
           print(
               json.dumps({
                   "decision": "block",
                   "reason": (
                       f"COST LIMIT REACHED: Today's fleet spend is ${today_spend:.2f}, "
                       f"which exceeds the daily limit of ${DAILY_SPEND_LIMIT:.2f}. "
                       f"No more agent runs allowed today. "
                       f"Review {HISTORY_FILE} and adjust limit if needed."
                   ),
               })
           )
           sys.exit(2)

       # Allow — log remaining budget
       remaining = DAILY_SPEND_LIMIT - today_spend
       # stdout is captured by the hook system; use stderr for info logging
       print(
           f"Cost watchdog: ${today_spend:.2f} spent today, "
           f"${remaining:.2f} remaining of ${DAILY_SPEND_LIMIT:.2f} limit",
           file=sys.stderr,
       )
       sys.exit(0)


   if __name__ == "__main__":
       main()
   ```

3. **Create vault-integrity.py**

   Create `~/Code-Brain/claude-code-superuser-pack/.claude/hooks/vault-integrity.py`:

   ```python
   #!/usr/bin/env python3
   """
   vault-integrity.py — PreToolUse hook

   Blocks vault_inject calls if the anchor string is empty.
   An empty anchor would cause the entire file to be overwritten
   instead of injecting content at a specific point.

   Also validates that the target file exists and contains the anchor.

   Hook Type: PreToolUse (before tool execution)
   Trigger: Only for vault_inject tool calls
   Action: Exits with code 2 (BLOCK) if anchor is empty or missing
   """

   import json
   import sys
   from pathlib import Path


   def main():
       try:
           hook_input = json.loads(sys.stdin.read())
       except json.JSONDecodeError:
           sys.exit(0)  # Can't parse — allow

       tool_name = hook_input.get("tool_name", "")

       # Only intercept vault_inject calls
       if "vault_inject" not in tool_name:
           sys.exit(0)

       tool_input = hook_input.get("tool_input", {})
       anchor = tool_input.get("anchor", "")
       file_path = tool_input.get("file_path", "")
       content = tool_input.get("content", "")

       # Block 1: Empty anchor
       if not anchor or not anchor.strip():
           print(
               json.dumps({
                   "decision": "block",
                   "reason": (
                       "VAULT INTEGRITY: vault_inject called with empty anchor string. "
                       "This would overwrite the entire file. "
                       "Provide a valid HTML comment anchor (e.g., '<!-- jira-log -->')."
                   ),
               })
           )
           sys.exit(2)

       # Block 2: Empty content (likely a bug)
       if not content or not content.strip():
           print(
               json.dumps({
                   "decision": "block",
                   "reason": (
                       "VAULT INTEGRITY: vault_inject called with empty content. "
                       "This is likely a bug — nothing to inject."
                   ),
               })
           )
           sys.exit(2)

       # Block 3: Target file doesn't exist
       if file_path:
           target = Path(file_path)
           if not target.exists():
               print(
                   json.dumps({
                       "decision": "block",
                       "reason": (
                           f"VAULT INTEGRITY: Target file does not exist: {file_path}. "
                           f"Create the file (from template) before injecting content."
                       ),
                   })
               )
               sys.exit(2)

           # Block 4: Anchor not found in file
           try:
               file_content = target.read_text()
               anchor_tag = f"<!-- {anchor} -->"
               if anchor_tag not in file_content and anchor not in file_content:
                   print(
                       json.dumps({
                           "decision": "block",
                           "reason": (
                               f"VAULT INTEGRITY: Anchor '{anchor}' not found in {file_path}. "
                               f"The file may be missing the anchor comment. "
                               f"Expected: {anchor_tag}"
                           ),
                       })
                   )
                   sys.exit(2)
           except (OSError, UnicodeDecodeError):
               pass  # Can't read file — allow and let vault_inject handle the error

       # All checks passed
       sys.exit(0)


   if __name__ == "__main__":
       main()
   ```

4. **Register hooks in .claude/settings.json**

   Update `~/Code-Brain/claude-code-superuser-pack/.claude/settings.json`:

   ```json
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "*",
           "command": "python3 .claude/hooks/loop-detector.py"
         }
       ],
       "PreRun": [
         {
           "matcher": "*",
           "command": "python3 .claude/hooks/cost-watchdog.py"
         }
       ],
       "PreToolUse": [
         {
           "matcher": "vault_inject",
           "command": "python3 .claude/hooks/vault-integrity.py"
         }
       ]
     }
   }
   ```

   **Why:** The hooks system reads from `.claude/settings.json` and executes the specified Python scripts at the appropriate lifecycle points. Autonomous agents inherit these hooks via `setting_sources=["project"]`.

5. **Make hooks executable**

   ```bash
   chmod +x .claude/hooks/loop-detector.py
   chmod +x .claude/hooks/cost-watchdog.py
   chmod +x .claude/hooks/vault-integrity.py
   ```

6. **Write tests for the hooks**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/tests/test_hooks.py`:

   ```python
   """Tests for safety hooks."""

   import json
   import subprocess
   import tempfile
   from pathlib import Path

   import pytest

   HOOKS_DIR = Path(__file__).parent.parent.parent / ".claude" / "hooks"


   class TestLoopDetector:
       def _run_hook(self, tool_name: str, tool_input: dict) -> tuple[int, str]:
           """Run loop-detector.py with given input, return (exit_code, stdout)."""
           input_data = json.dumps({
               "tool_name": tool_name,
               "tool_input": tool_input,
           })
           result = subprocess.run(
               ["python3", str(HOOKS_DIR / "loop-detector.py")],
               input=input_data,
               capture_output=True,
               text=True,
           )
           return result.returncode, result.stdout

       def test_no_loop_on_first_calls(self):
           # Clean state
           Path("/tmp/claude-loop-detector-state.json").unlink(missing_ok=True)

           code, _ = self._run_hook("Read", {"path": "/a"})
           assert code == 0
           code, _ = self._run_hook("Write", {"path": "/b"})
           assert code == 0
           code, _ = self._run_hook("Edit", {"path": "/c"})
           assert code == 0

       def test_detects_loop(self):
           # Clean state
           Path("/tmp/claude-loop-detector-state.json").unlink(missing_ok=True)

           # First sequence
           self._run_hook("Read", {"path": "/a"})
           self._run_hook("Write", {"path": "/b"})
           self._run_hook("Edit", {"path": "/c"})

           # Repeated sequence (should trigger loop detection)
           self._run_hook("Read", {"path": "/a"})
           self._run_hook("Write", {"path": "/b"})
           code, stdout = self._run_hook("Edit", {"path": "/c"})
           assert code == 2
           assert "LOOP DETECTED" in stdout


   class TestCostWatchdog:
       def test_allows_under_limit(self, tmp_path):
           # Create a history file with small costs
           csv_file = tmp_path / "agent-run-history.csv"
           from datetime import date
           today = date.today().isoformat()
           csv_file.write_text(
               "date,time,agent,mode,status,cost_usd,duration_ms,turns,notes\n"
               f"{today},08:00,daily_driver,morning,success,0.25,5000,10,\n"
               f"{today},17:00,daily_driver,evening,success,0.15,3000,8,\n"
           )

           # The hook reads from a hardcoded path, so this test
           # validates the logic but needs the actual file for integration testing
           # For a proper test, you'd mock HISTORY_FILE


   class TestVaultIntegrity:
       def _run_hook(self, tool_input: dict) -> tuple[int, str]:
           input_data = json.dumps({
               "tool_name": "mcp__vault-tools__vault_inject",
               "tool_input": tool_input,
           })
           result = subprocess.run(
               ["python3", str(HOOKS_DIR / "vault-integrity.py")],
               input=input_data,
               capture_output=True,
               text=True,
           )
           return result.returncode, result.stdout

       def test_blocks_empty_anchor(self):
           code, stdout = self._run_hook({
               "anchor": "",
               "file_path": "/tmp/test.md",
               "content": "some content",
           })
           assert code == 2
           assert "empty anchor" in stdout.lower()

       def test_blocks_empty_content(self):
           code, stdout = self._run_hook({
               "anchor": "jira-log",
               "file_path": "/tmp/test.md",
               "content": "",
           })
           assert code == 2
           assert "empty content" in stdout.lower()

       def test_allows_valid_inject(self, tmp_path):
           # Create a file with an anchor
           test_file = tmp_path / "daily.md"
           test_file.write_text("# Daily\n<!-- jira-log -->\n")

           code, _ = self._run_hook({
               "anchor": "jira-log",
               "file_path": str(test_file),
               "content": "- PROJ-123: did a thing",
           })
           assert code == 0
   ```

   Run the tests:
   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_hooks.py -v
   ```

   **Verify:** All tests pass.

**Gotchas:**
- The loop detector uses `/tmp/` for state, which is cleared on reboot. This is intentional — loop state should not persist across reboots.
- The cost watchdog reads from the hardcoded CSV path. If your vault path is different, update `HISTORY_FILE`.
- Hooks exit with code 0 (allow) or code 2 (block). Any other exit code is treated as allow.

---

### 1.9 macOS Keychain Credential Helper — 1h

**Depends on:** 1.2 (already implemented as part of 1.2 step 5)
**Can parallel with:** Everything
**Machine:** Mac Mini

This task was completed in Task 1.2, Step 5. The `lib/keychain.py` module is fully implemented with:
- `set_credential()` — stores secrets in macOS Keychain
- `get_credential()` — retrieves secrets at runtime
- `list_credentials()` — lists all agent credentials
- `delete_credential()` — removes a credential
- CLI interface for manual management

**Remaining setup steps:**

1. **Store all required credentials**

   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   source .venv/bin/activate

   # Store each credential
   python3 lib/keychain.py set jira-api-token "YOUR_JIRA_TOKEN"
   python3 lib/keychain.py set jira-email "sean.winslow28@gmail.com"
   python3 lib/keychain.py set github-pat "ghp_YOUR_GITHUB_PAT"
   python3 lib/keychain.py set fal-ai-key "YOUR_FAL_AI_KEY"
   python3 lib/keychain.py set google-genai-key "YOUR_GOOGLE_GENAI_KEY"
   python3 lib/keychain.py set replicate-api-token "YOUR_REPLICATE_TOKEN"
   ```

2. **Test credential retrieval in Python**

   ```python
   # Quick test
   from lib.keychain import get_credential
   token = get_credential("jira-api-token")
   assert token is not None, "Jira token not found in Keychain!"
   print(f"✓ Jira token retrieved ({len(token)} chars)")
   ```

---

### 1.10 Pixel Quantizer Prototype — 6h (can parallel with 1.1-1.9)

**Depends on:** None — can start immediately
**Can parallel with:** ALL Phase 1 tasks (completely independent)
**Machine:** MacBook Pro

This is the **gate check** for the entire hybrid pipeline. If the quantizer can't convert high-res video frames into clean pixel art, the hybrid approach is dead.

**Steps:**

1. **Set up the project on MacBook Pro**

   ```bash
   # Navigate to the sprite pipeline project
   cd ~/Code-Brain/16bitfit-battle-mode  # Adjust to your actual project path

   # Ensure Node.js 20+ is installed
   node --version
   # Expected: v24.x or v20.x+

   # Install additional dependencies needed for the quantizer
   npm install sharp yargs pino
   npm install -D @types/yargs
   ```

2. **Create the project structure**

   ```bash
   mkdir -p src/tools/quantizer/steps
   mkdir -p src/tools/quantizer/palettes
   mkdir -p test/tools/quantizer
   mkdir -p test-frames/input
   mkdir -p test-frames/output
   ```

3. **Create the types file**

   Create `src/tools/quantizer/types.ts`:

   ```typescript
   /**
    * Shared types for the Pixel Quantizer pipeline.
    */

   export interface QuantizerConfig {
     inputDir: string;
     outputDir: string;
     palette: PaletteEntry[];
     targetSize: number;
     backgroundMode: 'chroma' | 'auto';
     chromaColor: string;
     outlineWeight: number;
     outlineColor: string;
     staticThreshold: number;
     skipTemporal: boolean;
     skipOutline: boolean;
     verbose: boolean;
   }

   export interface PaletteEntry {
     hex: string;
     r: number;
     g: number;
     b: number;
     name?: string;
   }

   export interface FrameReport {
     filename: string;
     dimensions: { width: number; height: number };
     offPalettePixels: number;
     outlineCoverage: number;
     transparencyComplete: boolean;
     baselinePosition: number;
     processingTimeMs: number;
     passed: boolean;
   }

   export interface SequenceReport {
     totalFrames: number;
     passedFrames: number;
     failedFrames: number;
     frameReports: FrameReport[];
     temporalJitterScore: number;
     totalProcessingTimeMs: number;
   }

   export interface StepResult {
     buffer: Buffer;
     width: number;
     height: number;
     channels: number;
     metadata?: Record<string, unknown>;
   }
   ```

4. **Create the palette configuration**

   Create `src/tools/quantizer/palettes/sean.json`:

   ```json
   {
     "name": "Sean — Test Character",
     "description": "16-color palette for the SF2-style test character",
     "colors": [
       { "hex": "#F5D6C6", "name": "Skin — light peach" },
       { "hex": "#C2A769", "name": "Hair — dirty blonde" },
       { "hex": "#4682B4", "name": "Eyes — steel blue" },
       { "hex": "#F2F0EF", "name": "Tank top — off white" },
       { "hex": "#2323FF", "name": "Pants — neon blue" },
       { "hex": "#F5F5F5", "name": "Shoes — white" },
       { "hex": "#272929", "name": "Outlines — bold dark" },
       { "hex": "#000000", "name": "Pure black (shadows)" },
       { "hex": "#FFFFFF", "name": "Pure white (highlights)" },
       { "hex": "#D4B5A5", "name": "Skin shadow" },
       { "hex": "#B89A58", "name": "Hair shadow" },
       { "hex": "#3A6B94", "name": "Eyes shadow" },
       { "hex": "#D4D2D0", "name": "Tank top shadow" },
       { "hex": "#1A1ABF", "name": "Pants shadow" },
       { "hex": "#D4D4D4", "name": "Shoes shadow" },
       { "hex": "#00FF00", "name": "Chroma key green (background)" }
     ]
   }
   ```

5. **Create the palette loader**

   Create `src/tools/quantizer/palettes/index.ts`:

   ```typescript
   import { readFileSync } from 'fs';
   import { join } from 'path';
   import { PaletteEntry } from '../types';

   function hexToRgb(hex: string): { r: number; g: number; b: number } {
     const cleaned = hex.replace('#', '');
     return {
       r: parseInt(cleaned.substring(0, 2), 16),
       g: parseInt(cleaned.substring(2, 4), 16),
       b: parseInt(cleaned.substring(4, 6), 16),
     };
   }

   export function loadPalette(nameOrPath: string): PaletteEntry[] {
     let raw: { colors: { hex: string; name?: string }[] };

     // Check if it's a built-in palette name
     const builtInPath = join(__dirname, `${nameOrPath}.json`);
     try {
       raw = JSON.parse(readFileSync(builtInPath, 'utf-8'));
     } catch {
       // Try as a direct file path
       raw = JSON.parse(readFileSync(nameOrPath, 'utf-8'));
     }

     return raw.colors.map((c) => ({
       hex: c.hex,
       ...hexToRgb(c.hex),
       name: c.name,
     }));
   }

   export function findNearestColor(
     r: number, g: number, b: number,
     palette: PaletteEntry[]
   ): PaletteEntry {
     let minDist = Infinity;
     let nearest = palette[0];

     for (const entry of palette) {
       const dist = Math.sqrt(
         (r - entry.r) ** 2 +
         (g - entry.g) ** 2 +
         (b - entry.b) ** 2
       );
       if (dist < minDist) {
         minDist = dist;
         nearest = entry;
       }
     }

     return nearest;
   }
   ```

6. **Implement Step 1: Nearest-Neighbor Downscale**

   Create `src/tools/quantizer/steps/downscale.ts`:

   ```typescript
   import sharp from 'sharp';
   import { QuantizerConfig, StepResult } from '../types';

   /**
    * Step 1: Nearest-Neighbor Downscale
    *
    * Resizes input frame to target size using nearest-neighbor interpolation.
    * This preserves hard pixel edges instead of introducing anti-aliased colors
    * that don't exist in pixel art.
    */
   export async function downscale(
     inputBuffer: Buffer,
     config: QuantizerConfig
   ): Promise<StepResult> {
     const { targetSize } = config;

     const result = await sharp(inputBuffer)
       .resize(targetSize, targetSize, {
         kernel: sharp.kernel.nearest,
         fit: 'fill',
       })
       .raw()
       .toBuffer({ resolveWithObject: true });

     return {
       buffer: result.data,
       width: result.info.width,
       height: result.info.height,
       channels: result.info.channels,
       metadata: {
         originalSize: (await sharp(inputBuffer).metadata()).width,
         step: 'downscale',
       },
     };
   }
   ```

7. **Implement Step 2: Palette Quantization**

   Create `src/tools/quantizer/steps/palette-quantize.ts`:

   ```typescript
   import { QuantizerConfig, StepResult, PaletteEntry } from '../types';
   import { findNearestColor } from '../palettes';

   /**
    * Step 2: Palette Quantization
    *
    * Snaps every pixel to the nearest color in the predetermined palette
    * using Euclidean distance in RGB space. Does NOT use Sharp's built-in
    * palette option (which picks its own colors via median-cut).
    */
   export async function paletteQuantize(
     input: StepResult,
     config: QuantizerConfig
   ): Promise<StepResult> {
     const { buffer, width, height, channels } = input;
     const { palette } = config;
     const output = Buffer.alloc(buffer.length);

     let offPaletteCount = 0;

     for (let i = 0; i < buffer.length; i += channels) {
       const r = buffer[i];
       const g = buffer[i + 1];
       const b = buffer[i + 2];
       const a = channels === 4 ? buffer[i + 3] : 255;

       // Skip fully transparent pixels
       if (a === 0) {
         output[i] = 0;
         output[i + 1] = 0;
         output[i + 2] = 0;
         if (channels === 4) output[i + 3] = 0;
         continue;
       }

       const nearest = findNearestColor(r, g, b, palette);

       // Check if the pixel was already on-palette
       if (r !== nearest.r || g !== nearest.g || b !== nearest.b) {
         offPaletteCount++;
       }

       output[i] = nearest.r;
       output[i + 1] = nearest.g;
       output[i + 2] = nearest.b;
       if (channels === 4) output[i + 3] = a;
     }

     return {
       buffer: output,
       width,
       height,
       channels,
       metadata: {
         offPalettePixels: offPaletteCount,
         totalPixels: (width * height),
         step: 'palette-quantize',
       },
     };
   }
   ```

8. **Implement Step 3: Temporal Smoothing**

   Create `src/tools/quantizer/steps/temporal-smooth.ts`:

   ```typescript
   import { QuantizerConfig, StepResult } from '../types';

   /**
    * Step 3: Temporal Smoothing
    *
    * For each pixel position, looks across all frames in the sequence.
    * If a pixel barely changes (RGB distance < threshold), locks it to the
    * mode color (most common value) across all frames.
    *
    * This eliminates sub-pixel jitter in areas that should be static
    * (torso, head during walk cycle).
    */
   export function temporalSmooth(
     frames: StepResult[],
     config: QuantizerConfig
   ): StepResult[] {
     if (frames.length <= 1 || config.skipTemporal) {
       return frames;
     }

     const { staticThreshold } = config;
     const { width, height, channels } = frames[0];
     const pixelCount = width * height;
     const smoothedFrames: StepResult[] = frames.map((f) => ({
       ...f,
       buffer: Buffer.from(f.buffer), // Clone buffers
     }));

     for (let px = 0; px < pixelCount; px++) {
       const offset = px * channels;

       // Collect colors at this pixel across all frames
       const colors: { r: number; g: number; b: number; a: number }[] = [];
       for (const frame of frames) {
         colors.push({
           r: frame.buffer[offset],
           g: frame.buffer[offset + 1],
           b: frame.buffer[offset + 2],
           a: channels === 4 ? frame.buffer[offset + 3] : 255,
         });
       }

       // Skip if any frame has this pixel transparent
       if (colors.some((c) => c.a === 0)) continue;

       // Check if this pixel is "static" — small variance across frames
       const maxDist = getMaxDistance(colors);
       if (maxDist < staticThreshold) {
         // Lock to mode color (most common)
         const modeColor = getModeColor(colors);
         for (const frame of smoothedFrames) {
           frame.buffer[offset] = modeColor.r;
           frame.buffer[offset + 1] = modeColor.g;
           frame.buffer[offset + 2] = modeColor.b;
         }
       }
     }

     return smoothedFrames;
   }

   function getMaxDistance(
     colors: { r: number; g: number; b: number }[]
   ): number {
     let maxDist = 0;
     for (let i = 0; i < colors.length; i++) {
       for (let j = i + 1; j < colors.length; j++) {
         const dist = Math.sqrt(
           (colors[i].r - colors[j].r) ** 2 +
           (colors[i].g - colors[j].g) ** 2 +
           (colors[i].b - colors[j].b) ** 2
         );
         if (dist > maxDist) maxDist = dist;
       }
     }
     return maxDist;
   }

   function getModeColor(
     colors: { r: number; g: number; b: number }[]
   ): { r: number; g: number; b: number } {
     // Find the most common RGB value
     const counts = new Map<string, { count: number; r: number; g: number; b: number }>();
     for (const c of colors) {
       const key = `${c.r},${c.g},${c.b}`;
       const existing = counts.get(key);
       if (existing) {
         existing.count++;
       } else {
         counts.set(key, { count: 1, r: c.r, g: c.g, b: c.b });
       }
     }

     let mode = colors[0];
     let maxCount = 0;
     for (const entry of counts.values()) {
       if (entry.count > maxCount) {
         maxCount = entry.count;
         mode = { r: entry.r, g: entry.g, b: entry.b };
       }
     }
     return mode;
   }
   ```

9. **Implement Step 4: Outline Enforcement**

   Create `src/tools/quantizer/steps/outline-enforce.ts`:

   ```typescript
   import { QuantizerConfig, StepResult, PaletteEntry } from '../types';

   /**
    * Step 4: Outline Enforcement
    *
    * Detects sprite edges (adjacent to transparent) and internal color
    * boundaries, then applies bold outline color at those edges.
    * This re-applies the bold outlines that video models soften
    * during interpolation.
    */
   export function outlineEnforce(
     input: StepResult,
     config: QuantizerConfig
   ): StepResult {
     if (config.skipOutline) return input;

     const { buffer, width, height, channels } = input;
     const { outlineWeight, outlineColor } = config;
     const output = Buffer.from(buffer); // Clone

     const outlineRgb = hexToRgb(outlineColor);

     // Color distance threshold for detecting internal boundaries
     const BOUNDARY_THRESHOLD = 80;

     for (let y = 0; y < height; y++) {
       for (let x = 0; x < width; x++) {
         const idx = (y * width + x) * channels;
         const a = channels === 4 ? buffer[idx + 3] : 255;

         // Skip transparent pixels
         if (a === 0) continue;

         // Skip if this pixel is already the outline color
         if (
           buffer[idx] === outlineRgb.r &&
           buffer[idx + 1] === outlineRgb.g &&
           buffer[idx + 2] === outlineRgb.b
         ) continue;

         // Check if this pixel is at a sprite edge (adjacent to transparent)
         const isEdge = isAdjacentToTransparent(buffer, x, y, width, height, channels, outlineWeight);

         // Check if this pixel is at an internal color boundary
         const isBoundary = isAtColorBoundary(
           buffer, x, y, width, height, channels, BOUNDARY_THRESHOLD
         );

         if (isEdge || isBoundary) {
           output[idx] = outlineRgb.r;
           output[idx + 1] = outlineRgb.g;
           output[idx + 2] = outlineRgb.b;
         }
       }
     }

     return {
       buffer: output,
       width,
       height,
       channels,
       metadata: { step: 'outline-enforce' },
     };
   }

   function isAdjacentToTransparent(
     buffer: Buffer, x: number, y: number,
     width: number, height: number, channels: number,
     weight: number
   ): boolean {
     for (let dy = -weight; dy <= weight; dy++) {
       for (let dx = -weight; dx <= weight; dx++) {
         if (dx === 0 && dy === 0) continue;
         const nx = x + dx;
         const ny = y + dy;
         if (nx < 0 || nx >= width || ny < 0 || ny >= height) {
           return true; // Edge of canvas = treat as transparent
         }
         const nIdx = (ny * width + nx) * channels;
         if (channels === 4 && buffer[nIdx + 3] === 0) {
           return true;
         }
       }
     }
     return false;
   }

   function isAtColorBoundary(
     buffer: Buffer, x: number, y: number,
     width: number, height: number, channels: number,
     threshold: number
   ): boolean {
     const idx = (y * width + x) * channels;
     const r = buffer[idx], g = buffer[idx + 1], b = buffer[idx + 2];

     // Check 4-connected neighbors
     const neighbors = [
       [x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1],
     ];

     for (const [nx, ny] of neighbors) {
       if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
       const nIdx = (ny * width + nx) * channels;
       if (channels === 4 && buffer[nIdx + 3] === 0) continue; // Skip transparent

       const dist = Math.sqrt(
         (r - buffer[nIdx]) ** 2 +
         (g - buffer[nIdx + 1]) ** 2 +
         (b - buffer[nIdx + 2]) ** 2
       );
       if (dist > threshold) return true;
     }
     return false;
   }

   function hexToRgb(hex: string): { r: number; g: number; b: number } {
     const cleaned = hex.replace('#', '');
     return {
       r: parseInt(cleaned.substring(0, 2), 16),
       g: parseInt(cleaned.substring(2, 4), 16),
       b: parseInt(cleaned.substring(4, 6), 16),
     };
   }
   ```

10. **Implement Step 5: Alpha Recovery**

    Create `src/tools/quantizer/steps/alpha-recover.ts`:

    ```typescript
    import { QuantizerConfig, StepResult } from '../types';

    /**
     * Step 5: Alpha Recovery
     *
     * Removes background color and enforces binary alpha:
     * - Chroma key mode: removes a specific color (default: #00FF00)
     * - Auto-detect mode: finds and removes the dominant background color
     * - All alpha values are forced to 0 or 255 (no semi-transparency)
     */
    export function alphaRecover(
      input: StepResult,
      config: QuantizerConfig
    ): StepResult {
      const { buffer, width, height, channels } = input;

      // Ensure we're working with RGBA
      let rgba: Buffer;
      if (channels === 3) {
        rgba = Buffer.alloc(width * height * 4);
        for (let i = 0; i < width * height; i++) {
          rgba[i * 4] = buffer[i * 3];
          rgba[i * 4 + 1] = buffer[i * 3 + 1];
          rgba[i * 4 + 2] = buffer[i * 3 + 2];
          rgba[i * 4 + 3] = 255;
        }
      } else {
        rgba = Buffer.from(buffer);
      }

      const bgColor = config.backgroundMode === 'chroma'
        ? hexToRgb(config.chromaColor)
        : detectDominantBackground(rgba, width, height);

      // Color distance threshold for background removal
      const BG_THRESHOLD = 50;

      for (let i = 0; i < width * height; i++) {
        const offset = i * 4;
        const r = rgba[offset];
        const g = rgba[offset + 1];
        const b = rgba[offset + 2];

        const dist = Math.sqrt(
          (r - bgColor.r) ** 2 +
          (g - bgColor.g) ** 2 +
          (b - bgColor.b) ** 2
        );

        if (dist < BG_THRESHOLD) {
          // This pixel is background — make transparent
          rgba[offset] = 0;
          rgba[offset + 1] = 0;
          rgba[offset + 2] = 0;
          rgba[offset + 3] = 0;
        } else {
          // Force binary alpha: >= 128 → 255, < 128 → 0
          rgba[offset + 3] = rgba[offset + 3] >= 128 ? 255 : 0;
        }
      }

      return {
        buffer: rgba,
        width,
        height,
        channels: 4,
        metadata: {
          backgroundColorRemoved: `rgb(${bgColor.r},${bgColor.g},${bgColor.b})`,
          step: 'alpha-recover',
        },
      };
    }

    function detectDominantBackground(
      buffer: Buffer, width: number, height: number
    ): { r: number; g: number; b: number } {
      // Sample the border pixels to find the most common color
      const counts = new Map<string, { count: number; r: number; g: number; b: number }>();

      const sampleBorder = (x: number, y: number) => {
        const offset = (y * width + x) * 4;
        const key = `${buffer[offset]},${buffer[offset + 1]},${buffer[offset + 2]}`;
        const existing = counts.get(key);
        if (existing) {
          existing.count++;
        } else {
          counts.set(key, {
            count: 1,
            r: buffer[offset],
            g: buffer[offset + 1],
            b: buffer[offset + 2],
          });
        }
      };

      // Sample all border pixels
      for (let x = 0; x < width; x++) {
        sampleBorder(x, 0);            // Top row
        sampleBorder(x, height - 1);    // Bottom row
      }
      for (let y = 1; y < height - 1; y++) {
        sampleBorder(0, y);             // Left column
        sampleBorder(width - 1, y);     // Right column
      }

      // Find most common border color
      let maxCount = 0;
      let dominant = { r: 0, g: 0, b: 0 };
      for (const entry of counts.values()) {
        if (entry.count > maxCount) {
          maxCount = entry.count;
          dominant = { r: entry.r, g: entry.g, b: entry.b };
        }
      }

      return dominant;
    }

    function hexToRgb(hex: string): { r: number; g: number; b: number } {
      const cleaned = hex.replace('#', '');
      return {
        r: parseInt(cleaned.substring(0, 2), 16),
        g: parseInt(cleaned.substring(2, 4), 16),
        b: parseInt(cleaned.substring(4, 6), 16),
      };
    }
    ```

11. **Implement Step 6: Baseline Registration**

    Create `src/tools/quantizer/steps/baseline-register.ts`:

    ```typescript
    import { QuantizerConfig, StepResult } from '../types';

    /**
     * Step 6: Baseline Registration
     *
     * Aligns all sprites in the sequence so their feet land on a consistent
     * baseline. This prevents the "floating" or "bouncing" effect where
     * characters drift vertically between frames.
     */
    export function baselineRegister(
      frames: StepResult[],
      config: QuantizerConfig
    ): StepResult[] {
      if (frames.length === 0) return frames;

      const { targetSize } = config;

      // Detect bottom edge (lowest non-transparent row) for each frame
      const bottomEdges: number[] = frames.map((frame) =>
        findBottomEdge(frame.buffer, frame.width, frame.height, frame.channels)
      );

      // Target baseline: mode of all bottom edges
      const targetBaseline = getMode(bottomEdges);

      return frames.map((frame, i) => {
        const drift = targetBaseline - bottomEdges[i];

        if (drift === 0) return frame;

        // Clamp shift to ±32px safety valve
        const clampedDrift = Math.max(-32, Math.min(32, drift));

        const shifted = shiftVertical(
          frame.buffer, frame.width, frame.height, frame.channels, clampedDrift
        );

        return {
          ...frame,
          buffer: shifted,
          metadata: {
            ...frame.metadata,
            baselineDrift: drift,
            clampedDrift,
            targetBaseline,
            originalBottom: bottomEdges[i],
            step: 'baseline-register',
          },
        };
      });
    }

    function findBottomEdge(
      buffer: Buffer, width: number, height: number, channels: number
    ): number {
      for (let y = height - 1; y >= 0; y--) {
        for (let x = 0; x < width; x++) {
          const offset = (y * width + x) * channels;
          const a = channels === 4 ? buffer[offset + 3] : 255;
          if (a > 0) return y;
        }
      }
      return height - 1; // Fallback
    }

    function getMode(values: number[]): number {
      const counts = new Map<number, number>();
      for (const v of values) {
        counts.set(v, (counts.get(v) || 0) + 1);
      }
      let maxCount = 0;
      let mode = values[0];
      for (const [value, count] of counts) {
        if (count > maxCount) {
          maxCount = count;
          mode = value;
        }
      }
      return mode;
    }

    function shiftVertical(
      buffer: Buffer, width: number, height: number,
      channels: number, dy: number
    ): Buffer {
      const output = Buffer.alloc(buffer.length);

      for (let y = 0; y < height; y++) {
        const srcY = y - dy;
        if (srcY < 0 || srcY >= height) {
          // Fill with transparent
          for (let x = 0; x < width; x++) {
            const dstOffset = (y * width + x) * channels;
            for (let c = 0; c < channels; c++) {
              output[dstOffset + c] = 0;
            }
          }
        } else {
          const srcOffset = srcY * width * channels;
          const dstOffset = y * width * channels;
          buffer.copy(output, dstOffset, srcOffset, srcOffset + width * channels);
        }
      }

      return output;
    }
    ```

12. **Implement Step 7: Validation Report**

    Create `src/tools/quantizer/steps/validate.ts`:

    ```typescript
    import { QuantizerConfig, StepResult, FrameReport, SequenceReport, PaletteEntry } from '../types';

    /**
     * Step 7: Validation Report
     *
     * Generates per-frame and sequence-level reports to verify
     * the quantizer output meets pixel art spec.
     */
    export function validateFrame(
      frame: StepResult,
      filename: string,
      config: QuantizerConfig,
      processingTimeMs: number
    ): FrameReport {
      const { buffer, width, height, channels } = frame;
      const { palette, targetSize } = config;

      let offPalettePixels = 0;
      let outlinePixels = 0;
      let transparentPixels = 0;
      let opaquePixels = 0;
      let edgePixels = 0;
      let bottomRow = 0;

      const outlineRgb = hexToRgb(config.outlineColor);

      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const offset = (y * width + x) * channels;
          const a = channels === 4 ? buffer[offset + 3] : 255;

          if (a === 0) {
            transparentPixels++;
            continue;
          }

          opaquePixels++;

          const r = buffer[offset];
          const g = buffer[offset + 1];
          const b = buffer[offset + 2];

          // Check if on-palette
          if (!isOnPalette(r, g, b, palette)) {
            offPalettePixels++;
          }

          // Check if outline pixel
          if (r === outlineRgb.r && g === outlineRgb.g && b === outlineRgb.b) {
            outlinePixels++;
          }

          // Track bottom edge for baseline
          if (a > 0) bottomRow = Math.max(bottomRow, y);
        }
      }

      // Edge pixels (adjacent to transparent)
      for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
          const offset = (y * width + x) * channels;
          if (channels === 4 && buffer[offset + 3] === 0) continue;
          if (isAdjacentToTransparent(buffer, x, y, width, height, channels)) {
            edgePixels++;
          }
        }
      }

      const outlineCoverage = edgePixels > 0 ? outlinePixels / edgePixels : 0;

      return {
        filename,
        dimensions: { width, height },
        offPalettePixels,
        outlineCoverage: Math.round(outlineCoverage * 100) / 100,
        transparencyComplete: opaquePixels > 0 && transparentPixels > 0,
        baselinePosition: bottomRow,
        processingTimeMs: Math.round(processingTimeMs),
        passed: (
          width === targetSize &&
          height === targetSize &&
          offPalettePixels === 0 &&
          outlineCoverage > 0.3 &&
          processingTimeMs < 2000
        ),
      };
    }

    export function validateSequence(
      frameReports: FrameReport[]
    ): SequenceReport {
      const baselines = frameReports.map((r) => r.baselinePosition);
      const baselineVariance = baselines.length > 1
        ? Math.max(...baselines) - Math.min(...baselines)
        : 0;

      return {
        totalFrames: frameReports.length,
        passedFrames: frameReports.filter((r) => r.passed).length,
        failedFrames: frameReports.filter((r) => !r.passed).length,
        frameReports,
        temporalJitterScore: baselineVariance,
        totalProcessingTimeMs: frameReports.reduce((sum, r) => sum + r.processingTimeMs, 0),
      };
    }

    function isOnPalette(r: number, g: number, b: number, palette: PaletteEntry[]): boolean {
      return palette.some((p) => p.r === r && p.g === g && p.b === b);
    }

    function isAdjacentToTransparent(
      buffer: Buffer, x: number, y: number,
      width: number, height: number, channels: number
    ): boolean {
      const neighbors = [[x-1,y],[x+1,y],[x,y-1],[x,y+1]];
      for (const [nx, ny] of neighbors) {
        if (nx < 0 || nx >= width || ny < 0 || ny >= height) return true;
        const nOffset = (ny * width + nx) * channels;
        if (channels === 4 && buffer[nOffset + 3] === 0) return true;
      }
      return false;
    }

    function hexToRgb(hex: string): { r: number; g: number; b: number } {
      const cleaned = hex.replace('#', '');
      return {
        r: parseInt(cleaned.substring(0, 2), 16),
        g: parseInt(cleaned.substring(2, 4), 16),
        b: parseInt(cleaned.substring(4, 6), 16),
      };
    }
    ```

13. **Implement the main pipeline orchestrator**

    Create `src/tools/quantizer/index.ts`:

    ```typescript
    import sharp from 'sharp';
    import { readdirSync, mkdirSync, writeFileSync } from 'fs';
    import { join, basename } from 'path';
    import pino from 'pino';
    import { QuantizerConfig, StepResult, SequenceReport } from './types';
    import { downscale } from './steps/downscale';
    import { paletteQuantize } from './steps/palette-quantize';
    import { temporalSmooth } from './steps/temporal-smooth';
    import { outlineEnforce } from './steps/outline-enforce';
    import { alphaRecover } from './steps/alpha-recover';
    import { baselineRegister } from './steps/baseline-register';
    import { validateFrame, validateSequence } from './steps/validate';

    const logger = pino({ level: 'info' });

    /**
     * Run the full 7-step pixel quantizer pipeline on a directory of frames.
     */
    export async function runPipeline(config: QuantizerConfig): Promise<SequenceReport> {
      const log = config.verbose ? logger : pino({ level: 'silent' });

      // Ensure output directory exists
      mkdirSync(config.outputDir, { recursive: true });

      // Read input frames (sorted for determinism)
      const inputFiles = readdirSync(config.inputDir)
        .filter((f) => f.endsWith('.png'))
        .sort();

      if (inputFiles.length === 0) {
        throw new Error(`No PNG files found in ${config.inputDir}`);
      }

      log.info(`Processing ${inputFiles.length} frames from ${config.inputDir}`);

      // === Steps 1-2: Process each frame individually ===
      const processedFrames: StepResult[] = [];

      for (const file of inputFiles) {
        const inputPath = join(config.inputDir, file);
        const inputBuffer = await sharp(inputPath).toBuffer();

        log.info(`Step 1: Downscaling ${file}`);
        const downscaled = await downscale(inputBuffer, config);

        log.info(`Step 2: Palette quantizing ${file}`);
        const quantized = await paletteQuantize(downscaled, config);

        processedFrames.push(quantized);
      }

      // === Step 3: Temporal smoothing (across all frames) ===
      log.info('Step 3: Temporal smoothing');
      const smoothed = temporalSmooth(processedFrames, config);

      // === Step 4: Outline enforcement ===
      log.info('Step 4: Outline enforcement');
      const outlined = smoothed.map((frame) => outlineEnforce(frame, config));

      // === Step 5: Alpha recovery ===
      log.info('Step 5: Alpha recovery');
      const alphaRecovered = outlined.map((frame) => alphaRecover(frame, config));

      // === Step 6: Baseline registration ===
      log.info('Step 6: Baseline registration');
      const registered = baselineRegister(alphaRecovered, config);

      // === Step 7: Validate and save ===
      log.info('Step 7: Validation and export');
      const frameReports = [];

      for (let i = 0; i < registered.length; i++) {
        const frame = registered[i];
        const filename = inputFiles[i];
        const startTime = performance.now();

        // Save output PNG
        const outputPath = join(config.outputDir, filename);
        await sharp(frame.buffer, {
          raw: { width: frame.width, height: frame.height, channels: frame.channels as 3 | 4 },
        })
          .png()
          .toFile(outputPath);

        const processingTime = performance.now() - startTime;
        const report = validateFrame(frame, filename, config, processingTime);
        frameReports.push(report);

        log.info({
          file: filename,
          passed: report.passed,
          offPalette: report.offPalettePixels,
          outlineCoverage: report.outlineCoverage,
        });
      }

      const sequenceReport = validateSequence(frameReports);

      // Save report
      const reportPath = join(config.outputDir, 'validation-report.json');
      writeFileSync(reportPath, JSON.stringify(sequenceReport, null, 2));
      log.info(`Validation report saved to ${reportPath}`);

      return sequenceReport;
    }
    ```

14. **Create the CLI entry point**

    Create `src/tools/pixel-quantizer.ts`:

    ```typescript
    #!/usr/bin/env npx ts-node
    /**
     * Pixel Quantizer CLI — Standalone tool for converting high-resolution
     * frames into palette-locked pixel art.
     *
     * Usage:
     *   npx ts-node src/tools/pixel-quantizer.ts \
     *     --input ./test-frames/input/ \
     *     --output ./test-frames/output/ \
     *     --palette sean \
     *     --target-size 128
     */

    import yargs from 'yargs';
    import { hideBin } from 'yargs/helpers';
    import { runPipeline } from './quantizer';
    import { loadPalette } from './quantizer/palettes';
    import { QuantizerConfig } from './quantizer/types';

    async function main() {
      const argv = await yargs(hideBin(process.argv))
        .option('input', {
          alias: 'i',
          type: 'string',
          demandOption: true,
          describe: 'Directory of input PNG frames',
        })
        .option('output', {
          alias: 'o',
          type: 'string',
          demandOption: true,
          describe: 'Directory for processed output',
        })
        .option('palette', {
          alias: 'p',
          type: 'string',
          demandOption: true,
          describe: 'Palette name (built-in) or path to JSON palette file',
        })
        .option('target-size', {
          type: 'number',
          default: 128,
          describe: 'Output frame dimensions (square)',
        })
        .option('background-mode', {
          type: 'string',
          default: 'chroma',
          choices: ['chroma', 'auto'] as const,
          describe: 'Background removal mode',
        })
        .option('chroma-color', {
          type: 'string',
          default: '#00FF00',
          describe: 'Chroma key color (hex)',
        })
        .option('outline-weight', {
          type: 'number',
          default: 2,
          describe: 'Outline thickness in pixels',
        })
        .option('outline-color', {
          type: 'string',
          default: '#272929',
          describe: 'Outline color (hex)',
        })
        .option('static-threshold', {
          type: 'number',
          default: 15,
          describe: 'RGB distance threshold for temporal smoothing',
        })
        .option('skip-temporal', {
          type: 'boolean',
          default: false,
          describe: 'Skip temporal smoothing step',
        })
        .option('skip-outline', {
          type: 'boolean',
          default: false,
          describe: 'Skip outline enforcement step',
        })
        .option('verbose', {
          alias: 'v',
          type: 'boolean',
          default: false,
          describe: 'Detailed per-step logging',
        })
        .help()
        .argv;

      const palette = loadPalette(argv.palette);

      const config: QuantizerConfig = {
        inputDir: argv.input,
        outputDir: argv.output,
        palette,
        targetSize: argv['target-size'],
        backgroundMode: argv['background-mode'] as 'chroma' | 'auto',
        chromaColor: argv['chroma-color'],
        outlineWeight: argv['outline-weight'],
        outlineColor: argv['outline-color'],
        staticThreshold: argv['static-threshold'],
        skipTemporal: argv['skip-temporal'],
        skipOutline: argv['skip-outline'],
        verbose: argv.verbose,
      };

      console.log('=== Pixel Quantizer ===');
      console.log(`Input:  ${config.inputDir}`);
      console.log(`Output: ${config.outputDir}`);
      console.log(`Palette: ${argv.palette} (${palette.length} colors)`);
      console.log(`Target: ${config.targetSize}×${config.targetSize}`);
      console.log('');

      const report = await runPipeline(config);

      console.log('\n=== Results ===');
      console.log(`Frames: ${report.totalFrames} total, ${report.passedFrames} passed, ${report.failedFrames} failed`);
      console.log(`Temporal jitter: ${report.temporalJitterScore}px`);
      console.log(`Total time: ${Math.round(report.totalProcessingTimeMs)}ms`);

      if (report.failedFrames > 0) {
        console.log('\nFailed frames:');
        for (const fr of report.frameReports.filter((r) => !r.passed)) {
          console.log(`  ${fr.filename}: off-palette=${fr.offPalettePixels}, outline=${fr.outlineCoverage}`);
        }
        process.exit(1);
      }

      console.log('\n✓ All frames passed validation');
    }

    main().catch((err) => {
      console.error('FATAL:', err.message);
      process.exit(1);
    });
    ```

15. **Create the test data generator**

    Create `src/tools/generate-test-data.ts`:

    ```typescript
    #!/usr/bin/env npx ts-node
    /**
     * Generate synthetic test input for the Pixel Quantizer.
     *
     * Creates Q-01 through Q-04 experiment directories from a source sprite.
     * If no source sprite exists, generates a simple one programmatically.
     *
     * Usage:
     *   npx ts-node src/tools/generate-test-data.ts
     */

    import sharp from 'sharp';
    import { mkdirSync, existsSync } from 'fs';
    import { join } from 'path';

    const TEST_DIR = './test-frames';
    const SIZE = 128;
    const UPSCALE = 512;

    /**
     * Create a simple pixel art sprite programmatically.
     * A rough humanoid figure using the Sean palette.
     */
    async function createSourceSprite(): Promise<Buffer> {
      const channels = 4;
      const data = Buffer.alloc(SIZE * SIZE * channels); // RGBA, starts as transparent

      const setPixel = (x: number, y: number, r: number, g: number, b: number) => {
        if (x < 0 || x >= SIZE || y < 0 || y >= SIZE) return;
        const offset = (y * SIZE + x) * channels;
        data[offset] = r;
        data[offset + 1] = g;
        data[offset + 2] = b;
        data[offset + 3] = 255;
      };

      const fillRect = (x: number, y: number, w: number, h: number, r: number, g: number, b: number) => {
        for (let dy = 0; dy < h; dy++) {
          for (let dx = 0; dx < w; dx++) {
            setPixel(x + dx, y + dy, r, g, b);
          }
        }
      };

      // Simple fighter character (centered, facing right)
      const cx = 64; // center x

      // Head (skin)
      fillRect(cx - 8, 20, 16, 16, 0xF5, 0xD6, 0xC6);
      // Hair (dirty blonde)
      fillRect(cx - 8, 16, 16, 6, 0xC2, 0xA7, 0x69);
      // Eyes (steel blue)
      fillRect(cx + 2, 26, 3, 3, 0x46, 0x82, 0xB4);
      // Tank top (off white)
      fillRect(cx - 10, 36, 20, 20, 0xF2, 0xF0, 0xEF);
      // Arms (skin)
      fillRect(cx - 14, 38, 4, 16, 0xF5, 0xD6, 0xC6);
      fillRect(cx + 10, 38, 4, 16, 0xF5, 0xD6, 0xC6);
      // Pants (neon blue)
      fillRect(cx - 8, 56, 16, 20, 0x23, 0x23, 0xFF);
      // Legs gap
      fillRect(cx - 1, 66, 2, 10, 0, 0, 0); // gap between legs (transparent later)
      // Shoes (white)
      fillRect(cx - 10, 76, 8, 6, 0xF5, 0xF5, 0xF5);
      fillRect(cx + 2, 76, 8, 6, 0xF5, 0xF5, 0xF5);

      // Outline everything (simplified: just draw border around non-transparent pixels)
      // For testing, we'll add outlines programmatically in a second pass
      const withOutline = Buffer.from(data);
      for (let y = 0; y < SIZE; y++) {
        for (let x = 0; x < SIZE; x++) {
          const offset = (y * SIZE + x) * channels;
          if (data[offset + 3] === 0) continue; // Skip transparent

          // Check if adjacent to transparent
          const neighbors = [[x-1,y],[x+1,y],[x,y-1],[x,y+1]];
          for (const [nx, ny] of neighbors) {
            if (nx < 0 || nx >= SIZE || ny < 0 || ny >= SIZE) {
              withOutline[offset] = 0x27;
              withOutline[offset + 1] = 0x29;
              withOutline[offset + 2] = 0x29;
              break;
            }
            const nOffset = (ny * SIZE + nx) * channels;
            if (data[nOffset + 3] === 0) {
              withOutline[offset] = 0x27;
              withOutline[offset + 1] = 0x29;
              withOutline[offset + 2] = 0x29;
              break;
            }
          }
        }
      }

      return sharp(withOutline, { raw: { width: SIZE, height: SIZE, channels: 4 } })
        .png()
        .toBuffer();
    }

    async function main() {
      console.log('=== Test Data Generator ===\n');

      // Create source sprite
      const sourceSprite = await createSourceSprite();
      mkdirSync(join(TEST_DIR, 'source'), { recursive: true });
      await sharp(sourceSprite).toFile(join(TEST_DIR, 'source', 'sprite-128.png'));
      console.log('✓ Created source sprite (128×128)');

      // Q-01: Control test — upscaled pixel art (nearest-neighbor)
      const q01Dir = join(TEST_DIR, 'Q-01-control');
      mkdirSync(q01Dir, { recursive: true });
      await sharp(sourceSprite)
        .resize(UPSCALE, UPSCALE, { kernel: sharp.kernel.nearest })
        .toFile(join(q01Dir, 'frame-001.png'));
      console.log('✓ Q-01: Control test (nearest-neighbor upscale to 512×512)');

      // Q-02: Anti-aliased input (bilinear upscale)
      const q02Dir = join(TEST_DIR, 'Q-02-antialiased');
      mkdirSync(q02Dir, { recursive: true });
      await sharp(sourceSprite)
        .resize(UPSCALE, UPSCALE, { kernel: sharp.kernel.cubic })
        .toFile(join(q02Dir, 'frame-001.png'));
      console.log('✓ Q-02: Anti-aliased input (cubic upscale to 512×512)');

      // Q-03: Color-drifted input
      const q03Dir = join(TEST_DIR, 'Q-03-color-drift');
      mkdirSync(q03Dir, { recursive: true });
      const upscaled = await sharp(sourceSprite)
        .resize(UPSCALE, UPSCALE, { kernel: sharp.kernel.cubic })
        .raw()
        .toBuffer({ resolveWithObject: true });

      const drifted = Buffer.from(upscaled.data);
      for (let i = 0; i < drifted.length; i += upscaled.info.channels) {
        if (upscaled.info.channels === 4 && drifted[i + 3] === 0) continue;
        // Random drift ±15 per channel
        drifted[i] = Math.max(0, Math.min(255, drifted[i] + (Math.random() * 30 - 15)));
        drifted[i + 1] = Math.max(0, Math.min(255, drifted[i + 1] + (Math.random() * 30 - 15)));
        drifted[i + 2] = Math.max(0, Math.min(255, drifted[i + 2] + (Math.random() * 30 - 15)));
      }
      await sharp(drifted, {
        raw: { width: upscaled.info.width, height: upscaled.info.height, channels: upscaled.info.channels as 3 | 4 },
      })
        .png()
        .toFile(join(q03Dir, 'frame-001.png'));
      console.log('✓ Q-03: Color-drifted input (±15 RGB drift)');

      // Q-04: Simulated video sequence (4 frames with wobble)
      const q04Dir = join(TEST_DIR, 'Q-04-sequence');
      mkdirSync(q04Dir, { recursive: true });
      for (let f = 0; f < 4; f++) {
        const shiftX = Math.round(Math.sin(f * Math.PI / 2) * 2);
        const shiftY = Math.round(Math.cos(f * Math.PI / 2) * 1);

        const shifted = await sharp(sourceSprite)
          .extend({
            top: Math.max(0, -shiftY),
            bottom: Math.max(0, shiftY),
            left: Math.max(0, -shiftX),
            right: Math.max(0, shiftX),
            background: { r: 0, g: 0, b: 0, alpha: 0 },
          })
          .extract({
            left: Math.max(0, shiftX),
            top: Math.max(0, shiftY),
            width: SIZE,
            height: SIZE,
          })
          .resize(UPSCALE, UPSCALE, { kernel: sharp.kernel.cubic })
          .toBuffer();

        // Add color drift
        const rawShifted = await sharp(shifted).raw().toBuffer({ resolveWithObject: true });
        const driftedSeq = Buffer.from(rawShifted.data);
        for (let i = 0; i < driftedSeq.length; i += rawShifted.info.channels) {
          if (rawShifted.info.channels === 4 && driftedSeq[i + 3] === 0) continue;
          driftedSeq[i] = Math.max(0, Math.min(255, driftedSeq[i] + (Math.random() * 20 - 10)));
          driftedSeq[i + 1] = Math.max(0, Math.min(255, driftedSeq[i + 1] + (Math.random() * 20 - 10)));
          driftedSeq[i + 2] = Math.max(0, Math.min(255, driftedSeq[i + 2] + (Math.random() * 20 - 10)));
        }

        await sharp(driftedSeq, {
          raw: {
            width: rawShifted.info.width,
            height: rawShifted.info.height,
            channels: rawShifted.info.channels as 3 | 4,
          },
        })
          .png()
          .toFile(join(q04Dir, `frame-${String(f + 1).padStart(3, '0')}.png`));
      }
      console.log('✓ Q-04: Simulated video sequence (4 frames with wobble + drift)');

      console.log('\nAll test data generated. Run the quantizer with:');
      console.log('  npx ts-node src/tools/pixel-quantizer.ts -i test-frames/Q-01-control -o test-frames/output/Q-01 -p sean');
    }

    main().catch(console.error);
    ```

16. **Run the full test suite**

    ```bash
    # Generate test data
    npx ts-node src/tools/generate-test-data.ts

    # Run Q-01: Control test (should pass easily)
    npx ts-node src/tools/pixel-quantizer.ts \
      --input ./test-frames/Q-01-control \
      --output ./test-frames/output/Q-01 \
      --palette sean \
      --target-size 128 \
      --skip-temporal \
      --verbose

    # Run Q-02: Anti-aliased input
    npx ts-node src/tools/pixel-quantizer.ts \
      --input ./test-frames/Q-02-antialiased \
      --output ./test-frames/output/Q-02 \
      --palette sean \
      --target-size 128 \
      --skip-temporal \
      --verbose

    # Run Q-03: Color-drifted input
    npx ts-node src/tools/pixel-quantizer.ts \
      --input ./test-frames/Q-03-color-drift \
      --output ./test-frames/output/Q-03 \
      --palette sean \
      --target-size 128 \
      --skip-temporal \
      --verbose

    # Run Q-04: Full sequence with temporal smoothing
    npx ts-node src/tools/pixel-quantizer.ts \
      --input ./test-frames/Q-04-sequence \
      --output ./test-frames/output/Q-04 \
      --palette sean \
      --target-size 128 \
      --verbose

    # Review validation reports
    cat test-frames/output/Q-01/validation-report.json | python3 -m json.tool
    cat test-frames/output/Q-04/validation-report.json | python3 -m json.tool
    ```

**Decision Gate:** Does the quantizer produce acceptable pixel art from video-like input?

- **Q-01 PASS criteria:** Output should be near-identical to source sprite. Off-palette pixels = 0.
- **Q-02 PASS criteria:** Anti-aliased edges should snap to clean palette colors. Character should be recognizable.
- **Q-03 PASS criteria:** Drifted colors should snap back to correct palette entries. No visual artifacts.
- **Q-04 PASS criteria:** Temporal smoothing should eliminate jitter in static areas. Baseline should be consistent across frames.

**If ALL pass:** The hybrid pipeline is viable. Proceed to Phase 2.
**If Q-01/Q-02 fail:** Debug the quantizer — these are the easiest cases.
**If Q-03 fails:** Try adjusting `staticThreshold` and the palette distance algorithm. Consider Lab color space instead of RGB.
**If Q-04 fails:** Try the escalation path from the kickoff prompt: 256×256 target, Gemini restyle pass, or narrow hybrid scope.

**Gotchas:**
- The test data generator creates a crude programmatic sprite. For more realistic testing, manually create a proper pixel art sprite in Aseprite and place it at `test-frames/source/sprite-128.png`.
- Sharp may need to be rebuilt if you upgrade Node.js: `npm rebuild sharp`
- The palette quantizer uses Euclidean distance in RGB space. For better perceptual matching, consider switching to Lab color space in a future iteration.

---

## PHASE 2: FIRST AGENTS + VIDEO MODEL TESTING (Weeks 3-4, Apr 10 – Apr 24)

**Goal:** Deploy the first two autonomous agents, establish the baton file dependency chain, benchmark Gemini image models, evaluate video models, and test the full hybrid pipeline end-to-end.

**Phase 2 Task Map:**

```
Agent Track:                          Sprite Pipeline Track:
2.1 Process Inbox Agent ──┐           2.4 Nano Banana Benchmarking ──┐
2.2 Spending Analysis ────┤           2.5 rd-animation Evaluation ───┤
2.3 Baton File Chain ─────┘           2.6 Video Model Sprint ────────┤
                                      2.7 Pipeline Integration ──────┘
```

---

### 2.1 Process Inbox Agent — 3h

**Depends on:** 1.1, 1.2, 1.7, 1.8 (Mac Mini Ollama, SDK, router, hooks)
**Can parallel with:** 2.2, 2.4, 2.5
**Machine:** Mac Mini (100% local — phi4-mini-reasoning via Ollama)

**Steps:**

1. **Audit the process-inbox skill for interactive language**

   Before building the agent, check the skill file for phrases that assume a human is present:

   ```bash
   grep -in "ask me\|confirm with\|review with the user\|what would you like\|check with me\|should I" \
     .claude/skills/process-inbox/SKILL.md
   ```

   Replace any matches with autonomous decision criteria:
   - "Ask the user for tags" → "Apply tags based on content analysis. If confidence < 80%, add `#triage/human` tag."
   - "Confirm with the user" → "Make best-judgment decision and log reasoning."
   - "Should I continue?" → "Continue unless a hard gate fails."

2. **Create the agent implementation**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/process_inbox.py`:

   ```python
   #!/usr/bin/env python3
   """
   process_inbox.py — Process Inbox Agent

   Runs at 8:00 AM daily on the Mac Mini. Reads the Obsidian vault inbox,
   triages items, applies tags, routes to appropriate vault locations,
   and creates a summary in the daily note.

   100% local: uses phi4-mini-reasoning via Ollama on the Mac Mini.
   Cost per run: $0.00 (no API calls).

   Usage:
       PYTHONPATH=. .venv/bin/python3 agents/process_inbox.py [--dry-run]
   """

   import argparse
   import asyncio
   import time
   from datetime import date
   from pathlib import Path

   from claude_agent_sdk import query, ClaudeAgentOptions
   from lib.config import load_config
   from lib.skill_loader import load_skills
   from lib.logging_setup import setup_logger, record_run
   from lib.vault_io import daily_note_path, inject_at_anchor
   from lib.custom_tools import create_vault_mcp_server


   def build_preamble() -> str:
       """Autonomous operation context."""
       return """
   You are an autonomous inbox processing agent running on a Mac Mini.
   No human is present. You must make all decisions independently.

   RULES:
   - Process each inbox item: read, analyze, tag, route
   - If confidence in tag assignment is < 80%, add #triage/human
   - Never ask for confirmation — make your best judgment and log it
   - Write a summary of actions to the daily note under <!-- inbox-log -->
   - If the inbox is empty, write "Inbox empty — no items to process" and stop
   - Maximum 20 items per run to stay within turn limits
   """


   def build_prompt(config) -> str:
       """Task-specific instructions."""
       today = date.today().isoformat()
       vault_root = config.vault_root

       skill_content = load_skills(
           config.agent_config("process_inbox").skills,
           config.skills_dir,
       )

       return f"""
   {build_preamble()}

   ## Skills
   {skill_content}

   ## Today's Context
   - Date: {today}
   - Vault root: {vault_root}
   - Daily note: {daily_note_path(vault_root)}
   - Inbox location: {vault_root}/00_inbox/

   ## Task
   1. List all files in the inbox directory ({vault_root}/00_inbox/)
   2. For each file (up to 20):
      a. Read the file content
      b. Analyze: what is this about? (project, reference, task, idea)
      c. Assign tags based on content
      d. Move the file to the appropriate vault location:
         - Tasks → {vault_root}/30_tasks/
         - Project notes → {vault_root}/20_projects/[project-name]/
         - Reference → {vault_root}/50_sources/
         - Ideas → {vault_root}/40_ideas/
      e. Log the action
   3. Write a summary to the daily note at anchor <!-- inbox-log -->
   4. On success, create baton file at ~/.claude/batons/inbox_done.flag
   """


   def build_options(config) -> ClaudeAgentOptions:
       """SDK configuration."""
       agent_cfg = config.agent_config("process_inbox")
       vault_server = create_vault_mcp_server()

       return ClaudeAgentOptions(
           max_turns=agent_cfg.max_turns or 25,
           system_prompt="claude_code",
           setting_sources=["project"],
           permission_mode="acceptEdits",
           mcp_servers={"vault-tools": vault_server},
           allowed_tools=[
               "Read", "Write", "Edit", "Glob", "Grep",
               "mcp__vault-tools__vault_inject",
           ],
       )


   async def run(dry_run: bool = False):
       """Execute the Process Inbox agent."""
       config = load_config()
       agent_cfg = config.agent_config("process_inbox")

       if not agent_cfg.enabled:
           print("Process Inbox agent is disabled in config.toml")
           return

       logger = setup_logger("process_inbox", config.log_dir)
       prompt = build_prompt(config)

       if dry_run:
           print("=== DRY RUN — Process Inbox Agent ===")
           print(f"Skills: {agent_cfg.skills}")
           print(f"Max turns: {agent_cfg.max_turns}")
           print(f"\n--- PROMPT ---")
           print(prompt)
           print(f"\n--- END PROMPT ---")
           return

       logger.info("Starting Process Inbox agent")
       start_time = time.time()

       try:
           options = build_options(config)
           result = await query(prompt=prompt, options=options)

           duration_ms = (time.time() - start_time) * 1000
           cost = 0.0  # 100% local — no API cost

           # Extract response content
           response_text = ""
           for message in result:
               if hasattr(message, "content"):
                   response_text += str(message.content)

           logger.info(f"Process Inbox completed in {duration_ms:.0f}ms")
           logger.info(f"Response preview: {response_text[:200]}")

           record_run(
               log_dir=config.log_dir,
               agent_name="process_inbox",
               mode="daily",
               status="success",
               cost_usd=cost,
               duration_ms=duration_ms,
               turns=options.max_turns,
               notes="100% local via phi4-mini-reasoning",
           )

           # Create baton file for Daily Driver dependency chain
           baton_dir = Path.home() / ".claude" / "batons"
           baton_dir.mkdir(parents=True, exist_ok=True)
           baton_file = baton_dir / "inbox_done.flag"
           baton_file.write_text(f"completed:{date.today().isoformat()}")
           logger.info(f"Baton file created: {baton_file}")

       except Exception as e:
           duration_ms = (time.time() - start_time) * 1000
           logger.error(f"Process Inbox failed: {e}")
           record_run(
               log_dir=config.log_dir,
               agent_name="process_inbox",
               mode="daily",
               status="error",
               cost_usd=0.0,
               duration_ms=duration_ms,
               turns=0,
               notes=str(e),
           )


   def main():
       parser = argparse.ArgumentParser(description="Process Inbox Agent")
       parser.add_argument("--dry-run", action="store_true", help="Print prompt without running")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

3. **Add config.toml section**

   Ensure the following exists in `config.toml`:

   ```toml
   [agents.process_inbox]
   enabled = true
   skills = ["process-inbox", "vault-read-write"]
   max_turns = 25
   max_budget_usd = 0.00
   schedule = "08:00"
   machine = "mac_mini"
   model = "phi4-mini-reasoning"
   ```

4. **Create the launchd plist for 8:00 AM daily schedule**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/com.sean.agent.process-inbox.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.process-inbox</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>agents/process_inbox.py</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
       </dict>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>8</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/process-inbox-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/process-inbox-stderr.log</string>
   </dict>
   </plist>
   ```

   Install:
   ```bash
   cp schedules/com.sean.agent.process-inbox.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.process-inbox.plist

   # Verify
   launchctl list | grep process-inbox
   ```

5. **Test with dry run first**

   ```bash
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 agents/process_inbox.py --dry-run
   ```

   **Verify:** The prompt prints correctly with all skill content loaded and vault paths correct.

**Gotchas:**
- The `process-inbox` skill must exist at `.claude/skills/process-inbox/SKILL.md`. Create it if it doesn't exist yet.
- If the inbox is empty, the agent should handle this gracefully (write "no items" to the daily note and exit).
- The launchd plist paths must be absolute. Update `/Users/seanwinslow/` if your home directory is different.

---

### 2.2 Spending Analysis Agent — 3h

**Depends on:** 1.3 (MacBook Pro Ollama/MLX set up)
**Can parallel with:** 2.1, 2.4, 2.5
**Machine:** MacBook Pro (100% local — Qwen3:14b via Ollama or MLX)

**Steps:**

1. **Create the CSV anonymizer**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/sanitize_finance.py`:

   ```python
   #!/usr/bin/env python3
   """
   sanitize_finance.py — Financial Data Airgap

   Pre-processes raw bank CSVs before they reach any AI model.
   This is a "dumb" Python script (no AI) that:
   1. Drops account numbers and routing numbers
   2. Hashes transaction IDs (preserves uniqueness without exposing real IDs)
   3. Drops PII fields (full names, addresses)
   4. Outputs sanitized JSON for the Spending Analysis agent

   The raw CSV is NEVER seen by any LLM.

   Usage:
       python3 lib/sanitize_finance.py \
           --input ~/Downloads/chase-march-2026.csv \
           --output life-systems/finance/sanitized/march-2026.json
   """

   import argparse
   import csv
   import hashlib
   import json
   import re
   import sys
   from pathlib import Path
   from typing import Any


   # Fields to DROP completely (never reaches the agent)
   DROP_FIELDS = {
       "account number", "account_number", "accountnumber",
       "routing number", "routing_number", "routingnumber",
       "card number", "card_number", "cardnumber",
       "full name", "full_name", "name",
       "address", "street", "city", "state", "zip",
       "ssn", "social security",
   }

   # Fields to HASH (preserve uniqueness, hide real values)
   HASH_FIELDS = {
       "transaction id", "transaction_id", "transactionid",
       "reference number", "reference_number", "ref",
       "confirmation", "confirmation_number",
   }

   # PII patterns to scrub from description fields
   PII_PATTERNS = [
       r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card numbers
       r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',              # SSN
       r'\b\d{9,12}\b',                                   # Account numbers
   ]


   def normalize_field_name(name: str) -> str:
       """Normalize field name for comparison."""
       return name.lower().strip().replace("-", " ").replace("_", " ")


   def should_drop(field: str) -> bool:
       return normalize_field_name(field) in DROP_FIELDS


   def should_hash(field: str) -> bool:
       return normalize_field_name(field) in HASH_FIELDS


   def scrub_pii(text: str) -> str:
       """Remove PII patterns from free-text fields like descriptions."""
       result = text
       for pattern in PII_PATTERNS:
           result = re.sub(pattern, '[REDACTED]', result)
       return result


   def hash_value(val: str) -> str:
       """One-way hash a value. Preserves uniqueness, hides real value."""
       return hashlib.sha256(val.encode()).hexdigest()[:16]


   def sanitize_row(row: dict[str, str]) -> dict[str, Any] | None:
       """Sanitize a single CSV row."""
       sanitized = {}
       for field, value in row.items():
           if should_drop(field):
               continue
           elif should_hash(field):
               sanitized[field] = hash_value(value)
           elif normalize_field_name(field) in {"description", "memo", "notes", "details"}:
               sanitized[field] = scrub_pii(value)
           else:
               sanitized[field] = value
       return sanitized


   def sanitize_csv(input_path: Path, output_path: Path) -> dict[str, Any]:
       """Read a CSV, sanitize it, write JSON output."""
       output_path.parent.mkdir(parents=True, exist_ok=True)

       with open(input_path, newline='', encoding='utf-8-sig') as f:
           reader = csv.DictReader(f)
           if reader.fieldnames is None:
               print(f"ERROR: Could not read headers from {input_path}", file=sys.stderr)
               sys.exit(1)

           rows = []
           dropped_fields = set()
           hashed_fields = set()

           for row in reader:
               sanitized = sanitize_row(row)
               if sanitized:
                   rows.append(sanitized)

           # Track what was dropped/hashed for the audit log
           for field in reader.fieldnames:
               if should_drop(field):
                   dropped_fields.add(field)
               elif should_hash(field):
                   hashed_fields.add(field)

       output = {
           "metadata": {
               "source_file": input_path.name,
               "total_rows": len(rows),
               "dropped_fields": sorted(dropped_fields),
               "hashed_fields": sorted(hashed_fields),
               "sanitizer_version": "1.0.0",
           },
           "transactions": rows,
       }

       with open(output_path, 'w') as f:
           json.dump(output, f, indent=2)

       return output["metadata"]


   def main():
       parser = argparse.ArgumentParser(description="Sanitize bank CSV exports")
       parser.add_argument("--input", required=True, help="Path to raw bank CSV")
       parser.add_argument("--output", required=True, help="Path for sanitized JSON output")
       args = parser.parse_args()

       input_path = Path(args.input).expanduser()
       output_path = Path(args.output).expanduser()

       if not input_path.exists():
           print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
           sys.exit(1)

       metadata = sanitize_csv(input_path, output_path)
       print(f"✓ Sanitized {metadata['total_rows']} transactions")
       print(f"  Dropped fields: {metadata['dropped_fields']}")
       print(f"  Hashed fields: {metadata['hashed_fields']}")
       print(f"  Output: {output_path}")


   if __name__ == "__main__":
       main()
   ```

   **Why:** Raw bank CSVs contain account numbers, SSNs, and card numbers. This script creates a "data airgap" — no AI model ever sees the raw financial data. The agent only sees the sanitized JSON.

   **Verify:**
   ```bash
   # Create a test CSV
   cat > /tmp/test-bank.csv << 'EOF'
   Date,Description,Amount,Account Number,Transaction ID
   2026-03-01,VENMO PAYMENT,-25.00,1234567890,TXN-ABC-123
   2026-03-02,TRADER JOES,-45.67,1234567890,TXN-DEF-456
   EOF

   # Run the sanitizer
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   python3 lib/sanitize_finance.py \
       --input /tmp/test-bank.csv \
       --output /tmp/test-sanitized.json

   # Inspect output — should have NO account numbers, hashed transaction IDs
   cat /tmp/test-sanitized.json | python3 -m json.tool
   ```

2. **Create the Spending Analysis agent**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/spending_analysis.py`:

   ```python
   #!/usr/bin/env python3
   """
   Spending Analysis Agent — 100% Local (MacBook Pro)

   Analyzes sanitized financial data and writes insights to the vault.
   Runs weekly on Sunday at 9:00 AM.

   Model: Qwen3:14b via Ollama (or MLX if benchmark showed 2x+ improvement)
   Machine: MacBook Pro (routed via hybrid_router.py)

   IMPORTANT: This agent ONLY sees sanitized JSON from sanitize_finance.py.
   Raw bank CSVs are NEVER processed by any AI model.
   """

   import argparse
   import asyncio
   import json
   import sys
   from datetime import datetime
   from pathlib import Path

   # Add parent to path for lib imports
   sys.path.insert(0, str(Path(__file__).parent.parent))

   from claude_agent_sdk import ClaudeAgentOptions, query
   from lib.config import load_config
   from lib.custom_tools import create_vault_mcp_server
   from lib.logging_setup import record_run, setup_logger
   from lib.skill_loader import load_skills


   def find_latest_sanitized(config) -> Path | None:
       """Find the most recent sanitized JSON file."""
       finance_dir = Path(config.repo_root) / config.agent_config("spending_analysis").input_dir
       sanitized_dir = finance_dir / "sanitized"
       if not sanitized_dir.exists():
           return None
       json_files = sorted(sanitized_dir.glob("*.json"), reverse=True)
       return json_files[0] if json_files else None


   def build_preamble(config) -> str:
       return """You are an autonomous financial analysis agent. No human is present.
   Make best-judgment decisions. Write all output to vault files, not stdout.

   RULES:
   - Never ask for confirmation or clarification
   - If data is ambiguous, document the ambiguity and proceed with your best interpretation
   - Write findings to the daily note under the <!-- finance --> anchor
   - Use structured markdown tables for transaction summaries
   - Flag any spending anomalies (unusual amounts, duplicate charges, new subscriptions)
   - Calculate category totals and compare to previous periods if available
   - All amounts in USD
   """


   def build_prompt(mode: str, config, data_path: Path) -> str:
       # Read the sanitized data
       with open(data_path) as f:
           data = json.load(f)

       skills_prompt = load_skills(
           config.agent_config("spending_analysis").skills,
           config.skills_dir,
       )

       return f"""{build_preamble(config)}

   {skills_prompt}

   ## Task: Weekly Spending Analysis

   Analyze the following sanitized financial data and produce:
   1. **Category Breakdown** — Group transactions by merchant/category, show totals
   2. **Anomaly Detection** — Flag unusual charges, potential duplicates, new subscriptions
   3. **Top 5 Spending Categories** — Ranked by total amount
   4. **Week-over-Week Trend** — Compare to last week's analysis if available in the vault

   Write results to today's daily note under the `<!-- finance -->` anchor.

   ### Sanitized Financial Data
   ```json
   {json.dumps(data, indent=2)[:8000]}
   ```

   If the data exceeds what's shown above, note that in your analysis.
   """


   def build_options(config) -> ClaudeAgentOptions:
       agent_cfg = config.agent_config("spending_analysis")
       vault_server = create_vault_mcp_server()

       return ClaudeAgentOptions(
           system_prompt={"type": "preset", "preset": "claude_code"},
           max_turns=agent_cfg.max_turns or 20,
           max_budget_usd=agent_cfg.max_budget_usd or 0.25,
           permission_mode="acceptEdits",
           setting_sources=["project"],
           mcp_servers={"vault-tools": vault_server},
           allowed_tools=[
               "Read", "Write", "Edit", "Glob", "Grep",
               "mcp__vault-tools__vault_inject",
           ],
       )


   async def run(dry_run: bool = False):
       config = load_config()
       agent_cfg = config.agent_config("spending_analysis")

       if not agent_cfg.enabled:
           print("Spending analysis agent is disabled in config.toml")
           return

       logger = setup_logger("spending_analysis", config.log_dir)

       # Find latest sanitized data
       data_path = find_latest_sanitized(config)
       if data_path is None:
           logger.warning("No sanitized financial data found. Run sanitize_finance.py first.")
           record_run(config.log_dir, "spending_analysis", "weekly",
                      "skipped", 0.0, 0, 0, "No sanitized data found")
           return

       prompt = build_prompt("weekly", config, data_path)

       if dry_run:
           print("=== DRY RUN — Spending Analysis Agent ===")
           print(f"Data source: {data_path}")
           print(f"Prompt length: {len(prompt)} chars")
           print("---")
           print(prompt[:2000])
           print("... [truncated]")
           return

       options = build_options(config)
       logger.info(f"Starting spending analysis with data from {data_path.name}")
       start = datetime.now()

       try:
           result = await query(prompt=prompt, options=options)
           duration = (datetime.now() - start).total_seconds() * 1000
           cost = getattr(result, 'cost_usd', 0.0)
           logger.info(f"Spending analysis complete. Cost: ${cost:.4f}")
           record_run(config.log_dir, "spending_analysis", "weekly",
                      "success", cost, duration,
                      getattr(result, 'num_turns', 0))
       except Exception as e:
           duration = (datetime.now() - start).total_seconds() * 1000
           logger.error(f"Spending analysis failed: {e}")
           record_run(config.log_dir, "spending_analysis", "weekly",
                      "error", 0.0, duration, 0, str(e))
           raise


   def main():
       parser = argparse.ArgumentParser(description="Spending Analysis Agent")
       parser.add_argument("--dry-run", action="store_true",
                           help="Print prompt without calling API")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

3. **Add agent configuration to config.toml**

   Add these lines to `~/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml`:

   ```toml
   [agents.spending_analysis]
   enabled = true
   skills = ["subscription-audit", "vault-read-write"]
   max_turns = 20
   max_budget_usd = 0.25
   input_dir = "life-systems/finance"
   output_dir = "vault/50_sources/finance"
   schedule = "Sunday 09:00"
   ```

4. **Create the launchd plist for Sunday scheduling**

   Create `~/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/com.sean.agent.spending-analysis.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
       "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.spending-analysis</string>

       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/spending_analysis.py</string>
       </array>

       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack</string>

       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
           <key>PATH</key>
           <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
       </dict>

       <!-- Sunday = 0 in launchd (Sunday=0, Monday=1, ... Saturday=6) -->
       <key>StartCalendarInterval</key>
       <dict>
           <key>Weekday</key>
           <integer>0</integer>
           <key>Hour</key>
           <integer>9</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>

       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/spending-analysis-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/spending-analysis-stderr.log</string>
   </dict>
   </plist>
   ```

5. **Install the launchd plist (on Mac Mini)**

   ```bash
   # Machine: Mac Mini
   cp ~/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/com.sean.agent.spending-analysis.plist \
       ~/Library/LaunchAgents/

   launchctl load ~/Library/LaunchAgents/com.sean.agent.spending-analysis.plist
   ```

   **Why:** Even though the model runs on the MacBook Pro, the Mac Mini orchestrates the schedule. The agent script uses `hybrid_router.py` to route the inference call to the MacBook Pro's Ollama/MLX endpoint over the LAN. If the MacBook is closed, it falls back to a smaller model on the Mac Mini or to Claude Haiku API.

   **Verify:**
   ```bash
   # Verify the plist is loaded
   launchctl list | grep spending

   # Test with dry run
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 agents/spending_analysis.py --dry-run
   ```

**Gotchas:**
- The sanitizer must run BEFORE the agent. The agent never sees raw CSVs.
- Chase, Bilt, and other banks export CSVs with slightly different column names. The `normalize_field_name()` function handles common variants, but you may need to add new ones.
- The `sunday = 0` convention in launchd is different from cron (where Sunday = 0 or 7). Double-check the plist.
- If you use Google Drive as the CSV drop zone, the sanitizer reads from the synced folder. Make sure Google Drive has finished syncing before the agent runs.

---

### 2.3 Baton File Dependency Chain — 1.5h

**Depends on:** 2.1 (Process Inbox Agent exists)
**Can parallel with:** 2.4, 2.5, 2.6
**Machine:** Mac Mini

**Steps:**

1. **Understand the baton pattern**

   The Baton File pattern creates dependencies between launchd agents without hardcoding times. Instead of "run Process Inbox at 8:00 AM, then Daily Driver at 8:15 AM," the chain is:
   - Process Inbox runs at 8:00 AM
   - On success, Process Inbox touches a flag file
   - Daily Driver's launchd plist watches for that flag file
   - When the flag appears, Daily Driver runs immediately

   **Why:** This is more reliable than time-based scheduling. If Process Inbox takes 2 minutes one day and 10 minutes another, the Daily Driver always runs at the right time — after inbox processing is complete, not at a hardcoded offset.

2. **Add baton file creation to Process Inbox agent**

   Add this to the end of the `run()` function in `agents/process_inbox.py` (after the successful `query()` call):

   ```python
   # At the top of the file, add:
   BATON_DIR = Path.home() / ".claude" / "batons"

   # Inside the run() function, after successful query():
   def touch_baton(name: str):
       """Create a baton file to signal dependent agents."""
       BATON_DIR.mkdir(parents=True, exist_ok=True)
       baton_path = BATON_DIR / f"{name}.flag"
       baton_path.write_text(datetime.now().isoformat())
       logger.info(f"Baton touched: {baton_path}")

   # After successful query() in run():
   touch_baton("inbox_done")
   ```

   **Verify:**
   ```bash
   # After running Process Inbox
   cat ~/.claude/batons/inbox_done.flag
   # Should show an ISO timestamp like: 2026-04-11T08:03:42.123456
   ```

3. **Create a WatchPaths-based launchd plist for Daily Driver**

   Create (or update) `~/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/com.sean.agent.daily-morning-chained.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
       "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.daily-morning-chained</string>

       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/daily_driver.py</string>
           <string>--mode</string>
           <string>morning</string>
       </array>

       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack</string>

       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
           <key>PATH</key>
           <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
       </dict>

       <!-- Trigger when the baton file is created/modified -->
       <key>WatchPaths</key>
       <array>
           <string>/Users/seanwinslow/.claude/batons/inbox_done.flag</string>
       </array>

       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/daily-morning-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/daily-morning-stderr.log</string>
   </dict>
   </plist>
   ```

   **Why:** The `WatchPaths` key tells launchd to run this job whenever any file in the array is modified. When Process Inbox writes the baton file, launchd detects the change and triggers Daily Driver immediately.

4. **Add baton cleanup to Daily Driver**

   Add this at the START of the `run()` function in `agents/daily_driver.py`:

   ```python
   BATON_DIR = Path.home() / ".claude" / "batons"

   def clean_baton(name: str):
       """Remove a consumed baton file."""
       baton_path = BATON_DIR / f"{name}.flag"
       if baton_path.exists():
           baton_path.unlink()
           logger.info(f"Baton consumed: {baton_path}")

   # At the START of run() for morning mode:
   if mode == "morning":
       clean_baton("inbox_done")
   ```

   **Why:** Cleaning the baton prevents re-triggering. If you don't clean it, modifying the baton directory for any reason could re-trigger the Daily Driver.

5. **Install the chained plist**

   ```bash
   # Machine: Mac Mini

   # First, unload the old time-based morning plist if it exists
   launchctl unload ~/Library/LaunchAgents/com.sean.agent.daily-morning.plist 2>/dev/null

   # Install the new WatchPaths-based plist
   cp ~/Code-Brain/claude-code-superuser-pack/agents-sdk/schedules/com.sean.agent.daily-morning-chained.plist \
       ~/Library/LaunchAgents/

   launchctl load ~/Library/LaunchAgents/com.sean.agent.daily-morning-chained.plist
   ```

6. **Add a safety fallback: keep a time-based trigger too**

   What if Process Inbox fails and never writes the baton? The Daily Driver should still run by a deadline. Add BOTH `WatchPaths` and `StartCalendarInterval` to the plist:

   ```xml
   <!-- Add this ALONGSIDE the WatchPaths key in the plist above -->
   <key>StartCalendarInterval</key>
   <dict>
       <key>Hour</key>
       <integer>8</integer>
       <key>Minute</key>
       <integer>30</integer>
   </dict>
   ```

   **Why:** With both triggers, Daily Driver runs EITHER when the baton appears (ideal) OR at 8:30 AM (fallback). This ensures it never misses a day even if Process Inbox fails.

7. **Test the full chain end-to-end**

   ```bash
   # Machine: Mac Mini

   # Step 1: Manually trigger Process Inbox
   cd ~/Code-Brain/claude-code-superuser-pack/agents-sdk
   PYTHONPATH=. .venv/bin/python3 agents/process_inbox.py --dry-run

   # Step 2: Check that the baton was created (even dry-run should touch it for testing)
   ls -la ~/.claude/batons/
   cat ~/.claude/batons/inbox_done.flag

   # Step 3: Check if Daily Driver was triggered
   # Wait 5-10 seconds, then check
   tail -5 ~/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/daily-morning-stdout.log

   # Step 4: Verify baton was cleaned up
   ls -la ~/.claude/batons/
   # inbox_done.flag should be gone
   ```

   **Verify:** The chain is working when:
   1. Process Inbox runs and creates `~/.claude/batons/inbox_done.flag`
   2. Within seconds, Daily Driver starts (check stdout log for new entries)
   3. Daily Driver removes the baton file after starting

**Decision Gate:** If `WatchPaths` doesn't trigger reliably (some macOS versions have a small delay), fall back to the time-offset approach: Process Inbox at 8:00 AM, Daily Driver at 8:15 AM. The baton pattern is better but not critical.

**Gotchas:**
- `WatchPaths` only monitors for file system changes — it won't fire if the file already exists and hasn't changed since the last check. That's why we write the current timestamp to the baton (not just `touch`).
- The baton directory (`~/.claude/batons/`) must exist before launchd tries to watch it. Add a `mkdir -p` to your install script.
- If both `WatchPaths` and `StartCalendarInterval` trigger at the same time, launchd will only run the job once, not twice.

---

### 2.4 Nano Banana 2 vs Pro Benchmarking — 2h

**Depends on:** None — can start immediately (just needs a Google AI API key)
**Can parallel with:** 2.1, 2.2, 2.3, 2.5
**Machine:** MacBook Pro (for running the benchmark script; API calls go to Google Cloud)

**Steps:**

1. **Set up the benchmark project**

   ```bash
   # Machine: MacBook Pro
   mkdir -p ~/Code-Brain/sprite-pipeline/benchmarks/gemini-image
   cd ~/Code-Brain/sprite-pipeline/benchmarks/gemini-image

   npm init -y
   npm install @google/genai@1.20.0 sharp yargs
   npm install -D typescript @types/node ts-node
   npx tsc --init --target ES2022 --module NodeNext --moduleResolution NodeNext \
       --outDir dist --strict true --esModuleInterop true
   ```

   **Why:** We use `@google/genai` v1.20.0 (NOT the older `@google/generative-ai` package). This is the current SDK for Gemini image generation.

2. **Create the benchmark script**

   Create `~/Code-Brain/sprite-pipeline/benchmarks/gemini-image/benchmark.ts`:

   ```typescript
   #!/usr/bin/env npx ts-node
   /**
    * Nano Banana 2 vs Pro Benchmark
    *
    * Generates the same sprite prompt with both models, 10 iterations each.
    * Measures: generation time, cost per image, saves outputs for manual quality review.
    *
    * Models:
    *   - Nano Banana Pro:  gemini-3-pro-image-preview     (~$0.035/image)
    *   - Nano Banana 2:    gemini-3.1-flash-image-preview  (~$0.01-0.02/image)
    *
    * Usage:
    *   GOOGLE_API_KEY=your-key npx ts-node benchmark.ts
    */

   import { GoogleGenAI, type GenerateContentResponse } from '@google/genai';
   import * as fs from 'fs';
   import * as path from 'path';

   // --- Configuration ---
   const MODELS = {
     'nano-banana-pro': 'gemini-3-pro-image-preview',
     'nano-banana-2': 'gemini-3.1-flash-image-preview',
   } as const;

   const ITERATIONS = 10;

   const SPRITE_PROMPT = `Generate a single 2D pixel art sprite of a muscular male fighter character in an idle standing pose.

   Style: Street Fighter II / Capcom arcade, 16-bit era, full color.
   Character: Athletic build, dirty blonde hair, wearing a white tank top, neon blue pants, white shoes.
   Pose: Idle standing, slight bounce, fists at sides, facing RIGHT.
   Background: Solid #00FF00 chroma key green.
   Resolution: 512x512 pixels.
   Art style: Bold dark outlines (#272929), 2-3px weight. Clean pixel art with no anti-aliasing.
   No text, no watermark, no signature.`;

   const OUTPUT_DIR = path.join(__dirname, 'output');

   // --- Types ---
   interface BenchmarkResult {
     model: string;
     modelId: string;
     iteration: number;
     durationMs: number;
     success: boolean;
     error?: string;
     outputFile?: string;
   }

   // --- Main ---
   async function generateImage(
     client: GoogleGenAI,
     modelId: string,
     prompt: string,
   ): Promise<{ imageData: Buffer | null; durationMs: number; error?: string }> {
     const start = performance.now();

     try {
       const response: GenerateContentResponse = await client.models.generateContent({
         model: modelId,
         contents: prompt,
         config: {
           responseModalities: ['image', 'text'],
           temperature: 1.0,
         },
       });

       const durationMs = performance.now() - start;

       // Extract image from response
       const parts = response.candidates?.[0]?.content?.parts ?? [];
       for (const part of parts) {
         if (part.inlineData?.mimeType?.startsWith('image/')) {
           const imageData = Buffer.from(part.inlineData.data!, 'base64');
           return { imageData, durationMs };
         }
       }

       return { imageData: null, durationMs, error: 'No image in response' };
     } catch (err: any) {
       const durationMs = performance.now() - start;
       return { imageData: null, durationMs, error: err.message };
     }
   }

   async function runBenchmark(): Promise<void> {
     const apiKey = process.env.GOOGLE_API_KEY;
     if (!apiKey) {
       console.error('ERROR: Set GOOGLE_API_KEY environment variable');
       process.exit(1);
     }

     const client = new GoogleGenAI({ apiKey });
     const results: BenchmarkResult[] = [];

     // Create output directories
     for (const modelName of Object.keys(MODELS)) {
       fs.mkdirSync(path.join(OUTPUT_DIR, modelName), { recursive: true });
     }

     for (const [modelName, modelId] of Object.entries(MODELS)) {
       console.log(`\n=== Benchmarking: ${modelName} (${modelId}) ===`);

       for (let i = 1; i <= ITERATIONS; i++) {
         console.log(`  Iteration ${i}/${ITERATIONS}...`);

         const { imageData, durationMs, error } = await generateImage(
           client,
           modelId,
           SPRITE_PROMPT,
         );

         const result: BenchmarkResult = {
           model: modelName,
           modelId,
           iteration: i,
           durationMs: Math.round(durationMs),
           success: imageData !== null,
           error,
         };

         if (imageData) {
           const filename = `${modelName}_iter${String(i).padStart(2, '0')}.png`;
           const outputPath = path.join(OUTPUT_DIR, modelName, filename);
           fs.writeFileSync(outputPath, imageData);
           result.outputFile = filename;
           console.log(`    ✓ ${Math.round(durationMs)}ms → ${filename}`);
         } else {
           console.log(`    ✗ ${Math.round(durationMs)}ms — ${error}`);
         }

         results.push(result);

         // Rate limit: wait 2 seconds between calls
         await new Promise((resolve) => setTimeout(resolve, 2000));
       }
     }

     // --- Summary ---
     console.log('\n\n=== BENCHMARK RESULTS ===\n');

     for (const modelName of Object.keys(MODELS)) {
       const modelResults = results.filter((r) => r.model === modelName);
       const successes = modelResults.filter((r) => r.success);
       const avgMs =
         successes.reduce((sum, r) => sum + r.durationMs, 0) / successes.length;
       const minMs = Math.min(...successes.map((r) => r.durationMs));
       const maxMs = Math.max(...successes.map((r) => r.durationMs));

       console.log(`${modelName}:`);
       console.log(`  Success rate: ${successes.length}/${modelResults.length}`);
       console.log(`  Avg time:     ${Math.round(avgMs)}ms`);
       console.log(`  Min time:     ${Math.round(minMs)}ms`);
       console.log(`  Max time:     ${Math.round(maxMs)}ms`);
       console.log(
         `  Est. cost:    $${modelName === 'nano-banana-pro' ? (successes.length * 0.035).toFixed(3) : (successes.length * 0.015).toFixed(3)}`,
       );
       console.log();
     }

     // Save results JSON
     const reportPath = path.join(OUTPUT_DIR, 'benchmark-results.json');
     fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));
     console.log(`Full results saved to: ${reportPath}`);
     console.log(`\nImages saved to: ${OUTPUT_DIR}/`);
     console.log(
       '\nNext step: Manually review images side-by-side using the scoring rubric below.',
     );
   }

   runBenchmark().catch(console.error);
   ```

   **Verify:**
   ```bash
   cd ~/Code-Brain/sprite-pipeline/benchmarks/gemini-image
   GOOGLE_API_KEY=your-key-here npx ts-node benchmark.ts
   ```

3. **Manual quality scoring rubric**

   After the benchmark generates images, score each pair side-by-side:

   | Criterion | Weight | 1 (Poor) | 3 (Acceptable) | 5 (Excellent) |
   |-----------|--------|----------|-----------------|---------------|
   | **Palette fidelity** | 25% | Many off-palette colors | Mostly correct, some drift | Exact palette match |
   | **Outline quality** | 20% | Soft/missing outlines | Inconsistent weight | Bold, consistent #272929 |
   | **Pose accuracy** | 20% | Wrong pose entirely | Roughly correct | Exact idle pose |
   | **Character consistency** | 20% | Unrecognizable | Recognizable but drifted | Identical to prompt |
   | **Background cleanliness** | 15% | Artifacts in background | Some fringe | Pure #00FF00 |

   Calculate weighted average for each model. If Nano Banana 2 scores within 15% of Pro, use Flash for volume generation to save ~65% on image costs.

**Decision Gate:**
- **If Nano Banana 2 scores ≥ 85% of Pro:** Use Nano Banana 2 for all volume generation (keyframes, bulk frames). Use Pro only for anchor/gold reference sprites.
- **If Nano Banana 2 scores < 85% of Pro:** Use Pro for anchors AND keyframes. Use Nano Banana 2 only for experimentation/iteration.
- **If both fail:** Re-evaluate the prompt. The scoring rubric tells you exactly what to fix.

**Gotchas:**
- Rate limits differ between Pro and Flash. Pro may be more restrictive. Add longer delays if you hit 429 errors.
- Both models are non-deterministic at temperature 1.0. That's expected — you're benchmarking the distribution of quality, not individual outputs.
- `@google/genai` v1.20.0 is the correct package. If you see import errors, make sure you're NOT using `@google/generative-ai` (the older, deprecated SDK).

---

### 2.5 Retro Diffusion rd-animation Evaluation — 2h (NEW per validation audit)

**Depends on:** None — can start immediately (just needs Replicate API key)
**Can parallel with:** 2.1, 2.2, 2.3, 2.4, 2.6
**Machine:** MacBook Pro (API calls go to Replicate cloud)

**Steps:**

1. **Set up Replicate access**

   ```bash
   # Machine: MacBook Pro
   npm install replicate
   # Or if using Python:
   pip install replicate
   ```

   Set your API token:
   ```bash
   export REPLICATE_API_TOKEN=r8_your_token_here
   ```

   **Why:** Retro Diffusion's `rd-animation` is now live on Replicate (4.9K+ runs). It generates pixel art animations natively — meaning it could bypass the entire hybrid pipeline (Gemini keyframes → video model → pixel quantizer) for standard animations like walk cycles.

2. **Create the evaluation script**

   Create `~/Code-Brain/sprite-pipeline/benchmarks/retro-diffusion/evaluate-rd.ts`:

   ```typescript
   #!/usr/bin/env npx ts-node
   /**
    * Retro Diffusion rd-animation Evaluation
    *
    * Tests rd-animation on Replicate for:
    * 1. Walk cycle generation (SF2-style character)
    * 2. four_angle_walking style preset
    * 3. Quality comparison to Gemini-generated keyframes
    */

   import Replicate from 'replicate';
   import * as fs from 'fs';
   import * as path from 'path';

   const OUTPUT_DIR = path.join(__dirname, 'output');

   interface TestCase {
     name: string;
     prompt: string;
     style_preset?: string;
     num_frames?: number;
   }

   const TEST_CASES: TestCase[] = [
     {
       name: 'walk-cycle-basic',
       prompt:
         'A muscular male pixel art fighter character walking, Street Fighter II style, dirty blonde hair, white tank top, neon blue pants, white shoes, bold dark outlines, 128x128 pixels, facing right, transparent background',
       num_frames: 8,
     },
     {
       name: 'walk-cycle-four-angle',
       prompt:
         'A muscular male pixel art fighter character, Street Fighter II style, dirty blonde hair, white tank top, neon blue pants, white shoes, bold dark outlines',
       style_preset: 'four_angle_walking',
       num_frames: 8,
     },
     {
       name: 'idle-animation',
       prompt:
         'A muscular male pixel art fighter character in idle stance, slight breathing animation, Street Fighter II style, dirty blonde hair, white tank top, neon blue pants, white shoes, bold dark outlines, 128x128 pixels, facing right',
       num_frames: 4,
     },
   ];

   async function runTest(
     replicate: Replicate,
     testCase: TestCase,
   ): Promise<void> {
     console.log(`\n--- Testing: ${testCase.name} ---`);
     console.log(`Prompt: ${testCase.prompt.substring(0, 80)}...`);

     const start = performance.now();

     try {
       // Note: Check the actual model version on Replicate
       // The model identifier may be "retrodiffusion/rd-animation" or similar
       const output = await replicate.run('retrodiffusion/rd-animation', {
         input: {
           prompt: testCase.prompt,
           ...(testCase.style_preset && {
             style_preset: testCase.style_preset,
           }),
           ...(testCase.num_frames && { num_frames: testCase.num_frames }),
           // Add other parameters as documented on Replicate
         },
       });

       const durationMs = performance.now() - start;
       console.log(`  Completed in ${Math.round(durationMs)}ms`);

       // Save output (could be URL(s) to generated sprite sheet or GIF)
       const outputDir = path.join(OUTPUT_DIR, testCase.name);
       fs.mkdirSync(outputDir, { recursive: true });

       // Handle different output formats
       if (typeof output === 'string') {
         // Single URL output
         console.log(`  Output URL: ${output}`);
         fs.writeFileSync(
           path.join(outputDir, 'output-url.txt'),
           output as string,
         );
       } else if (Array.isArray(output)) {
         // Multiple outputs
         for (let i = 0; i < output.length; i++) {
           console.log(`  Output ${i}: ${output[i]}`);
           fs.writeFileSync(
             path.join(outputDir, `output-${i}-url.txt`),
             String(output[i]),
           );
         }
       }

       // Save metadata
       fs.writeFileSync(
         path.join(outputDir, 'metadata.json'),
         JSON.stringify(
           {
             testCase,
             durationMs: Math.round(durationMs),
             output,
             timestamp: new Date().toISOString(),
           },
           null,
           2,
         ),
       );

       console.log(`  Results saved to: ${outputDir}/`);
     } catch (err: any) {
       const durationMs = performance.now() - start;
       console.error(`  FAILED (${Math.round(durationMs)}ms): ${err.message}`);
     }
   }

   async function main(): Promise<void> {
     const token = process.env.REPLICATE_API_TOKEN;
     if (!token) {
       console.error('ERROR: Set REPLICATE_API_TOKEN environment variable');
       process.exit(1);
     }

     const replicate = new Replicate({ auth: token });
     fs.mkdirSync(OUTPUT_DIR, { recursive: true });

     for (const testCase of TEST_CASES) {
       await runTest(replicate, testCase);
     }

     console.log('\n\n=== EVALUATION COMPLETE ===');
     console.log(`Results in: ${OUTPUT_DIR}/`);
     console.log('\nManual review checklist:');
     console.log('  □ Walk cycle: Correct left/right leg alternation?');
     console.log('  □ Walk cycle: Consistent character appearance across frames?');
     console.log('  □ Walk cycle: Pixel art quality (crisp edges, no anti-aliasing)?');
     console.log('  □ Four-angle: All four directions present and correct?');
     console.log('  □ Style: Matches SF2/Capcom aesthetic?');
     console.log('  □ Resolution: Appropriate for 128x128 final output?');
     console.log('  □ Background: Clean/transparent or easily removable?');
   }

   main().catch(console.error);
   ```

3. **Run the evaluation**

   ```bash
   cd ~/Code-Brain/sprite-pipeline/benchmarks/retro-diffusion
   npm init -y && npm install replicate typescript ts-node @types/node
   REPLICATE_API_TOKEN=r8_your_token npx ts-node evaluate-rd.ts
   ```

4. **Score the results**

   Review the generated animations against these criteria:

   | Criterion | Pass | Fail |
   |-----------|------|------|
   | Correct walk cycle mechanics (proper leg alternation) | Left/right legs clearly alternate | Legs don't move or skip |
   | Character consistency across frames | Same character in all frames | Significant drift between frames |
   | Pixel art fidelity | Clean edges, no anti-aliasing, clear pixels | Blurry, anti-aliased, gradient-heavy |
   | Palette compatibility | Colors close to target palette (can be snapped) | Wildly different color scheme |
   | Resolution/detail at 128x128 | Recognizable details at target res | Too much detail lost at downscale |
   | Background separation | Clean transparency or removable background | Complex background mixed with character |

**Decision Gate:**
- **If rd-animation produces quality walk cycles:** This could bypass the entire hybrid pipeline (Gemini keyframes → video model → pixel quantizer) for standard animations. Keep the hybrid pipeline for complex, custom animations only. This is a potential massive simplification.
- **If rd-animation quality is close but not quite there:** Could be used as a starting point that's refined by the pixel quantizer (fewer steps needed than processing video model output).
- **If rd-animation quality is insufficient:** Proceed with hybrid pipeline as planned. rd-animation is a nice-to-have, not a dependency.

**Gotchas:**
- Replicate bills per-prediction. Check current pricing for rd-animation before running many iterations.
- The model's exact input parameters may differ from what's documented. Check the Replicate model page for the current API schema.
- rd-animation may output sprite sheets (single image with all frames) rather than individual frame files. You'll need to split the sheet.

---

### 2.6 Video Model API Setup and Evaluation Sprint — 6h

**Depends on:** 1.10 (Pixel Quantizer must be built and passing Q-01 through Q-04)
**Can parallel with:** 2.1, 2.2, 2.3
**Machine:** MacBook Pro (API calls go to cloud services)

**Steps:**

1. **Set up fal.ai account for Pika Pikaframes 2.2**

   ```bash
   # Machine: MacBook Pro
   # Create account at https://fal.ai
   # Get API key from https://fal.ai/dashboard/keys

   # Install the fal.ai client
   npm install @fal-ai/client
   ```

   Set environment variable:
   ```bash
   export FAL_KEY=your-fal-ai-key-here
   ```

2. **Set up Kling API access**

   ```bash
   # Kling API: https://docs.klingai.com/
   # Create account and get API key
   # Install via their SDK or use fetch/axios for REST calls
   npm install axios
   ```

3. **Create the evaluation framework**

   Create `~/Code-Brain/sprite-pipeline/benchmarks/video-models/evaluation-framework.ts`:

   ```typescript
   #!/usr/bin/env npx ts-node
   /**
    * Video Model Evaluation Framework
    *
    * Tests the full pipeline:
    *   1. Generate 3-4 keyframes with Gemini (Nano Banana Pro)
    *   2. Send keyframes to video model for interpolation
    *   3. Extract frames from video output
    *   4. Run through pixel quantizer
    *   5. Score results
    *
    * Video models tested:
    *   - Pika Pikaframes 2.2 (via fal.ai) — Priority 1
    *   - Kling 3.0 start/end frame control — Priority 2
    *   - Kling 2.6 motion transfer — Priority 3
    *
    * Scoring:
    *   - SSIM (Structural Similarity) between output and anchor
    *   - Aesthetic quality (manual 1-5 scale)
    *   - Walk cycle correctness (manual: proper leg alternation)
    *   - Pixel art quality after quantization (manual: clean edges)
    */

   import * as fal from '@fal-ai/client';
   import * as fs from 'fs';
   import * as path from 'path';
   import { execSync } from 'child_process';

   // --- Configuration ---
   const OUTPUT_BASE = path.join(__dirname, 'output');
   const KEYFRAME_DIR = path.join(OUTPUT_BASE, 'keyframes');
   const VIDEO_DIR = path.join(OUTPUT_BASE, 'videos');
   const FRAMES_DIR = path.join(OUTPUT_BASE, 'extracted-frames');
   const QUANTIZED_DIR = path.join(OUTPUT_BASE, 'quantized');

   // --- Step 1: Generate keyframes with Gemini ---
   // (Assumes you have keyframes already generated from task 2.4,
   //  or generate them using the benchmark script from 2.4)
   // For this evaluation, place 3-4 keyframe PNGs in KEYFRAME_DIR:
   //   keyframe_01.png (idle/start pose)
   //   keyframe_02.png (left foot forward)
   //   keyframe_03.png (passing position)
   //   keyframe_04.png (right foot forward)

   // --- Step 2: Test Pika Pikaframes 2.2 ---
   async function testPikaPikaframes(keyframePaths: string[]): Promise<string> {
     console.log('\n=== Testing Pika Pikaframes 2.2 via fal.ai ===');

     // Configure fal.ai
     fal.config({ credentials: process.env.FAL_KEY });

     const start = performance.now();

     try {
       // Read keyframe images as base64
       const keyframeImages = keyframePaths.map((p) => {
         const data = fs.readFileSync(p);
         return `data:image/png;base64,${data.toString('base64')}`;
       });

       // Call Pika Pikaframes 2.2
       // Note: Check fal.ai docs for exact endpoint and parameters
       const result = await fal.subscribe('fal-ai/pika/pikaframes', {
         input: {
           keyframes: keyframeImages,
           // Parameters may include:
           // fps: 12,
           // duration: 2,
           // guidance_scale: 7.5,
         },
       });

       const durationMs = performance.now() - start;
       console.log(`  Completed in ${Math.round(durationMs)}ms`);

       // Save the video output
       const videoUrl = (result as any).data?.video?.url || (result as any).video?.url;
       if (videoUrl) {
         const outputPath = path.join(VIDEO_DIR, 'pika-pikaframes.mp4');
         // Download the video
         execSync(`curl -sL "${videoUrl}" -o "${outputPath}"`);
         console.log(`  Video saved to: ${outputPath}`);
         return outputPath;
       }

       console.log('  No video URL in response');
       console.log('  Response:', JSON.stringify(result, null, 2).substring(0, 500));
       return '';
     } catch (err: any) {
       console.error(`  FAILED: ${err.message}`);
       return '';
     }
   }

   // --- Step 3: Extract frames from video ---
   function extractFrames(videoPath: string, outputDir: string, fps: number = 12): string[] {
     console.log(`\nExtracting frames at ${fps}fps from ${path.basename(videoPath)}...`);

     fs.mkdirSync(outputDir, { recursive: true });

     // Use ffmpeg to extract frames
     execSync(
       `ffmpeg -y -i "${videoPath}" -vf "fps=${fps}" "${outputDir}/frame_%04d.png"`,
       { stdio: 'pipe' },
     );

     const frames = fs.readdirSync(outputDir)
       .filter((f) => f.endsWith('.png'))
       .sort()
       .map((f) => path.join(outputDir, f));

     console.log(`  Extracted ${frames.length} frames`);
     return frames;
   }

   // --- Step 4: Run through pixel quantizer ---
   function runQuantizer(inputDir: string, outputDir: string): void {
     console.log(`\nRunning pixel quantizer on ${inputDir}...`);

     // Call the pixel quantizer from task 1.10
     // Adjust path to wherever the quantizer is installed
     const quantizerPath = path.join(
       process.env.HOME || '~',
       'Code-Brain/sprite-pipeline/src/tools/pixel-quantizer.ts',
     );

     execSync(
       `npx ts-node "${quantizerPath}" \
         --input "${inputDir}" \
         --output "${outputDir}" \
         --palette sean \
         --target-size 128 \
         --background-mode chroma \
         --verbose`,
       { stdio: 'inherit' },
     );
   }

   // --- Step 5: Scoring ---
   interface ScoreCard {
     model: string;
     videoGenTimeMs: number;
     framesExtracted: number;
     quantizerPassed: boolean;
     // Manual scores (fill in after review):
     walkCycleCorrectness: number; // 1-5: proper leg alternation
     characterConsistency: number; // 1-5: same character across frames
     pixelArtQuality: number;      // 1-5: clean edges after quantization
     temporalSmoothness: number;   // 1-5: no jitter in static regions
     overallScore: number;         // Weighted average
   }

   function printScoringRubric(): void {
     console.log('\n\n=== MANUAL SCORING RUBRIC ===\n');
     console.log('Review the quantized frames and score each model:');
     console.log();
     console.log('Walk Cycle Correctness (25%):');
     console.log('  1: No walking motion / random poses');
     console.log('  3: Walking motion but wrong limb order');
     console.log('  5: Perfect left-right-left alternation');
     console.log();
     console.log('Character Consistency (25%):');
     console.log('  1: Different character in each frame');
     console.log('  3: Same character, minor drift (color/proportion)');
     console.log('  5: Identical character, zero drift');
     console.log();
     console.log('Pixel Art Quality (25%):');
     console.log('  1: Blurry, anti-aliased, lost all pixel art feel');
     console.log('  3: Recognizable as pixel art, some soft edges');
     console.log('  5: Clean, crisp pixel art matching target aesthetic');
     console.log();
     console.log('Temporal Smoothness (25%):');
     console.log('  1: Heavy jitter, flickering between frames');
     console.log('  3: Some jitter in static regions');
     console.log('  5: Smooth motion, static regions are stable');
     console.log();
     console.log('Overall = (Walk×0.25 + Consistency×0.25 + PixelArt×0.25 + Temporal×0.25)');
   }

   // --- Main ---
   async function main(): Promise<void> {
     // Create all output directories
     for (const dir of [OUTPUT_BASE, KEYFRAME_DIR, VIDEO_DIR, FRAMES_DIR, QUANTIZED_DIR]) {
       fs.mkdirSync(dir, { recursive: true });
     }

     // Check for keyframes
     const keyframes = fs
       .readdirSync(KEYFRAME_DIR)
       .filter((f) => f.endsWith('.png'))
       .sort()
       .map((f) => path.join(KEYFRAME_DIR, f));

     if (keyframes.length < 2) {
       console.error(
         `ERROR: Need at least 2 keyframe PNGs in ${KEYFRAME_DIR}`,
       );
       console.error(
         'Generate them using the Gemini benchmark script from task 2.4,',
       );
       console.error(
         'or manually create walk cycle keyframes and place them there.',
       );
       process.exit(1);
     }

     console.log(`Found ${keyframes.length} keyframes in ${KEYFRAME_DIR}`);

     // --- Test Pika Pikaframes 2.2 (Priority 1) ---
     const pikaVideo = await testPikaPikaframes(keyframes);
     if (pikaVideo) {
       const pikaFramesDir = path.join(FRAMES_DIR, 'pika');
       extractFrames(pikaVideo, pikaFramesDir, 12);

       const pikaQuantizedDir = path.join(QUANTIZED_DIR, 'pika');
       try {
         runQuantizer(pikaFramesDir, pikaQuantizedDir);
         console.log(`  ✓ Pika quantized frames in: ${pikaQuantizedDir}`);
       } catch (err: any) {
         console.error(`  ✗ Quantizer failed on Pika output: ${err.message}`);
       }
     }

     // --- Kling tests would go here (Priority 2 & 3) ---
     // Similar pattern: call API, download video, extract frames, quantize
     // Uncomment and implement when you have Kling API access:
     //
     // const klingVideo = await testKling30(keyframes);
     // if (klingVideo) { ... }
     //
     // const klingMTVideo = await testKling26MotionTransfer(keyframes);
     // if (klingMTVideo) { ... }

     printScoringRubric();

     console.log('\n\nFiles to review:');
     console.log(`  Keyframes:        ${KEYFRAME_DIR}/`);
     console.log(`  Raw video:        ${VIDEO_DIR}/`);
     console.log(`  Extracted frames: ${FRAMES_DIR}/`);
     console.log(`  Quantized output: ${QUANTIZED_DIR}/`);
   }

   main().catch(console.error);
   ```

4. **Generate keyframes first**

   Before running the evaluation, you need 3-4 keyframes of a walk cycle. Use the Gemini benchmark from task 2.4 with modified prompts:

   ```bash
   # Machine: MacBook Pro
   # Place these keyframes in the video-models benchmark keyframes directory:
   # keyframe_01.png — Idle/contact pose (right foot forward, left foot back)
   # keyframe_02.png — Passing position (feet together, body lifted)
   # keyframe_03.png — Contact pose (left foot forward, right foot back)
   # keyframe_04.png — Passing position (reverse)
   ```

   Generate each with a specific pose prompt via the Gemini API, then save to `~/Code-Brain/sprite-pipeline/benchmarks/video-models/output/keyframes/`.

5. **Run the full evaluation**

   ```bash
   cd ~/Code-Brain/sprite-pipeline/benchmarks/video-models
   npm init -y
   npm install @fal-ai/client axios typescript ts-node @types/node
   FAL_KEY=your-key GOOGLE_API_KEY=your-key npx ts-node evaluation-framework.ts
   ```

6. **Score results manually**

   Open the quantized frames side-by-side and score using the rubric. Save scores:

   ```bash
   # Create a scoring file
   cat > ~/Code-Brain/sprite-pipeline/benchmarks/video-models/output/scores.json << 'EOF'
   {
     "pika_pikaframes_2.2": {
       "walk_cycle_correctness": 0,
       "character_consistency": 0,
       "pixel_art_quality": 0,
       "temporal_smoothness": 0,
       "notes": ""
     },
     "kling_3.0": {
       "walk_cycle_correctness": 0,
       "character_consistency": 0,
       "pixel_art_quality": 0,
       "temporal_smoothness": 0,
       "notes": ""
     },
     "kling_2.6_motion_transfer": {
       "walk_cycle_correctness": 0,
       "character_consistency": 0,
       "pixel_art_quality": 0,
       "temporal_smoothness": 0,
       "notes": ""
     }
   }
   EOF
   ```

**Decision Gate:** Which video model(s) produce the best raw material for the pixel quantizer?

| Outcome | Action |
|---------|--------|
| Pika wins clearly | Use Pika Pikaframes 2.2 as primary video adapter |
| Kling 3.0 wins | Use Kling 3.0 for start/end frame interpolation |
| Kling 2.6 motion transfer works | Could bypass keyframe step entirely for standard animations |
| Multiple models competitive | Build adapters for top 2, let manifest select per-animation |
| All models produce poor raw material | The hybrid pipeline may not be viable — fall back to enhanced image-only with rd-animation |

**Gotchas:**
- fal.ai has per-model pricing. Check Pika Pikaframes 2.2 cost per video before running many iterations.
- Video model APIs are asynchronous. The `fal.subscribe()` call waits for completion, which can take 30-120 seconds per video.
- ffmpeg must be installed on the MacBook Pro for frame extraction: `brew install ffmpeg`
- Kling API access may require a waitlist or business account. If unavailable, skip to Priority 1 (Pika) results.

---

### 2.7 Pixel Quantizer Integration with Video Model Output — 2h

**Depends on:** 1.10 (Pixel Quantizer built), 2.6 (Video model output available)
**Can parallel with:** Nothing — this is the integration test
**Machine:** MacBook Pro

**Steps:**

1. **Gather the best video model output from 2.6**

   ```bash
   # Machine: MacBook Pro
   # Identify which video model scored highest in task 2.6
   cat ~/Code-Brain/sprite-pipeline/benchmarks/video-models/output/scores.json

   # Copy the best model's extracted frames to a test directory
   mkdir -p ~/Code-Brain/sprite-pipeline/integration-test/input
   cp ~/Code-Brain/sprite-pipeline/benchmarks/video-models/output/extracted-frames/pika/*.png \
       ~/Code-Brain/sprite-pipeline/integration-test/input/
   ```

2. **Run the pixel quantizer on real video output**

   ```bash
   cd ~/Code-Brain/sprite-pipeline

   npx ts-node src/tools/pixel-quantizer.ts \
       --input ./integration-test/input/ \
       --output ./integration-test/output/ \
       --palette sean \
       --target-size 128 \
       --background-mode chroma \
       --outline-weight 2 \
       --verbose
   ```

   **Why:** This is the real test. Tasks 1.10 (Q-01 through Q-04) tested the quantizer with synthetic input. Now you're feeding it actual video model output — the "sludge" that video models produce.

3. **Review the validation report**

   ```bash
   cat ./integration-test/output/validation-report.json | python3 -m json.tool
   ```

   Check these specific metrics:
   - `off_palette_pixels`: Must be 0 for every frame
   - `outline_coverage`: Should be > 80%
   - `background_transparency`: Must be 100%
   - `temporal_jitter_score`: Lower is better (< 5% variance in static regions)

4. **Create before/after comparison**

   ```bash
   # Create a visual comparison directory
   mkdir -p ./integration-test/comparison

   # Use ImageMagick or Sharp to create side-by-side comparisons
   # If you have ImageMagick:
   # brew install imagemagick  (if not already installed)
   for i in $(seq -w 1 $(ls ./integration-test/input/*.png | wc -l)); do
       convert +append \
           "./integration-test/input/frame_${i}.png" \
           "./integration-test/output/frame_${i}.png" \
           "./integration-test/comparison/compare_${i}.png"
   done
   ```

   Alternatively, create a simple HTML viewer:

   ```bash
   cat > ./integration-test/comparison/viewer.html << 'HTMLEOF'
   <!DOCTYPE html>
   <html>
   <head>
       <title>Pixel Quantizer Integration Test</title>
       <style>
           body { background: #1a1a1a; color: white; font-family: monospace; }
           .frame-pair { display: inline-block; margin: 10px; text-align: center; }
           img { image-rendering: pixelated; width: 256px; height: 256px; border: 1px solid #444; }
           h3 { margin: 5px 0; }
       </style>
   </head>
   <body>
       <h1>Pixel Quantizer — Integration Test Results</h1>
       <p>Left: Raw video frame | Right: Quantized output</p>
       <div id="frames"></div>
       <script>
           // Adjust frame count based on your actual files
           for (let i = 1; i <= 12; i++) {
               const num = String(i).padStart(4, '0');
               const div = document.createElement('div');
               div.className = 'frame-pair';
               div.innerHTML = `
                   <h3>Frame ${i}</h3>
                   <img src="../input/frame_${num}.png" alt="Raw">
                   <img src="../output/frame_${num}.png" alt="Quantized">
               `;
               document.getElementById('frames').appendChild(div);
           }
       </script>
   </body>
   </html>
   HTMLEOF
   ```

   Open in browser:
   ```bash
   open ./integration-test/comparison/viewer.html
   ```

5. **Document results**

   Create `~/Code-Brain/sprite-pipeline/integration-test/RESULTS.md`:

   ```markdown
   # Hybrid Pipeline Integration Test Results

   **Date:** [today's date]
   **Video Model:** [which model was used]
   **Quantizer Version:** 1.0.0

   ## Pipeline
   Gemini keyframes → [Video Model] interpolation → Pixel Quantizer → Output

   ## Metrics
   - Frames processed: [N]
   - Off-palette pixels: [should be 0]
   - Outline coverage: [%]
   - Temporal jitter: [%]
   - Processing time per frame: [ms]

   ## Visual Assessment
   - Walk cycle correctness: [1-5]
   - Character consistency: [1-5]
   - Pixel art quality: [1-5]
   - Overall: [pass/fail]

   ## Decision
   [PASS/FAIL] — The hybrid pipeline [is/is not] viable for walk cycle generation.

   ## Next Steps
   - [ ] If PASS: Proceed to Phase 3 (pipeline integration)
   - [ ] If FAIL: Try fallback approaches from hybrid-pipeline-plan.md Section 4
   ```

**Decision Gate: This is the most important decision gate in the entire project.**

| Outcome | Action |
|---------|--------|
| **PASS** — Quantized frames look like clean pixel art with correct walk cycle | Proceed to Phase 3. The hybrid pipeline works. Integrate the best video model as an adapter. |
| **PARTIAL** — Walk cycle is correct but pixel art quality needs work | Tune quantizer thresholds (outline weight, static threshold, palette tolerance). Try at 256×256 instead of 128×128. Consider adding a Gemini restyle pass between downscale and palette quantization. |
| **FAIL on quantization** — Walk cycle is correct in raw video but quantizer destroys it | The quantizer needs more work. Investigate: is the downscale too aggressive? Is the palette too restrictive? Try the "RestyleToPixelSpec" approach from hybrid-pipeline-plan.md Section 8. |
| **FAIL on video** — Video model doesn't produce usable walk cycles regardless of quantization | The hybrid pipeline approach may not work with current video models. Check if rd-animation from task 2.5 is viable. If nothing works, invest in enhanced image-only generation with better pose references. |

**Gotchas:**
- The quantizer expects consistent frame dimensions. If the video model outputs varying sizes, add a resize step first.
- Frame numbering from ffmpeg starts at 1 (`frame_0001.png`). Make sure the quantizer handles this naming convention.
- If the video model adds a watermark, you'll need to crop or mask it before quantization.
- Save ALL intermediate artifacts (raw video, extracted frames, quantized frames, reports). You'll need these for Phase 3 tuning.

---

## Phase 1-2 Summary

### Total Time Estimates

| Phase | Task | Hours |
|-------|------|-------|
| **Phase 1** | 1.1 Mac Mini Ollama | 1.5 |
| | 1.2 Mac Mini Python/SDK | 1.0 |
| | 1.3 MacBook Pro Ollama/MLX | 2.0 |
| | 1.4 Alienware Ollama CUDA | 1.5 |
| | 1.5 Alienware ComfyUI | 2.5 |
| | 1.6 Three-Machine Networking | 1.5 |
| | 1.7 hybrid_router.py | 4.0 |
| | 1.8 Safety Hooks | 3.0 |
| | 1.9 Keychain Credential Helper | 1.0 |
| | 1.10 Pixel Quantizer | 6.0 |
| | **Phase 1 Total** | **24.0h** |
| **Phase 2** | 2.1 Process Inbox Agent | 3.0 |
| | 2.2 Spending Analysis Agent | 3.0 |
| | 2.3 Baton File Chain | 1.5 |
| | 2.4 Nano Banana Benchmark | 2.0 |
| | 2.5 rd-animation Evaluation | 2.0 |
| | 2.6 Video Model Sprint | 6.0 |
| | 2.7 Integration Test | 2.0 |
| | **Phase 2 Total** | **19.5h** |
| | **GRAND TOTAL** | **43.5h** |

### Parallelization Opportunities

**Phase 1 — Week 1 (can all start Day 1):**
- 1.1 + 1.2 on Mac Mini (sequential, ~2.5h)
- 1.3 on MacBook Pro (independent, ~2h)
- 1.4 + 1.5 on Alienware (sequential, ~4h)
- 1.10 Pixel Quantizer on MacBook Pro (independent, start after 1.3)

**Phase 1 — Week 2:**
- 1.6 Networking (needs all machines set up from Week 1)
- 1.7 hybrid_router.py (after 1.6)
- 1.8 Safety Hooks (independent of 1.6/1.7)
- 1.9 Keychain Helper (independent)

**Phase 2 — Week 3:**
- 2.1 + 2.2 + 2.3 (sequential dependency: agents → baton chain)
- 2.4 + 2.5 (fully independent, can run Day 1 of Week 3)

**Phase 2 — Week 4:**
- 2.6 Video Model Sprint (needs 1.10 complete)
- 2.7 Integration Test (needs 2.6 complete; end of week 4)

### Key Decision Gates to Track

| Gate | Task | Question | Impact |
|------|------|----------|--------|
| G1 | 1.3 | MLX 2x+ faster than Ollama? | Determines MacBook Pro inference method |
| G2 | 1.10 | Quantizer passes Q-01 through Q-04? | If NO, hybrid pipeline needs rethinking |
| G3 | 2.4 | Nano Banana 2 quality ≥ 85% of Pro? | Determines cost structure for sprite gen |
| G4 | 2.5 | rd-animation viable for standard anims? | Could bypass hybrid pipeline entirely |
| G5 | 2.6 | Best video model identified? | Determines which adapter to build first |
| G6 | 2.7 | Full hybrid pipeline viable? | **GO/NO-GO for Phase 3** |


---

# Execution Blueprint — Phases 3-5 (Weeks 5-12)

**Created:** 2026-03-27
**Author:** Sean Winslow
**Scope:** Pipeline Integration, LoRA Training, Autoresearch & Scale
**Prerequisites:** Phases 1-2 complete (three-machine infrastructure, Pixel Quantizer validated, video model selected, first agents running)

---

## PHASE 3: PIPELINE INTEGRATION + PM AGENTS (Weeks 5-6, Apr 24 - May 8)

Phase 3 wires the proven Pixel Quantizer and winning video model into the production pipeline, implements the full adapter/strategy architecture, and stands up the PM agent layer.

---

### 3.1 Generator Adapter Interface Implementation — 5h

**Depends on:** Phase 1 (Pixel Quantizer validated), Phase 2 (video model selected)
**Can parallel with:** 3.4, 3.5, 3.6 (agent tasks are fully independent)
**Machine:** MacBook Pro

This task implements the four atomic operations from the hybrid pipeline plan, the adapter pattern, and the strategy router. All code lives in the existing sprite pipeline repo.

**Steps:**

1. **Create the core TypeScript interfaces**

   Create the file `src/domain/generator-interfaces.ts`:

   ```typescript
   // src/domain/generator-interfaces.ts
   //
   // Four atomic generation operations.
   // Each adapter implements only the methods its model supports.
   // Strategy objects compose these into complete workflows.

   import { Result, SystemError } from './types.js';

   // ── Supporting Types ──────────────────────────────────────────────

   export interface FrameGenContext {
     anchor: string;                    // Path to character anchor image
     poseRef?: string;                  // Path to pose reference image
     styleRefs: string[];               // Up to 6 high-fidelity style references
     guide?: string;                    // Grid/baseline guide overlay
     prompt: string;                    // Fully resolved prompt from template system
     targetSize: { w: number; h: number };
     attemptIndex: number;
   }

   export interface KeyframeGenContext {
     anchor: string;
     poseRefs: string[];                // One pose ref per keyframe
     styleRefs: string[];
     prompts: string[];                 // One prompt per keyframe
     keyframeIndices: number[];         // Which frame positions these keyframes represent
     targetSize: { w: number; h: number };
   }

   export interface InterpolationContext {
     keyframes: GeneratedFrame[];       // 2-5 keyframe images
     motionPrompt: string;             // Text description of the motion
     duration: number;                  // Video duration in seconds
     fps: number;                       // Target frame rate for extraction
     loop: boolean;                     // Whether animation should loop
     creativityScale?: number;          // 0-1, lower = more faithful to keyframes
   }

   export interface VideoGenContext {
     characterRef: string;              // Path to character anchor
     motionRef?: string;                // Path to reference motion video
     motionPrompt: string;
     duration: number;
     fps: number;
   }

   export interface GeneratedFrame {
     path: string;
     index: number;
     metadata: Record<string, unknown>;
   }

   export interface GeneratedVideo {
     videoPath: string;
     duration: number;
     fps: number;
     resolution: { w: number; h: number };
     metadata: Record<string, unknown>;
   }

   export interface ExtractionConfig {
     targetFrameCount: number;
     fps?: number;
     frameIndices?: number[];
   }

   export interface PixelArtConfig {
     targetSize: { w: number; h: number };
     palette: string[];                  // Hex color strings
     outlineColor: string;              // Default: '#272929'
     outlineWeight: number;             // Pixels, default: 2
     backgroundStrategy: 'true_alpha' | 'chroma_key';
     chromaColor?: string;              // Default: '#00FF00'
   }

   export interface TemporalConfig {
     staticRegionThreshold: number;
     smoothingWindow: number | 'all';
     loopable: boolean;
   }

   export type ProcessedFrame = GeneratedFrame;
   export type RawFrame = GeneratedFrame;

   // ── Generator Adapter Interface ──────────────────────────────────

   export interface GeneratorAdapter {
     /** Generate a single frame from reference + pose description */
     generateFrame(ctx: FrameGenContext): Promise<Result<GeneratedFrame, SystemError>>;

     /** Generate multiple keyframes (batch optimization possible) */
     generateKeyframes?(ctx: KeyframeGenContext): Promise<Result<GeneratedFrame[], SystemError>>;

     /** Interpolate motion between anchor frames → produces video */
     interpolateFrames?(ctx: InterpolationContext): Promise<Result<GeneratedVideo, SystemError>>;

     /** Generate video from a single reference + motion description */
     generateVideo?(ctx: VideoGenContext): Promise<Result<GeneratedVideo, SystemError>>;
   }

   // ── Post-Processor Interface ─────────────────────────────────────

   export interface PostProcessor {
     /** Extract individual frames from video */
     extractFrames(video: GeneratedVideo, config: ExtractionConfig): Promise<Result<RawFrame[], SystemError>>;

     /** Apply the full pixel art quantization pipeline to a single frame */
     quantizeFrame(frame: RawFrame, config: PixelArtConfig): Promise<Result<ProcessedFrame, SystemError>>;

     /** Apply temporal smoothing across a sequence of frames */
     temporalSmooth(frames: ProcessedFrame[], config: TemporalConfig): Promise<Result<ProcessedFrame[], SystemError>>;
   }

   // ── Generation Strategy Interface ────────────────────────────────

   export interface GenerationStrategy {
     name: string;
     execute(ctx: StrategyExecutionContext): Promise<Result<ProcessedFrame[], SystemError>>;
   }

   export interface StrategyExecutionContext {
     manifest: ResolvedManifest;
     imageAdapter: GeneratorAdapter;
     videoAdapter?: GeneratorAdapter;
     postProcessor: PostProcessor;
     outputDir: string;
   }

   // ResolvedManifest is your existing manifest type extended with
   // the new generator.strategy, keyframe, interpolation, and
   // post_processing fields from hybrid-pipeline-plan Section 11.
   export interface ResolvedManifest {
     identity: {
       character: string;
       character_type: 'champion' | 'boss';
       move: string;
       version: string;
       frame_count: number;
       target_resolution: number;
     };
     inputs: {
       anchor: string;
       style_refs: string[];
       pose_refs: string[];
       guides: string[];
     };
     generator: {
       strategy: 'image_only' | 'hybrid_keyframe_video' | 'motion_transfer';
       strategy_fallback: string;
       keyframe?: {
         backend: string;
         model: string;
         keyframe_indices: number[];
         interpolation_frames: number[];
       };
       interpolation?: {
         backend: string;
         model: string;
         duration: number;
         fps: number;
         loop: boolean;
         creativity_scale: number;
         motion_prompt: string;
       };
       motion_transfer?: {
         backend: string;
         reference_video: string;
         motion_prompt: string;
       };
       prompts: Record<string, string>;
       max_attempts_per_frame: number;
     };
     post_processing?: {
       enabled: boolean;
       restyle_pass: boolean;
       quantizer: PixelArtConfig;
       temporal_smoothing: TemporalConfig;
     };
     [key: string]: unknown;
   }

   // ── Adapter Capabilities Registry ────────────────────────────────

   export interface AdapterCapabilities {
     name: string;
     type: 'image' | 'video' | 'both';
     supports: {
       generateFrame: boolean;
       generateKeyframes: boolean;
       interpolateFrames: boolean;
       generateVideo: boolean;
     };
     constraints: {
       maxKeyframes?: number;
       maxReferenceImages?: number;
       maxDuration?: number;
       supportsLoop?: boolean;
       supportsAlpha?: boolean;
       supportsSeed?: boolean;
     };
     pricing: {
       costPerGeneration?: number;
       costPerSecondVideo?: number;
     };
   }
   ```

   **Why:** These interfaces are the "ports" in the hexagonal architecture — they decouple the pipeline logic from any specific image or video model. Every adapter plugs into the same socket.

   **Verify:** `npm run build` completes with zero type errors. All existing tests still pass.

2. **Implement the GeminiAdapter**

   Create `src/adapters/gemini-adapter.ts`:

   ```typescript
   // src/adapters/gemini-adapter.ts
   import { GoogleGenAI } from '@google/genai';
   import { resolve } from 'node:path';
   import { readFile, writeFile } from 'node:fs/promises';
   import {
     GeneratorAdapter,
     FrameGenContext,
     KeyframeGenContext,
     GeneratedFrame,
     GeneratedVideo,
     InterpolationContext,
     VideoGenContext,
   } from '../domain/generator-interfaces.js';
   import { Result, SystemError } from '../domain/types.js';
   import { logger } from '../utils/logger.js';

   export class GeminiAdapter implements GeneratorAdapter {
     private client: GoogleGenAI;
     private model: string;

     constructor(apiKey: string, model: string = 'gemini-2.0-flash-exp') {
       // @google/genai v1.20.0 — NOT @google/generative-ai
       this.client = new GoogleGenAI({ apiKey });
       this.model = model;
     }

     async generateFrame(ctx: FrameGenContext): Promise<Result<GeneratedFrame, SystemError>> {
       try {
         const parts: Array<{ text: string } | { inlineData: { mimeType: string; data: string } }> = [];

         // Semantic interleaving: text label precedes each image
         parts.push({ text: 'CHARACTER ANCHOR (maintain exact identity):' });
         const anchorData = await readFile(ctx.anchor);
         parts.push({
           inlineData: { mimeType: 'image/png', data: anchorData.toString('base64') },
         });

         if (ctx.poseRef) {
           parts.push({ text: 'POSE REFERENCE (match this pose):' });
           const poseData = await readFile(ctx.poseRef);
           parts.push({
             inlineData: { mimeType: 'image/png', data: poseData.toString('base64') },
           });
         }

         for (const [i, ref] of ctx.styleRefs.entries()) {
           parts.push({ text: `STYLE REFERENCE ${i + 1}:` });
           const refData = await readFile(ref);
           parts.push({
             inlineData: { mimeType: 'image/png', data: refData.toString('base64') },
           });
         }

         parts.push({ text: ctx.prompt });

         const response = await this.client.models.generateContent({
           model: this.model,
           contents: [{ role: 'user', parts }],
           config: {
             responseModalities: ['IMAGE', 'TEXT'],
             temperature: 1.0, // Locked — values < 1.0 cause mode collapse
           },
         });

         // Extract the generated image from response
         const imagePart = response.candidates?.[0]?.content?.parts?.find(
           (p: any) => p.inlineData?.mimeType?.startsWith('image/')
         );

         if (!imagePart?.inlineData?.data) {
           return Result.err({
             code: 'SYS_GEMINI_NO_IMAGE',
             message: 'Gemini response contained no image data',
           });
         }

         const outputPath = resolve(ctx.anchor, '..', '..', 'candidates', `frame_${ctx.attemptIndex}.png`);
         await writeFile(outputPath, Buffer.from(imagePart.inlineData.data, 'base64'));

         return Result.ok({
           path: outputPath,
           index: ctx.attemptIndex,
           metadata: { model: this.model, strategy: 'image_only' },
         });
       } catch (error) {
         logger.error({ error }, 'GeminiAdapter.generateFrame failed');
         return Result.err({
           code: 'SYS_GEMINI_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }

     async generateKeyframes(ctx: KeyframeGenContext): Promise<Result<GeneratedFrame[], SystemError>> {
       // Generate keyframes sequentially — Gemini doesn't support batch image gen
       const frames: GeneratedFrame[] = [];

       for (let i = 0; i < ctx.keyframeIndices.length; i++) {
         const frameCtx: FrameGenContext = {
           anchor: ctx.anchor,
           poseRef: ctx.poseRefs[i],
           styleRefs: ctx.styleRefs,
           prompt: ctx.prompts[i],
           targetSize: ctx.targetSize,
           attemptIndex: ctx.keyframeIndices[i],
         };

         const result = await this.generateFrame(frameCtx);
         if (!result.ok) {
           return Result.err(result.error);
         }
         frames.push(result.value);

         // Rate limit: 200ms between calls to stay under quota
         await new Promise(r => setTimeout(r, 200));
       }

       return Result.ok(frames);
     }

     // GeminiAdapter does NOT support video operations
     // interpolateFrames and generateVideo remain undefined
   }
   ```

   **Why:** The GeminiAdapter wraps `@google/genai` v1.20.0, implements `generateFrame` and `generateKeyframes`, and follows the semantic interleaving pattern (text labels before images) proven in v0.1.0.

   **Verify:** Write a unit test that mocks the Google GenAI client and confirms generateFrame returns a valid Result.

3. **Implement the PikaAdapter (example video adapter)**

   Create `src/adapters/pika-adapter.ts`:

   ```typescript
   // src/adapters/pika-adapter.ts
   //
   // NOTE: This adapter is written assuming Pika wins the Phase 2 evaluation.
   // If a different video model wins, clone this pattern and swap the API calls.
   // The adapter interface ensures zero changes to the pipeline.

   import { fal } from '@fal-ai/client';
   import { readFile, writeFile } from 'node:fs/promises';
   import { resolve } from 'node:path';
   import {
     GeneratorAdapter,
     FrameGenContext,
     GeneratedFrame,
     GeneratedVideo,
     InterpolationContext,
   } from '../domain/generator-interfaces.js';
   import { Result, SystemError } from '../domain/types.js';
   import { logger } from '../utils/logger.js';

   export class PikaAdapter implements GeneratorAdapter {
     constructor() {
       // fal.ai reads FAL_KEY from environment
       // Set via: export FAL_KEY=your_key_here
     }

     async generateFrame(): Promise<Result<GeneratedFrame, SystemError>> {
       return Result.err({
         code: 'SYS_UNSUPPORTED',
         message: 'PikaAdapter does not support single frame generation. Use GeminiAdapter.',
       });
     }

     async interpolateFrames(ctx: InterpolationContext): Promise<Result<GeneratedVideo, SystemError>> {
       try {
         // Upload keyframe images to fal.ai
         const imageUrls: string[] = [];
         for (const kf of ctx.keyframes) {
           const data = await readFile(kf.path);
           const url = await fal.storage.upload(data);
           imageUrls.push(url);
         }

         logger.info(
           { keyframeCount: imageUrls.length, duration: ctx.duration },
           'Submitting to Pika Pikaframes for interpolation'
         );

         // Submit to Pika Pikaframes 2.2 via fal.ai
         const result = await fal.subscribe('fal-ai/pikaframes', {
           input: {
             images: imageUrls,
             prompt: ctx.motionPrompt,
             duration: ctx.duration,
             loop: ctx.loop,
             guidance_scale: ctx.creativityScale
               ? Math.round((1 - ctx.creativityScale) * 10 + 3) // Map 0-1 creativity to ~13-3 CFG
               : 7,
           },
           logs: true,
           onQueueUpdate: (update) => {
             if (update.status === 'IN_PROGRESS') {
               logger.debug({ logs: update.logs }, 'Pika generation in progress');
             }
           },
         });

         if (!result.data?.video?.url) {
           return Result.err({
             code: 'SYS_PIKA_NO_VIDEO',
             message: 'Pika response contained no video URL',
           });
         }

         // Download the video
         const videoResponse = await fetch(result.data.video.url);
         const videoBuffer = Buffer.from(await videoResponse.arrayBuffer());
         const outputPath = resolve('runs', 'current', 'video', 'interpolated.mp4');
         await writeFile(outputPath, videoBuffer);

         return Result.ok({
           videoPath: outputPath,
           duration: ctx.duration,
           fps: ctx.fps,
           resolution: { w: 1080, h: 1080 },
           metadata: {
             model: 'pika-pikaframes-2.2',
             provider: 'fal.ai',
             requestId: result.requestId,
           },
         });
       } catch (error) {
         logger.error({ error }, 'PikaAdapter.interpolateFrames failed');
         return Result.err({
           code: 'SYS_PIKA_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }
   }
   ```

   **Why:** The PikaAdapter wraps fal.ai's Pikaframes API, handling keyframe upload, job submission, polling, and video download. The same pattern applies to any video model — swap the API endpoint and input format.

   **Verify:** `npm run build` passes. Mock test confirms interpolateFrames maps inputs correctly.

4. **Implement the PostProcessor (wires in the Phase 1 Pixel Quantizer)**

   Create `src/core/post-processor.ts`:

   ```typescript
   // src/core/post-processor.ts
   import { execa } from 'execa';
   import { resolve, join } from 'node:path';
   import { mkdir } from 'node:fs/promises';
   import {
     PostProcessor,
     GeneratedVideo,
     ExtractionConfig,
     PixelArtConfig,
     TemporalConfig,
     RawFrame,
     ProcessedFrame,
   } from '../domain/generator-interfaces.js';
   import { Result, SystemError } from '../domain/types.js';
   import { quantizeFrame as pixelQuantize } from '../utils/pixel-quantizer.js';
   import { temporalSmooth as applyTemporalSmoothing } from '../utils/temporal-smoother.js';
   import { logger } from '../utils/logger.js';

   export class SpritePostProcessor implements PostProcessor {
     async extractFrames(
       video: GeneratedVideo,
       config: ExtractionConfig
     ): Promise<Result<RawFrame[], SystemError>> {
       try {
         const extractDir = resolve(video.videoPath, '..', '..', 'extracted');
         await mkdir(extractDir, { recursive: true });

         if (config.frameIndices && config.frameIndices.length > 0) {
           // Extract specific frame indices
           const selectExpr = config.frameIndices.map(i => `eq(n\\,${i})`).join('+');
           await execa('ffmpeg', [
             '-i', video.videoPath,
             '-vf', `select='${selectExpr}'`,
             '-vsync', 'vfr',
             join(extractDir, 'raw_frame_%03d.png'),
           ]);
         } else {
           // Extract at constant FPS then pick the best N frames
           const fps = config.fps ?? video.fps;
           await execa('ffmpeg', [
             '-i', video.videoPath,
             '-vf', `fps=${fps}`,
             join(extractDir, 'raw_frame_%03d.png'),
           ]);
         }

         // Read extracted frames
         const { globSync } = await import('node:fs');
         // Using a simple readdir + sort instead
         const { readdir } = await import('node:fs/promises');
         const files = (await readdir(extractDir))
           .filter(f => f.startsWith('raw_frame_') && f.endsWith('.png'))
           .sort();

         // Select exactly targetFrameCount frames, evenly spaced
         const selected: RawFrame[] = [];
         const step = files.length / config.targetFrameCount;
         for (let i = 0; i < config.targetFrameCount; i++) {
           const fileIndex = Math.min(Math.round(i * step), files.length - 1);
           selected.push({
             path: join(extractDir, files[fileIndex]),
             index: i,
             metadata: { sourceFrame: fileIndex, totalExtracted: files.length },
           });
         }

         logger.info(
           { extracted: files.length, selected: selected.length },
           'Frame extraction complete'
         );

         return Result.ok(selected);
       } catch (error) {
         logger.error({ error }, 'Frame extraction failed');
         return Result.err({
           code: 'DEP_FFMPEG_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }

     async quantizeFrame(
       frame: RawFrame,
       config: PixelArtConfig
     ): Promise<Result<ProcessedFrame, SystemError>> {
       try {
         // Delegates to the existing pixel-quantizer.ts from Phase 1
         const outputPath = frame.path.replace('extracted', 'quantized').replace('raw_', 'quant_');
         await pixelQuantize(frame.path, outputPath, config);

         return Result.ok({
           path: outputPath,
           index: frame.index,
           metadata: { ...frame.metadata, quantized: true },
         });
       } catch (error) {
         return Result.err({
           code: 'SYS_QUANTIZER_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }

     async temporalSmooth(
       frames: ProcessedFrame[],
       config: TemporalConfig
     ): Promise<Result<ProcessedFrame[], SystemError>> {
       try {
         const smoothed = await applyTemporalSmoothing(
           frames.map(f => f.path),
           config
         );

         return Result.ok(
           smoothed.map((path, i) => ({
             path,
             index: i,
             metadata: { ...frames[i].metadata, temporalSmoothed: true },
           }))
         );
       } catch (error) {
         return Result.err({
           code: 'SYS_TEMPORAL_SMOOTH_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }
   }
   ```

   **Why:** The PostProcessor wraps ffmpeg for frame extraction (via Execa, already in the dependency stack) and delegates quantization to the existing pixel-quantizer module from Phase 1.

   **Verify:** Unit test with a short test video confirms frame extraction produces the expected number of PNGs.

5. **Implement the three strategies and the StrategyRouter**

   Create `src/core/strategies/image-only-strategy.ts`:

   ```typescript
   // src/core/strategies/image-only-strategy.ts
   import {
     GenerationStrategy,
     StrategyExecutionContext,
     ProcessedFrame,
   } from '../../domain/generator-interfaces.js';
   import { Result, SystemError } from '../../domain/types.js';
   import { logger } from '../../utils/logger.js';

   export class ImageOnlyStrategy implements GenerationStrategy {
     name = 'image_only';

     async execute(ctx: StrategyExecutionContext): Promise<Result<ProcessedFrame[], SystemError>> {
       const { manifest, imageAdapter, outputDir } = ctx;
       const frames: ProcessedFrame[] = [];

       for (let i = 0; i < manifest.identity.frame_count; i++) {
         const poseRef = manifest.inputs.pose_refs[i % manifest.inputs.pose_refs.length];
         const prompt = manifest.generator.prompts.master
           .replace('{{frame_index}}', String(i))
           .replace('{{frame_count}}', String(manifest.identity.frame_count));

         const result = await imageAdapter.generateFrame({
           anchor: manifest.inputs.anchor,
           poseRef,
           styleRefs: manifest.inputs.style_refs,
           guide: manifest.inputs.guides[0],
           prompt,
           targetSize: {
             w: manifest.identity.target_resolution,
             h: manifest.identity.target_resolution,
           },
           attemptIndex: i,
         });

         if (!result.ok) {
           logger.error({ frame: i, error: result.error }, 'Frame generation failed');
           return Result.err(result.error);
         }

         frames.push(result.value);
         logger.info({ frame: i }, 'Frame generated (image-only)');
       }

       return Result.ok(frames);
     }
   }
   ```

   Create `src/core/strategies/hybrid-kv-strategy.ts`:

   ```typescript
   // src/core/strategies/hybrid-kv-strategy.ts
   import {
     GenerationStrategy,
     StrategyExecutionContext,
     ProcessedFrame,
   } from '../../domain/generator-interfaces.js';
   import { Result, SystemError } from '../../domain/types.js';
   import { logger } from '../../utils/logger.js';
   import { mkdir } from 'node:fs/promises';
   import { resolve } from 'node:path';

   export class HybridKVStrategy implements GenerationStrategy {
     name = 'hybrid_keyframe_video';

     async execute(ctx: StrategyExecutionContext): Promise<Result<ProcessedFrame[], SystemError>> {
       const { manifest, imageAdapter, videoAdapter, postProcessor, outputDir } = ctx;

       if (!videoAdapter?.interpolateFrames) {
         return Result.err({
           code: 'SYS_NO_VIDEO_ADAPTER',
           message: 'HybridKV strategy requires a video adapter with interpolateFrames capability',
         });
       }

       if (!manifest.generator.keyframe || !manifest.generator.interpolation) {
         return Result.err({
           code: 'SYS_MANIFEST_MISSING',
           message: 'HybridKV strategy requires keyframe and interpolation config in manifest',
         });
       }

       const kfConfig = manifest.generator.keyframe;
       const interpConfig = manifest.generator.interpolation;

       // ── Step 1: Generate keyframes with image adapter (Gemini) ──
       logger.info({ indices: kfConfig.keyframe_indices }, 'Generating keyframes via image adapter');

       if (!imageAdapter.generateKeyframes) {
         return Result.err({
           code: 'SYS_NO_KEYFRAMES',
           message: 'Image adapter does not support generateKeyframes',
         });
       }

       const prompts = kfConfig.keyframe_indices.map((idx, i) => {
         const poseRef = manifest.inputs.pose_refs[i % manifest.inputs.pose_refs.length];
         return manifest.generator.prompts.master
           .replace('{{frame_index}}', String(idx))
           .replace('{{frame_count}}', String(manifest.identity.frame_count));
       });

       const keyframeResult = await imageAdapter.generateKeyframes({
         anchor: manifest.inputs.anchor,
         poseRefs: manifest.inputs.pose_refs.slice(0, kfConfig.keyframe_indices.length),
         styleRefs: manifest.inputs.style_refs,
         prompts,
         keyframeIndices: kfConfig.keyframe_indices,
         targetSize: {
           w: manifest.identity.target_resolution,
           h: manifest.identity.target_resolution,
         },
       });

       if (!keyframeResult.ok) {
         return Result.err(keyframeResult.error);
       }

       logger.info({ count: keyframeResult.value.length }, 'Keyframes generated successfully');

       // ── Step 2: Interpolate with video adapter ──
       logger.info('Submitting keyframes for video interpolation');

       const videoResult = await videoAdapter.interpolateFrames({
         keyframes: keyframeResult.value,
         motionPrompt: interpConfig.motion_prompt,
         duration: interpConfig.duration,
         fps: interpConfig.fps,
         loop: interpConfig.loop,
         creativityScale: interpConfig.creativity_scale,
       });

       if (!videoResult.ok) {
         return Result.err(videoResult.error);
       }

       logger.info({ videoPath: videoResult.value.videoPath }, 'Video interpolation complete');

       // ── Step 3: Extract frames from video ──
       const extractResult = await postProcessor.extractFrames(videoResult.value, {
         targetFrameCount: manifest.identity.frame_count,
       });

       if (!extractResult.ok) {
         return Result.err(extractResult.error);
       }

       logger.info({ count: extractResult.value.length }, 'Frames extracted from video');

       // ── Step 4: Quantize each frame to pixel art spec ──
       const quantizedDir = resolve(outputDir, 'quantized');
       await mkdir(quantizedDir, { recursive: true });

       const quantizedFrames: ProcessedFrame[] = [];
       const quantizerConfig = manifest.post_processing?.quantizer ?? {
         targetSize: {
           w: manifest.identity.target_resolution,
           h: manifest.identity.target_resolution,
         },
         palette: [],
         outlineColor: '#272929',
         outlineWeight: 2,
         backgroundStrategy: 'chroma_key' as const,
         chromaColor: '#00FF00',
       };

       for (const rawFrame of extractResult.value) {
         const qResult = await postProcessor.quantizeFrame(rawFrame, quantizerConfig);
         if (!qResult.ok) {
           logger.warn({ frame: rawFrame.index, error: qResult.error }, 'Quantization failed for frame');
           return Result.err(qResult.error);
         }
         quantizedFrames.push(qResult.value);
       }

       logger.info({ count: quantizedFrames.length }, 'All frames quantized');

       // ── Step 5: Apply temporal smoothing ──
       const smoothConfig = manifest.post_processing?.temporal_smoothing ?? {
         staticRegionThreshold: 15,
         smoothingWindow: 'all' as const,
         loopable: true,
       };

       const smoothResult = await postProcessor.temporalSmooth(quantizedFrames, smoothConfig);

       if (!smoothResult.ok) {
         return Result.err(smoothResult.error);
       }

       logger.info('Temporal smoothing applied — frames ready for audit');

       return Result.ok(smoothResult.value);
     }
   }
   ```

   Create `src/core/strategies/motion-transfer-strategy.ts`:

   ```typescript
   // src/core/strategies/motion-transfer-strategy.ts (experimental)
   import {
     GenerationStrategy,
     StrategyExecutionContext,
     ProcessedFrame,
   } from '../../domain/generator-interfaces.js';
   import { Result, SystemError } from '../../domain/types.js';
   import { logger } from '../../utils/logger.js';

   export class MotionTransferStrategy implements GenerationStrategy {
     name = 'motion_transfer';

     async execute(ctx: StrategyExecutionContext): Promise<Result<ProcessedFrame[], SystemError>> {
       const { manifest, videoAdapter, postProcessor } = ctx;

       if (!videoAdapter?.generateVideo) {
         return Result.err({
           code: 'SYS_NO_VIDEO_ADAPTER',
           message: 'MotionTransfer strategy requires a video adapter with generateVideo',
         });
       }

       if (!manifest.generator.motion_transfer) {
         return Result.err({
           code: 'SYS_MANIFEST_MISSING',
           message: 'MotionTransfer strategy requires motion_transfer config in manifest',
         });
       }

       const mtConfig = manifest.generator.motion_transfer;

       // Step 1: Generate video from character ref + motion reference
       logger.info('Generating video via motion transfer');
       const videoResult = await videoAdapter.generateVideo({
         characterRef: manifest.inputs.anchor,
         motionRef: mtConfig.reference_video,
         motionPrompt: mtConfig.motion_prompt,
         duration: manifest.generator.interpolation?.duration ?? 2.0,
         fps: manifest.generator.interpolation?.fps ?? 24,
       });

       if (!videoResult.ok) return Result.err(videoResult.error);

       // Steps 2-4: Same post-processing as HybridKV
       const extractResult = await postProcessor.extractFrames(videoResult.value, {
         targetFrameCount: manifest.identity.frame_count,
       });
       if (!extractResult.ok) return Result.err(extractResult.error);

       const quantizerConfig = manifest.post_processing?.quantizer ?? {
         targetSize: {
           w: manifest.identity.target_resolution,
           h: manifest.identity.target_resolution,
         },
         palette: [],
         outlineColor: '#272929',
         outlineWeight: 2,
         backgroundStrategy: 'chroma_key' as const,
       };

       const quantizedFrames: ProcessedFrame[] = [];
       for (const rawFrame of extractResult.value) {
         const qResult = await postProcessor.quantizeFrame(rawFrame, quantizerConfig);
         if (!qResult.ok) return Result.err(qResult.error);
         quantizedFrames.push(qResult.value);
       }

       const smoothConfig = manifest.post_processing?.temporal_smoothing ?? {
         staticRegionThreshold: 15,
         smoothingWindow: 'all' as const,
         loopable: true,
       };

       return postProcessor.temporalSmooth(quantizedFrames, smoothConfig);
     }
   }
   ```

   Create `src/core/strategy-router.ts`:

   ```typescript
   // src/core/strategy-router.ts
   import { GenerationStrategy, ResolvedManifest } from '../domain/generator-interfaces.js';
   import { ImageOnlyStrategy } from './strategies/image-only-strategy.js';
   import { HybridKVStrategy } from './strategies/hybrid-kv-strategy.js';
   import { MotionTransferStrategy } from './strategies/motion-transfer-strategy.js';
   import { logger } from '../utils/logger.js';

   const STRATEGY_MAP: Record<string, () => GenerationStrategy> = {
     image_only: () => new ImageOnlyStrategy(),
     hybrid_keyframe_video: () => new HybridKVStrategy(),
     motion_transfer: () => new MotionTransferStrategy(),
   };

   export class StrategyRouter {
     selectStrategy(manifest: ResolvedManifest): GenerationStrategy {
       const strategyName = manifest.generator.strategy;
       const factory = STRATEGY_MAP[strategyName];

       if (!factory) {
         logger.warn(
           { requested: strategyName },
           'Unknown strategy requested, falling back to image_only'
         );
         return new ImageOnlyStrategy();
       }

       logger.info({ strategy: strategyName }, 'Strategy selected');
       return factory();
     }
   }
   ```

   **Why:** The Strategy pattern lets the manifest drive which generation approach to use per animation. Adding a new strategy requires zero changes to existing code — just add a new class and register it.

   **Verify:** `npm run build` passes. Write a test that creates a StrategyRouter, feeds it each strategy name, and asserts the correct class is returned.

6. **Install new dependencies**

   ```bash
   cd ~/Code-Brain/16BitFit/sprite-pipeline
   npm install @fal-ai/client
   # @google/genai should already be installed from Phase 1
   npm ls @google/genai  # Should show v1.20.0+
   ```

   **Why:** The fal.ai client provides Pika Pikaframes API access. `@google/genai` v1.20.0 is the current SDK (renamed from `@google/generative-ai`).

   **Verify:** `npm ls @fal-ai/client @google/genai` shows both installed.

**Decision Gate:** N/A — this is infrastructure. Verify with unit tests + type checking.

**Gotchas:**
- `@google/genai` v1.20.0 has a different API surface than the old `@google/generative-ai` package. If your existing code uses the old package, update imports.
- The fal.ai client reads `FAL_KEY` from the environment. Don't hardcode it.
- TypeScript strict mode may flag missing optional method implementations — use `?` on interface methods that not all adapters implement.

---

### 3.2 Best Video Model Wired into Hybrid Pipeline — 3h

**Depends on:** 3.1 (adapter interfaces), Phase 2 decision gate (which video model won)
**Can parallel with:** 3.4, 3.5, 3.6
**Machine:** MacBook Pro

This task takes the winning video model from Phase 2's evaluation sprint and wires its adapter into the HybridKV workflow end-to-end.

**Steps:**

1. **Confirm the Phase 2 winner and create/verify its adapter**

   Check your Phase 2 evaluation results. The adapter pattern from 3.1 means this is mostly configuration:

   ```bash
   # Review Phase 2 results
   cat runs/video-model-eval/results-summary.json
   ```

   If Pika won, the PikaAdapter from 3.1 is ready. If a different model won (Kling, Veo, Wan, LTX-2), clone the PikaAdapter pattern and swap the API calls:

   ```bash
   cp src/adapters/pika-adapter.ts src/adapters/kling-adapter.ts
   # Edit to use Kling's API instead of fal.ai
   ```

   **Why:** The adapter interface guarantees the pipeline doesn't care which video model sits behind it. A new adapter is ~100 lines of API-wrapping code.

   **Verify:** The new adapter's `interpolateFrames` method compiles and unit tests pass with mocked API responses.

2. **Wire the full HybridKV pipeline in a test script**

   Create `scripts/test-hybrid-pipeline.ts`:

   ```typescript
   // scripts/test-hybrid-pipeline.ts
   // End-to-end test of the HybridKV workflow without the full CLI
   import { GeminiAdapter } from '../src/adapters/gemini-adapter.js';
   import { PikaAdapter } from '../src/adapters/pika-adapter.js';
   import { SpritePostProcessor } from '../src/core/post-processor.js';
   import { HybridKVStrategy } from '../src/core/strategies/hybrid-kv-strategy.js';
   import { resolve } from 'node:path';
   import { readFileSync } from 'node:fs';
   import yaml from 'js-yaml';

   async function main() {
     // Load manifest
     const manifestPath = resolve('manifests/champion-sean/walk.yaml');
     const manifest = yaml.load(readFileSync(manifestPath, 'utf8')) as any;

     // Create adapters
     const gemini = new GeminiAdapter(process.env.GEMINI_API_KEY!, 'gemini-2.0-flash-exp');
     const pika = new PikaAdapter(); // Reads FAL_KEY from env
     const postProcessor = new SpritePostProcessor();
     const strategy = new HybridKVStrategy();

     const outputDir = resolve('runs', `hybrid-test-${Date.now()}`);

     console.log('Starting HybridKV pipeline test...');
     console.log(`Output directory: ${outputDir}`);

     const result = await strategy.execute({
       manifest,
       imageAdapter: gemini,
       videoAdapter: pika,
       postProcessor,
       outputDir,
     });

     if (result.ok) {
       console.log(`SUCCESS: ${result.value.length} frames produced`);
       result.value.forEach(f => console.log(`  Frame ${f.index}: ${f.path}`));
     } else {
       console.error(`FAILED: ${result.error.code} — ${result.error.message}`);
       process.exit(1);
     }
   }

   main().catch(console.error);
   ```

   Run it:
   ```bash
   GEMINI_API_KEY=your_key FAL_KEY=your_key npx tsx scripts/test-hybrid-pipeline.ts
   ```

   **Why:** This validates the full data flow: Gemini generates keyframes → video adapter interpolates → ffmpeg extracts frames → pixel quantizer processes → temporal smoother finishes.

   **Verify:** The script produces 8 quantized PNG files in `runs/hybrid-test-*/quantized/`.

3. **Verify frame extraction with ffmpeg**

   ```bash
   # Manually verify ffmpeg extracts the correct number of frames
   ffmpeg -i runs/hybrid-test-*/video/interpolated.mp4 -vf fps=24 /tmp/test_frames/frame_%03d.png
   ls /tmp/test_frames/ | wc -l
   # Should produce 48 frames for a 2-second 24fps video
   ```

   **Why:** Frame extraction is the bridge between video models and the pixel quantizer. If ffmpeg doesn't produce clean PNGs, nothing downstream works.

   **Verify:** Extracted frames are clean PNGs with no corruption. Open 3-4 in an image viewer to visually confirm.

4. **Run quantized frames through the existing auditor**

   ```bash
   # Use the pipeline's audit command on the quantized frames
   ./bin/run pipeline:audit --input runs/hybrid-test-*/quantized/ --anchor assets/anchor-characters/champion-anchor-characters/Champion-Sean-anchor.png
   ```

   **Why:** The auditor checks SSIM, palette fidelity, baseline drift, and alpha quality. This tells you whether the hybrid pipeline's output meets the same quality bar as image-only generation.

   **Verify:** Audit report shows pass rate. Expect 60-80% on first attempt (improvement comes from tuning in 3.3).

**Decision Gate:** Does the hybrid pipeline produce output that passes through the auditor with at least 50% frame acceptance? If YES → proceed to 3.3 for tuning. If NO → investigate which stage is producing failures (keyframe quality? video interpolation? quantizer settings?) and address before continuing.

**Gotchas:**
- Video model API calls can take 30-120 seconds. Set appropriate timeouts.
- If fal.ai returns 429 (rate limit), wait 60 seconds and retry once.
- Frame extraction count depends on video duration and fps — do the math: 2s × 24fps = 48 raw frames, from which you select 8 evenly spaced.

---

### 3.3 End-to-End Hybrid Test: 1 Champion Walk Cycle — 4h

**Depends on:** 3.2 (hybrid pipeline wired)
**Can parallel with:** 3.4, 3.5, 3.6
**Machine:** MacBook Pro (pipeline), Alienware (if ComfyUI needed for restyle pass)

This is the integration test — one complete walk cycle from manifest to Phaser-validated atlas.

**Steps:**

1. **Create the walk cycle manifest**

   Create `manifests/champion-sean/walk.yaml`:

   ```yaml
   # manifests/champion-sean/walk.yaml
   # Champion Sean — 8-frame walk cycle via HybridKV strategy

   identity:
     character: sean
     character_type: champion
     move: walk_forward
     version: v1
     frame_count: 8
     target_resolution: 128

   inputs:
     anchor: assets/anchor-characters/champion-anchor-characters/Champion-Sean-anchor.png
     style_refs:
       - assets/style-refs/sean-turnaround.png
     pose_refs:
       - assets/pose-refs/walk-cycle/contact-left.png
       - assets/pose-refs/walk-cycle/passing.png
       - assets/pose-refs/walk-cycle/contact-right.png
       - assets/pose-refs/walk-cycle/passing-return.png
     guides:
       - assets/guides/guide_128.png

   generator:
     strategy: hybrid_keyframe_video
     strategy_fallback: image_only

     keyframe:
       backend: gemini-flash
       model: gemini-2.0-flash-exp
       mode: edit_from_anchor
       keyframe_indices: [0, 2, 4, 6]
       interpolation_frames: [1, 3, 5, 7]

     interpolation:
       backend: pika-pikaframes  # Or whatever won Phase 2
       model: pika-2.2
       duration: 2.0
       fps: 24
       loop: true
       creativity_scale: 0.3
       motion_prompt: >
         Pixel art fighting game character performing a smooth walk cycle.
         Character walks forward (right) with natural leg alternation.
         Fixed side-view camera. Solid green (#00FF00) background.
         Bold dark outlines. No anti-aliasing, no blur, no gradients.
         Loop seamlessly from last frame back to first frame.

     prompts:
       master: >
         Generate frame {{frame_index}} of {{frame_count}} for a pixel art
         fighting game walk cycle animation. 128×128 pixels. The character
         walks forward (facing right) with natural biomechanical leg alternation.
         Bold #272929 outlines, flat cel shading, solid green #00FF00 background.
         Maintain exact character identity from the anchor image.
       negative: >
         blur, anti-aliasing, gradient, 3D rendering, realistic style,
         photographic, smooth shading, camera movement
     max_attempts_per_frame: 5
     seed_policy: random

   post_processing:
     enabled: true
     restyle_pass: false
     quantizer:
       targetSize: { w: 128, h: 128 }
       palette:
         - '#F5D6C6'   # Skin — light peach
         - '#C2A769'   # Hair — dirty blonde
         - '#4682B4'   # Eyes — steel blue
         - '#F2F0EF'   # Tank top — off white
         - '#2323FF'   # Pants — neon blue
         - '#F5F5F5'   # Shoes — white
         - '#272929'   # Outlines — bold dark
         - '#000000'   # Pure black (shadows)
         - '#FFFFFF'   # Pure white (highlights)
         - '#D4B5A5'   # Skin shadow
         - '#B89A58'   # Hair shadow
         - '#3A6B94'   # Eyes shadow
         - '#D4D2D0'   # Tank top shadow
         - '#1A1ABF'   # Pants shadow
         - '#D4D4D4'   # Shoes shadow
       outlineColor: '#272929'
       outlineWeight: 2
       backgroundStrategy: chroma_key
       chromaColor: '#00FF00'
     temporal_smoothing:
       enabled: true
       staticRegionThreshold: 15
       smoothingWindow: all
       loopable: true

   auditor:
     thresholds:
       identity_min: 0.85
       palette_min: 0.90
       alpha_artifact_max: 0.3
       baseline_drift_max: 2
       composite_min: 0.70
       temporal_jitter_max: 0.15
       frame_to_frame_ssim_min: 0.80

   retry:
     strategy_escalation:
       max_hybrid_failures: 3
     ladder:
       - action: regenerate_video
       - action: adjust_creativity
       - action: regenerate_keyframes
       - action: swap_video_model
       - action: fallback_image_only
       - action: stop

   export:
     packer_flags: "--format phaser --trim-mode Trim --extrude 1 --shape-padding 2 --border-padding 2 --disable-rotation --alpha-handling ReduceBorderArtifacts --max-size 2048 --trim-sprite-names --prepend-folder-name"
     atlas_format: phaser
   ```

   **Why:** This manifest fully specifies the walk cycle generation using the HybridKV strategy with Sean's exact palette from the character description.

   **Verify:** `./bin/run pipeline:schema --validate manifests/champion-sean/walk.yaml` passes.

2. **Run the full pipeline**

   ```bash
   ./bin/run pipeline:run --manifest manifests/champion-sean/walk.yaml --verbose
   ```

   Monitor the output for each stage:
   - `[Keyframes]` — Should generate 4 keyframes (frames 0, 2, 4, 6)
   - `[Interpolation]` — Should submit to video model and receive video
   - `[Extraction]` — Should extract frames via ffmpeg
   - `[Quantization]` — Should process each frame through pixel quantizer
   - `[Temporal Smooth]` — Should apply static region locking
   - `[Audit]` — Should run all HF/SF gates on each frame
   - `[Pack]` — Should generate atlas via TexturePacker
   - `[Validate]` — Should run Phaser headless test

   **Why:** This is the moment of truth — the full pipeline running from YAML to Phaser-validated atlas.

   **Verify:** The run completes. Check `runs/<run_id>/export/` for `atlas.png` and `atlas.json`.

3. **Inspect the output at each stage**

   ```bash
   RUN_ID=$(ls -t runs/ | head -1)

   # View keyframes
   open runs/$RUN_ID/keyframes/

   # View raw video
   open runs/$RUN_ID/video/interpolated.mp4

   # View extracted frames
   open runs/$RUN_ID/extracted/

   # View quantized frames
   open runs/$RUN_ID/quantized/

   # View final atlas
   open runs/$RUN_ID/export/atlas.png

   # Check audit report
   cat runs/$RUN_ID/audit/audit-report.json | python3 -m json.tool
   ```

   **Why:** Visual inspection at each stage catches issues that automated gates miss. The keyframes should look clean; the video should show smooth motion; the quantized frames should look like pixel art.

   **Verify:** Human assessment: does the 8-frame walk cycle look like a Street Fighter II walk animation?

4. **Run the Phaser validation**

   ```bash
   ./bin/run pipeline:validate --atlas runs/$RUN_ID/export/atlas.json
   ```

   This loads the atlas into headless Phaser, plays the animation, and checks for:
   - All 8 frames load correctly
   - No jitter at animation boundaries (frame 7 → frame 0 transition)
   - Baseline stability (sprite doesn't "ice skate")

   **Why:** Phaser is the engine truth — if it renders the animation correctly, the pipeline worked.

   **Verify:** Phaser validation passes with zero errors. Animation loops smoothly.

5. **Document results**

   ```bash
   # Create test report
   cat > runs/$RUN_ID/test-report.md << 'EOF'
   # Hybrid Pipeline E2E Test Report

   ## Configuration
   - Character: Sean (Champion, 128×128)
   - Animation: Walk Cycle (8 frames)
   - Strategy: HybridKV
   - Keyframe model: Gemini Flash
   - Video model: [WINNER FROM PHASE 2]
   - LoRA: None (pre-LoRA baseline)

   ## Results
   - Keyframes generated: 4/4
   - Video interpolation: Success/Failure
   - Frames extracted: X
   - Frames post quantization: 8
   - Audit pass rate: X/8 (XX%)
   - Phaser validation: Pass/Fail
   - Total generation cost: $X.XX
   - Total time: XXm

   ## Issues Found
   - [List any issues and their severity]

   ## Decision
   - [ ] PROCEED to Phase 4
   - [ ] INVESTIGATE [specific issue]
   EOF
   ```

   **Verify:** Report is filled out with actual results.

**Decision Gate:** Does the end-to-end test produce an acceptable walk cycle atlas that passes Phaser validation? If YES → Phase 3 pipeline work is complete, proceed to Phase 4. If NO:
- If keyframes are poor → revisit Gemini prompts/references
- If video interpolation is poor → try a different video model or adjust creativity_scale
- If quantization is poor → tune palette snap thresholds, try Gemini restyle pass
- If temporal smoothing is destroying detail → lower static_threshold from 15 to 10

**Gotchas:**
- The walk cycle MUST loop seamlessly (frame 7 → frame 0). If it doesn't, enable `loop: true` in the interpolation config and verify the video model respects it.
- Watch for "ice skating" — the feet slide instead of plant. This means baseline registration in the quantizer needs tuning.
- First runs will likely need 2-3 iterations to get quantizer settings dialed in. Budget time for this.

---

### 3.4 Sprint Health Monitor Agent — 3h

**Depends on:** 3.6 (Jira MCP setup), Phase 1 infrastructure (Mac Mini orchestrator running)
**Can parallel with:** 3.1, 3.2, 3.3, 3.5
**Machine:** Mac Mini (orchestrator) → Claude Sonnet API for Jira analysis

**Steps:**

1. **Create the agent skill file**

   Create `.claude/skills/sprint-health/SKILL.md` on Mac Mini:

   ```markdown
   # Sprint Health Monitor

   You are an autonomous sprint health analyst. No human is present.

   ## Protocol

   1. Query Jira for the current active sprint in the 16BitFit project
   2. Retrieve all issues in the sprint with their status, assignee, story points, and dates
   3. Calculate:
      - Sprint velocity (points completed vs. planned)
      - Burn-down trajectory (on track / at risk / behind)
      - Blocked issues (status = "Blocked" or has blocker links)
      - Scope creep (issues added after sprint start)
      - Carry-over risk (issues likely to not complete by sprint end)
   4. Write a structured summary to the vault daily note under the `<!-- sprint-health -->` anchor
   5. If the sprint is at risk (velocity < 70% of planned at midpoint), flag it prominently

   ## Output Format

   Write to today's daily note under `<!-- sprint-health -->`:

   ```
   ### Sprint Health — [Sprint Name]
   **Status:** 🟢 On Track / 🟡 At Risk / 🔴 Behind
   **Velocity:** X/Y points (XX%)
   **Blocked:** N issues
   **Scope Creep:** N issues added post-start
   **Carry-Over Risk:** [list of issues unlikely to complete]
   ```

   ## Decision Criteria (Autonomous)
   - If no active sprint exists, write "No active sprint found" and exit
   - If Jira is unreachable, log the error and exit gracefully
   - Never create or modify Jira issues — read only
   ```

   **Why:** The skill file defines what the agent does in autonomous mode. It uses explicit decision criteria instead of "ask the user" language.

   **Verify:** File exists at `.claude/skills/sprint-health/SKILL.md`. No interactive language present.

2. **Create the agent implementation**

   Create `agents-sdk/agents/sprint_health.py`:

   ```python
   #!/usr/bin/env python3
   """Sprint Health Monitor Agent — reads Jira sprint data, writes summary to vault."""

   import argparse
   import asyncio
   import sys
   from pathlib import Path

   # Add parent to path for lib imports
   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.skill_loader import load_skills
   from lib.vault_io import daily_note_path, inject_at_anchor
   from lib.logging_setup import setup_logger, record_run
   from lib.custom_tools import create_vault_mcp_server

   from claude_agent_sdk import ClaudeAgentOptions, query


   async def run(dry_run: bool = False):
       config = load_config()
       agent_cfg = config.agent_config("sprint_health")

       if not agent_cfg.enabled:
           print("Sprint Health Monitor is disabled in config.toml")
           return

       logger = setup_logger("sprint-health", config.log_dir)

       # Load skills
       skill_prompt = load_skills(
           agent_cfg.skills,
           config.skills_dir
       )

       # Build the autonomous preamble
       preamble = (
           "You are an autonomous agent. No human is present. "
           "Make best-judgment decisions. Write to vault files, not stdout. "
           "Today's daily note: " + str(daily_note_path(config.vault_root))
       )

       prompt = f"""{preamble}

   {skill_prompt}

   ## Task
   Run the Sprint Health Monitor protocol:
   1. Query Jira for the current active sprint
   2. Analyze sprint health metrics
   3. Write the summary to today's daily note under <!-- sprint-health -->
   """

       if dry_run:
           print("=== DRY RUN ===")
           print(prompt)
           return

       logger.info("Starting Sprint Health Monitor")

       vault_server = create_vault_mcp_server()

       options = ClaudeAgentOptions(
           system_prompt={"type": "preset", "preset": "claude_code"},
           model="claude-sonnet-4-20250514",
           max_turns=agent_cfg.max_turns or 20,
           max_budget_usd=agent_cfg.max_budget_usd or 0.30,
           permission_mode="acceptEdits",
           setting_sources=["project"],
           mcp_servers={
               "vault-tools": vault_server,
               "mcp-atlassian": {
                   "type": "stdio",
                   "command": "uvx",
                   "args": ["mcp-atlassian"],
                   "env": {
                       # Credentials pulled from macOS Keychain at runtime
                       "JIRA_URL": "https://theblock.atlassian.net",
                       "JIRA_USERNAME": "$(security find-generic-password -s 'jira-username' -w)",
                       "JIRA_API_TOKEN": "$(security find-generic-password -s 'jira-api-token' -w)",
                   }
               },
           },
           allowed_tools=[
               "Read", "Write", "Edit", "Glob", "Grep",
               "mcp__vault-tools__vault_inject",
               "mcp__mcp-atlassian__jira_search",
               "mcp__mcp-atlassian__jira_get_issue",
               "mcp__mcp-atlassian__jira_get_sprint",
               "mcp__mcp-atlassian__jira_get_board",
           ],
       )

       import time
       start = time.time()
       try:
           result = await query(prompt=prompt, options=options)
           duration_ms = int((time.time() - start) * 1000)
           cost = getattr(result, 'cost_usd', 0.0)

           record_run(
               config.log_dir, "sprint-health", "analyze",
               "success", cost, duration_ms,
               getattr(result, 'num_turns', 0),
               "Sprint health summary written"
           )
           logger.info(f"Sprint Health Monitor completed in {duration_ms}ms, cost: ${cost:.4f}")

       except Exception as e:
           duration_ms = int((time.time() - start) * 1000)
           record_run(
               config.log_dir, "sprint-health", "analyze",
               "error", 0.0, duration_ms, 0, str(e)
           )
           logger.error(f"Sprint Health Monitor failed: {e}")
           raise


   def main():
       parser = argparse.ArgumentParser(description="Sprint Health Monitor Agent")
       parser.add_argument("--dry-run", action="store_true", help="Print prompt without running")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

   **Why:** Uses the established agent pattern from daily_driver.py. Claude Sonnet provides the reasoning needed to analyze sprint health from raw Jira data.

   **Verify:** `PYTHONPATH=. python3 agents/sprint_health.py --dry-run` prints the full prompt with skills loaded.

3. **Add agent configuration to config.toml**

   ```toml
   [agents.sprint_health]
   enabled = true
   skills = ["sprint-health", "vault-read-write"]
   max_turns = 20
   max_budget_usd = 0.30
   schedule = "Mon,Thu 09:00"
   ```

   **Why:** Central configuration keeps all agent settings in one place.

   **Verify:** `python3 -c "from lib.config import load_config; c = load_config(); print(c.agent_config('sprint_health'))"` prints the config.

4. **Create the launchd schedule**

   Create `agents-sdk/schedules/com.sean.agent.sprint-health.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.sprint-health</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/sprint_health.py</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack</string>
       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
           <key>PATH</key>
           <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
       </dict>
       <key>StartCalendarInterval</key>
       <array>
           <!-- Monday 9:00 AM -->
           <dict>
               <key>Weekday</key>
               <integer>1</integer>
               <key>Hour</key>
               <integer>9</integer>
               <key>Minute</key>
               <integer>0</integer>
           </dict>
           <!-- Thursday 9:00 AM -->
           <dict>
               <key>Weekday</key>
               <integer>4</integer>
               <key>Hour</key>
               <integer>9</integer>
               <key>Minute</key>
               <integer>0</integer>
           </dict>
       </array>
       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/sprint-health-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/sprint-health-stderr.log</string>
   </dict>
   </plist>
   ```

   Install:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.sprint-health.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.sprint-health.plist
   launchctl list | grep sprint-health
   ```

   **Why:** launchd on the Mac Mini runs this reliably on Monday and Thursday mornings regardless of whether your laptop is open.

   **Verify:** `launchctl list | grep sprint-health` shows the job loaded.

**Decision Gate:** N/A — agent either runs or it doesn't. Check vault daily note after first scheduled run.

**Gotchas:**
- The Jira MCP env vars using `$(security ...)` subshells may not expand in the plist context. If they don't, create a wrapper script (`agents-sdk/scripts/run-with-keychain.sh`) that exports the credentials before running the agent. See task 3.6 for the Keychain setup.
- Claude Sonnet costs ~$0.10-0.25 per sprint analysis depending on sprint size.
- If no active sprint exists in Jira, the agent should gracefully write "No active sprint" and exit.

---

### 3.5 Meeting Defender Agent — 3h

**Depends on:** Phase 1 infrastructure (Mac Mini + phi4-mini-reasoning running, MacBook Pro available)
**Can parallel with:** 3.1, 3.2, 3.3, 3.4, 3.6
**Machine:** Mac Mini (orchestration + local pre-classification) → Claude Haiku API (synthesis)

This agent uses two-stage routing: phi4-mini-reasoning (3.8B, local on Mac Mini) handles the cheap classification pass, and Claude Haiku (API) handles the expensive natural-language synthesis of Slack draft messages.

**Steps:**

1. **Create the agent skill file**

   Create `.claude/skills/meeting-defender/SKILL.md`:

   ```markdown
   # Meeting Defender

   You are an autonomous meeting optimizer. No human is present.

   ## Protocol

   1. Read the upcoming week's calendar events from BOTH calendars:
      - sean.winslow28@gmail.com (personal)
      - swinslow@theblock.co (work — The Block)
   2. For each meeting, classify as one of:
      - ESSENTIAL: Skip. 1:1s with your manager, sprint reviews, client meetings
      - OPTIMIZABLE: Could be shorter. Meetings > 30 min with > 4 attendees and no clear agenda
      - DECLINABLE: Could skip. Informational meetings where notes would suffice, optional attendee
      - CONFLICTING: Overlapping meetings that need resolution
   3. For OPTIMIZABLE and DECLINABLE meetings, draft a Slack DM to the organizer
   4. NEVER auto-send messages. Write drafts to vault only.
   5. Write the full analysis to vault under <!-- meeting-defender -->

   ## Classification Criteria (Autonomous)
   - 1:1 with direct manager → always ESSENTIAL
   - Sprint ceremony (standup, retro, planning, review) → always ESSENTIAL
   - Meeting with "optional" in your attendee status → DECLINABLE candidate
   - Recurring meeting > 30 min with no description/agenda → OPTIMIZABLE
   - Meeting at 8 AM or after 5 PM → flag for review regardless

   ## Draft Message Templates
   For DECLINABLE: "Hey [name], I noticed I'm on [meeting]. Would it work if I caught up via the notes instead? Happy to join if there's a specific topic where you need my input."
   For OPTIMIZABLE: "Hey [name], quick thought on [meeting] — would a 25-minute timebox work for this? I find shorter meetings tend to stay focused."

   ## Output to Vault (<!-- meeting-defender -->)
   | Meeting | Day/Time | Classification | Action |
   | ... | ... | ... | Draft written / No action |
   ```

   **Verify:** File exists, no interactive language.

2. **Create the two-stage agent implementation**

   Create `agents-sdk/agents/meeting_defender.py`:

   ```python
   #!/usr/bin/env python3
   """Meeting Defender Agent — two-stage: local classification → API synthesis."""

   import argparse
   import asyncio
   import json
   import sys
   from pathlib import Path

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.skill_loader import load_skills
   from lib.vault_io import daily_note_path, inject_at_anchor
   from lib.logging_setup import setup_logger, record_run
   from lib.custom_tools import create_vault_mcp_server

   try:
       import requests
   except ImportError:
       import subprocess
       subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
       import requests

   from claude_agent_sdk import ClaudeAgentOptions, query


   # ── Stage 1: Local Classification via phi4-mini-reasoning ────────

   def classify_meetings_locally(calendar_events: list[dict]) -> list[dict]:
       """
       Use phi4-mini-reasoning (3.8B) on Mac Mini to classify meetings.
       This is the cheap, fast, local pass.
       """
       OLLAMA_URL = "http://localhost:11434"

       classifications = []
       for event in calendar_events:
           prompt = f"""Classify this calendar meeting as exactly one of:
   ESSENTIAL, OPTIMIZABLE, DECLINABLE, CONFLICTING

   Meeting: {event.get('summary', 'No title')}
   Duration: {event.get('duration_minutes', '?')} minutes
   Attendees: {event.get('attendee_count', '?')}
   Your status: {event.get('my_status', 'accepted')}
   Has agenda/description: {'Yes' if event.get('description') else 'No'}
   Recurring: {event.get('recurring', False)}
   Organizer: {event.get('organizer', 'unknown')}

   Rules:
   - 1:1 with manager = ESSENTIAL
   - Sprint ceremony = ESSENTIAL
   - Optional attendee status = DECLINABLE candidate
   - Recurring > 30 min with no description = OPTIMIZABLE
   - Overlapping with another meeting = CONFLICTING

   Respond with ONLY the classification word and a 1-sentence reason.
   Format: CLASSIFICATION: reason"""

           try:
               resp = requests.post(
                   f"{OLLAMA_URL}/api/generate",
                   json={
                       "model": "phi4-mini-reasoning",
                       "prompt": prompt,
                       "stream": False,
                       "options": {"temperature": 0.1, "num_predict": 100},
                   },
                   timeout=30,
               )
               result = resp.json().get("response", "ESSENTIAL: classification failed")

               # Parse classification
               classification = "ESSENTIAL"  # Safe default
               reason = result
               for cat in ["ESSENTIAL", "OPTIMIZABLE", "DECLINABLE", "CONFLICTING"]:
                   if cat in result.upper():
                       classification = cat
                       reason = result.split(":", 1)[-1].strip() if ":" in result else result
                       break

               classifications.append({
                   **event,
                   "classification": classification,
                   "reason": reason,
               })

           except Exception as e:
               classifications.append({
                   **event,
                   "classification": "ESSENTIAL",  # Fail safe — don't decline
                   "reason": f"Classification failed: {e}",
               })

       return classifications


   # ── Stage 2: API Synthesis via Claude Haiku ──────────────────────

   async def synthesize_recommendations(classified_meetings: list[dict], config, dry_run=False):
       """
       Use Claude Haiku (API) to draft Slack messages for actionable meetings.
       Only called for OPTIMIZABLE and DECLINABLE meetings.
       """
       actionable = [m for m in classified_meetings if m["classification"] in ("OPTIMIZABLE", "DECLINABLE")]

       if not actionable:
           return "No actionable meetings found this week."

       skill_prompt = load_skills(
           config.agent_config("meeting_defender").skills,
           config.skills_dir,
       )

       prompt = f"""{skill_prompt}

   ## Classified Meetings Requiring Action

   {json.dumps(actionable, indent=2, default=str)}

   ## Task
   For each meeting above:
   1. Draft a Slack DM to the organizer (friendly, professional tone)
   2. Use the templates from the skill file
   3. Write ALL drafts and the full meeting analysis table to today's daily note
      under the <!-- meeting-defender --> anchor

   Today's daily note: {daily_note_path(config.vault_root)}

   IMPORTANT: Write drafts to vault ONLY. Never send any messages.
   """

       if dry_run:
           print("=== Stage 2 Prompt ===")
           print(prompt)
           return

       vault_server = create_vault_mcp_server()

       options = ClaudeAgentOptions(
           system_prompt={"type": "preset", "preset": "claude_code"},
           model="claude-haiku-3-20250307",
           max_turns=15,
           max_budget_usd=0.10,
           permission_mode="acceptEdits",
           setting_sources=["project"],
           mcp_servers={"vault-tools": vault_server},
           allowed_tools=[
               "Read", "Write", "Edit",
               "mcp__vault-tools__vault_inject",
           ],
       )

       return await query(prompt=prompt, options=options)


   # ── Main ────────────────────────────────────────────────────────

   async def run(dry_run: bool = False):
       config = load_config()
       agent_cfg = config.agent_config("meeting_defender")

       if not agent_cfg.enabled:
           print("Meeting Defender is disabled in config.toml")
           return

       logger = setup_logger("meeting-defender", config.log_dir)
       logger.info("Starting Meeting Defender — Stage 1: Local classification")

       import time
       start = time.time()

       try:
           # Stage 1: Fetch calendar events (simplified — in production, use Google Calendar MCP)
           # For now, use a direct API call or MCP query
           # The full implementation would query both calendars via the google-workspace MCP
           calendar_events = fetch_upcoming_meetings()  # TODO: implement with MCP

           # Stage 1: Classify locally with phi4-mini-reasoning
           classified = classify_meetings_locally(calendar_events)
           logger.info(f"Classified {len(classified)} meetings locally")

           if dry_run:
               print(json.dumps(classified, indent=2, default=str))
               await synthesize_recommendations(classified, config, dry_run=True)
               return

           # Stage 2: Synthesize recommendations with Claude Haiku (API)
           result = await synthesize_recommendations(classified, config)

           duration_ms = int((time.time() - start) * 1000)
           cost = getattr(result, 'cost_usd', 0.0) if result else 0.0

           record_run(
               config.log_dir, "meeting-defender", "analyze",
               "success", cost, duration_ms,
               getattr(result, 'num_turns', 0) if result else 0,
               f"Classified {len(classified)} meetings, {sum(1 for m in classified if m['classification'] in ('OPTIMIZABLE', 'DECLINABLE'))} actionable"
           )
           logger.info(f"Meeting Defender completed in {duration_ms}ms")

       except Exception as e:
           duration_ms = int((time.time() - start) * 1000)
           record_run(
               config.log_dir, "meeting-defender", "analyze",
               "error", 0.0, duration_ms, 0, str(e)
           )
           logger.error(f"Meeting Defender failed: {e}")
           raise


   def fetch_upcoming_meetings() -> list[dict]:
       """
       Fetch meetings for the upcoming week from both Google Calendars.
       In the full implementation, this uses the google-workspace MCP or
       Google Calendar API. Placeholder returns empty list.
       """
       # TODO: Implement via Google Calendar MCP or direct API
       # Query both: sean.winslow28@gmail.com AND swinslow@theblock.co
       # Return list of dicts with: summary, duration_minutes, attendee_count,
       #   my_status, description, recurring, organizer, start_time
       return []


   def main():
       parser = argparse.ArgumentParser(description="Meeting Defender Agent")
       parser.add_argument("--dry-run", action="store_true")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

   **Why:** Two-stage routing saves money. Stage 1 (classification) runs on free local phi4-mini-reasoning — it just needs to categorize meetings into 4 buckets. Stage 2 (drafting Slack messages) requires natural language quality, so it uses Claude Haiku (~$0.02-0.05 per run).

   **Verify:** `PYTHONPATH=. python3 agents/meeting_defender.py --dry-run` prints both stage prompts.

3. **Add config.toml entry**

   ```toml
   [agents.meeting_defender]
   enabled = true
   skills = ["meeting-defender", "vault-read-write"]
   max_turns = 15
   max_budget_usd = 0.10
   schedule = "Sun 19:00"
   ```

4. **Create the launchd schedule**

   Create `agents-sdk/schedules/com.sean.agent.meeting-defender.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.meeting-defender</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/meeting_defender.py</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack</string>
       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
           <key>PATH</key>
           <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
       </dict>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Weekday</key>
           <integer>0</integer>
           <key>Hour</key>
           <integer>19</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/meeting-defender-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/meeting-defender-stderr.log</string>
   </dict>
   </plist>
   ```

   Install:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.meeting-defender.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.meeting-defender.plist
   launchctl list | grep meeting-defender
   ```

   **Verify:** Job appears in launchctl list.

**Gotchas:**
- phi4-mini-reasoning is 3.8B, not 14B. Make sure you pulled the correct model: `ollama pull phi4-mini-reasoning`
- Sunday 7 PM launchd uses Weekday=0 (Sunday) in Apple's convention
- Google Calendar API requires querying BOTH calendars in parallel — one calendarId per request
- The agent writes drafts to vault ONLY. Never auto-sends Slack messages. This is a safety invariant.

---

### 3.6 Jira MCP Setup with Keychain Credentials — 1.5h

**Depends on:** Phase 1 infrastructure (Mac Mini set up)
**Can parallel with:** Everything else in Phase 3
**Machine:** Mac Mini

**Steps:**

1. **Create Jira API token**

   Go to https://id.atlassian.com/manage-profile/security/api-tokens and create a new API token. Label it "Mac Mini Agent SDK".

   **Why:** API tokens are the only auth method supported by mcp-atlassian. Personal Access Tokens (PATs) are for server-based Jira, not cloud.

   **Verify:** Token is generated and copied.

2. **Store credentials in macOS Keychain**

   ```bash
   # Store Jira username
   security add-generic-password \
     -a "sean" \
     -s "jira-username" \
     -w "swinslow@theblock.co" \
     -T "" \
     /Users/seanwinslow/Library/Keychains/login.keychain-db

   # Store Jira API token
   security add-generic-password \
     -a "sean" \
     -s "jira-api-token" \
     -w "YOUR_JIRA_API_TOKEN_HERE" \
     -T "" \
     /Users/seanwinslow/Library/Keychains/login.keychain-db

   # Verify retrieval
   security find-generic-password -s "jira-username" -w
   security find-generic-password -s "jira-api-token" -w
   ```

   **Why:** macOS Keychain is more secure than `.env` files. The `block-secrets.py` hook prevents agents from reading `.env`, so Keychain is the correct credential store for autonomous agents.

   **Verify:** Both `security find-generic-password` commands return the correct values.

3. **Install mcp-atlassian**

   ```bash
   # On Mac Mini
   pip install mcp-atlassian
   # OR use uvx (runs without install)
   uvx mcp-atlassian --help
   ```

   **Why:** mcp-atlassian provides Jira and Confluence access via the MCP protocol.

   **Verify:** `uvx mcp-atlassian --help` prints usage information.

4. **Create a Keychain wrapper script for agents**

   Create `agents-sdk/scripts/run-with-keychain.sh`:

   ```bash
   #!/bin/bash
   # run-with-keychain.sh — Exports Keychain credentials before running an agent
   # Usage: ./run-with-keychain.sh python3 agents/sprint_health.py

   export JIRA_URL="https://theblock.atlassian.net"
   export JIRA_USERNAME="$(security find-generic-password -s 'jira-username' -w 2>/dev/null)"
   export JIRA_API_TOKEN="$(security find-generic-password -s 'jira-api-token' -w 2>/dev/null)"

   if [ -z "$JIRA_USERNAME" ] || [ -z "$JIRA_API_TOKEN" ]; then
       echo "ERROR: Could not retrieve Jira credentials from Keychain"
       exit 1
   fi

   exec "$@"
   ```

   ```bash
   chmod +x agents-sdk/scripts/run-with-keychain.sh
   ```

   **Why:** launchd plists can't execute subshells in env vars. This wrapper script handles Keychain retrieval and then execs the actual agent process.

   **Verify:** `./agents-sdk/scripts/run-with-keychain.sh env | grep JIRA` shows the credentials.

5. **Update launchd plists to use the wrapper**

   In `com.sean.agent.sprint-health.plist`, change ProgramArguments to:

   ```xml
   <key>ProgramArguments</key>
   <array>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/run-with-keychain.sh</string>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/sprint_health.py</string>
   </array>
   ```

   **Why:** The wrapper handles credential injection for any agent that needs Jira access.

   **Verify:** Reload the plist and check that a manual trigger works:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.sean.agent.sprint-health.plist
   launchctl load ~/Library/LaunchAgents/com.sean.agent.sprint-health.plist
   launchctl start com.sean.agent.sprint-health
   # Check logs:
   tail -f vault/90_system/agent-logs/sprint-health-stdout.log
   ```

6. **Configure the allowed_tools whitelist for Jira-connected agents**

   The Jira MCP exposes many tools. Restrict each agent to only what it needs:

   ```python
   # Sprint Health Monitor — READ ONLY
   SPRINT_HEALTH_JIRA_TOOLS = [
       "mcp__mcp-atlassian__jira_search",
       "mcp__mcp-atlassian__jira_get_issue",
       "mcp__mcp-atlassian__jira_get_sprint",
       "mcp__mcp-atlassian__jira_get_board",
   ]

   # Future: Jira Issue Creator agent — READ + WRITE
   JIRA_CREATOR_TOOLS = [
       *SPRINT_HEALTH_JIRA_TOOLS,
       "mcp__mcp-atlassian__jira_create_issue",
       "mcp__mcp-atlassian__jira_transition_issue",
   ]
   ```

   **Why:** Principle of least privilege. The Sprint Health Monitor only reads Jira — it should never be able to create or modify issues.

   **Verify:** Sprint Health agent's allowed_tools list does not include any write operations.

**Gotchas:**
- macOS Keychain access from launchd may trigger a permission prompt the first time. You may need to unlock the keychain for launchd: `security unlock-keychain -p "YOUR_LOGIN_PASSWORD" ~/Library/Keychains/login.keychain-db` (add to the wrapper script if needed).
- mcp-atlassian requires the Jira URL without a trailing slash.
- If using Confluence, add those credentials to Keychain too with service name "confluence-api-token".

---

## PHASE 4: LoRA + MEMORY LAYER (Weeks 7-8, May 8 - May 22)

Phase 4 splits into two parallel tracks: LoRA training on the Alienware (tasks 4.1-4.6) and memory/retrieval agents on the Mac Mini and MacBook Pro (tasks 4.7-4.9). The LoRA track is the critical path for Workstream C.

---

### 4.1 kohya_ss Dev Branch Installation on Alienware — 2h

**Depends on:** Phase 1 (Alienware set up with NVIDIA drivers + CUDA)
**Can parallel with:** 4.7, 4.8, 4.9 (memory agents are independent)
**Machine:** Alienware (Windows 11)

This is the most error-prone setup in the entire blueprint. Follow EXACTLY — every deviation risks hours of debugging.

**Steps:**

1. **Verify NVIDIA driver and CUDA prerequisites**

   Open PowerShell as Administrator:

   ```powershell
   # Check NVIDIA driver version (must be 570+)
   nvidia-smi

   # Check CUDA version (must be 12.8+)
   nvcc --version

   # If nvcc not found, CUDA toolkit needs installing:
   # Download from https://developer.nvidia.com/cuda-12-8-0-download-archive
   # Select: Windows → x86_64 → 11 → exe (local)
   ```

   **Why:** The RTX 5080 uses CUDA compute capability sm_120. Driver 570+ and CUDA 12.8+ are minimum requirements — older versions will silently fail or throw cryptic errors.

   **Verify:** `nvidia-smi` shows driver 570+ and CUDA 12.8+. `nvcc --version` shows 12.8.x.

2. **Clone kohya_ss and switch to dev branch**

   ```powershell
   # Use a SHORT path to avoid Windows 260-char limit
   cd C:\
   mkdir lora-training
   cd lora-training

   git clone https://github.com/bmaltais/kohya_ss.git
   cd kohya_ss
   git checkout dev
   git pull origin dev
   ```

   **Why:** The stable branch does NOT support sm_120 (Blackwell GPUs). The dev branch includes fixes for RTX 5080/5090 compatibility. The short path (`C:\lora-training\`) prevents Windows path length errors during training.

   **Verify:** `git branch` shows `* dev`. Path is `C:\lora-training\kohya_ss\`.

3. **Option A (Recommended): Use gui-uv.bat launcher**

   ```powershell
   # This bundles the correct PyTorch/CUDA versions automatically
   .\gui-uv.bat
   ```

   The launcher will:
   - Create a Python virtual environment
   - Install PyTorch with cu128 support
   - Install all kohya_ss dependencies
   - Launch the GUI at http://localhost:7860

   **Why:** gui-uv.bat is the path of least resistance — it sidesteps most version-mismatch issues by bundling tested-compatible versions of PyTorch, CUDA bindings, and Python packages.

   **Verify:** Browser opens at localhost:7860. The LoRA training tab is accessible.

4. **Option B (Manual): Set up venv + PyTorch cu128**

   If gui-uv.bat fails or you prefer CLI:

   ```powershell
   cd C:\lora-training\kohya_ss

   # Create virtual environment
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Install PyTorch STABLE with cu128 (NOT nightly — stable now supports sm_120)
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

   # CRITICAL: Do NOT install xformers
   pip uninstall xformers -y 2>$null

   # Install kohya_ss requirements
   pip install -r requirements.txt

   # Install accelerate
   pip install accelerate

   # Verify CUDA works
   python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0))"
   ```

   Expected output:
   ```
   CUDA available: True
   CUDA version: 12.8
   GPU: NVIDIA GeForce RTX 5080
   ```

   **Why:** PyTorch stable ≥2.7.0 with cu128 now supports sm_120 — nightly is no longer required. This is a critical update from the original LoRA guide which specified nightly.

   **Verify:** The three-line Python command outputs True, 12.8, and RTX 5080.

5. **Run accelerate config**

   ```powershell
   accelerate config

   # Answer the prompts:
   # - Computing environment: This machine
   # - Machine type: No distributed training
   # - GPU to use: 0
   # - Mixed precision: bf16
   ```

   **Why:** Accelerate manages distributed training and mixed precision. Single GPU + bf16 is the correct config for the RTX 5080.

   **Verify:** `accelerate config` completes without errors.

6. **Add directories to Windows Defender exclusion**

   ```powershell
   # Run as Administrator
   Add-MpPreference -ExclusionPath "C:\lora-training"
   Add-MpPreference -ExclusionPath "C:\Users\$env:USERNAME\ComfyUI"

   # Verify
   Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
   ```

   **Why:** Windows Defender actively scans every file written during training, slowing I/O by 30-50%. Excluding the training directories eliminates this bottleneck.

   **Verify:** Both paths appear in the exclusion list.

7. **Verify xformers is NOT installed**

   ```powershell
   pip list | Select-String xformers
   # Should return NOTHING
   ```

   If xformers appears:
   ```powershell
   pip uninstall xformers -y
   ```

   **Why:** xformers causes `cutlassF: no kernel found` crashes on sm_120 (Blackwell). SDPA (Scaled Dot-Product Attention, built into PyTorch) is the replacement. This is the #1 setup failure for RTX 5080 users.

   **Verify:** `pip list | Select-String xformers` returns empty.

**Decision Gate:** N/A — either the setup works or it doesn't. The PyTorch verification command is the definitive test.

**Gotchas:**
- `cutlassF: no kernel found` error = xformers is installed. Uninstall it immediately.
- Prodigy optimizer is pathologically slow on Blackwell (4.78 s/it reported on 5090). Use Adafactor. Always.
- GPU shows 100% utilization but temperature is only 40°C = driver issue. Update to latest Game Ready or Studio driver.
- bitsandbytes CUDA errors on Windows = use bitsandbytes 0.44.0+ or switch to Adafactor (which doesn't need bitsandbytes).
- Windows path length: keep EVERYTHING under `C:\lora-training\`. Never use deep nested paths.

---

### 4.2 Dataset Preparation — 3h

**Depends on:** Having 30-50 PNGs of your 16BitFit art style
**Can parallel with:** 4.1 (Alienware setup), 4.7-4.9 (memory agents)
**Machine:** MacBook Pro (image editing, captioning) → transfer to Alienware

**Steps:**

1. **Gather source images**

   Collect 30-50 PNG images that represent your 16BitFit art style. Include variety:
   - Different characters/poses
   - Different animation states
   - Different color palettes
   - Consistent style elements (bold outlines, flat shading, pixel art aesthetic)

   Place them in a working directory:
   ```bash
   mkdir -p ~/Desktop/lora-dataset/raw/
   # Copy your 16BitFit art PNGs here
   ```

   **Why:** Quality and diversity matter more than quantity. The model learns style from the visual features that are consistent across all images. Different subjects and poses force it to learn STYLE, not content.

   **Verify:** 30-50 PNGs in the raw/ directory. All are PNG format (not JPEG).

2. **Upscale to 1024px+ using nearest-neighbor ONLY**

   Create a batch upscale script:

   ```bash
   # Install Sharp CLI if not present
   npm install -g sharp-cli

   # Or use this Node.js script:
   cat > ~/Desktop/lora-dataset/upscale.mjs << 'SCRIPT'
   import sharp from 'sharp';
   import { readdir, mkdir } from 'node:fs/promises';
   import { join, basename } from 'node:path';

   const INPUT_DIR = './raw';
   const OUTPUT_DIR = './upscaled';
   const TARGET_SIZE = 1024;

   await mkdir(OUTPUT_DIR, { recursive: true });

   const files = (await readdir(INPUT_DIR)).filter(f => f.endsWith('.png'));

   for (const file of files) {
     const inputPath = join(INPUT_DIR, file);
     const outputPath = join(OUTPUT_DIR, file);

     const metadata = await sharp(inputPath).metadata();
     const shortSide = Math.min(metadata.width, metadata.height);

     if (shortSide >= TARGET_SIZE) {
       // Already large enough — just copy
       await sharp(inputPath).toFile(outputPath);
     } else {
       // Upscale with NEAREST-NEIGHBOR — critical for pixel art
       const scale = Math.ceil(TARGET_SIZE / shortSide);
       await sharp(inputPath)
         .resize(metadata.width * scale, metadata.height * scale, {
           kernel: sharp.kernel.nearest,
         })
         .toFile(outputPath);
     }

     console.log(`Upscaled: ${file} (${metadata.width}x${metadata.height} → ${metadata.width * (shortSide < TARGET_SIZE ? Math.ceil(TARGET_SIZE / shortSide) : 1)}px)`);
   }

   console.log(`\nDone: ${files.length} images upscaled to ${OUTPUT_DIR}/`);
   SCRIPT

   cd ~/Desktop/lora-dataset
   node upscale.mjs
   ```

   **Why:** SDXL/Illustrious XL trains at 1024×1024. Images smaller than this MUST be upscaled with nearest-neighbor to preserve the crisp pixel art edges. Bilinear/bicubic/Lanczos upscaling introduces anti-aliased blur that destroys pixel art — this is a fatal mistake.

   **Verify:** All images in `upscaled/` are ≥1024px on the shortest side. Open 3-4 in Preview and zoom in to confirm crisp pixel edges with no blur.

3. **Auto-caption with WD Tagger**

   Install and run WD Tagger for auto-captioning:

   ```bash
   pip install wd-tagger

   # Or use this Python script for batch captioning:
   cat > ~/Desktop/lora-dataset/caption.py << 'SCRIPT'
   #!/usr/bin/env python3
   """Batch caption images with WD Tagger, prepend trigger word."""

   import os
   import sys
   from pathlib import Path

   try:
       from wdtagger import Tagger
   except ImportError:
       # Alternative: use the HuggingFace transformers approach
       print("Installing wd-tagger...")
       os.system(f"{sys.executable} -m pip install wd-tagger")
       from wdtagger import Tagger

   TRIGGER_WORD = "16bitfit_style"
   INPUT_DIR = Path("./upscaled")
   OUTPUT_DIR = Path("./captioned")

   OUTPUT_DIR.mkdir(exist_ok=True)

   tagger = Tagger()

   for img_path in sorted(INPUT_DIR.glob("*.png")):
       # Get tags from WD Tagger
       tags = tagger.tag(str(img_path))

       # Build caption: trigger word + style keywords + content tags
       style_prefix = f"{TRIGGER_WORD}, pixel art, retro game style, bold outlines, flat shading"
       caption = f"{style_prefix}, {', '.join(tags)}"

       # Write caption file (same name, .txt extension)
       caption_path = OUTPUT_DIR / img_path.with_suffix('.txt').name
       caption_path.write_text(caption)

       # Copy image to output dir
       import shutil
       shutil.copy2(img_path, OUTPUT_DIR / img_path.name)

       print(f"Captioned: {img_path.name}")
       print(f"  → {caption[:100]}...")

   print(f"\nDone: {len(list(OUTPUT_DIR.glob('*.png')))} image/caption pairs in {OUTPUT_DIR}/")
   SCRIPT

   python3 ~/Desktop/lora-dataset/caption.py
   ```

   **Why:** WD Tagger generates tag-based captions optimized for SDXL/Illustrious. The trigger word "16bitfit_style" becomes the activation token — during inference, including this word in the prompt activates the learned style. Captioning everything that ISN'T style forces the model to learn style from visual features.

   **Verify:** Every `.png` in `captioned/` has a matching `.txt` file. Open 3-4 caption files and confirm they start with "16bitfit_style, pixel art, retro game style".

4. **Organize into kohya_ss folder structure**

   ```bash
   mkdir -p ~/Desktop/lora-dataset/training_data/10_16bitfit_style

   # Copy captioned images and captions
   cp ~/Desktop/lora-dataset/captioned/*.png ~/Desktop/lora-dataset/training_data/10_16bitfit_style/
   cp ~/Desktop/lora-dataset/captioned/*.txt ~/Desktop/lora-dataset/training_data/10_16bitfit_style/

   # Verify structure
   ls ~/Desktop/lora-dataset/training_data/10_16bitfit_style/ | head -20
   ```

   Final structure:
   ```
   training_data/
     10_16bitfit_style/
       image001.png
       image001.txt
       image002.png
       image002.txt
       ...
   ```

   **Why:** The `10_` prefix means 10 repeats per image per epoch. With 40 images × 10 repeats × 10 epochs / batch_size 1 = 4,000 total training steps.

   **Verify:** The folder contains matched .png/.txt pairs. Count: `ls *.png | wc -l` should equal `ls *.txt | wc -l`.

5. **Transfer to Alienware**

   ```bash
   # Option A: SCP over LAN
   scp -r ~/Desktop/lora-dataset/training_data/ sean@ALIENWARE_IP:C:/lora-training/

   # Option B: Google Drive (already synced on both machines)
   cp -r ~/Desktop/lora-dataset/training_data/ ~/Google\ Drive/My\ Drive/AI/lora-training/

   # Option C: USB drive
   cp -r ~/Desktop/lora-dataset/training_data/ /Volumes/USB_DRIVE/lora-training/
   ```

   **Why:** The training data needs to be on the Alienware's local SSD for fast I/O during training.

   **Verify:** On the Alienware, `dir C:\lora-training\training_data\10_16bitfit_style\` shows all files.

**Decision Gate:** N/A — dataset is ready for training.

**Gotchas:**
- JPEG compression destroys pixel art. If any source images are JPEG, convert to PNG first: `sharp input.jpg --output output.png` — but be aware the JPEG damage is already done.
- Never use bilinear/bicubic upscaling. This cannot be stressed enough. One wrong upscale contaminates the entire dataset.
- If WD Tagger doesn't install cleanly, you can manually caption the images. Use the formula: `16bitfit_style, pixel art, retro game style, [content description]`.
- Text encoder LR will be set to 0 during training (UNet only). This is correct for style LoRAs.

---

### 4.3 Download Base Model: Illustrious XL v2.0-STABLE — 0.5h

**Depends on:** 4.1 (Alienware set up)
**Can parallel with:** 4.2 (dataset prep)
**Machine:** Alienware

**Steps:**

1. **Download from HuggingFace**

   Open PowerShell on the Alienware:

   ```powershell
   # Install huggingface-cli if needed
   pip install huggingface-hub

   # Download Illustrious XL v2.0-STABLE
   # NOTE: Updated from v0.1 per validation audit — v2.0-STABLE is the current best
   huggingface-cli download OnomaAIResearch/Illustrious-XL-v2.0 --local-dir C:\lora-training\models\illustrious-xl-v2

   # The main checkpoint file is typically named something like:
   # illustrious-xl-v2.0.safetensors or diffusion_pytorch_model.safetensors
   ```

   Alternative direct download:
   ```powershell
   # If huggingface-cli doesn't work, use wget or browser
   # Go to: https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0
   # Download the .safetensors checkpoint file
   ```

   **Why:** Illustrious XL is purpose-built for 2D illustration and anime. v2.0-STABLE (not v0.1, not v3.x) is the current recommended version per the March 2026 validation audit. It delivers cleaner line work and stronger prompt adherence than base SDXL.

   **Verify:** `dir C:\lora-training\models\illustrious-xl-v2\*.safetensors` shows the checkpoint file. File size should be ~6-7 GB.

2. **Make available to both kohya_ss and ComfyUI**

   ```powershell
   # Symlink for ComfyUI (or copy if symlink doesn't work on Windows)
   # Assuming ComfyUI is at C:\Users\Sean\ComfyUI
   New-Item -ItemType SymbolicLink `
     -Path "C:\Users\$env:USERNAME\ComfyUI\models\checkpoints\illustrious-xl-v2.0.safetensors" `
     -Target "C:\lora-training\models\illustrious-xl-v2\illustrious-xl-v2.0.safetensors"

   # If symlink fails (needs admin), just copy:
   Copy-Item "C:\lora-training\models\illustrious-xl-v2\*.safetensors" `
     "C:\Users\$env:USERNAME\ComfyUI\models\checkpoints\"
   ```

   **Why:** Both kohya_ss (for training) and ComfyUI (for inference/testing) need access to the base model.

   **Verify:** The model appears in ComfyUI's checkpoint dropdown after refreshing.

**Gotchas:**
- Do NOT use Illustrious XL v0.1 (outdated) or v3.x (may have different architecture). v2.0-STABLE is the validated choice.
- The download is ~6-7 GB. Ensure sufficient disk space on the SSD.
- Windows symlinks require administrator PowerShell. If that's not available, copy the file instead.

---

### 4.4 First LoRA Training Run — 2h

**Depends on:** 4.1 (kohya_ss installed), 4.2 (dataset prepared), 4.3 (base model downloaded)
**Can parallel with:** 4.7, 4.8, 4.9
**Machine:** Alienware (Windows 11)

**Steps:**

1. **Create sample prompts for monitoring**

   Create `C:\lora-training\sample_prompts.txt`:

   ```
   16bitfit_style, pixel art, retro game style, a warrior character standing in idle pose, bold dark outlines, flat shading, transparent background
   16bitfit_style, pixel art, retro game style, a character performing a punch attack, dynamic pose, bold outlines, arcade fighter style
   16bitfit_style, pixel art, retro game style, a character walking forward, side view, clean pixel art, limited color palette
   ```

   **Why:** kohya_ss generates sample images at configured intervals using these prompts. This lets you visually monitor training progress without waiting for it to complete.

   **Verify:** File exists at `C:\lora-training\sample_prompts.txt` with 3 prompts, each starting with the trigger word.

2. **Configure the training run**

   If using the kohya_ss GUI (gui-uv.bat):

   Navigate to the LoRA training tab and set these parameters:

   | Setting | Value | Tab/Section |
   |---------|-------|-------------|
   | Pretrained model | `C:\lora-training\models\illustrious-xl-v2\illustrious-xl-v2.0.safetensors` | Model |
   | Train data dir | `C:\lora-training\training_data` | Folders |
   | Output dir | `C:\lora-training\output` | Folders |
   | Output name | `16bitfit_style_lora` | Folders |
   | Max train epochs | `10` | Training |
   | Batch size | `1` | Training |
   | Gradient accumulation | `2` | Training |
   | Gradient checkpointing | `Enabled` | Training |
   | Mixed precision | `bf16` | Training |
   | Save every N epochs | `5` | Training |
   | Network rank (dim) | `32` | Network |
   | Network alpha | `32` | Network |
   | Network type | `networks.lora` | Network |
   | Optimizer | `Adafactor` | Optimizer |
   | Learning rate | `0.0005` | Optimizer |
   | Text encoder LR | `0` | Optimizer |
   | Train UNet only | `True` | Optimizer |
   | LR scheduler | `cosine` | Optimizer |
   | Fused backward pass | `Enabled` | Advanced |
   | Cache latents | `Enabled` | Advanced |
   | Cache latents to disk | `Enabled` | Advanced |
   | Min SNR gamma | `5` | Advanced |
   | Noise offset | `0.03` | Advanced |
   | Clip skip | `1` | Advanced |
   | Sample every N epochs | `5` | Samples |
   | Sample prompts | `C:\lora-training\sample_prompts.txt` | Samples |

   If using the CLI, create `C:\lora-training\train_config.toml`:

   ```toml
   [model]
   pretrained_model_name_or_path = "C:\\lora-training\\models\\illustrious-xl-v2\\illustrious-xl-v2.0.safetensors"

   [dataset]
   train_data_dir = "C:\\lora-training\\training_data"
   resolution = "1024,1024"
   enable_bucket = true
   bucket_reso_steps = 64
   bucket_no_upscale = true
   cache_latents = true
   cache_latents_to_disk = true

   [training]
   output_dir = "C:\\lora-training\\output"
   output_name = "16bitfit_style_lora"
   max_train_epochs = 10
   train_batch_size = 1
   gradient_accumulation_steps = 2
   gradient_checkpointing = true
   mixed_precision = "bf16"
   save_every_n_epochs = 5
   sample_every_n_epochs = 5
   sample_prompts = "C:\\lora-training\\sample_prompts.txt"

   [network]
   network_module = "networks.lora"
   network_dim = 32
   network_alpha = 32
   network_train_unet_only = true

   [optimizer]
   optimizer_type = "Adafactor"
   learning_rate = 0.0005
   text_encoder_lr = 0.0
   lr_scheduler = "cosine"
   fused_backward_pass = true

   [advanced]
   min_snr_gamma = 5
   noise_offset = 0.03
   clip_skip = 1
   ```

   Run via CLI:
   ```powershell
   cd C:\lora-training\kohya_ss
   .\venv\Scripts\Activate.ps1

   accelerate launch --mixed_precision=bf16 train_network.py `
     --config_file "C:\lora-training\train_config.toml"
   ```

   **Why:** Every parameter is chosen specifically for the RTX 5080's 16GB VRAM constraint. Adafactor + fused backward pass reduces VRAM to ~10GB. bf16 is native on Blackwell. Batch 1 + grad accum 2 simulates batch 2 within VRAM limits.

   **Verify:** Training starts without CUDA OOM errors. GPU utilization shows 80-100% and temperature reaches 70°C+.

3. **Monitor training**

   Watch for these signs during training:

   ```
   ✅ GOOD: Loss starts ~0.12-0.15, decreases gradually to ~0.08-0.10
   ✅ GOOD: GPU temp 65-80°C, utilization 80-100%
   ✅ GOOD: ~1-3 seconds per iteration

   ❌ BAD: Loss stuck above 0.15 after 100 steps → LR too low
   ❌ BAD: Loss drops below 0.05 → overfitting, stop early
   ❌ BAD: Loss spikes suddenly → LR too high
   ❌ BAD: GPU 100% but temp only 40°C → driver issue
   ❌ BAD: >5 seconds per iteration → Prodigy or xformers problem
   ```

   **Why:** Training loss is your primary signal. The sample images generated every 5 epochs give visual confirmation.

   **Verify:** Training completes in 30-90 minutes. Output directory contains epoch checkpoint files.

4. **Check output files**

   ```powershell
   dir C:\lora-training\output\

   # Expected:
   # 16bitfit_style_lora-000005.safetensors   (epoch 5 checkpoint)
   # 16bitfit_style_lora-000010.safetensors   (epoch 10 / final)
   # sample/                                  (sample images from each checkpoint)
   ```

   **Why:** You save at epochs 5 and 10 to compare — the best checkpoint may not be the last one (overfitting risk).

   **Verify:** Two .safetensors files exist. Sample images show recognizable style transfer.

**VRAM Troubleshooting Ladder** (if you hit OOM errors, apply in order):

| Step | Action | Expected VRAM |
|------|--------|---------------|
| 1 | Verify fused_backward_pass is ON + Adafactor | ~10 GB |
| 2 | Reduce resolution from 1024 to 768 | ~8 GB |
| 3 | Reduce network_dim from 32 to 16 | ~9 GB |
| 4 | Enable cache_latents_to_disk | ~9.5 GB |
| 5 | Last resort: optimizer_groups=8 | ~14 GB |

**Decision Gate:** Review sample outputs at epochs 5 and 10. Is the trigger word ("16bitfit_style") producing recognizable style transfer? Signs of overfitting (reproduced training poses) or underfitting (output barely differs from base model)?

**Gotchas:**
- The Prodigy optimizer is pathologically slow on Blackwell. If you accidentally select it, training will crawl at 4-5 s/it. Switch to Adafactor immediately.
- If you see `cutlassF: no kernel found`, xformers snuck back in. Uninstall it.
- Training time varies: 40 images × 10 repeats × 10 epochs = 4,000 steps. At 1-2 s/step = 70-130 minutes.
- Don't panic if epoch 5 samples look rough. Style LoRAs often need the full 10 epochs to converge.

---

### 4.5 LoRA Testing in ComfyUI — 1.5h

**Depends on:** 4.4 (first training run complete)
**Can parallel with:** 4.7, 4.8, 4.9
**Machine:** Alienware

**Steps:**

1. **Copy LoRA files to ComfyUI**

   ```powershell
   Copy-Item "C:\lora-training\output\*.safetensors" `
     "C:\Users\$env:USERNAME\ComfyUI\models\loras\"

   # Restart ComfyUI or click "Refresh" in the model dropdown
   ```

   **Why:** ComfyUI looks for LoRA files in its `models/loras/` directory.

   **Verify:** Both epoch 5 and epoch 10 checkpoints appear in ComfyUI's LoRA dropdown.

2. **Test basic LoRA workflow**

   Build this workflow in ComfyUI (either via the GUI or by importing the JSON below):

   ```
   Node connections:
   [Load Checkpoint: illustrious-xl-v2.0.safetensors]
       → model output → [Load LoRA: 16bitfit_style_lora-000010.safetensors, strength: 0.8]
           → model output → [KSampler]
       → clip output  → [Load LoRA] → clip output → [CLIP Text Encode (Positive)]
                                                    → [CLIP Text Encode (Negative)]

   [CLIP Text Encode Positive]: "16bitfit_style, pixel art, retro game style, a warrior character standing in idle pose, bold dark outlines, flat shading, transparent background"
   [CLIP Text Encode Negative]: "blur, anti-aliasing, gradient, 3D, photorealistic, smooth shading"

   [KSampler]:
     - seed: 42 (fixed for comparison)
     - steps: 25
     - cfg: 7
     - sampler: euler
     - scheduler: normal
     - denoise: 1.0

   [KSampler] → [VAE Decode] → [Save Image]
   ```

   Click "Queue Prompt" to generate.

   **Why:** This is the simplest possible LoRA test — load the base model, apply your LoRA, and generate. If the trigger word activates the style, the LoRA is working.

   **Verify:** Generated image shows visible style influence from your training data. Compare with generating the same prompt WITHOUT the LoRA loaded.

3. **Run X/Y/Z plot to find the sweet spot**

   Install the ComfyUI Efficiency Nodes if not already present:
   ```
   ComfyUI Manager → Install Custom Nodes → Search "Efficiency Nodes"
   ```

   Create an X/Y/Z plot workflow:

   ```
   X axis: LoRA checkpoint (epoch 5 vs epoch 10)
   Y axis: LoRA strength (0.5, 0.7, 0.8, 0.9, 1.0)

   This generates a 2×5 grid comparing both checkpoints at different strengths.
   Use the same seed (42) and prompt for all generations.
   ```

   Configuration for the XY Plot node:
   - X: LoRA file names → `16bitfit_style_lora-000005.safetensors, 16bitfit_style_lora-000010.safetensors`
   - Y: LoRA strength values → `0.5, 0.7, 0.8, 0.9, 1.0`
   - Fixed seed: 42
   - Prompt: `16bitfit_style, pixel art, retro game style, a warrior character in fighting stance, bold outlines`

   **Why:** The X/Y/Z plot systematically finds the best checkpoint + strength combination. Overfitting shows as artifacts at high strengths; underfitting shows as minimal style change at low strengths. The sweet spot is typically 0.7-0.9 strength on the best checkpoint.

   **Verify:** Save the grid image. Visually identify which cell has the best style transfer without artifacts.

4. **Record the sweet spot**

   ```
   Best checkpoint: epoch [5 or 10]
   Best strength: [0.5-1.0]
   Notes: [any observations about artifacts, quality, etc.]
   ```

   **Why:** These values will be used in the pipeline integration (4.6) and the autoresearch optimization (Phase 5).

   **Verify:** Sweet spot documented. You have a clear winner.

**Decision Gate:** Does the LoRA meaningfully improve sprite generation quality vs. prompting alone? Compare LoRA output against baseline (same prompt, no LoRA). If YES → proceed to integration. If NO:
- If underfitting → train for more epochs (15-20) or increase LR to 0.001
- If overfitting → use the epoch 5 checkpoint or reduce network_dim to 16
- If style is wrong → review dataset. Are all images truly representative of the target style?

**Gotchas:**
- LoRA strength 1.0+ can cause artifacts. If epoch 10 looks great at 0.7 but breaks at 1.0, the training is slightly overfit — use 0.7-0.8.
- Make sure you include the trigger word "16bitfit_style" in every prompt. Without it, the LoRA has minimal effect.
- ComfyUI v0.18.2 has a built-in NanoBanana2 API node — this will be useful later for combining LoRA-enhanced local generation with Gemini cloud generation.

---

### 4.6 LoRA Integration into Pipeline — 2h

**Depends on:** 4.5 (sweet spot identified)
**Can parallel with:** 4.7, 4.8, 4.9
**Machine:** MacBook Pro (code), Alienware (ComfyUI server)

**Steps:**

1. **Create the ComfyUI adapter for the sprite pipeline**

   Create `src/adapters/comfyui-adapter.ts`:

   ```typescript
   // src/adapters/comfyui-adapter.ts
   //
   // Wraps ComfyUI's REST API for LoRA-enhanced sprite generation.
   // ComfyUI runs on the Alienware at http://ALIENWARE_IP:8188
   // This adapter runs in the pipeline on the MacBook Pro.

   import {
     GeneratorAdapter,
     FrameGenContext,
     GeneratedFrame,
   } from '../domain/generator-interfaces.js';
   import { Result, SystemError } from '../domain/types.js';
   import { logger } from '../utils/logger.js';
   import { writeFile, readFile, mkdir } from 'node:fs/promises';
   import { resolve, join } from 'node:path';
   import { randomUUID } from 'node:crypto';

   interface ComfyUIConfig {
     host: string;              // e.g., 'http://192.168.1.X:8188'
     checkpoint: string;        // e.g., 'illustrious-xl-v2.0.safetensors'
     loraFile: string;          // e.g., '16bitfit_style_lora-000010.safetensors'
     loraStrength: number;      // e.g., 0.8
     sampler: string;           // e.g., 'euler'
     steps: number;             // e.g., 25
     cfg: number;               // e.g., 7
   }

   export class ComfyUIAdapter implements GeneratorAdapter {
     private config: ComfyUIConfig;
     private clientId: string;

     constructor(config: ComfyUIConfig) {
       this.config = config;
       this.clientId = randomUUID();
     }

     async generateFrame(ctx: FrameGenContext): Promise<Result<GeneratedFrame, SystemError>> {
       try {
         // Build the ComfyUI workflow JSON programmatically
         const workflow = this.buildWorkflow(ctx);

         // Submit to ComfyUI API
         const response = await fetch(`${this.config.host}/prompt`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
             prompt: workflow,
             client_id: this.clientId,
           }),
         });

         if (!response.ok) {
           return Result.err({
             code: 'SYS_COMFYUI_SUBMIT_ERROR',
             message: `ComfyUI returned ${response.status}: ${await response.text()}`,
           });
         }

         const { prompt_id } = await response.json();
         logger.info({ promptId: prompt_id }, 'ComfyUI job submitted');

         // Poll for completion
         const result = await this.waitForCompletion(prompt_id);
         if (!result) {
           return Result.err({
             code: 'SYS_COMFYUI_TIMEOUT',
             message: 'ComfyUI generation timed out after 120 seconds',
           });
         }

         // Download the generated image
         const imageInfo = result.outputs?.SaveImage?.images?.[0];
         if (!imageInfo) {
           return Result.err({
             code: 'SYS_COMFYUI_NO_OUTPUT',
             message: 'ComfyUI completed but produced no image',
           });
         }

         const imageUrl = `${this.config.host}/view?filename=${imageInfo.filename}&subfolder=${imageInfo.subfolder || ''}&type=${imageInfo.type || 'output'}`;
         const imageResp = await fetch(imageUrl);
         const imageBuffer = Buffer.from(await imageResp.arrayBuffer());

         const outputPath = resolve('runs', 'current', 'candidates', `comfyui_frame_${ctx.attemptIndex}.png`);
         await mkdir(resolve(outputPath, '..'), { recursive: true });
         await writeFile(outputPath, imageBuffer);

         return Result.ok({
           path: outputPath,
           index: ctx.attemptIndex,
           metadata: {
             model: 'comfyui-illustrious-xl-v2',
             lora: this.config.loraFile,
             loraStrength: this.config.loraStrength,
           },
         });
       } catch (error) {
         logger.error({ error }, 'ComfyUIAdapter.generateFrame failed');
         return Result.err({
           code: 'SYS_COMFYUI_ERROR',
           message: error instanceof Error ? error.message : String(error),
         });
       }
     }

     private buildWorkflow(ctx: FrameGenContext): Record<string, any> {
       // ComfyUI API format workflow JSON
       return {
         '1': {
           class_type: 'CheckpointLoaderSimple',
           inputs: { ckpt_name: this.config.checkpoint },
         },
         '2': {
           class_type: 'LoraLoader',
           inputs: {
             model: ['1', 0],
             clip: ['1', 1],
             lora_name: this.config.loraFile,
             strength_model: this.config.loraStrength,
             strength_clip: this.config.loraStrength,
           },
         },
         '3': {
           class_type: 'CLIPTextEncode',
           inputs: {
             text: ctx.prompt,
             clip: ['2', 1],
           },
         },
         '4': {
           class_type: 'CLIPTextEncode',
           inputs: {
             text: 'blur, anti-aliasing, gradient, 3D, photorealistic, smooth shading, camera movement',
             clip: ['2', 1],
           },
         },
         '5': {
           class_type: 'EmptyLatentImage',
           inputs: {
             width: ctx.targetSize.w >= 512 ? ctx.targetSize.w : 1024,
             height: ctx.targetSize.h >= 512 ? ctx.targetSize.h : 1024,
             batch_size: 1,
           },
         },
         '6': {
           class_type: 'KSampler',
           inputs: {
             model: ['2', 0],
             positive: ['3', 0],
             negative: ['4', 0],
             latent_image: ['5', 0],
             seed: Math.floor(Math.random() * 2 ** 32),
             steps: this.config.steps,
             cfg: this.config.cfg,
             sampler_name: this.config.sampler,
             scheduler: 'normal',
             denoise: 1.0,
           },
         },
         '7': {
           class_type: 'VAEDecode',
           inputs: {
             samples: ['6', 0],
             vae: ['1', 2],
           },
         },
         '8': {
           class_type: 'SaveImage',
           inputs: {
             images: ['7', 0],
             filename_prefix: `sprite_${ctx.attemptIndex}`,
           },
         },
       };
     }

     private async waitForCompletion(promptId: string, timeoutMs = 120_000): Promise<any | null> {
       const start = Date.now();
       while (Date.now() - start < timeoutMs) {
         const resp = await fetch(`${this.config.host}/history/${promptId}`);
         const history = await resp.json();

         if (history[promptId]?.status?.completed) {
           return history[promptId];
         }

         if (history[promptId]?.status?.status_str === 'error') {
           logger.error({ promptId }, 'ComfyUI generation failed');
           return null;
         }

         await new Promise(r => setTimeout(r, 2000)); // Poll every 2 seconds
       }

       return null; // Timeout
     }
   }
   ```

   **Why:** The ComfyUI adapter calls the Alienware's ComfyUI REST API from the pipeline running on the MacBook Pro. The LoRA, checkpoint, and sampler settings are all configurable per manifest.

   **Verify:** `npm run build` passes.

2. **Add ComfyUI config to the manifest schema**

   Extend the manifest to support ComfyUI-based generation:

   ```yaml
   # In manifests/champion-sean/idle.yaml (example using ComfyUI + LoRA)
   generator:
     strategy: image_only
     keyframe:
       backend: comfyui
       model: illustrious-xl-v2.0
       comfyui:
         host: "http://192.168.1.X:8188"     # Alienware's IP
         checkpoint: "illustrious-xl-v2.0.safetensors"
         lora_file: "16bitfit_style_lora-000010.safetensors"
         lora_strength: 0.8                   # From 4.5 sweet spot
         sampler: "euler"
         steps: 25
         cfg: 7
   ```

   **Why:** LoRA-enhanced generation becomes just another adapter option in the manifest. The pipeline doesn't need to know whether frames come from Gemini, ComfyUI, or any future generator.

   **Verify:** The manifest loads and validates correctly.

3. **Test with and without LoRA**

   ```bash
   # Generate a sprite WITH LoRA
   ./bin/run pipeline:run --manifest manifests/champion-sean/idle-lora.yaml

   # Generate the same sprite WITHOUT LoRA (Gemini only)
   ./bin/run pipeline:run --manifest manifests/champion-sean/idle-gemini.yaml

   # Compare outputs side by side
   open runs/*/export/atlas.png
   ```

   **Why:** This A/B test confirms the LoRA adds measurable style improvement over prompting alone.

   **Verify:** Visual comparison shows the LoRA version has more consistent style elements (outlines, palette, shading).

**Decision Gate:** Does the LoRA meaningfully improve sprite quality vs. Gemini-only? Document the comparison.

**Gotchas:**
- ComfyUI must be running on the Alienware for this to work. Start it with: `python main.py --listen 0.0.0.0 --port 8188`
- The Alienware's firewall must allow port 8188 from the MacBook's IP. Configure Windows Firewall: `netsh advfirewall firewall add rule name="ComfyUI" dir=in action=allow protocol=TCP localport=8188`
- If ComfyUI returns 504 (timeout), the generation is taking too long. Reduce steps from 25 to 20.

---

### 4.7 Vault Embedding Indexer Agent — 2.5h

**Depends on:** Phase 1 infrastructure (Mac Mini + nomic-embed-text running)
**Can parallel with:** 4.1-4.6 (entire LoRA track), 4.8, 4.9
**Machine:** Mac Mini (nightly, 100% local)

**Steps:**

1. **Create the SQLite schema for embeddings**

   Create `agents-sdk/lib/embedding_store.py`:

   ```python
   """Local SQLite vector store for vault note embeddings."""

   import sqlite3
   import json
   import hashlib
   from pathlib import Path
   from datetime import datetime

   DB_PATH = Path("vault/90_system/embeddings/vault_embeddings.db")


   def init_db():
       """Create the embeddings database and tables if they don't exist."""
       DB_PATH.parent.mkdir(parents=True, exist_ok=True)
       conn = sqlite3.connect(str(DB_PATH))
       conn.execute("""
           CREATE TABLE IF NOT EXISTS embeddings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               note_path TEXT NOT NULL UNIQUE,
               content_hash TEXT NOT NULL,
               embedding BLOB NOT NULL,       -- JSON-encoded float array
               title TEXT,
               tags TEXT,                      -- JSON array of tags
               modified_at TEXT NOT NULL,      -- ISO 8601
               indexed_at TEXT NOT NULL,       -- ISO 8601
               chunk_index INTEGER DEFAULT 0,  -- For multi-chunk notes
               chunk_text TEXT                 -- The text that was embedded
           )
       """)
       conn.execute("""
           CREATE INDEX IF NOT EXISTS idx_note_path ON embeddings(note_path)
       """)
       conn.execute("""
           CREATE INDEX IF NOT EXISTS idx_content_hash ON embeddings(content_hash)
       """)
       conn.commit()
       conn.close()


   def get_connection():
       init_db()
       return sqlite3.connect(str(DB_PATH))


   def needs_update(conn: sqlite3.Connection, note_path: str, content_hash: str) -> bool:
       """Check if a note needs re-embedding (content changed)."""
       cursor = conn.execute(
           "SELECT content_hash FROM embeddings WHERE note_path = ?",
           (note_path,)
       )
       row = cursor.fetchone()
       if row is None:
           return True  # New note
       return row[0] != content_hash  # Content changed


   def store_embedding(
       conn: sqlite3.Connection,
       note_path: str,
       content_hash: str,
       embedding: list[float],
       title: str,
       tags: list[str],
       modified_at: str,
       chunk_index: int = 0,
       chunk_text: str = "",
   ):
       """Store or update an embedding for a vault note."""
       conn.execute("""
           INSERT INTO embeddings (note_path, content_hash, embedding, title, tags, modified_at, indexed_at, chunk_index, chunk_text)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(note_path) DO UPDATE SET
               content_hash = excluded.content_hash,
               embedding = excluded.embedding,
               title = excluded.title,
               tags = excluded.tags,
               modified_at = excluded.modified_at,
               indexed_at = excluded.indexed_at,
               chunk_text = excluded.chunk_text
       """, (
           note_path,
           content_hash,
           json.dumps(embedding),
           title,
           json.dumps(tags),
           modified_at,
           datetime.now().isoformat(),
           chunk_index,
           chunk_text,
       ))


   def search_similar(query_embedding: list[float], top_k: int = 10) -> list[dict]:
       """Find the top-K most similar notes using cosine similarity."""
       conn = get_connection()
       cursor = conn.execute("SELECT note_path, embedding, title, tags FROM embeddings")

       import math
       results = []
       for row in cursor:
           stored_emb = json.loads(row[1])
           # Cosine similarity
           dot = sum(a * b for a, b in zip(query_embedding, stored_emb))
           norm_q = math.sqrt(sum(a * a for a in query_embedding))
           norm_s = math.sqrt(sum(a * a for a in stored_emb))
           similarity = dot / (norm_q * norm_s) if norm_q * norm_s > 0 else 0

           results.append({
               "note_path": row[0],
               "title": row[2],
               "tags": json.loads(row[3]),
               "similarity": similarity,
           })

       conn.close()
       results.sort(key=lambda x: x["similarity"], reverse=True)
       return results[:top_k]


   def content_hash(text: str) -> str:
       return hashlib.sha256(text.encode()).hexdigest()[:16]
   ```

   **Why:** SQLite is lightweight, requires no external database server, and the cosine similarity search is fast enough for ~1,500 notes. This gives every future agent semantic search over the entire vault at zero API cost.

   **Verify:** `python3 -c "from lib.embedding_store import init_db; init_db(); print('DB created')"` creates the database file.

2. **Create the embedding indexer agent**

   Create `agents-sdk/agents/vault_indexer.py`:

   ```python
   #!/usr/bin/env python3
   """Vault Embedding Indexer — nightly job that embeds modified notes into SQLite."""

   import asyncio
   import sys
   import time
   import json
   import hashlib
   from pathlib import Path
   from datetime import datetime

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.logging_setup import setup_logger, record_run
   from lib.embedding_store import (
       get_connection, needs_update, store_embedding, content_hash
   )

   try:
       import requests
   except ImportError:
       import subprocess
       subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
       import requests

   OLLAMA_URL = "http://localhost:11434"
   EMBED_MODEL = "nomic-embed-text"


   def get_embedding(text: str) -> list[float]:
       """Get embedding from nomic-embed-text via local Ollama."""
       resp = requests.post(
           f"{OLLAMA_URL}/api/embeddings",
           json={"model": EMBED_MODEL, "prompt": text},
           timeout=30,
       )
       resp.raise_for_status()
       return resp.json()["embedding"]


   def extract_frontmatter(content: str) -> dict:
       """Extract YAML frontmatter from a markdown note."""
       if not content.startswith("---"):
           return {}
       try:
           end = content.index("---", 3)
           import yaml
           return yaml.safe_load(content[3:end]) or {}
       except (ValueError, Exception):
           return {}


   def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
       """Split text into chunks for embedding (nomic-embed-text has 8192 token limit)."""
       if len(text) <= max_chars:
           return [text]

       chunks = []
       paragraphs = text.split("\n\n")
       current_chunk = ""

       for para in paragraphs:
           if len(current_chunk) + len(para) > max_chars:
               if current_chunk:
                   chunks.append(current_chunk.strip())
               current_chunk = para
           else:
               current_chunk += "\n\n" + para

       if current_chunk.strip():
           chunks.append(current_chunk.strip())

       return chunks or [text[:max_chars]]


   async def run():
       config = load_config()
       logger = setup_logger("vault-indexer", config.log_dir)
       start = time.time()

       vault_root = Path(config.vault_root)
       notes = list(vault_root.rglob("*.md"))

       logger.info(f"Found {len(notes)} markdown files in vault")

       conn = get_connection()
       updated = 0
       skipped = 0
       errors = 0

       for note_path in notes:
           try:
               # Skip system files
               rel_path = str(note_path.relative_to(vault_root))
               if rel_path.startswith("90_system/") or rel_path.startswith("."):
                   skipped += 1
                   continue

               content = note_path.read_text(encoding="utf-8", errors="replace")
               c_hash = content_hash(content)

               # Skip if content hasn't changed
               if not needs_update(conn, rel_path, c_hash):
                   skipped += 1
                   continue

               # Extract metadata
               fm = extract_frontmatter(content)
               title = fm.get("title", note_path.stem)
               tags = fm.get("tags", [])
               if isinstance(tags, str):
                   tags = [tags]

               # Strip frontmatter for embedding
               text_body = content
               if content.startswith("---"):
                   try:
                       end = content.index("---", 3)
                       text_body = content[end + 3:].strip()
                   except ValueError:
                       pass

               # Chunk and embed
               chunks = chunk_text(text_body)
               for i, chunk in enumerate(chunks):
                   embedding = get_embedding(f"{title}\n\n{chunk}")
                   store_embedding(
                       conn, rel_path, c_hash, embedding,
                       title, tags,
                       datetime.fromtimestamp(note_path.stat().st_mtime).isoformat(),
                       chunk_index=i,
                       chunk_text=chunk[:500],  # Store first 500 chars for preview
                   )

               updated += 1
               if updated % 50 == 0:
                   conn.commit()
                   logger.info(f"Progress: {updated} notes indexed")

           except Exception as e:
               errors += 1
               logger.warning(f"Failed to index {note_path}: {e}")

       conn.commit()
       conn.close()

       duration_ms = int((time.time() - start) * 1000)
       logger.info(
           f"Indexing complete: {updated} updated, {skipped} skipped, {errors} errors "
           f"in {duration_ms}ms"
       )

       record_run(
           config.log_dir, "vault-indexer", "nightly",
           "success", 0.0, duration_ms, 0,
           f"{updated} updated, {skipped} skipped, {errors} errors"
       )


   def main():
       asyncio.run(run())


   if __name__ == "__main__":
       main()
   ```

   **Why:** This is pure infrastructure — it makes every other agent smarter by providing semantic search over the vault. Running nightly on the Mac Mini at 2 AM means it's always up to date by morning. The content hash check means unchanged notes are skipped (fast incremental updates).

   **Verify:** `PYTHONPATH=. python3 agents/vault_indexer.py` runs and creates/updates the SQLite database.

3. **Add config and schedule**

   Add to `config.toml`:
   ```toml
   [agents.vault_indexer]
   enabled = true
   skills = []
   max_turns = 0
   max_budget_usd = 0.0
   schedule = "daily 02:00"
   ```

   Create `agents-sdk/schedules/com.sean.agent.vault-indexer.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.vault-indexer</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3</string>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_indexer.py</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack</string>
       <key>EnvironmentVariables</key>
       <dict>
           <key>PYTHONPATH</key>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk</string>
       </dict>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>2</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/vault-indexer-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/vault-indexer-stderr.log</string>
   </dict>
   </plist>
   ```

   Install:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.vault-indexer.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.vault-indexer.plist
   ```

   **Verify:** `launchctl list | grep vault-indexer` shows loaded.

**Gotchas:**
- nomic-embed-text must be pulled on Mac Mini first: `ollama pull nomic-embed-text`
- First run may take 10-20 minutes for ~1,500 notes. Subsequent runs are incremental (only changed notes).
- The SQLite database will be ~50-100 MB with embeddings for all notes. Ensure adequate disk space.
- This agent costs $0.00 per run — 100% local.

---

### 4.8 Preserve Session Agent — 2h

**Depends on:** Phase 1 infrastructure (MacBook Pro running local models)
**Can parallel with:** Everything else in Phase 4
**Machine:** MacBook Pro (triggered by Claude Code Stop hook)

**Steps:**

1. **Create the Stop hook**

   Create `.claude/hooks/preserve-session.sh`:

   ```bash
   #!/bin/bash
   # .claude/hooks/preserve-session.sh
   # Triggered when a Claude Code session ends (Stop hook)
   # Captures decisions and key outputs, writes to vault

   AGENTS_SDK="/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk"
   PYTHONPATH="$AGENTS_SDK" "$AGENTS_SDK/.venv/bin/python3" "$AGENTS_SDK/agents/preserve_session.py" &
   ```

   ```bash
   chmod +x .claude/hooks/preserve-session.sh
   ```

   Register in `.claude/settings.json`:
   ```json
   {
     "hooks": {
       "Stop": [
         {
           "matcher": "",
           "hooks": [".claude/hooks/preserve-session.sh"]
         }
       ]
     }
   }
   ```

   **Why:** The hook fires automatically when you close a Claude Code session. It runs in the background (&) so it doesn't block your terminal.

2. **Create the agent implementation**

   Create `agents-sdk/agents/preserve_session.py`:

   ```python
   #!/usr/bin/env python3
   """Preserve Session Agent — captures Claude Code session context to vault."""

   import asyncio
   import sys
   import time
   from pathlib import Path

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.skill_loader import load_skills
   from lib.vault_io import daily_note_path
   from lib.logging_setup import setup_logger, record_run
   from lib.custom_tools import create_vault_mcp_server

   from claude_agent_sdk import ClaudeAgentOptions, query


   async def run():
       config = load_config()
       agent_cfg = config.agent_config("preserve_session")

       if not agent_cfg.enabled:
           return

       logger = setup_logger("preserve-session", config.log_dir)
       logger.info("Preserve Session triggered — capturing session context")

       skill_prompt = load_skills(agent_cfg.skills, config.skills_dir)

       prompt = f"""{skill_prompt}

   ## Task
   A Claude Code session just ended. Capture the session context:

   1. Read the most recent Claude Code session transcript from the current working directory
      (look for .claude/ session files or recent file modifications)
   2. Extract:
      - Key decisions made during the session
      - Files created or significantly modified
      - Open questions or TODOs mentioned
      - Any errors encountered and how they were resolved
   3. Write a concise summary to today's daily note under <!-- claude-sessions -->

   Today's daily note: {daily_note_path(config.vault_root)}

   Format the summary as:
   ### Claude Code Session — [time]
   **Project:** [detected project name]
   **Decisions:** [bullet list]
   **Files Changed:** [bullet list]
   **Open Items:** [bullet list]
   """

       vault_server = create_vault_mcp_server()
       start = time.time()

       try:
           # Use a local model via Ollama on MacBook Pro
           # DeepSeek-R1:14B or Qwen3:14b for reasoning about session content
           options = ClaudeAgentOptions(
               system_prompt={"type": "preset", "preset": "claude_code"},
               model="claude-haiku-3-20250307",  # Fast + cheap for session capture
               max_turns=10,
               max_budget_usd=0.05,
               permission_mode="acceptEdits",
               setting_sources=["project"],
               mcp_servers={"vault-tools": vault_server},
               allowed_tools=[
                   "Read", "Glob", "Grep",
                   "mcp__vault-tools__vault_inject",
               ],
           )

           result = await query(prompt=prompt, options=options)
           duration_ms = int((time.time() - start) * 1000)
           cost = getattr(result, 'cost_usd', 0.0)

           record_run(
               config.log_dir, "preserve-session", "capture",
               "success", cost, duration_ms,
               getattr(result, 'num_turns', 0),
               "Session preserved to vault"
           )
           logger.info(f"Session preserved in {duration_ms}ms, cost: ${cost:.4f}")

       except Exception as e:
           duration_ms = int((time.time() - start) * 1000)
           record_run(
               config.log_dir, "preserve-session", "capture",
               "error", 0.0, duration_ms, 0, str(e)
           )
           logger.error(f"Preserve Session failed: {e}")


   def main():
       asyncio.run(run())


   if __name__ == "__main__":
       main()
   ```

   **Why:** Session preservation captures decisions and context that would otherwise be lost when you close Claude Code. The vault becomes a continuous knowledge base across sessions.

3. **Add to config.toml**

   ```toml
   [agents.preserve_session]
   enabled = true
   skills = ["preserve-session", "vault-read-write"]
   max_turns = 10
   max_budget_usd = 0.05
   ```

   **Verify:** `PYTHONPATH=. python3 agents/preserve_session.py` runs (will produce minimal output without an active session to capture).

**Gotchas:**
- The Stop hook fires AFTER the session ends, so the agent can't read the session transcript from memory. It reads recent file modifications and infers what happened.
- Running in background (&) means errors go to stderr. Check the agent log files.
- Keep max_budget very low ($0.05) since this runs after every session.

---

### 4.9 PR Digest Agent — 2h

**Depends on:** Phase 1 infrastructure (MacBook Pro running local models), GitHub MCP connected
**Can parallel with:** Everything else in Phase 4
**Machine:** MacBook Pro (Qwen2.5-Coder via MLX or Ollama)

**Steps:**

1. **Create the agent implementation**

   Create `agents-sdk/agents/pr_digest.py`:

   ```python
   #!/usr/bin/env python3
   """PR Digest Agent — summarizes new GitHub PRs, writes to vault."""

   import argparse
   import asyncio
   import sys
   import time
   from pathlib import Path

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.skill_loader import load_skills
   from lib.vault_io import daily_note_path
   from lib.logging_setup import setup_logger, record_run
   from lib.custom_tools import create_vault_mcp_server

   from claude_agent_sdk import ClaudeAgentOptions, query


   async def run(dry_run: bool = False):
       config = load_config()
       agent_cfg = config.agent_config("pr_digest")

       if not agent_cfg.enabled:
           print("PR Digest is disabled in config.toml")
           return

       logger = setup_logger("pr-digest", config.log_dir)

       skill_prompt = load_skills(agent_cfg.skills, config.skills_dir)

       prompt = f"""{skill_prompt}

   ## Task
   Generate a PR digest for today:

   1. Search GitHub for PRs updated in the last 24 hours across these repos:
      - theblock (main work repo)
      - 16BitFit repos (sprite-pipeline, etc.)
   2. For each PR, summarize:
      - Title and author
      - What it changes (1-2 sentences)
      - Impact on your work (if any)
      - Review status
   3. Write the digest to today's daily note under <!-- pr-digest -->

   Today's daily note: {daily_note_path(config.vault_root)}
   """

       if dry_run:
           print(prompt)
           return

       logger.info("Starting PR Digest")

       vault_server = create_vault_mcp_server()
       start = time.time()

       try:
           options = ClaudeAgentOptions(
               system_prompt={"type": "preset", "preset": "claude_code"},
               model="claude-haiku-3-20250307",
               max_turns=15,
               max_budget_usd=0.15,
               permission_mode="acceptEdits",
               setting_sources=["project"],
               mcp_servers={
                   "vault-tools": vault_server,
                   "github": {
                       "type": "stdio",
                       "command": "docker",
                       "args": ["run", "-i", "--rm",
                           "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                           "ghcr.io/github/github-mcp-server"],
                       "env": {
                           "GITHUB_PERSONAL_ACCESS_TOKEN": "$(security find-generic-password -s 'github-pat' -w)"
                       }
                   },
               },
               allowed_tools=[
                   "Read", "Write", "Edit",
                   "mcp__vault-tools__vault_inject",
                   "mcp__github__search_issues",
                   "mcp__github__list_pull_requests",
                   "mcp__github__get_pull_request",
               ],
           )

           result = await query(prompt=prompt, options=options)
           duration_ms = int((time.time() - start) * 1000)
           cost = getattr(result, 'cost_usd', 0.0)

           record_run(
               config.log_dir, "pr-digest", "digest",
               "success", cost, duration_ms,
               getattr(result, 'num_turns', 0),
               "PR digest written"
           )
           logger.info(f"PR Digest completed in {duration_ms}ms")

       except Exception as e:
           duration_ms = int((time.time() - start) * 1000)
           record_run(
               config.log_dir, "pr-digest", "digest",
               "error", 0.0, duration_ms, 0, str(e)
           )
           logger.error(f"PR Digest failed: {e}")
           raise


   def main():
       parser = argparse.ArgumentParser(description="PR Digest Agent")
       parser.add_argument("--dry-run", action="store_true")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

2. **Add config and launchd schedule**

   Add to `config.toml`:
   ```toml
   [agents.pr_digest]
   enabled = true
   skills = ["vault-read-write"]
   max_turns = 15
   max_budget_usd = 0.15
   schedule = "weekdays 08:00"
   ```

   Create launchd plist with Monday-Friday 8:00 AM schedule (5 separate StartCalendarInterval entries for Weekday 1-5).

   **Verify:** `PYTHONPATH=. python3 agents/pr_digest.py --dry-run` prints the prompt.

**Gotchas:**
- Store GitHub PAT in Keychain: `security add-generic-password -a "sean" -s "github-pat" -w "ghp_YOUR_TOKEN"  ~/Library/Keychains/login.keychain-db`
- The GitHub MCP runs via Docker. Ensure Docker Desktop is running on the MacBook.
- PR Digest only makes sense on weekdays. The launchd schedule should reflect this.

---

## PHASE 5: AUTORESEARCH + SCALE (Weeks 9-12, May 22 - Jun 19)

Phase 5 deploys the Karpathy autoresearch pattern for overnight ComfyUI optimization, scales the sprite pipeline to additional champions, and builds the meta-agent layer for fleet management.

---

### 5.1 autoresearch-loop/ Scaffolding — 4h

**Depends on:** Phase 4 LoRA track (ComfyUI + LoRA working), Phase 1 infrastructure (Mac Mini orchestrator)
**Can parallel with:** 5.4, 5.5, 5.6
**Machine:** Mac Mini (orchestrator) + Alienware (ComfyUI execution)

**Steps:**

1. **Create the autoresearch directory structure**

   On the Mac Mini:

   ```bash
   mkdir -p ~/Code-Brain/claude-code-superuser-pack/autoresearch-loop/
   cd ~/Code-Brain/claude-code-superuser-pack/autoresearch-loop/
   mkdir -p experiments/ results/ logs/
   ```

   Structure:
   ```
   autoresearch-loop/
   ├── loop_runner.py           # Generic keep/revert cycle
   ├── experiments/             # Pluggable experiment modules
   │   ├── __init__.py
   │   └── comfyui_experiment.py
   ├── results/                 # TSV result logs
   ├── logs/                    # Per-run logs
   └── README.md
   ```

   **Why:** This shared scaffolding can be pointed at any optimization problem where you have a mutable artifact and a measurable metric. The ComfyUI experiment is the first module; others (prompt optimization, LoRA hyperparameters) can follow the same interface.

2. **Implement the generic loop_runner.py**

   Create `autoresearch-loop/loop_runner.py`:

   ```python
   #!/usr/bin/env python3
   """
   Generic Autoresearch Loop Runner
   ================================
   Implements Karpathy's autoresearch pattern:
   - One mutable artifact
   - One measurable metric
   - Keep/revert cycle with git commits
   - TSV results logging
   - Configurable time budget per experiment

   Usage:
       python loop_runner.py --experiment comfyui --budget-hours 7 --max-experiments 500
   """

   import argparse
   import json
   import csv
   import time
   import shutil
   import subprocess
   import importlib
   import sys
   from pathlib import Path
   from datetime import datetime, timedelta
   from typing import Protocol, Any

   RESULTS_DIR = Path(__file__).parent / "results"
   LOGS_DIR = Path(__file__).parent / "logs"


   # ── Experiment Interface ──────────────────────────────────────────

   class ExperimentModule(Protocol):
       """Interface that all experiment modules must implement."""

       def name(self) -> str:
           """Human-readable experiment name."""
           ...

       def get_current_artifact(self) -> dict:
           """Return the current mutable artifact (e.g., workflow JSON parameters)."""
           ...

       def propose_mutation(self, history: list[dict]) -> dict:
           """Propose a new artifact based on experiment history. Uses optuna or similar."""
           ...

       def apply_artifact(self, artifact: dict) -> None:
           """Apply the mutated artifact (e.g., update workflow JSON)."""
           ...

       def run_experiment(self) -> dict:
           """
           Execute one experiment. Returns a dict with at least:
           - 'score': float (the primary metric to optimize)
           - 'metrics': dict (all measured metrics)
           - 'duration_s': float
           """
           ...

       def revert_artifact(self, previous: dict) -> None:
           """Revert to a previous artifact state."""
           ...


   # ── Loop Runner ───────────────────────────────────────────────────

   class LoopRunner:
       def __init__(
           self,
           experiment: ExperimentModule,
           budget_hours: float = 7.0,
           max_experiments: int = 500,
           results_file: str | None = None,
       ):
           self.experiment = experiment
           self.budget_seconds = budget_hours * 3600
           self.max_experiments = max_experiments
           self.start_time = time.time()

           RESULTS_DIR.mkdir(exist_ok=True)
           LOGS_DIR.mkdir(exist_ok=True)

           timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
           self.results_file = Path(results_file) if results_file else (
               RESULTS_DIR / f"{experiment.name()}_{timestamp}.tsv"
           )

           self.history: list[dict] = []
           self.best_score: float = float("-inf")
           self.best_artifact: dict = {}

           # Initialize TSV
           with open(self.results_file, "w", newline="") as f:
               writer = csv.writer(f, delimiter="\t")
               writer.writerow([
                   "experiment_id", "timestamp", "score", "best_score",
                   "kept", "duration_s", "metrics_json", "artifact_json"
               ])

       def time_remaining(self) -> float:
           return self.budget_seconds - (time.time() - self.start_time)

       def run(self):
           """Main loop — run experiments until budget exhausted or max reached."""
           print(f"Starting autoresearch loop: {self.experiment.name()}")
           print(f"Budget: {self.budget_seconds / 3600:.1f} hours, Max experiments: {self.max_experiments}")
           print(f"Results: {self.results_file}")

           # Capture initial state
           self.best_artifact = self.experiment.get_current_artifact()

           # Run baseline
           print("\n[Baseline] Running initial experiment...")
           baseline_result = self.experiment.run_experiment()
           self.best_score = baseline_result["score"]
           self._log_result(0, baseline_result, kept=True)
           print(f"[Baseline] Score: {self.best_score:.4f}")

           experiment_id = 1
           consecutive_failures = 0
           MAX_CONSECUTIVE_FAILURES = 10

           while (
               self.time_remaining() > 0
               and experiment_id <= self.max_experiments
               and consecutive_failures < MAX_CONSECUTIVE_FAILURES
           ):
               remaining_min = self.time_remaining() / 60
               print(f"\n[Experiment {experiment_id}] ({remaining_min:.0f} min remaining)")

               # Save current artifact for potential revert
               previous_artifact = self.experiment.get_current_artifact()

               try:
                   # Propose mutation
                   proposed = self.experiment.propose_mutation(self.history)
                   self.experiment.apply_artifact(proposed)

                   # Run experiment
                   result = self.experiment.run_experiment()
                   score = result["score"]

                   if score > self.best_score:
                       # KEEP — new best
                       self.best_score = score
                       self.best_artifact = proposed
                       self._log_result(experiment_id, result, kept=True)
                       print(f"  ✓ KEEP — Score: {score:.4f} (best: {self.best_score:.4f})")
                       consecutive_failures = 0

                       # Git commit the improvement
                       self._git_commit(experiment_id, score)
                   else:
                       # REVERT
                       self.experiment.revert_artifact(previous_artifact)
                       self._log_result(experiment_id, result, kept=False)
                       print(f"  ✗ REVERT — Score: {score:.4f} (best: {self.best_score:.4f})")
                       consecutive_failures += 1

               except Exception as e:
                   print(f"  ✗ ERROR — {e}")
                   self.experiment.revert_artifact(previous_artifact)
                   self._log_result(experiment_id, {
                       "score": 0, "metrics": {"error": str(e)}, "duration_s": 0
                   }, kept=False)
                   consecutive_failures += 1

               experiment_id += 1

           print(f"\n{'='*60}")
           print(f"Autoresearch complete: {experiment_id - 1} experiments")
           print(f"Best score: {self.best_score:.4f}")
           print(f"Results saved to: {self.results_file}")

           # Write best artifact
           best_file = self.results_file.with_suffix(".best.json")
           with open(best_file, "w") as f:
               json.dump(self.best_artifact, f, indent=2)
           print(f"Best artifact saved to: {best_file}")

       def _log_result(self, exp_id: int, result: dict, kept: bool):
           self.history.append({
               "id": exp_id,
               "score": result["score"],
               "kept": kept,
               "metrics": result.get("metrics", {}),
           })

           with open(self.results_file, "a", newline="") as f:
               writer = csv.writer(f, delimiter="\t")
               writer.writerow([
                   exp_id,
                   datetime.now().isoformat(),
                   f"{result['score']:.6f}",
                   f"{self.best_score:.6f}",
                   kept,
                   f"{result.get('duration_s', 0):.1f}",
                   json.dumps(result.get("metrics", {})),
                   json.dumps(self.experiment.get_current_artifact()),
               ])

       def _git_commit(self, exp_id: int, score: float):
           try:
               subprocess.run(
                   ["git", "add", "-A"],
                   cwd=str(Path(__file__).parent),
                   capture_output=True, timeout=10,
               )
               subprocess.run(
                   ["git", "commit", "-m",
                    f"autoresearch: exp {exp_id}, score {score:.4f}"],
                   cwd=str(Path(__file__).parent),
                   capture_output=True, timeout=10,
               )
           except Exception:
               pass  # Git commit is best-effort


   # ── CLI ────────────────────────────────────────────────────────────

   def main():
       parser = argparse.ArgumentParser(description="Autoresearch Loop Runner")
       parser.add_argument("--experiment", required=True, help="Experiment module name")
       parser.add_argument("--budget-hours", type=float, default=7.0, help="Time budget in hours")
       parser.add_argument("--max-experiments", type=int, default=500, help="Max number of experiments")
       parser.add_argument("--results-file", type=str, default=None, help="Custom results file path")
       args = parser.parse_args()

       # Dynamically load experiment module
       sys.path.insert(0, str(Path(__file__).parent / "experiments"))
       module = importlib.import_module(f"{args.experiment}_experiment")
       experiment = module.create_experiment()

       runner = LoopRunner(
           experiment=experiment,
           budget_hours=args.budget_hours,
           max_experiments=args.max_experiments,
           results_file=args.results_file,
       )
       runner.run()


   if __name__ == "__main__":
       main()
   ```

   **Why:** The generic scaffolding separates the loop mechanics (keep/revert, logging, git commits, time budget) from experiment-specific logic. Adding a new optimization target means implementing 5 methods in a new module — zero changes to the runner.

   **Verify:** `python3 loop_runner.py --help` prints usage. `python3 -c "from loop_runner import ExperimentModule; print('Protocol loaded')"` succeeds.

**Decision Gate:** N/A — this is scaffolding. Verified by the ComfyUI experiment module in 5.2.

**Gotchas:**
- Initialize a git repo in the autoresearch-loop/ directory so the keep/revert cycle can use git commits.
- The TSV format matches Karpathy's original for compatibility.
- The `MAX_CONSECUTIVE_FAILURES = 10` guard prevents infinite loops when the experiment module is broken.

---

### 5.2 ComfyUI Experiment Module — 5h

**Depends on:** 5.1 (scaffolding), Phase 4 LoRA (ComfyUI + LoRA working on Alienware)
**Can parallel with:** 5.5, 5.6
**Machine:** Alienware (runs ComfyUI + scoring)

**Steps:**

1. **Create the ComfyUI experiment module**

   Create `autoresearch-loop/experiments/comfyui_experiment.py`:

   ```python
   """
   ComfyUI Experiment Module for Autoresearch
   ============================================
   Maps the autoresearch pattern to ComfyUI sprite optimization:
   - Mutable artifact: ComfyUI workflow JSON (parameter values)
   - Metric: Composite of CLIP similarity + SSIM + aesthetic score
   - Mutation: Optuna Bayesian optimization over parameter space
   """

   import json
   import time
   import hashlib
   import requests
   import uuid
   from pathlib import Path
   from typing import Any

   import optuna
   import numpy as np

   # Scoring imports — all run locally on Alienware GPU
   import torch
   from PIL import Image
   from skimage.metrics import structural_similarity as ssim

   COMFYUI_URL = "http://127.0.0.1:8188"
   REFERENCE_IMAGE = Path("inputs/champion-sean-anchor.png")  # Your anchor image
   WORKFLOW_TEMPLATE = Path("inputs/base_workflow_api.json")    # Base ComfyUI workflow
   OUTPUT_DIR = Path("outputs/")


   class ComfyUIExperiment:
       """Implements the ExperimentModule protocol for ComfyUI optimization."""

       def __init__(self):
           self.client_id = str(uuid.uuid4())
           self.current_params: dict = {}

           # Load base workflow
           with open(WORKFLOW_TEMPLATE) as f:
               self.base_workflow = json.load(f)

           # Load reference image for similarity scoring
           self.reference_image = np.array(Image.open(REFERENCE_IMAGE).convert("RGB"))

           # Initialize optuna study
           self.study = optuna.create_study(
               direction="maximize",
               study_name="comfyui_sprite_optimization",
               sampler=optuna.samplers.TPESampler(seed=42),
           )

           # Load CLIP model for similarity scoring
           self._load_scoring_models()

           OUTPUT_DIR.mkdir(exist_ok=True)

       def _load_scoring_models(self):
           """Load CLIP and aesthetic models for scoring."""
           from transformers import CLIPProcessor, CLIPModel

           self.clip_model = CLIPModel.from_pretrained(
               "openai/clip-vit-base-patch32"
           ).to("cuda")
           self.clip_processor = CLIPProcessor.from_pretrained(
               "openai/clip-vit-base-patch32"
           )

           # Get reference image embedding
           inputs = self.clip_processor(
               images=Image.open(REFERENCE_IMAGE),
               return_tensors="pt"
           ).to("cuda")
           with torch.no_grad():
               self.reference_clip_embedding = self.clip_model.get_image_features(**inputs)
               self.reference_clip_embedding = (
                   self.reference_clip_embedding / self.reference_clip_embedding.norm()
               )

       def name(self) -> str:
           return "comfyui"

       def get_current_artifact(self) -> dict:
           return self.current_params.copy()

       def propose_mutation(self, history: list[dict]) -> dict:
           """Use optuna to propose next parameter set."""
           trial = self.study.ask()

           params = {
               "controlnet_strength": trial.suggest_float("controlnet_strength", 0.3, 1.0),
               "ipadapter_weight": trial.suggest_float("ipadapter_weight", 0.3, 1.0),
               "lora_strength": trial.suggest_float("lora_strength", 0.5, 1.2),
               "cfg": trial.suggest_float("cfg", 3.0, 12.0),
               "sampler": trial.suggest_categorical("sampler", [
                   "euler", "euler_ancestral", "dpmpp_2m",
                   "dpmpp_2m_sde", "dpmpp_2s_ancestral",
               ]),
               "steps": trial.suggest_int("steps", 15, 40),
               "seed": 42,  # Fixed seed for fair comparison
           }

           self._current_trial = trial
           return params

       def apply_artifact(self, artifact: dict) -> None:
           """Apply parameter mutations to the workflow JSON."""
           self.current_params = artifact
           # Parameters are applied when building the workflow in run_experiment

       def run_experiment(self) -> dict:
           """Run one ComfyUI generation and score it."""
           start = time.time()

           # Build workflow with current params
           workflow = self._build_workflow(self.current_params)

           # Submit to ComfyUI
           resp = requests.post(
               f"{COMFYUI_URL}/prompt",
               json={"prompt": workflow, "client_id": self.client_id},
               timeout=10,
           )
           resp.raise_for_status()
           prompt_id = resp.json()["prompt_id"]

           # Wait for completion
           output_image = self._wait_and_download(prompt_id)
           duration = time.time() - start

           if output_image is None:
               if hasattr(self, '_current_trial'):
                   self.study.tell(self._current_trial, 0.0)
               return {"score": 0.0, "metrics": {"error": "generation_failed"}, "duration_s": duration}

           # Score the output
           metrics = self._score_image(output_image)
           composite = (
               0.4 * metrics["clip_similarity"]
               + 0.3 * metrics["ssim"]
               + 0.3 * metrics.get("aesthetic_score", 0.5)
           )

           # Report to optuna
           if hasattr(self, '_current_trial'):
               self.study.tell(self._current_trial, composite)

           return {
               "score": composite,
               "metrics": metrics,
               "duration_s": duration,
           }

       def revert_artifact(self, previous: dict) -> None:
           self.current_params = previous

       def _build_workflow(self, params: dict) -> dict:
           """Build ComfyUI API workflow with the given parameters."""
           workflow = json.loads(json.dumps(self.base_workflow))

           # Map params to workflow node inputs
           # These node IDs depend on your specific workflow JSON
           # Adjust to match your exported API format
           for node_id, node in workflow.items():
               if node.get("class_type") == "KSampler":
                   node["inputs"]["cfg"] = params["cfg"]
                   node["inputs"]["sampler_name"] = params["sampler"]
                   node["inputs"]["steps"] = params["steps"]
                   node["inputs"]["seed"] = params["seed"]

               elif node.get("class_type") == "LoraLoader":
                   node["inputs"]["strength_model"] = params["lora_strength"]
                   node["inputs"]["strength_clip"] = params["lora_strength"]

               elif node.get("class_type") == "ControlNetApplyAdvanced":
                   node["inputs"]["strength"] = params["controlnet_strength"]

               elif node.get("class_type") == "IPAdapterAdvanced":
                   node["inputs"]["weight"] = params["ipadapter_weight"]

           return workflow

       def _wait_and_download(self, prompt_id: str, timeout: int = 120) -> np.ndarray | None:
           """Poll ComfyUI and download the result image."""
           start = time.time()
           while time.time() - start < timeout:
               resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=5)
               history = resp.json()

               if prompt_id in history and history[prompt_id].get("status", {}).get("completed"):
                   # Find the output image
                   outputs = history[prompt_id].get("outputs", {})
                   for node_output in outputs.values():
                       images = node_output.get("images", [])
                       if images:
                           img_info = images[0]
                           img_url = (
                               f"{COMFYUI_URL}/view?"
                               f"filename={img_info['filename']}"
                               f"&subfolder={img_info.get('subfolder', '')}"
                               f"&type={img_info.get('type', 'output')}"
                           )
                           img_resp = requests.get(img_url, timeout=30)
                           from io import BytesIO
                           img = Image.open(BytesIO(img_resp.content)).convert("RGB")

                           # Save for reference
                           ts = int(time.time())
                           img.save(OUTPUT_DIR / f"exp_{ts}.png")

                           return np.array(img)

               time.sleep(2)

           return None  # Timeout

       def _score_image(self, image: np.ndarray) -> dict:
           """Score an image against the reference using CLIP + SSIM."""
           pil_image = Image.fromarray(image)

           # CLIP similarity
           inputs = self.clip_processor(images=pil_image, return_tensors="pt").to("cuda")
           with torch.no_grad():
               image_embedding = self.clip_model.get_image_features(**inputs)
               image_embedding = image_embedding / image_embedding.norm()

           clip_sim = float(
               torch.nn.functional.cosine_similarity(
                   self.reference_clip_embedding, image_embedding
               ).item()
           )

           # SSIM — resize both to same dimensions first
           ref_resized = np.array(
               Image.fromarray(self.reference_image).resize(pil_image.size, Image.NEAREST)
           )
           gen_resized = np.array(pil_image)

           ssim_score = float(ssim(
               ref_resized, gen_resized,
               channel_axis=2, data_range=255,
           ))

           # Aesthetic score (simplified — LAION aesthetic predictor)
           # For full implementation, load the LAION aesthetic model
           # For now, use a normalized combination
           aesthetic = 0.5  # Placeholder — replace with LAION model

           return {
               "clip_similarity": clip_sim,
               "ssim": ssim_score,
               "aesthetic_score": aesthetic,
           }


   def create_experiment() -> ComfyUIExperiment:
       """Factory function called by loop_runner.py."""
       return ComfyUIExperiment()
   ```

   **Why:** This maps the autoresearch three-file architecture to ComfyUI: `prepare.py` = reference images + scoring models + ComfyUI API client (fixed), mutable artifact = workflow parameter values, `program.md` = the optuna sampler's exploration strategy. Each experiment takes ~30-60 seconds (image generation + scoring), so you get 60-120 experiments per hour on the RTX 5080.

   **Verify:** `python3 -c "from experiments.comfyui_experiment import create_experiment; e = create_experiment(); print(e.name())"` prints "comfyui".

2. **Install Python dependencies on Alienware**

   ```powershell
   # On Alienware — in the autoresearch venv
   cd C:\lora-training\autoresearch
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   pip install optuna torch torchvision transformers scikit-image Pillow requests
   # CLIP model will auto-download on first use (~600MB)
   ```

   **Why:** These are the scoring pipeline dependencies. They all run locally on the RTX 5080 GPU.

   **Verify:** `python -c "import optuna, torch, transformers; print('All imports OK')"`.

3. **Prepare the base workflow**

   Export your working ComfyUI workflow in API format:
   - In ComfyUI, enable Dev Mode (Settings → Dev Mode → On)
   - Click "Save (API Format)" to export the workflow JSON
   - Save as `autoresearch-loop/inputs/base_workflow_api.json`

   Copy your anchor image:
   ```bash
   cp assets/anchor-characters/champion-anchor-characters/Champion-Sean-anchor.png \
     autoresearch-loop/inputs/champion-sean-anchor.png
   ```

   **Verify:** `base_workflow_api.json` exists and contains valid JSON with node definitions.

4. **Run a test experiment**

   ```bash
   cd autoresearch-loop
   python loop_runner.py --experiment comfyui --budget-hours 0.1 --max-experiments 5
   ```

   This runs 5 experiments (about 5 minutes) to verify the full pipeline works.

   **Verify:** `results/comfyui_*.tsv` contains 6 rows (1 baseline + 5 experiments). Scores are non-zero.

**Gotchas:**
- ComfyUI must be running on the Alienware: `python main.py --listen 0.0.0.0 --port 8188`
- The CLIP model download (~600MB) happens on first run — make sure you have internet.
- The workflow JSON node IDs in `_build_workflow` must match YOUR workflow. Export it fresh from ComfyUI.
- If optuna suggests cfg=3 and your workflow looks washed out, add bounds constraints.

---

### 5.3 Overnight Optimization Configuration — 2h

**Depends on:** 5.1, 5.2 (autoresearch working)
**Can parallel with:** 5.4, 5.5, 5.6
**Machine:** Mac Mini (orchestrator) → Alienware (execution)

**Steps:**

1. **Create the orchestration script on Mac Mini**

   Create `autoresearch-loop/orchestrate_overnight.sh`:

   ```bash
   #!/bin/bash
   # orchestrate_overnight.sh — Mac Mini wakes Alienware, runs autoresearch
   # Called by launchd at 11:00 PM

   set -e

   ALIENWARE_MAC="XX:XX:XX:XX:XX:XX"  # Replace with Alienware's MAC address
   ALIENWARE_IP="192.168.1.X"          # Replace with Alienware's static IP
   ALIENWARE_USER="sean"
   RESULTS_DIR="/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/autoresearch-loop/results"
   LOG_FILE="/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/autoresearch-overnight.log"

   log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }

   log "Starting overnight autoresearch orchestration"

   # Step 1: Wake the Alienware
   log "Sending Wake-on-LAN packet to Alienware ($ALIENWARE_MAC)"
   /opt/homebrew/bin/wakeonlan "$ALIENWARE_MAC"

   # Wait for it to boot (typically 30-90 seconds)
   log "Waiting for Alienware to come online..."
   for i in $(seq 1 30); do
       if ping -c 1 -W 2 "$ALIENWARE_IP" > /dev/null 2>&1; then
           log "Alienware is online after ${i}0 seconds"
           break
       fi
       sleep 10
   done

   # Verify ComfyUI is accessible
   for i in $(seq 1 12); do
       if curl -sf "http://$ALIENWARE_IP:8188/system_stats" > /dev/null 2>&1; then
           log "ComfyUI is ready"
           break
       fi
       log "Waiting for ComfyUI... (attempt $i)"
       sleep 10
   done

   if ! curl -sf "http://$ALIENWARE_IP:8188/system_stats" > /dev/null 2>&1; then
       log "ERROR: ComfyUI not accessible after 2 minutes. Aborting."
       exit 1
   fi

   # Step 2: Run autoresearch via SSH
   log "Starting autoresearch loop (7 hour budget)"
   ssh "$ALIENWARE_USER@$ALIENWARE_IP" \
       "cd C:\\lora-training\\autoresearch && \
        .\\venv\\Scripts\\python.exe loop_runner.py \
        --experiment comfyui \
        --budget-hours 7 \
        --max-experiments 500" 2>&1 | tee -a "$LOG_FILE"

   EXIT_CODE=${PIPESTATUS[0]}

   # Step 3: Copy results back to Mac Mini
   log "Copying results from Alienware..."
   scp "$ALIENWARE_USER@$ALIENWARE_IP:C:/lora-training/autoresearch/results/*.tsv" \
       "$RESULTS_DIR/" 2>> "$LOG_FILE"
   scp "$ALIENWARE_USER@$ALIENWARE_IP:C:/lora-training/autoresearch/results/*.best.json" \
       "$RESULTS_DIR/" 2>> "$LOG_FILE"

   log "Autoresearch completed with exit code $EXIT_CODE"

   # Step 4: Write summary to vault
   LATEST_RESULTS=$(ls -t "$RESULTS_DIR"/*.tsv | head -1)
   EXPERIMENTS=$(wc -l < "$LATEST_RESULTS")
   BEST_SCORE=$(tail -1 "$LATEST_RESULTS" | cut -f4)

   cat >> "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/10_timeline/daily/$(date '+%Y-%m-%d').md" << EOF

   <!-- autoresearch -->
   ### Autoresearch Overnight Run — $(date '+%Y-%m-%d')
   - Experiments: $((EXPERIMENTS - 1))
   - Best composite score: $BEST_SCORE
   - Results: $LATEST_RESULTS
   EOF

   log "Summary written to vault daily note"
   ```

   ```bash
   chmod +x autoresearch-loop/orchestrate_overnight.sh
   ```

   **Why:** The Mac Mini orchestrates from its always-on position: it wakes the Alienware via WOL, verifies ComfyUI is running, starts the autoresearch loop via SSH, copies results when done, and logs a summary to the vault.

   **Verify:** Manually run the script to test the full flow (reduce `--budget-hours` to 0.1 for testing).

2. **Configure Alienware power management**

   On the Alienware, prevent it from sleeping during optimization:

   ```powershell
   # Prevent sleep while running (as admin)
   powercfg /change standby-timeout-ac 0
   powercfg /change hibernate-timeout-ac 0

   # Alternatively, create a power plan
   powercfg /create "Autoresearch" "Power plan for overnight optimization"
   # Set display off after 5 min, never sleep
   ```

   Also configure ComfyUI to auto-start:
   - Create a batch file `C:\lora-training\start-comfyui.bat`:
     ```batch
     cd C:\Users\%USERNAME%\ComfyUI
     python main.py --listen 0.0.0.0 --port 8188
     ```
   - Add to Windows Task Scheduler to run at login

   **Why:** The Alienware must stay awake for 7 hours during overnight optimization. Sleep/hibernate would kill the running experiments.

   **Verify:** `powercfg /query` shows sleep timeout = 0 on AC power.

3. **Create launchd schedule for nightly runs**

   Create `agents-sdk/schedules/com.sean.agent.autoresearch.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.sean.agent.autoresearch</string>
       <key>ProgramArguments</key>
       <array>
           <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/autoresearch-loop/orchestrate_overnight.sh</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/autoresearch-loop</string>
       <key>EnvironmentVariables</key>
       <dict>
           <key>PATH</key>
           <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
       </dict>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>23</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/autoresearch-stdout.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/agent-logs/autoresearch-stderr.log</string>
   </dict>
   </plist>
   ```

   Install:
   ```bash
   cp agents-sdk/schedules/com.sean.agent.autoresearch.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.sean.agent.autoresearch.plist
   ```

   **Verify:** `launchctl list | grep autoresearch` shows loaded.

**Gotchas:**
- Install `wakeonlan` on Mac Mini: `brew install wakeonlan`
- SSH key auth must be set up between Mac Mini and Alienware for passwordless login
- If WOL doesn't work, check: BIOS enabled? Network adapter settings correct? See research-context.md for the full WOL checklist.
- The 7-hour budget (11 PM → 6 AM) allows 420-840 experiments at 30-60s each

---

### 5.4 Pipeline Scaling: Batch Generation for Additional Champions — 4h

**Depends on:** Phase 3 (hybrid pipeline working), Phase 4 (LoRA optional but helpful)
**Can parallel with:** 5.1, 5.2, 5.3, 5.5, 5.6
**Machine:** MacBook Pro (pipeline) + Alienware (ComfyUI)

**Steps:**

1. **Create the strategy decision map**

   | Animation | Frames | Strategy | Rationale |
   |-----------|--------|----------|-----------|
   | Idle | 4 | image_only | Static pose, slight breathing. Proven in v0.1.0 |
   | Walk Forward | 8 | hybrid_keyframe_video | Locomotion with leg alternation — the problem HybridKV was built to solve |
   | Walk Backward | 8 | hybrid_keyframe_video | Same rationale as walk forward, reversed |
   | Run | 8 | hybrid_keyframe_video | Fast locomotion, needs temporal coherence |
   | Jump | 6 | image_only | Distinct keyframe poses, no cyclic motion |
   | Light Punch | 4 | image_only | Fast, distinct windup/hit/recover |
   | Heavy Punch | 6 | image_only | Distinct poses, can use pose refs |
   | Light Kick | 4 | image_only | Same as light punch |
   | Heavy Kick | 6 | image_only | Same as heavy punch |
   | Special 1 | 8 | hybrid_keyframe_video | Complex multi-frame attack |
   | Block | 2 | image_only | Just 2 frames, trivial |
   | Hit React | 4 | image_only | Distinct poses |
   | Victory | 12 | hybrid_keyframe_video | Long animation, benefits from interpolation |

   **Why:** Not every animation benefits from hybrid generation. Simple 2-4 frame animations with distinct poses are better served by image-only (cheaper, faster, proven). Hybrid is reserved for locomotion and long complex sequences.

   **Verify:** Decision map is documented and matches the 13 animation types from the production scope.

2. **Create manifests for Champion 2 and Champion 3**

   ```bash
   mkdir -p manifests/champion-luna manifests/champion-kai

   # Create walk cycle manifests (copy Sean's and update)
   cp manifests/champion-sean/walk.yaml manifests/champion-luna/walk.yaml
   cp manifests/champion-sean/walk.yaml manifests/champion-kai/walk.yaml

   # Update: character name, palette, anchor image paths
   ```

   Each manifest needs:
   - Updated `identity.character`
   - Updated `inputs.anchor` path to the new character's anchor
   - Updated palette colors in `post_processing.quantizer.palette`

   **Why:** The manifest-driven architecture means scaling to new characters is mostly configuration, not code.

   **Verify:** Both new manifests validate: `./bin/run pipeline:schema --validate manifests/champion-luna/walk.yaml`

3. **Batch processing script**

   Create `scripts/batch-generate.sh`:

   ```bash
   #!/bin/bash
   # batch-generate.sh — Generate animations for multiple characters
   # Usage: ./scripts/batch-generate.sh champion-sean champion-luna champion-kai

   set -e

   CHARACTERS="$@"
   if [ -z "$CHARACTERS" ]; then
       CHARACTERS="champion-sean champion-luna champion-kai"
   fi

   for CHARACTER in $CHARACTERS; do
       echo "=== Generating animations for $CHARACTER ==="
       for MANIFEST in manifests/$CHARACTER/*.yaml; do
           ANIM=$(basename "$MANIFEST" .yaml)
           echo "  → $ANIM"
           ./bin/run pipeline:run --manifest "$MANIFEST" || {
               echo "  ✗ FAILED: $CHARACTER/$ANIM"
               continue
           }
           echo "  ✓ Complete: $CHARACTER/$ANIM"
       done
   done

   echo "=== Batch generation complete ==="
   ```

   ```bash
   chmod +x scripts/batch-generate.sh
   ```

   **Verify:** `./scripts/batch-generate.sh champion-sean` processes all of Sean's manifests.

4. **Create the expanded manifest YAML for Champion 2 (example)**

   ```yaml
   # manifests/champion-luna/walk.yaml
   identity:
     character: luna
     character_type: champion
     move: walk_forward
     version: v1
     frame_count: 8
     target_resolution: 128

   inputs:
     anchor: assets/anchor-characters/champion-anchor-characters/Champion-Luna-anchor.png
     style_refs:
       - assets/style-refs/luna-turnaround.png
     pose_refs:
       - assets/pose-refs/walk-cycle/contact-left.png
       - assets/pose-refs/walk-cycle/passing.png
       - assets/pose-refs/walk-cycle/contact-right.png
       - assets/pose-refs/walk-cycle/passing-return.png
     guides:
       - assets/guides/guide_128.png

   generator:
     strategy: hybrid_keyframe_video
     strategy_fallback: image_only
     keyframe:
       backend: gemini-flash
       model: gemini-2.0-flash-exp
       mode: edit_from_anchor
       keyframe_indices: [0, 2, 4, 6]
       interpolation_frames: [1, 3, 5, 7]
     interpolation:
       backend: pika-pikaframes
       model: pika-2.2
       duration: 2.0
       fps: 24
       loop: true
       creativity_scale: 0.3
       motion_prompt: >
         Pixel art fighting game character performing a smooth walk cycle.
         Character walks forward (right) with natural leg alternation.
         Fixed side-view camera. Solid green (#00FF00) background.
         Bold dark outlines. No anti-aliasing, no blur, no gradients.

     prompts:
       master: >
         Generate frame {{frame_index}} of {{frame_count}} for a pixel art
         fighting game walk cycle animation. 128×128 pixels.
       negative: "blur, anti-aliasing, gradient, 3D, photorealistic"
     max_attempts_per_frame: 5

   post_processing:
     enabled: true
     restyle_pass: false
     quantizer:
       targetSize: { w: 128, h: 128 }
       palette:
         # Luna's palette — update with actual character colors
         - '#E8C4A0'   # Skin
         - '#2C1810'   # Hair — dark brown
         - '#8B4513'   # Eyes — brown
         - '#FF4444'   # Top — red
         - '#1A1A2E'   # Pants — dark navy
         - '#CCCCCC'   # Boots — grey
         - '#272929'   # Outlines
         - '#000000'   # Black
         - '#FFFFFF'   # White
       outlineColor: '#272929'
       outlineWeight: 2
       backgroundStrategy: chroma_key
       chromaColor: '#00FF00'
     temporal_smoothing:
       enabled: true
       staticRegionThreshold: 15
       smoothingWindow: all
       loopable: true
   ```

   **Verify:** Manifest validates and generates output.

**Gotchas:**
- Each character needs unique anchor art and palette. Don't reuse Sean's palette for Luna.
- Batch generation can take 1-2 hours per character (13 animations × 5-15 min each).
- API costs scale linearly. Budget ~$2-5 per character for Gemini + video model calls.

---

### 5.5 Meta-Agent Implementation — 4h

**Depends on:** Phases 1-4 (agents running, vault populated with data)
**Can parallel with:** 5.1-5.4, 5.6
**Machine:** Mac Mini (orchestrates), MacBook Pro (local summaries), Claude Opus (synthesis)

**Steps:**

1. **Create the Meta-Agent**

   Create `agents-sdk/agents/meta_agent.py`:

   ```python
   #!/usr/bin/env python3
   """
   Meta-Agent / Chief of Staff — Monthly "State of Sean" report.
   Map-reduce pattern:
   - MacBook Pro runs Qwen2.5-32B via MLX for individual data summaries
   - Claude Opus synthesizes the final report
   """

   import argparse
   import asyncio
   import json
   import sys
   import time
   import csv
   from pathlib import Path
   from datetime import datetime, timedelta

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.config import load_config
   from lib.vault_io import daily_note_path, recent_daily_notes
   from lib.logging_setup import setup_logger, record_run
   from lib.custom_tools import create_vault_mcp_server

   import requests
   from claude_agent_sdk import ClaudeAgentOptions, query

   MACBOOK_OLLAMA = "http://192.168.1.X:11434"  # MacBook Pro's Ollama endpoint


   def local_summarize(text: str, task: str) -> str:
       """Run a summarization task on MacBook Pro via Qwen2.5-32B."""
       try:
           resp = requests.post(
               f"{MACBOOK_OLLAMA}/api/generate",
               json={
                   "model": "qwen2.5:32b",
                   "prompt": f"Summarize the following data for a monthly report.\nTask: {task}\n\nData:\n{text[:8000]}",
                   "stream": False,
                   "options": {"temperature": 0.3, "num_predict": 500},
               },
               timeout=120,
           )
           return resp.json().get("response", "Summary unavailable")
       except Exception as e:
           return f"Local summarization failed: {e}"


   async def run(dry_run: bool = False):
       config = load_config()
       logger = setup_logger("meta-agent", config.log_dir)
       start = time.time()

       logger.info("Starting Meta-Agent — State of Sean report")

       # ── MAP PHASE: Gather and locally summarize data ──

       # 1. Agent run history
       history_path = Path(config.log_dir) / "agent-run-history.csv"
       if history_path.exists():
           with open(history_path) as f:
               history_data = f.read()
           agent_summary = local_summarize(history_data, "Summarize agent run patterns, costs, and failures from the last 30 days")
       else:
           agent_summary = "No agent run history available."

       # 2. Recent daily notes (last 30)
       vault_root = Path(config.vault_root)
       recent_notes = recent_daily_notes(vault_root, 30)
       note_contents = "\n---\n".join(
           [n.read_text(errors="replace")[:2000] for n in recent_notes[:15]]
       )
       vault_summary = local_summarize(note_contents, "Identify key themes, accomplishments, and patterns from daily notes")

       # 3. Cost analysis
       if history_path.exists():
           with open(history_path) as f:
               reader = csv.DictReader(f)
               costs = [float(row.get("cost_usd", 0)) for row in reader if row.get("cost_usd")]
           total_cost = sum(costs)
           avg_cost = total_cost / len(costs) if costs else 0
           cost_summary = f"Total cost: ${total_cost:.2f}, Avg per run: ${avg_cost:.4f}, Runs: {len(costs)}"
       else:
           cost_summary = "No cost data available."

       logger.info("MAP phase complete — local summaries generated")

       # ── REDUCE PHASE: Opus synthesizes the final report ──

       synthesis_prompt = f"""You are the Chief of Staff for Sean's autonomous agent system.
   Generate a monthly "State of Sean" report based on these summaries.

   ## Agent Fleet Summary
   {agent_summary}

   ## Vault Activity Summary
   {vault_summary}

   ## Cost Summary
   {cost_summary}

   ## Report Template
   Generate a report with these sections:
   1. **Executive Summary** — 3-sentence overview of the month
   2. **Agent Fleet Health** — Which agents ran well, which had issues
   3. **Key Accomplishments** — From daily notes and agent outputs
   4. **Cost Analysis** — Current spend vs. $6-10/month target
   5. **Recommendations** — 3 specific action items for next month

   Write this to the vault as a monthly review note.
   """

       if dry_run:
           print(synthesis_prompt)
           return

       vault_server = create_vault_mcp_server()

       options = ClaudeAgentOptions(
           system_prompt={"type": "preset", "preset": "claude_code"},
           model="claude-opus-4-20250514",
           max_turns=15,
           max_budget_usd=1.00,  # Opus is more expensive
           permission_mode="acceptEdits",
           setting_sources=["project"],
           mcp_servers={"vault-tools": vault_server},
           allowed_tools=[
               "Read", "Write", "Edit",
               "mcp__vault-tools__vault_inject",
           ],
       )

       result = await query(prompt=synthesis_prompt, options=options)
       duration_ms = int((time.time() - start) * 1000)
       cost = getattr(result, 'cost_usd', 0.0)

       record_run(
           config.log_dir, "meta-agent", "monthly",
           "success", cost, duration_ms,
           getattr(result, 'num_turns', 0),
           "State of Sean report generated"
       )
       logger.info(f"Meta-Agent completed in {duration_ms}ms, cost: ${cost:.4f}")


   def main():
       parser = argparse.ArgumentParser(description="Meta-Agent — State of Sean")
       parser.add_argument("--dry-run", action="store_true")
       args = parser.parse_args()
       asyncio.run(run(dry_run=args.dry_run))


   if __name__ == "__main__":
       main()
   ```

   **Why:** Map-reduce saves money. The expensive Opus call only sees pre-digested summaries (generated locally for free by Qwen2.5-32B), not raw data. This keeps the Opus input under ~2,000 tokens.

   **Verify:** `PYTHONPATH=. python3 agents/meta_agent.py --dry-run` prints the synthesis prompt.

2. **Schedule monthly run**

   Add to `config.toml`:
   ```toml
   [agents.meta_agent]
   enabled = true
   skills = ["vault-read-write"]
   max_turns = 15
   max_budget_usd = 1.00
   schedule = "1st of month 09:00"
   ```

   Create a launchd plist with Day=1 for monthly execution.

   **Verify:** Agent runs on the 1st of the month.

**Gotchas:**
- Opus 4.6 price dropped 67% ($5/$25 per MTok) — still the most expensive model. Keep the input concise.
- MacBook Pro must be awake when the map phase runs. Schedule for 9 AM when the laptop is likely open.
- If the MacBook is asleep, the map phase can fall back to using Haiku for summaries (more expensive but works from Mac Mini).

---

### 5.6 Fleet Optimization — 3h

**Depends on:** Phases 1-4 (fleet running, agent-run-history.csv populated)
**Can parallel with:** 5.1-5.5
**Machine:** Mac Mini

**Steps:**

1. **Create the token audit script**

   Create `agents-sdk/scripts/fleet_audit.py`:

   ```python
   #!/usr/bin/env python3
   """Analyze agent-run-history.csv for cost optimization opportunities."""

   import csv
   import sys
   from pathlib import Path
   from collections import defaultdict
   from datetime import datetime

   HISTORY_FILE = Path("vault/90_system/agent-logs/agent-run-history.csv")

   def analyze():
       if not HISTORY_FILE.exists():
           print("No agent-run-history.csv found")
           return

       with open(HISTORY_FILE) as f:
           reader = csv.DictReader(f)
           rows = list(reader)

       # Cost by agent
       agent_costs = defaultdict(float)
       agent_runs = defaultdict(int)
       agent_durations = defaultdict(list)
       agent_errors = defaultdict(int)

       for row in rows:
           agent = row.get("agent", "unknown")
           cost = float(row.get("cost_usd", 0))
           duration = int(row.get("duration_ms", 0))
           status = row.get("status", "")

           agent_costs[agent] += cost
           agent_runs[agent] += 1
           agent_durations[agent].append(duration)
           if status == "error":
               agent_errors[agent] += 1

       print("=" * 60)
       print("FLEET COST AUDIT")
       print("=" * 60)
       print(f"\nTotal runs: {len(rows)}")
       print(f"Total cost: ${sum(agent_costs.values()):.4f}")
       print(f"\nCost by Agent:")

       for agent in sorted(agent_costs, key=lambda a: agent_costs[a], reverse=True):
           avg_cost = agent_costs[agent] / agent_runs[agent]
           avg_duration = sum(agent_durations[agent]) / len(agent_durations[agent]) / 1000
           error_rate = agent_errors[agent] / agent_runs[agent] * 100
           print(f"  {agent:25s} ${agent_costs[agent]:8.4f} total "
                 f"({agent_runs[agent]:3d} runs, ${avg_cost:.4f}/run, "
                 f"{avg_duration:.1f}s avg, {error_rate:.0f}% errors)")

       # Optimization recommendations
       print(f"\n{'='*60}")
       print("OPTIMIZATION RECOMMENDATIONS")
       print("=" * 60)

       for agent, cost in sorted(agent_costs.items(), key=lambda x: x[1], reverse=True):
           if cost / agent_runs[agent] > 0.10:
               print(f"  ⚠ {agent}: ${cost/agent_runs[agent]:.4f}/run — consider local model routing")
           if agent_errors[agent] / agent_runs[agent] > 0.2:
               print(f"  ⚠ {agent}: {agent_errors[agent]/agent_runs[agent]*100:.0f}% error rate — investigate")

   if __name__ == "__main__":
       analyze()
   ```

   **Verify:** `python3 agents-sdk/scripts/fleet_audit.py` produces a cost breakdown.

2. **Optimize launchd schedules for prompt caching**

   Cluster API-calling agents within 5-minute windows:

   ```
   BEFORE (scattered):
   5:30 AM — Process Inbox (local)
   6:00 AM — Daily Driver (Sonnet API)
   8:00 AM — PR Digest (Haiku API)
   9:00 AM — Sprint Health (Sonnet API)

   AFTER (clustered for cache hits):
   5:30 AM — Process Inbox (local, no cache benefit)
   6:00 AM — Daily Driver (Sonnet API) ← Writes cache
   6:02 AM — Sprint Health (Sonnet API) ← READS cache, 90% discount
   6:04 AM — PR Digest (Haiku API) ← Separate model, no cache sharing
   ```

   **Why:** Anthropic charges $3.75/MTok to write to the 5-minute prompt cache but only $0.30/MTok for cache reads. Clustering agents that use the same model (Sonnet) within a 5-minute window means agent 2+ get the 90% cache discount on shared system prompts and skill content.

   Update the launchd plists:
   ```xml
   <!-- Sprint Health: Changed from 9:00 AM to 6:02 AM -->
   <key>StartCalendarInterval</key>
   <dict>
       <key>Hour</key><integer>6</integer>
       <key>Minute</key><integer>2</integer>
   </dict>
   ```

   **Verify:** `launchctl list | grep com.sean.agent` shows updated schedules. Cost audit after 2 weeks shows reduced Sonnet costs.

3. **Document updated schedule**

   | Time | Agent | Machine | Model | Cache |
   |------|-------|---------|-------|-------|
   | 2:00 AM | Vault Indexer | Mac Mini | nomic-embed-text (local) | N/A |
   | 5:30 AM | Process Inbox | Mac Mini | phi4-mini-reasoning (local) | N/A |
   | 6:00 AM | Daily Driver | Mac Mini | Claude Sonnet (API) | Writes cache |
   | 6:02 AM | Sprint Health | Mac Mini | Claude Sonnet (API) | Reads cache |
   | 8:00 AM | PR Digest | MacBook Pro | Claude Haiku (API) | Own cache |
   | 5:00 PM | Daily Driver (evening) | Mac Mini | Claude Sonnet (API) | Writes cache |
   | 7:00 PM Sun | Meeting Defender | Mac Mini | phi4-mini + Haiku | N/A + own |
   | 11:00 PM | Autoresearch | Mac Mini → Alienware | N/A (local) | N/A |
   | 1st of month | Meta-Agent | Mac Mini + MBP | Qwen 32B + Opus | N/A |

   **Verify:** Schedule is documented. No overlapping agents on the same machine at the same time.

**Gotchas:**
- Prompt caching only works within the same model. Clustering Sonnet and Haiku agents doesn't help.
- The 5-minute cache window is from the first request. If agent 1 takes 6 minutes, agent 2 misses the cache.
- Keep at least 30 seconds between clustered agents to avoid Anthropic rate limits.
- Monitor costs for 2 weeks after schedule optimization to measure actual savings.

---

## Summary: Phase 3-5 Time Estimates

| Phase | Task | Hours | Machine |
|-------|------|-------|---------|
| **3** | 3.1 Generator Adapter Interface | 5h | MacBook Pro |
| | 3.2 Best Video Model Wired | 3h | MacBook Pro |
| | 3.3 E2E Hybrid Test | 4h | MacBook Pro |
| | 3.4 Sprint Health Monitor Agent | 3h | Mac Mini |
| | 3.5 Meeting Defender Agent | 3h | Mac Mini |
| | 3.6 Jira MCP Setup | 1.5h | Mac Mini |
| | **Phase 3 Total** | **19.5h** | |
| **4** | 4.1 kohya_ss Installation | 2h | Alienware |
| | 4.2 Dataset Preparation | 3h | MacBook Pro → Alienware |
| | 4.3 Download Base Model | 0.5h | Alienware |
| | 4.4 First LoRA Training Run | 2h | Alienware |
| | 4.5 LoRA Testing in ComfyUI | 1.5h | Alienware |
| | 4.6 LoRA Integration into Pipeline | 2h | MacBook Pro + Alienware |
| | 4.7 Vault Embedding Indexer Agent | 2.5h | Mac Mini |
| | 4.8 Preserve Session Agent | 2h | MacBook Pro |
| | 4.9 PR Digest Agent | 2h | MacBook Pro |
| | **Phase 4 Total** | **17.5h** | |
| **5** | 5.1 Autoresearch Scaffolding | 4h | Mac Mini + Alienware |
| | 5.2 ComfyUI Experiment Module | 5h | Alienware |
| | 5.3 Overnight Optimization Config | 2h | Mac Mini → Alienware |
| | 5.4 Pipeline Scaling | 4h | MacBook Pro + Alienware |
| | 5.5 Meta-Agent Implementation | 4h | Mac Mini + MacBook Pro |
| | 5.6 Fleet Optimization | 3h | Mac Mini |
| | **Phase 5 Total** | **22h** | |
| | **Grand Total (Phases 3-5)** | **59h** | |

At ~10 hours/week of focused development time, Phases 3-5 span approximately 6 weeks (Weeks 5-12), tracking to the original timeline.

---

*Document Status: COMPLETE — Phases 3-5 of the 12-week execution blueprint.*
*Prerequisites: Phases 1-2 must be complete before starting Phase 3.*
*Next Action: Begin Phase 3.1 (Generator Adapter Interface) + Phase 3.6 (Jira MCP Setup) in parallel.*
