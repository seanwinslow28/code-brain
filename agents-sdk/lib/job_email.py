"""Gmail email-digest helper for the Job Feed agent.

Sends a daily digest of new qualifying role fits to Sean's inbox so the Gmail
app notifies him when he's away from the desk. Mirrors lib/pushover.py: a thin,
best-effort notify layer over the agent's already-scored fits.

Credentials live in macOS Keychain (never plaintext in config, never in the
tracked repo):
    gmail_address        — the account used as BOTH sender and recipient
    gmail_app_password    — a 16-char Gmail App Password (requires 2-Step Verification)

Store them once via the existing helper:
    python3 lib/keychain.py set gmail_address you@gmail.com
    python3 lib/keychain.py set gmail_app_password <16-char-app-password>

Wiring: agents/job_feed.run_pipeline calls maybe_send_digest() after the roll-up
is written. A per-day ledger (.emailed-<date>.json in the roll-up dir) dedupes by
db_id so the 7 morning fires never re-send a role.
"""

from __future__ import annotations

import json
import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Callable

from lib.keychain import get_credential

logger = logging.getLogger(__name__)

SMTP_HOST_DEFAULT = "smtp.gmail.com"
SMTP_PORT_DEFAULT = 465
_TIMEOUT = 20.0

# A scored fit is the agent's (db_id, Posting, ScoringResult) tuple — see
# JobDB.scored_today(). We read attributes duck-typed so this module needs no
# import of the DB layer and stays trivially testable with stand-ins.
Fit = tuple


class JobEmailError(Exception):
    """Raised when an email digest send fails."""


# ── pure helpers (unit-testable, no I/O) ─────────────────────────────────────

def select_unsent_fits(
    fits: list[Fit], *, already_sent_ids: set[int], min_fit_score: int
) -> list[Fit]:
    """Return fits at/above min_fit_score whose db_id hasn't been emailed yet.

    Order is preserved (scored_today already sorts by fit_score desc).
    """
    out: list[Fit] = []
    for fit in fits:
        db_id, _posting, score = fit
        if score.fit_score is None or score.fit_score < min_fit_score:
            continue
        if db_id in already_sent_ids:
            continue
        out.append(fit)
    return out


def _fit_line_text(idx: int, fit: Fit) -> str:
    db_id, p, s = fit
    posted = p.posted_at.date().isoformat() if getattr(p, "posted_at", None) else "unknown"
    comp = getattr(p, "salary_disclosed", None) or "not disclosed"
    concerns = "; ".join(s.concerns) if getattr(s, "concerns", None) else "none"
    return (
        f"{idx}. {p.company} — {p.title}  ★ {s.fit_score}/5\n"
        f"   {p.source} · {p.location or 'unspecified'} · posted {posted} · {comp}\n"
        f"   Band: {s.role_band} · Concerns: {concerns}\n"
        f"   {s.rationale}\n"
        f"   Apply: {p.url}   (db_id {db_id})\n"
    )


def _fit_block_html(idx: int, fit: Fit) -> str:
    db_id, p, s = fit
    posted = p.posted_at.date().isoformat() if getattr(p, "posted_at", None) else "unknown"
    comp = getattr(p, "salary_disclosed", None) or "not disclosed"
    concerns = "; ".join(s.concerns) if getattr(s, "concerns", None) else "none"

    def esc(x: str) -> str:
        return (
            str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    return (
        f'<div style="margin:0 0 18px 0;padding:0 0 14px 0;border-bottom:1px solid #eee;">'
        f'<div style="font-size:15px;font-weight:600;">{idx}. {esc(p.company)} — {esc(p.title)} '
        f'<span style="color:#b8860b;">★ {s.fit_score}/5</span></div>'
        f'<div style="font-size:12px;color:#666;margin:3px 0;">{esc(p.source)} · '
        f'{esc(p.location or "unspecified")} · posted {posted} · {esc(comp)}</div>'
        f'<div style="font-size:12px;color:#666;margin:3px 0;"><b>Band:</b> {esc(s.role_band)} · '
        f'<b>Concerns:</b> {esc(concerns)}</div>'
        f'<div style="font-size:13px;margin:6px 0;">{esc(s.rationale)}</div>'
        f'<div style="font-size:13px;"><a href="{esc(p.url)}">Apply</a> '
        f'<span style="color:#999;">· db_id {db_id}</span></div>'
        f'</div>'
    )


def build_digest(today_iso: str, fits: list[Fit]) -> tuple[str, str, str]:
    """Return (subject, text_body, html_body) for the given fits.

    Assumes `fits` is the already-filtered list of NEW qualifying fits.
    """
    n = len(fits)
    strong = sum(1 for (_d, _p, s) in fits if s.fit_score is not None and s.fit_score >= 4)
    plural = "fit" if n == 1 else "fits"
    if strong:
        subject = f"Job Feed — {n} new {plural} ({strong} strong) · {today_iso}"
    else:
        subject = f"Job Feed — {n} new {plural} · {today_iso}"

    text = (
        f"Job Feed — {today_iso}\n"
        f"{n} new {plural} · {strong} strong (>=4)\n\n"
        + "\n".join(_fit_line_text(i, f) for i, f in enumerate(fits, start=1))
        + "\n\nTriage in an interactive Claude session: update status <db_id> to applied | passed\n"
    )

    html = (
        f'<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;'
        f'max-width:640px;margin:0 auto;">'
        f'<h2 style="font-size:18px;margin:0 0 4px 0;">Job Feed — {today_iso}</h2>'
        f'<div style="font-size:13px;color:#666;margin:0 0 16px 0;">'
        f'{n} new {plural} · {strong} strong (≥4)</div>'
        + "".join(_fit_block_html(i, f) for i, f in enumerate(fits, start=1))
        + '<div style="font-size:12px;color:#999;margin-top:8px;">Apply same-day to the strong ones.</div>'
        f'</div>'
    )
    return subject, text, html


# ── ledger (per-day db_id dedupe so 7 morning fires don't re-send) ───────────

def load_sent_ledger(path: Path) -> set[int]:
    if not path.exists():
        return set()
    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, ValueError, OSError):
        return set()


