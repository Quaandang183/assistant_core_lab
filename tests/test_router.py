import pytest


@pytest.mark.parametrize(
    "text",
    [
        "hi",
        "hello",
        "hey",
        "xin chao",
        "HELLO",
        "  Hi  ",
        "hello!",
        "xin chao?!.",
    ],
)
def test_route_greeting(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.GREETING


@pytest.mark.parametrize(
    "text",
    [
        "help",
        "HELP",
        "  help  ",
        "help!",
        "tro giup",
        "support",
        "huong dan?!.",
    ],
)
def test_route_help(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.HELP


@pytest.mark.parametrize(
    "text",
    [
        "exam absence",
        "EXAM ABSENCE",
        "What is the deadline for exam absence?",
        "missed exam",
        "vang thi",
        "nghi thi?!.",
    ],
)
def test_route_exam_absence(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.EXAM_ABSENCE



@pytest.mark.parametrize(
    "text",
    [
        "fee",
        "What is the tuition?",
        "TUITION!",
        "How much is the fee?",
    ],
)
def test_route_fee(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.FEE


@pytest.mark.parametrize(
    "text",
    [
        "phong dao tao",
        "Where is student affairs?",
        "  PHONG DAO TAO!  ",
    ],
)
def test_route_office(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.OFFICE


@pytest.mark.parametrize(
    "text",
    [
        "What are the graduation requirements?",
        "Tell me the rules",
        "hello everyone",
        "unknown question",
    ],
)
def test_route_defaults_to_rule(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.RULE


def test_route_fee_takes_priority_over_office(router_module, intent_type, office_names):
    text = "Ask student affairs about tuition"

    assert router_module.route(text, office_names) is intent_type.FEE


def test_route_greeting_takes_priority_over_office(router_module, intent_type):
    assert router_module.route("hello", {"hello"}) is intent_type.GREETING


def test_route_with_empty_office_names(router_module, intent_type):
    assert router_module.route("student affairs", set()) is intent_type.RULE


@pytest.mark.parametrize("text", ["", "   ", "?!.", "\n\t"])
def test_route_blank_text_defaults_to_rule(router_module, intent_type, office_names, text):
    assert router_module.route(text, office_names) is intent_type.RULE


def test_route_does_not_modify_office_names(router_module, office_names):
    original = office_names.copy()

    router_module.route("Where is student affairs?", office_names)

    assert office_names == original
