"""Application lifespan events."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from routes.create_admin_user import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    create_admin()
    yield
    # Shutdown (if needed)

