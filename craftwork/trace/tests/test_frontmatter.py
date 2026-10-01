"""The record frontmatter is a YAML subset parsed with the stdlib only.

The Close ritual runs on whatever python3 the session has; nothing may need
installing. The subset is exactly what record-template.md uses: scalars,
lists of scalars, one-level nested mappings, lists of mappings, flow lists.
"""
import pytest

from tracekit.frontmatter import FrontmatterError, parse_yaml_subset, split_frontmatter


def test_split_returns_mapping_and_body():
    doc = "---\npass: pass-01\nstage: 1\n---\n\n## Notes\n\nbody\n"
    fm, body = split_frontmatter(doc)
    assert fm == {"pass": "pass-01", "stage": 1}
    assert body == "\n## Notes\n\nbody\n"


def test_split_without_frontmatter_raises():
    with pytest.raises(FrontmatterError):
        split_frontmatter("## Notes\n\nno header\n")


def test_scalar_types():
    fm = parse_yaml_subset(
        "shadow_of: null\nflag: true\noff: false\nn: 42\nneg: -3\n"
        "when: 2026-10-06T08:12:00-04:00\nname: Agent tool\n"
    )
    assert fm["shadow_of"] is None
    assert fm["flag"] is True and fm["off"] is False
    assert fm["n"] == 42 and fm["neg"] == -3
    assert fm["when"] == "2026-10-06T08:12:00-04:00"  # instants stay strings
    assert fm["name"] == "Agent tool"


def test_quoted_strings_keep_hash_and_colon():
    fm = parse_yaml_subset('launch: "codex exec --model x -c a=b # not a comment"\nnote: \'it: kept\'\n')
    assert fm["launch"] == "codex exec --model x -c a=b # not a comment"
    assert fm["note"] == "it: kept"


def test_trailing_comment_stripped():
    fm = parse_yaml_subset("stage: 1   # fixed train numbering\nkind: draft # a comment\n")
    assert fm == {"stage": 1, "kind": "draft"}


def test_list_of_scalars():
    fm = parse_yaml_subset("withheld:\n  - the drafting conversation\n  - ledger entries of other engagements\n")
    assert fm["withheld"] == ["the drafting conversation", "ledger entries of other engagements"]


def test_nested_mapping():
    fm = parse_yaml_subset("meter:\n  input: 182400\n  output: 21300\n  cached: 96000\nmeter_source: codex footer\n")
    assert fm["meter"] == {"input": 182400, "output": 21300, "cached": 96000}
    assert fm["meter_source"] == "codex footer"


def test_list_of_mappings():
    fm = parse_yaml_subset(
        "inputs:\n  - path: brief.md\n    sha256: abc\n  - path: artifacts/x.md\n    sha256: def\nraw_log: logs/p.jsonl\n"
    )
    assert fm["inputs"] == [{"path": "brief.md", "sha256": "abc"}, {"path": "artifacts/x.md", "sha256": "def"}]
    assert fm["raw_log"] == "logs/p.jsonl"


def test_mixed_list_of_mappings_and_scalars_in_outputs():
    fm = parse_yaml_subset("outputs:\n  - path: artifacts/x.md\n    sha256: abc\n  - id: pc-eng-001.d01\n")
    assert fm["outputs"] == [{"path": "artifacts/x.md", "sha256": "abc"}, {"id": "pc-eng-001.d01"}]


def test_flow_lists():
    fm = parse_yaml_subset("thin_lane: []\nconsulted: [insights-analytics, delivery-execution]\n")
    assert fm["thin_lane"] == []
    assert fm["consulted"] == ["insights-analytics", "delivery-execution"]


def test_key_with_nothing_after_it_is_none():
    fm = parse_yaml_subset("meter:\nmeter_source: UNMEASURED\n")
    assert fm["meter"] is None
    assert fm["meter_source"] == "UNMEASURED"


def test_bad_indentation_raises_with_line_number():
    with pytest.raises(FrontmatterError) as e:
        parse_yaml_subset("meter:\n  input: 1\n output: 2\n")
    assert "line 3" in str(e.value)


def test_duplicate_key_raises():
    with pytest.raises(FrontmatterError):
        parse_yaml_subset("pass: pass-01\npass: pass-02\n")
