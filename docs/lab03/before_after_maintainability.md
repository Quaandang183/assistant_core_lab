# Lab 3 — Before / after maintainability comparison

| Question | Before | After |
|---|---|---|
| Where would you change the credit rate? How many places? | Hardcoded in script, 2+ places | In `.env` (or `config.py`), 1 place |
| Can you run the tests without internet or an API key? | No (required live API key) | Yes (uses `StubLLMResponder`) |
| What happens if `handbook.json` is missing? | Unhandled `FileNotFoundError` crash | Handled with a clear `DataError` |
| Is any secret printed or logged? | Yes (API key exposed) | No (`repr=False` and structured logging) |
| How long does it take a new teammate to find the fee logic? | Minutes (scrolling monolith script) | Seconds (directly in `tools.py`) |
| Number of global variables | > 5 | 0 |
| Number of bare `except:` blocks | > 1 | 0 (uses specific `ProviderError`) |
| Lines in the longest function | ~50+ lines | ~20 lines |
| `ruff check` issues | Multiple warnings/errors | 0 issues |
| Can you swap the LLM without touching the service? | No (tightly coupled) | Yes (via `Responder` protocol) |

**Three sentences summary:**
1. **What improved most:** Separation of concerns improved the most, allowing exact tuition math in `tools.py` and offline testing with `StubLLMResponder` without network dependencies.
2. **What got more complex:** Project setup and file management became slightly more complex due to multiple modular files (`models.py`, `responder.py`, `service.py`) and environment dependency injection.
3. **What you would still change:** I would still add full type annotations for all remaining helper methods and implement automated integration tests for edge-case CLI inputs.