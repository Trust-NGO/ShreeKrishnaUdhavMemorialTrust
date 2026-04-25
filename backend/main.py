from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routes import donation_routes, event_routes, page_routes, admin_routes, auth_routes
from database import engine, Base

app = FastAPI(title="NGO ERP System")

# DB
Base.metadata.create_all(bind=engine)

# 🔐 SESSION SECURITY (THIS IS REQUIRED)
app.add_middleware(SessionMiddleware, secret_key="ngo_erp_super_secret_key_2026")

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routes
app.mount("/receipts", StaticFiles(directory="receipts"), name="receipts")
app.include_router(page_routes.router)
app.include_router(event_routes.router, prefix="/api/events")
app.include_router(donation_routes.router, prefix="/api/donation")
app.include_router(admin_routes.router, prefix="/admin")
app.include_router(auth_routes.router, prefix="/admin")