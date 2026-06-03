# Tier C Batch Route Wiring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the soak-validated `gemma4_26b-32k` @ Alienware into a real, cost-safe HybridRouter route — registered as a manual/opt-in **batch** route that can never silently bill the paid Claude API on a miss.

**Architecture:** Add one `[routing.task_map]` entry (`tier_c_batch_summarize`) plus a new per-route `fallback = "none"` opt-out in `HybridRouter.route()`. When the Alienware (offline ~16h/day under Pattern E) is unreachable, the route raises a dedicated `RouteUnavailable` exception instead of cascading to WoL → within-tier → paid API. No auto-consumer is wired this round; the route is callable by hand or by a future batch job. No launchd, no hardware touch.

**Tech Stack:** Python 3.11 (agents-sdk `.venv`), `httpx`, `pytest`, TOML config (`agents-sdk/config.toml`), Ollama on Alienware (`192.168.68.201:11434`).

---

## The four hard decisions (settled)

### Decision 1 — What concrete workload routes to Tier C? → **Option 1(b): register the route only; defer the auto-consumer.**

**Call:** Register a `tier_c_batch_summarize` `task_map` route now for manual/opt-in use. Do **not** wire an automatic production consumer this round.

**Rationale (not hand-waved):**
- Every candidate consumer in [vault/00_inbox/tickets.md](../../../vault/00_inbox/tickets.md) is **unbuilt and gated**:
  - "Build a $0/run local critic-synthesizer" — explicitly **GATED** ("only build after ~2 weeks of clean vault_critic nightly runs"; recent runs are `status=partial / ag_fail=5`). Also specced for **Mac Mini gemma4:e4b**, not Alienware.
  - "Build a $0/run local summarizer" for the fleet-memory namespace — also specced for **Mac Mini gemma4:e4b**.
  - "Re-add fleet-memory to daily_driver" — a read-only inject, not a batch-LLM consumer.
  None of these asks for a 26B Alienware model; they ask for the always-on Mac Mini's e4b. Hijacking them onto Tier C would be a scope and quality change Sean didn't sign off on.
