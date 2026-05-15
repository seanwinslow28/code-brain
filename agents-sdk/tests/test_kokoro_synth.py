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
