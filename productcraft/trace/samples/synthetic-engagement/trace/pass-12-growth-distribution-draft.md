---
pass: pass-12
seat: growth-distribution
kind: draft
stage: 4
runtime: claude-sonnet-5
launch: "Agent tool, fresh context"
effort: high
launched: 2026-10-06T13:20:00-04:00
completed: 2026-10-06T13:42:00-04:00
wall_clock_s: 1320
meter:
  input: 151200
  output: 17400
  cached: 140000
meter_source: Agent-tool usage
inputs:
  - path: artifacts/strategy-pov.md
    sha256: 4cbcb041c5463d7ac95d0ea8dac43b7ed20f8aed0aecb74540ce8045c478805d
  - path: artifacts/discovery-packet.md
    sha256: deea84c6861f8733c64250b5c450bf093b19795013a65e0f29335288679c279f
  - path: artifacts/metrics-evidence-plan.md
    sha256: 4c3e6cad5cbaec5f4243359b81028b7caba71f939274694cd767c8762424f530
  - path: corpus/growth/shelf.md
    sha256: 5079606e4b3cdedb86837a2fc949feaa0ff3ac753e7836c5d9a851be5ebfe98c
withheld:
  - the drafting conversation
  - ledger entries of other engagements
outputs:
  - path: artifacts/growth-gtm.md
    sha256: e4e1b502de2f2b35d43f16e1634b397f11aa72d28289de3441a0eb59c9efa1e7
  - id: pc-eng-000.d07
raw_log: trace/logs/pass-12.jsonl
checks:
  - pass: pass-13
    kind: audit
    verdict: AUDIT LOOPBACK — 1 material
triggered_by: null
shadow_of: null
---

## Corpus read

- corpus/growth/shelf.md
- artifacts/metrics-evidence-plan.md

## Moves

artifacts/growth-gtm.md § Moves

## Notes

Grounding manifest-only for Growth's corpus (shelf label read; book not opened).
