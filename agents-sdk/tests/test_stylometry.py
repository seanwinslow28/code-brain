"""Tests for stylometry module."""
import math
import pytest
from lib.skill_optimizer.stylometry import (
    extract_features,
    extract_distinctive_ngrams,
    extract_voice_corpus_chunks,
    compute_distance,
)


class TestExtractVoiceCorpusChunks:
    SAMPLE = (
        "# Voice Samples\n\n"
        "> _Note: em dashes normalized. This is an editor note, not voice._\n\n"
        "### A real story\n"
        "> " + ("I was hammered drunk on the ferry with my hoodlum friends and we "
                "passed out under the seats again that night. ") * 4 + "\n\n"
        "**Signature moves:** Pop Culture Anchoring; Hard Cut deflation; the SKILL.md table.\n\n"
        "**Why it works:** mundane accumulation builds to a pivot in the calibration corpus.\n\n"
        "**AI wrote:** \"Every rep is a vote for the person you're becoming.\"\n"
    )

    def test_keeps_blockquoted_voice(self):
        chunks = extract_voice_corpus_chunks(self.SAMPLE)
        joined = " ".join(chunks).lower()
        assert "hoodlum friends" in joined
        assert len(chunks) >= 1

    def test_excludes_meta_commentary_and_notes(self):
        joined = " ".join(extract_voice_corpus_chunks(self.SAMPLE)).lower()
        # Document analysis vocabulary must NOT leak into the corpus.
        assert "signature moves" not in joined
        assert "skill.md" not in joined and "skill md" not in joined
        assert "why it works" not in joined
        assert "editor note" not in joined  # italic `>` note is dropped
        assert "every rep is a vote" not in joined  # AI-wrote line excluded


class TestExtractFeatures:
    def test_returns_expected_keys(self):
        text = "Hello world. This is a test."
        features = extract_features(text)
        assert set(features.keys()) == {
            "sentence_length_mean",
            "sentence_length_stdev",
            "comma_density_per_100w",
            "em_dash_density_per_100w",
            "first_person_freq_per_100w",
        }

    def test_sentence_length_mean(self):
        text = "One two three. Four five six."
        features = extract_features(text)
        assert features["sentence_length_mean"] == pytest.approx(3.0)

    def test_comma_density(self):
        # 4 commas in 20 words → 20.0 per 100w
        text = "a, b, c, d, e f g h i j k l m n o p q r s t."
        features = extract_features(text)
        assert features["comma_density_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_em_dash_density(self):
        # 2 em dashes in 10 words → 20.0 per 100w
        text = "one two — three four — five six seven eight nine ten."
        features = extract_features(text)
        assert features["em_dash_density_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_first_person_freq(self):
        # "I" appears twice in 10 words → 20.0 per 100w
        text = "I went and I came back home for dinner tonight."
        features = extract_features(text)
        assert features["first_person_freq_per_100w"] == pytest.approx(20.0, rel=0.01)

    def test_handles_empty_string(self):
        features = extract_features("")
        assert features["sentence_length_mean"] == 0.0
        assert features["comma_density_per_100w"] == 0.0


class TestExtractDistinctiveNgrams:
    def test_returns_top_n_results(self):
        target = "the kind of thing that happens on a Tuesday and we never talk about it"
        baseline = "the the the the the the the the the the"
        ngrams = extract_distinctive_ngrams(target, [baseline], top_n=5, ns=(2, 3))
        assert len(ngrams) <= 5

    def test_returns_target_specific_ngrams(self):
        target = "kind of thing kind of thing kind of thing"
        baseline = "the dog ran fast and the cat slept slowly in the sun"
        ngrams = extract_distinctive_ngrams(target, [baseline], top_n=10, ns=(2, 3))
        # "kind of" should appear in the distinctive set
        ngram_strings = [" ".join(ng) for ng in ngrams]
        assert any("kind of" in s for s in ngram_strings)

    def test_handles_empty_target(self):
        ngrams = extract_distinctive_ngrams("", ["any baseline"], top_n=5, ns=(2,))
        assert ngrams == []


class TestComputeDistance:
    def test_zero_distance_when_identical(self):
        baseline = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
            "_stdevs": {  # required for z-score
                "sentence_length_mean": 1.0,
                "sentence_length_stdev": 0.5,
                "comma_density_per_100w": 1.0,
                "em_dash_density_per_100w": 0.3,
                "first_person_freq_per_100w": 0.5,
            },
            "_ngrams": [],
        }
        target_features = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
        }
        d = compute_distance(target_features, baseline, target_text="hello")
        assert d == pytest.approx(0.0, abs=0.5)  # may include n-gram component

    def test_increases_with_feature_divergence(self):
        baseline = {
            "sentence_length_mean": 10.0,
            "sentence_length_stdev": 2.0,
            "comma_density_per_100w": 5.0,
            "em_dash_density_per_100w": 1.0,
            "first_person_freq_per_100w": 3.0,
            "_stdevs": {
                "sentence_length_mean": 1.0,
                "sentence_length_stdev": 0.5,
                "comma_density_per_100w": 1.0,
                "em_dash_density_per_100w": 0.3,
                "first_person_freq_per_100w": 0.5,
            },
            "_ngrams": [],
        }
        close = {"sentence_length_mean": 10.5, "sentence_length_stdev": 2.0,
                 "comma_density_per_100w": 5.0, "em_dash_density_per_100w": 1.0,
                 "first_person_freq_per_100w": 3.0}
        far = {"sentence_length_mean": 25.0, "sentence_length_stdev": 8.0,
               "comma_density_per_100w": 0.5, "em_dash_density_per_100w": 0.0,
               "first_person_freq_per_100w": 0.5}
        d_close = compute_distance(close, baseline, target_text="x")
        d_far = compute_distance(far, baseline, target_text="x")
        assert d_far > d_close
