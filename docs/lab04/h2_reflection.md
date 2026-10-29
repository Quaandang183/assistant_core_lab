# H2 — Reflection: `service.handle()` (Lab 3) vs `POST /v1/chat` (Lab 4)

> Draft: rewrite it in your own words before you submit.

Calling `service.handle()` is a normal Python call: the caller must be Python code in the same program, import the package and
build the objects itself. Calling `POST /v1/chat` sends a request over the network, so any program in any language (a browser,
a phone app, a test) can use the assistant with plain JSON. A team prefers the HTTP version because there is one contract for
every caller, the backend can run on a server and change inside without breaking clients, and we gain status codes, validation,
an API key, rate limiting and automatic `/docs`. The price is a little more latency and more things that can fail.
