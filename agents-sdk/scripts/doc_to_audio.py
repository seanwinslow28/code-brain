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
import tomllib
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
    # errors="strict": this is a verbatim pipeline — surface encoding corruption
    # loudly rather than substitute replacement characters that would be spoken
    # as "question mark" in the MP3. If a vault doc has malformed UTF-8 we want
    # to fix the source, not narrate the corruption.
    text = source.read_text(encoding="utf-8", errors="strict")
    elements: list[Element] = preprocess(text)
    # Count both Segment and SectionBreak — every element either speaks text
    # or inserts a silence+title cue, so both contribute to the audio output.
    element_count = sum(1 for e in elements if isinstance(e, Segment)) \
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
        duration_sec=duration, segments_synthesized=element_count,
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
    # [doc_to_audio] sits at top-level (not under [agents.*]) — read directly.
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
