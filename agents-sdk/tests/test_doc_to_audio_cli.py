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
