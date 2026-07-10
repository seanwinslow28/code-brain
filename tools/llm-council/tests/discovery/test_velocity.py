from council.discovery.velocity import (
    VelocitySignal, _series_slope, _normalize, VELOCITY_NORM_NEUTRAL,
)


def test_series_slope_sign_and_bounds():
    assert _series_slope([10, 20, 30, 40, 50]) > 0        # rising
    assert _series_slope([50, 40, 30, 20, 10]) < 0        # falling
    assert _series_slope([30, 30, 30, 30]) == 0.0         # flat
    assert _series_slope([1]) == 0.0                       # too few points
    assert _series_slope([]) == 0.0
    steep = _series_slope([1, 50, 100, 100, 100])
    assert -1.0 <= steep <= 1.0                            # clamped


def test_normalize_maps_flat_to_neutral_and_stays_bounded():
    assert _normalize(0.0) == VELOCITY_NORM_NEUTRAL        # flat -> 0.5
    assert _normalize(1.0) == 1.0
    assert _normalize(-1.0) == 0.0
    assert 0.5 < _normalize(0.4) < 1.0                     # rising -> above neutral
    assert 0.0 < _normalize(-0.4) < 0.5                    # falling -> below neutral


def test_velocity_signal_is_frozen():
    import dataclasses
    s = VelocitySignal(term="x", slope=0.4, normalized=0.7, source="pytrends",
                       window_days=90, points=5)
    assert s.term == "x" and s.normalized == 0.7
    try:
        s.slope = 1.0  # type: ignore[misc]
        assert False, "should be frozen"
    except dataclasses.FrozenInstanceError:
        pass


def test_velocity_module_never_imports_the_gate():
    # THE INVARIANT, source-level: the channel must never IMPORT the gate. (The docstring may
    # explain the invariant using the word "verify", so assert on import statements, not substrings.)
    import pathlib
    src = pathlib.Path(__file__).resolve().parents[2] / "council" / "discovery" / "velocity.py"
    text = src.read_text()
    assert "from council.discovery.verify" not in text
    assert "import verify" not in text
    import council.discovery.velocity as V
    assert not hasattr(V, "verify"), "velocity.py must not bind the gate module"


import council.discovery.velocity as V
from council.discovery.velocity import PytrendsProvider, get_velocity_provider


def test_provider_maps_rising_series_to_signal_and_caches():
    calls = []

    def fake_fetch(terms, window_days):
        calls.append(list(terms))
        return {t: [10, 20, 30, 40, 50] for t in terms}

    p = PytrendsProvider(fetch=fake_fetch, window_days=90)
    out = p.measure_batch(["ai code review", "ai code review", "mcp auth"])  # dupe collapses
    assert out["mcp auth"].normalized > 0.5 and out["mcp auth"].source == "pytrends"
    assert out["ai code review"].points == 5
    # second call for an already-measured term hits cache, not fetch
    p.measure_batch(["mcp auth"])
    assert sum(len(c) for c in calls) == 2  # only the 2 unique terms ever fetched


def test_provider_thin_series_and_failures_become_none():
    def fake_fetch(terms, window_days):
        return {terms[0]: [42]}            # one thin (single-point) series; others absent

    p = PytrendsProvider(fetch=fake_fetch)
    out = p.measure_batch(["thin", "missing"])
    assert out["thin"] is None and out["missing"] is None


def test_provider_never_raises_when_fetch_explodes():
    def boom(terms, window_days):
        raise RuntimeError("rate limited")

    out = PytrendsProvider(fetch=boom).measure_batch(["a", "b"])
    assert out == {"a": None, "b": None}


def test_measure_batch_chunks_terms_beyond_five():
    calls = []
    def fake_fetch(terms, window_days):
        calls.append(list(terms))
        return {t: [10, 20, 30, 40, 50] for t in terms}
    p = PytrendsProvider(fetch=fake_fetch)
    terms = [f"term {i}" for i in range(7)]
    out = p.measure_batch(terms)
    assert len(calls) == 2 and [len(c) for c in calls] == [5, 2]   # chunked by 5
    assert all(out[t] is not None for t in terms)                   # all resolved


def test_get_velocity_provider_env_gating(monkeypatch):
    monkeypatch.delenv("DISCOVERY_VELOCITY", raising=False)
    assert get_velocity_provider() is None                         # default: off
    monkeypatch.setenv("DISCOVERY_VELOCITY", "pytrends")
    monkeypatch.setattr(V, "_pytrends_available", lambda: False)
    assert get_velocity_provider() is None                         # opted-in but not installed
    monkeypatch.setattr(V, "_pytrends_available", lambda: True)
    assert isinstance(get_velocity_provider(), PytrendsProvider)   # opted-in and available
