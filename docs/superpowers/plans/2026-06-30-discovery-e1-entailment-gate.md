# E1 — Entailment Gate v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the shared anti-fabrication chokepoint from substring containment to a substring-prefilter → atomic-claim + NLI-entailment cascade, with ALCE-style citation precision/recall, backed by an optional in-process ONNX NLI model that degrades gracefully to today's behavior.

**Architecture:** A pure decision cascade in `verify.py` takes an **injected scorer** (dependency injection = the hermetic-test seam). A separate `nli.py` is the real-model adapter whose `get_scorer()` returns `None` on any import/load failure, triggering substring-only fallback. The pipeline obtains the scorer once and records the active mode + metrics in the session JSON. Tasks 1–3 + 5 are fully hermetic (fake scorer); Task 4 adds the real model behind a skip-marker; Task 6 adds the optional dependency, setup script, and docs.

**Tech Stack:** Python 3, pytest, onnxruntime (optional extra), `cross-encoder/nli-deberta-v3-small` int8 ONNX, `uv` for the test runner.

## Global Constraints

- Run tests with: `cd tools/llm-council && uv run pytest tests/ -q`. Baseline before this work: **the current `main` count** (re-run once to capture it; E1 only ADDS tests + an optional `scorer` param, so the baseline must stay green).
- Validator: `python3 scripts/validate.py` must PASS.
- **Recall-safety invariant (load-bearing):** the substring pre-filter may only ever *add* an accept — it must **never reject**. Every substring-miss falls through to NLI (or, when degraded, rejects only because NLI is unavailable, exactly as today).
- **Graceful fallback:** when no scorer/model/deps are present, the gate behaves EXACTLY as today (substring-only). Every existing `verify` test must stay green unchanged.
- **Hermetic suite:** no model download in CI. The real model is exercised only by one skip-marked integration test.
- Default entailment threshold `τ = 0.5` (module constant `_ENTAIL_TAU` in `verify.py`).
- Scorer interface (used everywhere): an object with `entails(*, premise: str, hypothesis: str) -> float` returning the entailment-class probability in [0, 1].
- Commit trailer on every commit: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- Keep the branch free of vault changes (Obsidian-Git owns the vault).

---

### Task 1: Cascade + atomic-claim split in `quote_supported_at_url`

**Files:**
- Modify: `tools/llm-council/council/discovery/verify.py`
- Test: `tools/llm-council/tests/discovery/test_verify_entailment.py` (create)

**Interfaces:**
- Produces: `quote_supported_at_url(*, cited_quote: str, fetched_text: str, scorer=None) -> bool`; module constant `_ENTAIL_TAU = 0.5`; helper `_claim_sentences(text: str) -> list[str]`.
- Consumes: a `scorer` duck-type with `entails(*, premise, hypothesis) -> float`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/discovery/test_verify_entailment.py
from council.discovery.verify import quote_supported_at_url


class FakeScorer:
    """Deterministic stand-in for the real NLI model. Maps (premise, hypothesis) -> entailment prob."""
    def __init__(self, prob=0.0, table=None):
        self.prob, self.table, self.calls = prob, table or {}, []
    def entails(self, *, premise, hypothesis):
        self.calls.append((premise, hypothesis))
        return self.table.get(hypothesis, self.prob)


def test_substring_hit_accepts_without_consulting_scorer():
    s = FakeScorer(prob=0.0)  # would reject everything if consulted
    assert quote_supported_at_url(cited_quote="exports fail silently",
                                  fetched_text="users say exports fail silently a lot", scorer=s) is True
    assert s.calls == []  # fast-path: scorer never consulted on a substring hit


def test_paraphrase_accepted_via_nli_on_substring_miss():
    s = FakeScorer(table={"the export feature loses data": 0.92})
    assert quote_supported_at_url(cited_quote="the export feature loses data",
                                  fetched_text="reviewers report exporting silently drops rows", scorer=s) is True


def test_unsupported_claim_rejected_when_nli_low():
    s = FakeScorer(prob=0.10)
    assert quote_supported_at_url(cited_quote="it has great SSO support",
                                  fetched_text="reviewers report exporting silently drops rows", scorer=s) is False


