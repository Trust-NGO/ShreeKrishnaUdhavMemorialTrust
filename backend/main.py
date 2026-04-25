from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from routes.create_admin_user import create_admin
from routes import donation_routes, event_routes, page_routes, admin_routes, auth_routes
from database import engine, Base
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_admin()
    yield
    # Shutdown (if needed)

app = FastAPI(title="NGO ERP System", lifespan=lifespan)

# DB
Base.metadata.create_all(bind=engine)

# 🔐 SESSION SECURITY (THIS IS REQUIRED)
secret_key = os.getenv("SESSION_SECRET_KEY")
if not secret_key:
    if os.getenv("ENVIRONMENT") == "production":
        raise ValueError("SESSION_SECRET_KEY must be set in production!")
    secret_key = "fallback_key_for_dev_only"

app.add_middleware(SessionMiddleware, secret_key=secret_key)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/receipts", StaticFiles(directory="receipts"), name="receipts")

# Routes
app.include_router(page_routes.router)
app.include_router(event_routes.router, prefix="/api/events")
app.include_router(donation_routes.router, prefix="/api/donation")
app.include_router(admin_routes.router, prefix="/admin")
app.include_router(auth_routes.router, prefix="/admin")