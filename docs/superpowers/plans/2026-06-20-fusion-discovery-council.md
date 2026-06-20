# fusion-discovery-council — Phase 1 (Core Vertical Slice) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working `fusion-discovery-council <topic> --lens pm --tier quick|standard` skill end-to-end: gather fresh evidence (last30days + Sonar + web), fuse it through an OpenRouter Fusion panel, drop any pain point that can't be traced to a real fetched URL, and emit a ranked, evidence-linked idea ledger.

**Architecture:** A new `discovery/` subpackage co-located inside `tools/llm-council/` so it directly reuses the council's `client.py` (OpenRouter HTTP + retry) and `budget.py` (caps + spend). A 4-stage pipeline — GATHER (deterministic collectors → evidence bundle of real URLs) → FUSE (one Fusion API call, panel + judge) → VERIFY (fabrication gate) → FRAME (pm lens → idea ledger). Co-location is deliberate: it shares the budget/spend spine without a second package or duplicated HTTP code.

**Tech Stack:** Python ≥3.10, `httpx` (async, already a council dep), `click` (CLI), `pydantic`/dataclasses, `pytest` + `pytest-asyncio` + `pytest-httpx`. OpenRouter Fusion server tool. last30days Python script (shell-out). Spec: [docs/superpowers/specs/2026-06-20-fusion-discovery-council-design.md](../specs/2026-06-20-fusion-discovery-council-design.md).

## Global Constraints

- Python `requires-python = ">=3.10"` (matches `tools/llm-council/pyproject.toml`; do not raise the floor).
- Run all commands from `tools/llm-council/`. Tests: `uv run pytest tests/discovery/ -v`.
- Reuse `council.client.OpenRouterClient` and `council.budget` — do NOT add a second HTTP client or a second spend file.
- Spend file is shared: `vault/health/council-spend-{YYYY-MM-DD}.json` (override via `COUNCIL_SPEND_DIR`). Discovery runs are tagged `tool="discovery"`; discovery caps are **$10/day, $50/month**, enforced independently of council's own caps by filtering spend records on `tool`.
- Per-run cost caps: `quick` $0.50, `standard` $1.50, `deep` $4.00. `deep` confirms cost before running.
- **Fabrication gate is non-negotiable:** every pain point in the ledger must trace to ≥1 quote whose URL exists in the evidence bundle. Untraceable → dropped or marked `unverified`. No silent softening.
- The skill NEVER runs `git add` against the vault (CLAUDE.md rule 8 — Obsidian-Git owns vault commits).
- Verified OpenRouter model IDs (2026-06-20): `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `google/gemini-pro-latest`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, `mistralai/mistral-medium-3.5`, `perplexity/sonar-reasoning-pro`, `perplexity/sonar-deep-research`. Sonar models are `tools=False` → Stage 1b only, never the panel.

---

## File Structure

```
tools/llm-council/council/discovery/
├── __init__.py        # package marker
├── evidence.py        # EvidenceRecord, EvidenceBundle (dedup, url index)
├── tiers.py           # TierConfig (panel, judge, max_tool_calls, per-run cap), get_tier
├── fusion.py          # fuse(): one OpenRouter Fusion call → CandidatePainPoint list
├── gather/
│   ├── __init__.py    # gather_evidence(): run tier collectors → EvidenceBundle
│   ├── last30.py      # last30days shell-out + parse
│   ├── sonar.py       # Perplexity Sonar fresh-article collector
│   └── web.py         # Exa/Brave search + fetch-extract collector
├── verify.py          # verify_pain_points(): fabrication gate
├── frame.py           # frame_pm(): clusters → IdeaCard list + quote bank + blind-spot map
├── render.py          # render_ledger(): markdown idea ledger
├── pipeline.py        # run_discovery(): orchestrates the 4 stages + session json
└── __main__.py        # CLI: python -m council.discovery
tools/llm-council/council/budget.py   # MODIFY: add tool= to record_spend + per-tool reads
tools/llm-council/tests/discovery/    # one test module per source file above
.claude/skills/fusion-discovery-council/SKILL.md   # the invocable skill
```

---

## Task 1: Scaffold `discovery/` package + evidence model

**Files:**
- Create: `tools/llm-council/council/discovery/__init__.py`
- Create: `tools/llm-council/council/discovery/evidence.py`
- Create: `tools/llm-council/tests/discovery/__init__.py`
- Test: `tools/llm-council/tests/discovery/test_evidence.py`

**Interfaces:**
- Produces:
  - `EvidenceRecord(source_type: str, source_name: str, url: str, date: str, quote: str, engagement: int = 0)` — frozen dataclass.
  - `EvidenceBundle` with `.add(record) -> bool` (returns False if deduped), `.records: list[EvidenceRecord]`, `.has_url(url: str) -> bool`, `.urls: set[str]`.
  - Dedup key = `(url, quote.strip().lower()[:200])`.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_evidence.py
from council.discovery.evidence import EvidenceRecord, EvidenceBundle


def _rec(url="https://r.com/1", quote="it crashes daily", **kw):
    base = dict(source_type="reddit", source_name="r/x", url=url, date="2026-06-19", quote=quote, engagement=12)
    base.update(kw)
    return EvidenceRecord(**base)


def test_add_returns_true_then_false_on_dup():
    b = EvidenceBundle()
    assert b.add(_rec()) is True
    assert b.add(_rec()) is False           # same url+quote → deduped
    assert len(b.records) == 1


def test_has_url_and_urls():
    b = EvidenceBundle()
    b.add(_rec(url="https://a.com/x"))
    b.add(_rec(url="https://b.com/y", quote="other pain"))
    assert b.has_url("https://a.com/x") is True
    assert b.has_url("https://nope.com") is False
    assert b.urls == {"https://a.com/x", "https://b.com/y"}


def test_dedup_is_case_insensitive_on_quote():
    b = EvidenceBundle()
    b.add(_rec(quote="It Crashes Daily"))
    assert b.add(_rec(quote="it crashes daily")) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_evidence.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/__init__.py
"""fusion-discovery-council: multi-model fresh-evidence discovery, co-located with council to share the budget/client spine."""
```

```python
# council/discovery/evidence.py
"""Evidence model: real-URL records gathered in Stage 1, consumed by fuse/verify/frame."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvidenceRecord:
    source_type: str   # "reddit" | "x" | "youtube" | "hn" | "sonar" | "web" | ...
    source_name: str   # "r/ProductManagement", "@handle", "G2", publication name
    url: str
    date: str          # ISO "YYYY-MM-DD" or "" if unknown
    quote: str         # verbatim text actually present at url
    engagement: int = 0


def _dedup_key(r: EvidenceRecord) -> tuple[str, str]:
    return (r.url, r.quote.strip().lower()[:200])


@dataclass
class EvidenceBundle:
    records: list[EvidenceRecord] = field(default_factory=list)
    _keys: set = field(default_factory=set)
    urls: set = field(default_factory=set)

    def add(self, record: EvidenceRecord) -> bool:
        key = _dedup_key(record)
        if key in self._keys:
            return False
        self._keys.add(key)
        self.records.append(record)
        self.urls.add(record.url)
        return True

    def has_url(self, url: str) -> bool:
        return url in self.urls
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_evidence.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/__init__.py council/discovery/evidence.py tests/discovery/
git commit -m "feat(discovery): evidence model (EvidenceRecord + dedup bundle)"
```

---

## Task 2: Tier configuration