def test_substring_never_rejects_even_if_scorer_would():
    s = FakeScorer(prob=0.0)  # scorer says reject, but substring present must still accept
    assert quote_supported_at_url(cited_quote="drops rows",
                                  fetched_text="exporting silently drops rows", scorer=s) is True


def test_scorer_none_is_substring_only_todays_behavior():
    # paraphrase, no substring, no scorer -> reject exactly as today
    assert quote_supported_at_url(cited_quote="the export feature loses data",
                                  fetched_text="exporting silently drops rows", scorer=None) is False
    # substring still accepts with no scorer
    assert quote_supported_at_url(cited_quote="drops rows",
                                  fetched_text="exporting silently drops rows", scorer=None) is True


def test_multi_sentence_claim_requires_all_supported():
    # first sentence substring-present, second neither substring nor entailed -> overall reject (AND)
    s = FakeScorer(prob=0.0)
    assert quote_supported_at_url(cited_quote="drops rows. it also lacks SSO.",
                                  fetched_text="exporting silently drops rows", scorer=s) is False


def test_empty_inputs_reject():
    assert quote_supported_at_url(cited_quote="", fetched_text="anything", scorer=None) is False
    assert quote_supported_at_url(cited_quote="x", fetched_text="", scorer=None) is False
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_entailment.py -q`
Expected: FAIL — `quote_supported_at_url()` got an unexpected keyword `scorer` (or assertion failures).

- [ ] **Step 3: Implement the cascade in `verify.py`**

Replace `quote_supported_at_url` and add helpers. Keep the existing docstring intent; add:

```python
import logging
import re

_ENTAIL_TAU = 0.5
_CLAIM_SENT = re.compile(r"[^.!?]+[.!?]|[^.!?]+$")
_logger = logging.getLogger("council.discovery.verify")
_degraded_warned = False


def _claim_sentences(text: str) -> list[str]:
    parts = [s.strip() for s in _CLAIM_SENT.findall(text)]
    parts = [p for p in parts if p]
    return parts or ([text.strip()] if text.strip() else [])


def _warn_degraded_once() -> None:
    global _degraded_warned
    if not _degraded_warned:
        _degraded_warned = True
        _logger.warning("NLI scorer unavailable — VERIFY gate running in substring-only (degraded) mode.")


def _claim_supported(claim: str, fetched_text: str, doc_lower: str, scorer) -> bool:
    needle = claim.strip().lower()
    if not needle:
        return True                       # empty fragment never vetoes the AND
    if needle in doc_lower:               # substring pre-filter: fast ACCEPT, never rejects
        return True
    if scorer is None:
        _warn_degraded_once()
        return False                      # degraded: substring-only, exactly as today
    return scorer.entails(premise=fetched_text, hypothesis=claim) >= _ENTAIL_TAU


def quote_supported_at_url(*, cited_quote: str, fetched_text: str, scorer=None) -> bool:
    """Substring pre-filter -> atomic-claim NLI-entailment cascade (E1). Shared by VERIFY + BACKFILL.
    Substring is a fast, high-precision ACCEPT that NEVER rejects; every substring-miss falls through
    to NLI. With scorer=None the gate is substring-only (today's behavior)."""
    doc_lower = fetched_text.strip().lower()
    if not doc_lower:
        return False
    sentences = _claim_sentences(cited_quote)
    if not sentences:
        return False
    return all(_claim_supported(s, fetched_text, doc_lower, scorer) for s in sentences)
```

- [ ] **Step 4: Run to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_entailment.py -q`
Expected: PASS (7 tests).

