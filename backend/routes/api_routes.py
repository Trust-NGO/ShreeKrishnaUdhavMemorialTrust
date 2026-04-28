"""Standalone API endpoints extracted from main.py."""

import os
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from core.config import RAZORPAY_KEY_ID, ENVIRONMENT, DB_PATH
from services.payment_service import create_razorpay_order
from utils.security import generate_csrf_token

router = APIRouter()

class CreateOrderRequest(BaseModel):
    amount: int = Field(..., ge=1, le=1000000, description="Amount in INR")

@router.post("/create-order")
def create_order(data: CreateOrderRequest):
    """Create Razorpay order."""
    try:
        return create_razorpay_order(data.amount)
    except Exception as e:
        from core.logging_config import logging
        logging.getLogger(__name__).error(f"Order creation error: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Failed to create order"})


@router.get("/config/razorpay")
def get_razorpay_key():
    """Return Razorpay public key for frontend."""
    if not RAZORPAY_KEY_ID:
        return JSONResponse(status_code=500, content={"error": "Razorpay key not configured"})
    return {"key": RAZORPAY_KEY_ID}


@router.get("/csrf-token")
def get_csrf_token(request: Request):
    """Generate CSRF token for form protection."""
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = generate_csrf_token()
    return {"csrf_token": request.session["csrf_token"]}


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "timestamp": os.path.getmtime(DB_PATH) if os.path.exists(DB_PATH) else None
    }

