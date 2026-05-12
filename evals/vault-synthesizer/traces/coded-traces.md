# Coded Traces — the evidence behind `failure-modes.md`

Each block below is a real excerpt from production logs in the error-analysis
window (2026-04-24 → 2026-05-10). The open code identifies the failure mode
and the case ID(s) it justifies.

---

## Excerpt 1 — Mode 1 (silent empty output, status="ok") → vs-015, vs-016, vs-017

`vault/health/synth-manifest-2026-05-09.json`:
```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 1915.11,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 21,
  "model_used": "",
  "rejected_count": 0,
  "run_id": "2026-05-09T02:38:59",
  "status": "ok",
  "wol_status": ""
}
```

Open code: `status: "ok"` is reported while `concepts_written: 0` — the run
processed 21 files, ran for 31 minutes, and produced nothing. Three monitoring
layers (manifest, daily-driver brief, Pushover) all read this as healthy. This
is the canonical load-bearing failure mode the suite was built to catch.

Corresponding log line from `vault-synthesizer-2026-05-09.log`:
```
2026-05-09 03:56:24,570 [INFO] synthesis ok concepts=0 connections=0 rejected=0 edges=0 edges_rejected=0 duration=1915.1s
```

Open code (log): the log line's status token is `ok` while every count is `0`.
The logger wrote the truth; the status token obscured it.

---

## Excerpt 2 — Mode 1 (silent empty output, status="partial") → vs-015, vs-016, vs-017

`vault/health/synth-manifest-2026-05-08.json`:
```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 2729.33,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 30,
  "model_used": "",
  "rejected_count": 0,
  "run_id": "2026-05-08T02:30:04",
  "status": "partial",
  "wol_status": ""
}
```

Open code: `status: "partial"` — the other failure-state variant — also yields
`concepts_written: 0`. Five nights in this window (2026-05-07, 2026-05-08,
2026-05-10) used `"partial"` while the other nights used `"ok"`. Both map to
zero output. The distinction between `ok` and `partial` carries no signal about
whether knowledge articles were produced.

Corresponding log line from `vault-synthesizer-2026-05-08.log`:
```
2026-05-08 03:15:34,330 [INFO] synthesis partial concepts=0 connections=0 rejected=0 edges=0 edges_rejected=0 duration=2729.3s
```

---

## Excerpt 3 — Mode 3 + Mode 6 (missing status taxonomy, downstream misread) → vs-017, vs-020, vs-021

`vault/health/synth-manifest-2026-05-10.json`:
```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 2756.0,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 30,
  "model_used": "",
  "rejected_count": 0,
  "run_id": "2026-05-10T02:37:33",
  "status": "partial",
  "wol_status": ""
}
```

Open code: the status taxonomy has two observed values (`"ok"`, `"partial"`)
but no `"success-empty"` or `"partial-empty"` that would let a downstream
consumer distinguish "structurally successful, zero output" from "structurally
successful, output present." The daily-driver brief reads `status` at face
value; `"partial"` with `concepts_written: 0` renders in the morning brief as
a non-critical partial run — which is the literal string and a complete lie about
vault health.

Corresponding log line from `vault-synthesizer-2026-05-10.log`:
```
2026-05-10 04:41:15,506 [INFO] synthesis partial concepts=0 connections=0 rejected=0 edges=0 edges_rejected=0 duration=2756.0s
```

---

## Excerpt 4 — Mode 4 (model_used schema integrity) → vs-018

From any of the seven manifests in the error window (representative: `synth-manifest-2026-05-03.json`):
```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 1809.35,
  "files_processed": 20,
  "model_used": "",
  "rejected_count": 0,
  "run_id": "2026-05-03T02:30:05",
  "status": "ok",
  "wol_status": ""
}
```

Open code: `model_used: ""` is the empty-string sentinel left when zero LLM
calls succeed. The documented values are model identifiers (e.g.,
`"qwen3-14b-research:latest"`); `""` is not part of any documented enum. Every
downstream consumer that reads this field must handle a value it was never told
to expect. The pattern recurs across all seven manifests in the window — it is
structural, not a one-off.

---

## Excerpt 5 — Mode 5 (Pushover credentials fail-quiet) → vs-019

`vault/90_system/agent-logs/vault-synthesizer-stderr.log` (repeating pattern —
the full log is 75 KB of this triplet cycling every run):
```
Health check failed for macbook_pro:
Health check failed for macbook_pro:
Pushover notify_wol_failure send failed: Missing Pushover credentials in Keychain (pushover_user_key / pushover_app_token)
```

Open code: the Pushover notification subsystem fails silently and repeatedly.
`Health check failed for macbook_pro:` emits with an empty message body (the
exception detail is swallowed), then `notify_wol_failure` raises and logs
without propagating. The synthesizer continues to `status: "ok"` or `"partial"`.
The catastrophic regression the system was designed to surface — MBP offline,
zero knowledge production — is silenced by the very notification layer designed
to surface it.

---

## Excerpt 6 — Mode 2 (run-level status misreport, per-file failures absorbed) → vs-016

From `vault/90_system/agent-logs/vault-synthesizer-stderr.log` (final two lines
written by the 2026-05-12 run, same pattern as every night in the window):
```
[INFO] synth-manifest written: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/health/synth-manifest-2026-05-12.json
[INFO] synthesis partial concepts=0 connections=0 rejected=0 edges=0 edges_rejected=0 duration=2731.3s
```

Open code: per-file LLM failures are caught inside the inner loop and logged;
the outer function returns normally with `status="partial"`. Run-level status
is never escalated to `error` because the outer function itself did not raise.
The final `[INFO]` line is structurally indistinguishable from a successful run
that processed a quiet vault — only the counts reveal the truth, and those
counts are not checked by any monitor.

---

## Pattern summary across all excerpts

| Date | status | concepts_written | model_used | files_processed |
|------|--------|-----------------|------------|-----------------|
| 2026-05-03 | ok | 0 | "" | 20 |
| 2026-05-07 | partial | 0 | "" | 30 |
| 2026-05-08 | partial | 0 | "" | 30 |
| 2026-05-09 | ok | 0 | "" | 21 |
| 2026-05-10 | partial | 0 | "" | 30 |

Seven consecutive manifests in the error-analysis window. Zero concepts written.
No monitor fired. This is why the eval suite exists.
