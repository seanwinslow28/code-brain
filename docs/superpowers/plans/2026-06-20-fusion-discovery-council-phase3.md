# fusion-discovery-council — Phase 3 (Live Reliability) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make live discovery runs reliable: decode OpenRouter's SSE-padded Fusion responses without crashing, record the spend we actually incur even when FUSE fails, persist the session diagnostics on failure, and harden the last30 subprocess — then confirm a live e2e run end-to-end.

**Architecture:** Surgical hardening of the FUSE/failure path in the existing `council/discovery/` subpackage — no new stages, sources, or lenses. The two live e2e failures (2026-06-20) both traced to `fuse()`'s unguarded `resp.json()` choking on OpenRouter's `: OPENROUTER PROCESSING` keep-alive padding, plus the fact that a failed Fusion call bills OpenRouter but records $0 locally and leaves no session artifact. This plan fixes the decode, threads the incurred cost out through a typed failure, and persists diagnostics, then bundles the cheap same-file safe-failure nits.

**Tech Stack:** Python ≥3.10, `httpx` (async), `click`, `pytest` + `pytest-asyncio` + `pytest-httpx`. Source-of-truth: the [Phase 2 field report](../../../tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md) §5/§6, [FUSION_SCHEMA.md](../../../tools/llm-council/council/discovery/FUSION_SCHEMA.md), open tickets [tickets.md](../../../vault/00_inbox/tickets.md) lines 14–15.

## Global Constraints

- Python floor stays `>=3.10`. Reuse the council spine; no second HTTP client or spend file.
- **Run all commands from `tools/llm-council/`.** Test command: **`uv run --extra dev python -m pytest -v`** (plain `uv run pytest` does NOT work — pytest is in the `dev` extra). Baseline: **76 passed, 1 skipped**; every task keeps the full suite green.
- Fabrication gate stays sacred and untouched (`verify.py` not modified).
- The skill never `git add`s `vault/` (CLAUDE.md rule 8).
- **Cost integrity is the theme:** never bill OpenRouter and record $0. A run that incurs cost must `record_spend` that cost, success or failure.
- Caps unchanged: per-run quick $0.50 / standard $1.50 / deep $4.00; discovery daily $10 / monthly $50 (`tool="discovery"`); council daily $7 / monthly $40 (`tool="council"`).
- Verified model IDs unchanged (`~google/gemini-pro-latest`, `mistralai/mistral-medium-3-5`, etc. — do not reintroduce the bare/dotted forms).

---

## File Structure (touched in this plan)

```
tools/llm-council/council/discovery/fusion.py        # Tasks 1,2: SSE-safe decode + balanced-brace parse; FusionError carries cost
tools/llm-council/council/discovery/pipeline.py      # Task 3: DiscoveryFailed; persist session + raise typed failure on FusionError
tools/llm-council/council/discovery/__main__.py      # Task 3: record spend + echo gather_status on failure; exit 3
tools/llm-council/council/discovery/gather/last30.py # Task 4: proc.kill on timeout + stderr breadcrumbs
tools/llm-council/tests/discovery/*                   # new + updated tests per task
.claude/skills/fusion-discovery-council/SKILL.md      # Task 6: failure-mode reconciliation
CHANGELOG.md, phase2 field report                     # Task 6: changelog + RESOLVED notes
```

---

## Task 1: SSE-padding-safe Fusion response decode + prose-tolerant `_parse`

**Files:**
- Modify: `tools/llm-council/council/discovery/fusion.py`
- Test: `tools/llm-council/tests/discovery/test_fusion.py` (add)

**Interfaces:**
- Produces (new helpers): `_strip_sse_padding(text) -> str`, `_first_json_object(text) -> dict | None`, `_decode_payload(resp) -> dict`.
- Changed: `_parse(content)` now falls back to `_first_json_object` when direct/fenced parsing fails (tolerates prose around the JSON — the Run 1 failure mode). `fuse` decodes the body via `_decode_payload(resp)` instead of `resp.json()` (the Run 2 failure mode: SSE keep-alive padding).