**Files:**
- Create: `tools/llm-council/council/discovery/tiers.py`
- Test: `tools/llm-council/tests/discovery/test_tiers.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `TierConfig(name, panel: tuple[str,...], judge: str, max_tool_calls: int, max_cost_per_run: float, sonar_model: str, social: bool, web: bool)`
  - `get_tier(name: str) -> TierConfig` (raises `KeyError` listing valid names).
  - `TIERS` dict with keys `quick`, `standard`, `deep`.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_tiers.py
import pytest
from council.discovery.tiers import get_tier, TIERS


def test_three_tiers_exist():
    assert set(TIERS) == {"quick", "standard", "deep"}


def test_standard_panel_is_four_frontier_vendors():
    t = get_tier("standard")
    assert t.panel == (
        "anthropic/claude-opus-4.7",
        "openai/gpt-5.5",
        "google/gemini-pro-latest",
        "x-ai/grok-4.3",
    )
    assert t.judge == "anthropic/claude-opus-4.7"
    assert t.max_cost_per_run == 1.50


def test_sonar_never_in_panel():
    for name in TIERS:
        panel = get_tier(name).panel
        assert not any("sonar" in m or "perplexity" in m for m in panel)


def test_deep_adds_two_more_lineages_and_confirms_cost():
    t = get_tier("deep")
    assert "deepseek/deepseek-v4-pro" in t.panel
    assert "mistralai/mistral-medium-3.5" in t.panel
    assert t.max_cost_per_run == 4.00


def test_unknown_tier_raises():
    with pytest.raises(KeyError):
        get_tier("ultra")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_tiers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.tiers'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/tiers.py
"""Tier configs: panel/judge/tool-budget/cost-cap per quick|standard|deep."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TierConfig:
    name: str
    panel: tuple[str, ...]      # Fusion analysis_models (tool-capable only)
    judge: str                  # Fusion judge / outer model
    max_tool_calls: int         # per-panel-model web tool-call budget
    max_cost_per_run: float
    sonar_model: str            # Stage 1b article harvester
    social: bool                # run last30days backbone
    web: bool                   # run exa/brave web collector


_STANDARD_PANEL = (
    "anthropic/claude-opus-4.7",
    "openai/gpt-5.5",
    "google/gemini-pro-latest",
    "x-ai/grok-4.3",
)

TIERS: dict[str, TierConfig] = {
    "quick": TierConfig(
        name="quick",
        panel=("google/gemini-pro-latest", "x-ai/grok-4.3", "deepseek/deepseek-v4-pro"),
        judge="google/gemini-pro-latest",
        max_tool_calls=3,
        max_cost_per_run=0.50,
        sonar_model="perplexity/sonar",
        social=True,
        web=True,
    ),
    "standard": TierConfig(
        name="standard",
        panel=_STANDARD_PANEL,
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=5,
        max_cost_per_run=1.50,
        sonar_model="perplexity/sonar-reasoning-pro",
        social=True,
        web=True,
    ),
    "deep": TierConfig(
        name="deep",
        panel=_STANDARD_PANEL + ("deepseek/deepseek-v4-pro", "mistralai/mistral-medium-3.5"),
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=8,
        max_cost_per_run=4.00,
        sonar_model="perplexity/sonar-deep-research",
        social=True,
        web=True,
    ),
}


def get_tier(name: str) -> TierConfig:
    if name not in TIERS:
        raise KeyError(f"Unknown tier {name!r}. Available: {', '.join(sorted(TIERS))}")
    return TIERS[name]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_tiers.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/tiers.py tests/discovery/test_tiers.py
git commit -m "feat(discovery): tier configs (quick/standard/deep panels + caps)"
```

---

## Task 3: Per-tool budget caps (extend `budget.py`)

**Files:**
- Modify: `tools/llm-council/council/budget.py`
- Test: `tools/llm-council/tests/discovery/test_budget_tool.py`

**Interfaces:**
- Consumes: existing `record_spend`, `preflight`, `_read_total_for_day/month`.
- Produces:
  - `record_spend(..., tool: str = "council")` — adds `tool` to each run record (backward compatible).
  - `tool_total_for_day(on_date, tool) -> float` and `tool_total_for_month(on_date, tool) -> float` — sum only runs whose `tool` matches.
  - `preflight_tool(*, estimated, per_query_cap, daily_cap, monthly_cap, on_date, tool, force=False)` — same gates as `preflight` but daily/monthly read per-tool.

**Why:** discovery and council share the spend file; caps must be independent so a heavy discovery day can't block a council critique.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_budget_tool.py
from datetime import date
from council import budget


def test_tool_totals_isolated(tmp_spend_dir):
    d = date(2026, 6, 20)
    budget.record_spend(amount=0.30, profile="standard", tag="t1", on_date=d, tool="discovery")
    budget.record_spend(amount=0.90, profile="premium", tag="t2", on_date=d, tool="council")
    assert round(budget.tool_total_for_day(d, "discovery"), 4) == 0.30
    assert round(budget.tool_total_for_day(d, "council"), 4) == 0.90


