---
type: implementation-plan
project: prj-job-hunt-2026
artifact: vault-critic-v1
created: 2026-05-21
status: drafted-awaiting-implementation
companion_artifacts:
  - ../multi-cli-integration-patterns.md
  - ../../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
sprint_epoch: 2026-05-04
related_intent_skill: .claude/skills/intent-engineering/SKILL.md
ai-context: "Implementation plan for Pattern 1 / vault_critic — a new nightly SDK agent (03:30 daily) that shells to Codex CLI (gpt-5.5, ChatGPT Plus) and Anti-Gravity CLI (Gemini 3.1 Pro, Google personal OAuth) in parallel to produce generative critique files at vault/knowledge/expansions/{slug}.md for each newly-written concept article from the night's vault_synthesizer run. Born 2026-05-21 from Sean's complaint that the synthesizer describes what exists but cannot tell him what is missing; the integration patterns doc captured the design and smoke-test evidence, this plan converts that into TDD-ordered tasks. v1 scope: Pattern 1 only — Patterns 2 (zero-cost council profile) and 3 (HybridRouter task-class routing) are out of scope. Cost: $0 incremental on personal subscriptions. Sonnet fallback explicitly NOT in v1 — rate-cap on both CLIs marks the run partial and exits cleanly. Verification gate to mark shipped-and-verified: 3 consecutive nights with manifest populated AND median random-sample of expansion files reads as thinking-partner shape per feedback_synth_verify_against_median_not_best.md."
---

# vault_critic v1 — Pattern 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Future Sean / future Claude:** check the **Status Tracker** at the bottom before starting work. The spec is in [`../multi-cli-integration-patterns.md`](../multi-cli-integration-patterns.md) §Pattern 1; the smoke-test fixtures live in [`../multi-cli-smoke-2026-05-21/`](../multi-cli-smoke-2026-05-21/). This plan is the implementation contract.

**Goal:** Ship a new nightly SDK agent that critiques each newly-written concept article from the synthesizer's `02:30` run, fans the critique to two external CLIs (Codex + Anti-Gravity) in parallel at `$0` incremental cost, and writes sibling expansion files at `vault/knowledge/expansions/{slug}.md` that name 3 specific things Sean is missing per article.

**Architecture:** Pure-Python orchestration agent (mirrors `deep_researcher.py` topology — Claude Agent SDK is NOT used in the nightly path; the CLIs are the reasoners). Inputs: today's Mac-Mini-canonical synth-manifest + the concept article bodies. Outputs: expansion markdown files + `vault/health/critic-manifest-{date}.json` + one CSV row via `record_run`. Subprocess fan-out uses `asyncio.gather`; one CLI failing does not block the other. Trust flags + sandbox modes are set explicitly per invocation, never inherited.

**Tech Stack:** Python 3.13 (agents-sdk/.venv), `asyncio` subprocess, `subprocess.PIPE` capture, `json` for Anti-Gravity output, regex for Codex token footer, `lib.filelock.FileLock` for `vault/knowledge/expansions/.lock`, `lib.logging_setup.record_run` for CSV, `lib.config.load_config` for paths. No new third-party dependencies. External binaries: `/opt/homebrew/bin/codex` v0.130.0, `/opt/homebrew/bin/gemini` v0.42.0.

---

## Scope guard — what this plan does NOT do

These are explicit non-goals. If a task starts drifting toward any of them, stop and either log it as deferred work in the Status Tracker or break it into a separate plan.

| Non-goal | Why deferred |
|---|---|
| Pattern 2 — zero-cost council profile in `tools/llm-council/` | Reuse the wrappers shipped here, but ship the adapter classes + profile TOML in a separate plan after Pattern 1 has run ≥1 week. |
| Pattern 3 — HybridRouter `route_to_cli` for task-class routing across all four backends | Premature without ≥2 weeks of Pattern 1 + Pattern 2 production signal proving the existing single-backend agents have quality gaps worth a routing layer. |
| Sonnet 4.6 fallback when both CLIs rate-cap | Out of scope for v1 — rate-cap on both CLIs marks the run `status: partial` and exits cleanly. Isolates vault_critic from any cloud-API blast radius. Revisit after 3 consecutive nights of rate-cap evidence (none expected). |
| MBP-side deployment | Mac Mini is the always-on agent driver per v3.14.3. vault_critic runs there. MBP stays as Qwen3-14B inference backend only. |
| Convergence detection across the two CLIs | Open question #2 in [`../multi-cli-integration-patterns.md`](../multi-cli-integration-patterns.md). Cheap string-match on author names is tempting but the smoke test was n=1; ship after 5+ real runs surface enough signal to know whether convergence is meaningful or coincidental. |
| Output fencing markers (`<critique>...</critique>`) on the Codex prompt | Open question #1. Defer — Codex stdout in the smoke test was clean markdown with no preamble. Add only if production runs surface drift. |
| Article-count cap that scales with the night's synthesizer volume | Open question #3. Defer — fixed cap of 3 articles/night is the v1 default. Revisit after 1 week. |
| Expansion file regeneration when the underlying concept is rewritten | Open question #4. Defer — expansion files are snapshots in time. Snapshot is simpler; revisit if Sean reports stale expansions blocking value. |
| `skill_optimizer` footer with run-this-deeper command | Open question #5. Defer — Pattern 1 is the cheap nightly tier; `skill_optimizer` is the deep manual tier. Composition can wait. |

---

## File map

Each file has one clear responsibility. Files that change together live together.

**New files:**

```
agents-sdk/lib/cli_runners.py              # async subprocess wrappers for Codex + Anti-Gravity
agents-sdk/lib/critique_prompt.py          # builds the per-article critique prompt
agents-sdk/agents/vault_critic.py          # main agent orchestration
agents-sdk/schedules/com.sean.agent.vault-critic.plist
agents-sdk/tests/test_cli_runners.py
agents-sdk/tests/test_critique_prompt.py
agents-sdk/tests/test_vault_critic.py
agents-sdk/tests/fixtures/critic/codex-out.txt            # symlink → ../docs/multi-cli-smoke-2026-05-21/codex-out.txt
agents-sdk/tests/fixtures/critic/codex-err.txt            # symlink → ../docs/multi-cli-smoke-2026-05-21/codex-err.txt
agents-sdk/tests/fixtures/critic/gemini-out.json         # symlink → ../docs/multi-cli-smoke-2026-05-21/gemini-out.json
agents-sdk/tests/fixtures/critic/gemini-err.txt          # symlink → ../docs/multi-cli-smoke-2026-05-21/gemini-err.txt
agents-sdk/tests/fixtures/critic/critique-prompt.md      # symlink → ../docs/multi-cli-smoke-2026-05-21/critique-prompt.md
agents-sdk/prompts/vault-critic-prompt-template.md       # generalized prompt template — referenced by lib/critique_prompt.py
```

**Modified files:**

```
agents-sdk/config.toml                     # add [agents.vault_critic] block
agents-sdk/agents/daily_driver.py          # surface critic-manifest in the morning brief
agents-sdk/lib/lint_report.py              # add latest_critic_manifest + critic_health_summary
agents-sdk/lib/fleet_summary.py            # add "vault-critic" to AGENT_ORDER + AGENT_DISPLAY
CLAUDE.md                                  # agents table + active-agents count + non-negotiable rule if applicable
CHANGELOG.md                               # entry under current version Added
README.md                                  # agent counts + table
```

**Phase-D parent doc update (post-merge):**

```
vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
# Update §Follow-on layer Implementation status block to point at this plan as the canonical implementation contract.
```

---

## Phase breakdown — execution order

Each phase is independently committable and produces a working partial system. Total estimated effort: ~3h15m, cross-checking the 3h figure in `../multi-cli-integration-patterns.md` §Pattern 1 Effort estimate.

| Phase | Deliverable | Est. | Dependencies |
|---|---|---|---|
| A | CLI wrappers in `lib/cli_runners.py` with replay tests | 45m | none |
| B | Prompt builder in `lib/critique_prompt.py` | 20m | A |
| C | Target selector with PR-contamination filter | 30m | none |
| D | Main agent `agents/vault_critic.py` + critic-manifest | 45m | A, B, C |
| E | launchd plist + install_schedules.sh + config.toml | 15m | D |
| F | daily_driver morning-brief integration | 20m | D |
| G | fleet_summary + meta-agent surfacing | 10m | D |
| H | CHANGELOG + CLAUDE.md + README counts/tables | 15m | E, F, G |

---

## Phase A — CLI wrappers (`agents-sdk/lib/cli_runners.py`)

**Why this is Phase A:** every other phase depends on these wrappers. Smoke-tested behavior from `agents-sdk/docs/multi-cli-smoke-2026-05-21/` is the ground truth; the replay tests pin the parser shape so future Codex / Anti-Gravity CLI updates don't silently break the nightly path.

**Files:**
- Create: `agents-sdk/lib/cli_runners.py`
- Create: `agents-sdk/tests/test_cli_runners.py`
- Create: `agents-sdk/tests/fixtures/critic/` (directory + 5 symlinks per File map above)

### Task A1: Bootstrap test fixtures as symlinks

- [ ] **Step 1: Create fixtures directory and symlinks**

```bash
mkdir -p agents-sdk/tests/fixtures/critic
cd agents-sdk/tests/fixtures/critic
ln -s ../../../docs/multi-cli-smoke-2026-05-21/codex-out.txt codex-out.txt
ln -s ../../../docs/multi-cli-smoke-2026-05-21/codex-err.txt codex-err.txt
ln -s ../../../docs/multi-cli-smoke-2026-05-21/gemini-out.json gemini-out.json
ln -s ../../../docs/multi-cli-smoke-2026-05-21/gemini-err.txt gemini-err.txt
ln -s ../../../docs/multi-cli-smoke-2026-05-21/critique-prompt.md critique-prompt.md
cd -
ls -la agents-sdk/tests/fixtures/critic/
```

Expected: 5 symbolic links pointing into `agents-sdk/docs/multi-cli-smoke-2026-05-21/`.

- [ ] **Step 2: Commit fixture wiring**

```bash
git add agents-sdk/tests/fixtures/critic
git commit -m "test: wire smoke-test fixtures for vault_critic via symlinks"
```

### Task A2: Codex token footer parser — TDD

- [ ] **Step 1: Write the failing test**

In `agents-sdk/tests/test_cli_runners.py`:

```python
from pathlib import Path

from lib.cli_runners import parse_codex_tokens

FIXTURES = Path(__file__).parent / "fixtures" / "critic"


def test_parse_codex_tokens_from_real_stderr():
    stderr_text = (FIXTURES / "codex-err.txt").read_text(encoding="utf-8")
    tokens = parse_codex_tokens(stderr_text)
    assert tokens == 17182


def test_parse_codex_tokens_missing_footer_returns_none():
    assert parse_codex_tokens("no tokens used line here") is None


def test_parse_codex_tokens_handles_comma_thousands():
    # Codex prints 17,182 not 17182 in some terminals — match either.
    assert parse_codex_tokens("tokens used\n17,182\n") == 17182
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py::test_parse_codex_tokens_from_real_stderr -v
```

Expected: FAIL with `ImportError` or `AttributeError` — `parse_codex_tokens` doesn't exist yet.

- [ ] **Step 3: Write minimal implementation**

In `agents-sdk/lib/cli_runners.py`:

```python
"""Async subprocess wrappers for Codex CLI and Anti-Gravity CLI.

Smoke-tested 2026-05-21 — see agents-sdk/docs/multi-cli-integration-patterns.md
§Smoke Test Evidence for the ground-truth behavior. These wrappers are the
single point in the codebase that knows the CLIs' trust flags, sandbox modes,
and output shapes. Both vault_critic and (future) tools/llm-council adapters
import from here.

Trust flags / sandbox modes are set explicitly per invocation; silent reliance
on inherited env is a latent bug we are deliberately avoiding.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

_CODEX_TOKENS_RE = re.compile(r"tokens used\s*\n\s*([\d,]+)")


def parse_codex_tokens(stderr_text: str) -> int | None:
    """Return the token count from Codex's `tokens used` footer, or None.

    Codex prints `tokens used\\n<count>` at the end of stderr. The count may
    or may not contain comma thousands separators depending on terminal width.
    """
    m = _CODEX_TOKENS_RE.search(stderr_text or "")
    if not m:
        return None
    return int(m.group(1).replace(",", ""))
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/cli_runners.py agents-sdk/tests/test_cli_runners.py
git commit -m "feat(cli_runners): parse Codex tokens used footer with comma tolerance"
```

### Task A3: CLIResponse dataclass

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_cli_runners.py`:

```python
from lib.cli_runners import CLIResponse


def test_cliresponse_holds_response_and_meta():
    r = CLIResponse(
        cli="codex",
        text="hello world",
        tokens=123,
        duration_s=1.5,
        exit_code=0,
        rate_capped=False,
        error=None,
    )
    assert r.cli == "codex"
    assert r.text == "hello world"
    assert r.tokens == 123
    assert r.ok is True


def test_cliresponse_ok_false_when_exit_nonzero():
    r = CLIResponse(cli="codex", text="", tokens=None, duration_s=0.1,
                    exit_code=1, rate_capped=False, error="boom")
    assert r.ok is False


