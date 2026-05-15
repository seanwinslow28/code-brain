---
type: implementation-plan
created: 2026-05-15
status: awaiting-approval
related: agents-sdk/scripts/doc_to_audio.py
---

# Local TTS Pipeline (Kokoro-82M) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a single-voice, verbatim local TTS CLI at `agents-sdk/scripts/doc_to_audio.py` that converts vault markdown (deep-research, synthesis, plans, retrofit docs) into MP3s on Apple Silicon at $0/run for commute listening.

**Architecture:** A pure-ONNX inference pipeline using `kokoro-onnx` (no PyTorch dependency) loaded into the existing `agents-sdk/.venv`. The CLI orchestrates three layers: (1) `lib/markdown_to_speech.py` deterministically strips frontmatter / code fences / wikilinks / markdown links while preserving sentence-level content verbatim; (2) `lib/kokoro_synth.py` splits the cleaned text into sentence-boundary chunks (≤400 chars) and feeds them through `kokoro-onnx` at 24kHz; (3) `scripts/doc_to_audio.py` concatenates the float32 audio buffers, writes a WAV via `soundfile`, and shells out to `ffmpeg` (already installed at `/opt/homebrew/bin/ffmpeg`) to encode MP3 at `vault/90_system/audio/<source-stem>.mp3`. Idempotency via mtime comparison (skip if MP3 newer than source MD). All four mandatory verification checkpoints from the user prompt are wired into the plan as explicit pauses.

