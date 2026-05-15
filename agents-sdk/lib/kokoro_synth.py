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
_COMMA_SPLIT_RE = re.compile(r"(?<=,)\s+")


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
        candidate = (buf + " " + p).strip() if buf else p
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