def append_sent_ledger(path: Path, ids: list[int]) -> None:
    current = load_sent_ledger(path)
    current.update(ids)
    path.write_text(json.dumps(sorted(current)), encoding="utf-8")


# ── send ─────────────────────────────────────────────────────────────────────

def send_job_digest(
    *,
    subject: str,
    text_body: str,
    html_body: str,
    gmail_address: str | None = None,
    app_password: str | None = None,
    smtp_host: str = SMTP_HOST_DEFAULT,
    smtp_port: int = SMTP_PORT_DEFAULT,
    smtp_factory: Callable[..., smtplib.SMTP] | None = None,
) -> None:
    """Send the digest via Gmail SMTP over SSL.

    Credentials default to Keychain (`gmail_address`, `gmail_app_password`).
    `smtp_factory` is injectable for tests (defaults to smtplib.SMTP_SSL).
    Raises JobEmailError on missing creds or send failure.
    """
    addr = gmail_address or get_credential("gmail_address")
    pw = app_password or get_credential("gmail_app_password")
    if not addr or not pw:
        raise JobEmailError(
            "Missing Gmail credentials in Keychain (gmail_address / gmail_app_password)"
        )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = addr
    msg["To"] = addr  # digest to self
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    factory = smtp_factory or (lambda: smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=_TIMEOUT))
    try:
        server = factory()
        try:
            server.login(addr, pw)
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                pass
    except JobEmailError:
        raise
    except Exception as exc:  # smtplib.SMTPException, OSError, etc.
        raise JobEmailError(f"Gmail send failed: {exc}") from exc


# ── orchestrator (the single call job_feed makes) ───────────────────────────

def maybe_send_digest(
    *,
    email_cfg: dict | None,
    fits: list[Fit],
    ledger_path: Path,
    today_iso: str,
    smtp_factory: Callable[..., smtplib.SMTP] | None = None,
) -> dict:
    """Best-effort: email any new qualifying fits. Never raises into the agent.

    Returns {"sent": int, "error": str | None}. A disabled config or no new
    fits is a no-op returning {"sent": 0, "error": None}.
    """
    if not email_cfg or not email_cfg.get("enabled", False):
        return {"sent": 0, "error": None}

    min_fit_score = int(email_cfg.get("min_fit_score", 3))
    already = load_sent_ledger(ledger_path)
    new_fits = select_unsent_fits(
        fits, already_sent_ids=already, min_fit_score=min_fit_score
    )
    if not new_fits:
        return {"sent": 0, "error": None}

    subject, text_body, html_body = build_digest(today_iso, new_fits)
    try:
        send_job_digest(
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            smtp_host=email_cfg.get("smtp_host", SMTP_HOST_DEFAULT),
            smtp_port=int(email_cfg.get("smtp_port", SMTP_PORT_DEFAULT)),
            smtp_factory=smtp_factory,
        )
    except JobEmailError as exc:
        logger.error("Job-feed email digest send failed: %s", exc)
        return {"sent": 0, "error": str(exc)}

    append_sent_ledger(ledger_path, [db_id for (db_id, _p, _s) in new_fits])
    return {"sent": len(new_fits), "error": None}
