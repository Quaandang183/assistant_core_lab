# Lab 4 homework — design for an external service that goes down

Service chosen (weather / maps / news / other approved): **weather (Open-Meteo)**   Base URL: **https://api.open-meteo.com/v1/forecast**

| Failure | How you simulate it | What your API returns | What the user sees |
|---|---|---|---|
| timeout | transport raises ConnectTimeout | retry once; then the last cached weather with `stale: true`, or 503 `weather_service_unavailable` if there is no cache | old weather marked "outdated", or "Weather is unavailable right now" |
| 500 from upstream | MockTransport returns 500 | same as above | same as above |
| malformed JSON | MockTransport returns `{}` | same as above (the missing `current` key is treated as a failure) | same as above |
| rate limited (429) | MockTransport returns 429 | same as above | same as above |

Timeout value and why: **3 s** — a page should not freeze because of a side feature such as weather.
Retries and why: **1 retry** (2 attempts, short pause between them) — covers a brief network glitch without making the user wait long.
Cache TTL and why: **600 s (10 min)** — weather changes slowly, so the cache saves calls and gives a "backup plan" when the site is down.
Tests added (file + names): `tests/test_weather_failures.py` — `test_failure_without_cache_raises_external_service_error[timeout|upstream_500|malformed_json|rate_limited_429]`,
`test_failure_is_retried_once`; in `tests/test_api.py` — `test_weather_down_returns_503`, `test_weather_stale_cache_when_upstream_fails`.
