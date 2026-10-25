# Lab 3 — AI Extension Review

## 1. Feature Request
Extend the service to handle student inquiries about **exam absence** deadlines using rules from the handbook.

---

## 2. Prompt Used
> "Refactor my Python assistant service into modular files (service.py, responder.py, tools.py) adhering to Single Responsibility Principle, and implement a fallback mechanism when LLM fails."

---

## 3. Code Review & Manual Changes

| # | What the AI generated | Problem you found | What you changed | Why |
|:-:|:---|:---|:---|:---|
| **1** | Placed test code (`def test_fallback_when_provider_fails`) directly inside `src/assistant_core/service.py`. | Violated the Single Responsibility Principle and directory structure standard by mixing unit tests into production source code. | Moved `test_fallback_when_provider_fails` to `tests/test_service.py`. | Keeps production service logic strictly separated from testing code. |
| **2** | Called `self.offices.find(text)` and directly accessed its properties (`office.name`) without validating the return value. | Caused an `AttributeError` crash when a user queried an office name that does not exist in `offices.csv` (returned `None`). | Added a guard clause `if office is None:` in `_office()` that returns `Intent.UNKNOWN`. | Prevents runtime crashes and safely handles edge cases for invalid office queries. |
| **3** | Formatted tuition output as plain integer strings without thousand separators: `f"Your tuition is {total} VND"`. | Inconsistent with `architecture.md` specification (`9,450,000 VND`) and harder for users to read. | Updated `_fee()` to format tuition using comma separators: `f"Your tuition is {total:,} VND."`. | Ensures clear financial presentation and adheres to Decision #1 in the architecture note. |

---

## 4. Checklist
- [x] **Interfaces respected?** Yes, preserved `AssistantService.handle(Message) -> Response`.
- [x] **New dependencies?** None added.
- [x] **Secrets exposed?** None (no hardcoded API keys).
- [x] **Logging of user data?** No sensitive PII logged.
- [x] **Tests added and meaningful?** Yes, verified via pytest in `tests/test_service.py`.