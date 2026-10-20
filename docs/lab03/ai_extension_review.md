1. "Add an 'exam absence' answer that tells students the deadline from the handbook."
2. > "Add a 'help' feature to the assistant_core service. When the user asks 'help' or 'what can you do', the bot should return a list of supported features. Update router.py, models.py, and service.py accordingly."

3. 

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | `log.info(f"User sent: {msg.text}")` inside the `handle()` function to debug the help request. | Logged the full raw user message, violating the requirement to prevent logging of user data. | Removed the logging statement completely and relied on the existing structured JSON logger which only logs the `intent`[cite: 23]. | To ensure data privacy and prevent leaking raw user input into the system logs. |
| 2 | `answer="I can help with greetings, fees, offices, rules."` hardcoded in `service.py`. | Magic string. If a new intent is added later, this string must be manually tracked and updated. | Generated the list of capabilities dynamically by iterating over the `Intent` enum values (excluding `UNKNOWN`). | Improves maintainability, ensures a single source of truth, and respects the boundaries of the data models. |
| 3 | Provided the implementation logic but no test cases for `router.py` or `service.py`. | Incomplete feature; missing tests violate the quality gates and the requirement for meaningful tests[cite: 23]. | Added `test_route_help()` in `test_router.py` and a characterization test in `test_service.py` to verify the routing behavior. | Ensures the new routing logic is deterministic, testable offline, and protected against future regressions[cite: 23]. |