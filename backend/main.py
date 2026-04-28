from fastapi import FastAPI

from database import engine, Base
from core.logging_config import setup_logging
from core.lifespan import lifespan
from core.middleware import setup_middlewares, error_handling_middleware
from core.app_setup import setup_static_files
from routes import donation_routes, event_routes, page_routes, admin_routes, auth_routes, api_routes

# Configure logging
setup_logging()

# Create app
app = FastAPI(title="NGO ERP System", lifespan=lifespan)

# Database tables
Base.metadata.create_all(bind=engine)

# Middlewares
setup_middlewares(app)
app.middleware("http")(error_handling_middleware)

# Static files & directories
setup_static_files(app)

# Routes
app.include_router(page_routes.router)
app.include_router(event_routes.router, prefix="/api/events")
app.include_router(donation_routes.router, prefix="/api/donation")
app.include_router(admin_routes.router, prefix="/admin")
app.include_router(auth_routes.router, prefix="/admin")
app.include_router(api_routes.router, prefix="/api")

