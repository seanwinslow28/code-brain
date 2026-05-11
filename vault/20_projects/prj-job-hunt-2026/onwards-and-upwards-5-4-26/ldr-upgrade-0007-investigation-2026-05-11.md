---
title: "LDR migration 0007 — root cause forensics for the 2026-05-11 upgrade failure"
date: 2026-05-11
status: investigation-complete
related:
  - "[[ldr-upgrade-attempt-2026-05-11]]"
  - "[[project_ldr_upgrade_in_flight_2026-05-11]]"
upstream_refs:
  - "PR #4000 (open, 2026-05-10) — fix(db): unblock multi-migration upgrades blocked by FK mismatch + orphan _alembic_tmp_* tables"
  - "Issue #3990 (open, 2026-05-10) — second user hitting Sean's exact bug"
  - "Issue #3817 (open, 2026-05-04) — sibling bug (orphan _alembic_tmp_journals)"
  - "PR #3708 (merged 2026-04-28) — the original migration 0007 that introduced this regression"
---

# Root cause: TL;DR

**Sean did not break anything. This is a confirmed upstream regression in
LDR 1.6.x's Alembic runner.** Issue #3990 was filed yesterday by another
user hitting the exact same error message. PR #4000 was opened yesterday
to fix it. Neither has shipped — `1.6.9` (released 2026-05-02) is the
latest version on PyPI and still has the bug.

The failure is a **schema-evaluation bug, not a data bug, not a Sean-DB
quirk**. `download_tracker.url_hash` was created without UNIQUE backing
during the v1.5.6 install. Two FK declarations (`download_attempts.url_hash`,
`download_duplicates.url_hash`) point at that non-UNIQUE column. With
`PRAGMA foreign_keys = ON` (the v1.6.x default), SQLite refuses to even
*parse* DML against either child table — the FK target is invalid.

Migration 0007 was written to fix exactly this state. Its first action is
`PRAGMA foreign_keys = OFF` before the orphan scrub. But that PRAGMA is
**silently ignored** because Alembic has already opened a transaction
(via `engine.begin()` in `alembic_runner.run_migrations`). Per
`sqlite.org/pragma.html#pragma_foreign_keys`: the pragma is a no-op
inside a pending BEGIN or SAVEPOINT. The migration's comment at lines
156-161 of `0007_backfill_missing_indexes.py` claiming "no DML has
opened the implicit transaction yet" is **wrong** — Alembic auto-began
the transaction one stack frame up. Migrations 0002-0006 issue DML
before 0007 runs, freezing FK in the connect-time `ON` state for the
rest of the upgrade chain.

The fix has to live in the runner (toggle PRAGMA on the connection
*before* `conn.begin()`), not in the migration body. PR #4000 does
exactly that.

# Evidence — forensic inspection of Sean's DB

Working copy: `/tmp/ldr_inspect.db` — byte-identical copy of the
pre-upgrade backup at
`~/Code-Brain/local-deep-research-stack/backups-pre-upgrade/ldr-data-20260511-155624/`.
Inspected via the v1.6.9-failed venv's `sqlcipher3` + `create_sqlcipher_connection`,
read-only with rollback on any DML.

| Probe | Result |
|---|---|
| `alembic_version` | `0005` — confirms post-Alembic DB. v1.6.8 BUG-3747 (pre-Alembic stamping) does not apply. |
| `download_tracker_indexes` (sqlite_schema) | **empty** |
| `PRAGMA index_list(download_tracker)` | **empty** |
| `sqlite_autoindex_download_tracker_*` | **empty** |
| `download_tracker` CREATE TABLE contains `UniqueConstraint`? | **No.** No inline UNIQUE on `url_hash`. |
| `download_attempts` FK → `download_tracker(url_hash)` | **Yes** — declared. |
| `download_duplicates` FK → `download_tracker(url_hash)` | **Yes** — declared. |
| Row counts | `download_tracker: 0`, `download_attempts: 0`, `download_duplicates: 0`. **All three tables empty.** |
| Orphan rows in `download_attempts` | `0` |
| Orphan rows in `download_duplicates` | `0` |
| Duplicate `url_hash` values in `download_tracker` | `0` |
| `PRAGMA foreign_keys` at connect | `1` (ON) |
| `PRAGMA foreign_key_check` | raises `OperationalError: foreign key mismatch - "download_attempts" referencing "download_tracker"` |
| `EXPLAIN DELETE FROM download_attempts WHERE url_hash NOT IN (SELECT url_hash FROM download_tracker)` | raises **at plan time** — `foreign key mismatch` |
| `DELETE FROM download_attempts WHERE id < 0` (matches nothing) | raises `foreign key mismatch` — FK validation fires at *parse*, not at row write |
| Same DELETE after `PRAGMA foreign_keys = OFF` set OUTSIDE any transaction | **succeeds** — proves the fix path |
| Orphan `_alembic_tmp_*` tables | **none** — the 1.6.9 transaction rolled back cleanly, no #3817-style leftover |

