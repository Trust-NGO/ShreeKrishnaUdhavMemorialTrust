"""Application static files and directory setup."""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import STATIC_DIR, UPLOADS_DIR, RECEIPTS_DIR


def setup_static_files(app: FastAPI) -> None:
    """Create required directories and mount static file routes."""
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
    app.mount("/receipts", StaticFiles(directory=RECEIPTS_DIR), name="receipts")

