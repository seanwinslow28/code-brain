"""The tracked lint report must never carry SOUL-derived text (2026-09-03).

Regression guard for a live near-miss. `vault/health/2026-08-30-lint-report.md`
was staged for commit to this PUBLIC repo with a `soul-tier-a-conflict` finding
quoting the job-hunt SOUL verbatim — a base-salary relocation threshold and a
named target employer. `git grep` confirmed that figure was in no committed
file, so it would have been first exposure. CLAUDE.md rule 9 forbids writing
income or employer data into tracked files, which is why the fixtures below are
synthetic: this test file is tracked in the same public repo.

The original ticket proposed redacting the `tier_a_item` field. That is not
sufficient: the model reproduces SOUL content in its free-prose `detail` too,
and the 08-30 finding leaked through BOTH. So the whole KIND leaves the tracked
report, and a verbatim-quote scrub backstops every other kind.
"""

from __future__ import annotations

from pathlib import Path

from agents.knowledge_lint import (
    LintIssue,
    LintSeverity,
    SOUL_CONFLICT_KIND,
    Tier1Report,
    format_report,
    format_private_sidecar,
    partition_private_issues,
    scrub_soul_quotes,
    write_private_sidecar,
)


# A SYNTHETIC stand-in with the same SHAPE as the 2026-08-30 finding: a quoted
# `tier_a_item` followed by model prose that restates the same private values.
#
# The real strings are deliberately NOT reproduced here. This file is tracked in
# the same public repo, so pasting the actual salary figure and employer name
# into a test would republish exactly what the code under test exists to
# withhold. The shape is what the assertions need; the values are invented.
LEAKING_DETAIL = (
    "tier_a_item=\"SOUL — job-hunt-2026: 'Remote is preferred but not absolute. "
    "Two override conditions: a role at Fictional Example Corp specifically, or "
    "any role with $999k+/yr base anywhere — would relocate for either.'\": The "
    "concept describes a reliability contract based on error budgets. The conflict "
    "arises if applied to career decisions, creating a false equivalence between "
    "technical reliability metrics and career relocation thresholds, which are "
    "defined strictly by company (Fictional Example Corp) or salary ($999k+)."
)

# Probes drawn from BOTH halves of the fixture: the quoted `tier_a_item` and the
# model's own prose. Redacting only the former leaves the latter — which is why
# the original ticket's "redact tier_a_item" proposal was not sufficient.
LEAK_PROBES = (
    "$999k",
    "Fictional Example Corp",
    "Remote is preferred but not absolute",
    "would relocate for either",
)


def _leaking_issue() -> LintIssue:
    return LintIssue(
        kind=SOUL_CONFLICT_KIND,
        severity=LintSeverity.HIGH,
        file=Path("knowledge/concepts/tier-a-relocation-exception-clauses.md"),
        detail=LEAKING_DETAIL,
        tier=2,
    )


def _mundane_issue() -> LintIssue:
    return LintIssue(
        kind="orphan",
        severity=LintSeverity.LOW,
        file=Path("knowledge/concepts/a.md"),
        detail="no inbound links",
    )


# ─── the property that matters ───────────────────────────────────────────────

def test_public_report_carries_no_fragment_of_the_2026_08_30_leak() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[]), tier2=[_leaking_issue()], today="2026-08-30"
    )
    for probe in LEAK_PROBES:
        assert probe not in report, f"tracked report still leaks {probe!r}"


def test_leak_probes_cover_the_models_prose_not_just_the_quoted_field() -> None:
    """Guards the guard: if someone 'fixes' this by redacting only
    `tier_a_item`, these probes must still catch the prose half."""
    prose_half = LEAKING_DETAIL.split('":', 1)[1]
    assert "Fictional Example Corp" in prose_half and "$999k" in prose_half


# ─── the public report stays useful ──────────────────────────────────────────

def test_public_report_keeps_the_file_path_which_is_already_public() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[]), tier2=[_leaking_issue()], today="2026-08-30"
    )
    assert "tier-a-relocation-exception-clauses.md" in report
    assert SOUL_CONFLICT_KIND in report


def test_severity_counts_are_unaffected_so_the_morning_brief_still_works() -> None:
    """lib/lint_report.py:vault_health_summary parses `## HIGH (n)`. Withheld
    findings must stay counted or the fleet under-reports its own health."""
    report = format_report(
        tier1=Tier1Report(issues=[]),
        tier2=[_leaking_issue(), _leaking_issue()],
        today="2026-08-30",
    )
    assert "## HIGH (2)" in report


