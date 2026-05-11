from datetime import datetime
from lib.job_types import Posting, ScoringResult


def test_posting_minimal_construction():
    p = Posting(
        source="remoteok",
        source_role_id="123",
        url="https://example.com/job/123",
        company="Acme",
        title="Product Manager",
        location=None,
        salary_disclosed=None,
        posted_at=None,
        description="A PM role.",
    )
    assert p.source == "remoteok"
    assert p.description == "A PM role."


def test_posting_full_construction():
    p = Posting(
        source="greenhouse:anthropic",
        source_role_id="role-9",
        url="https://example.com",
        company="Anthropic",
        title="PM, Claude Code",
        location="Remote (US)",
        salary_disclosed="$160k-$200k",
        posted_at=datetime(2026, 5, 9, 12, 0),
        description="Long description...",
    )
    assert p.location == "Remote (US)"


def test_scoring_result_construction():
    r = ScoringResult(
        fit_score=4,
        role_band="PM",
        rationale="Strong fit.",
        concerns=["YOE floor"],
        fit_dimensions={"role_band_fit": 4, "geo_fit": 5, "industry_fit": 5, "yoe_fit": 3},
    )
    assert r.fit_score == 4
    assert r.role_band == "PM"
    assert r.fit_dimensions["geo_fit"] == 5
