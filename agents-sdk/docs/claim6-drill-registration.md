# Claim-6 drill registration and deploy handoff

The ADR-12 runner is built but deliberately unarmed. It must not be installed
until B3's seven-night window has a start date and the three registration
values below are known.

## Register before the first qualifying fire

Edit `[agents.claim6_drill]` in `agents-sdk/config.toml`:

1. `day_of_month` — choose the day whose first 08:15 occurrence falls inside
   B3's persisted seven-night window. Supported values are 1–31; dates absent
   from a shorter month have no occurrence in that month, as launchd defines.
2. `launchd_label` — register the exact label launchd will supply through
   `CLAIM6_LAUNCHD_LABEL`.
3. `acknowledged_device` — register the exact Pushover Receipts API device name
   that is allowed to qualify the drill. Do not put a real value in a commit;
   production registration belongs in the private deploy revision.

After all three are present, set `schedule_enabled = true`. On a separately
approved Mini deploy, the ordinary `schedules/install_schedules.sh` run renders
the checked-in template as a monthly `Day / Hour=8 / Minute=15` plist and loads
it. While the flag is false, that installer converges the generated plist to
absence. Do not invoke `claim6_drill.py` to simulate the fire: the runner has no
manual send mode and refuses any real send without PPID 1, the registered label,
and the exact registered calendar minute.

At 08:15 the scheduled runner writes `scheduled`, sends one plainly labeled
priority-2 Pushover drill with retry 300 seconds and expiry 900 seconds, writes
`send_accepted` immediately after provider acceptance, and polls receipts no
faster than every five seconds. Only `acknowledged=1`, a nonzero
`acknowledged_at`, and the exact registered device produces `acknowledged`.
Failure, receipt-read failure, expiry, and a different-device acknowledgment
remain negative rows in `vault/health/claim6-drills.jsonl`.

## What the 08:45 report does

The meta-agent compares the registered occurrence with the drill JSONL and
places a typed three-line Claim-6 block in both fleet reports before its own
Pushover step. That removes Pushover circularity, but it can still be silent if
the Mini or launchd is broadly down, the meta-agent does not run, the vault
cannot be written, or nobody reads the report.

## 1A migration contract

The Phase-0 JSONL is the authority until the 1A store cutover. At cutover it
migrates once into a separate append-only `drill_records` sibling table, never
`incident_records`. The migration must preserve each drill ID, lifecycle row,
timestamp, receipt link, source-file hash, and source line; prove source and
destination row equality before readers switch; retain the JSONL as an
immutable hashed archive; and stop dual-writing. `drill_records` must reject
incident fields, while `incident_records` must reject drill record types and
lifecycle names. The 1A store does not exist yet, so this build does not perform
that later migration.

## What tests do not prove

The tests use fake senders and clocks. They prove schema, provenance decisions,
receipt interpretation, five-second polling, schedule rendering, and report
output. They do not prove that launchd fires, Pushover accepts a deployed send,
or a notification reaches a phone. Only the first deployed scheduled occurrence
can produce that evidence.
