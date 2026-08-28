"""`python -m council` entry point."""

import asyncio
import math
import sys
import uuid
from decimal import Decimal
from pathlib import Path

import click
from rich.console import Console

from council import budget, policy
from council.budget import BudgetExceeded, utc_accounting_date
from council.client import OpenRouterClient
from council.pipeline import DEFAULT_STAGE_BOUNDS, run_council
from council.profiles import PROFILES, get_profile

console = Console()

# Task 3c prices the worst case from this ceiling using byte >= token. Raising
# it changes reservation sizing and therefore requires a Sean gate; disclose
# the value at the Task 3c STOP.
PROMPT_MAX_BYTES = 131072

# Imported after PROMPT_MAX_BYTES so reservations can import the shipped CLI ceiling
# without duplicating the value or creating a partially initialized missing constant.
from council import reservations  # noqa: E402


def _render_markdown(session, profile, user_query: str, cost_usd: float | None) -> str:
    lines = []
    lines.append(f"# Council Session — {session.tag}\n")
    lines.append(f"- **Session ID:** `{session.id}`")
    lines.append(f"- **Profile:** `{profile.name}`")
    lines.append(f"- **Duration:** {session.duration_ms / 1000:.1f}s")
    lines.append(f"- **Tokens:** {session.total_tokens_in} in, {session.total_tokens_out} out")
    lines.append(f"- **Cost:** ${cost_usd:.4f}" if cost_usd is not None else "- **Cost:** unknown")
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
        lines.append(r["content"] or "_(no response: model returned null)_")
        lines.append("")

    lines.append("## Cross-rankings\n")
    for rk in session.rankings:
        lines.append(f"### Judge: {rk['judge_model']}\n")
        lines.append(f"- **Order:** {' > '.join(rk['ranking'])}")
        lines.append(f"- **Reasoning:** {rk['reasoning'] or '_(no reasoning returned)_'}")
        lines.append("")

    lines.append("## Chairman synthesis\n")
    lines.append(f"_Chairman model: `{session.chairman_response.model_id}`_\n")
    lines.append(session.chairman_response.content or "_(no response: chairman returned null)_")
    lines.append("")
    return "\n".join(lines)


@click.command()
@click.option("--profile", type=click.Choice(list(PROFILES.keys())), required=True)
@click.option("--prompt-file", type=click.Path(exists=True, dir_okay=False, path_type=Path), required=True)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), required=True)
@click.option("--tag", type=str, default="adhoc", help="Free-form label for spend tracking + filename.")
@click.option("--force", is_flag=True, help="Bypass per-query cap (daily/monthly still enforced).")
def main(profile: str, prompt_file: Path, output: Path, tag: str, force: bool) -> None:
    """Run an LLM council session against the given prompt file."""
    raw_user_query = prompt_file.read_text()
    prompt_bytes = len(raw_user_query.encode("utf-8"))
    if prompt_bytes > PROMPT_MAX_BYTES:
        console.print(
            f"[red]Prompt file is {prompt_bytes} UTF-8 bytes; "
            f"the cap is {PROMPT_MAX_BYTES} bytes.[/red]"
        )
        sys.exit(1)
    user_query = raw_user_query.strip()
    if not user_query:
        console.print("[red]Prompt file is empty.[/red]")
        sys.exit(1)

    p = get_profile(profile)

    cap_registry = policy.load_policy()
    council_caps = cap_registry["tools"]["council"]
    aggregate_caps = cap_registry["aggregate"]
    accounting_date = utc_accounting_date()
    run_id = uuid.uuid4().hex
    reserved_cost = reservations.council_worst_case_cost(p)
    try:
        reservation = budget.check_and_reserve(
            reserved_cost=reserved_cost,
            tool="council",
            tag=tag,
            profile=p.name,
            run_id=run_id,
            on_date=accounting_date,
            per_query_cap=p.max_cost_per_query,
            tool_daily_cap=council_caps["daily_cap"],
            tool_monthly_cap=council_caps["monthly_cap"],
            aggregate_daily_cap=aggregate_caps["daily_cap"],
            aggregate_monthly_cap=aggregate_caps["monthly_cap"],
            force=force,
        )
    except BudgetExceeded as e:
        console.print(f"[red]Budget rejected: {e}[/red]")
        sys.exit(2)

    # This fsynced transition is the last operation before client construction. A crash
    # beyond it retains the debit for reconciliation; there is no refund path here.
    budget.mark_dispatched(reservation)
    attempt_count = 0
    all_attempts_known = True
    actual_cost = Decimal(0)

    def _record_attempt(attempt: dict) -> None:
        nonlocal attempt_count, all_attempts_known, actual_cost
        attempt_count += 1
        raw_cost = attempt.get("cost")
        usable_cost = (
            not isinstance(raw_cost, bool)
            and isinstance(raw_cost, (int, float))
            and math.isfinite(raw_cost)
            and raw_cost >= 0
        )
        cost = raw_cost if usable_cost else None
        budget.record_actual(
            reservation,
            attempt_id=f"{run_id}-{attempt_count:02d}",
            generation_id=attempt.get("generation_id"),
            usage_cost=cost,
            status="settled" if usable_cost else "unknown",
        )
        if usable_cost:
            actual_cost += Decimal(str(raw_cost))
        else:
            all_attempts_known = False

    async def _go():
        # Transport retries are FORBIDDEN on the reserve-backed gateway (max_retries=0,
        # the-oracle's rule): a retried-but-billed HTTP dispatch is invisible to
        # on_attempt, which would let real spend escape both the 13-call reservation
        # bound and the settled accounting. One logical call == one HTTP dispatch.
        client = OpenRouterClient(max_retries=0)
        try:
            sessions_dir = output.parent / ".sessions"
            session = await run_council(
                client=client,
                profile=p,
                user_query=user_query,
                tag=tag,
                sessions_dir=sessions_dir,
                dispatch_bounds=DEFAULT_STAGE_BOUNDS,
                on_attempt=_record_attempt,
            )
            return session
        finally:
            await client.aclose()

    try:
        session = asyncio.run(_go())
        close_status = "settled" if attempt_count > 0 and all_attempts_known else "unknown"
        known_cost = float(actual_cost) if close_status == "settled" else None
        output.write_text(_render_markdown(session, p, user_query, known_cost))
    except Exception as e:
        try:
            budget.close(reservation, status="unknown")
        except Exception as accounting_error:
            console.print(f"[red]Spend accounting failed: {accounting_error}[/red]")
            raise
        console.print(f"[red]{e}[/red]")
        sys.exit(3)

    try:
        budget.close(reservation, status=close_status)
    except Exception as accounting_error:
        console.print(f"[red]Spend accounting failed: {accounting_error}[/red]")
        raise

    console.print(f"[green]Council session written:[/green] {output}")
    if known_cost is not None:
        console.print(f"[dim]Actual cost: ${known_cost:.4f}[/dim]")
    else:
        console.print("[dim]Actual cost: unknown[/dim]")
