"""Rule-based intent routing."""

from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
EXAM_ABSENCE_KEYWORDS = ("exam absence", "missed exam", "final exam absence", "vang thi", "nghi thi")


def route(text: str, office_names: set[str]) -> Intent:
    t = text.lower().strip().rstrip("?!.")
    if t in GREETINGS:
        return Intent.GREETING
    if any(kw in t for kw in EXAM_ABSENCE_KEYWORDS):
        return Intent.EXAM_ABSENCE
    if "fee" in t or "tuition" in t:
        return Intent.FEE
    if any(name in t for name in office_names):
        return Intent.OFFICE
    return Intent.RULE