- [ ] **Step 5: Run the full suite (no regressions)**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: baseline + 7, all green. The existing `test_verify.py` / `test_verify_supplement.py` stay green (scorer defaults to None → substring-only).

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/discovery/verify.py tools/llm-council/tests/discovery/test_verify_entailment.py
git commit -m "discovery E1: substring-prefilter -> atomic-claim NLI cascade in quote_supported_at_url"
```

---

### Task 2: Thread the scorer through VERIFY

**Files:**
- Modify: `tools/llm-council/council/discovery/verify.py`
- Test: `tools/llm-council/tests/discovery/test_verify_entailment.py` (append)

**Interfaces:**
- Produces: `_quote_present_at_url(bundle, url, quotes, scorer=None) -> bool`; `verify_pain_points(points, bundle, scorer=None) -> list[VerifiedPainPoint]`.
- Consumes: `quote_supported_at_url(..., scorer=...)` from Task 1.

- [ ] **Step 1: Write the failing test**

```python
def test_verify_pain_points_accepts_paraphrase_with_scorer():
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.fusion import CandidatePainPoint
    from council.discovery.verify import verify_pain_points

    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exporting silently drops rows"))
    pt = CandidatePainPoint("Export loss", "s", ["the export feature loses data"], ["https://r.com/1"], intensity=5)

    # no scorer -> paraphrase not a substring -> dropped (today's behavior)
    assert verify_pain_points([pt], b)[0].verified is False

    # with scorer that entails the paraphrase -> verified
    s = FakeScorer(table={"the export feature loses data": 0.9})
    out = verify_pain_points([pt], b, scorer=s)
    assert out[0].verified is True
    assert out[0].supporting_urls == ["https://r.com/1"]
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_entailment.py::test_verify_pain_points_accepts_paraphrase_with_scorer -q`
Expected: FAIL — `verify_pain_points()` got unexpected keyword `scorer`.

- [ ] **Step 3: Thread `scorer` through both functions**

```python
def _quote_present_at_url(bundle, url, quotes, scorer=None) -> bool:
    for rec in bundle.records:
        if rec.url != url:
            continue
        for q in quotes:
            if quote_supported_at_url(cited_quote=q, fetched_text=rec.quote, scorer=scorer):
                return True
    return False


def verify_pain_points(points, bundle, scorer=None):
    out = []
    for pt in points:
        supporting = [
            u for u in pt.urls
            if bundle.has_url(u) and _quote_present_at_url(bundle, u, pt.quotes, scorer=scorer)
        ]
        out.append(VerifiedPainPoint(point=pt, verified=bool(supporting), supporting_urls=supporting))
    return out
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_entailment.py -q`
Expected: PASS.

- [ ] **Step 5: Full suite**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: all green (BACKFILL's call site uses the default `scorer=None`, unchanged).

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/discovery/verify.py tools/llm-council/tests/discovery/test_verify_entailment.py
git commit -m "discovery E1: thread optional scorer through verify_pain_points + _quote_present_at_url"
```

---

### Task 3: ALCE-style citation precision/recall

**Files:**
- Modify: `tools/llm-council/council/discovery/verify.py`
- Test: `tools/llm-council/tests/discovery/test_verify_metrics.py` (create)

**Interfaces:**
- Produces: `@dataclass CitationMetrics(precision: float | None, recall: float | None)`; `citation_metrics(verified: list[VerifiedPainPoint], bundle, scorer=None) -> CitationMetrics`.
- Consumes: `VerifiedPainPoint`, `quote_supported_at_url`.

**Definitions (reference-free, ALCE):** for each verified point, build the premise = concatenation of the `rec.quote`s at its `supporting_urls`. **Recall** = fraction of points whose cited quotes are all supported by that concatenated premise. **Precision** = over each (point, supporting_url) citation, fraction that are *not* redundant — a citation is redundant iff removing it still leaves the point supported by the remaining premise. When `scorer is None`, return `CitationMetrics(None, None)` (metrics are an NLI-mode feature).

- [ ] **Step 1: Write the failing tests**