def test_public_report_names_the_sidecar_so_the_detail_is_findable() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[]),
        tier2=[_leaking_issue()],
        today="2026-08-30",
        private_sidecar_path=Path("vault/health/private/2026-08-30-private-findings.md"),
    )
    assert "vault/health/private/2026-08-30-private-findings.md" in report


def test_report_without_soul_findings_gains_no_withholding_note() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[_mundane_issue()]), tier2=[], today="2026-08-30"
    )
    assert "withheld" not in report
    assert "no inbound links" in report, "ordinary details must render in full"


# ─── the sidecar keeps the analytical value, locally ─────────────────────────

def test_sidecar_retains_the_full_detail_the_public_report_dropped() -> None:
    sidecar = format_private_sidecar([_leaking_issue()], today="2026-08-30")
    for probe in LEAK_PROBES:
        assert probe in sidecar


def test_sidecar_holds_only_soul_findings() -> None:
    _, soul = partition_private_issues([_mundane_issue(), _leaking_issue()])
    sidecar = format_private_sidecar(soul, today="2026-08-30")
    assert "no inbound links" not in sidecar


def test_sidecar_warns_the_reader_it_is_local_only() -> None:
    sidecar = format_private_sidecar([_leaking_issue()], today="2026-08-30")
    assert "LOCAL-ONLY" in sidecar


def test_sidecar_is_written_beneath_the_gitignored_private_directory(tmp_path) -> None:
    out = write_private_sidecar(tmp_path, "body", today="2026-08-30")
    assert out == tmp_path / "health" / "private" / "2026-08-30-private-findings.md"
    assert out.read_text(encoding="utf-8") == "body"


def test_partition_preserves_every_issue_across_both_halves() -> None:
    issues = [_mundane_issue(), _leaking_issue(), _mundane_issue()]
    public, soul = partition_private_issues(issues)
    assert len(public) == 2 and len(soul) == 1
    assert len(public) + len(soul) == len(issues), "no finding may be dropped"


# ─── defence in depth: SOUL quoted from some OTHER issue kind ────────────────

SOUL_LINE = (
    "Remote is preferred but not absolute. Two override conditions: a role at "
    "Fictional Example Corp specifically, or any role with $999k+/yr base anywhere."
)


def test_scrub_redacts_verbatim_soul_quoted_by_a_non_soul_issue_kind() -> None:
    """The structural split routes one KIND. This catches a `contradiction`
    detail — or any future kind — that quotes SOUL anyway."""
    report = format_report(
        tier1=Tier1Report(issues=[
            LintIssue(kind="contradiction", severity=LintSeverity.CRITICAL,
                      file=Path("b.md"), detail=f"conflicts with {SOUL_LINE}")
        ]),
        tier2=[], today="2026-08-30",
    )
    assert SOUL_LINE in report, "precondition: the leak is present before scrubbing"
    scrubbed, redactions = scrub_soul_quotes(report, f"- {SOUL_LINE}\n")
    assert redactions == 1
    assert SOUL_LINE not in scrubbed
    assert "[SOUL text redacted]" in scrubbed


def test_scrub_leaves_a_clean_report_untouched() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[_mundane_issue()]), tier2=[], today="2026-08-30"
    )
    scrubbed, redactions = scrub_soul_quotes(report, f"- {SOUL_LINE}\n")
    assert redactions == 0
    assert scrubbed == report


def test_scrub_ignores_soul_lines_too_short_to_fingerprint() -> None:
    """Short SOUL headings like 'Sacred Cows' appear in ordinary prose;
    matching them would redact the report into uselessness."""
    report = "This mentions Sacred Cows in passing."
    scrubbed, redactions = scrub_soul_quotes(report, "- Sacred Cows\n- Tier-A Truths\n")
    assert redactions == 0
    assert scrubbed == report


def test_scrub_tolerates_an_empty_soul_context() -> None:
    """Tier 2 can be gate-skipped, leaving soul_context empty."""
    scrubbed, redactions = scrub_soul_quotes("body", "")
    assert (scrubbed, redactions) == ("body", 0)


# ─── second leak class: findings ABOUT files in gitignored subtrees ──────────
#
# Found 2026-09-03 while backfilling the SOUL split. Ten committed reports name
# files under `vault/knowledge/private/` — e.g. a connection slug reading
# "relocation-flexibility-through-target-role-specs-and-relocation-exception-
# clauses". That subtree is gitignored, so naming the file discloses both its
# existence and its subject. Same side channel that leaked 69 target companies
# through job-feed manifests in 2026-08.

from agents.knowledge_lint import (  # noqa: E402
    PRIVATE_VAULT_PREFIXES,
    is_private_finding,
)

