# D3 Discovery Dashboard + Session-Persistence Fix — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop the discovery session-persistence leak (persist by default) and ship a one-command, self-contained HTML dashboard over discovery run history.

**Architecture:** Slice A hardens `council/discovery/pipeline.py` — a `_write_session` helper used at all four write sites (including the empty-bundle early-return that currently writes nothing) plus a `_default_sessions_dir()` resolver so `run_discovery()` persists even when callers omit `sessions_dir`. Slice B adds `council/discovery/dashboard.py` (tolerant readers + aggregations + click CLI) and `council/discovery/dashboard_render.py` (Python-built inline SVG/CSS HTML — zero JS), invoked as `uv run python -m council.discovery.dashboard`.

**Tech Stack:** Python 3.12, stdlib + click (already a dep), pytest (+pytest-asyncio, already configured). No new dependencies. No network. $0.

**Spec:** `docs/superpowers/specs/2026-07-09-discovery-d3-dashboard-design.md`
**Branch:** `feat/discovery-d3-dashboard` (already created; spec committed)

## Global Constraints

- Baseline before this work: `cd tools/llm-council && uv run pytest tests/ -q` → **326 passed, 1 skipped**. Never regress it.
- All pytest commands run from `tools/llm-council/` via `uv run pytest …`.
- `python3 scripts/validate.py` (repo root) must stay PASSED.
- Session-JSON changes are **additive only** — no field removed or renamed.
- Caps are never hardcoded in the dashboard: per-run caps from `council.discovery.tiers`, $10/day + $50/mo from `council.discovery.__main__` (`DISCOVERY_DAILY_CAP` / `DISCOVERY_MONTHLY_CAP`).
- Dashboard render output is deterministic: `generated_at` is a parameter, never `datetime.now()` inside render code.
- Missing metrics on old runs render as explicit `n/a (…)` markers — never silently zeroed.
- Tests must be hermetic: nothing may write into the real `vault/` (Task 2 adds the autouse fixture guaranteeing this).
- Commit trailer: `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Do NOT touch `velocity_weight` (ticketed separately) or build PM3 persistence.

---

### Task 1: `_write_session` helper, empty-bundle write, session-schema additions

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py` (append)

**Interfaces:**
- Consumes: existing `run_discovery(...)` signature (default `sessions_dir=None` — unchanged in this task).
- Produces: module-level `_write_session(sessions_dir: Path | None, session_id: str, payload: dict) -> None` (Task 2 reuses it); session JSON schema now includes `segment` (all four payloads) and `lens`/`tier`/`cost_usd` on the empty-bundle payload. Dashboard tasks (3–5) rely on these keys.

- [ ] **Step 1: Write the failing tests**

Append to `tools/llm-council/tests/discovery/test_pipeline.py` (`json` and `Path` may need importing at top — `import json` is NOT currently imported there; add `import json` below the existing imports):

```python
# --- D3 Slice A: session persistence ---------------------------------------


def _empty_gather(gather_cost: float = 0.0):
    async def gather_fn(**kw):
        b = EvidenceBundle()
        b.gather_cost_usd = gather_cost
        return b, {"sonar": "ok: 0 records (0 found)"}
    return gather_fn


@pytest.mark.asyncio
async def test_empty_bundle_session_is_persisted(tmp_path):
    # THE LEAK: the empty-bundle early-return must write a session file when a dir is given.
    sdir = tmp_path / "sessions"
    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=_empty_gather(0.018), fuse_fn=None, sessions_dir=sdir)
    files = list(sdir.glob("*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data["empty"] is True
    assert data["lens"] == "pm"
    assert data["tier"] == "quick"
    assert data["segment"] == ""
    assert data["cost_usd"] == pytest.approx(0.018)
    assert data["id"] == res.session["id"]


@pytest.mark.asyncio
async def test_empty_bundle_bad_sessions_dir_does_not_crash(tmp_path):
    # Mirror the fuse-fail guard: a broken sessions_dir must never mask the run result.
    bad = tmp_path / "not-a-dir"
    bad.write_text("i am a file")
    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=_empty_gather(), fuse_fn=None, sessions_dir=bad)
    assert res.verified_count == 0          # returned normally despite failed write


@pytest.mark.asyncio
async def test_success_session_records_segment(tmp_path):
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18",
                              "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"],
                               ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=100, tokens_out=50, web_calls=0)

    sdir = tmp_path / "sessions"
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              segment="developer", sessions_dir=sdir, scorer=None)
    assert res.session["segment"] == "developer"
    data = json.loads(next(iter(sdir.glob("*.json"))).read_text())
    assert data["segment"] == "developer"


@pytest.mark.asyncio
async def test_failure_sessions_record_segment(tmp_path):
    # fuse-failure diagnostic session must carry segment too (re-run affordance needs it).
    from council.discovery.fusion import FusionError
    from council.discovery.pipeline import DiscoveryFailed
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "quote", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        raise FusionError("panel collapsed")

    sdir = tmp_path / "sessions"
    with pytest.raises(DiscoveryFailed):
        await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn,
                            segment="creative", sessions_dir=sdir)
    data = json.loads(next(iter(sdir.glob("*.json"))).read_text())
    assert data["segment"] == "creative"
    assert data["failed_stage"] == "fuse"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -q -k "persisted or bad_sessions_dir_does_not_crash or records_segment"`
Expected: 4 FAIL — empty-bundle tests find no file / `KeyError: 'segment'`.

- [ ] **Step 3: Implement in `pipeline.py`**

3a. Add the helper below `_normalize_segment` (module level):

```python
def _write_session(sessions_dir: Path | None, session_id: str, payload: dict) -> None:
    """Persist a session JSON. Never raises: a failed diagnostic write must not mask the
    run result or eat the spend record — warn on stderr and move on."""
    if sessions_dir is None:
        return
    try:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(payload, indent=2))
    except Exception as write_err:
        print(f"[discovery] failed to persist session {session_id}: {write_err}", file=sys.stderr)
```

3b. Empty-bundle early-return (`if not bundle.records:` block): build the session dict as a variable, add the new fields, write it, and return it:

```python
    if not bundle.records:
        md = render_ledger(topic=topic, lens=lens, tier=tier, segment=segment, cards=[],
                           quote_bank=[], fusion_result=FusionResult(), cost_usd=gather_cost,
                           dropped_count=0, supplement=None, verify_mode="substring-only")
        session = {"id": session_id, "topic": topic, "lens": lens, "tier": tier,
                   "segment": segment, "empty": True, "cost_usd": gather_cost,
                   "gather_status": gather_status,
                   "verify_mode": "substring-only",
                   "citation_precision": None, "citation_recall": None,
                   "velocity_mode": "off", "why_now_coverage": 0.0}
        _write_session(sessions_dir, session_id, session)
        return DiscoveryResult(markdown=md, cost_usd=gather_cost, verified_count=0,
                               dropped_count=0, session=session)
```

