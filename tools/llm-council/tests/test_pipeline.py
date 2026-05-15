import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from council.client import ModelResponse, ClientError
from council.pipeline import run_council, CouncilSession
from council.profiles import Profile


@pytest.fixture
def fake_profile():
    return Profile(
        name="test",
        models=("m1", "m2", "m3", "m4"),
        chairman="m1",
        max_cost_per_query=10.0,
    )


def _resp(model: str, text: str, tin: int = 10, tout: int = 10) -> ModelResponse:
    return ModelResponse(model_id=model, content=text, tokens_in=tin, tokens_out=tout, latency_ms=10)


@pytest.mark.asyncio
async def test_run_council_happy_path_calls_all_three_stages(fake_profile):
    client = MagicMock()
    # Stage 1: 4 fan-out calls
    # Stage 2: 4 cross-rank calls
    # Stage 3: 1 chairman call
    valid_ranking = '{"ranking": ["A", "B", "C"], "reasoning": "fine."}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "answer 1"),
        _resp("m2", "answer 2"),
        _resp("m3", "answer 3"),
        _resp("m4", "answer 4"),
        _resp("m1", valid_ranking),
        _resp("m2", valid_ranking),
        _resp("m3", valid_ranking),
        _resp("m4", valid_ranking),
        _resp("m1", "synthesized."),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert isinstance(session, CouncilSession)
    assert len(session.responses) == 4
    assert len(session.rankings) == 4
    assert session.chairman_response.content == "synthesized."
    assert client.complete.call_count == 9


@pytest.mark.asyncio
async def test_run_council_degraded_with_one_stage1_failure(fake_profile):
    client = MagicMock()
    valid_ranking = '{"ranking": ["A", "B"], "reasoning": "fine."}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        ClientError("m2 timed out"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        # Cross-rank: now only 3 judges (m1, m3, m4)
        _resp("m1", valid_ranking),
        _resp("m3", valid_ranking),
        _resp("m4", valid_ranking),
        # Chairman
        _resp("m1", "synth"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert len(session.responses) == 3  # N-1 survivors
    assert len(session.rankings) == 3
    assert "m2" in session.dropped_models
    assert session.chairman_response.content == "synth"


@pytest.mark.asyncio
async def test_run_council_wraps_chairman_failure_as_runtime_error(fake_profile):
    """Spec §5: chairman failure must surface as a RuntimeError the CLI can catch."""
    client = MagicMock()
    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", valid),
        _resp("m2", valid),
        _resp("m3", valid),
        _resp("m4", valid),
        ClientError("chairman timeout"),  # Stage 3 fails
    ])

    with pytest.raises(RuntimeError) as exc:
        await run_council(
            client=client,
            profile=fake_profile,
            user_query="Q",
            tag="t",
        )
    assert "chairman synthesis failed" in str(exc.value).lower()
    assert "m1" in str(exc.value)  # the chairman model name appears


@pytest.mark.asyncio
async def test_run_council_aborts_on_two_stage1_failures(fake_profile):
    client = MagicMock()
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        ClientError("m2 timed out"),
        ClientError("m3 timed out"),
        _resp("m4", "a4"),
    ])

    with pytest.raises(RuntimeError) as exc:
        await run_council(
            client=client,
            profile=fake_profile,
            user_query="Q",
            tag="t",
        )
    assert "two or more" in str(exc.value).lower() or "council unavailable" in str(exc.value).lower()


@pytest.mark.asyncio
async def test_cross_rank_retries_non_json_then_skips(fake_profile):
    client = MagicMock()
    # m2 returns garbage twice → its ranking is skipped; chairman still gets 3 rankings.
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m2", "not json"),         # first attempt fails to parse
        _resp("m2", "still not json"),   # retry also fails
        _resp("m3", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m4", '{"ranking": ["A","B","C"], "reasoning": "ok"}'),
        _resp("m1", "synthesized"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="t",
    )

    assert len(session.rankings) == 3  # m2's ranking skipped
    assert all(r["judge_model"] != "m2" for r in session.rankings)


@pytest.mark.asyncio
async def test_session_writes_json_to_data_sessions_dir(fake_profile, tmp_path):
    client = MagicMock()
    valid = '{"ranking": ["A","B","C"], "reasoning": "ok"}'
    client.complete = AsyncMock(side_effect=[
        _resp("m1", "a1"),
        _resp("m2", "a2"),
        _resp("m3", "a3"),
        _resp("m4", "a4"),
        _resp("m1", valid),
        _resp("m2", valid),
        _resp("m3", valid),
        _resp("m4", valid),
        _resp("m1", "synth"),
    ])

    session = await run_council(
        client=client,
        profile=fake_profile,
        user_query="Q",
        tag="voice-mode",
        sessions_dir=tmp_path,
    )

    # A JSON file should have been written at tmp_path/<session.id>.json
    session_files = list(tmp_path.glob("*.json"))
    assert len(session_files) == 1
    data = json.loads(session_files[0].read_text())
    assert data["tag"] == "voice-mode"
    assert data["profile"] == "test"
    assert len(data["responses"]) == 4
