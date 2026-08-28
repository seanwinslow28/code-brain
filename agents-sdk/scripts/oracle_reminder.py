#!/usr/bin/env python3
"""Weekly probation reminder for the Content Oracle (content-machine stage 0).

Deliberately the dumbest thing that works: stdlib plus Keychain, one fixed email,
no model, no SDK, no repo reads. It exists so a probation week cannot quietly get
skipped -- not to do any part of the Oracle's job.

That restraint is the point. The Oracle is on probation precisely because a
scheduled agent has to earn its schedule (L7). A reminder that swept sources or
drafted spikes would have smuggled the Oracle past its own probation, and the
reminder would have become the thing probation was meant to test.

Credentials (shared with the Job Feed digest, already in Keychain):
    gmail_address        -- sender and recipient
    gmail_app_password   -- 16-char Gmail App Password

    python3 agents-sdk/scripts/oracle_reminder.py            # send
    python3 agents-sdk/scripts/oracle_reminder.py --dry-run  # print, send nothing
"""

from __future__ import annotations

import argparse
import smtplib
import sys
from datetime import date, timedelta
from email.message import EmailMessage
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.keychain import get_credential  # noqa: E402

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
TIMEOUT = 20.0

# Ruled on ticket #169, 2026-08-26. Probation is six Sundays from here.
PROBATION_START = date(2026, 8, 30)
PROBATION_WEEKS = 6

BODY = """\
Run the Oracle.

    /content-oracle

It sweeps the last 7 days of your own systems (git, closed issues, dailies,
partner-session sidecars, fleet manifests), runs the last30days external scan,
and hands you ~10 ranked spike cards. Pick one; the rest bank to
creative-studio/content-machine/ideas-bank.md.

{probation}

A run with zero picks still counts -- record it. The graduation decision reads
the probation record, not the calendar.
"""


def probation_line(today: date) -> str:
    """One line of honest state, computed from the fixed start date.

    Arithmetic only -- no state file, no repo read. The reminder stays dumb.
    """
    if today < PROBATION_START:
        return f"Probation week 1 starts {PROBATION_START.isoformat()}."
    week = (today - PROBATION_START).days // 7 + 1
    if week > PROBATION_WEEKS:
        last = PROBATION_START + timedelta(weeks=PROBATION_WEEKS - 1)
        return (
            f"Probation is over ({PROBATION_WEEKS} weeks ended {last.isoformat()}). "
            "Decide from the run record whether the Oracle earns a schedule -- "
            "or turn this reminder off."
        )
    return f"Probation week {week} of {PROBATION_WEEKS}."


def build_message(address: str, today: date) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = f"Oracle run — {today.isoformat()} — {probation_line(today)}"
    msg["From"] = address
    msg["To"] = address
    msg.set_content(BODY.format(probation=probation_line(today)))
    return msg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print, send nothing")
    args = ap.parse_args()

    today = date.today()
    address = get_credential("gmail_address")
    password = get_credential("gmail_app_password")

    if args.dry_run:
        msg = build_message(address or "<gmail_address missing>", today)
        print(f"creds: address={'set' if address else 'MISSING'} "
              f"password={'set' if password else 'MISSING'}")
        print(f"Subject: {msg['Subject']}\n")
        print(msg.get_content())
        return 0

    if not address or not password:
        print(
            "missing Keychain credentials gmail_address / gmail_app_password. "
            "Set them with: python3 agents-sdk/lib/keychain.py set <name> <value>",
            file=sys.stderr,
        )
        return 1

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=TIMEOUT) as smtp:
            smtp.login(address, password)
            smtp.send_message(build_message(address, today))
    except Exception as exc:  # smtplib.SMTPException, OSError, ssl errors
        print(f"oracle reminder send failed: {exc}", file=sys.stderr)
        return 1

    print(f"oracle reminder sent to {address} — {probation_line(today)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
