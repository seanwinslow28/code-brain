"""Trigger a graceful sleep on the Alienware via SSH.

Windows: invokes `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` (modern sleep).
Linux: invokes `systemctl suspend`.

The OS is inferred from a small probe — if the SSH banner contains "Windows"
the Windows command is used; otherwise Linux is assumed. Override with --os.
"""
from __future__ import annotations

import argparse
import subprocess
import sys


def detect_os(host: str, user: str) -> str:
    """Return 'windows' or 'linux' based on the remote SSH banner."""
    result = subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=5",
         f"{user}@{host}", "ver"],
        capture_output=True, text=True, timeout=10,
    )
    out = (result.stdout + result.stderr).lower()
    if "windows" in out or "microsoft" in out:
        return "windows"
    return "linux"


def sleep_remote(host: str, user: str, os_override: str | None = None) -> int:
    os_kind = os_override or detect_os(host, user)
    if os_kind == "windows":
        # Modern Standby on the Alienware Aurora ACT1 250 silently rejects
        # both rundll32.exe SetSuspendState (XP-era API) and the .NET
        # System.Windows.Forms.Application.SetSuspendState call — both return
        # success but the OS never actually transitions to S0ix when invoked
        # via SSH, with or without ForceCritical=$true. Sysinternals
        # psshutdown.exe is the canonical headless-sleep tool for Windows
        # and it works reliably from non-interactive SSH sessions.
        # Install: see Topic 20 Phase 2 decision record.
        #   -d   = Suspend (sleep, not hibernate)
        #   -t 0 = 0-second countdown
        # Discovered 2026-05-24 during Topic 20 Phase 2.
        cmd = r'C:\Tools\PsTools\psshutdown.exe -d -t 0'
    else:
        cmd = "sudo systemctl suspend"

    result = subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=accept-new", f"{user}@{host}", cmd],
        timeout=30,
    )
    return result.returncode


def main() -> int:
    p = argparse.ArgumentParser(description="Gracefully sleep the Alienware (Tier C) via SSH.")
    p.add_argument("--host", default="192.168.68.201")
    p.add_argument("--user", required=True, help="SSH username on the Alienware")
    p.add_argument("--os", choices=["windows", "linux"], help="Skip OS auto-detect")
    args = p.parse_args()
    return sleep_remote(args.host, args.user, args.os)


if __name__ == "__main__":
    sys.exit(main())
