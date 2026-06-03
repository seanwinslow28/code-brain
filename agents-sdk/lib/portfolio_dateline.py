"""Render the portfolio's daily-dated JSON layer from real fleet data.

The sw-ai-pm-portfolio hero dateline, About-teaser pulse strip, and
"next piece" card read three static files under the portfolio's
``public/api/``:

    - dateline.json     (hero: voiced wire-service fleet pulse)
    - about-pulse.json  (About-teaser: last-24h making-activity items)
    - next-piece.json   (next-in-production card)

Until now nothing bridged the fleet's real output into those files, so
they went stale and the build's freshness validator flagged them every
morning even though the Daily Driver ran clean. This module is the
bridge: it reads the SAME structured sources the Fleet Overnight Digest
reads (``agent-run-history.csv`` + the latest synth manifest) and renders
the portfolio JSONs deterministically.

Deterministic on purpose: the dateline body is terse wire-service
stat-speak ("indexer wrote 139 chunks at 02:00."), not creative prose, so
templating reproduces the established voice exactly and never hallucinates
a number. The Daily Driver calls publish() at the end of its morning run;
see daily_driver.py.

The renderer NEVER fabricates: a missing agent row is reported honestly
("no run") and a missing manifest omits the synth clause rather than
guessing.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

from .fleet_summary import _read_recent_runs
from .lint_report import latest_synth_manifest

# Agents whose overnight runs feed the hero dateline body, in narration order.
_DATELINE_AGENTS = ("vault-indexer", "vault-synthesizer", "vault-critic")


def _hhmm(time_str: str) -> str:
    """'02:00:13' -> '02:00'. Returns the input unchanged if unparseable."""
    m = re.match(r"^(\d{2}:\d{2})", (time_str or "").strip())
    return m.group(1) if m else (time_str or "").strip()


def _note_field(notes: str, key: str) -> str | None:
    """Pull `key=value` out of a CSV notes cell. Tolerates ', ' or ' ' joins."""
    m = re.search(rf"{re.escape(key)}=([^,\s]+)", notes or "")
    return m.group(1) if m else None


def _plural(n: int, singular: str) -> str:
    return f"{n} {singular}" if n == 1 else f"{n} {singular}s"


def render_dateline(
    repo_root: Path, vault_root: Path | None = None, today: date | None = None
) -> dict:
    """Render dateline.json from the last 24h of fleet runs + synth manifest.

    `vault_root` is where the synth manifest lives (``<vault>/health/``);
    it defaults to ``repo_root/vault`` to match the repo's layout. Mirrors
    the established body voice:
      "morning fleet ran clean. indexer wrote 139 chunks at 02:00.
       synth landed 2 concepts + 1 connection. critic flagged partial.
       fleet green."
    """
    today = today or date.today()
    vault_root = vault_root or (repo_root / "vault")
    runs = _read_recent_runs(repo_root)

    # Read the latest synth manifest once (authoritative for synth numbers
    # and the synth's internal status).
    manifest: dict = {}
    manifest_path = latest_synth_manifest(vault_root)
    if manifest_path:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            manifest = {}

    clauses: list[str] = []
    all_ran = all(runs.get(a) for a in _DATELINE_AGENTS)
    no_errors = all_ran and all(
        (runs[a].get("status") or "").strip() == "success" for a in _DATELINE_AGENTS
    )

    # "ran clean / fleet green" is reserved for a fully clean night: every
    # run succeeded structurally AND no agent reported an internal `partial`
    # verdict. The dateline must not claim green when the critic flagged
    # partial — the honesty of the strip is the load-bearing part.
    crit_run = runs.get("vault-critic")
    crit_internal = _note_field(crit_run.get("notes", ""), "status") if crit_run else None
    synth_internal = manifest.get("status")
    fully_clean = no_errors and crit_internal != "partial" and synth_internal != "partial"

    # Indexer
    idx = runs.get("vault-indexer")
    if idx:
        chunks = _note_field(idx.get("notes", ""), "chunks")
        if chunks:
            clauses.append(f"indexer wrote {chunks} chunks at {_hhmm(idx.get('time', ''))}.")

    # Synthesizer — prefer the manifest (authoritative) over the CSV note.
    concepts = connections = None
    if manifest:
        try:
            concepts = int(manifest.get("concepts_written", 0))
            connections = int(manifest.get("connections_written", 0))
        except (ValueError, TypeError):
            concepts = connections = None
    if concepts is None and runs.get("vault-synthesizer"):
        sn = runs["vault-synthesizer"].get("notes", "")
        c, k = _note_field(sn, "concepts"), _note_field(sn, "connections")
        concepts = int(c) if c and c.isdigit() else None
        connections = int(k) if k and k.isdigit() else None
    if concepts is not None and connections is not None:
        clauses.append(f"synth landed {_plural(concepts, 'concept')} + {_plural(connections, 'connection')}.")

    # Critic — surface its internal verdict honestly (success-empty / partial).
    crit = runs.get("vault-critic")
    if crit:
        cstatus = _note_field(crit.get("notes", ""), "status") or "ran"
        articles = _note_field(crit.get("notes", ""), "articles")
        if cstatus == "partial":
            clauses.append("critic flagged partial.")
        elif articles == "0":
            clauses.append("critic returned success-empty.")
        else:
            clauses.append(f"critic returned {cstatus}.")

    opener = "morning fleet ran clean." if fully_clean else "morning fleet logged in."
    verdict = "fleet green." if fully_clean else "fleet up."
    body = " ".join([opener, *clauses, verdict])

    return {
        "date_iso": today.isoformat(),
        "date_display": f"BOSTON, {today.strftime('%B %-d, %Y').upper()}",
        "pattern": "fleet_pulse",
        "body": body,
        "updated_at": datetime.now().astimezone().replace(microsecond=0).isoformat(),
    }


def render_about_pulse(
    repo_root: Path, vault_root: Path | None = None, today: date | None = None
) -> dict:
    """Render about-pulse.json items from verifiable last-24h fleet facts.

    Only emits items it can verify: fleet runs (distinct fleet agents that
    ran), and whether today's daily note was written. Stays a pure function
    of fleet state — no fabricated commit/draft counts.
    """
    today = today or date.today()
    vault_root = vault_root or (repo_root / "vault")
    runs = _read_recent_runs(repo_root)

    fleet_keys = ("vault-indexer", "vault-synthesizer", "vault-critic")
    ran = [k for k in fleet_keys if runs.get(k) and (runs[k].get("status") or "") == "success"]
    short = " · ".join(k.split("-", 1)[1] for k in ran)  # indexer · synthesizer · critic
    items: list[dict] = []
    if ran:
        items.append({"type": "fleet_runs", "count": len(ran), "label": f"{len(ran)} fleet runs ({short})"})

    daily_note = vault_root / "10_timeline" / "daily" / f"{today.isoformat()}.md"
    if daily_note.exists():
        items.append({"type": "reading", "count": 1, "label": "1 daily note"})

    return {
        "date_iso": today.isoformat(),
        "items": items,
        "updated_at": datetime.now().astimezone().replace(microsecond=0).isoformat(),
    }


def publish(
    repo_root: Path, portfolio_api_dir: Path, *, vault_root: Path | None = None, dry_run: bool = True
) -> dict[str, dict]:
    """Render the JSONs and (unless dry_run) write them to the portfolio.

    Returns the rendered dicts keyed by filename so the caller can log or
    test them. Writing is the only side effect; committing/pushing the
    portfolio repo is the caller's responsibility (kept separate so the
    consequential git step is explicit and easy to gate).
    """
    rendered = {
        "dateline.json": render_dateline(repo_root, vault_root),
        "about-pulse.json": render_about_pulse(repo_root, vault_root),
    }
    if not dry_run:
        portfolio_api_dir.mkdir(parents=True, exist_ok=True)
        for name, data in rendered.items():
            (portfolio_api_dir / name).write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
    return rendered


def _git(args: list[str], cwd: Path, timeout: int = 60) -> subprocess.CompletedProcess:
    """Run a git command non-interactively. GIT_TERMINAL_PROMPT=0 makes a
    missing-credential push fail fast instead of hanging the unattended run."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True, text=True, timeout=timeout, env=env, check=False,
    )


