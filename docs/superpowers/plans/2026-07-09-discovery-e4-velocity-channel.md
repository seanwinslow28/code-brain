# E4 Velocity Scoring Channel — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give each discovery idea card a real "why now" — a demand *slope* fed into the score, never into the fabrication gate.

**Architecture:** A new isolated `velocity.py` channel produces a *number* (a normalized demand slope) that reaches only `score_opportunity` / `ScoreBreakdown` / `_why_now`. It is resolved and used strictly *after* the verify gate, mirroring E1's `nli.get_scorer()→None` optional-dependency seam. Default is a no-op (no provider → scores byte-identical to today); pytrends is opt-in via `DISCOVERY_VELOCITY=pytrends`. The velocity weight ships at 0.0, so nothing re-ranks until Sean turns it up.

**Tech Stack:** Python 3, `uv` + `pytest` (async via `pytest.mark.asyncio`). Optional runtime dep: `pytrends` (never a hard dependency; all tests are offline).

## Global Constraints

- **THE LOAD-BEARING INVARIANT:** velocity is a SCORE signal ONLY, NEVER gate-evidence. `velocity.py` imports **nothing** from `verify.py` or any `EvidenceBundle`-write path; it takes plain `str` terms and returns numbers. The provider is resolved/used strictly *after* `verify_pain_points`/`citation_metrics`.
- **Default weight = 0.0** (`VELOCITY_WEIGHT`). Shipping E4 must leave every existing card's composite byte-identical until the weight is raised. Always report the raw slope (`velocity_raw`) so a regression is visible.
- **Weight resolution is a `None`-check, never `or`:** `weight = VELOCITY_WEIGHT if velocity_weight is None else velocity_weight` (an explicit `0.0` must force the term off; `0.0` is falsy).
- **No live network in tests, ever.** pytrends is reached only through the injectable `_pytrends_fetch` seam; tests inject fakes / pure lists.
- **Never raises out of the channel:** any provider/network/parse failure maps that term to `None` (that card degrades to the recency-only `_why_now`).
- **Baseline:** `main` after PR #112 = **303 passed, 1 skipped**. The default (no-provider) path must keep the suite green.
- **Working dir for all test commands:** `tools/llm-council`. Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

## File Structure

- **Create** `council/discovery/velocity.py` — the channel: `VelocitySignal`, `VelocityProvider` protocol, slope/normalization math, `PytrendsProvider` (via injectable `_pytrends_fetch`), `get_velocity_provider()`.
- **Create** `tests/discovery/test_velocity.py`.
- **Modify** `council/discovery/scoring.py` — 4 new `ScoreBreakdown` fields, `VELOCITY_WEIGHT`/`VELOCITY_NEUTRAL`, velocity folding in `score_opportunity`.
- **Modify** `council/discovery/frame.py` — `_velocity_term`, batched measure in `frame_pm`, rewritten `_why_now`.
- **Modify** `council/discovery/pipeline.py` — `velocity_provider=_UNSET` resolution, thread `topic`+provider to `frame_pm`, session `velocity_mode` + `why_now_coverage` (both paths).
- **Modify** `tests/discovery/test_scoring.py`, `tests/discovery/test_frame.py`, `tests/discovery/test_pipeline.py`.
- **Modify** `pyproject.toml` — optional `pytrends` extra (Task 6).

---

### Task 1: `velocity.py` core — signal type + slope math + protocol + import guard

**Files:**
- Create: `council/discovery/velocity.py`
- Test: `tests/discovery/test_velocity.py`

