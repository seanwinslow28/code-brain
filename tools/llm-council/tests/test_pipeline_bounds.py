"""Worst-case input, completion, and provider-price bounds for the council."""

import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from council import cli
from council.client import ModelResponse
from council.pipeline import (
    CHAIRMAN_MAX_TOKENS,
    CROSSRANK_MAX_TOKENS,
    DEFAULT_STAGE_BOUNDS,
    FANOUT_MAX_TOKENS,
    RANKING_REASONING_EMBED_MAX_BYTES,
    RESPONSE_EMBED_MAX_BYTES,
    run_council,
)
from council.pricing import provider_price_policy
from council.profiles import PROFILES
from council.prompts import (
    CHAIRMAN_SYSTEM,
    CROSSRANK_SYSTEM,
    FANOUT_SYSTEM,
    chairman_prompt,
    crossrank_prompt,
)


VALID_RANKING = json.dumps(
    {"ranking": ["A", "B", "C"], "reasoning": "Sound ordering."}
)


def _response(model: str, content: str) -> ModelResponse:
    return ModelResponse(
        model_id=model,
        content=content,
        tokens_in=10,
        tokens_out=10,
        latency_ms=1,
    )


class SpyClient:
    """No-network completion boundary that records the enforced request kwargs."""

    def __init__(self, response_for_call=None):
        self.calls: list[dict] = []
        self._response_for_call = response_for_call or self._default_response

    async def complete(self, **kwargs):
        self.calls.append(dict(kwargs))
        return self._response_for_call(kwargs, self.calls)

    @staticmethod
    def _default_response(kwargs, _calls):
        if kwargs["system"] == FANOUT_SYSTEM:
            content = f"answer from {kwargs['model']}"
        elif kwargs["system"].startswith(CROSSRANK_SYSTEM):
            content = VALID_RANKING
        else:
            content = "chairman synthesis"
        return _response(kwargs["model"], content)


class NarrowSpyClient:
    """Self-bounding client matching the-oracle's deliberately narrow seam."""

    def __init__(self):
        self.calls: list[dict] = []

    async def complete(self, *, model, system, user):
        call = {"model": model, "system": system, "user": user}
        self.calls.append(call)
        if system == FANOUT_SYSTEM:
            content = f"answer from {model}"
        elif system.startswith(CROSSRANK_SYSTEM):
            content = VALID_RANKING
        else:
            content = "chairman synthesis"
        return _response(model, content)


@pytest.mark.asyncio
async def test_run_council_without_dispatch_bounds_supports_self_bounding_client():
    client = NarrowSpyClient()

    await run_council(
        client=client,
        profile=PROFILES["premium"],
        user_query="Q",
        tag="self-bounded",
    )

    assert len(client.calls) == 9
    assert all(set(call) == {"model", "system", "user"} for call in client.calls)


@pytest.mark.asyncio
async def test_run_council_enforces_stage_token_and_provider_price_bounds():
    profile = PROFILES["premium"]
    client = SpyClient()

    await run_council(
        client=client,
        profile=profile,
        user_query="Q",
        tag="bounds",
        dispatch_bounds=DEFAULT_STAGE_BOUNDS,
    )

    fanout = [call for call in client.calls if call["system"] == FANOUT_SYSTEM]
    crossrank = [
        call for call in client.calls if call["system"].startswith(CROSSRANK_SYSTEM)
    ]
    chairman = [call for call in client.calls if call["system"] == CHAIRMAN_SYSTEM]
    assert (len(fanout), len(crossrank), len(chairman)) == (4, 4, 1)
    for call in fanout:
        assert call["max_tokens"] == FANOUT_MAX_TOKENS
        assert call["provider"] == provider_price_policy(call["model"])
    for call in crossrank:
        assert call["max_tokens"] == CROSSRANK_MAX_TOKENS
        assert call["provider"] == provider_price_policy(call["model"])
    for call in chairman:
        assert call["max_tokens"] == CHAIRMAN_MAX_TOKENS
        assert call["provider"] == provider_price_policy(call["model"])


@pytest.mark.asyncio
async def test_crossrank_parse_retry_keeps_judges_own_bounds_on_both_calls():
    profile = PROFILES["premium"]
    retry_judge = profile.models[1]
    judge_attempts = 0

    def response_for_call(kwargs, calls):
        nonlocal judge_attempts
        if kwargs["system"] == FANOUT_SYSTEM:
            return _response(kwargs["model"], f"answer from {kwargs['model']}")
        if kwargs["system"].startswith(CROSSRANK_SYSTEM):
            if kwargs["model"] == retry_judge:
                judge_attempts += 1
                if judge_attempts == 1:
                    return _response(retry_judge, "not JSON")
            return _response(kwargs["model"], VALID_RANKING)
        return _response(kwargs["model"], "chairman synthesis")

    client = SpyClient(response_for_call)
    await run_council(
        client=client,
        profile=profile,
        user_query="Q",
        tag="retry",
        dispatch_bounds=DEFAULT_STAGE_BOUNDS,
    )

    retry_calls = [
        call
        for call in client.calls
        if call["model"] == retry_judge
        and call["system"].startswith(CROSSRANK_SYSTEM)
    ]
    assert len(retry_calls) == 2
    for call in retry_calls:
        assert call["max_tokens"] == CROSSRANK_MAX_TOKENS
        assert call["provider"] == provider_price_policy(retry_judge)


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


