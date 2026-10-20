Fill in for the monolith (before) and your refactored package (after).

| Question | Before | After |
|---|---|---|
| Where would you change the credit rate? How many places? | 1 constant in code[cite: 16] | 1 variable in `.env`[cite: 16] |
| Can you run the tests without internet or an API key? | No (non-deterministic)[cite: 16] | Yes (tests run offline using stubs)[cite: 16] |
| What happens if `handbook.json` is missing? | Prints and continues silently[cite: 16] | Raises `DataError` at startup[cite: 16] |
| Is any secret printed or logged? | Yes[cite: 16] | No[cite: 16] |
| How long does it take a new teammate to find the fee logic? | Hard to find, mixed inside a giant `handle()` function[cite: 6, 16] | Easy and fast, clearly isolated in `tools.py`[cite: 8, 12] |
| Number of global variables | 9 (3 mutable)[cite: 16] | 0[cite: 16] |
| Number of bare `except:` blocks | 3[cite: 16] | 0[cite: 16] |
| Lines in the longest function | ~65 (`handle`)[cite: 16] | ~15[cite: 16] |
| `ruff check` issues | Many (due to bare excepts, unused variables, globals)[cite: 6] | 0 (All checks passed)[cite: 15] |
| Can you swap the LLM without touching the service? | No[cite: 16] | Yes[cite: 16] |

**Three sentences:** what improved most, what got more complex, and what you would still change.

What improved most is the separation of concerns and code reliability, as configuration is now isolated, logic is highly testable, and errors are handled explicitly[cite: 8, 16]. What got more complex is the project structure, which now requires navigating multiple files, interfaces (like Pydantic models), and passing dependencies instead of just running a single script[cite: 8, 16]. What I would still change is improving the knowledge retrieval logic, such as replacing the simple keyword overlap search with a more advanced vector search or embedding mechanism for better accuracy.