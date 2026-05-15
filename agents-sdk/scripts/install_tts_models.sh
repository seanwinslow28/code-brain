#!/usr/bin/env bash
# install_tts_models.sh — set up the local TTS pipeline on a fresh machine.
#
# Idempotent: re-running on a fully-set-up machine is a no-op.
# Run from the repo root or from agents-sdk/ — both work.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_SDK_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MODELS_DIR="${AGENTS_SDK_DIR}/models/kokoro"
VENV_PY="${AGENTS_SDK_DIR}/.venv/bin/python3"

MODEL_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
VOICES_URL="https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

echo "[install_tts_models] agents-sdk: ${AGENTS_SDK_DIR}"

# 1. Verify the agents-sdk venv exists
if [[ ! -x "${VENV_PY}" ]]; then
  echo "[install_tts_models] ERROR: ${VENV_PY} not found." >&2
  echo "[install_tts_models] Set up agents-sdk first: cd agents-sdk && python3 -m venv .venv && .venv/bin/python3 -m pip install -e ." >&2
  exit 1
fi

# 2. Install / upgrade the two Python deps (no-op if already at pinned versions)
echo "[install_tts_models] Installing kokoro-onnx + soundfile into existing venv…"
"${VENV_PY}" -m pip install --quiet 'kokoro-onnx>=0.5.0,<0.6' 'soundfile>=0.12,<0.14'

# 3. Verify ffmpeg is on PATH
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[install_tts_models] ERROR: ffmpeg not found on PATH. Install via 'brew install ffmpeg'." >&2
  exit 2
fi

# 4. Fetch model weights (only if missing)
mkdir -p "${MODELS_DIR}"
if [[ ! -f "${MODELS_DIR}/kokoro-v1.0.onnx" ]]; then
  echo "[install_tts_models] Downloading kokoro-v1.0.onnx (~88MB)…"
  curl -fL --retry 3 -o "${MODELS_DIR}/kokoro-v1.0.onnx" "${MODEL_URL}"
else
  echo "[install_tts_models] kokoro-v1.0.onnx already present — skipping download."
fi
if [[ ! -f "${MODELS_DIR}/voices-v1.0.bin" ]]; then
  echo "[install_tts_models] Downloading voices-v1.0.bin (~27MB)…"
  curl -fL --retry 3 -o "${MODELS_DIR}/voices-v1.0.bin" "${VOICES_URL}"
else
  echo "[install_tts_models] voices-v1.0.bin already present — skipping download."
fi

# 5. Verify checksums match the tracked CHECKSUMS.txt
if [[ -f "${MODELS_DIR}/CHECKSUMS.txt" ]]; then
  echo "[install_tts_models] Verifying checksums…"
  (cd "${MODELS_DIR}" && shasum -a 256 -c CHECKSUMS.txt)
else
  echo "[install_tts_models] WARNING: CHECKSUMS.txt not found — skipping verification." >&2
fi

# 6. Smoke-test the model load
echo "[install_tts_models] Smoke-testing model load…"
"${VENV_PY}" - <<PYEOF
from kokoro_onnx import Kokoro
k = Kokoro("${MODELS_DIR}/kokoro-v1.0.onnx", "${MODELS_DIR}/voices-v1.0.bin")
voices = k.get_voices()
assert "af_heart" in voices, f"af_heart missing — voices: {sorted(voices)[:10]}"
print(f"  voices loaded: {len(voices)}  af_heart: OK")
PYEOF

echo "[install_tts_models] Done. Try: cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py --source <path-to-md>"
