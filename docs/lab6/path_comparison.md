# Lab 6 — Part F: Path Comparison

Evaluation: 20 cases on the Lab 6 starter with TV2's changes, BM25 (threshold: 2.0), and the offline LLM stub.

| Path | Correct | Correct abstentions | p50 (ms) | Max (ms) | Failed cases |
|---|---:|---:|---:|---:|---|
| Deterministic | 7/20 | 5/5 | 0.0 | 0.9 | E01, E02, E05–E15 |
| Retrieval | 16/20 | 4/5 | 0.1 | 0.2 | E13, E14, E15, E19 |
| LLM (stub) | 16/20 | 4/5 | 0.4 | 1.5 | E13, E14, E15, E19 |

| Case | Why it failed |
|---|---|
| E13 — Tuition deadline | The router treats “tuition” as a fee calculation and asks for the number of credits instead of looking up the deadline. |
| E14 — Taking 32 credits | BM25 treats “credit” and “credits” as separate terms and ranks an exam absence rule above the credit limit. |
| E15 — Library loan period | The router matches “library” and returns the location and opening hours without looking up the loan period. |
| E19 — Open-book final exam | BM25 retrieves a rule about missing an exam. The source is valid but does not answer the question, so the system should abstain. |

I recommend retrieval for handbook questions. It matched the LLM stub at 16/20 and provides sources without requiring a model call. I would fix E19 first because citing an unrelated rule can mislead students about what is allowed in an exam.
