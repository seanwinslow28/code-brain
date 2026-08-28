"""CLI: panel-vs-single-model discovery gate. Gather once → dual-fuse → blind-rateable A/B."""

import asyncio
import json
import math
import os
import time
import uuid
from dataclasses import asdict
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from council import budget, policy, reservations
from council.budget import BudgetExceeded, utc_accounting_date
from council.discovery.fusion import FusionError, FusionResult
from council.discovery.tiers import get_tier
from experiments.blind_rating import build_blind_rating
from experiments.panel_vs_single_core import run_panel_vs_single

console = Console()
# The documented experiment per-query cap intentionally has the same semantic value
# as discovery's daily cap and is enumerated separately in the policy registry.
EXPERIMENT_PER_QUERY_CAP = 30.00
DEFAULT_TOPIC = ("artists, writers, and designers who say AI is a slot machine — the same prompt never "
                 "gives the same result twice — and who have stopped chasing prompts in favor of "
                 "building a repeatable system they can trust")


def _arm_payload(fr: FusionResult) -> dict:
    return {
        "pain_points": [asdict(p) for p in fr.pain_points],
        "blind_spots": list(fr.blind_spots),
        "contradictions": list(fr.contradictions),
        "cost": round(fr.cost or 0.0, 6),
    }


def _write_artifacts(out_dir: Path, result: dict, topic: str) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "bundle.json").write_text(json.dumps(result["bundle"].to_dict(), indent=2))
    (out_dir / "arm-A.json").write_text(json.dumps(_arm_payload(result["arm_a"]), indent=2))
    (out_dir / "arm-B.json").write_text(json.dumps(_arm_payload(result["arm_b"]), indent=2))
    md, key = build_blind_rating(result["arm_a"].pain_points, result["arm_b"].pain_points, topic)
    (out_dir / "blind-rating.md").write_text(md)
    (out_dir / "key.json").write_text(json.dumps(key, indent=2))
    return {n: out_dir / n for n in ("bundle.json", "arm-A.json", "arm-B.json", "blind-rating.md", "key.json")}


@click.command()
@click.option("--topic", default=DEFAULT_TOPIC)
@click.option("--tier", "tier_name", type=click.Choice(["quick", "standard", "deep"]), default="standard")
@click.option("--single-model", default="anthropic/claude-opus-4.7")
@click.option("--out", type=click.Path(file_okay=False, path_type=Path), default=None)
@click.option("--yes", is_flag=True, help="Auto-confirm the dual-fuse cost.")
def main(topic, tier_name, single_model, out, yes):
    load_dotenv()
    tcfg = get_tier(tier_name)
    reserved_cost = reservations.experiment_worst_case_reservation(tcfg)

    console.print(f"[yellow]Dual-fuse (panel vs {single_model}) — reserved up to ${reserved_cost:.2f} "
                  f"(2 real OpenRouter calls).[/yellow]")
    if not yes and not click.confirm("Proceed with the paid run?"):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(1)

    cap_registry = policy.load_policy()
    discovery_caps = cap_registry["tools"]["discovery"]
    aggregate_caps = cap_registry["aggregate"]
    accounting_date = utc_accounting_date()
    run_id = uuid.uuid4().hex
    try:
        reservation = budget.check_and_reserve(
            reserved_cost=reserved_cost,
            tool="discovery",
            tag="discovery-experiment",
            profile=tier_name,
            run_id=run_id,
            on_date=accounting_date,
            per_query_cap=EXPERIMENT_PER_QUERY_CAP,
            tool_daily_cap=discovery_caps["daily_cap"],
            tool_monthly_cap=discovery_caps["monthly_cap"],
            aggregate_daily_cap=aggregate_caps["daily_cap"],
            aggregate_monthly_cap=aggregate_caps["monthly_cap"],
        )
    except BudgetExceeded as e:
        console.print(f"[red]Budget rejected: {e}[/red]")
        raise SystemExit(2)

    out_dir = out or Path("experiments/runs") / f"panel-vs-single-{time.strftime('%Y%m%d-%H%M%S')}"
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    budget.mark_dispatched(reservation)
    attempt_count = 0

    def _record_estimate(*, amount, **kwargs):
        nonlocal attempt_count
        attempt_count += 1
        usable_cost = (
            not isinstance(amount, bool)
            and isinstance(amount, (int, float))
            and math.isfinite(amount)
            and amount >= 0
        )
        budget.record_actual(
            reservation,
            attempt_id=f"{run_id}-{attempt_count:02d}",
            generation_id=None,
            usage_cost=amount if usable_cost else None,
            status="settled" if usable_cost else "unknown",
            provenance="estimated" if usable_cost else None,
        )

    try:
        result = asyncio.run(run_panel_vs_single(
            topic=topic, tier_name=tier_name, single_model=single_model,
            api_key=api_key, on_date=accounting_date, record_fn=_record_estimate,
        ))
    except FusionError:
        budget.close(reservation, status="unknown")
        raise
    except Exception:
        budget.close(reservation, status="unknown")
        raise
    budget.close(reservation, status="unknown")

    paths = _write_artifacts(out_dir, result, topic)
    console.print(f"[green]Done.[/green] ${result['cost']:.4f} across both arms.")
    console.print(f"[dim]Artifacts: {out_dir}[/dim]")
    for p in paths.values():
        console.print(f"[dim] - {p}[/dim]")


if __name__ == "__main__":
    main()
