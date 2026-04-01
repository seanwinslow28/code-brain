"""Three-tier model routing across Mac Mini, MacBook Pro, and Alienware.

Routing tiers:
  1. Mac Mini (always-on, lightweight Ollama models)
  2. MacBook Pro (heavyweight local inference via MLX-LM)
  3. Alienware (CUDA-specialized, Ollama + ComfyUI)
  Fallback: Claude API (if all local machines are unreachable)

Health checks:
  - Ollama machines: GET /api/tags
  - MacBook Pro MLX-LM: check for running process (localhost only)

Wake-on-LAN:
  - Alienware can be woken via magic packet before routing CUDA tasks.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class MachineStatus(Enum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


@dataclass
class MachineConfig:
    """Configuration for a single machine in the fleet."""
    name: str
    host: str
    port: int
    tier: int
    runtime: str  # "ollama" or "mlx-lm"
    always_on: bool
    models: list[str]
    wol_mac: str = ""

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


@dataclass
class MachineHealth:
    """Cached health state for a machine."""
    status: MachineStatus = MachineStatus.UNKNOWN
    last_check: float = 0.0
    available_models: list[str] = field(default_factory=list)
    latency_ms: float = 0.0


@dataclass
class RoutingDecision:
    """Result of a routing decision."""
    machine: str
    model: str
    base_url: str
    runtime: str
    is_fallback: bool = False
    reason: str = ""


class HybridRouter:
    """Three-tier model router with health checking and WOL support."""

    def __init__(
        self,
        machines: dict[str, MachineConfig],
        task_map: dict[str, dict[str, str]],
        health_check_timeout: float = 3.0,
        health_check_interval: float = 60.0,
        fallback_to_api: bool = True,
    ) -> None:
        self.machines = machines
        self.task_map = task_map
        self.health_check_timeout = health_check_timeout
        self.health_check_interval = health_check_interval
        self.fallback_to_api = fallback_to_api
        self._health: dict[str, MachineHealth] = {
            name: MachineHealth() for name in machines
        }

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> HybridRouter:
        """Create a HybridRouter from a parsed config.toml routing section."""
        routing = config["routing"]
        machines: dict[str, MachineConfig] = {}
        for name, mc in routing["machines"].items():
            machines[name] = MachineConfig(
                name=name,
                host=mc["host"],
                port=mc["port"],
                tier=mc["tier"],
                runtime=mc["runtime"],
                always_on=mc["always_on"],
                models=mc["models"],
                wol_mac=mc.get("wol_mac", ""),
            )
        task_map = routing.get("task_map", {})
        return cls(
            machines=machines,
            task_map=task_map,
            health_check_timeout=routing.get("health_check_timeout_secs", 3.0),
            health_check_interval=routing.get("health_check_interval_secs", 60.0),
            fallback_to_api=routing.get("fallback_to_api", True),
        )

    async def check_health(self, machine_name: str) -> MachineHealth:
        """Check if a machine is reachable and what models are loaded."""
        mc = self.machines[machine_name]
        health = self._health[machine_name]

        # Skip if checked recently
        now = time.monotonic()
        if (
            health.status != MachineStatus.UNKNOWN
            and (now - health.last_check) < self.health_check_interval
        ):
            return health

        start = time.monotonic()
        try:
            if mc.runtime == "ollama":
                health = await self._check_ollama(mc)
            elif mc.runtime == "mlx-lm":
                health = await self._check_mlx(mc)
            else:
                health = MachineHealth(status=MachineStatus.UNHEALTHY)
            health.latency_ms = (time.monotonic() - start) * 1000
            health.last_check = now
        except Exception as exc:
            logger.warning("Health check failed for %s: %s", machine_name, exc)
            health = MachineHealth(
                status=MachineStatus.UNHEALTHY,
                last_check=now,
                latency_ms=(time.monotonic() - start) * 1000,
            )

        self._health[machine_name] = health
        return health

    async def _check_ollama(self, mc: MachineConfig) -> MachineHealth:
        """Health check via Ollama /api/tags endpoint."""
        async with httpx.AsyncClient(timeout=self.health_check_timeout) as client:
            resp = await client.get(f"{mc.base_url}/api/tags")
            resp.raise_for_status()
            data = resp.json()
            model_names = [m["name"].split(":")[0] for m in data.get("models", [])]
            return MachineHealth(
                status=MachineStatus.HEALTHY,
                available_models=model_names,
            )

    async def _check_mlx(self, mc: MachineConfig) -> MachineHealth:
        """Health check for MLX-LM server.

        MLX-LM exposes an OpenAI-compatible API. Try /v1/models.
        Falls back to a simple TCP connect check.
        """
        async with httpx.AsyncClient(timeout=self.health_check_timeout) as client:
            try:
                resp = await client.get(f"{mc.base_url}/v1/models")
                resp.raise_for_status()
                data = resp.json()
                model_names = [m["id"] for m in data.get("data", [])]
                return MachineHealth(
                    status=MachineStatus.HEALTHY,
                    available_models=model_names,
                )
            except (httpx.HTTPStatusError, httpx.ConnectError, KeyError):
                # Fallback: just check TCP connectivity
                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(mc.host, mc.port),
                        timeout=self.health_check_timeout,
                    )
                    writer.close()
                    await writer.wait_closed()
                    return MachineHealth(
                        status=MachineStatus.HEALTHY,
                        available_models=mc.models,
                    )
                except (OSError, asyncio.TimeoutError):
                    return MachineHealth(status=MachineStatus.UNHEALTHY)

    async def check_all_health(self) -> dict[str, MachineHealth]:
        """Check health of all machines concurrently."""
        tasks = {
            name: self.check_health(name)
            for name in self.machines
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        for name, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                self._health[name] = MachineHealth(
                    status=MachineStatus.UNHEALTHY,
                    last_check=time.monotonic(),
                )
        return dict(self._health)

    def send_wol(self, machine_name: str) -> bool:
        """Send Wake-on-LAN magic packet to a machine.

        Returns True if packet was sent, False if no MAC configured.
        """
        mc = self.machines.get(machine_name)
        if not mc or not mc.wol_mac:
            logger.warning("No WOL MAC configured for %s", machine_name)
            return False

        try:
            from wakeonlan import send_magic_packet
            send_magic_packet(mc.wol_mac)
            logger.info("WOL packet sent to %s (%s)", machine_name, mc.wol_mac)
            return True
        except ImportError:
            logger.warning("wakeonlan package not installed; sending raw packet")
            return self._send_raw_wol(mc.wol_mac)
        except Exception as exc:
            logger.error("WOL failed for %s: %s", machine_name, exc)
            return False

    @staticmethod
    def _send_raw_wol(mac: str) -> bool:
        """Send a raw WOL magic packet via UDP broadcast."""
        import socket
        import struct

        mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
        magic = b"\xff" * 6 + mac_bytes * 16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic, ("<broadcast>", 9))
        return True

    async def route(self, task: str) -> RoutingDecision:
        """Route a task to the best available machine.

        Routing logic:
        1. Look up preferred machine/model from task_map
        2. If preferred machine is healthy, use it
        3. Otherwise, try other machines that have the model (by tier order)
        4. If no local machine works, fall back to Claude API
        """
        mapping = self.task_map.get(task)
        if not mapping:
            if self.fallback_to_api:
                return RoutingDecision(
                    machine="claude_api",
                    model="claude-sonnet-4-6",
                    base_url="https://api.anthropic.com",
                    runtime="api",
                    is_fallback=True,
                    reason=f"No task mapping for '{task}'",
                )
            raise ValueError(f"No task mapping for '{task}' and API fallback disabled")

        preferred_machine = mapping["machine"]
        preferred_model = mapping["model"]

        # Skip routing for non-model tasks (e.g., ComfyUI REST)
        if preferred_model == "none":
            return RoutingDecision(
                machine=preferred_machine,
                model="none",
                base_url=self.machines[preferred_machine].base_url,
                runtime=self.machines[preferred_machine].runtime,
                reason="Direct machine task (no model needed)",
            )

        # Check preferred machine first
        health = await self.check_health(preferred_machine)
        if health.status == MachineStatus.HEALTHY:
            mc = self.machines[preferred_machine]
            return RoutingDecision(
                machine=preferred_machine,
                model=preferred_model,
                base_url=mc.base_url,
                runtime=mc.runtime,
                reason=f"Preferred machine healthy (tier {mc.tier})",
            )

        # Try WOL for Alienware if it's the preferred machine
        if preferred_machine == "alienware":
            self.send_wol("alienware")

        # Fallback: try other machines by tier order
        sorted_machines = sorted(
            self.machines.values(),
            key=lambda m: m.tier,
        )
        for mc in sorted_machines:
            if mc.name == preferred_machine:
                continue  # Already tried
            if preferred_model in mc.models:
                h = await self.check_health(mc.name)
                if h.status == MachineStatus.HEALTHY:
                    return RoutingDecision(
                        machine=mc.name,
                        model=preferred_model,
                        base_url=mc.base_url,
                        runtime=mc.runtime,
                        is_fallback=True,
                        reason=f"Fallback from {preferred_machine} to {mc.name} (tier {mc.tier})",
                    )

        # All local machines failed — fall back to Claude API
        if self.fallback_to_api:
            return RoutingDecision(
                machine="claude_api",
                model="claude-sonnet-4-6",
                base_url="https://api.anthropic.com",
                runtime="api",
                is_fallback=True,
                reason=f"All local machines unreachable for '{task}'",
            )

        raise RuntimeError(f"No available machine for task '{task}' and API fallback disabled")

    def set_machine_status(self, machine_name: str, status: MachineStatus) -> None:
        """Manually override a machine's health status (for testing).

        Sets last_check far into the future so check_health() respects the override.
        """
        if machine_name in self._health:
            self._health[machine_name].status = status
            # Use a very large last_check so the cache is always fresh
            self._health[machine_name].last_check = time.monotonic() + 1_000_000

    def get_health_summary(self) -> dict[str, str]:
        """Get a human-readable summary of all machine health states."""
        return {
            name: f"{h.status.value} (latency: {h.latency_ms:.0f}ms)"
            for name, h in self._health.items()
        }
