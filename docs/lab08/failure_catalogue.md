# Lab 8 — Failure catalogue

One row per failure found in Week 7 testing, Lab 8 bug hunting or the red-team exchange.

| # | Failure | Category | Found by | Severity | Mitigation | Regression test |
|---|---|---|---|---|---|---|
| 1 | | prompt injection / privacy / out-of-scope / malformed input / unavailable service / wrong answer / UI | | | | |
| 2 | | | | | | |
| 3 | Sidebar disclaimer implied the Training Office handles student card reissue | UI | Lab 7 usability tester | Minor | Confirm with the office named in the answer or an academic advisor | `test_sidebar_guidance_does_not_route_all_requests_to_training_office` |

At least **3 mitigations** must be implemented and tested.