**Interfaces:**
- Produces:
  - `VelocitySignal(term: str, slope: float, normalized: float, source: str, window_days: int, points: int)` (frozen dataclass).
  - `VelocityProvider` — `typing.Protocol` with `measure_batch(self, terms: list[str]) -> dict[str, VelocitySignal | None]`.
  - `_series_slope(values: list[float]) -> float` — OLS slope / mean, clamped to `[-1.0, 1.0]`; `0.0` for `< 2` points.
  - `_normalize(slope: float) -> float` — `clamp(0.5 + slope / 2, 0.0, 1.0)`.
  - `VELOCITY_NORM_NEUTRAL = 0.5`.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_velocity.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_velocity.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'council.discovery.velocity'`

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/velocity.py
"""E4 — velocity scoring channel. Produces a demand SLOPE (a number), fed ONLY into scoring —
never the verify gate, never the EvidenceBundle. Optional: get_velocity_provider() returns None
(no signal) unless DISCOVERY_VELOCITY=pytrends AND pytrends is importable, mirroring nli.get_scorer().
This module imports nothing from verify.py — that exclusion is the load-bearing moat invariant."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Protocol

_logger = logging.getLogger("council.discovery.velocity")

VELOCITY_NORM_NEUTRAL = 0.5   # normalized value of a flat / absent trend


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass(frozen=True)
class VelocitySignal:
    term: str
    slope: float        # raw OLS slope / mean, clamped to [-1, 1] (regression-visibility field)
    normalized: float   # 0-1 for scoring; 0.5 = flat
    source: str         # "pytrends"
    window_days: int
    points: int


class VelocityProvider(Protocol):
    def measure_batch(self, terms: list[str]) -> "dict[str, VelocitySignal | None]": ...


def _series_slope(values: list[float]) -> float:
    """OLS slope over 0..n-1, divided by the series mean (scale-independent), clamped to [-1, 1]."""
    n = len(values)
    if n < 2:
        return 0.0
    mean_x = (n - 1) / 2.0
    mean_y = sum(values) / n
    num = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    den = sum((i - mean_x) ** 2 for i in range(n))
    if den == 0:
        return 0.0
    slope = num / den
    return _clamp(slope / (mean_y or 1.0), -1.0, 1.0)


def _normalize(slope: float) -> float:
    return _clamp(0.5 + slope / 2.0, 0.0, 1.0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_velocity.py -q`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add council/discovery/velocity.py tests/discovery/test_velocity.py
git commit -m "feat(discovery-e4): velocity signal type + slope math + gate-import guard

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `PytrendsProvider` + `get_velocity_provider()` env gating

**Files:**
- Modify: `council/discovery/velocity.py`
- Test: `tests/discovery/test_velocity.py`

**Interfaces:**
- Consumes: `VelocitySignal`, `_series_slope`, `_normalize` (Task 1).
- Produces:
  - `_pytrends_fetch(terms: list[str], window_days: int) -> dict[str, list[float]]` — the ONLY seam that touches pytrends/pandas; tests monkeypatch it. Returns `{term: interest_series}`.
  - `_pytrends_available() -> bool` — import probe; tests monkeypatch it.
  - `PytrendsProvider(fetch=None, window_days=90)` implementing `measure_batch` (dedupes, caches per-term, chunks by 5, maps failures/thin series to `None`, never raises).
  - `get_velocity_provider() -> VelocityProvider | None` — `None` unless `DISCOVERY_VELOCITY=pytrends` and pytrends importable.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/discovery/test_velocity.py
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


def test_get_velocity_provider_env_gating(monkeypatch):
    monkeypatch.delenv("DISCOVERY_VELOCITY", raising=False)
    assert get_velocity_provider() is None                         # default: off
    monkeypatch.setenv("DISCOVERY_VELOCITY", "pytrends")
    monkeypatch.setattr(V, "_pytrends_available", lambda: False)
    assert get_velocity_provider() is None                         # opted-in but not installed
    monkeypatch.setattr(V, "_pytrends_available", lambda: True)
    assert isinstance(get_velocity_provider(), PytrendsProvider)   # opted-in and available
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_velocity.py -q`
Expected: FAIL with `ImportError: cannot import name 'PytrendsProvider'`

- [ ] **Step 3: Write minimal implementation**

```python
# append to council/discovery/velocity.py

def _dedup_preserve(terms: list[str]) -> list[str]:
    seen, out = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _chunks(items: list[str], n: int) -> "list[list[str]]":
    return [items[i:i + n] for i in range(0, len(items), n)]


