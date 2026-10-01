"""Strip-then-hash (#326): the binding names the process parts, the copy crosses without them, the hash holds."""
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from tracekit.freeze import BindingError, freeze, read_rules, strip, unstamp, verify

TRACE = Path(__file__).resolve().parents[1]
REPO = TRACE.parents[1]
AT = "2026-10-01T19:00:00+02:00"

BINDING = """# A binding

Prose first; only the fenced block is read.

```strip
heading: ## Moves
heading: ## Loopbacks
heading-ending: ## dispositioned
heading-tag: [Δ
paragraph: **Repair note
paragraph: meter:
key: audit
```
"""

ARTIFACT = """---
id: pc-eng-009.strategy
seat: product-strategist
audit: landed 2026-10-01 → pc-eng-009.audit-strategy (LOOPBACK, 2 material)
  → repaired at revision 2
revision: 2
---

**Repair note (revision 2, rule 9).** M1 and M2 repaired; nothing reversed.

**Read this first.** Nobody has been asked anything yet.

## Diagnosis

The kernel. A line about **Repair note** mid-paragraph stays.

### A subsection [Δ g2 — C1 / C2]

Content under a tagged heading stays.

## Loopbacks to the Strategist

- L1 sent back on 2026-10-01.

### Inside the loopback

Still the loopback.

## Material findings dispositioned

- M1 shipped.

## Non-goals

```markdown
## Moves
paragraph inside a fence stays
**Repair note in a fence stays
```

## Moves

- kept — O1 from pc-eng-009.strategy

meter: claude-opus-5-5 · tokens UNMEASURED · wall-clock UNMEASURED
"""


@pytest.fixture
def binding(tmp_path) -> Path:
    p = tmp_path / "binding.md"
    p.write_text(BINDING)
    return p


@pytest.fixture
def artifact(tmp_path) -> Path:
    p = tmp_path / "artifacts" / "strategy-pov.md"
    p.parent.mkdir()
    p.write_text(ARTIFACT)
    return p


def test_strips_exactly_what_the_binding_names(binding):
    out, removed = strip(ARTIFACT, read_rules(binding))
    assert "Loopbacks" not in out and "L1 sent back" not in out and "Inside the loopback" not in out
    assert "Material findings dispositioned" not in out and "M1 shipped" not in out
    assert "**Repair note (revision 2" not in out
    assert "audit:" not in out and "repaired at revision 2" not in out
    assert "meter:" not in out and "- kept — O1" not in out
    for kept in ("id: pc-eng-009.strategy", "revision: 2", "**Read this first.**", "## Diagnosis",
                 "A line about **Repair note** mid-paragraph stays.", "## Non-goals",
                 "Content under a tagged heading stays."):
        assert kept in out, kept
    # The meter line sits under ## Moves, so it leaves with the section, not as a paragraph.
    assert removed == [
        "key: audit",
        "## Loopbacks to the Strategist",
        "## Material findings dispositioned",
        "## Moves",
        "tag: [Δ ×1",
        "paragraph: **Repair note",
    ]


def test_a_tag_comes_off_the_heading_and_the_heading_stays(binding):
    out, _ = strip(ARTIFACT, read_rules(binding))
    assert "### A subsection\n" in out
    assert "[Δ" not in out


def test_fenced_code_is_never_matched(binding):
    out, _ = strip(ARTIFACT, read_rules(binding))
    assert "```markdown\n## Moves\nparagraph inside a fence stays\n**Repair note in a fence stays\n```" in out


def test_a_heading_name_matches_whole_words_only(tmp_path):
    b = tmp_path / "b.md"
    b.write_text("```strip\nheading: ## Move\n```\n")
    out, removed = strip("## Moves\n\nkept\n", read_rules(b))
    assert out == "## Moves\n\nkept\n" and removed == []


def test_a_section_runs_to_the_next_heading_of_the_same_or_higher_level(binding):
    text = "# Title\n\n## Moves\n\n### deeper\n\nx\n\n# Next part\n\nkept\n"
    out, _ = strip(text, read_rules(binding))
    assert out == "# Title\n\n# Next part\n\nkept\n"


def test_a_binding_without_a_strip_block_is_refused(tmp_path):
    b = tmp_path / "b.md"
    b.write_text("# A binding that forgot its list\n")
    with pytest.raises(BindingError, match="nothing is stripped by guess"):
        read_rules(b)


@pytest.mark.parametrize("line", ["heading: Moves", "sections: ## Moves", "key:"])
def test_a_malformed_directive_is_refused(tmp_path, line):
    b = tmp_path / "b.md"
    b.write_text(f"```strip\n{line}\n```\n")
    with pytest.raises(BindingError):
        read_rules(b)


