# A12 build — the claim-6 drill runner, plus the schedule-truth cleanup

**Implementation pass.** This is fleet engineering on `agents-sdk/`, not a Systemcraft seat pass. The design is already ratified; you are building it, not redesigning it.

---

You are implementing ADR-12 in Sean's Code-Brain repo. Repo root: `/Users/seanwinslow/Code-Brain/code-brain`.

## Read first — these are your specification, not suggestions

1. `systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/artifacts/adr-workforce-architecture.md` — **ADR-12** (starts ~line 600). This is the authoritative design: runner, provenance guards, receipt semantics, the JSONL schema and its closed event set, the migration contract, and the fleet-report surface. Build what it says.
2. Ledger `d155`, `d156`, `d157` in the same engagement dir — the three decisions ADR-12 records.
3. Ledger `d152` — **B3's required row shapes.** Your `send_accepted` row must carry the transport fields B3 checks (`alerts=1`, `attempted=true`, `delivered=true`, `probe="not-run"`, `dry_run=false`). Read it so what you emit is what B3 can actually read.
4. `CLAUDE.md` (repo root) — house rules. Note rule 8 (tickets), the launchd `PATH` requirement, and the Agents SDK section.
5. `agents-sdk/BUGFIX-2026-04-07-launchd-path.md` — every plist needs `EnvironmentVariables` with the full `PATH` or the agent fails with `CLIConnectionError`.
6. `agents-sdk/agents/meta_agent.py`, `agents-sdk/lib/pushover.py`, `agents-sdk/schedules/install_schedules.sh`, `agents-sdk/config.toml` — what you are extending.

## Task 1 — Build the drill runner per ADR-12

Test-driven: write the failing test first, then the code. The suite is `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q`. **It currently passes 997 on the Mac Mini and 993/4 on this MacBook** — the four MacBook failures are pre-existing and environmental (bare-`python3` subprocesses without `dotenv`); confirm that baseline before you start and do not "fix" them.

What ADR-12 requires you to produce, in its own terms — read it for the detail, this is only the shape:

- A `claim6_drill` runner with **no hand-run send mode**. Production sends refuse unless the parent is launchd (PPID 1), `CLAIM6_LAUNCHD_LABEL` matches the registered label, and the current slot equals the registered calendar occurrence. Test clock/sender injection must be **network-disabled**.
- `lib/pushover.py` gains `retry`/`expire` send parameters and a **receipt-status reader**. Respect the provider's five-second polling floor.
- The acknowledgment rule, exactly: qualifying only on `acknowledged=1` **and** a nonzero `acknowledged_at` **and** `acknowledged_by_device` equal to the registered device. Provider acceptance, `request`, `receipt`, `delivered=true` and `last_delivered_at` are transport facts and never acknowledgment. Expiry, send failure, receipt-read failure, or an ack from a different device are **retained negative evidence** — persist them, never discard.
- `vault/health/claim6-drills.jsonl` with the fixed `record_type="drill"`, the closed event set (`scheduled | send_accepted | acknowledged | send_failed | expired_unacknowledged | receipt_poll_failed`), and a writer that **rejects incident-only fields** (`incident_id`, `severity`, `verified_restored_at`, restore-verification data). Enforce this in the writer, not by convention.
- A **monthly launchd plist** at `Hour=8, Minute=15`, full `PATH` + `PYTHONPATH` + the fixed label.
- **Meta-agent reconciliation:** at its 08:45 run, compare the schedule contract against the drill JSONL and write the typed three-line drill block into both `daily-fleet-status-YYYY-MM-DD.md` and rolling `fleet-state.md` **before** its own Pushover step. Ordering is load-bearing — that is what keeps the missed-fire surface independent of the channel under test. A missing expected `scheduled` row past the grace instant renders `DRILL FIRE MISSING — SCHEDULED EXECUTION NOT OBSERVED` with its Means / Does not mean lines.

**Three things you must NOT hardcode**, because they are not yours to choose:

- **The drill day-of-month.** ADR-12 ties the first occurrence to B3's window, and **B3 has not started** — Sean has not ruled its start date. Make the day a config value, default the schedule to **not installed**, and document registration as a deploy-time step.
- **Sean's Pushover device name** for `acknowledged_by_device`. Config value; it must be registered before the first drill can qualify. Name this in your handoff.
- **The registered launchd label**, if ADR-12 leaves any freedom — keep it config-visible rather than buried.

## Task 2 — The schedule-truth cleanup (Sean asked for this by name)

Sean's words: the meta-agent and daily-driver were **switched**, because the meta-agent kept reporting the daily driver hadn't run — it was reading ten minutes before the driver fired. The swap was made in launchd; **the code still describes the old world**, and he cannot remember which runs when.

**Ground truth, measured from the Mini's loaded plists on 2026-08-30 — this is authoritative, not the code and not the docs:**