def _pytrends_fetch(terms: list[str], window_days: int) -> "dict[str, list[float]]":
    """The ONLY pytrends/pandas touch point. Returns {term: interest_over_time series}.
    Isolated behind this function so all tests inject a pure-list fake and never hit the network."""
    from pytrends.request import TrendReq  # lazy: import cost + optional dep only when used
    req = TrendReq(hl="en-US", tz=0)
    req.build_payload(terms, timeframe=f"today {max(1, window_days // 30)}-m")
    df = req.interest_over_time()
    out: dict[str, list[float]] = {}
    for t in terms:
        if t in getattr(df, "columns", []):
            out[t] = [float(v) for v in df[t].tolist()]
    return out


def _pytrends_available() -> bool:
    try:
        import pytrends  # noqa: F401
        return True
    except Exception:
        return False


class PytrendsProvider:
    """Google-Trends demand slope. measure_batch dedupes, caches per-term, chunks by 5, and maps
    any failure or thin (<2 point) series to None. Never raises."""

    def __init__(self, fetch=None, window_days: int = 90):
        self._fetch = fetch or _pytrends_fetch
        self._window_days = window_days
        self._cache: dict[str, VelocitySignal | None] = {}

    def measure_batch(self, terms: list[str]) -> "dict[str, VelocitySignal | None]":
        out: dict[str, VelocitySignal | None] = {}
        todo: list[str] = []
        for t in _dedup_preserve(terms):
            if t in self._cache:
                out[t] = self._cache[t]
            else:
                todo.append(t)
        for group in _chunks(todo, 5):
            try:
                series_map = self._fetch(group, self._window_days)
            except Exception as e:  # rate-limit / network / parse — degrade this group to None
                _logger.warning("velocity fetch failed for %s (%s) — those cards degrade.", group, e)
                series_map = {}
            for t in group:
                vals = series_map.get(t) or []
                if len(vals) < 2:
                    sig = None
                else:
                    slope = _series_slope(vals)
                    sig = VelocitySignal(term=t, slope=round(slope, 4),
                                         normalized=round(_normalize(slope), 4),
                                         source="pytrends", window_days=self._window_days,
                                         points=len(vals))
                self._cache[t] = sig
                out[t] = sig
        return out


def get_velocity_provider() -> "VelocityProvider | None":
    """Lazy resolver. None (no signal) unless DISCOVERY_VELOCITY=pytrends and pytrends importable.
    Mirrors nli.get_scorer(): opt-in, degrades to None, never crashes a run."""
    if os.environ.get("DISCOVERY_VELOCITY", "").strip().lower() != "pytrends":
        return None
    if not _pytrends_available():
        _logger.warning("DISCOVERY_VELOCITY=pytrends but pytrends is not installed — velocity off.")
        return None
    return PytrendsProvider()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_velocity.py -q`
Expected: PASS (all Task 1 + Task 2 tests). Re-confirm the import guard still passes (the new code references no `verify`).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/velocity.py tests/discovery/test_velocity.py
git commit -m "feat(discovery-e4): pytrends provider + get_velocity_provider env gating

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `scoring.py` — velocity fields + bounded folding (weight defaults to 0)

**Files:**
- Modify: `council/discovery/scoring.py`
- Test: `tests/discovery/test_scoring.py`

**Interfaces:**
- Consumes: `VelocitySignal`, `VELOCITY_NORM_NEUTRAL` (Task 1).
- Produces:
  - `ScoreBreakdown` gains `velocity: float`, `velocity_raw: float`, `velocity_source: str`, `velocity_term: str` (appended after `evidence_date`).
  - Module constants `VELOCITY_WEIGHT = 0.0`, `VELOCITY_NEUTRAL = 0.5`.
  - `score_opportunity(..., velocity: VelocitySignal | None = None, velocity_weight: float | None = None)`.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/discovery/test_scoring.py
from council.discovery.scoring import VELOCITY_WEIGHT
from council.discovery.velocity import VelocitySignal


def _sig(normalized):
    return VelocitySignal(term="t", slope=(normalized - 0.5) * 2, normalized=normalized,
                          source="pytrends", window_days=90, points=5)


def test_velocity_weight_defaults_to_zero():
    assert VELOCITY_WEIGHT == 0.0


def test_no_velocity_signal_is_neutral_and_marks_empty_source():
    s = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY)
    assert s.velocity == 0.5 and s.velocity_raw == 0.0
    assert s.velocity_source == "" and s.velocity_term == ""


def test_default_weight_leaves_composite_identical_even_with_a_rising_signal():
    base = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY)
    with_sig = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY, velocity=_sig(0.95))
    assert with_sig.composite == base.composite            # weight 0 -> byte-identical
    assert with_sig.velocity == 0.95 and with_sig.velocity_source == "pytrends"  # but reported


def test_positive_weight_boosts_rising_and_discounts_falling_bounded():
    base = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY)
    up = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY,
                           velocity=_sig(1.0), velocity_weight=0.2)
    down = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY,
                             velocity=_sig(0.0), velocity_weight=0.2)
    assert up.composite > base.composite > down.composite
    assert up.value <= 1.0                                 # clamped


def test_explicit_zero_weight_forces_term_off_not_the_constant():
    # 0.0 is falsy: an `or` fallback here would silently apply the module weight. Guard it.
    up_default = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY,
                                   velocity=_sig(1.0), velocity_weight=0.5)
    off = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY,
                            velocity=_sig(1.0), velocity_weight=0.0)
    base = score_opportunity(_pt(), [], EvidenceBundle(), today=TODAY)
    assert off.composite == base.composite and up_default.composite > base.composite
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_scoring.py -q`
Expected: FAIL with `ImportError: cannot import name 'VELOCITY_WEIGHT'`

