---
date: 2026-05-07
tags: [agent-fleet, vault-synthesizer, status-reporting]
---

# 2026-05-07 daily note

The vault synthesizer produced a synth-manifest today but the daily note said
"0 concepts written." The manifest JSON showed `concepts_written: 3` — clear
mismatch. The daily driver is reading a stale manifest from yesterday, not
today's file. This is a status misreport: the agent succeeded, the report lied.

The synthesizer and the daily driver are decoupled by filesystem; the driver
reads `vault/health/synth-manifest-{today}.json` but the date comparison was
off by one timezone. Related: [[silent-empty-output]] and [[vault-synthesizer]].
Also flagged as [[status-misreport]] — the output exists but the consumer
can't see it.
