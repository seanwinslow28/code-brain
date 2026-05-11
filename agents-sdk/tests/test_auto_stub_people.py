"""Tests for the auto_stub_people SessionEnd hook script.

Verify the two filters that protect against creating garbage stubs:
  1. Wikilinks must appear in `author:` YAML frontmatter.
  2. Target must match the person-name shape (1-3 capitalized tokens).

Plus dedup against existing people/ files and the per-run safety cap.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Import the script module directly. The scripts/ folder isn't on the
# default Python path; sys.path.insert below makes the import work at
# test runtime even though static analyzers can't resolve it.
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import auto_stub_people as asp  # type: ignore[import-not-found]  # noqa: E402


def _touch(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _retarget(tmp_vault: Path) -> tuple[Path, Path]:
    """Repoint the module's VAULT_ROOT and PEOPLE_DIR globals at a tmp vault."""
    people_dir = tmp_vault / "40_knowledge" / "people"
    asp.VAULT_ROOT = tmp_vault
    asp.PEOPLE_DIR = people_dir
    asp.LOG_FILE = tmp_vault / "90_system" / "agent-logs" / "auto-stub-people.log"
    return tmp_vault, people_dir


def test_slugify_handles_diacritics() -> None:
    assert asp._slugify("Ali Çevik") == "ali-cevik"
    assert asp._slugify("Brian Danga") == "brian-danga"
    assert asp._slugify("RT Watson") == "rt-watson"


def test_extract_author_wikilinks_inline() -> None:
    text = '---\nauthor: "[[Inline Author]]"\n---\nBody'
    assert asp._extract_author_wikilinks(text) == ["Inline Author"]


def test_extract_author_wikilinks_list() -> None:
    text = '---\nauthor:\n  - "[[First Author]]"\n  - "[[Second Author]]"\ntitle: X\n---\nBody'
    assert asp._extract_author_wikilinks(text) == ["First Author", "Second Author"]


def test_extract_skips_non_author_wikilinks() -> None:
    """Wikilinks in body or in non-author frontmatter fields must NOT match."""
    text = (
        "---\n"
        'related:\n  - "[[Some Concept]]"\n'
        "title: X\n"
        "---\n"
        "Body refers to [[Random Person]] in prose.\n"
    )
    assert asp._extract_author_wikilinks(text) == []


def test_person_name_regex_accepts_real_names() -> None:
    for name in ["Nate", "RT Watson", "Ali Çevik", "Brian Danga", "Mary-Alice McKee", "J.J. Smith"]:
        assert asp._PERSON_NAME_RE.match(name), f"should accept {name!r}"


def test_person_name_regex_rejects_non_persons() -> None:
    for non_person in ["stage", "intent-engineering", "10", "prj-job-hunt-2026", "lowercase name", ""]:
        assert not asp._PERSON_NAME_RE.match(non_person), f"should reject {non_person!r}"


def test_find_candidates_creates_only_for_author_field(tmp_path: Path) -> None:
    vault, _people = _retarget(tmp_path / "vault")
    _touch(
        vault / "00_inbox" / "clip-a.md",
        '---\nauthor:\n  - "[[Sample Person]]"\n---\nBody',
    )
    # Wikilink in body / related field should NOT trigger.
    _touch(
        vault / "00_inbox" / "clip-b.md",
        '---\nrelated:\n  - "[[Body Reference]]"\n---\n[[Random Mention]] in prose.',
    )
    candidates = asp.find_candidates()
    assert "Sample Person" in candidates
    assert "Body Reference" not in candidates
    assert "Random Mention" not in candidates


def test_find_candidates_skips_existing_stub_by_filename(tmp_path: Path) -> None:
    vault, people = _retarget(tmp_path / "vault")
    _touch(
        vault / "00_inbox" / "clip.md",
        '---\nauthor:\n  - "[[Test Person]]"\n---\nBody',
    )
    _touch(people / "test-person.md", '---\ntitle: "Test Person"\n---\nExisting')
    candidates = asp.find_candidates()
    assert "Test Person" not in candidates