- [ ] **Step 3: Write minimal implementation**

In `council/discovery/scoring.py`:

3a. Add the import near the top (after the existing `from council.discovery.fusion import ...`):

```python
from council.discovery.velocity import VelocitySignal, VELOCITY_NORM_NEUTRAL
```

3b. Add constants in the tunable block (after `CONF_CONSENSUS_WT = 0.3`):

```python
VELOCITY_WEIGHT = 0.0     # E4: velocity term OFF by default — ship moves no card's rank until raised
VELOCITY_NEUTRAL = 0.5    # normalized velocity of a flat / absent trend (no nudge)
```

3c. Append four fields to `ScoreBreakdown` (after `evidence_date: str`):

```python
    velocity: float = VELOCITY_NEUTRAL   # 0-1 normalized; 0.5 = flat / no signal
    velocity_raw: float = 0.0            # raw slope (regression-visibility); 0.0 when no signal
    velocity_source: str = ""            # "pytrends" when a real signal is attached, else ""
    velocity_term: str = ""              # the term measured, else ""
```

3d. Change the `score_opportunity` signature (add two keyword-only params):

```python
def score_opportunity(
    point: CandidatePainPoint,
    supporting_urls: list[str],
    bundle: EvidenceBundle,
    *,
    today: date | None = None,
    value_weights: dict[str, float] | None = None,
    velocity: VelocitySignal | None = None,
    velocity_weight: float | None = None,
) -> ScoreBreakdown:
```

3e. Replace the `value = _clamp(...)` block (the three-weight sum) with the base + bounded velocity fold:

```python
    value_base = _clamp(value_weights["importance"] * importance
                        + value_weights["reach"] * reach
                        + value_weights["recency"] * recency)

    # E4 — bounded velocity nudge. centered=0 when flat/absent, so the default weight 0 (and any
    # flat signal) leaves value_base untouched. None-check (NOT `or`): explicit 0.0 forces it off.
    weight = VELOCITY_WEIGHT if velocity_weight is None else velocity_weight
    vel_norm = velocity.normalized if velocity is not None else VELOCITY_NEUTRAL
    centered = (vel_norm - 0.5) * 2.0
    value = _clamp(value_base * (1.0 + weight * centered))
```

3f. Update the `return ScoreBreakdown(...)` to pass the new fields (append after `evidence_date=evidence_date,`):

