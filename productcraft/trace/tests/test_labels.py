"""labels.md — one per engagement, rows keyed by pass id (#272 decision 6).

Columns, in the order the viewer's Copy label rows exports:
pass | verdict | first_failing_stage | critique | failure_code
"""
import pytest

from tracekit.labels import LabelsError, Label, parse_labels

HEADER = "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n"


def doc(rows: str) -> str:
    return "---\nengagement: pc-eng-000-callboard\nlabeler: Sean\n---\n\n# Labels\n\nprose above the table\n\n" + HEADER + rows


def test_rows_keyed_by_pass_id():
    labels = parse_labels(doc("| pass-01 | pass | | Diagnosis names the constraint. | |\n| pass-02 | fail | 1 | Lead with it. | |\n"))
    assert labels["pass-01"] == Label("pass-01", "pass", None, "Diagnosis names the constraint.", "")
    assert labels["pass-02"] == Label("pass-02", "fail", 1, "Lead with it.", "")


def test_escaped_pipe_in_critique_is_unescaped():
    labels = parse_labels(doc("| pass-03 | pass | | KR-1 \\| KR-2 both measured. | |\n"))
    assert labels["pass-03"].critique == "KR-1 | KR-2 both measured."


def test_empty_verdict_is_an_unlabeled_row():
    labels = parse_labels(doc("| pass-17 | | | | |\n"))
    assert labels["pass-17"].verdict is None


def test_unknown_verdict_raises():
    with pytest.raises(LabelsError) as e:
        parse_labels(doc("| pass-01 | mostly fine | | | |\n"))
    assert "pass-01" in str(e.value)


def test_fail_without_first_failing_stage_raises():
    with pytest.raises(LabelsError):
        parse_labels(doc("| pass-02 | fail | | why | |\n"))


def test_duplicate_pass_raises():
    with pytest.raises(LabelsError):
        parse_labels(doc("| pass-01 | pass | | | |\n| pass-01 | fail | 1 | | |\n"))


def test_missing_table_yields_no_rows():
    assert parse_labels("---\nengagement: x\n---\n\nnothing yet\n") == {}


def test_wrong_header_raises():
    with pytest.raises(LabelsError):
        parse_labels("| pass | verdict | critique |\n|---|---|---|\n| pass-01 | pass | ok |\n")