PRIVATE_SLUG = (
    "knowledge/private/connections/"
    "relocation-flexibility-through-target-role-specs-and-relocation-exception-clauses.md"
)


def _private_path_issue(path: str = PRIVATE_SLUG) -> LintIssue:
    return LintIssue(
        kind="orphan", severity=LintSeverity.LOW, file=Path(path), detail=path
    )


def test_finding_about_a_gitignored_file_is_classified_private() -> None:
    assert is_private_finding(_private_path_issue()) is True


def test_ordinary_concept_finding_is_not_classified_private() -> None:
    assert is_private_finding(_mundane_issue()) is False


def test_absolute_tier1_paths_are_classified_by_their_vault_relative_part() -> None:
    """Tier-1 findings carry absolute paths; Tier-2 vault-relative ones. Both
    shapes must be recognised or the leak survives in half the report."""
    absolute = _private_path_issue(
        f"/Users/seanwinslow/Code-Brain/code-brain/vault/{PRIVATE_SLUG}"
    )
    assert is_private_finding(absolute) is True


def test_public_report_withholds_the_private_path_itself() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[_private_path_issue()]), tier2=[], today="2026-08-30"
    )
    assert "relocation-flexibility" not in report
    assert "knowledge/private/" not in report
    assert "<private vault path withheld>" in report


def test_withheld_private_path_findings_stay_counted() -> None:
    """Omitting the rows entirely would make the fleet under-report its own
    health. The row survives; only path and detail are withheld."""
    report = format_report(
        tier1=Tier1Report(issues=[_private_path_issue(), _private_path_issue()]),
        tier2=[], today="2026-08-30",
    )
    assert "## LOW (2)" in report


def test_sidecar_retains_the_private_path_for_local_reading() -> None:
    _, private = partition_private_issues([_private_path_issue()])
    sidecar = format_private_sidecar(private, today="2026-08-30")
    assert "relocation-flexibility" in sidecar


def test_every_private_prefix_is_actually_gitignored() -> None:
    """PRIVATE_VAULT_PREFIXES mirrors .gitignore's PRIVATE LAYER. If the two
    drift, this module starts publishing paths it believes are safe."""
    import subprocess

    repo = Path(__file__).parent.parent.parent
    if not (repo / ".git").exists():
        import pytest as _pytest
        _pytest.skip("not a git checkout")
    for prefix in PRIVATE_VAULT_PREFIXES:
        probe = f"vault/{prefix}probe.md"
        result = subprocess.run(
            ["git", "check-ignore", "-q", probe], cwd=repo, capture_output=True
        )
        assert result.returncode == 0, (
            f"{prefix!r} is in PRIVATE_VAULT_PREFIXES but {probe} is NOT "
            "gitignored — the two have drifted"
        )


def test_both_leak_classes_land_in_one_sidecar() -> None:
    issues = [_mundane_issue(), _leaking_issue(), _private_path_issue()]
    public, private = partition_private_issues(issues)
    assert len(public) == 1 and len(private) == 2
    sidecar = format_private_sidecar(private, today="2026-08-30")
    assert "$999k" in sidecar and "relocation-flexibility" in sidecar


# ─── third leak shape: a private path inside a PUBLIC file's detail ──────────

from agents.knowledge_lint import scrub_private_paths  # noqa: E402


def test_private_path_in_a_public_findings_detail_is_scrubbed() -> None:
    """`is_private_finding` only inspects `file`. A broken wikilink on a PUBLIC
    note can still name a private path in its detail — exactly how one such
    reference survived the 2026-09-03 backfill."""
    row = (
        "- **broken-wikilink** (T1): `/Users/s/vault/40_knowledge/public.md` "
        "— 20_projects/prj-job-hunt-2026/campaign-strategy"
    )
    scrubbed, redactions = scrub_private_paths(row)
    assert redactions == 1
    assert "prj-job-hunt-2026" not in scrubbed
    assert "40_knowledge/public.md" in scrubbed, "public paths must survive"


def test_path_scrub_does_not_redact_the_sidecar_pointer() -> None:
    """The header note names `vault/health/private/...`. Redacting it would
    hide the pointer to the withheld detail."""
    note = "full detail is in `vault/health/private/2026-08-30-private-findings.md`"
    scrubbed, redactions = scrub_private_paths(note)
    assert redactions == 0
    assert scrubbed == note


def test_path_scrub_leaves_an_entirely_public_report_untouched() -> None:
    report = format_report(
        tier1=Tier1Report(issues=[_mundane_issue()]), tier2=[], today="2026-08-30"
    )
    scrubbed, redactions = scrub_private_paths(report)
    assert redactions == 0
    assert scrubbed == report