```python
        velocity=round(vel_norm, 4),
        velocity_raw=round(velocity.slope, 4) if velocity is not None else 0.0,
        velocity_source=velocity.source if velocity is not None else "",
        velocity_term=velocity.term if velocity is not None else "",
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_scoring.py -q`
Expected: PASS (existing scoring tests + 5 new). The existing `test_full_evidence_scores_near_max_confidence` etc. must still pass — velocity defaults leave `value` unchanged.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/scoring.py tests/discovery/test_scoring.py
git commit -m "feat(discovery-e4): velocity fields + bounded weight-0 folding in score_opportunity

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: `frame.py` — per-card term, batched measure, velocity-aware `_why_now`

**Files:**
- Modify: `council/discovery/frame.py`
- Test: `tests/discovery/test_frame.py`

**Interfaces:**
- Consumes: `VelocityProvider` / `VelocitySignal` (Tasks 1-2), `score_opportunity(..., velocity=, velocity_weight=)` (Task 3).
- Produces:
  - `_velocity_term(pt: CandidatePainPoint, topic: str) -> str`.
  - `frame_pm(verified, fusion_result, bundle, *, today=None, topic="", velocity_provider=None, velocity_weight=None)` — one batched `measure_batch` per call.
  - `_why_now(score: ScoreBreakdown) -> str` — leads with velocity when `score.velocity_source`, else the current recency note.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/discovery/test_frame.py
from council.discovery.velocity import VelocitySignal
from council.discovery.frame import _velocity_term


class _FakeProvider:
    def __init__(self, mapping):
        self.mapping = mapping
        self.calls = 0

    def measure_batch(self, terms):
        self.calls += 1
        return {t: self.mapping.get(t) for t in terms}


def _sig(term, normalized):
    return VelocitySignal(term=term, slope=(normalized - 0.5) * 2, normalized=normalized,
                          source="pytrends", window_days=90, points=5)


def test_velocity_term_uses_title_then_topic_fallback():
    pt = CandidatePainPoint("Slow CSV Export!", "s", quotes=["q"], urls=[])
    assert _velocity_term(pt, "pm tools") == "slow csv export"
    empty = CandidatePainPoint("", "s", quotes=["q"], urls=[])
    assert _velocity_term(empty, "pm tools") == "pm tools"        # fallback


def test_why_now_leads_with_velocity_when_present():
    bundle = _bundle(["https://a.com/1"])
    prov = _FakeProvider({"rising pain": _sig("rising pain", 0.9)})
    cards, _ = frame_pm([_vpp("Rising pain", 4, ["https://a.com/1"])], FusionResult(), bundle,
                        today=TODAY, topic="pm", velocity_provider=prov, velocity_weight=0.2)
    assert prov.calls == 1                                        # exactly one batched call
    wn = cards[0].why_now
    assert "accelerating" in wn.lower() and "pytrends" in wn.lower()


def test_why_now_falls_back_to_recency_without_signal():
    bundle = _bundle(["https://a.com/1"])
    # provider returns None for this term -> graceful fallback to the recency note
    prov = _FakeProvider({})
    cards, _ = frame_pm([_vpp("No trend", 3, ["https://a.com/1"])], FusionResult(), bundle,
                        today=TODAY, topic="pm", velocity_provider=prov)
    assert "signal" in cards[0].why_now.lower()                  # the recency-style note
    assert "pytrends" not in cards[0].why_now.lower()


def test_frame_pm_without_provider_is_unchanged_default_path():
    bundle = _bundle(["https://a.com/1"])
    cards, _ = frame_pm([_vpp("X", 3, ["https://a.com/1"])], FusionResult(), bundle, today=TODAY)
    assert cards[0].score.velocity_source == "" and cards[0].why_now  # no provider -> neutral
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_frame.py -q`
Expected: FAIL with `ImportError: cannot import name '_velocity_term'`

- [ ] **Step 3: Write minimal implementation**

In `council/discovery/frame.py`:

3a. Add `import re` at the top and this helper above `_why_now`:

```python
import re

_MAX_TERM_WORDS = 5


