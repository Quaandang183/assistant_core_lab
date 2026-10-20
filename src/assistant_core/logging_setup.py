"""Structured JSON logging. Logs go to stderr; never log secrets or full user messages."""

import json
import logging
import sys

EXTRA_FIELDS = ("intent", "latency_ms", "session", "degraded")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {"level": record.levelname, "logger": record.name, "msg": record.getMessage()}
        for key in EXTRA_FIELDS:
            if hasattr(record, key):
                data[key] = getattr(record, key)
        return json.dumps(data, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    """Attach one JSON handler (stderr) to the 'assistant_core' logger. Safe to call twice."""
    logger = logging.getLogger("assistant_core")
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger.handlers[:] = [handler]
    logger.setLevel(level.upper())
    logger.propagate = False
