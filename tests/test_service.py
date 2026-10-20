from assistant_core.models import Intent, Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


def test_handle_greeting(service: AssistantService) -> None:
    response = service.handle(Message(text="hi"))
    assert response.intent is Intent.GREETING
    assert "Hello!" in response.answer


def test_handle_fee(service: AssistantService) -> None:
    response = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert response.intent is Intent.FEE
    assert "9450000" in response.answer or "9,450,000" in response.answer


def test_handle_office(service: AssistantService) -> None:
    response = service.handle(Message(text="where is the library"))
    assert response.intent is Intent.OFFICE
    assert "B.201" in response.answer


def test_handle_rule_success(service: AssistantService) -> None:
    response = service.handle(Message(text="thesis registration credits"))
    assert response.intent is Intent.RULE
    assert response.degraded is False
    assert len(response.sources) > 0


def test_handle_rule_unknown(service: AssistantService) -> None:
    response = service.handle(Message(text="xyz random question 12345"))
    assert response.intent is Intent.UNKNOWN
    assert "Sorry" in response.answer


def test_fallback_when_provider_fails(service: AssistantService) -> None:
    service.responder = StubLLMResponder(fail=True)
    response = service.handle(Message(text="thesis registration credits"))

    assert response.intent is Intent.RULE
    assert response.degraded is True
    assert len(response.sources) > 0


def test_fee_answer_is_formatted(service: AssistantService) -> None:
    response = service.handle(Message(text="tuition for 18 credits and 2 retake"))
    assert response.answer == "Your tuition is 9,450,000 VND."


def test_fee_without_credits_raises_invalid_request(service: AssistantService) -> None:
    import pytest

    from assistant_core.errors import InvalidRequest

    with pytest.raises(InvalidRequest):
        service.handle(Message(text="tuition"))


def test_empty_message_rejected() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Message(text="")