def test_cliresponse_ok_false_when_rate_capped():
    r = CLIResponse(cli="codex", text="", tokens=None, duration_s=0.1,
                    exit_code=0, rate_capped=True, error=None)
    assert r.ok is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 3 new tests FAIL with `ImportError: CLIResponse`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/lib/cli_runners.py`:

```python
@dataclass(frozen=True)
class CLIResponse:
    """Result of a single CLI invocation.

    `text` is the raw markdown response (Codex stdout or Anti-Gravity
    `response` field). `tokens` is None when the CLI did not report a
    token count. `rate_capped` is set by the wrapper when the CLI's
    stderr matches a known rate-cap signature; the caller MUST treat
    rate-capped responses as failures even if exit_code == 0.
    """

    cli: str            # "codex" or "antigravity"
    text: str
    tokens: int | None
    duration_s: float
    exit_code: int
    rate_capped: bool
    error: str | None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/cli_runners.py agents-sdk/tests/test_cli_runners.py
git commit -m "feat(cli_runners): add CLIResponse dataclass with ok property"
```

### Task A4: Rate-cap detector — heuristic stderr matcher

- [ ] **Step 1: Write the failing test**

Append:

```python
from lib.cli_runners import detect_rate_cap


def test_detect_rate_cap_codex_429_signature():
    # Anecdotal Codex rate-cap shape: "rate limit" or "quota" in stderr.
    assert detect_rate_cap("codex", "error: rate limit exceeded") is True
    assert detect_rate_cap("codex", "Error: 429 Too Many Requests") is True
    assert detect_rate_cap("codex", "your daily quota has been reached") is True


def test_detect_rate_cap_antigravity_shape():
    # Anti-Gravity surfaces quota errors as JSON-formatted stderr; the wrapper
    # also checks for "RESOURCE_EXHAUSTED" and "quota" in any case.
    assert detect_rate_cap("antigravity", "RESOURCE_EXHAUSTED: Quota exceeded") is True
    assert detect_rate_cap("antigravity", "rate limit hit, try again later") is True


def test_detect_rate_cap_negative_on_normal_stderr():
    # Smoke-test stderr was clean — no false positive.
    normal = (FIXTURES / "codex-err.txt").read_text(encoding="utf-8")
    assert detect_rate_cap("codex", normal) is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py::test_detect_rate_cap_codex_429_signature -v
```

Expected: FAIL with `ImportError: detect_rate_cap`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/lib/cli_runners.py`:

```python
_RATE_CAP_PATTERNS = (
    "rate limit",
    "429",
    "quota",
    "resource_exhausted",
    "too many requests",
)


def detect_rate_cap(cli: str, stderr_text: str) -> bool:
    """Heuristic rate-cap detector. True when stderr looks rate-capped.

    Both Codex and Anti-Gravity surface rate-cap errors as free-text or JSON
    in stderr (no consistent structured signal). We match a small set of
    case-insensitive substrings that cover the documented + anecdotal shapes.
    False positives on non-cap errors are tolerable — the run is marked
    partial either way and the wrapper logs full stderr.
    """
    lowered = (stderr_text or "").lower()
    return any(p in lowered for p in _RATE_CAP_PATTERNS)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 9 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/cli_runners.py agents-sdk/tests/test_cli_runners.py
git commit -m "feat(cli_runners): detect rate-cap signatures in CLI stderr"
```

### Task A5: `run_codex` async wrapper — fake-subprocess smoke replay

- [ ] **Step 1: Write the failing test**

Append:

```python
import asyncio
from unittest.mock import AsyncMock, patch

from lib.cli_runners import run_codex


def _fake_proc(stdout_bytes: bytes, stderr_bytes: bytes, returncode: int = 0):
    """Return a mocked asyncio subprocess that emits the given bytes."""
    proc = AsyncMock()
    proc.communicate = AsyncMock(return_value=(stdout_bytes, stderr_bytes))
    proc.returncode = returncode
    return proc


def test_run_codex_replays_smoke_fixture():
    stdout = (FIXTURES / "codex-out.txt").read_bytes()
    stderr = (FIXTURES / "codex-err.txt").read_bytes()

    async def go():
        fake = _fake_proc(stdout, stderr, returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=60)

    resp = asyncio.run(go())
    assert resp.cli == "codex"
    assert resp.tokens == 17182
    assert resp.exit_code == 0
    assert resp.rate_capped is False
    # The Codex stdout fixture starts with "1. **Add..."; assert we captured it.
    assert resp.text.startswith("1. **Add")
    assert resp.ok is True


def test_run_codex_timeout_returns_error_not_raise():
    async def go():
        async def slow_communicate():
            await asyncio.sleep(10)
            return (b"", b"")
        fake = AsyncMock()
        fake.communicate = slow_communicate
        fake.returncode = None
        fake.kill = AsyncMock()
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=0.05)

    resp = asyncio.run(go())
    assert resp.ok is False
    assert resp.error is not None
    assert "timeout" in resp.error.lower()


def test_run_codex_rate_cap_marks_response_capped():
    async def go():
        fake = _fake_proc(b"", b"Error: rate limit exceeded", returncode=1)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_codex("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.rate_capped is True
    assert resp.ok is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py::test_run_codex_replays_smoke_fixture -v
```

Expected: FAIL with `ImportError: run_codex`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/lib/cli_runners.py`:

```python
import time


CODEX_BINARY = "/opt/homebrew/bin/codex"
CODEX_DEFAULT_TIMEOUT_S = 120


async def run_codex(prompt: str, timeout_s: int = CODEX_DEFAULT_TIMEOUT_S) -> CLIResponse:
    """Invoke `codex exec` with read-only sandbox and skip-git-repo-check.

    Runs from `Path.home()` (trusted per ~/.codex/config.toml `[projects]`).
    Captures stdout (markdown response) and stderr (session metadata +
    `tokens used` footer). Returns a CLIResponse — never raises on CLI failure;
    timeouts and rate-caps surface via response fields.
    """
    cmd = [
        CODEX_BINARY,
        "exec",
        "--sandbox", "read-only",
        "--skip-git-repo-check",
        prompt,
    ]
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex binary missing: {exc}",
        )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex timeout after {timeout_s}s",
        )

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    return CLIResponse(
        cli="codex",
        text=stdout_text,
        tokens=parse_codex_tokens(stderr_text),
        duration_s=time.monotonic() - t0,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=detect_rate_cap("codex", stderr_text),
        error=None if proc.returncode == 0 else stderr_text[:500],
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 12 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/cli_runners.py agents-sdk/tests/test_cli_runners.py
git commit -m "feat(cli_runners): run_codex async wrapper with timeout + rate-cap detection"
```

### Task A6: `run_antigravity` async wrapper — JSON parsing + env-based trust

- [ ] **Step 1: Write the failing test**

Append:

```python
from lib.cli_runners import run_antigravity


def test_run_antigravity_replays_smoke_fixture():
    stdout = (FIXTURES / "gemini-out.json").read_bytes()
    stderr = (FIXTURES / "gemini-err.txt").read_bytes()

    async def go():
        fake = _fake_proc(stdout, stderr, returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)) as create:
            resp = await run_antigravity("any prompt", timeout_s=60)
            # Verify the env var was set on the subprocess call
            kwargs = create.call_args.kwargs
            env = kwargs.get("env", {})
            assert env.get("GEMINI_CLI_TRUST_WORKSPACE") == "true"
            return resp

    resp = asyncio.run(go())
    assert resp.cli == "antigravity"
    assert resp.exit_code == 0
    assert resp.rate_capped is False
    # The response field starts with "### 1. Surgical Cultural Synthesis"
    assert resp.text.startswith("### 1. Surgical Cultural Synthesis")
    # Token total from stats.models["gemini-3.1-pro-preview"].tokens.total
    assert resp.tokens == 15746
    assert resp.ok is True


