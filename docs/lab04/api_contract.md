# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | — | 200 {status, version} | — | ops, UI |
| POST | /v1/chat | body `{message: str 1-2000, session_id: str ≤64, default "anonymous"}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 `invalid_request`; 429 `too_many_requests` | UI, tests |
| POST | /v1/feedback | body `{request_id: str 1-64, rating: -1/0/1, comment?: str ≤500}` | 201 `{request_id, rating, comment, id, created_at}` | 422 `invalid_request` | UI |
| GET | /v1/feedback | header X-API-Key | 200 list of feedback | 401 `missing_or_invalid_api_key` | staff dashboard |
| GET | /v1/weather | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 `weather_service_unavailable` | UI |
| GET | /v1/offices | — | 200 `[{name, room, hours}]` sorted by name | — | UI |

Questions:
1. **Which fields are required, and what are their limits?**
   `message` is required (1–2000 characters); `session_id` is optional (≤64). For feedback, `request_id` (1–64) and `rating`
   (only -1, 0 or 1) are required; `comment` is optional (≤500). The admin endpoint requires the `X-API-Key` header.
2. **What does the UI show for each error code?**
   `invalid_request` (422): "Please type a question between 1 and 2000 characters" (or the field message);
   `too_many_requests` (429): "Too many questions, please wait a minute";
   `missing_or_invalid_api_key` (401): staff login / "not allowed";
   `weather_service_unavailable` (503): "Weather is unavailable right now"; the rest of the app keeps working.
3. **What changes would force a `/v2`?**
   Changes that break existing clients: renaming or removing a response field (for example `answer`), changing a field's type,
   making an optional request field required, or changing a status code or the error shape. Adding an optional field or a new
   endpoint does not need `/v2`.
