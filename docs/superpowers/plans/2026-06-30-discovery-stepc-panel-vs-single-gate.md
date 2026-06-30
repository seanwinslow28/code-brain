# Step C Panel-vs-Single-Model Gate — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a controlled dual-fuse experiment harness that fuses one frozen evidence bundle through the full 4-model panel vs a single strong model, emitting blind-rateable A/B pain-point sets — to decide whether the panel earns its cost (gates E2).

**Architecture:** A reusable `EvidenceBundle` serializer freezes a gathered bundle to disk; a pure blind-rating renderer turns two pain-point sets into anonymized, deterministically-shuffled markdown + a separate key; an async experiment core (dependency-injectable gather/fuse/record for hermetic tests) runs gather-once → dual-fuse → record-spend-per-arm; a thin `click` CLI wires it to disk with a budget preflight and a cost-confirm gate.

**Tech Stack:** Python 3, `click`, `httpx` (existing), `dataclasses`, `hashlib`, `pytest`. All under `tools/llm-council/`.

## Global Constraints

- Run all commands from `tools/llm-council/` unless noted: `uv run pytest tests/ -q` (baseline **249 passed, 1 skipped**).
- Repo-root validator must stay green: `python3 scripts/validate.py`.
- **TDD**: write the failing test, watch it fail, implement minimally, watch it pass, commit.
- **No vault changes staged on this branch.** Branch: `feat/discovery-stepc-panel-vs-single-gate`.
- All non-test, non-trivial paid paths are dependency-injected so tests never hit network or `record_spend`'s real spend file.
- The judge stays `anthropic/claude-opus-4.7` in **both** arms; only `panel` (analysis_models) varies.
- Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

### Task 1: `EvidenceBundle` / `EvidenceRecord` serialization

**Files:**
- Modify: `tools/llm-council/council/discovery/evidence.py`
- Test: `tools/llm-council/tests/discovery/test_evidence_serialization.py`

**Interfaces:**
- Consumes: existing `EvidenceRecord` (frozen dataclass: `source_type, source_name, url, date, quote, engagement`) and `EvidenceBundle` (`records`, `add()`).
- Produces:
  - `EvidenceBundle.to_dict(self) -> dict` → `{"records": [ {record fields...}, ... ]}`
  - `EvidenceBundle.from_dict(d: dict) -> "EvidenceBundle"` (classmethod) → bundle rebuilt via `add()` so `_keys`/`urls` invariants are restored.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_evidence_serialization.py
from council.discovery.evidence import EvidenceBundle, EvidenceRecord


def _sample_bundle() -> EvidenceBundle:
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="reddit", source_name="r/ProductManagement",
                         url="https://example.com/a", date="2026-06-01",
                         quote="Prompts never give the same result twice.", engagement=42))
    b.add(EvidenceRecord(source_type="sonar", source_name="Perplexity Sonar",
                         url="https://example.com/b", date="", quote="Creators want a repeatable system."))
    return b


def test_to_dict_lists_all_records():
    b = _sample_bundle()
    d = b.to_dict()
    assert [r["url"] for r in d["records"]] == ["https://example.com/a", "https://example.com/b"]
    assert d["records"][0]["engagement"] == 42


def test_round_trip_equals_original():
    b = _sample_bundle()
    restored = EvidenceBundle.from_dict(b.to_dict())
    assert restored == b                      # records + _keys + urls all match
    assert restored.has_url("https://example.com/a")


def test_from_dict_restores_dedup_guard():
    b = _sample_bundle()
    restored = EvidenceBundle.from_dict(b.to_dict())
    # adding a duplicate of an existing record must be rejected (dedup key rebuilt)
    dup = EvidenceRecord(source_type="reddit", source_name="r/ProductManagement",
                         url="https://example.com/a", date="2026-06-01",
                         quote="Prompts never give the same result twice.", engagement=42)
    assert restored.add(dup) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_evidence_serialization.py -q`
Expected: FAIL — `AttributeError: ... has no attribute 'to_dict'` / `from_dict`.

- [ ] **Step 3: Write minimal implementation**

In `evidence.py`, add `from dataclasses import asdict` to the imports, then add these methods to `EvidenceBundle`:

```python
    def to_dict(self) -> dict:
        return {"records": [asdict(r) for r in self.records]}

    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceBundle":
        bundle = cls()
        for rd in d.get("records", []):
            bundle.add(EvidenceRecord(**rd))
        return bundle
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_evidence_serialization.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/evidence.py tools/llm-council/tests/discovery/test_evidence_serialization.py
git commit -m "feat(discovery): EvidenceBundle to_dict/from_dict round-trip serialization

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Blind-rating renderer + deterministic shuffle + key

