# Architecture Note — assistant_core

`assistant_core` is a small Python package. The CLI today, the FastAPI backend (Lab 4) and the UI (Lab 7)
all call one entry point: `AssistantService.handle`.

## 1. Modules

| Module | Responsibility |
| :--- | :--- |
| `config.py` | Read settings from the environment (`.env`) and validate them. |
| `errors.py` | Named exceptions: `AssistantError`, `ConfigError`, `DataError`, `InvalidRequest`, `ProviderError`. |
| `models.py` | Public contract: `Message`, `Response`, `Intent`, `Source`. |
| `router.py` | Choose an `Intent` with simple rules. |
| `knowledge.py` | Office directory (CSV) and handbook (JSON) with keyword search. |
| `tools.py` | Deterministic tuition calculation (pure functions). |
| `responder.py` | Response generation behind one `Responder` protocol (stub LLM, template). |
| `service.py` | `AssistantService.handle(Message) -> Response` — the only entry point. |
| `logging_setup.py` | Structured JSON logs to stderr. |
| `__main__.py` | Command-line interface; wires the dependencies together. |

```text
CLI (__main__) -> AssistantService -> router / tools / knowledge / responder
                  config, models, errors, logging are shared by all modules
```

## 2. Service interface

```python
AssistantService.handle(msg: Message) -> Response
```

- `Message`: `text` (1–2000 characters), `session_id` (default `"local"`).
- `Response`: `answer`, `intent`, `sources[]`, `degraded` (`True` if a fallback answered).
- Errors:
  - Invalid input: `ValidationError` (empty or too long text) or `InvalidRequest` (e.g. fee question without credits, credits out of range).
  - Startup: `ConfigError` (bad or missing settings) and `DataError` (missing or malformed knowledge files).
  - Provider failures never reach the caller: the service falls back to `TemplateResponder` and sets `degraded=True`.

## 3. Design decisions

1. **Fees are computed in `tools.py`, never by an LLM.** The result is exact, deterministic and covered by a
   characterisation test (`18 credits + 2 retake = 9,450,000 VND`, same as the original script).
2. **The LLM sits behind the `Responder` protocol and is injected into the service.** The stub needs no API key,
   so tests and CI run offline; a real provider can be added in Week 4 without editing `service.py`.
3. **Configuration comes from the environment.** Rates and limits live in `.env` (documented in `.env.example`),
   `llm_api_key` has `repr=False`, and logs record only intent, latency, session and degraded flag — never the key
   or the full user message.
