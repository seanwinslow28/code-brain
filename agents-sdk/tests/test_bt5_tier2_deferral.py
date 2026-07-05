"""BT5 Phase C — C1 (route-once per run + mid-run circuit breaker + typed
`wol-deferred` deferral) and C2 (notification honesty) for the Tier-2 (MBP)
reachability path.

Failing-test-first (verification-loops) for the fix spec at
docs/plans/wwf5d/fable-runs/bt5-fable.md. Each test names the Origin it fixes:

  Origin A — the reachability gap itself (fixed-instant schedule vs opportunistic host)
  Origin B — the synthesizer's dead deferral path (per-file `except Exception`
             swallowed WOLUnavailable → 45-min poll storm + status=error + page/file)

These assert the DESIRED post-fix behavior, so they are RED against the current
tree (no `host_probe` param, no circuit breaker, per-file routing, and
route_to_macbook notifies unconditionally).
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from agents.vault_synthesizer import run_synthesis
from lib.hybrid_router import (
    HybridRouter,
    MachineConfig,
    MachineStatus,
    WOLUnavailable,
)


# ─── shared fixtures ─────────────────────────────────────────────────────────

def _stub_pushover_creds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PUSHOVER_USER_KEY", "test-stub-user")
    monkeypatch.setenv("PUSHOVER_API_TOKEN", "test-stub-token")


def _make_vault(tmp_path: Path, files: dict[str, str]) -> Path:
    vault = tmp_path / "vault"
    for rel, content in files.items():
        p = vault / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return vault


def _retriever_two_chunks(query: str, top_k: int = 5) -> list[dict]:
    # ≥2 chunks (no embeddings) so Tier-1.5's thin-source skip never fires and
    # the cluster path falls back cleanly → the LLM call is always attempted.
    return [
        {"file_path": "a.md", "chunk_text": "chunk one body text here", "similarity": 0.9},
        {"file_path": "b.md", "chunk_text": "chunk two body text here", "similarity": 0.8},
    ]


def _mbp_router() -> HybridRouter:
    machines = {
        "macbook_pro": MachineConfig(
            name="macbook_pro", host="127.0.0.1", port=8080, tier=2,
            runtime="ollama", always_on=False, models=["qwen3.6_35b-a3b-32k"],
        ),
    }
    task_map = {"vault_synthesis": {"model": "qwen3.6_35b-a3b-32k", "machine": "macbook_pro"}}
    return HybridRouter(machines=machines, task_map=task_map)


# ─── C1: mid-run circuit breaker (Fixes Origin B — kills the poll storm) ──────

def test_circuit_breaker_stops_after_k_failures_when_host_down(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fixes Origin B: when the host drops mid-run, K=2 consecutive LLM
    failures + a failed re-probe must STOP the loop. The remaining files must
    NOT each re-attempt (today's 90s-poll-per-file storm over ~30 files)."""
    _stub_pushover_creds(monkeypatch)
    vault = _make_vault(tmp_path, {f"n{i}.md": f"# Note {i}\nbody {i}" for i in range(5)})
    changed = [vault / f"n{i}.md" for i in range(5)]

    calls = {"n": 0}

    def failing_llm(prompt: str, max_tokens: int = 2000) -> dict:
        calls["n"] += 1
        raise httpx.ConnectError("connection refused")

    result = run_synthesis(
        vault_root=vault,
        changed_files=changed,
        llm_caller=failing_llm,
        retriever=_retriever_two_chunks,
        now_iso="2026-07-05",
        budget_seconds=300,
        host_probe=lambda: False,  # re-probe confirms host is down
    )

    assert calls["n"] == 2, "breaker must stop the loop at K=2, not grind all 5 files"
    assert result.status in {"partial", "partial-empty"}
    assert any("host lost mid-run" in w for w in result.warnings)


