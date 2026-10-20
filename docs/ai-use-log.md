# AI Use Log

## Entry: Lab 3 — AI Extension Review

- **Date**: 2026-10-20
- **AI Tool**: Antigravity Coding Assistant (Gemini)
- **Task**: Extend `assistant_core` with a `help` feature listing bot capabilities.

### Prompt Given to AI
```text
Please extend the assistant_core service with a 'help' feature that lists what the bot can do (greetings, tuition fees, office info, and handbook rules).
```

### AI Proposed Output
The AI suggested adding help keyword matching and returning a help message.

### Human Review & Manual Improvements
1. **Architecture Compliance (`route -> service -> responder`)**:
   - Ensured `router.py` only classifies the intent (`Intent.HELP`) rather than formatting or returning messages directly.
   - Updated `models.py` with `Intent.HELP`.
   - Placed the response logic inside `AssistantService.handle` in `service.py`.

2. **Input Normalization & Multi-language Support**:
   - Cleaned trailing punctuation and whitespace.
   - Added support for synonyms and Vietnamese phrasing (`"tro giup"`, `"huong dan"`, `"support"`).

3. **Automated Testing & Quality Checks**:
   - Added parameterized tests in `tests/test_router.py` (`test_route_help`).
   - Added `test_handle_help` in `tests/test_service.py`.
   - Verified that no user PII/text is logged and no new dependencies were introduced.

### Verification
- **Automated Tests**: Ran `pytest` -> 50 passed in 0.87s.
- **Linter**: Ran `ruff check` -> All checks passed.
- **Manual CLI Test**: Ran `python -m assistant_core "help"` -> Output correctly formatted with intent `help` and log metadata intact.
