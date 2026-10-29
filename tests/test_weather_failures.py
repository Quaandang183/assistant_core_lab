"""Weather client failure modes (worksheet lab04/worksheets/external_api_failure.md)."""

import httpx
import pytest

from assistant_api.weather import ExternalServiceError, WeatherClient


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr("assistant_api.weather.time.sleep", lambda _s: None)


def client_with(handler) -> WeatherClient:
    transport = httpx.MockTransport(handler)
    return WeatherClient("https://example.test/forecast", 10.76, 106.68, retries=1, transport=transport)


def _timeout(req):
    raise httpx.ConnectTimeout("timeout", request=req)


@pytest.mark.parametrize(
    "handler",
    [
        _timeout,  # timeout
        lambda req: httpx.Response(500),  # upstream error
        lambda req: httpx.Response(200, json={}),  # malformed JSON (no "current")
        lambda req: httpx.Response(429),  # rate limited
    ],
    ids=["timeout", "upstream_500", "malformed_json", "rate_limited_429"],
)
def test_failure_without_cache_raises_external_service_error(handler):
    with pytest.raises(ExternalServiceError):
        client_with(handler).current()


def test_failure_is_retried_once():
    calls = {"n": 0}

    def always_500(req):
        calls["n"] += 1
        return httpx.Response(500)

    with pytest.raises(ExternalServiceError):
        client_with(always_500).current()
    assert calls["n"] == 2  # first try + 1 retry