```python
# tests/discovery/test_verify_metrics.py
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint
from council.discovery.verify import verify_pain_points, citation_metrics
from tests.discovery.test_verify_entailment import FakeScorer


def _bundle(*recs):
    b = EvidenceBundle()
    for r in recs:
        b.add(r)
    return b


def test_metrics_none_without_scorer():
    b = _bundle(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports drop rows"))
    pt = CandidatePainPoint("Export", "s", ["exports drop rows"], ["https://r.com/1"], intensity=5)
    verified = verify_pain_points([pt], b)
    m = citation_metrics(verified, b, scorer=None)
    assert m.precision is None and m.recall is None


def test_recall_full_when_all_claims_supported():
    b = _bundle(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports silently drop rows"))
    pt = CandidatePainPoint("Export", "s", ["exports silently drop rows"], ["https://r.com/1"], intensity=5)
    s = FakeScorer(prob=0.9)
    verified = verify_pain_points([pt], b, scorer=s)
    m = citation_metrics(verified, b, scorer=s)
    assert m.recall == 1.0


def test_precision_flags_redundant_citation():
    # two citations, the claim is a verbatim substring of url1 only; url2 adds nothing -> redundant
    b = _bundle(
        EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports silently drop rows"),
        EvidenceRecord("reddit", "r", "https://r.com/2", "", "unrelated note about billing"),
    )
    pt = CandidatePainPoint("Export", "s", ["exports silently drop rows"],
                            ["https://r.com/1", "https://r.com/2"], intensity=5)
    s = FakeScorer(prob=0.0)  # no paraphrase help; rely on substring at url1
    verified = verify_pain_points([pt], b, scorer=s)
    m = citation_metrics(verified, b, scorer=s)
    assert m.precision == 0.5  # 1 of 2 citations contributes
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_metrics.py -q`
Expected: FAIL — `cannot import name 'citation_metrics'`.

- [ ] **Step 3: Implement `citation_metrics`**

```python
from dataclasses import dataclass


@dataclass
class CitationMetrics:
    precision: float | None
    recall: float | None


def _premise_for(bundle, urls) -> str:
    return " ".join(r.quote for r in bundle.records if r.url in set(urls))


def _all_claims_supported(quotes, premise, scorer) -> bool:
    return all(quote_supported_at_url(cited_quote=q, fetched_text=premise, scorer=scorer) for q in quotes)


def citation_metrics(verified, bundle, scorer=None) -> CitationMetrics:
    if scorer is None:
        return CitationMetrics(None, None)
    points = [v for v in verified if v.verified]
    if not points:
        return CitationMetrics(None, None)

    recalls = []
    contributing = total = 0
    for v in points:
        quotes = v.point.quotes
        urls = v.supporting_urls
        recalls.append(1.0 if _all_claims_supported(quotes, _premise_for(bundle, urls), scorer) else 0.0)
        for u in urls:
            total += 1
            remaining = [x for x in urls if x != u]
            # redundant iff the point is still supported WITHOUT this citation
            still = bool(remaining) and _all_claims_supported(quotes, _premise_for(bundle, remaining), scorer)
            if not still:
                contributing += 1
    recall = round(sum(recalls) / len(recalls), 4)
    precision = round(contributing / total, 4) if total else None
    return CitationMetrics(precision=precision, recall=recall)
```

- [ ] **Step 4: Run to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify_metrics.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Full suite**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: green.

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/discovery/verify.py tools/llm-council/tests/discovery/test_verify_metrics.py
git commit -m "discovery E1: ALCE-style citation precision/recall (NLI-mode only)"
```

---

### Task 4: Real NLI scorer adapter `nli.py` (graceful `get_scorer`)

**Files:**
- Create: `tools/llm-council/council/discovery/nli.py`
- Test: `tools/llm-council/tests/discovery/test_nli.py` (create)

**Interfaces:**
- Produces: `class NliScorer` with `entails(*, premise, hypothesis) -> float`; `get_scorer() -> NliScorer | None` (lazy singleton, returns `None` on any import/load failure); `reset_scorer_cache()` (test helper).
- Consumes: onnxruntime + tokenizer (optional deps) and the model dir (`DISCOVERY_NLI_MODEL_DIR` env, default `tools/llm-council/models/nli-deberta-v3-small/`).

**Note on the entailment label index:** `cross-encoder/nli-deberta-v3-small` emits 3 logits. Confirm the entailment index from the model card's `id2label` at build time and encode it as a named constant `_ENTAILMENT_IDX`; a wrong index silently inverts the gate. Verify by running the skip-marked integration test (Step 6) against a known entailing pair.

- [ ] **Step 1: Write the failing unit tests (hermetic — no model)**

```python
# tests/discovery/test_nli.py
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
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_nli.py -q`
Expected: FAIL — `No module named 'council.discovery.nli'`.

- [ ] **Step 3: Implement `nli.py`**

```python
# council/discovery/nli.py
"""In-process NLI entailment scorer (E1). Optional: get_scorer() returns None on any import/load
failure so the VERIFY gate degrades to substring-only. Model = cross-encoder/nli-deberta-v3-small
int8 ONNX, run on onnxruntime CPU, no server (so no asleep-host failure mode)."""