The "raises at plan time" / "matches nothing but still raises" rows are
the smoking gun. **There is nothing to clean up data-wise.** SQLite is
rejecting the *shape* of the statement because the FK references a
non-UNIQUE column. No DELETE against `download_attempts` or
`download_duplicates` can succeed while FK enforcement is `ON`.

# Why the schema is in this state

`encrypted_db.create_user_database()` in pre-#3708 LDR (i.e. v1.5.6 and
earlier) compiled `Base.metadata` and emitted only `CreateTable(...)`
statements — never `CreateIndex(...)`. Any model-declared index
(`index=True`, `unique=True` at column level, `Index(...)` in
`__table_args__`) was missing from the on-disk schema.

In v1.5.6, the `DownloadTracker` model declared `url_hash` with
column-level `unique=True`, which SQLAlchemy compiles to a separate
`CREATE UNIQUE INDEX` rather than an inline `UNIQUE` constraint. With
the create-tables loop skipping CreateIndex, the unique backing was
never created. The bug was harmless until v1.6.0 turned `PRAGMA
foreign_keys = ON` by default.

PR #3708 (merged 2026-04-28, shipped in 1.6.x) made two changes:

1. Rewrote the model to use `__table_args__ = (UniqueConstraint("url_hash", ...),)` — an inline `UNIQUE` lands inside `CREATE TABLE` itself, no separate index needed. New fresh DBs get correct shape.
2. Added migration `0007_backfill_missing_indexes` to repair existing pre-fix DBs.

Migration 0007 *intent* is correct. Migration 0007 *execution* is broken
because of the PRAGMA-inside-transaction issue.

# Why migration 0007's mitigation doesn't work

`alembic_runner.run_migrations` at line 349 opens the upgrade in
`with engine.begin() as conn:`. That's SQLAlchemy's "begin a transaction
on this connection" context manager.

Alembic's `env.py` then runs `with context.begin_transaction():` (a
nested SAVEPOINT) and invokes each migration's `upgrade()` in sequence.
By the time `0007.upgrade()` fires, the driver is inside a pending
transaction — explicit at the SQLAlchemy layer for 0007, and
*auto-begun by the sqlite3/sqlcipher3 driver* on first DML for migrations
0002-0006 that ran before it.

SQLite docs are explicit:
> This pragma is a no-op within a transaction; foreign key constraint
> enforcement may only be enabled or disabled when there is no pending
> BEGIN or SAVEPOINT.

So `bind.execute(text("PRAGMA foreign_keys = OFF"))` at line 162 of
`0007_backfill_missing_indexes.py` returns successfully but does
**nothing**. FK stays `ON`. The next statement —
`DELETE FROM download_attempts WHERE url_hash NOT IN (SELECT url_hash FROM download_tracker)`
— fails at parse time because SQLite checks the FK validity (target
must be UNIQUE or PRIMARY KEY) for any DML touching a table with FKs.

The migration's own comment at lines 156-161 acknowledges this risk
("PRAGMA `foreign_keys` lands here because no DML has opened the
implicit transaction yet") but is mistaken about which layer opens the
transaction. PR #4000 corrects the comment and moves the PRAGMA toggle
to `alembic_runner._disable_fk_for_migration`, invoked on the
connection *before* `conn.begin()`.

# Is this a known upstream bug or Sean-specific?

**Known upstream.** Two independent data points:

1. **Issue #3990** (filed 2026-05-10 by another user) — same error message,
   same context ("upgraded to 1.6.9 from a couple of versions before").
   Reporter runs the "slim docker version on Oracle Cloud Linux ARM."
   Sean runs native macOS. Different OS, different architecture, same bug.
2. **PR #4000** (opened 2026-05-10 by the maintainer `LearningCircuit`)
   directly attributes the bug to the `PRAGMA foreign_keys = OFF` no-op
   inside a transaction. The PR description names the failure mode verbatim:
   `foreign key mismatch — "download_attempts" referencing "download_tracker"`.

Sean's DB is in the canonical pre-fix state the migration was designed
to repair. Sean is not unusual.

# Data vs schema verdict

**Schema, not data.**

Data state:
- `download_tracker`, `download_attempts`, `download_duplicates` are all empty.
- No orphans, no duplicates, nothing to scrub.

Schema state:
- `download_tracker.url_hash` lacks UNIQUE backing → FK targets on the
  two child tables are invalid in SQLite's eyes.

Even a data-cleanup script would fail to run any DELETE on the child
tables because `foreign_keys=ON` rejects the statement at parse time.
The remediation must touch the schema (add the UNIQUE backing) before
any DML on child tables is possible — or it must disable FK enforcement
outside a transaction first.

# Smallest safe remediation (describe — do NOT execute)

There are three viable paths, listed cheapest → safest:

## Option A — Wait for PR #4000 to merge and ship in 1.6.10+

Lowest-effort, highest-confidence. The PR has tests that reproduce
Sean's exact failure (`TestUpgradeFromBuggyV16xUserDbProductionEngine`
with `isolation_level=""` and FK ON at connect). The fix is in the
runner, not the migration body, so it'll apply cleanly to Sean's DB.

