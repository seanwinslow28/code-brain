# tests/discovery/test_verify.py
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint
from council.discovery.verify import verify_pain_points


def _bundle():
    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "exports fail silently", 9))
    return b


def test_grounded_point_verifies():
    pt = CandidatePainPoint("Export loss", "s", quotes=["exports fail silently"], urls=["https://r.com/1"])
    out = verify_pain_points([pt], _bundle())
    assert out[0].verified is True
    assert out[0].supporting_urls == ["https://r.com/1"]


def test_fabricated_url_fails():
    pt = CandidatePainPoint("Fake", "s", quotes=["exports fail silently"], urls=["https://made-up.com/x"])
    out = verify_pain_points([pt], _bundle())
    assert out[0].verified is False
    assert out[0].supporting_urls == []


def test_real_url_but_quote_not_present_fails():
    pt = CandidatePainPoint("Drift", "s", quotes=["totally different invented complaint"], urls=["https://r.com/1"])
    out = verify_pain_points([pt], _bundle())
    assert out[0].verified is False


def test_embedding_attack_fails():
    # A fabricated long "quote" that merely EMBEDS the real bundle quote must NOT verify.
    pt = CandidatePainPoint(
        "Embedded fabrication", "s",
        quotes=["exports fail silently because the vendor secretly sells your data"],
        urls=["https://r.com/1"],
    )
    out = verify_pain_points([pt], _bundle())
    assert out[0].verified is False
    assert out[0].supporting_urls == []