def test_preflight_tool_rejects_on_tool_daily_cap(tmp_spend_dir):
    d = date(2026, 6, 20)
    budget.record_spend(amount=9.80, profile="standard", tag="t", on_date=d, tool="discovery")
    import pytest
    with pytest.raises(budget.BudgetExceeded):
        budget.preflight_tool(
            estimated=0.50, per_query_cap=1.50, daily_cap=10.0, monthly_cap=50.0,
            on_date=d, tool="discovery",
        )
    # council budget is unaffected by discovery spend
    budget.preflight_tool(
        estimated=0.50, per_query_cap=1.00, daily_cap=10.0, monthly_cap=50.0,
        on_date=d, tool="council",
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_budget_tool.py -v`
Expected: FAIL — `AttributeError: module 'council.budget' has no attribute 'tool_total_for_day'`.

- [ ] **Step 3: Write minimal implementation**

In `council/budget.py`, change `record_spend` to accept `tool` and store it, and add the per-tool readers + `preflight_tool`:

```python
def record_spend(*, amount: float, profile: str, tag: str, on_date: date, tool: str = "council") -> None:
    """Append a run to today's daily spend file. Atomic write."""
    f = _daily_file(on_date)
    if f.exists():
        data = json.loads(f.read_text())
    else:
        data = {"date": on_date.isoformat(), "total": 0.0, "runs": []}
    data["runs"].append({"amount": amount, "profile": profile, "tag": tag, "tool": tool})
    data["total"] = round(data["total"] + amount, 6)
    _atomic_write_json(f, data)


def _sum_runs(path: Path, tool: str) -> float:
    if not path.exists():
        return 0.0
    try:
        runs = json.loads(path.read_text()).get("runs", [])
    except (json.JSONDecodeError, ValueError):
        return 0.0
    # Records written before the tool field default to "council".
    return sum(float(r.get("amount", 0.0)) for r in runs if r.get("tool", "council") == tool)


def tool_total_for_day(on_date: date, tool: str) -> float:
    return _sum_runs(_daily_file(on_date), tool)


def tool_total_for_month(on_date: date, tool: str) -> float:
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    return sum(_sum_runs(f, tool) for f in _spend_dir().glob(f"{prefix}*.json"))


def preflight_tool(
    *, estimated: float, per_query_cap: float, daily_cap: float, monthly_cap: float,
    on_date: date, tool: str, force: bool = False,
) -> None:
    """Like preflight, but daily/monthly totals are scoped to one tool."""
    if not force and estimated > per_query_cap:
        raise BudgetExceeded(
            f"per-run cap exceeded: estimated ${estimated:.4f} > cap ${per_query_cap:.4f}. "
            f"Use --force to override (still subject to daily/monthly caps)."
        )
    today = tool_total_for_day(on_date, tool)
    if today + estimated > daily_cap:
        raise BudgetExceeded(
            f"{tool} daily cap would be exceeded: today=${today:.4f} + "
            f"estimated=${estimated:.4f} > daily_cap=${daily_cap:.4f}"
        )
    month = tool_total_for_month(on_date, tool)
    if month + estimated > monthly_cap:
        raise BudgetExceeded(
            f"{tool} monthly cap would be exceeded: month-to-date=${month:.4f} + "
            f"estimated=${estimated:.4f} > monthly_cap=${monthly_cap:.4f}"
        )
```

- [ ] **Step 4: Run tests (new + existing budget tests stay green)**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_budget_tool.py tests/test_budget.py -v`
Expected: PASS (new tests + all existing `test_budget.py`; `record_spend`'s new kwarg is defaulted so existing calls are unaffected).

- [ ] **Step 5: Commit**

```bash
git add council/budget.py tests/discovery/test_budget_tool.py
git commit -m "feat(discovery): per-tool spend caps (independent discovery vs council budgets)"
```

---

## Task 4: Verify Fusion request/response schema (live spike)

**Files:**
- Create: `tools/llm-council/council/discovery/FUSION_SCHEMA.md` (captured request + response shape)

**Why first:** the public docs name the params (`analysis_models`, judge `model`, `max_tool_calls`, tool `{"type":"openrouter:fusion"}`, `tool_choice:"required"`) but not the exact JSON envelope of the judge's structured output. Task 5 builds the parser against this captured shape, so we de-risk it with one real minimal call. This task writes NO production code — it records ground truth.

- [ ] **Step 1: Make one minimal live Fusion call**

Run (requires `OPENROUTER_API_KEY` in the council `.env`):

```bash
cd tools/llm-council
uv run python - <<'PY'
import os, json, httpx
key = os.environ["OPENROUTER_API_KEY"]
body = {
  "model": "google/gemini-pro-latest",
  "messages": [{"role": "user", "content": "What are the 2 most common complaints about Obsidian sync? Use web search."}],
  "tools": [{"type": "openrouter:fusion"}],
  "tool_choice": "required",
  "fusion": {
    "analysis_models": ["x-ai/grok-4.3", "deepseek/deepseek-v4-pro"],
    "max_tool_calls": 2
  }
}
r = httpx.post("https://openrouter.ai/api/v1/chat/completions",
               headers={"Authorization": f"Bearer {key}"}, json=body, timeout=180)
print("STATUS", r.status_code)
print(json.dumps(r.json(), indent=2)[:6000])
PY
```

- [ ] **Step 2: Record the captured shape**

Write `council/discovery/FUSION_SCHEMA.md` documenting, verbatim from the response:
- The exact request envelope that worked (top-level `fusion` object vs tool-embedded args — correct it if the call above 4xx'd, e.g. params may belong inside the tool object).
- Where the panel responses, the judge's consensus/contradiction/blind-spot analysis, and the final synthesized text appear in the response JSON (path to each).
- The `usage` block fields for cost (prompt/completion tokens; any `cost` field; web-search call count if present).

Expected: a markdown file with real JSON excerpts. If the call returned 4xx, document the error and the corrected request shape that succeeds before moving on.

- [ ] **Step 3: Commit**

```bash
git add council/discovery/FUSION_SCHEMA.md
git commit -m "docs(discovery): capture live OpenRouter Fusion request/response schema"
```

---

## Task 5: Fusion client (`fuse`)

**Files:**
- Create: `tools/llm-council/council/discovery/fusion.py`
- Test: `tools/llm-council/tests/discovery/test_fusion.py`

**Interfaces:**
- Consumes: `EvidenceBundle` (Task 1), `TierConfig` (Task 2), `council.client.OpenRouterClient` env/key handling, `FUSION_SCHEMA.md` (Task 4).
- Produces:
  - `CandidatePainPoint(title, summary, quotes: list[str], urls: list[str], consensus: str, intensity: int, recency: str, segment: str)` dataclass.
  - `FusionResult(pain_points: list[CandidatePainPoint], blind_spots: list[str], contradictions: list[str], tokens_in: int, tokens_out: int, web_calls: int)`.
  - `async fuse(*, api_key, bundle, tier, topic, timeout=180.0) -> FusionResult`.
- The judge is instructed to return a JSON object: `{"pain_points":[{title,summary,quotes,urls,consensus,intensity,recency,segment}], "blind_spots":[...], "contradictions":[...]}`. Parse with the same fence-stripping approach as `pipeline._parse_ranking`.

**Note:** adjust the request body in `_build_body` to match the exact shape recorded in `FUSION_SCHEMA.md`. The code below assumes a top-level `fusion` object; correct if the spike found otherwise.

- [ ] **Step 1: Write the failing test (mocked httpx)**

```python
# tests/discovery/test_fusion.py
import json
import httpx
import pytest
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery import fusion


def _bundle():
    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "sync drops notes", 40))
    return b


@pytest.mark.asyncio
async def test_fuse_parses_judge_json(httpx_mock):
    judge_payload = {
        "pain_points": [{
            "title": "Sync data loss",
            "summary": "Notes silently dropped on conflict.",
            "quotes": ["sync drops notes"],
            "urls": ["https://r.com/1"],
            "consensus": "4/4 models",
            "intensity": 5, "recency": "2026-06", "segment": "power users",
        }],
        "blind_spots": ["no model addressed enterprise SSO"],
        "contradictions": ["grok: mobile-only; gemini: desktop too"],
    }
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": json.dumps(judge_payload)}}],
        "usage": {"prompt_tokens": 1200, "completion_tokens": 400},
    })
    res = await fusion.fuse(api_key="k", bundle=_bundle(), tier=get_tier("quick"), topic="obsidian sync")
    assert len(res.pain_points) == 1
    assert res.pain_points[0].title == "Sync data loss"
    assert res.pain_points[0].urls == ["https://r.com/1"]
    assert res.blind_spots == ["no model addressed enterprise SSO"]
    assert res.tokens_in == 1200 and res.tokens_out == 400


@pytest.mark.asyncio
async def test_fuse_retries_then_raises_on_unparseable(httpx_mock):
    httpx_mock.add_response(json={"choices": [{"message": {"content": "not json"}}], "usage": {}})
    httpx_mock.add_response(json={"choices": [{"message": {"content": "still not json"}}], "usage": {}})
    with pytest.raises(fusion.FusionError):
        await fusion.fuse(api_key="k", bundle=_bundle(), tier=get_tier("quick"), topic="x")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_fusion.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.fusion'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/fusion.py
"""Stage 2 — one OpenRouter Fusion call: panel reasons over the evidence bundle, judge clusters pain points."""

import json
from dataclasses import dataclass, field

import httpx

from council.discovery.evidence import EvidenceBundle
from council.discovery.tiers import TierConfig

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class FusionError(Exception):
    pass


@dataclass
class CandidatePainPoint:
    title: str
    summary: str
    quotes: list[str]
    urls: list[str]
    consensus: str = ""
    intensity: int = 0
    recency: str = ""
    segment: str = ""


@dataclass
class FusionResult:
    pain_points: list[CandidatePainPoint] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    web_calls: int = 0


def _evidence_block(bundle: EvidenceBundle) -> str:
    lines = []
    for r in bundle.records:
        lines.append(f"[{r.source_type}/{r.source_name} | {r.date} | {r.url}] {r.quote}")
    return "\n".join(lines)


_JUDGE_INSTRUCTION = (
    "You are the judge of a multi-model discovery panel. Cluster the panel's findings into "
    "user PAIN POINTS grounded ONLY in the evidence provided. Return ONLY a JSON object: "
    '{"pain_points":[{"title","summary","quotes":[verbatim strings from evidence],'
    '"urls":[urls from evidence that contain those quotes],"consensus","intensity":1-5,'
    '"recency","segment"}],"blind_spots":[strings],"contradictions":[strings]}. '
    "Every quote MUST be copied verbatim from the evidence and every url MUST appear in the evidence. "
    "Do not invent sources."
)


def _build_body(bundle: EvidenceBundle, tier: TierConfig, topic: str) -> dict:
    user = (
        f"TOPIC: {topic}\n\nEVIDENCE (real, fetched):\n{_evidence_block(bundle)}\n\n"
        "Find the highest-signal user pain points. Use web_search only to fill gaps."
    )
    # NOTE: shape per FUSION_SCHEMA.md (Task 4). Correct field placement if the spike differed.
    return {
        "model": tier.judge,
        "messages": [
            {"role": "system", "content": _JUDGE_INSTRUCTION},
            {"role": "user", "content": user},
        ],
        "tools": [{"type": "openrouter:fusion"}],
        "tool_choice": "required",
        "fusion": {
            "analysis_models": list(tier.panel),
            "max_tool_calls": tier.max_tool_calls,
        },
    }


def _parse(content: str) -> dict | None:
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return None
    return data if "pain_points" in data else None


def _to_result(data: dict, usage: dict) -> FusionResult:
    pts = [
        CandidatePainPoint(
            title=p.get("title", ""), summary=p.get("summary", ""),
            quotes=list(p.get("quotes", [])), urls=list(p.get("urls", [])),
            consensus=p.get("consensus", ""), intensity=int(p.get("intensity", 0) or 0),
            recency=p.get("recency", ""), segment=p.get("segment", ""),
        )
        for p in data.get("pain_points", [])
    ]
    return FusionResult(
        pain_points=pts,
        blind_spots=list(data.get("blind_spots", [])),
        contradictions=list(data.get("contradictions", [])),
        tokens_in=usage.get("prompt_tokens", 0),
        tokens_out=usage.get("completion_tokens", 0),
        web_calls=int(usage.get("web_search_calls", 0) or 0),
    )


async def fuse(*, api_key: str, bundle: EvidenceBundle, tier: TierConfig, topic: str, timeout: float = 180.0) -> FusionResult:
    body = _build_body(bundle, tier, topic)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(2):
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            resp.raise_for_status()
            payload = resp.json()
            choice = (payload.get("choices") or [{}])[0]
            content = choice.get("message", {}).get("content", "")
            data = _parse(content)
            if data is not None:
                return _to_result(data, payload.get("usage", {}))
            body["messages"][0]["content"] = _JUDGE_INSTRUCTION + "\n\nReturn ONLY the JSON object."
        raise FusionError("Fusion judge did not return parseable pain-point JSON after retry.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_fusion.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py tests/discovery/test_fusion.py
git commit -m "feat(discovery): Fusion client — panel+judge over evidence bundle"
```

---

## Task 6: last30days gather collector

**Files:**
- Create: `tools/llm-council/council/discovery/gather/__init__.py` (stub; orchestrator added in Task 9)
- Create: `tools/llm-council/council/discovery/gather/last30.py`
- Test: `tools/llm-council/tests/discovery/test_gather_last30.py`

**Interfaces:**
- Consumes: `EvidenceRecord` (Task 1).
- Produces: `parse_last30_output(text: str) -> list[EvidenceRecord]` and `async collect_last30(topic: str, runner=...) -> list[EvidenceRecord]` where `runner(topic) -> str` defaults to a subprocess shell-out (injected in tests).
- Parser handles the `--emit=compact` line shapes from last30days: Reddit/X/YouTube items carry a URL and a quote/top-comment. Extract `(source_type, source_name, url, quote)`; `date=""`, `engagement` from a `[Npts]`/`[Nlikes]` token when present (else 0).

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_gather_last30.py
import pytest
from council.discovery.gather.last30 import parse_last30_output, collect_last30


SAMPLE = """\
🟠 Reddit
r/ProductManagement (score:120) https://reddit.com/r/pm/abc [120pts, 30cmt]
title: Roadmap tools all suck
💬 Top comment (88 upvotes): "Every roadmap tool forces a process my team hates"

🔵 X
@pmhandle (score:50) https://x.com/pmhandle/status/9 [50likes, 5rt]
"Linear is great until you need cross-team OKRs, then it falls apart"
"""


def test_parse_extracts_reddit_and_x_records():
    recs = parse_last30_output(SAMPLE)
    by_type = {r.source_type for r in recs}
    assert "reddit" in by_type and "x" in by_type
    reddit = next(r for r in recs if r.source_type == "reddit")
    assert reddit.url == "https://reddit.com/r/pm/abc"
    assert "roadmap tool forces a process" in reddit.quote
    assert reddit.engagement == 120


@pytest.mark.asyncio
async def test_collect_uses_injected_runner():
    async def fake_runner(topic):
        return SAMPLE
    recs = await collect_last30("roadmap tools", runner=fake_runner)
    assert len(recs) >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_last30.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.gather.last30'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/gather/__init__.py
"""Stage 1 collectors. Orchestrator gather_evidence() added in Task 9."""
```

```python
# council/discovery/gather/last30.py
"""Collector: shell out to last30days --agent and parse its compact output into evidence."""

import asyncio
import re
import shutil
from pathlib import Path

from council.discovery.evidence import EvidenceRecord

_URL = re.compile(r"https?://\S+")
_ENGAGE = re.compile(r"\[(\d+)\s*(?:pts|likes)")
_QUOTE = re.compile(r'"([^"]{12,})"')
_SECTION = {"reddit": "reddit", "x": "x", "youtube": "youtube", "hn": "hn"}


def parse_last30_output(text: str) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    section = "web"
    cur_url = cur_name = ""
    cur_engage = 0
    for raw in text.splitlines():
        line = raw.strip()
        low = line.lower()
        for key, st in _SECTION.items():
            if low.startswith(("🟠", "🔵", "🔴", "🟡")) and key in low:
                section = st
        m = _URL.search(line)
        if m:
            cur_url = m.group(0).rstrip(").,")
            cur_name = line.split()[0] if line.split() else section
            e = _ENGAGE.search(line)
            cur_engage = int(e.group(1)) if e else 0
        q = _QUOTE.search(line)
        if q and cur_url:
            records.append(EvidenceRecord(
                source_type=section, source_name=cur_name, url=cur_url,
                date="", quote=q.group(1), engagement=cur_engage,
            ))
    return records


def _find_last30_script() -> Path:
    for cand in (
        Path.home() / ".claude/skills/last30days/scripts/last30days.py",
        Path.home() / ".agents/skills/last30days/scripts/last30days.py",
    ):
        if cand.exists():
            return cand
    raise FileNotFoundError("last30days script not found in ~/.claude or ~/.agents skills.")


async def _subprocess_runner(topic: str) -> str:
    script = _find_last30_script()
    py = shutil.which("python3") or "python3"
    proc = await asyncio.create_subprocess_exec(
        py, str(script), topic, "--agent", "--emit=compact", "--no-native-web",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    out, _ = await asyncio.wait_for(proc.communicate(), timeout=300)
    return out.decode("utf-8", "replace")


async def collect_last30(topic: str, runner=_subprocess_runner) -> list[EvidenceRecord]:
    try:
        text = await runner(topic)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
    return parse_last30_output(text)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_last30.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/ tests/discovery/test_gather_last30.py
git commit -m "feat(discovery): last30days social collector + compact-output parser"
```

---

## Task 7: Sonar fresh-article collector

**Files:**
- Create: `tools/llm-council/council/discovery/gather/sonar.py`
- Test: `tools/llm-council/tests/discovery/test_gather_sonar.py`

**Interfaces:**
- Consumes: `EvidenceRecord`, `council.client.OpenRouterClient`-style HTTP (but Sonar needs the raw response `citations`, so call httpx directly here).
- Produces: `async collect_sonar(*, api_key, topic, model, timeout=120.0) -> list[EvidenceRecord]`. Sends a chat completion to the Sonar `model`; reads `choices[0].message.content` for claim sentences and the response-level `citations` (list of URLs) to build records with `source_type="sonar"`, `source_name="Perplexity Sonar"`, real citation URLs. If no citations, return `[]` (never fabricate URLs).

- [ ] **Step 1: Write the failing test (mocked)**

```python
# tests/discovery/test_gather_sonar.py
import pytest
from council.discovery.gather.sonar import collect_sonar


@pytest.mark.asyncio
async def test_collect_sonar_uses_citations(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Teams report onboarding is slow. Pricing is opaque."}}],
        "citations": ["https://news.com/a", "https://blog.com/b"],
        "usage": {"prompt_tokens": 100, "completion_tokens": 60},
    })
    recs = await collect_sonar(api_key="k", topic="pm tools", model="perplexity/sonar-reasoning-pro")
    assert len(recs) >= 1
    assert all(r.url.startswith("http") for r in recs)
    assert all(r.source_type == "sonar" for r in recs)


@pytest.mark.asyncio
async def test_no_citations_yields_nothing(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Some claim."}}], "citations": [], "usage": {},
    })
    recs = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar")
    assert recs == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_sonar.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/gather/sonar.py
"""Collector: Perplexity Sonar fresh-article harvest. Citation URLs are the evidence anchors."""

import re
import httpx

from council.discovery.evidence import EvidenceRecord

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_SENT = re.compile(r"[^.!?]{20,}[.!?]")


async def collect_sonar(*, api_key: str, topic: str, model: str, timeout: float = 120.0) -> list[EvidenceRecord]:
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"What are the most recent, specific user complaints and unmet needs about {topic}? "
                       f"Quote real users where possible. Cite sources.",
        }],
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            resp.raise_for_status()
            payload = resp.json()
    except (httpx.HTTPError,):
        return []
    citations = payload.get("citations") or []
    if not citations:
        return []
    content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "")
    sentences = [s.strip() for s in _SENT.findall(content)][: len(citations)] or [content[:200]]
    recs = []
    for i, url in enumerate(citations):
        quote = sentences[i] if i < len(sentences) else sentences[-1]
        recs.append(EvidenceRecord(
            source_type="sonar", source_name="Perplexity Sonar", url=url,
            date="", quote=quote, engagement=0,
        ))
    return recs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_sonar.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/sonar.py tests/discovery/test_gather_sonar.py
