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
