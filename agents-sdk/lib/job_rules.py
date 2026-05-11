"""Rules filter — drops obvious-no postings before LLM scoring.

Returns (True, None) for survivors, (False, reason) for drops.
Per spec, dropped postings are still persisted with rules_passed=0 so the
audit trail exists and they don't re-process on the next run.
"""

from __future__ import annotations

import re

from lib.job_types import Posting

# Title regexes — order matters: senior-band patterns matched FIRST so a
# "Director, Product Manager" lands in the senior bucket, not the PM bucket.

_SENIOR_BAND_RE = re.compile(
    r"\b("
    r"director|"
    r"vp|vice\s*president|"
    r"head\s+of|"
    r"group\s+pm|group\s+product\s+manager|"
    r"sr\s*\.?\s*director|senior\s+director|"
    r"evp|executive\s+vice\s+president|"
    r"cpo|chief\s+product\s+officer"
    r")\b",
    re.IGNORECASE,
)

_PM_TITLE_RE = re.compile(
    r"\b("
    r"product\s+manager|"
    r"associate\s+product\s+manager|apm|"
    r"pm\s+i|pm\s+ii|"
    r"senior\s+pm|sr\s*\.?\s*pm|"
    r"principal\s+pm|"
    r"product\s+lead|product\s+owner|"
    r"technical\s+pm|lead\s+pm"
    r")\b",
    re.IGNORECASE,
)

_YOE_FLOOR_RE = re.compile(r"\b(7|8|9|1[0-9])\+?\s*years?\b", re.IGNORECASE)

# Non-US, non-remote location markers
_GEO_BLOCKED = {
    "london", "berlin", "munich", "paris", "amsterdam", "dublin",
    "tokyo", "singapore", "seoul", "hong kong", "shanghai", "beijing",
    "sydney", "melbourne", "toronto only", "vancouver only",
    "emea only", "apac only", "uk only", "europe only",
}

_SALARY_RANGE_RE = re.compile(
    r"\$?\s*(\d+k|\d{1,3}(?:,\d{3})+|\d+)\s*[-–to]+\s*\$?\s*(\d+k|\d{1,3}(?:,\d{3})+|\d+)",
    re.IGNORECASE,
)


def _normalize_money(token: str) -> int:
    """Convert '$140k' or '140,000' or '140000' to integer 140000."""
    t = token.strip().lower().replace("$", "").replace(",", "").strip()
    if t.endswith("k"):
        return int(float(t[:-1]) * 1000)
    return int(t)


def _parse_salary_upper(disclosed: str) -> int | None:
    m = _SALARY_RANGE_RE.search(disclosed)
    if not m:
        return None
    try:
        return _normalize_money(m.group(2))
    except ValueError:
        return None


def apply_rules(posting: Posting) -> tuple[bool, str | None]:
    """Apply hard filters. Returns (passed, rejection_reason)."""
    # 1. Senior-band title — drop first so it wins over the PM pattern overlap
    if _SENIOR_BAND_RE.search(posting.title):
        return False, "too senior (title band)"

    # 2. Not a PM role
    if not _PM_TITLE_RE.search(posting.title):
        return False, "not a PM role"

    # 3. YOE floor — only look at first 500 chars to avoid false positives in body
    if _YOE_FLOOR_RE.search(posting.description[:500]):
        return False, "too senior (YOE floor)"

    # 4. Geo
    if posting.location:
        loc_lower = posting.location.lower()
        if any(blocker in loc_lower for blocker in _GEO_BLOCKED):
            return False, f"geo ineligible: {posting.location}"

    # 5. Salary floor ($90k soft buffer)
    if posting.salary_disclosed:
        upper = _parse_salary_upper(posting.salary_disclosed)
        if upper is not None and upper < 90_000:
            return False, f"below salary floor: {posting.salary_disclosed}"

    return True, None
