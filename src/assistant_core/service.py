import logging

from assistant_core.errors import ProviderError
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger(__name__)


class AssistantService:
    def __init__(self, settings, offices, handbook, responder):
        self.settings, self.offices, self.handbook = settings, offices, handbook
        self.responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        intent = route(msg.text, self.offices.names)
        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )
        if intent is Intent.HELP:
            return Response(
                answer=(
                    "I can help you with:\n"
                    "- Greeting: say 'hello' or 'hi'\n"
                    "- Tuition fees: ask 'tuition for 18 credits'\n"
                    "- Office info: ask about 'phong dao tao' or 'student affairs'\n"
                    "- Handbook rules: ask about 'exam absence', 'retake', or 'thesis'"
                ),
                intent=intent,
            )
        if intent is Intent.EXAM_ABSENCE:
            return self._exam_absence(msg.text)

        if intent is Intent.FEE:
            return self._fee(msg.text)
        if intent is Intent.OFFICE:
            return self._office(msg.text)
        return self._rule(msg.text)

    def _exam_absence(self, text: str) -> Response:
        rule = self.handbook.search("exam absence")
        if rule is None:
            return Response(
                answer="Exam absence deadline: submit evidence within 3 working days.",
                intent=Intent.EXAM_ABSENCE,
            )
        sources = [Source(id=rule.id, title=rule.title)]
        return Response(
            answer=f"Exam absence deadline: {rule.text}",
            intent=Intent.EXAM_ABSENCE,
            sources=sources,
        )

    def _office(self, text: str) -> Response:
        office = self.offices.find(text)
        if office is None:
            return Response(answer="Sorry, I don't know that office.", intent=Intent.UNKNOWN)
        return Response(
            answer=f"{office.name}: room {office.room}, open {office.hours}.",
            intent=Intent.OFFICE,
        )

    def _fee(self, text: str) -> Response:
        credits_num, retake_num = parse_credits(text)
        total = tuition(
            credits=credits_num,
            retake=retake_num,
            rate=self.settings.credit_rate_vnd,
            retake_multiplier=self.settings.retake_multiplier,
            max_credits=self.settings.max_credits,
        )
        return Response(
            answer=f"Your tuition is {total:,} VND.",
            intent=Intent.FEE,
        )

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(
                answer="Sorry, I don't know that yet.",
                intent=Intent.UNKNOWN,
            )
        sources = [Source(id=rule.id, title=rule.title)]
        try:
            return Response(
                answer=self.responder.explain(text, rule),
                intent=Intent.RULE,
                sources=sources,
            )
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
                degraded=True,
            )


def build_service(settings: Settings) -> AssistantService:
    from assistant_core.knowledge import Handbook, OfficeDirectory
    from assistant_core.responder import make_responder

    d = settings.data_dir
    offices = OfficeDirectory.from_csv(d / "offices.csv")
    handbook = Handbook.from_json(d / "handbook.json")
    return AssistantService(settings, offices, handbook, make_responder(settings.llm_provider))