def test_run_antigravity_malformed_json_marks_error():
    async def go():
        fake = _fake_proc(b"not json at all", b"", returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_antigravity("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.ok is False
    assert resp.error is not None
    assert "json" in resp.error.lower()


def test_run_antigravity_extracts_routed_model_from_stats():
    """Don't hardcode gemini-3.1-pro-preview — read from stats.models keys."""
    payload = {
        "session_id": "abc",
        "response": "body",
        "stats": {
            "models": {
                "gemini-4.0-pro-preview": {  # hypothetical future model
                    "tokens": {"total": 999}
                }
            }
        },
    }
    async def go():
        fake = _fake_proc(json.dumps(payload).encode(), b"", returncode=0)
        with patch("lib.cli_runners.asyncio.create_subprocess_exec",
                   AsyncMock(return_value=fake)):
            return await run_antigravity("any prompt", timeout_s=10)

    resp = asyncio.run(go())
    assert resp.tokens == 999
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py::test_run_antigravity_replays_smoke_fixture -v
```

Expected: FAIL with `ImportError: run_antigravity`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/lib/cli_runners.py`:

```python
ANTIGRAVITY_BINARY = "/opt/homebrew/bin/gemini"
ANTIGRAVITY_DEFAULT_TIMEOUT_S = 120


def _antigravity_tokens(payload: dict) -> int | None:
    """Pluck the total token count from Anti-Gravity stats, model-name-agnostic.

    `stats.models` is a {<model_name>: {tokens: {total: int, ...}}} map.
    The model name is whichever the auto-router resolved to and may change
    over time, so we read whichever single key is present.
    """
    models = (payload.get("stats") or {}).get("models") or {}
    if not models:
        return None
    # If multiple models surface (multi-model routing in a future CLI version),
    # sum them — total across the call is the right number for our manifest.
    total = 0
    found = False
    for entry in models.values():
        tk = (entry or {}).get("tokens") or {}
        if "total" in tk:
            total += int(tk["total"])
            found = True
    return total if found else None


async def run_antigravity(prompt: str, timeout_s: int = ANTIGRAVITY_DEFAULT_TIMEOUT_S) -> CLIResponse:
    """Invoke `gemini -p` with JSON output and plan approval mode.

    Trust set via GEMINI_CLI_TRUST_WORKSPACE=true env var (explicit, not
    inherited). Sandbox via --approval-mode plan (read-only per smoke test).
    Returns a CLIResponse; never raises on CLI failure.
    """
    cmd = [
        ANTIGRAVITY_BINARY,
        "-p", prompt,
        "--output-format", "json",
        "--approval-mode", "plan",
    ]
    env = {**os.environ, "GEMINI_CLI_TRUST_WORKSPACE": "true"}
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
            env=env,
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"gemini binary missing: {exc}",
        )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"antigravity timeout after {timeout_s}s",
        )

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    duration = time.monotonic() - t0
    rate_capped = detect_rate_cap("antigravity", stderr_text)

    try:
        payload = json.loads(stdout_text)
    except json.JSONDecodeError as exc:
        return CLIResponse(
            cli="antigravity", text=stdout_text, tokens=None,
            duration_s=duration,
            exit_code=proc.returncode if proc.returncode is not None else -1,
            rate_capped=rate_capped,
            error=f"antigravity json parse failed: {exc}",
        )

    return CLIResponse(
        cli="antigravity",
        text=str(payload.get("response", "")),
        tokens=_antigravity_tokens(payload),
        duration_s=duration,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=rate_capped,
        error=None if proc.returncode == 0 else stderr_text[:500],
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_cli_runners.py -v
```

Expected: 15 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/cli_runners.py agents-sdk/tests/test_cli_runners.py
git commit -m "feat(cli_runners): run_antigravity wrapper with model-agnostic token parse"
```

---

## Phase B — Prompt builder (`agents-sdk/lib/critique_prompt.py`)

**Why this is Phase B:** isolates the prompt-engineering surface from the agent orchestration. The smoke-tested prompt is the prototype; this generalization takes an article body + index context and returns the rendered prompt string.

**Files:**
- Create: `agents-sdk/lib/critique_prompt.py`
- Create: `agents-sdk/prompts/vault-critic-prompt-template.md`
- Create: `agents-sdk/tests/test_critique_prompt.py`

### Task B1: Persist the prompt template at its production home

- [ ] **Step 1: Copy the smoke template into the production prompt directory**

```bash
mkdir -p agents-sdk/prompts
cp agents-sdk/docs/multi-cli-smoke-2026-05-21/critique-prompt.md \
   agents-sdk/prompts/vault-critic-prompt-template.md
```

- [ ] **Step 2: Generalize the template body**

Edit `agents-sdk/prompts/vault-critic-prompt-template.md` so the per-article body is templated:

```markdown
You are reviewing a concept article from Sean Winslow's personal knowledge vault. Sean's complaint: his agent fleet produces descriptive summaries of what he already has, not generative critique of what he should add.

ARTICLE UNDER REVIEW: `{slug}`

{article_body}

CONTEXT
- Article frontmatter source path: {source_path}
- Cross-references in article body: {wikilink_summary}
- Recent vault concepts (top {context_limit} by recency, for orientation only): {recent_titles}

TASK: Give Sean 3 specific things he is MISSING from this concept — adjacent techniques, canonical references, missing facets, contradicting frameworks. For each:
- (1) WHAT to add (named technique, idea, framework, voice, pattern, etc.),
- (2) WHO/WHAT exemplifies it — cite the specific work, not the field (a specific author + specific book/essay/paper/repo/talk),
- (3) WHAT this would unlock for Sean — name the genre of work, the kind of decision, the kind of artifact this would let him produce that the current concept cannot reach.

Be specific. No generic advice. If you cite an author, cite a specific work. No "consider exploring X" — instead, "Add 'X mode' anchored on AUTHOR's WORK, sentence pattern: PATTERN; this unlocks GENRE where Sean currently sounds GENERIC-FAILURE-MODE."

Respond in plain markdown, under 600 words. Lead with the 3 recommendations, no preamble.
```

- [ ] **Step 3: Commit**

```bash
git add agents-sdk/prompts/vault-critic-prompt-template.md
git commit -m "feat(critique_prompt): generalize smoke-tested prompt template for production"
```

### Task B2: `build_critique_prompt` pure function — TDD

- [ ] **Step 1: Write the failing test**

In `agents-sdk/tests/test_critique_prompt.py`:

```python
from pathlib import Path

from lib.critique_prompt import build_critique_prompt, extract_wikilinks_summary


ARTICLE = """\
---
title: "Writing Voice Modes"
type: concept
sources:
  - .claude/skills/writing-voice-modes/SKILL.md
created: 2026-05-13
---

## Definition

Sean's writing-voice-modes skill calibrates 5 authorial voices for long-form writing:
1. Domestic Observer (David Sedaris)
2. Gonzo Technical (Hunter S. Thompson)
3. Beat Flow (Jack Kerouac)
4. Minimalist Absurdist (Kurt Vonnegut)
5. Sean Mode

## Related Concepts

[[creative-writing]] [[blog-cadence]] [[tone-calibration]]
"""


def test_build_critique_prompt_includes_slug_and_body():
    prompt = build_critique_prompt(
        slug="writing-voice-modes",
        article_body=ARTICLE,
        source_path=".claude/skills/writing-voice-modes/SKILL.md",
        recent_titles=["agentic-engineering", "vault-architecture"],
    )
    assert "writing-voice-modes" in prompt
    assert "Domestic Observer (David Sedaris)" in prompt
    assert ".claude/skills/writing-voice-modes/SKILL.md" in prompt


def test_build_critique_prompt_extracts_wikilink_summary():
    prompt = build_critique_prompt(
        slug="writing-voice-modes",
        article_body=ARTICLE,
        source_path="any.md",
        recent_titles=[],
    )
    # The wikilink summary lists the three [[targets]] from the article body.
    assert "creative-writing" in prompt
    assert "blog-cadence" in prompt
    assert "tone-calibration" in prompt


def test_build_critique_prompt_caps_recent_titles_at_default_limit():
    long_titles = [f"concept-{i}" for i in range(100)]
    prompt = build_critique_prompt(
        slug="x", article_body="body", source_path="p", recent_titles=long_titles,
    )
    # Default cap is 30 — verify concept-99 NOT present but concept-0 IS.
    assert "concept-0" in prompt
    assert "concept-99" not in prompt


def test_extract_wikilinks_summary_dedupes_and_orders():
    body = "Some [[alpha]] text [[beta]] more [[alpha]] [[gamma]]"
    assert extract_wikilinks_summary(body) == "alpha, beta, gamma"


def test_extract_wikilinks_summary_handles_aliased():
    body = "Reference [[real-slug|Display Name]] in body"
    assert extract_wikilinks_summary(body) == "real-slug"


def test_extract_wikilinks_summary_empty_when_no_links():
    assert extract_wikilinks_summary("no links here") == "(no wikilinks)"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critique_prompt.py -v
```

Expected: FAIL with `ImportError`.

- [ ] **Step 3: Write minimal implementation**

In `agents-sdk/lib/critique_prompt.py`:

```python
"""Build the per-article critique prompt sent to Codex + Anti-Gravity.

Pure functions — no I/O outside the named template path read. The smoke-
tested prompt template lives at `agents-sdk/prompts/vault-critic-prompt-
template.md` and is the source of truth; this module only fills the slots.
"""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "vault-critic-prompt-template.md"

_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

DEFAULT_CONTEXT_LIMIT = 30


def extract_wikilinks_summary(article_body: str) -> str:
    """Return a comma-separated, deduped, order-preserving wikilink list.

    `[[real|Display]]` is normalized to `real`. Empty input → "(no wikilinks)"
    so the prompt template never has a dangling empty list.
    """
    seen: dict[str, None] = {}
    for target in _WIKILINK_RE.findall(article_body):
        seen.setdefault(target.strip(), None)
    if not seen:
        return "(no wikilinks)"
    return ", ".join(seen.keys())


def build_critique_prompt(
    *,
    slug: str,
    article_body: str,
    source_path: str,
    recent_titles: list[str],
    context_limit: int = DEFAULT_CONTEXT_LIMIT,
    template_path: Path | None = None,
) -> str:
    """Render the critique prompt for a single article.

    `recent_titles` is the recent-concepts orientation list from
    `vault/knowledge/index.md`; cap-limited to `context_limit` (default 30)
    by recency. The cap keeps the prompt under ~14K input tokens even on
    busy nights — Codex / Anti-Gravity smoke test was 13.2K input.
    """
    template = (template_path or _TEMPLATE_PATH).read_text(encoding="utf-8")
    capped = recent_titles[:context_limit]
    return template.format(
        slug=slug,
        article_body=article_body.strip(),
        source_path=source_path,
        wikilink_summary=extract_wikilinks_summary(article_body),
        context_limit=context_limit,
        recent_titles=", ".join(capped) if capped else "(none)",
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critique_prompt.py -v
```

Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/critique_prompt.py agents-sdk/tests/test_critique_prompt.py
git commit -m "feat(critique_prompt): build_critique_prompt + wikilink extractor with cap"
```

---

## Phase C — Target selector with PR-contamination filter

**Why this is Phase C:** Per memory [`feedback_synth_verify_filter_to_manifest.md`](../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_filter_to_manifest.md), naive `ls -lt` selection is a known bug. PR #52 contamination on 2026-05-21 would have produced wasted vault_critic compute on pre-retrofit shallow articles. The filter cross-references the Mac Mini auto-commit's file list, NOT mtime.

**Files:**
- Modify: `agents-sdk/lib/cli_runners.py` (add `select_target_articles` — colocated because both modules belong to the critic neighborhood; alternative is `lib/vault_critic_selector.py` if the runner module grows too large, see Risk #4).

Actually colocate in a separate module to keep cli_runners focused. See revised file map below.

**Revised file map:**
- Create: `agents-sdk/lib/critic_selector.py`
- Modify: `agents-sdk/tests/test_vault_critic.py` (created in Phase D — selector tests will live there alongside agent tests)

For test discovery during Phase C, create:
- Create: `agents-sdk/tests/test_critic_selector.py`

### Task C1: Read synth-manifest + Mac Mini commit file list

- [ ] **Step 1: Write the failing test**

In `agents-sdk/tests/test_critic_selector.py`:

```python
import json
from datetime import date
from pathlib import Path

import pytest

from lib.critic_selector import (
    list_macmini_synth_files,
    select_target_articles,
)


@pytest.fixture
def tmp_vault(tmp_path):
    """Minimal vault layout mirroring the production paths."""
    (tmp_path / "vault" / "knowledge" / "concepts").mkdir(parents=True)
    (tmp_path / "vault" / "knowledge" / "expansions").mkdir(parents=True)
    (tmp_path / "vault" / "health").mkdir(parents=True)
    return tmp_path


def _write_concept(vault_root: Path, slug: str, title: str) -> Path:
    p = vault_root / "vault" / "knowledge" / "concepts" / f"{slug}.md"
    p.write_text(
        f'---\ntitle: "{title}"\ntype: concept\n---\n\n## Definition\n\nbody\n',
        encoding="utf-8",
    )
    return p


def _write_manifest(vault_root: Path, today_iso: str, **kwargs):
    payload = {
        "run_id": f"{today_iso}T02:31:00",
        "status": "ok",
        "concepts_written": 1,
        "connections_written": 0,
        **kwargs,
    }
    (vault_root / "vault" / "health" / f"synth-manifest-{today_iso}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_list_macmini_synth_files_returns_concept_paths_from_commit(monkeypatch, tmp_vault):
    """The function shells to git log to enumerate files written by Mac Mini's
    auto-commit in the synth window (02:00-04:00 today), then filters to
    vault/knowledge/concepts/*.md paths. Mock the git call to keep the test
    hermetic."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "real-mm-concept", "Real Mac Mini Concept")
    _write_concept(tmp_vault, "pr-contamination", "PR Contamination Concept")

    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        # Simulate a Mac Mini auto-commit listing exactly one concept file.
        class Result:
            returncode = 0
            stdout = "vault/knowledge/concepts/real-mm-concept.md\n"
            stderr = ""
        return Result()

    monkeypatch.setattr("lib.critic_selector.subprocess.run", fake_run)

    files = list_macmini_synth_files(tmp_vault, date_iso=today)
    assert len(files) == 1
    assert files[0].name == "real-mm-concept.md"
    # The git command must scope to the synth window today.
    assert "--since" in captured["cmd"]
    assert today in " ".join(captured["cmd"])


def test_select_target_articles_filters_to_manifest_count(monkeypatch, tmp_vault):
    """If the manifest reports concepts_written=1 but ls shows 5 fresh concept
    files, only the 1 file from the Mac Mini auto-commit is selected."""
    today = "2026-05-21"
    for slug in ("good", "bad1", "bad2", "bad3", "bad4"):
        _write_concept(tmp_vault, slug, slug.title())
    _write_manifest(tmp_vault, today, concepts_written=1)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            root / "vault" / "knowledge" / "concepts" / "good.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert len(targets) == 1
    assert targets[0].name == "good.md"


def test_select_target_articles_caps_at_max_targets(monkeypatch, tmp_vault):
    today = "2026-05-21"
    for slug in ("a", "b", "c", "d", "e"):
        _write_concept(tmp_vault, slug, slug.upper())
    _write_manifest(tmp_vault, today, concepts_written=5)

    all_paths = [
        tmp_vault / "vault" / "knowledge" / "concepts" / f"{s}.md"
        for s in ("a", "b", "c", "d", "e")
    ]
    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: all_paths,
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert len(targets) == 3


def test_select_target_articles_returns_empty_when_no_manifest(tmp_vault):
    """No synth ran or wasn't completed — exit cleanly with empty list.
    This is the 2026-05-15 MBP-offline canonical case."""
    targets = select_target_articles(tmp_vault, date_iso="2026-05-21", max_targets=3)
    assert targets == []


def test_select_target_articles_skips_already_critiqued(monkeypatch, tmp_vault):
    """If vault/knowledge/expansions/foo.md already exists, skip foo —
    snapshot semantics, no regeneration in v1."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "already", "Already")
    _write_concept(tmp_vault, "fresh", "Fresh")
    (tmp_vault / "vault" / "knowledge" / "expansions" / "already.md").write_text(
        "previous critique", encoding="utf-8",
    )
    _write_manifest(tmp_vault, today, concepts_written=2)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            tmp_vault / "vault" / "knowledge" / "concepts" / "already.md",
            tmp_vault / "vault" / "knowledge" / "concepts" / "fresh.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert [t.name for t in targets] == ["fresh.md"]


def test_select_target_articles_skips_when_manifest_status_is_error(monkeypatch, tmp_vault):
    """If the synthesizer's manifest says status=error, don't critique its
    output — those articles are an error path, not real synth output."""
    today = "2026-05-21"
    _write_concept(tmp_vault, "fresh", "Fresh")
    _write_manifest(tmp_vault, today, status="error", concepts_written=0)

    monkeypatch.setattr(
        "lib.critic_selector.list_macmini_synth_files",
        lambda root, date_iso: [
            tmp_vault / "vault" / "knowledge" / "concepts" / "fresh.md",
        ],
    )

    targets = select_target_articles(tmp_vault, date_iso=today, max_targets=3)
    assert targets == []
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critic_selector.py -v
```

Expected: FAIL with `ImportError: lib.critic_selector`.

- [ ] **Step 3: Write minimal implementation**

In `agents-sdk/lib/critic_selector.py`:

```python
"""Select target articles for vault_critic, defending against PR contamination.

Per memory feedback_synth_verify_filter_to_manifest.md (2026-05-21):
naive `ls -lt` selection mixes Mac-Mini-written articles with files merged
in from stale-checkout machines via PR. The PR #52 contamination on
2026-05-21 nearly produced wasted vault_critic compute on 88 pre-Tier-2
files. The filter here cross-references the Mac Mini auto-commit's file
list using `git log --since/--until --name-only`, NOT mtime.

Skip semantics: missing manifest → empty list (2026-05-15 MBP-offline case).
Manifest status=error → empty list. Already-critiqued (expansion file exists)
→ skip. These keep the agent quiet on degraded nights rather than producing
wasted output.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

CONCEPTS_REL = "vault/knowledge/concepts"
EXPANSIONS_REL = "vault/knowledge/expansions"
HEALTH_REL = "vault/health"
SYNTH_WINDOW_START_HOUR = "02:00"
SYNTH_WINDOW_END_HOUR = "04:00"


def list_macmini_synth_files(
    repo_root: Path,
    *,
    date_iso: str | None = None,
) -> list[Path]:
    """Return the concept files Mac Mini's auto-commit wrote in today's
    synth window. Shells to `git log --name-only` scoped to the synth
    window (02:00–04:00 today). Filters to vault/knowledge/concepts/*.md.

    Returns [] on any git failure — caller treats that as a quiet night.
    """
    date_iso = date_iso or date.today().isoformat()
    since = f"{date_iso} {SYNTH_WINDOW_START_HOUR}"
    until = f"{date_iso} {SYNTH_WINDOW_END_HOUR}"

    cmd = [
        "git", "log",
        f"--since={since}",
        f"--until={until}",
        "--name-only",
        "--pretty=format:",
        "--",
        f"{CONCEPTS_REL}/*.md",
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (subprocess.SubprocessError, OSError):
        return []

    if result.returncode != 0:
        return []

    out: list[Path] = []
    seen: set[str] = set()
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith(f"{CONCEPTS_REL}/"):
            continue
        if line in seen:
            continue
        seen.add(line)
        full = repo_root / line
        if full.exists():
            out.append(full)
    return out


def _read_manifest(repo_root: Path, date_iso: str) -> dict | None:
    p = repo_root / HEALTH_REL / f"synth-manifest-{date_iso}.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def select_target_articles(
    repo_root: Path,
    *,
    date_iso: str | None = None,
    max_targets: int = 3,
) -> list[Path]:
    """Select up to `max_targets` concept articles to critique tonight.

    Filters applied in order:
      1. Today's synth-manifest must exist (else 2026-05-15-style MBP-offline).
      2. Manifest status must NOT be `error`.
      3. Article must be in Mac Mini's auto-commit file list (PR-contamination filter).
      4. Article must not already have an expansion file (snapshot semantics).
      5. Cap at `max_targets`, preserving auto-commit file order.

    Returns [] on any disqualifying condition.
    """
    date_iso = date_iso or date.today().isoformat()
    manifest = _read_manifest(repo_root, date_iso)
    if manifest is None:
        return []
    if manifest.get("status") == "error":
        return []

    mm_files = list_macmini_synth_files(repo_root, date_iso=date_iso)
    if not mm_files:
        return []

    expansions_dir = repo_root / EXPANSIONS_REL
    selected: list[Path] = []
    for fp in mm_files:
        if (expansions_dir / fp.name).exists():
            continue
        selected.append(fp)
        if len(selected) >= max_targets:
            break
    return selected
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critic_selector.py -v
```

Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/critic_selector.py agents-sdk/tests/test_critic_selector.py
git commit -m "feat(critic_selector): select targets with PR-contamination filter"
```

---

## Phase D — Main agent (`agents-sdk/agents/vault_critic.py`)

**Why this is Phase D:** orchestration ties the wrappers, prompt builder, and selector together into the nightly process. The manifest contract is finalized here. The hardest tests (rate-cap partial status, MBP-offline skip, smoke-fixture replay) live here because they exercise the full agent path.

**Files:**
- Create: `agents-sdk/agents/vault_critic.py`
- Create: `agents-sdk/tests/test_vault_critic.py`

### Task D1: `CritiqueResult` dataclass + manifest writer — TDD

- [ ] **Step 1: Write the failing test**

In `agents-sdk/tests/test_vault_critic.py`:

```python
import json
from pathlib import Path

import pytest

from agents.vault_critic import (
    CritiqueResult,
    write_critic_manifest,
    AGENT_NAME,
    STATUS_OK,
    STATUS_PARTIAL,
    STATUS_SUCCESS_EMPTY,
    STATUS_ERROR,
)


@pytest.fixture
def tmp_repo(tmp_path):
    (tmp_path / "vault" / "health").mkdir(parents=True)
    return tmp_path


def test_agent_name_constant():
    # Must match the launchd plist label + record_run CSV value.
    assert AGENT_NAME == "vault-critic"


def test_critique_result_defaults():
    r = CritiqueResult(status=STATUS_OK, run_id="2026-05-22T03:30:00")
    assert r.articles_critiqued == 0
    assert r.codex_calls == 0
    assert r.codex_failures == 0
    assert r.expansions_written == []


def test_write_critic_manifest_round_trip(tmp_repo):
    r = CritiqueResult(
        status=STATUS_OK,
        run_id="2026-05-22T03:30:00",
        articles_critiqued=2,
        codex_calls=2, codex_failures=0, codex_tokens_total=34000,
        antigravity_calls=2, antigravity_failures=0, antigravity_tokens_total=31000,
        duration_seconds=180.5,
        expansions_written=[
            "vault/knowledge/expansions/foo.md",
            "vault/knowledge/expansions/bar.md",
        ],
    )
    path = write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")
    assert path.name == "critic-manifest-2026-05-22.json"
    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == STATUS_OK
    assert payload["articles_critiqued"] == 2
    assert payload["expansions_written"] == [
        "vault/knowledge/expansions/foo.md",
        "vault/knowledge/expansions/bar.md",
    ]
    assert payload["duration_seconds"] == 180.5


def test_write_critic_manifest_atomic_via_tmp_rename(tmp_repo):
    r = CritiqueResult(status=STATUS_SUCCESS_EMPTY, run_id="x")
    path = write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")
    # No leftover .tmp file
    assert not path.with_suffix(path.suffix + ".tmp").exists()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: FAIL with `ImportError`.

- [ ] **Step 3: Write minimal implementation**

In `agents-sdk/agents/vault_critic.py`:

```python
#!/usr/bin/env python3
"""Vault Critic — nightly generative critique of synthesizer concept articles.

Runs on Mac Mini via launchd at 03:30 daily, after vault_synthesizer (02:30)
and deep_researcher (02:45). For each newly-written concept article from
today's synth-manifest (Mac-Mini-canonical, PR-contamination-filtered), fans
out two parallel subprocess critiques — Codex CLI (gpt-5.5) and Anti-Gravity
CLI (Gemini 3.1 Pro) — and writes a sibling expansion file at
vault/knowledge/expansions/{slug}.md plus a per-run manifest at
vault/health/critic-manifest-{date}.json.

Cost: $0 incremental on existing personal subscriptions. Sonnet fallback is
out of scope for v1; both-CLIs-rate-capped marks the run partial and exits
cleanly.

Schedule sequence:
    02:00  vault-indexer
    02:30  vault-synthesizer
    02:45  deep-researcher
    03:30  vault-critic        <- this agent
    08:30  daily-driver morning
    08:45  meta-agent
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.cli_runners import CLIResponse, run_antigravity, run_codex
from lib.config import load_config
from lib.critic_selector import select_target_articles
from lib.critique_prompt import build_critique_prompt
from lib.filelock import FileLock
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "vault-critic"

STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_SUCCESS_EMPTY = "success-empty"
STATUS_ERROR = "error"
STATUS_VALUES = frozenset({STATUS_OK, STATUS_PARTIAL, STATUS_SUCCESS_EMPTY, STATUS_ERROR})

DEFAULT_MAX_TARGETS = 3
DEFAULT_WALL_BUDGET_S = 600
DEFAULT_PER_CLI_TIMEOUT_S = 120
RECENT_TITLES_CONTEXT_LIMIT = 30

EXPANSIONS_REL = "vault/knowledge/expansions"
HEALTH_REL = "vault/health"
KNOWLEDGE_INDEX_REL = "vault/knowledge/index.md"

_TITLE_FRONTMATTER_RE = re.compile(r'^title:\s*"?([^"\n]+)"?', re.MULTILINE)


@dataclass
class CritiqueResult:
    """Per-run summary written verbatim into critic-manifest-{date}.json."""
    status: str
    run_id: str
    articles_critiqued: int = 0
    codex_calls: int = 0
    codex_failures: int = 0
    codex_tokens_total: int = 0
    antigravity_calls: int = 0
    antigravity_failures: int = 0
    antigravity_tokens_total: int = 0
    duration_seconds: float = 0.0
    expansions_written: list[str] = field(default_factory=list)
    error: str = ""
    warnings: list[str] = field(default_factory=list)


def write_critic_manifest(
    *,
    repo_root: Path,
    result: CritiqueResult,
    today: str,
) -> Path:
    """Atomic write to vault/health/critic-manifest-{today}.json."""
    health = repo_root / HEALTH_REL
    health.mkdir(parents=True, exist_ok=True)
    path = health / f"critic-manifest-{today}.json"
    payload = {
        "run_id": result.run_id,
        "status": result.status,
        "articles_critiqued": result.articles_critiqued,
        "codex_calls": result.codex_calls,
        "codex_failures": result.codex_failures,
        "codex_tokens_total": result.codex_tokens_total,
        "antigravity_calls": result.antigravity_calls,
        "antigravity_failures": result.antigravity_failures,
        "antigravity_tokens_total": result.antigravity_tokens_total,
        "duration_seconds": round(result.duration_seconds, 2),
        "expansions_written": list(result.expansions_written),
        "warnings": list(result.warnings),
        "error": result.error,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
    return path
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/vault_critic.py agents-sdk/tests/test_vault_critic.py
git commit -m "feat(vault_critic): CritiqueResult dataclass + atomic manifest writer"
```

### Task D2: Expansion-file formatter — TDD

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_vault_critic.py`:

```python
from agents.vault_critic import format_expansion_body


def test_format_expansion_body_both_clis_succeeded():
    body = format_expansion_body(
        original_title="Writing Voice Modes",
        original_slug="writing-voice-modes",
        codex_text="1. Forensic Moral Essayist — Joan Didion ...",
        antigravity_text="### 1. Surgical Cultural Synthesis ...",
        today="2026-05-22",
        codex_failed=False,
        antigravity_failed=False,
    )
    assert body.startswith("---\n")
    assert 'title: "How to make `Writing Voice Modes` better"\n' in body
    assert 'type: expansion\n' in body
    assert 'parent: "[[writing-voice-modes]]"\n' in body
    assert '- codex (gpt-5.5)' in body
    assert '- anti-gravity (gemini-3.1-pro-preview)' in body
    assert "## From Codex (gpt-5.5)" in body
    assert "## From Anti-Gravity (Gemini 3)" in body
    assert "1. Forensic Moral Essayist" in body
    assert "Surgical Cultural Synthesis" in body


def test_format_expansion_body_one_cli_failed_renders_status_marker():
    body = format_expansion_body(
        original_title="X",
        original_slug="x",
        codex_text="codex response",
        antigravity_text="",
        today="2026-05-22",
        codex_failed=False,
        antigravity_failed=True,
    )
    assert "codex response" in body
    assert "_Anti-Gravity rate-capped or failed; no critique this run._" in body


def test_format_expansion_body_includes_required_wikilink():
    """Per validator pattern: every expansion file must contain ≥1 wikilink
    so it isn't orphaned in vault/knowledge/index.md downstream."""
    body = format_expansion_body(
        original_title="X", original_slug="x",
        codex_text="text", antigravity_text="text",
        today="2026-05-22",
        codex_failed=False, antigravity_failed=False,
    )
    assert "[[x]]" in body
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 3 new tests FAIL with `ImportError: format_expansion_body`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/agents/vault_critic.py`:

```python
def format_expansion_body(
    *,
    original_title: str,
    original_slug: str,
    codex_text: str,
    antigravity_text: str,
    today: str,
    codex_failed: bool,
    antigravity_failed: bool,
) -> str:
    """Render the markdown body for vault/knowledge/expansions/{slug}.md.

    Snapshot semantics: one file per critiqued concept; not regenerated when
    the underlying concept is rewritten. Always contains a `[[parent-slug]]`
    wikilink so the file is not orphaned in the knowledge index.
    """
    codex_block = (
        codex_text.strip()
        if not codex_failed and codex_text.strip()
        else "_Codex rate-capped or failed; no critique this run._"
    )
    antigravity_block = (
        antigravity_text.strip()
        if not antigravity_failed and antigravity_text.strip()
        else "_Anti-Gravity rate-capped or failed; no critique this run._"
    )
    return (
        f"---\n"
        f'title: "How to make `{original_title}` better"\n'
        f"type: expansion\n"
        f'parent: "[[{original_slug}]]"\n'
        f"sources:\n"
        f"  - codex (gpt-5.5)\n"
        f"  - anti-gravity (gemini-3.1-pro-preview)\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"---\n\n"
        f"## What this is\n\n"
        f"Critiques from two external reasoners (gpt-5.5 via Codex CLI, "
        f"Gemini 3 via Anti-Gravity CLI) of [[{original_slug}]]. The "
        f"synthesizer describes what the concept is; this expansion "
        f"proposes what's missing.\n\n"
        f"## From Codex (gpt-5.5)\n\n"
        f"{codex_block}\n\n"
        f"## From Anti-Gravity (Gemini 3)\n\n"
        f"{antigravity_block}\n"
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 7 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/vault_critic.py agents-sdk/tests/test_vault_critic.py
git commit -m "feat(vault_critic): format_expansion_body with one-CLI-failed handling"
```

### Task D3: `critique_one_article` — parallel fan-out + isolation — TDD

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_vault_critic.py`:

```python
import asyncio
from unittest.mock import AsyncMock, patch

from agents.vault_critic import critique_one_article


CONCEPT_BODY = """\
---
title: "Writing Voice Modes"
type: concept
sources:
  - .claude/skills/writing-voice-modes/SKILL.md
---

## Definition

Five voice modes plus Sean Mode.

## Related Concepts

[[creative-writing]] [[blog-cadence]]
"""


@pytest.fixture
def tmp_concept(tmp_path):
    (tmp_path / "vault" / "knowledge" / "concepts").mkdir(parents=True)
    (tmp_path / "vault" / "knowledge" / "expansions").mkdir(parents=True)
    p = tmp_path / "vault" / "knowledge" / "concepts" / "writing-voice-modes.md"
    p.write_text(CONCEPT_BODY, encoding="utf-8")
    return tmp_path, p


def _ok(cli: str, text: str, tokens: int) -> CLIResponse:
    from lib.cli_runners import CLIResponse
    return CLIResponse(
        cli=cli, text=text, tokens=tokens,
        duration_s=10.0, exit_code=0, rate_capped=False, error=None,
    )


def _fail(cli: str, error: str) -> CLIResponse:
    from lib.cli_runners import CLIResponse
    return CLIResponse(
        cli=cli, text="", tokens=None,
        duration_s=0.5, exit_code=1, rate_capped=False, error=error,
    )


def _capped(cli: str) -> CLIResponse:
    from lib.cli_runners import CLIResponse
    return CLIResponse(
        cli=cli, text="", tokens=None,
        duration_s=0.5, exit_code=0, rate_capped=True, error=None,
    )


def test_critique_one_article_both_clis_succeed(tmp_concept):
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_ok("codex", "codex content", 17000))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gemini content", 15000))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=["other-concept"],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path.name == "writing-voice-modes.md"
    assert expansion_path.parent.name == "expansions"
    assert expansion_path.exists()
    body = expansion_path.read_text(encoding="utf-8")
    assert "codex content" in body
    assert "gemini content" in body
    assert codex_resp.ok and ag_resp.ok


def test_critique_one_article_codex_capped_writes_antigravity_only(tmp_concept):
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_capped("codex"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gemini survived", 15000))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path.exists()
    body = expansion_path.read_text(encoding="utf-8")
    assert "Codex rate-capped or failed" in body
    assert "gemini survived" in body
    assert codex_resp.rate_capped is True
    assert ag_resp.ok is True


def test_critique_one_article_both_fail_returns_none_path(tmp_concept):
    """If BOTH CLIs fail, do not write a useless expansion file — return None.
    The caller increments failure counts and marks the run partial."""
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_fail("codex", "boom"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_fail("antigravity", "boom"))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path is None
    assert not codex_resp.ok and not ag_resp.ok
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 3 new tests FAIL with `ImportError: critique_one_article`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/agents/vault_critic.py`:

```python
async def critique_one_article(
    *,
    repo_root: Path,
    article_path: Path,
    recent_titles: list[str],
    today: str,
    per_cli_timeout_s: int = DEFAULT_PER_CLI_TIMEOUT_S,
) -> tuple[Path | None, CLIResponse, CLIResponse]:
    """Critique one article via Codex + Anti-Gravity in parallel.

    Returns (expansion_path, codex_resp, antigravity_resp). expansion_path
    is None when BOTH CLIs failed (no point writing a placeholder file).
    The returned CLIResponses let the caller account counts + tokens.
    """
    article_body = article_path.read_text(encoding="utf-8", errors="replace")
    title_match = _TITLE_FRONTMATTER_RE.search(article_body)
    original_title = title_match.group(1).strip() if title_match else article_path.stem
    original_slug = article_path.stem

    # Resolve a source_path the prompt can cite. Prefer the first entry from
    # the article's `sources:` frontmatter; fall back to the concept file
    # path itself when frontmatter is missing or empty.
    source_path = _extract_first_source(article_body) or str(
        article_path.relative_to(repo_root)
    )

    prompt = build_critique_prompt(
        slug=original_slug,
        article_body=article_body,
        source_path=source_path,
        recent_titles=recent_titles,
    )

    codex_task = run_codex(prompt, timeout_s=per_cli_timeout_s)
    ag_task = run_antigravity(prompt, timeout_s=per_cli_timeout_s)
    codex_resp, ag_resp = await asyncio.gather(codex_task, ag_task)

    # If both failed, do not write a useless expansion file.
    if not codex_resp.ok and not ag_resp.ok:
        return None, codex_resp, ag_resp

    body = format_expansion_body(
        original_title=original_title,
        original_slug=original_slug,
        codex_text=codex_resp.text,
        antigravity_text=ag_resp.text,
        today=today,
        codex_failed=not codex_resp.ok,
        antigravity_failed=not ag_resp.ok,
    )

    expansions_dir = repo_root / EXPANSIONS_REL
    expansions_dir.mkdir(parents=True, exist_ok=True)
    lock_path = expansions_dir / ".lock"
    expansion_path = expansions_dir / f"{original_slug}.md"
    with FileLock(lock_path, exclusive=True, timeout=30.0):
        expansion_path.write_text(body, encoding="utf-8")
    return expansion_path, codex_resp, ag_resp


_SOURCES_FRONTMATTER_RE = re.compile(
    r"^sources:\s*\n((?:\s*-\s+.+\n?)+)", re.MULTILINE
)


def _extract_first_source(article_body: str) -> str | None:
    """Pull the first entry from the `sources:` YAML list; None if absent."""
    block_match = _SOURCES_FRONTMATTER_RE.search(article_body[:1000])
    if not block_match:
        return None
    for line in block_match.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            return line[2:].strip().strip('"').strip("'") or None
    return None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 10 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/vault_critic.py agents-sdk/tests/test_vault_critic.py
git commit -m "feat(vault_critic): critique_one_article parallel fan-out with isolation"
```

### Task D4: Smoke-fixture replay regression test

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_vault_critic.py`:

```python
SMOKE_FIXTURES = Path(__file__).parent / "fixtures" / "critic"


def test_smoke_fixtures_replay_produces_expected_expansion_shape(tmp_concept):
    """Replay the persisted smoke-test outputs as subprocess stand-ins;
    assert the formatter produces an expansion file containing the verbatim
    headline recommendations from both CLIs. This is the regression test
    against future CLI output drift."""
    repo_root, concept_path = tmp_concept
    codex_stdout = (SMOKE_FIXTURES / "codex-out.txt").read_text(encoding="utf-8")
    gemini_payload = json.loads((SMOKE_FIXTURES / "gemini-out.json").read_text(encoding="utf-8"))
    gemini_response = gemini_payload["response"]

    async def go():
        codex_resp = _ok("codex", codex_stdout, 17182)
        ag_resp = _ok("antigravity", gemini_response, 15746)
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=codex_resp)), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=ag_resp)):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path is not None
    body = expansion_path.read_text(encoding="utf-8")

    # Both Codex headline recommendations are present byte-for-byte.
    assert "Forensic Moral Essayist" in body
    assert "Architectural Systems Narrator" in body
    assert "Intimate Intellectual Pressure" in body

    # All three Anti-Gravity headline recommendations are present byte-for-byte.
    assert "Surgical Cultural Synthesis" in body
    assert "Escalating Moral Architecture" in body
    assert "Techno-Dialectical Aphorist" in body

    # The convergence signal (Didion in both) is preserved.
    assert body.count("Didion") >= 2
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py::test_smoke_fixtures_replay_produces_expected_expansion_shape -v
```

Expected: PASS already (the formatter is wired). If it doesn't, fix the formatter or fixture wiring rather than tuning the test.

- [ ] **Step 3: Commit**

```bash
git add agents-sdk/tests/test_vault_critic.py
git commit -m "test(vault_critic): smoke-fixture replay regression test against CLI output drift"
```

### Task D5: `run` orchestrator + wall-clock budget — TDD

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_vault_critic.py`:

```python
from agents.vault_critic import run as run_critic


def _make_concept_at(vault_root: Path, slug: str) -> Path:
    p = vault_root / "vault" / "knowledge" / "concepts" / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'---\ntitle: "{slug}"\ntype: concept\n---\n\nbody [[wiki]]\n',
        encoding="utf-8",
    )
    return p


def _make_manifest(vault_root: Path, today_iso: str, **kwargs):
    (vault_root / "vault" / "health").mkdir(parents=True, exist_ok=True)
    (vault_root / "vault" / "health" / f"synth-manifest-{today_iso}.json").write_text(
        json.dumps({"status": "ok", "concepts_written": 2, **kwargs}),
        encoding="utf-8",
    )


def test_run_writes_manifest_when_no_synth_manifest_today(tmp_repo):
    """The 2026-05-15 MBP-offline canonical case: synthesizer didn't run.
    Agent exits cleanly with status=success-empty manifest. NOT status=error."""

    async def go():
        return await run_critic(
            repo_root=tmp_repo,
            date_iso="2026-05-22",
            max_targets=3,
            wall_budget_s=600,
        )

    result = asyncio.run(go())
    assert result.status == STATUS_SUCCESS_EMPTY
    assert result.articles_critiqued == 0

    manifest = tmp_repo / "vault" / "health" / "critic-manifest-2026-05-22.json"
    assert manifest.exists()


def test_run_codex_rate_capped_marks_partial_status(tmp_repo, monkeypatch):
    today = "2026-05-22"
    p = _make_concept_at(tmp_repo, "writing-voice-modes")
    _make_manifest(tmp_repo, today)

    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: [p])

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_capped("codex"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gem", 15000))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_PARTIAL
    assert result.articles_critiqued == 1   # the file WAS written (anti-gravity survived)
    assert result.codex_failures == 1
    assert result.antigravity_failures == 0
    expansion = tmp_repo / "vault" / "knowledge" / "expansions" / "writing-voice-modes.md"
    assert expansion.exists()


def test_run_both_clis_fail_for_every_article_marks_error(tmp_repo, monkeypatch):
    today = "2026-05-22"
    p = _make_concept_at(tmp_repo, "x")
    _make_manifest(tmp_repo, today)

    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: [p])

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_fail("codex", "boom"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_fail("antigravity", "boom"))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_ERROR
    assert result.articles_critiqued == 0
    assert result.codex_failures == 1
    assert result.antigravity_failures == 1


def test_run_succeeds_with_three_articles(tmp_repo, monkeypatch):
    today = "2026-05-22"
    paths = [_make_concept_at(tmp_repo, slug) for slug in ("a", "b", "c")]
    _make_manifest(tmp_repo, today)
    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: paths)

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(side_effect=lambda *a, **k: _ok("codex", "ok", 100))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(side_effect=lambda *a, **k: _ok("antigravity", "ok", 100))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_OK
    assert result.articles_critiqued == 3


def test_run_respects_wall_budget(tmp_repo, monkeypatch):
    """When wall_budget_s is exceeded mid-loop, mark partial and skip remaining."""
    today = "2026-05-22"
    paths = [_make_concept_at(tmp_repo, slug) for slug in ("a", "b", "c")]
    _make_manifest(tmp_repo, today)
    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: paths)

    async def slow_cli(*args, **kwargs):
        await asyncio.sleep(0.2)
        return _ok("codex", "ok", 100)

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(side_effect=slow_cli)), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(side_effect=slow_cli)):
            # 0.3s budget — first article should land; second/third should be skipped.
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=0.3,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_PARTIAL
    assert result.articles_critiqued <= 2
    assert any("budget" in w.lower() for w in result.warnings)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 5 new tests FAIL with `ImportError: run as run_critic`.

- [ ] **Step 3: Write minimal implementation**

Add to `agents-sdk/agents/vault_critic.py`:

```python
async def run(
    *,
    repo_root: Path,
    date_iso: str | None = None,
    max_targets: int = DEFAULT_MAX_TARGETS,
    wall_budget_s: float = DEFAULT_WALL_BUDGET_S,
    per_cli_timeout_s: int = DEFAULT_PER_CLI_TIMEOUT_S,
    logger=None,
) -> CritiqueResult:
    """Orchestrate one vault_critic run end-to-end.

    Status promotion (after the loop):
      - No targets selected (no manifest / status=error / nothing fresh) → success-empty
      - All articles produced both-CLIs-failed → error
      - At least one CLI failed across the run → partial
      - Budget exceeded mid-loop → partial (with budget warning)
      - Everything clean → ok
    """
    date_iso = date_iso or date.today().isoformat()
    start = time.monotonic()
    result = CritiqueResult(
        status=STATUS_SUCCESS_EMPTY,
        run_id=datetime.now().isoformat(timespec="seconds"),
    )

    targets = select_target_articles(
        repo_root, date_iso=date_iso, max_targets=max_targets,
    )
    if not targets:
        if logger:
            logger.info("vault_critic: no target articles for %s", date_iso)
        write_critic_manifest(repo_root=repo_root, result=result, today=date_iso)
        result.duration_seconds = time.monotonic() - start
        return result

    recent_titles = _read_recent_titles(repo_root, limit=RECENT_TITLES_CONTEXT_LIMIT)
    any_failure = False
    every_article_both_failed = True

    for fp in targets:
        if time.monotonic() - start >= wall_budget_s:
            result.warnings.append(
                f"wall budget {wall_budget_s}s ran out after "
                f"{result.articles_critiqued} articles"
            )
            any_failure = True
            break

        expansion_path, codex_resp, ag_resp = await critique_one_article(
            repo_root=repo_root,
            article_path=fp,
            recent_titles=recent_titles,
            today=date_iso,
            per_cli_timeout_s=per_cli_timeout_s,
        )

        result.codex_calls += 1
        result.antigravity_calls += 1
        if codex_resp.tokens:
            result.codex_tokens_total += codex_resp.tokens
        if ag_resp.tokens:
            result.antigravity_tokens_total += ag_resp.tokens
        if not codex_resp.ok:
            result.codex_failures += 1
            any_failure = True
        if not ag_resp.ok:
            result.antigravity_failures += 1
            any_failure = True

        if expansion_path is None:
            # Both CLIs failed for this article — don't reset
            # every_article_both_failed; if this stays true across all
            # targets, the run is error-class.
            continue

        every_article_both_failed = False
        result.articles_critiqued += 1
        result.expansions_written.append(
            str(expansion_path.relative_to(repo_root))
        )

    if every_article_both_failed:
        result.status = STATUS_ERROR
    elif any_failure:
        result.status = STATUS_PARTIAL
    elif result.articles_critiqued > 0:
        result.status = STATUS_OK
    else:
        result.status = STATUS_SUCCESS_EMPTY

    result.duration_seconds = time.monotonic() - start
    write_critic_manifest(repo_root=repo_root, result=result, today=date_iso)
    return result


def _read_recent_titles(repo_root: Path, limit: int) -> list[str]:
    """Pull recent concept titles from vault/knowledge/index.md for prompt context.

    The index file's `## Concepts` section is the source of truth; titles
    surface in `[[path|Title]]` form per regenerate_index() in
    vault_synthesizer.py. Empty list on missing/unreadable index.
    """
    index_path = repo_root / KNOWLEDGE_INDEX_REL
    if not index_path.exists():
        return []
    try:
        text = index_path.read_text(encoding="utf-8")
    except OSError:
        return []
    in_concepts = False
    titles: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            in_concepts = line.strip().lower() == "## concepts"
            continue
        if not in_concepts:
            continue
        m = re.search(r"\[\[[^\]|]+\|([^\]]+)\]\]", line)
        if m:
            titles.append(m.group(1).strip())
            if len(titles) >= limit:
                break
    return titles
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 15 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/vault_critic.py agents-sdk/tests/test_vault_critic.py
git commit -m "feat(vault_critic): run orchestrator with status promotion + budget guard"
```

### Task D6: CLI entry point — main() with dry-run + record_run

- [ ] **Step 1: Write the failing test**

Append to `agents-sdk/tests/test_vault_critic.py`:

```python
from agents.vault_critic import main


def test_main_dry_run_lists_targets_without_calling_clis(tmp_repo, monkeypatch, capsys):
    today = "2026-05-22"
    p = _make_concept_at(tmp_repo, "x")
    _make_manifest(tmp_repo, today)
    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: [p])

    # Force the run() function to fail loudly if it's invoked under dry-run.
    async def must_not_call(*a, **k):
        raise AssertionError("run() must not be called under --dry-run")
    monkeypatch.setattr("agents.vault_critic.run", must_not_call)

    # Make sure load_config returns our tmp_repo.
    from lib.config import Config, SafetyConfig
    fake_config = Config(
        repo_root=tmp_repo, vault_root=tmp_repo / "vault",
        skills_dir=tmp_repo / ".claude/skills",
        life_systems_scripts=tmp_repo / "life-systems/scripts",
        log_dir=tmp_repo / "vault/90_system/agent-logs",
        log_level="INFO",
        safety=SafetyConfig(),
        agents={}, anthropic_api_key=None, artifacts={},
    )
    monkeypatch.setattr("agents.vault_critic.load_config", lambda: fake_config)

    rc = main(["--dry-run", "--date", today])
    assert rc == 0
    out = capsys.readouterr().out
    assert "DRY RUN" in out
    assert "x.md" in out
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py::test_main_dry_run_lists_targets_without_calling_clis -v
```

Expected: FAIL — main() takes no args yet.

- [ ] **Step 3: Write minimal implementation**

Append to `agents-sdk/agents/vault_critic.py`:

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vault Critic Agent")
    parser.add_argument("--dry-run", action="store_true",
                        help="List target articles without invoking CLIs.")
    parser.add_argument("--date", default=None,
                        help="ISO date for the synth-manifest to consume (default: today).")
    parser.add_argument("--max-targets", type=int, default=DEFAULT_MAX_TARGETS)
    parser.add_argument("--wall-budget-seconds", type=float, default=DEFAULT_WALL_BUDGET_S)
    parser.add_argument("--per-cli-timeout-seconds", type=int, default=DEFAULT_PER_CLI_TIMEOUT_S)
    args = parser.parse_args(argv)

    cfg = load_config()
    logger = setup_logger(AGENT_NAME, cfg.log_dir, cfg.log_level)
    date_iso = args.date or date.today().isoformat()

    targets = select_target_articles(
        cfg.repo_root, date_iso=date_iso, max_targets=args.max_targets,
    )

    if args.dry_run:
        print("=== DRY RUN — Vault Critic ===")
        print(f"Date:          {date_iso}")
        print(f"Repo:          {cfg.repo_root}")
        print(f"Max targets:   {args.max_targets}")
        print(f"Wall budget:   {args.wall_budget_seconds}s")
        print(f"CLI timeout:   {args.per_cli_timeout_seconds}s each")
        print(f"Targets ({len(targets)}):")
        for t in targets:
            print(f"  - {t.relative_to(cfg.repo_root)}")
        print("=== END DRY RUN ===")
        return 0

    start_ms = time.monotonic_ns()
    try:
        result = asyncio.run(run(
            repo_root=cfg.repo_root,
            date_iso=date_iso,
            max_targets=args.max_targets,
            wall_budget_s=args.wall_budget_seconds,
            per_cli_timeout_s=args.per_cli_timeout_seconds,
            logger=logger,
        ))
    except Exception as exc:
        logger.exception("vault_critic failed: %s", exc)
        record_run(
            cfg.log_dir, AGENT_NAME, mode=None,
            status="error", cost_usd=0.0,
            duration_ms=int((time.monotonic_ns() - start_ms) // 1_000_000),
            turns=None, notes=str(exc)[:200],
        )
        return 1

    duration_ms = int((time.monotonic_ns() - start_ms) // 1_000_000)
    record_run(
        cfg.log_dir, AGENT_NAME, mode=None,
        status=("success" if result.status in {STATUS_OK, STATUS_PARTIAL, STATUS_SUCCESS_EMPTY}
                else result.status),
        cost_usd=0.0,
        duration_ms=duration_ms,
        turns=None,
        notes=(
            f"status={result.status} "
            f"articles={result.articles_critiqued} "
            f"codex_fail={result.codex_failures} "
            f"ag_fail={result.antigravity_failures}"
        ),
    )
    logger.info(
        "vault_critic %s articles=%d codex_fail=%d ag_fail=%d duration=%.1fs",
        result.status, result.articles_critiqued,
        result.codex_failures, result.antigravity_failures,
        result.duration_seconds,
    )
    print(
        f"OK — vault_critic {result.status}: {result.articles_critiqued} articles "
        f"({result.codex_failures + result.antigravity_failures} CLI failures, "
        f"{result.duration_seconds:.1f}s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_vault_critic.py -v
```

