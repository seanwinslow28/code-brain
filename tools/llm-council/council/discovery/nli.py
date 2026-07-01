"""In-process NLI entailment scorer (E1). Optional: get_scorer() returns None on any import/load
failure so the VERIFY gate degrades to substring-only. Model = cross-encoder/nli-deberta-v3-small
int8 ONNX, run on onnxruntime CPU, no server (so no asleep-host failure mode)."""

import logging
import os
from pathlib import Path

_logger = logging.getLogger("council.discovery.nli")
_DEFAULT_DIR = Path(__file__).resolve().parent.parent.parent / "models" / "nli-deberta-v3-small"
_ENTAILMENT_IDX = 1   # CONFIRMED: index 1 = entailment (verified against model card id2label
                       # {0: contradiction, 1: entailment, 2: neutral} and a live run — 2026-07-01)
_sentinel = object()
_cached = _sentinel


def _model_dir() -> Path:
    return Path(os.environ.get("DISCOVERY_NLI_MODEL_DIR") or _DEFAULT_DIR)


class NliScorer:
    def __init__(self, session, tokenizer):
        self._session, self._tok = session, tokenizer

    def entails(self, *, premise: str, hypothesis: str) -> float:
        import numpy as np
        enc = self._tok(premise, hypothesis, truncation=True, max_length=512, return_tensors="np")
        inputs = {k: v for k, v in enc.items() if k in {i.name for i in self._session.get_inputs()}}
        logits = self._session.run(None, inputs)[0][0]
        e = np.exp(logits - np.max(logits))
        probs = e / e.sum()
        return float(probs[_ENTAILMENT_IDX])


def reset_scorer_cache() -> None:
    global _cached
    _cached = _sentinel


def get_scorer():
    """Lazy singleton. Returns an NliScorer, or None if onnxruntime/tokenizer/model are unavailable."""
    global _cached
    if _cached is not _sentinel:
        return _cached
    _cached = None
    try:
        import onnxruntime as ort
        from transformers import AutoTokenizer
        d = _model_dir()
        onnx_path = d / "model_qint8_avx512_vnni.onnx"
        if not onnx_path.exists():
            _logger.warning("NLI model not found at %s — gate runs substring-only.", onnx_path)
            return _cached
        session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        tokenizer = AutoTokenizer.from_pretrained(str(d))
        _cached = NliScorer(session, tokenizer)
    except Exception as e:  # ImportError, file/load errors — degrade, never crash a run
        _logger.warning("NLI scorer load failed (%s) — gate runs substring-only.", e)
        _cached = None
    return _cached
