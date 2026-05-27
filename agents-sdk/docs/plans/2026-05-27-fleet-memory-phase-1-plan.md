# Fleet Memory Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a shared, path-traversal-hardened, namespaced filesystem-memory layer at `vault/90_system/fleet-memory/` that two pilot agents (`vault_synthesizer` and `daily_driver`) can write lessons to on one run and read back on the next — implementing Anthropic's `memory_20250818` protocol on the cloud side and a deterministic read-and-inject pattern on the local-Ollama side.

**Architecture:** A new `agents-sdk/lib/fleet_memory.py` module subclasses `anthropic.lib.tools.BetaAbstractMemoryTool` with all six required commands (`view` / `create` / `str_replace` / `insert` / `delete` / `rename`) routed through a single `_resolve_path()` guard that does `Path.realpath()` + prefix-check against the mount root and rejects any escape. Each agent is constructed with an `agent_id`, which scopes its writes to `fleet-memory/{agent_id}/`; promotion to `fleet-memory/shared/` requires an explicit `promote_to_shared()` helper (not a tool command — the agent has to call it deliberately). A `MEMORY_INDEX.md` at the mount root is rewritten by the helper after every mutation so the manifest-then-top-5 retrieval pattern works from day one. `daily_driver` (cloud, claude-agent-sdk) gets the tool via an MCP-server bridge (matching the existing `vault-tools` pattern in `lib/custom_tools.py`); `vault_synthesizer` (local Ollama, no Anthropic SDK in the hot path) gets a thin read-only `inject_memories_into_prompt()` helper that reads `MEMORY_INDEX.md` + the agent's namespace and prepends relevant entries to the synth prompt.

**Tech Stack:** `anthropic==0.101.0` (`BetaAbstractMemoryTool` + `BetaMemoryTool20250818*Command` types), `claude-agent-sdk==0.1.63` (MCP-server bridge for cloud agents), pure-Python filesystem I/O, existing `lib/config.py` for `[fleet_memory]` config, existing `lib/filelock.py` for `MEMORY_INDEX.md` write serialization, pytest matching `tests/test_artifact_loader.py` conventions.

---

## Non-Goals (explicit — surface during review)

These are out of scope for Phase 1 and must not creep in:

1. **Other 25 agents.** Only `vault_synthesizer` and `daily_driver` get wired up. Fleet rollout is Phase 2.
2. **CLAUDE.md feedback migration.** Moving the "do not do X" sections out of domain CLAUDE.md files into `fleet-memory/shared/feedback/` is Phase 2.
3. **Mem0 / Graphiti / Letta integration.** Phase 3 trigger logic isn't designed here; only named as a future outcome.
4. **Deduplication, contradiction resolution, or supersede semantics.** Both source reports flag Anthropic native memory's lack of dedup. We accept that limitation for Phase 1.
5. **Obsidian vault RAG (`nomic-embed-text` indexer) changes.** Document-scale retrieval stays untouched. Memory files are agent-scale lessons, not vault notes.
6. **Claude Code auto-memory (`~/.claude/projects/.../memory/`).** Run in parallel for the Phase 1 window; the consolidate-or-deprecate decision is Phase 2 audit.
7. **New launchd schedules.** This is a library + config + two-agent change. No new scheduled agents.
8. **Replacing `vault_critic`'s expansion files with memory entries.** The critic writes to `vault/knowledge/expansions/` and stays there.
9. **Anthropic SDK upgrade.** We use the pinned `claude-agent-sdk==0.1.63` and whatever `anthropic` version it transitively brings (currently 0.101.0 — `BetaAbstractMemoryTool` confirmed present).
10. **Cross-machine sync.** The mount lives in the vault, which the existing Mac Mini auto-commit process commits and `git pull` syncs. We do not build a new sync layer.

## Hard Constraints (verify each task respects these)

| # | Constraint | Source | Enforcement |
|---|---|---|---|
| C1 | All path operations go through `_resolve_path()` (realpath + prefix check). Reject `..`, symlinks-escaping-mount, absolute paths outside mount. | Synthesis Risk Register row 1; Perplexity DR developer-video citation | Task 2 (the guard); Task 3 (tests prove every command refuses escape) |
| C2 | Per-agent namespacing: writes go to `fleet-memory/{agent_id}/` unless explicitly promoted. | Synthesis §Phase 1 step 3; both source reports | Task 2 (`agent_id` constructor arg scopes every command); Task 7 (explicit promotion helper, not a tool command) |
| C3 | Vault sync ownership stays with the existing external Mac Mini auto-commit process — we add no new git operations. | CLAUDE.md rule 8 / issue #22 | Task 1 (verification step before any code is written); plan explicitly forbids `git add/commit` in `fleet_memory.py` |
| C4 | No new launchd schedules. | Synthesis §Phase 1; user's Step 3 constraint #4 | Task 0 confirms `agents-sdk/schedules/install_schedules.sh` is not touched |
| C5 | Pin SDK; document beta header. `claude-agent-sdk==0.1.63` is already pinned. The Anthropic `memory_20250818` tool requires the `context-management-2025-06-27` beta header on raw Anthropic SDK calls. For cloud agents using `claude-agent-sdk`, the betas list is set via `ClaudeAgentOptions.betas`. | User's Step 3 constraint #5 | Task 8 adds the beta to `daily_driver`'s `build_options`; Task 0 verifies the version. |
| C6 | Obsidian vault RAG untouched. | User's Step 3 constraint #6 | No file under `agents-sdk/agents/vault_indexer.py` is modified by this plan. |
| C7 | `~/.claude/projects/.../memory/` untouched. | User's Step 3 constraint #7 | No file under `~/.claude/projects/` is read or written by `fleet_memory.py`. |

---

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `agents-sdk/lib/fleet_memory.py` | **Create** | `BetaAbstractMemoryTool` subclass; `_resolve_path()` guard; namespacing logic; `MEMORY_INDEX.md` writer; `promote_to_shared()`; `inject_memories_into_prompt()` read-only helper for non-SDK agents. Single file because everything here is one coherent surface — splitting it would scatter the path-traversal guard. |
| `agents-sdk/tests/test_fleet_memory.py` | **Create** | Pytest suite matching `tests/test_artifact_loader.py` style. Path-traversal cases, namespacing cases, manifest-update cases, promotion cases, read-and-inject cases. |
| `agents-sdk/tests/fixtures/` (existing dir) | **Modify** | Add a `tmp_fleet_memory` fixture in `conftest.py` that creates the mount + bootstrap `MEMORY_INDEX.md`. Mirror `tmp_artifacts` shape. |
| `agents-sdk/tests/conftest.py` | **Modify** | Register the new fixture. |
| `agents-sdk/lib/custom_tools.py` | **Modify** | Add `create_fleet_memory_mcp_server(agent_id, mount_root)` factory next to the existing `create_vault_mcp_server()`. This is the bridge that makes the memory tool reachable from `daily_driver` (claude-agent-sdk doesn't accept `BetaAbstractMemoryTool` directly). |
| `agents-sdk/config.toml` | **Modify** | New `[fleet_memory]` section + `[fleet_memory.per_agent]` toggles. Mirror the `[artifacts]` block shape so the rollback story is "set enabled=false". |
| `agents-sdk/agents/daily_driver.py` | **Modify** | In `build_options()`: pull the fleet-memory MCP server from `custom_tools`, add it to `mcp_servers`, add `mcp__fleet-memory__memory` to `allowed_tools`, add `context-management-2025-06-27` to `betas`. In `build_preamble()` / `build_prompt()`: prepend the "you have a memory tool" instructions matching Anthropic's recommended pattern (view shared first, write lessons to your namespace). |
| `agents-sdk/agents/vault_synthesizer.py` | **Modify** | In `main()` / `run_synthesis()`: read `fleet-memory/MEMORY_INDEX.md` + the agent's own namespace once at start, inject as a "Lessons remembered from prior runs" block into `_build_synthesis_prompt()`. Write *successful-run* lessons (e.g. "produced N concepts from M files with model X") via `fleet_memory.create_or_append()` at end of `run_synthesis()`. **No** memory-tool protocol — synth talks to Ollama, not Anthropic. |
| `agents-sdk/tests/test_vault_synthesizer.py` | **Modify** | Add tests covering: prompt builder includes memory context when memory enabled; lesson is written on a successful run; no write on `wol-deferred` / `error`. |
| `agents-sdk/tests/test_daily_driver_*.py` | **Modify** | Add tests covering: `build_options` includes the fleet-memory MCP server when enabled; allowed_tools list includes `mcp__fleet-memory__memory`; betas list contains `context-management-2025-06-27`. |
| `vault/90_system/fleet-memory/MEMORY_INDEX.md` | **Create at runtime** | Bootstrapped on first `fleet_memory.ensure_mount()` call. Not in the repo at plan-execution time. |
| `vault/90_system/fleet-memory/{vault_synthesizer,daily_driver,shared}/.gitkeep` | **Create at runtime** | Same; ensures the empty namespaces exist on disk so the auto-commit process picks them up. |
| `CLAUDE.md` | **Modify** (Task 10) | Add a new row to the "Architecture decisions" table pointing at `fleet_memory.py` and the mount path. One line. |
| `evals/vault-synthesizer/cases.yaml` | **Modify** (Task 11) | Append 4 fleet-memory cases (vs-022 through vs-025). |
| `evals/vault-synthesizer/runner.py` | **Modify** (Task 11) | Add two new fixture-invocation helpers + dispatch for the new IDs. |
| `evals/vault-synthesizer/README.md` | **Modify** (Task 11) | Bump case-count language; document the Phase 1 fleet-memory addendum. |
| `evals/vault-synthesizer/traces/fixtures/memory-preamble.md` | **Create** (Task 11) | Synthetic preamble fixture for vs-022. |
| `evals/daily-driver/` (full directory) | **Create** (Task 12) | Mirror the synth eval-suite layout. README, cases.yaml (2 cases), runner.py, conftest.py, deferred-cases.yaml (4 deferred), failure-modes.md, last-run.md placeholder, traces/.gitkeep. |

---

## Task -1: Sync SDK venv to pin (prerequisite)

**Files:** None modified — this aligns the installed `claude-agent-sdk` with the version declared in `agents-sdk/pyproject.toml` so Phase 1's beta-header and memory-tool guarantees rest on a known surface.

**Why this is Task -1:** [pyproject.toml](agents-sdk/pyproject.toml) pins `claude-agent-sdk==0.1.63`, but the installed venv shows `0.1.56`. The SDK surface the fleet actually uses is narrow (`ClaudeAgentOptions`, `query`, `ResultMessage`, `create_sdk_mcp_server`, `tool`) — five names. A 0.1.56 → 0.1.63 bump is patch-level on a young project mostly hardening that surface; the existing pytest suite (679 tests) catches regressions before any memory code lands.

- [ ] **Step 1: Check current SDK version**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
.venv/bin/pip show claude-agent-sdk | grep Version
```
Expected output: `Version: 0.1.56` (the current drifted state).

- [ ] **Step 2: Sync to the pyproject pin**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
.venv/bin/pip install -e . --upgrade
.venv/bin/pip show claude-agent-sdk | grep Version
```
Expected: `Version: 0.1.63`.

- [ ] **Step 3: Run the full test suite to confirm no regressions**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
PYTHONPATH=. .venv/bin/pytest tests/ -v
```
Expected: All ~679 tests PASS. If any test fails, **stop and triage** — a 0.1.56 → 0.1.63 regression in the existing fleet is a separate problem from fleet-memory work, and shipping memory on top of a broken baseline is the wrong move. Diagnose the failure first.

- [ ] **Step 4: Re-confirm Task 0's import checks still pass**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
.venv/bin/python3 -c "from anthropic.lib.tools import BetaAbstractMemoryTool; print('OK')"
.venv/bin/python3 -c "from claude_agent_sdk import ClaudeAgentOptions; print(ClaudeAgentOptions(betas=['context-management-2025-06-27']).betas)"
```
Expected: `OK` and `['context-management-2025-06-27']`.

- [ ] **Step 5: Commit (no file changes, but tag the resolved state)**

There's nothing to commit code-wise (the venv isn't tracked). Note completion in the plan-execution log: `Task -1 done: claude-agent-sdk synced 0.1.56 → 0.1.63, 679/679 tests green.`

---

## Task 0: Pre-flight verification (no code)

**Files:** None modified — this task produces a written GO/NO-GO note in the plan-execution session.

- [ ] **Step 1: Confirm `BetaAbstractMemoryTool` is importable from the pinned SDK environment**

