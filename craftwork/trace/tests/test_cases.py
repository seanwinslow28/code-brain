"""trace/cases.md — the guided-reading content, keyed to a pass and hashed at writing time."""
import hashlib
from pathlib import Path

import pytest

from tracekit.cases import ASSIST_LEVELS, load_cases, parse_cases
from tracekit.engagement import load_engagement

SOURCE_TEXT = """# Audit of the strategy, revision 3

## Findings

| # | Finding | Severity |
|---|---|---|
| M8 | The plan depends on one final data refresh the contact rules do not allow. | MATERIAL |
"""

EXCERPT = "The plan depends on one final data refresh the contact rules do not allow."


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cases_md(**over) -> str:
    fields = dict(
        assist_a="worked",
        story_a="### Story\n\nSean wants to know whether people come back on rest days. The refresh that would settle it was not allowed.\n\nThe reviewer proposed one change; the owner has not ruled on it.\n",
        sha_a=over.get("sha_a") or sha(SOURCE_TEXT),
        excerpt_a=over.get("excerpt_a") or EXCERPT,
    )
    fields.update({k: v for k, v in over.items() if k in fields})
    return f"""---
engagement: pc-eng-000-callboard
written: 2026-09-20
status: proposed
---

# What happened in this review

Two runs are worth reading closely. One found a missing observation; the other accepted work that already met its requirement.

## Case: Can we tell a rest-day visit from any other visit

pass: pass-10
finding: M8
assist: {fields['assist_a']}
question: What should happen to the days nobody can classify?
options:
  - key: a
    label: Count them as returns
  - key: b
    label: Report them as unknown
sources:
  - path: audits/audit-strategy-r3.md
    sha256: {fields['sha_a']}
    excerpt: "{fields['excerpt_a']}"
    label: M8 · Audit of Strategy revision 3

{fields['story_a']}
### Hint

Ask what carries the workout data to the app before anyone judges the visit.

### Reveal

The reviewer ruled the days unknown and said so in the record.

### Your turn

Write, in your own words, what evidence you would need to change that answer.

### Terms

- rest day: a day with no recorded workout.

## Case: Whether the plan says who will build the record

pass: pass-14
finding: none
assist: independent
question: Does this part need a change before it proceeds?
options:
  - key: a
    label: Yes, require a named owner
  - key: b
    label: No, the owner is already named
sources:
  - path: audits/audit-strategy-r3.md
    sha256: {fields['sha_a']}
    excerpt: "Findings"
    label: The findings table

### Story

You are reading the plan for collecting the pilot's information.

The table has no owner column. The plan names Delivery elsewhere.

### Reveal

The reviewer accepted it, because the template never asked for that column.

### Your turn

Say which requirement you were applying.
"""


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    d = tmp_path / "pc-eng-000-callboard"
    (d / "trace").mkdir(parents=True)
    (d / "audits").mkdir()
    (d / "audits" / "audit-strategy-r3.md").write_text(SOURCE_TEXT, encoding="utf-8")
    return d


def write_cases(eng_dir: Path, text: str) -> None:
    (eng_dir / "trace" / "cases.md").write_text(text, encoding="utf-8")


def test_parses_a_well_formed_file(eng_dir):
    write_cases(eng_dir, cases_md())
    doc = load_cases(load_engagement(eng_dir))
    assert doc.errors == []
    assert doc.status == "proposed" and doc.written == "2026-09-20"
    assert doc.intro.startswith("Two runs are worth reading closely")
    assert [c.assist for c in doc.cases] == ["worked", "independent"]
    a, b = doc.cases
    assert a.title == "Can we tell a rest-day visit from any other visit"
    assert a.pass_id == "pass-10" and a.finding == "M8" and a.key == "pass-10-m8"
    assert [o.key for o in a.options] == ["a", "b"]
    assert len(a.story) == 2 and a.hint.startswith("Ask what carries")
    assert a.your_turn.startswith("Write, in your own words")
    assert a.terms == [("rest day", "a day with no recorded workout.")]
    assert b.finding == "" and b.assist == "independent"
    assert all(level in ASSIST_LEVELS for level in (a.assist, b.assist))


def test_a_matching_hash_resolves_the_excerpt_to_its_line(eng_dir):
    write_cases(eng_dir, cases_md())
    doc = load_cases(load_engagement(eng_dir))
    s = doc.cases[0].sources[0]
    assert s.state == "current" and s.shows_excerpt and not s.qualified
    assert s.line == 7 and s.current_sha256 == s.sha256


def test_a_missing_story_is_a_reported_error(eng_dir):
    write_cases(eng_dir, cases_md(story_a="### Hint\n\nNo story was written.\n"))
    doc = load_cases(load_engagement(eng_dir))
    assert len(doc.cases) == 1                      # the second case still renders
    assert any("no `### Story` section" in e for e in doc.errors)


def test_an_unknown_assist_is_a_reported_error(eng_dir):
    write_cases(eng_dir, cases_md(assist_a="spoonfed"))
    doc = load_cases(load_engagement(eng_dir))
    assert len(doc.cases) == 1
    assert any("assist must be one of" in e and "spoonfed" in e for e in doc.errors)


def test_an_excerpt_that_is_not_in_the_file_is_an_error(eng_dir):
    write_cases(eng_dir, cases_md(excerpt_a="A sentence nobody ever wrote into that audit."))
    doc = load_cases(load_engagement(eng_dir))
    s = doc.cases[0].sources[0]
    assert s.state == "excerpt-missing" and s.qualified and not s.shows_excerpt
    assert any("is not in that file" in e for e in doc.errors)


def test_a_changed_source_is_qualified_and_withholds_its_excerpt(eng_dir):
    write_cases(eng_dir, cases_md(sha_a="deadbeef" * 8))
    doc = load_cases(load_engagement(eng_dir))
    s = doc.cases[0].sources[0]
    assert s.state == "changed" and s.qualified is True and s.shows_excerpt is False
    assert "changed since this story was written" in s.qualification
    assert doc.cases[0].qualified is True


def test_a_missing_source_file_is_reported_not_guessed(eng_dir):
    write_cases(eng_dir, cases_md().replace("audits/audit-strategy-r3.md", "audits/gone.md"))
    doc = load_cases(load_engagement(eng_dir))
    assert doc.cases[0].sources[0].state == "missing"
    assert any("is not on disk" in e for e in doc.errors)


def test_no_file_is_not_an_error(eng_dir):
    assert load_cases(load_engagement(eng_dir)) is None


def test_an_independent_case_needs_options_to_answer_with(eng_dir):
    text = cases_md().replace(
        "options:\n  - key: a\n    label: Yes, require a named owner\n  - key: b\n    label: No, the owner is already named\n", "")
    write_cases(eng_dir, text)
    doc = load_cases(load_engagement(eng_dir))
    assert any("at least two options" in e for e in doc.errors)


def test_a_diagram_block_is_read_as_a_small_flow():
    doc = parse_cases(cases_md().replace(
        "### Terms\n\n- rest day: a day with no recorded workout.",
        "### Diagram\n\n- App visit recorded\n- ? Enough final workout data\n- no: Report the day as unknown\n- yes: Apply the rest-day rule\n"))
    assert doc.cases[0].diagram == [
        ("step", "", "App visit recorded"),
        ("decision", "", "Enough final workout data"),
        ("branch", "no", "Report the day as unknown"),
        ("branch", "yes", "Apply the rest-day rule"),
    ]