import logging
import os
from pathlib import Path

_logger = logging.getLogger("council.discovery.nli")
_DEFAULT_DIR = Path(__file__).resolve().parent.parent.parent / "models" / "nli-deberta-v3-small"
_ENTAILMENT_IDX = 1   # CONFIRM against the model card id2label before trusting; see Task 4 note
_sentinel = object()
_cached = _sentinel


def _model_dir() -> Path:
    return Path(os.environ.get("DISCOVERY_NLI_MODEL_DIR") or _DEFAULT_DIR)


class NliScorer:
    def __init__(self, session, tokenizer):
        self._session, self._tok = session, tokenizer

    def entails(self, *, premise: str, hypothesis: str) -> float:
        import numpy as np
        enc = self._tok(premise, hypothesis, truncation=True, max_length=512, return_tensors="np")
        inputs = {k: v for k, v in enc.items() if k in {i.name for i in self._session.get_inputs()}}
        logits = self._session.run(None, inputs)[0][0]
        e = np.exp(logits - np.max(logits))
        probs = e / e.sum()
        return float(probs[_ENTAILMENT_IDX])


def reset_scorer_cache() -> None:
    global _cached
    _cached = _sentinel


def get_scorer():
    """Lazy singleton. Returns an NliScorer, or None if onnxruntime/tokenizer/model are unavailable."""
    global _cached
    if _cached is not _sentinel:
        return _cached
    _cached = None
    try:
        import onnxruntime as ort
        from transformers import AutoTokenizer
        d = _model_dir()
        onnx_path = d / "model_qint8_avx512_vnni.onnx"
        if not onnx_path.exists():
            _logger.warning("NLI model not found at %s — gate runs substring-only.", onnx_path)
            return _cached
        session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
        tokenizer = AutoTokenizer.from_pretrained(str(d))
        _cached = NliScorer(session, tokenizer)
    except Exception as e:  # ImportError, file/load errors — degrade, never crash a run
        _logger.warning("NLI scorer load failed (%s) — gate runs substring-only.", e)
        _cached = None
    return _cached
```

- [ ] **Step 4: Run to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_nli.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Add the skip-marked real-model integration test**

```python
# append to tests/discovery/test_nli.py
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
```

- [ ] **Step 6: Run the full suite (integration test skips without the model)**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: green; `test_real_model_entails_paraphrase` reported as **skipped**.

- [ ] **Step 7: Commit**

```bash
git add tools/llm-council/council/discovery/nli.py tools/llm-council/tests/discovery/test_nli.py
git commit -m "discovery E1: in-process ONNX NLI scorer with graceful get_scorer() fallback"
```

---

### Task 5: Wire the scorer into the pipeline + session JSON

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py` (append)

**Interfaces:**
- Consumes: `get_scorer()` from `nli.py`; `verify_pain_points(..., scorer=...)`, `citation_metrics(...)` from `verify.py`.
- Produces: `run_discovery(..., scorer=...)` (new optional param, default = `get_scorer()` result, injectable for tests); session JSON keys `verify_mode`, `citation_precision`, `citation_recall`.

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/discovery/test_pipeline.py
@pytest.mark.asyncio
async def test_pipeline_records_verify_mode_substring_only_without_scorer(tmp_path):
    from tests.discovery.test_verify_entailment import FakeScorer  # noqa
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exports fail silently", 9))
    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}
    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=10, tokens_out=5, cost=0.1)
    sdir = tmp_path / ".sessions"
    res = await run_discovery(topic="x", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              sessions_dir=sdir, scorer=None)
    import json
    data = json.loads(next(sdir.glob("*.json")).read_text())
    assert data["verify_mode"] == "substring-only"
    assert data["citation_precision"] is None and data["citation_recall"] is None
    assert res.verified_count == 1


