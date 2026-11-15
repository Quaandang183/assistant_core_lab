import logging

from assistant_core.config import Settings
from assistant_core.errors import InvalidRequest, ProviderError
from assistant_core.guard import PRIVATE_REPLY, is_private_request
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.llm import make_llm
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.rag.answerer import RagAnswerer
from assistant_core.rag.chunker import load_folder
from assistant_core.rag.index import make_index
from assistant_core.responder import TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger(__name__)


class AssistantService:
    def __init__(self, settings, offices, handbook, responder, rag: RagAnswerer | None = None):
        self.settings, self.offices, self.handbook = settings, offices, handbook
        self.responder = responder
        self.fallback = TemplateResponder()
        self.rag = rag

    def handle(self, msg: Message) -> Response:
        if is_private_request(msg.text):
            return Response(
                answer=PRIVATE_REPLY,
                intent=Intent.UNKNOWN,
                path="guard",
                escalate=True,
                confidence=0.0,
            )

        intent = route(msg.text, self.offices.names)
        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
                path="deterministic",
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
                path="deterministic",
            )
        if intent is Intent.FEE:
            try:
                return self._fee(msg.text)
            except InvalidRequest:
                if self.rag is not None:
                    return self.rag.answer(msg.text)
                raise
        if intent is Intent.OFFICE:
            return self._office(msg.text)
        if self.rag is not None:
            return self.rag.answer(msg.text)
        if intent is Intent.EXAM_ABSENCE:
            return self._exam_absence(msg.text)
        return self._rule(msg.text)

    def _exam_absence(self, text: str) -> Response:
        rule = self.handbook.search("exam absence")
        if rule is None:
            return Response(
                answer="Exam absence deadline: submit evidence within 3 working days.",
                intent=Intent.EXAM_ABSENCE,
                path="deterministic",
            )
        sources = [Source(id=rule.id, title=rule.title)]
        return Response(
            answer=f"Exam absence deadline: {rule.text}",
            intent=Intent.EXAM_ABSENCE,
            sources=sources,
            path="deterministic",
        )

    def _office(self, text: str) -> Response:
        office = self.offices.find(text)
        if office is None:
            return Response(
                answer="Sorry, I don't know that office.",
                intent=Intent.UNKNOWN,
                path="deterministic",
                escalate=True,
            )
        return Response(
            answer=f"{office.name}: room {office.room}, open {office.hours}.",
            intent=Intent.OFFICE,
            path="deterministic",
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
            path="deterministic",
        )

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(
                answer="Sorry, I don't know that yet.",
                intent=Intent.UNKNOWN,
                path="deterministic",
                escalate=True,
            )
        sources = [Source(id=rule.id, title=rule.title)]
        try:
            return Response(
                answer=self.responder.explain(text, rule),
                intent=Intent.RULE,
                sources=sources,
                path="deterministic",
            )
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
                degraded=True,
                path="deterministic",
            )


def build_service(settings: Settings) -> AssistantService:
    offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
    handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    chunks = load_folder(settings.kb_dir)
    index = make_index(settings.retrieval_kind, chunks)
    provider = settings.llm_provider if settings.llm_provider != "template" else "stub"
    llm = make_llm(
        provider,
        settings.llm_model,
        settings.llm_base_url,
        settings.llm_api_key,
        settings.llm_timeout_s,
    )
    rag = RagAnswerer(index, llm, settings.retrieval_min_score, prompt_version=settings.prompt_version)
    return AssistantService(settings, offices, handbook, TemplateResponder(), rag)