@pytest.mark.asyncio
async def test_unbounded_dispatch_keeps_full_downstream_prompt_composition():
    profile = PROFILES["premium"]
    huge_response = "fanout-full-" + ("⚡" * 6_000)  # More than 16 KiB.
    huge_reasoning = "reasoning-full-" + ("💥" * 1_500)  # More than 4 KiB.

    def response_for_call(kwargs, calls):
        if kwargs["system"] == FANOUT_SYSTEM:
            content = huge_response if kwargs["model"] == profile.models[0] else "short answer"
            return _response(kwargs["model"], content)
        if kwargs["system"].startswith(CROSSRANK_SYSTEM):
            reasoning = huge_reasoning if kwargs["model"] == profile.models[0] else "short"
            return _response(
                kwargs["model"],
                json.dumps({"ranking": ["A", "B", "C"], "reasoning": reasoning}),
            )
        return _response(kwargs["model"], "chairman synthesis")

    client = SpyClient(response_for_call)
    await run_council(
        client=client,
        profile=profile,
        user_query="Q",
        tag="legacy-composition",
        dispatch_bounds=None,
    )

    crossrank_call = next(
        call
        for call in client.calls
        if call["model"] == profile.models[1]
        and call["system"].startswith(CROSSRANK_SYSTEM)
    )
    chairman_call = next(
        call for call in client.calls if call["system"] == CHAIRMAN_SYSTEM
    )
    # Review finding (3a-1 round 2): substring presence is not byte-identity — a
    # reordering/separator change would pass. Prove the None path composes the EXACT
    # strings the raw prompt functions produce from full, untruncated content: this is
    # the invariant that keeps the unmodified the-oracle's eval-gated prompts unchanged.
    responses_by_model = {}
    for call in client.calls:
        if call["system"] == FANOUT_SYSTEM:
            content = huge_response if call["model"] == profile.models[0] else "short answer"
            responses_by_model[call["model"]] = content
    judge = profile.models[1]
    expected_crossrank = crossrank_prompt(
        user_query="Q",
        others=[
            {"model_id": m, "content": responses_by_model[m]}
            for m in profile.models
            if m != judge
        ],
    )
    assert crossrank_call["user"] == expected_crossrank

    expected_rankings = []
    for m in profile.models:
        reasoning = huge_reasoning if m == profile.models[0] else "short"
        expected_rankings.append(
            {"judge_model": m, "ranking": ["A", "B", "C"], "reasoning": reasoning}
        )
    expected_chairman = chairman_prompt(
        user_query="Q",
        responses=[
            {"model_id": m, "content": responses_by_model[m]} for m in profile.models
        ],
        rankings=expected_rankings,
    )
    assert chairman_call["user"] == expected_chairman


@pytest.mark.asyncio
async def test_downstream_prompts_truncate_utf8_but_session_keeps_full_outputs():
    profile = PROFILES["premium"]
    huge_response = "⚡" * 21_846  # 65,538 UTF-8 bytes; cuts through a codepoint.
    huge_reasoning = "💥" * 16_385  # 65,540 UTF-8 bytes; cuts through a codepoint.

    def response_for_call(kwargs, calls):
        if kwargs["system"] == FANOUT_SYSTEM:
            content = huge_response if kwargs["model"] == profile.models[0] else "short answer"
            return _response(kwargs["model"], content)
        if kwargs["system"].startswith(CROSSRANK_SYSTEM):
            reasoning = huge_reasoning if kwargs["model"] == profile.models[0] else "short"
            return _response(
                kwargs["model"],
                json.dumps({"ranking": ["A", "B", "C"], "reasoning": reasoning}),
            )
        return _response(kwargs["model"], "chairman synthesis")

    client = SpyClient(response_for_call)
    session = await run_council(
        client=client,
        profile=profile,
        user_query="Q",
        tag="truncation",
        dispatch_bounds=DEFAULT_STAGE_BOUNDS,
    )

    judge_call = next(
        call
        for call in client.calls
        if call["model"] == profile.models[1]
        and call["system"].startswith(CROSSRANK_SYSTEM)
    )
    embedded_response = _between(
        judge_call["user"],
        "=== Response A ===\n",
        "\n\n=== Response B ===",
    )
    assert embedded_response.endswith("\n[truncated for bound]")
    assert len(embedded_response.encode("utf-8")) <= RESPONSE_EMBED_MAX_BYTES
    assert huge_response not in judge_call["user"]

    chairman_call = next(
        call for call in client.calls if call["system"] == CHAIRMAN_SYSTEM
    )
    embedded_reasoning = _between(
        chairman_call["user"],
        f"=== {profile.models[0]} ranked ===\nOrder (best first): A > B > C\nReasoning: ",
        f"\n\n=== {profile.models[1]} ranked ===",
    )
    assert embedded_reasoning.endswith("\n[truncated for bound]")
    assert (
        len(embedded_reasoning.encode("utf-8"))
        <= RANKING_REASONING_EMBED_MAX_BYTES
    )
    assert huge_reasoning not in chairman_call["user"]

    assert next(r for r in session.responses if r["model_id"] == profile.models[0])[
        "content"
    ] == huge_response
    assert next(
        ranking
        for ranking in session.rankings
        if ranking["judge_model"] == profile.models[0]
    )["reasoning"] == huge_reasoning


