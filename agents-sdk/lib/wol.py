"""Wake-on-LAN magic packet construction + send.

Pattern A — sender is the always-on Mac Mini; target is the Alienware on the
same wired LAN. Magic packet is broadcast UDP on port 9 (RFC convention).
"""
from __future__ import annotations

import re
import socket
import time
from typing import Optional


_MAC_RE = re.compile(
    r"^([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})"
    r"[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})[:-]([0-9A-Fa-f]{2})$"
)


def parse_mac(mac: str) -> bytes:
    """Parse a MAC address in colon or dash format into 6 raw bytes."""
    m = _MAC_RE.match(mac.strip())
    if not m:
        raise ValueError(f"invalid MAC address: {mac!r}")
    return bytes(int(group, 16) for group in m.groups())


def build_magic_packet(mac: str) -> bytes:
    """Build a standard WoL magic packet for the given MAC address.

    Format: 6 bytes of 0xFF + 16 repetitions of the target MAC = 102 bytes.
    """
    mac_bytes = parse_mac(mac)
    return b"\xff" * 6 + mac_bytes * 16


def send_magic_packet(
    mac: str,
    broadcast_addr: str = "255.255.255.255",
    port: int = 9,
    repeats: int = 3,
) -> None:
    """Send a WoL magic packet via UDP broadcast.

    Sends `repeats` times back-to-back (some NICs miss the first one).
    """
    packet = build_magic_packet(mac)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        for _ in range(repeats):
            sock.sendto(packet, (broadcast_addr, port))
    finally:
        sock.close()


def probe_until_ready(
    host: str,
    port: int,
    timeout_total_secs: int = 120,
    interval_secs: int = 3,
) -> Optional[float]:
    """Open a TCP connect to (host, port) every interval_secs until it succeeds.

    Returns elapsed seconds on success, None on total-timeout.
    """
    start = time.monotonic()
    deadline = start + timeout_total_secs
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=interval_secs):
                return time.monotonic() - start
        except (OSError, socket.timeout):
            time.sleep(interval_secs)
    return None
