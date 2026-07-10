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


_GATHER_OK = re.compile(r"^ok: (\d+) records \((\d+) found\)")


def collector_yield(sessions: list[dict]) -> dict[str, dict]:
    """Aggregate per-collector yield from gather_status strings. Unknown formats are kept
    verbatim as errors — never guessed into numbers."""
    out: dict[str, dict] = {}
    for s in sessions:
        for collector, status in (s.get("gather_status") or {}).items():
            slot = out.setdefault(collector, {"records": 0, "found": 0,
                                              "ok_runs": 0, "runs": 0, "errors": []})
            slot["runs"] += 1
            m = _GATHER_OK.match(str(status))
            if m:
                slot["records"] += int(m.group(1))
                slot["found"] += int(m.group(2))
                slot["ok_runs"] += 1
            else:
                slot["errors"].append(str(status))
    return out


def fuse_stats(sessions: list[dict]) -> dict:
    counts = {"success": 0, "failure": 0, "empty": 0}
    for s in sessions:
        counts[s["_kind"]] += 1
    attempts = counts["success"] + counts["failure"]
    return {**counts, "rate": (counts["success"] / attempts) if attempts else None}


def month_totals(days: list["SpendDay"]) -> dict[str, float]:
    out: dict[str, float] = {}
    for d in days:
        month = d.date[:7]
        out[month] = round(out.get(month, 0.0) + d.discovery_total, 4)
    return out


def discrepancies(sessions: list[dict], days: list["SpendDay"]) -> list[str]:
    """Session/ledger mismatches, flagged instead of papered over."""
    session_dates = {s["_date"] for s in sessions if s.get("cost_usd") and s["_date"]}
    ledger_dates = {d.date for d in days if d.discovery_total > 0}
    lines = []
    for date in sorted(session_dates - ledger_dates):
        lines.append(f"{date}: session(s) with cost recorded but no discovery spend in the ledger")
    for date in sorted(ledger_dates - session_dates):
        lines.append(f"{date}: discovery spend in the ledger but no session file (pre-fix leak?)")
    return lines


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:60].rstrip("-") or "topic"


def rerun_command(session: dict) -> str:
    """Copy-ready re-run of this topic. Pre-fix sessions lack segment — omit the flag."""
    parts = [f'uv run python -m council.discovery "{session.get("topic", "")}"',
             f"--lens {session.get('lens', 'pm')}", f"--tier {session.get('tier', 'standard')}"]
    segment = session.get("segment")
    if segment:
        parts.append(f'--segment "{segment}"')
    parts.append(f"--output vault/20_projects/research/{_slug(session.get('topic', ''))}-rerun-idea-ledger.md")
    return " ".join(parts)
