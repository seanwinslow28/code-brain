---
type: implementation-plan
project: prj-job-hunt-2026
created: 2026-05-15
status: awaiting-review
linked_artifacts:
  - "[[2026-05-15-agent-fleet-dashboard-design]]"
  - "[[2026-05-13-agent-fleet-dashboard-spec]]"
ai-context: "Step-by-step v1 implementation plan for the Agent Fleet Observability Dashboard. Source of truth is the 2026-05-15 locked design doc. 4-day working budget. New dedicated repo at github.com/seanwinslow28/agent-fleet-observability. Awaiting Sean's review before any code is written."
---

# Agent Fleet Observability Dashboard — v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a static observability dashboard that renders two HTML files (public + private) from one Python build pipeline, deployed at `fleet.seanwinslow.com` via Vercel and pinned to `file://` on the Mac Mini.

**Architecture:** A `build.py` orchestrator reads local vault data (CSV / JSON / SQLite / Markdown), aggregates telemetry, then renders two independent HTML passes via Jinja2 — public goes to the repo root (committed + auto-deployed by Vercel), private goes to `~/Sites/agent-fleet-private/` (gitignored at the home level). Privacy boundary is structural: separate output paths, separate render passes, public pass skips `vault/.job-feed.db` entirely. Local cron at 06:00 ET daily.

**Tech Stack:** Python 3.12 stdlib (csv, json, sqlite3, pathlib, subprocess) · Jinja2 templates · PyYAML for frontmatter · inline SVG for all charts (no Chart.js — see deviation note) · vanilla JS for kanban filter chips · pytest for tests · ruff for lint · Vercel static deploy · Cloudflare DNS-only CNAME · macOS launchd.

**Source of truth:** [[2026-05-15-agent-fleet-dashboard-design]]. This plan implements every section of that doc; section refs throughout for cross-checking.

---

## Pre-build assumptions to confirm with Sean

Three items I'd flag before code:

1. **Deviation from design Section 6a: drop Chart.js, go all inline SVG.** Design doc lists `assets/charts.js` for Chart.js init. Rationale for the swap: page-weight budget < 50 KB pre-data, deterministic build output, no CDN race on cold-cache load, simpler tooling. SVGs handle the hero regression line, KPI sparklines, model mix donut, cost trend stacked area, and the eval case grid. Vanilla JS still used for kanban filter chip toggling.
2. **Deviation from design Section 6a: combine `public_render.py` + `private_render.py` into one `lib/render.py` with `render_public()` / `render_private()` functions.** Both passes share ~90% of logic; difference is one call to `anonymize.public_pass()` before render. Keeps the codebase DRY. Output paths and behavior unchanged.
3. **Data gap to flag — design doc Section 4d references job-hunt fields that aren't in the live SQLite schema.** `vault/.job-feed.db` `job_postings` table has `status, fit_score, company, title, role_band, rationale, concerns`. It does NOT have `next_action`, `warm_intro_*`, or a Target-30 lookup. The four private-only "Job Hunt" panels (Target-30 funnel, Applications this week, Next Actions, Warm-Intro Pipeline) need either schema extension OR derived columns OR a separate companion file Sean maintains. v1 plan derives what it can from the existing schema + falls back to Sean-voice empty-state copy for what's missing. Day 2 Task 20 calls this out explicitly.

If any of these three is wrong, fix in this doc before kicking off Task 1.

---

## File Structure

```
agent-fleet-observability/
├── build.py                          # orchestrator (Day 4 Task 26)
├── Makefile                          # `make build` / `make test` / `make deploy` (Day 1 Task 2)
├── pyproject.toml                    # Python 3.12, deps, ruff config (Day 1 Task 2)
├── vercel.json                       # static deploy config (Day 4 Task 28)
├── .gitignore                        # blocks .venv, __pycache__, .DS_Store (Day 1 Task 1)
├── README.md                         # 4Q recruiter doc (Day 4 Task 31)
├── lib/
│   ├── __init__.py
│   ├── readers.py                    # data source loaders (Day 1 Tasks 3-8)
│   ├── aggregations.py               # KPI + sparkline + regression compute (Day 1 Tasks 9-11)
│   ├── anonymize.py                  # public-pass stripping (Day 2 Task 12)
│   ├── svg_charts.py                 # inline SVG chart helpers (Day 2 Tasks 13-14)
│   ├── kanban.py                     # ticket composer + column rules (Day 3 Tasks 21-22)
│   └── render.py                     # public + private render orchestrators (Day 3 Task 25)
├── templates/
│   ├── base.html                     # html shell + top bar + footer (Day 1 Task 16)
│   ├── fleet.html                    # /fleet page (Day 2 Task 19)
│   ├── kanban.html                   # /kanban page (Day 3 Task 23)
│   └── partials/
│       ├── mascot.html               # Asterisk Spark (Day 1 Task 16)
│       ├── topbar.html               # top bar (Day 1 Task 16)
│       ├── footer.html               # footer (Day 1 Task 16)
│       ├── agent_grid.html           # 8-tile agent grid (Day 1 Task 17)
│       ├── kpi_row.html              # 4-card KPI row (Day 1 Task 17)
│       ├── hero_regression.html      # 60-day hero chart (Day 2 Task 18)
│       ├── below_fold_public.html    # cost trend, model mix, runs, eval grid (Day 2 Task 19)
│       ├── below_fold_private.html   # private adds: alerts, job hunt, cloud spend (Day 2 Task 20)
│       └── kanban_board.html         # kanban columns + tickets (Day 3 Task 23)
├── assets/
│   ├── styles.css                    # full stylesheet (Day 1 Task 15 + Day 4 Task 27)
│   └── kanban-filter.js              # vanilla JS filter chip toggle (Day 3 Task 24)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # pytest fixtures (Day 1 Task 3)
│   ├── fixtures/                     # sample data
│   │   ├── sample-run-history.csv
│   │   ├── sample-synth-manifest-2026-05-13.json
│   │   ├── sample-gemini-spend.json
│   │   ├── sample-council-spend-2026-05-14.json
│   │   ├── sample-eval-last-run.md
│   │   ├── sample-lint-report.md
│   │   ├── sample-research-queue.md
│   │   ├── sample-tickets.md
│   │   └── sample-job-feed.db        # built by conftest
│   ├── test_readers.py               # Tasks 3-8
│   ├── test_aggregations.py          # Tasks 9-11
│   ├── test_anonymize.py             # Task 12
│   ├── test_svg_charts.py            # Tasks 13-14
│   ├── test_kanban.py                # Tasks 21-22
│   └── test_render_smoke.py          # Task 25
├── index.html                        # GENERATED — committed (Day 4 Task 26 output)
├── kanban.html                       # GENERATED — committed
└── data.json                         # GENERATED — committed (kanban filter sidecar)

# Outside the repo:
~/Sites/agent-fleet-private/
├── index.html                        # private fleet render
├── kanban.html                       # private kanban (5 lanes)
└── data.json                         # private sidecar

~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist  # cron (Day 4 Task 30)
```

---

# Day 1 — Scaffolding, data readers, aggregations, top bar, mascot

## Task 1: Initialize the new repo (local + GitHub)

**Files:**
- Create: `~/Code/agent-fleet-observability/` (working directory for the new repo)
- Create: `~/Code/agent-fleet-observability/.gitignore`
- Create: `~/Code/agent-fleet-observability/README.md` (stub — full version Day 4)

- [ ] **Step 1: Verify the parent directory exists, choose the working location**

Run: `ls ~/Code 2>/dev/null || ls ~/Code-Brain 2>/dev/null`

If `~/Code/` exists, use it. If only `~/Code-Brain/` exists, use `~/Code-Brain/agent-fleet-observability/`. Update the rest of the plan's absolute paths to match. Default below uses `~/Code/agent-fleet-observability/`.

- [ ] **Step 2: Create the directory and initialize git**

```bash
mkdir -p ~/Code/agent-fleet-observability
cd ~/Code/agent-fleet-observability
git init -b main
```

Expected: `Initialized empty Git repository in /Users/seanwinslow/Code/agent-fleet-observability/.git/`

- [ ] **Step 3: Write `.gitignore`**

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.DS_Store
.env
/tmp/
```

- [ ] **Step 4: Write `README.md` stub**

```markdown
# Agent Fleet Observability

Static observability dashboard for an 8-agent local-first AI fleet.

