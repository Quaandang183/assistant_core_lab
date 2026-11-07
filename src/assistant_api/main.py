"""FastAPI application - Lab 4.  Run:  uvicorn assistant_api.main:create_app --factory --reload

Endpoints (v1): GET /health, POST /v1/chat, POST /v1/feedback, GET /v1/feedback (admin),
GET /v1/weather, GET /v1/offices (homework H1).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from assistant_api.ratelimit import RateLimiter
from assistant_api.schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    FeedbackIn,
    FeedbackOut,
    OfficeOut,
    Weather,
)
from assistant_api.weather import ExternalServiceError, WeatherClient
from assistant_core import AssistantService, Message, build_service
from assistant_core.config import Settings, load_settings
from assistant_core.errors import InvalidRequest
from assistant_core.models import Intent


def create_app(
    settings: Settings | None = None, service: AssistantService | None = None, weather: WeatherClient | None = None
) -> FastAPI:
    settings = settings or load_settings()
    service = service or build_service(settings)
    weather = weather or WeatherClient(
        settings.weather_url, settings.campus_lat, settings.campus_lon, timeout_s=settings.weather_timeout_s
    )
    limiter = RateLimiter(settings.rate_limit_per_min)
    feedback_store: list[FeedbackOut] = []  # Lab 5 replaces this with a database

    app = FastAPI(
        title="Study Assistant API", version="1.0.0", description="Backend of the CSC10014 Smart Virtual Assistant."
    )

    def error(code: int, key: str, message: str) -> JSONResponse:
        return JSONResponse(status_code=code, content={"error": {"code": key, "message": message}})

    @app.exception_handler(RequestValidationError)
    async def on_validation(_: Request, exc: RequestValidationError):
        first = exc.errors()[0]
        field = ".".join(str(p) for p in first["loc"][1:]) or "body"
        return error(422, "invalid_request", f"{field}: {first['msg']}")

    @app.exception_handler(HTTPException)
    async def on_http(_: Request, exc: HTTPException):
        return error(exc.status_code, str(exc.detail).lower().replace(" ", "_"), str(exc.detail))

    def require_admin(x_api_key: str | None = Header(default=None)) -> None:
        if not settings.api_admin_key or x_api_key != settings.api_admin_key:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key")

    @app.get("/health", tags=["ops"])
    def health() -> dict:
        return {"status": "ok", "version": app.version}

    @app.post(
        "/v1/chat",
        response_model=ChatResponse,
        tags=["chat"],
        responses={422: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def chat(req: ChatRequest, request: Request) -> ChatResponse:
        # BONUS (Part F): rate limiting per client address
        client = request.client.host if request.client else "unknown"
        if not limiter.allow(client):
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many requests")

        # T1: ask the Lab 3 service and return its answer with a new request_id
        try:
            resp = service.handle(Message(text=req.message, session_id=req.session_id))
        except InvalidRequest as exc:
            # e.g. a fee question without credits: a normal chat answer, not a server error
            resp_data = {"answer": str(exc), "intent": Intent.FEE}
            return ChatResponse(**resp_data, request_id=uuid.uuid4().hex[:12])
        return ChatResponse(**resp.model_dump(), request_id=uuid.uuid4().hex[:12])

    @app.post("/v1/feedback", response_model=FeedbackOut, status_code=201, tags=["feedback"])
    def add_feedback(fb: FeedbackIn) -> FeedbackOut:
        # T2: store the feedback in memory and return it (201 Created)
        item = FeedbackOut(**fb.model_dump(), id=len(feedback_store) + 1, created_at=datetime.now(timezone.utc))
        feedback_store.append(item)
        return item

    @app.get("/v1/feedback", response_model=list[FeedbackOut], tags=["feedback"], dependencies=[Depends(require_admin)])
    def list_feedback() -> list[FeedbackOut]:
        # T3: the API-key check is done by `require_admin` above
        return feedback_store

    @app.get("/v1/weather", response_model=Weather, tags=["external"], responses={503: {"model": ErrorResponse}})
    def campus_weather() -> Weather:
        # T4: turn "the weather site is down" into a clean 503
        try:
            return weather.current()
        except ExternalServiceError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Weather service unavailable") from None

    @app.get("/v1/offices", response_model=list[OfficeOut], tags=["offices"])
    def list_offices() -> list[dict]:
        # H1: all offices, sorted by name
        return [o.__dict__ for o in service.offices.all()]

    return app
