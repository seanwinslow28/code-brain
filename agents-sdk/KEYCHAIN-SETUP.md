# Keychain Setup Guide — Multi-Machine `com.sean.agents`

macOS Keychain is per-machine. Credentials stored on one machine are not accessible from another. This guide covers which API keys to install on each machine and how to set them up.

**Keychain helper:** `agents-sdk/lib/keychain.py` (uses `security` CLI under the hood, service prefix `com.sean.agents`)

---

## What's on the MacBook Pro Today

These credentials are already stored on the MacBook Pro (your dev machine):

| Keychain Name | Service | Used By |
|---------------|---------|---------|
| `google-ai-key` | Gemini API (NB2 keyframe generation) | `GeminiAdapter` |
| `pixel_lab_api_key` | PixelLab API (sprite generation/animation) | `PixelLabAdapter` |
| `replicate-key` | Replicate API (rd-animation) | `ReplicateAdapter` |
| `fal-ai-key` | fal.ai API (Pika Pikaframes) | `PikaAdapter` |
| `huggingface-token` | Hugging Face Hub | Model downloads |
| `runware-key` | Runware API | Image generation (unused in current pipeline) |
| `google-oauth-client-id` | Google OAuth | MCP server auth |
| `google-oauth-client-secret` | Google OAuth | MCP server auth |
| `alienware_mac` | Alienware MAC address | Wake-on-LAN |

---

## Mac Mini Setup (192.168.68.200)

The Mac Mini is the always-on orchestrator. It runs launchd-scheduled agents and local Ollama models. It needs credentials if any of its agents call external APIs directly (rather than being proxied through the MacBook Pro).

### Required Keys

| Keychain Name | Why | Source in Your .env |
|---------------|-----|---------------------|
| `google-ai-key` | Batch orchestrator + autoresearch may run from Mac Mini. GeminiAdapter needs this for NB2 keyframe generation. | `GEMINI_API_KEY` from `.env` |
| `alienware_mac` | Wake-on-LAN for Alienware when routing CUDA tasks. Used by `hybrid_router.py`. | Already known: `B4:E9:B8:F7:71:47` |

### Optional Keys (install if you plan to run these from Mac Mini)

| Keychain Name | Why | Source in Your .env |
|---------------|-----|---------------------|
| `pixel_lab_api_key` | Only if running PixelLab generation directly from Mac Mini | Your PixelLab dashboard |
| `replicate-key` | Only if running rd-animation from Mac Mini | Your Replicate dashboard |
| `huggingface-token` | Only if downloading models to Mac Mini via `huggingface-cli` | Your HF settings |

### Setup Commands (run on Mac Mini)

First, copy `keychain.py` to the Mac Mini (or SSH in and access the repo):

```bash
# SSH into Mac Mini
ssh seanwinslow@192.168.68.200

# Navigate to the repo (adjust if path differs on Mac Mini)
cd ~/Code-Brain/claude-code-superuser-pack

# Required — Gemini API key for sprite generation
python3 agents-sdk/lib/keychain.py set google-ai-key "YOUR_GEMINI_API_KEY"

# Required — Alienware MAC for Wake-on-LAN
python3 agents-sdk/lib/keychain.py set alienware_mac "B4:E9:B8:F7:71:47"

# Verify
python3 agents-sdk/lib/keychain.py list
```

Replace `YOUR_GEMINI_API_KEY` with the value from your `.env` file (`GEMINI_API_KEY`).

---

## Alienware Setup (192.168.68.201)

The Alienware is the CUDA workhorse — it runs ComfyUI, vision QA, and will run overnight autoresearch jobs. ComfyUI itself doesn't need API keys (it uses local models), but if you run the batch orchestrator or autoresearch **directly on the Alienware** (rather than orchestrating from the MacBook Pro), the adapters need their keys.

