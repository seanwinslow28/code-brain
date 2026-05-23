"""Tests for lib/wol.py — magic packet construction."""
import pytest
from lib.wol import build_magic_packet, parse_mac


def test_parse_mac_colon_separated():
    assert parse_mac("B4:E9:B8:F7:71:47") == b"\xb4\xe9\xb8\xf7\x71\x47"


def test_parse_mac_dash_separated():
    assert parse_mac("B4-E9-B8-F7-71-47") == b"\xb4\xe9\xb8\xf7\x71\x47"


def test_parse_mac_lowercase():
    assert parse_mac("b4:e9:b8:f7:71:47") == b"\xb4\xe9\xb8\xf7\x71\x47"


def test_parse_mac_invalid_format_raises():
    with pytest.raises(ValueError):
        parse_mac("not-a-mac")


def test_magic_packet_structure():
    mac = "B4:E9:B8:F7:71:47"
    packet = build_magic_packet(mac)
    # Magic packet: 6 bytes 0xFF + 16 repetitions of the 6-byte MAC = 102 bytes
    assert len(packet) == 102
    assert packet[:6] == b"\xff" * 6
    # Verify the MAC repeats 16 times after the sync stream
    mac_bytes = b"\xb4\xe9\xb8\xf7\x71\x47"
    for i in range(16):
        offset = 6 + i * 6
        assert packet[offset:offset + 6] == mac_bytes