3c. Fuse-failure path: add `"segment": segment,` to `fail_session` (after `"tier": tier,`) and replace the inline `if sessions_dir is not None: try/except` write block with `_write_session(sessions_dir, session_id, fail_session)`.

3d. Success path: add `"segment": segment,` to the `session` dict (after `"tier": tier,`) and replace the inline `if sessions_dir is not None: mkdir/write` block with `_write_session(sessions_dir, session_id, session)`. (Behavior note, intended: a failed success-path write no longer aborts the run into `DiscoveryFailed` — the run and its spend record survive, matching the failure-path guards.)

3e. Post-fuse-failure path: add `"segment": segment,` to `fail_session` and replace its inline try/except write block with `_write_session(sessions_dir, session_id, fail_session)`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py tests/discovery/test_cli.py -q`
Expected: all pass (existing + 4 new).

- [ ] **Step 5: Full suite, then commit**

Run: `cd tools/llm-council && uv run pytest tests/ -q` → expect **330 passed, 1 skipped**.

```bash
git add tools/llm-council/council/discovery/pipeline.py tools/llm-council/tests/discovery/test_pipeline.py
git commit -m "fix(discovery): persist empty-bundle sessions; record segment in all session payloads

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Persist-by-default (`_default_sessions_dir` resolver + hermetic test fixture)

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py`
- Modify: `tools/llm-council/tests/discovery/conftest.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py` (append)

**Interfaces:**
- Consumes: `_write_session` and `_UNSET` from Task 1 / existing code.
- Produces: `_default_sessions_dir() -> Path | None` in `council.discovery.pipeline` (Task 6's CLI default reuses it); `run_discovery(..., sessions_dir=_UNSET)` — omitted arg now persists to the resolved default; explicit `None` disables; explicit `Path` unchanged. Env override: `DISCOVERY_SESSIONS_DIR`. Module constant `_REPO_ROOT` (monkeypatchable in tests).

- [ ] **Step 1: Add the hermetic autouse fixture FIRST**

Persist-by-default would make every existing test that omits `sessions_dir` write into the real vault. Append to `tools/llm-council/tests/discovery/conftest.py`:

```python
@pytest.fixture(autouse=True)
def _hermetic_sessions_dir(tmp_path, monkeypatch):
    """Persist-by-default (D3 Slice A) must never write into the real vault during tests:
    any test that omits sessions_dir resolves to a per-test tmp dir via the env override."""
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(tmp_path / "hermetic-sessions"))
    yield
```

- [ ] **Step 2: Write the failing tests**

Append to `tools/llm-council/tests/discovery/test_pipeline.py`:

```python
# --- D3 Slice A: persist-by-default resolution -------------------------------


def test_default_sessions_dir_env_wins(monkeypatch, tmp_path):
    from council.discovery import pipeline
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(tmp_path / "custom"))
    assert pipeline._default_sessions_dir() == tmp_path / "custom"


def test_default_sessions_dir_canonical_when_vault_exists(monkeypatch):
    from council.discovery import pipeline
    monkeypatch.delenv("DISCOVERY_SESSIONS_DIR", raising=False)
    d = pipeline._default_sessions_dir()
    assert d == pipeline._REPO_ROOT / "vault" / "20_projects" / "research" / ".discovery-sessions"


def test_default_sessions_dir_guard_disables_when_no_vault(monkeypatch, tmp_path, capsys):
    from council.discovery import pipeline
    monkeypatch.delenv("DISCOVERY_SESSIONS_DIR", raising=False)
    monkeypatch.setattr(pipeline, "_REPO_ROOT", tmp_path / "vendored-elsewhere")
    assert pipeline._default_sessions_dir() is None
    assert "persistence disabled" in capsys.readouterr().err


@pytest.mark.asyncio
async def test_run_discovery_persists_by_default(monkeypatch, tmp_path):
    # No sessions_dir arg at all → session lands in the resolved default.
    auto = tmp_path / "auto"
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(auto))
    await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                        gather_fn=_empty_gather(), fuse_fn=None)
    assert len(list(auto.glob("*.json"))) == 1


@pytest.mark.asyncio
async def test_run_discovery_explicit_none_disables_persistence(monkeypatch, tmp_path):
    auto = tmp_path / "auto"
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(auto))
    await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                        gather_fn=_empty_gather(), fuse_fn=None, sessions_dir=None)
    assert not auto.exists()
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -q -k "default_sessions_dir or persists_by_default or explicit_none"`
Expected: FAIL — `AttributeError: module ... has no attribute '_default_sessions_dir'`; the persist-by-default test finds no file.

- [ ] **Step 4: Implement in `pipeline.py`**

4a. Add `import os` to the stdlib imports.

4b. Below `_SEGMENT_OPERATOR_CHARS` add:

```python
# pipeline.py sits at <repo-root>/tools/llm-council/council/discovery/ → parents[4] = repo root.
_REPO_ROOT = Path(__file__).resolve().parents[4]


def _default_sessions_dir() -> Path | None:
    """Resolve where sessions persist when the caller doesn't say (D3 Slice A: persist by
    default — an un-persisted run is history we can't recover). $DISCOVERY_SESSIONS_DIR wins;
    else the canonical vault store, guarded so a vendored copy of this package never writes
    to a surprising location."""
    raw = os.environ.get("DISCOVERY_SESSIONS_DIR")
    if raw:
        return Path(raw)
    if (_REPO_ROOT / "vault").is_dir():
        return _REPO_ROOT / "vault" / "20_projects" / "research" / ".discovery-sessions"
    print("[discovery] no DISCOVERY_SESSIONS_DIR and no repo vault — session persistence disabled",
          file=sys.stderr)
    return None
```

4c. Change the `run_discovery` signature: `sessions_dir: Path | None = None` → `sessions_dir=_UNSET` (matching the `scorer`/`velocity_provider` sentinel style; keep the docstring-free style of the file). First line inside the function body, before `tcfg = get_tier(tier)`:

```python
    if sessions_dir is _UNSET:
        sessions_dir = _default_sessions_dir()
```

- [ ] **Step 5: Run the full suite**

Run: `cd tools/llm-council && uv run pytest tests/ -q`
Expected: **335 passed, 1 skipped**, and zero files created under the real `vault/20_projects/research/.discovery-sessions/` (verify: `git status` clean apart from staged work; `ls vault/20_projects/research/.discovery-sessions/ | wc -l` still 5 from repo root).

- [ ] **Step 6: Commit**

```bash
git add tools/llm-council/council/discovery/pipeline.py tools/llm-council/tests/discovery/test_pipeline.py tools/llm-council/tests/discovery/conftest.py
git commit -m "feat(discovery): persist sessions by default (env-overridable, guarded canonical path)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Dashboard readers (`dashboard.py`: sessions + spend, tolerant)

