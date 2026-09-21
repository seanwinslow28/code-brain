"""Entry-id allocation — the coordinator helper the first engagement wanted (#297)."""
from pathlib import Path

import pytest

from synth import build
from tracekit.engagement import load_engagement
from tracekit.ledger import entry_ids, next_entry_id


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def test_the_next_id_follows_the_high_water_mark(eng_dir):
    assert next_entry_id(eng_dir) == "pc-eng-000.d11"


def test_a_clean_engagement_has_no_gaps_and_nothing_unwritten(eng_dir):
    ids = entry_ids(eng_dir)
    assert ids.gaps == []
    assert ids.unwritten == []
    assert len(ids.on_disk) == 10


def test_an_id_reserved_by_a_record_is_claimed_even_with_no_file(eng_dir):
    """A reserved block is why the first engagement left gaps: never hand one out twice."""
    rec = sorted((eng_dir / "trace").glob("pass-01-*.md"))[0]
    rec.write_text(rec.read_text().replace("  - id: pc-eng-000.d02", "  - id: pc-eng-000.d02\n  - id: pc-eng-000.d14"))
    ids = entry_ids(eng_dir)
    assert ids.next_id == "pc-eng-000.d15"
    assert ids.unwritten == [14]
    assert ids.reserved[14] == "pass-01"
    assert ids.gaps == [11, 12, 13]
    assert "never reused" in ids.report()


def test_an_entry_a_pass_recorded_but_never_wrote_is_reported_as_unwritten(eng_dir):
    """At Close this is either a gap to leave alone or an entry someone forgot to write."""
    sorted(eng_dir.glob("d04-*.md"))[0].unlink()
    ids = entry_ids(eng_dir)
    assert ids.unwritten == [4]
    assert ids.reserved[4] == "pass-05"
    assert ids.next_id == "pc-eng-000.d11"
    assert "not written" in ids.report()


def test_ids_are_read_from_a_loaded_engagement_too(eng_dir):
    eng = load_engagement(eng_dir)
    assert entry_ids(eng).next_id == next_entry_id(eng_dir)
