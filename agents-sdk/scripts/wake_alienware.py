"""Wake the Alienware via WoL and block until Ollama is responsive.

Defaults pulled from config.toml [routing.machines.alienware]. The script
exits 0 once Ollama at /api/tags responds, exits 1 on total timeout.
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from lib.wol import send_magic_packet, probe_until_ready  # noqa: E402


CONFIG_PATH = HERE / "config.toml"


def _alienware_config() -> dict:
    with open(CONFIG_PATH, "rb") as f:
        raw = tomllib.load(f)
    return raw.get("routing", {}).get("machines", {}).get("alienware", {})


def main() -> int:
    p = argparse.ArgumentParser(
        description="WoL + readiness probe for the Alienware (Tier C)."
    )
    p.add_argument("--mac", help="Override MAC (default: config.toml routing.machines.alienware.wol_mac)")
    p.add_argument("--host", help="Override host for the readiness probe")
    p.add_argument("--port", type=int, help="Override port for the readiness probe")
    p.add_argument("--timeout", type=int, default=180, help="Total wait budget in seconds (default 180)")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    machine = _alienware_config()
    mac = args.mac or machine.get("wol_mac")
    host = args.host or machine.get("host", "192.168.68.201")
    port = int(args.port or machine.get("port", 11434))

    if not mac:
        print(
            "ERROR: no MAC address resolved "
            "(set --mac or config.toml routing.machines.alienware.wol_mac)",
            file=sys.stderr,
        )
        return 1

    if not args.quiet:
        print(f"[wake_alienware] sending magic packet to {mac} via UDP broadcast :9 (x3)")

    send_magic_packet(mac)

    if not args.quiet:
        print(f"[wake_alienware] probing tcp://{host}:{port} every 3s for up to {args.timeout}s")

    elapsed = probe_until_ready(host, port, timeout_total_secs=args.timeout, interval_secs=3)
    if elapsed is None:
        print(f"[wake_alienware] TIMEOUT after {args.timeout}s", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"[wake_alienware] ready in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