git commit -m "feat(discovery): Sonar fresh-article collector (citation-anchored)"
```

---

## Task 8: Web search collector (Exa/Brave + fetch)

**Files:**
- Create: `tools/llm-council/council/discovery/gather/web.py`
- Test: `tools/llm-council/tests/discovery/test_gather_web.py`

**Interfaces:**
- Consumes: `EvidenceRecord`.
- Produces: `async collect_web(*, topic, search=..., fetch=..., max_results=8) -> list[EvidenceRecord]`. `search(query) -> list[dict]` (each `{title,url,published}`) and `fetch(url) -> str` are injected (default: Exa if `EXA_API_KEY` set, else Brave if `BRAVE_API_KEY`, else return `[]`). For each result, fetch text, extract 1–2 complaint-shaped sentences as quotes, build records with `source_type="web"`, real `url`, `date=published`.

- [ ] **Step 1: Write the failing test (injected search+fetch)**

```python
# tests/discovery/test_gather_web.py
import pytest
from council.discovery.gather.web import collect_web, extract_quotes


def test_extract_quotes_prefers_complaint_sentences():
    text = "The dashboard is fine. Users complain that exports fail silently every week. Nice colors."
    quotes = extract_quotes(text)
    assert any("exports fail" in q for q in quotes)


@pytest.mark.asyncio
async def test_collect_web_builds_records():
    async def search(q):
        return [{"title": "T", "url": "https://blog.com/x", "published": "2026-06-15"}]
    async def fetch(u):
        return "Teams say the export silently fails and support never replies."
    recs = await collect_web(topic="exports", search=search, fetch=fetch)
    assert len(recs) == 1
    assert recs[0].url == "https://blog.com/x"
    assert recs[0].date == "2026-06-15"
    assert recs[0].source_type == "web"


