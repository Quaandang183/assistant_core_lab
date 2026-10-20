# Architecture Note — assistant_core

This document outlines the architecture of the `assistant_core` package, detailing module responsibilities, the public service interface, and key engineering decisions[cite: 3, 8, 15].

---

## 1. Module Overview[cite: 8, 15, 28]

| Module | Responsibility |
| :--- | :--- |
| `config.py` | Read settings from environment variables and validate runtime configuration. |
| `errors.py` | Define named domain exceptions (`AssistantError`, `ConfigError`, `DataError`, `InvalidRequest`, `ProviderError`)[cite: 8, 10]. |
| `models.py` | Public data contract models: `Message`, `Response`, `Intent`, `Source`. |
| `router.py` | Map input text to an `Intent` using deterministic rule matching[cite: 8, 13]. |
| `knowledge.py` | Load and query the office directory (CSV) and student handbook (JSON)[cite: 8, 11, 12]. |
| `tools.py` | Deterministic tuition fee calculation and input parsing[cite: 8, 12]. |
| `responder.py` | Response generation behind a `Protocol` interface (stub LLM and template fallback)[cite: 8, 13]. |
| `service.py` | Main entry point (`AssistantService`) orchestrating routing, retrieval, tools, and response generation[cite: 8, 13, 14]. |
| `logging_setup.py` | Structured JSON log formatting. |
| `__main__.py` | Command-line interface (CLI) entry point[cite: 8, 14]. |

---

## 2. Service Interface[cite: 8, 15, 28]

The service exposes a single unified entry point[cite: 8]:

```python
AssistantService.handle(msg: Message) -> Response