def commit_and_push(
    worktree: Path, files: list[str], *, do_push: bool, today: date | None = None,
) -> str:
    """Stage `files`, commit if anything changed, optionally push origin main.

    Returns a short human-readable status. Never raises on a git failure —
    returns an error string the caller logs, honoring the Zero-Interaction
    Mandate (an unattended run must never hang or crash on a push problem).
    """
    today = today or date.today()
    try:
        _git(["add", *files], worktree)
        staged = _git(["diff", "--cached", "--quiet"], worktree)
        if staged.returncode == 0:
            return "no changes to commit"
        commit = _git(["commit", "-m", f"chore(dateline): fleet pulse {today.isoformat()}"], worktree)
        if commit.returncode != 0:
            return f"commit failed: {commit.stderr.strip()[:160]}"
        if not do_push:
            return "committed (push disabled — auto_push=false)"
        # Rebase on origin/main first so a remote-ahead state doesn't reject.
        _git(["pull", "--rebase", "--autostash", "origin", "main"], worktree, timeout=90)
        push = _git(["push", "origin", "main"], worktree, timeout=90)
        if push.returncode != 0:
            return f"committed; PUSH FAILED (check launchd credentials): {push.stderr.strip()[:160]}"
        return "committed + pushed to main"
    except subprocess.TimeoutExpired:
        return "git timed out (likely a credential prompt — push left unattended-safe)"
    except OSError as e:
        return f"git unavailable: {e}"