**Tech Stack:**
- Python 3.13 (existing `agents-sdk/.venv`)
- `kokoro-onnx` 0.5.0+ (pure-ONNX, Apache 2.0, no PyTorch — chosen over the official `kokoro` PyPI package for the rationale documented in Task 0)
- `soundfile` (WAV writer; libsndfile is already on macOS)
- `numpy` (already a transitive dep of the existing venv)
- `ffmpeg` 8.1 (system tool, already installed) for WAV → MP3
- Model weights: `kokoro-v1.0.onnx` (int8 quantized, ~88MB) + `voices-v1.0.bin` from the `thewh1teagle/kokoro-onnx` v1.0 release
- Default voice: `af_heart` (American English Female, hexgrad's recommended default)
- Sample rate: 24000 Hz (Kokoro's native rate)
- Host: Mac Mini primary (always-on); falls back to MBP only via Sean's manual choice — no remote routing, the script runs wherever invoked

**Due Diligence Summary (2026-05-15):**

| Question | Finding | Decision |
|---|---|---|
| Kokoro license? | Apache 2.0, confirmed via [hexgrad/kokoro GitHub](https://github.com/hexgrad/kokoro) and the model card | ✅ Compatible |
| `kokoro` (PyPI, hexgrad/official) vs `kokoro-onnx` (PyPI, thewh1teagle)? | `kokoro` pulls PyTorch + `misaki[en]` + requires `espeak-ng` system binary + needs `PYTORCH_ENABLE_MPS_FALLBACK=1` env var on Apple Silicon. `kokoro-onnx` is pure ONNX, no PyTorch, no espeak-ng, single CPU/CoreML runtime, ~80MB model, near-realtime on M1 per the README. | ✅ `kokoro-onnx` — lighter footprint, no homebrew dep, faster cold start, matches the "$0/run, $0 dependencies" ethos of the existing fleet |
| Latest `kokoro-onnx` release? | v0.5.0 uploaded Jan 30 2026; model release `model-files-v1.0` Jan 28 2025 (stable). | ✅ Stable, recent |
| Apple Silicon ready? | README states "near real-time on macOS M1"; community reports (DEV.to, geeky-gadgets) confirm CPU-only Apple Silicon works without GPU; ONNX Runtime auto-selects best provider. | ✅ Mac Mini compatible |
| TTS Arena ranking? | Kokoro-82M ranked #1 on TTS Arena leaderboard Jan 2026, beating XTTS (467M) and MetaVoice (1.2B). | ✅ Quality bar cleared |
| Venv decision? | Existing `agents-sdk/.venv` (Python 3.13.12) hosts vault_indexer, vault_synthesizer, query.py, gemini_dr.py. `kokoro-onnx` adds ~80MB onnxruntime + ~88MB model = 168MB total. No conflicting deps. | ✅ Extend `agents-sdk/.venv` — single venv matches existing fleet pattern, no new isolation boundary |

**Hard constraints honored:** $0/run (local ONNX, no API), verbatim preprocessing (no LLM in the path), single voice (`af_heart` default, `--voice` flag overrides but stays single), no install or download happens during this plan phase — all installs gated to Task 1 post-approval.

---

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `agents-sdk/scripts/doc_to_audio.py` | CREATE | CLI entrypoint mirroring `query.py` shape — argparse, `--json`, `--voice`, `--speed`, `--force`, `--out-dir`, idempotency check, orchestration |
| `agents-sdk/lib/markdown_to_speech.py` | CREATE | Pure preprocessing — frontmatter strip, code fences, wikilinks, markdown links, headings → section markers, tables → row-by-row. No I/O, no model, fully unit-testable |
| `agents-sdk/lib/kokoro_synth.py` | CREATE | Thin wrapper around `kokoro-onnx` — lazy model load, sentence-boundary chunking ≤400 chars, per-chunk synthesis, audio array concatenation with 200ms silence between H1/H2/H3 section markers |
| `agents-sdk/tests/test_markdown_to_speech.py` | CREATE | Unit tests for preprocessing — no model load required, runs fast in CI |
| `agents-sdk/tests/test_kokoro_synth.py` | CREATE | Unit tests for chunking + concatenation — model layer mocked, no ONNX runtime invoked |
| `agents-sdk/tests/test_doc_to_audio_cli.py` | CREATE | End-to-end CLI test with model layer mocked; exercises idempotency, missing-file, voice override paths |
| `agents-sdk/models/kokoro/kokoro-v1.0.onnx` | DOWNLOAD | ~88MB int8 quantized model weights (gitignored) |
| `agents-sdk/models/kokoro/voices-v1.0.bin` | DOWNLOAD | Voices binary (gitignored) |
| `agents-sdk/models/kokoro/CHECKSUMS.txt` | CREATE | SHA-256 of both files captured at download time for reproducibility |
| `agents-sdk/config.toml` | MODIFY | Add `[doc_to_audio]` section with model paths, default voice, output dir, chunk size |
| `vault/90_system/audio/` | CREATE | Output directory for generated MP3s (contents gitignored, directory tracked via `.gitkeep`) |
| `vault/90_system/audio/.gitkeep` | CREATE | Empty file to track the directory in git |
| `.gitignore` | MODIFY | Add `agents-sdk/models/` and `vault/90_system/audio/*.mp3` |
| `agents-sdk/pyproject.toml` or requirements | MODIFY | Pin `kokoro-onnx>=0.5.0,<0.6` and `soundfile>=0.12,<0.14` |
| `CHANGELOG.md` | MODIFY | Add entry under current version's "Added" section |
| `CLAUDE.md` | MODIFY | Update agents-sdk script list; mention pipeline under "Connected External Research APIs" or new "Local Audio Pipeline" subsection |
| `README.md` | MODIFY | Update if it lists scripts or capabilities |
| `docs/superpowers/plans/2026-05-15-local-tts-pipeline.md` | THIS FILE | Reference artifact for future-Claude / Sean |

---

## Task 0: Capture due-diligence + package choice rationale in repo

**Files:**
- Create: `agents-sdk/docs/local-tts-decision-record.md`

This task exists so the package-selection rationale lives in the repo (not just this plan), and so Tasks 1+ have a single artifact to point at when CHANGELOG/CLAUDE.md updates need a citation.

- [ ] **Step 1: Write the decision record**

Create `agents-sdk/docs/local-tts-decision-record.md` with this exact content:

```markdown
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
| G2P | `misaki[en]` + espeak-ng system binary | Built into ONNX graph |
| Venv footprint | +2GB (PyTorch wheels) | +80MB (onnxruntime) |
| Model size | 327MB pth | 88MB int8 ONNX |
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
```

- [ ] **Step 2: Commit**

```bash
git add agents-sdk/docs/local-tts-decision-record.md
git commit -m "docs(agents-sdk): record kokoro-onnx vs hexgrad/kokoro decision"
```

---

## Task 1: Install kokoro-onnx + soundfile into agents-sdk/.venv

**Files:**
- Modify: `agents-sdk/pyproject.toml` (add deps)
- No code changes yet

**Constraint:** This task is the FIRST place a network call happens. Skip if not yet approved.

- [ ] **Step 1: Verify clean starting state**

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -c "import kokoro_onnx" 2>&1 | head -3
```
Expected: `ModuleNotFoundError: No module named 'kokoro_onnx'`

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -c "import soundfile" 2>&1 | head -3
```
Expected: `ModuleNotFoundError: No module named 'soundfile'`

- [ ] **Step 2: Pin the deps in pyproject.toml**

Read `agents-sdk/pyproject.toml`. Locate the `dependencies = [...]` array and add these two lines (preserve existing alphabetical-or-grouped ordering used in the file):

```toml
    "kokoro-onnx>=0.5.0,<0.6",
    "soundfile>=0.12,<0.14",
```

- [ ] **Step 3: Install into the existing venv**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  .venv/bin/python3 -m pip install 'kokoro-onnx>=0.5.0,<0.6' 'soundfile>=0.12,<0.14'
```

Expected: clean install, both packages and their transitive deps (onnxruntime, numpy if not already pinned, cffi for soundfile). No PyTorch should appear in the install output. If `torch` shows up in transitives, STOP — pip resolution drifted, re-check the pinned version.

- [ ] **Step 4: Smoke-test the imports**

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -c "
import kokoro_onnx, soundfile, onnxruntime
print('kokoro_onnx', getattr(kokoro_onnx, '__version__', '(no __version__)'))
print('soundfile', soundfile.__version__)
print('onnxruntime', onnxruntime.__version__)
print('providers:', onnxruntime.get_available_providers())
"
```
Expected: all three import cleanly, onnxruntime providers includes at least `CPUExecutionProvider` (CoreML may also appear).

- [ ] **Step 5: Confirm no PyTorch leaked in**

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -m pip list 2>/dev/null | grep -iE "^(torch|transformers|misaki)" | head -5
```
Expected: empty output. If anything matches, uninstall it and re-pin.

- [ ] **Step 6: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/pyproject.toml && \
  git commit -m "deps(agents-sdk): add kokoro-onnx 0.5.x + soundfile for local TTS"
```

---

## Task 2: Download Kokoro model + voices into agents-sdk/models/kokoro/

**Files:**
- Create: `agents-sdk/models/kokoro/kokoro-v1.0.onnx` (~88MB, gitignored)
- Create: `agents-sdk/models/kokoro/voices-v1.0.bin` (~27MB, gitignored)
- Create: `agents-sdk/models/kokoro/CHECKSUMS.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Update .gitignore first**

Read `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.gitignore`. Append these lines at the end (if not already present):

```gitignore

# Local TTS — model weights and generated audio
agents-sdk/models/
vault/90_system/audio/*.mp3
!vault/90_system/audio/.gitkeep
```

- [ ] **Step 2: Create the models directory**

```bash
mkdir -p /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro
```

- [ ] **Step 3: Download the ONNX model**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro && \
  curl -fL --retry 3 -o kokoro-v1.0.onnx \
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
```
Expected: ~88MB download, exit 0.

- [ ] **Step 4: Download the voices file**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro && \
  curl -fL --retry 3 -o voices-v1.0.bin \
    https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
Expected: ~27MB download, exit 0.

- [ ] **Step 5: Capture checksums for reproducibility**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro && \
  shasum -a 256 kokoro-v1.0.onnx voices-v1.0.bin > CHECKSUMS.txt && \
  cat CHECKSUMS.txt
```
Expected: two SHA-256 hashes printed. Keep this file in git so any future re-download can be verified.

- [ ] **Step 6: Confirm gitignore covers the binaries but not CHECKSUMS.txt**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git check-ignore -v agents-sdk/models/kokoro/kokoro-v1.0.onnx agents-sdk/models/kokoro/voices-v1.0.bin && \
  echo "---" && \
  ! git check-ignore agents-sdk/models/kokoro/CHECKSUMS.txt && echo "CHECKSUMS.txt is tracked: OK"
```
Expected: both binaries match `agents-sdk/models/`; CHECKSUMS.txt is NOT ignored.

- [ ] **Step 7: Smoke-test model load**

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -c "
from kokoro_onnx import Kokoro
k = Kokoro(
    '/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/kokoro-v1.0.onnx',
    '/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/voices-v1.0.bin',
)
voices = k.get_voices()
print('voice count:', len(voices))
assert 'af_heart' in voices, f'af_heart missing: {sorted(voices)[:10]}'
print('af_heart: present')
"
```
Expected: voice count ≥ 50, `af_heart: present`. If `af_heart` is missing the upstream voices set has changed — pause and re-pick a default voice before continuing.

- [ ] **Step 8: Generate the "hello world" smoke MP3**

```bash
/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 -c "
import soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro(
    '/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/kokoro-v1.0.onnx',
    '/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/voices-v1.0.bin',
)
samples, sr = k.create('Hello Sean. This is Kokoro narrating from the Mac Mini.', voice='af_heart', speed=1.0, lang='en-us')
sf.write('/tmp/kokoro-smoke.wav', samples, sr)
print(f'wrote /tmp/kokoro-smoke.wav  sr={sr}  samples={len(samples)}  duration={len(samples)/sr:.2f}s')
"
```
Expected: a WAV at `/tmp/kokoro-smoke.wav`, sample rate 24000, duration roughly 3-5 seconds.

- [ ] **Step 9: Convert smoke WAV to MP3 (verifies the ffmpeg leg)**

```bash
ffmpeg -y -i /tmp/kokoro-smoke.wav -codec:a libmp3lame -qscale:a 2 /tmp/kokoro-smoke.mp3 2>&1 | tail -5 && \
  ls -lh /tmp/kokoro-smoke.mp3
```
Expected: ffmpeg exit 0, MP3 around 40-80KB.

- [ ] **Step 10: Commit gitignore + checksums**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add .gitignore agents-sdk/models/kokoro/CHECKSUMS.txt && \
  git commit -m "feat(agents-sdk): pin Kokoro v1.0 ONNX model checksums + gitignore weights"
```

- [ ] **Step 11: Create the cross-machine install script for Mac Mini / re-clones**

The model binaries are gitignored, so any fresh machine (Mac Mini after `git pull`, or a future re-clone on MBP) needs the deps + weights re-fetched. This script makes that a one-liner.

Create `agents-sdk/scripts/install_tts_models.sh` with this exact content:

```bash
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
```

- [ ] **Step 12: Make it executable and run it (no-op verification on the MBP that just installed everything)**

```bash
chmod +x /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/install_tts_models.sh && \
  /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/install_tts_models.sh
```
Expected on the MBP (which already has everything from earlier steps): all "already present — skipping" messages, checksum verify OK, smoke test prints `voices loaded: NN  af_heart: OK`, exits 0.

- [ ] **Step 13: Commit the install script**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/scripts/install_tts_models.sh && \
  git commit -m "feat(agents-sdk): cross-machine install script for local TTS setup"
```

> **REVIEW CHECKPOINT 1 (per user prompt section "Execution shape"):** Install verified + smoke MP3 generated + cross-machine install script ready. STOP here and wait for Sean's confirmation before continuing to Task 3.

---

## Task 3: Build `lib/markdown_to_speech.py` preprocessing — TDD

**Files:**
- Create: `agents-sdk/lib/markdown_to_speech.py`
- Test: `agents-sdk/tests/test_markdown_to_speech.py`

This is the verbatim-preserving preprocessor. It must NOT paraphrase. Sentence content survives byte-for-byte; only structural markdown is normalized.

- [ ] **Step 1: Write the failing test file**

Create `agents-sdk/tests/test_markdown_to_speech.py` with this exact content:

```python
"""Tests for verbatim markdown → speech-ready text conversion."""
from __future__ import annotations

import pytest

from lib.markdown_to_speech import (
    SectionBreak,
    Segment,
    preprocess,
    strip_frontmatter,
    strip_code_fences,
    flatten_wikilinks,
    flatten_links,
    flatten_emphasis,
    table_to_segments,
)


# ─── frontmatter ──────────────────────────────────────────────────────────

def test_strip_frontmatter_removes_yaml_block():
    text = "---\ntitle: Foo\ntype: note\n---\n\n# Body\n\nHello."
    assert strip_frontmatter(text) == "# Body\n\nHello."


def test_strip_frontmatter_no_frontmatter_unchanged():
    text = "# Body\n\nHello."
    assert strip_frontmatter(text) == text


def test_strip_frontmatter_handles_trailing_dashes_in_body():
    text = "---\ntitle: Foo\n---\n\nBody with --- mid-sentence."
    assert strip_frontmatter(text) == "Body with --- mid-sentence."


# ─── code fences ──────────────────────────────────────────────────────────

def test_strip_code_fences_replaces_with_omitted_marker():
    text = "Before.\n\n```python\nprint('x')\n```\n\nAfter."
    assert strip_code_fences(text) == "Before.\n\nCode block omitted.\n\nAfter."


def test_strip_code_fences_unlabeled_fence():
    text = "A.\n\n```\nfoo\n```\n\nB."
    assert strip_code_fences(text) == "A.\n\nCode block omitted.\n\nB."


def test_strip_code_fences_inline_backticks_preserved_text():
    text = "Run `pytest` to verify."
    assert strip_code_fences(text) == "Run pytest to verify."


# ─── wikilinks ────────────────────────────────────────────────────────────

def test_flatten_wikilinks_pipe_form_uses_display():
    assert flatten_wikilinks("See [[concepts/error-handling|error handling]] for details.") == \
        "See error handling for details."


def test_flatten_wikilinks_bare_form_uses_target():
    assert flatten_wikilinks("See [[Nate]] yesterday.") == "See Nate yesterday."


def test_flatten_wikilinks_anchor_dropped():
    assert flatten_wikilinks("See [[doc#section|details]] now.") == "See details now."


# ─── markdown links ───────────────────────────────────────────────────────

def test_flatten_links_keeps_visible_text():
    assert flatten_links("Read the [Anthropic guide](https://example.com).") == \
        "Read the Anthropic guide."


def test_flatten_links_drops_images():
    assert flatten_links("Before ![alt](img.png) after.") == "Before  after."


# ─── emphasis ─────────────────────────────────────────────────────────────

def test_flatten_emphasis_strips_markers():
    assert flatten_emphasis("**bold** and *italic* and ***both***.") == \
        "bold and italic and both."


def test_flatten_emphasis_preserves_apostrophes():
    assert flatten_emphasis("It's Sean's vault.") == "It's Sean's vault."


# ─── tables ───────────────────────────────────────────────────────────────

def test_table_to_segments_speaks_rows_with_pauses():
    table = (
        "| Col A | Col B |\n"
        "|---|---|\n"
        "| foo | bar |\n"
        "| baz | qux |\n"
    )
    segs = table_to_segments(table)
    # Header row + 2 body rows = 3 segments, each cell comma-separated
    assert len(segs) == 3
    assert segs[0] == "Col A, Col B."
    assert segs[1] == "foo, bar."
    assert segs[2] == "baz, qux."


# ─── end-to-end preprocess ────────────────────────────────────────────────

def test_preprocess_canonical_test_doc_shape():
    """The canonical retrofit doc shape: frontmatter, H1, paragraph, table, code fence."""
    source = (
        "---\n"
        "type: retrofit-plan\n"
        "created: 2026-05-13\n"
        "---\n\n"
        "# Vault Synthesizer v2 — Retrofit Tiers\n\n"
        "On 2026-05-13 morning, after a clean nightly synth run.\n\n"
        "## Why this exists\n\n"
        "Specific evidence from [[concepts/cluster-collapse|cluster collapse]].\n\n"
        "| Defect | Pattern |\n"
        "|---|---|\n"
        "| Cluster bias | TopClustRAG |\n\n"
        "```python\n"
        "format_connection_article()\n"
        "```\n\n"
        "End of body.\n"
    )
    segments = preprocess(source)
    # Filter to just speakable text + section breaks
    section_titles = [s.title for s in segments if isinstance(s, SectionBreak)]
    speech_text = " ".join(s.text for s in segments if isinstance(s, Segment))

    assert "Vault Synthesizer v2 — Retrofit Tiers" in section_titles
    assert "Why this exists" in section_titles
    # Verbatim sentence preservation
    assert "On 2026-05-13 morning, after a clean nightly synth run." in speech_text
    # Wikilink flattened, display text preserved verbatim
    assert "Specific evidence from cluster collapse." in speech_text
    # Code fence replaced
    assert "Code block omitted." in speech_text
    # Table rows present
    assert "Defect, Pattern." in speech_text
    assert "Cluster bias, TopClustRAG." in speech_text
    # No frontmatter leakage
    assert "retrofit-plan" not in speech_text
    assert "created: 2026-05-13" not in speech_text


def test_preprocess_preserves_sentence_verbatim_no_paraphrase():
    """The hard guarantee: a sentence enters, the same sentence leaves."""
    source = "On 2026-05-13, the synthesizer wrote 203 concepts and 111 connections."
    segments = preprocess(source)
    speech = " ".join(s.text for s in segments if isinstance(s, Segment))
    assert speech.strip() == source.strip()
```

- [ ] **Step 2: Run the failing test**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_markdown_to_speech.py -v 2>&1 | tail -20
```
Expected: collection error (`ModuleNotFoundError: lib.markdown_to_speech`).

- [ ] **Step 3: Write the minimal implementation**

Create `agents-sdk/lib/markdown_to_speech.py` with this exact content:

```python
"""Verbatim markdown → speech-ready segments for the doc_to_audio pipeline.

Hard guarantee: sentence content is preserved byte-for-byte. Only structural
markdown (frontmatter, code fences, wikilinks, links, emphasis, tables) is
normalized. No paraphrasing, no rewriting.

Output is a list of `Segment` (speakable text) and `SectionBreak` (heading
markers, triggering a 200ms silence in the synthesizer). Tables are exploded
into one Segment per row with cells comma-joined.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union


# ─── data shapes ──────────────────────────────────────────────────────────

@dataclass
class Segment:
    """A speakable run of text."""
    text: str


@dataclass
class SectionBreak:
    """A heading break — render as a brief silence + the heading title."""
    level: int  # 1, 2, or 3
    title: str


Element = Union[Segment, SectionBreak]


# ─── regexes ──────────────────────────────────────────────────────────────

_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_CODE_FENCE_RE = re.compile(r"```[^\n]*\n.*?\n```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_WIKILINK_RE = re.compile(r"\[\[([^\]\n|#]+)(?:#[^\]\n|]+)?(?:\|([^\]\n]+))?\]\]")
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")
_BOLDITALIC_RE = re.compile(r"\*{1,3}([^*\n]+)\*{1,3}")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
_TABLE_LINE_RE = re.compile(r"^\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")
_BLOCKQUOTE_RE = re.compile(r"^>\s?", re.MULTILINE)
_LIST_MARKER_RE = re.compile(r"^(\s*)[-*+]\s+", re.MULTILINE)
_NUMBERED_LIST_RE = re.compile(r"^(\s*)\d+\.\s+", re.MULTILINE)
_HORIZONTAL_RULE_RE = re.compile(r"^[-*_]{3,}\s*$", re.MULTILINE)
_MULTI_BLANK_RE = re.compile(r"\n{3,}")


# ─── pure helpers (each composes for end-to-end preprocess) ───────────────


def strip_frontmatter(text: str) -> str:
    """Drop a leading `---\\n...\\n---\\n` YAML block if present."""
    return _FRONTMATTER_RE.sub("", text, count=1)


def strip_code_fences(text: str) -> str:
    """Replace fenced code blocks with 'Code block omitted.' and strip inline backticks."""
    text = _CODE_FENCE_RE.sub("Code block omitted.", text)
    text = _INLINE_CODE_RE.sub(r"\1", text)
    return text


def flatten_wikilinks(text: str) -> str:
    """`[[target|display]]` → `display`; `[[target]]` → `target`; anchors dropped."""
    def repl(m: re.Match[str]) -> str:
        target = m.group(1).strip()
        display = (m.group(2) or "").strip()
        return display if display else target
    return _WIKILINK_RE.sub(repl, text)


def flatten_links(text: str) -> str:
    """Drop images entirely; reduce `[text](url)` to `text`."""
    text = _IMAGE_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    return text


def flatten_emphasis(text: str) -> str:
    """`**bold**` / `*italic*` / `***both***` → bare visible text."""
    return _BOLDITALIC_RE.sub(r"\1", text)


def table_to_segments(table_text: str) -> list[str]:
    """One Segment per row, cells joined with ', '. Separator rows dropped.

    Input is the raw markdown table block; returns a list of strings ready to
    feed into Segment(...). Trailing period added per row so the TTS engine
    inserts a natural pause between rows.
    """
    out: list[str] = []
    for line in table_text.splitlines():
        line = line.strip()
        if not line or not _TABLE_LINE_RE.match(line):
            continue
        if _TABLE_SEP_RE.match(line):
            continue
        # Drop outer pipes, split on |, strip each cell
        cells = [c.strip() for c in line.strip("|").split("|")]
        cells = [c for c in cells if c]
        if not cells:
            continue
        out.append(", ".join(cells) + ".")
    return out


# ─── orchestrator ─────────────────────────────────────────────────────────


def preprocess(text: str) -> list[Element]:
    """Convert markdown text into ordered Segment / SectionBreak elements.

    Pipeline:
        1. strip_frontmatter
        2. strip_code_fences
        3. flatten_wikilinks, flatten_links, flatten_emphasis
        4. line-by-line walk:
            - heading line → SectionBreak
            - table block → table_to_segments (one Segment per row)
            - paragraph line → accumulate into a Segment, flushed on blank line
    """
    text = strip_frontmatter(text)
    text = strip_code_fences(text)
    text = flatten_wikilinks(text)
    text = flatten_links(text)
    text = flatten_emphasis(text)
    text = _BLOCKQUOTE_RE.sub("", text)
    text = _LIST_MARKER_RE.sub(r"\1", text)
    text = _NUMBERED_LIST_RE.sub(r"\1", text)
    text = _HORIZONTAL_RULE_RE.sub("", text)
    text = _MULTI_BLANK_RE.sub("\n\n", text)

    elements: list[Element] = []
    lines = text.splitlines()
    i = 0
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            joined = " ".join(p.strip() for p in paragraph if p.strip())
            if joined:
                elements.append(Segment(text=joined))
            paragraph.clear()

    while i < len(lines):
        line = lines[i]
        # Heading
        m = _HEADING_RE.match(line)
        if m:
            flush_paragraph()
            level = len(m.group(1))
            title = m.group(2).strip()
            elements.append(SectionBreak(level=level, title=title))
            i += 1
            continue
        # Table block
        if _TABLE_LINE_RE.match(line.strip()):
            flush_paragraph()
            table_lines: list[str] = []
            while i < len(lines) and _TABLE_LINE_RE.match(lines[i].strip()):
                table_lines.append(lines[i])
                i += 1
            for row_text in table_to_segments("\n".join(table_lines)):
                elements.append(Segment(text=row_text))
            continue
        # Blank line → flush
        if not line.strip():
            flush_paragraph()
            i += 1
            continue
        # Plain paragraph line
        paragraph.append(line)
        i += 1

    flush_paragraph()
    return elements
```

- [ ] **Step 4: Run tests to verify pass**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_markdown_to_speech.py -v 2>&1 | tail -30
```
Expected: all 14 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/lib/markdown_to_speech.py agents-sdk/tests/test_markdown_to_speech.py && \
  git commit -m "feat(agents-sdk): verbatim markdown preprocessor for doc_to_audio"
```

---

## Task 4: Build `lib/kokoro_synth.py` chunking + concatenation — TDD

**Files:**
- Create: `agents-sdk/lib/kokoro_synth.py`
- Test: `agents-sdk/tests/test_kokoro_synth.py`

The synth layer takes the preprocessed `Element` list, chunks each `Segment` on sentence boundaries (≤400 chars per chunk so prosody stays natural), feeds each chunk through the Kokoro model, and concatenates the resulting float32 arrays. `SectionBreak` becomes 200ms of silence followed by the title spoken. Tests mock the model so no ONNX inference runs in CI.

- [ ] **Step 1: Write the failing test file**

Create `agents-sdk/tests/test_kokoro_synth.py` with this exact content:

```python
"""Tests for kokoro_synth — chunking + concatenation. Model layer mocked."""
from __future__ import annotations

import numpy as np
import pytest

from lib.kokoro_synth import (
    chunk_sentences,
    synthesize_elements,
    SectionBreak,
    Segment,
    SAMPLE_RATE,
)


# ─── chunk_sentences ──────────────────────────────────────────────────────

def test_chunk_sentences_short_text_one_chunk():
    chunks = chunk_sentences("Hello world.", max_chars=400)
    assert chunks == ["Hello world."]


def test_chunk_sentences_splits_on_period_under_max():
    text = "First sentence. Second sentence. Third sentence."
    chunks = chunk_sentences(text, max_chars=22)  # forces each sentence its own chunk
    assert chunks == ["First sentence.", "Second sentence.", "Third sentence."]


def test_chunk_sentences_joins_short_sentences_under_max():
    text = "Hi. There. Friend."
    # All three fit in 20 chars after join+spaces; expect one chunk
    chunks = chunk_sentences(text, max_chars=400)
    assert chunks == ["Hi. There. Friend."]


def test_chunk_sentences_respects_question_and_exclamation():
    text = "Are you sure? Yes! Then continue."
    chunks = chunk_sentences(text, max_chars=15)
    assert chunks == ["Are you sure?", "Yes!", "Then continue."]


def test_chunk_sentences_splits_long_single_sentence_on_comma():
    # A pathological 500-char sentence with commas
    text = (
        "This is one very long sentence that has commas, "
        "and more commas, and then yet more commas, "
        "and even after all those commas it just keeps "
        "going for absolutely no good reason at all "
        "until the listener has long since lost the thread."
    )
    chunks = chunk_sentences(text, max_chars=80)
    # Every chunk must be under the limit
    assert all(len(c) <= 80 for c in chunks), chunks
    # All chunks reassembled must equal the original text byte-for-byte (modulo spacing)
    rejoined = " ".join(chunks)
    assert rejoined.replace("  ", " ") == text.replace("  ", " ")


# ─── synthesize_elements (with mocked Kokoro) ────────────────────────────

class FakeKokoro:
    """Returns 0.1 seconds of zeros per call. Records call args."""
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, float, str]] = []

    def create(self, text: str, voice: str, speed: float, lang: str):
        self.calls.append((text, voice, speed, lang))
        n_samples = int(SAMPLE_RATE * 0.1)
        return np.zeros(n_samples, dtype=np.float32), SAMPLE_RATE


def test_synthesize_elements_segment_only():
    fake = FakeKokoro()
    elements = [Segment(text="Hello world.")]
    audio, sr = synthesize_elements(
        elements=elements, kokoro=fake, voice="af_heart", speed=1.0, lang="en-us",
        max_chars=400, section_silence_ms=200,
    )
    assert sr == SAMPLE_RATE
    assert len(fake.calls) == 1
    assert fake.calls[0] == ("Hello world.", "af_heart", 1.0, "en-us")
    # 0.1s of synthesis, no silence (no SectionBreak)
    assert audio.shape[0] == int(SAMPLE_RATE * 0.1)


def test_synthesize_elements_section_break_inserts_silence_and_speaks_title():
    fake = FakeKokoro()
    elements = [
        Segment(text="Before."),
        SectionBreak(level=2, title="Heading"),
        Segment(text="After."),
    ]
    audio, _ = synthesize_elements(
        elements=elements, kokoro=fake, voice="af_heart", speed=1.0, lang="en-us",
        max_chars=400, section_silence_ms=200,
    )
    # 3 chunks fed to Kokoro: "Before.", "Heading.", "After."
    spoken = [c[0] for c in fake.calls]
    assert spoken == ["Before.", "Heading.", "After."]
    # Total audio: 0.1 + 0.2 + 0.1 + 0.1 = 0.5s of audio (2 segments x 0.1s + 1 title x 0.1s + 200ms silence before title)
    expected = int(SAMPLE_RATE * (0.1 + 0.2 + 0.1 + 0.1))
    assert audio.shape[0] == expected


def test_synthesize_elements_long_segment_chunks_then_concatenates():
    fake = FakeKokoro()
    long_text = "Sentence one. Sentence two. Sentence three. Sentence four."
    elements = [Segment(text=long_text)]
    audio, _ = synthesize_elements(
        elements=elements, kokoro=fake, voice="af_heart", speed=1.0, lang="en-us",
        max_chars=15, section_silence_ms=200,
    )
    # 4 chunks (one per sentence given max_chars=15)
    assert len(fake.calls) == 4
    # Each chunk produces 0.1s
    assert audio.shape[0] == int(SAMPLE_RATE * 0.4)
```

- [ ] **Step 2: Run the failing test**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_kokoro_synth.py -v 2>&1 | tail -20
```
Expected: collection error (`ModuleNotFoundError: lib.kokoro_synth`).

- [ ] **Step 3: Write the implementation**

Create `agents-sdk/lib/kokoro_synth.py` with this exact content:

```python
"""Kokoro-ONNX wrapper — sentence chunking, per-chunk synthesis, concatenation.

The Kokoro model is loaded lazily and held by the caller (the CLI). This
module's two public entrypoints are pure functions parameterized by a `kokoro`
object that exposes `create(text, voice, speed, lang) -> (np.ndarray, int)`.
In production the real `kokoro_onnx.Kokoro` instance is passed. In tests a
fake stand-in records calls and returns deterministic zero-buffers.

Section breaks (`SectionBreak`) are rendered as `section_silence_ms` of zero
samples followed by the heading title spoken at normal speed. This produces a
listenable "pause + cue" between document sections without paraphrasing.
"""
from __future__ import annotations

import re
from typing import Protocol

import numpy as np

from lib.markdown_to_speech import Segment, SectionBreak, Element

SAMPLE_RATE = 24000

_SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")
_COMMA_SPLIT_RE = re.compile(r",\s+")


class KokoroLike(Protocol):
    def create(self, text: str, voice: str, speed: float, lang: str): ...


# ─── pure chunker ─────────────────────────────────────────────────────────


def chunk_sentences(text: str, max_chars: int = 400) -> list[str]:
    """Split `text` into chunks ≤ max_chars at sentence boundaries.

    Strategy:
        1. Split on sentence-end punctuation (`. ! ?` followed by whitespace).
        2. Greedily pack consecutive sentences into chunks until the next
           sentence would overflow.
        3. If a single sentence exceeds max_chars, split it on commas; if it
           still exceeds, hard-split at the word boundary closest to max_chars.
    """
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    sentences = [s.strip() for s in _SENTENCE_END_RE.split(text) if s.strip()]
    chunks: list[str] = []
    buffer = ""

    def flush() -> None:
        nonlocal buffer
        if buffer.strip():
            chunks.append(buffer.strip())
        buffer = ""

    for sentence in sentences:
        if len(sentence) > max_chars:
            # Sentence alone overflows. Flush buffer, then split this sentence.
            flush()
            for sub in _split_long_sentence(sentence, max_chars):
                chunks.append(sub)
            continue
        candidate = (buffer + " " + sentence).strip() if buffer else sentence
        if len(candidate) <= max_chars:
            buffer = candidate
        else:
            flush()
            buffer = sentence
    flush()
    return chunks


def _split_long_sentence(sentence: str, max_chars: int) -> list[str]:
    """Fallback splitter for a single sentence longer than max_chars."""
    pieces = _COMMA_SPLIT_RE.split(sentence)
    out: list[str] = []
    buf = ""
    for p in pieces:
        candidate = (buf + ", " + p).strip(", ") if buf else p
        if len(candidate) <= max_chars:
            buf = candidate
        else:
            if buf:
                out.append(buf)
            if len(p) <= max_chars:
                buf = p
            else:
                # Hard word-boundary split as last resort
                out.extend(_word_split(p, max_chars))
                buf = ""
    if buf:
        out.append(buf)
    return out


def _word_split(text: str, max_chars: int) -> list[str]:
    words = text.split()
    out: list[str] = []
    buf = ""
    for w in words:
        candidate = (buf + " " + w).strip() if buf else w
        if len(candidate) <= max_chars:
            buf = candidate
        else:
            if buf:
                out.append(buf)
            buf = w
    if buf:
        out.append(buf)
    return out


# ─── synthesis orchestrator ───────────────────────────────────────────────


def synthesize_elements(
    *,
    elements: list[Element],
    kokoro: KokoroLike,
    voice: str,
    speed: float,
    lang: str,
    max_chars: int = 400,
    section_silence_ms: int = 200,
) -> tuple[np.ndarray, int]:
    """Render an ordered Element list to a single concatenated float32 array.

    Returns `(audio, sample_rate)`. `audio` is a 1-D numpy float32 array at
    SAMPLE_RATE Hz. Each Segment is sentence-chunked then synthesized one
    chunk at a time. SectionBreak emits `section_silence_ms` of zeros then
    speaks the heading title at the same voice/speed. Empty/whitespace-only
    segments are skipped.
    """
    silence_samples = int(SAMPLE_RATE * section_silence_ms / 1000)
    audio_parts: list[np.ndarray] = []

    for element in elements:
        if isinstance(element, SectionBreak):
            if silence_samples > 0:
                audio_parts.append(np.zeros(silence_samples, dtype=np.float32))
            title = element.title.strip()
            if title:
                # Append a period so prosody closes cleanly
                title_text = title if title.endswith((".", "!", "?")) else title + "."
                samples, _sr = kokoro.create(title_text, voice, speed, lang)
                audio_parts.append(np.asarray(samples, dtype=np.float32))
            continue

        if isinstance(element, Segment):
            chunks = chunk_sentences(element.text, max_chars=max_chars)
            for c in chunks:
                if not c.strip():
                    continue
                samples, _sr = kokoro.create(c, voice, speed, lang)
                audio_parts.append(np.asarray(samples, dtype=np.float32))
            continue

    if not audio_parts:
        return np.zeros(0, dtype=np.float32), SAMPLE_RATE
    return np.concatenate(audio_parts), SAMPLE_RATE
```

- [ ] **Step 4: Run tests**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_kokoro_synth.py -v 2>&1 | tail -30
```
Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/lib/kokoro_synth.py agents-sdk/tests/test_kokoro_synth.py && \
  git commit -m "feat(agents-sdk): Kokoro chunking + concatenation with section silence"
```

---

## Task 5: Build the CLI `scripts/doc_to_audio.py` — TDD on the orchestration

**Files:**
- Create: `agents-sdk/scripts/doc_to_audio.py`
- Test: `agents-sdk/tests/test_doc_to_audio_cli.py`
- Modify: `agents-sdk/config.toml`

- [ ] **Step 1: Add `[doc_to_audio]` config block**

Open `agents-sdk/config.toml`. Append this block at the end of the file (after the existing `[substack_drafter]` block):

```toml

# ─── Local TTS Pipeline (v3.36.0, 2026-05-15) ───────────────────────────
# Verbatim doc-to-audio via Kokoro-82M ONNX. CLI: scripts/doc_to_audio.py.
# Cost: $0/run (pure local ONNX inference). Default host: Mac Mini.
# Model files live under agents-sdk/models/kokoro/ (gitignored, checksum tracked).

[doc_to_audio]
model_path = "agents-sdk/models/kokoro/kokoro-v1.0.onnx"
voices_path = "agents-sdk/models/kokoro/voices-v1.0.bin"
default_voice = "af_heart"
default_speed = 1.0
default_lang = "en-us"
sample_rate = 24000
max_chars_per_chunk = 400
section_silence_ms = 200
output_dir = "vault/90_system/audio"
mp3_quality = 2                          # ffmpeg libmp3lame -qscale:a 2 (~190 kbps VBR)
```

- [ ] **Step 2: Write the failing CLI test**

Create `agents-sdk/tests/test_doc_to_audio_cli.py` with this exact content:

```python
"""End-to-end CLI test for doc_to_audio. Model + ffmpeg layers stubbed."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from scripts.doc_to_audio import (
    audio_path_for_source,
    should_skip_idempotent,
    render_document,
    main,
)
from lib.kokoro_synth import SAMPLE_RATE


class FakeKokoro:
    """Returns 0.05s of zeros per call."""
    def create(self, text, voice, speed, lang):
        return np.zeros(int(SAMPLE_RATE * 0.05), dtype=np.float32), SAMPLE_RATE


# ─── path + idempotency helpers ──────────────────────────────────────────

def test_audio_path_for_source_mirrors_basename(tmp_path):
    src = tmp_path / "2026-05-13-retrofit.md"
    out = audio_path_for_source(src, tmp_path / "audio")
    assert out == tmp_path / "audio" / "2026-05-13-retrofit.mp3"


def test_should_skip_idempotent_when_mp3_newer(tmp_path):
    src = tmp_path / "src.md"
    src.write_text("# Hi\n")
    out = tmp_path / "src.mp3"
    out.write_bytes(b"fake-mp3")
    # Force mp3 mtime to be after source
    import os, time
    os.utime(out, (time.time() + 10, time.time() + 10))
    assert should_skip_idempotent(src, out, force=False) is True


def test_should_skip_idempotent_force_overrides(tmp_path):
    src = tmp_path / "src.md"
    src.write_text("# Hi\n")
    out = tmp_path / "src.mp3"
    out.write_bytes(b"fake-mp3")
    assert should_skip_idempotent(src, out, force=True) is False


def test_should_not_skip_when_source_newer(tmp_path):
    src = tmp_path / "src.md"
    src.write_text("# Hi\n")
    out = tmp_path / "src.mp3"
    out.write_bytes(b"fake-mp3")
    import os, time
    # mp3 older than source
    os.utime(out, (time.time() - 60, time.time() - 60))
    assert should_skip_idempotent(src, out, force=False) is False


def test_should_not_skip_when_no_mp3(tmp_path):
    src = tmp_path / "src.md"
    src.write_text("# Hi\n")
    out = tmp_path / "src.mp3"
    assert should_skip_idempotent(src, out, force=False) is False


# ─── render_document end-to-end (model stubbed) ──────────────────────────

def test_render_document_writes_mp3(tmp_path, monkeypatch):
    src = tmp_path / "doc.md"
    src.write_text(
        "---\ntype: note\n---\n\n# Title\n\nHello world. This is a test.\n"
    )
    out = tmp_path / "doc.mp3"

    # Stub ffmpeg: just write a placeholder MP3 file
    def fake_run(cmd, *args, **kwargs):
        # cmd = ['ffmpeg', '-y', '-i', wav, '-codec:a', ..., out]
        out_path = Path(cmd[-1])
        out_path.write_bytes(b"ID3" + b"\x00" * 100)
        class R: returncode = 0
        return R()

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = render_document(
        source=src, output=out, kokoro=FakeKokoro(),
        voice="af_heart", speed=1.0, lang="en-us",
        max_chars=400, section_silence_ms=200, mp3_quality=2,
    )

    assert out.exists()
    assert out.stat().st_size > 0
    assert result.segments_synthesized >= 2  # "Title.", "Hello world. This is a test."
    assert result.duration_sec > 0
    assert result.output_path == out


# ─── CLI ──────────────────────────────────────────────────────────────────

def test_main_missing_source_returns_nonzero(tmp_path, capsys):
    rc = main(["--source", str(tmp_path / "nope.md")])
    assert rc != 0


def test_main_json_mode_emits_parseable_json(tmp_path, monkeypatch):
    src = tmp_path / "doc.md"
    src.write_text("# Hi\n\nHello.\n")
    out_dir = tmp_path / "audio"

    monkeypatch.setattr(
        "scripts.doc_to_audio.load_kokoro",
        lambda *a, **kw: FakeKokoro(),
    )
    def fake_run(cmd, *args, **kwargs):
        Path(cmd[-1]).write_bytes(b"ID3" + b"\x00" * 100)
        class R: returncode = 0
        return R()
    monkeypatch.setattr(subprocess, "run", fake_run)

    import io
    buf = io.StringIO()
    monkeypatch.setattr(sys, "stdout", buf)
    rc = main(["--source", str(src), "--out-dir", str(out_dir), "--json"])
    output = buf.getvalue()
    monkeypatch.setattr(sys, "stdout", sys.__stdout__)

    assert rc == 0
    payload = json.loads(output)
    assert payload["status"] == "ok"
    assert payload["output_path"].endswith("doc.mp3")
    assert payload["duration_sec"] > 0
    assert payload["voice"] == "af_heart"
```

- [ ] **Step 3: Run the failing test**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_doc_to_audio_cli.py -v 2>&1 | tail -20
```
Expected: `ModuleNotFoundError: scripts.doc_to_audio`.

- [ ] **Step 4: Write the CLI**

Create `agents-sdk/scripts/doc_to_audio.py` with this exact content:

```python
#!/usr/bin/env python3
"""doc_to_audio — verbatim local TTS for vault markdown documents.

Reads a markdown file, strips structural noise (frontmatter, code fences,
wikilinks, links, emphasis) while preserving sentence-level content
byte-for-byte, feeds the cleaned segments through Kokoro-82M (ONNX, local,
$0/run), and writes an MP3 next to the source name under
`vault/90_system/audio/`.

Single voice, no LLM in the path, no paraphrasing. Idempotent — skips when
the MP3 mtime ≥ source MD mtime unless `--force`.

Usage:
    python3 scripts/doc_to_audio.py --source vault/.../2026-05-13-retrofit.md
    python3 scripts/doc_to_audio.py --source ... --voice af_bella --speed 1.1
    python3 scripts/doc_to_audio.py --source ... --force --json
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.kokoro_synth import SAMPLE_RATE, synthesize_elements
from lib.logging_setup import record_run, setup_logger
from lib.markdown_to_speech import Element, Segment, SectionBreak, preprocess

AGENT_NAME = "doc-to-audio"


@dataclass
class RenderResult:
    source_path: Path
    output_path: Path
    duration_sec: float
    segments_synthesized: int
    voice: str
    speed: float
    skipped: bool = False
    reason: str = ""


# ─── path helpers ────────────────────────────────────────────────────────


def audio_path_for_source(source: Path, out_dir: Path) -> Path:
    """`/x/y/2026-05-13-retrofit.md` + `audio_dir` → `audio_dir/2026-05-13-retrofit.mp3`."""
    return out_dir / (source.stem + ".mp3")


def should_skip_idempotent(source: Path, output: Path, force: bool) -> bool:
    """Skip when output is at least as new as source and force is off."""
    if force:
        return False
    if not output.exists():
        return False
    return output.stat().st_mtime >= source.stat().st_mtime


# ─── model loader (overridable for tests) ────────────────────────────────


def load_kokoro(model_path: Path, voices_path: Path):
    """Lazy import + load. Kept thin so tests can monkeypatch this name."""
    from kokoro_onnx import Kokoro  # type: ignore[import-not-found]
    return Kokoro(str(model_path), str(voices_path))


# ─── core renderer ───────────────────────────────────────────────────────


def _encode_mp3(samples: np.ndarray, sample_rate: int, output: Path, quality: int) -> None:
    """Write samples as WAV via soundfile, then convert to MP3 via ffmpeg."""
    import soundfile as sf  # local import keeps `--help` fast

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = Path(tmp.name)
    try:
        sf.write(str(wav_path), samples, sample_rate)
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(wav_path),
            "-codec:a", "libmp3lame",
            "-qscale:a", str(quality),
            str(output),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed (rc={result.returncode}): {result.stderr[:500]}")
    finally:
        wav_path.unlink(missing_ok=True)


def render_document(
    *,
    source: Path,
    output: Path,
    kokoro,
    voice: str,
    speed: float,
    lang: str,
    max_chars: int,
    section_silence_ms: int,
    mp3_quality: int,
) -> RenderResult:
    """Preprocess → synthesize → encode. Returns RenderResult."""
    text = source.read_text(encoding="utf-8", errors="replace")
    elements: list[Element] = preprocess(text)
    segment_count = sum(1 for e in elements if isinstance(e, Segment)) \
        + sum(1 for e in elements if isinstance(e, SectionBreak))

    audio, sr = synthesize_elements(
        elements=elements, kokoro=kokoro,
        voice=voice, speed=speed, lang=lang,
        max_chars=max_chars, section_silence_ms=section_silence_ms,
    )
    _encode_mp3(audio, sr, output, mp3_quality)
    duration = float(audio.shape[0]) / float(sr) if sr else 0.0
    return RenderResult(
        source_path=source, output_path=output,
        duration_sec=duration, segments_synthesized=segment_count,
        voice=voice, speed=speed,
    )


# ─── CLI ─────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Convert a vault markdown doc to a verbatim local-TTS MP3.",
    )
    p.add_argument("--source", required=True, help="Path to the markdown file.")
    p.add_argument("--out-dir", default=None,
                   help="Override output directory (default: config [doc_to_audio].output_dir).")
    p.add_argument("--voice", default=None, help="Kokoro voice (default: af_heart).")
    p.add_argument("--speed", type=float, default=None, help="Speech speed (default: 1.0).")
    p.add_argument("--lang", default=None, help="Language code (default: en-us).")
    p.add_argument("--force", action="store_true",
                   help="Re-render even if MP3 is newer than source.")
    p.add_argument("--json", action="store_true", dest="json_mode",
                   help="Emit a single JSON object to stdout.")
    return p


def _emit_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    cfg = load_config()
    tts_cfg = cfg.agents.get("doc_to_audio", {}) if isinstance(cfg.agents, dict) else {}
    # The block lives at top-level [doc_to_audio], not under [agents.*]
    import tomllib
    with open(Path(__file__).parent.parent / "config.toml", "rb") as f:
        raw = tomllib.load(f)
    tts_cfg = raw.get("doc_to_audio", {})

    voice = args.voice or tts_cfg.get("default_voice", "af_heart")
    speed = args.speed if args.speed is not None else tts_cfg.get("default_speed", 1.0)
    lang = args.lang or tts_cfg.get("default_lang", "en-us")
    max_chars = tts_cfg.get("max_chars_per_chunk", 400)
    silence_ms = tts_cfg.get("section_silence_ms", 200)
    mp3_quality = tts_cfg.get("mp3_quality", 2)

    model_path = (cfg.repo_root / tts_cfg.get(
        "model_path", "agents-sdk/models/kokoro/kokoro-v1.0.onnx")).resolve()
    voices_path = (cfg.repo_root / tts_cfg.get(
        "voices_path", "agents-sdk/models/kokoro/voices-v1.0.bin")).resolve()
    out_dir_default = cfg.repo_root / tts_cfg.get("output_dir", "vault/90_system/audio")
    out_dir = Path(args.out_dir).resolve() if args.out_dir else out_dir_default.resolve()

    source = Path(args.source).resolve()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)

    if not source.exists():
        msg = f"source not found: {source}"
        logger.error(msg)
        if args.json_mode:
            _emit_json({"status": "error", "reason": msg})
        else:
            print(msg, file=sys.stderr)
        return 2

    output = audio_path_for_source(source, out_dir)
    if should_skip_idempotent(source, output, force=args.force):
        result = RenderResult(
            source_path=source, output_path=output,
            duration_sec=0.0, segments_synthesized=0,
            voice=voice, speed=speed, skipped=True,
            reason="mp3 mtime >= source mtime",
        )
        if args.json_mode:
            _emit_json({
                "status": "skipped",
                "reason": result.reason,
                "output_path": str(output),
                "voice": voice,
            })
        else:
            print(f"skip: {output} is up to date (use --force to override)")
        return 0

    if not model_path.exists() or not voices_path.exists():
        msg = f"model files missing: {model_path} or {voices_path}"
        logger.error(msg)
        if args.json_mode:
            _emit_json({"status": "error", "reason": msg})
        else:
            print(msg, file=sys.stderr)
        return 3

    start = time.monotonic()
    try:
        kokoro = load_kokoro(model_path, voices_path)
        result = render_document(
            source=source, output=output, kokoro=kokoro,
            voice=voice, speed=speed, lang=lang,
            max_chars=max_chars, section_silence_ms=silence_ms,
            mp3_quality=mp3_quality,
        )
    except Exception as exc:
        logger.exception("render failed: %s", exc)
        record_run(cfg.log_dir, AGENT_NAME, mode=None, status="error",
                   cost_usd=0.0, duration_ms=int((time.monotonic() - start) * 1000),
                   turns=None, notes=str(exc)[:200])
        if args.json_mode:
            _emit_json({"status": "error", "reason": str(exc)})
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    elapsed_ms = int((time.monotonic() - start) * 1000)
    if args.json_mode:
        _emit_json({
            "status": "ok",
            "output_path": str(result.output_path),
            "duration_sec": round(result.duration_sec, 2),
            "segments_synthesized": result.segments_synthesized,
            "voice": voice,
            "speed": speed,
            "elapsed_ms": elapsed_ms,
        })
    else:
        print(f"wrote {result.output_path}  ({result.duration_sec:.1f}s audio, "
              f"{result.segments_synthesized} segments, {elapsed_ms} ms wall)")

    record_run(cfg.log_dir, AGENT_NAME, mode=None, status="success",
               cost_usd=0.0, duration_ms=elapsed_ms, turns=None,
               notes=f"voice={voice} dur={result.duration_sec:.1f}s segs={result.segments_synthesized}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the CLI tests**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_doc_to_audio_cli.py -v 2>&1 | tail -30
```
Expected: all 7 CLI tests PASS.

- [ ] **Step 6: Run the full test suite to confirm no regressions**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q 2>&1 | tail -10
```
Expected: full suite passes; the new tests show up in the count.

- [ ] **Step 7: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/scripts/doc_to_audio.py agents-sdk/tests/test_doc_to_audio_cli.py agents-sdk/config.toml && \
  git commit -m "feat(agents-sdk): doc_to_audio CLI for verbatim local TTS"
```

> **REVIEW CHECKPOINT 2 (per user prompt section "Execution shape"):** Script scaffold passes on the canonical test doc. STOP here for Sean's review before Task 6 runs the real end-to-end render.

---

## Task 6: End-to-end run on the canonical test doc + verbatim verification

**Files:**
- Create (by running the script): `vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3`
- Create: `vault/90_system/audio/.gitkeep`

This is the first time the real Kokoro model runs over a real vault document. Verbatim accuracy is verified by listening to the first 60 seconds against the source.

- [ ] **Step 1: Create the audio output directory with .gitkeep**

```bash
mkdir -p /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio && \
  touch /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio/.gitkeep
```

- [ ] **Step 2: Render the canonical test doc**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py \
    --source ../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
```
Expected: a line like `wrote /Users/seanwinslow/.../vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3  (NN.Ns audio, MM segments, KK ms wall)`. For a ~3000-word doc at 1.0× speed, expect roughly 18-25 minutes of audio.

- [ ] **Step 3: Verify the file landed and has reasonable size**

```bash
ls -lh /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3 && \
  ffprobe -v error -show_entries format=duration -of csv=p=0 \
    /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3
```
Expected: MP3 size in the 15-30MB range; duration in seconds roughly 1000-1500 for a 3000-word doc at speed 1.0.

- [ ] **Step 4: Auto-listen the first 60 seconds (Sean's verbatim check)**

```bash
afplay -t 60 /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3
```
Sean must confirm:
- [ ] The frontmatter (`type: retrofit-plan`, `status: tier-1-shipped-...`) does NOT appear in the audio.
- [ ] The H1 "Vault Synthesizer v2 — Retrofit Tiers" is spoken once at the start.
- [ ] The paragraph "On 2026-05-13 morning, after a clean nightly synth run (203 concepts, 111 connections, 186 typed edges, status=ok), Sean and Claude ran `scripts/query.py` ..." is spoken **verbatim** — every number, every comma, no paraphrasing.
- [ ] The wikilink to `query.py` reads as "scripts/query.py" or similar (the visible display text), not as "double bracket".
- [ ] No audible seams between sentence chunks.

- [ ] **Step 5: Re-run to confirm idempotency**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py \
    --source ../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
```
Expected: `skip: .../vault/90_system/audio/2026-05-13-vault-synthesizer-retrofit-tiers.mp3 is up to date (use --force to override)` — and the script exits quickly without invoking Kokoro.

- [ ] **Step 6: Confirm `--force` re-renders**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py \
    --source ../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md \
    --force --json | tee /tmp/doc-to-audio-result.json
python3 -c "import json; d=json.load(open('/tmp/doc-to-audio-result.json')); assert d['status']=='ok'; print('JSON mode OK')"
```
Expected: a JSON line with `"status": "ok"` and the MP3 mtime gets refreshed.

- [ ] **Step 7: Commit the .gitkeep**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add vault/90_system/audio/.gitkeep && \
  git commit -m "feat(vault): create audio output directory for doc_to_audio MP3s"
```

> **REVIEW CHECKPOINT 3 (per user prompt section "Execution shape"):** Idempotency + chaptering polish verified. STOP for Sean's confirmation before docs are updated.

---

## Task 7: Update CHANGELOG.md, CLAUDE.md, README.md (per "Non-Negotiable Rules")

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`

- [ ] **Step 1: Determine the current version**

```bash
head -20 /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CHANGELOG.md
```
Note the most recent `## [X.Y.Z]` heading. The new entry goes either under that one's "Added" section (if it's unreleased) or as a new minor version (e.g., v3.36.0).

- [ ] **Step 2: Add the CHANGELOG entry**

Under the appropriate version's `### Added` subsection, insert this exact bullet (preserving the surrounding markdown formatting):

```markdown
- **Local TTS pipeline (`doc_to_audio.py`)** — verbatim narration of vault markdown via Kokoro-82M ONNX. New CLI at `agents-sdk/scripts/doc_to_audio.py`, preprocessing module `lib/markdown_to_speech.py`, synthesis wrapper `lib/kokoro_synth.py`. Apache 2.0, $0/run, single voice (default `af_heart`), Mac Mini primary host. Decision record at `agents-sdk/docs/local-tts-decision-record.md` captures the `kokoro-onnx` vs hexgrad/`kokoro` choice. Output: `vault/90_system/audio/<source-stem>.mp3`. Idempotent on mtime; `--force` re-renders. New deps: `kokoro-onnx>=0.5.0`, `soundfile>=0.12`. Model weights (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) live under `agents-sdk/models/kokoro/` (gitignored; SHA-256 in `CHECKSUMS.txt`). 28 new tests (`tests/test_markdown_to_speech.py`, `tests/test_kokoro_synth.py`, `tests/test_doc_to_audio_cli.py`). Skill / agent / hook counts unchanged — this is a script, not an agent.
```

- [ ] **Step 3: Update CLAUDE.md — Commands and Architecture sections**

In `CLAUDE.md`:

**(a)** Under the `## Commands` block (around the existing `scripts/install.sh` example), add this new code-fence example:

```bash
# Render a vault doc to MP3 (local Kokoro-82M, $0/run)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py \
  --source ../vault/20_projects/research/2026-05-13-foo.md
```

**(b)** In the architecture block (around the `agents-sdk/` tree), update the comment on `scripts/` to mention `doc_to_audio.py`. If the tree explicitly enumerates scripts, add `doc_to_audio.py` to it. If `agents-sdk/models/` is referenced anywhere, add a one-liner that it now holds Kokoro weights (gitignored).

**(c)** In the `## Connected External Research APIs` section (or as a new subsection right after it), add this paragraph:

```markdown
**Local TTS (NEW v3.36.0)** is available via `agents-sdk/scripts/doc_to_audio.py` — verbatim narration of vault markdown using Kokoro-82M ONNX (Apache 2.0, ~88MB int8 quantized model, $0/run). Single voice (default `af_heart`), Apple Silicon native via `kokoro-onnx`. Output lands at `vault/90_system/audio/<source-stem>.mp3`. Idempotent — re-running skips when MP3 mtime ≥ source MD mtime. Decision record + tradeoffs at [`agents-sdk/docs/local-tts-decision-record.md`](agents-sdk/docs/local-tts-decision-record.md). **Setup on a fresh machine (Mac Mini after `git pull`, or a re-clone): run `agents-sdk/scripts/install_tts_models.sh`** — installs the two Python deps, downloads the ~115MB model + voices binaries (gitignored), and verifies SHA-256 against the tracked `CHECKSUMS.txt`. Rollback at [`agents-sdk/docs/local-tts-rollback.md`](agents-sdk/docs/local-tts-rollback.md).
```

- [ ] **Step 4: Update README.md**

In `README.md`:

**(a)** If README has a "Scripts" or "Tools" table/list, add an entry for `doc_to_audio.py` with a one-line description.

**(b)** If README has a version/feature summary at the top, mention the new TTS capability ("Local verbatim TTS for vault markdown via Kokoro-82M").

**(c)** If README explicitly counts scripts in agents-sdk, increment by one (or update the count line).

- [ ] **Step 5: Run the validator**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  python3 scripts/validate.py 2>&1 | tail -20
```
Expected: validator passes. If it complains about counts, recheck the CLAUDE.md / README.md updates.

- [ ] **Step 6: Commit the doc updates**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add CHANGELOG.md CLAUDE.md README.md && \
  git commit -m "docs: register doc_to_audio.py local TTS pipeline (v3.36.0)"
```

> **REVIEW CHECKPOINT 4 (per user prompt section "Execution shape"):** Docs updated. STOP for final Sean confirmation before any optional follow-on work.

---

## Task 8: Spotify integration — sketch only, do NOT implement

**Files:**
- Create: `agents-sdk/docs/local-tts-spotify-handoff.md`

The user explicitly said: "Save-to-Spotify integration — sketch only, do not implement in this pass — leave a clear handoff point for a follow-up phase." This task delivers exactly that handoff doc.

- [ ] **Step 1: Write the handoff doc**

Create `agents-sdk/docs/local-tts-spotify-handoff.md` with this exact content:

```markdown
---
type: handoff-doc
created: 2026-05-15
status: deferred — gated on local TTS pipeline being stable across 10+ runs
---

# Save-to-Spotify Handoff — Sean's Research Briefings

## What this is

A handoff point for a future phase that pipes finished MP3s from
`vault/90_system/audio/` into Spotify's [`save-to-spotify`](https://github.com/spotify/save-to-spotify)
CLI as a private podcast / show titled "Sean's Research Briefings."

## Why deferred

The local TTS pipeline must prove itself on the verbatim guarantee and
chunking quality before adding a publishing leg. Re-open this doc once Sean
has listened end-to-end to at least 10 docs and the chaptering, prosody,
and idempotency feel right.

## Where to start when re-opening

1. **Verify save-to-spotify is the right tool.** As of 2026-05-15, the
   `spotify/save-to-spotify` repo state, license, and Spotify's private-show
   policy need fresh due diligence — none of it is being relied on yet.
   Spotify's "Anchor" / "Spotify for Podcasters" web UI may be a simpler
   route for a personal show than wiring a CLI.
2. **Define the show metadata model.** Each MP3 needs: episode title (from
   the source markdown H1 or filename), description (from the source's
   `description:` frontmatter or first paragraph), publish date (from
   filename prefix or frontmatter `created:`), cover art (probably a single
   static image reused across episodes).
3. **Decide the trigger.** Three options:
    - **a)** Manual `python3 scripts/publish_to_spotify.py --source x.mp3`
    - **b)** Auto-publish on every doc_to_audio run (extend the CLI)
    - **c)** Nightly batch — a new SDK agent that walks
      `vault/90_system/audio/` and publishes anything new
   Recommendation: start with (a). Promote to (c) only after 5+ uneventful
   manual runs.
4. **Authentication.** Spotify's API uses OAuth 2.0. Tokens belong in macOS
   Keychain via `agents-sdk/lib/keychain.py`, never in config.toml.
5. **Rollback.** Deleting a published episode is reversible via Spotify's UI
   — but URLs cached by clients may persist. Build the script to ALWAYS
   publish as DRAFT first; promote-to-live is a separate manual step.

## Handoff interface

The local TTS pipeline already gives you everything you need:

- **MP3 path:** `vault/90_system/audio/<source-stem>.mp3` — predictable from
  the source markdown path.
- **JSON output:** `doc_to_audio.py --json` emits `output_path`,
  `duration_sec`, `voice`, `speed`, `segments_synthesized` — perfect for a
  publisher script to consume via subprocess.
- **Idempotency:** the MP3 mtime tells you whether the source has been
  re-rendered and therefore whether to re-publish.

No changes to `doc_to_audio.py` itself are needed to support this. The
publisher is purely additive.

## Do NOT do in this phase

- Modify `doc_to_audio.py` to include a `--publish` flag (couples the
  layers).
- Add a `[spotify]` block to `config.toml` (premature).
- Pre-install `save-to-spotify` (no idea yet whether it's the right tool).

## When ready

Run a separate `/writing-plans` session with this doc as the spec input.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/docs/local-tts-spotify-handoff.md && \
  git commit -m "docs(agents-sdk): Spotify handoff sketch for local TTS (deferred)"
```

---

## Task 9: Document the rollback procedure (one terminal block per the user's "Hard constraints")

**Files:**
- Create: `agents-sdk/docs/local-tts-rollback.md`

Per the user prompt: "Rollback — exact uninstall steps (pip uninstalls, model file rm, generated MP3 cleanup) if Kokoro proves unsuitable. Should be one terminal block I can run."

- [ ] **Step 1: Write the rollback doc**

Create `agents-sdk/docs/local-tts-rollback.md` with this exact content:

````markdown
---
type: rollback-guide
created: 2026-05-15
applies_to: doc_to_audio.py (local Kokoro TTS pipeline)
---

# Local TTS Rollback

If Kokoro proves unsuitable, run this one block to fully remove the pipeline:

```bash
# 1. Stop using the script — no running services to kill (CLI only).

# 2. Uninstall Python deps from agents-sdk/.venv
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  .venv/bin/python3 -m pip uninstall -y kokoro-onnx soundfile

# 3. Remove model weights (preserves CHECKSUMS.txt for re-download reference)
rm -f /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/kokoro-v1.0.onnx
rm -f /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/models/kokoro/voices-v1.0.bin

# 4. Remove generated MP3s (keeps the .gitkeep so vault/90_system/audio/ stays tracked)
find /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/audio -maxdepth 1 -name "*.mp3" -delete

# 5. Remove script + lib + tests + config block (use git revert if commits are local)
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  rm -f agents-sdk/scripts/doc_to_audio.py \
        agents-sdk/lib/markdown_to_speech.py \
        agents-sdk/lib/kokoro_synth.py \
        agents-sdk/tests/test_markdown_to_speech.py \
        agents-sdk/tests/test_kokoro_synth.py \
        agents-sdk/tests/test_doc_to_audio_cli.py

# 6. Manually remove the [doc_to_audio] block from agents-sdk/config.toml
#    (search for the v3.36.0 marker comment).

# 7. Manually remove the CHANGELOG.md / CLAUDE.md / README.md entries added in v3.36.0.

# 8. Verify clean state
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk && \
  .venv/bin/python3 -c "import kokoro_onnx" 2>&1 | grep -q ModuleNotFound && echo "deps removed OK"
```

To **partially roll back** (keep the model and deps but stop generating new
MP3s), simply delete `agents-sdk/scripts/doc_to_audio.py` — nothing else
depends on it.

To **swap to hexgrad/`kokoro`** instead of removing the feature, see the
decision record at `agents-sdk/docs/local-tts-decision-record.md` — the swap
is a ~10-line change in `lib/kokoro_synth.py` plus `pip install kokoro
soundfile misaki[en]` and an espeak-ng homebrew install.
````

- [ ] **Step 2: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && \
  git add agents-sdk/docs/local-tts-rollback.md && \
  git commit -m "docs(agents-sdk): rollback guide for local TTS pipeline"
```

---

## Self-Review (skill-required)

**1. Spec coverage** — every bullet from the user's prompt mapped to a task:

| User-prompt bullet | Task |
|---|---|
| Dependencies & install (kokoro-onnx vs kokoro), venv choice, Apple Silicon, license due diligence | Tasks 0, 1 |
| Script architecture mirroring `query.py`, `--json` mode, sensible defaults | Task 5 |
| Markdown preprocessing — verbatim, frontmatter, code fences, wikilinks, links, headings as section breaks | Task 3 |
| Voice & chunking (default voice, speech rate, length limit handling) | Tasks 2 (smoke), 4 (chunker), 5 (config defaults) |
| Output handling (`vault/90_system/audio/`, mirrored filename, mtime idempotency) | Task 5 + Task 6 |
| Save-to-Spotify — sketch only | Task 8 |
| Verification on canonical retrofit doc | Task 6 |
| Rollback as one terminal block | Task 9 |
| Reference files consulted (CLAUDE.md, config.toml, query.py, lib/, canonical doc) | Done in plan preamble |
| Hard constraints — $0/run, verbatim, single voice, plan-before-install, Apple Silicon, mandatory doc updates | Honored throughout; doc updates in Task 7 |
| Execution shape with 4 review checkpoints | Wired into Tasks 2, 5, 6, 7 |

**2. Placeholder scan** — no "TBD", no "add appropriate error handling", no "similar to Task N", no unspecified code. Every code block is complete and runnable.

**3. Type consistency** — `Segment` / `SectionBreak` / `Element` are defined in `lib/markdown_to_speech.py` (Task 3), re-imported by `lib/kokoro_synth.py` (Task 4) and `scripts/doc_to_audio.py` (Task 5). `chunk_sentences()` signature matches across test and implementation. `KokoroLike.create()` signature `(text, voice, speed, lang) -> (np.ndarray, int)` is identical in `FakeKokoro` (tests), `synthesize_elements()` (lib), and `load_kokoro()` (CLI). `RenderResult` defined and used only in `scripts/doc_to_audio.py`. `SAMPLE_RATE = 24000` constant defined in `lib/kokoro_synth.py`, imported by tests.

**4. Skipped: nothing.** This plan does not depend on any external work being done first beyond the user's approval to start Task 1.

---

## Execution Choice

**Two options for executing this plan:**

**1. Subagent-Driven (recommended for this plan)** — Each task ships as an independent unit with green tests before the next starts; the four explicit REVIEW CHECKPOINTs map cleanly onto subagent handoffs. Fresh subagent per task, two-stage review between them.

**2. Inline Execution** — Run tasks in this session with batch execution and the four checkpoints as natural stop points.

**Which approach?**
