## BUG-3: Sidebar guidance points student card requests to the wrong office

**Found by:** External Lab 7 usability tester
**Severity:** Minor
**Where:** Streamlit UI sidebar

### Steps to reproduce on the Lab 7 baseline

1. Open the Streamlit app and expand the sidebar.
2. Look for help with reissuing a student ID card and read the general AI disclaimer.

### Expected

The disclaimer explains how to verify the answer without naming one office as the contact for every question.

### Actual

The sidebar displayed: "This is an AI assistant. Check important decisions with the Training Office." The tester took this as guidance to contact the Training Office about card reissue.

### Evidence and cause

The third observation in [Lab 7 user testing](../lab07/user_test_observations.md) records the misunderstanding. The sidebar hardcoded one office in a disclaimer displayed before the assistant knew the student's question.

### Mitigation and regression test

Keep the existing [Lab 7 fix](https://github.com/Quaandang183/assistant_core_lab/commit/e0983cc18eacc7a7c19ed9f14a1b7e99ef005823): recommend confirming with the office named in the answer or with an academic advisor. Keep any question-specific guidance in the response itself. The test `test_sidebar_guidance_does_not_route_all_requests_to_training_office` checks the sidebar as rendered.

### Verification

- Old disclaimer restored temporarily: FAIL because the rendered sidebar still names the Training Office.
- Lab 7 fix restored: PASS.
- Together with the existing UI tests: 9 passed.
