---
type: decision-record
created: 2026-05-15
status: accepted
---

# Local TTS — kokoro-onnx vs hexgrad/kokoro

## Decision

Use `kokoro-onnx` (PyPI, thewh1teagle) for the local doc-to-audio pipeline.

## Context

Sean wants verbatim narration of vault markdown (deep-research, synthesis, plans)
for commute listening on Apple Silicon. Single voice, no LLM rewriting, $0/run.
Two viable Python packages wrap Kokoro-82M:

| Dimension | `kokoro` (hexgrad, official) | `kokoro-onnx` (thewh1teagle) |
|---|---|---|
| Runtime | PyTorch + transformers | ONNX Runtime only |
| Apple Silicon | Needs `PYTORCH_ENABLE_MPS_FALLBACK=1` | Native, no env vars |
| G2P | `misaki[en]` + espeak-ng system binary | Bundled via `phonemizer-fork` + `espeakng-loader` wheels (pure Python) |
| Venv footprint | +2GB (PyTorch wheels) | +80MB (onnxruntime) |
| Model size | 327MB pth | 310MB fp32 ONNX (88MB int8 variant also available) |
| Cold start | 3-5s | <1s |
| Voices | All 54+ | All 54+ |
| Voice blending | Yes | Yes |
| License | Apache 2.0 | Apache 2.0 (model) + MIT (wrapper) |

## Rationale

- **No PyTorch in agents-sdk/.venv.** The fleet (vault_indexer, vault_synthesizer,
  query.py, gemini_dr.py) currently has zero PyTorch dependency. Adding it for a
  one-shot CLI tool blows up the venv 25x and forces a $0/run "local" pipeline to
  ship a research-grade ML framework as transitive baggage.
- **No espeak-ng.** Hexgrad's package requires the espeak-ng homebrew binary for
  English out-of-distribution fallback. kokoro-onnx bakes G2P into the graph.
- **Faster cold start matters.** This is a CLI tool invoked per-document, not a
  long-lived agent. Sub-second model load means total wall-clock per doc stays
  low.
- **Matches fleet idiom.** vault_indexer (nomic-embed-text via Ollama),
  deep_researcher (Qwen3-14B via Ollama), vault_synthesizer (Qwen3-14B via
  LM Studio) — every existing local model loads via a thin HTTP or ONNX wrapper,
  never via PyTorch directly.

## Tradeoff accepted

If Sean ever wants languages beyond English (`a` lang code in hexgrad's package),
PyTorch path would let him swap `lang_code='a'` → `lang_code='j'` more cleanly.
kokoro-onnx requires re-downloading a different voice file for non-English voices
but supports all the same languages. Not a blocker — Sean's listening corpus is
English-only.

## Rollback

Replacing kokoro-onnx with hexgrad/kokoro is a 3-line swap in
`lib/kokoro_synth.py` plus a venv pip uninstall/install. Not coupled to any other
file.

## Sources

- [hexgrad/Kokoro-82M on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M)
- [thewh1teagle/kokoro-onnx GitHub](https://github.com/thewh1teagle/kokoro-onnx)
- [hexgrad/kokoro GitHub](https://github.com/hexgrad/kokoro)
- [kokoro-onnx PyPI](https://pypi.org/project/kokoro-onnx/)
