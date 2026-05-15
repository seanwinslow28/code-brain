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