@pytest.mark.asyncio
async def test_pipeline_records_nli_mode_and_metrics_with_scorer(tmp_path):
    from tests.discovery.test_verify_entailment import FakeScorer
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exports fail silently", 9))
    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}
    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=10, tokens_out=5, cost=0.1)
    sdir = tmp_path / ".sessions"
    await run_discovery(topic="x", lens="pm", tier="standard", api_key="k",
                        gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                        sessions_dir=sdir, scorer=FakeScorer(prob=0.9))
    import json
    data = json.loads(next(sdir.glob("*.json")).read_text())
    assert data["verify_mode"] == "nli"
    assert data["citation_recall"] == 1.0
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -k verify_mode -q`
Expected: FAIL — `run_discovery()` got unexpected keyword `scorer` (or missing session keys).

- [ ] **Step 3: Wire it into `run_discovery`**

In `pipeline.py`:
- Add `scorer=_UNSET` to the signature (sentinel so tests can pass `scorer=None` explicitly to force degraded mode; when unset, resolve via `get_scorer()`):

```python
from council.discovery.nli import get_scorer
from council.discovery.verify import verify_pain_points, citation_metrics

_UNSET = object()

async def run_discovery(*, ..., scorer=_UNSET):
    ...
    active_scorer = get_scorer() if scorer is _UNSET else scorer
    ...
    verified = verify_pain_points(fr.pain_points, bundle, scorer=active_scorer)
    ...
    metrics = citation_metrics(verified, bundle, scorer=active_scorer)
    verify_mode = "nli" if active_scorer is not None else "substring-only"
```

Add to the success `session` dict:

```python
    "verify_mode": verify_mode,
    "citation_precision": metrics.precision,
    "citation_recall": metrics.recall,
```

(Compute `metrics` AFTER `dedup_verified` so it reflects the surfaced set; pass the deduped `verified`.)

- [ ] **Step 4: Run to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -k verify_mode -q`
Expected: PASS.

- [ ] **Step 5: Full suite + validator**

Run: `cd tools/llm-council && uv run pytest tests/ -q && cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: green; validator PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/discovery/pipeline.py tools/llm-council/tests/discovery/test_pipeline.py
git commit -m "discovery E1: wire NLI scorer into pipeline; record verify_mode + citation precision/recall"
```

---

### Task 6: Optional dependency, setup script, render note, docs

**Files:**
- Modify: `tools/llm-council/pyproject.toml`
- Create: `tools/llm-council/scripts/install_nli_model.sh`
- Modify: `tools/llm-council/council/discovery/render.py` (+ `render_substack.py` if it has the same footer) — degraded-mode note
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§6 the gate)
- Modify: `CHANGELOG.md`
- Test: `tools/llm-council/tests/discovery/test_render.py` (append, for the note)

**Interfaces:**
- Consumes: `verify_mode` passed into the renderer.

- [ ] **Step 1 (TDD the render note): failing test**

Add a test asserting that when `verify_mode == "substring-only"` the rendered ledger contains a one-line honesty note (e.g. `verification: substring-only`), and when `"nli"` it does not (or shows `verification: NLI entailment`). Mirror the existing `render_ledger` signature; thread `verify_mode` through `run_discovery`'s render calls.

```python
def test_render_shows_degraded_verification_note():
    from council.discovery.render import render_ledger
    from council.discovery.fusion import FusionResult
    md = render_ledger(topic="x", lens="pm", tier="standard", segment="", cards=[],
                       quote_bank=[], fusion_result=FusionResult(), cost_usd=0.0,
                       dropped_count=0, supplement=None, verify_mode="substring-only")
    assert "substring-only" in md.lower()
```