def _velocity_term(pt, topic: str) -> str:
    """Short Trends query from the pain title; fall back to the run topic when empty."""
    cleaned = re.sub(r"[^\w\s]", " ", (pt.title or "").lower()).strip()
    cleaned = " ".join(cleaned.split()[:_MAX_TERM_WORDS])
    return cleaned or (topic or "").strip().lower()
```

3b. Replace `_why_now` entirely:

```python
def _why_now(score: ScoreBreakdown) -> str:
    freshness = _freshness_note(score)
    if not score.velocity_source:
        return freshness                                   # no velocity signal -> recency note only
    slope = score.velocity_raw
    if slope > 0.05:
        lead = f"Demand accelerating — interest slope +{slope:.2f} over {_WINDOW_LABEL} ({score.velocity_source})."
    elif slope < -0.05:
        lead = f"Demand cooling — interest slope {slope:.2f} over {_WINDOW_LABEL} ({score.velocity_source})."
    else:
        lead = f"Demand flat — interest steady over {_WINDOW_LABEL} ({score.velocity_source})."
    return f"{lead} {freshness}"


def _freshness_note(score: ScoreBreakdown) -> str:
    if not score.evidence_date:
        return "Recency unknown — verify the pain is current."
    if score.recency >= 0.5:
        return f"Fresh signal — evidence dated {score.evidence_date}."
    return f"Older signal (evidence {score.evidence_date}); confirm it's still live."
```

Add the label constant near the top of the file (after imports):

```python
_WINDOW_LABEL = "90d"   # display label for the velocity window (PytrendsProvider default)
```

3c. Change the `frame_pm` signature and add the batched measure before the loop:

```python
def frame_pm(verified: list[VerifiedPainPoint], fusion_result: FusionResult,
             bundle: EvidenceBundle, *, today: date | None = None, topic: str = "",
             velocity_provider=None, velocity_weight=None) -> tuple[list[IdeaCard], list[str]]:
    today = today or date.today()
    # E4 — one batched demand-slope lookup for all verified cards (blind to the gate; score-only).
    signals: dict = {}
    if velocity_provider is not None:
        terms = _dedup_terms([_velocity_term(v.point, topic) for v in verified if v.verified])
        if terms:
            signals = velocity_provider.measure_batch(terms)
    cards: list[IdeaCard] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        signal = signals.get(_velocity_term(pt, topic))
        score = score_opportunity(pt, v.supporting_urls, bundle, today=today,
                                  velocity=signal, velocity_weight=velocity_weight)
```

(Leave the rest of the loop body and the `cards.sort(...)` / `return` unchanged.)

3d. Add the tiny dedup helper near `_velocity_term`:

```python
def _dedup_terms(terms: list[str]) -> list[str]:
    seen, out = set(), []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_frame.py -q`
Expected: PASS. The existing `test_why_now_reflects_recency_state` still passes ("Fresh signal"/"Older signal" now come from `_freshness_note`, which the no-signal path returns verbatim).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/frame.py tests/discovery/test_frame.py
git commit -m "feat(discovery-e4): per-card velocity term + batched measure + velocity-aware why_now

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: `pipeline.py` — resolve provider, thread to frame, session metrics + the invariant test

**Files:**
- Modify: `council/discovery/pipeline.py`
- Test: `tests/discovery/test_pipeline.py`

**Interfaces:**
- Consumes: `get_velocity_provider` (Task 2), `frame_pm(..., topic=, velocity_provider=)` (Task 4).
- Produces: `run_discovery(..., velocity_provider=_UNSET)`; session dict gains `velocity_mode` (`"off"`/`"pytrends"`) and `why_now_coverage` (float) on both the empty-bundle and success paths.

- [ ] **Step 1: Write the failing test**

```python
# append to tests/discovery/test_pipeline.py
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.velocity import VelocitySignal


class _FakeVProvider:
    def measure_batch(self, terms):
        # rising signal for every term
        return {t: VelocitySignal(term=t, slope=0.8, normalized=0.9, source="pytrends",
                                  window_days=90, points=5) for t in terms}


