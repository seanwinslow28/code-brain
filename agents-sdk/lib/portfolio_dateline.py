"""Render the portfolio's daily-dated JSON layer from real fleet data.

The sw-ai-pm-portfolio hero dateline, About-teaser pulse strip,
"next piece" card, and shipped case-study stats read four static files
under the portfolio's ``public/api/``:

    - dateline.json            (hero: voiced wire-service fleet pulse)
    - about-pulse.json         (About-teaser: last-24h making-activity items)
    - next-piece.json          (next-in-production card)
    - shipped-stats-<slug>.json (live npm/GitHub stats per shipped case study)

This module is the bridge between the fleet's real output and those
files. The dateline + about-pulse are rendered from the SAME structured
sources the Fleet Overnight Digest reads (``agent-run-history.csv`` + the
latest synth manifest) plus a measured code-brain commit count. The
next-piece is editorial — read verbatim from the ``[portfolio.next_piece]``
config block (the bridge only stamps ``updated_at``). The shipped-stats
are fetched live from public npm + GitHub APIs per slug declared in
``[portfolio.shipped_stats]``.

Deterministic on purpose: the dateline body is terse wire-service
stat-speak ("indexer wrote 139 chunks at 02:00."), not creative prose, so
templating reproduces the established voice exactly and never hallucinates
a number. The Daily Driver calls run_publish() at the end of its morning
run; see daily_driver.py.

The renderer NEVER fabricates: a missing agent row is reported honestly,
a missing manifest omits the synth clause rather than guessing, and a
shipped-stats fetch that fails (404 / network / missing field) returns
None so the caller SKIPS writing that file — the hand-curated file is left
to age to a muted "LATEST" badge rather than being zeroed.

Before any commit/push, run_publish() runs the portfolio's own
``npm run validate`` against the worktree and refuses to push if it fails,
so the fleet never ships JSON the Vercel build would reject.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
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


def _now_iso() -> str:
    """Local (ET on Sean's machines) ISO 8601 timestamp, second precision."""
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def _count_commits(repo_root: Path, *, hours: int = 24) -> int:
    """Count real code-brain commits in the last `hours`, excluding the
    Obsidian-Git vault auto-commits (message shape ``vault: auto-commit ...``).

    Honest by construction: vault auto-commits are machine noise, not making.
    Never raises — a git failure yields 0 so the morning run is unaffected.
    """
    res = _git(["log", f"--since={hours} hours ago", "--pretty=%s"], repo_root)
    if res.returncode != 0:
        return 0
    subjects = [s for s in res.stdout.splitlines() if s.strip()]
    return sum(1 for s in subjects if not s.startswith("vault: auto-commit"))


def _fetch_json(url: str, *, timeout: int = 10) -> dict | None:
    """GET a JSON document. Returns None on any non-200 / network / parse error
    so callers can skip honestly rather than fabricate. Never raises."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "code-brain-fleet/1.0", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 — fixed https hosts
            if resp.status != 200:
                return None
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return None


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
        "updated_at": _now_iso(),
    }


def render_about_pulse(
    repo_root: Path, vault_root: Path | None = None, today: date | None = None
) -> dict:
    """Render about-pulse.json items from verifiable last-24h fleet facts.

    Only emits items it can verify: real code-brain commits (excluding vault
    auto-commits), fleet runs (distinct fleet agents that ran), and whether
    today's daily note was written. Stays a pure function of measured state —
    no fabricated draft/cel counts. The home teaser shows the first 3 items,
    so the order is commits → fleet_runs → daily note.
    """
    today = today or date.today()
    vault_root = vault_root or (repo_root / "vault")
    runs = _read_recent_runs(repo_root)

    items: list[dict] = []

    commits = _count_commits(repo_root)
    items.append({"type": "commits", "count": commits, "label": _plural(commits, "commit")})

    fleet_keys = ("vault-indexer", "vault-synthesizer", "vault-critic")
    ran = [k for k in fleet_keys if runs.get(k) and (runs[k].get("status") or "") == "success"]
    short = " · ".join(k.split("-", 1)[1] for k in ran)  # indexer · synthesizer · critic
    if ran:
        items.append({"type": "fleet_runs", "count": len(ran), "label": f"{len(ran)} fleet runs ({short})"})

    daily_note = vault_root / "10_timeline" / "daily" / f"{today.isoformat()}.md"
    if daily_note.exists():
        items.append({"type": "reading", "count": 1, "label": "1 daily note"})

    return {
        "date_iso": today.isoformat(),
        "items": items,
        "updated_at": _now_iso(),
    }


def render_next_piece(spec: dict | None) -> dict | None:
    """Render next-piece.json from the editorial ``[portfolio.next_piece]`` block.

    "What ships next" is not derivable from fleet data, so the bridge reads the
    title + date_target verbatim from config and only stamps updated_at. Returns
    None when the block (or a required field) is absent, so a hand-curated file
    is never overwritten with empty data.
    """
    if not spec:
        return None
    title = spec.get("title")
    date_target = spec.get("date_target")
    if not title or not date_target:
        return None
    return {
        "title": str(title),
        "date_target": str(date_target),
        "updated_at": _now_iso(),
    }


def render_shipped_stats(slug: str, spec: dict | None) -> dict | None:
    """Render shipped-stats-<slug>.json from LIVE npm + GitHub public APIs.

    spec = {"npm_package": "...", "github_repo": "owner/name"}. Emits only what
    is API-measurable — weekly npm downloads and GitHub stars; the prior
    "verified installs (MCP registry)" row is intentionally dropped (no public
    API). Returns None on any missing identifier or fetch failure so the caller
    SKIPS writing the file (the hand-curated one ages to a muted "LATEST" badge
    rather than being zeroed). NEVER fabricates.
    """
    npm_pkg = (spec or {}).get("npm_package")
    gh_repo = (spec or {}).get("github_repo")
    if not npm_pkg or not gh_repo:
        return None

    dl = _fetch_json(f"https://api.npmjs.org/downloads/point/last-week/{npm_pkg}")
    gh = _fetch_json(f"https://api.github.com/repos/{gh_repo}")
    if not dl or not gh:
        return None

    downloads = dl.get("downloads")
    stars = gh.get("stargazers_count")
    if downloads is None or stars is None:
        return None

    return {
        "slug": slug,
        "updated_at": _now_iso(),
        "items": [
            {"label": "weekly downloads", "value": str(downloads), "unit": "npm"},
            {"label": "stars", "value": str(stars), "unit": "GitHub"},
        ],
    }


def publish(
    repo_root: Path,
    portfolio_api_dir: Path,
    *,
    vault_root: Path | None = None,
    dry_run: bool = True,
    next_piece_spec: dict | None = None,
    shipped_stats_specs: dict | None = None,
) -> dict[str, dict]:
    """Render the JSONs and (unless dry_run) write them to the portfolio.

    Always renders dateline.json + about-pulse.json. Additionally renders
    next-piece.json when a ``next_piece_spec`` is supplied, and one
    shipped-stats-<slug>.json per entry in ``shipped_stats_specs`` whose live
    fetch succeeds (failed/missing fetches are silently skipped — never zeroed).

    Returns the rendered dicts keyed by filename so the caller can log or test
    them. Writing is the only side effect; committing/pushing the portfolio repo
    is the caller's responsibility (kept separate so the consequential git step
    is explicit and easy to gate).
    """
    rendered: dict[str, dict] = {
        "dateline.json": render_dateline(repo_root, vault_root),
        "about-pulse.json": render_about_pulse(repo_root, vault_root),
    }

    next_piece = render_next_piece(next_piece_spec)
    if next_piece is not None:
        rendered["next-piece.json"] = next_piece

    for slug, spec in (shipped_stats_specs or {}).items():
        stats = render_shipped_stats(slug, spec)
        if stats is not None:
            rendered[f"shipped-stats-{slug}.json"] = stats

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
        commit = _git(["commit", "-m", f"chore(daily): fleet refresh {today.isoformat()}"], worktree)
        if commit.returncode != 0:
            return f"commit failed: {commit.stderr.strip()[:160]}"
        if not do_push:
            return "committed (push disabled — auto_push=false)"
        # Sync to the latest origin/main, then push the commit we just made.
        # GitHub PR merges advance origin/main between runs, so rebase our
        # commit onto it to avoid a non-fast-forward. Push HEAD explicitly —
        # NOT the local `main` ref: the rebase detaches HEAD, and pushing the
        # stale local `main` (left behind origin once PRs merge) is a
        # guaranteed non-fast-forward. That ref mismatch was the long-standing
        # cause of the silent morning "PUSH FAILED" — the good commit stranded
        # on a detached HEAD while the diverged branch ref was rejected.
        rebase = _git(["pull", "--rebase", "--autostash", "origin", "main"], worktree, timeout=90)
        if rebase.returncode != 0:
            _git(["rebase", "--abort"], worktree)
            return f"committed; REBASE-ON-ORIGIN FAILED (not pushed): {rebase.stderr.strip()[:160]}"
        push = _git(["push", "origin", "HEAD:main"], worktree, timeout=90)
        if push.returncode != 0:
            # A rejected push is a git-level failure (non-fast-forward, etc.),
            # not necessarily a credential problem — surface the real stderr.
            return f"committed; PUSH FAILED (git rejected — not a credential hang): {push.stderr.strip()[:200]}"
        # Reattach the worktree to a local `main` aligned with what we just
        # pushed, so the next run starts on a clean, fast-forwarded branch
        # instead of a detached HEAD that would strand the next commit.
        _git(["branch", "-f", "main", "HEAD"], worktree)
        _git(["checkout", "main"], worktree)
        return "committed + pushed to main"
    except subprocess.TimeoutExpired:
        return "git timed out (likely a credential prompt — push left unattended-safe)"
    except OSError as e:
        return f"git unavailable: {e}"


def _validate_portfolio(worktree: Path, *, timeout: int = 120) -> tuple[bool, str]:
    """Run the portfolio's own ``npm run validate`` (the prebuild content +
    dateline/about-pulse freshness guardrails) against the worktree.

    Returns (ok, tail) where tail is the last chunk of combined output on
    failure. Pure node builtins — no node_modules needed. Never raises: a
    timeout or missing npm yields (False, reason) so the caller refuses to push
    rather than shipping unvalidated JSON or hanging the unattended run.
    """
    try:
        proc = subprocess.run(
            ["npm", "run", "validate"],
            cwd=str(worktree),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"npm run validate timed out after {timeout}s"
    except OSError as e:
        return False, f"npm run validate could not start: {e}"
    if proc.returncode == 0:
        return True, ""
    tail = (proc.stdout + proc.stderr).strip()
    return False, tail[-500:]


def _sync_worktree_to_origin(worktree: Path) -> tuple[bool, str]:
    """Hard-reset the bot-owned worktree to the latest ``origin/main`` on a
    clean ``main`` branch *before* rendering.

    The portfolio's ``public/api/*.json`` are bot-owned outputs. Building from
    a fresh ``origin/main`` every morning means the run always overwrites the
    latest merged state cleanly, so the post-commit push is a plain
    fast-forward — no stale/detached ref, and no rebase conflict even if a PR
    touched those files between runs. ``checkout -f`` discards any leftover
    local state (e.g. a half-written file from a crashed run) and reattaches
    ``main`` if a prior run left HEAD detached.

    Best-effort and non-fatal: on any failure (offline, no remote, not a git
    dir) the caller proceeds and ``commit_and_push``'s post-commit rebase still
    guards against a remote-ahead reject. Returns (ok, reason)."""
    fetch = _git(["fetch", "origin", "main"], worktree, timeout=90)
    if fetch.returncode != 0:
        return False, f"fetch failed: {fetch.stderr.strip()[:160]}"
    checkout = _git(["checkout", "-f", "-B", "main", "origin/main"], worktree)
    if checkout.returncode != 0:
        return False, f"checkout failed: {checkout.stderr.strip()[:160]}"
    return True, ""


def run_publish(config, *, logger=None) -> str:
    """Daily-Driver morning post-step: render + write + validate + commit/push.

    Reads the [portfolio] config block. Self-activating: no-ops with a logged
    note when disabled or when the worktree hasn't been created yet, so wiring
    this in is safe before the worktree exists. Renders all four file types,
    then runs ``npm run validate`` and refuses to commit/push if it fails (the
    honesty + don't-break-the-build gate). Returns a status string.
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

    # Start from the latest origin/main so we always render over the newest
    # merged state on a clean, non-detached `main` (best-effort — see helper).
    synced, sync_err = _sync_worktree_to_origin(worktree)
    if synced:
        _log("worktree synced to origin/main")
    else:
        _log(f"worktree sync skipped ({sync_err}); proceeding — push step still rebases")

    api_dir = worktree / pcfg.get("api_subpath", "public/api")
    rendered = publish(
        Path(config.repo_root),
        api_dir,
        vault_root=Path(config.vault_root),
        dry_run=False,
        next_piece_spec=pcfg.get("next_piece"),
        shipped_stats_specs=pcfg.get("shipped_stats"),
    )
    _log(f"wrote {', '.join(rendered)} -> {api_dir}")
    _log(f"dateline: {rendered['dateline.json']['body']}")

    # Validation gate — never push JSON the portfolio's Vercel build would reject.
    ok, tail = _validate_portfolio(worktree)
    if not ok:
        _log(f"npm run validate FAILED — not pushing. tail: {tail}")
        return "validation-failed (not pushed)"
    _log("npm run validate passed")

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
    pcfg = getattr(config, "portfolio", {}) or {}
    api_dir = Path(args.portfolio_api_dir) if args.portfolio_api_dir else Path("/tmp/portfolio-api")
    rendered = publish(
        Path(config.repo_root),
        api_dir,
        vault_root=Path(config.vault_root),
        dry_run=args.dry_run,
        next_piece_spec=pcfg.get("next_piece"),
        shipped_stats_specs=pcfg.get("shipped_stats"),
    )
    print(json.dumps(rendered, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _main()