Expected: 16 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/agents/vault_critic.py agents-sdk/tests/test_vault_critic.py
git commit -m "feat(vault_critic): main() entry point with dry-run + record_run wiring"
```

### Task D7: Verify the synthesizer-neighborhood suite still passes

- [ ] **Step 1: Run the synthesizer-neighborhood suite (the canonical pre-merge gate per CLAUDE.md v3.38.0)**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
  tests/test_vault_synthesizer.py \
  tests/test_retrieval_diversity.py \
  tests/test_concept_edges.py \
  tests/test_knowledge_lint.py \
  tests/test_synth_manifest.py \
  tests/test_cli_runners.py \
  tests/test_critique_prompt.py \
  tests/test_critic_selector.py \
  tests/test_vault_critic.py \
  -v
```

Expected: 91 (synthesizer baseline) + 16 + 6 + 6 + 15 = ~134 pass; the 91 baseline must hold (0 regressions). Three pre-existing unrelated failures named in CLAUDE.md (`test_doc_to_audio_cli`, `test_job_feed_e2e`, `test_route_to_macbook`) are NOT in this subset and remain out of scope.

- [ ] **Step 2: If any baseline test regressed, debug before continuing.** Do NOT proceed to Phase E with a broken synth-neighborhood gate.

---

## Phase E — launchd plist + config.toml + install_schedules.sh wiring

