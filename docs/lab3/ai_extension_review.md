# Lab 3 — AI extension review

1. **Feature**: "Add an 'exam absence' answer that tells students the deadline from the handbook."
2. **Paste the prompt you used**:

```text
Extend the assistant_core service with an 'exam absence' feature that answers students' questions about the exam absence deadline using rule H26-7.2 from handbook.json.
```

3. **Review the generated code manually. Document at least three changes you made**:

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | AI hardcoded a static response string (`"Exam absence deadline is 3 days"`) inside `service.py` without looking up `handbook.json`. | Violated the single source of truth design. Handbook rules must come from `Handbook` and cite official sources (`Source(id, title)`). | Queried `self.handbook.search("exam absence")` dynamically and attached `sources=[Source(id=rule.id, title=rule.title)]`. | Ensures information consistency with `data/handbook.json` and provides verified citations to students. |
| 2 | AI placed keyword matching and regex logic directly inside `service.py` instead of `router.py`. | Violated the `route -> service -> responder` architectural contract. The router must handle intent classification. | Added `EXAM_ABSENCE = "exam_absence"` to `models.py`, added `EXAM_ABSENCE_KEYWORDS` in `router.py`, and dispatched via `AssistantService.handle()`. | Enforces strict separation of concerns and complies with the system architecture. |
| 3 | AI provided no automated tests and omitted fallback handling if the rule lookup returned `None`. | Missing test coverage for CI/pytest and risk of runtime `AttributeError` if handbook data is altered. | Added graceful fallback handling in `_exam_absence` and implemented unit tests in both `tests/test_router.py` and `tests/test_service.py`. | Ensures 100% test pass rate (49/49 tests) and protects against future regressions. |

### Checklist
- [x] Interfaces respected? (`route -> service -> responder`)
- [x] New dependencies? None (uses standard Python library)
- [x] Secrets? None exposed
- [x] Logging of user data? None (only structured metadata: intent, latency, session, degraded)
- [x] Tests added and meaningful? Yes (`test_route_exam_absence` and `test_handle_exam_absence`)

Record the use in `docs/ai-use-log.md`.