- [ ] **Step 2: Run → fail** (`render_ledger` got unexpected keyword `verify_mode`).

- [ ] **Step 3: Implement** — add `verify_mode: str = "nli"` param to `render_ledger` (and the substack renderer if symmetric); emit a one-line note only when `verify_mode == "substring-only"`. Thread `verify_mode` from `run_discovery` into both render calls. Keep it additive — default keeps existing callers green.

- [ ] **Step 4: Run → pass**, then full suite.

- [ ] **Step 5: pyproject optional extra**

Add to `tools/llm-council/pyproject.toml`:

```toml
[project.optional-dependencies]
nli = ["onnxruntime>=1.17", "transformers>=4.40", "numpy"]
```

(Use `transformers` for `AutoTokenizer` per `nli.py`. If the project prefers the lighter `tokenizers`-only path, adjust `nli.py` and this extra together.)

- [ ] **Step 6: Setup script** — `tools/llm-council/scripts/install_nli_model.sh` (mirror `agents-sdk/scripts/install_tts_models.sh`): `huggingface-cli download cross-encoder/nli-deberta-v3-small onnx/model_qint8_avx512_vnni.onnx <tokenizer files> --local-dir tools/llm-council/models/nli-deberta-v3-small/`, flattening the ONNX to `model_qint8_avx512_vnni.onnx` at the model-dir root (match the path `nli.py` expects). Make it idempotent. Add `tools/llm-council/models/` to `.gitignore` if not already covered.

- [ ] **Step 7: Confirm the entailment label index** — run the skip-marked `test_real_model_entails_paraphrase` after install; if it fails (high ≤ low), fix `_ENTAILMENT_IDX` in `nli.py` against the model card `id2label` and re-run. Commit the corrected constant.

- [ ] **Step 8: Docs** — update `SKILL.md` §6 (gate now does substring→NLI entailment, optional local model, `install_nli_model.sh`, graceful fallback, `verify_mode` in session JSON) and add a `CHANGELOG.md` entry under `## [Unreleased]`.

- [ ] **Step 9: Commit**

```bash
git add tools/llm-council/pyproject.toml tools/llm-council/scripts/install_nli_model.sh \
  tools/llm-council/council/discovery/render.py tools/llm-council/tests/discovery/test_render.py \
  .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md .gitignore
git commit -m "discovery E1: optional nli extra + model setup script + degraded-mode render note + docs"
```

---

## Final verification (before PR)

- [ ] `cd tools/llm-council && uv run pytest tests/ -q` → green (real-model test skipped unless installed).
- [ ] `python3 scripts/validate.py` → PASS.
- [ ] Optional: run `scripts/install_nli_model.sh`, re-run the suite, confirm `test_real_model_entails_paraphrase` PASSES (label index correct).
- [ ] **Final whole-branch adversarial review** (Code Reviewer, most capable model) focused on: the recall-safety invariant (substring never rejects), the graceful-degradation seam (no path hard-fails when the model is absent), label-index correctness, and that no existing verify/backfill test was deformed.
- [ ] Open PR; leave for Sean to squash-merge. Rebase on `main` after PR #110 (Task A) lands — disjoint files, no conflict expected.

## Self-review notes (author)

- **Spec coverage:** cascade (T1), thread-through (T2), ALCE metrics (T3), real scorer + graceful get_scorer (T4), pipeline/session-JSON wiring (T5), deps/setup/render-note/docs (T6) — every spec section maps to a task.
- **Hermetic:** T1–T3, T5 use the `FakeScorer`; T4's real model is skip-marked; no CI download.
- **Type consistency:** scorer interface `entails(*, premise, hypothesis) -> float` is identical across verify.py, nli.py, and the fake; `verify_mode` strings `"nli"`/`"substring-only"` are used identically in T5 and T6.
- **Known risk called out in-plan:** `_ENTAILMENT_IDX` must be confirmed against the model card (T4 note + T6 step 7) — a wrong index silently inverts the gate.