Risk: PR has been open ~24 hours. No merge ETA. Could be days or weeks.
The bug also takes out other users (#3990), so there's external pressure
for a fast merge.

While waiting, v1.5.6 continues to run with the known Issue #324 race
condition. Per `feedback_routing_rule_revisit_post_ldr_upgrade.md`, the
v3.26.3 routing rule stands and Gemini DR absorbs compound queries that
would have hit the race.

## Option B — Apply a one-shot schema patch to Sean's DB, then retry 1.6.9

The patch is small: create the missing UNIQUE INDEX on
`download_tracker.url_hash` while FK enforcement is disabled outside
any transaction. After the patch, the FK targets are valid, and 0007's
broken PRAGMA toggle becomes irrelevant because:
- The orphan scrubs are no-ops (zero rows to scrub).
- The UNIQUE INDEX 0007 wants to create already exists with the same name (`uq_download_tracker_url_hash`); `if_not_exists=True` is a no-op.
- `_backfill_model_indexes` runs independently and doesn't need FK off.

Pseudocode (do **not** execute without Sean's review):

```python
# Open Sean's DB via sqlcipher3 with isolation_level="" (deferred).
# IMPORTANT: PRAGMA foreign_keys=OFF must be issued BEFORE any DML
# so SQLite accepts it (no transaction active yet).
conn = create_sqlcipher_connection(db_path, password=...,
    connect_kwargs={"isolation_level": "", "check_same_thread": False})
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = OFF")
cur.execute(
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_download_tracker_url_hash "
    "ON download_tracker(url_hash)"
)
conn.commit()
conn.close()
```

The index name `uq_download_tracker_url_hash` matches the constant
`_DOWNLOAD_TRACKER_UNIQUE_INDEX` in 0007 — `if_not_exists=True` will
skip cleanly when the migration later tries to create the same index.

**Risks:**
- The patch is operating on the *production* DB. The pre-upgrade backup
  exists, so worst case is restore-from-backup. Should be done against a
  copy first, then promoted to live only after verification.
- After the patch, 0007 is no longer the *only* repair the chain expects.
  Migrations 0002-0006 will still auto-begin a transaction before 0007,
  so 0007's PRAGMA is still a no-op — but now that target is UNIQUE,
  the DELETE statements 0007 issues will parse and execute (against zero
  rows). The bug is sidestepped, not fixed.
- This won't help other LDR users hitting #3990. Sean's fix is isolated.

## Option C — Wipe and recreate the user DB

Sledgehammer. Per the per-user-DB architecture, the auth DB
(`ldr_auth.db`) and salt files stay; only the encrypted user DB is
recreated. Login credentials persist. Research history is **lost**.

Sean's `vault/20_projects/research/` already exports completed research
to markdown, so the *outputs* survive — the loss is LDR's internal
history (in-progress runs, draft outlines, citation cache). Per the
2026-05-08 → 2026-05-11 log entries, there's nothing in flight worth
preserving against schedule pressure.

Counter-argument: this throws away one of the most useful diagnostic
artifacts (Sean's exact pre-fix DB) that could test PR #4000 against
real data once it merges. Keep the backup either way.

## Recommendation

**Option A** — wait. PR #4000 has tests that mirror Sean's production
engine setup. Merging will likely happen within days given two open
issues are blocked on it (#3990 + #3817). v1.5.6 with the 1800s timeout
is a known-survivable holding pattern; Gemini DR covers what local LDR
can't. Cost of waiting is one week of "infinite-loop topics fail at
1800s" vs zero downside.

Fall back to **Option B** only if PR #4000 stalls beyond ~2 weeks and
Sean needs the 1.6.x compound-topic headroom for active job-hunt research.
Option B is reversible (the backup is the rollback), but it touches the
production DB and adds a manual step the upstream tracker doesn't know
about.

Do **not** do Option C unless a future failure surfaces actual DB
corruption that the upstream fix can't repair.

# Other migrations — exposure assessment

**0008** (`fix_research_strategy_fk`): Drops + recreates `research_strategies`.
The pre-rebuild check is `SELECT COUNT(*) FROM research_strategies` — a
read, no FK validation. The DROP TABLE + CREATE TABLE sequence has no
FK validation either. **Not exposed.**

**0009** (`default_fetch_mode_summary`): Pure `UPDATE settings SET ...`.
`settings` has no FK declarations involved. **Not exposed.**

But: since 0007 is the chain head, 0008 and 0009 never run on Sean's DB
while 0007 fails. Once the runner fix (PR #4000 or Option B's schema
patch) unblocks 0007, the rest of the chain runs unhindered.

Migrations later than 0009 don't exist yet (1.6.9 is head of the
released chain). Any future migration that does DML on a child of
`download_tracker.url_hash` before the schema patch lands would hit the
same wall — but that's hypothetical and irrelevant to the current
upgrade attempt.

# Recommended re-attempt strategy

1. **Subscribe to PR #4000** (`gh pr view 4000 --repo LearningCircuit/local-deep-research --web` and click Subscribe).
2. **Hold on v1.5.6 + 1800s timeout** until the PR merges and a release ships.
3. **When 1.6.10+ drops**, follow the existing plan at
   `/Users/seanwinslow/.claude/plans/you-are-picking-up-fuzzy-candle.md`
   with two corrections folded in from `ldr-upgrade-attempt-2026-05-11.md`:
   - Unload **both** launchd jobs (`com.sean.service.ldr-web` AND
     `com.sean.agent.deep-researcher`) before venv mutation.
   - Don't bother killing `ldr-web` by PID until after `launchctl unload -w` (`KeepAlive=true` respawns within `ThrottleInterval`).
4. **Smoke-test the upgraded install** by logging in (the failure mode
   is at *login*, not boot — refer to the v1.6.x app process and try to
   reach `/auth/login` then submit credentials).
5. If smoke passes, run the canonical configure_ldr.py dry-run, then
   live run, then the §5 smoke-test suite from the original plan.

If holding on 1.5.6 becomes painful before PR #4000 ships, **Option B**
(one-shot schema patch) is the escape hatch. The patch needs about 10
lines of Python and should be done against `/tmp/ldr_patch.db` first
(a copy), verified via `foreign_key_check`, then swapped in for the
live DB while LDR is stopped.

# Routing rule status — unchanged

Per `feedback_routing_rule_revisit_post_ldr_upgrade.md` and the
2026-05-11 attempt note: v3.26.3 stands. Both halves of the rule still
apply (Issue #324 race lives on v1.5.6; Qwen3-14B multi-target citation
limit is independent of LDR version). No re-test possible, no
relaxation appropriate, until the upgrade actually lands.

# Files referenced (read-only)

- `~/Code-Brain/local-deep-research-stack/.venv-1.6.9-failed/lib/python3.13/site-packages/local_deep_research/database/migrations/versions/0007_backfill_missing_indexes.py` — the broken migration
- `…/database/migrations/versions/{0008_fix_research_strategy_fk,0009_default_fetch_mode_summary}.py` — confirmed not exposed
- `…/database/alembic_runner.py` lines 226-387 — `run_migrations` with the transactional `engine.begin()` block
- `…/database/migrations/env.py` lines 28-51 — `run_migrations_online` with `context.begin_transaction()`
- `…/database/encrypted_db.py` lines 333-499 — `create_user_database` (the create-tables loop that historically skipped CreateIndex)
- `…/database/models/download_tracker.py` — model definitions for the three tables
- `~/Code-Brain/local-deep-research-stack/logs/ldr-web-stderr.log` lines 2333-2444 — full traceback of the live failure
- `~/Code-Brain/local-deep-research-stack/backups-pre-upgrade/ldr-data-20260511-155624/` — pre-upgrade DB backup (do not delete for at least 48h)
- `/tmp/ldr_inspect.py`, `/tmp/ldr_inspect.db`, `/tmp/ldr_inspect.db.salt` — the forensic harness used to generate the evidence table above; safe to discard

# Cleanup

- The `.venv-1.6.9-failed/` directory at `~/Code-Brain/local-deep-research-stack/` can be deleted **once PR #4000 merges and we no longer need 1.6.9 source for cross-referencing**. ~1.6 GB.
- The pre-upgrade backup at `…/backups-pre-upgrade/ldr-data-20260511-155624/` should be retained until the next upgrade attempt succeeds — it's the canonical rollback point for both venv-only and DB-level recovery.
- `/tmp/ldr_inspect.{py,db,db.salt}` can be discarded now; the report above captures everything they showed.
