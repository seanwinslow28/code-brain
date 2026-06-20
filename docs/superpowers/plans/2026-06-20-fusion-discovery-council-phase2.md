# fusion-discovery-council — Phase 2 (Harden the Slice) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the live-validated Phase 1 slice genuinely multi-source and cost-accurate: wire the two dark collectors (Brave web + last30days), make empty runs diagnosable, and fix the three budget/cost-integrity gaps (authoritative `usage.cost`, Fusion 4xx surfacing, symmetric per-tool budgets).

**Architecture:** Pure hardening of the existing `tools/llm-council/council/discovery/` subpackage — no new stages, no new lenses. Tier A makes all three Stage-1 collectors contribute real evidence and threads per-collector status into the session JSON. Tier B replaces the conservative cost *estimate* with OpenRouter's authoritative `usage.cost`, surfaces Fusion HTTP errors instead of swallowing them, and makes the council/discovery budgets isolated in both directions.

**Tech Stack:** Python ≥3.10, `httpx` (async), `click`, `pytest` + `pytest-asyncio` + `pytest-httpx`. OpenRouter Fusion + Sonar; Brave Search API; last30days `--emit=json`. Source-of-truth docs: the Phase 1 [spec](2026-06-20-fusion-discovery-council-design.md), [plan](2026-06-20-fusion-discovery-council.md), [FUSION_SCHEMA.md](../../../tools/llm-council/council/discovery/FUSION_SCHEMA.md), and the [field report](../../../tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase1-field-report.md).

## Global Constraints