Run:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk
.venv/bin/python3 -c "from anthropic.lib.tools import BetaAbstractMemoryTool, BetaLocalFilesystemMemoryTool; print('OK')"
```
Expected: `OK` printed and exit 0.

If this fails: STOP. The pinned `claude-agent-sdk==0.1.63` is bringing in an `anthropic` version that doesn't expose the memory-tool primitives. Update the plan to either (a) upgrade the SDK pin, or (b) drop down to direct `anthropic` SDK usage.

- [ ] **Step 2: Confirm `ClaudeAgentOptions.betas` accepts the memory beta header**

Run:
```bash
.venv/bin/python3 -c "
from claude_agent_sdk import ClaudeAgentOptions
opts = ClaudeAgentOptions(betas=['context-management-2025-06-27'])
print('betas:', opts.betas)
"
```
Expected: `betas: ['context-management-2025-06-27']` and exit 0.

If this fails: STOP. The SDK doesn't surface beta headers; we need an alternative injection path. Either upgrade the SDK or call the raw `anthropic` SDK and bypass `claude-agent-sdk` for memory-aware runs.

- [ ] **Step 3: Verify the vault auto-commit mechanism covers `vault/90_system/`**

Run:
```bash
git log --since="14 days ago" --all --name-only --pretty=format: -- 'vault/90_system/' | sort -u | head -20
```
Expected: A non-empty list of files under `vault/90_system/` that have been auto-committed in the last two weeks. (`vault/90_system/agent-logs/`, `vault/90_system/audio/`, and `vault/90_system/templates/` are known to be active; presence of any of them confirms coverage.)

If this fails (empty output, or no commits with the `vault: auto-commit` shape touching `vault/90_system/`): STOP. The auto-commit process is **not** owning `vault/90_system/`. We must not silently add a new path that the external sync doesn't cover. Resolve before proceeding by either (a) extending the external script's path scope, or (b) choosing a different mount root that is covered.

- [ ] **Step 4: Confirm `.claude/settings.json` has no SessionEnd hook named `session-end-auto-commit.sh`**

Run:
```bash
grep -c "session-end-auto-commit" /Users/seanwinslow/Code-Brain/code-brain/.claude/settings.json
```
Expected: `0`.

This sanity-check documents that the vault auto-commit is **external** (a launchd job on the Mac Mini or similar), not a Claude Code hook. It matters because the plan must not try to "modify the auto-commit hook" — that hook isn't in this repo.

- [ ] **Step 5: Write down the GO/NO-GO note**

Append a one-line entry to the plan execution log: `Phase 1 pre-flight: GO — anthropic={ver}, claude_agent_sdk=0.1.63, vault/90_system/ auto-commit verified active.` If any step failed, replace with `NO-GO — {reason}` and stop.

---

## Task 1: Add `[fleet_memory]` config block

**Files:**
- Modify: `agents-sdk/config.toml` (append a new section after `[doc_to_audio]`)

- [ ] **Step 1: Write the failing config-loader test first**

Add to a new section at the end of `agents-sdk/tests/test_config.py`:

```python
def test_fleet_memory_config_loads_with_defaults(tmp_path, monkeypatch):
    """[fleet_memory] block is parsed; defaults are conservative."""
    from lib.config import load_config
    cfg = load_config()
    # Section exists
    assert hasattr(cfg, "fleet_memory") or "fleet_memory" in cfg.raw
    fm = cfg.raw.get("fleet_memory", {})
    assert fm.get("enabled") is False, "Phase 1 default must be disabled — opt-in only"
    assert fm.get("mount_subpath") == "90_system/fleet-memory"
    assert fm.get("manifest_filename") == "MEMORY_INDEX.md"
    assert fm["per_agent"]["vault_synthesizer"]["enabled"] is False
    assert fm["per_agent"]["daily_driver"]["enabled"] is False
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_config.py::test_fleet_memory_config_loads_with_defaults -v
```
Expected: FAIL with `KeyError: 'fleet_memory'` or `AssertionError`.

- [ ] **Step 3: Add the config block**

Append to `agents-sdk/config.toml`:

```toml
# ─── Fleet Memory (Phase 1 pilot, 2026-05-27) ─────────────────────────────
# Shared filesystem-memory layer for the agent fleet. Subclass of Anthropic's
# memory_20250818 protocol for cloud agents; deterministic read-and-inject
# pattern for local-Ollama agents. Mount lives inside the vault so it
# inherits the external auto-commit process (CLAUDE.md rule 8 / issue #22).
# See docs/plans/2026-05-27-fleet-memory-phase-1-plan.md.

[fleet_memory]
enabled = false                                # Phase 1 default: opt-in per-agent
mount_subpath = "90_system/fleet-memory"       # resolved relative to vault_root
manifest_filename = "MEMORY_INDEX.md"
manifest_max_chars = 8000                      # truncate before injecting into prompts
beta_header = "context-management-2025-06-27"

[fleet_memory.per_agent.vault_synthesizer]
enabled = false                                # opt-in toggle for smoke testing
agent_id = "vault_synthesizer"
inject_on_run = true                           # read MEMORY_INDEX + own namespace at start
write_lessons_on = ["ok"]                      # only write on clean runs; never partial/error

[fleet_memory.per_agent.daily_driver]
enabled = false                                # opt-in toggle for smoke testing
agent_id = "daily_driver"
inject_on_run = true                           # MCP server is mounted; preamble cues the agent to call view
write_lessons_on = ["success"]
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_config.py::test_fleet_memory_config_loads_with_defaults -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/config.toml agents-sdk/tests/test_config.py
git commit -m "feat(fleet-memory): add [fleet_memory] config block (Phase 1 default disabled)"
```

---

## Task 2: Implement `_resolve_path()` path-traversal guard

**Files:**
- Create: `agents-sdk/lib/fleet_memory.py`
- Test: `agents-sdk/tests/test_fleet_memory.py` (new file)

This task lands the guard *first* — before any tool-command implementation. The guard is the load-bearing safety check and we want it locked in before any command method can use it.

- [ ] **Step 1: Write the failing tests for `_resolve_path`**

Create `agents-sdk/tests/test_fleet_memory.py`:

```python
"""Tests for lib.fleet_memory — shared filesystem-memory layer."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


class TestResolvePathGuard:
    """The path-traversal guard is non-negotiable per CLAUDE.md / synthesis Risk Register."""

    def test_simple_relative_path_resolves_under_mount(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        resolved = _resolve_path(mount, "agent_id/note.md")
        assert resolved == (mount / "agent_id/note.md").resolve()

    def test_dotdot_escape_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "../../etc/passwd")

    def test_absolute_path_outside_mount_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "/etc/passwd")

    def test_symlink_escape_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        outside_file = outside / "secret.txt"
        outside_file.write_text("nope")
        link = mount / "evil_link"
        link.symlink_to(outside_file)
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "evil_link")

    def test_resolves_to_nonexistent_descendant(self, tmp_path: Path):
        """We must allow paths that don't exist yet (create command), as long
        as they would land under the mount."""
        from lib.fleet_memory import _resolve_path
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        resolved = _resolve_path(mount, "new_agent/new_lesson.md")
        assert str(resolved).startswith(str(mount.resolve()))
        assert not resolved.exists()

    def test_empty_path_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "")
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestResolvePathGuard -v
```
Expected: All six FAIL with `ImportError: cannot import name '_resolve_path' from 'lib.fleet_memory'` (module doesn't exist yet).

- [ ] **Step 3: Implement `_resolve_path` and the exception type**

Create `agents-sdk/lib/fleet_memory.py`:

```python
"""Shared filesystem-memory layer for the agent fleet.

Subclasses Anthropic's BetaAbstractMemoryTool (memory_20250818) for cloud
agents and exposes a read-only `inject_memories_into_prompt()` helper for
local-Ollama agents that don't speak the tool protocol.

Mount: vault/90_system/fleet-memory/ (resolved from config.toml).
Namespacing: {mount}/{agent_id}/ for per-agent state, {mount}/shared/ for
cross-agent lessons. Promotion to shared is via explicit promote_to_shared()
call — never an implicit tool command.

Path traversal is the load-bearing safety check: every read/write goes
through _resolve_path(), which performs realpath + prefix containment.
Any attempt to escape the mount via .., absolute paths, or symlinks raises
PathEscapeError.

See agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger("fleet_memory")


class PathEscapeError(ValueError):
    """A memory command tried to access a path outside the mount root."""


def _resolve_path(mount_root: Path, raw_path: str) -> Path:
    """Resolve `raw_path` against `mount_root`, rejecting any escape.

    Args:
        mount_root: The fleet-memory mount directory. Must already exist.
        raw_path: A relative path the caller wants to access inside the mount.
            An empty string is rejected.

    Returns:
        The fully-resolved absolute path, guaranteed to live under
        `mount_root.resolve()`. The path itself may not exist yet (the
        memory-tool `create` command needs to write new files); the guard
        only ensures *where it would land* is inside the mount.

    Raises:
        PathEscapeError: If `raw_path` is empty, if it resolves outside the
            mount (via `..`, absolute path, or symlink chain), or if any
            intermediate component is a symlink pointing outside the mount.
    """
    if not raw_path:
        raise PathEscapeError("empty path")

    mount_real = mount_root.resolve()
    if not mount_real.exists():
        raise PathEscapeError(f"mount root does not exist: {mount_real}")

    candidate = (mount_real / raw_path).resolve()

    # Containment check via Path semantics (handles cross-platform separators
    # correctly; string prefix would false-positive on /tmp/fleet vs /tmp/fleet2).
    try:
        candidate.relative_to(mount_real)
    except ValueError as exc:
        raise PathEscapeError(
            f"path escapes mount: candidate={candidate} mount={mount_real}"
        ) from exc

    return candidate
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestResolvePathGuard -v
```
Expected: All six PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py
git commit -m "feat(fleet-memory): add _resolve_path traversal guard (Phase 1 step 1/9)"
```

---

## Task 3: Implement `ensure_mount()` and bootstrap layout

**Files:**
- Modify: `agents-sdk/lib/fleet_memory.py`
- Modify: `agents-sdk/tests/test_fleet_memory.py`
- Modify: `agents-sdk/tests/conftest.py` (add fixture)

- [ ] **Step 1: Write the failing tests**

Append to `agents-sdk/tests/test_fleet_memory.py`:

```python
class TestEnsureMount:
    def test_creates_mount_and_namespaces_idempotently(self, tmp_path: Path):
        from lib.fleet_memory import ensure_mount
        mount = tmp_path / "fleet-memory"
        ensure_mount(mount, agent_ids=["vault_synthesizer", "daily_driver"])
        assert mount.is_dir()
        assert (mount / "shared").is_dir()
        assert (mount / "vault_synthesizer").is_dir()
        assert (mount / "daily_driver").is_dir()
        assert (mount / "MEMORY_INDEX.md").is_file()
        # Idempotent: a second call must not raise and must not clobber.
        (mount / "shared" / "marker.md").write_text("existing")
        ensure_mount(mount, agent_ids=["vault_synthesizer", "daily_driver"])
        assert (mount / "shared" / "marker.md").read_text() == "existing"

    def test_manifest_has_well_known_header(self, tmp_path: Path):
        from lib.fleet_memory import ensure_mount
        mount = tmp_path / "fleet-memory"
        ensure_mount(mount, agent_ids=["vault_synthesizer"])
        manifest = (mount / "MEMORY_INDEX.md").read_text()
        assert manifest.startswith("# Fleet Memory Index")
        assert "_Auto-generated by lib.fleet_memory" in manifest
```

Append to `agents-sdk/tests/conftest.py` (next to the `tmp_artifacts` fixture if present, or at file end):

```python
@pytest.fixture
def tmp_fleet_memory(tmp_path: Path):
    """A bootstrapped fleet-memory mount with the two pilot namespaces."""
    from lib.fleet_memory import ensure_mount
    mount = tmp_path / "fleet-memory"
    ensure_mount(mount, agent_ids=["vault_synthesizer", "daily_driver"])
    return mount
```

