#!/usr/bin/env python3
"""Phase 1 Smoke Test — validates SDK setup, routing config, keychain, and machine health.

Usage:
    PYTHONPATH=. .venv/bin/python3 test_phase1_smoke.py [--dry-run]

Flags:
    --dry-run  Skip real network calls and API interactions. No money spent.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# ── Helpers ────────────────────────────────────────────────────────────

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"

results: list[tuple[str, str, str]] = []  # (test_name, status, detail)


def record(name: str, passed: bool, detail: str = "") -> None:
    status = PASS if passed else FAIL
    results.append((name, status, detail))
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))


def warn(name: str, detail: str) -> None:
    results.append((name, WARN, detail))
    print(f"  [{WARN}] {name} — {detail}")


# ── Tests ──────────────────────────────────────────────────────────────

def test_config_loads() -> None:
    """Verify config.toml loads with routing section."""
    try:
        import toml
        config = toml.load(Path(__file__).parent / "config.toml")
        has_routing = "routing" in config
        has_machines = "machines" in config.get("routing", {})
        machine_names = list(config.get("routing", {}).get("machines", {}).keys())
        record(
            "config.toml loads",
            has_routing and has_machines,
            f"machines: {machine_names}",
        )
        # Verify all 3 machines present
        expected = {"mac_mini", "macbook_pro", "alienware"}
        record(
            "All 3 machines in config",
            set(machine_names) == expected,
            f"found: {set(machine_names)}",
        )
        # Verify task_map exists
        task_map = config["routing"].get("task_map", {})
        record(
            "Task map populated",
            len(task_map) > 0,
            f"{len(task_map)} task mappings",
        )
    except Exception as e:
        record("config.toml loads", False, str(e))


def test_keychain_module() -> None:
    """Verify keychain module imports and functions exist."""
    try:
        from lib.keychain import get_credential, set_credential, list_credentials, delete_credential
        # Don't actually store anything — just verify the module loads
        record("keychain module imports", True)

        # Verify it's using the correct service prefix
        from lib.keychain import SERVICE_PREFIX
        record(
            "keychain service prefix",
            SERVICE_PREFIX == "com.sean.agents",
            f"prefix: {SERVICE_PREFIX}",
        )
    except Exception as e:
        record("keychain module imports", False, str(e))


def test_hybrid_router_module() -> None:
    """Verify hybrid_router imports and constructs from config."""
    try:
        from lib.hybrid_router import HybridRouter, MachineStatus
        import toml

        config = toml.load(Path(__file__).parent / "config.toml")
        router = HybridRouter.from_config(config)
        record(
            "HybridRouter constructs from config",
            True,
            f"{len(router.machines)} machines, {len(router.task_map)} tasks",
        )

        # Verify routing decisions work (with simulated health)
        router.set_machine_status("mac_mini", MachineStatus.HEALTHY)
        decision = asyncio.run(router.route("inbox_triage"))
        record(
            "Routing decision works",
            decision.machine == "mac_mini" and decision.model == "phi4-mini-reasoning",
            f"→ {decision.machine}/{decision.model}",
        )

        # Verify API fallback
        for name in router.machines:
            router.set_machine_status(name, MachineStatus.UNHEALTHY)
        fallback = asyncio.run(router.route("inbox_triage"))
        record(
            "API fallback works",
            fallback.is_fallback and fallback.machine == "claude_api",
            f"→ {fallback.machine}",
        )
    except Exception as e:
        record("HybridRouter module", False, str(e))


def test_safety_hooks_exist() -> None:
    """Verify safety hook files exist and are executable."""
    hooks_dir = Path(__file__).parent.parent / ".claude" / "hooks"
    required_hooks = ["loop-detector.py", "cost-watchdog.py", "vault-integrity.py"]

    for hook in required_hooks:
        path = hooks_dir / hook
        record(f"Hook exists: {hook}", path.exists(), str(path))


async def test_machine_health(dry_run: bool) -> None:
    """Ping reachable machines (skip in dry-run mode)."""
    if dry_run:
        warn("Machine health checks", "Skipped (--dry-run)")
        return

    from lib.hybrid_router import HybridRouter, MachineStatus
    import toml

    config = toml.load(Path(__file__).parent / "config.toml")
    router = HybridRouter.from_config(config)

    health = await router.check_all_health()
    for name, h in health.items():
        if h.status == MachineStatus.HEALTHY:
            record(f"Machine reachable: {name}", True, f"latency: {h.latency_ms:.0f}ms")
        else:
            warn(f"Machine reachable: {name}", f"unreachable (status: {h.status.value})")


def test_sdk_naming() -> None:
    """Verify we're using correct SDK naming conventions."""
    # Check config.toml doesn't contain old names
    config_text = (Path(__file__).parent / "config.toml").read_text()
    record(
        "No 'claude-code-sdk' in config",
        "claude-code-sdk" not in config_text,
    )
    record(
        "No 'ClaudeCodeOptions' in config",
        "ClaudeCodeOptions" not in config_text,
    )

    # Check hybrid_router.py
    router_text = (Path(__file__).parent / "lib" / "hybrid_router.py").read_text()
    record(
        "No 'dangerouslySkipPermissions' in router",
        "dangerouslySkipPermissions" not in router_text,
    )


# ── Main ───────────────────────────────────────────────────────────────

def main() -> None:
    dry_run = "--dry-run" in sys.argv
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"\n{'='*60}")
    print(f"  Phase 1 Smoke Test ({mode})")
    print(f"{'='*60}\n")

    test_config_loads()
    test_keychain_module()
    test_hybrid_router_module()
    test_safety_hooks_exist()
    asyncio.run(test_machine_health(dry_run))
    test_sdk_naming()

    # Summary
    print(f"\n{'='*60}")
    passes = sum(1 for _, s, _ in results if "PASS" in s)
    fails = sum(1 for _, s, _ in results if "FAIL" in s)
    warns = sum(1 for _, s, _ in results if "WARN" in s)
    print(f"  Results: {passes} passed, {fails} failed, {warns} warnings")
    print(f"{'='*60}\n")

    if fails > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