**Note:** The Alienware runs Windows. The `keychain.py` helper uses macOS `security` CLI and will **not work on Windows**. For Alienware, use environment variables or a `.env` file instead — see the Windows section below.

### Required Keys

| Key Name | Why | Source |
|----------|-----|--------|
| `GEMINI_API_KEY` | GeminiAdapter for NB2 keyframe generation during batch/autoresearch runs | `GEMINI_API_KEY` from `.env` |
| `HUGGING_FACE_HUB_TOKEN` | Model downloads via `huggingface-cli` (ComfyUI custom nodes, checkpoints) | Your HF settings |

### Optional Keys (install if running these adapters directly on Alienware)

| Key Name | Why | Source |
|----------|-----|--------|
| `PIXELLAB_API_KEY` | PixelLab adapter if testing directly | Your PixelLab dashboard |
| `REPLICATE_API_TOKEN` | Replicate adapter if testing directly | Your Replicate dashboard |
| `FAL_KEY` | fal.ai / Pika adapter if testing directly | Your fal.ai dashboard |

### Windows Setup (Alienware)

Since `keychain.py` is macOS-only, set environment variables on Windows:

**Option A: System Environment Variables (persistent)**

```powershell
# Run PowerShell as Administrator
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY", "User")
[Environment]::SetEnvironmentVariable("HUGGING_FACE_HUB_TOKEN", "YOUR_HF_TOKEN", "User")

# Verify (open new PowerShell window)
echo $env:GEMINI_API_KEY
```

**Option B: .env file (for scripts that load it)**

Create `C:\Users\seanw\Documents\Code-Brain\.env`:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
HUGGING_FACE_HUB_TOKEN=YOUR_HF_TOKEN
```

**Important:** The Python adapters currently call `keychain.get_credential()` which will fail on Windows. When running adapters on Alienware, either:
1. Set the environment variable with the same name and add an env-var fallback to the adapter, or
2. Pass the API key directly to the adapter constructor (e.g., `GeminiAdapter(api_key="...")`)

The adapters already have constructor parameters for this — `PixelLabAdapter(api_key=...)` works without Keychain.

---

## Where Your .env Keys Map To

| .env Variable | Keychain Name (`com.sean.agents`) | Which Machines Need It |
|---------------|-----------------------------------|----------------------|
| `GEMINI_API_KEY` | `google-ai-key` | MacBook Pro (has it), Mac Mini (add it), Alienware (env var) |
| — | `pixel_lab_api_key` | MacBook Pro (has it). Others only if running PixelLab directly. |
| — | `replicate-key` | MacBook Pro (has it). Others only if running Replicate directly. |
| — | `fal-ai-key` | MacBook Pro (has it). Others only if running Pika directly. |
| — | `huggingface-token` | MacBook Pro (has it). Alienware (env var for model downloads). |
| — | `alienware_mac` | MacBook Pro (has it), Mac Mini (add it for WOL). |

---

## Verification Checklist

### MacBook Pro (already done)
```bash
python3 agents-sdk/lib/keychain.py list
# Should show: alienware_mac, fal-ai-key, google-ai-key, google-oauth-client-id,
#              google-oauth-client-secret, huggingface-token, pixel_lab_api_key,
#              replicate-key, runware-key
```

### Mac Mini (after setup)
```bash
python3 agents-sdk/lib/keychain.py list
# Should show at minimum: google-ai-key, alienware_mac
```

### Alienware (after setup)
```powershell
echo $env:GEMINI_API_KEY
# Should print your Gemini API key (not empty)

echo $env:HUGGING_FACE_HUB_TOKEN
# Should print your HF token (not empty)
```

---

## Security Notes

- Never commit API keys to git. The `.env` file at the repo root is gitignored.
- Keychain credentials are encrypted at rest by macOS and protected by your login password.
- Windows environment variables are stored in the registry — less secure than macOS Keychain but acceptable for a local dev machine on a home network.
- If you rotate an API key, update it on **every machine** that has it.
