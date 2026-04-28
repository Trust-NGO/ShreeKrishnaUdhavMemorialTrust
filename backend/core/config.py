"""Centralized application configuration."""

import os
from dotenv import load_dotenv

# Get the backend directory path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Session secret key validation
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
if not SESSION_SECRET_KEY:
    if ENVIRONMENT == "production":
        raise ValueError("SESSION_SECRET_KEY must be set in production!")
    SESSION_SECRET_KEY = "fallback_key_for_dev_only"

# Razorpay keys
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

# Directory paths
STATIC_DIR = os.path.join(BACKEND_DIR, "static")
UPLOADS_DIR = os.path.join(BACKEND_DIR, "uploads")
RECEIPTS_DIR = os.path.join(BACKEND_DIR, "receipts")

# Database path
DB_PATH = os.path.join(BACKEND_DIR, "SKUMT_NGO.db")