**Why this is Phase E:** the agent code is now tested in-process; the next step is putting it on the launchd schedule. Phase E is dry-run-then-live: install the plist, fire it manually once via `launchctl start`, verify the manifest is written, then walk away and let 03:30 do its thing tomorrow night.

**Files:**
- Create: `agents-sdk/schedules/com.sean.agent.vault-critic.plist`
- Modify: `agents-sdk/config.toml` (add `[agents.vault_critic]`)
- Modify: `agents-sdk/schedules/install_schedules.sh` (no edits needed; the loop picks up any new `*.plist` — but verify the `--list` output names the new file)

### Task E1: Author the launchd plist

- [ ] **Step 1: Write the plist file**

Create `agents-sdk/schedules/com.sean.agent.vault-critic.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sean.agent.vault-critic</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/.venv/bin/python3</string>
        <string>/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>3</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    <key>WorkingDirectory</key>
    <string>/Users/seanwinslow/Code-Brain/code-brain</string>
    <key>StandardOutPath</key>
    <string>/Users/seanwinslow/Code-Brain/code-brain/vault/90_system/agent-logs/vault-critic-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/seanwinslow/Code-Brain/code-brain/vault/90_system/agent-logs/vault-critic-stderr.log</string>
</dict>
</plist>
```

Note: `PATH` matches the launchd-PATH fix per `agents-sdk/BUGFIX-2026-04-07-launchd-path.md` and CLAUDE.md non-negotiable rule #5. Without `/opt/homebrew/bin` on PATH, `codex` and `gemini` are not discoverable and the agent fails with `FileNotFoundError`.