def test_find_candidates_skips_existing_stub_by_title(tmp_path: Path) -> None:
    """Different filename, same title — should still dedup."""
    vault, people = _retarget(tmp_path / "vault")
    _touch(
        vault / "00_inbox" / "clip.md",
        '---\nauthor:\n  - "[[Quirky Name]]"\n---\nBody',
    )
    # Same title, different slug — should still be detected as existing.
    _touch(people / "qn.md", '---\ntitle: "Quirky Name"\n---\nExisting')
    candidates = asp.find_candidates()
    assert "Quirky Name" not in candidates


def test_find_candidates_filters_non_person_shape(tmp_path: Path) -> None:
    vault, _people = _retarget(tmp_path / "vault")
    # Garbage wikilinks in author field — common web-clip artifacts.
    _touch(
        vault / "00_inbox" / "clip.md",
        '---\nauthor:\n  - "[[stage]]"\n  - "[[10]]"\n  - "[[intent-engineering]]"\n---\nBody',
    )
    candidates = asp.find_candidates()
    assert candidates == {}


def test_create_stubs_writes_file_with_correct_frontmatter(tmp_path: Path) -> None:
    vault, people = _retarget(tmp_path / "vault")
    _touch(
        vault / "00_inbox" / "clip.md",
        '---\nauthor:\n  - "[[New Person]]"\n---\nBody',
    )
    created = asp.create_stubs(asp.find_candidates())
    assert len(created) == 1
    stub_path = created[0]
    assert stub_path.exists()
    body = stub_path.read_text(encoding="utf-8")
    assert 'title: "New Person"' in body
    assert "type: person" in body
    assert "status: unverified" in body
    assert "00_inbox/clip.md" in body


def test_create_stubs_dry_run_does_not_write(tmp_path: Path) -> None:
    vault, _people = _retarget(tmp_path / "vault")
    _touch(
        vault / "00_inbox" / "clip.md",
        '---\nauthor:\n  - "[[Dry Run Person]]"\n---\nBody',
    )
    created = asp.create_stubs(asp.find_candidates(), dry_run=True)
    assert len(created) == 1
    assert not created[0].exists()


def test_safety_cap_bails_on_excess(tmp_path: Path) -> None:
    vault, _people = _retarget(tmp_path / "vault")
    # Plant MAX+5 author candidates with names that pass the person regex.
    # (Single-word capitalized names — Alphaone / Alphatwo / ...)
    word = lambda n: "Alpha" + "abcdefghijklmno"[n].upper() + "test"  # e.g. AlphaAtest  # noqa: E731
    authors = "\n".join(
        f'  - "[[{word(i)}]]"' for i in range(asp._MAX_STUBS_PER_RUN + 5)
    )
    _touch(vault / "00_inbox" / "bulk.md", f"---\nauthor:\n{authors}\n---\nBody")
    candidates = asp.find_candidates()
    assert len(candidates) > asp._MAX_STUBS_PER_RUN
    created = asp.create_stubs(candidates)
    assert created == []  # safety cap engaged — no writes at all


def test_skips_files_inside_people_folder(tmp_path: Path) -> None:
    """Stubs themselves can reference [[Other Person]] in their bodies, but
    the author scan must not recurse into people/ to avoid stub-cycles."""
    vault, people = _retarget(tmp_path / "vault")
    _touch(
        people / "alice.md",
        '---\ntitle: "Alice"\nauthor:\n  - "[[Bob]]"\n---\nBody',
    )
    candidates = asp.find_candidates()
    assert "Bob" not in candidates


def test_skips_node_modules(tmp_path: Path) -> None:
    """Vendored npm packages must not pollute the scan."""
    vault, _people = _retarget(tmp_path / "vault")
    _touch(
        vault / "30_domains" / "node_modules" / "pkg" / "README.md",
        '---\nauthor:\n  - "[[Vendored Person]]"\n---\nBody',
    )
    candidates = asp.find_candidates()
    assert "Vendored Person" not in candidates
