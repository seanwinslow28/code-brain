"""CLI: panel-vs-single-model discovery gate. Gather once → dual-fuse → blind-rateable A/B."""

import asyncio
import json
import os
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from council.budget import BudgetExceeded, preflight_tool
from council.discovery.fusion import FusionResult
from council.discovery.tiers import get_tier
from experiments.blind_rating import build_blind_rating
from experiments.panel_vs_single_core import run_panel_vs_single

console = Console()
DISCOVERY_DAILY_CAP = 10.0
DISCOVERY_MONTHLY_CAP = 50.0
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
    # Two fuse calls intentionally exceed a single-run cap, so gate on the DAILY cap, not per-run.
    estimated = round(tcfg.max_cost_per_run * 1.5, 4)
    try:
        preflight_tool(estimated=estimated, per_query_cap=DISCOVERY_DAILY_CAP,
                       daily_cap=DISCOVERY_DAILY_CAP, monthly_cap=DISCOVERY_MONTHLY_CAP,
                       on_date=date.today(), tool="discovery")
    except BudgetExceeded as e:
        console.print(f"[red]Budget rejected: {e}[/red]")
        raise SystemExit(2)

    console.print(f"[yellow]Dual-fuse (panel vs {single_model}) — estimated up to ${estimated:.2f} "
                  f"(2 real OpenRouter calls).[/yellow]")
    if not yes and not click.confirm("Proceed with the paid run?"):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(1)

    out_dir = out or Path("experiments/runs") / f"panel-vs-single-{time.strftime('%Y%m%d-%H%M%S')}"
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    result = asyncio.run(run_panel_vs_single(
        topic=topic, tier_name=tier_name, single_model=single_model,
        api_key=api_key, on_date=date.today(),
    ))
    paths = _write_artifacts(out_dir, result, topic)
    console.print(f"[green]Done.[/green] ${result['cost']:.4f} across both arms.")
    console.print(f"[dim]Artifacts: {out_dir}[/dim]")
    for p in paths.values():
        console.print(f"[dim] - {p}[/dim]")


if __name__ == "__main__":
    main()
