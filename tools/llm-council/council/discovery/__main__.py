"""`python -m council.discovery` — fusion-discovery-council CLI."""

import asyncio
import os
import sys
from datetime import date
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from council.budget import BudgetExceeded, preflight_tool, record_spend
from council.discovery.pipeline import run_discovery, DiscoveryFailed
from council.discovery.tiers import get_tier

console = Console()
DISCOVERY_DAILY_CAP = 10.0
DISCOVERY_MONTHLY_CAP = 50.0


@click.command()
@click.argument("topic")
@click.option("--lens", type=click.Choice(["pm", "substack"]), default="pm")
@click.option("--tier", type=click.Choice(["quick", "standard", "deep"]), default="standard")
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--force", is_flag=True, help="Bypass per-run cap (daily/monthly still enforced).")
@click.option("--yes", is_flag=True, help="Auto-confirm deep-tier cost.")
@click.option("--skip-budget-check", is_flag=True, hidden=True)
def main(topic, lens, tier, output, force, yes, skip_budget_check):
    load_dotenv()  # resolve OPENROUTER_API_KEY from the repo-root .env (mirrors council.client)
    tcfg = get_tier(tier)

    if tier == "deep" and not yes:
        if not click.confirm(f"deep tier may cost up to ${tcfg.max_cost_per_run:.2f}. Proceed?"):
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(1)

    if not skip_budget_check:
        try:
            preflight_tool(
                estimated=tcfg.max_cost_per_run * 0.6,
                per_query_cap=tcfg.max_cost_per_run,
                daily_cap=DISCOVERY_DAILY_CAP, monthly_cap=DISCOVERY_MONTHLY_CAP,
                on_date=date.today(), tool="discovery", force=force,
            )
        except BudgetExceeded as e:
            console.print(f"[red]Budget rejected: {e}[/red]")
            sys.exit(2)

    api_key = os.environ.get("OPENROUTER_API_KEY", "") if not skip_budget_check else "test"
    sessions_dir = output.parent / ".discovery-sessions"

    try:
        result = asyncio.run(run_discovery(
            topic=topic, lens=lens, tier=tier, api_key=api_key, sessions_dir=sessions_dir,
        ))
    except DiscoveryFailed as e:
        if not skip_budget_check and e.cost_usd > 0:
            record_spend(amount=e.cost_usd, profile=tier, tag=f"discovery-{lens}",
                         on_date=date.today(), tool="discovery")
        status = (e.session or {}).get("gather_status", {})
        console.print(f"[red]Discovery failed at fuse:[/red] {e}")
        if status:
            console.print(f"[dim]Gather status: {status}[/dim]")
        if e.cost_usd > 0:
            console.print(f"[dim]Recorded spend: ${e.cost_usd:.2f} (billed even though FUSE failed)[/dim]")
        else:
            console.print("[dim]No spend recorded (FUSE failed before billing)[/dim]")
        sys.exit(3)
    except Exception as e:  # surface other pipeline failures cleanly (no spend incurred pre-fuse)
        console.print(f"[red]Discovery failed: {e}[/red]")
        sys.exit(3)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.markdown)
    if not skip_budget_check:
        record_spend(amount=result.cost_usd, profile=tier, tag=f"discovery-{lens}",
                     on_date=date.today(), tool="discovery")
    console.print(f"[green]Idea ledger written:[/green] {output}")
    console.print(f"[dim]Verified ideas: {result.verified_count} · dropped: {result.dropped_count} · ${result.cost_usd:.2f}[/dim]")


if __name__ == "__main__":
    main()
