---
title: LDR 1.5.6 → 1.6.9 upgrade attempt — rollback report (2026-05-11)
date: 2026-05-11
status: rolled-back
related: project_ldr_upgrade_in_flight_2026-05-11
---

# LDR upgrade attempt (Mac Mini production) — rolled back

## Outcome

**Rolled back to v1.5.6.** Production LDR (`http://localhost:5050`) is back up and serving. Login + all 7 `configure_ldr.py` settings verified intact post-rollback. The 02:45 deep-researcher cron is re-enabled.

## What blocked the upgrade

LDR 1.6.9 Alembic migration `0007_backfill_missing_indexes` (`_scrub_orphan_children`, line 102) failed on Sean's encrypted user database with:

```
sqlcipher3.dbapi2.OperationalError:
  foreign key mismatch - "download_attempts" referencing "download_tracker"
```

LDR's auth handler caught this cleanly at login time:
> Login refused for sean: database initialisation failed (see traceback above). Lockout counter NOT incremented — credentials are valid.

The migration runs inside a transaction, so the FK-mismatch raises before any rows are written. DB byte size matches the pre-upgrade backup (5,357,568 bytes); only the file mtime was bumped by the failed transaction's page-cache touch.

## What's preserved for triage

- **`.venv-1.6.9-failed/`** at `~/Code-Brain/local-deep-research-stack/.venv-1.6.9-failed/` — the broken Python 3.13 install with LDR 1.6.9. Keep until the root cause is found, then delete. ~1.6 GB.
- **`.venv/`** is the restored v1.5.6 Python 3.11 install (was `.venv-1.5.6-rollback/`, swapped back).
- **Pre-upgrade DB backup** at `~/Code-Brain/local-deep-research-stack/backups-pre-upgrade/ldr-data-20260511-155624/` — was *not* used because the venv-only rollback was sufficient. Keep at least 48h.
- **Full stderr traceback** is in `~/Code-Brain/local-deep-research-stack/logs/ldr-web-stderr.log` (search for `_scrub_orphan_children` and `foreign key mismatch`).

## Next-step triage paths

1. **Search upstream issues** for `_scrub_orphan_children` + `download_tracker` + `foreign key mismatch`. The v1.6.8 release notes mention migration 0007 was repaired for the pre-Alembic (v1.4.0-era) case, but Sean's DB has Alembic revisions 0001-0005 already applied (confirmed in older log entries from 2026-05-05 through 2026-05-08: `Database already at revision 0005`). The 0007 failure may be a separate, post-v1.6.8 regression.
2. **Inspect the DB schema directly** from the broken venv:
   ```bash
   .venv-1.6.9-failed/bin/python3 -c "
   import sqlcipher3, os
   con = sqlcipher3.connect(os.path.expanduser('~/Library/Application Support/local-deep-research/encrypted_databases/ldr_user_2d1d92b1f4cc7fd3.db'))
   # need the per-user encryption key from Keychain to PRAGMA key=... first
   "
   ```
   The encryption key derivation lives in LDR's `database/encrypted_db.py`; the v1.5.6 install can read the same DB.
3. **Skip 1.6.9, try 1.6.0 fresh**. The race-condition fix (the actual reason for the upgrade) landed in v1.6.0. Migration 0007 is in 1.6.0 too, so this may not help — but the failure mode may surface differently against a fresher migration chain.
4. **Wipe + recreate the encrypted DB** as a last resort. Sean's research history is the loss. Per the per-user-DB architecture, the auth DB (`ldr_auth.db`) stays separate, so credentials persist.

## Routing rule status

The v3.26.3 routing rule ("heavy multi-target research → Gemini DR, not local LDR") **stands unchanged**. Both halves of the rule still apply:

- **Timeout half**: LDR is back on v1.5.6, so Issue #324 (stuck-at-90% bug) is still live. Compound prompts continue to risk 900s timeout with no output.
- **Citation-collapse half**: Independent of the LDR version — that's a Qwen3-14B model limit. The rebuild-the-model project is Sean's stated next thread.

The `feedback_routing_rule_revisit_post_ldr_upgrade.md` memory said "re-test before relaxing" — since the upgrade didn't land, no re-test is possible, no relaxation appropriate.

## Config change retained per plan §7.6

`agents-sdk/config.toml:168` was bumped from `ldr_timeout_seconds = 900` → `1800`. Reasoning per plan: a longer timeout on v1.5.6 just means Topic 1b-shaped queries fail at 1800s instead of 900s — same symptom, same diagnosis path (route to Gemini DR). Not worth a separate revert.

## Plan deltas captured for next attempt

These are corrections to `/Users/seanwinslow/.claude/plans/you-are-picking-up-fuzzy-candle.md` discovered during execution — fold in if the upgrade is re-attempted:

1. **Two launchd jobs, not one**: `com.sean.service.ldr-web` (KeepAlive=true, owns the long-running Flask) is separate from `com.sean.agent.deep-researcher` (StartCalendarInterval at 02:45). The original plan only mentioned the agent. Both must be unloaded before venv mutation; both must be reloaded after.
2. **`kill ldr-web` is futile without unloading the service** — `KeepAlive=true` respawns the binary within ~60s (ThrottleInterval).
3. **HTTPS warning in stderr** is cosmetic: `Starting server with HTTPS (self-signed certificate)` → `WARNING ... HTTPS requested but not supported directly. Use a reverse proxy for HTTPS.` Server binds plain HTTP on 5050 either way.
4. **urllib3 2.7.0 vs requests' supported-versions warning** is also cosmetic — the env-mark `requires_python <3.15,>=3.12` for LDR 1.6.9 pulls newer transitive deps than `requests==2.x` was built against. No upgrade path needed.