**Files:**
- Create: `tools/llm-council/experiments/__init__.py` (empty)
- Create: `tools/llm-council/experiments/blind_rating.py`
- Test: `tools/llm-council/tests/discovery/test_blind_rating.py`

**Interfaces:**
- Consumes: `council.discovery.fusion.CandidatePainPoint` (`title, summary, quotes, urls, consensus, intensity, recency, segment`).
- Produces:
  - `build_blind_rating(arm_a: list[CandidatePainPoint], arm_b: list[CandidatePainPoint], topic: str) -> tuple[str, dict]`
  - Returns `(markdown, key)` where `key == {"Set 1": "A"|"B", "Set 2": "A"|"B"}`. Whether A maps to Set 1 or Set 2 is derived deterministically from `sha256(topic)` (stable across processes — NOT Python's salted `hash()`), so the run is reproducible while the rater stays blind.
  - Markdown contains the two sets under `## Set 1` / `## Set 2` headers with NO model names or arm labels, plus a fixed `## Rating criteria` block (signal density, evidence grounding, distinctness/dup-rate, actionability) and an instruction to pick a winner per criterion + overall.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_blind_rating.py
from council.discovery.fusion import CandidatePainPoint
from experiments.blind_rating import build_blind_rating


def _pt(title, summary="s", quotes=None, urls=None):
    return CandidatePainPoint(title=title, summary=summary,
                              quotes=quotes or ["q"], urls=urls or ["https://e.com/x"])


def test_key_maps_both_sets_to_distinct_arms():
    a = [_pt("Alpha pain")]
    b = [_pt("Beta pain")]
    md, key = build_blind_rating(a, b, topic="t")
    assert set(key.keys()) == {"Set 1", "Set 2"}
    assert set(key.values()) == {"A", "B"}


def test_shuffle_is_deterministic_per_topic():
    a, b = [_pt("Alpha pain")], [_pt("Beta pain")]
    _, key1 = build_blind_rating(a, b, topic="same-topic")
    _, key2 = build_blind_rating(a, b, topic="same-topic")
    assert key1 == key2


def test_markdown_hides_arm_identity_but_shows_content():
    a, b = [_pt("Alpha pain")], [_pt("Beta pain")]
    md, key = build_blind_rating(a, b, topic="t")
    assert "## Set 1" in md and "## Set 2" in md
    assert "Alpha pain" in md and "Beta pain" in md
    # no leakage of which arm is which
    assert "panel" not in md.lower() and "single" not in md.lower()
    assert "claude" not in md.lower() and "opus" not in md.lower()
    assert "Arm A" not in md and "Arm B" not in md
    assert "Rating criteria" in md
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_blind_rating.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'experiments'`.

- [ ] **Step 3: Write minimal implementation**

Create `experiments/__init__.py` (empty). Create `experiments/blind_rating.py`:

```python
"""Render two pain-point sets as anonymized, deterministically-shuffled blind-rating markdown."""

import hashlib

from council.discovery.fusion import CandidatePainPoint

_CRITERIA = (
    "## Rating criteria\n\n"
    "Rate each set on:\n"
    "1. **Signal density** — fraction of points naming a specific, real, recent user frustration (not generic).\n"
    "2. **Evidence grounding** — quotes/URLs that concretely support each point.\n"
    "3. **Distinctness / dup-rate** — are the points non-overlapping, or near-duplicates padding the count?\n"
    "4. **Actionability** — could a PM or creator act on this as an opportunity?\n\n"
    "Pick a winner per criterion, then an overall winner with a one-paragraph rationale. "
    "You are blind to how each set was produced — judge only the content.\n"
)


def _swap(topic: str) -> bool:
    """Deterministic, process-stable: True → A becomes Set 2 (sha256, not salted hash())."""
    return int(hashlib.sha256(topic.encode("utf-8")).hexdigest(), 16) % 2 == 1


def _render_set(points: list[CandidatePainPoint]) -> str:
    if not points:
        return "_(no pain points)_\n"
    lines = []
    for i, p in enumerate(points, 1):
        lines.append(f"{i}. **{p.title}** — {p.summary}")
        for q in p.quotes:
            lines.append(f"   - quote: \"{q}\"")
        for u in p.urls:
            lines.append(f"   - source: {u}")
    return "\n".join(lines) + "\n"


def build_blind_rating(arm_a: list[CandidatePainPoint], arm_b: list[CandidatePainPoint],
                       topic: str) -> tuple[str, dict]:
    if _swap(topic):
        set1, set2, key = arm_b, arm_a, {"Set 1": "B", "Set 2": "A"}
    else:
        set1, set2, key = arm_a, arm_b, {"Set 1": "A", "Set 2": "B"}
    md = (
        f"# Blind pain-point rating\n\n"
        f"Topic: {topic}\n\n"
        f"## Set 1\n\n{_render_set(set1)}\n"
        f"## Set 2\n\n{_render_set(set2)}\n"
        f"{_CRITERIA}"
    )
    return md, key
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_blind_rating.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/experiments/__init__.py tools/llm-council/experiments/blind_rating.py tools/llm-council/tests/discovery/test_blind_rating.py
git commit -m "feat(discovery): blind-rating renderer with deterministic per-topic shuffle + key

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Experiment core — gather-once → dual-fuse → record-per-arm

**Files:**
- Create: `tools/llm-council/experiments/panel_vs_single_core.py`
- Test: `tools/llm-council/tests/discovery/test_panel_vs_single_core.py`

**Interfaces:**
- Consumes: `get_tier` (`council.discovery.tiers`), `gather_evidence` (`council.discovery.gather`), `fuse` (`council.discovery.fusion`), `FusionResult`/`FusionError` (`council.discovery.fusion`), `record_spend` (`council.budget`), `EvidenceBundle` (Task 1).
- Produces:
  - `async def run_panel_vs_single(*, topic: str, tier_name: str, single_model: str, api_key: str, on_date, gather_fn=None, fuse_fn=None, record_fn=None) -> dict`
  - Returns `{"bundle": EvidenceBundle, "gather_status": dict, "arm_a": FusionResult, "arm_b": FusionResult, "cost": float}`.
  - Records spend once per arm via `record_fn` (default `record_spend`), `tool="discovery"`, `tag="discovery-experiment"`. Arm A is recorded before Arm B runs; if Arm B's fuse raises `FusionError`, its `.cost` is recorded before re-raising (no unrecorded spend).

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_panel_vs_single_core.py
import asyncio
from datetime import date

import pytest

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import FusionResult, FusionError, CandidatePainPoint
from experiments.panel_vs_single_core import run_panel_vs_single


def _bundle():
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="web", source_name="X", url="https://e.com/a", date="", quote="q"))
    return b