@pytest.mark.asyncio
async def test_no_search_provider_returns_empty():
    recs = await collect_web(topic="x", search=None, fetch=None)
    assert recs == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_web.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/gather/web.py
"""Collector: neural web search (Exa/Brave) + fetch → complaint-quote extraction."""

import os
import re

import httpx

from council.discovery.evidence import EvidenceRecord

_SENT = re.compile(r"[^.!?]{20,240}[.!?]")
_COMPLAINT = re.compile(
    r"\b(complain|frustrat|annoy|hate|broken|fails?|can't|cannot|wish|missing|lacks?|"
    r"slow|confusing|workaround|painful|bug|crash)\b", re.I,
)


def extract_quotes(text: str, limit: int = 2) -> list[str]:
    hits = [s.strip() for s in _SENT.findall(text) if _COMPLAINT.search(s)]
    return hits[:limit]


def _default_exa_search(api_key: str):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                "https://api.exa.ai/search",
                headers={"x-api-key": api_key, "Content-Type": "application/json"},
                json={"query": query, "numResults": 8, "type": "neural",
                      "contents": {"text": True}},
            )
            r.raise_for_status()
            out = []
            for it in r.json().get("results", []):
                out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                            "published": (it.get("publishedDate") or "")[:10],
                            "_text": (it.get("text") or "")})
            return out
    return search


