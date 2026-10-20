"""Command-line interface.

Usage:
    python -m assistant_core "tuition for 18 credits and 2 retake"
    python -m assistant_core            # interactive mode (type 'exit' to quit)

Answers go to stdout, logs go to stderr:
    python -m assistant_core "hi" 2> app.log
"""

import argparse
import logging
import sys
import time
from collections.abc import Sequence

from pydantic import ValidationError

from assistant_core.config import Settings, load_settings
from assistant_core.errors import AssistantError, ConfigError, InvalidRequest
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService

log = logging.getLogger("assistant_core")

EXIT_WORDS = frozenset({"exit", "quit", "q"})


def build_service(settings: Settings) -> AssistantService:
    """Wire the dependencies together (the only place that knows the concrete classes)."""
    offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
    handbook = Handbook.from_json(settings.data_dir / "handbook.json")

    if settings.llm_provider != "stub":
        # Week 4: add a real provider class here; the service stays unchanged.
        raise ConfigError(f"unsupported LLM_PROVIDER={settings.llm_provider!r} (only 'stub' for now)")
    responder = StubLLMResponder()

    return AssistantService(settings, offices, handbook, responder)


def ask(service: AssistantService, text: str, session_id: str) -> int:
    """Send one message to the service and print the answer. Returns an exit code."""
    start = time.perf_counter()
    try:
        response = service.handle(Message(text=text, session_id=session_id))
    except ValidationError:
        print("Invalid message: please type between 1 and 2000 characters.", file=sys.stderr)
        return 2
    except InvalidRequest as exc:
        print(exc)
        return 2

    # Never log the API key or the full user message: only metadata.
    log.info(
        "handled",
        extra={
            "intent": response.intent.value,
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "session": session_id,
            "degraded": response.degraded,
        },
    )
    print(response.answer)
    for source in response.sources:
        print(f"  (source: {source.id} - {source.title})")
    return 0


def interactive(service: AssistantService, session_id: str) -> int:
    """Simple read-eval-print loop."""
    print("Smart Virtual Assistant. Type 'exit' to quit.")
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if text.lower() in EXIT_WORDS:
            return 0
        if text:
            ask(service, text, session_id)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="assistant_core", description="Smart Virtual Assistant (CLI)")
    parser.add_argument("message", nargs="*", help="question to ask; omit for interactive mode")
    parser.add_argument("--session-id", default="local", help="session identifier (default: local)")
    parser.add_argument("--env-file", default=".env", help="path to the .env file (default: .env)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        settings = load_settings(args.env_file)
        setup_logging(settings.log_level)
        service = build_service(settings)
    except (AssistantError, ValueError) as exc:  # ValueError covers bad .env types (e.g. MAX_CREDITS=abc)
        print(f"Startup error: {exc}", file=sys.stderr)
        return 1

    if args.message:
        return ask(service, " ".join(args.message), args.session_id)
    return interactive(service, args.session_id)


if __name__ == "__main__":
    sys.exit(main())
