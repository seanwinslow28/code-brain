"""Tests for the Job Feed strong-fit Pushover path in lib/pushover.py.

Credential-free: send is injected via send_fn, no network, no `security` calls.
"""

from __future__ import annotations

import json
from datetime import datetime
from types import SimpleNamespace

from lib import pushover


def _fit(db_id: int, *, company: str, score: int, title: str = "Product Manager"):
    posting = SimpleNamespace(company=company, title=title, url=f"https://x/{db_id}")
    result = SimpleNamespace(fit_score=score, role_band="PM")
    return (db_id, posting, result)


def test_build_strong_fits_push_title_and_lines():
    fits = [_fit(1, company="Braintrust", score=5), _fit(2, company="Polymarket", score=4)]
    title, message = pushover.build_strong_fits_push(fits)
    assert title == "2 strong job fits"
    assert "★5 Braintrust — Product Manager" in message
    assert "★4 Polymarket — Product Manager" in message


def test_build_strong_fits_push_singular_and_overflow():
    one = pushover.build_strong_fits_push([_fit(1, company="Cresta", score=4)])
    assert one[0] == "1 strong job fit"
    many = [_fit(i, company=f"Co{i}", score=4) for i in range(1, 8)]  # 7
    title, message = pushover.build_strong_fits_push(many)
    assert title == "7 strong job fits"
    assert "+2 more" in message  # only first 5 listed


def test_maybe_push_disabled_is_noop(tmp_path):
    res = pushover.maybe_push_strong_fits(
        push_cfg={"enabled": False},
        fits=[_fit(1, company="Braintrust", score=5)],
        ledger_path=tmp_path / ".pushed.json",
        today_iso="2026-06-18",
        send_fn=lambda **k: None,
    )
    assert res == {"pushed": 0, "error": None}


def test_maybe_push_only_strong_and_dedupes(tmp_path):
    sent = []

    def fake_send(**kwargs):
        sent.append(kwargs)

    ledger = tmp_path / ".pushed-2026-06-18.json"
    fits = [
        _fit(1, company="Braintrust", score=5),
        _fit(2, company="Cresta", score=3),       # below min (4) — excluded
        _fit(3, company="Polymarket", score=4),
    ]
    res1 = pushover.maybe_push_strong_fits(
        push_cfg={"enabled": True, "min_fit_score": 4},
        fits=fits,
        ledger_path=ledger,
        today_iso="2026-06-18",
        send_fn=fake_send,
    )
    assert res1 == {"pushed": 2, "error": None}          # 1 and 3, not 2
    assert set(json.loads(ledger.read_text())) == {1, 3}
    assert len(sent) == 1 and sent[0]["priority"] == 1   # one push, high priority

    # Second fire: same fits already pushed => no-op
    res2 = pushover.maybe_push_strong_fits(
        push_cfg={"enabled": True, "min_fit_score": 4},
        fits=fits,
        ledger_path=ledger,
        today_iso="2026-06-18",
        send_fn=fake_send,
    )
    assert res2 == {"pushed": 0, "error": None}
    assert len(sent) == 1


def test_maybe_push_swallows_send_error(tmp_path):
    def boom(**kwargs):
        raise pushover.PushoverError("pushover down")

    res = pushover.maybe_push_strong_fits(
        push_cfg={"enabled": True, "min_fit_score": 4},
        fits=[_fit(1, company="Braintrust", score=5)],
        ledger_path=tmp_path / ".pushed.json",
        today_iso="2026-06-18",
        send_fn=boom,
    )
    assert res["pushed"] == 0
    assert res["error"] and "pushover down" in res["error"]
    assert not (tmp_path / ".pushed.json").exists()  # ledger not written on failure
