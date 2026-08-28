#!/usr/bin/env python3
"""Internal-sweep harvester for the Content Oracle (stage 0 of the content machine).

Stdlib only. No model. $0. It gathers; it does not judge.

The split is the same one the origin gate uses: a mechanical layer collects what
is verifiably there, and the reading layer -- the model, in session -- decides what
any of it means. A harvester that scored spikes would be inventing stories from
metadata, which is the exact failure the machine exists to prevent.

Every item carries an EVIDENCE pointer (sha, file, date, issue number). The Oracle
skill may not emit a card without one.

    python3 sweep.py --days 7
    python3 sweep.py --days 7 --out <git-ignored path>

Privacy: this reads git-ignored private material (dailies, partner-session
sidecars). --out refuses any path git does not ignore.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SIDECARS = Path.home() / ".creative-harness" / "partner-sessions"

# Commit subjects that are pure bookkeeping. They are real work, but there is no
# story under them, and they would otherwise flood the digest.
NOISE_SUBJECT = re.compile(
    r"^(chore\(tickets\)|chore\(daily\)|Merge |Revert |bump |wip\b)", re.I
)


def _run(cmd: list[str], cwd: Path | None = None) -> str:
    """Run a command, returning stdout. Empty string on any failure."""
    try:
        out = subprocess.run(
            cmd, cwd=cwd or REPO, capture_output=True, text=True, timeout=30
        )
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


# ── sources ──────────────────────────────────────────────────────────────────

def sweep_git(days: int) -> list[dict]:
    """Commits in the window, noise subjects dropped, body kept when present."""
    raw = _run([
        "git", "log", f"--since={days} days ago",
        "--pretty=format:%H%x1f%ad%x1f%s%x1f%b%x1e", "--date=short",
    ])
    items = []
    for record in raw.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 3:
            continue
        sha, when, subject = parts[0], parts[1], parts[2]
        body = parts[3].strip() if len(parts) > 3 else ""
        if NOISE_SUBJECT.match(subject):
            continue
        items.append({
            "source": "git",
            "evidence": sha[:9],
            "date": when,
            "title": subject,
            "detail": body,
        })
    return items


def sweep_dailies(days: int) -> list[dict]:
    """Daily notes in the window. Git-ignored; never quoted into a tracked file."""
    root = REPO / "vault" / "daily"
    if not root.is_dir():
        return []
    cutoff = date.today() - timedelta(days=days)
    items = []
    for path in sorted(root.glob("20*.md")):
        try:
            when = datetime.strptime(path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if when < cutoff:
            continue
        items.append({
            "source": "daily",
            "evidence": f"vault/daily/{path.name}",
            "date": when.isoformat(),
            "title": f"daily note {when.isoformat()}",
            "detail": path.read_text(encoding="utf-8", errors="replace"),
        })
    return items


def sweep_sidecars(days: int) -> list[dict]:
    """Creative-partner session sidecars touched in the window. Local-only."""
    if not SIDECARS.is_dir():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    items = []
    for path in sorted(SIDECARS.glob("*.md")):
        stat = path.stat()
        touched = datetime.fromtimestamp(stat.st_mtime)
        if touched < cutoff:
            continue
        items.append({
            "source": "sidecar",
            "evidence": f"~/.creative-harness/partner-sessions/{path.name}",
            "date": touched.date().isoformat(),
            "title": path.stem,
            "detail": path.read_text(encoding="utf-8", errors="replace"),
        })
    return items


def sweep_issues(days: int) -> list[dict]:
    """Issues closed in the window, via gh. Best-effort: no gh, no items.

    Wayfinder resolution comments are the densest story source in the repo --
    they are where a decision's real cost is written down.
    """
    since = (date.today() - timedelta(days=days)).isoformat()
    raw = _run([
        "gh", "issue", "list", "--state", "closed", "--limit", "40",
        "--search", f"closed:>={since}",
        "--json", "number,title,closedAt,labels",
    ])
    if not raw.strip():
        return []
    try:
        rows = json.loads(raw)
    except json.JSONDecodeError:
        return []
    items = []
    for row in rows:
        items.append({
            "source": "issue",
            "evidence": f"#{row['number']}",
            "date": (row.get("closedAt") or "")[:10],
            "title": row.get("title", ""),
            "detail": " ".join(l["name"] for l in row.get("labels", [])),
        })
    return items


def sweep_fleet(days: int) -> list[dict]:
    """Nightly fleet manifests in the window -- where the agents failed honestly."""
    root = REPO / "vault" / "health"
    if not root.is_dir():
        return []
    cutoff = date.today() - timedelta(days=days)
    items = []
    for path in sorted(root.glob("*.json")):
        found = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
        if not found:
            continue
        try:
            when = datetime.strptime(found.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        if when < cutoff:
            continue
        items.append({
            "source": "fleet",
            "evidence": f"vault/health/{path.name}",
            "date": when.isoformat(),
            "title": path.stem,
            "detail": path.read_text(encoding="utf-8", errors="replace")[:2000],
        })
    return items


def sweep_tickets() -> list[dict]:
    """Open manual tickets. Not windowed -- an old ticket still nags."""
    path = REPO / "vault" / "00_inbox" / "tickets.md"
    if not path.is_file():
        return []
    return [{
        "source": "tickets",
        "evidence": "vault/00_inbox/tickets.md",
        "date": date.today().isoformat(),
        "title": "open manual tickets",
        "detail": path.read_text(encoding="utf-8", errors="replace"),
    }]


SOURCES = {
    "git": lambda d: sweep_git(d),
    "issue": lambda d: sweep_issues(d),
    "daily": lambda d: sweep_dailies(d),
    "sidecar": lambda d: sweep_sidecars(d),
    "fleet": lambda d: sweep_fleet(d),
    "tickets": lambda d: sweep_tickets(),
}


# ── rendering ────────────────────────────────────────────────────────────────

def demote_headings(text: str) -> str:
    """Turn embedded ATX headings into bold lines.

    A daily note's own `## Sessions` would otherwise collide with the digest's
    section structure and the reader could not tell whose heading it is.
    """
    return re.sub(
        r"^(#{1,6})\s+(.*)$",
        lambda m: f"**{m.group(2).strip()}**",
        text,
        flags=re.M,
    )


def render(items: list[dict], days: int, truncate: int) -> str:
    lines = [
        f"# Oracle internal sweep — {date.today().isoformat()} — last {days} days",
        "",
        "Raw material, unscored. Every card the Oracle emits must point at one of",
        "these EVIDENCE values. A spike with no evidence pointer is an invention.",
        "",
        "**Private.** Dailies and sidecars are git-ignored. Nothing below is ever",
        "pasted into a tracked file, an issue, or a commit message.",
        "",
    ]
    for name in SOURCES:
        group = [i for i in items if i["source"] == name]
        if not group:
            lines += [f"## {name} — nothing in window", ""]
            continue
        lines += [f"## {name} — {len(group)} item(s)", ""]
        for item in group:
            lines.append(f"### [{item['evidence']}] {item['date']} — {item['title']}")
            detail = demote_headings((item["detail"] or "").strip())
            if detail:
                if truncate and len(detail) > truncate:
                    detail = detail[:truncate] + f"\n…[truncated at {truncate} chars]"
                lines += ["", detail, ""]
            else:
                lines.append("")
    return "\n".join(lines) + "\n"


def is_ignored(path: Path) -> bool:
    try:
        done = subprocess.run(
            ["git", "check-ignore", "-q", str(path)],
            cwd=REPO, capture_output=True, timeout=10,
        )
        return done.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="sweep window (default 7)")
    ap.add_argument("--out", type=Path, help="write here (must be git-ignored)")
    ap.add_argument(
        "--only", action="append", choices=sorted(SOURCES),
        help="restrict to these sources (repeatable)",
    )
    ap.add_argument(
        "--truncate", type=int, default=4000,
        help="max chars per item detail, 0 for no limit (default 4000)",
    )
    args = ap.parse_args()

    wanted = args.only or list(SOURCES)
    items: list[dict] = []
    for name in wanted:
        items.extend(SOURCES[name](args.days))

    text = render(items, args.days, args.truncate)

    if args.out:
        if not is_ignored(args.out):
            print(
                f"refusing to write {args.out}: git does not ignore it, and the "
                "sweep carries private material (CLAUDE.md rule 9).",
                file=sys.stderr,
            )
            return 2
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"{len(items)} item(s) → {args.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
