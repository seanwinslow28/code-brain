# Daily Driver — Failure Mode Taxonomy

Phase 1 ships with the fleet-memory-wiring slice only. Production-grounded
failure modes are authored as traces accumulate. This file mirrors the
shape of [`evals/vault-synthesizer/failure-modes.md`](../vault-synthesizer/failure-modes.md);
fill in modes 1–N below as you observe them in real morning runs.

## Mode 1 — Fleet-memory wiring drift (Phase 1)
**Observed:** N/A — guarded preemptively by dd-001, dd-002.
**Symptom:** `build_options` ships without the six MCP tools, or with the
wrong beta header. Model can't call memory tools; reads fail silently;
no lessons accumulate.
**Cases:** dd-001, dd-002.

## Mode 2+ — TBD (Phase 2)
Author production-grounded modes after Phase 1 produces ≥1 week of traces.
Suggested probes:
- Morning brief skips the 1-3-5 section when synth-manifest is malformed
- Fleet-overnight digest injected at wrong anchor (anchor drift)
- MBP-asleep state misreported in the digest
- Daily-note duplicate created when an earlier 08:45 run partial-completed