def test_both_arms_fuse_same_bundle_with_different_panels():
    bundle = _bundle()
    seen = []

    async def fake_gather(*, topic, tier, api_key, segment=""):
        return bundle, {"web": "ok: 1 records (1 found)"}

    async def fake_fuse(*, api_key, bundle, tier, topic):
        seen.append((id(bundle), tuple(tier.panel)))
        return FusionResult(pain_points=[CandidatePainPoint(title="t", summary="s", quotes=[], urls=[])], cost=0.1)

    records = []
    res = asyncio.run(run_panel_vs_single(
        topic="t", tier_name="standard", single_model="anthropic/claude-opus-4.7",
        api_key="k", on_date=date(2026, 6, 30),
        gather_fn=fake_gather, fuse_fn=fake_fuse,
        record_fn=lambda **kw: records.append(kw),
    ))
    # same bundle object both times; arm A panel has 4 models, arm B exactly 1
    assert seen[0][0] == seen[1][0]
    assert len(seen[0][1]) == 4
    assert seen[1][1] == ("anthropic/claude-opus-4.7",)
    # spend recorded once per arm, tagged discovery
    assert len(records) == 2
    assert all(r["tool"] == "discovery" and r["tag"] == "discovery-experiment" for r in records)
    assert res["arm_a"].cost == 0.1 and res["arm_b"].cost == 0.1
    assert res["cost"] == pytest.approx(0.2)