| Label | Actually fires |
|---|---|
| `com.sean.agent.daily-morning` | **08:30** |
| `com.sean.agent.meta-agent` | **08:45** |
| `com.sean.agent.vault-indexer` | 02:00 |
| `com.sean.agent.vault-synthesizer` | 02:30 |
| `com.sean.agent.deep-researcher` | 02:45 |
| `com.sean.agent.vault-critic` | 03:30 |
| `com.sean.agent.knowledge-lint` | Sunday 22:00 |
| `com.sean.job-feed` | 08:00, 08:30, 09:00, 09:30, 10:00, 10:30, 11:00 |
| `com.sean.agent-fleet-dashboard` | 06:00 |

Four known wrong strings — find any others rather than trusting this list to be complete:

- `agents-sdk/agents/meta_agent.py:76` — `"meta_agent"` metadata says `"8:35 AM daily"`. Should be **8:45**.
- `agents-sdk/agents/meta_agent.py:73` — `"daily_driver"` metadata says `"8:45 AM daily"`. Should be **8:30**. *(These two are the swap Sean remembers, still inverted in code.)*
- `agents-sdk/agents/meta_agent.py:14` — docstring says `"Schedule: Daily at 08:35 (before Daily Driver at 08:45)"`. Wrong time **and** wrong ordering: it runs **08:45, after** the daily driver at 08:30. That ordering is the whole point of the fix.
- `agents-sdk/agents/daily_driver.py:327` — writes `"_Auto-filled by Daily Driver at 08:45._"` **into Sean's daily note**, so the wrong time is user-visible in the vault. Should be **08:30**.

Every other `AGENT_METADATA` schedule string matched ground truth when I checked; verify rather than assume.

**Then make this class of drift hard to repeat.** These strings are hand-maintained beside plists that are the real authority, which is why they rotted. Add a test that reads the checked-in plists in `agents-sdk/schedules/` and asserts every `AGENT_METADATA` schedule string agrees with its plist's `StartCalendarInterval`. If a display format can't be mechanically derived, assert on a parsed hour/minute rather than loosening the test into uselessness. A test that can't fail is worse than no test.

## Task 3 — Report, do not fix: the critic's schedule is still live

Measured 2026-08-30: `agents-sdk/config.toml` has `schedule_enabled = false` for the critic and `install_schedules.sh` carries the ADR-04 convergent removal — but **`com.sean.agent.vault-critic` is still loaded on the Mini and fired every day 08-26 → 08-30 at ~03:35.** The convergent removal only takes effect when the installer runs, and it has not run since the deploy. So a ratified Phase-0 disable (eng-002.d15/d49) is shipped in code and **not applied in production**.

Softening detail, which you must not omit: its last five runs are `success` with `status=partial`, not `error` — so it is not currently generating the false alerts d15 feared. The risk is that it reverts during B3's window and turns a quiet night into an alert night.

**Do not run the installer and do not touch the Mini.** Report it, and file it as a rule-8 ticket.

## Hard constraints — violating any of these fails the pass

- **Never send a real Pushover notification.** It pages Sean's phone. All tests inject a fake sender; the production path must be unreachable from a test. If you believe you need one live send to verify, stop and say so instead.
- **Do not touch the Mac Mini.** No ssh writes, no deploy, no `install_schedules.sh`, no `launchctl`. Deployment is a separate, separately-approved step.
- **Do not redesign ADR-12.** If you find something in it that cannot be built as written, **stop and report it** — do not quietly build a different thing. That report is more valuable than a workaround.
- **Do not edit anything under `systemcraft/`.** The design record is closed. `git status --porcelain systemcraft/` must be empty when you finish.
- **Do not commit to `main` and do not push.** Work on a branch `feat/a12-claim6-drill` and commit there, so the work is durable without touching the trunk. Sean ratifies the merge; the push is his.
- **Never write real personal data into tracked files**, and never `git add` a private-layer path (CLAUDE.md rule 9).
- Leave no `__pycache__` under `systemcraft/`.

## Verify before you finish — actual output, not assertions

- Full suite: `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -q`. Report the count and confirm the only failures are the four pre-existing environmental ones.
- Your new tests, named, with what each actually exercises — and state plainly what they **do not** exercise (no test here proves a real launchd fire or a real notification reaching a phone; only a deployed scheduled run does).
- `git status --porcelain systemcraft/` — must be empty.
- `python3 systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/artifacts/check-version-drift.py` — must still exit 0.

## Deliverable — plain language, for a PM

1. What you built, in one breath, and what it does at 08:15 on drill day.
2. The three values Sean must register before the first drill can qualify, and where each lives.
3. How the missed-fire surface stays independent of Pushover, and where it can still fail silently.
4. The schedule-truth cleanup: every string you corrected, and how the new test prevents the drift returning.
5. The critic finding, restated for him, with your recommendation.
6. Test output, verbatim, with what it does and does not prove.
7. What remains before B3 can start.
8. Anything you found and did **not** fix, named explicitly.
