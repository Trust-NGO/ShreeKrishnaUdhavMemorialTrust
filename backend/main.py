from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from routes.create_admin_user import create_admin
from routes import donation_routes, event_routes, page_routes, admin_routes, auth_routes
from database import engine, Base
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from utils.security import generate_csrf_token
import logging
from datetime import datetime

# Get the backend directory path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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


# ================= ERROR HANDLING MIDDLEWARE =================
@app.middleware("http")
async def error_handling_middleware(request, call_next):
    """Centralized error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(e) if os.getenv("ENVIRONMENT") != "production" else None}
        )


# Static
static_dir = os.path.join(BACKEND_DIR, "static")
uploads_dir = os.path.join(BACKEND_DIR, "uploads")
receipts_dir = os.path.join(BACKEND_DIR, "receipts")

# Create directories if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(uploads_dir, exist_ok=True)
os.makedirs(receipts_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/receipts", StaticFiles(directory=receipts_dir), name="receipts")

# Routes
app.include_router(page_routes.router)
app.include_router(event_routes.router, prefix="/api/events")
app.include_router(donation_routes.router, prefix="/api/donation")
app.include_router(admin_routes.router, prefix="/admin")
app.include_router(auth_routes.router, prefix="/admin")


# ================= API ENDPOINTS =================

@app.post("/api/create-order")
def create_order(data: dict):
    """Create Razorpay order"""
    try:
        import razorpay
        import os
        razorpay_client = razorpay.Client(
            auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
        )
        amount = data.get("amount", 0)
        if amount < 1:
            return JSONResponse(status_code=400, content={"error": "Invalid amount"})
        
        order_data = {
            "amount": int(amount) * 100,  # Convert to paise
            "currency": "INR",
            "receipt": f"order_{datetime.now().timestamp()}",
            "payment_capture": 1
        }
        order = razorpay_client.order.create(data=order_data)
        return {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"]
        }
    except Exception as e:
        logger.error(f"Order creation error: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Failed to create order"})


@app.get("/api/config/razorpay")
def get_razorpay_key():
    """Return Razorpay public key for frontend"""
    razorpay_key = os.getenv("RAZORPAY_KEY_ID")
    if not razorpay_key:
        return JSONResponse(status_code=500, content={"error": "Razorpay key not configured"})
    return {"key": razorpay_key}


@app.get("/api/csrf-token")
def get_csrf_token(request):
    """Generate CSRF token for form protection"""
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = generate_csrf_token()
    return {"csrf_token": request.session["csrf_token"]}


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": os.path.getmtime("SKUMT_NGO.db") if os.path.exists("SKUMT_NGO.db") else None
    }