from datetime import datetime

from lib.job_rules import apply_rules
from lib.job_types import Posting


def _p(**overrides) -> Posting:
    base = dict(
        source="t", source_role_id="1", url="https://x.example",
        company="Co", title="Product Manager", location="Remote (US)",
        salary_disclosed=None, posted_at=datetime(2026, 5, 9),
        description="A 3+ years experience PM role.",
    )
    base.update(overrides)
    return Posting(**base)


# Title-band rules ------------------------------------------------------------

def test_drops_director():
    passed, reason = apply_rules(_p(title="Director of Product"))
    assert not passed
    assert "too senior" in reason.lower()

def test_drops_vp():
    assert apply_rules(_p(title="VP, Product"))[0] is False

def test_drops_head_of_product():
    assert apply_rules(_p(title="Head of Product"))[0] is False

def test_drops_group_pm():
    assert apply_rules(_p(title="Group PM"))[0] is False

def test_drops_cpo():
    assert apply_rules(_p(title="Chief Product Officer (CPO)"))[0] is False

def test_drops_engineer_title():
    passed, reason = apply_rules(_p(title="Senior Software Engineer"))
    assert not passed
    assert "not a pm role" in reason.lower()

def test_accepts_pm():
    assert apply_rules(_p(title="Product Manager"))[0] is True

def test_accepts_apm():
    assert apply_rules(_p(title="Associate Product Manager"))[0] is True

def test_accepts_principal_pm_stretch():
    assert apply_rules(_p(title="Principal PM"))[0] is True

# YOE-floor rule --------------------------------------------------------------

def test_drops_8_years_required():
    desc = "We need 8+ years of product management experience."
    passed, reason = apply_rules(_p(description=desc))
    assert not passed
    assert "yoe" in reason.lower()

def test_drops_10_years_required():
    desc = "Looking for 10+ years experience."
    assert apply_rules(_p(description=desc))[0] is False

def test_accepts_3_years_required():
    assert apply_rules(_p(description="3+ years preferred."))[0] is True

# Geo rule --------------------------------------------------------------------

def test_drops_london_only():
    assert apply_rules(_p(location="London, UK"))[0] is False

def test_drops_berlin():
    assert apply_rules(_p(location="Berlin"))[0] is False

def test_drops_tokyo():
    assert apply_rules(_p(location="Tokyo, Japan"))[0] is False

def test_accepts_remote():
    assert apply_rules(_p(location="Remote (US)"))[0] is True

def test_accepts_boston():
    assert apply_rules(_p(location="Boston, MA"))[0] is True

def test_accepts_none_location():
    # Spec: only EXPLICITLY non-US-and-non-remote drops; missing location passes
    assert apply_rules(_p(location=None))[0] is True

# Salary rule -----------------------------------------------------------------

def test_drops_below_floor():
    passed, reason = apply_rules(_p(salary_disclosed="$60k-$80k"))
    assert not passed
    assert "salary" in reason.lower()

def test_accepts_above_floor():
    assert apply_rules(_p(salary_disclosed="$110k-$140k"))[0] is True

def test_accepts_missing_salary():
    assert apply_rules(_p(salary_disclosed=None))[0] is True

def test_accepts_at_floor():
    # $90k buffer floor — exactly at buffer passes
    assert apply_rules(_p(salary_disclosed="$90000-$120000"))[0] is True