- **Public:** [fleet.seanwinslow.com](https://fleet.seanwinslow.com)
- **Build:** local Python on Mac Mini, cron 06:00 ET daily
- **Cost:** $0 cloud, 99% local-first inference

Full docs land here at the end of v1 (see Day 4 Task 31).
```

- [ ] **Step 5: Initial commit**

```bash
cd ~/Code/agent-fleet-observability
git add .gitignore README.md
git commit -m "$(cat <<'EOF'
feat: initial repo scaffold

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Create the GitHub repo + push**

```bash
cd ~/Code/agent-fleet-observability
gh repo create seanwinslow28/agent-fleet-observability \
  --public \
  --source=. \
  --description="Static observability dashboard for an 8-agent local-first AI fleet" \
  --push
```

Expected: `✓ Created repository seanwinslow28/agent-fleet-observability on GitHub` plus a push confirmation. If `gh repo create` errors with "repository already exists", verify it's Sean's intent before continuing.

---

## Task 2: Python project scaffolding (pyproject.toml, venv, Makefile)

**Files:**
- Create: `~/Code/agent-fleet-observability/pyproject.toml`
- Create: `~/Code/agent-fleet-observability/Makefile`
- Create: `~/Code/agent-fleet-observability/lib/__init__.py`
- Create: `~/Code/agent-fleet-observability/tests/__init__.py`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "agent-fleet-observability"
version = "0.1.0"
description = "Static observability dashboard for an 8-agent local-first AI fleet"
requires-python = ">=3.12"
dependencies = [
    "jinja2>=3.1.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.5",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "W", "B", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --strict-markers"
```

- [ ] **Step 2: Create venv + install**

```bash
cd ~/Code/agent-fleet-observability
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e ".[dev]"
```

Expected: `Successfully installed agent-fleet-observability-0.1.0 ...`

- [ ] **Step 3: Write `Makefile`**

```makefile
.PHONY: build test lint deploy clean

PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff

build:
	$(PYTHON) build.py

test:
	$(PYTEST) tests/ -v

lint:
	$(RUFF) check lib/ tests/ build.py
	$(RUFF) format --check lib/ tests/ build.py

format:
	$(RUFF) format lib/ tests/ build.py

deploy: build
	@if git diff --quiet index.html kanban.html data.json; then \
	  echo "no public changes — skipping commit"; \
	else \
	  git add index.html kanban.html data.json && \
	  git commit -m "snapshot $$(date -u +%Y-%m-%dT%H:%M:%SZ)" && \
	  git push; \
	fi

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -name "*.pyc" -delete
```

- [ ] **Step 4: Create empty package files**

```bash
cd ~/Code/agent-fleet-observability
mkdir -p lib tests/fixtures templates/partials assets
touch lib/__init__.py tests/__init__.py
```

- [ ] **Step 5: Verify test harness boots**

```bash
cd ~/Code/agent-fleet-observability
.venv/bin/pytest tests/ -v
```

Expected: `no tests ran in 0.00s` (or similar — exit code 5 from pytest is OK pre-tests).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml Makefile lib/__init__.py tests/__init__.py
git commit -m "$(cat <<'EOF'
feat: python project scaffolding (pyproject, venv, Makefile)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Test fixtures + `read_run_history` (TDD)

**Files:**
- Create: `~/Code/agent-fleet-observability/tests/conftest.py`
- Create: `~/Code/agent-fleet-observability/tests/fixtures/sample-run-history.csv`
- Create: `~/Code/agent-fleet-observability/tests/test_readers.py`
- Create: `~/Code/agent-fleet-observability/lib/readers.py`

- [ ] **Step 1: Write the fixture CSV**

File: `tests/fixtures/sample-run-history.csv`

```csv
date,time,agent,mode,status,cost_usd,duration_ms,turns,notes
2026-05-13,02:30:05,vault_synthesizer,nightly,ok,0.0000,2719760,,114 concepts
2026-05-13,02:00:00,vault_indexer,nightly,ok,0.0000,180400,,62 files
2026-05-13,02:45:00,deep_researcher,nightly,ok,0.0000,420000,,1 topic
2026-05-13,08:45:00,daily_driver,morning,ok,0.3812,540000,18,
2026-05-13,08:35:00,meta_agent,nightly,ok,0.0000,8200,,
2026-05-12,22:00:00,knowledge_lint,weekly,ok,0.0000,15400,,
2026-05-13,12:34:00,flush,session-end,ok,0.0000,4200,,12 msgs
2026-05-13,09:30:00,job_feed,morning,ok,0.0000,18500,,14 new
2026-05-13,02:30:05,vault_synthesizer,nightly,error,0.0000,12000,,model timeout
2026-05-12,02:30:00,vault_synthesizer,nightly,skipped,0.0000,,,mbp_asleep
```

- [ ] **Step 2: Write `conftest.py` exposing fixture paths**

File: `tests/conftest.py`

```python
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def run_history_path() -> Path:
    return FIXTURES / "sample-run-history.csv"
```

- [ ] **Step 3: Write the failing test**

File: `tests/test_readers.py`

```python
from datetime import datetime, timezone

from lib import readers


def test_read_run_history_parses_rows(run_history_path):
    rows = readers.read_run_history(run_history_path)
    assert len(rows) == 10
    row = rows[0]
    assert row["agent"] == "vault_synthesizer"
    assert row["status"] == "ok"
    assert row["cost_usd"] == 0.0
    assert row["duration_ms"] == 2719760
    assert isinstance(row["ts"], datetime)


def test_read_run_history_handles_blank_duration(run_history_path):
    rows = readers.read_run_history(run_history_path)
    skipped = [r for r in rows if r["status"] == "skipped"][0]
    assert skipped["duration_ms"] is None


def test_read_run_history_returns_utc_aware_timestamps(run_history_path):
    rows = readers.read_run_history(run_history_path)
    assert rows[0]["ts"].tzinfo is not None
```

- [ ] **Step 4: Run test, watch it fail**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: `ModuleNotFoundError: No module named 'lib.readers'` (or `AttributeError`).

- [ ] **Step 5: Implement `read_run_history`**

File: `lib/readers.py`

```python
"""Data source loaders for the Agent Fleet Observability Dashboard.

All readers return plain dicts / lists of dicts — no domain models. Aggregation
happens downstream in lib/aggregations.py. Empty inputs return empty containers,
not None, so callers can blindly iterate.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


def _parse_ts(date_str: str, time_str: str) -> datetime:
    iso = f"{date_str}T{time_str}"
    return datetime.fromisoformat(iso).replace(tzinfo=timezone.utc)


def _to_float(val: str) -> float:
    return float(val) if val else 0.0


def _to_int_or_none(val: str) -> int | None:
    return int(val) if val else None


def read_run_history(path: Path) -> list[dict]:
    """Load agent-run-history.csv → list of normalized run dicts.

    Schema: date, time, agent, mode, status, cost_usd, duration_ms, turns, notes.
    """
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            rows.append({
                "ts": _parse_ts(raw["date"], raw["time"]),
                "agent": raw["agent"],
                "mode": raw["mode"] or None,
                "status": raw["status"],
                "cost_usd": _to_float(raw["cost_usd"]),
                "duration_ms": _to_int_or_none(raw["duration_ms"]),
                "turns": _to_int_or_none(raw["turns"]),
                "notes": raw["notes"] or "",
            })
    return rows
```

- [ ] **Step 6: Run test, watch it pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 3 passed.

- [ ] **Step 7: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/conftest.py tests/fixtures/sample-run-history.csv
git commit -m "$(cat <<'EOF'
feat: read_run_history loader + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: `read_synth_manifests` (TDD)

**Files:**
- Create: `tests/fixtures/sample-synth-manifest-2026-05-13.json`
- Create: `tests/fixtures/sample-synth-manifest-2026-05-12.json`
- Modify: `tests/test_readers.py`
- Modify: `lib/readers.py`

- [ ] **Step 1: Write two fixture manifest files**

File: `tests/fixtures/sample-synth-manifest-2026-05-13.json`

```json
{
  "concepts_written": 114,
  "connections_written": 69,
  "duration_seconds": 2719.76,
  "edges_rejected": 2,
  "edges_written": 129,
  "files_processed": 62,
  "model_used": "qwen3-14b",
  "rejected_count": 2,
  "run_id": "2026-05-13T02:30:05",
  "status": "ok",
  "wol_status": "mbp_awake"
}
```

File: `tests/fixtures/sample-synth-manifest-2026-05-12.json`

```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 0.0,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 0,
  "model_used": "qwen3-14b",
  "rejected_count": 0,
  "run_id": "2026-05-12T02:30:00",
  "status": "skipped",
  "wol_status": "mbp_asleep"
}
```

- [ ] **Step 2: Extend conftest**

File: `tests/conftest.py` — append:

```python
@pytest.fixture
def synth_manifests_dir() -> Path:
    return FIXTURES
```

- [ ] **Step 3: Write the failing test**

File: `tests/test_readers.py` — append:

```python
from datetime import date


def test_read_synth_manifests_returns_dated_records(synth_manifests_dir):
    records = readers.read_synth_manifests(synth_manifests_dir)
    assert len(records) == 2
    by_date = {r["date"]: r for r in records}
    assert by_date[date(2026, 5, 13)]["concepts_written"] == 114
    assert by_date[date(2026, 5, 12)]["status"] == "skipped"


def test_read_synth_manifests_sorts_by_date(synth_manifests_dir):
    records = readers.read_synth_manifests(synth_manifests_dir)
    assert records[0]["date"] < records[1]["date"]
```

- [ ] **Step 4: Run test, watch it fail**

Run: `.venv/bin/pytest tests/test_readers.py::test_read_synth_manifests_returns_dated_records -v`
Expected: `AttributeError: module 'lib.readers' has no attribute 'read_synth_manifests'`.

- [ ] **Step 5: Implement `read_synth_manifests`**

File: `lib/readers.py` — append:

```python
import json
import re
from datetime import date


_SYNTH_NAME_RE = re.compile(r"(?:sample-)?synth-manifest-(\d{4})-(\d{2})-(\d{2})\.json$")


def read_synth_manifests(dir_path: Path) -> list[dict]:
    """Load all synth-manifest-YYYY-MM-DD.json files in `dir_path`.

    Returns list sorted ascending by date. Each record adds a parsed `date`
    field on top of the raw manifest JSON.
    """
    if not dir_path.exists():
        return []
    records: list[dict] = []
    for path in sorted(dir_path.glob("*synth-manifest-*.json")):
        m = _SYNTH_NAME_RE.search(path.name)
        if not m:
            continue
        yr, mo, dy = (int(g) for g in m.groups())
        raw = json.loads(path.read_text())
        raw["date"] = date(yr, mo, dy)
        records.append(raw)
    return sorted(records, key=lambda r: r["date"])
```

- [ ] **Step 6: Run, watch it pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 5 passed.

- [ ] **Step 7: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/conftest.py tests/fixtures/sample-synth-manifest-2026-05-*.json
git commit -m "$(cat <<'EOF'
feat: read_synth_manifests loader + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: `read_gemini_spend` + `read_council_spend` (TDD)

**Files:**
- Create: `tests/fixtures/sample-gemini-spend.json`
- Create: `tests/fixtures/sample-council-spend-2026-05-14.json`
- Modify: `tests/test_readers.py`
- Modify: `lib/readers.py`

- [ ] **Step 1: Write the fixture files**

File: `tests/fixtures/sample-gemini-spend.json`

```json
[
  {
    "interaction_id": "v1_test1",
    "agent_id": "deep-research-preview-04-2026",
    "tier": "dr",
    "cost_usd": 2.80,
    "wall_seconds": 423,
    "created": "2026-05-03T21:09:27Z"
  },
  {
    "interaction_id": "v1_test2",
    "agent_id": "deep-research-preview-04-2026",
    "tier": "max",
    "cost_usd": 5.40,
    "wall_seconds": 612,
    "created": "2026-05-06T11:14:00Z"
  }
]
```

File: `tests/fixtures/sample-council-spend-2026-05-14.json`

```json
{
  "date": "2026-05-14",
  "runs": [
    {"profile": "premium", "cost_usd": 0.29},
    {"profile": "variance", "cost_usd": 0.12}
  ],
  "day_total_usd": 0.41
}
```

- [ ] **Step 2: Write the failing tests**

File: `tests/test_readers.py` — append:

```python
def test_read_gemini_spend_returns_month_total(tmp_path):
    src = FIXTURES / "sample-gemini-spend.json"
    out = readers.read_gemini_spend(src)
    assert out["total_usd"] == 8.20
    assert out["run_count"] == 2
    assert out["tiers"] == {"dr": 1, "max": 1}


def test_read_gemini_spend_empty_when_missing(tmp_path):
    out = readers.read_gemini_spend(tmp_path / "nope.json")
    assert out == {"total_usd": 0.0, "run_count": 0, "tiers": {}}


def test_read_council_spend_aggregates_files(tmp_path):
    # symlink the fixture into a tmp dir to test glob behavior
    (tmp_path / "council-spend-2026-05-14.json").write_text(
        (FIXTURES / "sample-council-spend-2026-05-14.json").read_text()
    )
    out = readers.read_council_spend(tmp_path)
    assert out["month_total_usd"] == 0.41
    assert out["day_count"] == 1


def test_read_council_spend_empty_dir(tmp_path):
    out = readers.read_council_spend(tmp_path / "missing")
    assert out["month_total_usd"] == 0.0
```

Make sure `from tests.conftest import FIXTURES` works — since `FIXTURES` is module-level in conftest, add `from .conftest import FIXTURES` at the top of `tests/test_readers.py`. (Alternative: re-define `FIXTURES` in the test file.)

- [ ] **Step 3: Run, watch fail**

Run: `.venv/bin/pytest tests/test_readers.py -v -k "gemini or council"`
Expected: 4 errors (AttributeError on `read_gemini_spend`).

- [ ] **Step 4: Implement both readers**

File: `lib/readers.py` — append:

```python
def read_gemini_spend(path: Path) -> dict:
    """Aggregate a single gemini-spend-YYYY-MM.json (array of interactions)."""
    if not path.exists():
        return {"total_usd": 0.0, "run_count": 0, "tiers": {}}
    items = json.loads(path.read_text())
    total = sum(it.get("cost_usd", 0.0) or 0.0 for it in items)
    tiers: dict[str, int] = {}
    for it in items:
        tier = it.get("tier", "unknown")
        tiers[tier] = tiers.get(tier, 0) + 1
    return {
        "total_usd": round(total, 2),
        "run_count": len(items),
        "tiers": tiers,
    }


def read_council_spend(dir_path: Path) -> dict:
    """Aggregate all council-spend-YYYY-MM-DD.json files in dir_path for the month."""
    if not dir_path.exists():
        return {"month_total_usd": 0.0, "day_count": 0, "days": []}
    days: list[dict] = []
    total = 0.0
    for path in sorted(dir_path.glob("council-spend-*.json")):
        raw = json.loads(path.read_text())
        day_total = raw.get("day_total_usd", 0.0) or 0.0
        days.append({"date": raw.get("date"), "total_usd": day_total})
        total += day_total
    return {
        "month_total_usd": round(total, 2),
        "day_count": len(days),
        "days": days,
    }
```

- [ ] **Step 5: Run, watch pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 9 passed.

- [ ] **Step 6: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/fixtures/sample-gemini-spend.json tests/fixtures/sample-council-spend-2026-05-14.json
git commit -m "$(cat <<'EOF'
feat: read_gemini_spend + read_council_spend + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: `read_eval_last_run` + `read_lint_reports` (TDD)

**Files:**
- Create: `tests/fixtures/sample-eval-last-run.md`
- Create: `tests/fixtures/sample-lint-report.md`
- Modify: `tests/test_readers.py`
- Modify: `lib/readers.py`

- [ ] **Step 1: Write fixture files**

File: `tests/fixtures/sample-eval-last-run.md`

```markdown
---
run_id: "2026-05-14T02:30:05"
total_cases: 10
passed: 7
failed: 2
skipped: 1
cases:
  - id: "case-01-empty-vault"
    status: "passed"
  - id: "case-02-single-cluster"
    status: "passed"
  - id: "case-03-cross-domain"
    status: "failed"
  - id: "case-04-evidence-quotes"
    status: "passed"
  - id: "case-05-duplicate-merge"
    status: "failed"
  - id: "case-06-soul-tier-a"
    status: "passed"
  - id: "case-07-broken-wikilink"
    status: "passed"
  - id: "case-08-citation-fab"
    status: "passed"
  - id: "case-09-large-vault"
    status: "passed"
  - id: "case-10-tier4-agentic"
    status: "skipped"
---

# Vault Synthesizer Eval Run — 2026-05-14
```

File: `tests/fixtures/sample-lint-report.md`

```markdown
---
date: 2026-05-12
issues_total: 4
issues_by_severity:
  HIGH: 1
  MEDIUM: 2
  LOW: 1
---

# Knowledge Lint Report 2026-05-12

## Issues

- [HIGH] broken-wikilink — `concepts/foo.md`
- [MEDIUM] orphan-concept — `concepts/bar.md`
- [MEDIUM] stale-frontmatter — `vault/.../baz.md`
- [LOW] duplicate-title — `concepts/qux.md`
```

- [ ] **Step 2: Write failing tests**

File: `tests/test_readers.py` — append:

```python
def test_read_eval_last_run_extracts_counts():
    out = readers.read_eval_last_run(FIXTURES / "sample-eval-last-run.md")
    assert out["passed"] == 7
    assert out["total_cases"] == 10
    assert len(out["cases"]) == 10
    failed = [c for c in out["cases"] if c["status"] == "failed"]
    assert len(failed) == 2


def test_read_eval_last_run_missing_file(tmp_path):
    out = readers.read_eval_last_run(tmp_path / "no.md")
    assert out["passed"] == 0
    assert out["cases"] == []


def test_read_lint_reports_returns_latest(tmp_path):
    fixture = (FIXTURES / "sample-lint-report.md").read_text()
    (tmp_path / "2026-05-12-lint-report.md").write_text(fixture)
    (tmp_path / "2026-05-19-lint-report.md").write_text(fixture)
    out = readers.read_lint_reports(tmp_path)
    assert out["latest_date"] == "2026-05-19"
    assert out["issues_total"] == 4
```

- [ ] **Step 3: Run, watch fail**

Run: `.venv/bin/pytest tests/test_readers.py -v -k "eval or lint"`
Expected: errors on missing functions.

- [ ] **Step 4: Implement readers**

File: `lib/readers.py` — append:

```python
import yaml


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    return yaml.safe_load(text[3:end]) or {}


def read_eval_last_run(path: Path) -> dict:
    """Parse evals/vault-synthesizer/last-run.md frontmatter."""
    empty = {"passed": 0, "failed": 0, "skipped": 0, "total_cases": 0, "cases": []}
    if not path.exists():
        return empty
    fm = _parse_frontmatter(path.read_text())
    return {
        "passed": int(fm.get("passed", 0)),
        "failed": int(fm.get("failed", 0)),
        "skipped": int(fm.get("skipped", 0)),
        "total_cases": int(fm.get("total_cases", 0)),
        "cases": list(fm.get("cases", []) or []),
        "run_id": fm.get("run_id"),
    }


_LINT_NAME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})-lint-report\.md$")


def read_lint_reports(dir_path: Path) -> dict:
    """Find the most recent lint report; return its summary."""
    if not dir_path.exists():
        return {"latest_date": None, "issues_total": 0, "issues_by_severity": {}}
    dated: list[tuple[str, Path]] = []
    for p in dir_path.glob("*-lint-report.md"):
        m = _LINT_NAME_RE.search(p.name)
        if m:
            dated.append((m.group(1), p))
    if not dated:
        return {"latest_date": None, "issues_total": 0, "issues_by_severity": {}}
    dated.sort(reverse=True)
    latest_date, latest_path = dated[0]
    fm = _parse_frontmatter(latest_path.read_text())
    return {
        "latest_date": latest_date,
        "issues_total": int(fm.get("issues_total", 0)),
        "issues_by_severity": dict(fm.get("issues_by_severity", {}) or {}),
        "raw_body": latest_path.read_text(),
    }
```

- [ ] **Step 5: Run, watch pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 12 passed.

- [ ] **Step 6: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/fixtures/sample-eval-last-run.md tests/fixtures/sample-lint-report.md
git commit -m "$(cat <<'EOF'
feat: read_eval_last_run + read_lint_reports + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: `read_job_feed_db` (TDD)

**Files:**
- Modify: `tests/conftest.py` (build sample SQLite at session start)
- Modify: `tests/test_readers.py`
- Modify: `lib/readers.py`

- [ ] **Step 1: Add a `job_feed_db` session fixture to conftest**

File: `tests/conftest.py` — append:

```python
import sqlite3


@pytest.fixture(scope="session")
def job_feed_db_path(tmp_path_factory) -> Path:
    db_path = tmp_path_factory.mktemp("data") / "job-feed.db"
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE job_postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_role_id TEXT NOT NULL,
            url TEXT NOT NULL,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            salary_disclosed TEXT,
            posted_at TEXT,
            first_seen_at TEXT NOT NULL,
            description_excerpt TEXT,
            rules_passed INTEGER NOT NULL,
            rules_rejection_reason TEXT,
            fit_score INTEGER,
            role_band TEXT,
            rationale TEXT,
            concerns TEXT,
            fit_dimensions TEXT,
            scored_at TEXT,
            status TEXT DEFAULT 'new',
            UNIQUE(source, source_role_id)
        );
    """)
    conn.executemany(
        """INSERT INTO job_postings
           (source, source_role_id, url, company, title, first_seen_at,
            rules_passed, fit_score, role_band, status)
           VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)""",
        [
            ("greenhouse", "anthropic-fde", "https://x", "Anthropic", "FDE", "2026-05-12T10:00:00Z", 88, "ai-pm", "screen-scheduled"),
            ("greenhouse", "klaviyo-pm", "https://y", "Klaviyo", "Senior PM", "2026-05-13T10:00:00Z", 72, "tech-pm", "applied"),
            ("ats-watch", "sierra-1", "https://z", "Sierra", "Agent PM", "2026-05-14T10:00:00Z", 91, "ai-pm", "new"),
            ("ats-watch", "decagon-1", "https://w", "Decagon", "Agent PM", "2026-05-14T11:00:00Z", 84, "ai-pm", "rejected"),
        ],
    )
    conn.commit()
    conn.close()
    return db_path
```

- [ ] **Step 2: Write failing test**

File: `tests/test_readers.py` — append:

```python
def test_read_job_feed_db_returns_funnel(job_feed_db_path):
    out = readers.read_job_feed_db(job_feed_db_path)
    assert out["total_postings"] == 4
    assert out["by_status"]["new"] == 1
    assert out["by_status"]["applied"] == 1
    assert out["by_status"]["screen-scheduled"] == 1
    assert out["by_status"]["rejected"] == 1
    assert out["top_fit"][0]["company"] == "Sierra"


def test_read_job_feed_db_missing(tmp_path):
    out = readers.read_job_feed_db(tmp_path / "missing.db")
    assert out["total_postings"] == 0
```

- [ ] **Step 3: Run, watch fail**

Run: `.venv/bin/pytest tests/test_readers.py -v -k job_feed`
Expected: AttributeError.

- [ ] **Step 4: Implement reader**

File: `lib/readers.py` — append:

```python
import sqlite3


def read_job_feed_db(path: Path) -> dict:
    """Read aggregate stats from vault/.job-feed.db.

    Returns funnel by status, top-N fit-score rows, and timestamps.
    PRIVATE-ONLY: callers must skip this on public render pass.
    """
    empty = {"total_postings": 0, "by_status": {}, "top_fit": [], "active_count": 0}
    if not path.exists():
        return empty
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        cur = conn.execute("SELECT COUNT(*) FROM job_postings")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT status, COUNT(*) FROM job_postings GROUP BY status")
        by_status = {row[0] or "new": row[1] for row in cur.fetchall()}
        cur = conn.execute(
            """SELECT company, title, fit_score, status, first_seen_at
               FROM job_postings
               WHERE rules_passed = 1 AND fit_score IS NOT NULL
                 AND status NOT IN ('rejected', 'archived')
               ORDER BY fit_score DESC
               LIMIT 10"""
        )
        top_fit = [
            {"company": r[0], "title": r[1], "fit_score": r[2], "status": r[3], "first_seen_at": r[4]}
            for r in cur.fetchall()
        ]
        cur = conn.execute(
            "SELECT COUNT(*) FROM job_postings WHERE status NOT IN ('rejected', 'archived')"
        )
        active = cur.fetchone()[0]
    finally:
        conn.close()
    return {
        "total_postings": total,
        "by_status": by_status,
        "top_fit": top_fit,
        "active_count": active,
    }
```

- [ ] **Step 5: Run, watch pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 14 passed.

- [ ] **Step 6: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/conftest.py
git commit -m "$(cat <<'EOF'
feat: read_job_feed_db loader + tests (private-only)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: `read_research_queue` + `read_manual_tickets` + `read_job_feed_manifests` (TDD)

**Files:**
- Create: `tests/fixtures/sample-research-queue.md`
- Create: `tests/fixtures/sample-tickets.md`
- Create: `tests/fixtures/sample-job-feed-manifest-2026-05-13.json`
- Modify: `tests/test_readers.py`
- Modify: `lib/readers.py`

- [ ] **Step 1: Write fixtures**

File: `tests/fixtures/sample-research-queue.md`

```markdown
# Research Queue

## Pending

- [ ] **Substrate repricing in 2026 agent boards** — single-shape, local LDR
- [ ] **MCP catalog survey** — heavy, route to Gemini DR
- [ ] **AgentField vs LangSmith Fleet pricing** — single-shape

## In Flight

- [ ] **Anthropic FDE intake pattern** — assigned: deep_researcher

## Done

- [x] ~~Karpathy synthesis~~
```

File: `tests/fixtures/sample-tickets.md`

```markdown
# Manual Tickets

## Todo

- Bump synth eval suite to 12 cases (case-11: dead-link detection)
- Rotate api token for ldr — assigned: Sean

## In Progress

- Substack post 2 draft — assigned: Sean
```

File: `tests/fixtures/sample-job-feed-manifest-2026-05-13.json`

```json
{
  "date": "2026-05-13",
  "new_postings": 14,
  "rules_passed": 9,
  "fit_scored": 9,
  "duration_seconds": 18.5,
  "feeds_checked": ["greenhouse", "lever", "rss-1", "ats-watch"]
}
```

- [ ] **Step 2: Write failing tests**

File: `tests/test_readers.py` — append:

```python
def test_read_research_queue_parses_sections():
    out = readers.read_research_queue(FIXTURES / "sample-research-queue.md")
    assert len(out["pending"]) == 3
    assert len(out["in_flight"]) == 1
    assert out["in_flight"][0]["assigned_agent"] == "deep_researcher"


def test_read_manual_tickets_parses():
    out = readers.read_manual_tickets(FIXTURES / "sample-tickets.md")
    assert len(out["todo"]) == 2
    assert len(out["in_progress"]) == 1
    sean_ticket = [t for t in out["todo"] if t["assigned_agent"] == "Sean"][0]
    assert "Rotate" in sean_ticket["title"]


def test_read_job_feed_manifests(tmp_path):
    src = FIXTURES / "sample-job-feed-manifest-2026-05-13.json"
    (tmp_path / src.name.replace("sample-", "")).write_text(src.read_text())
    out = readers.read_job_feed_manifests(tmp_path)
    assert out["latest"]["new_postings"] == 14
    assert out["latest"]["date"] == "2026-05-13"
```

- [ ] **Step 3: Run, watch fail**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 3 failures.

- [ ] **Step 4: Implement readers**

File: `lib/readers.py` — append:

```python
_BULLET_RE = re.compile(r"^- \[[ x]\]\s*(.+?)(?:\s*—\s*assigned:\s*(\S+))?\s*$")
_PLAIN_BULLET_RE = re.compile(r"^-\s+(.+?)(?:\s*—\s*assigned:\s*(\S+))?\s*$")


def _parse_section_items(lines: list[str], regex: re.Pattern) -> list[dict]:
    items: list[dict] = []
    for line in lines:
        m = regex.match(line.strip())
        if not m:
            continue
        title = m.group(1).strip().strip("*_~")
        title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
        agent = m.group(2) if m.lastindex and m.lastindex >= 2 else None
        items.append({"title": title, "assigned_agent": agent})
    return items


def _split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "_pre"
    sections[current] = []
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower().replace(" ", "_")
            sections[current] = []
        else:
            sections[current].append(line)
    return sections


def read_research_queue(path: Path) -> dict:
    if not path.exists():
        return {"pending": [], "in_flight": [], "done": []}
    sections = _split_sections(path.read_text())
    return {
        "pending": _parse_section_items(sections.get("pending", []), _BULLET_RE),
        "in_flight": _parse_section_items(sections.get("in_flight", []), _BULLET_RE),
        "done": _parse_section_items(sections.get("done", []), _BULLET_RE),
    }


def read_manual_tickets(path: Path) -> dict:
    if not path.exists():
        return {"todo": [], "in_progress": [], "done": []}
    sections = _split_sections(path.read_text())
    return {
        "todo": _parse_section_items(sections.get("todo", []), _PLAIN_BULLET_RE),
        "in_progress": _parse_section_items(sections.get("in_progress", []), _PLAIN_BULLET_RE),
        "done": _parse_section_items(sections.get("done", []), _PLAIN_BULLET_RE),
    }


def read_job_feed_manifests(dir_path: Path) -> dict:
    """Return the latest job-feed-manifest-*.json plus a 7-day rollup."""
    if not dir_path.exists():
        return {"latest": None, "last_7": []}
    paths = sorted(dir_path.glob("job-feed-manifest-*.json"))
    if not paths:
        return {"latest": None, "last_7": []}
    last_7 = [json.loads(p.read_text()) for p in paths[-7:]]
    return {"latest": last_7[-1], "last_7": last_7}
```

- [ ] **Step 5: Run, watch pass**

Run: `.venv/bin/pytest tests/test_readers.py -v`
Expected: 17 passed.

- [ ] **Step 6: Commit**

```bash
git add lib/readers.py tests/test_readers.py tests/fixtures/sample-research-queue.md tests/fixtures/sample-tickets.md tests/fixtures/sample-job-feed-manifest-2026-05-13.json
git commit -m "$(cat <<'EOF'
feat: research-queue + manual-tickets + job-feed-manifest readers

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: `aggregations.compute_fleet_status` + `compute_kpis` (TDD)

**Files:**
- Create: `tests/test_aggregations.py`
- Create: `lib/aggregations.py`

- [ ] **Step 1: Write failing test for fleet status**

File: `tests/test_aggregations.py`

```python
from datetime import date, datetime, timedelta, timezone

from lib import aggregations, readers

from .conftest import FIXTURES


AGENT_NAMES = [
    "vault_indexer", "vault_synthesizer", "deep_researcher", "meta_agent",
    "daily_driver", "knowledge_lint", "flush", "job_feed",
]


def _runs():
    return readers.read_run_history(FIXTURES / "sample-run-history.csv")


def test_compute_fleet_status_returns_eight_tiles():
    status = aggregations.compute_fleet_status(_runs(), AGENT_NAMES)
    assert len(status) == 8
    names = [s["agent"] for s in status]
    assert set(names) == set(AGENT_NAMES)


def test_compute_fleet_status_health_per_agent():
    status = aggregations.compute_fleet_status(_runs(), AGENT_NAMES)
    by_name = {s["agent"]: s for s in status}
    # synthesizer has one error + one ok + one skipped → degraded (amber)
    assert by_name["vault_synthesizer"]["health"] == "degraded"
    # job_feed has one ok → healthy
    assert by_name["job_feed"]["health"] == "healthy"
    # any agent with no runs → unknown
    # (none in fixture qualify; we extend in a follow-up test)


def test_compute_kpis_eval_pass_and_spend():
    runs = _runs()
    eval_run = readers.read_eval_last_run(FIXTURES / "sample-eval-last-run.md")
    kpis = aggregations.compute_kpis(runs, eval_run, gemini_total=8.40, council_total=0.41)
    assert kpis["eval_pass"] == "7 / 10"
    assert kpis["fleet_spend_30d_usd"] == pytest.approx(0.3812)
    assert 0 < kpis["local_only_share_pct"] <= 100
    assert kpis["spend_governors"] == "$50 / mo"
```

(Add `import pytest` at top of test file.)

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_aggregations.py -v`
Expected: ModuleNotFoundError on `lib.aggregations`.

- [ ] **Step 3: Implement aggregations module**

File: `lib/aggregations.py`

```python
"""Telemetry aggregation for the Agent Fleet Observability Dashboard."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone


def _is_local(model: str | None) -> bool:
    if not model:
        return True  # no model field = local task (rsync, sqlite, etc.)
    return any(tok in model.lower() for tok in ("qwen", "nomic", "gemma", "kokoro", "ollama"))


def compute_fleet_status(runs: list[dict], agent_names: list[str]) -> list[dict]:
    """One tile per agent. Health from the last 7 days of runs."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    by_agent: dict[str, list[dict]] = {n: [] for n in agent_names}
    for r in runs:
        if r["agent"] in by_agent and r["ts"] >= cutoff:
            by_agent[r["agent"]].append(r)
    tiles: list[dict] = []
    for name in agent_names:
        agent_runs = sorted(by_agent[name], key=lambda r: r["ts"], reverse=True)
        if not agent_runs:
            tiles.append({"agent": name, "health": "unknown", "last_run": None, "last_cost": 0.0})
            continue
        statuses = [r["status"] for r in agent_runs]
        has_error = any(s in ("error", "failed", "capped") for s in statuses)
        has_ok = any(s == "ok" for s in statuses)
        if has_error and has_ok:
            health = "degraded"
        elif has_error:
            health = "down"
        else:
            health = "healthy"
        last = agent_runs[0]
        tiles.append({
            "agent": name,
            "health": health,
            "last_run": last["ts"],
            "last_cost": last["cost_usd"],
            "last_status": last["status"],
            "last_notes": last["notes"],
            "run_count_7d": len(agent_runs),
        })
    return tiles


def compute_kpis(
    runs: list[dict],
    eval_run: dict,
    gemini_total: float,
    council_total: float,
) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    last_30 = [r for r in runs if r["ts"] >= cutoff]
    spend_30d = sum(r["cost_usd"] for r in last_30)
    local_runs = [r for r in last_30 if _is_local(r.get("model")) and r["cost_usd"] == 0.0]
    pct_local = (len(local_runs) / len(last_30) * 100) if last_30 else 100.0
    return {
        "eval_pass": f"{eval_run['passed']} / {eval_run['total_cases']}",
        "eval_pass_count": eval_run["passed"],
        "eval_total": eval_run["total_cases"],
        "fleet_spend_30d_usd": round(spend_30d, 4),
        "fleet_spend_30d_label": f"${spend_30d:.2f}",
        "run_count_30d": len(last_30),
        "local_only_share_pct": round(pct_local, 1),
        "spend_governors": "$50 / mo",
        "monthly_headroom_usd": round(50.0 - gemini_total, 2),
        "council_month_total": round(council_total, 2),
    }
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_aggregations.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/aggregations.py tests/test_aggregations.py
git commit -m "$(cat <<'EOF'
feat: compute_fleet_status + compute_kpis aggregations + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: `aggregations.compute_sparkline` + `compute_regression_window` (TDD)

**Files:**
- Modify: `tests/test_aggregations.py`
- Modify: `lib/aggregations.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_aggregations.py` — append:

```python
def test_compute_synth_series_60_days():
    manifests = [
        {"date": date(2026, 5, 1), "concepts_written": 0},
        {"date": date(2026, 5, 2), "concepts_written": 0},
        {"date": date(2026, 5, 10), "concepts_written": 0},
        {"date": date(2026, 5, 11), "concepts_written": 90},
        {"date": date(2026, 5, 13), "concepts_written": 114},
    ]
    series = aggregations.compute_synth_series(manifests, days=14, end=date(2026, 5, 14))
    assert len(series) == 14
    # day 2026-05-13 = index 12 in 14-day series ending 5/14
    assert series[12]["concepts"] == 114
    # missing dates fill with None (not 0 — we want a visible gap)
    assert series[7]["concepts"] is None  # 2026-05-07


def test_compute_regression_window_detects_silent_nights():
    manifests = [{"date": date(2026, 5, d), "concepts_written": 0} for d in range(1, 11)]
    manifests.append({"date": date(2026, 5, 11), "concepts_written": 90})
    window = aggregations.compute_regression_window(manifests)
    assert window["start"] == date(2026, 5, 1)
    assert window["end"] == date(2026, 5, 10)
    assert window["nights"] == 10


def test_compute_eval_sparkline_returns_14_values():
    # eval suite history isn't on disk yet — we synthesize from last_run only for v1
    eval_run = {"passed": 7, "total_cases": 10, "cases": []}
    spark = aggregations.compute_eval_sparkline(eval_run, days=14)
    assert len(spark) == 14
    assert all(0 <= v <= 10 for v in spark)
    assert spark[-1] == 7
```

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_aggregations.py -v`
Expected: 3 new failures.

- [ ] **Step 3: Implement**

File: `lib/aggregations.py` — append:

```python
from datetime import date as _date


def compute_synth_series(manifests: list[dict], days: int, end: _date) -> list[dict]:
    """Build a `days`-long series ending on `end`. Missing dates → concepts=None."""
    by_date = {m["date"]: m for m in manifests}
    out: list[dict] = []
    for i in range(days - 1, -1, -1):
        d = end - timedelta(days=i)
        m = by_date.get(d)
        out.append({
            "date": d,
            "concepts": m["concepts_written"] if m else None,
            "connections": m.get("connections_written") if m else None,
        })
    return out


def compute_regression_window(manifests: list[dict]) -> dict:
    """Find the longest run of consecutive zero-concept nights."""
    if not manifests:
        return {"start": None, "end": None, "nights": 0}
    sorted_m = sorted(manifests, key=lambda m: m["date"])
    best = {"start": None, "end": None, "nights": 0}
    run_start = None
    run_len = 0
    for m in sorted_m:
        if m.get("concepts_written", 0) == 0:
            run_start = run_start or m["date"]
            run_len += 1
            if run_len > best["nights"]:
                best = {"start": run_start, "end": m["date"], "nights": run_len}
        else:
            run_start = None
            run_len = 0
    return best


def compute_eval_sparkline(eval_run: dict, days: int = 14) -> list[int]:
    """v1: no historical eval store, so emit a flat-tail sparkline ending at today.

    Day 2 Task 11 follow-up: when we wire an evals/vault-synthesizer/history.jsonl,
    swap this to read real history.
    """
    today_pass = eval_run.get("passed", 0)
    return [today_pass] * days
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_aggregations.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/aggregations.py tests/test_aggregations.py
git commit -m "$(cat <<'EOF'
feat: synth series + regression window + eval sparkline

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 11: `aggregations.compute_cost_trend` + `compute_model_mix` + `compute_recent_runs` (TDD)

**Files:**
- Modify: `tests/test_aggregations.py`
- Modify: `lib/aggregations.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_aggregations.py` — append:

```python
def test_compute_cost_trend_30_day_stacked():
    runs = _runs()
    trend = aggregations.compute_cost_trend(runs, days=30, end=date(2026, 5, 14))
    assert len(trend["days"]) == 30
    assert set(trend["agents"]) <= set(AGENT_NAMES) | {"other"}
    # series[agent] is a list of `days` floats
    for agent, series in trend["series"].items():
        assert len(series) == 30


def test_compute_model_mix_buckets():
    runs = _runs()
    mix = aggregations.compute_model_mix(runs)
    assert "local" in mix
    assert "cloud" in mix
    # fixture has one daily_driver run (cloud-ish) and several local
    total_pct = sum(v["pct"] for v in mix.values())
    assert 99.0 <= total_pct <= 101.0  # rounding slack


def test_compute_recent_runs_returns_last_50_desc():
    runs = _runs()
    recent = aggregations.compute_recent_runs(runs, n=5)
    assert len(recent) == 5
    timestamps = [r["ts"] for r in recent]
    assert timestamps == sorted(timestamps, reverse=True)
```

- [ ] **Step 2: Run, watch fail**

Expected: 3 failures.

- [ ] **Step 3: Implement**

File: `lib/aggregations.py` — append:

```python
def compute_cost_trend(runs: list[dict], days: int, end: _date) -> dict:
    """Per-day per-agent cost totals for stacked area rendering."""
    by_date_agent: dict[tuple[_date, str], float] = {}
    agents: set[str] = set()
    for r in runs:
        d = r["ts"].date()
        if d > end or d < end - timedelta(days=days - 1):
            continue
        a = r["agent"]
        agents.add(a)
        key = (d, a)
        by_date_agent[key] = by_date_agent.get(key, 0.0) + r["cost_usd"]
    ordered_agents = sorted(agents)
    day_axis = [end - timedelta(days=i) for i in range(days - 1, -1, -1)]
    series: dict[str, list[float]] = {a: [0.0] * days for a in ordered_agents}
    for (d, a), v in by_date_agent.items():
        idx = day_axis.index(d)
        series[a][idx] = round(v, 4)
    return {"days": [d.isoformat() for d in day_axis], "agents": ordered_agents, "series": series}


def compute_model_mix(runs: list[dict]) -> dict[str, dict]:
    """Bucket runs by local-vs-cloud + family. Returns {label: {count, pct}}."""
    buckets: Counter = Counter()
    for r in runs:
        model = (r.get("model") or "").lower()
        if "qwen" in model or "ollama" in model:
            label = "local-qwen"
        elif "nomic" in model:
            label = "local-nomic"
        elif "gemma" in model or "kokoro" in model:
            label = "local-other"
        elif "sonnet" in model or "opus" in model or "haiku" in model:
            label = "cloud-anthropic"
        elif "gemini" in model:
            label = "cloud-gemini"
        elif r["cost_usd"] == 0.0:
            label = "local"
        else:
            label = "cloud"
        buckets[label] += 1
    total = sum(buckets.values()) or 1
    return {label: {"count": n, "pct": round(n / total * 100, 1)} for label, n in buckets.items()}


def compute_recent_runs(runs: list[dict], n: int = 50) -> list[dict]:
    return sorted(runs, key=lambda r: r["ts"], reverse=True)[:n]


def compute_all(data: dict, *, end: _date | None = None) -> dict:
    """Single entry point: build every aggregate the renderers need."""
    end = end or datetime.now(timezone.utc).date()
    runs = data["agent_runs"]
    eval_run = data["eval_last_run"]
    gemini = data["gemini_spend"]
    council = data["council_spend"]
    manifests = data["synth_manifests"]
    agent_names = data["agent_names"]
    return {
        "fleet_status": compute_fleet_status(runs, agent_names),
        "kpis": compute_kpis(runs, eval_run, gemini["total_usd"], council["month_total_usd"]),
        "synth_series_60d": compute_synth_series(manifests, days=60, end=end),
        "synth_series_14d": compute_synth_series(manifests, days=14, end=end),
        "regression_window": compute_regression_window(manifests),
        "eval_sparkline": compute_eval_sparkline(eval_run, days=14),
        "cost_trend_30d": compute_cost_trend(runs, days=30, end=end),
        "model_mix": compute_model_mix([r for r in runs if r["ts"].date() >= end - timedelta(days=30)]),
        "recent_runs": compute_recent_runs(runs, n=50),
        "gemini": gemini,
        "council": council,
        "eval": eval_run,
        "lint": data.get("lint_reports", {}),
        "job_feed": data.get("job_feed_db", {}),
        "job_feed_manifests": data.get("job_feed_manifests", {}),
        "research_queue": data.get("research_queue", {}),
        "manual_tickets": data.get("manual_tickets", {}),
        "end_date": end,
    }
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_aggregations.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/aggregations.py tests/test_aggregations.py
git commit -m "$(cat <<'EOF'
feat: cost trend + model mix + recent runs + compute_all entry

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 12: `anonymize.public_pass` (TDD)

Implements design doc Sections 2c + 3f.

**Files:**
- Create: `tests/test_anonymize.py`
- Create: `lib/anonymize.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_anonymize.py`

```python
import copy
from datetime import date, datetime, timezone

from lib import anonymize


def _agg():
    return {
        "fleet_status": [{"agent": "vault_synthesizer", "last_notes": "vault/.job-feed.db hit cap"}],
        "kpis": {"fleet_spend_30d_usd": 8.40, "fleet_spend_30d_label": "$8.40"},
        "recent_runs": [
            {"ts": datetime(2026, 5, 13, 12, tzinfo=timezone.utc),
             "agent": "deep_researcher", "status": "ok", "cost_usd": 0.0,
             "notes": "vault/20_projects/research/2026-05-13-foo.md updated"},
        ],
        "job_feed": {"total_postings": 4, "by_status": {"new": 1}, "top_fit": [{"company": "X"}]},
        "research_queue": {"pending": [
            {"title": "Anthropic interview prep — vault/20_projects/prj-job-hunt-2026/notes.md",
             "assigned_agent": None},
        ]},
        "manual_tickets": {"todo": [], "in_progress": [], "done": []},
    }


def test_public_pass_strips_job_feed_db_content():
    pub = anonymize.public_pass(_agg())
    assert pub["job_feed"] == {"total_postings": 0, "by_status": {}, "top_fit": [], "active_count": 0}


def test_public_pass_redacts_vault_paths_in_notes():
    pub = anonymize.public_pass(_agg())
    assert "vault/" not in pub["fleet_status"][0]["last_notes"]
    assert "[redacted]" in pub["fleet_status"][0]["last_notes"]
    assert "vault/" not in pub["recent_runs"][0]["notes"]


def test_public_pass_redacts_vault_paths_in_ticket_titles():
    pub = anonymize.public_pass(_agg())
    title = pub["research_queue"]["pending"][0]["title"]
    assert "vault/" not in title


def test_public_pass_preserves_dollar_amounts():
    pub = anonymize.public_pass(_agg())
    assert pub["kpis"]["fleet_spend_30d_label"] == "$8.40"
    assert pub["kpis"]["fleet_spend_30d_usd"] == 8.40


def test_public_pass_does_not_mutate_input():
    src = _agg()
    snapshot = copy.deepcopy(src)
    anonymize.public_pass(src)
    assert src == snapshot
```

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_anonymize.py -v`
Expected: ModuleNotFoundError.

- [ ] **Step 3: Implement**

File: `lib/anonymize.py`

```python
"""Public-pass anonymization for the Agent Fleet Observability Dashboard.

Implements the privacy boundary described in design doc Sections 2c + 3f.
Rules:
1. Job Feed data source is fully zeroed (skipped on public pass).
2. Vault path references in notes / titles are replaced with `vault/[redacted]`.
3. Dollar amounts are PRESERVED — they tell the architectural story.
4. Eval case names, agent names, run timestamps are PRESERVED.
"""
from __future__ import annotations

import copy
import re


_VAULT_PATH_RE = re.compile(r"vault/[\w\-/.]+")


def _redact_paths(text: str | None) -> str:
    if not text:
        return text or ""
    return _VAULT_PATH_RE.sub("vault/[redacted]", text)


def public_pass(agg: dict) -> dict:
    """Return a deep copy of `agg` with public-safe substitutions."""
    out = copy.deepcopy(agg)
    for tile in out.get("fleet_status", []):
        tile["last_notes"] = _redact_paths(tile.get("last_notes"))
    for r in out.get("recent_runs", []):
        r["notes"] = _redact_paths(r.get("notes"))
    out["job_feed"] = {"total_postings": 0, "by_status": {}, "top_fit": [], "active_count": 0}
    out["job_feed_manifests"] = {"latest": None, "last_7": []}
    for section in ("pending", "in_flight", "done"):
        for item in out.get("research_queue", {}).get(section, []):
            item["title"] = _redact_paths(item.get("title"))
    for section in ("todo", "in_progress", "done"):
        for item in out.get("manual_tickets", {}).get(section, []):
            item["title"] = _redact_paths(item.get("title"))
    out["_public_pass_applied"] = True
    return out
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_anonymize.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/anonymize.py tests/test_anonymize.py
git commit -m "$(cat <<'EOF'
feat: public-pass anonymization layer + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 13: `svg_charts.line_chart_with_annotation` (TDD)

Hero regression chart helper. Implements design doc Section 3c.

**Files:**
- Create: `tests/test_svg_charts.py`
- Create: `lib/svg_charts.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_svg_charts.py`

```python
from datetime import date

from lib import svg_charts


def test_line_chart_returns_svg_string():
    series = [{"date": date(2026, 5, d), "value": v} for d, v in enumerate([10, 0, 0, 0, 90, 114], start=8)]
    svg = svg_charts.line_chart(series, width=600, height=160)
    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert "viewBox" in svg


def test_line_chart_with_annotation_includes_band():
    series = [{"date": date(2026, 5, d), "value": 0} for d in range(1, 11)]
    svg = svg_charts.line_chart(
        series,
        width=600, height=160,
        annotation={"start_date": date(2026, 5, 1), "end_date": date(2026, 5, 10),
                    "label": "9-DAY SILENT REGRESSION"},
    )
    assert "9-DAY SILENT REGRESSION" in svg
    # red dashed rect
    assert "stroke-dasharray" in svg


def test_line_chart_handles_none_gaps():
    series = [
        {"date": date(2026, 5, 1), "value": 0},
        {"date": date(2026, 5, 2), "value": None},
        {"date": date(2026, 5, 3), "value": 5},
    ]
    svg = svg_charts.line_chart(series, width=400, height=120)
    # Should still emit valid SVG, just skip the None
    assert svg.startswith("<svg")
```

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_svg_charts.py -v`
Expected: ModuleNotFoundError.

- [ ] **Step 3: Implement**

File: `lib/svg_charts.py`

```python
"""Inline SVG chart helpers.

Every helper returns a complete `<svg>...</svg>` string. No CSS classes inside
the SVG — colors and strokes are inlined so the markup is self-contained when
copy-pasted into Substack or screenshotted.
"""
from __future__ import annotations

from datetime import date, timedelta


# Palette mirrors design doc Section 5b
GREEN = "#3fb950"
TEAL = "#18b894"
AMBER = "#f0b429"
RED = "#f85149"
BLUE = "#58a6ff"
PURPLE = "#c084fc"
TEXT = "#e6edf3"
SECONDARY = "#8b949e"
PANEL = "#11151c"
GRID = "#1a2230"


def _scale(val: float, src_lo: float, src_hi: float, dst_lo: float, dst_hi: float) -> float:
    if src_hi == src_lo:
        return (dst_lo + dst_hi) / 2
    return dst_lo + (val - src_lo) * (dst_hi - dst_lo) / (src_hi - src_lo)


def line_chart(
    series: list[dict],
    width: int,
    height: int,
    annotation: dict | None = None,
    color: str = TEAL,
    pad_top: int = 20,
    pad_right: int = 20,
    pad_bottom: int = 28,
    pad_left: int = 40,
) -> str:
    inner_w = width - pad_left - pad_right
    inner_h = height - pad_top - pad_bottom
    if not series:
        return f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"></svg>'
    values = [s["value"] for s in series if s["value"] is not None] or [0]
    v_lo, v_hi = 0, max(max(values), 1)
    dates = [s["date"] for s in series]
    d_lo, d_hi = dates[0].toordinal(), dates[-1].toordinal()

    def x(d: date) -> float:
        return pad_left + _scale(d.toordinal(), d_lo, d_hi, 0, inner_w)

    def y(v: float) -> float:
        return pad_top + inner_h - _scale(v, v_lo, v_hi, 0, inner_h)

    parts: list[str] = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        'font-family="JetBrains Mono, monospace">'
    ]
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="{PANEL}"/>')
    for i in range(4):
        gy = pad_top + i * inner_h / 3
        parts.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{width - pad_right}" y2="{gy:.1f}" '
                     f'stroke="{GRID}" stroke-width="1"/>')

    if annotation:
        ax = x(annotation["start_date"])
        bx = x(annotation["end_date"])
        parts.append(f'<rect x="{ax:.1f}" y="{pad_top}" width="{(bx - ax):.1f}" '
                     f'height="{inner_h}" fill="{RED}" fill-opacity="0.10" '
                     f'stroke="{RED}" stroke-width="1" stroke-dasharray="4 3"/>')
        parts.append(f'<text x="{ax + 4:.1f}" y="{pad_top - 6}" font-size="9" fill="{RED}" '
                     f'font-weight="700">{annotation["label"]}</text>')

    pts: list[str] = []
    for s in series:
        if s["value"] is None:
            if pts:
                parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" '
                             f'points="{" ".join(pts)}"/>')
                pts = []
            continue
        pts.append(f"{x(s['date']):.1f},{y(s['value']):.1f}")
    if pts:
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" '
                     f'points="{" ".join(pts)}"/>')

    # x-axis labels — first, middle, last
    label_dates = [dates[0], dates[len(dates) // 2], dates[-1]]
    for d in label_dates:
        parts.append(f'<text x="{x(d):.1f}" y="{height - 6}" font-size="9" fill="{SECONDARY}" '
                     f'text-anchor="middle">{d.isoformat()}</text>')

    parts.append("</svg>")
    return "\n".join(parts)
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_svg_charts.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/svg_charts.py tests/test_svg_charts.py
git commit -m "$(cat <<'EOF'
feat: svg_charts.line_chart with regression annotation + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 14: `svg_charts.sparkline` + `donut` + `stacked_area` (TDD)

**Files:**
- Modify: `tests/test_svg_charts.py`
- Modify: `lib/svg_charts.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_svg_charts.py` — append:

```python
def test_sparkline_renders():
    svg = svg_charts.sparkline([1, 2, 3, 4, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7], width=80, height=16)
    assert svg.startswith("<svg")


def test_donut_renders_segments():
    segments = [{"label": "local-qwen", "value": 78, "color": "#18b894"},
                {"label": "cloud-anthropic", "value": 22, "color": "#58a6ff"}]
    svg = svg_charts.donut(segments, size=120)
    assert svg.startswith("<svg")
    assert "local-qwen" not in svg  # labels rendered separately by template


def test_stacked_area_handles_multi_agent():
    days = [f"2026-05-{d:02d}" for d in range(1, 8)]
    series = {"vault_synthesizer": [0]*7, "daily_driver": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    svg = svg_charts.stacked_area(days, series, width=400, height=120)
    assert svg.startswith("<svg")
```

- [ ] **Step 2: Run, watch fail**

Expected: 3 AttributeError failures.

- [ ] **Step 3: Implement**

File: `lib/svg_charts.py` — append:

```python
import math


def sparkline(values: list[float | int], width: int = 80, height: int = 16,
              color: str = GREEN) -> str:
    if not values:
        return f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"></svg>'
    v_lo, v_hi = min(values), max(values)
    if v_hi == v_lo:
        v_hi += 1
    pts: list[str] = []
    for i, v in enumerate(values):
        x = i * (width - 2) / max(1, len(values) - 1) + 1
        y = height - 1 - (v - v_lo) * (height - 2) / (v_hi - v_lo)
        pts.append(f"{x:.1f},{y:.1f}")
    return (
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<polyline fill="none" stroke="{color}" stroke-width="1.5" '
        f'points="{" ".join(pts)}"/></svg>'
    )


def donut(segments: list[dict], size: int = 120, stroke: int = 14) -> str:
    """`segments`: list of {'value': float, 'color': str}. Values normalize to 360°."""
    total = sum(s["value"] for s in segments) or 1.0
    radius = (size - stroke) / 2
    cx = cy = size / 2
    parts = [f'<svg viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">']
    angle = -90.0  # start at 12 o'clock
    for seg in segments:
        sweep = seg["value"] / total * 360.0
        large = 1 if sweep > 180 else 0
        a1 = math.radians(angle)
        a2 = math.radians(angle + sweep)
        x1 = cx + radius * math.cos(a1)
        y1 = cy + radius * math.sin(a1)
        x2 = cx + radius * math.cos(a2)
        y2 = cy + radius * math.sin(a2)
        parts.append(
            f'<path d="M {x1:.2f} {y1:.2f} A {radius:.2f} {radius:.2f} 0 {large} 1 {x2:.2f} {y2:.2f}" '
            f'fill="none" stroke="{seg["color"]}" stroke-width="{stroke}"/>'
        )
        angle += sweep
    parts.append("</svg>")
    return "".join(parts)


_AGENT_COLORS = [TEAL, GREEN, AMBER, BLUE, PURPLE, "#ff7b72", "#79c0ff", "#d2a8ff"]


def stacked_area(
    days: list[str],
    series: dict[str, list[float]],
    width: int,
    height: int,
    pad_top: int = 12,
    pad_right: int = 12,
    pad_bottom: int = 24,
    pad_left: int = 36,
) -> str:
    inner_w = width - pad_left - pad_right
    inner_h = height - pad_top - pad_bottom
    n = len(days)
    if n == 0:
        return f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"></svg>'
    stack: list[list[float]] = [[0.0] * n]
    agents = list(series.keys())
    for a in agents:
        stack.append([stack[-1][i] + series[a][i] for i in range(n)])
    total_max = max(stack[-1]) or 1.0
    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="JetBrains Mono, monospace">'
    ]
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="{PANEL}"/>')

    def x(i: int) -> float:
        return pad_left + i * inner_w / max(1, n - 1)

    def y(v: float) -> float:
        return pad_top + inner_h - v * inner_h / total_max

    for idx, a in enumerate(agents):
        color = _AGENT_COLORS[idx % len(_AGENT_COLORS)]
        upper = stack[idx + 1]
        lower = stack[idx]
        pts = [f"{x(i):.1f},{y(upper[i]):.1f}" for i in range(n)]
        pts += [f"{x(i):.1f},{y(lower[i]):.1f}" for i in range(n - 1, -1, -1)]
        parts.append(f'<polygon fill="{color}" fill-opacity="0.85" '
                     f'points="{" ".join(pts)}"/>')
    parts.append(f'<text x="{pad_left}" y="{height - 6}" font-size="9" fill="{SECONDARY}">'
                 f'{days[0]}</text>')
    parts.append(f'<text x="{width - pad_right}" y="{height - 6}" font-size="9" fill="{SECONDARY}" '
                 f'text-anchor="end">{days[-1]}</text>')
    parts.append("</svg>")
    return "".join(parts)
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_svg_charts.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/svg_charts.py tests/test_svg_charts.py
git commit -m "$(cat <<'EOF'
feat: svg sparkline + donut + stacked area + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 15: `assets/styles.css` — palette, typography, layout tokens

Implements design doc Sections 5b + 5c.

**Files:**
- Create: `assets/styles.css`

- [ ] **Step 1: Write `assets/styles.css`**

```css
/* Agent Fleet Observability — Personality D (dark hybrid) */
/* Palette + typography per design doc Section 5b-5c */

:root {
  --bg-primary: #0a0d12;
  --bg-panel: #11151c;
  --bg-recessed: #0d1219;
  --border-subtle: #1a2230;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-tertiary: #6e7681;
  --accent-green: #3fb950;
  --accent-teal: #18b894;
  --accent-amber: #f0b429;
  --accent-purple: #c084fc;
  --accent-red: #f85149;
  --accent-blue: #58a6ff;
  --font-heading: 'Sora', 'SF Pro', system-ui, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', Monaco, monospace;
  --radius-sm: 4px;
  --radius-md: 8px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--bg-primary); color: var(--text-primary); }
body {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent-blue); text-decoration: none; }
a:hover { text-decoration: underline; }

.priv-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-5) var(--space-4);
}

.panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-bottom: var(--space-4);
}

.panel-recessed { background: var(--bg-recessed); }

.eyebrow {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-tertiary);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.mono { font-family: var(--font-mono); }

.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}
.kpi-card { padding: var(--space-3); }
.kpi-label { font-family: var(--font-mono); font-size: 10px; color: var(--text-tertiary); text-transform: uppercase; }
.kpi-value { font-family: var(--font-heading); font-size: 28px; font-weight: 600; margin-top: var(--space-1); }
.kpi-sub { font-family: var(--font-mono); font-size: 11px; color: var(--text-secondary); margin-top: var(--space-1); }
.kpi-value.green { color: var(--accent-green); }
.kpi-value.amber { color: var(--accent-amber); }
.kpi-value.red { color: var(--accent-red); }

.agent-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}
.agent-tile {
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}
.agent-name { font-family: var(--font-heading); font-size: 12px; font-weight: 600; }
.agent-sub { font-family: var(--font-mono); font-size: 10px; color: var(--text-secondary); }
.status-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  vertical-align: middle; margin-right: var(--space-1);
}
.status-dot.healthy { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-dot.degraded { background: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }
.status-dot.down { background: var(--accent-red); box-shadow: 0 0 6px var(--accent-red); }
.status-dot.unknown { background: var(--text-tertiary); }

.topbar {
  display: flex; align-items: center; gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--border-subtle);
}
.wordmark { font-family: var(--font-heading); font-size: 16px; font-weight: 600; }
.subtitle { font-family: var(--font-mono); font-size: 11px; color: var(--text-tertiary); }
.status-pill {
  font-family: var(--font-mono); font-size: 10px; padding: 2px 8px;
  border-radius: 999px; background: var(--bg-recessed);
  border: 1px solid var(--border-subtle);
}
.nav-link {
  font-family: var(--font-mono); font-size: 11px; padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm); color: var(--text-secondary);
}
.nav-link.active { background: var(--bg-recessed); border: 1px solid var(--border-subtle); color: var(--text-primary); }
.private-badge {
  font-family: var(--font-mono); font-size: 10px;
  background: #2d1f3a; color: var(--accent-purple);
  padding: 2px 8px; border-radius: var(--radius-sm);
}

.footer {
  border-top: 1px solid var(--border-subtle);
  padding: var(--space-5) var(--space-4);
  font-family: var(--font-mono); font-size: 11px; color: var(--text-tertiary);
  text-align: center;
}

.hero-headline { font-family: var(--font-heading); font-size: 18px; line-height: 1.4; margin: var(--space-2) 0; }
.hero-headline .accent { color: var(--accent-amber); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/styles.css
git commit -m "$(cat <<'EOF'
feat: styles.css — dark hybrid palette + typography tokens

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 16: Mascot CSS + base template (topbar + footer)

Implements design doc Sections 3b, 5d, 5f.

**Files:**
- Modify: `assets/styles.css` (append mascot rules)
- Create: `templates/base.html`
- Create: `templates/partials/mascot.html`
- Create: `templates/partials/topbar.html`
- Create: `templates/partials/footer.html`

- [ ] **Step 1: Append Asterisk Spark mascot CSS to `assets/styles.css`**

```css
/* Asterisk Spark mascot — design doc Section 5d */
@keyframes m-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes m-blink {
  0%, 88%, 100% { transform: scaleY(1); }
  91%, 95% { transform: scaleY(0.08); }
}
.spark {
  width: 32px; height: 32px; position: relative;
  display: inline-flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.spark .arms { position: absolute; width: 100%; height: 100%; animation: m-spin 12s linear infinite; }
.spark .arm {
  position: absolute;
  background: linear-gradient(180deg, #f0b429 0%, #c084fc 100%);
  border-radius: 1px;
}
.spark .arm-v { width: 2px; height: 100%; left: 50%; transform: translateX(-50%); }
.spark .arm-h { width: 100%; height: 2px; top: 50%; transform: translateY(-50%); }
.spark .arm-d1 { width: 2px; height: 90%; left: 50%; top: 5%; transform: translateX(-50%) rotate(45deg); opacity: 0.6; }
.spark .arm-d2 { width: 2px; height: 90%; left: 50%; top: 5%; transform: translateX(-50%) rotate(-45deg); opacity: 0.6; }
.spark .core {
  width: 14px; height: 14px; background: var(--bg-primary);
  border-radius: 50%; position: relative; z-index: 2;
  border: 1px solid var(--accent-amber);
  box-shadow: 0 0 16px rgba(240, 180, 41, 0.4);
}
.spark .eye {
  position: absolute; width: 1.8px; height: 2.2px;
  background: var(--accent-amber); border-radius: 0.5px; top: 4px;
  animation: m-blink 5.5s infinite; transform-origin: center;
}
.spark .eye-l { left: 3px; }
.spark .eye-r { right: 3px; }
```

- [ ] **Step 2: Write `templates/partials/mascot.html`**

```html
<div class="spark" aria-hidden="true">
  <div class="arms">
    <div class="arm arm-v"></div>
    <div class="arm arm-h"></div>
    <div class="arm arm-d1"></div>
    <div class="arm arm-d2"></div>
  </div>
  <div class="core">
    <div class="eye eye-l"></div>
    <div class="eye eye-r"></div>
  </div>
</div>
```

- [ ] **Step 3: Write `templates/partials/topbar.html`**

```html
{# Vars: is_private (bool), active_route, snapshot_ts, fleet_health_label, extra_pills (list) #}
<div class="topbar">
  {% include "partials/mascot.html" %}
  <div>
    <div class="wordmark">Agent Fleet Observability</div>
    <div class="subtitle">fleet.seanwinslow.com</div>
  </div>
  {% if is_private %}<span class="private-badge">PRIVATE</span>{% endif %}
  <span class="status-pill mono">● {{ fleet_health_label }}</span>
  {% for pill in extra_pills %}
    <span class="status-pill mono">{{ pill }}</span>
  {% endfor %}
  <span class="subtitle" style="margin-left: auto;">{{ snapshot_ts }}</span>
  <nav style="display: flex; gap: 4px;">
    <a class="nav-link {% if active_route == 'fleet' %}active{% endif %}" href="./index.html">/fleet</a>
    <a class="nav-link {% if active_route == 'kanban' %}active{% endif %}" href="./kanban.html">/kanban</a>
  </nav>
</div>
```

- [ ] **Step 4: Write `templates/partials/footer.html`**

```html
<footer class="footer">
  <strong>Built by Sean Winslow.</strong>
  8 agents on macOS launchd, 99% local-first inference.
  <a href="https://github.com/seanwinslow28/agent-fleet-observability">View source</a>
  · last build {{ snapshot_ts }}
</footer>
```

- [ ] **Step 5: Write `templates/base.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page_title|default("Agent Fleet Observability") }}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Sora:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css">
  <meta name="description" content="Static observability dashboard for an 8-agent local-first AI fleet.">
</head>
<body>
  {% include "partials/topbar.html" %}
  <main class="priv-wrap">
    {% block content %}{% endblock %}
  </main>
  {% include "partials/footer.html" %}
  {% block scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Step 6: Commit**

```bash
git add assets/styles.css templates/
git commit -m "$(cat <<'EOF'
feat: base template + asterisk spark mascot + topbar + footer

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 17: KPI row + agent grid partials

Implements design doc Section 3c.

**Files:**
- Create: `templates/partials/kpi_row.html`
- Create: `templates/partials/agent_grid.html`

- [ ] **Step 1: Write `templates/partials/kpi_row.html`**

```html
{# Vars: kpis (dict from compute_kpis), eval_sparkline_svg, is_private #}
<div class="kpi-row">
  <div class="panel kpi-card">
    <div class="kpi-label">Eval pass · last night</div>
    <div class="kpi-value green">{{ kpis.eval_pass }}</div>
    <div class="kpi-sub">{{ eval_sparkline_svg|safe }}</div>
  </div>
  <div class="panel kpi-card">
    <div class="kpi-label">Fleet spend · 30 days</div>
    <div class="kpi-value">{{ kpis.fleet_spend_30d_label }}</div>
    <div class="kpi-sub">{{ kpis.local_only_share_pct }}% local · {{ kpis.run_count_30d }} runs</div>
  </div>
  <div class="panel kpi-card">
    <div class="kpi-label">{% if is_private %}Monthly headroom{% else %}Local-only share{% endif %}</div>
    <div class="kpi-value {% if is_private %}amber{% else %}green{% endif %}">
      {% if is_private %}${{ "%.0f"|format(kpis.monthly_headroom_usd) }} / $50
      {% else %}{{ kpis.local_only_share_pct }}%
      {% endif %}
    </div>
    <div class="kpi-sub">
      {% if is_private %}Gemini DR · {{ "%.0f"|format(50 - kpis.monthly_headroom_usd) }}% used
      {% else %}7 of 8 agents · $0/run
      {% endif %}
    </div>
  </div>
  <div class="panel kpi-card">
    <div class="kpi-label">Spend governors</div>
    <div class="kpi-value amber">{{ kpis.spend_governors }}</div>
    <div class="kpi-sub">$7 task · $20 daily breaker</div>
  </div>
</div>
```

- [ ] **Step 2: Write `templates/partials/agent_grid.html`**

```html
{# Vars: fleet_status (list of 8 dicts), is_private #}
<div class="agent-grid">
  {% for tile in fleet_status %}
    <div class="panel agent-tile">
      <div>
        <span class="status-dot {{ tile.health }}"></span>
        <span class="agent-name">{{ tile.agent }}</span>
      </div>
      <div class="agent-sub">
        {% if tile.last_run %}
          last run {{ tile.last_run.strftime('%Y-%m-%d %H:%M') }}
        {% else %}
          no runs in last 7 days
        {% endif %}
      </div>
      <div class="agent-sub">
        {% if tile.last_cost is defined %}${{ "%.4f"|format(tile.last_cost) }}{% endif %}
        {% if tile.last_status %} · {{ tile.last_status }}{% endif %}
      </div>
      {% if is_private and tile.last_notes %}
        <div class="agent-sub">{{ tile.last_notes }}</div>
      {% endif %}
    </div>
  {% endfor %}
</div>
```

- [ ] **Step 3: Commit**

```bash
git add templates/partials/kpi_row.html templates/partials/agent_grid.html
git commit -m "$(cat <<'EOF'
feat: kpi row + agent grid partials

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

# Day 2 — Hero chart, below-fold panels, render orchestration

## Task 18: Hero regression chart partial + fleet page skeleton

Implements design doc Section 3c.1.

**Files:**
- Create: `templates/partials/hero_regression.html`
- Create: `templates/fleet.html`

- [ ] **Step 1: Write `templates/partials/hero_regression.html`**

```html
{# Vars: hero_svg (rendered string), regression_window (dict), end_date #}
<div class="panel">
  <div class="eyebrow">Vault Synthesizer · concepts written per night · 60 days</div>
  <p class="hero-headline">
    For
    <span class="accent">{{ regression_window.nights }} consecutive nights</span>,
    the synthesizer wrote zero concepts. The eval suite caught it on day {{ regression_window.nights + 1 }}.
  </p>
  {{ hero_svg|safe }}
</div>
```

- [ ] **Step 2: Write `templates/fleet.html`**

```html
{% extends "base.html" %}
{% block content %}
  {% include "partials/hero_regression.html" %}
  {% include "partials/kpi_row.html" %}
  {% include "partials/agent_grid.html" %}
  {% if is_private %}
    {% include "partials/below_fold_private.html" %}
  {% else %}
    {% include "partials/below_fold_public.html" %}
  {% endif %}
{% endblock %}
```

- [ ] **Step 3: Commit**

```bash
git add templates/partials/hero_regression.html templates/fleet.html
git commit -m "$(cat <<'EOF'
feat: hero regression partial + fleet page skeleton

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 19: Below-fold public panels (cost trend, model mix, recent runs, synth telemetry, eval grid)

Implements design doc Section 3d.

**Files:**
- Create: `templates/partials/below_fold_public.html`

- [ ] **Step 1: Write the public below-fold partial**

```html
{# Vars: cost_trend_svg, model_mix_svg, model_mix_segments, synth_60d_svg, recent_runs (list),
         eval_cases (list), is_private (bool — false here) #}

<section class="panel">
  <div class="eyebrow">30-day cost trend · stacked area</div>
  {{ cost_trend_svg|safe }}
</section>

<section class="panel">
  <div class="eyebrow">Model mix · last 30 days</div>
  <div style="display: flex; gap: 24px; align-items: center;">
    {{ model_mix_svg|safe }}
    <ul style="list-style: none; padding: 0; margin: 0; font-family: var(--font-mono); font-size: 11px;">
      {% for seg in model_mix_segments %}
        <li><span class="status-dot" style="background: {{ seg.color }};"></span>
          {{ seg.label }} — {{ seg.pct }}%</li>
      {% endfor %}
    </ul>
  </div>
</section>

<section class="panel">
  <div class="eyebrow">Synthesizer telemetry · 60 nights</div>
  {{ synth_60d_svg|safe }}
</section>

<section class="panel">
  <div class="eyebrow">Recent runs · last 50</div>
  <table style="width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 11px;">
    <thead>
      <tr style="color: var(--text-tertiary); text-align: left;">
        <th style="padding: 4px;">ts</th><th>agent</th><th>status</th>
        <th>duration</th><th>cost</th>
      </tr>
    </thead>
    <tbody>
      {% for r in recent_runs %}
        <tr style="border-top: 1px solid var(--border-subtle);">
          <td style="padding: 4px;">{{ r.ts.strftime('%Y-%m-%d %H:%M') }}</td>
          <td>{{ r.agent }}</td>
          <td>{{ r.status }}</td>
          <td>{% if r.duration_ms %}{{ (r.duration_ms / 1000)|int }}s{% else %}—{% endif %}</td>
          <td>${{ "%.4f"|format(r.cost_usd) }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</section>

<section class="panel">
  <div class="eyebrow">Eval suite · last 14 days</div>
  <div style="display: grid; grid-template-columns: 180px repeat(14, 1fr); gap: 2px;">
    <div></div>
    {% for col in range(14) %}<div style="font-family: var(--font-mono); font-size: 9px; color: var(--text-tertiary); text-align: center;">{{ col + 1 }}</div>{% endfor %}
    {% for case in eval_cases %}
      <div style="font-family: var(--font-mono); font-size: 10px;">{{ case.id }}</div>
      {% for col in range(14) %}
        {% set s = case.status %}
        <div style="height: 14px; border-radius: 2px;
          background: {% if s == 'passed' %}var(--accent-green){% elif s == 'failed' %}var(--accent-red){% elif s == 'skipped' %}var(--accent-amber){% else %}var(--border-subtle){% endif %};
          opacity: {% if col < 13 %}0.35{% else %}1{% endif %};"></div>
      {% endfor %}
    {% endfor %}
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add templates/partials/below_fold_public.html
git commit -m "$(cat <<'EOF'
feat: below-fold public panels — cost trend, model mix, runs, eval grid

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 20: Below-fold private panels (alerts banner, job hunt, cloud spend governance, recent failures)

Implements design doc Sections 4c.1 + 4d.

**Note on data gaps (per pre-build assumption #3 above):** The "Job Hunt — Next Actions" and "Warm-Intro Pipeline" panels do not have backing schema in `vault/.job-feed.db`. v1 renders these panels with a Sean-voice empty-state ("Pipeline not yet structured — see prj-job-hunt-2026 notes"). The Target-30 funnel uses `by_status` aggregates from the live schema, mapped against a Tier-A target list maintained by Sean in `vault/00_inbox/target-30.md` (new file Sean optionally creates; falls back to empty-state if missing).

**Files:**
- Create: `templates/partials/below_fold_private.html`
- Create: `templates/partials/alerts_banner.html`

- [ ] **Step 1: Write `templates/partials/alerts_banner.html`**

```html
{# Vars: alerts (list of {severity, message, ts}). Renders nothing if empty. #}
{% if alerts %}
<div class="panel" style="border-color: var(--accent-amber);">
  <div style="display: flex; justify-content: space-between; align-items: baseline;">
    <strong style="color: var(--accent-amber); font-family: var(--font-heading);">
      ⚠ {{ alerts|length }} thing{% if alerts|length != 1 %}s{% endif %} need{% if alerts|length == 1 %}s{% endif %} your attention
    </strong>
    <span class="subtitle">overnight · last 12h</span>
  </div>
  {% for a in alerts %}
    <div style="display: flex; gap: 12px; padding: 8px 0; border-top: 1px solid var(--border-subtle);">
      <span class="status-dot {{ a.severity }}"></span>
      <span style="flex: 1;">{{ a.message }}</span>
      <span class="subtitle">{{ a.ts }}</span>
    </div>
  {% endfor %}
</div>
{% endif %}
```

- [ ] **Step 2: Write `templates/partials/below_fold_private.html`**

```html
{# Extends public below-fold with private-only panels. Public partials reused. #}
{% include "partials/below_fold_public.html" %}

<section class="panel">
  <div class="eyebrow">Job Hunt · Target funnel</div>
  {% if job_feed.total_postings == 0 %}
    <p class="subtitle">Job feed paused. Watchlist hasn't fired today.</p>
  {% else %}
    <p>Total tracked: <strong class="mono">{{ job_feed.total_postings }}</strong></p>
    <ul style="font-family: var(--font-mono); font-size: 12px; list-style: none; padding: 0;">
      {% for status, n in job_feed.by_status.items() %}
        <li>{{ status }} — <strong>{{ n }}</strong></li>
      {% endfor %}
    </ul>
  {% endif %}
</section>

<section class="panel">
  <div class="eyebrow">Job Hunt · Top 10 by fit score</div>
  {% if not job_feed.top_fit %}
    <p class="subtitle">No scored postings in window.</p>
  {% else %}
    <table style="width: 100%; font-family: var(--font-mono); font-size: 11px; border-collapse: collapse;">
      <thead><tr style="color: var(--text-tertiary); text-align: left;">
        <th>company</th><th>title</th><th>fit</th><th>status</th>
      </tr></thead>
      <tbody>
        {% for p in job_feed.top_fit %}
          <tr style="border-top: 1px solid var(--border-subtle);">
            <td style="padding: 4px;">{{ p.company }}</td>
            <td>{{ p.title }}</td>
            <td><strong>{{ p.fit_score }}</strong></td>
            <td>{{ p.status }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% endif %}
</section>

<section class="panel">
  <div class="eyebrow">Job Hunt · Next actions</div>
  <p class="subtitle">Pipeline not yet structured — see <span class="mono">vault/20_projects/prj-job-hunt-2026/</span> notes.</p>
</section>

<section class="panel">
  <div class="eyebrow">Job Hunt · Warm-intro pipeline</div>
  <p class="subtitle">Pipeline not yet structured — schema extension deferred to v1.1.</p>
</section>

<section class="panel">
  <div class="eyebrow">Cloud spend · Gemini DR (this month)</div>
  <p>
    <strong class="mono">${{ "%.2f"|format(gemini.total_usd) }}</strong>
    of $50 cap · {{ gemini.run_count }} runs
  </p>
  <div style="height: 8px; background: var(--bg-recessed); border-radius: 4px; overflow: hidden;">
    <div style="height: 100%; width: {{ ((gemini.total_usd / 50.0) * 100)|round(1) }}%; background: var(--accent-amber);"></div>
  </div>
</section>

<section class="panel">
  <div class="eyebrow">Cloud spend · LLM Council</div>
  <p>
    <strong class="mono">${{ "%.2f"|format(council.month_total_usd) }}</strong>
    of $40 cap · {{ council.day_count }} days with runs
  </p>
  <div style="height: 8px; background: var(--bg-recessed); border-radius: 4px; overflow: hidden;">
    <div style="height: 100%; width: {{ ((council.month_total_usd / 40.0) * 100)|round(1) }}%; background: var(--accent-blue);"></div>
  </div>
</section>

<section class="panel">
  <div class="eyebrow">Recent failures · last 5</div>
  {% set fails = recent_runs|selectattr('status', 'in', ['error', 'failed', 'capped'])|list %}
  {% if not fails %}
    <p class="subtitle">Nothing on fire. Carry on.</p>
  {% else %}
    <ul style="font-family: var(--font-mono); font-size: 11px; list-style: none; padding: 0;">
      {% for f in fails[:5] %}
        <li style="padding: 4px 0; border-top: 1px solid var(--border-subtle);">
          <strong>{{ f.agent }}</strong> · {{ f.status }} · {{ f.ts.strftime('%Y-%m-%d %H:%M') }} — {{ f.notes }}
        </li>
      {% endfor %}
    </ul>
  {% endif %}
</section>
```

- [ ] **Step 3: Wire the alerts banner into `fleet.html`**

File: `templates/fleet.html` — modify block content:

```html
{% extends "base.html" %}
{% block content %}
  {% if is_private %}
    {% include "partials/alerts_banner.html" %}
  {% endif %}
  {% include "partials/hero_regression.html" %}
  {% include "partials/kpi_row.html" %}
  {% include "partials/agent_grid.html" %}
  {% if is_private %}
    {% include "partials/below_fold_private.html" %}
  {% else %}
    {% include "partials/below_fold_public.html" %}
  {% endif %}
{% endblock %}
```

- [ ] **Step 4: Commit**

```bash
git add templates/partials/below_fold_private.html templates/partials/alerts_banner.html templates/fleet.html
git commit -m "$(cat <<'EOF'
feat: below-fold private panels + alerts banner

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

# Day 3 — Kanban, render orchestration, build entry point

## Task 21: `kanban.compose_tickets` (TDD)

Implements design doc Section 3e ticket sources.

**Files:**
- Create: `tests/test_kanban.py`
- Create: `lib/kanban.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_kanban.py`

```python
from datetime import datetime, timezone

from lib import kanban


def _data():
    return {
        "research_queue": {
            "pending": [{"title": "Substrate repricing", "assigned_agent": None}],
            "in_flight": [{"title": "FDE intake pattern", "assigned_agent": "deep_researcher"}],
            "done": [],
        },
        "lint_reports": {"latest_date": "2026-05-12", "issues_total": 2,
                         "issues_by_severity": {"HIGH": 1, "MEDIUM": 1},
                         "raw_body": "- [HIGH] broken-wikilink — `foo.md`\n- [MEDIUM] orphan — `bar.md`"},
        "eval_last_run": {"passed": 7, "total_cases": 10,
                          "cases": [
                              {"id": "case-03-cross-domain", "status": "failed"},
                              {"id": "case-05-duplicate-merge", "status": "failed"},
                              {"id": "case-01-empty-vault", "status": "passed"},
                          ]},
        "manual_tickets": {
            "todo": [{"title": "Bump synth eval suite to 12", "assigned_agent": None},
                     {"title": "Rotate ldr api token", "assigned_agent": "Sean"}],
            "in_progress": [{"title": "Substack post 2 draft", "assigned_agent": "Sean"}],
            "done": [],
        },
        "job_feed": {
            "total_postings": 4,
            "top_fit": [
                {"company": "Sierra", "title": "Agent PM", "fit_score": 91, "status": "new"},
                {"company": "Anthropic", "title": "FDE", "fit_score": 88, "status": "screen-scheduled"},
            ],
            "by_status": {"new": 1, "screen-scheduled": 1},
            "active_count": 3,
        },
    }


def test_compose_tickets_includes_all_sources_private():
    tickets = kanban.compose_tickets(_data(), include_job_feed=True)
    sources = {t["source"] for t in tickets}
    assert sources == {"research", "lint", "eval", "manual", "feed"}


def test_compose_tickets_excludes_job_feed_when_public():
    tickets = kanban.compose_tickets(_data(), include_job_feed=False)
    sources = {t["source"] for t in tickets}
    assert "feed" not in sources
    assert sources == {"research", "lint", "eval", "manual"}


def test_compose_tickets_ids_are_stable():
    t1 = kanban.compose_tickets(_data(), include_job_feed=True)
    t2 = kanban.compose_tickets(_data(), include_job_feed=True)
    ids1 = sorted(t["id"] for t in t1)
    ids2 = sorted(t["id"] for t in t2)
    assert ids1 == ids2


def test_compose_tickets_eval_failures_only():
    tickets = kanban.compose_tickets(_data(), include_job_feed=True)
    eval_tickets = [t for t in tickets if t["source"] == "eval"]
    assert len(eval_tickets) == 2
    titles = [t["title"] for t in eval_tickets]
    assert all("cross-domain" in t or "duplicate-merge" in t for t in titles)
```

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_kanban.py -v`
Expected: ModuleNotFoundError.

- [ ] **Step 3: Implement compose_tickets**

File: `lib/kanban.py`

```python
"""Kanban ticket composer + column membership rules.

Implements design doc Section 3e (sources) + 3e column rules. Tickets are
deterministic dicts; column assignment is computed after composition.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone


_LINT_LINE_RE = re.compile(r"^- \[(HIGH|MEDIUM|LOW)\]\s+(.+?)(?:\s+—\s+`(.+?)`)?\s*$")


def _stable_id(source: str, title: str) -> str:
    h = hashlib.sha1(f"{source}|{title}".encode()).hexdigest()
    return f"{source}-{h[:8]}"


def compose_tickets(data: dict, *, include_job_feed: bool) -> list[dict]:
    """Build a single list of tickets across all sources.

    Each ticket has: id, title, source, assigned_agent, column (filled by
    compute_columns), is_running (default False), created_at, moved_at, details.
    """
    out: list[dict] = []
    now = datetime.now(timezone.utc).isoformat()

    rq = data.get("research_queue", {})
    for item in rq.get("pending", []):
        out.append({
            "id": _stable_id("research", item["title"]),
            "title": item["title"], "source": "research",
            "assigned_agent": item.get("assigned_agent"),
            "_section_hint": "pending",
            "created_at": now, "moved_at": now, "details": None,
        })
    for item in rq.get("in_flight", []):
        out.append({
            "id": _stable_id("research", item["title"]),
            "title": item["title"], "source": "research",
            "assigned_agent": item.get("assigned_agent"),
            "_section_hint": "in_flight",
            "created_at": now, "moved_at": now, "details": None,
        })

    lint = data.get("lint_reports", {})
    for line in (lint.get("raw_body") or "").splitlines():
        m = _LINT_LINE_RE.match(line.strip())
        if not m:
            continue
        severity, msg, target = m.groups()
        title = f"[{severity}] {msg}" + (f" ({target})" if target else "")
        out.append({
            "id": _stable_id("lint", title),
            "title": title, "source": "lint",
            "assigned_agent": None, "_section_hint": "pending",
            "created_at": now, "moved_at": now, "details": None,
        })

    eval_run = data.get("eval_last_run", {})
    for case in eval_run.get("cases", []):
        if case.get("status") != "failed":
            continue
        title = f"Eval failing: {case['id']}"
        out.append({
            "id": _stable_id("eval", title),
            "title": title, "source": "eval",
            "assigned_agent": None, "_section_hint": "todo",
            "created_at": now, "moved_at": now, "details": None,
        })

    mt = data.get("manual_tickets", {})
    for section_name, hint in [("todo", "todo"), ("in_progress", "in_progress"), ("done", "done")]:
        for item in mt.get(section_name, []):
            out.append({
                "id": _stable_id("manual", item["title"]),
                "title": item["title"], "source": "manual",
                "assigned_agent": item.get("assigned_agent"),
                "_section_hint": hint,
                "created_at": now, "moved_at": now, "details": None,
            })

    if include_job_feed:
        for p in data.get("job_feed", {}).get("top_fit", []):
            title = f"{p['company']} · {p['title']}"
            out.append({
                "id": _stable_id("feed", title),
                "title": title, "source": "feed",
                "assigned_agent": "Sean",
                "_section_hint": p.get("status", "new"),
                "created_at": now, "moved_at": now,
                "details": f"fit {p.get('fit_score')}",
            })

    return out
```

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_kanban.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/kanban.py tests/test_kanban.py
git commit -m "$(cat <<'EOF'
feat: kanban.compose_tickets across all 5 sources + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 22: `kanban.compute_columns` + `kanban.live_pulse_flag` (TDD)

Implements design doc Section 3e column membership rules.

**Files:**
- Modify: `tests/test_kanban.py`
- Modify: `lib/kanban.py`

- [ ] **Step 1: Write failing tests**

File: `tests/test_kanban.py` — append:

```python
from datetime import timedelta


def test_compute_columns_unassigned_research_goes_backlog():
    t = {"source": "research", "assigned_agent": None, "_section_hint": "pending",
         "title": "x", "id": "x"}
    out = kanban.compute_columns([t], runs=[])
    assert out[0]["column"] == "backlog"


def test_compute_columns_assigned_research_goes_todo():
    t = {"source": "research", "assigned_agent": "deep_researcher",
         "_section_hint": "in_flight", "title": "x", "id": "x"}
    out = kanban.compute_columns([t], runs=[])
    assert out[0]["column"] == "todo"


def test_compute_columns_eval_failure_in_todo():
    t = {"source": "eval", "assigned_agent": None, "_section_hint": "todo",
         "title": "Eval failing: case-03", "id": "x"}
    out = kanban.compute_columns([t], runs=[])
    assert out[0]["column"] == "todo"


def test_compute_columns_in_progress_when_started_recently():
    now = datetime.now(timezone.utc)
    runs = [
        {"agent": "deep_researcher", "status": "started",
         "ts": now - timedelta(minutes=2), "cost_usd": 0.0,
         "duration_ms": None, "notes": "x", "mode": None, "turns": None},
    ]
    t = {"source": "research", "assigned_agent": "deep_researcher",
         "_section_hint": "in_flight", "title": "x", "id": "x"}
    out = kanban.compute_columns([t], runs=runs)
    assert out[0]["column"] == "in_progress"
    assert out[0]["is_running"] is True


def test_compute_columns_done_recent():
    t = {"source": "manual", "assigned_agent": None, "_section_hint": "done",
         "title": "x", "id": "x"}
    out = kanban.compute_columns([t], runs=[])
    assert out[0]["column"] == "done"
```

- [ ] **Step 2: Run, watch fail**

Expected: 5 AttributeError failures.

- [ ] **Step 3: Implement**

File: `lib/kanban.py` — append:

```python
RUNNING_WINDOW = timedelta(minutes=10)


def _recent_started_agents(runs: list[dict], now: datetime) -> set[str]:
    started: set[str] = set()
    completed: set[str] = set()
    for r in runs:
        if r["ts"] < now - RUNNING_WINDOW:
            continue
        if r["status"] == "started":
            started.add(r["agent"])
        elif r["status"] in ("ok", "error", "failed", "completed"):
            completed.add(r["agent"])
    return started - completed


def compute_columns(tickets: list[dict], runs: list[dict]) -> list[dict]:
    """Apply design doc Section 3e column rules to every ticket.

    Mutates each dict to add `column` and `is_running` keys; returns the list.
    """
    now = datetime.now(timezone.utc)
    running = _recent_started_agents(runs, now)
    for t in tickets:
        agent = t.get("assigned_agent")
        section = t.get("_section_hint")
        if section == "done":
            t["column"] = "done"
            t["is_running"] = False
            continue
        if agent and agent in running:
            t["column"] = "in_progress"
            t["is_running"] = True
            continue
        if section == "in_progress":
            t["column"] = "in_progress"
            t["is_running"] = False
            continue
        if section == "todo":
            t["column"] = "todo"
            t["is_running"] = False
            continue
        if agent or (t["source"] == "eval"):
            t["column"] = "todo"
            t["is_running"] = False
            continue
        t["column"] = "backlog"
        t["is_running"] = False
    return tickets
```

Note: the test fixture imports `from datetime import datetime, timezone` already; add `from datetime import timedelta` at top of the test file if not present.

- [ ] **Step 4: Run, watch pass**

Run: `.venv/bin/pytest tests/test_kanban.py -v`
Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/kanban.py tests/test_kanban.py
git commit -m "$(cat <<'EOF'
feat: kanban.compute_columns with live-pulse flagging + tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 23: Kanban page template + board partial + live-pulse CSS

Implements design doc Sections 3e + 4e.

**Files:**
- Create: `templates/kanban.html`
- Create: `templates/partials/kanban_board.html`
- Modify: `assets/styles.css` (append kanban + live-pulse rules)

- [ ] **Step 1: Append kanban CSS to `assets/styles.css`**

```css
/* Kanban */
.kanban-filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.filter-chip {
  font-family: var(--font-mono); font-size: 11px;
  padding: 4px 10px; border-radius: 999px;
  background: var(--bg-recessed); border: 1px solid var(--border-subtle);
  color: var(--text-secondary); cursor: pointer; user-select: none;
}
.filter-chip[data-active="true"] { color: var(--text-primary); border-color: currentColor; }
.filter-chip.research { color: var(--accent-purple); }
.filter-chip.lint { color: var(--accent-amber); }
.filter-chip.eval { color: var(--accent-red); }
.filter-chip.manual { color: var(--text-secondary); }
.filter-chip.feed { color: var(--accent-blue); }

.kanban-board {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.kanban-column {
  background: var(--bg-recessed);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 12px;
  min-height: 200px;
}
.kanban-column-header {
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 12px; font-family: var(--font-mono); font-size: 11px;
  color: var(--text-tertiary); text-transform: uppercase;
}
.ticket {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--text-tertiary);
  border-radius: 4px;
  padding: 8px 10px;
  margin-bottom: 8px;
  font-size: 12px;
}
.ticket[data-source="research"] { border-left-color: var(--accent-purple); }
.ticket[data-source="lint"] { border-left-color: var(--accent-amber); }
.ticket[data-source="eval"] { border-left-color: var(--accent-red); }
.ticket[data-source="manual"] { border-left-color: var(--text-secondary); }
.ticket[data-source="feed"] { border-left-color: var(--accent-blue); }
.ticket-meta { font-family: var(--font-mono); font-size: 10px; color: var(--text-tertiary); margin-top: 4px; }

/* Live pulse — design doc Section 3e */
@keyframes live-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.pulse-dot {
  display: inline-block; width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent-green); margin-right: 6px;
  animation: live-pulse 2s ease-in-out infinite;
}
.ticket.hidden { display: none; }
```

- [ ] **Step 2: Write `templates/partials/kanban_board.html`**

```html
{# Vars: tickets (list with .column / .source / .is_running), is_private (bool) #}
{% set chips = [
  ('research', 'Research'),
  ('lint', 'Lint'),
  ('eval', 'Eval'),
  ('manual', 'Manual'),
] %}
{% if is_private %}
  {% set chips = chips + [('feed', 'Job Feed')] %}
{% endif %}

<div class="kanban-filters">
  {% for src, label in chips %}
    {% set count = tickets|selectattr('source','equalto', src)|list|length %}
    <button class="filter-chip {{ src }}" data-source="{{ src }}" data-active="true">
      ● {{ label }} {{ count }}{% if src == 'feed' %} [private]{% endif %}
    </button>
  {% endfor %}
</div>

<div class="kanban-board">
  {% set columns = [
    ('backlog', 'Backlog'),
    ('todo', 'ToDo'),
    ('in_progress', 'InProgress'),
    ('testing', 'Testing'),
    ('done', 'Done'),
  ] %}
  {% for col_key, col_label in columns %}
    {% set col_tickets = tickets|selectattr('column','equalto', col_key)|list %}
    <div class="kanban-column" data-column="{{ col_key }}">
      <div class="kanban-column-header">
        <span>{{ col_label }}</span><span>{{ col_tickets|length }}</span>
      </div>
      {% for t in col_tickets %}
        <div class="ticket" data-source="{{ t.source }}" data-id="{{ t.id }}">
          {% if t.is_running %}<span class="pulse-dot"></span>{% endif %}
          {{ t.title }}
          <div class="ticket-meta">
            {{ t.source }}
            {% if t.assigned_agent %} · @{{ t.assigned_agent }}{% endif %}
            {% if t.details %} · {{ t.details }}{% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
  {% endfor %}
</div>
```

- [ ] **Step 3: Write `templates/kanban.html`**

```html
{% extends "base.html" %}
{% block content %}
  {% include "partials/kanban_board.html" %}
{% endblock %}
{% block scripts %}
  <script src="assets/kanban-filter.js"></script>
{% endblock %}
```

- [ ] **Step 4: Commit**

```bash
git add templates/kanban.html templates/partials/kanban_board.html assets/styles.css
git commit -m "$(cat <<'EOF'
feat: kanban board template + live-pulse CSS

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 24: `assets/kanban-filter.js` — filter chip toggle

**Files:**
- Create: `assets/kanban-filter.js`

- [ ] **Step 1: Write the JS file**

```javascript
// Filter chip toggle for the kanban board. Vanilla JS, no framework.
(function () {
  'use strict';
  function init() {
    var chips = document.querySelectorAll('.filter-chip');
    var tickets = document.querySelectorAll('.ticket');
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var nowActive = chip.getAttribute('data-active') !== 'true';
        chip.setAttribute('data-active', nowActive ? 'true' : 'false');
        applyFilter();
      });
    });

    function applyFilter() {
      var enabled = {};
      chips.forEach(function (c) {
        enabled[c.getAttribute('data-source')] = c.getAttribute('data-active') === 'true';
      });
      tickets.forEach(function (t) {
        var src = t.getAttribute('data-source');
        if (enabled[src] === false) {
          t.classList.add('hidden');
        } else {
          t.classList.remove('hidden');
        }
      });
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

- [ ] **Step 2: Commit**

```bash
git add assets/kanban-filter.js
git commit -m "$(cat <<'EOF'
feat: kanban filter chip vanilla JS toggle

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 25: `lib/render.py` — public + private renderers + smoke tests

**Files:**
- Create: `tests/test_render_smoke.py`
- Create: `lib/render.py`

- [ ] **Step 1: Write the smoke tests**

File: `tests/test_render_smoke.py`

```python
import json
from datetime import date, datetime, timezone
from pathlib import Path

from lib import aggregations, kanban, render, readers

from .conftest import FIXTURES


def _data():
    return {
        "agent_runs": readers.read_run_history(FIXTURES / "sample-run-history.csv"),
        "synth_manifests": readers.read_synth_manifests(FIXTURES),
        "gemini_spend": readers.read_gemini_spend(FIXTURES / "sample-gemini-spend.json"),
        "council_spend": {"month_total_usd": 0.41, "day_count": 1, "days": []},
        "lint_reports": readers.read_lint_reports(FIXTURES),
        "eval_last_run": readers.read_eval_last_run(FIXTURES / "sample-eval-last-run.md"),
        "job_feed_db": {"total_postings": 4, "by_status": {"new": 1}, "top_fit": [], "active_count": 3},
        "job_feed_manifests": {"latest": None, "last_7": []},
        "research_queue": readers.read_research_queue(FIXTURES / "sample-research-queue.md"),
        "manual_tickets": readers.read_manual_tickets(FIXTURES / "sample-tickets.md"),
        "agent_names": [
            "vault_indexer", "vault_synthesizer", "deep_researcher", "meta_agent",
            "daily_driver", "knowledge_lint", "flush", "job_feed",
        ],
    }


def test_render_public_emits_html_and_data_json(tmp_path):
    data = _data()
    agg = aggregations.compute_all(data, end=date(2026, 5, 14))
    tickets = kanban.compose_tickets({**data, "lint_reports": {**data["lint_reports"], "raw_body": ""},
                                       "eval_last_run": data["eval_last_run"]}, include_job_feed=False)
    tickets = kanban.compute_columns(tickets, data["agent_runs"])
    render.render_public(agg, tickets, tmp_path)
    fleet = (tmp_path / "index.html").read_text()
    kb = (tmp_path / "kanban.html").read_text()
    sidecar = json.loads((tmp_path / "data.json").read_text())
    assert "Agent Fleet Observability" in fleet
    assert "Job Feed" not in kb  # public kanban has 4 chips, not 5
    assert sidecar["tickets"]
    # privacy boundary smoke check
    assert "vault/.job-feed" not in fleet
    assert "vault/20_projects" not in fleet


def test_render_private_includes_job_feed_lane(tmp_path):
    data = _data()
    agg = aggregations.compute_all(data, end=date(2026, 5, 14))
    tickets = kanban.compose_tickets({**data, "lint_reports": {**data["lint_reports"], "raw_body": ""}},
                                      include_job_feed=True)
    tickets = kanban.compute_columns(tickets, data["agent_runs"])
    render.render_private(agg, tickets, tmp_path)
    kb = (tmp_path / "kanban.html").read_text()
    assert "Job Feed" in kb
    assert (tmp_path / "data.json").exists()
```

- [ ] **Step 2: Run, watch fail**

Run: `.venv/bin/pytest tests/test_render_smoke.py -v`
Expected: ModuleNotFoundError on `lib.render`.

- [ ] **Step 3: Implement `lib/render.py`**

File: `lib/render.py`

```python
"""Render orchestrators for public + private dashboard passes."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from lib import anonymize, svg_charts


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "templates"


_ENV = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


_MODEL_MIX_COLORS = {
    "local-qwen": svg_charts.TEAL,
    "local-nomic": svg_charts.GREEN,
    "local-other": svg_charts.AMBER,
    "local": svg_charts.GREEN,
    "cloud-anthropic": svg_charts.BLUE,
    "cloud-gemini": svg_charts.PURPLE,
    "cloud": svg_charts.RED,
}


def _build_charts(agg: dict) -> dict:
    hero_series = [
        {"date": s["date"], "value": s["concepts"]}
        for s in agg["synth_series_60d"]
    ]
    rw = agg["regression_window"]
    annotation = None
    if rw["start"] and rw["nights"] >= 3:
        annotation = {
            "start_date": rw["start"], "end_date": rw["end"],
            "label": f"{rw['nights']}-DAY SILENT REGRESSION",
        }
    hero_svg = svg_charts.line_chart(hero_series, width=1100, height=240, annotation=annotation)

    eval_spark_svg = svg_charts.sparkline(agg["eval_sparkline"], width=80, height=18)

    cost = agg["cost_trend_30d"]
    cost_svg = svg_charts.stacked_area(cost["days"], cost["series"], width=1100, height=180)

    mix_segments = [
        {"label": label, "value": v["count"], "pct": v["pct"],
         "color": _MODEL_MIX_COLORS.get(label, svg_charts.AMBER)}
        for label, v in agg["model_mix"].items()
    ]
    model_mix_svg = svg_charts.donut(mix_segments, size=120)

    synth_series = [
        {"date": s["date"], "value": s["concepts"]} for s in agg["synth_series_60d"]
    ]
    synth_60d_svg = svg_charts.line_chart(synth_series, width=1100, height=180,
                                          color=svg_charts.GREEN)

    return {
        "hero_svg": hero_svg,
        "eval_sparkline_svg": eval_spark_svg,
        "cost_trend_svg": cost_svg,
        "model_mix_svg": model_mix_svg,
        "model_mix_segments": mix_segments,
        "synth_60d_svg": synth_60d_svg,
    }


def _common_context(agg: dict, *, is_private: bool, snapshot_ts: str | None = None) -> dict:
    ts = snapshot_ts or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    healthy = sum(1 for t in agg["fleet_status"] if t["health"] == "healthy")
    total = len(agg["fleet_status"])
    fleet_health_label = f"{healthy}/{total} HEALTHY"
    extra_pills: list[str] = []
    if is_private:
        active = agg.get("job_feed", {}).get("active_count", 0)
        if active:
            extra_pills.append(f"HUNT · {active} ACTIVE")
    return {
        "snapshot_ts": ts,
        "is_private": is_private,
        "active_route": "fleet",
        "fleet_health_label": fleet_health_label,
        "extra_pills": extra_pills,
        "kpis": agg["kpis"],
        "fleet_status": agg["fleet_status"],
        "regression_window": agg["regression_window"],
        "end_date": agg["end_date"],
        "recent_runs": agg["recent_runs"],
        "eval_cases": agg["eval"].get("cases", []),
        "gemini": agg["gemini"],
        "council": agg["council"],
        "job_feed": agg["job_feed"],
        "alerts": _build_alerts(agg, is_private),
        **_build_charts(agg),
    }


def _build_alerts(agg: dict, is_private: bool) -> list[dict]:
    if not is_private:
        return []
    alerts: list[dict] = []
    if agg["gemini"]["total_usd"] > 35:
        alerts.append({"severity": "degraded",
                       "message": f"Gemini DR ${agg['gemini']['total_usd']:.2f} / $50 cap (>70% used)",
                       "ts": "now"})
    if agg["eval"].get("passed", 10) < 6:
        alerts.append({"severity": "down",
                       "message": f"Eval pass dropped to {agg['eval']['passed']}/{agg['eval']['total_cases']}",
                       "ts": "today"})
    return alerts


def render_public(agg: dict, tickets: list[dict], out_dir: Path) -> None:
    pub_agg = anonymize.public_pass(agg)
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = _common_context(pub_agg, is_private=False)

    fleet_html = _ENV.get_template("fleet.html").render(
        page_title="Agent Fleet Observability", **ctx)
    (out_dir / "index.html").write_text(fleet_html)

    ctx_k = {**ctx, "active_route": "kanban", "tickets": tickets}
    kb_html = _ENV.get_template("kanban.html").render(
        page_title="Agent Fleet · Kanban", **ctx_k)
    (out_dir / "kanban.html").write_text(kb_html)

    (out_dir / "data.json").write_text(json.dumps({
        "tickets": tickets,
        "snapshot_ts": ctx["snapshot_ts"],
    }, default=str, indent=2))


def render_private(agg: dict, tickets: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = _common_context(agg, is_private=True)

    fleet_html = _ENV.get_template("fleet.html").render(
        page_title="Agent Fleet Observability · Private", **ctx)
    (out_dir / "index.html").write_text(fleet_html)

    ctx_k = {**ctx, "active_route": "kanban", "tickets": tickets}
    kb_html = _ENV.get_template("kanban.html").render(
        page_title="Agent Fleet · Kanban · Private", **ctx_k)
    (out_dir / "kanban.html").write_text(kb_html)

    (out_dir / "data.json").write_text(json.dumps({
        "tickets": tickets,
        "snapshot_ts": ctx["snapshot_ts"],
    }, default=str, indent=2))
```

- [ ] **Step 4: Run smoke tests, watch pass**

Run: `.venv/bin/pytest tests/test_render_smoke.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add lib/render.py tests/test_render_smoke.py
git commit -m "$(cat <<'EOF'
feat: render.py public + private orchestrators + smoke tests

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 26: `build.py` — end-to-end build entry point

Implements design doc Section 6b.

**Files:**
- Create: `build.py`

- [ ] **Step 1: Write `build.py`**

File: `~/Code/agent-fleet-observability/build.py`

```python
#!/usr/bin/env python3
"""Agent Fleet Observability Dashboard — build script.

Runs on Mac Mini cron at 06:00 ET daily. Reads vault data, emits public
index.html / kanban.html / data.json (committed + pushed) plus a private
mirror under ~/Sites/agent-fleet-private/ (gitignored).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from lib import aggregations, kanban, readers, render


VAULT = Path.home() / "Code-Brain/code-brain/vault"
EVALS = Path.home() / "Code-Brain/code-brain/evals"
PRIVATE_OUT = Path.home() / "Sites/agent-fleet-private"
REPO = Path(__file__).resolve().parent

AGENT_NAMES = [
    "vault_indexer", "vault_synthesizer", "deep_researcher", "meta_agent",
    "daily_driver", "knowledge_lint", "flush", "job_feed",
]


def _load(month_yyyy_mm: str) -> dict:
    return {
        "agent_runs": readers.read_run_history(VAULT / "90_system/agent-logs/agent-run-history.csv"),
        "synth_manifests": readers.read_synth_manifests(VAULT / "health"),
        "gemini_spend": readers.read_gemini_spend(VAULT / f"health/gemini-spend-{month_yyyy_mm}.json"),
        "council_spend": readers.read_council_spend(VAULT / "health"),
        "lint_reports": readers.read_lint_reports(VAULT / "health"),
        "eval_last_run": readers.read_eval_last_run(EVALS / "vault-synthesizer/last-run.md"),
        "job_feed_db": readers.read_job_feed_db(VAULT / ".job-feed.db"),
        "job_feed_manifests": readers.read_job_feed_manifests(VAULT / "health"),
        "research_queue": readers.read_research_queue(VAULT / "00_inbox/research-queue.md"),
        "manual_tickets": readers.read_manual_tickets(VAULT / "00_inbox/tickets.md"),
        "agent_names": AGENT_NAMES,
    }


def _has_public_changes() -> bool:
    res = subprocess.run(
        ["git", "-C", str(REPO), "status", "--porcelain", "index.html", "kanban.html", "data.json"],
        capture_output=True, text=True, check=True)
    return bool(res.stdout.strip())


def _commit_and_push() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    subprocess.run(["git", "-C", str(REPO), "add", "index.html", "kanban.html", "data.json"], check=True)
    subprocess.run(["git", "-C", str(REPO), "commit", "-m", f"snapshot {ts}"], check=True)
    subprocess.run(["git", "-C", str(REPO), "push"], check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-push", action="store_true",
                    help="Build artifacts but skip git commit/push")
    ap.add_argument("--private-only", action="store_true",
                    help="Render only the private surface (skip public)")
    args = ap.parse_args()

    month = datetime.now(timezone.utc).strftime("%Y-%m")
    try:
        data = _load(month)
    except Exception as exc:
        print(f"[build] aborting: vault read failed: {exc}", file=sys.stderr)
        return 1

    agg = aggregations.compute_all(data)

    public_tickets = kanban.compose_tickets(data, include_job_feed=False)
    public_tickets = kanban.compute_columns(public_tickets, data["agent_runs"])
    private_tickets = kanban.compose_tickets(data, include_job_feed=True)
    private_tickets = kanban.compute_columns(private_tickets, data["agent_runs"])

    if not args.private_only:
        render.render_public(agg, public_tickets, REPO)
    render.render_private(agg, private_tickets, PRIVATE_OUT)

    if args.private_only or args.no_push:
        print("[build] done (no push)")
        return 0

    if not _has_public_changes():
        print("[build] no public changes — skipping commit")
        return 0

    _commit_and_push()
    print("[build] pushed snapshot")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke test against live data with `--no-push --private-only`**

```bash
cd ~/Code/agent-fleet-observability
.venv/bin/python build.py --no-push --private-only
```

Expected: prints `[build] done (no push)`. Then verify the private file:

```bash
ls -lh ~/Sites/agent-fleet-private/
```

Should show `index.html`, `kanban.html`, `data.json`.

- [ ] **Step 3: Sanity-check page weight on the private artifact**

```bash
wc -c ~/Sites/agent-fleet-private/index.html ~/Sites/agent-fleet-private/kanban.html
```

Expected: index.html should fit budget (< ~200KB with data baked in). Flag if either exceeds 250KB.

- [ ] **Step 4: Run the full smoke test against the real vault, no push**

```bash
cd ~/Code/agent-fleet-observability
.venv/bin/python build.py --no-push
```

Expected: `[build] done (no push)`. Open `~/Code/agent-fleet-observability/index.html` in Chrome (drag-drop) and eyeball every panel.

- [ ] **Step 5: Commit**

```bash
git add build.py
git commit -m "$(cat <<'EOF'
feat: build.py entry point — reads vault, renders public + private

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

# Day 4 — Mobile, Vercel + Cloudflare, launchd, README, validation

## Task 27: Mobile responsive pass (375px floor)

Implements design doc Section 8.

**Files:**
- Modify: `assets/styles.css` (append breakpoints)

- [ ] **Step 1: Append responsive rules to `assets/styles.css`**

```css
/* Mobile + responsive — design doc Section 8 */
@media (max-width: 1023px) {
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
  .agent-grid { grid-template-columns: repeat(2, 1fr); }
  .kanban-board { grid-template-columns: 1fr; gap: 16px; }
  .topbar { flex-wrap: wrap; }
}
@media (max-width: 767px) {
  .priv-wrap { padding: 16px 12px; }
  .kpi-value { font-size: 22px; }
  .topbar { gap: 8px; }
  .nav-link { font-size: 10px; padding: 2px 6px; }
}
@media (max-width: 479px) {
  .kpi-row { grid-template-columns: 1fr; }
  .agent-grid { grid-template-columns: 1fr; }
  .wordmark { font-size: 14px; }
  .subtitle { font-size: 10px; }
  table { font-size: 10px; }
}

/* Hero SVG fluid */
.panel svg { max-width: 100%; height: auto; }
```

- [ ] **Step 2: Verify at 375px**

Open `~/Code/agent-fleet-observability/index.html` in Chrome. DevTools → Toggle Device Toolbar → Set width 375px. Walk every panel top to bottom; nothing should clip or horizontal-scroll. Repeat for `kanban.html`.

If clipping found: tighten that specific selector and re-verify.

- [ ] **Step 3: Take iPhone-shaped screenshot for Substack hero**

Manual: take a 375 × ~2400 screenshot of `index.html` for the Substack post 2 hero. Save to `~/Code/agent-fleet-observability/docs/screenshots/2026-05-XX-fleet-mobile.png` (create the dir if missing). Not committed; just for reference.

- [ ] **Step 4: Commit**

```bash
git add assets/styles.css
git commit -m "$(cat <<'EOF'
polish: mobile responsive breakpoints (1023/767/479px) + fluid SVG

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 28: Vercel deploy + `vercel.json`

Implements design doc Section 2d.

**Files:**
- Create: `vercel.json`

- [ ] **Step 1: Write `vercel.json`**

```json
{
  "version": 2,
  "public": true,
  "cleanUrls": true,
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=86400, immutable" }
      ]
    },
    {
      "source": "/(index|kanban).html",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=300, s-maxage=600" }
      ]
    }
  ]
}
```

- [ ] **Step 2: Install Vercel CLI if missing + log in**

```bash
which vercel || npm i -g vercel
vercel login
```

Expected: Email login flow completes.

- [ ] **Step 3: Link the project**

```bash
cd ~/Code/agent-fleet-observability
vercel link
```

Pick: scope = personal Sean account; project = create new, name `agent-fleet-observability`. Confirm. This writes `.vercel/` (gitignored — verify `.vercel` is in `.gitignore`; add it if missing).

- [ ] **Step 4: Add `.vercel/` to `.gitignore` if not present**

Verify:

```bash
grep -q "^\.vercel" .gitignore || echo ".vercel/" >> .gitignore
```

- [ ] **Step 5: Deploy preview**

```bash
cd ~/Code/agent-fleet-observability
vercel deploy
```

Expected: preview URL like `agent-fleet-observability-<hash>-seanwinslow28.vercel.app`. Open it. Confirm fleet + kanban load.

- [ ] **Step 6: Deploy production**

```bash
vercel deploy --prod
```

Expected: production URL like `agent-fleet-observability.vercel.app`. Confirm it loads.

- [ ] **Step 7: Commit**

```bash
git add vercel.json .gitignore
git commit -m "$(cat <<'EOF'
feat: vercel.json — static deploy config with cache headers

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push
```

Expected: GitHub push triggers Vercel auto-deploy.

---

## Task 29: Cloudflare CNAME for `fleet.seanwinslow.com`

Implements design doc Section 2d. DNS-only (gray cloud) — Vercel terminates SSL.

**Files:** None in repo. Manual config in Vercel dashboard + Cloudflare dashboard.

- [ ] **Step 1: Add custom domain in Vercel**

In the Vercel dashboard for `agent-fleet-observability` project → Settings → Domains → Add `fleet.seanwinslow.com`. Vercel will give a CNAME target (something like `cname.vercel-dns.com`). Copy this value.

- [ ] **Step 2: Add CNAME record in Cloudflare**

Open Cloudflare dashboard → seanwinslow.com → DNS → Records → Add record:
- Type: `CNAME`
- Name: `fleet`
- Target: paste the CNAME target from Vercel
- Proxy status: **DNS only (gray cloud)** — critical; Vercel must see the request to terminate SSL
- TTL: Auto

Save.

- [ ] **Step 3: Verify DNS resolves**

```bash
dig fleet.seanwinslow.com +short
```

Expected: returns Vercel's CNAME target (may take 1-5 minutes to propagate).

- [ ] **Step 4: Verify Vercel issues a certificate**

Back in Vercel dashboard → Domains. Wait for the `fleet.seanwinslow.com` row to show "Valid Configuration" + SSL active. May take a few minutes.

- [ ] **Step 5: Smoke test the live URL**

```bash
curl -sIL https://fleet.seanwinslow.com | head -20
```

Expected: HTTP/2 200, content-type text/html, cache headers present.

Open `https://fleet.seanwinslow.com` in Chrome. Confirm fleet + kanban routes both load.

- [ ] **Step 6: Note this step is manual — no commit**

---

## Task 30: launchd plist + cron at 06:00 ET daily

Implements design doc Section 6c.

**Files:**
- Create: `~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist` (outside repo)
- Create: `schedules/com.sean.agent-fleet-dashboard.plist` (template — committed for reference)

- [ ] **Step 1: Write the plist template into the repo for reference**

File: `~/Code/agent-fleet-observability/schedules/com.sean.agent-fleet-dashboard.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.sean.agent-fleet-dashboard</string>
  <key>WorkingDirectory</key>
  <string>/Users/seanwinslow/Code/agent-fleet-observability</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/seanwinslow/Code/agent-fleet-observability/.venv/bin/python</string>
    <string>/Users/seanwinslow/Code/agent-fleet-observability/build.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>6</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/Users/seanwinslow/Code/agent-fleet-observability/logs/build.out.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/seanwinslow/Code/agent-fleet-observability/logs/build.err.log</string>
</dict>
</plist>
```

- [ ] **Step 2: Make log dir + add to gitignore**

```bash
cd ~/Code/agent-fleet-observability
mkdir -p logs
echo "logs/" >> .gitignore
```

- [ ] **Step 3: Copy plist to LaunchAgents + load**

```bash
cp ~/Code/agent-fleet-observability/schedules/com.sean.agent-fleet-dashboard.plist \
   ~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist
launchctl load ~/Library/LaunchAgents/com.sean.agent-fleet-dashboard.plist
launchctl list | grep agent-fleet
```

Expected: `agent-fleet-dashboard` appears with a status (PID or `-`).

- [ ] **Step 4: Test-fire the cron manually**

```bash
launchctl start com.sean.agent-fleet-dashboard
sleep 30
tail -20 ~/Code/agent-fleet-observability/logs/build.out.log
tail -20 ~/Code/agent-fleet-observability/logs/build.err.log
```

Expected: `[build] pushed snapshot` (or `no public changes`) in `build.out.log`; `build.err.log` empty.

- [ ] **Step 5: Verify Vercel auto-deployed**

```bash
curl -sI https://fleet.seanwinslow.com | grep -i last-modified
```

Should be recent.

- [ ] **Step 6: Commit the plist template**

```bash
cd ~/Code/agent-fleet-observability
git add schedules/com.sean.agent-fleet-dashboard.plist .gitignore
git commit -m "$(cat <<'EOF'
chore: launchd plist template for 06:00 ET daily cron

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push
```

---

## Task 31: `README.md` — 4Q recruiter-friendly format

Implements design doc Section 9 criterion #7.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite the README in 4Q format**

File: `~/Code/agent-fleet-observability/README.md`

```markdown
# Agent Fleet Observability

[![dashboard](https://img.shields.io/badge/dashboard-fleet.seanwinslow.com-c084fc)](https://fleet.seanwinslow.com)

Static observability dashboard for an 8-agent local-first AI fleet.
Builds nightly on a Mac Mini. $0 cloud, 99% local-first inference.

> **The story:** for nine consecutive nights, my vault synthesizer wrote zero
> concepts. A 10-case eval suite caught it on day ten. This dashboard preserves
> the incident timeline + the recovery as proof of operational maturity.

---

## 1 · What problem this solves

Eight cron-scheduled AI agents (vault indexer, synthesizer, deep researcher,
meta-agent, daily driver, knowledge lint, flush, job feed) generate ~30 runs/day
across local + cloud models. Without a single surface, you trust-fall every
night: did the synthesizer run, did the eval pass, did the Gemini budget hold?

This dashboard makes the fleet inspectable in 30 seconds: which agents are
healthy, what was last night's eval score, what's the 30-day spend pattern,
which tickets are mid-flight on the kanban board.

## 2 · How it works

```
Mac Mini cron (06:00 ET)
        │
        ├──▶ Read vault data (CSV + JSON + SQLite + Markdown)
        ├──▶ Aggregate (KPIs, sparklines, regression window, model mix)
        └──▶ Render two passes:
              ├─ public  → repo root → git push → Vercel auto-deploy
              └─ private → ~/Sites/agent-fleet-private/ (gitignored)
```

- **Backend:** Python 3.12 stdlib, no framework, ~600 lines including tests.
- **Frontend:** Jinja2 templates, inline SVG charts, ~10 KB stylesheet.
- **Auth:** none. Public read-only. Privacy is structural — the public render
  pass never reads `vault/.job-feed.db`, period.
- **Hosting:** Vercel static deploy + Cloudflare DNS-only CNAME.

## 3 · What's notable

- **Privacy boundary is structural, not policy.** Job-hunt data physically
  cannot leak — the data source is skipped on public render, the output paths
  are separate directories, and one is gitignored at the home level.
- **Honest empty states.** Every panel renders "what actually happened"
  copy when data is missing — no spinners-that-never-resolve, no mock data.
- **Regression as hero.** The 9-day silent regression is the central visual,
  not a buried annotation. Operational maturity is recovered failures.
- **All telemetry traces to a verifiable file.** Every number on the page
  has a CSV row, JSON record, SQLite row, or Markdown file behind it.

## 4 · How to read this code

- [`build.py`](build.py) — orchestrator (read → aggregate → render).
- [`lib/readers.py`](lib/readers.py) — all data source loaders.
- [`lib/aggregations.py`](lib/aggregations.py) — KPI + regression window compute.
- [`lib/anonymize.py`](lib/anonymize.py) — public-pass stripping rules.
- [`lib/kanban.py`](lib/kanban.py) — ticket composer + column membership.
- [`lib/render.py`](lib/render.py) — public + private render orchestrators.
- [`tests/`](tests/) — pytest suite (≈30 tests; `make test` to run).

### Local dev

```bash
git clone https://github.com/seanwinslow28/agent-fleet-observability
cd agent-fleet-observability
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
make test    # run the pytest suite
make build   # render against your vault (paths in build.py)
```

---

Built by [Sean Winslow](https://github.com/seanwinslow28) · 2026 · MIT
```

- [ ] **Step 2: Commit + push**

```bash
git add README.md
git commit -m "$(cat <<'EOF'
docs: 4Q recruiter-friendly README

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push
```

---

## Task 32: Validate every success criterion in design doc Section 9

Walk every line of Section 9 and confirm or fix. This is the v1 acceptance gate.

**Files:** None modified unless a criterion fails.

- [ ] **Step 1: Run full pytest suite**

```bash
cd ~/Code/agent-fleet-observability
make test
```

Expected: ~30+ passed. Any failure: fix before continuing.

- [ ] **Step 2: Page-weight check (criterion #1)**

```bash
wc -c index.html kanban.html
```

Note: with data baked in, design doc gives a generous < 200 KB budget. Each file should be well under. The < 50 KB "pre-data" target is structural — if data alone pushes past 200 KB, log the over-budget warning per design Section 6d.

- [ ] **Step 3: Cold-cache load time (criterion #2)**

Open `https://fleet.seanwinslow.com` in Chrome incognito → DevTools → Network → disable cache → reload. `DOMContentLoaded` < 2s.

- [ ] **Step 4: All 8 agent tiles show real data (criterion #3)**

Eyeball each tile. Cross-check timestamps with:

```bash
tail -50 ~/Code-Brain/code-brain/vault/90_system/agent-logs/agent-run-history.csv
```

- [ ] **Step 5: Regression visible + annotated (criterion #4)**

Confirm the hero chart shows a flatline window in early May with the red dashed band + "N-DAY SILENT REGRESSION" callout.

- [ ] **Step 6: Mobile 375px survives (criterion #5)**

DevTools → 375px. Walk every panel. No clipping.

- [ ] **Step 7: 30-sec recruiter cold-open test (criterion #6)**

Send the URL to 2 outside readers (not PMs). Ask: "tell me what you see in 30 seconds." Note their answers — they should land on "agent fleet, caught a regression, has costs". If they don't, the hero copy needs another pass.

- [ ] **Step 8: README readability (criterion #7)**

Manual: open the rendered README on GitHub, time how long it takes to skim. Target < 90 sec.

- [ ] **Step 9: 60-sec Loom recording (criterion #8)**

Record a Loom walking through: hero → KPI row → agent grid → kanban → footer. Drop the URL in `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/distribution-assets.md` under a new "Agent Fleet Dashboard" section.

- [ ] **Step 10: Substack post 2 hero screenshot (criterion #9)**

Capture a 375 × 2400 screenshot of `fleet.seanwinslow.com` on iPhone-size. Stage it for Substack post 2.

- [ ] **Step 11: Recruiter attribution slot (criterion #10)**

Manual — add an `## Agent Fleet Dashboard mentions` heading to `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/target-companies.md`. Empty for now; track as engagement happens.

- [ ] **Step 12: Privacy boundary holds (criterion #11)**

```bash
cd ~/Code/agent-fleet-observability
grep -i -E "(target-30|warm.intro|job.feed.db|application.velocity|vault/\.job-feed)" index.html kanban.html data.json
```

Expected: no matches. Repeat on the live URL:

```bash
curl -s https://fleet.seanwinslow.com | grep -i -E "(target-30|warm.intro|job.feed.db|application.velocity)"
```

Expected: no matches.

- [ ] **Step 13: Mascot renders across browsers (criterion #12)**

Open `https://fleet.seanwinslow.com` in Chrome, Safari, Firefox. Mascot spins + blinks in each.

- [ ] **Step 14: Build < 60 sec (criterion #13)**

```bash
cd ~/Code/agent-fleet-observability
time .venv/bin/python build.py --no-push
```

Expected: real time < 30 sec (cron-fire-to-live needs Vercel deploy ~30 sec on top — total < 60 sec).

- [ ] **Step 15: Kanban shows at least 1 ticket per source type (criterion #14)**

Open `/kanban`. Confirm each chip count is > 0 on the private surface; > 0 on at least 3 of 4 chips on the public surface. If lint or eval are empty, populate fixtures by inducing a failing eval case or running knowledge_lint manually.

- [ ] **Step 16: Reduced-motion disables mascot animation (criterion #15)**

macOS System Settings → Accessibility → Display → Reduce Motion ON. Reload the dashboard. Mascot should freeze (no spin, no blink). Toggle back off.

- [ ] **Step 17: Lock the spec**

Once all 15 criteria pass, edit `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-15-agent-fleet-dashboard-design.md` frontmatter:

```yaml
status: shipped
shipped_at: 2026-05-XX
```

And in the unified roadmap, flip Task 11 to `done`.

- [ ] **Step 18: Final commit**

```bash
cd ~/Code/agent-fleet-observability
git tag -a v1.0.0 -m "v1.0.0 — initial ship"
git push --tags
```

---

# Plan Self-Review

I ran the spec-coverage / placeholder / type-consistency check from the writing-plans skill against the locked design doc. Findings:

**Section coverage (design doc § → plan task):**

| Design § | Topic | Plan task(s) |
|---|---|---|
| 1 | Decision summary | All tasks; locked decisions threaded through |
| 2a | Two render modes / one pipeline | Tasks 25 + 26 |
| 2b | Data sources (10 paths) | Tasks 3-8 |
| 2c | Privacy boundary | Tasks 12 + 25 + 32 step 12 |
| 2d | Distribution (Vercel + Cloudflare) | Tasks 28 + 29 |
| 3a | Routes | Task 18 + 23 + 25 |
| 3b | Top bar | Task 16 |
| 3c | `/fleet` above the fold (hero + KPI + grid) | Tasks 13, 17, 18 |
| 3d | `/fleet` below fold (public) | Tasks 14 + 19 |
| 3e | Kanban v1 read-only | Tasks 21, 22, 23, 24 |
| 3f | Public anonymization rules | Task 12 |
| 3g | Footer | Task 16 |
| 4a-4f | Private artifact | Tasks 20 + 25 |
| 5a-5c | Visual personality + palette + typography | Task 15 |
| 5d | Asterisk Spark mascot | Task 16 |
| 5e | Microcopy voice | Embedded in templates (Tasks 19 + 20) |
| 5f | Footer copy | Task 16 |
| 6a | Repo layout | Tasks 1-2, file structure section |
| 6b | build.py pseudocode | Task 26 |
| 6c | launchd schedule | Task 30 |
| 6d | Performance budget | Task 32 steps 2 + 14 |
| 6e | Failure handling | Task 26 (try/except + private-only fallback) + 32 |
| 7 | Kanban v1 spec | Tasks 21-24 |
| 8 | Mobile + responsive | Task 27 |
| 9 | Success criteria | Task 32 (all 15) |
| 10 | Anti-patterns | Honored throughout — no nested spans (no waterfall), no auth, no live polling, no >7 chart colors |
| 11 | v2 / future work | Out of scope per memory |
| 13 | 4-day schedule + cost | Day 1 / 2 / 3 / 4 task grouping |
| 14 | Tier-A compliance | Implicit — build fits 8:30–5:30 container |

**Placeholder scan:** No "TBD", "TODO", "fill in later". Two explicit data-gap acknowledgments (Pre-build assumption #3, Task 20 note) describe what falls back to empty-state copy rather than leaving the plan ambiguous.

**Type-consistency check:**
- `compute_fleet_status(runs, agent_names)` — same signature used by Task 9 + 11 + 26 ✓
- `compute_columns(tickets, runs)` — same signature in Task 22 + 26 ✓
- `compose_tickets(data, *, include_job_feed)` — kwarg-only flag, same usage in Task 21 + 26 ✓
- `render_public(agg, tickets, out_dir)` / `render_private(...)` — same 3-arg shape in Task 25 + 26 ✓
- `public_pass(agg)` returns a deep copy with same shape ✓
- SVG helpers (`line_chart`, `sparkline`, `donut`, `stacked_area`) — argument signatures consistent between Tasks 13/14 and Task 25 ✓

**Anti-pattern compliance with design doc Section 10:**
- ✅ No real-time polling (build is daily cron, static snapshot)
- ✅ No login / auth
- ✅ No mocked data labeled as real (fixtures are explicitly fixtures; live data is live)
- ✅ ≤ 7 colors used per chart
- ✅ No carousel / auto-rotating hero
- ✅ Every agent tile is a real agent (8 named from CLAUDE.md)
- ✅ Job-hunt data is structurally invisible on public (Task 12 + Task 25 separate output dirs)
- ✅ Recovered failures are surfaced (regression hero + recent failures panel)
- ✅ **No nested-session-span / waterfall** — explicit rejection honored
- ✅ Cloudflare DNS-only (gray cloud) — Task 29 step 2 enforces it

No gaps found.

---

**Status:** Plan complete and saved. Awaiting Sean's review before any code is written.

