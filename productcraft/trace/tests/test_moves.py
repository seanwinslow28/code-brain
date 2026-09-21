"""The `## Moves` section every artifact closes with (#272 decision 4).

Grammar, one line per move:
    - kept — <upstream item> from <source>
    - added — <new item> from <source>
    - split — <upstream item> → <child>, <child> from <source>
    - merged — <upstream item> + <upstream item> → <item> from <source>
    - dropped — <upstream item> from <source>; <why>
The Strategist's origin draft writes "origin draft, no upstream — leaned on: …".
"""
from tracekit.moves import extract_ids, parse_moves

ART = """---
id: pc-eng-000.discovery
---

## Part 1

text

## Moves

- kept — O1 from pc-eng-000.strategy
- kept — O3 "the callback scramble" from pc-eng-000.strategy
- added — E1–E5 from interviews 1–8
- split — OC-1 → OC-1a, OC-1b from pc-eng-000.strategy
- merged — O2 + O5 → O2 from pc-eng-000.strategy
- dropped — Action 4 from pc-eng-000.strategy; no source survived the split

meter: claude-opus-5 · 240100 in · 41 min
"""


def test_counts_by_op():
    mv = parse_moves(ART)
    assert mv.counts() == {"kept": 2, "added": 1, "split": 1, "merged": 1, "dropped": 1}
    assert mv.origin is False


def test_lines_carry_op_item_source():
    mv = parse_moves(ART)
    kept = mv.lines[0]
    assert (kept.op, kept.item, kept.source) == ("kept", "O1", "pc-eng-000.strategy")


def test_split_names_children():
    mv = parse_moves(ART)
    split = [m for m in mv.lines if m.op == "split"][0]
    assert split.item == "OC-1"
    assert split.children == ["OC-1a", "OC-1b"]


def test_merged_names_every_source_item_and_the_result():
    mv = parse_moves(ART)
    merged = [m for m in mv.lines if m.op == "merged"][0]
    assert merged.items == ["O2", "O5"]
    assert merged.result == "O2"


def test_dropped_keeps_its_why():
    mv = parse_moves(ART)
    dropped = [m for m in mv.lines if m.op == "dropped"][0]
    assert dropped.item == "Action 4"
    assert dropped.why == "no source survived the split"


def test_origin_draft():
    mv = parse_moves("## Moves\n\norigin draft, no upstream — leaned on: Rumelt's kernel; the brief §2\n\nmeter: x\n")
    assert mv.origin is True
    assert mv.leaned_on == ["Rumelt's kernel", "the brief §2"]
    assert mv.lines == []


def test_unknown_op_is_reported_not_swallowed():
    mv = parse_moves("## Moves\n\n- tweaked — O1 from x\n- kept — O2 from x\n")
    assert mv.errors == ["line 3: unknown move `tweaked` (kept | added | split | merged | dropped)"]
    assert mv.counts()["kept"] == 1


def test_line_without_source_is_reported():
    mv = parse_moves("## Moves\n\n- kept — O1\n")
    assert mv.errors and "names no source" in mv.errors[0]


def test_no_moves_section_returns_none():
    assert parse_moves("## Part 1\n\ntext\n") is None


def test_extract_ids_expands_ranges_and_suffixes():
    assert extract_ids("E1–E5") == ["E1", "E2", "E3", "E4", "E5"]
    assert extract_ids("OC-1a and OC-1b") == ["OC-1a", "OC-1b"]
    assert extract_ids("Action 4") == []
    assert extract_ids("B1-B3 with appetites") == ["B1", "B2", "B3"]


# --------------------------------------------------------------------------- #
# #297 · the section is declared machine-read in a comment block
# --------------------------------------------------------------------------- #

COMMENT_BLOCK = """## Moves

<!-- MACHINE-READ. Move lines only, one per line, from the five-op grammar.
     A sentence of prose here is a malformed line and a finding, not a note. -->

- kept — O1 from pc-eng-001.strategy
"""


def test_a_multi_line_comment_block_is_not_read_as_moves():
    mv = parse_moves(COMMENT_BLOCK)
    assert mv.errors == []
    assert [m.op for m in mv.lines] == ["kept"]


def test_prose_outside_a_comment_is_still_a_malformed_line():
    mv = parse_moves("## Moves\n\nThe seat rewrote the roadmap around the new constraint.\n")
    assert len(mv.errors) == 1
    assert "not a move line" in mv.errors[0]
