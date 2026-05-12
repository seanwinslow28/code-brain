---
date: 2026-05-04
tags: [agent-fleet, pushover, vault-synthesizer]
---

# 2026-05-04 daily note

Spent an hour debugging why the vault synthesizer wasn't pinging on failures.
Turns out the Pushover credentials weren't in the keychain — the notify call was
logging "missing creds" and returning silently. The system designed to surface
failure was the first thing to fail quietly.

Checked `vault/90_system/agent-logs/vault-synthesizer-stderr.log` and confirmed
the agent ran, produced zero output, and exited 0. The synthesizer treated
empty output as success. Related: [[pushover-fail-quiet]] and [[vault-synthesizer]].