def run_publish(config, *, logger=None) -> str:
    """Daily-Driver morning post-step: render + write + (optionally) commit/push.

    Reads the [portfolio] config block. Self-activating: no-ops with a logged
    note when disabled or when the worktree hasn't been created yet, so wiring
    this in is safe before the worktree exists. Returns a status string.
    """
    def _log(msg: str) -> None:
        if logger:
            logger.info(f"[portfolio-dateline] {msg}")

    pcfg = getattr(config, "portfolio", {}) or {}
    if not pcfg.get("enabled", False):
        _log("disabled in config; skipping")
        return "disabled"

    worktree = Path(pcfg.get("worktree_path", ""))
    if not worktree.exists():
        _log(f"worktree not found at {worktree} (create it to activate); skipping")
        return "no-worktree"

    api_dir = worktree / pcfg.get("api_subpath", "public/api")
    rendered = publish(
        Path(config.repo_root), api_dir, vault_root=Path(config.vault_root), dry_run=False
    )
    _log(f"wrote {', '.join(rendered)} -> {api_dir}")
    _log(f"dateline: {rendered['dateline.json']['body']}")

    if pcfg.get("commit", True):
        files = [f"{pcfg.get('api_subpath', 'public/api')}/{n}" for n in rendered]
        status = commit_and_push(worktree, files, do_push=pcfg.get("auto_push", False))
        _log(status)
        return status
    return "written (commit disabled)"


def _main() -> None:
    import argparse

    from .config import load_config

    parser = argparse.ArgumentParser(description="Render the portfolio daily-dated JSON layer.")
    parser.add_argument("--dry-run", action="store_true", help="Print the JSONs without writing.")
    parser.add_argument("--portfolio-api-dir", default=None, help="Target public/api dir.")
    args = parser.parse_args()

    config = load_config()
    api_dir = Path(args.portfolio_api_dir) if args.portfolio_api_dir else Path("/tmp/portfolio-api")
    rendered = publish(
        Path(config.repo_root), api_dir, vault_root=Path(config.vault_root), dry_run=args.dry_run
    )
    print(json.dumps(rendered, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _main()