- Python floor stays `>=3.10`. Reuse the council spine; do not add a second HTTP client or a second spend file.
- **Run all commands from `tools/llm-council/`.** The test command is **`uv run --extra dev python -m pytest -v`** — plain `uv run pytest` does NOT work (pytest lives in the `dev` extra). Current baseline: **66 passed, 1 skipped**; every task must keep the full suite green (no regressions) on top of its new tests.
- Fabrication gate stays sacred and untouched: every ledger pain point traces to a quote whose URL is in the evidence bundle (`needle in hay` containment only — do not loosen).
- The skill never `git add`s the `vault/` directory (CLAUDE.md rule 8).
- Verified OpenRouter model IDs (live 2026-06-20): `~google/gemini-pro-latest` (tilde = floating alias; bare form 400s), `mistralai/mistral-medium-3-5` (hyphen; dotted form 400s), plus `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, all Sonar variants. Do not reintroduce the invalid forms.
- Caps unchanged: per-run quick $0.50 / standard $1.50 / deep $4.00; discovery daily $10 / monthly $50 (tagged `tool="discovery"`); council daily $7 / monthly $40 (tagged `tool="council"`).
- Env keys available in the repo-root `.env` (gitignored, loaded via dotenv): `OPENROUTER_API_KEY`, `SCRAPECREATORS_API_KEY`, `BRAVE_API_KEY`, optional `EXA_API_KEY`.

---

## File Structure (touched in this plan)

```
tools/llm-council/council/discovery/gather/web.py      # MODIFY: add Brave provider + simple fetch fallback
tools/llm-council/council/discovery/gather/__init__.py # MODIFY: gather_evidence → (bundle, status); per-collector diagnosability
tools/llm-council/council/discovery/gather/last30.py   # REWRITE: real path + drop --agent + --emit=json parser
tools/llm-council/council/discovery/fusion.py          # MODIFY: capture usage.cost; surface HTTP errors (no 4xx retry)
tools/llm-council/council/discovery/pipeline.py        # MODIFY: thread gather status; prefer usage.cost
tools/llm-council/council/cli.py                       # MODIFY: route council preflight through preflight_tool(tool="council")
tools/llm-council/.claude/skills/.../SKILL.md (repo)   # MODIFY (Task 7): reconcile claims with reality
tests/discovery/*                                       # new + updated tests per task
```

---

## Task 1: Wire the Brave web provider

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/web.py`
- Test: `tools/llm-council/tests/discovery/test_gather_web.py` (add tests; keep existing 3 green)

**Interfaces:**
- Consumes: `EvidenceRecord`.
- Produces (new): `_default_brave_search(api_key) -> callable`, `_simple_fetch(url, timeout=20.0) -> str`. `collect_web` now selects Exa if `EXA_API_KEY` else Brave if `BRAVE_API_KEY` else returns `[]`, and falls back to fetching full page text when a result's inline text yields no complaint quotes.

**Context:** Today `collect_web` only implements Exa and only checks `EXA_API_KEY`; the docstring claims "Exa/Brave" but Brave was never built. Sean has `BRAVE_API_KEY`. Brave returns a short `description` snippet (not full text), so a fetch fallback is needed for quote density.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_gather_web.py`:

```python
import pytest
from council.discovery.gather import web as webmod
from council.discovery.gather.web import collect_web, _default_brave_search, _simple_fetch


@pytest.mark.asyncio
async def test_brave_search_normalizes(httpx_mock):
    httpx_mock.add_response(
        url="https://api.search.brave.com/res/v1/web/search?q=acme+user+complaints+problems+frustrations+2026&count=8",
        json={"web": {"results": [
            {"title": "Acme is broken", "url": "https://b.com/1",
             "description": "Users complain Acme crashes on export.", "page_age": "2026-06-10T00:00:00"},
        ]}},
    )
    search = _default_brave_search("k")
    out = await search("acme user complaints problems frustrations 2026")
    assert out[0]["url"] == "https://b.com/1"
    assert out[0]["published"] == "2026-06-10"
    assert "crashes on export" in out[0]["_text"]


@pytest.mark.asyncio
async def test_simple_fetch_strips_html(httpx_mock):
    httpx_mock.add_response(url="https://x.com/p",
                            text="<html><body><p>Exports fail silently every time.</p><script>x()</script></body></html>")
    text = await _simple_fetch("https://x.com/p")
    assert "Exports fail silently" in text
    assert "x()" not in text


@pytest.mark.asyncio
async def test_collect_web_fetch_fallback_when_snippet_has_no_quote():
    # snippet has no complaint word → fetch fallback supplies the quote
    async def search(q):
        return [{"title": "T", "url": "https://b.com/2", "published": "2026-06-15", "_text": "neutral blurb"}]
    async def fetch(u):
        return "Teams say the dashboard is painfully slow to load."
    recs = await collect_web(topic="dashboards", search=search, fetch=fetch)
    assert len(recs) == 1
    assert "painfully slow" in recs[0].quote


@pytest.mark.asyncio
async def test_collect_web_selects_brave_when_only_brave_key(monkeypatch, httpx_mock):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    monkeypatch.setenv("BRAVE_API_KEY", "bk")
    httpx_mock.add_response(  # brave search
        json={"web": {"results": [
            {"title": "T", "url": "https://b.com/3", "description": "Users hate the broken sync.", "page_age": "2026-06-01"}]}})
    recs = await collect_web(topic="sync")
    assert any(r.url == "https://b.com/3" for r in recs)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py -v`
Expected: FAIL — `ImportError: cannot import name '_default_brave_search'`.

- [ ] **Step 3: Implement**

In `council/discovery/gather/web.py`, add the imports/helpers and rewrite the provider-selection block of `collect_web`:

```python
def _default_brave_search(api_key: str):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
                params={"q": query, "count": 8},
            )
            r.raise_for_status()
            out = []
            for it in r.json().get("web", {}).get("results", []):
                out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                            "published": (it.get("page_age") or it.get("age") or "")[:10],
                            "_text": it.get("description", "")})
            return out
    return search


async def _simple_fetch(url: str, timeout: float = 20.0) -> str:
    """Best-effort full-page text for quote density. Crude tag-strip; Phase 3 may swap a real parser."""
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as c:
            r = await c.get(url, headers={"User-Agent": "Mozilla/5.0 (discovery-bot)"})
            r.raise_for_status()
            html = r.text
    except httpx.HTTPError:
        return ""
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


async def collect_web(*, topic: str, search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        if os.environ.get("EXA_API_KEY"):
            search = _default_exa_search(os.environ["EXA_API_KEY"])
            if fetch is ...:
                fetch = None  # Exa returns full _text already
        elif os.environ.get("BRAVE_API_KEY"):
            search = _default_brave_search(os.environ["BRAVE_API_KEY"])
            if fetch is ...:
                fetch = _simple_fetch  # Brave returns a snippet only
        else:
            search = None
    if fetch is ...:
        fetch = None
    if search is None:
        return []
    query = f"{topic} user complaints problems frustrations 2026"
    results = await search(query)
    recs: list[EvidenceRecord] = []
    for it in results[:max_results]:
        url = it.get("url", "")
        if not url:
            continue
        text = it.get("_text") or ""
        if not extract_quotes(text) and fetch is not None:
            text = await fetch(url)
        for q in extract_quotes(text):
            recs.append(EvidenceRecord(
                source_type="web", source_name=it.get("title", "") or "web",
                url=url, date=it.get("published", ""), quote=q, engagement=0,
            ))
    return recs
```

- [ ] **Step 4: Run the web tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py -v`
Expected: PASS (existing 3 + new 4).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/web.py tests/discovery/test_gather_web.py
git commit -m "feat(discovery): wire Brave web provider + full-page fetch fallback"
```

---

## Task 2: Diagnosable, failure-surfacing gather orchestrator

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/__init__.py`
- Modify: `tools/llm-council/council/discovery/pipeline.py` (gather call + session)
- Modify: `tools/llm-council/tests/discovery/test_gather_orchestrator.py` (existing test → tuple)
- Modify: `tools/llm-council/tests/discovery/test_pipeline.py` (fake gather_fn → tuple)

**Interfaces:**
- Changed: `gather_evidence(...) -> tuple[EvidenceBundle, dict[str, str]]`. The second element maps collector name → status string (`"ok: N records (M found)"` or `"error: <ExcType>: <repr>"`). Exceptions are logged to stderr, never swallowed silently.
- Consumed by: `pipeline.run_discovery`, which unpacks the tuple and includes `gather_status` in the session JSON (both the empty and normal branches).

**Context:** Today the orchestrator returns only a bundle and silently drops collector exceptions (`if isinstance(r, Exception): continue`). That's exactly what made the Phase 1 run #1 empty bundle undiagnosable.

- [ ] **Step 1: Write the failing test (orchestrator) + update the existing one**

Replace `tests/discovery/test_gather_orchestrator.py` with:

```python
import pytest
from council.discovery.evidence import EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence


@pytest.mark.asyncio
async def test_gather_returns_bundle_and_status():
    async def s(topic): return [EvidenceRecord("sonar", "S", "https://a/1", "", "pain a")]
    async def w(topic): return [EvidenceRecord("web", "W", "https://a/1", "", "pain a"),   # dup
                                EvidenceRecord("web", "W", "https://b/2", "", "pain b")]
    async def l(topic): raise RuntimeError("last30 down")
    bundle, status = await gather_evidence(
        topic="x", tier=get_tier("quick"), api_key="k",
        collectors={"sonar": s, "web": w, "last30": l},
    )
    assert len(bundle.records) == 2                 # dup dropped, last30 failure tolerated
    assert bundle.has_url("https://b/2")
    assert status["sonar"].startswith("ok:")
    assert "1 records" in status["web"]             # 2 found, 1 net-new after dedup
    assert status["last30"].startswith("error: RuntimeError")
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_orchestrator.py -v`
Expected: FAIL — `ValueError: too many values to unpack` (gather still returns a bare bundle).

- [ ] **Step 3: Implement the orchestrator**

Replace `council/discovery/gather/__init__.py` body:

```python
# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → (deduped bundle, per-collector status)."""

import asyncio
import sys

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str,
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
        }
    active = {name: fn for name, fn in collectors.items() if fn is not None}
    results = await asyncio.gather(*(fn(topic) for fn in active.values()), return_exceptions=True)
    bundle = EvidenceBundle()
    status: dict[str, str] = {}
    for name, r in zip(active.keys(), results):
        if isinstance(r, Exception):
            status[name] = f"error: {type(r).__name__}: {r!r}"
            print(f"[gather] collector {name!r} failed: {type(r).__name__}: {r}", file=sys.stderr)
        else:
            added = sum(1 for rec in r if bundle.add(rec))
            status[name] = f"ok: {added} records ({len(r)} found)"
    return bundle, status
```

- [ ] **Step 4: Update the pipeline to unpack + record status**

In `council/discovery/pipeline.py`, change the gather call and both session dicts:

```python
    gather = gather_fn or gather_evidence
    bundle, gather_status = await gather(topic=topic, tier=tcfg, api_key=api_key)

    if not bundle.records:
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=[], quote_bank=[],
                           fusion_result=FusionResult(), cost_usd=0.0, dropped_count=0)
        return DiscoveryResult(markdown=md, cost_usd=0.0, verified_count=0, dropped_count=0,
                               session={"id": session_id, "topic": topic, "empty": True,
                                        "gather_status": gather_status})
```

and add `gather_status` to the populated `session` dict:

```python
    session = {
        "id": session_id, "topic": topic, "lens": lens, "tier": tier,
        "evidence_count": len(bundle.records), "verified": len(cards),
        "dropped": dropped, "cost_usd": cost,
        "gather_status": gather_status,
        "blind_spots": fr.blind_spots, "contradictions": fr.contradictions,
    }
```

- [ ] **Step 5: Update the existing pipeline tests' fake gather_fn to return a tuple**

In `tests/discovery/test_pipeline.py`, change both fakes:

```python
    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}
```
and in `test_empty_bundle_renders_low_signal`:
```python
    async def gather_fn(**kw):
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
```

- [ ] **Step 6: Run the affected tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_orchestrator.py tests/discovery/test_pipeline.py -v`
Expected: PASS. Then full suite:
Run: `cd tools/llm-council && uv run --extra dev python -m pytest -v`
Expected: PASS (66+ passed, 1 skipped).

- [ ] **Step 7: Commit**

```bash
git add council/discovery/gather/__init__.py council/discovery/pipeline.py tests/discovery/test_gather_orchestrator.py tests/discovery/test_pipeline.py
git commit -m "feat(discovery): per-collector gather status + stderr logging (diagnosable empty runs)"
```

---

## Task 3: Rewrite the last30days collector (real path + flags + JSON parser)

**Files:**
- Rewrite: `tools/llm-council/council/discovery/gather/last30.py`
- Test: `tools/llm-council/tests/discovery/test_gather_last30.py` (replace)

**Interfaces:**
- Produces: `parse_last30_json(data: dict) -> list[EvidenceRecord]` (replaces `parse_last30_output`) and `async collect_last30(topic, runner=...) -> list[EvidenceRecord]`. `runner(topic) -> str` returns the raw `--emit=json` stdout (injected in tests).

**Context (the three Phase-1 bugs, from the field report):**
1. Wrong script path — the real script is `~/.claude/plugins/marketplaces/last30days-skill/scripts/last30days.py`.
2. `--agent` is not a real flag (argparse errors → empty). Correct flags: `--emit=json --quick --no-native-web`.
3. The parser was written against an *assumed* compact-text format. The real `--emit=json` shape is `report.to_dict()` from `lib/schema.py` — verified below.

**Verified `--emit=json` shape** (top-level keys `topic, range, generated_at, mode, reddit[], x[], web[], youtube[], hackernews[], ...`). Relevant item shapes:
- `reddit[]`: `{title, url, subreddit, date, engagement:{score,...}, top_comments:[{score,date,author,excerpt,url}], ...}`
- `x[]`: `{text, url, author_handle, date, engagement:{likes,...}}`
- `web[]`: `{title, url, source_domain, snippet, date}`
- `youtube[]`: `{title, url, channel_name, date, transcript_highlights:[...], engagement:{views}}`
- `hackernews[]`: `{title, url, hn_url, author, date, engagement:{score,...}, top_comments:[{excerpt,url,score,date}]}`

- [ ] **Step 1: Write the failing test (inline fixture mirrors the verified schema)**

Replace `tests/discovery/test_gather_last30.py`:

```python
import json
import pytest
from council.discovery.gather.last30 import parse_last30_json, collect_last30

SAMPLE = {
    "topic": "roadmap tools",
    "reddit": [{
        "title": "Roadmap tools all suck", "url": "https://reddit.com/r/pm/abc",
        "subreddit": "ProductManagement", "date": "2026-06-18",
        "engagement": {"score": 120, "num_comments": 30},
        "top_comments": [
            {"score": 88, "date": "2026-06-18", "author": "u/x",
             "excerpt": "Every roadmap tool forces a process my team hates", "url": "https://reddit.com/r/pm/abc/c1"},
        ],
    }],
    "x": [{"text": "Linear falls apart for cross-team OKRs", "url": "https://x.com/h/9",
           "author_handle": "pmhandle", "date": "2026-06-17", "engagement": {"likes": 50}}],
    "web": [{"title": "Why PM tools fail", "url": "https://blog.com/z", "source_domain": "blog.com",
             "snippet": "Teams complain exports break weekly.", "date": "2026-06-15"}],
    "youtube": [{"title": "PM tool rant", "url": "https://youtu.be/v", "channel_name": "PMcast",
                 "date": "2026-06-12", "transcript_highlights": ["the sprint board never syncs"],
                 "engagement": {"views": 9000}}],
    "hackernews": [{"title": "Roadmapping is broken", "url": "https://news.site/a",
                    "hn_url": "https://news.ycombinator.com/item?id=1", "author": "hnuser",
                    "date": "2026-06-10", "engagement": {"score": 200},
                    "top_comments": [{"score": 40, "date": "2026-06-10", "author": "hn2",
                                      "excerpt": "Jira's roadmap view is unusable at scale", "url": "https://news.ycombinator.com/item?id=1#c"}]}],
}


def test_parse_extracts_all_source_types():
    recs = parse_last30_json(SAMPLE)
    types = {r.source_type for r in recs}
    assert {"reddit", "x", "web", "youtube", "hn"} <= types
    reddit_comment = next(r for r in recs if "forces a process" in r.quote)
    assert reddit_comment.url == "https://reddit.com/r/pm/abc/c1"   # comment's own url, not the thread
    assert reddit_comment.engagement == 88
    x_rec = next(r for r in recs if r.source_type == "x")
    assert x_rec.url == "https://x.com/h/9" and x_rec.engagement == 50


def test_parser_tolerates_missing_sections():
    assert parse_last30_json({"topic": "x"}) == []


@pytest.mark.asyncio
async def test_collect_uses_injected_runner_and_parses_json():
    async def fake_runner(topic):
        return json.dumps(SAMPLE)
    recs = await collect_last30("roadmap tools", runner=fake_runner)
    assert len(recs) >= 5


@pytest.mark.asyncio
async def test_collect_returns_empty_on_runner_failure():
    async def boom(topic):
        raise FileNotFoundError("no script")
    assert await collect_last30("x", runner=boom) == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_last30.py -v`
Expected: FAIL — `ImportError: cannot import name 'parse_last30_json'`.

- [ ] **Step 3: Rewrite the collector**

Replace `council/discovery/gather/last30.py`:

```python
"""Collector: shell out to last30days --emit=json and parse its report into evidence.

Real script: ~/.claude/plugins/marketplaces/last30days-skill/scripts/last30days.py
JSON shape: report.to_dict() from that skill's lib/schema.py.
"""

import asyncio
import json
import shutil
from pathlib import Path

from council.discovery.evidence import EvidenceRecord


def _eng(item: dict, *keys: str) -> int:
    e = item.get("engagement") or {}
    for k in keys:
        v = e.get(k)
        if v:
            return int(v)
    return 0


def parse_last30_json(data: dict) -> list[EvidenceRecord]:
    recs: list[EvidenceRecord] = []

    for it in data.get("reddit", []):
        sub = it.get("subreddit", "")
        name = f"r/{sub}" if sub else "reddit"
        url, date = it.get("url", ""), it.get("date") or ""
        if url and it.get("title"):
            recs.append(EvidenceRecord("reddit", name, url, date, it["title"], _eng(it, "score", "num_comments")))
        for c in it.get("top_comments", []):
            cu, ex = c.get("url") or url, c.get("excerpt", "")
            if cu and ex:
                recs.append(EvidenceRecord("reddit", name, cu, c.get("date") or date, ex, int(c.get("score") or 0)))

    for it in data.get("x", []):
        url, txt = it.get("url", ""), it.get("text", "")
        if url and txt:
            recs.append(EvidenceRecord("x", it.get("author_handle", "") or "x", url, it.get("date") or "", txt, _eng(it, "likes")))

    for it in data.get("web", []):
        url, sn = it.get("url", ""), it.get("snippet", "")
        if url and sn:
            recs.append(EvidenceRecord("web", it.get("source_domain", "") or "web", url, it.get("date") or "", sn, 0))

    for it in data.get("youtube", []):
        url = it.get("url", "")
        for hl in it.get("transcript_highlights", []) or []:
            if url and hl:
                recs.append(EvidenceRecord("youtube", it.get("channel_name", "") or "youtube", url, it.get("date") or "", hl, _eng(it, "views")))

    for it in data.get("hackernews", []):
        url = it.get("url", "") or it.get("hn_url", "")
        name = it.get("author", "") or "hn"
        if url and it.get("title"):
            recs.append(EvidenceRecord("hn", name, url, it.get("date") or "", it["title"], _eng(it, "score", "num_comments")))
        for c in it.get("top_comments", []):
            cu, ex = c.get("url") or url, c.get("excerpt", "")
            if cu and ex:
                recs.append(EvidenceRecord("hn", name, cu, c.get("date") or "", ex, int(c.get("score") or 0)))

    return recs


def _find_last30_script() -> Path:
    candidates = [
        Path.home() / ".claude/plugins/marketplaces/last30days-skill/scripts/last30days.py",
        Path.home() / ".claude/skills/last30days/scripts/last30days.py",
        Path.home() / ".agents/skills/last30days/scripts/last30days.py",
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    raise FileNotFoundError("last30days script not found in plugin marketplace or skills dirs.")


async def _subprocess_runner(topic: str) -> str:
    script = _find_last30_script()
    py = shutil.which("python3") or "python3"
    proc = await asyncio.create_subprocess_exec(
        py, str(script), topic, "--emit=json", "--quick", "--no-native-web",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    out, _ = await asyncio.wait_for(proc.communicate(), timeout=300)
    return out.decode("utf-8", "replace")


async def collect_last30(topic: str, runner=_subprocess_runner) -> list[EvidenceRecord]:
    try:
        text = await runner(topic)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return []
    return parse_last30_json(data)
```

- [ ] **Step 4: Run the last30 tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_last30.py -v`
Expected: PASS (4 tests). Then `uv run --extra dev python -m pytest -v` → full suite green.

- [ ] **Step 5 (optional live integration check — only if `SCRAPECREATORS_API_KEY` present):**

Run once to confirm the subprocess actually returns parseable JSON:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python - <<'PY'
import asyncio, json
from council.discovery.gather.last30 import _subprocess_runner, parse_last30_json
out = asyncio.run(_subprocess_runner("project management tools"))
data = json.loads(out)
print("sources with items:", {k: len(v) for k, v in data.items() if isinstance(v, list) and v})
print("evidence records parsed:", len(parse_last30_json(data)))
PY
```
Expected: prints non-zero record count. If it errors on deps/keys, note it in the field report and proceed (unit tests already prove the parser; this only validates the live wiring).

- [ ] **Step 6: Commit**

```bash
git add council/discovery/gather/last30.py tests/discovery/test_gather_last30.py
git commit -m "fix(discovery): last30days collector — real plugin path, --emit=json parser, drop bogus --agent flag"
```

---

## Task 4: Capture and prefer the authoritative `usage.cost`

**Files:**
- Modify: `tools/llm-council/council/discovery/fusion.py` (`FusionResult` + `_to_result`)
- Modify: `tools/llm-council/council/discovery/pipeline.py` (`_estimate_cost`)
- Test: `tools/llm-council/tests/discovery/test_fusion.py` + `tests/discovery/test_pipeline.py` (add)

**Interfaces:**
- Changed: `FusionResult` gains `cost: float = 0.0`. `_to_result` reads `usage.get("cost")`. `pipeline._estimate_cost(fr, tier)` returns `fr.cost` when `> 0`, else the token+web estimate.

**Context:** the Fusion response includes `usage.cost` (exact USD; e.g. the spike's `$0.497`). Today the pipeline records a conservative token estimate; `usage.cost` is strictly more accurate and tightens cap enforcement.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_fusion.py`:

```python
@pytest.mark.asyncio
async def test_fuse_captures_usage_cost(httpx_mock):
    import json
    payload = {"pain_points": [{"title": "T", "summary": "s", "quotes": ["q"], "urls": ["https://r.com/1"]}]}
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": json.dumps(payload)}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "cost": 0.4231},
    })
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    from council.discovery import fusion
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    res = await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert res.cost == 0.4231
```

Add to `tests/discovery/test_pipeline.py`:

```python
def test_estimate_cost_prefers_usage_cost():
    from council.discovery.pipeline import _estimate_cost
    from council.discovery.fusion import FusionResult
    from council.discovery.tiers import get_tier
    fr = FusionResult(tokens_in=1000, tokens_out=300, web_calls=4, cost=0.88)
    assert _estimate_cost(fr, get_tier("standard")) == 0.88
    fr0 = FusionResult(tokens_in=1000, tokens_out=300, web_calls=4, cost=0.0)
    assert _estimate_cost(fr0, get_tier("standard")) > 0      # falls back to token estimate
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py::test_fuse_captures_usage_cost tests/discovery/test_pipeline.py::test_estimate_cost_prefers_usage_cost -v`
Expected: FAIL — `TypeError: ... unexpected keyword argument 'cost'` (FusionResult has no cost field).

- [ ] **Step 3: Implement**

In `council/discovery/fusion.py`, add `cost` to `FusionResult`:

```python
@dataclass
class FusionResult:
    pain_points: list[CandidatePainPoint] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    web_calls: int = 0
    cost: float = 0.0
```

and in `_to_result`, read it:

```python
    return FusionResult(
        pain_points=pts,
        blind_spots=list(data.get("blind_spots", [])),
        contradictions=list(data.get("contradictions", [])),
        tokens_in=usage.get("prompt_tokens", 0),
        tokens_out=usage.get("completion_tokens", 0),
        web_calls=_web_calls(usage),
        cost=float(usage.get("cost", 0.0) or 0.0),
    )
```

In `council/discovery/pipeline.py`, update `_estimate_cost`:

```python
def _estimate_cost(fr: FusionResult, tier) -> float:
    if getattr(fr, "cost", 0.0):
        return round(fr.cost, 4)                  # authoritative OpenRouter usage.cost
    tok = (fr.tokens_in / 1000.0) * DISCOVERY_PRICE_IN_PER_1K + (fr.tokens_out / 1000.0) * DISCOVERY_PRICE_OUT_PER_1K
    web = len(tier.panel) * tier.max_tool_calls * WEB_QUERY_PRICE
    return round(tok + web, 4)
```

- [ ] **Step 4: Run the new tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py tests/discovery/test_pipeline.py -v`
Expected: PASS (incl. the existing pipeline test, whose fake `FusionResult` has `cost=0.0` default → still uses the token estimate → `cost_usd > 0`). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py council/discovery/pipeline.py tests/discovery/test_fusion.py tests/discovery/test_pipeline.py
git commit -m "feat(discovery): record authoritative usage.cost (fall back to token estimate)"
```

---

## Task 5: Surface Fusion HTTP errors (no retry on 4xx)

**Files:**
- Modify: `tools/llm-council/council/discovery/fusion.py` (`fuse`)
- Test: `tools/llm-council/tests/discovery/test_fusion.py` (add)

**Interfaces:** unchanged signatures. `fuse` now raises `FusionError` with the OpenRouter error body on any `>= 400` response, and does NOT retry HTTP errors (the prompt-only retry is useless against a 400). The existing 200-but-unparseable retry is unchanged.

**Context:** today `fuse` calls `resp.raise_for_status()`, which raises a bare `httpx.HTTPStatusError` that the CLI swallows into a generic "Discovery failed" with no OpenRouter message.

- [ ] **Step 1: Write the failing test**

Add to `tests/discovery/test_fusion.py`:

```python
@pytest.mark.asyncio
async def test_fuse_surfaces_4xx_body_without_retry(httpx_mock):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    from council.discovery import fusion
    httpx_mock.add_response(status_code=400, json={"error": {"message": "max_tool_calls too high"}})
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    with pytest.raises(fusion.FusionError) as exc:
        await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert "max_tool_calls too high" in str(exc.value)
    assert "400" in str(exc.value)
    assert len(httpx_mock.get_requests()) == 1          # no retry on HTTP error
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py::test_fuse_surfaces_4xx_body_without_retry -v`
Expected: FAIL — raises `httpx.HTTPStatusError` (or makes 2 requests), not `FusionError` with the body.

- [ ] **Step 3: Implement**

In `council/discovery/fusion.py`, replace `resp.raise_for_status()` inside `fuse`'s loop with explicit handling:

```python
async def fuse(*, api_key: str, bundle: EvidenceBundle, tier: TierConfig, topic: str, timeout: float = 180.0) -> FusionResult:
    body = _build_body(bundle, tier, topic)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(2):
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            if resp.status_code >= 400:
                try:
                    msg = resp.json().get("error", {}).get("message") or resp.text
                except Exception:
                    msg = resp.text
                raise FusionError(f"OpenRouter {resp.status_code} on Fusion call (judge={tier.judge}): {msg}")
            payload = resp.json()
            choice = (payload.get("choices") or [{}])[0]
            content = choice.get("message", {}).get("content", "")
            data = _parse(content)
            if data is not None:
                return _to_result(data, payload.get("usage", {}))
            body["messages"][0]["content"] = _JUDGE_INSTRUCTION + "\n\nReturn ONLY the JSON object."
        raise FusionError("Fusion judge did not return parseable pain-point JSON after retry.")
```

- [ ] **Step 4: Run the new test + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py -v`
Expected: PASS (incl. existing `test_fuse_retries_then_raises_on_unparseable`, which uses 200 responses and is unaffected). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py tests/discovery/test_fusion.py
git commit -m "feat(discovery): surface OpenRouter Fusion HTTP errors verbatim, no retry on 4xx"
```

---

## Task 6: Symmetric per-tool budgets (council CLI → `preflight_tool`)

**Files:**
- Modify: `tools/llm-council/council/cli.py` (preflight call)
- Test: `tools/llm-council/tests/discovery/test_budget_symmetry.py` (new)

**Interfaces:** no new functions. Council's CLI preflight now calls `budget.preflight_tool(..., tool="council")` instead of `budget.preflight(...)`, so council's daily/monthly headroom is computed from council-tagged runs only — making isolation bidirectional. (Discovery already uses `preflight_tool(tool="discovery")`.)

**Context:** field-report review item 1 — `preflight` reads the file's aggregate `total`, so discovery spend currently eats into council's headroom (the reverse is already prevented). This contradicts the SKILL.md "never cross-deplete" claim. Council records spend untagged (defaults to `tool="council"`), so `preflight_tool(tool="council")` sums exactly council's runs.

- [ ] **Step 1: Write the failing test**

Create `tests/discovery/test_budget_symmetry.py`:

```python
from datetime import date
from click.testing import CliRunner
from council import budget


def test_large_discovery_spend_does_not_reject_council_run(tmp_spend_dir, fake_api_key, tmp_path, monkeypatch):
    d = date(2026, 6, 20)
    # Discovery has spent $9.50 today (well over council's $7 daily aggregate, under discovery's $10).
    budget.record_spend(amount=9.50, profile="standard", tag="disc", on_date=d, tool="discovery")

    # A council run should still pass preflight because council's own spend is $0.
    from council import cli
    monkeypatch.setattr(cli.date, "today", lambda: d)

    async def fake_run(**kw):
        from council.pipeline import CouncilSession
        from council.client import ModelResponse
        return CouncilSession(id="s", profile="variance", tag="t", user_query="q",
                              responses=[], rankings=[],
                              chairman_response=ModelResponse("m", "ok", 1, 1, 1))
    monkeypatch.setattr(cli, "run_council", fake_run)

    prompt = tmp_path / "p.txt"; prompt.write_text("hello")
    out = tmp_path / "o.md"
    res = CliRunner().invoke(cli.main, [
        "--profile", "variance", "--prompt-file", str(prompt), "--output", str(out), "--tag", "t",
    ])
    assert res.exit_code == 0, res.output
    assert "Budget rejected" not in res.output
```

> Note: `cli.date` must be patchable — `council/cli.py` already does `from datetime import date`, so `cli.date.today` is monkeypatchable. If the fake `run_council` signature differs from the real one, match the real `run_council(*, client, profile, user_query, tag, sessions_dir=None)` keyword set (it's called with `**kw`).

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_budget_symmetry.py -v`
Expected: FAIL — council's current `preflight` reads the aggregate `$9.50` total > `$7` daily cap → `Budget rejected`, exit 2.

- [ ] **Step 3: Implement**

In `council/cli.py`, change the import and the preflight call. Import:

```python
from council.budget import BudgetExceeded, preflight_tool, record_spend
```

Replace the `preflight(...)` call in `main()` with:

```python
        try:
            preflight_tool(
                estimated=rough,
                per_query_cap=p.max_cost_per_query,
                daily_cap=_load_daily_cap(),
                monthly_cap=_load_monthly_cap(),
                on_date=date.today(),
                tool="council",
                force=force,
            )
        except BudgetExceeded as e:
            console.print(f"[red]Budget rejected: {e}[/red]")
            sys.exit(2)
```

(Leave `record_spend(...)` as-is — it already defaults `tool="council"`. The legacy `preflight` function stays in `budget.py` for its own unit tests; it's simply no longer called by the CLI.)

- [ ] **Step 4: Run the new test + the existing council CLI tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_budget_symmetry.py tests/test_cli.py tests/test_budget.py -v`
Expected: PASS (new symmetry test; existing council CLI tests still green — they use `--skip-budget-check` or don't trip caps; `test_budget.py` still tests `preflight` directly). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/cli.py tests/discovery/test_budget_symmetry.py
git commit -m "fix(budget): council CLI uses per-tool preflight — discovery + council budgets fully isolated"
```

---

## Task 7: Reconcile docs with reality + final verification

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md`
- Modify: `CHANGELOG.md`
- Modify: `tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase1-field-report.md` (mark resolved items)

**Interfaces:** none (docs + final gate).

- [ ] **Step 1: Update SKILL.md §2 (GATHER) — all three collectors now live**

In `.claude/skills/fusion-discovery-council/SKILL.md`, the §2 GATHER note currently says extended collectors are deferred — that's still true, but the *core* web + last30days collectors are now wired. Edit the line "A web collector for supplementary articles." to:

```
   - A **web collector** (Exa if `EXA_API_KEY` set, else Brave) for supplementary fresh articles, with a full-page fetch fallback for quote density.
```

and confirm the `last30days` line stands (now using `--emit=json --quick`). Leave the "Extended collectors … deferred to Phase 2/3 … do not claim them" blockquote — review sites / GitHub / trends are still out.

- [ ] **Step 2: Update SKILL.md §5 (cost) — the cross-deplete claim is now true bidirectionally**

The §5 bullet already claims the two tools "never cross-deplete each other." That is now *actually enforced* (Task 6). Append to that bullet: ` (enforced bidirectionally via per-tool pre-flight as of Phase 2).` Also add a bullet: `- Recorded spend uses OpenRouter's authoritative \`usage.cost\` when available, falling back to a conservative token estimate.`

- [ ] **Step 3: Add a CHANGELOG entry**

Add a dated entry under the latest `CHANGELOG.md` heading:

```markdown
### fusion-discovery-council Phase 2 — hardened slice (2026-06-20)
- Wired the Brave web provider + full-page fetch fallback; last30days collector fixed (real plugin path, `--emit=json` parser, dropped the bogus `--agent` flag) — all three Stage-1 collectors now contribute evidence.
- Gather orchestrator returns per-collector status (logged to stderr + recorded in the session JSON) so empty runs are diagnosable.
- Cost integrity: record OpenRouter's authoritative `usage.cost`; surface Fusion HTTP errors verbatim with no retry on 4xx; council + discovery budgets now isolated bidirectionally via per-tool pre-flight.
- Plan: docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase2.md. Deferred to Phase 3+: extended collectors (review/GitHub/intent/Q&A/trends), the substack lens.
```

- [ ] **Step 4: Mark resolved items in the field report**

In `tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase1-field-report.md`, add a short "**RESOLVED in Phase 2**" note at the top of §5 (Brave + last30days now wired) and §6 items 1–4 (budget symmetry, usage.cost, 4xx surfacing, per-collector diagnosability), each referencing this plan. Do not delete the original findings — append the resolution status.

- [ ] **Step 5: Full verification gate**

Run the whole suite and the repo validator:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run --extra dev python -m pytest -v
cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py
```
Expected: pytest fully green (≥ 66 + the new Phase-2 tests passed, 1 skipped); `validate.py` passes.

- [ ] **Step 6 (optional live end-to-end — ask Sean before spending):**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "obsidian plugins" --lens pm --tier quick --output /tmp/p2-ledger.md
```
Expected: a ledger now drawing on Sonar **+ web (+ last30days if keys resolve)**; the session JSON under `/tmp/.discovery-sessions/` shows non-error `gather_status` for each collector; cost reflects `usage.cost`.

- [ ] **Step 7: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase1-field-report.md
git commit -m "docs(discovery): reconcile SKILL.md/CHANGELOG/field-report with Phase 2 hardening"
```

---

## Self-Review (completed during plan authoring)

**Coverage of the field report's Tier A + B backlog:**
- Tier A — Brave web (Task 1) ✅ · last30days path/flags/JSON parser (Task 3) ✅ · per-collector diagnosability into session JSON + stderr (Task 2) ✅.
- Tier B — symmetric per-tool budgets (Task 6) ✅ · capture+prefer `usage.cost` (Task 4) ✅ · Fusion 4xx surfacing, no-retry (Task 5) ✅.
- Out of scope (deferred, correctly): Tier C extended collectors + substack lens (Phase 3+); Tier D creative-segment qualifier; minor items 5 (frame quote-bank positional pairing), 6 (Sonar verbatim WebFetch), 7 (URL escaping in render), 8 (web_calls in estimate) — these are quality polish, tracked in the field report; not blockers and intentionally left for Phase 3 to avoid scope creep.

**Placeholder scan:** every code/test step carries complete code grounded in the real current files (re-read 2026-06-20) and the verified last30days schema; no TBD/TODO. The one live step (Task 3 Step 5) is an optional integration check, clearly gated, with the deterministic unit tests as the real gate.

**Type consistency:** `gather_evidence` tuple return (Task 2) is consumed by the pipeline + both injected test fakes updated in the same task; `FusionResult.cost` (Task 4) added before it's read in `_estimate_cost`; `parse_last30_json` (Task 3) replaces `parse_last30_output` and its only caller (`collect_last30`) is updated in the same task; `preflight_tool` (already in `budget.py` from Phase 1) is the symmetric path Task 6 wires into council's CLI.

---

## Phasing reminder

This plan is **Phase 2 (harden)** only. After it lands and a live run confirms multi-source evidence + accurate cost:
- **Phase 3:** extended tier-gated collectors (review sites + competitor-weakness mining, GitHub Issues/Canny/roadmaps, demand/intent, Q&A, trend velocity) + quote-verbatim hardening (WebFetch Sonar citations).
- **Phase 4:** the `substack` lens (`frame_substack` + handoff brief into `substack-value-engine`) + the `--segment` creative-signal qualifier.
