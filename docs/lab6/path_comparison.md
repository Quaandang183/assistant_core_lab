# Lab 6 — Part F: Path Comparison

Evaluation: 20 original cases on the Lab 6 starter with TV2's changes, BM25 (threshold: 2.0) and the offline LLM stub. Output of `python eval/compare_paths.py` with the first 20 cases:

| Path | Correct | Correct abstentions | p50 (ms) | Max (ms) | Failed cases |
|---|---:|---:|---:|---:|---|
| Deterministic | 7/20 | 5/5 | 0.0 | 0.4 | E01, E02, E05–E15 |
| Retrieval | 16/20 | 4/5 | 0.0 | 0.1 | E13, E14, E15, E19 |
| LLM (stub) | 16/20 | 4/5 | 0.1 | 0.3 | E13, E14, E15, E19 |

| Case | Why it failed |
|---|---|
| E13 — Tuition deadline | The router treats “tuition” as a fee calculation and asks for the number of credits instead of looking up the deadline. |
| E14 — Taking 32 credits | The word “take” also appears in the exam absence rule (“students take the exam…”), and “32” is in no document, so `H26#7.2` (2.086) outranks the correct credit load rule `H26#6.1` (1.475). |
| E15 — Library loan period | The router matches “library” and returns the location and opening hours without looking up the loan period. |
| E19 — Open-book final exam | BM25 retrieves a rule about missing an exam (`H26#7.2`, 5.62). The source is valid but does not answer the question, so the system should abstain. |

I recommend retrieval for handbook questions. It matched the LLM stub (16/20) and provides sources without requiring a model call. I would fix E19 first because citing an unrelated rule can mislead students about what is allowed in an exam.

---

# Homework

## H1 — Five More Test Questions

Added 5 new test cases (`E21`–`E25`) to `eval/cases.jsonl` (3 normal questions with expected sources `S26#1`, `S26#3`, `H26#5.3`, and 2 out-of-scope/privacy questions with `"expect_abstain": true`) and re-ran `python eval/compare_paths.py` on all 25 cases :

| Path | Correct | Correct abstentions | p50 (ms) | Max (ms) | Failed cases |
|---|---:|---:|---:|---:|---|
| Deterministic | 9/25 | 7/7 | 0.0 | 0.4 | E01, E02, E05–E15, E21, E22, E23 |
| Retrieval | 20/25 | 6/7 | 0.0 | 0.1 | E13, E14, E15, E19, E21 |
| LLM (stub) | 20/25 | 6/7 | 0.1 | 0.3 | E13, E14, E15, E19, E21 |

Among the five new test questions, `E21` ("how many books can I borrow from the library") failed on both the retrieval and LLM paths because the deterministic router matched the keyword “library” first and routed the query to the office lookup tool (`Intent.OFFICE`) instead of searching the knowledge base chunks (`S26#1`). The other four new questions (E22–E25) passed.

## H2 — Reflection

Asking a standard LLM directly is like a closed-book exam where the model answers from memory and may confidently invent rules or numbers when unsure. RAG (Retrieval-Augmented Generation) turns this into an open-book exam: our search code first retrieves the most relevant paragraph from the official faculty documents, hands it to the model, and instructs it to answer strictly from that text. Because we still cannot trust the model blindly, our Python code performs a strict grounding check (`set(draft.source_ids) <= allowed_ids`) to verify that every cited source ID was actually retrieved rather than fabricated. Additionally, our code checks whether the search score meets the minimum threshold (`min_score`) before calling the model, forcing an honest "I don't know" refusal when no relevant document is found.

## H3 (bonus) — Fix E14 by removing a final "s" (not applied)

I tried H3 (remove a final "s" from words longer than four letters in `tokenize`) and then reverted it, so `rag/index.py` keeps the original `tokenize`. If I write the function as required by problem H3:

```python
def tokenize(text: str) -> list[str]:
    tokens = [t for t in re.findall(r"\w+", text.lower()) if t not in STOP]
    return [t[:-1] if len(t) > 4 and t.endswith("s") else t for t in tokens]
```

Results on 25 cases (retrieval path):

| Retrieval path | Correct | Correct abstentions | Failed cases |
|---|---:|---:|---|
| Original tokenize | 20/25 | 6/7 | E13, E14, E15, E19, E21 |
| With H3 | 19/25 | 5/7 | E13, E14, E15, E19, E20, E21 |

- **Does E14 pass?** No. “credits” matches “credit”, but “take” still matches the exam absence rule and “32” is in no document, so `H26#7.2` still outranks `H26#6.1`.
- **What else changed?** E20 (“tell me about exams”) started failing: “exams” became “exam”, matched the title of `H26#7.2` (score 3.997, above the 2.0 threshold), and the assistant answered instead of abstaining.
- **Decision:** the change does not fix E14 and makes the assistant less careful, so it is not kept.