**Context:** OpenRouter streams `: OPENROUTER PROCESSING` SSE comment lines as keep-alive padding on slow Fusion calls (panel + web tools) even on non-stream requests; `resp.json()` then raises a bare `JSONDecodeError` that escapes as an uncaught crash.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_fusion.py`:

```python
import json
import pytest
from council.discovery import fusion
from council.discovery.fusion import _strip_sse_padding, _first_json_object, _parse


def test_strip_sse_padding_removes_comment_lines():
    raw = ": OPENROUTER PROCESSING\n\n: OPENROUTER PROCESSING\n\n{\"a\": 1}"
    assert _strip_sse_padding(raw) == '{"a": 1}'


def test_first_json_object_extracts_balanced_object_from_prose():
    text = 'Sure, here you go:\n{"pain_points": [{"title": "x"}]}\nLet me know!'
    obj = _first_json_object(text)
    assert obj == {"pain_points": [{"title": "x"}]}


def test_first_json_object_handles_braces_inside_strings():
    text = '{"q": "a } b { c", "pain_points": []}'
    assert _first_json_object(text) == {"q": "a } b { c", "pain_points": []}


def test_parse_tolerates_prose_wrapped_json():
    content = 'Here are the results:\n{"pain_points": [{"title": "T"}], "blind_spots": []}\nDone.'
    assert _parse(content) == {"pain_points": [{"title": "T"}], "blind_spots": []}


@pytest.mark.asyncio
async def test_fuse_decodes_sse_padded_response(httpx_mock):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    judge = {"pain_points": [{"title": "T", "summary": "s", "quotes": ["q"], "urls": ["https://r.com/1"]}]}
    envelope = {"choices": [{"message": {"content": json.dumps(judge)}}], "usage": {"cost": 0.3}}
    padded = ": OPENROUTER PROCESSING\n\n: OPENROUTER PROCESSING\n\n" + json.dumps(envelope)
    httpx_mock.add_response(text=padded)   # text/plain → resp.json() would fail; _decode_payload recovers
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    res = await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert res.pain_points[0].title == "T"
    assert res.cost == 0.3
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py -k "sse or first_json or prose" -v`
Expected: FAIL — `ImportError: cannot import name '_strip_sse_padding'`.

- [ ] **Step 3: Implement the decode helpers + use them**

In `council/discovery/fusion.py`, add the helpers (after `OPENROUTER_URL`):

```python
def _strip_sse_padding(text: str) -> str:
    """Drop OpenRouter SSE keep-alive comment lines (": OPENROUTER PROCESSING") + blanks."""
    return "\n".join(
        ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(":")
    ).strip()


def _first_json_object(text: str) -> dict | None:
    """Return the first balanced top-level {...} object in text, or None. String-aware."""
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _decode_payload(resp) -> dict:
    """Decode a Fusion HTTP response, tolerating OpenRouter SSE keep-alive padding."""
    text = resp.text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    stripped = _strip_sse_padding(text)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        obj = _first_json_object(stripped or text)
        if isinstance(obj, dict):
            return obj
        raise FusionError("Fusion response was not decodable JSON (after SSE-padding strip).")
```

Harden `_parse`:

```python
def _parse(content: str) -> dict | None:
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        data = _first_json_object(text)            # tolerate prose around the JSON
    if isinstance(data, dict) and "pain_points" in data:
        return data
    return None
```

In `fuse`, replace `payload = resp.json()` with `payload = _decode_payload(resp)`. (Leave the 4xx branch's `resp.json()` as-is — error bodies are clean JSON.)

- [ ] **Step 4: Run the new + existing fusion tests**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py -v`
Expected: PASS (new 5 + all existing — `json=` mocks decode on the fast path, so prior tests are unaffected).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py tests/discovery/test_fusion.py
git commit -m "fix(discovery): decode SSE-padded Fusion responses + prose-tolerant JSON parse"
```

---

## Task 2: `FusionError` carries incurred cost; sum cost across attempts

**Files:**
- Modify: `tools/llm-council/council/discovery/fusion.py` (`FusionError`, `fuse`)
- Test: `tools/llm-council/tests/discovery/test_fusion.py` (add)

**Interfaces:**
- Changed: `FusionError(message, *, cost: float = 0.0)` — exposes `.cost`. `fuse` accumulates `usage.cost` across attempts and attaches the total to both the returned `FusionResult.cost` and any raised `FusionError.cost`. This fixes the cost leak (a billed-but-unparseable response now reports its cost) and the retry double-bill (two billed attempts now sum).

**Context:** field report §5 — a failed Fusion call bills OpenRouter but the cost never reaches `record_spend`; and the reprompt-retry can bill twice while only the last attempt's cost would be recorded.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_fusion.py`:

```python
@pytest.mark.asyncio
async def test_fuse_failure_carries_summed_cost(httpx_mock):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    # Two 200 responses, both valid envelopes but content lacks pain_points → unparseable twice.
    for c in (0.10, 0.12):
        httpx_mock.add_response(json={"choices": [{"message": {"content": "no json here"}}], "usage": {"cost": c}})
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    with pytest.raises(fusion.FusionError) as exc:
        await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert round(exc.value.cost, 4) == 0.22          # billed both attempts


@pytest.mark.asyncio
async def test_fuse_success_after_retry_sums_cost(httpx_mock):
    import json
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    httpx_mock.add_response(json={"choices": [{"message": {"content": "garbage"}}], "usage": {"cost": 0.10}})
    good = {"pain_points": [{"title": "T", "summary": "s", "quotes": ["q"], "urls": ["https://r.com/1"]}]}
    httpx_mock.add_response(json={"choices": [{"message": {"content": json.dumps(good)}}], "usage": {"cost": 0.12}})
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    res = await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert round(res.cost, 4) == 0.22
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py -k "summed_cost or after_retry" -v`
Expected: FAIL — `TypeError: FusionError() got an unexpected keyword argument 'cost'` / `AttributeError: 'FusionError' object has no attribute 'cost'`.

- [ ] **Step 3: Implement**

Redefine `FusionError` and update `fuse`'s accumulation in `council/discovery/fusion.py`:

```python
class FusionError(Exception):
    def __init__(self, message: str, *, cost: float = 0.0):
        super().__init__(message)
        self.cost = cost
```

```python
async def fuse(*, api_key: str, bundle: EvidenceBundle, tier: TierConfig, topic: str, timeout: float = 180.0) -> FusionResult:
    body = _build_body(bundle, tier, topic)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    total_cost = 0.0
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(2):
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            if resp.status_code >= 400:
                try:
                    msg = resp.json().get("error", {}).get("message") or resp.text
                except Exception:
                    msg = resp.text
                raise FusionError(f"OpenRouter {resp.status_code} on Fusion call (judge={tier.judge}): {msg}",
                                  cost=round(total_cost, 6))
            payload = _decode_payload(resp)
            usage = payload.get("usage", {}) or {}
            total_cost += float(usage.get("cost", 0.0) or 0.0)
            content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "")
            data = _parse(content)
            if data is not None:
                res = _to_result(data, usage)
                if total_cost:
                    res.cost = round(total_cost, 6)        # sum across attempts (fixes retry double-bill)
                return res
            body["messages"][0]["content"] = _JUDGE_INSTRUCTION + "\n\nReturn ONLY the JSON object."
        raise FusionError("Fusion judge did not return parseable pain-point JSON after retry.",
                          cost=round(total_cost, 6))
```