def _one_point_bundle_and_fuse():
    url = "https://ex.com/a"
    async def gather_fn(**kw):
        b = EvidenceBundle()
        b.add(EvidenceRecord("reddit", "r/pm", url, "2026-06-20", "slow export", engagement=100))
        return b, {"ok": True}
    async def fuse_fn(**kw):
        pt = CandidatePainPoint("Slow export", "it's slow", quotes=["slow export"], urls=[url],
                                intensity=4, recency="2026-06", consensus="4/4 models")
        return FusionResult(pain_points=[pt])
    return gather_fn, fuse_fn


@pytest.mark.asyncio
async def test_velocity_off_by_default_in_session():
    gather_fn, fuse_fn = _one_point_bundle_and_fuse()
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              velocity_provider=None)
    assert res.session["velocity_mode"] == "off"
    assert res.session["why_now_coverage"] == 0.0


@pytest.mark.asyncio
async def test_velocity_provider_threads_and_reports_coverage():
    gather_fn, fuse_fn = _one_point_bundle_and_fuse()
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              velocity_provider=_FakeVProvider())
    assert res.session["velocity_mode"] == "pytrends"
    assert res.session["why_now_coverage"] == 1.0                 # the one card carries a signal


@pytest.mark.asyncio
async def test_empty_bundle_session_carries_velocity_keys():
    async def gather_fn(**kw):
        return EvidenceBundle(), {"ok": True}
    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=gather_fn, fuse_fn=None)
    assert res.session["velocity_mode"] == "off"
    assert res.session["why_now_coverage"] == 0.0


@pytest.mark.asyncio
async def test_invariant_velocity_cannot_perturb_the_gate():
    # THE MOAT: verified set + citation metrics identical velocity on vs off (weight defaults to 0),
    # and no velocity string leaks into evidence urls/quotes.
    g1, f1 = _one_point_bundle_and_fuse()
    off = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=g1, fuse_fn=f1, supplement=False, velocity_provider=None)
    g2, f2 = _one_point_bundle_and_fuse()
    on = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                             gather_fn=g2, fuse_fn=f2, supplement=False,
                             velocity_provider=_FakeVProvider())
    assert off.session["verified"] == on.session["verified"]
    assert off.session["dropped"] == on.session["dropped"]
    assert off.session["citation_precision"] == on.session["citation_precision"]
    assert off.session["citation_recall"] == on.session["citation_recall"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_pipeline.py -q`
Expected: FAIL — `run_discovery()` has no `velocity_provider` kwarg (`TypeError`), and `session["velocity_mode"]` `KeyError`.

- [ ] **Step 3: Write minimal implementation**

In `council/discovery/pipeline.py`:

3a. Add the import (near `from council.discovery.nli import get_scorer`):

```python
from council.discovery.velocity import get_velocity_provider
```

3b. Add `velocity_provider=_UNSET` to the `run_discovery` signature:

```python
async def run_discovery(*, topic: str, lens: str, tier: str, api_key: str, segment: str = "",
                        gather_fn=None, fuse_fn=None, backfill_fn=None, supplement: bool = True,
                        sessions_dir: Path | None = None, scorer=_UNSET,
                        velocity_provider=_UNSET) -> DiscoveryResult:
```

3c. In the empty-bundle early return, add the two keys to the session dict (after `"citation_precision": None, "citation_recall": None`):

```python
                                        "citation_precision": None, "citation_recall": None,
                                        "velocity_mode": "off", "why_now_coverage": 0.0})
```

3d. In the success path, resolve the provider and thread it into the pm-lens `frame_pm` call. Replace the `else:` branch (`cards, quote_bank = frame_pm(verified, fr, bundle, today=today)`) with:

```python
        else:
            active_vp = get_velocity_provider() if velocity_provider is _UNSET else velocity_provider
            cards, quote_bank = frame_pm(verified, fr, bundle, today=today, topic=topic,
                                         velocity_provider=active_vp)
            md = render_ledger(topic=topic, lens=lens, tier=tier, segment=segment, cards=cards,
                               quote_bank=quote_bank, fusion_result=fr, cost_usd=cost,
                               dropped_count=dropped, supplement=supplement_result,
                               merged_count=len(merges), verify_mode=verify_mode)
            verified_count = len(cards)
            velocity_mode = "pytrends" if active_vp is not None else "off"
            why_now_coverage = (round(sum(1 for c in cards if c.score.velocity_source) / len(cards), 4)
                                if cards else 0.0)