def test_arm_b_failure_still_records_arm_a_and_arm_b_cost():
    bundle = _bundle()
    calls = {"n": 0}

    async def fake_gather(*, topic, tier, api_key, segment=""):
        return bundle, {}

    async def fake_fuse(*, api_key, bundle, tier, topic):
        calls["n"] += 1
        if calls["n"] == 1:
            return FusionResult(cost=0.1)
        raise FusionError("arm B blew up", cost=0.05)

    records = []
    with pytest.raises(FusionError):
        asyncio.run(run_panel_vs_single(
            topic="t", tier_name="standard", single_model="anthropic/claude-opus-4.7",
            api_key="k", on_date=date(2026, 6, 30),
            gather_fn=fake_gather, fuse_fn=fake_fuse,
            record_fn=lambda **kw: records.append(kw),
        ))
    # both the successful arm-A cost and the failed arm-B cost are recorded
    assert [r["amount"] for r in records] == [0.1, 0.05]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_panel_vs_single_core.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'experiments.panel_vs_single_core'`.

- [ ] **Step 3: Write minimal implementation**

Create `experiments/panel_vs_single_core.py`:

```python
"""Experiment core: gather one bundle, fuse it through the full panel vs a single model."""

from dataclasses import replace

from council.budget import record_spend as _record_spend
from council.discovery.fusion import FusionError, fuse as _fuse
from council.discovery.gather import gather_evidence
from council.discovery.tiers import get_tier


async def run_panel_vs_single(*, topic, tier_name, single_model, api_key, on_date,
                              gather_fn=None, fuse_fn=None, record_fn=None) -> dict:
    tcfg = get_tier(tier_name)
    single_cfg = replace(tcfg, panel=(single_model,))
    gather = gather_fn or gather_evidence
    fuse = fuse_fn or _fuse
    record = record_fn or _record_spend

    def _bill(fr_cost: float) -> None:
        record(amount=round(fr_cost or 0.0, 6), profile=tier_name,
               tag="discovery-experiment", on_date=on_date, tool="discovery")

    bundle, gather_status = await gather(topic=topic, tier=tcfg, api_key=api_key)

    fr_a = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)
    _bill(fr_a.cost)

    try:
        fr_b = await fuse(api_key=api_key, bundle=bundle, tier=single_cfg, topic=topic)
    except FusionError as e:
        _bill(getattr(e, "cost", 0.0) or 0.0)   # record the failed arm's real spend before surfacing
        raise
    _bill(fr_b.cost)

    return {"bundle": bundle, "gather_status": gather_status,
            "arm_a": fr_a, "arm_b": fr_b, "cost": round((fr_a.cost or 0.0) + (fr_b.cost or 0.0), 6)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_panel_vs_single_core.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/experiments/panel_vs_single_core.py tools/llm-council/tests/discovery/test_panel_vs_single_core.py
git commit -m "feat(discovery): panel-vs-single experiment core (gather-once, dual-fuse, record-per-arm)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: CLI harness — preflight, confirm, write artifacts

**Files:**
- Create: `tools/llm-council/experiments/panel_vs_single.py`
- Test: `tools/llm-council/tests/discovery/test_panel_vs_single_cli.py`

**Interfaces:**
- Consumes: `run_panel_vs_single` (Task 3), `build_blind_rating` (Task 2), `EvidenceBundle.to_dict` (Task 1), `preflight_tool`/`BudgetExceeded` (`council.budget`), `CandidatePainPoint`.
- Produces:
  - `_write_artifacts(out_dir: Path, result: dict, topic: str) -> dict[str, Path]` — writes `bundle.json`, `arm-A.json`, `arm-B.json`, `blind-rating.md`, `key.json`; returns the path map. Pure I/O over an already-computed result → unit-testable without network.
  - A `click` command `main` (the module's `__main__`) wiring preflight → confirm → `asyncio.run(run_panel_vs_single(...))` → `_write_artifacts`.

The default topic constant lives here:
```python
DEFAULT_TOPIC = ("artists, writers, and designers who say AI is a slot machine — the same prompt never "
                 "gives the same result twice — and who have stopped chasing prompts in favor of "
                 "building a repeatable system they can trust")
```

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_panel_vs_single_cli.py
import json
from pathlib import Path

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import FusionResult, CandidatePainPoint
from experiments.panel_vs_single import _write_artifacts


def _result():
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="web", source_name="X", url="https://e.com/a", date="", quote="q"))
    fa = FusionResult(pain_points=[CandidatePainPoint(title="Alpha", summary="s", quotes=["qa"], urls=["https://e.com/a"])],
                      blind_spots=["bs"], contradictions=[], cost=0.12)
    fb = FusionResult(pain_points=[CandidatePainPoint(title="Beta", summary="s", quotes=["qb"], urls=["https://e.com/b"])],
                      cost=0.05)
    return {"bundle": b, "gather_status": {"web": "ok"}, "arm_a": fa, "arm_b": fb, "cost": 0.17}