async def collect_web(*, topic: str, search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        exa = os.environ.get("EXA_API_KEY")
        search = _default_exa_search(exa) if exa else None
    if search is None:
        return []
    query = f"{topic} user complaints problems frustrations 2026"
    results = await search(query)
    recs: list[EvidenceRecord] = []
    for it in results[:max_results]:
        url = it.get("url", "")
        if not url:
            continue
        text = it.get("_text") or ("" if fetch in (None, ...) else await fetch(url))
        for q in extract_quotes(text):
            recs.append(EvidenceRecord(
                source_type="web", source_name=it.get("title", "") or "web",
                url=url, date=it.get("published", ""), quote=q, engagement=0,
            ))
    return recs
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_web.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/web.py tests/discovery/test_gather_web.py
git commit -m "feat(discovery): web search+fetch collector with complaint extraction"
```

---

## Task 9: Gather orchestrator

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/__init__.py`
- Test: `tools/llm-council/tests/discovery/test_gather_orchestrator.py`

**Interfaces:**
- Consumes: `collect_last30` (T6), `collect_sonar` (T7), `collect_web` (T8), `TierConfig` (T2), `EvidenceBundle` (T1).
- Produces: `async gather_evidence(*, topic, tier, api_key, collectors=None) -> EvidenceBundle`. Runs the tier-enabled collectors concurrently (`asyncio.gather(..., return_exceptions=True)`), folds all records into a deduped bundle, and never raises on one collector failing (a failed collector contributes 0 records). `collectors` is an injectable dict for tests.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_gather_orchestrator.py
import pytest
from council.discovery.evidence import EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence


@pytest.mark.asyncio
async def test_gather_merges_and_dedups():
    async def s(topic): return [EvidenceRecord("sonar", "S", "https://a/1", "", "pain a")]
    async def w(topic): return [EvidenceRecord("web", "W", "https://a/1", "", "pain a"),  # dup
                                EvidenceRecord("web", "W", "https://b/2", "", "pain b")]
    async def l(topic): raise RuntimeError("last30 down")
    bundle = await gather_evidence(
        topic="x", tier=get_tier("quick"), api_key="k",
        collectors={"sonar": s, "web": w, "last30": l},
    )
    assert len(bundle.records) == 2          # dup dropped, last30 failure tolerated
    assert bundle.has_url("https://b/2")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_orchestrator.py -v`
Expected: FAIL — `ImportError: cannot import name 'gather_evidence'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → deduped EvidenceBundle."""

import asyncio

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str, collectors: dict | None = None) -> EvidenceBundle:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
        }
    coros = [fn(topic) for fn in collectors.values() if fn is not None]
    results = await asyncio.gather(*coros, return_exceptions=True)
    bundle = EvidenceBundle()
    for r in results:
        if isinstance(r, Exception):
            continue
        for rec in r:
            bundle.add(rec)
    return bundle
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_gather_orchestrator.py -v`
Expected: PASS (1 test).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/__init__.py tests/discovery/test_gather_orchestrator.py
git commit -m "feat(discovery): gather orchestrator (concurrent, failure-tolerant)"
```

---

## Task 10: Verify gate (fabrication killer)

**Files:**
- Create: `tools/llm-council/council/discovery/verify.py`
- Test: `tools/llm-council/tests/discovery/test_verify.py`

**Interfaces:**
- Consumes: `CandidatePainPoint` (T5), `EvidenceBundle` (T1).
- Produces: `VerifiedPainPoint(point: CandidatePainPoint, verified: bool, supporting_urls: list[str])` and `verify_pain_points(points, bundle) -> list[VerifiedPainPoint]`. A point is `verified=True` iff ≥1 of its `urls` is in `bundle.urls` AND the matching quote substring appears in some bundle record at that URL. `supporting_urls` = the subset that checks out. Unverified points are returned with `verified=False` (caller decides to drop or mark).

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/verify.py
"""Stage 3 — fabrication gate. A pain point survives only if a quote it cites
actually appears at a URL present in the evidence bundle."""

from dataclasses import dataclass

from council.discovery.evidence import EvidenceBundle
from council.discovery.fusion import CandidatePainPoint


@dataclass
class VerifiedPainPoint:
    point: CandidatePainPoint
    verified: bool
    supporting_urls: list[str]


def _quote_present_at_url(bundle: EvidenceBundle, url: str, quotes: list[str]) -> bool:
    for rec in bundle.records:
        if rec.url != url:
            continue
        hay = rec.quote.strip().lower()
        for q in quotes:
            needle = q.strip().lower()
            if needle and (needle in hay or hay in needle):
                return True
    return False


def verify_pain_points(points: list[CandidatePainPoint], bundle: EvidenceBundle) -> list[VerifiedPainPoint]:
    out: list[VerifiedPainPoint] = []
    for pt in points:
        supporting = [
            u for u in pt.urls
            if bundle.has_url(u) and _quote_present_at_url(bundle, u, pt.quotes)
        ]
        out.append(VerifiedPainPoint(point=pt, verified=bool(supporting), supporting_urls=supporting))
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_verify.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/verify.py tests/discovery/test_verify.py
git commit -m "feat(discovery): fabrication gate — drop pain points without traceable evidence"
```

---

## Task 11: Frame (pm lens) — idea cards + scoring

**Files:**
- Create: `tools/llm-council/council/discovery/frame.py`
- Test: `tools/llm-council/tests/discovery/test_frame.py`

**Interfaces:**
- Consumes: `VerifiedPainPoint` (T10), `FusionResult` (T5, for blind_spots/contradictions).
- Produces:
  - `IdeaCard(title, who, pain, workaround, opportunity, evidence_urls, quotes, score, corroboration)`.
  - `frame_pm(verified, fusion_result) -> tuple[list[IdeaCard], list[str]]` → `(ranked_idea_cards, quote_bank)`. Only `verified=True` points become cards. `score = intensity * (1 + corroboration)` where `corroboration` = number of distinct source domains across supporting urls; cards sorted by score desc. The `opportunity` line is templated from the pain (`"Build/ship X that removes <pain>"`). Quote bank = unique `quote — url` strings across all verified points.

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_frame.py
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.verify import VerifiedPainPoint
from council.discovery.frame import frame_pm


def _vpp(title, intensity, urls):
    pt = CandidatePainPoint(title, "summary", quotes=[f"{title} quote"], urls=urls,
                            intensity=intensity, segment="PMs")
    return VerifiedPainPoint(point=pt, verified=True, supporting_urls=urls)


def test_cards_sorted_by_score_and_only_verified():
    low = _vpp("Low", 2, ["https://a.com/1"])
    high = _vpp("High", 5, ["https://a.com/2", "https://b.com/3"])  # 2 domains → higher corroboration
    dropped = VerifiedPainPoint(point=CandidatePainPoint("X", "", [], []), verified=False, supporting_urls=[])
    cards, quote_bank = frame_pm([low, high, dropped], FusionResult())
    assert [c.title for c in cards] == ["High", "Low"]
    assert all(c.score > 0 for c in cards)
    assert len(cards) == 2                       # unverified excluded
    assert any("High quote" in q for q in quote_bank)


def test_opportunity_line_references_pain():
    cards, _ = frame_pm([_vpp("Slow export", 4, ["https://a.com/1"])], FusionResult())
    assert "Slow export" in cards[0].pain
    assert cards[0].opportunity
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_frame.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/frame.py
"""Stage 4 (pm lens) — verified pain points → ranked opportunity cards + quote bank."""

from dataclasses import dataclass
from urllib.parse import urlparse

from council.discovery.fusion import FusionResult
from council.discovery.verify import VerifiedPainPoint


@dataclass
class IdeaCard:
    title: str
    who: str
    pain: str
    workaround: str
    opportunity: str
    evidence_urls: list[str]
    quotes: list[str]
    score: float
    corroboration: int


def _domains(urls: list[str]) -> int:
    return len({urlparse(u).netloc for u in urls if u})


def frame_pm(verified: list[VerifiedPainPoint], fusion_result: FusionResult) -> tuple[list[IdeaCard], list[str]]:
    cards: list[IdeaCard] = []
    quote_bank: list[str] = []
    seen_q: set[str] = set()
    for v in verified:
        if not v.verified:
            continue
        pt = v.point
        corr = _domains(v.supporting_urls)
        score = float(pt.intensity or 1) * (1 + corr)
        cards.append(IdeaCard(
            title=pt.title,
            who=pt.segment or "users",
            pain=f"{pt.title}: {pt.summary}",
            workaround="(from evidence — see quotes)",
            opportunity=f"Ship a capability that removes '{pt.title}' for {pt.segment or 'users'}.",
            evidence_urls=v.supporting_urls,
            quotes=pt.quotes,
            score=score,
            corroboration=corr,
        ))
        for q, u in zip(pt.quotes, v.supporting_urls + [""] * len(pt.quotes)):
            line = f'"{q}" — {u}'.rstrip(" —")
            if line not in seen_q:
                seen_q.add(line)
                quote_bank.append(line)
    cards.sort(key=lambda c: c.score, reverse=True)
    return cards, quote_bank
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_frame.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/frame.py tests/discovery/test_frame.py
git commit -m "feat(discovery): pm-lens framing — ranked opportunity cards + quote bank"
```

---

## Task 12: Render markdown idea ledger

**Files:**
- Create: `tools/llm-council/council/discovery/render.py`
- Test: `tools/llm-council/tests/discovery/test_render.py`

**Interfaces:**
- Consumes: `IdeaCard` (T11), `FusionResult` (T5).
- Produces: `render_ledger(*, topic, lens, tier, cards, quote_bank, fusion_result, cost_usd, dropped_count) -> str`. Sections: title/meta, ranked opportunity cards (with evidence links + score), blind-spot/whitespace map, contradiction map, quote bank, cost summary (incl. dropped-by-verify count).

- [ ] **Step 1: Write the failing test**

```python
# tests/discovery/test_render.py
from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult
from council.discovery.render import render_ledger


def test_render_includes_all_sections():
    cards = [IdeaCard("Slow export", "PMs", "Slow export: s", "wa", "opp",
                      ["https://a.com/1"], ['"slow"'], 8.0, 1)]
    fr = FusionResult(blind_spots=["no SSO talk"], contradictions=["mobile vs desktop"])
    md = render_ledger(topic="pm tools", lens="pm", tier="standard", cards=cards,
                       quote_bank=['"slow" — https://a.com/1'], fusion_result=fr,
                       cost_usd=0.91, dropped_count=2)
    assert "# Idea Ledger — pm tools" in md
    assert "Slow export" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "no SSO talk" in md
    assert "Quote Bank" in md and "Contradiction" in md
    assert "$0.91" in md and "dropped by verification: 2" in md
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/render.py
"""Render the idea ledger markdown artifact."""

from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult


def render_ledger(*, topic: str, lens: str, tier: str, cards: list[IdeaCard],
                  quote_bank: list[str], fusion_result: FusionResult,
                  cost_usd: float, dropped_count: int) -> str:
    L: list[str] = []
    L.append(f"# Idea Ledger — {topic}\n")
    L.append(f"- **Lens:** `{lens}`  **Tier:** `{tier}`  **Verified ideas:** {len(cards)}")
    L.append(f"- **Cost:** ${cost_usd:.2f}  ·  Pain points dropped by verification: {dropped_count}\n")

    L.append("## Ranked Opportunities\n")
    if not cards:
        L.append("_No pain points survived verification. Low verifiable signal — widen the topic or raise the tier._\n")
    for i, c in enumerate(cards, 1):
        L.append(f"### {i}. {c.title}  ·  score {c.score:.1f}")
        L.append(f"- **Who:** {c.who}")
        L.append(f"- **Pain:** {c.pain}")
        L.append(f"- **Opportunity:** {c.opportunity}")
        L.append(f"- **Corroboration:** {c.corroboration} source domain(s)")
        L.append("- **Evidence:** " + ", ".join(c.evidence_urls))
        L.append("")

    L.append("## Blind-spot / Whitespace Map\n")
    L.extend(f"- {b}" for b in (fusion_result.blind_spots or ["_(none surfaced)_"]))
    L.append("")
    L.append("## Contradiction Map\n")
    L.extend(f"- {c}" for c in (fusion_result.contradictions or ["_(none surfaced)_"]))
    L.append("")
    L.append("## Quote Bank\n")
    L.extend(f"- {q}" for q in (quote_bank or ["_(empty)_"]))
    L.append("")
    L.append("## Cost Summary\n")
    L.append(f"- Approx cost: ${cost_usd:.2f}")
    L.append(f"- Pain points dropped by verification: {dropped_count}")
    return "\n".join(L)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_render.py -v`
Expected: PASS (1 test).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/render.py tests/discovery/test_render.py
git commit -m "feat(discovery): idea-ledger markdown renderer"
```

---

## Task 13: Pipeline orchestrator

**Files:**
- Create: `tools/llm-council/council/discovery/pipeline.py`
- Test: `tools/llm-council/tests/discovery/test_pipeline.py`

**Interfaces:**
- Consumes: all of the above.
- Produces:
  - `DiscoveryResult(markdown, cost_usd, verified_count, dropped_count, session)` dataclass.
  - `async run_discovery(*, topic, lens, tier, api_key, gather_fn=None, fuse_fn=None, sessions_dir=None) -> DiscoveryResult`. Flow: `gather_evidence` → `fuse` → `verify_pain_points` → `frame_pm` → `render_ledger`. `dropped_count = len(verified) - sum(verified flags)`. On empty bundle, skip fuse and render the low-signal ledger. `gather_fn`/`fuse_fn` injectable for tests. Writes session JSON if `sessions_dir` given.
- Cost estimate (post-run): `_estimate_cost(fusion_result, tier)` = token cost via `DISCOVERY_PRICING` + `len(panel) * max_tool_calls * WEB_QUERY_PRICE`. Pricing constants live here.

- [ ] **Step 1: Write the failing test (injected gather + fuse)**

```python
# tests/discovery/test_pipeline.py
import pytest
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.pipeline import run_discovery


@pytest.mark.asyncio
async def test_pipeline_end_to_end_drops_unverified():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
            CandidatePainPoint("Fabricated", "s", ["never said this"], ["https://fake.com/x"], intensity=4),
        ], blind_spots=["no SSO"], tokens_in=1000, tokens_out=300, web_calls=4)

    res = await run_discovery(topic="pm tools", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert res.verified_count == 1
    assert res.dropped_count == 1
    assert "Export loss" in res.markdown
    assert "Fabricated" not in res.markdown
    assert res.cost_usd > 0


@pytest.mark.asyncio
async def test_empty_bundle_renders_low_signal():
    async def gather_fn(**kw):
        return EvidenceBundle()
    res = await run_discovery(topic="x", lens="pm", tier="quick",
                              api_key="k", gather_fn=gather_fn, fuse_fn=None)
    assert res.verified_count == 0
    assert "Low verifiable signal" in res.markdown or "No pain points survived" in res.markdown
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -v`
Expected: FAIL — `ModuleNotFoundError`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/pipeline.py
"""4-stage orchestrator: gather → fuse → verify → frame → render."""

import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from council.discovery.fusion import FusionResult, fuse as _fuse
from council.discovery.frame import frame_pm
from council.discovery.gather import gather_evidence
from council.discovery.render import render_ledger
from council.discovery.tiers import get_tier
from council.discovery.verify import verify_pain_points

# Per-1k-token blended prices (USD) and per-web-query price for cost estimation.
DISCOVERY_PRICE_IN_PER_1K = 0.003
DISCOVERY_PRICE_OUT_PER_1K = 0.015
WEB_QUERY_PRICE = 0.012


@dataclass
class DiscoveryResult:
    markdown: str
    cost_usd: float
    verified_count: int
    dropped_count: int
    session: dict


def _estimate_cost(fr: FusionResult, tier) -> float:
    tok = (fr.tokens_in / 1000.0) * DISCOVERY_PRICE_IN_PER_1K + (fr.tokens_out / 1000.0) * DISCOVERY_PRICE_OUT_PER_1K
    web = len(tier.panel) * tier.max_tool_calls * WEB_QUERY_PRICE
    return round(tok + web, 4)


async def run_discovery(*, topic: str, lens: str, tier: str, api_key: str,
                        gather_fn=None, fuse_fn=None, sessions_dir: Path | None = None) -> DiscoveryResult:
    tcfg = get_tier(tier)
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    gather = gather_fn or gather_evidence
    bundle = await gather(topic=topic, tier=tcfg, api_key=api_key)

    if not bundle.records:
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=[], quote_bank=[],
                           fusion_result=FusionResult(), cost_usd=0.0, dropped_count=0)
        return DiscoveryResult(markdown=md, cost_usd=0.0, verified_count=0, dropped_count=0,
                               session={"id": session_id, "topic": topic, "empty": True})

    fuse = fuse_fn or _fuse
    fr = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)

    verified = verify_pain_points(fr.pain_points, bundle)
    dropped = sum(1 for v in verified if not v.verified)
    cards, quote_bank = frame_pm(verified, fr)
    cost = _estimate_cost(fr, tcfg)

    md = render_ledger(topic=topic, lens=lens, tier=tier, cards=cards, quote_bank=quote_bank,
                       fusion_result=fr, cost_usd=cost, dropped_count=dropped)

    session = {
        "id": session_id, "topic": topic, "lens": lens, "tier": tier,
        "evidence_count": len(bundle.records), "verified": len(cards),
        "dropped": dropped, "cost_usd": cost,
        "blind_spots": fr.blind_spots, "contradictions": fr.contradictions,
    }
    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(session, indent=2))

    return DiscoveryResult(markdown=md, cost_usd=cost, verified_count=len(cards),
                           dropped_count=dropped, session=session)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_pipeline.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/pipeline.py tests/discovery/test_pipeline.py
git commit -m "feat(discovery): pipeline orchestrator (gather→fuse→verify→frame→render)"
```

---

## Task 14: CLI entry point

**Files:**
- Create: `tools/llm-council/council/discovery/__main__.py`
- Test: `tools/llm-council/tests/discovery/test_cli.py`

**Interfaces:**
- Consumes: `run_discovery` (T13), `budget.preflight_tool`/`record_spend` (T3), `get_tier` (T2).
- Produces: `python -m council.discovery <topic> --lens pm --tier standard --output PATH [--force] [--yes]`. Flow: tier preflight (`tool="discovery"`, daily $10/monthly $50, per-run cap = tier cap); `deep` requires `--yes` or interactive confirm; run pipeline; write markdown to `--output`; `record_spend(tool="discovery")`; print path + cost. Uses `--skip-budget-check` hidden flag for tests (mirrors council CLI).

- [ ] **Step 1: Write the failing test (CliRunner + monkeypatched pipeline)**

```python
# tests/discovery/test_cli.py
import asyncio
from click.testing import CliRunner
from council.discovery.__main__ import main
from council.discovery.pipeline import DiscoveryResult


def test_cli_writes_ledger(tmp_path, monkeypatch, fake_api_key):
    out = tmp_path / "ledger.md"

    async def fake_run(**kw):
        return DiscoveryResult(markdown="# Idea Ledger — x\nok", cost_usd=0.42,
                               verified_count=1, dropped_count=0, session={"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)

    res = CliRunner().invoke(main, [
        "roadmap tools", "--lens", "pm", "--tier", "quick",
        "--output", str(out), "--skip-budget-check",
    ])
    assert res.exit_code == 0, res.output
    assert out.read_text().startswith("# Idea Ledger")
    assert "0.42" in res.output


def test_cli_deep_requires_confirmation(tmp_path, monkeypatch, fake_api_key):
    async def fake_run(**kw):
        return DiscoveryResult("md", 3.0, 1, 0, {"id": "s"})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", fake_run)
    res = CliRunner().invoke(main, [
        "x", "--tier", "deep", "--output", str(tmp_path / "o.md"),
        "--skip-budget-check",
    ], input="n\n")
    assert res.exit_code != 0 or "aborted" in res.output.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_cli.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.__main__'`.

- [ ] **Step 3: Write minimal implementation**

```python
# council/discovery/__main__.py
"""`python -m council.discovery` — fusion-discovery-council CLI."""

import asyncio
import os
import sys
from datetime import date
from pathlib import Path

import click
from rich.console import Console

from council.budget import BudgetExceeded, preflight_tool, record_spend
from council.discovery.pipeline import run_discovery
from council.discovery.tiers import get_tier

console = Console()
DISCOVERY_DAILY_CAP = 10.0
DISCOVERY_MONTHLY_CAP = 50.0


@click.command()
@click.argument("topic")
@click.option("--lens", type=click.Choice(["pm", "substack"]), default="pm")
@click.option("--tier", type=click.Choice(["quick", "standard", "deep"]), default="standard")
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--force", is_flag=True, help="Bypass per-run cap (daily/monthly still enforced).")
@click.option("--yes", is_flag=True, help="Auto-confirm deep-tier cost.")
@click.option("--skip-budget-check", is_flag=True, hidden=True)
def main(topic, lens, tier, output, force, yes, skip_budget_check):
    tcfg = get_tier(tier)

    if tier == "deep" and not yes:
        if not click.confirm(f"deep tier may cost up to ${tcfg.max_cost_per_run:.2f}. Proceed?"):
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(1)

    if not skip_budget_check:
        try:
            preflight_tool(
                estimated=tcfg.max_cost_per_run * 0.6,
                per_query_cap=tcfg.max_cost_per_run,
                daily_cap=DISCOVERY_DAILY_CAP, monthly_cap=DISCOVERY_MONTHLY_CAP,
                on_date=date.today(), tool="discovery", force=force,
            )
        except BudgetExceeded as e:
            console.print(f"[red]Budget rejected: {e}[/red]")
            sys.exit(2)

    api_key = os.environ.get("OPENROUTER_API_KEY", "") if not skip_budget_check else "test"
    sessions_dir = output.parent / ".discovery-sessions"

    try:
        result = asyncio.run(run_discovery(
            topic=topic, lens=lens, tier=tier, api_key=api_key, sessions_dir=sessions_dir,
        ))
    except Exception as e:  # surface pipeline failure cleanly
        console.print(f"[red]Discovery failed: {e}[/red]")
        sys.exit(3)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.markdown)
    if not skip_budget_check:
        record_spend(amount=result.cost_usd, profile=tier, tag=f"discovery-{lens}",
                     on_date=date.today(), tool="discovery")
    console.print(f"[green]Idea ledger written:[/green] {output}")
    console.print(f"[dim]Verified ideas: {result.verified_count} · dropped: {result.dropped_count} · ${result.cost_usd:.2f}[/dim]")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools/llm-council && uv run pytest tests/discovery/test_cli.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Run the FULL discovery suite + existing council suite (no regressions)**

Run: `cd tools/llm-council && uv run pytest -v`
Expected: PASS — all `tests/discovery/*` plus all pre-existing council tests.

- [ ] **Step 6: Commit**

```bash
git add council/discovery/__main__.py tests/discovery/test_cli.py
git commit -m "feat(discovery): CLI entry point with per-tool budget gate + deep confirm"
```

---

## Task 15: SKILL.md (make it invocable)

**Files:**
- Create: `.claude/skills/fusion-discovery-council/SKILL.md`
- Test: manual (skill files have no unit tests; validate via `python3 scripts/validate.py` at repo root).

**Interfaces:** none (documentation/activation surface).

- [ ] **Step 1: Write the SKILL.md**

Create `.claude/skills/fusion-discovery-council/SKILL.md` with YAML frontmatter and body. Frontmatter:

```yaml
---
name: fusion-discovery-council
description: Multi-model fresh-evidence discovery — mine real user pain points across last30days social + Sonar/web articles, fuse through an OpenRouter Fusion panel (Opus/GPT/Gemini/Grok), drop anything not traceable to a real fetched URL, and frame survivors as ranked, evidence-linked PM opportunities or Substack ideas. Use when Sean says "discovery research", "mine pain points", "what are users complaining about", "find substack ideas", "fresh research on X", "opportunity discovery", or "where do competitors fail". Tiered quick/standard/deep with hard $10/day $50/month caps. Skip for text critique (use llm-council), for code, or for simple lookups.
allowed-tools: Bash, Read, Write, AskUserQuestion
---
```

Body must document: the four stages; the `--lens pm|substack` and `--tier quick|standard|deep` flags; the exact CLI invocation (`cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery "<topic>" --lens pm --tier standard --output <ABS PATH>`); output path convention `vault/20_projects/research/<YYYY-MM-DD>-<topic-slug>-<lens>-idea-ledger.md`; the non-negotiable verification gate; cost discipline + that the skill NEVER `git add`s the vault (rule 8). Mirror the structure/tone of `.claude/skills/llm-council/SKILL.md` §0 path-resolution + §3 cost discipline.

- [ ] **Step 2: Validate the skill loads**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: PASS (validator accepts the new skill; no broken structure).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/fusion-discovery-council/SKILL.md
git commit -m "feat(discovery): fusion-discovery-council SKILL.md (invocable skill)"
```

---

## Task 16: Docs — CHANGELOG + count tables

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md` (Connected External Research APIs section — add a fusion-discovery-council row/paragraph)
- Modify: `README.md` (if it carries a skill count/table)

**Interfaces:** none.

- [ ] **Step 1: Add CHANGELOG entry**

Add a dated entry under the latest CHANGELOG heading describing the new skill: purpose, four-stage pipeline, tiers + caps, Fusion panel + Sonar-in-gather, fabrication gate, pm lens (substack deferred to Phase 3). Reference the spec + this plan path.

- [ ] **Step 2: Update CLAUDE.md research-APIs section**

In `CLAUDE.md`, under "Connected External Research APIs", add a short paragraph for `fusion-discovery-council` paralleling the LLM Council entry: what it is, the CLI path, tiers, caps ($10/day, $50/month, separate from council), spend file shared with council tagged `tool="discovery"`, and that it reuses the council client/budget spine.

- [ ] **Step 3: Update README skill table (if present)**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && grep -n "llm-council" README.md || echo "no README skill table reference"`
If a skill table/count exists, add the new skill; otherwise skip.

- [ ] **Step 4: Validate + commit**

Run: `cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py`
Expected: PASS.

```bash
git add CHANGELOG.md CLAUDE.md README.md
git commit -m "docs: register fusion-discovery-council (CHANGELOG + CLAUDE.md + README)"
```

---

## Self-Review (completed during plan authoring)

**Spec coverage (Phase 1 scope):**
- Evidence → idea pipeline ✅ (T1, T11, T13) · GATHER last30+Sonar+web ✅ (T6–T9) · FUSE ✅ (T4–T5) · VERIFY fabrication gate ✅ (T10) · FRAME pm lens ✅ (T11) · idea ledger + quote bank + blind-spot/contradiction map ✅ (T12) · tiers + panels w/ Sonar-in-gather ✅ (T2) · per-tool caps $10/$50 ✅ (T3, T14) · output path + no vault git-add ✅ (T15) · CLI ✅ (T14) · docs ✅ (T16).
- **Deferred to follow-on plans (out of Phase 1):** review-site / GitHub-issues / intent / Q&A / trends collectors (spec §6 tier-gated rows); the `substack` lens + handoff brief (spec §5 Stage 4); Apify enhancement; autonomous mode. These depend on Phase-1 interfaces (`EvidenceRecord`, `gather_evidence`, `VerifiedPainPoint`, `frame_*`) and will be planned once those are real, to avoid speculative code.

**Placeholder scan:** every code/test step carries complete code; no TBD/TODO. Task 4 is an intentional spike that writes a captured-schema doc (not code) and de-risks Task 5.

**Type consistency:** `EvidenceRecord`/`EvidenceBundle` (T1) used identically in T5–T13; `CandidatePainPoint`/`FusionResult` (T5) consumed by T10/T11/T13; `VerifiedPainPoint` (T10) → `frame_pm` (T11) → `IdeaCard` → `render_ledger` (T12) signatures match across T13; `preflight_tool`/`record_spend(tool=...)` (T3) called consistently in T14.

---

## Phasing & Follow-on Plans

- **Phase 1 (this plan):** working `quick`/`standard`/`deep` panels, `pm` lens, core sources (last30days + Sonar + web), full verify gate, ledger, CLI, skill, docs.
- **Phase 2 (next plan):** tier-gated extended collectors — review sites + competitor-weakness mining, GitHub Issues / Canny / roadmaps, demand/intent (PAA/autocomplete), Q&A, trend velocity — each a new `gather/<source>.py` slotted into `gather_evidence`.
- **Phase 3 (next plan):** `substack` lens (`frame_substack` + handoff brief consumable by `substack-value-engine`), plus its render variant.
