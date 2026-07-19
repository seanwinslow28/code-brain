"""`python -m council.discovery` — fusion-discovery-council CLI."""

import asyncio
import math
import os
import sys
import uuid
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

from council import budget, policy, reservations
from council.budget import BudgetExceeded, utc_accounting_date
from council.discovery.pipeline import DiscoveryFailed, run_discovery
from council.discovery.tiers import get_tier

console = Console()

# These three tier choices are members of the discovery registry enumeration; the
# fourth enumerated value ($30) is the panel-vs-single experiment's daily-cap semantic.
TIER_PER_QUERY_CAP = {"quick": 3.25, "standard": 4.50, "deep": 7.50}


def _brief_path(output: Path) -> Path:
    """Sibling path for the substack handoff brief: drop a trailing '-idea-ledger', add '-brief'."""
    stem = output.stem
    if stem.endswith("-idea-ledger"):
        stem = stem[: -len("-idea-ledger")]
    return output.with_name(f"{stem}-brief{output.suffix}")


@click.command()
@click.argument("topic")
@click.option("--lens", type=click.Choice(["pm", "substack"]), default="pm")
@click.option("--tier", type=click.Choice(["quick", "standard", "deep"]), default="standard")
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--segment", default="", help="Reshape gather queries toward an audience (e.g. developer, creative, pm).")
@click.option("--force", is_flag=True, help="Bypass per-run cap (daily/monthly still enforced).")
@click.option("--yes", is_flag=True, help="Auto-confirm deep-tier cost.")
@click.option("--supplement/--no-supplement", default=False,
              help="Opt-in Stage 5 BACKFILL: deterministic Exa/Brave web-search of the blind-spot map "
                   "(off-subscription, for the headless/no-agent path). Default OFF — in an agent "
                   "session, let the orchestrating agent backfill via WebSearch/WebFetch ($0). Needs "
                   "EXA_API_KEY or BRAVE_API_KEY.")
def main(topic, lens, tier, output, segment, force, yes, supplement):
    load_dotenv()  # resolve OPENROUTER_API_KEY from the repo-root .env (mirrors council.client)
    tcfg = get_tier(tier)
    api_key = os.environ.get("OPENROUTER_API_KEY", "")

    if tier == "deep" and not yes:
        if not click.confirm(f"deep tier may cost up to ${tcfg.max_cost_per_run:.2f}. Proceed?"):
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(1)

    cap_registry = policy.load_policy()
    discovery_caps = cap_registry["tools"]["discovery"]
    aggregate_caps = cap_registry["aggregate"]
    accounting_date = utc_accounting_date()
    run_id = uuid.uuid4().hex
    reserved_cost = reservations.discovery_worst_case_reservation(tcfg)
    try:
        reservation = budget.check_and_reserve(
            reserved_cost=reserved_cost,
            tool="discovery",
            tag=f"discovery-{lens}",
            profile=tier,
            run_id=run_id,
            on_date=accounting_date,
            per_query_cap=TIER_PER_QUERY_CAP[tier],
            tool_daily_cap=discovery_caps["daily_cap"],
            tool_monthly_cap=discovery_caps["monthly_cap"],
            aggregate_daily_cap=aggregate_caps["daily_cap"],
            aggregate_monthly_cap=aggregate_caps["monthly_cap"],
            force=force,
        )
    except BudgetExceeded as e:
        console.print(f"[red]Budget rejected: {e}[/red]")
        sys.exit(2)

    sessions_dir = output.parent / ".discovery-sessions"
    budget.mark_dispatched(reservation)

    try:
        result = asyncio.run(run_discovery(
            topic=topic, lens=lens, tier=tier, api_key=api_key, segment=segment,
            supplement=supplement, sessions_dir=sessions_dir,
        ))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.markdown)
        if lens == "substack" and result.brief_markdown:
            brief = _brief_path(output)
            brief.write_text(result.brief_markdown)
    except DiscoveryFailed as e:
        usable_cost = (
            not isinstance(e.cost_usd, bool)
            and isinstance(e.cost_usd, (int, float))
            and math.isfinite(e.cost_usd)
            and e.cost_usd > 0
        )
        try:
            if usable_cost:
                budget.record_actual(
                    reservation,
                    attempt_id=f"{run_id}-01",
                    generation_id=None,
                    usage_cost=e.cost_usd,
                    status="settled",
                    provenance="estimated",
                )
            budget.close(reservation, status="unknown")
        except Exception as accounting_error:
            console.print(f"[red]Spend accounting failed: {accounting_error}[/red]")
            raise
        status = (e.session or {}).get("gather_status", {})
        stage = (e.session or {}).get("failed_stage", "fuse")
        console.print(f"[red]Discovery failed ({stage}):[/red] {e}")
        if status:
            console.print(f"[dim]Gather status: {status}[/dim]")
        if usable_cost:
            console.print(
                f"[dim]Recorded estimated spend: ${e.cost_usd:.2f} "
                f"(preserved despite the {stage} failure)[/dim]"
            )
        else:
            console.print("[dim]No spend recorded (failed before billing)[/dim]")
        sys.exit(3)
    except Exception as e:
        try:
            budget.close(reservation, status="unknown")
        except Exception as accounting_error:
            console.print(f"[red]Spend accounting failed: {accounting_error}[/red]")
            raise
        console.print(f"[red]Discovery failed: {e}[/red]")
        sys.exit(3)

    usable_cost = (
        not isinstance(result.cost_usd, bool)
        and isinstance(result.cost_usd, (int, float))
        and math.isfinite(result.cost_usd)
        and result.cost_usd >= 0
    )
    try:
        budget.record_actual(
            reservation,
            attempt_id=f"{run_id}-01",
            generation_id=None,
            usage_cost=result.cost_usd if usable_cost else None,
            status="settled" if usable_cost else "unknown",
            provenance="estimated" if usable_cost else None,
        )
        # Discovery reports an estimate, not provider-authoritative cash. Its debit stays
        # retained and the graph can never be represented as fully settled.
        budget.close(reservation, status="unknown")
    except Exception as accounting_error:
        console.print(f"[red]Spend accounting failed: {accounting_error}[/red]")
        raise

    console.print(f"[green]Idea ledger written:[/green] {output}")
    if lens == "substack" and result.brief_markdown:
        console.print(f"[green]Substack handoff brief written:[/green] {_brief_path(output)}")
    if usable_cost:
        cost_text = f"${result.cost_usd:.2f} estimated"
    else:
        cost_text = "estimated cost unknown"
    console.print(
        f"[dim]Verified ideas: {result.verified_count} · "
        f"dropped: {result.dropped_count} · {cost_text}[/dim]"
    )


if __name__ == "__main__":
    main()