def test_freeze_stamps_both_hashes_and_verifies(binding, artifact, tmp_path):
    fc = freeze(artifact, "pc-eng-009.strategy", read_rules(binding), tmp_path / "out", AT)
    assert fc.copy.name == "pc-eng-009.strategy--strategy-pov.md"
    text = fc.copy.read_text()
    head = text.split("\n")[:7]
    assert head[0] == "---"
    assert head[1] == "frozen_from: pc-eng-009.strategy (artifacts/strategy-pov.md)"
    assert head[2] == f"sha256: {fc.sha256}"
    assert head[3] == f"source_sha256: {hashlib.sha256(artifact.read_bytes()).hexdigest()}"
    assert head[4] == f"frozen_at: {AT}"
    assert head[5].startswith('stripped: ["key: audit"')
    assert head[6] == "id: pc-eng-009.strategy"
    stripped, _ = strip(ARTIFACT, read_rules(binding))
    assert unstamp(text) == stripped
    assert fc.sha256 == hashlib.sha256(stripped.encode()).hexdigest()
    v = verify(fc.copy, artifact)
    assert v.ok, v.lines


def test_an_edited_copy_is_hash_drift(binding, artifact, tmp_path):
    fc = freeze(artifact, "pc-eng-009.strategy", read_rules(binding), tmp_path / "out", AT)
    fc.copy.write_text(fc.copy.read_text().replace("Nobody has been asked", "Everybody was asked"))
    v = verify(fc.copy)
    assert not v.ok and "HASH DRIFT" in v.lines[0]


def test_a_source_edited_after_the_freeze_has_moved(binding, artifact, tmp_path):
    fc = freeze(artifact, "pc-eng-009.strategy", read_rules(binding), tmp_path / "out", AT)
    artifact.write_text(ARTIFACT + "\nA later revision.\n")
    v = verify(fc.copy, artifact)
    assert not v.ok and "SOURCE MOVED" in v.lines[-1]
    assert verify(fc.copy).ok   # the copy itself is untouched


def test_a_copy_frozen_verbatim_before_the_rule_still_verifies(artifact, tmp_path):
    """pc-eng-002's six copies (2026-09-30, d191): three stamps, sha256 of the source bytes, no strip."""
    src = artifact.read_bytes()
    digest = hashlib.sha256(src).hexdigest()
    body = artifact.read_text().split("\n", 1)[1]
    legacy = tmp_path / "pc-eng-009.strategy--strategy-pov.md"
    legacy.write_text(f"---\nfrozen_from: pc-eng-009.strategy (artifacts/strategy-pov.md)\nsha256: {digest}\nfrozen_at: {AT}\n{body}")
    assert verify(legacy, artifact).ok


def test_a_source_without_frontmatter_gets_a_stamp_block(binding, tmp_path):
    src = tmp_path / "note.md"
    src.write_text("## Diagnosis\n\nx\n\n## Moves\n\n- kept — a from b\n")
    fc = freeze(src, "pc-eng-009.note", read_rules(binding), tmp_path / "out", AT)
    assert fc.copy.read_text().startswith("---\nfrozen_from:")
    assert unstamp(fc.copy.read_text()) == "## Diagnosis\n\nx\n"
    assert verify(fc.copy, src).ok


def run(*args):
    return subprocess.run([sys.executable, "freeze.py", *map(str, args)], capture_output=True, text=True, cwd=TRACE)


def test_cli_copy_show_verify(binding, artifact, tmp_path):
    out = tmp_path / "handoff" / "outbound" / "artifacts"
    r = run("show", "--binding", binding, artifact)
    assert r.returncode == 0 and "## Moves" in r.stdout and not out.exists()
    r = run("copy", "--binding", binding, "--out", out, "--at", AT, f"{artifact}=pc-eng-009.strategy")
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("| Source id | Frozen copy |")
    assert "| pc-eng-009.strategy | artifacts/pc-eng-009.strategy--strategy-pov.md |" in r.stdout
    copy = out / "pc-eng-009.strategy--strategy-pov.md"
    r = run("verify", f"{copy}={artifact}")
    assert r.returncode == 0 and r.stdout.count("PASS") == 2
    copy.write_text(copy.read_text() + "tampered\n")
    assert run("verify", copy).returncode == 1


def test_cli_refuses_without_a_binding(artifact, tmp_path):
    r = run("copy", "--out", tmp_path, f"{artifact}=pc-eng-009.strategy")
    assert r.returncode == 2 and "--binding" in r.stderr


@pytest.mark.parametrize("binding_path", [
    "productcraft/templates/handoff-binding-systemcraft.md",
    "systemcraft/templates/handoff-return.md",
])
def test_the_tracked_bindings_parse(binding_path):
    rules = read_rules(REPO / binding_path)
    assert (2, "Moves") in rules.headings
    assert "meter:" in rules.paragraphs