- [ ] **Step 2: Verify install_schedules.sh --list picks it up**

```bash
./agents-sdk/schedules/install_schedules.sh --list
```

Expected: output includes `com.sean.agent.vault-critic.plist` in the "Available schedules" block (with no opt-in suffix — it's default-enabled like deep-researcher).

- [ ] **Step 3: Commit**

```bash
git add agents-sdk/schedules/com.sean.agent.vault-critic.plist
git commit -m "feat(schedules): launchd plist for vault-critic at 03:30 with PATH env"
```

### Task E2: Add the config.toml block

- [ ] **Step 1: Append `[agents.vault_critic]` to `agents-sdk/config.toml`**

Insert immediately after the `[agents.deep_researcher]` block (line ~169):

```toml
[agents.vault_critic]
# Pattern 1 (2026-05-21) — nightly generative critique of synthesizer concept
# articles. Shells to Codex CLI (gpt-5.5) and Anti-Gravity CLI (Gemini 3.1 Pro)
# in parallel. Cost: $0 incremental on personal subscriptions. No Anthropic
# SDK in the nightly path; Sonnet fallback is OUT OF SCOPE for v1 (both-CLIs-
# rate-capped → status=partial, exits cleanly). Sequence: runs at 03:30 after
# vault_synthesizer (02:30) and deep_researcher (02:45), before daily_driver
# (08:30) and meta_agent (08:45).
enabled = true
skills = []
max_turns = 0                          # decorative — no Claude SDK loop in this agent
max_budget_usd = 0.00                  # decorative — costs absorbed by ChatGPT Plus + Google personal OAuth
schedule = "03:30"
target_machine = "mac_mini"
max_targets_per_run = 3
wall_budget_seconds = 600
per_cli_timeout_seconds = 120
output_dir = "vault/knowledge/expansions"
manifest_dir = "vault/health"
```

- [ ] **Step 2: Commit**

```bash
git add agents-sdk/config.toml
git commit -m "feat(config): register vault_critic agent at 03:30 daily, mac_mini, \$0/run"
```

### Task E3: Smoke-fire the plist once manually

- [ ] **Step 1: Symlink + load the plist**

```bash
./agents-sdk/schedules/install_schedules.sh
```

Expected: output names `com.sean.agent.vault-critic.plist` as installed.

- [ ] **Step 2: Trigger one manual fire**

```bash
launchctl start com.sean.agent.vault-critic
```

- [ ] **Step 3: Verify the run produced a manifest + log entries**

```bash
ls -lh vault/health/critic-manifest-$(date +%Y-%m-%d).json \
       vault/90_system/agent-logs/vault-critic-stdout.log \
       vault/90_system/agent-logs/vault-critic-stderr.log
cat vault/health/critic-manifest-$(date +%Y-%m-%d).json | head -30
grep vault-critic vault/90_system/agent-logs/agent-run-history.csv | tail -3
```

Expected: manifest file exists with `status: ok | partial | success-empty`. CSV has one new row. stderr log has no `FileNotFoundError`.

- [ ] **Step 4: If a manifest landed and the status is one of the expected values, the plist is wired correctly.** If `status: error`, debug from the stderr log before proceeding.

- [ ] **Step 5: Commit any plist / config tweaks if smoke fire surfaced issues**

```bash
# Only if changes were needed:
git add agents-sdk/schedules/com.sean.agent.vault-critic.plist agents-sdk/config.toml
git commit -m "fix(vault_critic): adjust plist/config from manual smoke fire"
```

---

## Phase F — daily_driver morning-brief integration

**Why this is Phase F:** without this, vault_critic output is invisible to Sean's morning workflow. The brief needs a one-line surface that says how many expansions were written last night and where they live.

**Files:**
- Modify: `agents-sdk/lib/lint_report.py` (add `latest_critic_manifest` + `critic_health_summary`)
- Modify: `agents-sdk/agents/daily_driver.py` (call the new helper in `build_preamble`)
- Modify: `agents-sdk/tests/test_daily_driver_vault_health.py` (extend existing tests with a critic-manifest case)

### Task F1: `latest_critic_manifest` + `critic_health_summary` — TDD

- [ ] **Step 1: Write the failing test**

Create `agents-sdk/tests/test_critic_health_summary.py`:

```python
import json
from pathlib import Path

import pytest

from lib.lint_report import critic_health_summary, latest_critic_manifest


@pytest.fixture
def tmp_vault(tmp_path):
    (tmp_path / "health").mkdir(parents=True)
    return tmp_path


def test_latest_critic_manifest_returns_most_recent(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-21.json").write_text("{}")
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text("{}")
    p = latest_critic_manifest(tmp_vault)
    assert p is not None
    assert p.name == "critic-manifest-2026-05-22.json"


def test_critic_health_summary_empty_when_no_manifest(tmp_vault):
    assert critic_health_summary(tmp_vault) == ""


def test_critic_health_summary_status_ok(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "ok",
            "articles_critiqued": 2,
            "codex_failures": 0,
            "antigravity_failures": 0,
            "duration_seconds": 87.3,
            "expansions_written": [
                "vault/knowledge/expansions/foo.md",
                "vault/knowledge/expansions/bar.md",
            ],
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "✓" in s or "ok" in s.lower()
    assert "2" in s   # articles count
    assert "expansions" in s.lower()


def test_critic_health_summary_status_partial_surfaces_failures(tmp_vault):
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "partial",
            "articles_critiqued": 1,
            "codex_failures": 1,
            "antigravity_failures": 0,
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "partial" in s.lower()
    assert "codex" in s.lower()


def test_critic_health_summary_status_success_empty(tmp_vault):
    """MBP-offline / synth-skipped night: vault_critic ran and exited cleanly."""
    (tmp_vault / "health" / "critic-manifest-2026-05-22.json").write_text(
        json.dumps({
            "status": "success-empty",
            "articles_critiqued": 0,
        })
    )
    s = critic_health_summary(tmp_vault)
    assert "no articles" in s.lower() or "0 articles" in s.lower()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critic_health_summary.py -v
```

Expected: FAIL with `ImportError`.

- [ ] **Step 3: Write minimal implementation**

Append to `agents-sdk/lib/lint_report.py`:

```python
def latest_critic_manifest(vault_root: Path) -> Path | None:
    """Return newest `vault/health/critic-manifest-*.json` or None.

    Sorts by name; the manifest filenames embed an ISO date so name-sort
    matches chronological order.
    """
    health_dir = vault_root / "health"
    if not health_dir.exists():
        return None
    manifests = sorted(health_dir.glob("critic-manifest-*.json"))
    return manifests[-1] if manifests else None


def critic_health_summary(vault_root: Path) -> str:
    """One-line summary of the latest vault_critic run for the morning brief.

    Returns '' when no manifest exists so the caller can suppress the line
    entirely. Mirrors synth_health_summary's empty-string contract.
    """
    manifest = latest_critic_manifest(vault_root)
    if not manifest:
        return ""
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(data, dict):
        return ""

    status = data.get("status", "unknown")
    n = data.get("articles_critiqued", 0)
    codex_fail = data.get("codex_failures", 0)
    ag_fail = data.get("antigravity_failures", 0)

    if status == "ok":
        return f"VAULT CRITIC ✓ — {n} expansions written (see {manifest.as_posix()})"
    if status == "success-empty":
        return f"VAULT CRITIC ○ — 0 articles to critique tonight (see {manifest.as_posix()})"
    if status == "partial":
        return (
            f"VAULT CRITIC ◐ — partial: {n} expansions written, "
            f"codex_failures={codex_fail}, antigravity_failures={ag_fail} "
            f"(see {manifest.as_posix()})"
        )
    return f"VAULT CRITIC ✗ — status `{status}` (see {manifest.as_posix()})"
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_critic_health_summary.py -v
```

Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/lint_report.py agents-sdk/tests/test_critic_health_summary.py
git commit -m "feat(lint_report): critic_health_summary for morning-brief surface"
```

### Task F2: Wire `critic_health_summary` into the daily-driver preamble

- [ ] **Step 1: Edit `agents-sdk/agents/daily_driver.py`**

In the `build_preamble` function, in the `if mode == "morning":` block (around line 261-276), add the critic_health_summary call BELOW the synth-manifest block:

Replace:
```python
        manifest_path = latest_synth_manifest(config.vault_root)
        if manifest_path:
            try:
                manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                manifest_data = {}
            base += render_vault_health(manifest_data) + "\n"
        artifact_block = build_artifact_preamble(config)
```

With:
```python
        manifest_path = latest_synth_manifest(config.vault_root)
        if manifest_path:
            try:
                manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                manifest_data = {}
            base += render_vault_health(manifest_data) + "\n"
        critic_line = critic_health_summary(config.vault_root)
        if critic_line:
            base += critic_line + "\n"
        artifact_block = build_artifact_preamble(config)
```

And update the import at line 47-51 to include `critic_health_summary`:

```python
from lib.lint_report import (  # noqa: E402
    critic_health_summary,
    latest_lint_report,
    latest_synth_manifest,
    vault_health_summary,
)
```

- [ ] **Step 2: Verify the daily-driver dry-run renders the new line**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run 2>&1 | grep -i "vault critic"
```

Expected: one line beginning with `VAULT CRITIC` (`○` for success-empty if no run has happened yet today, `✓` after first successful run).

- [ ] **Step 3: Run the daily-driver-vault-health test suite to confirm no regression**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_daily_driver_vault_health.py -v
```

Expected: PASS (none of those tests assert against the critic line; adding the line below them is additive).

- [ ] **Step 4: Commit**

```bash
git add agents-sdk/agents/daily_driver.py
git commit -m "feat(daily_driver): surface vault_critic manifest in morning brief"
```

---

## Phase G — fleet_summary + meta-agent surfacing

**Why this is Phase G:** the fleet overnight digest in the daily note must include vault-critic alongside the other 6 agents. Otherwise Sean's daily note has a gap.

**Files:**
- Modify: `agents-sdk/lib/fleet_summary.py` (add `vault-critic` to `AGENT_ORDER` + `AGENT_DISPLAY`)

### Task G1: Update fleet_summary constants — TDD

- [ ] **Step 1: Write the failing test**

Append to a new `agents-sdk/tests/test_fleet_summary_vault_critic.py`:

```python
from datetime import datetime
from pathlib import Path

import pytest

from lib.fleet_summary import build_fleet_overnight_digest, AGENT_ORDER, AGENT_DISPLAY


def test_agent_order_includes_vault_critic_after_deep_researcher():
    """vault_critic runs after deep_researcher (03:30 vs 02:45) and the
    display order should reflect the schedule sequence."""
    assert "vault-critic" in AGENT_ORDER
    dr_idx = AGENT_ORDER.index("deep-researcher")
    vc_idx = AGENT_ORDER.index("vault-critic")
    assert vc_idx > dr_idx


def test_agent_display_has_vault_critic_label():
    assert AGENT_DISPLAY["vault-critic"] == "Vault Critic"


def test_fleet_digest_renders_vault_critic_line(tmp_path):
    """When a vault-critic run is present in agent-run-history.csv, the
    digest names it explicitly."""
    repo_root = tmp_path
    csv = repo_root / "vault" / "90_system" / "agent-logs" / "agent-run-history.csv"
    csv.parent.mkdir(parents=True)
    csv.write_text(
        "date,time,agent,mode,status,cost_usd,duration_ms,turns,notes\n"
        "2026-05-22,03:30:01,vault-critic,,success,0.0000,180000,,"
        "status=ok articles=2 codex_fail=0 ag_fail=0\n"
    )
    vault_root = repo_root / "vault"
    digest = build_fleet_overnight_digest(
        repo_root=repo_root,
        vault_root=vault_root,
        now=datetime.fromisoformat("2026-05-22T08:30:00"),
    )
    assert "Vault Critic" in digest
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_fleet_summary_vault_critic.py -v
```

Expected: FAIL — `vault-critic` not in `AGENT_ORDER`.

- [ ] **Step 3: Edit `agents-sdk/lib/fleet_summary.py`**

In `AGENT_ORDER`, insert `"vault-critic"` after `"deep-researcher"`:

```python
AGENT_ORDER = [
    "vault-indexer",
    "vault-synthesizer",
    "deep-researcher",
    "vault-critic",
    "meta-agent",
    "daily-driver",
    "knowledge-lint",
    "flush",
]
```

And add to `AGENT_DISPLAY`:

```python
AGENT_DISPLAY = {
    "vault-indexer": "Vault Indexer",
    "vault-synthesizer": "Vault Synthesizer",
    "deep-researcher": "Deep Researcher",
    "vault-critic": "Vault Critic",
    "meta-agent": "Meta-Agent",
    "daily-driver": "Daily Driver",
    "knowledge-lint": "Knowledge Lint",
    "flush": "Session Flush",
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_fleet_summary_vault_critic.py tests/test_meta_agent_health.py -v
```

Expected: PASS (the meta-agent health tests confirm no regression on the existing AGENT_ORDER contract).

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_summary.py agents-sdk/tests/test_fleet_summary_vault_critic.py
git commit -m "feat(fleet_summary): include vault-critic in fleet overnight digest"
```

---

## Phase H — Mandatory doc updates

**Why this is Phase H:** CLAUDE.md non-negotiable rule §When Modifying mandates updates to CHANGELOG, CLAUDE.md, and README when a new SDK agent ships. These are pure-text edits — no TDD — but mandatory before merge.

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`
- Modify: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md` (Status Tracker only)

### Task H1: CHANGELOG.md entry

- [ ] **Step 1: Read the current CHANGELOG header to identify the unreleased version block**

```bash
head -30 CHANGELOG.md
```

- [ ] **Step 2: Add an `### Added` entry under the current unreleased / next version block**

Example shape (adjust version to match what's current):

```markdown
### Added

- **vault_critic agent (v3.39.0, Pattern 1)** — new nightly SDK agent at 03:30 daily that critiques newly-written concept articles from the synthesizer's 02:30 run by shelling to Codex CLI (gpt-5.5, ChatGPT Plus) and Anti-Gravity CLI (Gemini 3.1 Pro, Google personal OAuth) in parallel. Writes generative expansion files at `vault/knowledge/expansions/{slug}.md` naming 3 specific things Sean is missing per article. Cost: $0 incremental. Cap of 3 critiques per night, 600s wall budget, 120s per-CLI timeout. Both-CLIs-rate-capped → `status: partial`, exits cleanly (no Sonnet fallback in v1). Manifest at `vault/health/critic-manifest-{date}.json`. Surfaced in daily-driver morning brief under Vault Health + fleet overnight digest. Plan + intent at [`agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`](agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md). Smoke-test evidence at [`agents-sdk/docs/multi-cli-smoke-2026-05-21/`](agents-sdk/docs/multi-cli-smoke-2026-05-21/). Rollback: `./agents-sdk/schedules/install_schedules.sh --remove` + set `[agents.vault_critic].enabled = false` in `config.toml` — existing expansion files are preserved.
```

- [ ] **Step 3: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(changelog): vault_critic Pattern 1 agent ship"
```

### Task H2: CLAUDE.md updates

- [ ] **Step 1: Update the Architecture comment**

Change `13 Claude Code subagents, 14 hooks, 16 autonomous SDK agents (8 active on launchd, 1 manual-trigger)` to reflect the new agent count. Specifically: increment `16 autonomous SDK agents` → `17 autonomous SDK agents` and the `8 active on launchd` → `9 active on launchd`.

- [ ] **Step 2: Add `vault_critic` to the agents table**

In the "Active agents" table, insert a new row after `Deep Researcher`:

```markdown
| Vault Critic (NEW v3.39.0) | 3:30 AM daily | Codex CLI (gpt-5.5) + Anti-Gravity CLI (Gemini 3.1 Pro) — shell-out, no Claude SDK in path | $0 ($0 on ChatGPT Plus + Google personal OAuth) |
```

- [ ] **Step 3: Add a narrative paragraph under the existing knowledge-loop paragraphs**

Insert (chronologically positioned, e.g., right after the Tier 1.5 paragraph since vault_critic was born from the same 2026-05-21 review):

```markdown
**Vault Critic — generative critique layer (NEW v3.39.0, 2026-05-21):** Born from Sean's 2026-05-21 review surfacing the next-tier complaint after Tier 1.5 landed: the synthesizer describes what exists but can't tell him what's missing. Pure-Python orchestration agent at [`agents-sdk/agents/vault_critic.py`](agents-sdk/agents/vault_critic.py) that runs on launchd at 03:30 daily (after vault_synthesizer 02:30, deep_researcher 02:45, before daily-driver 08:30 and meta-agent 08:45). Reads today's Mac-Mini-canonical synth-manifest (PR-contamination-filtered per `feedback_synth_verify_filter_to_manifest.md`), selects up to 3 newly-written concept articles, and for each fans out two parallel subprocess critiques — Codex CLI (gpt-5.5 with `--sandbox read-only --skip-git-repo-check`, cwd=$HOME) and Anti-Gravity CLI (Gemini 3.1 Pro with `--output-format json --approval-mode plan`, `GEMINI_CLI_TRUST_WORKSPACE=true` set explicitly per invocation). Writes sibling expansion files at `vault/knowledge/expansions/{slug}.md` naming 3 specific things Sean is missing with named-author + named-work + sentence-pattern + genre-unlock specificity (smoke-tested 2026-05-21 — both CLIs independently named Joan Didion / *The White Album* as the #1 missing voice mode for the `writing-voice-modes` skill; full evidence at [`agents-sdk/docs/multi-cli-smoke-2026-05-21/`](agents-sdk/docs/multi-cli-smoke-2026-05-21/)). Per-run manifest at `vault/health/critic-manifest-{date}.json`. Cost: $0 incremental on existing personal subscriptions; no Anthropic SDK calls in the nightly path. Sonnet fallback is **out of scope for v1** — both-CLIs-rate-capped marks the run `status: partial` and exits cleanly, isolating Pattern 1 from any cloud-API blast radius. Wall-clock budget: 600s soft cap; per-CLI timeout: 120s. Surfaces in daily-driver morning brief under Vault Health + in meta-agent fleet overnight digest + in vault `02_Areas/Agent-Fleet/` snapshots. Patterns 2 (zero-cost LLM council profile) and 3 (HybridRouter CLI routing) are deferred per [`agents-sdk/docs/multi-cli-integration-patterns.md`](agents-sdk/docs/multi-cli-integration-patterns.md). Rollback: `./agents-sdk/schedules/install_schedules.sh --remove` + set `[agents.vault_critic].enabled = false` in `config.toml`; existing expansion files preserved.
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude-md): document vault_critic Pattern 1 ship + counts"
```

### Task H3: README.md updates

- [ ] **Step 1: Update top-line counts**

Find the README's hero text where agent counts surface (search for `autonomous SDK agents`); increment the SDK agent count by 1 and the active launchd count by 1.

- [ ] **Step 2: Add vault_critic to any agent-listing table in README**

If the README has an agents table mirroring CLAUDE.md's, add the same row.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs(readme): vault_critic Pattern 1 ship — counts + table"
```

### Task H4: Synthesizer retrofit plan Status Tracker update

- [ ] **Step 1: Edit `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`**

Find the `### Implementation status (2026-05-21)` paragraph under `## Follow-on layer` and replace the line:

> The integration patterns doc is written and the smoke tests passed. The next step is a structured implementation plan via the [`writing-plans`] skill in a fresh Claude Code session — the prompt to seed that session is captured in the 2026-05-21 working notes and lands at `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md` when produced. **Do not start implementation without that plan in hand**

With:

> The integration patterns doc is written, the smoke tests passed, and the **implementation plan landed at [`agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`](../../../../../agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md)** on 2026-05-21. The plan is TDD-ordered across 8 phases (A–H, ~3h15m total). v1 ships Pattern 1 only — Patterns 2 (zero-cost council profile) and 3 (HybridRouter CLI routing) are deferred per the plan's scope guard. Sonnet fallback is out of scope for v1 — both-CLIs-rate-capped → status=partial, exits cleanly. Verification gate to mark shipped-and-verified: 3 consecutive nights with manifest populated AND median random-sample of expansion files (drawn ONLY from Mac Mini manifest output per `feedback_synth_verify_filter_to_manifest.md`) reads as thinking-partner shape per `feedback_synth_verify_against_median_not_best.md`.

- [ ] **Step 2: Commit**

```bash
git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md
git commit -m "docs(retrofit-plan): point §Follow-on layer at vault-critic implementation plan"
```

---

## Risks + Mitigations

| # | Risk | Probability | Blast radius | Mitigation |
|---|---|---|---|---|
| 1 | **CLI rate-cap behavior unknown** — neither ChatGPT Plus nor Google personal-OAuth publish daily quotas for these endpoints. The smoke test was n=1. | Medium | Low — rate-cap marks run partial; expansions still write for the surviving CLI. | (a) `detect_rate_cap` heuristic surfaces caps in manifest; (b) monitor `critic_health_summary` for 3 consecutive nights; (c) the wall budget + per-CLI timeout prevent runaway calls; (d) hard cap of 3 articles/night = 6 messages/day = ~4% of conservative ChatGPT Plus 150-per-5h cap. |
| 2 | **Codex output format drift** — OpenAI auto-migrates between model versions (config has `gpt-5.3-codex → gpt-5.4` mapping). Stdout format could change. | Low | High — silent parser breakage would mean `tokens=None` everywhere and possibly empty `text`. | (a) `test_smoke_fixtures_replay_produces_expected_expansion_shape` is the regression test pinning today's known-good behavior; (b) `parse_codex_tokens` handles comma-tolerance + missing-footer cases; (c) `CLIResponse.ok` requires non-empty text via the caller, so blank stdout doesn't pretend to be a success. |
| 3 | **Anti-Gravity routed-model rename** — `auto-gemini-3` could route to a new model name in a future release. | Low | Low — `_antigravity_tokens` reads whatever single model key is present in `stats.models`, no hardcode. | (a) `test_run_antigravity_extracts_routed_model_from_stats` pins the model-agnostic parse; (b) display in expansion frontmatter says "Gemini 3" not "gemini-3.1-pro-preview" so future re-routing doesn't require a doc rewrite. |
| 4 | **MBP-side contamination recurring** — PR #52 was an isolated incident, but the MBP runs a parallel synthesizer on a stale checkout and the issue is not resolved. | High — likely to recur every few weeks. | Medium — would waste vault_critic compute on shallow articles, generating misleading expansion files. | (a) `select_target_articles` cross-references `git log --since/--until` against Mac Mini's auto-commit window — not mtime; (b) `test_select_target_articles_filters_to_manifest_count` is the regression test; (c) operational note in CLAUDE.md flags the recurring risk; (d) the long-term fix is resolving the MBP parallel-synth issue, out of scope here. |
| 5 | **One CLI catastrophically slow (>120s)** — Anti-Gravity smoke test was 43s, Codex 21s, but unknown variance under load. | Medium | Low — per-CLI timeout kicks in, CLIResponse.error is set, the other CLI still writes. | (a) `test_run_codex_timeout_returns_error_not_raise` + Anti-Gravity equivalent verify timeout handling; (b) the asyncio.gather is `return_exceptions=False` BUT both wrappers catch their own timeouts and return error responses (never raise), so gather completes; (c) `test_run_respects_wall_budget` verifies the outer agent skips remaining articles when its 600s budget runs out. |
| 6 | **Codex binary path drifts** — `/opt/homebrew/bin/codex` symlinked to `~/.codex/` was the smoke-test path; brew or codex upgrades might relocate. | Low | High — agent fails with FileNotFoundError every night until noticed. | (a) `run_codex` catches `FileNotFoundError` and returns a CLIResponse with explicit error (vs. raising); (b) launchd plist PATH is set explicitly per the v3.14 launchd-PATH bugfix — no inherited PATH dependency; (c) the meta-agent fleet status surfaces the error within ~8 hours via the morning brief. |
| 7 | **Trust flags accidentally inherit from env instead of being set explicitly** — a future refactor that "cleans up" the env dict could silently break the trust gate. | Low | Medium — agent would refuse to run from any non-trusted dir, or worse, run with surprise trust scope. | (a) `test_run_antigravity_replays_smoke_fixture` asserts on `env.get("GEMINI_CLI_TRUST_WORKSPACE") == "true"` — an explicit pinning test; (b) Codex uses the CLI flag `--skip-git-repo-check` not an env var, so refactor-resistant by construction. |
| 8 | **Expansion-file location collisions with future `vault/knowledge/{type}` tiers** — vault_synthesizer might someday emit `vault/knowledge/critiques/`. | Low | Medium — silent overwrite or path confusion. | (a) Pattern's expansion files live under `vault/knowledge/expansions/`, a tier the synthesizer doesn't touch; (b) `regenerate_index` in vault_synthesizer doesn't list expansions (separate concern); (c) if a future tier needs the name, Sean / future Claude will discover it via this plan + CHANGELOG entry. |

---

## Verification gate to mark v1 shipped-and-verified

This mirrors the gate pattern used by the Tier 1.5 retrofit (3 consecutive healthy nights + manual median review). Status promotion in the Status Tracker proceeds only when ALL of:

1. **Three consecutive nights with `vault/health/critic-manifest-{date}.json` populated** with `status: ok` or `status: success-empty` (success-empty on MBP-offline nights is expected and healthy).
2. **No `status: error` runs** across those three nights. Any error → investigate before promotion.
3. **For each of those nights, the daily note's Vault Health block shows the `VAULT CRITIC` line correctly.** Manual visual check; one screenshot per night logged in the Status Tracker.
4. **Sean reads ≥2 randomly-sampled expansion files from each successful night and confirms they read as thinking-partner shape.** Random sample is drawn ONLY from Mac Mini manifest output per [`feedback_synth_verify_filter_to_manifest.md`](../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_filter_to_manifest.md). Median, not best, per [`feedback_synth_verify_against_median_not_best.md`](../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_against_median_not_best.md).
5. **`grep -c "rate-capped or failed" vault/knowledge/expansions/*.md`** across those three nights is acceptable (≤1 expansion file marked with a CLI failure — n=1 doesn't justify Sonnet fallback yet).

**Failure modes that re-open the plan instead of promoting:**

- All three nights are `success-empty` because the synthesizer didn't run / MBP was offline → the gate hasn't tested anything real; extend to 3 nights of *non-empty* manifest signal.
- Expansion file shape regresses (output got more generic) → diagnose whether prompt template needs tightening or CLI behavior drifted; add a test pinning the regression.
- Codex or Anti-Gravity rate-caps on 2+ of 3 nights → consider whether v1's "skip Sonnet fallback" call needs revisiting; document the rate-cap rate before deciding.

---

## Rollback path

Each phase is independently revertable; the strongest emergency lever stops the agent entirely without losing already-written expansion files.

**Emergency stop (preserves expansions, manifests, log history):**

```bash
# 1. Disable the launchd schedule
launchctl unload ~/Library/LaunchAgents/com.sean.agent.vault-critic.plist
# 2. Remove the symlink
rm ~/Library/LaunchAgents/com.sean.agent.vault-critic.plist
# 3. Belt-and-suspenders: flip the config
sed -i.bak 's/^enabled = true$/enabled = false/' agents-sdk/config.toml  # carefully — applies to FIRST true match
# Better: edit by hand under [agents.vault_critic] specifically
```

**Full source-code revert:**

```bash
# Identify the commit range — H2/H1/H4 docs first, then phases G/F/E/D/C/B/A
git log --oneline -20 -- agents-sdk/agents/vault_critic.py
# Walk back commits in reverse order — see file map for the deletable files
git revert <newest>..<oldest>
# OR for a hard reset before merge:
git reset --hard <commit-before-A1>
```

**What stays even after rollback:**

- `vault/knowledge/expansions/*.md` files — these are useful artifacts even if the agent is paused; they live in the vault and don't depend on the agent existing.
- `vault/health/critic-manifest-*.json` files — useful audit trail.
- `vault/90_system/agent-logs/agent-run-history.csv` rows — append-only history.
- `agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md` — this plan.
- `agents-sdk/docs/multi-cli-smoke-2026-05-21/` — smoke-test evidence.

---

## Open questions — v1 resolution

The 5 open questions named in [`../multi-cli-integration-patterns.md`](../multi-cli-integration-patterns.md) §Open questions are resolved as follows for v1:

| # | Question | v1 resolution | Trigger to revisit |
|---|---|---|---|
| 1 | Codex output fencing (`<critique>` markers)? | **Deferred.** Smoke-test stdout was clean markdown with no preamble. The smoke-fixture replay test pins today's known-good shape. | Add fencing only if production runs surface drift (text leakage before recommendation #1, or trailing session metadata). |
| 2 | Convergence detection between Codex + Anti-Gravity? | **Deferred.** Cheap string-match on author names is tempting but n=1 (Didion in both smoke runs) is too small a sample to know whether convergence is signal or coincidence. | Revisit after 5+ real runs surface enough author overlap to characterize the base rate. |
| 3 | Article-count cap (3 fixed vs scaling)? | **Fixed at 3 for v1.** Simple, defensible, matches the rate-limit guard. | Revisit after 1 week if synthesizer routinely writes 10+ articles/night and Sean wants more critique surface. |
| 4 | Expansion file lifecycle on re-synthesis? | **Snapshot semantics.** `select_target_articles` skips concepts that already have an expansion file. Each expansion is a frozen point-in-time critique. | Revisit if Sean reports stale expansions blocking value when a concept is rewritten. |
| 5 | `skill_optimizer` footer in expansion file? | **Deferred.** Pattern 1 is the cheap nightly tier; skill_optimizer is the deep manual tier ($20-$145/run). Composition adds complexity without clear demand signal. | Revisit if Sean starts running skill_optimizer on critiqued concepts and wants the trigger to be discoverable from the expansion file. |

---

## Status Tracker

| Phase | Status | Began | Verified | Notes |
|---|---|---|---|---|
| A — CLI wrappers (`lib/cli_runners.py`) | pending | — | — | TDD via smoke-fixture replays; 15 tests planned. |
| B — Prompt builder (`lib/critique_prompt.py`) | pending | — | — | Pure function; 6 tests planned. |
| C — Target selector with contamination filter (`lib/critic_selector.py`) | pending | — | — | 6 tests planned including PR-contamination filter regression. |
| D — Main agent (`agents/vault_critic.py`) | pending | — | — | 16 tests planned across CritiqueResult / formatter / parallel fan-out / smoke replay / run orchestrator / main entry. |
| E — launchd plist + config.toml | pending | — | — | Includes one manual smoke fire via `launchctl start` before walking away. |
| F — daily_driver morning-brief integration | pending | — | — | 5 tests on `critic_health_summary` + one daily-driver dry-run verification. |
| G — fleet_summary + meta-agent surfacing | pending | — | — | 3 tests pinning the AGENT_ORDER + AGENT_DISPLAY contract. |
| H — Doc updates (CHANGELOG / CLAUDE.md / README / retrofit-plan) | pending | — | — | No TDD; pure-text edits per CLAUDE.md non-negotiable rule. |
| **First production-night verification** | pending | — | — | First night of `critic-manifest-{date}.json` with manifest fields populated. Run Sean's median-sample protocol per `feedback_synth_verify_against_median_not_best.md`. |
| **3-night verification gate** | pending | — | — | Promote to shipped-and-verified when all 5 conditions in the Verification gate section are met. |

---

## Pre-merge verification commands

Before opening the PR (or merging directly), run:

```bash
# 1. Synthesizer-neighborhood suite (the canonical gate per CLAUDE.md v3.38.0)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
  tests/test_vault_synthesizer.py \
  tests/test_retrieval_diversity.py \
  tests/test_concept_edges.py \
  tests/test_knowledge_lint.py \
  tests/test_synth_manifest.py \
  -v

# 2. New vault_critic neighborhood
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
  tests/test_cli_runners.py \
  tests/test_critique_prompt.py \
  tests/test_critic_selector.py \
  tests/test_vault_critic.py \
  tests/test_critic_health_summary.py \
  tests/test_fleet_summary_vault_critic.py \
  -v

# 3. Full repo validator (CLAUDE.md non-negotiable rule)
python3 scripts/validate.py

# 4. Smoke-fire the agent in dry-run before the first nightly fire
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/vault_critic.py --dry-run
```

Expected: (1) 91 pass (baseline holds); (2) 51 pass across new tests; (3) validator OK; (4) dry-run prints the expected target list or "0 targets" if synth hasn't run today.
