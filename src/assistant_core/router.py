"""Rule-based intent routing."""

from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
HELP_KEYWORDS = frozenset({"help", "support", "tro giup", "huong dan"})


def route(text: str, office_names: set[str]) -> Intent:
    t = text.lower().strip().rstrip("?!.")
    if t in GREETINGS:
        return Intent.GREETING
    if t in HELP_KEYWORDS or t == "what can you do":
        return Intent.HELP
    if "fee" in t or "tuition" in t:
        return Intent.FEE
    if any(name in t for name in office_names):
        return Intent.OFFICE
    return Intent.RULE