- Building a consumer's internals is **explicitly out of scope** for option 1(b) (per the task brief).
- The soak validated **exactly** long-context article summarization ([2026-06-03-topic-20-tier-c-soak-closeout.md](../../../vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md)) — so a `*_summarize` route is the faithful name for what's proven.
- Registering the route (vs. leaving the soak's hardcoded constants as the only access path) converts Tier C from "a model on a box" into an **addressable, cost-safe capability**. The first real consumer — whenever one of the gated tickets is built — just calls `router.route("tier_c_batch_summarize")` and inherits the fail-fast safety below for free.

**What this is NOT:** not an auto-firing agent, not a launchd job, not a daily_driver dependency. It is a route definition + its safety contract + tests.

### Decision 2 — Fallback policy (safety-critical). → **Fail-fast. No fallback at all. Never the paid API.**

**Call:** The route sets `fallback = "none"`. On an Alienware miss it raises `RouteUnavailable` — it does **not** fire WoL, does **not** scan other tiers, and does **not** fall through to `claude_api`, even though the global `fallback_to_api = true` stays on for every other route.

**Why fail-fast and not the two alternatives:**
- **Why not fall back to a local Tier B model?** The only Tier B hosts are the MBP (`always_on = false`, frequently asleep) and the Mac Mini (whose batch model is `gemma4:e4b` — a 4B model). Silently routing a job validated on a **26B** model down to a **4B** model is an invisible quality regression the consumer never asked for. A batch job is latency-tolerant by definition — it can simply wait for the next Pattern E window rather than accept a quiet downgrade. (Also: HybridRouter's within-tier fallback only matches the **same** model name on another machine — `gemma4_26b-32k` exists nowhere but the Alienware — so "fall back to a different local model" isn't even what the current code does; it would require building new cross-model fallback logic. Out of scope and undesirable.)
- **Why not gate on an awake-window probe inside the router?** The router already health-checks the preferred machine (3s probe via `/api/tags`). That probe **is** the awake gate. Adding a separate time-window gate duplicates it and would wrongly block a route during an off-hours manual wake (Pattern E availability was a non-issue across the 9-day soak — the box was reachable every attempted day, including weekends). Let reachability, not the clock, decide.
- **Why fail-fast wins:** it exactly mirrors the soak's operating contract (`exit 2` on unreachable, no retry, no fallback target — [tier_c_soak.py:132-138](../../scripts/tier_c_soak.py)), it is the **only** option with zero surprise cloud spend and zero silent quality change, and the open ticket already anticipates it ("decide whether HybridRouter `fallback_to_api` is acceptable on that route (probably not — keep fail-fast Pattern E shape)" — tickets.md).

**How it's enforced so it can't regress:** the global `fallback_to_api` flag is shared by all routes, so we do **not** flip it. Instead `route()` checks `mapping.get("fallback") == "none"` immediately after the preferred-machine health check fails, and raises **before** the WoL / within-tier / API cascade can run. A unit test asserts the miss raises `RouteUnavailable` while `fallback_to_api` is still `True` — proving the per-route override beats the global flag and the paid API is never reached.

### Decision 3 — Scheduling reality. → **Manual / opt-in invocation inside the 7am–5pm Pattern E window. No launchd. A miss is a clean exception, never a hang or a fake datapoint.**

**Call:**
- **This round:** the route is invoked **by hand** (a REPL/CLI call, or the existing soak harness) inside the Alienware-awake window. No plist is created.
- **Miss handling:** if the Alienware is asleep, the 3s health probe fails → `route()` raises `RouteUnavailable` in well under 4 seconds. No hang (probe timeout is 3s), no WoL packet (architecturally dead — `project_alienware_wake_impossible.md`), no recorded datapoint.
- **When a real consumer is eventually built** (a future ticket, out of scope here): it should run on a launchd schedule **inside** 7am–5pm and treat `RouteUnavailable` as a **graceful skip** — log `status="skipped: alienware asleep"` (a *healthy* idle status, like the deep-researcher's `empty-queue`), **not** an `error`. It must never fabricate a datapoint for a missed window. This is stated here so the consumer author inherits the contract; it is **not** implemented now.

**Why no launchd now:** `project_fleet_no_run_at_load.md` — overnight/idle agents miss fires after machine shutdown (no `RunAtLoad` fallback). The Alienware is offline most of the day. A scheduled Tier C job would miss most fires. Until there is a real consumer, a schedule would be cargo-culted infrastructure with nothing to run.

### Decision 4 — Host / port / model-tag reconciliation. → **Config becomes the single source of truth; the route composes the endpoint from `[routing.machines.alienware]`; the soak harness is left as-is this round.**

- **Endpoint:** `[routing.machines.alienware]` already stores `host = "192.168.68.201"`, `port = 11434`; `MachineConfig.base_url` composes `http://192.168.68.201:11434` — **identical** to the soak's hardcoded `ALIENWARE_HOST`. The route's `RoutingDecision.base_url` is therefore correct with no new fields. ✔ verified, no drift.
- **Model tag:** the soak sends `gemma4_26b-32k:latest`. Ollama resolves a bare tag to `:latest`, and HybridRouter's health check strips the tag (`m["name"].split(":")[0]` → `gemma4_26b-32k`). So the **routing/config name is `gemma4_26b-32k`** (no `:latest`), which (a) matches the tag-stripped health-check name and (b) still resolves to `:latest` when a consumer puts `decision.model` into the `/api/chat` body. One name, no drift.
- **Soak harness:** **left hardcoded this round** (refactoring it is optional per scope). Its constants already match config exactly (verified above). An *optional, deferred* future cleanup could have `tier_c_soak.py` read `base_url` + model via `HybridRouter` — logged as Open Question Q4 below, not done here.
- **Pre-existing mismatch left untouched:** the alienware `models = ["qwen3-vl:8b"]` vs `sprite_vision_qa` `model = "Qwen3-VL-7B"` casing mismatch is pre-existing tech debt and **out of scope**. The new Tier C entry is internally consistent on its own (`gemma4_26b-32k` in both the models list and the task_map model field).

---

## Files touched

| Action | Path | Responsibility |
|---|---|---|
| **Edit** | [agents-sdk/lib/hybrid_router.py](../../lib/hybrid_router.py) | Add `RouteUnavailable` exception; add per-route `fallback == "none"` opt-out in `route()` (raise before WoL/within-tier/API cascade). |
| **Edit** | [agents-sdk/config.toml](../../config.toml) | Add `gemma4_26b-32k` to `[routing.machines.alienware].models`; add `tier_c_batch_summarize` `[routing.task_map]` entry with `fallback = "none"`. |
| **Test** | [agents-sdk/tests/test_hybrid_router.py](../../tests/test_hybrid_router.py) | Add tier_c fixtures + 3 tests: healthy→Alienware, unreachable→`RouteUnavailable` (NOT paid API), no-WoL-on-miss. |
| **Edit** | [CLAUDE.md](../../../CLAUDE.md) | Add a "Tier C batch route" row to the Architecture-decisions table (honest batch-only / Pattern-E / ~30 tok/s framing). |
| **Create** | `agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md` | This plan (repo file → committed). |
| **NOT touched** | `agents-sdk/scripts/tier_c_soak.py` | Soak harness stays hardcoded this round (optional config-read deferred — Q4). |
| **NOT touched** | `agents-sdk/schedules/` | No launchd plist (Pattern E + no-RunAtLoad reality; no consumer yet). |
| **NOT touched** | Alienware hardware / firmware / WoL / `wake_alienware.py` | Architecturally dead — not reopened. |
| **NOT git-added** | `vault/**` (soak closeout, `tickets.md`) | Obsidian-Git-owned per CLAUDE.md Rule 8. The tier-C ticket on tickets.md:38 may be edited to mark done, but **never `git add`-ed**. |

---

## Task 1: `RouteUnavailable` + per-route fail-fast in `route()` (TDD)

**Files:**
- Modify: `agents-sdk/lib/hybrid_router.py` (exception near line 33; `route()` body around lines 294–308)
- Test: `agents-sdk/tests/test_hybrid_router.py` (imports lines 9–13; `_make_machines` ~37–46; `_make_task_map` ~50–59)

- [ ] **Step 1: Extend the test fixtures**

In `agents-sdk/tests/test_hybrid_router.py`, add `gemma4_26b-32k` to the alienware machine's `models` list, and add the tier-C route to the task map.

In `_make_machines()`, change the alienware entry's models line:

```python
        "alienware": MachineConfig(
            name="alienware",
            host="192.168.68.201",
            port=11434,
            tier=3,
            runtime="ollama",
            always_on=False,
            models=["Qwen3-VL-7B", "gemma4_26b-32k"],
            wol_mac="AA:BB:CC:DD:EE:FF",
        ),
```

In `_make_task_map()`, add a final entry:

```python
        "comfyui_orchestration": {"model": "none", "machine": "alienware"},
        "tier_c_batch_summarize": {
            "model": "gemma4_26b-32k",
            "machine": "alienware",
            "fallback": "none",
        },
```

- [ ] **Step 2: Write the failing tests**

Update the import block at the top of the test file:

```python
from lib.hybrid_router import (
    HybridRouter,
    MachineConfig,
    MachineStatus,
    RouteUnavailable,
)
```

Add these three tests after `test_comfyui_direct_routing`:

```python
def test_route_tier_c_to_alienware_when_healthy(router: HybridRouter) -> None:
    """tier_c_batch_summarize routes to Alienware when it is awake."""
    router.set_machine_status("alienware", MachineStatus.HEALTHY)
    result = asyncio.run(router.route("tier_c_batch_summarize"))
    assert result.machine == "alienware"
    assert result.model == "gemma4_26b-32k"
    assert not result.is_fallback


def test_tier_c_unreachable_raises_never_api(router: HybridRouter) -> None:
    """When Alienware is asleep, the route fails fast — it must NOT bill the
    paid Claude API, even though the global fallback_to_api is True."""
    assert router.fallback_to_api is True  # the global default is still on
    router.set_machine_status("alienware", MachineStatus.UNHEALTHY)
    # Other machines are healthy but lack gemma4_26b-32k → must not be grabbed.
    router.set_machine_status("mac_mini", MachineStatus.HEALTHY)
    router.set_machine_status("macbook_pro", MachineStatus.HEALTHY)
    with pytest.raises(RouteUnavailable):
        asyncio.run(router.route("tier_c_batch_summarize"))


def test_tier_c_miss_sends_no_wol(router: HybridRouter, monkeypatch) -> None:
    """A fail-fast miss must not fire the (architecturally dead) WoL packet."""
    calls = []
    monkeypatch.setattr(router, "send_wol", lambda name: calls.append(name) or False)
    router.set_machine_status("alienware", MachineStatus.UNHEALTHY)
    with pytest.raises(RouteUnavailable):
        asyncio.run(router.route("tier_c_batch_summarize"))
    assert calls == []  # send_wol never called
```

- [ ] **Step 3: Run the tests to verify they fail**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_hybrid_router.py -v
```

Expected: the three new tests ERROR/FAIL with `ImportError: cannot import name 'RouteUnavailable'` (collection error). That is the expected red state.

- [ ] **Step 4: Add the `RouteUnavailable` exception**

In `agents-sdk/lib/hybrid_router.py`, immediately after the `WOLUnavailable` class (around line 38), add:

```python
class RouteUnavailable(Exception):
    """Raised when a route's preferred machine is down AND the route has
    explicitly opted out of fallback via task_map `fallback = "none"`.

    This is the cost-safety contract for routes on frequently-offline hosts
    (the Tier C batch route on the Alienware, offline ~16h/day under Pattern
    E). It guarantees a miss never silently bills the paid Claude API and
    never fires a (non-functional) Wake-on-LAN packet. Callers catch this and
    skip/defer to the next awake window — a healthy idle outcome, not an error.
    """
```

- [ ] **Step 5: Add the fail-fast branch in `route()`**

In `route()`, find the preferred-machine health block (ends with the healthy `return RoutingDecision(...)` around line 304) and the WoL block that follows:

```python
        # Try WOL for Alienware if it's the preferred machine
        if preferred_machine == "alienware":
            self.send_wol("alienware")
```

Insert the opt-out check **between** the healthy-return block and that WoL block:

```python
        # Per-route fail-fast opt-out. A task_map entry may set
        # `fallback = "none"` to forbid the entire WoL → within-tier → paid
        # API cascade when its preferred machine is unreachable. This is the
        # cost-safety contract for the Tier C batch route: the Alienware is
        # offline ~16h/day (Pattern E manual wake, 7am–5pm) and the global
        # fallback_to_api=true would otherwise SILENTLY bill the Claude API on
        # every miss. Raise before any side effect (no dead-WoL packet, no
        # cross-tier scan, no API spend). Callers defer to the next window.
        if mapping.get("fallback") == "none":
            raise RouteUnavailable(
                f"{preferred_machine} unreachable for '{task}' and route opts "
                f'out of fallback (fallback="none"); no WoL, no API spend.'
            )

        # Try WOL for Alienware if it's the preferred machine
        if preferred_machine == "alienware":
            self.send_wol("alienware")
```

(No change to `from_config` is needed — it copies `task_map` from TOML verbatim, so the new `fallback` key flows through automatically.)

- [ ] **Step 6: Run the tests to verify they pass**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_hybrid_router.py -v
```

Expected: PASS — all prior tests plus the 3 new ones green. (Adding `gemma4_26b-32k` to the fixture's alienware models list does not affect the existing sprite/comfyui tests; the existing API-fallback tests are untouched because they use routes without a `fallback` key.)

- [ ] **Step 7: Commit** — deferred to the single end-of-plan commit (Task 4 / "Commit shape"). Do not commit yet.

---

## Task 2: Register the route in `config.toml`

**Files:**
- Modify: `agents-sdk/config.toml` (alienware models line ~333; task_map block ending at `judge_layer` ~370)

- [ ] **Step 1: Add the model to the Alienware models list**

Change line ~333:

```toml
models = ["qwen3-vl:8b"]
```

to:

```toml
# gemma4_26b-32k added 2026-06-03 — Topic 20 Tier C soak ADOPTED (17/17 clean).
# Bare tag (no :latest) so it matches the tag-stripped health-check name and
# still resolves to :latest in /api/chat. See tier_c_batch_summarize below.
models = ["qwen3-vl:8b", "gemma4_26b-32k"]
```

- [ ] **Step 2: Add the task_map route**

After the `judge_layer = { ... }` entry (end of `[routing.task_map]`, ~line 370), append:

```toml
# Tier C batch route — fleet's first Tier C production model.
# Topic 20 soak ADOPTED 2026-06-03: gemma4_26b-32k @ Alienware (RTX 5080 16GB)
# passed 17/17 Pattern E datapoints clean (0 think-leak, 0 truncation, no
# drift; mean ~29.6 tok/s, workload-bound). See
# vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md.
# BATCH / ASYNC ONLY — ~30 tok/s sustained, explicitly NOT for interactive use.
# fallback = "none": the Alienware is offline ~16h/day (Pattern E manual wake,
# 7am–5pm; remote wake is architecturally impossible on this hardware). The
# global fallback_to_api=true would otherwise SILENTLY bill the paid Claude
# API on every off-hours miss. This route fails fast (raises RouteUnavailable)
# instead — no surprise cloud spend, no silent quality downgrade. A batch
# consumer catches RouteUnavailable and defers to the next awake window.
# No auto-consumer wired yet (2026-06-03) — manual / opt-in route. Plan:
# agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md
tier_c_batch_summarize = { model = "gemma4_26b-32k", machine = "alienware", fallback = "none" }
```

- [ ] **Step 3: Verify the config still parses and the route resolves through `from_config`**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
from lib.config import load_config
from lib.hybrid_router import HybridRouter
import tomllib, pathlib
cfg = tomllib.loads(pathlib.Path('config.toml').read_text())
r = HybridRouter.from_config(cfg)
m = r.task_map['tier_c_batch_summarize']
assert m == {'model': 'gemma4_26b-32k', 'machine': 'alienware', 'fallback': 'none'}, m
assert 'gemma4_26b-32k' in r.machines['alienware'].models
print('config OK:', m, '| base_url:', r.machines['alienware'].base_url)
"
```

Expected: `config OK: {'model': 'gemma4_26b-32k', 'machine': 'alienware', 'fallback': 'none'} | base_url: http://192.168.68.201:11434`

(Note: `load_config()` is imported only to confirm the module loads cleanly; the assertion path reads the raw TOML so it does not depend on `Config`'s internal shape. If `from_config` expects the full parsed dict, the raw `tomllib.loads` result above is exactly that shape.)

- [ ] **Step 4: Commit** — deferred to the single end-of-plan commit.

---

## Task 3: CLAUDE.md production note

**Files:**
- Modify: `CLAUDE.md` (Architecture-decisions table; insert after the "Fleet memory (Phase 1)" row at line 168)

- [ ] **Step 1: Add the table row**

Immediately after the `| Fleet memory (Phase 1) | ... |` row (line 168), add:

```markdown
| Tier C batch route | Fleet's **first Tier C production model**: `gemma4_26b-32k` @ Alienware (RTX 5080 16GB, Ollama `192.168.68.201:11434`). **Batch / async only** (~30 tok/s sustained — NOT interactive), **Pattern-E-gated** (Alienware reachable ~7am–5pm via manual wake only; remote wake architecturally impossible). Exposed as `task_map` route `tier_c_batch_summarize` with `fallback = "none"` — an off-hours miss raises `RouteUnavailable`, never the paid Claude API (cost-safety) and never a dead WoL packet. **No auto-consumer wired** (2026-06-03) — manual / opt-in route. Soak verdict: 17/17 datapoints clean. | [`agents-sdk/lib/hybrid_router.py`](agents-sdk/lib/hybrid_router.py); soak closeout [`vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md`](vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md); plan [`agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md`](agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md) |
```

- [ ] **Step 2: Verify the table renders (row count sanity)**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
grep -c "Tier C batch route" CLAUDE.md
```

Expected: `1`

- [ ] **Step 3: Commit** — deferred to the single end-of-plan commit.

---

## Task 4: Verification gates, live smoke, commit, rollback

- [ ] **Step 1: Router unit tests (the file under change)**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_hybrid_router.py -v
```

Expected: all tests PASS (existing + 3 new).

- [ ] **Step 2: Full agents-sdk test suite (with the known-hang deselected)**

The brief asks for `pytest agents-sdk/tests/`. Note: a full `pytest tests/` **hangs** on `tests/test_gemini_dr.py` (an unmocked real network call with no timeout — open ticket in tickets.md). Run the suite with that file deselected so it completes:

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -m pytest tests/ --deselect tests/test_gemini_dr.py -q
```

Expected: PASS / no failures (gemini_dr deselected). If the deselect path differs, fall back to `-k "not gemini_dr"`.

- [ ] **Step 3: Repo validator**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
python3 scripts/validate.py
```

Expected: validator passes (3 primary domain folders intact; no schema break).

- [ ] **Step 4: Live route smoke test — ONLY inside the 7am–5pm Pattern E window**

This step requires the Alienware to be physically awake. Skip it outside the window (a miss is expected and correct off-hours).

First confirm reachability + model presence:

```bash
nc -z -w 3 192.168.68.201 11434 && echo REACHABLE
curl -sS http://192.168.68.201:11434/api/tags | python3 -c "import sys,json; print([m['name'] for m in json.load(sys.stdin)['models'] if 'gemma4_26b-32k' in m['name']])"
```

Expected: `REACHABLE` and a list containing `gemma4_26b-32k:latest`.

Then exercise the real route through HybridRouter (proves the wired config resolves end-to-end, awake case):

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/python3 -c "
import asyncio, tomllib, pathlib
from lib.hybrid_router import HybridRouter, RouteUnavailable
cfg = tomllib.loads(pathlib.Path('config.toml').read_text())
r = HybridRouter.from_config(cfg)
try:
    d = asyncio.run(r.route('tier_c_batch_summarize'))
    print('AWAKE route:', d.machine, d.model, d.base_url, 'is_fallback=', d.is_fallback)
except RouteUnavailable as e:
    print('ASLEEP (fail-fast OK):', e)
"
```

Expected (awake): `AWAKE route: alienware gemma4_26b-32k http://192.168.68.201:11434 is_fallback= False`.
Expected (asleep): `ASLEEP (fail-fast OK): alienware unreachable ...` — and crucially **not** a `claude_api` decision.

(Optional, end-to-end generation proof, awake only: the existing soak harness still works unchanged — `PYTHONPATH=. .venv/bin/python3 scripts/tier_c_soak.py --workload summarize --dry-run`.)

- [ ] **Step 5: Single focused commit (repo files only)**

Commit only the four repo files. **Do not `git add` any `vault/**` path** (the soak closeout report and `tickets.md` are Obsidian-Git-owned — CLAUDE.md Rule 8).

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add agents-sdk/lib/hybrid_router.py \
        agents-sdk/config.toml \
        agents-sdk/tests/test_hybrid_router.py \
        CLAUDE.md \
        agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md
git status   # confirm NO vault/ files are staged
git commit -m "$(cat <<'EOF'
feat(routing): wire gemma4_26b-32k Tier C batch route (fail-fast, no API spend)

Topic 20 soak ADOPTED 2026-06-03 (gemma4_26b-32k @ Alienware, 17/17 clean).
Register the fleet's first Tier C production model as a manual/opt-in batch
route — no auto-consumer this round.

- hybrid_router.py: add RouteUnavailable + per-route `fallback = "none"`
  opt-out. A miss on such a route raises before the WoL/within-tier/API
  cascade, so the Alienware (offline ~16h/day, Pattern E) can never silently
  bill the paid Claude API despite the global fallback_to_api=true.
- config.toml: add gemma4_26b-32k to alienware models + tier_c_batch_summarize
  task_map entry (fallback="none"). Bare model tag matches the tag-stripped
  health-check name and resolves to :latest in /api/chat — no drift.
- tests: healthy->Alienware, unreachable->RouteUnavailable (asserts NOT the
  paid API while fallback_to_api stays True), no-WoL-on-miss.
- CLAUDE.md: Tier C batch route row (batch-only, ~30 tok/s, Pattern-E-gated).

Batch/async only — not interactive. No launchd (Pattern E + no RunAtLoad).
Soak harness left hardcoded (its constants already match config).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
EOF
)"
```

(If on the default `main` branch and the user wants a PR, branch first — but per CLAUDE.md the vault auto-commits to `main`, so a direct commit of repo files on `main` is consistent with the repo's norm. Confirm with Sean before pushing.)

- [ ] **Step 6: Mark the ticket done (vault — NEVER `git add`)**

Optionally edit [vault/00_inbox/tickets.md](../../../vault/00_inbox/tickets.md) to move the "Tier C soak ADOPTED … wire it as a Tier C batch route" bullet (line 38) from `## Todo` to `## Done`. This is a vault file — Obsidian-Git commits it automatically. **Do not `git add` it.**

---

## Rollback

Clean revert — no launchd to uninstall, no hardware to touch, no migrations:

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git revert <commit-sha>
```

This removes the `RouteUnavailable` class, the `route()` opt-out branch, the `config.toml` route + models-list addition, the tests, and the CLAUDE.md row in one step. The route simply ceases to exist; every other route is unaffected (the global `fallback_to_api` was never changed). Vault artifacts under `vault/health/tier-c-soak*` stay (vault-owned historical record, harmless). If a partial rollback is wanted, delete just the `tier_c_batch_summarize` line from `[routing.task_map]` — with the route gone, any caller falls through to the existing "unknown task" path (global API fallback), so remove callers first if that matters.

---

## Open questions (surfaced, not silently resolved)

- **Q1 (consumer):** This plan registers the route only and defers the auto-consumer (Decision 1, option 1(b)). Confirm Sean is OK with no production agent calling Tier C yet — the first consumer arrives when one of the gated tickets (local critic-synthesizer / fleet-memory curator) is built, and those are currently specced for **Mac Mini gemma4:e4b**, not this 26B model. If Sean wants Tier C to be a candidate runtime for one of those, that's a separate scoping decision.
- **Q2 (route name):** `tier_c_batch_summarize` is named for the validated workload (summarization). If Tier C should host non-summarization batch work later, a more generic `tier_c_batch` name (or multiple per-workload routes) may be cleaner. Renaming is a trivial config + test edit; chosen the specific name to avoid over-claiming what's been soaked.
- **Q3 (miss signal — raise vs sentinel):** This plan raises `RouteUnavailable` on a fail-fast miss (consistent with the existing `WOLUnavailable` exception style and the soak's exit-code contract). The alternative is returning a sentinel `RoutingDecision(machine="unavailable")`. Raising forces the caller to handle the miss explicitly; confirm that's the preferred ergonomics for the eventual consumer.
- **Q4 (soak harness config-read):** The soak harness keeps its hardcoded `ALIENWARE_HOST` / `MODEL_TAG` this round (they already match config exactly). An optional future cleanup could have `tier_c_soak.py` read `base_url` + model via `HybridRouter` so there is one source of truth. Deferred — flag if Sean wants it folded in.
