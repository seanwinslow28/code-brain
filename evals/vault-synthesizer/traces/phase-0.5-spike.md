# Phase 0.5 — Synthesizer spike test (run 2026-05-12)

Purpose: confirm the regression-suite claim that vs-016, vs-017, vs-018 fail on the current
synthesizer code AS WRITTEN, before we write the YAML cases.

## Setup
- Python: /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/.venv/bin/python3 (3.13)
- Branch: eval-suite-2026-05-12
- run_synthesis() signature: `(*, vault_root: Path, changed_files: list[Path], llm_caller: Callable[..., dict], retriever: Callable[..., list[dict[str, Any]]], now_iso: str | None = None, budget_seconds: int = 2700, top_k: int = 5, db_conn: sqlite3.Connection | None = None, classifier_version: str | None = None, logger: logging.Logger | None = None) -> SynthesisResult`
- Invocation kwargs (besides llm_caller): vault_root=<tempdir Path>, changed_files=[<one fake note>], retriever=<trivial lambda returning []>, budget_seconds=30, db_conn=None

## vs-016 probe — all-file LLM failure
- llm_caller: `def always_raise(*a, **kw): raise ConnectionRefusedError("synthetic LLM failure")`
- result.status: `'ok'`
- result.concepts_written: `0`
- Verdict: PASS — case fails today as expected. When every per-file LLM call raises, the
  exception is caught at line 366-368, appended to `result.warnings`, and the loop
  `continue`s WITHOUT touching `result.status`. Status stays `"ok"` (initialized at line 326).
  A future fix (Workstream B) should flip status to `"partial"` or a new `"partial-empty"`
  value when zero files produced output. The case is correctly targeted at the current bug.

## vs-017 probe — partial-empty distinction
- Today's status taxonomy: `"ok" | "partial" | "budget-exhausted" | "wol-deferred" | "error"`
- Verdict: PASS (naturally) — no `"partial-empty"` or `"success-empty"` value exists anywhere
  in the codebase today. The case will fail by definition until Workstream B introduces the
  new status value. No code path today can accidentally produce it, so the case is safe to
  lock into YAML as-is.

## vs-018 probe — model_used default
- result.model_used: `''`
- Verdict: PASS — case fails today as expected. `model_used` starts as `""` on
  `SynthesisResult` (dataclass default, line 79) and is ONLY set in `main()` after
  `run_synthesis()` returns (line 627: `result.model_used = manifest_state.get("model_used", "")`).
  When `run_synthesis()` is called directly (as in the eval harness or unit tests), the field
  is never populated and stays `""`. A future fix (Workstream B) should accept `model_used`
  as a parameter to `run_synthesis()` or have the function populate it internally.

## Conclusion
- vs-016: PASS — status stays `"ok"` when all LLM calls fail (should be `"partial"` or `"partial-empty"`).
- vs-017: PASS — `"partial-empty"` value does not exist in today's code; case naturally fails.
- vs-018: PASS — `model_used` stays `""` when `run_synthesis()` is called directly (not via `main()`).

All three regression-suite cases (vs-016, vs-017, vs-018) fail on today's code as expected. Proceed to Task A1.
