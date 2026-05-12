---
date: 2026-05-08
tags: [agent-fleet, vault-synthesizer, status-reporting]
---

# 2026-05-08 daily note

Traced the timezone bug in the daily driver manifest lookup. The Mac Mini runs
UTC but `date.today().isoformat()` on the MBP (Pacific) produces a different
string for the same synthesizer run. The vault synthesizer writes the manifest
with the MBP's local date; the daily driver reads with UTC — they never agree
near midnight.

This is a textbook [[silent-empty-output]] scenario: the synthesizer output is
real, sitting on disk, but the consumer path returns nothing because the key
doesn't match. The fix is to write the manifest filename with UTC explicitly.
See also [[status-misreport]] and [[vault-synthesizer]] for the broader pattern
of agents that produce correct output that gets silently dropped downstream.
