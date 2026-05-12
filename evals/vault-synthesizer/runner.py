# evals/vault-synthesizer/runner.py
"""Vault Synthesizer Eval Runner.

Run with:
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest \
        ../evals/vault-synthesizer/runner.py -v

Standalone (for the Loom demo):
    cd agents-sdk && PYTHONPATH=. .venv/bin/python3 ../evals/vault-synthesizer/runner.py
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent
CASES_PATH = ROOT / "cases.yaml"
LAST_RUN_PATH = ROOT / "last-run.md"


def grade_exact_match(result, case) -> tuple[str, str]:
    """Evaluate `case['pass_criteria']` as a Python expression against `result`.

    The expression has `result` bound in its namespace; nothing else. Failure to
    evaluate is reported as FAIL with the exception message, not a runner crash.
    """
    expr = case["pass_criteria"]
    try:
        ok = bool(eval(expr, {"__builtins__": {}}, {"result": result}))
    except Exception as e:
        return "FAIL", f"grader-eval-error: {e!r}"
    return ("PASS", "") if ok else ("FAIL", f"{expr} evaluated False")


def grade_rubric(result, case) -> tuple[str, str]:
    """Structured rubric checks — case-specific Python that asserts against `result`.

    For v1, this is identical to exact-match (pass_criteria is a Python expr).
    The split exists so future rubric cases can grow without re-shaping the schema.
    """
    return grade_exact_match(result, case)


GRADERS = {"exact-match": grade_exact_match, "rubric": grade_rubric}


def _load_cases() -> list[dict]:
    return yaml.safe_load(CASES_PATH.read_text())


def _invoke_synthesizer(case) -> object:
    """Build the synthesizer call from case['input'] and invoke it.

    Materializes a temp vault_root with N fixture notes copied from
    traces/fixtures/note-*.md, builds the real signature run_synthesis() takes,
    and returns the SynthesisResult.

    vs-019 (Pushover missing creds) is handled at the call site in test_case().
    """
    from agents import vault_synthesizer as vs  # agents-sdk/ is on sys.path via conftest.py
    import shutil
    import tempfile

    inp = case.get("input", {})

    # Build the mock llm_caller.
    # The real llm_caller must return a dict with "concepts" and "connections".
    mock_spec = inp.get("llm_caller_mock")
    if mock_spec is None:
        # No mock — for cases that don't specify a mock (vs-014, vs-015), use a
        # stub that always fails so we deterministically reach the "zero output"
        # state. The point of vs-015 is to assert status != "ok" when
        # concepts_written == 0, so a failing caller is the right fixture.
        def llm_caller(*a, **kw):
            raise ConnectionRefusedError("eval-suite: no live LLM in eval runs")
    elif "raises ConnectionRefusedError" in mock_spec:
        def llm_caller(*a, **kw):
            raise ConnectionRefusedError("synthetic LLM failure")
    elif "raises on file 1 + 2, succeeds with empty body on file 3" in mock_spec:
        state = {"n": 0}
        def llm_caller(*a, **kw):
            state["n"] += 1
            if state["n"] <= 2:
                raise ConnectionRefusedError("synthetic LLM failure")
            # Return a valid dict with empty lists — produces zero concepts/connections
            return {"concepts": [], "connections": []}
    else:
        raise ValueError(f"unsupported llm_caller_mock: {mock_spec!r}")

    # Trivial retriever — embedding similarity isn't what these regression cases
    # test; they probe status promotion / model_used / schema integrity. Return
    # an empty result so the synthesizer doesn't try to call the real vault indexer.
    def retriever(text, top_k):
        return []

    # Materialize a temp vault_root with N fixture notes
    fixtures_dir = ROOT / (inp.get("fixtures") or "traces/fixtures")
    note_count = inp.get("note_count")
    tmpdir = tempfile.mkdtemp(prefix="eval-synth-")
    vault_root = Path(tmpdir)
    changed_files: list[Path] = []
    if note_count is not None and fixtures_dir.exists():
        note_paths = sorted(fixtures_dir.glob("note-*.md"))[:note_count]
        for src in note_paths:
            dst = vault_root / src.name
            shutil.copy(src, dst)
            changed_files.append(dst)

    # Pushover-removed scenario for vs-019 — clear keychain-source env vars
    if inp.get("pushover_keychain") == "removed":
        import os
        os.environ.pop("PUSHOVER_USER_KEY", None)
        os.environ.pop("PUSHOVER_API_TOKEN", None)

    return vs.run_synthesis(
        vault_root=vault_root,
        changed_files=changed_files,
        llm_caller=llm_caller,
        retriever=retriever,
        budget_seconds=30,
        db_conn=None,
    )


def _invoke_brief(case) -> str:
    """vs-021: invoke the daily-driver brief builder with a fake synth manifest.

    Workstream B adds render_vault_health() — if it doesn't exist yet, raise
    ImportError so the caller can emit a clear FAIL message.
    """
    try:
        from agents import daily_driver as dd  # agents-sdk/ on sys.path via conftest.py
        render_fn = getattr(dd, "render_vault_health", None)
    except ImportError:
        render_fn = None
    if render_fn is None:
        raise ImportError("vs-021: daily_driver.render_vault_health does not exist yet (Workstream B adds it)")
    fake = case["input"]["fake_manifest"]
    return render_fn(fake)


@pytest.fixture(scope="session")
def cases():
    return _load_cases()


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_case(case):
    if case.get("skip_reason"):
        pytest.skip(case["skip_reason"])

    if case["id"] == "vs-021":
        try:
            result_text = _invoke_brief(case)
        except ImportError as exc:
            pytest.fail(str(exc))
            return
        class _Wrap:
            pass
        w = _Wrap()
        w.brief = result_text
        case = dict(case)
        case["pass_criteria"] = (
            "'WARNING' in result.brief and "
            "('concepts_written: 0' in result.brief or 'empty' in result.brief)"
        )
        result = w

    elif case["id"] == "vs-019":
        # Workstream B adds PushoverConfigurationError. Until it exists this
        # case fails deterministically with a clear message (not an ImportError
        # traceback).
        try:
            from lib.pushover import PushoverConfigurationError  # agents-sdk/ on sys.path via conftest.py
        except ImportError:
            pytest.fail(
                "vs-019: PushoverConfigurationError class does not exist yet (Workstream B adds it)"
            )
            return
        with pytest.raises(PushoverConfigurationError):
            _invoke_synthesizer(case)
        return

    elif case["id"] == "vs-020":
        # Index-integrity check — no synthesizer invocation needed.
        # Compare entry count in the fixture index.md against file count in concepts dir.
        inp = case.get("input", {})
        concepts_dir = ROOT / inp.get("fixture_concepts_dir", "traces/fixtures/concepts_3files")
        index_md = ROOT / inp.get("fixture_index_md", "traces/fixtures/index_lists_3.md")
        concept_files = list(concepts_dir.glob("*.md")) if concepts_dir.exists() else []
        index_text = index_md.read_text(encoding="utf-8") if index_md.exists() else ""
        # Count lines under "## Concepts" that start with "- [["
        import re
        concept_entries = re.findall(r"^\s*-\s*\[\[", index_text, re.MULTILINE)
        file_count = len(concept_files)
        entry_count = len(concept_entries)
        class _IndexResult:
            pass
        r = _IndexResult()
        r.consistent = (file_count == entry_count)
        r.file_count = file_count
        r.entry_count = entry_count
        # pass_criteria for vs-020 is prose ("count(index.md...) == count(concepts/*.md)"),
        # not a Python expr — evaluate r.consistent directly rather than through eval().
        if not r.consistent:
            pytest.fail(
                f"vs-020: index entry count ({entry_count}) != concept file count ({file_count})"
            )
        return

    else:
        result = _invoke_synthesizer(case)

    grader = GRADERS[case["judge_type"]]
    status, detail = grader(result, case)
    if status == "FAIL":
        pytest.fail(f"{case['id']}: {detail}")

    grader = GRADERS[case["judge_type"]]
    status, detail = grader(result, case)
    if status == "FAIL":
        pytest.fail(f"{case['id']}: {detail}")


def _write_last_run(report_lines: list[str]) -> None:
    header = [
        f"# Vault Synthesizer Eval Run — {datetime.now(timezone.utc).isoformat()}",
        "",
        "> **Read this first.** This suite ships intentionally red. Each ❌ below is a",
        "> real production failure mode this suite catches — not a broken eval. The",
        "> pass rate jumps after the Workstream B synthesizer fix lands. See",
        "> `EXPLANATION.md` for the design rationale.",
        "",
        "| ID | Category | Result | Notes |",
        "|---|---|---|---|",
    ]
    LAST_RUN_PATH.write_text("\n".join(header + report_lines) + "\n")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
