"""Tests for hybrid_router.py — three-tier model routing."""

from __future__ import annotations

import asyncio

import pytest

from lib.hybrid_router import (
    HybridRouter,
    MachineConfig,
    MachineStatus,
)

# ── Fixtures ───────────────────────────────────────────────────────────

def _make_machines() -> dict[str, MachineConfig]:
    return {
        "mac_mini": MachineConfig(
            name="mac_mini",
            host="192.168.68.200",
            port=11434,
            tier=1,
            runtime="ollama",
            always_on=True,
            models=["phi4-mini-reasoning", "phi4-mini", "nomic-embed-text"],
        ),
        "macbook_pro": MachineConfig(
            name="macbook_pro",
            host="127.0.0.1",
            port=8080,
            tier=2,
            runtime="mlx-lm",
            always_on=False,
            models=["Qwen3-14B", "Qwen2.5-Coder-32B", "Qwen3.5"],
        ),
        "alienware": MachineConfig(
            name="alienware",
            host="192.168.68.201",
            port=11434,
            tier=3,
            runtime="ollama",
            always_on=False,
            models=["Qwen3-VL-7B"],
            wol_mac="AA:BB:CC:DD:EE:FF",
        ),
    }


def _make_task_map() -> dict[str, dict[str, str]]:
    return {
        "inbox_triage": {"model": "phi4-mini-reasoning", "machine": "mac_mini"},
        "vault_embeddings": {"model": "nomic-embed-text", "machine": "mac_mini"},
        "financial_analysis": {"model": "Qwen3-14B", "machine": "macbook_pro"},
        "code_review": {"model": "Qwen2.5-Coder-32B", "machine": "macbook_pro"},
        "heavy_synthesis": {"model": "Qwen3.5", "machine": "macbook_pro"},
        "sprite_vision_qa": {"model": "Qwen3-VL-7B", "machine": "alienware"},
        "comfyui_orchestration": {"model": "none", "machine": "alienware"},
    }


@pytest.fixture
def router() -> HybridRouter:
    r = HybridRouter(
        machines=_make_machines(),
        task_map=_make_task_map(),
        health_check_timeout=1.0,
        health_check_interval=3600,  # Long interval; tests use set_machine_status override
        fallback_to_api=True,
    )
    return r


# ── Tests ──────────────────────────────────────────────────────────────

def test_route_inbox_to_mac_mini(router: HybridRouter) -> None:
    """inbox_triage should route to Mac Mini when healthy."""
    router.set_machine_status("mac_mini", MachineStatus.HEALTHY)
    result = asyncio.run(router.route("inbox_triage"))
    assert result.machine == "mac_mini"
    assert result.model == "phi4-mini-reasoning"
    assert not result.is_fallback


def test_route_code_review_to_macbook(router: HybridRouter) -> None:
    """code_review should route to MacBook Pro when healthy."""
    router.set_machine_status("macbook_pro", MachineStatus.HEALTHY)
    result = asyncio.run(router.route("code_review"))
    assert result.machine == "macbook_pro"
    assert result.model == "Qwen2.5-Coder-32B"
    assert not result.is_fallback


def test_route_sprite_qa_to_alienware(router: HybridRouter) -> None:
    """sprite_vision_qa should route to Alienware when healthy."""
    router.set_machine_status("alienware", MachineStatus.HEALTHY)
    result = asyncio.run(router.route("sprite_vision_qa"))
    assert result.machine == "alienware"
    assert result.model == "Qwen3-VL-7B"
    assert not result.is_fallback


def test_fallback_to_api_when_all_down(router: HybridRouter) -> None:
    """When all machines are unhealthy, fall back to Claude API."""
    for name in router.machines:
        router.set_machine_status(name, MachineStatus.UNHEALTHY)
    result = asyncio.run(router.route("inbox_triage"))
    assert result.machine == "claude_api"
    assert result.is_fallback
    assert "unreachable" in result.reason.lower()


def test_fallback_within_tier(router: HybridRouter) -> None:
    """If preferred machine is down but another has the model, use that."""
    router.set_machine_status("mac_mini", MachineStatus.UNHEALTHY)
    router.set_machine_status("macbook_pro", MachineStatus.HEALTHY)
    router.set_machine_status("alienware", MachineStatus.HEALTHY)
    # inbox_triage wants mac_mini's phi4-mini-reasoning
    # No other machine has that model → should fall to API
    result = asyncio.run(router.route("inbox_triage"))
    assert result.is_fallback
    assert result.machine == "claude_api"


def test_comfyui_direct_routing(router: HybridRouter) -> None:
    """comfyui_orchestration routes directly (no model needed)."""
    result = asyncio.run(router.route("comfyui_orchestration"))
    assert result.machine == "alienware"
    assert result.model == "none"
    assert not result.is_fallback


def test_unknown_task_falls_to_api(router: HybridRouter) -> None:
    """Unknown task should fall back to Claude API."""
    result = asyncio.run(router.route("nonexistent_task"))
    assert result.machine == "claude_api"
    assert result.is_fallback


def test_no_api_fallback_raises(router: HybridRouter) -> None:
    """With fallback disabled, unknown tasks raise ValueError."""
    router.fallback_to_api = False
    with pytest.raises(ValueError, match="No task mapping"):
        asyncio.run(router.route("nonexistent_task"))


def test_from_config() -> None:
    """Test building router from a config dict."""
    config = {
        "routing": {
            "health_check_timeout_secs": 2.0,
            "health_check_interval_secs": 30.0,
            "fallback_to_api": True,
            "machines": {
                "mac_mini": {
                    "host": "192.168.68.200",
                    "port": 11434,
                    "tier": 1,
                    "runtime": "ollama",
                    "always_on": True,
                    "models": ["phi4-mini-reasoning"],
                },
            },
            "task_map": {
                "inbox_triage": {"model": "phi4-mini-reasoning", "machine": "mac_mini"},
            },
        }
    }
    router = HybridRouter.from_config(config)
    assert "mac_mini" in router.machines
    assert router.health_check_timeout == 2.0


def test_health_summary(router: HybridRouter) -> None:
    """Health summary returns human-readable strings."""
    router.set_machine_status("mac_mini", MachineStatus.HEALTHY)
    summary = router.get_health_summary()
    assert "healthy" in summary["mac_mini"]
