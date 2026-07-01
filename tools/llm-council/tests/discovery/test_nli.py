import importlib
import council.discovery.nli as nli


def test_get_scorer_returns_none_when_onnxruntime_missing(monkeypatch):
    nli.reset_scorer_cache()
    real_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __import__
    def fake_import(name, *a, **k):
        if name == "onnxruntime":
            raise ImportError("no onnxruntime")
        return real_import(name, *a, **k)
    monkeypatch.setattr("builtins.__import__", fake_import)
    assert nli.get_scorer() is None


def test_get_scorer_returns_none_when_model_dir_absent(monkeypatch, tmp_path):
    nli.reset_scorer_cache()
    monkeypatch.setenv("DISCOVERY_NLI_MODEL_DIR", str(tmp_path / "nope"))
    # onnxruntime may or may not be installed; either way a missing model dir -> None
    assert nli.get_scorer() is None


def test_scorer_cache_is_singleton(monkeypatch, tmp_path):
    nli.reset_scorer_cache()
    monkeypatch.setenv("DISCOVERY_NLI_MODEL_DIR", str(tmp_path / "nope"))
    a = nli.get_scorer()
    b = nli.get_scorer()
    assert a is b  # both None, cached without re-attempting load


import pytest
import council.discovery.nli as nli


@pytest.mark.skipif(nli.get_scorer() is None, reason="NLI model not installed (run scripts/install_nli_model.sh)")
def test_real_model_entails_paraphrase():
    nli.reset_scorer_cache()
    s = nli.get_scorer()
    high = s.entails(premise="exporting silently drops rows", hypothesis="the export loses data")
    low = s.entails(premise="exporting silently drops rows", hypothesis="it has excellent SSO support")
    assert high > low
    assert high >= 0.5
