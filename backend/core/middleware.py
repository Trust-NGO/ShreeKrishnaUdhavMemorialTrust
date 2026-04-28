"""Application middleware setup."""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from core.config import SESSION_SECRET_KEY, ENVIRONMENT

logger = logging.getLogger(__name__)


def setup_middlewares(app: FastAPI) -> None:
    """Register all application middlewares."""
    app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)


async def error_handling_middleware(request: Request, call_next):
    """Centralized error handling middleware."""
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error("Unhandled error: %s", str(exc), exc_info=True)
        detail = str(exc) if ENVIRONMENT != "production" else None
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": detail}
        )

