---
pass: pass-15
seat: growth-distribution
kind: audit
stage: 5
runtime: claude-sonnet-5
launch: "Agent tool, fresh context"
effort: high
launched: 2026-10-06T14:48:00-04:00
completed: 2026-10-06T14:57:00-04:00
wall_clock_s: 540
meter:
  input: 122400
  output: 4100
  cached: 0
meter_source: Agent-tool usage
inputs:
  - path: artifacts/business-case.md
    sha256: 716fdcc6d80e65557a3c6844ae2d89cab1d4282e0911ec3e6cc9101a1e46566e
  - path: artifacts/growth-gtm.md
    sha256: e4e1b502de2f2b35d43f16e1634b397f11aa72d28289de3441a0eb59c9efa1e7
withheld:
  - the drafting conversation
  - ledger entries of other engagements
outputs:
  - path: audits/audit-business.md
    sha256: e75618222b8f73d05e440488b620a1aa2a17502cc0f7b502c0569c7f437a5ed7
raw_log: trace/logs/pass-15.jsonl
checks: []
triggered_by: null
shadow_of: null
---

## Corpus read

- artifacts/business-case.md

## Moves

none — this kind hands no artifact forward

## Notes

Stake: does the model price the loop it depends on? Yes.
