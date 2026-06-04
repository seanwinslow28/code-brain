# Portfolio daily-dated layer — fleet refresh runbook

How the Daily Driver keeps https://seanwinslow.com's "daily-dated layer" honest and
current each morning. Owner module: [`lib/portfolio_dateline.py`](../lib/portfolio_dateline.py).
Config: the `[portfolio]` block in [`config.toml`](../config.toml).

## What it does

After the Daily Driver's 08:30 ET morning run writes the daily note, its post-step
(`run_publish`, wired non-fatally at [daily_driver.py:534-540](../agents/daily_driver.py))
renders the portfolio's four build-time JSON files from **real measured fleet activity**,
runs the portfolio's own validator, and — only if it passes — commits + pushes to the
portfolio's `main`. Vercel's GitHub integration auto-deploys the push.

## The data contract (`sw-ai-pm-portfolio/public/api/`)

The portfolio reads these at **build time** (Node `fs` / static import — never client fetch).
The displayed *date* everywhere derives from the Vercel **build date** (`src/lib/dateline.ts`);
the JSON supplies the *body/numbers*, gated by `isFresh(date_iso)` (48h window, anchored
08:30 ET). Stale JSON → the component falls back to an evergreen, undated line.

| File | Source | Renderer |
|------|--------|----------|
| `dateline.json` | `agent-run-history.csv` (last 24h) + latest synth manifest | `render_dateline` |
| `about-pulse.json` | code-brain commits (ex-`vault: auto-commit`) + fleet runs + daily note | `render_about_pulse` |
| `next-piece.json` | **editorial** — `[portfolio.next_piece]` in config.toml | `render_next_piece` |
| `shipped-stats-<slug>.json` | **live** npm weekly downloads + GitHub stars | `render_shipped_stats` |

### about-pulse metrics (what's measured)
- **commits** — real code-brain commits in the last 24h, **excluding** the Obsidian-Git
  `vault: auto-commit …` noise. Honest 0 on a quiet day.
- **fleet_runs** — distinct fleet agents (indexer/synth/critic) that succeeded.
- **reading** — whether today's daily note exists.
- Drafts and cels are **not** measured (no reliable source). They are never faked.

### next-piece (editorial)
"What ships next" isn't derivable from fleet data, so it's read verbatim from config —
the bridge only stamps `updated_at`. **Edit it when the answer changes:**
```toml
[portfolio.next_piece]
title = "Vault Scorecard"
date_target = "2026-06-10"
```

### shipped-stats (currently inactive — by design)
As of 2026-06-04, `intent-engineering-mcp` is **not** on the npm registry (404) and has no
public GitHub repo, so `[portfolio.shipped_stats]` is left **empty/commented**. The renderer
skips any slug whose live fetch fails — it never zeroes or fabricates the hand-seeded file
(which simply ages to a muted **LATEST** badge). **To activate once the product ships:**
publish the npm package, then uncomment in config.toml:
```toml
[portfolio.shipped_stats.intent-engineering-mcp]
npm_package = "intent-engineering-mcp"
github_repo = "seanwinslow28/intent-engineering-mcp"
```
It measures **weekly npm downloads** + **GitHub stars** only; the old "verified installs
(MCP registry)" row was dropped because there's no public API for it.

## The freshness gate (honesty mechanism — do not defeat)

`render_dateline`/`render_about_pulse` always write **today's** `date_iso` with the real
body/numbers for that morning. On a clean night the body reads "ran clean … fleet green";
on a partial night it honestly says "logged in … fleet up" and never claims green. Because
`date_iso` advances daily there's always a content diff → always a deploy → the build
re-stamps "today" automatically. **Never bump `date_iso` without real new data** — the
48h `isFresh` gate exists precisely to prevent stale content wearing a fresh date.

## The validation gate (don't break the build)

Before any commit/push, `run_publish` runs `npm run validate` (the portfolio's
`scripts/validate_content.mjs`) against the worktree. It needs **no `node_modules`** (pure
node builtins). If it fails, the run logs the tail and returns `"validation-failed (not
pushed)"` — **nothing is committed or pushed.** This stops the fleet from shipping JSON the
Vercel build would reject (future/≥2-day-stale dates, malformed content collections, etc.).

## Trigger choice: push-only

We rely on **`git push` → Vercel GitHub-integration auto-deploy**. No Deploy Hook secret.
Rationale: `date_iso` changes every morning, so there is always a content diff → always a
push → always a production deploy. A forced deploy hook would be redundant.

The push uses a dedicated git **worktree** pinned to `main`
(`/Users/seanwinslow/Code-Brain/.portfolio-dateline-worktree`) so bot commits never touch
whatever branch the primary portfolio clone has checked out. Commit message:
`chore(daily): fleet refresh <YYYY-MM-DD>`. Idempotent: a re-run with no content change is a
no-op (`git diff --cached --quiet` → "no changes to commit"). Pushes are unattended-safe
(`GIT_TERMINAL_PROMPT=0` → a missing credential fails fast, never hangs).

### Optional: Vercel Deploy Hook (not used — documented for completeness)
If you ever want a forced rebuild on a literal no-change day: Vercel → project
`sw-ai-pm-portfolio` → Settings → Git → Deploy Hooks → create one targeting `main` → store
the URL as a **gitignored** secret in code-brain (e.g. `.env` as
`VERCEL_PORTFOLIO_DEPLOY_HOOK` — anyone with the URL can deploy) → `curl -X POST
"$VERCEL_PORTFOLIO_DEPLOY_HOOK"`. Not wired today.

## Test it manually

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/agents-sdk

# 1. Unit tests
PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_portfolio_dateline.py -v

# 2. Inspect rendered JSON (writes to a temp dir, not the worktree)
PYTHONPATH=. .venv/bin/python3 -m lib.portfolio_dateline --portfolio-api-dir /tmp/portfolio-api
#   or --dry-run to print without writing

# 3. Full morning run (this DOES commit + push if validation passes)
PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning
git -C /Users/seanwinslow/Code-Brain/.portfolio-dateline-worktree log -1   # chore(daily): fleet refresh <today>

# 3b. Render + validate against the real worktree WITHOUT pushing, then discard:
WT=/Users/seanwinslow/Code-Brain/.portfolio-dateline-worktree
PYTHONPATH=. .venv/bin/python3 -c "from pathlib import Path; from lib.config import load_config; \
from lib.portfolio_dateline import publish, _validate_portfolio; c=load_config(); p=c.portfolio; \
wt=Path(p['worktree_path']); publish(Path(c.repo_root), wt/p['api_subpath'], vault_root=Path(c.vault_root), \
dry_run=False, next_piece_spec=p.get('next_piece'), shipped_stats_specs=p.get('shipped_stats')); \
print('validate:', _validate_portfolio(wt))"
git -C "$WT" checkout -- public/api   # discard, no commit/push
```

## Failure modes (all non-fatal to the morning run)

| Symptom | Meaning | Fix |
|---------|---------|-----|
| `disabled` | `[portfolio].enabled = false` | enable in config.toml |
| `no-worktree` | worktree dir missing | `git -C sw-ai-pm-portfolio worktree add ../.portfolio-dateline-worktree main` |
| `validation-failed (not pushed)` | `npm run validate` failed | read the logged tail; fix content/dates; nothing was pushed |
| `PUSH FAILED (check launchd credentials)` | committed locally, push rejected | check osxkeychain access from launchd |
| `no changes to commit` | re-run, identical content | expected/idempotent |
| shipped-stats file absent from output | live fetch failed or slug not configured | expected until the product is published + configured |
