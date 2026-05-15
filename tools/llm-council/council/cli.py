"""`python -m council` entry point."""

import asyncio
import sys
from datetime import date
from pathlib import Path

import click
from rich.console import Console

from council.budget import BudgetExceeded, preflight, record_spend
from council.client import OpenRouterClient
from council.pipeline import run_council
from council.profiles import PROFILES, get_profile

console = Console()


def _render_markdown(session, profile, user_query: str, cost_usd: float) -> str:
    lines = []
    lines.append(f"# Council Session — {session.tag}\n")
    lines.append(f"- **Session ID:** `{session.id}`")
    lines.append(f"- **Profile:** `{profile.name}`")
    lines.append(f"- **Duration:** {session.duration_ms / 1000:.1f}s")
    lines.append(f"- **Tokens:** {session.total_tokens_in} in, {session.total_tokens_out} out")
    lines.append(f"- **Cost:** ${cost_usd:.4f}")
    if session.dropped_models:
        lines.append(f"- **Dropped models (Stage 1 failures):** {', '.join(session.dropped_models)}")
    if session.ranking_failed_models:
        lines.append(f"- **Ranking-failed judges (Stage 2):** {', '.join(session.ranking_failed_models)}")
    lines.append("")
    lines.append("## Original prompt\n")
    lines.append("```")
    lines.append(user_query)
    lines.append("```\n")

    lines.append("## Council responses\n")
    for r in session.responses:
        lines.append(f"### {r['model_id']}\n")
        lines.append(r["content"])
        lines.append("")

    lines.append("## Cross-rankings\n")
    for rk in session.rankings:
        lines.append(f"### Judge: {rk['judge_model']}\n")
        lines.append(f"- **Order:** {' > '.join(rk['ranking'])}")
        lines.append(f"- **Reasoning:** {rk['reasoning']}")
        lines.append("")

    lines.append("## Chairman synthesis\n")
    lines.append(f"_Chairman model: `{session.chairman_response.model_id}`_\n")
    lines.append(session.chairman_response.content)
    lines.append("")
    return "\n".join(lines)


@click.command()
@click.option("--profile", type=click.Choice(list(PROFILES.keys())), required=True)
@click.option("--prompt-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--tag", type=str, default="adhoc", help="Free-form label for spend tracking + filename.")
@click.option("--force", is_flag=True, help="Bypass per-query cap (daily/monthly still enforced).")
@click.option("--skip-budget-check", is_flag=True, hidden=True, help="Test-only: skip all budget gates.")
def main(profile: str, prompt_file: Path, output: Path, tag: str, force: bool, skip_budget_check: bool) -> None:
    """Run an LLM council session against the given prompt file."""
    user_query = prompt_file.read_text().strip()
    if not user_query:
        console.print("[red]Prompt file is empty.[/red]")
        sys.exit(1)

    p = get_profile(profile)

    if not skip_budget_check:
        # Pre-flight uses a coarse estimate. Real cost is computed post-run.
        # Conservative estimate: 4 models × (2k in + 2k out) + 1 chairman × (8k in + 2k out)
        # This is a rough enough estimate that we lean on per-query cap as the real gate.
        rough = p.max_cost_per_query * 0.5  # half the cap, before actual call
        try:
            preflight(
                estimated=rough,
                per_query_cap=p.max_cost_per_query,
                daily_cap=_load_daily_cap(),
                monthly_cap=_load_monthly_cap(),
                on_date=date.today(),
                force=force,
            )
        except BudgetExceeded as e:
            console.print(f"[red]Budget rejected: {e}[/red]")
            sys.exit(2)

    async def _go():
        client = OpenRouterClient()
        try:
            sessions_dir = output.parent / ".sessions"
            session = await run_council(
                client=client,
                profile=p,
                user_query=user_query,
                tag=tag,
                sessions_dir=sessions_dir,
            )
            return session
        finally:
            await client.aclose()

    try:
        session = asyncio.run(_go())
    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(3)

    # Post-run actual cost (uses recorded usage; pricing snapshot loaded lazily).
    # For v0.1 we estimate from token counts × profile's avg price; refine in a future task.
    estimated_cost = (session.total_tokens_in / 1000.0) * 0.005 + (session.total_tokens_out / 1000.0) * 0.015

    if not skip_budget_check:
        record_spend(amount=estimated_cost, profile=p.name, tag=tag, on_date=date.today())

    output.write_text(_render_markdown(session, p, user_query, estimated_cost))
    console.print(f"[green]Council session written:[/green] {output}")
    console.print(f"[dim]Approximate cost: ${estimated_cost:.4f}[/dim]")


def _load_daily_cap() -> float:
    """Read daily cap from model-selection doc. v0.1 uses a hardcoded value; refine later."""
    return float(_DAILY_CAP_USD)


def _load_monthly_cap() -> float:
    return float(_MONTHLY_CAP_USD)


# Hardcoded from model-selection-2026-05-14.md output of Task 1 (Sean approved "Looser" caps).
# Update both files together when refreshing caps.
_DAILY_CAP_USD = 7.00
_MONTHLY_CAP_USD = 40.00
