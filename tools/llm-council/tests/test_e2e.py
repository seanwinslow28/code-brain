"""End-to-end integration test that hits the real OpenRouter API.

Skipped unless INTEGRATION=1 is set. Uses the cheapest variance-profile models
to keep cost under ~$0.05 per run. Run manually with:

    INTEGRATION=1 uv run pytest tests/test_e2e.py -v -s
"""

import os
from pathlib import Path

import pytest

from council.client import OpenRouterClient
from council.pipeline import run_council
from council.profiles import get_profile

pytestmark = pytest.mark.skipif(
    os.environ.get("INTEGRATION") != "1",
    reason="set INTEGRATION=1 to run live API integration test",
)


@pytest.mark.asyncio
async def test_full_variance_council_run(tmp_path):
    """Cheap, real, end-to-end. Validates wire compatibility with OpenRouter."""
    client = OpenRouterClient(timeout_seconds=180.0)
    try:
        profile = get_profile("variance")
        session = await run_council(
            client=client,
            profile=profile,
            user_query=(
                "In one sentence, what is the most underrated principle of writing "
                "good unit tests?"
            ),
            tag="e2e-smoke",
            sessions_dir=tmp_path,
        )
    finally:
        await client.aclose()

    assert len(session.responses) >= 3            # allow N-1 degraded
    assert len(session.rankings) >= 2             # allow some ranking failures
    assert session.chairman_response.content      # non-empty
    assert session.total_tokens_in > 0
    assert session.total_tokens_out > 0
