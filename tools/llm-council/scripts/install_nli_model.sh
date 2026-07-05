#!/usr/bin/env bash
# install_nli_model.sh — set up the optional local NLI entailment model (E1) for the
# fusion-discovery-council VERIFY gate.
#
# Model: cross-encoder/nli-deberta-v3-small, int8 ONNX (onnx/model_qint8_avx512_vnni.onnx),
# run on onnxruntime CPU. Without this model installed, the gate degrades gracefully to
# substring-only verification (never a hard failure) — see council/discovery/nli.py.
#
# Idempotent: re-running on a fully-set-up machine is a no-op.
# Run from the repo root or from tools/llm-council/ — both work.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COUNCIL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MODEL_ID="cross-encoder/nli-deberta-v3-small"
MODELS_DIR="${COUNCIL_DIR}/models/nli-deberta-v3-small"
ONNX_SUBPATH="onnx/model_qint8_avx512_vnni.onnx"
ONNX_FILENAME="model_qint8_avx512_vnni.onnx"

echo "[install_nli_model] tools/llm-council: ${COUNCIL_DIR}"

# 1. Resolve the HF Hub CLI. `hf` is the current entry point (huggingface_hub>=0.27);
# `huggingface-cli` is the older/deprecated name and still works on older installs.
HF_CLI=""
if command -v hf >/dev/null 2>&1; then
  HF_CLI="hf"
elif command -v huggingface-cli >/dev/null 2>&1; then
  HF_CLI="huggingface-cli"
fi
if [[ -z "${HF_CLI}" ]]; then
  echo "[install_nli_model] ERROR: neither 'hf' nor 'huggingface-cli' found on PATH." >&2
  echo "[install_nli_model] Install it: uv pip install --python ${COUNCIL_DIR}/.venv/bin/python3 huggingface_hub" >&2
  exit 1
fi
echo "[install_nli_model] Using HF Hub CLI: ${HF_CLI}"

# 2. Fetch model weights + tokenizer files (only if the ONNX is missing)
mkdir -p "${MODELS_DIR}"
if [[ ! -f "${MODELS_DIR}/${ONNX_FILENAME}" ]]; then
  echo "[install_nli_model] Downloading ${MODEL_ID} (~173MB int8 ONNX + tokenizer)…"
  "${HF_CLI}" download "${MODEL_ID}" \
    "${ONNX_SUBPATH}" \
    tokenizer.json tokenizer_config.json spm.model special_tokens_map.json added_tokens.json config.json \
    --local-dir "${MODELS_DIR}"
else
  echo "[install_nli_model] ${ONNX_FILENAME} already present — skipping download."
fi

# 3. Flatten the ONNX file: huggingface-cli --local-dir preserves the repo's onnx/ subdir,
# but nli.py::get_scorer() expects the file directly at the model-dir root.
if [[ -f "${MODELS_DIR}/${ONNX_SUBPATH}" && ! -f "${MODELS_DIR}/${ONNX_FILENAME}" ]]; then
  echo "[install_nli_model] Flattening ${ONNX_SUBPATH} -> ${ONNX_FILENAME}…"
  mv "${MODELS_DIR}/${ONNX_SUBPATH}" "${MODELS_DIR}/${ONNX_FILENAME}"
  rmdir "${MODELS_DIR}/onnx" 2>/dev/null || true
fi

# 4. Verify the ONNX landed where nli.py expects it
if [[ ! -f "${MODELS_DIR}/${ONNX_FILENAME}" ]]; then
  echo "[install_nli_model] ERROR: expected ${MODELS_DIR}/${ONNX_FILENAME} after download/flatten but it's missing." >&2
  echo "[install_nli_model] Check network access and that the huggingface-cli download above succeeded." >&2
  exit 2
fi

# 5. Verify tokenizer files landed (AutoTokenizer.from_pretrained needs these alongside the model)
if [[ ! -f "${MODELS_DIR}/tokenizer.json" && ! -f "${MODELS_DIR}/tokenizer_config.json" ]]; then
  echo "[install_nli_model] WARNING: no tokenizer files found in ${MODELS_DIR} — AutoTokenizer.from_pretrained may fail." >&2
fi

echo "[install_nli_model] Done. Model dir: ${MODELS_DIR}"
echo "[install_nli_model] Install the optional Python deps: cd tools/llm-council && uv pip install -e '.[nli]'"
echo "[install_nli_model] Then verify: uv run pytest tests/discovery/test_nli.py::test_real_model_entails_paraphrase -q"
