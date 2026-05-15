"""Cost estimation, spend recording, and pre-flight cap enforcement.

Spend files live at $COUNCIL_SPEND_DIR (default: vault/health/) and are append-only
JSON written atomically via tmp + rename.
"""

import json
import os
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Pricing:
    """Per-1k-token prices in USD."""
    prompt_per_1k: float
    completion_per_1k: float


class BudgetExceeded(Exception):
    """Raised when a pre-flight check rejects a query."""


def _spend_dir() -> Path:
    raw = os.environ.get("COUNCIL_SPEND_DIR")
    if raw:
        d = Path(raw)
    else:
        # Walk up to find vault/health/ relative to this file.
        here = Path(__file__).resolve()
        d = here.parents[3] / "vault" / "health"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _daily_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.isoformat()}.json"


def _monthly_file(on_date: date) -> Path:
    return _spend_dir() / f"council-spend-{on_date.strftime('%Y-%m')}.json"


def estimate_cost(*, pricing: dict[str, Pricing], per_model_tokens: list[tuple[str, int, int]]) -> float:
    """Sum per-model (in_tokens × prompt_per_1k + out_tokens × completion_per_1k) over /1000.

    `per_model_tokens` is a list of (model_id, in_tokens, out_tokens) tuples.
    Raises KeyError if any model_id is missing from pricing.
    """
    total = 0.0
    for model_id, in_tokens, out_tokens in per_model_tokens:
        if model_id not in pricing:
            raise KeyError(f"pricing missing for model {model_id!r}")
        p = pricing[model_id]
        total += (in_tokens / 1000.0) * p.prompt_per_1k
        total += (out_tokens / 1000.0) * p.completion_per_1k
    return total


def _atomic_write_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def _read_total_for_day(on_date: date) -> float:
    f = _daily_file(on_date)
    if not f.exists():
        return 0.0
    return float(json.loads(f.read_text()).get("total", 0.0))


def _read_total_for_month(on_date: date) -> float:
    # Sum every council-spend-YYYY-MM-DD.json in the same YYYY-MM
    prefix = f"council-spend-{on_date.strftime('%Y-%m')}-"
    total = 0.0
    for f in _spend_dir().glob(f"{prefix}*.json"):
        try:
            total += float(json.loads(f.read_text()).get("total", 0.0))
        except (json.JSONDecodeError, ValueError):
            continue
    return total


def record_spend(*, amount: float, profile: str, tag: str, on_date: date) -> None:
    """Append a run to today's daily spend file. Atomic write."""
    f = _daily_file(on_date)
    if f.exists():
        data = json.loads(f.read_text())
    else:
        data = {"date": on_date.isoformat(), "total": 0.0, "runs": []}
    data["runs"].append({"amount": amount, "profile": profile, "tag": tag})
    data["total"] = round(data["total"] + amount, 6)
    _atomic_write_json(f, data)


def preflight(
    *,
    estimated: float,
    per_query_cap: float,
    daily_cap: float,
    monthly_cap: float,
    on_date: date,
    force: bool = False,
) -> None:
    """Reject the query if any cap would be breached.

    `force=True` bypasses per-query cap (but still respects daily/monthly).
    Daily and monthly caps are NEVER bypassed.
    """
    if not force and estimated > per_query_cap:
        raise BudgetExceeded(
            f"per-query cap exceeded: estimated ${estimated:.4f} > cap ${per_query_cap:.4f}. "
            f"Use --force to override (still subject to daily/monthly caps)."
        )
    today_total = _read_total_for_day(on_date)
    if today_total + estimated > daily_cap:
        raise BudgetExceeded(
            f"daily cap would be exceeded: today=${today_total:.4f} + "
            f"estimated=${estimated:.4f} > daily_cap=${daily_cap:.4f}"
        )
    month_total = _read_total_for_month(on_date)
    if month_total + estimated > monthly_cap:
        raise BudgetExceeded(
            f"monthly cap would be exceeded: month-to-date=${month_total:.4f} + "
            f"estimated=${estimated:.4f} > monthly_cap=${monthly_cap:.4f}"
        )
