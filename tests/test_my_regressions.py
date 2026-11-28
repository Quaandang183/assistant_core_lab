"""Lab 8 Part E: turn YOUR Week-7 failures into regression tests.

Write at least three tests. Each one must:
  - have a name that says what went wrong, e.g. test_empty_sources_does_not_crash_ui
  - FAIL on the old code (check by temporarily undoing your fix), and PASS after the fix.
Use the fixtures `service`, `settings` from conftest.py, or build a TestClient like tests/test_security.py.
"""
from assistant_core.models import Message

def test_example_greeting_still_works(service):
    """Example: a control case that must never break."""
    assert "Hello" in service.handle(Message(text="hi")).answer

def test_sidebar_guidance_does_not_route_all_requests_to_training_office(monkeypatch):
    """The global disclaimer must not send card reissue requests to the wrong office."""
    from pathlib import Path

    from streamlit.testing.v1 import AppTest

    from ui import api_client

    class HealthyBackend:
        def __init__(self, _base_url):
            pass

        def healthy(self):
            return True

    monkeypatch.setattr(api_client, "AssistantClient", HealthyBackend)
    app_path = Path(__file__).resolve().parents[1] / "ui" / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    disclaimers = [
        caption.value.casefold()
        for caption in app.sidebar.caption
        if "ai assistant" in caption.value.casefold()
    ]
    assert len(disclaimers) == 1
    assert "training office" not in disclaimers[0]
    assert "office named in the answer" in disclaimers[0] or "academic advisor" in disclaimers[0]