def test_write_artifacts_emits_all_files_and_blind_key(tmp_path):
    paths = _write_artifacts(tmp_path, _result(), topic="t")
    for name in ("bundle.json", "arm-A.json", "arm-B.json", "blind-rating.md", "key.json"):
        assert (tmp_path / name).exists(), name
    # bundle round-trips
    bundle_d = json.loads((tmp_path / "bundle.json").read_text())
    assert EvidenceBundle.from_dict(bundle_d).has_url("https://e.com/a")
    # key maps both sets to distinct arms; blind md never names the arms
    key = json.loads((tmp_path / "key.json").read_text())
    assert set(key.values()) == {"A", "B"}
    md = (tmp_path / "blind-rating.md").read_text()
    assert "Alpha" in md and "Beta" in md
    assert "arm-A" not in md.lower() and "panel" not in md.lower()
    # arm json carries the real (unblinded) identity for the writeup
    arm_a = json.loads((tmp_path / "arm-A.json").read_text())
    assert arm_a["pain_points"][0]["title"] == "Alpha"
    assert arm_a["cost"] == 0.12
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_panel_vs_single_cli.py -q`
Expected: FAIL — `ImportError: cannot import name '_write_artifacts'`.

- [ ] **Step 3: Write minimal implementation**

Create `experiments/panel_vs_single.py`:

```python
"""CLI: panel-vs-single-model discovery gate. Gather once → dual-fuse → blind-rateable A/B."""

import asyncio
import json
import os
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from council.budget import BudgetExceeded, preflight_tool
from council.discovery.fusion import FusionResult
from council.discovery.tiers import get_tier
from experiments.blind_rating import build_blind_rating
from experiments.panel_vs_single_core import run_panel_vs_single

console = Console()
DISCOVERY_DAILY_CAP = 10.0
DISCOVERY_MONTHLY_CAP = 50.0
DEFAULT_TOPIC = ("artists, writers, and designers who say AI is a slot machine — the same prompt never "
                 "gives the same result twice — and who have stopped chasing prompts in favor of "
                 "building a repeatable system they can trust")


def _arm_payload(fr: FusionResult) -> dict:
    return {
        "pain_points": [asdict(p) for p in fr.pain_points],
        "blind_spots": list(fr.blind_spots),
        "contradictions": list(fr.contradictions),
        "cost": round(fr.cost or 0.0, 6),
    }


def _write_artifacts(out_dir: Path, result: dict, topic: str) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle.json").write_text(json.dumps(result["bundle"].to_dict(), indent=2))
    (out_dir / "arm-A.json").write_text(json.dumps(_arm_payload(result["arm_a"]), indent=2))
    (out_dir / "arm-B.json").write_text(json.dumps(_arm_payload(result["arm_b"]), indent=2))
    md, key = build_blind_rating(result["arm_a"].pain_points, result["arm_b"].pain_points, topic)
    (out_dir / "blind-rating.md").write_text(md)
    (out_dir / "key.json").write_text(json.dumps(key, indent=2))
    return {n: out_dir / n for n in ("bundle.json", "arm-A.json", "arm-B.json", "blind-rating.md", "key.json")}


