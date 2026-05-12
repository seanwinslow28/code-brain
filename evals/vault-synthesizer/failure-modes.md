# Vault Synthesizer — Failure Modes (open-coded from 17 days of real logs)

> The cases in `cases.yaml` are not imagined. Each one is grounded in an observed
> failure mode from 2026-04-24 → 2026-05-10 production logs. This file is the
> Rosetta Stone between log evidence and case ID.

## Mode 1 — Silent empty output

The synthesizer reports `status: "ok"` while writing zero concept articles to disk.
Three layers of monitoring (manifest, daily-driver brief, Pushover) all read this
as healthy. The system rotted silently for nine consecutive nights before the
discrepancy surfaced.

Evidence: `vault/health/synth-manifest-2026-05-{02,03,06,07,08,09,10}.json` —
each has `"status": "ok"` with `"concepts_written": 0`.

Caught by: **vs-015**, **vs-016**, **vs-017**.

## Mode 2 — Status-field misreport on per-file LLM failures

When every per-file LLM call raises (WOL fails, model returns an error, network
drops), the synthesizer's outer loop catches each one, logs it, and continues.
The run-level status promotion does not happen — final status reports `ok`
because the function returned without itself raising.

Evidence: stderr logs on the same dates as Mode 1.

Caught by: **vs-016**.

## Mode 3 — Missing status taxonomy values

The status enum today is `{ok, error, partial}`. There is no `success-empty`
(succeeded structurally, produced no output) or `partial-empty` (some files
processed, none produced articles). Downstream consumers cannot distinguish
"healthy and quiet" from "broken and quiet."

Caught by: **vs-017**.

## Mode 4 — `model_used` schema integrity

`model_used` is initialized to `""` and overwritten on the first successful LLM
response. Zero-success runs leave the empty string in the manifest. Any
downstream code that reads this field has to handle a sentinel that isn't part
of the documented enum.

Caught by: **vs-018**.

## Mode 5 — Pushover credentials fail-quiet

Missing keychain credentials cause Pushover's `notify()` to log "missing creds"
and return. The synthesizer treats this as a successful notification. A
catastrophic failure in the very system designed to surface failures.

Evidence: `vault/90_system/agent-logs/vault-synthesizer-stderr.log` — repeated
`"pushover credentials missing"` lines with no corresponding crash.

Caught by: **vs-019**.

## Mode 6 — Downstream-consumer misread of healthy status

The daily-driver morning brief takes the synth manifest's `status` field at face
value. A `status=ok, concepts_written=0` manifest renders in the brief as
"Vault Health: ok," which is the literal truth and a complete lie.

Caught by: **vs-020** (index/disk integrity) and **vs-021** (brief consumer).
