"""F8b Task 3b — every council provider attempt reaches accounting."""

import asyncio

import pytest

from council.client import ClientError, ModelResponse
from council.pipeline import ChairmanFailure, FanoutAbort, run_council
from council.profiles import Profile
from council.prompts import CROSSRANK_SYSTEM


class SpyClient:
    """Deterministic no-network provider boundary spy."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        await asyncio.sleep(0)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class GatedCrossrankClient:
    """Lets one judge finish while the other judges remain genuinely in flight."""

    def __init__(self, first_outcome=None):
        self.first_outcome = first_outcome
        self.first_finished = asyncio.Event()
        self.release_siblings = asyncio.Event()
        self.siblings_started = asyncio.Event()
        self._waiting_siblings = 0

    async def complete(self, **kwargs):
        await asyncio.sleep(0)
        model = kwargs["model"]
        if kwargs["system"] == CROSSRANK_SYSTEM:
            if model == "m1":
                self.first_finished.set()
                if isinstance(self.first_outcome, BaseException):
                    raise self.first_outcome
                return _response(model, VALID_RANKING)
            self._waiting_siblings += 1
            if self._waiting_siblings == 3:
                self.siblings_started.set()
            await self.release_siblings.wait()
            return _response(model, VALID_RANKING)
        if kwargs["system"] != CROSSRANK_SYSTEM:
            return _response(model, f"answer-{model}")


class BlockingClient:
    """A real suspension point for caller-cancellation propagation."""

    def __init__(self):
        self.all_started = asyncio.Event()
        self.never_release = asyncio.Event()
        self.started = 0
        self.cancelled = 0

    async def complete(self, **kwargs):
        self.started += 1
        if self.started == 4:
            self.all_started.set()
        try:
            await self.never_release.wait()
        except asyncio.CancelledError:
            self.cancelled += 1
            raise


@pytest.fixture
def profile():
    return Profile(
        name="capture",
        models=("m1", "m2", "m3", "m4"),
        chairman="m1",
        max_cost_per_query=10.0,
    )


def _response(model, content):
    return ModelResponse(
        model_id=model,
        content=content,
        tokens_in=11,
        tokens_out=7,
        latency_ms=3,
        returned_model_id=f"served/{model}",
        generation_id=f"gen-{model}-{content}",
        cost=0.0123,
        finish_reason="stop",
    )


def _assert_delivered_once(delivered):
    """No provider attempt may cross the accounting boundary twice."""
    keys = [
        (
            row["stage"],
            row["requested_model"],
            row["generation_id"],
            row.get("error"),
        )
        for row in delivered
    ]
    assert len({id(row) for row in delivered}) == len(delivered)
    assert len(set(keys)) == len(keys)


VALID_RANKING = '{"ranking": ["A", "B", "C"], "reasoning": "ok"}'


def _happy_outcomes():
    return [
        *[_response(f"m{i}", f"answer-{i}") for i in range(1, 5)],
        *[_response(f"m{i}", VALID_RANKING) for i in range(1, 5)],
        _response("m1", "synthesis"),
    ]


@pytest.mark.asyncio
async def test_happy_path_delivers_nine_attempts_matching_session(profile):
    delivered = []
    session = await run_council(
        client=SpyClient(_happy_outcomes()),
        profile=profile,
        user_query="Q",
        tag="capture",
        on_attempt=delivered.append,
    )

    assert len(delivered) == 9
    assert delivered == session.attempts
    assert all(got is stored for got, stored in zip(delivered, session.attempts))
    assert [row["stage"] for row in delivered] == [
        "fanout", "fanout", "fanout", "fanout",
        "crossrank", "crossrank", "crossrank", "crossrank",
        "chairman",
    ]
    assert all("error" not in row for row in session.attempts)
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_parse_retry_path_delivers_all_thirteen_attempts(profile):
    delivered = []
    outcomes = [
        *[_response(f"m{i}", f"answer-{i}") for i in range(1, 5)],
        *[_response(f"m{i}", "not json") for i in range(1, 5)],
        *[_response(f"m{i}", VALID_RANKING) for i in range(1, 5)],
        _response("m1", "synthesis"),
    ]

    session = await run_council(
        client=SpyClient(outcomes),
        profile=profile,
        user_query="Q",
        tag="capture",
        on_attempt=delivered.append,
    )

    assert len(delivered) == len(session.attempts) == 13
    assert {id(row) for row in delivered} == {id(row) for row in session.attempts}
    assert [row["stage"] for row in delivered].count("crossrank") == 8
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_fanout_abort_carries_survivors_and_exact_error_records(profile):
    delivered = []
    outcomes = [
        _response("m1", "answer-1"),
        ClientError("m2 timed out"),
        ValueError("m3 malformed"),
        _response("m4", "answer-4"),
    ]
    expected_message = (
        "Council unavailable: two or more models failed in Stage 1 (['m2', 'm3']). "
        "Fall back to single-model review."
    )

    with pytest.raises(FanoutAbort) as caught:
        await run_council(
            client=SpyClient(outcomes),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )

    error_m2 = {
        "stage": "fanout",
        "requested_model": "m2",
        "returned_model_id": None,
        "generation_id": None,
        "tokens_in": None,
        "tokens_out": None,
        "cost": None,
        "finish_reason": None,
        "error": "ClientError: m2 timed out",
    }
    error_m3 = {**error_m2, "requested_model": "m3", "error": "ValueError: m3 malformed"}
    assert isinstance(caught.value, RuntimeError)
    assert str(caught.value) == expected_message
    assert caught.value.stage == "fanout"
    assert len(caught.value.attempts) == 4
    assert [row["requested_model"] for row in caught.value.attempts] == ["m1", "m4", "m2", "m3"]
    assert caught.value.attempts[2:] == [error_m2, error_m3]
    assert len(delivered) == 4
    assert error_m2 in delivered and error_m3 in delivered
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_chairman_failure_carries_prior_attempts_and_preserves_chain(profile):
    delivered = []
    cause = ClientError("chairman timeout")
    outcomes = [*_happy_outcomes()[:-1], cause]
    expected_message = (
        "Chairman synthesis failed (m1): chairman timeout. "
        "Stage-1 produced 4 responses; Stage-2 produced 4 rankings. "
        "Council session JSON was not written. "
        "Fall back to single-model review or retry."
    )

    with pytest.raises(ChairmanFailure) as caught:
        await run_council(
            client=SpyClient(outcomes),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )

    assert isinstance(caught.value, RuntimeError)
    assert str(caught.value) == expected_message
    assert caught.value.stage == "chairman"
    assert caught.value.__cause__ is cause
    assert caught.value.attempts == delivered
    assert len(caught.value.attempts) == 9
    assert caught.value.attempts[-1] == {
        "stage": "chairman",
        "requested_model": "m1",
        "returned_model_id": None,
        "generation_id": None,
        "tokens_in": None,
        "tokens_out": None,
        "cost": None,
        "finish_reason": None,
        "error": "ClientError: chairman timeout",
    }
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_crossrank_client_error_delivers_response_then_error(profile):
    delivered = []
    outcomes = [
        *[_response(f"m{i}", f"answer-{i}") for i in range(1, 5)],
        _response("m1", "not json"),
        *[_response(f"m{i}", VALID_RANKING) for i in range(2, 5)],
        ClientError("judge retry failed"),
        _response("m1", "synthesis"),
    ]

    session = await run_council(
        client=SpyClient(outcomes),
        profile=profile,
        user_query="Q",
        tag="capture",
        on_attempt=delivered.append,
    )

    assert len(session.attempts) == 9
    assert len(delivered) == 10
    error = next(row for row in delivered if "error" in row)
    assert error["stage"] == "crossrank"
    assert error["requested_model"] == "m1"
    assert error["error"] == "ClientError: judge retry failed"
    first = next(
        row
        for row in delivered
        if row["stage"] == "crossrank" and row["requested_model"] == "m1" and "error" not in row
    )
    assert any(first is row for row in session.attempts)
    assert error not in session.attempts
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_omitting_callback_preserves_success_session(profile):
    session = await run_council(
        client=SpyClient(_happy_outcomes()),
        profile=profile,
        user_query="Q",
        tag="capture",
    )

    assert len(session.attempts) == 9
    assert [row["stage"] for row in session.attempts] == [
        "fanout", "fanout", "fanout", "fanout",
        "crossrank", "crossrank", "crossrank", "crossrank",
        "chairman",
    ]
    assert all("error" not in row for row in session.attempts)


@pytest.mark.asyncio
async def test_callback_failure_mid_fanout_propagates(profile):
    failure = LookupError("ledger unavailable")
    delivered = []

    def accounting_boundary(attempt):
        delivered.append(attempt)
        if len(delivered) == 2:
            raise failure

    with pytest.raises(LookupError) as caught:
        await run_council(
            client=SpyClient(_happy_outcomes()),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=accounting_boundary,
        )

    assert caught.value is failure
    assert len(delivered) == 4
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_chairman_non_client_error_is_delivered_then_reraised_raw(profile):
    failure = ValueError("billed 2xx malformed chairman payload")
    delivered = []

    with pytest.raises(ValueError) as caught:
        await run_council(
            client=SpyClient([*_happy_outcomes()[:-1], failure]),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )

    assert caught.value is failure
    assert delivered[-1] == {
        "stage": "chairman",
        "requested_model": "m1",
        "returned_model_id": None,
        "generation_id": None,
        "tokens_in": None,
        "tokens_out": None,
        "cost": None,
        "finish_reason": None,
        "error": "ValueError: billed 2xx malformed chairman payload",
    }
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_crossrank_non_client_error_drains_judges_then_reraises_raw(profile):
    failure = ValueError("billed 2xx malformed judge payload")
    client = GatedCrossrankClient(first_outcome=failure)
    delivered = []
    task = asyncio.create_task(
        run_council(
            client=client,
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )
    )
    await client.first_finished.wait()
    await client.siblings_started.wait()
    for _ in range(10):
        if task.done():
            break
        await asyncio.sleep(0)
    returned_before_siblings_finished = task.done()
    client.release_siblings.set()

    with pytest.raises(ValueError) as caught:
        await task

    assert caught.value is failure
    assert not returned_before_siblings_finished
    crossrank = [row for row in delivered if row["stage"] == "crossrank"]
    assert [row["requested_model"] for row in crossrank] == ["m1", "m2", "m3", "m4"]
    assert crossrank[0]["error"] == "ValueError: billed 2xx malformed judge payload"
    assert all("error" not in row for row in crossrank[1:])
    assert len(delivered) == 8
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_crossrank_callback_failure_drains_before_raise_and_then_stays_quiet(profile):
    client = GatedCrossrankClient()
    failure = LookupError("ledger unavailable")
    callback_failed = asyncio.Event()
    delivered = []

    def accounting_boundary(attempt):
        delivered.append(attempt)
        if attempt["stage"] == "crossrank" and attempt["requested_model"] == "m1":
            callback_failed.set()
            raise failure

    task = asyncio.create_task(
        run_council(
            client=client,
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=accounting_boundary,
        )
    )
    await callback_failed.wait()
    await client.siblings_started.wait()
    for _ in range(10):
        if task.done():
            break
        await asyncio.sleep(0)
    returned_before_siblings_finished = task.done()
    callbacks_when_task_finished = len(delivered)
    client.release_siblings.set()

    with pytest.raises(LookupError) as caught:
        await task

    callbacks_at_raise = len(delivered)
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert caught.value is failure
    assert not returned_before_siblings_finished
    assert callbacks_when_task_finished == 5
    assert callbacks_at_raise == 8
    assert len(delivered) == callbacks_at_raise
    _assert_delivered_once(delivered)


def test_run_council_documents_cancellation_contract():
    doc = " ".join((run_council.__doc__ or "").split())

    assert "Cancellation of the caller cancels the gather and its children" in doc
    assert "a spontaneous child CancelledError propagates" in doc


@pytest.mark.asyncio
async def test_cancelling_run_council_cancels_children_and_delivers_nothing_afterward(profile):
    client = BlockingClient()
    delivered = []
    task = asyncio.create_task(
        run_council(
            client=client,
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )
    )
    await client.all_started.wait()

    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    callbacks_at_cancel = len(delivered)
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert client.cancelled == 4
    assert callbacks_at_cancel == 0
    assert len(delivered) == callbacks_at_cancel


@pytest.mark.asyncio
async def test_chairman_callback_failure_propagates_once_and_stays_quiet(profile):
    failure = LookupError("chairman accounting failed")
    delivered = []

    def accounting_boundary(attempt):
        delivered.append(attempt)
        if attempt["stage"] == "chairman":
            raise failure

    with pytest.raises(LookupError) as caught:
        await run_council(
            client=SpyClient(_happy_outcomes()),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=accounting_boundary,
        )

    callbacks_at_raise = len(delivered)
    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert caught.value is failure
    assert callbacks_at_raise == 9
    assert len(delivered) == callbacks_at_raise
    assert delivered[-1]["stage"] == "chairman"
    _assert_delivered_once(delivered)


@pytest.mark.asyncio
async def test_crossrank_first_client_error_is_preserved_in_later_chairman_failure(profile):
    judge_error = ClientError("judge first call failed")
    chairman_error = ClientError("chairman failed later")
    delivered = []
    outcomes = [
        *[_response(f"m{i}", f"answer-{i}") for i in range(1, 5)],
        judge_error,
        *[_response(f"m{i}", VALID_RANKING) for i in range(2, 5)],
        chairman_error,
    ]

    with pytest.raises(ChairmanFailure) as caught:
        await run_council(
            client=SpyClient(outcomes),
            profile=profile,
            user_query="Q",
            tag="capture",
            on_attempt=delivered.append,
        )

    attempts = caught.value.attempts
    assert attempts == delivered
    assert [row["stage"] for row in attempts] == [
        "fanout",
        "fanout",
        "fanout",
        "fanout",
        "crossrank",
        "crossrank",
        "crossrank",
        "crossrank",
        "chairman",
    ]
    assert attempts[4]["requested_model"] == "m1"
    assert attempts[4]["error"] == "ClientError: judge first call failed"
    assert attempts[-1]["error"] == "ClientError: chairman failed later"
    _assert_delivered_once(delivered)
