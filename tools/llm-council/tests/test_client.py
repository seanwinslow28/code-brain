import pytest
from httpx import Response

from council.client import OpenRouterClient, ModelResponse, ClientError


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