(The decode-failure `FusionError` raised inside `_decode_payload` keeps the default `cost=0.0` — a body we couldn't decode also has no readable usage; conservative.)

- [ ] **Step 4: Run the fusion suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py -v`
Expected: PASS (new 2 + existing — single-response `test_fuse_captures_usage_cost` still yields `res.cost == 0.4231` since the sum of one attempt equals it).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py tests/discovery/test_fusion.py
git commit -m "fix(discovery): FusionError carries incurred cost; sum usage.cost across attempts"
```

---

## Task 3: Persist session + record spend on Fusion failure

**Files:**
- Modify: `tools/llm-council/council/discovery/pipeline.py` (new `DiscoveryFailed`; wrap fuse)
- Modify: `tools/llm-council/council/discovery/__main__.py` (catch `DiscoveryFailed` → record spend + echo status)
- Test: `tools/llm-council/tests/discovery/test_pipeline.py`, `tests/discovery/test_cli.py` (add)

**Interfaces:**
- Produces: `DiscoveryFailed(message, *, cost_usd: float = 0.0, session: dict | None = None)` in `pipeline.py`.
- Changed: `run_discovery` wraps the `fuse` call; on `FusionError` it writes the session JSON (with `gather_status`, `error`, `cost_usd`, `failed_stage="fuse"`) to `sessions_dir` and raises `DiscoveryFailed` carrying that cost + session. The CLI catches `DiscoveryFailed`, `record_spend`s the incurred cost (tagged `tool="discovery"`), echoes `gather_status` to the console, and exits 3.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_pipeline.py`:

```python
@pytest.mark.asyncio
async def test_fuse_failure_persists_session_and_raises_discoveryfailed(tmp_path):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.fusion import FusionError
    from council.discovery.pipeline import run_discovery, DiscoveryFailed
    import json as _json

    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))

    async def gather_fn(**kw):
        return b, {"sonar": "ok: 1 records (1 found)", "web": "error: RuntimeError: boom"}

    async def fuse_fn(**kw):
        raise FusionError("unparseable after retry", cost=0.42)

    sdir = tmp_path / ".sessions"
    with pytest.raises(DiscoveryFailed) as exc:
        await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn, sessions_dir=sdir)
    assert exc.value.cost_usd == 0.42
    assert exc.value.session["gather_status"]["sonar"].startswith("ok:")
    written = list(sdir.glob("*.json"))
    assert len(written) == 1
    data = _json.loads(written[0].read_text())
    assert data["failed_stage"] == "fuse" and data["cost_usd"] == 0.42
    assert "gather_status" in data
```

Add to `tests/discovery/test_cli.py`:

```python
def test_cli_records_spend_and_echoes_status_on_failure(tmp_path, monkeypatch, fake_api_key, tmp_spend_dir):
    from datetime import date
    from council import budget
    from council.discovery.pipeline import DiscoveryFailed

    async def boom(**kw):
        raise DiscoveryFailed("fuse blew up", cost_usd=0.42,
                              session={"gather_status": {"sonar": "ok: 3 records (3 found)"}})
    monkeypatch.setattr("council.discovery.__main__.run_discovery", boom)

    res = CliRunner().invoke(main, [
        "obsidian", "--lens", "pm", "--tier", "quick", "--output", str(tmp_path / "o.md"),
    ])
    assert res.exit_code == 3
    assert "Gather status" in res.output
    assert round(budget.tool_total_for_day(date.today(), "discovery"), 2) == 0.42
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_pipeline.py::test_fuse_failure_persists_session_and_raises_discoveryfailed tests/discovery/test_cli.py::test_cli_records_spend_and_echoes_status_on_failure -v`
Expected: FAIL — `ImportError: cannot import name 'DiscoveryFailed'`.

- [ ] **Step 3: Implement the pipeline change**

In `council/discovery/pipeline.py`, import `FusionError`, add the exception, and wrap the fuse call. Change the import line:

```python
from council.discovery.fusion import FusionResult, FusionError, fuse as _fuse
```

Add after the `DiscoveryResult` dataclass:

```python
class DiscoveryFailed(Exception):
    def __init__(self, message: str, *, cost_usd: float = 0.0, session: dict | None = None):
        super().__init__(message)
        self.cost_usd = cost_usd
        self.session = session or {}
```

Replace the `fuse` call block:

```python
    fuse = fuse_fn or _fuse
    try:
        fr = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)
    except FusionError as e:
        cost = round(getattr(e, "cost", 0.0) or 0.0, 4)
        fail_session = {
            "id": session_id, "topic": topic, "lens": lens, "tier": tier,
            "evidence_count": len(bundle.records), "gather_status": gather_status,
            "failed_stage": "fuse", "error": str(e), "cost_usd": cost,
        }
        if sessions_dir is not None:
            sessions_dir.mkdir(parents=True, exist_ok=True)
            (sessions_dir / f"{session_id}.json").write_text(json.dumps(fail_session, indent=2))
        raise DiscoveryFailed(str(e), cost_usd=cost, session=fail_session) from e