(If `conftest.py` doesn't already import `pytest` and `Path`, add those imports.)

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestEnsureMount -v
```
Expected: FAIL with `ImportError: cannot import name 'ensure_mount'`.

- [ ] **Step 3: Implement `ensure_mount`**

Append to `agents-sdk/lib/fleet_memory.py`:

```python
MANIFEST_HEADER = (
    "# Fleet Memory Index\n\n"
    "_Auto-generated by lib.fleet_memory. Do not edit by hand._\n\n"
    "One-line summary per memory file. Used by agents for the\n"
    "manifest-then-top-5 retrieval pattern (Perplexity DR, Apr 2026).\n\n"
)


def ensure_mount(mount_root: Path, *, agent_ids: list[str]) -> None:
    """Create the mount layout idempotently.

    Layout:
        {mount_root}/
            shared/
            {agent_id}/         (one per id passed in)
            MEMORY_INDEX.md     (created with header if absent)

    Existing files are never overwritten. Safe to call on every run.
    """
    mount_root.mkdir(parents=True, exist_ok=True)
    (mount_root / "shared").mkdir(exist_ok=True)
    for aid in agent_ids:
        (mount_root / aid).mkdir(exist_ok=True)
    manifest = mount_root / "MEMORY_INDEX.md"
    if not manifest.exists():
        manifest.write_text(MANIFEST_HEADER, encoding="utf-8")
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestEnsureMount -v
```
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py agents-sdk/tests/conftest.py
git commit -m "feat(fleet-memory): add ensure_mount bootstrap (Phase 1 step 2/9)"
```

---

## Task 4: Implement `FleetMemoryTool` — `view` and `create` commands

**Files:**
- Modify: `agents-sdk/lib/fleet_memory.py`
- Modify: `agents-sdk/tests/test_fleet_memory.py`

This task lands the `BetaAbstractMemoryTool` subclass scaffolding plus the two simplest commands. Subsequent tasks add the remaining four (`str_replace`, `insert`, `delete`, `rename`).

- [ ] **Step 1: Write the failing tests for view + create**

Append to `agents-sdk/tests/test_fleet_memory.py`:

```python
class TestFleetMemoryToolViewCreate:
    def test_constructor_requires_agent_id(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        with pytest.raises(TypeError):
            FleetMemoryTool(mount_root=tmp_fleet_memory)  # type: ignore[call-arg]

    def test_view_lists_agent_namespace(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        ns = tmp_fleet_memory / "vault_synthesizer"
        (ns / "lesson-1.md").write_text("first")
        (ns / "lesson-2.md").write_text("second")
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        result = tool._view_path("vault_synthesizer/")
        assert "lesson-1.md" in result
        assert "lesson-2.md" in result

    def test_view_reads_file_body(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        ns = tmp_fleet_memory / "vault_synthesizer"
        (ns / "lesson.md").write_text("# Lesson\nDon't trust mock retrievers.\n")
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        result = tool._view_path("vault_synthesizer/lesson.md")
        assert "Lesson" in result
        assert "Don't trust mock retrievers." in result

    def test_view_rejects_path_escape(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, PathEscapeError
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        with pytest.raises(PathEscapeError):
            tool._view_path("../../../etc/passwd")

    def test_create_writes_to_agent_namespace(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path(
            "vault_synthesizer/pr52-stale-checkout.md",
            "PR #52 wrote pre-Tier-2 articles. Always filter to manifest.",
        )
        on_disk = tmp_fleet_memory / "vault_synthesizer/pr52-stale-checkout.md"
        assert on_disk.read_text().startswith("PR #52")

    def test_create_rejects_writes_outside_own_namespace(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, NamespaceViolation
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        # Synth must not write into daily_driver/ directly.
        with pytest.raises(NamespaceViolation):
            tool._create_path("daily_driver/sneaky.md", "no")

    def test_create_allows_writes_to_shared(self, tmp_fleet_memory: Path):
        """Writes to shared/ are *allowed* by the namespace guard — the actual
        promotion ergonomics live in the explicit promote_to_shared() helper
        (Task 7). But the tool isn't blocked from writing directly to shared/
        because that's how an agent flushes an already-validated lesson."""
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("shared/cross-fleet-lesson.md", "All agents read this.")
        assert (tmp_fleet_memory / "shared/cross-fleet-lesson.md").exists()
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestFleetMemoryToolViewCreate -v
```
Expected: All seven FAIL with `ImportError: cannot import name 'FleetMemoryTool'`.

- [ ] **Step 3: Implement the class skeleton + view + create**

Append to `agents-sdk/lib/fleet_memory.py`:

```python
from anthropic.lib.tools import BetaAbstractMemoryTool
from anthropic.types.beta import (
    BetaMemoryTool20250818CreateCommand,
    BetaMemoryTool20250818DeleteCommand,
    BetaMemoryTool20250818InsertCommand,
    BetaMemoryTool20250818RenameCommand,
    BetaMemoryTool20250818StrReplaceCommand,
    BetaMemoryTool20250818ViewCommand,
)


class NamespaceViolation(ValueError):
    """A tool tried to write outside its agent_id namespace AND outside shared/."""


class FleetMemoryTool(BetaAbstractMemoryTool):
    """Per-agent memory tool scoped to {mount_root}/{agent_id}/ for writes.

    Reads are allowed from anywhere under the mount (so agents can see
    shared/ and peer namespaces); writes are restricted to the agent's
    own namespace plus shared/. Use promote_to_shared() for an explicit,
    auditable promotion path.
    """

    def __init__(
        self,
        *,
        mount_root: Path,
        agent_id: str,
    ) -> None:
        super().__init__()
        if not agent_id:
            raise ValueError("agent_id is required")
        self._mount_root = mount_root
        self._agent_id = agent_id

    # ─── path discipline helpers ───────────────────────────────────────

    def _resolve(self, raw_path: str) -> Path:
        # Strip any leading "/memories/" prefix the Anthropic protocol uses.
        # Agents see paths as "/memories/vault_synthesizer/foo.md" but on
        # disk we mount at {mount_root}/vault_synthesizer/foo.md.
        relpath = raw_path.lstrip("/")
        if relpath.startswith("memories/"):
            relpath = relpath[len("memories/"):]
        return _resolve_path(self._mount_root, relpath)

    def _assert_write_allowed(self, target: Path) -> None:
        rel = target.relative_to(self._mount_root.resolve())
        first = rel.parts[0] if rel.parts else ""
        if first == self._agent_id or first == "shared":
            return
        raise NamespaceViolation(
            f"agent={self._agent_id} tried to write {rel} — only "
            f"{self._agent_id}/** and shared/** are writable"
        )

    # ─── internal command implementations (testable without SDK objects) ──

    def _view_path(self, raw_path: str) -> str:
        target = self._resolve(raw_path)
        if target.is_dir():
            entries = sorted(p.name for p in target.iterdir())
            return "\n".join(entries) if entries else "(empty)"
        return target.read_text(encoding="utf-8")

    def _create_path(self, raw_path: str, body: str) -> str:
        target = self._resolve(raw_path)
        self._assert_write_allowed(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        return f"created {target.relative_to(self._mount_root.resolve())}"

    # ─── BetaAbstractMemoryTool overrides (thin dispatch) ──────────────

    def view(self, command: BetaMemoryTool20250818ViewCommand) -> str:
        return self._view_path(command.path)

    def create(self, command: BetaMemoryTool20250818CreateCommand) -> str:
        return self._create_path(command.path, command.file_text)

    # The remaining four are stubs until Task 5 lands them.
    def str_replace(self, command: BetaMemoryTool20250818StrReplaceCommand) -> str:
        raise NotImplementedError("str_replace lands in Task 5")

    def insert(self, command: BetaMemoryTool20250818InsertCommand) -> str:
        raise NotImplementedError("insert lands in Task 5")

    def delete(self, command: BetaMemoryTool20250818DeleteCommand) -> str:
        raise NotImplementedError("delete lands in Task 5")

    def rename(self, command: BetaMemoryTool20250818RenameCommand) -> str:
        raise NotImplementedError("rename lands in Task 5")
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestFleetMemoryToolViewCreate -v
```
Expected: All seven PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py
git commit -m "feat(fleet-memory): FleetMemoryTool with view+create commands (Phase 1 step 3/9)"
```

---

## Task 5: Implement remaining four memory commands

**Files:**
- Modify: `agents-sdk/lib/fleet_memory.py`
- Modify: `agents-sdk/tests/test_fleet_memory.py`

The Anthropic protocol's six commands match a subset of `str_replace_editor`. We mirror that surface so any Anthropic-recommended retrieval pattern works unchanged.

- [ ] **Step 1: Write failing tests for str_replace, insert, delete, rename**

Append to `agents-sdk/tests/test_fleet_memory.py`:

```python
class TestFleetMemoryToolRemainingCommands:
    def test_str_replace_replaces_unique_match(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/note.md", "Lesson: trust mocks.")
        tool._str_replace_path(
            "vault_synthesizer/note.md", "trust mocks", "do not trust mocks"
        )
        assert (tmp_fleet_memory / "vault_synthesizer/note.md").read_text() == (
            "Lesson: do not trust mocks."
        )

    def test_str_replace_raises_on_missing_old(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/note.md", "Lesson: trust mocks.")
        with pytest.raises(ValueError):
            tool._str_replace_path("vault_synthesizer/note.md", "missing-text", "x")

    def test_str_replace_raises_on_multiple_matches(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/note.md", "a a a")
        with pytest.raises(ValueError):
            tool._str_replace_path("vault_synthesizer/note.md", "a", "b")

    def test_insert_inserts_after_line_number(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/note.md", "line1\nline3\n")
        tool._insert_path("vault_synthesizer/note.md", insert_line=1, insert_text="line2\n")
        assert (tmp_fleet_memory / "vault_synthesizer/note.md").read_text() == (
            "line1\nline2\nline3\n"
        )

    def test_delete_removes_file(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/note.md", "x")
        tool._delete_path("vault_synthesizer/note.md")
        assert not (tmp_fleet_memory / "vault_synthesizer/note.md").exists()

    def test_delete_refuses_paths_outside_writable_namespaces(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, NamespaceViolation
        # Create a peer file via direct disk write — simulating daily_driver's file.
        peer = tmp_fleet_memory / "daily_driver" / "peer.md"
        peer.write_text("peer")
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        with pytest.raises(NamespaceViolation):
            tool._delete_path("daily_driver/peer.md")

    def test_rename_moves_within_writable_namespaces(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/old.md", "x")
        tool._rename_path("vault_synthesizer/old.md", "vault_synthesizer/new.md")
        assert not (tmp_fleet_memory / "vault_synthesizer/old.md").exists()
        assert (tmp_fleet_memory / "vault_synthesizer/new.md").read_text() == "x"

    def test_rename_refuses_cross_namespace_target(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, NamespaceViolation
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool._create_path("vault_synthesizer/x.md", "x")
        with pytest.raises(NamespaceViolation):
            tool._rename_path("vault_synthesizer/x.md", "daily_driver/x.md")
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestFleetMemoryToolRemainingCommands -v
```
Expected: All eight FAIL with `AttributeError: 'FleetMemoryTool' object has no attribute '_str_replace_path'` (and similar for the others).

- [ ] **Step 3: Implement the four commands**

In `agents-sdk/lib/fleet_memory.py`, replace the four `NotImplementedError` stubs and add the four `_*_path()` internal methods. The new methods go above the public overrides for readability:

```python
    # ─── internal command implementations (continued) ──────────────────

    def _str_replace_path(self, raw_path: str, old: str, new: str) -> str:
        target = self._resolve(raw_path)
        self._assert_write_allowed(target)
        body = target.read_text(encoding="utf-8")
        count = body.count(old)
        if count == 0:
            raise ValueError(f"old string not found in {raw_path}")
        if count > 1:
            raise ValueError(
                f"old string appears {count} times in {raw_path}; must be unique"
            )
        target.write_text(body.replace(old, new), encoding="utf-8")
        return f"str_replace ok in {raw_path}"

    def _insert_path(self, raw_path: str, insert_line: int, insert_text: str) -> str:
        target = self._resolve(raw_path)
        self._assert_write_allowed(target)
        body = target.read_text(encoding="utf-8")
        lines = body.splitlines(keepends=True)
        if insert_line < 0 or insert_line > len(lines):
            raise ValueError(
                f"insert_line {insert_line} out of range for {raw_path} "
                f"(0..{len(lines)})"
            )
        new_lines = lines[:insert_line] + [insert_text] + lines[insert_line:]
        target.write_text("".join(new_lines), encoding="utf-8")
        return f"insert ok in {raw_path}"

    def _delete_path(self, raw_path: str) -> str:
        target = self._resolve(raw_path)
        self._assert_write_allowed(target)
        if target.is_dir():
            raise ValueError(f"refusing to delete directory {raw_path}")
        target.unlink()
        return f"deleted {raw_path}"

    def _rename_path(self, old_raw: str, new_raw: str) -> str:
        old_target = self._resolve(old_raw)
        new_target = self._resolve(new_raw)
        self._assert_write_allowed(old_target)
        self._assert_write_allowed(new_target)
        new_target.parent.mkdir(parents=True, exist_ok=True)
        old_target.rename(new_target)
        return f"renamed {old_raw} -> {new_raw}"
```

Then replace the four public override stubs:

```python
    def str_replace(self, command: BetaMemoryTool20250818StrReplaceCommand) -> str:
        return self._str_replace_path(command.path, command.old_str, command.new_str)

    def insert(self, command: BetaMemoryTool20250818InsertCommand) -> str:
        return self._insert_path(command.path, command.insert_line, command.insert_text)

    def delete(self, command: BetaMemoryTool20250818DeleteCommand) -> str:
        return self._delete_path(command.path)

    def rename(self, command: BetaMemoryTool20250818RenameCommand) -> str:
        return self._rename_path(command.old_path, command.new_path)
```

(Field names — `old_str`/`new_str`, `old_path`/`new_path`, `insert_text`/`insert_line` — must match the actual `BetaMemoryTool20250818*Command` dataclass attribute names from `anthropic==0.101.0`. The task-9 type-check step verifies these names; if mismatched, fix the override to use the real attribute names.)

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestFleetMemoryToolRemainingCommands -v
```
Expected: All eight PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py
git commit -m "feat(fleet-memory): str_replace/insert/delete/rename (Phase 1 step 4/9)"
```

---

## Task 6: Implement `MEMORY_INDEX.md` manifest writer

**Files:**
- Modify: `agents-sdk/lib/fleet_memory.py`
- Modify: `agents-sdk/tests/test_fleet_memory.py`

The manifest is what makes the Perplexity-DR "manifest-then-top-5" pattern work past 200 files. Every successful mutation appends or updates a one-line entry under the agent's heading. Concurrent writes serialize via the existing `lib/filelock.py`.

- [ ] **Step 1: Write failing tests for the manifest updater**

Append to `agents-sdk/tests/test_fleet_memory.py`:

```python
class TestManifestUpdate:
    def test_manifest_appends_entry_under_agent_heading(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(
            slug="pr52-stale-checkout",
            summary="Filter critic candidates to synth manifest, not mtime.",
            body="# PR #52 Stale Checkout\n\nThe MBP runs a parallel pre-retrofit ...",
        )
        manifest = (tmp_fleet_memory / "MEMORY_INDEX.md").read_text()
        assert "## vault_synthesizer" in manifest
        assert "pr52-stale-checkout" in manifest
        assert "Filter critic candidates" in manifest

    def test_second_write_does_not_duplicate_heading(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="a", summary="A", body="A")
        tool.write_lesson(slug="b", summary="B", body="B")
        manifest = (tmp_fleet_memory / "MEMORY_INDEX.md").read_text()
        assert manifest.count("## vault_synthesizer") == 1

    def test_rewriting_same_slug_updates_in_place(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="x", summary="first version", body="A")
        tool.write_lesson(slug="x", summary="second version", body="B")
        manifest = (tmp_fleet_memory / "MEMORY_INDEX.md").read_text()
        assert manifest.count("- x:") == 1
        assert "second version" in manifest
        assert "first version" not in manifest
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestManifestUpdate -v
```
Expected: All three FAIL with `AttributeError: 'FleetMemoryTool' object has no attribute 'write_lesson'`.

- [ ] **Step 3: Implement `write_lesson` + manifest updater**

Add imports to the top of `agents-sdk/lib/fleet_memory.py`:

```python
import re
from lib.filelock import FileLock
```

Append to `agents-sdk/lib/fleet_memory.py`:

```python
_MANIFEST_LINE_RE_TEMPLATE = r"^- {slug}:.*$"


def _update_manifest_section(
    manifest_path: Path,
    *,
    agent_id: str,
    slug: str,
    summary: str,
) -> None:
    """Idempotently upsert a `- {slug}: {summary}` line under `## {agent_id}`.

    Serialized via FileLock so multiple agents writing concurrently can't
    interleave heading creation. Pure file I/O; never raises on missing
    sections — creates the section on first use.
    """
    lock = FileLock(manifest_path.with_suffix(manifest_path.suffix + ".lock"),
                    exclusive=True, timeout=10.0)
    with lock:
        body = manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else MANIFEST_HEADER
        heading = f"## {agent_id}"
        line = f"- {slug}: {summary}"
        line_re = re.compile(
            _MANIFEST_LINE_RE_TEMPLATE.format(slug=re.escape(slug)),
            re.MULTILINE,
        )
        if heading not in body:
            body = body.rstrip() + f"\n\n{heading}\n\n{line}\n"
        elif line_re.search(body):
            body = line_re.sub(line, body)
        else:
            # Insert immediately under the heading.
            body = body.replace(heading + "\n", heading + "\n\n" + line + "\n", 1)
        manifest_path.write_text(body, encoding="utf-8")


# Add as a method on FleetMemoryTool:
class FleetMemoryTool(BetaAbstractMemoryTool):  # noqa — extended
    ...
    def write_lesson(self, *, slug: str, summary: str, body: str) -> str:
        """High-level helper: write a lesson under the agent's namespace AND
        upsert the manifest entry. Used by agents that don't speak the tool
        protocol (vault_synthesizer) or that want to record a lesson outside
        the LLM loop (deterministic post-run signals)."""
        if "/" in slug or slug.startswith("."):
            raise ValueError(f"invalid slug: {slug}")
        raw_path = f"{self._agent_id}/{slug}.md"
        self._create_path(raw_path, body)
        _update_manifest_section(
            self._mount_root / "MEMORY_INDEX.md",
            agent_id=self._agent_id,
            slug=slug,
            summary=summary,
        )
        return f"wrote lesson {raw_path} + manifest"
```

(Note: in the actual implementation, the second `class FleetMemoryTool` block above is meant as a continuation hint — the method is added to the existing class definition, not redeclared. The plan executor must insert `write_lesson` and the supporting `_update_manifest_section` function into the existing module, not literally copy the second class definition.)

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py::TestManifestUpdate -v
```
Expected: All three PASS.

- [ ] **Step 5: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py
git commit -m "feat(fleet-memory): MEMORY_INDEX.md manifest writer (Phase 1 step 5/9)"
```

---

## Task 7: Add `promote_to_shared()` and `inject_memories_into_prompt()` helpers

**Files:**
- Modify: `agents-sdk/lib/fleet_memory.py`
- Modify: `agents-sdk/tests/test_fleet_memory.py`

Two helpers for the non-tool-protocol surface:
1. `promote_to_shared()` — explicit cross-agent publication (synthesis requirement: "promotion to shared is an explicit tool call, never automatic").
2. `inject_memories_into_prompt()` — read-only manifest + body reader for agents like `vault_synthesizer` that don't speak the tool protocol.

- [ ] **Step 1: Write failing tests**

Append to `agents-sdk/tests/test_fleet_memory.py`:

```python
class TestPromoteToShared:
    def test_promote_copies_file_to_shared_with_provenance(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="x", summary="X", body="content")
        tool.promote_to_shared(slug="x")
        shared = tmp_fleet_memory / "shared/from-vault_synthesizer-x.md"
        assert shared.exists()
        text = shared.read_text()
        assert "content" in text
        assert "promoted_from: vault_synthesizer/x.md" in text  # provenance frontmatter

    def test_promote_appends_to_shared_section_in_manifest(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="x", summary="X", body="content")
        tool.promote_to_shared(slug="x")
        manifest = (tmp_fleet_memory / "MEMORY_INDEX.md").read_text()
        assert "## shared" in manifest
        assert "from-vault_synthesizer-x" in manifest


class TestInjectMemoriesIntoPrompt:
    def test_returns_empty_when_disabled(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import inject_memories_into_prompt
        result = inject_memories_into_prompt(
            mount_root=tmp_fleet_memory, agent_id="vault_synthesizer", enabled=False
        )
        assert result == ""

    def test_returns_manifest_plus_own_namespace_bodies(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, inject_memories_into_prompt
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="pr52", summary="PR52 lesson", body="filter to manifest")
        # Simulate a peer-written shared lesson:
        (tmp_fleet_memory / "shared/general.md").write_text("Trust no mock retriever.")
        result = inject_memories_into_prompt(
            mount_root=tmp_fleet_memory, agent_id="vault_synthesizer", enabled=True
        )
        assert "PR52 lesson" in result          # manifest summary visible
        assert "filter to manifest" in result   # own-namespace body included
        assert "Trust no mock retriever." in result  # shared/ body included

    def test_truncates_at_max_chars(self, tmp_fleet_memory: Path):
        from lib.fleet_memory import FleetMemoryTool, inject_memories_into_prompt
        tool = FleetMemoryTool(mount_root=tmp_fleet_memory, agent_id="vault_synthesizer")
        tool.write_lesson(slug="big", summary="big", body="x" * 50_000)
        result = inject_memories_into_prompt(
            mount_root=tmp_fleet_memory, agent_id="vault_synthesizer",
            enabled=True, max_chars=2000,
        )
        assert len(result) <= 2000 + 100  # +100 cushion for the truncation marker
        assert "(truncated)" in result
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py -k "promote or inject" -v
```
Expected: All five FAIL with `AttributeError` / `ImportError`.

- [ ] **Step 3: Implement both helpers**

Append to `agents-sdk/lib/fleet_memory.py`:

Add method on `FleetMemoryTool`:

```python
    def promote_to_shared(self, *, slug: str) -> str:
        """Copy {agent_id}/{slug}.md → shared/from-{agent_id}-{slug}.md
        with provenance frontmatter. Explicit cross-agent publication
        — never automatic; agents must call this deliberately."""
        src = self._resolve(f"{self._agent_id}/{slug}.md")
        if not src.exists():
            raise ValueError(f"source lesson does not exist: {self._agent_id}/{slug}.md")
        dest_slug = f"from-{self._agent_id}-{slug}"
        provenance = (
            f"---\n"
            f"promoted_from: {self._agent_id}/{slug}.md\n"
            f"promoted_at: {__import__('datetime').date.today().isoformat()}\n"
            f"---\n\n"
        )
        body = provenance + src.read_text(encoding="utf-8")
        dest = self._mount_root / "shared" / f"{dest_slug}.md"
        dest.write_text(body, encoding="utf-8")
        _update_manifest_section(
            self._mount_root / "MEMORY_INDEX.md",
            agent_id="shared",
            slug=dest_slug,
            summary=f"promoted from {self._agent_id}/{slug}",
        )
        return f"promoted {self._agent_id}/{slug} -> shared/{dest_slug}"
```

Add module-level function:

```python
def inject_memories_into_prompt(
    *,
    mount_root: Path,
    agent_id: str,
    enabled: bool,
    max_chars: int = 8000,
) -> str:
    """Read-only memory injection for agents that don't speak the tool protocol.

    Returns a single markdown string ready to prepend to an LLM prompt.
    Format:

        # Lessons remembered from prior runs

        ## Manifest

        {full MEMORY_INDEX.md body}

        ## Your namespace ({agent_id}/)

        {body of every .md file under {mount_root}/{agent_id}/}

        ## Shared lessons (shared/)

        {body of every .md file under {mount_root}/shared/}

    Truncates at `max_chars` and appends "(truncated)" if anything was cut.
    Returns "" when `enabled=False` — caller can unconditionally string-concat.
    """
    if not enabled:
        return ""
    parts: list[str] = ["# Lessons remembered from prior runs\n"]
    manifest = mount_root / "MEMORY_INDEX.md"
    if manifest.exists():
        parts.append("## Manifest\n")
        parts.append(manifest.read_text(encoding="utf-8"))
    for label, ns in (("Your namespace", agent_id), ("Shared lessons", "shared")):
        ns_dir = mount_root / ns
        if not ns_dir.is_dir():
            continue
        parts.append(f"\n## {label} ({ns}/)\n")
        for f in sorted(ns_dir.glob("*.md")):
            parts.append(f"\n### {f.name}\n")
            parts.append(f.read_text(encoding="utf-8"))
    combined = "\n".join(parts)
    if len(combined) > max_chars:
        combined = combined[:max_chars] + "\n\n(truncated)\n"
    return combined
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py -k "promote or inject" -v
```
Expected: All five PASS.

- [ ] **Step 5: Run the full test_fleet_memory module to catch regressions**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory.py -v
```
Expected: All tests across all classes PASS (totals roughly: 6 guard + 2 mount + 7 view/create + 8 commands + 3 manifest + 5 promote/inject = 31 tests).

- [ ] **Step 6: Commit**

```bash
git add agents-sdk/lib/fleet_memory.py agents-sdk/tests/test_fleet_memory.py
git commit -m "feat(fleet-memory): promote_to_shared + inject_memories_into_prompt (Phase 1 step 6/9)"
```

---

## Task 8: Wire `vault_synthesizer` to read memory + write lessons

**Files:**
- Modify: `agents-sdk/agents/vault_synthesizer.py`
- Modify: `agents-sdk/tests/test_vault_synthesizer.py`

This task connects the synthesizer (local Ollama, no Anthropic SDK in the loop) to the memory layer via the **read-only injection** helper plus a `write_lesson` call on clean runs.

- [ ] **Step 1: Write the failing test for prompt injection**

Append to `agents-sdk/tests/test_vault_synthesizer.py`:

```python
class TestFleetMemoryWiring:
    def test_memory_injection_prepended_to_prompt_when_enabled(self, tmp_path, monkeypatch):
        """When [fleet_memory.per_agent.vault_synthesizer].enabled=true, the
        synth prompt builder receives a memory preamble from the mount."""
        from agents import vault_synthesizer as vs
        from lib import fleet_memory

        mount = tmp_path / "fleet-memory"
        fleet_memory.ensure_mount(mount, agent_ids=["vault_synthesizer"])
        tool = fleet_memory.FleetMemoryTool(mount_root=mount, agent_id="vault_synthesizer")
        tool.write_lesson(
            slug="pr52", summary="Filter to manifest, not mtime.",
            body="Lesson: PR #52 stale-checkout incident.",
        )
        preamble = fleet_memory.inject_memories_into_prompt(
            mount_root=mount, agent_id="vault_synthesizer", enabled=True
        )
        assert "Filter to manifest" in preamble
        assert "PR #52" in preamble

    def test_lesson_written_on_clean_run(self, tmp_path):
        """A successful run (status=ok, concepts_written>0) writes a one-line
        lesson capturing the run's notable signal."""
        from lib import fleet_memory
        from agents.vault_synthesizer import _maybe_write_run_lesson, SynthesisResult, STATUS_OK

        mount = tmp_path / "fleet-memory"
        fleet_memory.ensure_mount(mount, agent_ids=["vault_synthesizer"])
        result = SynthesisResult(status=STATUS_OK)
        result.concepts_written = 3
        result.connections_written = 1
        result.model_used = "qwen3.6_35b-a3b-32k"
        result.run_id = "2026-05-27T03:00:00"
        _maybe_write_run_lesson(mount_root=mount, result=result, enabled=True)
        ns = mount / "vault_synthesizer"
        lessons = list(ns.glob("*.md"))
        assert len(lessons) == 1
        assert "qwen3.6_35b-a3b-32k" in lessons[0].read_text()

    def test_no_lesson_on_error_run(self, tmp_path):
        from lib import fleet_memory
        from agents.vault_synthesizer import _maybe_write_run_lesson, SynthesisResult, STATUS_ERROR

        mount = tmp_path / "fleet-memory"
        fleet_memory.ensure_mount(mount, agent_ids=["vault_synthesizer"])
        result = SynthesisResult(status=STATUS_ERROR)
        _maybe_write_run_lesson(mount_root=mount, result=result, enabled=True)
        assert list((mount / "vault_synthesizer").glob("*.md")) == []

    def test_no_lesson_when_disabled(self, tmp_path):
        from lib import fleet_memory
        from agents.vault_synthesizer import _maybe_write_run_lesson, SynthesisResult, STATUS_OK

        mount = tmp_path / "fleet-memory"
        fleet_memory.ensure_mount(mount, agent_ids=["vault_synthesizer"])
        result = SynthesisResult(status=STATUS_OK)
        result.concepts_written = 1
        _maybe_write_run_lesson(mount_root=mount, result=result, enabled=False)
        assert list((mount / "vault_synthesizer").glob("*.md")) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_vault_synthesizer.py::TestFleetMemoryWiring -v
```
Expected: All four FAIL with `ImportError: cannot import name '_maybe_write_run_lesson'`.

- [ ] **Step 3: Add `_maybe_write_run_lesson` to `vault_synthesizer.py`**

Add near the top of `agents-sdk/agents/vault_synthesizer.py` (after imports, before the existing `AGENT_NAME = "vault-synthesizer"` constant):

```python
from lib import fleet_memory as _fleet_memory  # noqa: E402


def _maybe_write_run_lesson(
    *,
    mount_root: Path,
    result: "SynthesisResult",
    enabled: bool,
) -> None:
    """Write a one-line run-lesson to fleet-memory if the run was clean.

    Only fires on status=ok with concepts_written>0. Lesson body captures
    model_used / concepts_written / connections_written / clusters_sampled
    so future runs can recall "what shape of run produces what output."
    No-op when disabled or when run was not clean.
    """
    if not enabled:
        return
    if result.status != STATUS_OK or result.concepts_written == 0:
        return
    tool = _fleet_memory.FleetMemoryTool(
        mount_root=mount_root, agent_id="vault_synthesizer"
    )
    slug = f"run-{result.run_id.replace(':', '-')}"
    summary = (
        f"{result.concepts_written}c/{result.connections_written}x "
        f"via {result.model_used}"
    )
    body = (
        f"# Run lesson — {result.run_id}\n\n"
        f"- model_used: {result.model_used}\n"
        f"- concepts_written: {result.concepts_written}\n"
        f"- connections_written: {result.connections_written}\n"
        f"- clusters_sampled: {result.clusters_sampled}\n"
        f"- rejected_count: {result.rejected_count}\n"
        f"- duration_seconds: {result.duration_seconds:.1f}\n"
    )
    tool.write_lesson(slug=slug, summary=summary, body=body)
```

- [ ] **Step 4: Wire memory into `run_synthesis` (Option 3 — orchestrator placement)**

The chosen placement is the **orchestrator**, not the caller-factory and not the prompt builder. Rationale: `_build_synthesis_prompt` stays pure (no test churn across the existing prompt-builder tests); `_default_llm_caller_factory` stays focused on transport + JSON parsing (uncoupled from memory state); `run_synthesis` already coordinates run-wide context (`run_id`, `manifest_state`, `db_conn`) so memory is at the right level of abstraction.

Modify `run_synthesis(...)` signature to accept a memory preamble:

```python
def run_synthesis(
    *,
    vault_root: Path,
    changed_files: list[Path],
    llm_caller: Callable[..., dict],
    retriever: Callable[..., list[dict[str, Any]]],
    now_iso: str | None = None,
    budget_seconds: int = DEFAULT_BUDGET_SECONDS,
    top_k: int = 5,
    db_conn: sqlite3.Connection | None = None,
    classifier_version: str | None = None,
    logger: logging.Logger | None = None,
    memory_preamble: str = "",     # NEW — empty string disables injection
) -> SynthesisResult:
```

Inside the per-file loop in `run_synthesis`, find the existing block:

```python
        prompt = _build_synthesis_prompt(
            primary_file_rel=str(fp.relative_to(vault_root)),
            primary_text=primary_text,
            similar=similar,
            existing_titles=existing_titles,
        )
        try:
            parsed = llm_caller(prompt)
```

Insert a memory-preamble prepend between `_build_synthesis_prompt` and `llm_caller`:

```python
        prompt = _build_synthesis_prompt(
            primary_file_rel=str(fp.relative_to(vault_root)),
            primary_text=primary_text,
            similar=similar,
            existing_titles=existing_titles,
        )
        if memory_preamble:
            prompt = memory_preamble + "\n\n" + prompt
        try:
            parsed = llm_caller(prompt)
```

The caller factory (`_default_llm_caller_factory`) is **not** touched. The prompt builder (`_build_synthesis_prompt`) is **not** touched. Only `run_synthesis` itself learns about memory.

In `main()`, after `cfg = load_config()` and before the `run_synthesis(...)` call, add the load-and-inject block:

```python
    # Fleet memory (Phase 1 pilot, 2026-05-27).
    fm_cfg = cfg.raw.get("fleet_memory", {})
    fm_agent_cfg = fm_cfg.get("per_agent", {}).get("vault_synthesizer", {})
    fm_enabled = bool(fm_cfg.get("enabled") and fm_agent_cfg.get("enabled"))
    fm_mount = cfg.vault_root / fm_cfg.get("mount_subpath", "90_system/fleet-memory")
    if fm_enabled:
        _fleet_memory.ensure_mount(fm_mount, agent_ids=["vault_synthesizer", "daily_driver"])
    memory_preamble = _fleet_memory.inject_memories_into_prompt(
        mount_root=fm_mount, agent_id="vault_synthesizer", enabled=fm_enabled,
        max_chars=fm_cfg.get("manifest_max_chars", 8000),
    )
```

Update the existing `run_synthesis(...)` call to pass the preamble:

```python
        result = run_synthesis(
            vault_root=cfg.vault_root,
            changed_files=changed,
            llm_caller=llm,
            retriever=retriever,
            budget_seconds=args.budget_seconds,
            db_conn=db_conn,
            classifier_version=(
                f"{manifest_state.get('model_used', 'unknown')}/{today_iso}"
            ),
            logger=logger,
            memory_preamble=memory_preamble,    # NEW
        )
```

After `run_synthesis(...)` returns (after the existing `result.model_used = ...` lines and the manifest write), add:

```python
    _maybe_write_run_lesson(mount_root=fm_mount, result=result, enabled=fm_enabled)
```

Also add a unit-test case asserting the orchestrator-level placement (append to `TestFleetMemoryWiring` from Step 1):

```python
    def test_run_synthesis_prepends_memory_preamble_to_prompt(self, tmp_path):
        """When memory_preamble is non-empty, run_synthesis prepends it before
        every per-file llm_caller invocation. Verified by capturing what
        llm_caller receives."""
        from agents.vault_synthesizer import run_synthesis

        captured: list[str] = []

        def mock_llm(prompt: str, max_tokens: int = 2000) -> dict:
            captured.append(prompt)
            return {"concepts": [], "connections": []}

        def mock_retriever(query: str, top_k: int = 5, **kw):
            return []

        note = tmp_path / "note.md"
        note.write_text("---\ntype: note\n---\n\nbody")
        # Pushover stubs so ensure_credentials_or_raise passes
        import os
        os.environ.setdefault("PUSHOVER_USER_KEY", "stub")
        os.environ.setdefault("PUSHOVER_API_TOKEN", "stub")

        run_synthesis(
            vault_root=tmp_path,
            changed_files=[note],
            llm_caller=mock_llm,
            retriever=mock_retriever,
            budget_seconds=30,
            memory_preamble="# Lessons remembered\n\nLesson A",
        )
        assert captured, "llm_caller was not invoked"
        assert captured[0].startswith("# Lessons remembered")
        assert "Lesson A" in captured[0]

    def test_run_synthesis_omits_preamble_when_empty(self, tmp_path):
        from agents.vault_synthesizer import run_synthesis

        captured: list[str] = []

        def mock_llm(prompt: str, max_tokens: int = 2000) -> dict:
            captured.append(prompt)
            return {"concepts": [], "connections": []}

        def mock_retriever(query: str, top_k: int = 5, **kw):
            return []

        note = tmp_path / "note.md"
        note.write_text("---\ntype: note\n---\n\nbody")
        import os
        os.environ.setdefault("PUSHOVER_USER_KEY", "stub")
        os.environ.setdefault("PUSHOVER_API_TOKEN", "stub")

        run_synthesis(
            vault_root=tmp_path,
            changed_files=[note],
            llm_caller=mock_llm,
            retriever=mock_retriever,
            budget_seconds=30,
            memory_preamble="",
        )
        assert captured
        assert not captured[0].startswith("# Lessons remembered")
```

- [ ] **Step 5: Run the tests to verify all four pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_vault_synthesizer.py::TestFleetMemoryWiring -v
```
Expected: All four PASS.

- [ ] **Step 6: Run the existing synth test suite to catch regressions**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_vault_synthesizer.py tests/test_synth_manifest.py -v
```
Expected: PASS (no regressions in existing 80+ synth tests).

- [ ] **Step 7: Commit**

```bash
git add agents-sdk/agents/vault_synthesizer.py agents-sdk/tests/test_vault_synthesizer.py
git commit -m "feat(fleet-memory): wire vault_synthesizer to memory layer (Phase 1 step 7/9)"
```

---

## Task 9: Wire `daily_driver` via MCP-server bridge

**Files:**
- Modify: `agents-sdk/lib/custom_tools.py`
- Modify: `agents-sdk/agents/daily_driver.py`
- Modify: `agents-sdk/tests/test_daily_driver_artifacts.py` (or whichever test file covers `build_options`)

The cloud daily-driver gets the real Anthropic memory tool. `claude-agent-sdk` doesn't accept `BetaAbstractMemoryTool` instances directly; we expose the tool as an MCP server, the same pattern used by `vault-tools`.

**Verified SDK shape (read from `agents-sdk/lib/custom_tools.py`):**
- Decorator: `from claude_agent_sdk import create_sdk_mcp_server, tool` — single name `tool`, not `sdk_tool`.
- Decorator signature: `@tool(name: str, description: str, input_schema: dict[str, type])` — positional args, schema is a flat `{field_name: python_type}` dict.
- Handler signature: `async def fn(args: dict[str, Any]) -> dict[str, Any]`.
- Success return shape: `{"content": [{"type": "text", "text": "..."}]}`.
- Error return shape: `{"content": [{"type": "text", "text": "..."}], "is_error": True}`.
- Server factory: `create_sdk_mcp_server(name=..., version=..., tools=[fn1, fn2, ...])`.

**Design choice:** expose **six separate MCP tools** (`memory_view`, `memory_create`, `memory_str_replace`, `memory_insert`, `memory_delete`, `memory_rename`) rather than one `memory` tool with a `command` field. The model handles typed schemas more reliably than a discriminated-union string field, and `allowed_tools` matching is per-name in the CLI permission layer. Each handler is a thin shim into the matching `FleetMemoryTool._{command}_path` method built in Tasks 4–5.

- [ ] **Step 1: Write failing test for the MCP-server factory**

Add a new test file `agents-sdk/tests/test_fleet_memory_mcp.py`:

```python
"""Tests for the fleet-memory MCP-server bridge used by daily_driver."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_factory_returns_a_server_object(tmp_path: Path):
    """Factory returns whatever create_sdk_mcp_server returns — we don't
    assert on its internal shape, only that the call succeeds and that
    side effects (mount bootstrap) happen."""
    from lib.custom_tools import create_fleet_memory_mcp_server
    mount = tmp_path / "fleet-memory"
    server = create_fleet_memory_mcp_server(
        agent_id="daily_driver", mount_root=mount,
    )
    assert server is not None
    # Side effect: ensure_mount fired
    assert (mount / "daily_driver").is_dir()
    assert (mount / "shared").is_dir()
    assert (mount / "MEMORY_INDEX.md").exists()


@pytest.mark.asyncio
async def test_memory_create_tool_writes_to_namespace(tmp_path: Path):
    """The memory_create handler routes through FleetMemoryTool._create_path
    and produces the standard MCP success envelope."""
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_create"](
        {"path": "/memories/daily_driver/note.md", "file_text": "hello"}
    )
    assert "is_error" not in result
    assert result["content"][0]["type"] == "text"
    assert (mount / "daily_driver/note.md").read_text() == "hello"


@pytest.mark.asyncio
async def test_memory_view_returns_text_envelope(tmp_path: Path):
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    (mount / "daily_driver" / "x.md").write_text("body")
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_view"]({"path": "/memories/daily_driver/x.md"})
    assert "is_error" not in result
    assert result["content"][0]["text"] == "body"


@pytest.mark.asyncio
async def test_path_escape_returns_error_envelope_not_raise(tmp_path: Path):
    """When the underlying _resolve_path raises PathEscapeError, the MCP
    handler must catch it and return is_error=True — never let the SDK
    process crash."""
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_view"]({"path": "/memories/../../etc/passwd"})
    assert result.get("is_error") is True
    assert "PathEscapeError" in result["content"][0]["text"]
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory_mcp.py -v
```
Expected: All four FAIL with `ImportError: cannot import name 'create_fleet_memory_mcp_server'` / `_build_memory_handlers`.

- [ ] **Step 3: Implement the MCP-server factory**

Open `agents-sdk/lib/custom_tools.py`. The current shape is:

```python
from claude_agent_sdk import create_sdk_mcp_server, tool
from .vault_io import inject_at_anchor

@tool("vault_inject", "...description...", {"file_path": str, "anchor_name": str, "content": str})
async def vault_inject_tool(args: dict[str, Any]) -> dict[str, Any]:
    ...
    return {"content": [{"type": "text", "text": "..."}]}
    # error path: return {"content": [...], "is_error": True}

def create_vault_mcp_server():
    return create_sdk_mcp_server(name="vault-tools", version="1.0.0", tools=[vault_inject_tool])
```

Append to that file (after `create_vault_mcp_server`):

```python
from lib.fleet_memory import FleetMemoryTool, ensure_mount


def _ok(text: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def _err(exc: Exception) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
        "is_error": True,
    }


def _build_memory_handlers(
    *,
    agent_id: str,
    mount_root: Path,
) -> dict[str, Any]:
    """Return a dict of six async handlers, one per memory command.

    Extracted from `create_fleet_memory_mcp_server` so unit tests can call
    the handlers directly without spinning up an MCP server. Each handler
    catches every exception and returns the MCP error envelope — the SDK
    process must never crash on bad model input.
    """
    ensure_mount(mount_root, agent_ids=[agent_id])
    fmt = FleetMemoryTool(mount_root=mount_root, agent_id=agent_id)

    async def memory_view(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._view_path(args["path"]))
        except Exception as exc:
            return _err(exc)

    async def memory_create(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._create_path(args["path"], args["file_text"]))
        except Exception as exc:
            return _err(exc)

    async def memory_str_replace(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._str_replace_path(
                args["path"], args["old_str"], args["new_str"],
            ))
        except Exception as exc:
            return _err(exc)

    async def memory_insert(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._insert_path(
                args["path"], args["insert_line"], args["insert_text"],
            ))
        except Exception as exc:
            return _err(exc)

    async def memory_delete(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._delete_path(args["path"]))
        except Exception as exc:
            return _err(exc)

    async def memory_rename(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._rename_path(args["old_path"], args["new_path"]))
        except Exception as exc:
            return _err(exc)

    return {
        "memory_view": memory_view,
        "memory_create": memory_create,
        "memory_str_replace": memory_str_replace,
        "memory_insert": memory_insert,
        "memory_delete": memory_delete,
        "memory_rename": memory_rename,
    }


def create_fleet_memory_mcp_server(*, agent_id: str, mount_root: Path):
    """Expose six memory-protocol tools as an in-process MCP server.

    Mirrors create_vault_mcp_server's shape. Each tool maps 1:1 onto an
    Anthropic memory_20250818 command, routed into the namespace-scoped
    FleetMemoryTool built in lib/fleet_memory.py.

    Tool names visible to the CLI (`allowed_tools` matchers):
        mcp__fleet-memory__memory_view
        mcp__fleet-memory__memory_create
        mcp__fleet-memory__memory_str_replace
        mcp__fleet-memory__memory_insert
        mcp__fleet-memory__memory_delete
        mcp__fleet-memory__memory_rename
    """
    handlers = _build_memory_handlers(agent_id=agent_id, mount_root=mount_root)

    view_tool = tool(
        "memory_view",
        "View a memory file or list a directory under /memories/. "
        "Paths must stay inside the fleet-memory mount; escapes raise an error.",
        {"path": str},
    )(handlers["memory_view"])

    create_tool = tool(
        "memory_create",
        "Create or overwrite a memory file. Writes are restricted to "
        f"/memories/{agent_id}/** and /memories/shared/**.",
        {"path": str, "file_text": str},
    )(handlers["memory_create"])

    str_replace_tool = tool(
        "memory_str_replace",
        "Replace a unique substring in a memory file. Fails if `old_str` "
        "is missing or appears more than once.",
        {"path": str, "old_str": str, "new_str": str},
    )(handlers["memory_str_replace"])

    insert_tool = tool(
        "memory_insert",
        "Insert text at a 0-indexed line number in a memory file.",
        {"path": str, "insert_line": int, "insert_text": str},
    )(handlers["memory_insert"])

    delete_tool = tool(
        "memory_delete",
        "Delete a memory file. Only files inside the agent's namespace "
        "or /memories/shared/ can be deleted.",
        {"path": str},
    )(handlers["memory_delete"])

    rename_tool = tool(
        "memory_rename",
        "Rename or move a memory file. Both source and destination must "
        "be inside the agent's namespace or /memories/shared/.",
        {"old_path": str, "new_path": str},
    )(handlers["memory_rename"])

    return create_sdk_mcp_server(
        name="fleet-memory",
        version="1.0.0",
        tools=[
            view_tool, create_tool, str_replace_tool,
            insert_tool, delete_tool, rename_tool,
        ],
    )
```

**Note on the `tool(...)(handler)` pattern:** the `@tool(...)` decorator is normally applied at definition time on a module-level async function. Here we need *parameterized* tool definitions (the description embeds `agent_id`) and we want the handlers built inside `_build_memory_handlers` so unit tests can call them directly. Applying the decorator as a function call — `tool(name, desc, schema)(handler)` — gives us the same wrapped tool object without forcing module-level definitions. If the SDK's `@tool` decorator is not in fact callable this way, fall back to defining six module-level decorated async functions and replicating the dispatch logic inline; the test suite will catch the mismatch.

- [ ] **Step 4: Run the MCP-server test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory_mcp.py -v
```
Expected: PASS.

- [ ] **Step 4: Run the MCP-server tests to verify they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_fleet_memory_mcp.py -v
```
Expected: All four PASS.

- [ ] **Step 5: Write failing test for `daily_driver.build_options`**

Add to `agents-sdk/tests/test_daily_driver_artifacts.py` (or create a new `test_daily_driver_fleet_memory.py`):

```python
class TestDailyDriverFleetMemoryWiring:
    # The six MCP tool names the daily_driver must declare in allowed_tools
    # when fleet-memory is enabled. Pre-computed here so test assertions and
    # the implementation stay in lockstep.
    EXPECTED_TOOL_NAMES = {
        "mcp__fleet-memory__memory_view",
        "mcp__fleet-memory__memory_create",
        "mcp__fleet-memory__memory_str_replace",
        "mcp__fleet-memory__memory_insert",
        "mcp__fleet-memory__memory_delete",
        "mcp__fleet-memory__memory_rename",
    }

    def test_build_options_includes_fleet_memory_mcp_when_enabled(self, monkeypatch, tmp_path):
        from lib.config import load_config
        cfg = load_config()
        cfg.raw.setdefault("fleet_memory", {})["enabled"] = True
        cfg.raw["fleet_memory"].setdefault("per_agent", {}).setdefault(
            "daily_driver", {}
        )["enabled"] = True

        from agents.daily_driver import build_options
        opts = build_options(cfg, mode="morning")
        assert "fleet-memory" in opts.mcp_servers
        assert self.EXPECTED_TOOL_NAMES.issubset(set(opts.allowed_tools))
        assert "context-management-2025-06-27" in opts.betas

    def test_build_options_omits_fleet_memory_when_disabled(self, monkeypatch):
        from lib.config import load_config
        from agents.daily_driver import build_options
        cfg = load_config()
        # Default: fleet_memory.enabled=false in config.toml
        opts = build_options(cfg, mode="morning")
        assert "fleet-memory" not in opts.mcp_servers
        # None of the six memory tool names should appear when disabled.
        assert not any("fleet-memory" in t for t in opts.allowed_tools)
```

- [ ] **Step 6: Run the test to verify it fails**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py::TestDailyDriverFleetMemoryWiring -v
```
Expected: FAIL — `build_options` doesn't know about fleet-memory yet.

- [ ] **Step 7: Wire `build_options` and `build_preamble`**

In `agents-sdk/agents/daily_driver.py`, modify `build_options(config, mode)`:

After the existing `vault_server = create_vault_mcp_server()` line, add:

```python
    fm_cfg = config.raw.get("fleet_memory", {})
    fm_agent_cfg = fm_cfg.get("per_agent", {}).get("daily_driver", {})
    fm_enabled = bool(fm_cfg.get("enabled") and fm_agent_cfg.get("enabled"))
    mcp_servers = {"vault-tools": vault_server}
    allowed_tools = [
        "Read", "Write", "Edit", "Glob", "Grep",
        "mcp__vault-tools__vault_inject",
    ]
    betas = []
    if fm_enabled:
        from lib.custom_tools import create_fleet_memory_mcp_server
        fm_mount = config.vault_root / fm_cfg.get(
            "mount_subpath", "90_system/fleet-memory"
        )
        mcp_servers["fleet-memory"] = create_fleet_memory_mcp_server(
            agent_id="daily_driver", mount_root=fm_mount,
        )
        allowed_tools.extend([
            "mcp__fleet-memory__memory_view",
            "mcp__fleet-memory__memory_create",
            "mcp__fleet-memory__memory_str_replace",
            "mcp__fleet-memory__memory_insert",
            "mcp__fleet-memory__memory_delete",
            "mcp__fleet-memory__memory_rename",
        ])
        betas.append(fm_cfg.get("beta_header", "context-management-2025-06-27"))
```

Then replace the `return ClaudeAgentOptions(...)` block to use these locals:

```python
    return ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": skills_prompt,
        },
        allowed_tools=allowed_tools,
        permission_mode=config.safety.permission_mode,
        max_turns=max_turns,
        max_budget_usd=max_budget,
        cwd=str(config.repo_root),
        mcp_servers=mcp_servers,
        betas=betas,
        setting_sources=["project"],
        env=env,
    )
```

And in `build_preamble(mode, config)` (the function that builds the user-facing prompt), append a fleet-memory cue when enabled:

```python
    fm_cfg = config.raw.get("fleet_memory", {})
    if fm_cfg.get("enabled") and fm_cfg.get("per_agent", {}).get(
        "daily_driver", {}
    ).get("enabled"):
        preamble += (
            "\n\n## Fleet Memory\n\n"
            "You have six memory tools (mcp__fleet-memory__memory_{view,create,\n"
            "str_replace,insert,delete,rename}) implementing the Anthropic\n"
            "memory_20250818 protocol against a shared fleet-memory mount.\n"
            "Start every run by calling `memory_view` on `/memories/shared/`\n"
            "and `/memories/daily_driver/` to surface relevant prior lessons.\n"
            "Record new lessons via `memory_create` against\n"
            "`/memories/daily_driver/{slug}.md`. Use `/memories/shared/{slug}.md`\n"
            "ONLY when the lesson generalizes to multiple agents.\n"
        )
```

- [ ] **Step 8: Run the daily-driver wiring test to verify it passes**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py::TestDailyDriverFleetMemoryWiring -v
```
Expected: PASS.

- [ ] **Step 9: Run all daily-driver tests to catch regressions**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/test_daily_driver_artifacts.py tests/test_daily_driver_job_feed.py tests/test_daily_driver_vault_health.py -v
```
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add agents-sdk/lib/custom_tools.py agents-sdk/agents/daily_driver.py agents-sdk/tests/test_fleet_memory_mcp.py agents-sdk/tests/test_daily_driver_artifacts.py
git commit -m "feat(fleet-memory): wire daily_driver via MCP-server bridge (Phase 1 step 8/9)"
```

---

## Task 10: Update `CLAUDE.md` Architecture-decisions table

**Files:**
- Modify: `CLAUDE.md` (the project root one — not a domain CLAUDE.md)

- [ ] **Step 1: Add a new row to the "Architecture decisions" table**

Find the `## Architecture decisions (current capabilities — full history in CHANGELOG.md)` section in `CLAUDE.md`. Add this row immediately before the closing `**launchd requirement:**` block, after the existing "Knowledge Lint scope" row:

```markdown
| Fleet memory (Phase 1) | Shared filesystem-memory layer at `vault/90_system/fleet-memory/`. `BetaAbstractMemoryTool` subclass with realpath-prefix-checked path guard, per-agent namespacing, explicit promote_to_shared(). Pilot agents: `vault_synthesizer` (read-and-inject) + `daily_driver` (MCP-server bridge). Default-disabled; opt in via `[fleet_memory.per_agent.{agent_id}].enabled=true`. | [`agents-sdk/lib/fleet_memory.py`](agents-sdk/lib/fleet_memory.py); plan [`agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md`](agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md) |
```

- [ ] **Step 2: Verify the table still renders cleanly**

```bash
grep -n "Fleet memory" /Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md
```
Expected: One match showing the new row.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude-md): document fleet-memory Phase 1 in arch-decisions table"
```

---

## Task 11: Extend `evals/vault-synthesizer/` with fleet-memory cases

**Files:**
- Modify: `evals/vault-synthesizer/cases.yaml`
- Modify: `evals/vault-synthesizer/runner.py` (add memory-preamble fixture path)
- Modify: `evals/vault-synthesizer/README.md` (bump baseline counts)
- Create: `evals/vault-synthesizer/traces/fixtures/memory-preamble.md` (small synthetic preamble)

The existing 8 cases (vs-014…vs-021) test pre-memory behavior and are grounded in 17 days of production logs. Fleet-memory introduces 4 new behaviors to cover at the eval layer (separate from unit tests in `agents-sdk/tests/`). These cases live alongside the existing ones and use the same runner pattern.

- [ ] **Step 1: Add 4 cases to `cases.yaml`**

Append to `evals/vault-synthesizer/cases.yaml`:

```yaml
- id: vs-022
  category: fleet-memory
  description: "memory_preamble parameter prepends to per-file LLM prompt when non-empty"
  failure_mode_under_test: "Phase 1 fleet-memory — preamble must reach the LLM, not be silently dropped"
  input:
    fixtures: traces/fixtures
    note_count: 1
    memory_preamble_path: traces/fixtures/memory-preamble.md
  expected_output:
    preamble_first_in_prompt: true
  judge_type: rubric
  pass_criteria: "result.captured_prompts and result.captured_prompts[0].startswith('# Lessons remembered')"

- id: vs-023
  category: fleet-memory
  description: "_maybe_write_run_lesson writes a lesson on STATUS_OK with concepts_written>0"
  failure_mode_under_test: "Phase 1 fleet-memory — clean run must persist a lesson for future recall"
  input:
    simulated_result:
      status: ok
      concepts_written: 2
      connections_written: 1
      model_used: qwen3.6_35b-a3b-32k
      run_id: "2026-06-15T03:00:00"
  expected_output:
    lesson_file_exists: true
    manifest_updated: true
  judge_type: rubric
  pass_criteria: "result.lesson_files_count == 1 and 'qwen3.6_35b-a3b-32k' in result.lesson_body"

- id: vs-024
  category: fleet-memory
  description: "_maybe_write_run_lesson is a no-op on STATUS_ERROR"
  failure_mode_under_test: "Phase 1 fleet-memory — error runs must not pollute memory with false signal"
  input:
    simulated_result:
      status: error
      concepts_written: 0
  expected_output:
    lesson_files_count: 0
  judge_type: exact-match
  pass_criteria: "result.lesson_files_count == 0"

- id: vs-025
  category: fleet-memory
  description: "_maybe_write_run_lesson is a no-op when fleet_memory.enabled=false even on a clean run"
  failure_mode_under_test: "Phase 1 fleet-memory — opt-in toggle must gate all write paths"
  input:
    simulated_result:
      status: ok
      concepts_written: 5
    fleet_memory_enabled: false
  expected_output:
    lesson_files_count: 0
  judge_type: exact-match
  pass_criteria: "result.lesson_files_count == 0"
```

- [ ] **Step 2: Create the fixture preamble**

Create `evals/vault-synthesizer/traces/fixtures/memory-preamble.md`:

```markdown
# Lessons remembered from prior runs

## Manifest

- pr52-stale-checkout: Filter critic candidates to synth manifest, not mtime.

## Your namespace (vault_synthesizer/)

### pr52-stale-checkout.md
PR #52 wrote pre-Tier-2 articles. Always filter to manifest.
```

- [ ] **Step 3: Extend `runner.py` to handle the new cases**

Add a helper function near `_invoke_synthesizer` in `evals/vault-synthesizer/runner.py`:

```python
def _invoke_synthesizer_with_capture(case) -> object:
    """vs-022: capture what llm_caller actually receives so we can assert
    on prompt shape (memory preamble must be the first content)."""
    from agents import vault_synthesizer as vs
    import tempfile

    inp = case.get("input", {})
    captured: list[str] = []

    def llm_caller(prompt: str, max_tokens: int = 2000) -> dict:
        captured.append(prompt)
        return {"concepts": [], "connections": []}

    def retriever(text, top_k, **kw):
        return []

    preamble_path = ROOT / inp["memory_preamble_path"]
    memory_preamble = preamble_path.read_text(encoding="utf-8")

    fixtures_dir = ROOT / (inp.get("fixtures") or "traces/fixtures")
    note_count = inp.get("note_count", 1)
    tmpdir = tempfile.mkdtemp(prefix="eval-synth-mem-")
    vault_root = Path(tmpdir)
    changed: list[Path] = []
    for src in sorted(fixtures_dir.glob("note-*.md"))[:note_count]:
        import shutil
        dst = vault_root / src.name
        shutil.copy(src, dst)
        changed.append(dst)

    import os
    os.environ.setdefault("PUSHOVER_USER_KEY", "eval-stub-user")
    os.environ.setdefault("PUSHOVER_API_TOKEN", "eval-stub-token")

    vs.run_synthesis(
        vault_root=vault_root,
        changed_files=changed,
        llm_caller=llm_caller,
        retriever=retriever,
        budget_seconds=30,
        db_conn=None,
        memory_preamble=memory_preamble,
    )

    class _Wrap:
        pass
    w = _Wrap()
    w.captured_prompts = captured
    return w


def _invoke_lesson_writer(case) -> object:
    """vs-023/024/025: simulate a SynthesisResult and assert lesson-write
    behavior. Avoids running the full synth pipeline."""
    from agents.vault_synthesizer import _maybe_write_run_lesson, SynthesisResult
    from lib import fleet_memory
    import tempfile

    inp = case.get("input", {})
    sim = inp["simulated_result"]
    enabled = inp.get("fleet_memory_enabled", True)
    tmpdir = tempfile.mkdtemp(prefix="eval-synth-lesson-")
    mount = Path(tmpdir) / "fleet-memory"
    fleet_memory.ensure_mount(mount, agent_ids=["vault_synthesizer"])

    result = SynthesisResult(status=sim["status"])
    result.concepts_written = sim.get("concepts_written", 0)
    result.connections_written = sim.get("connections_written", 0)
    result.model_used = sim.get("model_used", "none")
    result.run_id = sim.get("run_id", "eval-run")

    _maybe_write_run_lesson(mount_root=mount, result=result, enabled=enabled)

    lesson_files = list((mount / "vault_synthesizer").glob("*.md"))
    lesson_body = lesson_files[0].read_text() if lesson_files else ""

    class _Wrap:
        pass
    w = _Wrap()
    w.lesson_files_count = len(lesson_files)
    w.lesson_body = lesson_body
    return w
```

Then in the `test_case` function, add dispatch branches for the new IDs (insert before the existing `elif case["id"] == "vs-019":` block):

```python
    elif case["id"] == "vs-022":
        result = _invoke_synthesizer_with_capture(case)

    elif case["id"] in ("vs-023", "vs-024", "vs-025"):
        result = _invoke_lesson_writer(case)
```

- [ ] **Step 4: Update README baseline counts**

In `evals/vault-synthesizer/README.md`, change the case count language. Find this line:

```markdown
**Post-fix (Workstream B complete, 2026-05-12): 7/10 (70%).**
```

Add a new paragraph after it:

```markdown
**Phase 1 fleet-memory addendum (2026-05-27): 4 cases added (vs-022 to vs-025) covering memory-preamble injection and lesson-write gating. Pass-rate target after Task 11 ships: 11/14 = 79% (the three skipped cases vs-012/013/014 remain deferred).**
```

- [ ] **Step 5: Run the new eval cases to confirm they pass**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/vault-synthesizer/runner.py -v -k "vs-022 or vs-023 or vs-024 or vs-025"
```
Expected: All four PASS.

- [ ] **Step 6: Run the full eval suite to confirm no regressions**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/vault-synthesizer/runner.py -v
```
Expected: 11 PASS, 3 SKIP (the existing vs-012/013/014 deferrals).

- [ ] **Step 7: Commit**

```bash
git add evals/vault-synthesizer/cases.yaml evals/vault-synthesizer/runner.py evals/vault-synthesizer/README.md evals/vault-synthesizer/traces/fixtures/memory-preamble.md
git commit -m "feat(evals): add 4 fleet-memory cases to vault-synthesizer eval suite"
```

---

## Task 12: Scaffold `evals/daily-driver/` from scratch

**Files:**
- Create: `evals/daily-driver/README.md`
- Create: `evals/daily-driver/cases.yaml`
- Create: `evals/daily-driver/runner.py`
- Create: `evals/daily-driver/conftest.py`
- Create: `evals/daily-driver/deferred-cases.yaml`
- Create: `evals/daily-driver/failure-modes.md`
- Create: `evals/daily-driver/last-run.md` (placeholder; regenerated on each pytest run)
- Create: `evals/daily-driver/traces/.gitkeep`

This mirrors the [vault-synthesizer eval suite](evals/vault-synthesizer/) structure. Phase 1 ships **2 cases** focused on the fleet-memory wiring (the highest-confidence new behavior); additional cases get added in Phase 2 once production traces accumulate to ground production-grade failure modes. The deferred-cases.yaml file holds 4 named-but-not-yet-runnable cases as forward markers.

- [ ] **Step 1: Create the directory and `.gitkeep` files**

```bash
mkdir -p evals/daily-driver/traces/fixtures
touch evals/daily-driver/traces/.gitkeep
```

- [ ] **Step 2: Create `evals/daily-driver/conftest.py`**

Mirrors the synth conftest pattern verbatim, with the path-prepend logic plus the `last-run.md` writer:

```python
"""Make agents-sdk importable from the eval runner regardless of pytest's CWD.

Same pattern as evals/vault-synthesizer/conftest.py — see that file for the
full rationale. Pytest auto-registers hooks from conftest.py but NOT from a
parametrized test module like runner.py, which is why the last-run.md
writer lives here.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_AGENTS_SDK = _REPO_ROOT / "agents-sdk"
if _AGENTS_SDK.exists() and str(_AGENTS_SDK) not in sys.path:
    sys.path.insert(0, str(_AGENTS_SDK))


_RESULTS: list[tuple[str, str, str]] = []


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    case_id = report.nodeid.split("[", 1)[-1].rstrip("]")
    if report.passed:
        _RESULTS.append((case_id, "✅ PASS", ""))
    elif report.skipped:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "⏸️ SKIPPED", notes))
    else:
        notes = str(report.longrepr).splitlines()[-1] if report.longrepr else ""
        _RESULTS.append((case_id, "❌ FAIL", notes))


def pytest_sessionfinish(session, exitstatus):
    if not _RESULTS:
        return
    from runner import _load_cases, _write_last_run
    cases_by_id = {c["id"]: c for c in _load_cases()}
    lines = []
    for case_id, status, notes in _RESULTS:
        cat = cases_by_id.get(case_id, {}).get("category", "?")
        lines.append(f"| {case_id} | {cat} | {status} | {notes} |")
    pass_count = sum(1 for _, s, _ in _RESULTS if "PASS" in s)
    total = len(_RESULTS)
    lines.append("")
    lines.append(f"**Pass rate: {pass_count}/{total} ({100*pass_count//total}%).**")
    _write_last_run(lines)
```

- [ ] **Step 3: Create `evals/daily-driver/cases.yaml`** with two Phase-1 cases:

```yaml
# evals/daily-driver/cases.yaml
# Schema mirrors evals/vault-synthesizer/cases.yaml.
# Phase 1 ships 2 cases covering the fleet-memory wiring. Additional cases land
# in Phase 2 once production traces accumulate to ground non-fleet-memory
# failure modes (see deferred-cases.yaml for the forward markers).

- id: dd-001
  category: fleet-memory-wiring
  description: "build_options registers the 6 fleet-memory MCP tool names in allowed_tools when enabled"
  failure_mode_under_test: "Phase 1 fleet-memory — daily_driver must declare all six memory tools so the CLI permission layer routes them"
  input:
    fleet_memory_enabled: true
  expected_output:
    expected_tool_names:
      - mcp__fleet-memory__memory_view
      - mcp__fleet-memory__memory_create
      - mcp__fleet-memory__memory_str_replace
      - mcp__fleet-memory__memory_insert
      - mcp__fleet-memory__memory_delete
      - mcp__fleet-memory__memory_rename
    expected_beta: context-management-2025-06-27
  judge_type: rubric
  pass_criteria: "set(result.expected_tool_names).issubset(set(result.allowed_tools)) and 'context-management-2025-06-27' in result.betas"

- id: dd-002
  category: fleet-memory-wiring
  description: "build_options omits fleet-memory MCP server when fleet_memory.enabled=false"
  failure_mode_under_test: "Phase 1 fleet-memory — opt-in toggle must gate the entire MCP-server wiring, not just write paths"
  input:
    fleet_memory_enabled: false
  expected_output:
    fleet_memory_server_absent: true
    no_fleet_memory_tools: true
  judge_type: exact-match
  pass_criteria: "'fleet-memory' not in result.mcp_server_names and not any('fleet-memory' in t for t in result.allowed_tools)"
```

- [ ] **Step 4: Create `evals/daily-driver/runner.py`**

```python
# evals/daily-driver/runner.py
"""Daily Driver Eval Runner.

Run with:
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \\
        ../evals/daily-driver/runner.py -v

Phase 1 scope: 2 cases covering the fleet-memory MCP-server wiring.
Phase 2 scope (see deferred-cases.yaml): morning-brief shape, vault-health
WARNING propagation, MBP-asleep fallback path, fleet-overnight digest
injection. Those need production traces to author cases against.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent
CASES_PATH = ROOT / "cases.yaml"
LAST_RUN_PATH = ROOT / "last-run.md"


def grade_exact_match(result, case) -> tuple[str, str]:
    expr = case["pass_criteria"]
    try:
        ok = bool(eval(expr, {"__builtins__": {}}, {"result": result}))
    except Exception as e:
        return "FAIL", f"grader-eval-error: {e!r}"
    return ("PASS", "") if ok else ("FAIL", f"{expr} evaluated False")


def grade_rubric(result, case) -> tuple[str, str]:
    return grade_exact_match(result, case)


GRADERS = {"exact-match": grade_exact_match, "rubric": grade_rubric}


def _load_cases() -> list[dict]:
    return yaml.safe_load(CASES_PATH.read_text())


def _write_last_run(lines: list[str]) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    header = (
        f"# Daily Driver Eval — last-run\n\n"
        f"_Auto-generated by runner.py at {ts}._\n\n"
        f"| Case | Category | Result | Notes |\n"
        f"|------|----------|--------|-------|\n"
    )
    LAST_RUN_PATH.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")


def _invoke_build_options(case) -> object:
    """Both Phase-1 cases (dd-001, dd-002) inspect `build_options` output —
    no full agent run, no network, no LLM. Just config + the SDK options
    builder.
    """
    from lib.config import load_config
    from agents.daily_driver import build_options

    inp = case.get("input", {})
    cfg = load_config()
    cfg.raw.setdefault("fleet_memory", {})["enabled"] = inp.get(
        "fleet_memory_enabled", False
    )
    cfg.raw["fleet_memory"].setdefault("per_agent", {}).setdefault(
        "daily_driver", {}
    )["enabled"] = inp.get("fleet_memory_enabled", False)

    opts = build_options(cfg, mode="morning")

    class _Wrap:
        pass
    w = _Wrap()
    w.allowed_tools = list(opts.allowed_tools)
    w.betas = list(opts.betas) if opts.betas else []
    w.mcp_server_names = list(opts.mcp_servers.keys())
    # Surface the expected-tool list from the case so pass_criteria can read it
    w.expected_tool_names = inp.get("expected_tool_names", []) or case.get(
        "expected_output", {}
    ).get("expected_tool_names", [])
    return w


@pytest.fixture(scope="session")
def cases():
    return _load_cases()


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_case(case):
    if case.get("skip_reason"):
        pytest.skip(case["skip_reason"])

    if case["id"] in ("dd-001", "dd-002"):
        result = _invoke_build_options(case)
    else:
        pytest.fail(f"runner.py has no dispatch for case id {case['id']!r}")
        return

    grader = GRADERS[case["judge_type"]]
    status, msg = grader(result, case)
    assert status == "PASS", msg


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
```

- [ ] **Step 5: Create `evals/daily-driver/deferred-cases.yaml`**

```yaml
# evals/daily-driver/deferred-cases.yaml
# Cases named but not yet runnable. Move into cases.yaml when traces exist.

- id: dd-003
  category: morning-brief-shape
  description: "Morning brief must contain a `## Morning Focus` section with 1-3-5 priority list shape"
  status: deferred
  blocker: "Need 7+ days of production morning-brief traces to ground the assertion against actual output shape"

- id: dd-004
  category: vault-health-propagation
  description: "When synth-manifest reports status=success-empty, the daily brief Vault Health block must contain WARNING and `concepts_written: 0`"
  status: deferred
  blocker: "vs-021 covers the render_vault_health function unit-side; dd-004 will cover the integration through build_prompt → query loop. Needs a way to run claude-agent-sdk.query() in offline eval mode."

- id: dd-005
  category: mbp-asleep-fallback
  description: "When fleet-overnight digest indicates MBP was asleep, the morning brief surfaces the fallback path (cloud Sonnet) rather than silently degrading"
  status: deferred
  blocker: "Need MBP-asleep production traces to ground the assertion; the fallback path text shape is not stable yet."

- id: dd-006
  category: fleet-memory-content
  description: "When fleet-memory contains a lesson tagged `daily_driver/{slug}.md` from a prior run, the agent's morning brief references the lesson by file path"
  status: deferred
  blocker: "Need ≥7 days of Phase 1 fleet-memory production runs to know what the model actually does with retrieved memory entries. Author after Phase 1 audit."
```

- [ ] **Step 6: Create `evals/daily-driver/failure-modes.md`**

```markdown
# Daily Driver — Failure Mode Taxonomy

Phase 1 ships with the fleet-memory-wiring slice only. Production-grounded
failure modes are authored as traces accumulate. This file mirrors the
shape of [`evals/vault-synthesizer/failure-modes.md`](../vault-synthesizer/failure-modes.md);
fill in modes 1–N below as you observe them in real morning runs.

## Mode 1 — Fleet-memory wiring drift (Phase 1)
**Observed:** N/A — guarded preemptively by dd-001, dd-002.
**Symptom:** `build_options` ships without the six MCP tools, or with the
wrong beta header. Model can't call memory tools; reads fail silently;
no lessons accumulate.
**Cases:** dd-001, dd-002.

## Mode 2+ — TBD (Phase 2)
Author production-grounded modes after Phase 1 produces ≥1 week of traces.
Suggested probes:
- Morning brief skips the 1-3-5 section when synth-manifest is malformed
- Fleet-overnight digest injected at wrong anchor (anchor drift)
- MBP-asleep state misreported in the digest
- Daily-note duplicate created when an earlier 08:45 run partial-completed
```

- [ ] **Step 7: Create `evals/daily-driver/README.md`**

```markdown
# Daily Driver — Eval Suite

A binary pass/fail eval suite for the autonomous morning daily-driver agent.
Mirrors the [`evals/vault-synthesizer/`](../vault-synthesizer/) structure.

> **Phase 1 scope: fleet-memory wiring only.** Two cases (dd-001, dd-002)
> verify that the daily_driver builds correct SDK options when fleet-memory
> is enabled vs. disabled. Production-grounded morning-brief failure modes
> land in Phase 2 once traces accumulate.

## Quickstart

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/daily-driver/runner.py -v
```

(Running from any other CWD breaks the `agents` import — the `cd agents-sdk`
prefix is mandatory, same as the synth eval.)

## Current baseline

**Phase 1 ship (2026-05-27 plan): 2/2 (100%).** Both cases assert wiring
shape and pass against the implementation built in Tasks 9 and 10. Cases
are pre-emptive (guarding the wiring against drift), not regression-driven
— there's no production failure to point to yet.

## Forward roadmap

[`deferred-cases.yaml`](deferred-cases.yaml) lists 4 named-but-not-runnable
cases (dd-003 through dd-006) for Phase 2:

- **dd-003** Morning-brief shape (`## Morning Focus`, 1-3-5 structure)
- **dd-004** Vault Health propagation (success-empty → WARNING)
- **dd-005** MBP-asleep fallback signaling
- **dd-006** Fleet-memory retrieval — does the model actually reference
  stored lessons in its brief?

Each blocked on accumulating traces, not on test infrastructure.

## Sources

- Eval pattern lifted from [`evals/vault-synthesizer/`](../vault-synthesizer/)
- Underlying agent: [`agents-sdk/agents/daily_driver.py`](../../agents-sdk/agents/daily_driver.py)
- Fleet-memory plan: [`agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md`](../../agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md)
```

- [ ] **Step 8: Create `evals/daily-driver/last-run.md` placeholder**

```markdown
# Daily Driver Eval — last-run

_Will be auto-generated on the first `pytest` run by `conftest.py:pytest_sessionfinish`._
```

- [ ] **Step 9: Run the new eval suite**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
    ../evals/daily-driver/runner.py -v
```
Expected: dd-001 PASS, dd-002 PASS.

- [ ] **Step 10: Confirm `last-run.md` regenerated**

```bash
cat /Users/seanwinslow/Code-Brain/code-brain/evals/daily-driver/last-run.md
```
Expected: a table with `dd-001 | fleet-memory-wiring | ✅ PASS` and `dd-002 | fleet-memory-wiring | ✅ PASS`.

- [ ] **Step 11: Commit**

```bash
git add evals/daily-driver/
git commit -m "feat(evals): scaffold daily-driver eval suite (Phase 1: 2 cases, 4 deferred)"
```

---

## Smoke Test Protocol (post-Task 12)

Run these manually after all tasks pass. This is the "does it actually work end-to-end" gate the user requested. The unit-test layer (Tasks 2–9) and the eval layer (Tasks 11–12) both pass at this point; the smoke tests confirm real production agents wire correctly against a real vault.

### Smoke 1 — vault_synthesizer round-trip

- [ ] **Step 1: Enable for one run only**

Edit `agents-sdk/config.toml`:
```toml
[fleet_memory]
enabled = true
...

[fleet_memory.per_agent.vault_synthesizer]
enabled = true
```

- [ ] **Step 2: Run the synthesizer dry to verify it loads memory**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/vault_synthesizer.py --dry-run
```
Expected: Exit 0. The mount `vault/90_system/fleet-memory/` exists with `MEMORY_INDEX.md`, `vault_synthesizer/`, `daily_driver/`, `shared/`.

- [ ] **Step 3: Run synthesis live and confirm lesson is written**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/vault_synthesizer.py
```
Expected on success:
- `vault/90_system/fleet-memory/vault_synthesizer/run-2026-05-27T*.md` exists with a body containing `model_used`, `concepts_written`, etc.
- `vault/90_system/fleet-memory/MEMORY_INDEX.md` has a `## vault_synthesizer` section with one `- run-2026-05-27...: Nc/Mx via {model}` line.

If `result.status` is not `ok` or `concepts_written == 0`, no lesson is written — that's the documented behaviour, not a failure.

- [ ] **Step 4: Re-run to confirm the prompt now contains the prior lesson**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -c "
from lib.config import load_config
from lib import fleet_memory
cfg = load_config()
mount = cfg.vault_root / cfg.raw['fleet_memory']['mount_subpath']
print(fleet_memory.inject_memories_into_prompt(
    mount_root=mount, agent_id='vault_synthesizer', enabled=True
))
"
```
Expected: Output contains the manifest section + the run lesson body from Step 3.

- [ ] **Step 5: Revert config toggle**

```bash
git checkout agents-sdk/config.toml
```
Restores the default `enabled=false`. Phase 1 stays opt-in.

### Smoke 2 — daily_driver round-trip

- [ ] **Step 1: Enable for one run only**

Edit `agents-sdk/config.toml`:
```toml
[fleet_memory]
enabled = true

[fleet_memory.per_agent.daily_driver]
enabled = true
```

- [ ] **Step 2: Dry run shows the MCP server is wired**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run
```
Expected: Stdout shows `Allowed tools: [..., 'mcp__fleet-memory__memory_view', 'mcp__fleet-memory__memory_create', 'mcp__fleet-memory__memory_str_replace', 'mcp__fleet-memory__memory_insert', 'mcp__fleet-memory__memory_delete', 'mcp__fleet-memory__memory_rename']` and the preamble contains `## Fleet Memory`.

- [ ] **Step 3: Live morning run, hand-prompt a lesson save**

```bash
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning
```
Expected: The agent calls `view` on `/memories/shared/` and `/memories/daily_driver/` at least once (visible in the SDK's tool-use log under `vault/90_system/agent-logs/daily-driver-*.log`). It does not need to write a lesson on this first run — the agent learns when there's something worth remembering.

To force a write for the smoke test, manually use the agent with a prompt like "Remember that the MBP is asleep on weekends — fall back to the cloud path." On the next dry-run pass, `vault/90_system/fleet-memory/daily_driver/*.md` should exist with that lesson.

- [ ] **Step 4: Verify the auto-commit picks up the new files**

```bash
# Wait at minimum one auto-commit cycle (the external process commits hourly),
# then:
git log --since="2 hours ago" --name-only --pretty=format: -- vault/90_system/fleet-memory/ | sort -u
```
Expected: One or more files under `vault/90_system/fleet-memory/` appear in the auto-commit log. If empty, surface as an open issue — the auto-commit process may need its path scope extended.

- [ ] **Step 5: Revert config toggle**

```bash
git checkout agents-sdk/config.toml
```

---

## Rollback Plan

If Phase 1 reveals a fatal issue — path-traversal escape, namespace bleed, prompt-budget blowup, or any unanticipated interaction with the existing knowledge-loop — the rollback is deliberately cheap:

1. **Instant rollback (config flag):** Set `[fleet_memory] enabled = false` in `agents-sdk/config.toml`. All `_maybe_write_run_lesson` and `inject_memories_into_prompt` calls become no-ops. `daily_driver.build_options` returns to its pre-Phase-1 shape (no fleet-memory MCP, no beta header). Verified in Task 9 step 2 test.

2. **Code-level rollback (one revert):** `git revert <task-1-commit>..<task-10-commit>` reverts all changes. The mount directory `vault/90_system/fleet-memory/` may still contain bootstrap files — these are inert markdown and can be deleted manually or left in place. The auto-commit hook will commit the deletions on its next cycle.

3. **Selective rollback (per-agent):** Set `[fleet_memory.per_agent.{agent_id}].enabled = false` for just the failing agent. The other pilot stays live.

The synthesis explicitly names the three-store baseline (Anthropic auto-memory + Obsidian RAG + CLAUDE.md files) as "rational scaffolding" — rolling back to it is a valid outcome and does not invalidate the Phase 1 experiment.

---

## Phase 2 — Out of Scope (named for traceability)

These are deliberately deferred. List them in the rollout-decision doc when Phase 2 starts; do not start them as part of this plan:

- **Fleet rollout to the remaining 25 agents.** Trigger: 30 days of Phase 1 with zero security or namespace incidents and ≥10 lessons written across both pilots.
- **CLAUDE.md feedback migration.** Move "do not do X" sections from `the-block/CLAUDE.md`, `creative-studio/CLAUDE.md`, `life-systems/CLAUDE.md` into `fleet-memory/shared/feedback/`. Trigger: Phase 2 rollout.
- **`~/.claude/projects/.../memory/` audit + consolidate-or-deprecate.** Trigger: 30-day parallel-run window ends.
- **MCP-server bridge for non-daily-driver cloud agents** (`flush`, `meta_agent` when those make cloud calls). Same factory in `lib/custom_tools.py` — just call it from those agents' `build_options`.

## Phase 3 — Out of Scope (trigger logic, not designed)

From the synthesis §Phase 3 — re-evaluate later when one or more of:
- Fleet crosses 50 agents.
- mem0 issue #4956 (ADD-only extraction) closes with an independently verified fix.
- Cross-entity relational queries become first-class needs.
- Anthropic memory tool's lack of dedup becomes a maintenance burden (target: 200+ memory files where retrieval starts degrading even with manifest-first).

When a trigger fires, run a fresh deep-research synthesis (Topic 27 re-run) rather than designing Phase 3 now — the landscape moves fast.

---

## Open Questions (BLOCK implementation start — Sean to answer)

Implementation must not start until these are resolved:

1. ~~**MCP-server bridge API shape.**~~ **RESOLVED 2026-05-27** — read `lib/custom_tools.py`, locked in actual SDK shape in Task 9: `tool(name, description, schema_dict)(handler)` parameterized-decorator pattern, six separate MCP tools (`memory_view` / `memory_create` / etc.), `{"content": [{"type": "text", "text": ...}], "is_error": ...}` envelope. No remaining ambiguity in Task 9; one residual edge case noted in the implementation (`tool(...)(handler)` call style) — if it doesn't work, fall back to six module-level decorated functions.

2. ~~**Anthropic SDK version drift.**~~ **RESOLVED 2026-05-27** — sync the venv to the `0.1.63` pin as a Task -1 prerequisite (see new task below). Full test suite must pass before Task 0 starts.

3. ~~**External auto-commit path coverage.**~~ **RESOLVED 2026-05-27** — Obsidian-Git is the active auto-commit source (user-confirmed). It commits the whole vault root, so `vault/90_system/fleet-memory/` is covered automatically. CLAUDE.md rule 8 updated 2026-05-27 to reflect this.

4. ~~**Memory-injection placement.**~~ **RESOLVED 2026-05-27** — Option 3: inject in the `run_synthesis` orchestrator. Prompt builder stays pure; LLM caller stays uncoupled from memory; orchestrator threads the run-wide preamble. Task 8 updated below.

5. ~~**First-run empty `shared/`.**~~ **RESOLVED 2026-05-27** — accept empty. The `MEMORY_INDEX.md` header (Task 3) and daily-driver's preamble (Task 9) document the system; no seed file. If smoke testing shows the model is confused by emptiness, add a seed in a 5-minute follow-up.

6. ~~**`vault_synthesizer` lesson cadence.**~~ **RESOLVED 2026-05-27** — per-run, no dedup. Phase 1 is a learning window; per-run gives the data to make a Phase 2 dedup decision. Read-side collapsing (via `inject_memories_into_prompt`) remains an option if the manifest gets noisy — it's reversible, write-time dedup isn't.

---

## Plan Self-Review

- **Spec coverage:**
  - Goal + non-goals → covered (top section + Non-Goals).
  - `fleet_memory.py` architecture sketch → Task 2 (guard), Task 3 (mount), Task 4 (class + view/create), Task 5 (remaining commands), Task 6 (manifest), Task 7 (promote + inject).
  - File-by-file change list → File Structure table.
  - Test plan matching existing pytest conventions → every task is a TDD pair (failing test → implementation → passing test); fixture in `conftest.py` mirrors `tmp_artifacts`.
  - Eval coverage matching `evals/` conventions → Task 11 extends vault-synthesizer with 4 cases (vs-022 to vs-025); Task 12 scaffolds daily-driver with 2 active + 4 deferred cases.
  - Smoke-test protocol → "Smoke Test Protocol" section, two end-to-end flows.
  - Rollback plan → "Rollback Plan" section, three escape hatches.
  - Open questions → six questions listed; all six resolved 2026-05-27. Implementation can start.
  - Phase 2 / 3 named but out-of-scope → "Phase 2 — Out of Scope" + "Phase 3 — Out of Scope" sections.
  - SDK version drift → Task -1 prerequisite.

- **Placeholder scan:** No "TBD", "implement later", "add appropriate error handling", or "similar to Task N" wording present in the implementation-bearing tasks. The eval deferred-cases.yaml uses `status: deferred` + `blocker:` fields per the existing synth convention — that's a known pattern, not a placeholder.

- **Type consistency:** Methods stay consistently named: `_resolve_path` (module function) vs `_resolve` (instance method) is intentional — the module function is the load-bearing guard; the instance method is a thin wrapper that strips the `/memories/` SDK prefix before delegating. `write_lesson` (Task 6) and `promote_to_shared` (Task 7) and `inject_memories_into_prompt` (Task 7) are stable across all task references. `FleetMemoryTool` is the only class name. Constructor signature `(mount_root, agent_id)` is consistent across Tasks 4, 6, 7, 8, 9. `run_synthesis` signature gains exactly one new param (`memory_preamble: str = ""`), consistent across Task 8 references and Task 11 eval cases.
