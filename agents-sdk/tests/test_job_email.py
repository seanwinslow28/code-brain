"""Tests for lib/job_email.py — the Job Feed Gmail digest layer.

Credential-free: keychain is monkeypatched, SMTP is injected. No network, no
real `security` calls — green in CI and in the sandbox.
"""

from __future__ import annotations

import json
from datetime import datetime
from types import SimpleNamespace

import pytest

from lib import job_email


def _fit(db_id: int, *, company: str, score: int, title: str = "Product Manager"):
    """Build a (db_id, posting, scoring_result) tuple matching scored_today()."""
    posting = SimpleNamespace(
        company=company,
        title=title,
        location="Remote, US",
        salary_disclosed=None,
        posted_at=datetime(2026, 6, 18),
        url=f"https://example.com/{company.lower()}/{db_id}",
        source=f"greenhouse:{company.lower()}",
    )
    result = SimpleNamespace(
        fit_score=score,
        role_band="PM",
        rationale=f"{company} is a strong AI-PM fit.",
        concerns=["salary: undisclosed"],
        fit_dimensions={},
    )
    return (db_id, posting, result)


def test_select_unsent_fits_filters_by_score_and_ledger():
    fits = [
        _fit(1, company="Braintrust", score=5),
        _fit(2, company="Cresta", score=3),
        _fit(3, company="WeakCo", score=2),     # below min
        _fit(4, company="Polymarket", score=4),
    ]
    out = job_email.select_unsent_fits(
        fits, already_sent_ids={4}, min_fit_score=3
    )
    ids = [db_id for (db_id, _p, _s) in out]
    assert ids == [1, 2]  # 3 dropped (weak), 4 dropped (already sent)


def test_build_digest_subject_and_body():
    fits = [_fit(1, company="Braintrust", score=5), _fit(2, company="Cresta", score=3)]
    subject, text, html = job_email.build_digest("2026-06-18", fits)

    assert "2 new fits" in subject
    assert "1 strong" in subject
    # both companies + apply links + db_ids present in each rendering
    for body in (text, html):
        assert "Braintrust" in body
        assert "Cresta" in body
        assert "https://example.com/braintrust/1" in body
    assert "db_id 1" in html


def test_build_digest_singular_no_strong():
    fits = [_fit(7, company="Cresta", score=3)]
    subject, _text, _html = job_email.build_digest("2026-06-18", fits)
    assert "1 new fit " in subject + " "  # singular
    assert "strong" not in subject


class _FakeSMTP:
    def __init__(self):
        self.logged_in = None
        self.sent = []
        self.quit_called = False

    def login(self, addr, pw):
        self.logged_in = (addr, pw)

    def send_message(self, msg):
        self.sent.append(msg)

    def quit(self):
        self.quit_called = True


def test_send_job_digest_logs_in_and_sends(monkeypatch):
    fake = _FakeSMTP()
    job_email.send_job_digest(
        subject="s",
        text_body="t",
        html_body="<p>h</p>",
        gmail_address="me@gmail.com",
        app_password="apppw",
        smtp_factory=lambda: fake,
    )
    assert fake.logged_in == ("me@gmail.com", "apppw")
    assert len(fake.sent) == 1
    msg = fake.sent[0]
    assert msg["From"] == "me@gmail.com"
    assert msg["To"] == "me@gmail.com"
    assert fake.quit_called


def test_send_job_digest_missing_creds_raises(monkeypatch):
    monkeypatch.setattr(job_email, "get_credential", lambda name: None)
    with pytest.raises(job_email.JobEmailError):
        job_email.send_job_digest(
            subject="s", text_body="t", html_body="h", smtp_factory=lambda: _FakeSMTP()
        )


def test_maybe_send_digest_disabled_is_noop(tmp_path):
    res = job_email.maybe_send_digest(
        email_cfg={"enabled": False},
        fits=[_fit(1, company="Braintrust", score=5)],
        ledger_path=tmp_path / ".emailed.json",
        today_iso="2026-06-18",
    )
    assert res == {"sent": 0, "error": None}
    assert not (tmp_path / ".emailed.json").exists()


def test_maybe_send_digest_sends_then_dedupes(tmp_path, monkeypatch):
    monkeypatch.setattr(job_email, "get_credential", lambda name: "x")
    fake = _FakeSMTP()
    ledger = tmp_path / ".emailed-2026-06-18.json"
    fits = [_fit(1, company="Braintrust", score=5), _fit(2, company="Cresta", score=3)]

    res1 = job_email.maybe_send_digest(
        email_cfg={"enabled": True, "min_fit_score": 3},
        fits=fits,
        ledger_path=ledger,
        today_iso="2026-06-18",
        smtp_factory=lambda: fake,
    )
    assert res1 == {"sent": 2, "error": None}
    assert set(json.loads(ledger.read_text())) == {1, 2}
    assert len(fake.sent) == 1  # one digest email covering both

    # Second fire, same fits already in ledger => no-op, no second email
    fake2 = _FakeSMTP()
    res2 = job_email.maybe_send_digest(
        email_cfg={"enabled": True, "min_fit_score": 3},
        fits=fits,
        ledger_path=ledger,
        today_iso="2026-06-18",
        smtp_factory=lambda: fake2,
    )
    assert res2 == {"sent": 0, "error": None}
    assert fake2.sent == []


def test_maybe_send_digest_swallows_send_error(tmp_path, monkeypatch):
    monkeypatch.setattr(job_email, "get_credential", lambda name: "x")

    def boom():
        raise OSError("smtp down")

    res = job_email.maybe_send_digest(
        email_cfg={"enabled": True, "min_fit_score": 3},
        fits=[_fit(1, company="Braintrust", score=5)],
        ledger_path=tmp_path / ".emailed.json",
        today_iso="2026-06-18",
        smtp_factory=boom,
    )
    assert res["sent"] == 0
    assert res["error"] and "smtp down" in res["error"]
    # ledger NOT written on failure => the next run retries
    assert not (tmp_path / ".emailed.json").exists()