```

- [ ] **Step 4: Implement the CLI change**

In `council/discovery/__main__.py`, import `DiscoveryFailed` and add a dedicated `except` before the generic one:

```python
from council.discovery.pipeline import run_discovery, DiscoveryFailed
```

```python
    try:
        result = asyncio.run(run_discovery(
            topic=topic, lens=lens, tier=tier, api_key=api_key, sessions_dir=sessions_dir,
        ))
    except DiscoveryFailed as e:
        if not skip_budget_check and e.cost_usd > 0:
            record_spend(amount=e.cost_usd, profile=tier, tag=f"discovery-{lens}",
                         on_date=date.today(), tool="discovery")
        status = (e.session or {}).get("gather_status", {})
        console.print(f"[red]Discovery failed at fuse:[/red] {e}")
        if status:
            console.print(f"[dim]Gather status: {status}[/dim]")
        console.print(f"[dim]Recorded spend: ${e.cost_usd:.2f} (billed even though FUSE failed)[/dim]")
        sys.exit(3)
    except Exception as e:  # surface other pipeline failures cleanly (no spend incurred pre-fuse)
        console.print(f"[red]Discovery failed: {e}[/red]")
        sys.exit(3)
```

- [ ] **Step 5: Run the affected tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_pipeline.py tests/discovery/test_cli.py -v`
Expected: PASS (new 2 + existing). Then `uv run --extra dev python -m pytest -v` → full suite green.

- [ ] **Step 6: Commit**

```bash
git add council/discovery/pipeline.py council/discovery/__main__.py tests/discovery/test_pipeline.py tests/discovery/test_cli.py
git commit -m "fix(discovery): record spend + persist session diagnostics on Fusion failure"
```

---

## Task 4: last30 subprocess robustness (kill on timeout + stderr breadcrumbs)

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/last30.py`
- Test: `tools/llm-council/tests/discovery/test_gather_last30.py` (add)

**Interfaces:** unchanged signatures. `_subprocess_runner` now `proc.kill()`s + reaps the child on timeout (no orphan) and prints a one-line stderr breadcrumb when stdout is empty. `collect_last30` prints a breadcrumb when the output is non-JSON. Both still degrade to `[]`.

**Context:** field report §4/§5 — the upstream `INCLUDE_SOURCES=None` crash makes last30 return empty *silently* today; a breadcrumb makes live failures diagnosable. A timed-out child is currently never killed.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_gather_last30.py`:

```python
@pytest.mark.asyncio
async def test_collect_breadcrumb_on_non_json(capsys):
    async def runner(topic):
        return "AttributeError: 'NoneType' object has no attribute 'split'"
    recs = await collect_last30("x", runner=runner)
    assert recs == []
    assert "[last30]" in capsys.readouterr().err


@pytest.mark.asyncio
async def test_collect_empty_output_returns_empty(capsys):
    async def runner(topic):
        return "   \n"
    recs = await collect_last30("x", runner=runner)
    assert recs == []
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_last30.py -k "breadcrumb or empty_output" -v`
Expected: FAIL — no stderr breadcrumb emitted (or the blank-output path isn't guarded).

- [ ] **Step 3: Implement**

In `council/discovery/gather/last30.py`, add `import sys` at the top, then update the runner + collector:

```python
async def _subprocess_runner(topic: str) -> str:
    script = _find_last30_script()
    py = shutil.which("python3") or "python3"
    proc = await asyncio.create_subprocess_exec(
        py, str(script), topic, "--emit=json", "--quick", "--no-native-web",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    try:
        out, err = await asyncio.wait_for(proc.communicate(), timeout=300)
    except asyncio.TimeoutError:
        proc.kill()                          # reap the child so it can't orphan
        await proc.wait()
        raise
    text = out.decode("utf-8", "replace")
    if not text.strip():
        tail = (err.decode("utf-8", "replace").strip().splitlines() or ["<no stderr>"])[-1]
        print(f"[last30] empty stdout (exit {proc.returncode}); stderr tail: {tail}", file=sys.stderr)
    return text


async def collect_last30(topic: str, runner=_subprocess_runner) -> list[EvidenceRecord]:
    try:
        text = await runner(topic)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
    if not text.strip():
        return []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        print(f"[last30] non-JSON output; first 80 chars: {text.strip()[:80]!r}", file=sys.stderr)
        return []
    return parse_last30_json(data)
```

- [ ] **Step 4: Run the last30 tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_last30.py -v`
Expected: PASS (new 2 + existing 4). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/last30.py tests/discovery/test_gather_last30.py
git commit -m "fix(discovery): last30 runner kills timed-out child + emits stderr breadcrumbs"
```

---

## Task 5: Budget monthly cross-depletion regression test

**Files:**
- Test: `tools/llm-council/tests/discovery/test_budget_symmetry.py` (add)

**Interfaces:** none (test-only — closes the Phase-2 review nit that only the *daily* isolation path was regression-guarded).

- [ ] **Step 1: Write the test**

Add to `tests/discovery/test_budget_symmetry.py`:

```python
def test_prior_day_discovery_spend_does_not_deplete_council_monthly(tmp_spend_dir):
    from datetime import date
    from council import budget
    # A large discovery spend earlier this month must not reduce council's monthly headroom.
    budget.record_spend(amount=30.0, profile="standard", tag="d", on_date=date(2026, 6, 10), tool="discovery")
    budget.preflight_tool(estimated=0.50, per_query_cap=1.00, daily_cap=7.0, monthly_cap=40.0,
                          on_date=date(2026, 6, 20), tool="council")   # must not raise
    assert budget.tool_total_for_month(date(2026, 6, 20), "discovery") == 30.0
    assert budget.tool_total_for_month(date(2026, 6, 20), "council") == 0.0
```

- [ ] **Step 2: Run to verify it passes (already-correct behavior, now guarded)**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_budget_symmetry.py -v`
Expected: PASS. (This guards existing correct behavior; if it were to fail, monthly isolation would be broken.)

- [ ] **Step 3: Commit**

```bash
git add tests/discovery/test_budget_symmetry.py
git commit -m "test(budget): regression-guard monthly cross-depletion isolation"
```

---

## Task 6: Docs reconciliation + full verification + live e2e

**Files:**
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md` (§8 failure modes)
- Modify: `CHANGELOG.md`
- Modify: `tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md` (RESOLVED notes)

- [ ] **Step 1: Update SKILL.md §8 failure modes**

In `.claude/skills/fusion-discovery-council/SKILL.md`, the §8 "Discovery failed (exit 3)" bullet currently says "No ledger is written and no spend is recorded for a failed run." That is no longer fully true. Replace that bullet with:

```
- **Discovery failed at fuse** (exit 3) — the Fusion call failed (after SSE-padding-safe decode + one reprompt retry). The CLI **records the spend OpenRouter actually billed** (tagged `tool="discovery"`), **persists the session JSON** with per-collector `gather_status`, and echoes that status — so a failed run is diagnosable and never silently free. No ledger is written.
- **Discovery failed (exit 3, pre-fuse)** — a gather/setup error before any billable call; no spend recorded.
```

- [ ] **Step 2: Add a CHANGELOG entry**

Add under the latest `CHANGELOG.md` heading:

```markdown
### fusion-discovery-council Phase 3 — live reliability (2026-06-20)
- Fusion responses now decode through OpenRouter's `: OPENROUTER PROCESSING` SSE keep-alive padding (the bug that intermittently crashed live `quick`/`standard` runs); `_parse` tolerates prose-wrapped JSON.
- Cost integrity on failure: `FusionError` carries the incurred cost (summed across retry attempts); a failed Fusion call now records the spend OpenRouter billed and persists the session JSON (with per-collector `gather_status`) instead of silently recording $0.
- last30 subprocess kills timed-out children and emits stderr breadcrumbs so silent-empty runs (e.g. the upstream `INCLUDE_SOURCES=null` crash) are diagnosable.
- Plan: docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase3.md. Deferred to Phase 4+: extended collectors, the substack lens, `_simple_fetch` SSRF allow-list.
```

- [ ] **Step 3: Mark resolved items in the Phase-2 field report**

In `tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md` §5 ("Live-surfaced") and §6, append a `**RESOLVED in Phase 3**` note to the three live items (Fusion SSE robustness, failed-Fusion spend recording, `gather_status` lost on failure), each referencing this plan. Do not delete the original findings.

- [ ] **Step 4: Full verification gate**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run --extra dev python -m pytest -v
cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py
```
Expected: pytest fully green (76 + the new Phase-3 tests passed, 1 skipped); `validate.py` passes.

- [ ] **Step 5: Live e2e — the payoff (ask Sean before spending; ~$0.40–0.50)**

This is the whole point of Phase 3 — confirm a live `quick` run now survives the SSE padding end-to-end:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "obsidian plugins" --lens pm --tier quick --output /tmp/p3-ledger.md
```
Expected: a written ledger (or, if FUSE still fails for a *different* reason, a clean exit-3 with `Gather status: …` echoed + spend recorded). Then inspect the session JSON under `/tmp/.discovery-sessions/`:
- On success: `gather_status` shows non-error entries for sonar + web (last30 may show empty until the upstream `INCLUDE_SOURCES` config is fixed — tickets.md line 15), and `cost_usd` reflects `usage.cost`.
- Confirm a discovery row landed in `vault/health/council-spend-<today>.json` tagged `tool="discovery"`.

Report the outcome (success ledger, or the new failure signature if any) in a short Phase-3 field report.

- [ ] **Step 6: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase2-field-report.md
git commit -m "docs(discovery): reconcile failure-mode docs + changelog for Phase 3 live reliability"
```

---

## Self-Review (completed during plan authoring)

**Coverage of the Phase-2 field report's live blockers + bundled nits:**
- Fusion SSE-padding robustness (Task 1) ✅ · failed-Fusion spend recording (Tasks 2+3) ✅ · `gather_status` persisted on failure (Task 3) ✅ · last30 kill-on-timeout + breadcrumbs (Task 4) ✅ · monthly cross-deplete guard (Task 5) ✅ · echo gather_status to console (Task 3 CLI) ✅ · docs reconciliation + live re-test (Task 6) ✅.
- **Consciously deferred (Phase 4+):** `_simple_fetch` SSRF/redirect allow-list (security hardening, low-risk on a personal machine with Brave-sourced URLs — noted, not cheap); extended tier-gated collectors; the `substack` lens + `--segment` qualifier; Phase-1 Minor items 5–8 (frame quote-bank positional pairing, Sonar verbatim WebFetch, render URL escaping, `web_calls` in estimate). The upstream last30 `INCLUDE_SOURCES=null` fix is external config (ticketed, Sean) — Task 4 makes it diagnosable, not fixed.

**Placeholder scan:** every code/test step carries complete code grounded in the re-read current files (`fusion.py`, `pipeline.py`, `__main__.py`, `last30.py` as of 2026-06-20 post-Phase-2). No TBD/TODO. Task 6 Step 5 is a clearly-gated optional live run; the deterministic suite is the real gate.

**Type consistency:** `_decode_payload`/`_first_json_object`/`_strip_sse_padding` (Task 1) are used by `fuse` and `_parse` within the same file; `FusionError.cost` (Task 2) is read by `pipeline.run_discovery` (Task 3) which raises `DiscoveryFailed(cost_usd=...)` consumed by `__main__` (Task 3) — names/signatures match end-to-end. `record_spend(tool="discovery")`, `tool_total_for_day/month`, `preflight_tool` are the existing Phase-1/2 budget API.

---

## Phasing reminder

Phase 3 = **live reliability** only. After it lands and the live e2e produces a real ledger:
- **Phase 4:** extended tier-gated collectors (review sites + competitor-weakness mining, GitHub Issues/Canny/roadmaps, demand/intent, Q&A, trend velocity) + quote-verbatim hardening + `_simple_fetch` SSRF allow-list.
- **Phase 5:** the `substack` lens (`frame_substack` + handoff into `substack-value-engine`) + the `--segment` creative-signal qualifier.
