import json

import pytest
from httpx import Response

from council.client import OpenRouterClient, ModelResponse, ClientError


def _ok_response():
    return {
        "choices": [{"message": {"content": "ok"}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1},
    }


@pytest.mark.asyncio
async def test_complete_includes_max_tokens_when_set(fake_api_key, httpx_mock):
    httpx_mock.add_response(json=_ok_response())
    client = OpenRouterClient()
    await client.complete(model="m", system="s", user="u", max_tokens=1500)
    body = json.loads(httpx_mock.get_request().content)
    assert body["max_tokens"] == 1500
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_omits_max_tokens_when_unset(fake_api_key, httpx_mock):
    httpx_mock.add_response(json=_ok_response())
    client = OpenRouterClient()
    await client.complete(model="m", system="s", user="u")
    body = json.loads(httpx_mock.get_request().content)
    assert "max_tokens" not in body
    await client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", [0, -1, 1.5, "100", True, False])
async def test_complete_rejects_invalid_max_tokens(fake_api_key, httpx_mock, bad):
    client = OpenRouterClient()
    with pytest.raises(ClientError):
        await client.complete(model="m", system="s", user="u", max_tokens=bad)
    # A rejected max_tokens must fail closed before any network call.
    assert len(httpx_mock.get_requests()) == 0
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_includes_provider_when_set(fake_api_key, httpx_mock):
    httpx_mock.add_response(json=_ok_response())
    client = OpenRouterClient()
    prov = {
        "allow_fallbacks": False,
        "require_parameters": True,
        "max_price": {"prompt": 15.0, "completion": 75.0, "request": 0},
    }
    await client.complete(model="m", system="s", user="u", provider=prov)
    body = json.loads(httpx_mock.get_request().content)
    assert body["provider"] == prov
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_omits_provider_when_unset(fake_api_key, httpx_mock):
    httpx_mock.add_response(json=_ok_response())
    client = OpenRouterClient()
    await client.complete(model="m", system="s", user="u")
    body = json.loads(httpx_mock.get_request().content)
    assert "provider" not in body
    await client.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", ["x", 5, [1], True, ()])
async def test_complete_rejects_non_dict_provider(fake_api_key, httpx_mock, bad):
    client = OpenRouterClient()
    with pytest.raises(ClientError):
        await client.complete(model="m", system="s", user="u", provider=bad)
    assert len(httpx_mock.get_requests()) == 0
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_returns_typed_response(fake_api_key, httpx_mock):
    httpx_mock.add_response(
        url="https://openrouter.ai/api/v1/chat/completions",
        method="POST",
        json={
            "choices": [{"message": {"content": "hello world"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        },
    )
    client = OpenRouterClient()
    resp = await client.complete(
        model="openai/gpt-X",
        system="You are helpful.",
        user="hi",
    )
    assert isinstance(resp, ModelResponse)
    assert resp.model_id == "openai/gpt-X"
    assert resp.content == "hello world"
    assert resp.tokens_in == 10
    assert resp.tokens_out == 5
    assert resp.latency_ms > 0
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_captures_returned_model_generation_cost_finish(fake_api_key, httpx_mock):
    httpx_mock.add_response(
        json={
            "id": "gen-abc123",
            "model": "anthropic/claude-opus-4.7",
            "choices": [{"message": {"content": "hi"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 20, "completion_tokens": 8, "cost": 0.0123},
        }
    )
    client = OpenRouterClient()
    resp = await client.complete(model="anthropic/claude-opus-4.7", system="s", user="u")
    assert resp.model_id == "anthropic/claude-opus-4.7"  # requested id — lineage
    assert resp.returned_model_id == "anthropic/claude-opus-4.7"  # served id — audit
    assert resp.generation_id == "gen-abc123"
    assert resp.cost == 0.0123
    assert resp.finish_reason == "stop"
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_returned_model_can_differ_from_requested(fake_api_key, httpx_mock):
    # OpenRouter may serve a different endpoint/model; the client records BOTH and keeps
    # lineage on the REQUESTED id so the-oracle can enforce returned==requested (finding 5).
    httpx_mock.add_response(
        json={
            "id": "gen-x",
            "model": "anthropic/claude-opus-4.7-alt",
            "choices": [{"message": {"content": "hi"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "cost": 0.001},
        }
    )
    client = OpenRouterClient()
    resp = await client.complete(model="anthropic/claude-opus-4.7", system="s", user="u")
    assert resp.model_id == "anthropic/claude-opus-4.7"
    assert resp.returned_model_id == "anthropic/claude-opus-4.7-alt"
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_missing_optional_fields_default_to_none(fake_api_key, httpx_mock):
    httpx_mock.add_response(json=_ok_response())
    client = OpenRouterClient()
    resp = await client.complete(model="m", system="s", user="u")
    assert resp.returned_model_id is None
    assert resp.generation_id is None
    assert resp.cost is None
    assert resp.finish_reason is None
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_sends_correct_payload(fake_api_key, httpx_mock):
    httpx_mock.add_response(
        url="https://openrouter.ai/api/v1/chat/completions",
        method="POST",
        json={
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
        },
    )
    client = OpenRouterClient()
    await client.complete(model="m", system="sys", user="usr")
    sent = httpx_mock.get_request()
    assert sent.headers["authorization"] == "Bearer sk-or-v1-fake-for-tests"
    import json
    body = json.loads(sent.content)
    assert body["model"] == "m"
    assert body["messages"] == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ]
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_retries_on_5xx_then_succeeds(fake_api_key, httpx_mock):
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(
        json={
            "choices": [{"message": {"content": "ok"}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
        }
    )
    client = OpenRouterClient(max_retries=1)
    resp = await client.complete(model="m", system="s", user="u")
    assert resp.content == "ok"
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_raises_on_persistent_5xx(fake_api_key, httpx_mock):
    httpx_mock.add_response(status_code=503)
    httpx_mock.add_response(status_code=503)
    client = OpenRouterClient(max_retries=1)
    with pytest.raises(ClientError) as exc:
        await client.complete(model="m", system="s", user="u")
    assert "503" in str(exc.value)
    await client.aclose()


@pytest.mark.asyncio
async def test_complete_raises_on_content_filter_no_retry(fake_api_key, httpx_mock):
    # Content-policy refusals are non-retryable
    httpx_mock.add_response(
        status_code=400,
        json={"error": {"code": "content_filter", "message": "refused"}},
    )
    client = OpenRouterClient(max_retries=3)
    with pytest.raises(ClientError) as exc:
        await client.complete(model="m", system="s", user="u")
    assert "content_filter" in str(exc.value) or "refused" in str(exc.value)
    # Should have made exactly 1 request, not retried
    assert len(httpx_mock.get_requests()) == 1
    await client.aclose()


@pytest.mark.asyncio
async def test_missing_api_key_raises_at_init(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ClientError) as exc:
        OpenRouterClient()
    assert "OPENROUTER_API_KEY" in str(exc.value)
