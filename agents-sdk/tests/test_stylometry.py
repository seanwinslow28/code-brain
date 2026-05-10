"""Tests for stylometry module."""
import math
import pytest
from lib.skill_optimizer.stylometry import extract_features


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
