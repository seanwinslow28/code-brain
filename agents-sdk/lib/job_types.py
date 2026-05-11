"""Shared dataclasses for the job-feed agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Posting:
    """Unified posting shape produced by every feed/ATS adapter."""

    source: str
    source_role_id: str
    url: str
    company: str
    title: str
    location: str | None
    salary_disclosed: str | None
    posted_at: datetime | None
    description: str


@dataclass
class ScoringResult:
    """Strict-JSON shape returned by Qwen3-14B for a single posting."""

    fit_score: int  # 0..5
    role_band: str  # PM | APM | Sr_PM_stretch | Principal_stretch | Other
    rationale: str
    concerns: list[str] = field(default_factory=list)
    fit_dimensions: dict[str, int] = field(default_factory=dict)