def test_circuit_breaker_host_reachable_still_stops(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Edge (model-not-pulled → 404): the host probes healthy but every call
    fails. The breaker must still stop after K repeats rather than grind on."""
    _stub_pushover_creds(monkeypatch)
    vault = _make_vault(tmp_path, {f"n{i}.md": f"# Note {i}\nbody {i}" for i in range(5)})
    changed = [vault / f"n{i}.md" for i in range(5)]

    calls = {"n": 0}

    def failing_llm(prompt: str, max_tokens: int = 2000) -> dict:
        calls["n"] += 1
        raise RuntimeError("HTTP 404 model not found")

    result = run_synthesis(
        vault_root=vault,
        changed_files=changed,
        llm_caller=failing_llm,
        retriever=_retriever_two_chunks,
        now_iso="2026-07-05",
        budget_seconds=300,
        host_probe=lambda: True,  # host up, but calls keep failing
    )

    assert calls["n"] == 2
    assert any("host reachable" in w for w in result.warnings)


def test_breaker_inert_without_host_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Backward-compat: with no host_probe injected (pure unit path), the
    breaker is inert — every changed file is attempted, exactly as before."""
    _stub_pushover_creds(monkeypatch)
    vault = _make_vault(tmp_path, {f"n{i}.md": f"# Note {i}\nbody {i}" for i in range(4)})
    changed = [vault / f"n{i}.md" for i in range(4)]

    calls = {"n": 0}

    def failing_llm(prompt: str, max_tokens: int = 2000) -> dict:
        calls["n"] += 1
        raise httpx.ConnectError("x")

    run_synthesis(
        vault_root=vault,
        changed_files=changed,
        llm_caller=failing_llm,
        retriever=_retriever_two_chunks,
        now_iso="2026-07-05",
        budget_seconds=300,
    )
    assert calls["n"] == 4  # all files attempted; no breaker without a probe


# ─── C2: notification honesty (Fixes Origin B's page-storm + config bypass) ───

def test_route_to_macbook_silent_when_event_not_in_notify_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fixes Origin B / C2: notify_wol_failure must honor
    [notifications].notify_on. v3.14.3 removed `wol_failure` from notify_on, so
    an unreachable host is SILENT by default — the manifest + morning brief
    carry the signal, no page."""
    r = _mbp_router()
    r.set_machine_status("macbook_pro", MachineStatus.UNHEALTHY)

    with patch("lib.hybrid_router.notify_wol_failure") as mock_notify, \
         patch("lib.hybrid_router.asyncio.sleep", new=AsyncMock()):
        async def go():
            return await r.route_to_macbook(
                task="vault_synthesis", wake_timeout_s=0.5,
                notify_on=["agent_error", "gate_check_fail"],
            )
        with pytest.raises(WOLUnavailable):
            asyncio.run(go())

    mock_notify.assert_not_called()


def test_route_to_macbook_notifies_when_opted_in(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If Sean opts in by adding `host_unreachable` to notify_on, exactly one
    page fires per run (route-once means one call site)."""
    r = _mbp_router()
    r.set_machine_status("macbook_pro", MachineStatus.UNHEALTHY)

    with patch("lib.hybrid_router.notify_wol_failure") as mock_notify, \
         patch("lib.hybrid_router.asyncio.sleep", new=AsyncMock()):
        async def go():
            return await r.route_to_macbook(
                task="vault_synthesis", wake_timeout_s=0.5,
                notify_on=["agent_error", "host_unreachable"],
            )
        with pytest.raises(WOLUnavailable):
            asyncio.run(go())

    mock_notify.assert_called_once()


def test_route_to_macbook_legacy_none_still_notifies() -> None:
    """Backward-compat: callers that pass no notify_on (flush, legacy tests)
    keep the previous notify-on-failure behavior."""
    r = _mbp_router()
    r.set_machine_status("macbook_pro", MachineStatus.UNHEALTHY)

    with patch("lib.hybrid_router.notify_wol_failure") as mock_notify, \
         patch("lib.hybrid_router.asyncio.sleep", new=AsyncMock()):
        async def go():
            return await r.route_to_macbook(task="vault_synthesis", wake_timeout_s=0.5)
        with pytest.raises(WOLUnavailable):
            asyncio.run(go())

    mock_notify.assert_called_once()


# ─── C1: main() route-once + typed deferral (Fixes Origin A+B end-to-end) ─────

def test_main_defers_once_when_host_unreachable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fixes Origin A+B end-to-end: on a down-host night with changed files,
    main() must resolve the route ONCE, take the typed deferral path, and:
      - exit 0 (launchd-friendly)
      - write exactly one wol-deferred manifest (status/wol_status truthful)
      - NOT advance indexer state (work re-queues next opportunity)
      - route exactly once (no per-file poll storm)
    """
    import agents.vault_synthesizer as vs
    import agents.vault_indexer as vi

    _stub_pushover_creds(monkeypatch)
    vault = tmp_path / "vault"
    logs = tmp_path / "logs"
    (vault / "health").mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    cfg = SimpleNamespace(
        vault_root=vault, log_dir=logs, log_level="INFO", fleet_memory={},
    )
    monkeypatch.setattr(vs, "load_config", lambda: cfg)

    # One changed file so there IS Tier-2 work to defer (the empty-run edge
    # case must NOT defer, but that's a separate test). The pre-flight route
    # resolution defers before run_synthesis ever reads it, but make it real
    # so the RED reason is the missing routing hoist, not a missing-file read.
    (vault / "n0.md").write_text("# Note 0\nbody 0", encoding="utf-8")
    monkeypatch.setattr(vi, "read_indexer_state", lambda p: {})
    monkeypatch.setattr(
        vi, "detect_changed_files",
        lambda root, prior: ([vault / "n0.md"], {"n0.md": "hash"}),
    )
    wis = MagicMock()
    monkeypatch.setattr(vi, "write_indexer_state", wis)

    route_calls = {"n": 0}

    async def _raise_wol(self, *args, **kwargs):
        route_calls["n"] += 1
        raise WOLUnavailable("macbook_pro unreachable (test)")

    monkeypatch.setattr(HybridRouter, "route_to_macbook", _raise_wol)
    monkeypatch.setattr(sys, "argv", ["vault_synthesizer"])

    rc = vs.main()

    assert rc == 0, "environmental deferral must exit 0"
    assert route_calls["n"] == 1, "must route exactly once per run, not per file"
    wis.assert_not_called()  # indexer state must NOT advance on a deferral

    manifest = vault / "health" / f"synth-manifest-{date.today().isoformat()}.json"
    assert manifest.exists(), "a wol-deferred manifest must be written"
    import json
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["status"] == "wol-deferred"
    assert data["wol_status"] == "wol_deferred"
