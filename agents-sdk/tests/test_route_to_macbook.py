"""Tests for HybridRouter.route_to_macbook() — Phase 6 cross-machine transport."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from lib.hybrid_router import (
    HybridRouter,
    MachineConfig,
    MachineHealth,
    MachineStatus,
    WOLUnavailable,
)


def _router() -> HybridRouter:
    machines = {
        "mac_mini": MachineConfig(
            name="mac_mini",
            host="192.168.68.200",
            port=11434,
            tier=1,
            runtime="ollama",
            always_on=True,
            models=["phi4-mini-reasoning"],
        ),
        "macbook_pro": MachineConfig(
            name="macbook_pro",
            host="127.0.0.1",
            port=8080,
            tier=2,
            runtime="lm-studio",
            always_on=True,
            models=["Qwen3-14B"],
        ),
    }
    task_map = {
        "vault_synthesis": {"model": "Qwen3-14B", "machine": "macbook_pro"},
    }
    return HybridRouter(machines=machines, task_map=task_map)


def test_route_to_macbook_healthy_returns_decision() -> None:
    r = _router()
    r.set_machine_status("macbook_pro", MachineStatus.HEALTHY)

    async def go():
        return await r.route_to_macbook(task="vault_synthesis")

    decision = asyncio.run(go())
    assert decision.machine == "macbook_pro"
    assert decision.model == "Qwen3-14B"
    assert decision.runtime == "lm-studio"
    assert "127.0.0.1" in decision.base_url


def test_route_to_macbook_unhealthy_raises_wol_unavailable() -> None:
    r = _router()
    r.set_machine_status("macbook_pro", MachineStatus.UNHEALTHY)

    async def go():
        return await r.route_to_macbook(task="vault_synthesis", wake_timeout_s=0.5)

    with patch("lib.hybrid_router.notify_wol_failure") as mock_notify:
        with pytest.raises(WOLUnavailable):
            asyncio.run(go())
        mock_notify.assert_called_once()
        kwargs = mock_notify.call_args.kwargs
        assert kwargs["task"] == "vault_synthesis"
        assert kwargs["machine"] == "macbook_pro"


def test_route_to_macbook_unknown_task_raises() -> None:
    r = _router()
    r.set_machine_status("macbook_pro", MachineStatus.HEALTHY)

    async def go():
        return await r.route_to_macbook(task="not_a_task")

    with pytest.raises(ValueError, match="not_a_task"):
        asyncio.run(go())


def test_route_to_macbook_rejects_non_macbook_task() -> None:
    """If the task maps to a different machine, route_to_macbook must refuse."""
    r = _router()
    r.task_map["inbox_triage"] = {"model": "phi4-mini-reasoning", "machine": "mac_mini"}
    r.set_machine_status("macbook_pro", MachineStatus.HEALTHY)

    async def go():
        return await r.route_to_macbook(task="inbox_triage")

    with pytest.raises(ValueError, match="not mapped to macbook_pro"):
        asyncio.run(go())


# ─── Phase 6 P0.2 — WOL path tests ───────────────────────────────────────────


def _router_with_wol() -> HybridRouter:
    """Router fixture with wol_mac configured on macbook_pro."""
    r = _router()
    r.machines["macbook_pro"].wol_mac = "50:F2:65:EF:AC:3D"
    r.machines["macbook_pro"].always_on = False
    return r


def test_route_to_macbook_sends_wol_when_mac_configured() -> None:
    """When wol_mac is set and MBP is already healthy, still fire exactly one
    magic packet, then return the RoutingDecision without retrying."""
    r = _router_with_wol()
    r.set_machine_status("macbook_pro", MachineStatus.HEALTHY)

    with patch("wakeonlan.send_magic_packet") as mock_wol:
        async def go():
            return await r.route_to_macbook(task="vault_synthesis")
        decision = asyncio.run(go())

    mock_wol.assert_called_once_with("50:F2:65:EF:AC:3D")
    assert decision.machine == "macbook_pro"
    assert decision.reason == "route_to_macbook: healthy"


def test_route_to_macbook_wakes_after_retries() -> None:
    """MBP is UNHEALTHY for the first 3 polls, then HEALTHY. Must send WOL
    exactly once, retry health-check, and return a successful RoutingDecision."""
    r = _router_with_wol()

    call_count = {"n": 0}

    async def flaky_check(_machine_name: str) -> MachineHealth:
        call_count["n"] += 1
        if call_count["n"] <= 3:
            return MachineHealth(status=MachineStatus.UNHEALTHY, last_check=0.0)
        return MachineHealth(status=MachineStatus.HEALTHY, last_check=0.0)

    with patch("wakeonlan.send_magic_packet") as mock_wol, \
         patch.object(r, "check_health", side_effect=flaky_check), \
         patch("lib.hybrid_router.asyncio.sleep", new=AsyncMock()):
        async def go():
            return await r.route_to_macbook(task="vault_synthesis", wake_timeout_s=30.0)
        decision = asyncio.run(go())

    mock_wol.assert_called_once_with("50:F2:65:EF:AC:3D")
    assert call_count["n"] == 4  # 3 failures + 1 success
    assert decision.machine == "macbook_pro"


def test_route_to_macbook_wol_fails_notifies_once() -> None:
    """If MBP never responds before wake_timeout_s, send WOL once, fire
    exactly one Pushover notification, and raise WOLUnavailable."""
    r = _router_with_wol()
    r.set_machine_status("macbook_pro", MachineStatus.UNHEALTHY)

    with patch("wakeonlan.send_magic_packet") as mock_wol, \
         patch("lib.hybrid_router.notify_wol_failure") as mock_notify, \
         patch("lib.hybrid_router.asyncio.sleep", new=AsyncMock()):
        async def go():
            return await r.route_to_macbook(task="vault_synthesis", wake_timeout_s=0.5)
        with pytest.raises(WOLUnavailable):
            asyncio.run(go())

    mock_wol.assert_called_once_with("50:F2:65:EF:AC:3D")
    mock_notify.assert_called_once()
    kwargs = mock_notify.call_args.kwargs
    assert kwargs["task"] == "vault_synthesis"
    assert kwargs["machine"] == "macbook_pro"
