#!/usr/bin/env python3
"""Live Wake-on-LAN verification for MacBook Pro — Phase 6 P0.2.

Run this FROM THE MAC MINI (not the MBP — you can't wake yourself).
Expected flow:
  1. Put the MBP to sleep (Apple menu → Sleep) on the MBP itself.
  2. Wait ~30s so deep sleep settles.
  3. Run this script on the Mac Mini.
  4. MBP should wake within 90s, LM Studio should respond on :1234.

Stdlib-only (no wakeonlan package dep). Safe to run from any machine on
the 192.168.68.0/22 subnet.
"""

from __future__ import annotations

import socket
import sys
import time
import urllib.error
import urllib.request

MBP_IP = "192.168.68.50"
MBP_MAC = "50:F2:65:EF:AC:3D"
MBP_LMSTUDIO_URL = f"http://{MBP_IP}:1234/v1/models"
TIMEOUT_S = 90
POLL_INTERVAL_S = 2


def send_magic_packet(mac: str) -> None:
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    if len(mac_bytes) != 6:
        raise ValueError(f"Bad MAC length: {mac}")
    magic = b"\xff" * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic, ("<broadcast>", 9))
        sock.sendto(magic, ("<broadcast>", 7))


def poll_lm_studio(deadline: float) -> tuple[bool, float]:
    start = time.monotonic()
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(MBP_LMSTUDIO_URL, timeout=2) as r:
                if r.status == 200:
                    return True, time.monotonic() - start
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            pass
        time.sleep(POLL_INTERVAL_S)
    return False, time.monotonic() - start


def main() -> int:
    print(f"[{time.strftime('%H:%M:%S')}] Phase 6 P0.2 — MBP WOL live verification")
    print(f"  target: {MBP_IP} (MAC {MBP_MAC})")
    print(f"  endpoint: {MBP_LMSTUDIO_URL}")

    # Pre-flight: confirm MBP is currently unreachable (proves we're testing a wake, not a no-op)
    print("\n[pre-flight] Checking MBP is asleep...")
    try:
        with urllib.request.urlopen(MBP_LMSTUDIO_URL, timeout=2) as r:
            print(f"  ⚠️  MBP already reachable (status={r.status}). "
                  "This test should be run with the MBP asleep.")
            print("     Continuing anyway to exercise the WOL path end-to-end.")
            already_up = True
    except Exception as exc:
        print(f"  ✓ MBP unreachable ({exc.__class__.__name__}) — good, ready to wake it.")
        already_up = False

    # Fire magic packet
    print(f"\n[{time.strftime('%H:%M:%S')}] Sending WOL magic packet to {MBP_MAC}...")
    send_magic_packet(MBP_MAC)
    print("  ✓ Packet broadcast on UDP ports 7 + 9.")

    # Poll
    print(f"\n[{time.strftime('%H:%M:%S')}] Polling LM Studio (timeout {TIMEOUT_S}s)...")
    deadline = time.monotonic() + TIMEOUT_S
    up, elapsed = poll_lm_studio(deadline)

    if up:
        print(f"\n✅ SUCCESS — MBP responded after {elapsed:.1f}s")
        if already_up:
            print("   (MBP was already up; this only confirmed connectivity, not a wake.)")
            return 2
        return 0
    print(f"\n❌ TIMEOUT — MBP did not respond within {TIMEOUT_S}s")
    print("   Troubleshooting:")
    print("   - Verify MBP System Settings → Battery → Options → 'Wake for network access' is ON")
    print("   - On Wi-Fi: check 'Wake for Wi-Fi network access' is ON (flaky on Apple Silicon)")
    print("   - Check Private Wi-Fi Address setting; WOL needs the NIC's permanent MAC")
    print("   - Confirm MBP + Mini are on the same broadcast domain (no VLAN separation)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
