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
