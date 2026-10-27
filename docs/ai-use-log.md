# AI Use Log

## Entry: Lab 3 — AI Extension Review (Branch TV2)

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
- **Automated Tests**: Ran `pytest` -> 50 passed.
- **Linter**: Ran `ruff check` -> All checks passed.
- **Manual CLI Test**: Ran `python -m assistant_core "help"` -> Output correctly formatted with intent `help` and log metadata intact.

---

## Entry: Lab 3 — AI Extension Review (Branch TV3)

- **Date**: 2026-10-20
- **AI Tool**: Antigravity Coding Assistant (Gemini)
- **Task**: Extend `assistant_core` with an `exam absence` feature that tells students the deadline from the handbook.

### Prompt Given to AI
```text
Extend the assistant_core service with an 'exam absence' feature that answers students' questions about the exam absence deadline using rule H26-7.2 from handbook.json.
```

### AI Proposed Output
The AI suggested parsing the exam absence question and returning the deadline.

### Human Review & Manual Improvements
1. **Dynamic Handbook Lookup & Source Citation**:
   - Replaced static strings with dynamic lookup via `self.handbook.search("exam absence")`.
   - Included official source citation: `Source(id="H26-7.2", title="Exam absence")`.

2. **Architecture Compliance (`route -> service -> responder`)**:
   - Registered `Intent.EXAM_ABSENCE` in `models.py`.
   - Centralized routing in `router.py` using `EXAM_ABSENCE_KEYWORDS` (covering synonyms and Vietnamese queries like `"vang thi"`).
   - Delegated execution to `_exam_absence` in `service.py`.

3. **Automated Testing & Edge-Case Protection**:
   - Added graceful fallback in case the rule is missing from data.
   - Added `test_route_exam_absence` in `tests/test_router.py`.
   - Added `test_handle_exam_absence` in `tests/test_service.py`.

### Verification
- **Automated Tests**: Ran `pytest` -> 49 passed.
- **Linter**: Ran `ruff check` -> All checks passed.
- **Manual CLI Test**: Ran `python -m assistant_core "what is the exam absence deadline?"` -> Printed deadline with citation `(source: H26-7.2 - Exam absence)` and logged metadata correctly.
