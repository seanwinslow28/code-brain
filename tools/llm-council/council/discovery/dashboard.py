# council/discovery/dashboard.py
"""D3 — discovery dashboard: readers + aggregations + CLI over run history.

Reads session JSONs (written by pipeline.py) and council-spend ledgers, renders one
self-contained HTML artifact (see dashboard_render.py). $0: local files only.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

# Session id "YYYYMMDD-HHMMSS-hex" → "YYYY-MM-DD".
_ID_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})-")


def _session_date(session_id: str) -> str:
    m = _ID_DATE.match(str(session_id or ""))
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def _classify(payload: dict) -> str | None:
    """A session record is one of success/failure/empty; anything else (e.g. the pm3-t0
    evidence-bundle capture) is foreign — skipped honestly, never guessed at."""
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
        return None
    if payload.get("failed_stage"):
        return "failure"
    if payload.get("empty"):
        return "empty"
    if "verified" in payload:
        return "success"
    return None


def load_sessions(sessions_dir: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    """Parse every *.json in sessions_dir → (sessions, skipped). Each session gains
    _file/_kind/_date. Tolerant by design: malformed or foreign files are skipped and
    reported, never fatal."""
    sessions: list[dict] = []
    skipped: list[tuple[str, str]] = []
    if not sessions_dir.is_dir():
        return sessions, skipped
    for path in sorted(sessions_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as e:
            skipped.append((path.name, f"malformed JSON ({e.__class__.__name__})"))
            continue
        kind = _classify(payload)
        if kind is None:
            skipped.append((path.name, "foreign shape (not a session record)"))
            continue
        payload["_file"] = path.name
        payload["_kind"] = kind
        payload["_date"] = _session_date(payload.get("id", ""))
        sessions.append(payload)
    sessions.sort(key=lambda s: s.get("id", ""))
    return sessions, skipped


@dataclass
class SpendDay:
    date: str
    discovery_total: float
    runs: list[dict]


def load_spend(spend_dir: Path) -> tuple[list[SpendDay], list[tuple[str, str]]]:
    """Parse council-spend-*.json → (days, skipped), keeping only tool=="discovery" runs
    so council spend never pollutes discovery totals."""
    days: list[SpendDay] = []
    skipped: list[tuple[str, str]] = []
    if not spend_dir.is_dir():
        return days, skipped
    for path in sorted(spend_dir.glob("council-spend-*.json")):
        try:
            payload = json.loads(path.read_text())
            if not isinstance(payload, dict):
                skipped.append((path.name, "malformed ledger (not an object)"))
                continue
            runs = [r for r in payload.get("runs", []) if r.get("tool") == "discovery"]
            days.append(SpendDay(date=payload["date"],
                                 discovery_total=round(sum((r.get("amount", 0.0) for r in runs), 0.0), 4),
                                 runs=runs))
        except (json.JSONDecodeError, OSError, KeyError, TypeError) as e:
            skipped.append((path.name, f"malformed ledger ({e.__class__.__name__})"))
    days.sort(key=lambda d: d.date)
    return days, skipped