```

3e. For the substack lens, velocity does not apply — set defaults so the session dict is uniform. At the top of the success `try`, before the `if lens == "substack":` branch, initialize:

```python
        velocity_mode = "off"
        why_now_coverage = 0.0
```

(The pm-lens branch overwrites them; the substack branch leaves them.)

3f. Add both keys to the success `session` dict (after `"citation_recall": metrics.recall,`):

```python
            "citation_recall": metrics.recall,
            "velocity_mode": velocity_mode,
            "why_now_coverage": why_now_coverage,
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_pipeline.py -q`
Expected: PASS (existing pipeline tests + 4 new).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/pipeline.py tests/discovery/test_pipeline.py
git commit -m "feat(discovery-e4): resolve velocity provider, thread to frame, session why_now_coverage + invariant test

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: optional `pytrends` extra + whole-suite regression + validate

**Files:**
- Modify: `pyproject.toml`

**Interfaces:**
- Consumes: everything above. No new code.

- [ ] **Step 1: Declare pytrends as an optional extra (never a hard dep)**

Inspect `tools/llm-council/pyproject.toml`. If it has an `[project.optional-dependencies]` table, add a `velocity` extra; otherwise create the table:

```toml
[project.optional-dependencies]
velocity = ["pytrends>=4.9"]
```

Do NOT add pytrends to the base `dependencies` array. (If `pyproject.toml` uses a non-PEP-621 layout, mirror the existing optional/extra convention already present in the file instead.)

- [ ] **Step 2: Full discovery suite**

Run: `uv run pytest tests/ -q`
Expected: **all pass** — baseline 303 + the new tests (target ~324, 1 skipped). Zero failures.

- [ ] **Step 3: Repo validator**

Run (from repo root): `python3 scripts/validate.py`
Expected: PASSED (pre-existing warnings OK; none in the changed files).

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore(discovery-e4): declare optional pytrends extra + regression green

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:**
- velocity.py channel (VelocitySignal / provider / get_velocity_provider) → Tasks 1-2 ✓
- Invariant (no verify import; verify byte-identical on/off) → Task 1 import guard + Task 5 invariant test ✓
- scoring fields + bounded weight-0 folding + None-check guard → Task 3 ✓
- per-card term + topic fallback + batched call + velocity `_why_now` + degradation → Task 4 ✓
- pipeline resolution + `velocity_mode` + `why_now_coverage` (both paths) → Task 5 ✓
- optional dependency, regression, validate → Task 6 ✓
- **Deliberate spec deviation:** session JSON carries run-level `velocity_mode` + `why_now_coverage` only, NOT a per-card velocity array (cards aren't serialized today; adding an array is D3's call). Per-card velocity remains visible in `ScoreBreakdown` + rendered `why_now`. Noted in the spec's pipeline section intent; `why_now_coverage` is the §9 metric D3 renders.
- Demand-intent (autocomplete/PAA) → correctly OUT of v1 (needs SerpApi); channel shape carries it later ✓

**Placeholder scan:** none — every code step is complete and runnable.

**Type consistency:** `measure_batch(terms) -> dict[str, VelocitySignal | None]` consistent across Tasks 1/2/4/5. `_velocity_term(pt, topic)` returns lowercased short string, used identically for the batch call and the per-card lookup (same key). `velocity`/`velocity_weight` keyword params match between `score_opportunity` (Task 3), `frame_pm` (Task 4), and the pipeline call (Task 5). `velocity_source`/`velocity_raw`/`velocity_term`/`velocity` field names consistent across scoring, frame, pipeline, and tests.

**Note on the `_why_now` fallback assertion:** the no-signal path returns `_freshness_note`, whose strings ("Fresh signal" / "Older signal" / "Recency unknown") all still satisfy the existing `test_why_now_reflects_recency_state` and the new `"signal" in why_now` fallback assertion.
