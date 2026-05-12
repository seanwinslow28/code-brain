"""Tests for agents-sdk/agents/substack_drafter.py — voice-rotation module."""
from datetime import date
import pytest
from agents.substack_drafter import pick_voice_mode

# SPEC rotation table: 0=sean, 1=sedaris, 2=kerouac, 3=thompson, 4=vonnegut

def test_voice_mode_at_epoch():
    assert pick_voice_mode(today=date(2026, 5, 4), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_week_1():
    # 7 days after epoch → index 1 → sedaris
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4)) == "sedaris"


def test_voice_mode_week_2():
    # 14 days after epoch → index 2 → kerouac
    assert pick_voice_mode(today=date(2026, 5, 18), epoch=date(2026, 5, 4)) == "kerouac"


def test_voice_mode_week_3():
    # 21 days after epoch → index 3 → thompson
    assert pick_voice_mode(today=date(2026, 5, 25), epoch=date(2026, 5, 4)) == "thompson"


def test_voice_mode_week_4():
    # 28 days after epoch → index 4 → vonnegut
    assert pick_voice_mode(today=date(2026, 6, 1), epoch=date(2026, 5, 4)) == "vonnegut"


def test_voice_mode_wraps_at_5():
    # 35 days after epoch → index 5 → wraps to 0 → sean
    assert pick_voice_mode(today=date(2026, 6, 8), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_override_pins():
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="vonnegut") == "vonnegut"


def test_voice_mode_rejects_bad_override():
    with pytest.raises(ValueError):
        pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="hemingway")
