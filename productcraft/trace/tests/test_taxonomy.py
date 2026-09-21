"""taxonomy.md — rung 1's tracked vocabulary, and the rung-0 line that enforces it.

The codes ratified on #296 clause 8, landed on #298: a lone `manufactured` code
with no instances invites every unwelcome finding to be filed under it, so the
process-waste family is written down and the serious code has to quote what it
indicts.
"""
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, run_checks
from tracekit.engagement import load_engagement
from tracekit.labels import Label
from tracekit.taxonomy import (
    DEFAULT_TAXONOMY_PATH, Taxonomy, critique_quotes, load_taxonomy, parse_taxonomy,
)

@pytest.fixture
def eng(tmp_path):
    return load_engagement(build(tmp_path / "pc-eng-000-callboard"))


TABLE = (
    "| code | family | a label with this code says | quote |\n"
    "|---|---|---|---|\n"
    "| `manufactured` | process-waste | evidence does not support it | **required** |\n"
    "| `kit-induced` | process-waste | a template made correct work read as a defect | — |\n"
)


# --------------------------------------------------------------------------- #
# the file
# --------------------------------------------------------------------------- #


def test_the_studios_own_taxonomy_carries_the_process_waste_family():
    tax = load_taxonomy()
    assert tax.open
    assert set(tax.codes) == {"manufactured", "stale-restatement", "overstated-scope", "kit-induced"}
    assert all(c.family == "process-waste" for c in tax.codes.values())


def test_only_manufactured_requires_a_quote():
    tax = load_taxonomy()
    assert tax.codes["manufactured"].quote_required
    assert not any(c.quote_required for k, c in tax.codes.items() if k != "manufactured")


def test_the_default_path_is_the_kits_own_folder():
    assert DEFAULT_TAXONOMY_PATH == Path(__file__).resolve().parents[1] / "taxonomy.md"
    assert DEFAULT_TAXONOMY_PATH.is_file()


def test_prose_tables_elsewhere_in_the_file_are_ignored():
    text = "| a | b |\n|---|---|\n| 1 | 2 |\n\n" + TABLE
    assert set(parse_taxonomy(text).codes) == {"manufactured", "kit-induced"}


def test_a_missing_file_is_an_unopened_rung_not_a_crash():
    tax = load_taxonomy(Path("/nowhere/taxonomy.md"))
    assert not tax.open and tax.codes == {}


def test_a_file_with_no_code_table_has_no_codes():
    assert not parse_taxonomy("# taxonomy\n\nnothing yet\n").open


def test_a_quotation_is_one_a_reader_can_go_and_find():
    assert critique_quotes('the audit said "no pointer exists" and one does')
    assert critique_quotes("it indicts `Part 3 — Evidence` with nothing behind it")
    assert not critique_quotes("the finding is unsupported by anything it names")
    assert not critique_quotes('a bare "" pair is not a quotation')


# --------------------------------------------------------------------------- #
# rung-0 line 10
# --------------------------------------------------------------------------- #


def codes_check(eng, labels, tax=None):
    eng.labels = {l.pass_id: l for l in labels}
    checks = run_checks(eng, tax if tax is not None else parse_taxonomy(TABLE))
    c = checks[9]
    assert c.name == CHECK_NAMES[9]
    return c


def test_a_blank_column_is_the_normal_state(eng):
    c = codes_check(eng, [Label("pass-01", "pass", None, "reads clean", "")])
    assert c.ok and c.n_total == 0
    assert any("no failure codes yet" in n for n in c.notes)


def test_a_code_in_the_taxonomy_passes(eng):
    c = codes_check(eng, [Label("pass-01", "fail", 1, "the template forced it", "kit-induced")])
    assert c.ok and c.count == "1 of 1"


def test_a_code_outside_the_taxonomy_is_free_text_and_a_finding(eng):
    c = codes_check(eng, [Label("pass-01", "fail", 1, "vibes", "too-adversarial")])
    assert not c.ok
    assert "is not in the taxonomy" in c.findings[0]
    assert "kit-induced" in c.findings[0]


def test_manufactured_without_a_quote_is_a_finding(eng):
    c = codes_check(eng, [Label("pass-01", "fail", 1, "it invented the defect", "manufactured")])
    assert not c.ok
    assert "must quote the text it indicts" in c.findings[0]


def test_manufactured_with_a_quote_passes(eng):
    c = codes_check(eng, [Label("pass-01", "fail", 1, 'claims "no evidence exists"; the pointer opens', "manufactured")])
    assert c.ok and c.count == "1 of 1"


def test_a_code_with_no_taxonomy_file_is_a_finding_naming_the_path(eng):
    c = codes_check(eng, [Label("pass-01", "fail", 1, "x", "kit-induced")], tax=Taxonomy({}, Path("/nowhere/taxonomy.md")))
    assert not c.ok
    assert "no taxonomy file to draw from" in c.findings[0] and "/nowhere/taxonomy.md" in c.findings[0]
