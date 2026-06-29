from council.discovery.receipts import receipt_line, receipts_legend
from council.discovery.scoring import ScoreBreakdown


def _score(*, distinct_domains=3, recency=0.84, evidence_date="2026-06-20"):
    return ScoreBreakdown(
        composite=62.0, value=0.7, confidence=0.86, importance=0.8, reach=0.55,
        recency=recency, source_corroboration=0.7, consensus_ratio=1.0, intensity=4,
        engagement_sum=300, distinct_sources=5, distinct_domains=distinct_domains,
        evidence_date=evidence_date)


def test_well_corroborated_three_domains():
    assert "well-corroborated · 3 independent domains" in receipt_line(_score(distinct_domains=3))


def test_corroborated_two_domains():
    line = receipt_line(_score(distinct_domains=2))
    assert "corroborated · 2 independent domains" in line
    assert "well-corroborated" not in line and "single-source" not in line


def test_single_source_one_domain_is_singular():
    line = receipt_line(_score(distinct_domains=1))
    assert "single-source · 1 domain" in line
    assert "domains" not in line          # singular noun


def test_uncorroborated_zero_domains():
    assert "uncorroborated · 0 domains" in receipt_line(_score(distinct_domains=0))


def test_caps_at_well_corroborated_no_higher_tier():
    line = receipt_line(_score(distinct_domains=5))
    assert "well-corroborated · 5 independent domains" in line
    assert "very" not in line.lower()     # no invented higher tier


def test_fresh_badge_when_recency_high_and_dated():
    assert "fresh · evidence 2026-06-20" in receipt_line(_score(recency=0.84, evidence_date="2026-06-20"))


def test_recent_badge_between_floor_and_fresh():
    line = receipt_line(_score(recency=0.4, evidence_date="2026-05-20"))
    assert "recent · evidence 2026-05-20" in line
    assert "fresh" not in line


def test_aging_badge_at_floor():
    assert "aging · evidence 2026-04-01" in receipt_line(_score(recency=0.3, evidence_date="2026-04-01"))


def test_undated_never_reads_fresh_even_at_neutral_recency():
    # honesty trap: unparseable date -> scoring sets recency=0.5; must NOT badge 'fresh'
    line = receipt_line(_score(recency=0.5, evidence_date=""))
    assert "undated · no parseable evidence date" in line
    assert "fresh" not in line


def test_legend_explains_depth_not_verdict():
    leg = receipts_legend()
    assert "depth" in leg and "not a verdict" in leg
    assert "single-source" in leg and "well-corroborated" in leg
    assert "freshness signal" in leg.lower()
