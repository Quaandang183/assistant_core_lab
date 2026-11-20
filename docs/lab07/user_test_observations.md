# User Test Observations (Homework H1)

- **Test Participant:** External student (not a member of the development team)
- **Assigned Tasks:**
  1. Check whether a student with 118 credits is eligible to register for a graduation thesis.
  2. Find out where to get a student ID card reissued.

---

## Misunderstanding 1: Interpreting the input placeholder as supporting only broad topic lookups
- **Observation:** When asked to verify if 118 credits is sufficient for thesis registration, the user hesitated and initially typed single keywords (`"handbook"`, `"thesis"`) instead of asking the actual condition-checking question (`"Can I register for a thesis with 118 credits?"`).
- **UI / System Cause:** The chat input placeholder (`"Ask about fees, offices or the handbook…"`) suggests that the assistant only performs general keyword searches rather than answering specific eligibility or credit-threshold questions.

## Misunderstanding 2: Overlooking example prompts hidden inside the collapsible sidebar
- **Observation:** When viewing the app in a narrower browser window, the user did not notice the `"Try an example"` section inside `st.sidebar` and was unsure how to phrase questions about administrative procedures like reissuing a student card.
- **UI / System Cause:** Example prompts (`EXAMPLES`) are placed exclusively in the left sidebar—which collapses automatically on smaller screens—instead of being visible in the main chat area on startup.

## Misunderstanding 3: Assuming the global "Training Office" disclaimer applies to student ID card reissuance
- **Observation:** While looking for where to reissue a student ID card, the user read the static caption at the bottom of the sidebar (`"This is an AI assistant. Check important decisions with the Training Office."`) and assumed the Training Office handles student ID cards, even though Student Affairs or another office may be responsible.
- **UI / System Cause:** Hardcoding a single department name (`Training Office`) in a global disclaimer misleads users into thinking every administrative request is handled by that office.