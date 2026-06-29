"""Tests for the agent-backfill anti-fabrication backstop (council.discovery.verify_supplement).

After the 2026-06-28 agent-layer pivot, the orchestrating agent writes the `## Web Supplement
(gap-fill)` section by hand (WebSearch/WebFetch on the subscription). The agent judges *relevance*
natively — that's the hard part it does best. This module re-checks the cheap, objective part the
agent could still get wrong: is each cited quote actually VERBATIM at its URL? It reuses the one
shared anti-fabrication primitive (verify.quote_supported_at_url). Trust, but verify.
"""

import pytest
from click.testing import CliRunner

from council.discovery.verify_supplement import (
    SupplementFinding,
    audit_supplement,
    main,
    parse_supplement,
)

_LEDGER = """# Idea Ledger — AI iteration tax

## Blind-spot / Whitespace Map
- No quantified before/after time-tracking data.

## Web Supplement (gap-fill)

> Gap-fill **LEADS** from a solution-side web search of the blind-spot map — verbatim quotes at real
> URLs; relevance agent-vetted. Treat as leads; verify before use.

### No quantified before/after time-tracking data.
- **Query:** `AI rework before after time tracking 2026`
- "37% of the time employees saved using AI tools was lost to rework" — https://example.com/report
- still open — not filled

### A gap nothing was found for.
- **Query:** `obscure gap query 2026`
- still open — not filled

## Sources
- a stray link after the section that MUST be ignored — https://ignored.example.com/x
"""


def test_parse_supplement_extracts_gap_quote_and_url():
    findings = parse_supplement(_LEDGER)
    assert findings == [
        SupplementFinding(
            gap="No quantified before/after time-tracking data.",
            quote="37% of the time employees saved using AI tools was lost to rework",
            url="https://example.com/report",
        )
    ]


def test_parse_supplement_skips_query_and_still_open_lines():
    findings = parse_supplement(_LEDGER)
    # The `**Query:**` line and the two `still open — not filled` lines are not findings.
    assert all("Query" not in f.quote for f in findings)
    assert all("still open" not in f.quote.lower() for f in findings)


def test_parse_supplement_ignores_content_outside_the_section():
    # The stray https://ignored.example.com link lives under a later `## Sources` heading.
    findings = parse_supplement(_LEDGER)
    assert all("ignored.example.com" not in f.url for f in findings)


def test_parse_supplement_returns_empty_when_no_section():
    assert parse_supplement("# Ledger\n\n## Blind-spot / Whitespace Map\n- a gap\n") == []


def test_parse_supplement_recovers_quote_from_legacy_empty_double_quote_format():
    # The deprecated in-CLI backfill sometimes emitted `"" · "real quote" — url`; the leading
    # empty-quote + middot must not leak into the parsed quote (else verbatim check always fails).
    md = (
        "## Web Supplement (gap-fill)\n\n"
        "### A gap\n"
        '- "" · "For every 10 hours of efficiency gained through AI, nearly 4 hours are lost" '
        "— https://example.com/r\n"
    )
    findings = parse_supplement(md)
    assert len(findings) == 1
    assert findings[0].quote == (
        "For every 10 hours of efficiency gained through AI, nearly 4 hours are lost"
    )


@pytest.mark.asyncio
async def test_audit_marks_verbatim_quote_supported():
    async def fetch(url):
        return "Background. 37% of the time employees saved using AI tools was lost to rework, per the report."

    verdicts = await audit_supplement(_LEDGER, fetch=fetch)
    assert len(verdicts) == 1
    assert verdicts[0].supported is True


@pytest.mark.asyncio
async def test_audit_marks_quote_not_on_page_unsupported():
    async def fetch(url):
        return "This page is about something else entirely and does not contain the cited sentence."

    verdicts = await audit_supplement(_LEDGER, fetch=fetch)
    assert len(verdicts) == 1
    assert verdicts[0].supported is False
    assert "not found" in verdicts[0].reason.lower()


@pytest.mark.asyncio
async def test_audit_marks_empty_fetch_unsupported():
    async def fetch(url):
        return ""  # _simple_fetch returns "" on any fetch error / non-HTML / SSRF block

    verdicts = await audit_supplement(_LEDGER, fetch=fetch)
    assert len(verdicts) == 1
    assert verdicts[0].supported is False
    assert "fetch" in verdicts[0].reason.lower()


def test_cli_exits_nonzero_when_any_quote_unsupported(tmp_path, monkeypatch):
    async def fetch(url):
        return "this page does not contain the cited sentence"
    monkeypatch.setattr("council.discovery.verify_supplement._simple_fetch", fetch)

    led = tmp_path / "ledger.md"
    led.write_text(_LEDGER)
    res = CliRunner().invoke(main, [str(led)])
    assert res.exit_code == 1, res.output
    assert "UNSUPPORTED" in res.output


def test_cli_exits_zero_when_all_quotes_supported(tmp_path, monkeypatch):
    async def fetch(url):
        return "37% of the time employees saved using AI tools was lost to rework"
    monkeypatch.setattr("council.discovery.verify_supplement._simple_fetch", fetch)

    led = tmp_path / "ledger.md"
    led.write_text(_LEDGER)
    res = CliRunner().invoke(main, [str(led)])
    assert res.exit_code == 0, res.output


def test_cli_exits_zero_when_no_supplement_section(tmp_path, monkeypatch):
    async def fetch(url):
        raise AssertionError("fetch must not be called when there is nothing to verify")
    monkeypatch.setattr("council.discovery.verify_supplement._simple_fetch", fetch)

    led = tmp_path / "ledger.md"
    led.write_text("# Ledger\n\n## Blind-spot / Whitespace Map\n- a gap\n")
    res = CliRunner().invoke(main, [str(led)])
    assert res.exit_code == 0, res.output
