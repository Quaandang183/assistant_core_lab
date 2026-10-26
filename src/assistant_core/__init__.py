"""assistant_core: the Smart Virtual Assistant service (Lab 3).

Public API: everything a caller (CLI, FastAPI in Lab 4, UI in Lab 7) needs.
Callers talk to ``AssistantService.handle(Message) -> Response`` only.
"""

from assistant_core.config import Settings, load_settings
from assistant_core.errors import (
    AssistantError,
    ConfigError,
    DataError,
    InvalidRequest,
    ProviderError,
)
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.service import AssistantService, build_service

__version__ = "0.3.0"

__all__ = [
    "AssistantError",
    "AssistantService", "build_service",
    "ConfigError",
    "DataError",
    "Intent",
    "InvalidRequest",
    "Message",
    "ProviderError",
    "Response",
    "Settings",
    "Source",
    "__version__",
    "load_settings",
]
