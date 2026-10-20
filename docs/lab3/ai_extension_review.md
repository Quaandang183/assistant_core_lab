# Lab 3 — AI extension review

1. Ask an AI coding assistant to extend your service with ONE feature, e.g.
   "Add an 'exam absence' answer that tells students the deadline from the handbook."
2. Paste the prompt you used:

```text
Please extend the assistant_core service with a 'help' feature that lists what the bot can do (greetings, tuition fees, office info, and handbook rules).
```

3. Review the generated code manually. Document **at least three changes** you made:

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | AI returned the help string directly inside `router.py` without adding an `Intent` enum member. | Violated the system architecture (`route -> service -> responder`). Router should only classify intent; `AssistantService` must handle responses. | Added `HELP = "help"` to `Intent` in `models.py`, updated `router.py` to return `Intent.HELP`, and added handler logic inside `AssistantService.handle` in `service.py`. | Preserves separation of concerns and complies with the service contract in `docs/architecture.md`. |
| 2 | AI checked for exact match `if text == "help":`. | Fragile input handling: fails on capitalized input (`HELP`), punctuation (`help!`), leading/trailing spaces, or Vietnamese/synonyms (`tro giup`, `support`). | Defined `HELP_KEYWORDS = frozenset({"help", "support", "tro giup", "huong dan"})` and checked against normalized text `t = text.lower().strip().rstrip("?!.")`. | Improves robustness and user experience without adding heavy external dependencies. |
| 3 | AI did not write any automated tests for router or service. | No test coverage for the new feature; regressions would not be caught by `pytest` or CI. | Added `test_route_help` with parameterized inputs in `tests/test_router.py` and `test_handle_help` in `tests/test_service.py`. | Ensures test suite coverage and automated verification (all 50 tests pass). |

Checklist:
- [x] Interfaces respected? (`route -> service -> responder` flow preserved)
- [x] New dependencies? None (uses standard Python libraries and existing `pydantic`)
- [x] Secrets? None hardcoded
- [x] Logging of user data? None (CLI continues to log only metadata: intent, latency, session, degraded)
- [x] Tests added and meaningful? Yes, added unit tests in both `test_router.py` and `test_service.py`

Record the use in `docs/ai-use-log.md`.