@click.command()
@click.option("--topic", default=DEFAULT_TOPIC)
@click.option("--tier", "tier_name", type=click.Choice(["quick", "standard", "deep"]), default="standard")
@click.option("--single-model", default="anthropic/claude-opus-4.7")
@click.option("--out", type=click.Path(file_okay=False, path_type=Path), default=None)
@click.option("--yes", is_flag=True, help="Auto-confirm the dual-fuse cost.")
def main(topic, tier_name, single_model, out, yes):
    load_dotenv()
    tcfg = get_tier(tier_name)
    # Two fuse calls intentionally exceed a single-run cap, so gate on the DAILY cap, not per-run.
    estimated = round(tcfg.max_cost_per_run * 1.5, 4)
    try:
        preflight_tool(estimated=estimated, per_query_cap=DISCOVERY_DAILY_CAP,
                       daily_cap=DISCOVERY_DAILY_CAP, monthly_cap=DISCOVERY_MONTHLY_CAP,
                       on_date=date.today(), tool="discovery")
    except BudgetExceeded as e:
        console.print(f"[red]Budget rejected: {e}[/red]")
        raise SystemExit(2)

    console.print(f"[yellow]Dual-fuse (panel vs {single_model}) — estimated up to ${estimated:.2f} "
                  f"(2 real OpenRouter calls).[/yellow]")
    if not yes and not click.confirm("Proceed with the paid run?"):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(1)

    out_dir = out or Path("experiments/runs") / f"panel-vs-single-{time.strftime('%Y%m%d-%H%M%S')}"
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    result = asyncio.run(run_panel_vs_single(
        topic=topic, tier_name=tier_name, single_model=single_model,
        api_key=api_key, on_date=date.today(),
    ))
    paths = _write_artifacts(out_dir, result, topic)
    console.print(f"[green]Done.[/green] ${result['cost']:.4f} across both arms.")
    console.print(f"[dim]Artifacts: {out_dir}[/dim]")
    for p in paths.values():
        console.print(f"[dim] - {p}[/dim]")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_panel_vs_single_cli.py -q`
Expected: PASS (1 passed).

- [ ] **Step 5: Full suite + validator + commit**

```bash
uv run pytest tests/ -q          # expect 255 passed, 1 skipped (249 + 6 new)
cd ../.. && python3 scripts/validate.py && cd tools/llm-council
git add tools/llm-council/experiments/panel_vs_single.py tools/llm-council/tests/discovery/test_panel_vs_single_cli.py
git commit -m "feat(discovery): panel-vs-single CLI harness — preflight, confirm, blind A/B artifacts

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:**
- §3.1 serialization → Task 1. ✓
- §3.2 harness (preflight, gather-once, dual-fuse, record-per-arm, artifacts, blind+key) → Tasks 2 (blind+key), 3 (gather/dual-fuse/record), 4 (preflight/confirm/artifacts). ✓
- §3.3 council rating → executed *after* the build, manually (writes a prompt file from `blind-rating.md` and runs `python -m council`); not code, so no task. ✓
- §5 testing → each task is TDD; Task 4 Step 5 runs full suite + validator. ✓
- §6 out-of-scope (Sonar leak, production persistence, second topic) → not built; captured as tickets at session end. ✓

**Placeholder scan:** No TBD/TODO; every code step shows complete code. ✓

**Type consistency:** `to_dict`/`from_dict` (Task 1) used verbatim in Tasks 3-bundle and 4. `run_panel_vs_single` return dict keys (`bundle/arm_a/arm_b/cost`) consistent across Tasks 3 and 4. `build_blind_rating(a, b, topic) -> (md, key)` consistent Tasks 2 and 4. `record_fn(**kw)` keys (`amount/profile/tag/on_date/tool`) match `record_spend` signature. ✓

**Note on running the gate:** the harness is built + tested with NO paid call in this plan. The actual paid run (and the council rating + writeup) happens after the plan executes, with an explicit cost go-ahead from Sean.