def test_cli_rejects_oversize_prompt_before_budget_or_network(
    tmp_path, tmp_spend_dir, monkeypatch
):
    prompt_file = tmp_path / "oversize.txt"
    prompt_file.write_bytes(b"x" * (cli.PROMPT_MAX_BYTES + 1))
    preflight = Mock(side_effect=AssertionError("preflight must not run"))
    record = Mock(side_effect=AssertionError("record_spend must not run"))
    network = Mock(side_effect=AssertionError("client must not be constructed"))
    monkeypatch.setattr(cli, "preflight_tool", preflight)
    monkeypatch.setattr(cli, "record_spend", record)
    monkeypatch.setattr(cli, "OpenRouterClient", network)

    result = CliRunner().invoke(
        cli.main,
        [
            "--profile",
            "premium",
            "--prompt-file",
            str(prompt_file),
            "--output",
            str(tmp_path / "out.md"),
        ],
    )

    assert result.exit_code == 1
    assert str(cli.PROMPT_MAX_BYTES + 1) in result.output
    assert str(cli.PROMPT_MAX_BYTES) in result.output
    preflight.assert_not_called()
    record.assert_not_called()
    network.assert_not_called()


def test_cli_accepts_prompt_exactly_at_byte_cap(
    tmp_path, tmp_spend_dir, monkeypatch
):
    prompt_file = tmp_path / "at-cap.txt"
    prompt_file.write_bytes(b"x" * cli.PROMPT_MAX_BYTES)
    output = tmp_path / "out.md"
    reached_pipeline = Mock()

    async def fake_run_council(**kwargs):
        reached_pipeline(kwargs)
        return SimpleNamespace(
            tag="cap",
            id="session",
            duration_ms=1,
            total_tokens_in=0,
            total_tokens_out=0,
            dropped_models=[],
            ranking_failed_models=[],
            responses=[],
            rankings=[],
            chairman_response=_response("anthropic/claude-opus-4.7", "done"),
        )

    fake_client = SimpleNamespace(aclose=Mock())

    async def fake_aclose():
        return None

    fake_client.aclose = fake_aclose
    monkeypatch.setattr(cli, "run_council", fake_run_council)
    monkeypatch.setattr(cli, "OpenRouterClient", Mock(return_value=fake_client))

    result = CliRunner().invoke(
        cli.main,
        [
            "--profile",
            "premium",
            "--prompt-file",
            str(prompt_file),
            "--output",
            str(output),
            "--tag",
            "cap",
            "--skip-budget-check",
        ],
    )

    assert result.exit_code == 0, result.output
    reached_pipeline.assert_called_once()
    pipeline_kwargs = reached_pipeline.call_args.args[0]
    assert len(pipeline_kwargs["user_query"].encode("utf-8")) == cli.PROMPT_MAX_BYTES
    assert pipeline_kwargs["dispatch_bounds"] is DEFAULT_STAGE_BOUNDS
    assert output.exists()


def test_truncation_never_expands_content_below_marker_sized_caps():
    """Review finding (3a-1 round 2): caps at or below the marker length previously
    sliced negatively and RETURNED MORE bytes than the cap. The cap must win over the
    marker: output byte length never exceeds max_bytes, for any cap value."""
    from council.pipeline import _truncate_for_prompt

    content = "x" * 100
    for max_bytes in (1, 21, 22, 23, 40):
        out = _truncate_for_prompt(content, max_bytes)
        assert len(out.encode("utf-8")) <= max_bytes, max_bytes

    multibyte = "⚡" * 50  # 3 bytes per codepoint: boundary must stay codepoint-safe
    for max_bytes in (1, 2, 21, 22):
        out = _truncate_for_prompt(multibyte, max_bytes)
        assert len(out.encode("utf-8")) <= max_bytes, max_bytes