**Files:**
- Create: `tools/llm-council/council/discovery/dashboard.py`
- Test: `tools/llm-council/tests/discovery/test_dashboard.py` (create)

**Interfaces:**
- Consumes: nothing from other tasks (pure file readers).
- Produces (Tasks 4–6 rely on these exact names):
  - `load_sessions(sessions_dir: Path) -> tuple[list[dict], list[tuple[str, str]]]` — `(sessions, skipped)`. Sessions sorted by `_date`/`id`; each dict gains `_file` (filename), `_kind` (`"success" | "failure" | "empty"`), `_date` (`YYYY-MM-DD` from the id, `""` if unparseable). `skipped` is `(filename, reason)` for foreign/malformed files.
  - `load_spend(spend_dir: Path) -> tuple[list[SpendDay], list[tuple[str, str]]]`
  - `@dataclass SpendDay: date: str; discovery_total: float; runs: list[dict]` (runs filtered to `tool == "discovery"`; `discovery_total` sums those amounts, NOT the file's `total`).

- [ ] **Step 1: Write the failing tests**

Create `tools/llm-council/tests/discovery/test_dashboard.py`:

```python
# tests/discovery/test_dashboard.py
import json

import pytest

from council.discovery.dashboard import SpendDay, load_sessions, load_spend

SUCCESS_SESSION = {
    "id": "20260707-101500-abc123", "topic": "ai coding agents", "lens": "pm",
    "tier": "standard", "segment": "developer", "evidence_count": 40, "verified": 9,
    "dropped": 2, "merged_count": 1, "cost_usd": 1.05,
    "gather_status": {"sonar": "ok: 15 records (15 found)", "web": "ok: 6 records (6 found)"},
    "blind_spots": [], "contradictions": [], "supplement": None,
    "verify_mode": "nli", "citation_precision": 0.97, "citation_recall": 0.88,
    "velocity_mode": "off", "why_now_coverage": 0.0,
}

PRE_E1_SESSION = {  # 2026-06-21 vintage: no citation/velocity/merged/segment keys
    "id": "20260621-133044-0c8894", "topic": "2D animation pipelines", "lens": "pm",
    "tier": "standard", "evidence_count": 26, "verified": 12, "dropped": 0,
    "cost_usd": 2.7369, "gather_status": {"sonar": "ok: 15 records (15 found)"},
    "blind_spots": [], "contradictions": [],
}

FAILURE_SESSION = {
    "id": "20260630-172729-4ee6bd", "topic": "broken run", "lens": "pm", "tier": "quick",
    "evidence_count": 12, "gather_status": {"sonar": "ok: 12 records (12 found)"},
    "failed_stage": "fuse", "error": "panel collapsed", "cost_usd": 0.11,
}

EMPTY_SESSION = {
    "id": "20260709-090000-eeeeee", "topic": "niche topic", "lens": "pm", "tier": "quick",
    "segment": "", "empty": True, "cost_usd": 0.018,
    "gather_status": {"sonar": "ok: 0 records (0 found)"},
    "verify_mode": "substring-only", "citation_precision": None, "citation_recall": None,
    "velocity_mode": "off", "why_now_coverage": 0.0,
}

FOREIGN_BUNDLE = {  # pm3-t0 shape: an evidence-bundle capture, not a session record
    "stamp": "t0", "date": "2026-06-30", "topic": "ai coding assistants",
    "tier": "standard", "lens": "pm", "verified_count": 8, "dropped_count": 2,
    "cost_usd": 1.8465, "evidence_count": 93, "gather_cost_usd": 0.02984,
    "bundle": {"records": [], "gather_cost_usd": 0.02984},
}


def _write_sessions(d, **files):
    d.mkdir(parents=True, exist_ok=True)
    for name, payload in files.items():
        p = d / f"{name}.json"
        p.write_text(payload if isinstance(payload, str) else json.dumps(payload))


def test_load_sessions_classifies_and_sorts(tmp_path):
    d = tmp_path / "s"
    _write_sessions(d, ok=SUCCESS_SESSION, old=PRE_E1_SESSION,
                    fail=FAILURE_SESSION, empty=EMPTY_SESSION)
    sessions, skipped = load_sessions(d)
    assert skipped == []
    assert [s["_kind"] for s in sessions] == ["success", "failure", "success", "empty"]
    assert [s["_date"] for s in sessions] == ["2026-06-21", "2026-06-30", "2026-07-07", "2026-07-09"]
    assert sessions[0]["_file"] == "old.json"


def test_load_sessions_skips_foreign_and_malformed(tmp_path):
    d = tmp_path / "s"
    _write_sessions(d, ok=SUCCESS_SESSION, bundle=FOREIGN_BUNDLE, broken="{not json")
    sessions, skipped = load_sessions(d)
    assert len(sessions) == 1
    reasons = dict(skipped)
    assert "foreign" in reasons["bundle.json"]
    assert "malformed" in reasons["broken.json"]


def test_load_sessions_missing_dir(tmp_path):
    sessions, skipped = load_sessions(tmp_path / "nope")
    assert sessions == [] and skipped == []


def test_load_spend_filters_to_discovery(tmp_path):
    d = tmp_path / "health"
    d.mkdir()
    (d / "council-spend-2026-07-07.json").write_text(json.dumps({
        "date": "2026-07-07", "total": 1.34,
        "runs": [
            {"amount": 1.0485, "profile": "standard", "tag": "discovery-pm", "tool": "discovery"},
            {"amount": 0.29, "profile": "premium", "tag": "critique", "tool": "council"},
        ],
    }))
    (d / "council-spend-2026-07-05.json").write_text(json.dumps({
        "date": "2026-07-05", "total": 0.29,
        "runs": [{"amount": 0.29, "profile": "premium", "tag": "critique", "tool": "council"}],
    }))
    days, skipped = load_spend(d)
    assert skipped == []
    assert [f"{x.date}:{x.discovery_total}" for x in days] == ["2026-07-05:0.0", "2026-07-07:1.0485"]
    assert len(days[1].runs) == 1


def test_load_spend_skips_malformed(tmp_path):
    d = tmp_path / "health"
    d.mkdir()
    (d / "council-spend-2026-07-01.json").write_text("{oops")
    days, skipped = load_spend(d)
    assert days == []
    assert skipped and "malformed" in skipped[0][1]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.dashboard'`.

- [ ] **Step 3: Implement the readers**

Create `tools/llm-council/council/discovery/dashboard.py`:

```python
# council/discovery/dashboard.py
"""D3 — discovery dashboard: readers + aggregations + CLI over run history.

Reads session JSONs (written by pipeline.py) and council-spend ledgers, renders one
self-contained HTML artifact (see dashboard_render.py). $0: local files only.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

# Session id "YYYYMMDD-HHMMSS-hex" → "YYYY-MM-DD".
_ID_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})-")


def _session_date(session_id: str) -> str:
    m = _ID_DATE.match(session_id or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def _classify(payload: dict) -> str | None:
    """A session record is one of success/failure/empty; anything else (e.g. the pm3-t0
    evidence-bundle capture) is foreign — skipped honestly, never guessed at."""
    if not isinstance(payload, dict) or "id" not in payload:
        return None
    if payload.get("failed_stage"):
        return "failure"
    if payload.get("empty"):
        return "empty"
    if "verified" in payload:
        return "success"
    return None


def load_sessions(sessions_dir: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    """Parse every *.json in sessions_dir → (sessions, skipped). Each session gains
    _file/_kind/_date. Tolerant by design: malformed or foreign files are skipped and
    reported, never fatal."""
    sessions: list[dict] = []
    skipped: list[tuple[str, str]] = []
    if not sessions_dir.is_dir():
        return sessions, skipped
    for path in sorted(sessions_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as e:
            skipped.append((path.name, f"malformed JSON ({e.__class__.__name__})"))
            continue
        kind = _classify(payload)
        if kind is None:
            skipped.append((path.name, "foreign shape (not a session record)"))
            continue
        payload["_file"] = path.name
        payload["_kind"] = kind
        payload["_date"] = _session_date(payload.get("id", ""))
        sessions.append(payload)
    sessions.sort(key=lambda s: s.get("id", ""))
    return sessions, skipped


@dataclass
class SpendDay:
    date: str
    discovery_total: float
    runs: list[dict]


def load_spend(spend_dir: Path) -> tuple[list[SpendDay], list[tuple[str, str]]]:
    """Parse council-spend-*.json → (days, skipped), keeping only tool=="discovery" runs
    so council spend never pollutes discovery totals."""
    days: list[SpendDay] = []
    skipped: list[tuple[str, str]] = []
    if not spend_dir.is_dir():
        return days, skipped
    for path in sorted(spend_dir.glob("council-spend-*.json")):
        try:
            payload = json.loads(path.read_text())
            runs = [r for r in payload.get("runs", []) if r.get("tool") == "discovery"]
            days.append(SpendDay(date=payload["date"],
                                 discovery_total=round(sum(r.get("amount", 0.0) for r in runs), 4),
                                 runs=runs))
        except (json.JSONDecodeError, OSError, KeyError, TypeError) as e:
            skipped.append((path.name, f"malformed ledger ({e.__class__.__name__})"))
    days.sort(key=lambda d: d.date)
    return days, skipped
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard.py -q`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dashboard.py tools/llm-council/tests/discovery/test_dashboard.py
git commit -m "feat(discovery): dashboard readers — tolerant session + spend loading

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Aggregations + re-run command reconstruction (`dashboard.py`)

**Files:**
- Modify: `tools/llm-council/council/discovery/dashboard.py` (append)
- Test: `tools/llm-council/tests/discovery/test_dashboard.py` (append)

**Interfaces:**
- Consumes: `load_sessions` / `load_spend` shapes from Task 3.
- Produces (Task 5's renderer relies on these exact names):
  - `collector_yield(sessions: list[dict]) -> dict[str, dict]` — per collector: `{"records": int, "found": int, "ok_runs": int, "runs": int, "errors": list[str]}` (unknown status strings land verbatim in `errors`).
  - `fuse_stats(sessions) -> dict` — `{"success": int, "failure": int, "empty": int, "rate": float | None}` (rate = success / (success + failure), `None` when no fuse attempts).
  - `month_totals(days: list[SpendDay]) -> dict[str, float]` — `"YYYY-MM" → discovery total`.
  - `discrepancies(sessions, days) -> list[str]` — human-readable ledger/session mismatch lines.
  - `rerun_command(session: dict) -> str` — copy-ready CLI line.
  - `_slug(text: str) -> str` — lowercase, non-alnum → `-`, collapsed, ≤60 chars.

- [ ] **Step 1: Write the failing tests**

Append to `tools/llm-council/tests/discovery/test_dashboard.py`:

```python
from council.discovery.dashboard import (
    collector_yield, discrepancies, fuse_stats, month_totals, rerun_command,
)


def _rows(*payloads):
    out = []
    for p in payloads:
        q = dict(p)
        q.setdefault("_kind", "failure" if q.get("failed_stage") else
                     "empty" if q.get("empty") else "success")
        q["_date"] = q["id"][:4] + "-" + q["id"][4:6] + "-" + q["id"][6:8]
        q.setdefault("_file", q["id"] + ".json")
        out.append(q)
    return out


def test_collector_yield_parses_ok_and_keeps_errors_verbatim():
    rows = _rows(SUCCESS_SESSION,
                 {**PRE_E1_SESSION, "gather_status": {"sonar": "error: 429 too many requests"}})
    y = collector_yield(rows)
    assert y["sonar"]["records"] == 15 and y["sonar"]["found"] == 15
    assert y["sonar"]["ok_runs"] == 1 and y["sonar"]["runs"] == 2
    assert y["sonar"]["errors"] == ["error: 429 too many requests"]
    assert y["web"]["records"] == 6


def test_fuse_stats_counts_kinds():
    s = fuse_stats(_rows(SUCCESS_SESSION, PRE_E1_SESSION, FAILURE_SESSION, EMPTY_SESSION))
    assert s == {"success": 2, "failure": 1, "empty": 1, "rate": pytest.approx(2 / 3)}


def test_fuse_stats_no_attempts():
    assert fuse_stats(_rows(EMPTY_SESSION))["rate"] is None


def test_month_totals():
    days = [SpendDay("2026-06-30", 1.85, []), SpendDay("2026-07-05", 0.0, []),
            SpendDay("2026-07-07", 1.0485, [])]
    assert month_totals(days) == {"2026-06": 1.85, "2026-07": 1.0485}


def test_discrepancies_both_directions():
    rows = _rows(SUCCESS_SESSION)                      # session on 2026-07-07, cost > 0
    days = [SpendDay("2026-07-05", 0.5, [{}])]         # spend on a day with no session
    lines = discrepancies(rows, days)
    assert any("2026-07-07" in ln and "no discovery spend" in ln for ln in lines)
    assert any("2026-07-05" in ln and "no session" in ln for ln in lines)


def test_rerun_command_full_and_pre_fix():
    full = rerun_command(_rows(SUCCESS_SESSION)[0])
    assert full.startswith('uv run python -m council.discovery "ai coding agents"')
    assert "--lens pm" in full and "--tier standard" in full
    assert '--segment "developer"' in full
    assert "--output vault/20_projects/research/ai-coding-agents-rerun-idea-ledger.md" in full
    pre = rerun_command(_rows(PRE_E1_SESSION)[0])
    assert "--segment" not in pre                       # pre-fix run: segment unrecorded
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard.py -q`
Expected: ImportError on the new names.

- [ ] **Step 3: Implement**

Append to `tools/llm-council/council/discovery/dashboard.py`:

```python
_GATHER_OK = re.compile(r"^ok: (\d+) records \((\d+) found\)")


def collector_yield(sessions: list[dict]) -> dict[str, dict]:
    """Aggregate per-collector yield from gather_status strings. Unknown formats are kept
    verbatim as errors — never guessed into numbers."""
    out: dict[str, dict] = {}
    for s in sessions:
        for collector, status in (s.get("gather_status") or {}).items():
            slot = out.setdefault(collector, {"records": 0, "found": 0,
                                              "ok_runs": 0, "runs": 0, "errors": []})
            slot["runs"] += 1
            m = _GATHER_OK.match(str(status))
            if m:
                slot["records"] += int(m.group(1))
                slot["found"] += int(m.group(2))
                slot["ok_runs"] += 1
            else:
                slot["errors"].append(str(status))
    return out


def fuse_stats(sessions: list[dict]) -> dict:
    counts = {"success": 0, "failure": 0, "empty": 0}
    for s in sessions:
        counts[s["_kind"]] += 1
    attempts = counts["success"] + counts["failure"]
    return {**counts, "rate": (counts["success"] / attempts) if attempts else None}


def month_totals(days: list["SpendDay"]) -> dict[str, float]:
    out: dict[str, float] = {}
    for d in days:
        month = d.date[:7]
        out[month] = round(out.get(month, 0.0) + d.discovery_total, 4)
    return out


def discrepancies(sessions: list[dict], days: list["SpendDay"]) -> list[str]:
    """Session/ledger mismatches, flagged instead of papered over."""
    session_dates = {s["_date"] for s in sessions if s.get("cost_usd") and s["_date"]}
    ledger_dates = {d.date for d in days if d.discovery_total > 0}
    lines = []
    for date in sorted(session_dates - ledger_dates):
        lines.append(f"{date}: session(s) with cost recorded but no discovery spend in the ledger")
    for date in sorted(ledger_dates - session_dates):
        lines.append(f"{date}: discovery spend in the ledger but no session file (pre-fix leak?)")
    return lines


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:60].rstrip("-") or "topic"


def rerun_command(session: dict) -> str:
    """Copy-ready re-run of this topic. Pre-fix sessions lack segment — omit the flag."""
    parts = [f'uv run python -m council.discovery "{session.get("topic", "")}"',
             f"--lens {session.get('lens', 'pm')}", f"--tier {session.get('tier', 'standard')}"]
    segment = session.get("segment")
    if segment:
        parts.append(f'--segment "{segment}"')
    parts.append(f"--output vault/20_projects/research/{_slug(session.get('topic', ''))}-rerun-idea-ledger.md")
    return " ".join(parts)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard.py -q`
Expected: all pass (12 total in this file).

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dashboard.py tools/llm-council/tests/discovery/test_dashboard.py
git commit -m "feat(discovery): dashboard aggregations + re-run command reconstruction

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: HTML renderer (`dashboard_render.py`)

**Files:**
- Create: `tools/llm-council/council/discovery/dashboard_render.py`
- Test: `tools/llm-council/tests/discovery/test_dashboard_render.py` (create)

**Interfaces:**
- Consumes: session dicts (`_kind`/`_date` injected), `SpendDay`, and every Task-4 function (`collector_yield`, `fuse_stats`, `month_totals`, `discrepancies`, `rerun_command`).
- Produces: `render_dashboard(sessions, skipped_sessions, spend_days, skipped_spend, *, generated_at: str, sessions_dir: Path) -> str` (Task 6's CLI calls exactly this). Constants `THIN_THRESHOLD = 10`.
- Caps: `DISCOVERY_DAILY_CAP`/`DISCOVERY_MONTHLY_CAP` imported from `council.discovery.__main__`; per-tier `max_cost_per_run` via `council.discovery.tiers.get_tier`.

- [ ] **Step 1: Write the failing tests**

Create `tools/llm-council/tests/discovery/test_dashboard_render.py`:

```python
# tests/discovery/test_dashboard_render.py
from pathlib import Path

from council.discovery.dashboard import SpendDay
from council.discovery.dashboard_render import render_dashboard
from tests.discovery.test_dashboard import (
    EMPTY_SESSION, FAILURE_SESSION, PRE_E1_SESSION, SUCCESS_SESSION, _rows,
)

GEN = "2026-07-09 12:00"
SDIR = Path("/tmp/sessions")


def _render(sessions=(), skipped_sessions=(), days=(), skipped_spend=()):
    return render_dashboard(list(sessions), list(skipped_sessions), list(days),
                            list(skipped_spend), generated_at=GEN, sessions_dir=SDIR)


def test_thin_badge_and_header():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert "thin: 1 runs" in html
    assert GEN in html


def test_empty_state_names_dir_and_fix():
    html = _render()
    assert str(SDIR) in html
    assert "persist" in html.lower()          # points at the Slice A fix


def test_run_table_metrics_and_na_markers():
    html = _render(sessions=_rows(SUCCESS_SESSION, PRE_E1_SESSION))
    assert "ai coding agents" in html
    assert "0.97" in html and "0.88" in html            # citation P/R when present
    assert "n/a (pre-E1 run)" in html                    # missing citation keys on old run
    assert "n/a (pre-E4 run)" in html                    # missing velocity keys on old run
    assert "why-now" in html.lower()


def test_spend_section_uses_caps():
    html = _render(sessions=_rows(SUCCESS_SESSION),
                   days=[SpendDay("2026-07-07", 1.0485, [{"amount": 1.0485}])])
    assert "$10.00/day" in html and "$50.00/mo" in html
    assert "1.05" in html
    # per-run tier cap from tiers.py (standard = $1.50), never hardcoded prose
    assert "1.50" in html


def test_failure_and_health_section():
    html = _render(sessions=_rows(SUCCESS_SESSION, FAILURE_SESSION, EMPTY_SESSION))
    assert "panel collapsed" in html
    assert "fuse" in html
    assert "sonar" in html


def test_rerun_block_present():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert 'uv run python -m council.discovery "ai coding agents"' in html


def test_footer_lists_skipped_files():
    html = _render(sessions=_rows(SUCCESS_SESSION),
                   skipped_sessions=[("pm3-t0-ai-coding-assistants-2026-06-30.json",
                                      "foreign shape (not a session record)")],
                   skipped_spend=[("council-spend-2026-07-01.json", "malformed ledger (KeyError)")])
    assert "pm3-t0-ai-coding-assistants-2026-06-30.json" in html
    assert "council-spend-2026-07-01.json" in html


def test_pm3_slot_and_discrepancies():
    html = _render(sessions=_rows(SUCCESS_SESSION), days=[SpendDay("2026-07-05", 0.5, [{}])])
    assert "Pain-taxonomy movement" in html and "7/21" in html
    assert "no session" in html                          # 07-05 spend, no session


def test_topic_html_escaped():
    evil = {**SUCCESS_SESSION, "topic": "<script>alert(1)</script>"}
    html = _render(sessions=_rows(evil))
    assert "<script>alert(1)" not in html
    assert "&lt;script&gt;" in html


def test_no_javascript():
    html = _render(sessions=_rows(SUCCESS_SESSION))
    assert "<script" not in html
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard_render.py -q`
Expected: `ModuleNotFoundError: No module named 'council.discovery.dashboard_render'`.

- [ ] **Step 3: Implement the renderer**

Create `tools/llm-council/council/discovery/dashboard_render.py`:

```python
# council/discovery/dashboard_render.py
"""D3 dashboard HTML: Python-built inline SVG + CSS, zero JS, one self-contained file.
Honesty rules: a global thin badge under THIN_THRESHOLD runs; missing metrics render as
explicit n/a markers (pre-E1 / pre-E4 vintage), never zeros; skipped files are listed."""

import html
from pathlib import Path

from council.discovery.__main__ import DISCOVERY_DAILY_CAP, DISCOVERY_MONTHLY_CAP
from council.discovery.dashboard import (
    SpendDay, collector_yield, discrepancies, fuse_stats, month_totals, rerun_command,
)
from council.discovery.tiers import TIERS

THIN_THRESHOLD = 10

_CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;margin:2rem auto;
     max-width:1100px;padding:0 1rem;background:#0f1115;color:#d7dae0}
h1{font-size:1.4rem} h2{font-size:1.05rem;margin-top:2rem;border-bottom:1px solid #2a2f3a;
     padding-bottom:.3rem} table{border-collapse:collapse;width:100%;font-size:.82rem}
th,td{padding:.35rem .5rem;text-align:left;border-bottom:1px solid #232833;vertical-align:top}
th{color:#8b93a5;font-weight:600} .na{color:#6a7285;font-style:italic}
.badge{display:inline-block;background:#5c4a00;color:#ffd75e;border-radius:4px;
       padding:.1rem .45rem;font-size:.75rem;margin-left:.5rem}
.ok{color:#7bd88f} .bad{color:#ff7a7a} .dim{color:#8b93a5;font-size:.78rem}
.bar{background:#1b202b;border-radius:3px;height:10px;width:180px;display:inline-block;
     vertical-align:middle;margin-right:.5rem}
.bar>i{display:block;height:100%;border-radius:3px;background:#4c8dff}
.bar>i.over{background:#ff7a7a}
pre{background:#161a22;border:1px solid #232833;border-radius:6px;padding:.5rem .7rem;
    font-size:.78rem;overflow-x:auto;white-space:pre-wrap}
footer{margin-top:2.5rem;color:#6a7285;font-size:.75rem}
"""


def _e(text) -> str:
    return html.escape(str(text))


def _na(label: str = "") -> str:
    return f'<span class="na">n/a{f" ({label})" if label else ""}</span>'


def _metric(session: dict, key: str, vintage: str, fmt=lambda v: f"{v}") -> str:
    """Missing key = the run predates the feature (honest vintage label);
    key present but None = the run degraded (plain n/a)."""
    if key not in session:
        return _na(vintage)
    value = session[key]
    return _na() if value is None else fmt(value)


def _cap_bar(amount: float, cap: float) -> str:
    pct = min(100.0, (amount / cap) * 100.0) if cap else 0.0
    over = " over" if amount > cap else ""
    return (f'<span class="bar"><i class="{over.strip()}" style="width:{pct:.0f}%"></i></span>'
            f"${amount:.2f}")


def _mini_bars(values: list[int], color: str = "#4c8dff") -> str:
    """Inline-SVG mini bar chart (verified/dropped trend)."""
    if not values:
        return _na()
    top = max(max(values), 1)
    width, gap, h = 9, 3, 26
    bars = []
    for i, v in enumerate(values):
        bh = max(1, round((v / top) * (h - 2)))
        bars.append(f'<rect x="{i * (width + gap)}" y="{h - bh}" width="{width}" '
                    f'height="{bh}" fill="{color}" rx="1"/>')
    total_w = len(values) * (width + gap)
    return f'<svg width="{total_w}" height="{h}" role="img">{"".join(bars)}</svg>'


def _tier_cap(tier: str) -> float | None:
    cfg = TIERS.get(tier)
    return cfg.max_cost_per_run if cfg else None


def _run_rows(sessions: list[dict]) -> str:
    rows = []
    for s in sessions:
        cap = _tier_cap(s.get("tier", ""))
        cost = s.get("cost_usd")
        cost_cell = (_na() if cost is None else
                     f"${cost:.2f}" + (f' <span class="dim">/ ${cap:.2f} cap</span>' if cap else ""))
        if s["_kind"] == "failure":
            status = f'<span class="bad">failed: {_e(s.get("failed_stage", "?"))}</span>'
        elif s["_kind"] == "empty":
            status = '<span class="dim">empty gather</span>'
        else:
            status = '<span class="ok">ok</span>'
        rows.append(f"""<tr>
<td>{_e(s["_date"] or "?")}</td><td>{_e(s.get("topic", ""))}</td>
<td>{_e(s.get("lens", ""))}/{_e(s.get("tier", ""))}</td>
<td>{_metric(s, "segment", "pre-fix run", lambda v: _e(v) if v else '<span class="dim">—</span>')}</td>
<td>{status}</td>
<td>{_metric(s, "evidence_count", "")}</td>
<td>{_metric(s, "verified", "")} / {_metric(s, "dropped", "")} / {_metric(s, "merged_count", "pre-E3 run")}</td>
<td>{_metric(s, "verify_mode", "pre-E1 run", _e)}</td>
<td>{_metric(s, "citation_precision", "pre-E1 run", lambda v: f"{v:.2f}")} /
    {_metric(s, "citation_recall", "pre-E1 run", lambda v: f"{v:.2f}")}</td>
<td>{_metric(s, "velocity_mode", "pre-E4 run", _e)}</td>
<td>{_metric(s, "why_now_coverage", "pre-E4 run", lambda v: f"{v * 100:.0f}%")}</td>
<td>{cost_cell}</td></tr>""")
    return "".join(rows)


def render_dashboard(sessions: list[dict], skipped_sessions: list[tuple[str, str]],
                     spend_days: list[SpendDay], skipped_spend: list[tuple[str, str]],
                     *, generated_at: str, sessions_dir: Path) -> str:
    n = len(sessions)
    thin = f'<span class="badge">⚠ thin: {n} runs</span>' if n < THIN_THRESHOLD else ""
    parts = [f"<style>{_CSS}</style>",
             f"<h1>fusion-discovery-council — run dashboard{thin}</h1>",
             f'<p class="dim">generated {_e(generated_at)} · {n} session(s) · '
             f"source: {_e(sessions_dir)}</p>"]

    if not sessions:
        parts.append(
            f"<p><b>No session history found</b> in <code>{_e(sessions_dir)}</code>. "
            "Runs before the persist-by-default fix (D3 Slice A) were not persisted; "
            "new runs will appear here automatically.</p>")

    # Spend vs caps
    parts.append(f"<h2>Spend vs caps <span class='dim'>(${DISCOVERY_DAILY_CAP:.2f}/day · "
                 f"${DISCOVERY_MONTHLY_CAP:.2f}/mo)</span></h2>")
    if spend_days:
        day_rows = "".join(
            f"<tr><td>{_e(d.date)}</td><td>{_cap_bar(d.discovery_total, DISCOVERY_DAILY_CAP)}</td>"
            f"<td class='dim'>{len(d.runs)} run(s)</td></tr>" for d in spend_days)
        parts.append(f"<table><tr><th>day</th><th>discovery spend vs $"
                     f"{DISCOVERY_DAILY_CAP:.2f}/day</th><th></th></tr>{day_rows}</table>")
        months = "".join(
            f"<tr><td>{_e(m)}</td><td>{_cap_bar(total, DISCOVERY_MONTHLY_CAP)}</td></tr>"
            for m, total in sorted(month_totals(spend_days).items()))
        parts.append(f"<table><tr><th>month</th><th>vs ${DISCOVERY_MONTHLY_CAP:.2f}/mo</th></tr>"
                     f"{months}</table>")
    else:
        parts.append("<p class='dim'>No discovery spend recorded in the ledgers.</p>")

    # Run history
    parts.append("<h2>Run history</h2>")
    if sessions:
        ok = [s for s in sessions if s["_kind"] == "success"]
        trend = (f"<p class='dim'>verified trend {_mini_bars([s.get('verified') or 0 for s in ok])}"
                 f" · dropped trend {_mini_bars([s.get('dropped') or 0 for s in ok], '#ff7a7a')}</p>"
                 if ok else "")
        parts.append(trend)
        parts.append("<table><tr><th>date</th><th>topic</th><th>lens/tier</th><th>segment</th>"
                     "<th>status</th><th>evidence</th><th>verified/dropped/merged</th>"
                     "<th>verify</th><th>citation P/R</th><th>velocity</th>"
                     "<th>why-now coverage</th><th>cost</th></tr>"
                     f"{_run_rows(sessions)}</table>")

    # Pipeline health
    parts.append("<h2>Pipeline health</h2>")
    stats = fuse_stats(sessions)
    rate = "n/a" if stats["rate"] is None else f"{stats['rate'] * 100:.0f}%"
    parts.append(f"<p>FUSE success rate: <b>{rate}</b> "
                 f"<span class='dim'>({stats['success']} ok · {stats['failure']} failed · "
                 f"{stats['empty']} empty gathers)</span></p>")
    failures = [s for s in sessions if s["_kind"] == "failure"]
    if failures:
        parts.append("<table><tr><th>date</th><th>topic</th><th>stage</th><th>error</th></tr>" +
                     "".join(f"<tr><td>{_e(s['_date'])}</td><td>{_e(s.get('topic', ''))}</td>"
                             f"<td class='bad'>{_e(s.get('failed_stage', '?'))}</td>"
                             f"<td class='dim'>{_e(s.get('error', ''))}</td></tr>"
                             for s in failures) + "</table>")
    yields = collector_yield(sessions)
    if yields:
        parts.append("<table><tr><th>collector</th><th>records</th><th>found</th>"
                     "<th>ok runs</th><th>errors</th></tr>" +
                     "".join(f"<tr><td>{_e(c)}</td><td>{y['records']}</td><td>{y['found']}</td>"
                             f"<td>{y['ok_runs']}/{y['runs']}</td>"
                             f"<td class='bad'>{_e('; '.join(y['errors']) or '')}</td></tr>"
                             for c, y in sorted(yields.items())) + "</table>")
    for line in discrepancies(sessions, spend_days):
        parts.append(f"<p class='bad'>⚠ {_e(line)}</p>")

    # Re-run affordances
    if sessions:
        parts.append("<h2>Re-open / re-run a topic</h2>")
        for s in sessions:
            parts.append(f"<p class='dim'>{_e(s['_date'])} — {_e(s.get('topic', ''))}</p>"
                         f"<pre>{_e(rerun_command(s))}</pre>")

    # PM3 slot
    parts.append("<h2>Pain-taxonomy movement</h2>"
                 "<p class='dim'>Slot reserved: lands when PM3 persistence ships "
                 "(gated on the 7/21 t1 verdict).</p>")

    # Footer: honesty about what was skipped
    footer = [f"generated {_e(generated_at)}"]
    for name, reason in skipped_sessions:
        footer.append(f"skipped session file {_e(name)}: {_e(reason)}")
    for name, reason in skipped_spend:
        footer.append(f"skipped ledger {_e(name)}: {_e(reason)}")
    parts.append("<footer>" + "<br>".join(footer) + "</footer>")
    return "\n".join(parts)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard_render.py tests/discovery/test_dashboard.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add tools/llm-council/council/discovery/dashboard_render.py tools/llm-council/tests/discovery/test_dashboard_render.py
git commit -m "feat(discovery): dashboard HTML renderer — inline SVG/CSS, honest n/a + thin markers

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: CLI entry (`python -m council.discovery.dashboard`) + real-data smoke run

**Files:**
- Modify: `tools/llm-council/council/discovery/dashboard.py` (append CLI)
- Test: `tools/llm-council/tests/discovery/test_dashboard.py` (append)

**Interfaces:**
- Consumes: `render_dashboard` (Task 5), `load_sessions`/`load_spend` (Task 3), `pipeline._default_sessions_dir` (Task 2), `council.budget._spend_dir`.
- Produces: `main` click command — `uv run python -m council.discovery.dashboard --output PATH [--sessions-dir PATH] [--spend-dir PATH]`.

- [ ] **Step 1: Write the failing tests**

Append to `tools/llm-council/tests/discovery/test_dashboard.py`:

```python
from click.testing import CliRunner


def test_cli_renders_html(tmp_path):
    from council.discovery.dashboard import main
    sdir = tmp_path / "s"
    _write_sessions(sdir, ok=SUCCESS_SESSION)
    spend = tmp_path / "health"
    spend.mkdir()
    out = tmp_path / "dash.html"
    res = CliRunner().invoke(main, ["--sessions-dir", str(sdir),
                                    "--spend-dir", str(spend), "--output", str(out)])
    assert res.exit_code == 0, res.output
    html = out.read_text()
    assert "ai coding agents" in html
    assert "thin: 1 runs" in html
    assert str(out) in res.output


def test_cli_default_sessions_dir_resolution(tmp_path, monkeypatch):
    # Omitted --sessions-dir → pipeline resolution (env override, hermetic in tests).
    from council.discovery.dashboard import main
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(tmp_path / "resolved"))
    out = tmp_path / "dash.html"
    res = CliRunner().invoke(main, ["--spend-dir", str(tmp_path / "nohealth"),
                                    "--output", str(out)])
    assert res.exit_code == 0, res.output
    assert "No session history found" in out.read_text()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_dashboard.py -q`
Expected: ImportError — `main` not defined.

- [ ] **Step 3: Implement the CLI**

Add `import click` to the top-level imports of `dashboard.py`, then append:

```python
def _run_cli(sessions_dir: Path | None, spend_dir: Path | None) -> tuple[str, Path]:
    """Resolve dirs, load, render → (html, resolved_sessions_dir). Split from main() so the
    resolution logic is unit-callable. Heavy imports stay local so load_sessions/load_spend
    remain importable without pulling the whole pipeline."""
    from datetime import datetime

    from council.budget import _spend_dir as _default_spend_dir
    from council.discovery.dashboard_render import render_dashboard
    from council.discovery.pipeline import _default_sessions_dir

    if sessions_dir is None:
        sessions_dir = _default_sessions_dir()
        if sessions_dir is None:
            raise click.ClickException(
                "no sessions dir: pass --sessions-dir or set DISCOVERY_SESSIONS_DIR")
    if spend_dir is None:
        spend_dir = _default_spend_dir()
    sessions, skipped_sessions = load_sessions(sessions_dir)
    days, skipped_spend = load_spend(spend_dir)
    html = render_dashboard(sessions, skipped_sessions, days, skipped_spend,
                            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
                            sessions_dir=sessions_dir)
    return html, sessions_dir


@click.command()
@click.option("--sessions-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help="Session-JSON dir (default: pipeline resolution — $DISCOVERY_SESSIONS_DIR "
                   "or the canonical vault store).")
@click.option("--spend-dir", type=click.Path(file_okay=False, path_type=Path), default=None,
              help="council-spend-*.json dir (default: $COUNCIL_SPEND_DIR or vault/health/).")
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True,
              help="Self-contained HTML output path.")
def main(sessions_dir, spend_dir, output):
    """Render the discovery run-history dashboard (one self-contained HTML file, $0)."""
    html, resolved = _run_cli(sessions_dir, spend_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)
    click.echo(f"Dashboard written: {output} (sessions: {resolved})")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests, then the real smoke run**

Run: `cd tools/llm-council && uv run pytest tests/discovery/ -q`
Expected: all pass.

Smoke over the real vault data (read-only over sessions/spend; writes only the HTML):

```bash
cd tools/llm-council && uv run python -m council.discovery.dashboard \
  --output /private/tmp/claude-501/-Users-seanwinslow-Code-Brain-code-brain/96c80629-340f-4c53-8298-3dac89ee37d4/scratchpad/discovery-dashboard-smoke.html
```

Expected: exit 0; open the file and verify — 4 session rows (3× 2026-06-21 with `n/a (pre-E1 run)` / `n/a (pre-E4 run)` markers, 1× 2026-06-30), `pm3-t0-…json` listed as skipped-foreign in the footer, `⚠ thin: 4 runs` badge, spend bars for the ledger days, at least one discrepancy line (ledger days with no sessions — the leak this branch fixes).

- [ ] **Step 5: Full suite + validator, then commit**

Run: `cd tools/llm-council && uv run pytest tests/ -q` → all pass, 1 skipped.
Run (repo root): `python3 scripts/validate.py` → PASSED.

```bash
git add tools/llm-council/council/discovery/dashboard.py tools/llm-council/tests/discovery/test_dashboard.py
git commit -m "feat(discovery): dashboard CLI — one command renders the run-history HTML

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Docs — CHANGELOG + CLAUDE.md blurb

**Files:**
- Modify: `CHANGELOG.md` (repo root — new entry at top, matching existing entry style)
- Modify: `CLAUDE.md` (repo root — fusion-discovery-council paragraph in "Connected External Research APIs")

**Interfaces:**
- Consumes: final CLI shape from Task 6.
- Produces: docs only. No code.

- [ ] **Step 1: Read the top of `CHANGELOG.md`** to match the current entry format, then add an entry dated 2026-07-09 covering: (a) persist-by-default session store (`DISCOVERY_SESSIONS_DIR` override, empty-bundle leak fixed, `segment` recorded), (b) the D3 dashboard (`uv run python -m council.discovery.dashboard`, self-contained HTML, honest thin/n-a labeling, re-run affordances, PM3 slot).

- [ ] **Step 2: Update `CLAUDE.md`** — in the **fusion-discovery-council** paragraph, append one sentence after the caps sentence: `Run history persists to vault/20_projects/research/.discovery-sessions/ by default ($DISCOVERY_SESSIONS_DIR overrides); render the run-history dashboard with 'uv run python -m council.discovery.dashboard --output <path>' ($0, self-contained HTML).`

- [ ] **Step 3: Verify + commit**

Run (repo root): `python3 scripts/validate.py` → PASSED.

```bash
git add CHANGELOG.md CLAUDE.md
git commit -m "docs: D3 dashboard + persist-by-default session store

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Final verification (before the PR)

- [ ] `cd tools/llm-council && uv run pytest tests/ -q` — everything passes (expect ~349 passed, 1 skipped; exact count reported in the PR).
- [ ] `python3 scripts/validate.py` (repo root) — PASSED.
- [ ] `git status` — no vault paths staged (the smoke HTML lives in the scratchpad, not the repo).
- [ ] Re-run the Task-6 smoke command; visually confirm the dashboard over real data.
- [ ] Whole-branch adversarial review on the most capable model (per subagent-driven-development), then PR for Sean's squash-merge.
