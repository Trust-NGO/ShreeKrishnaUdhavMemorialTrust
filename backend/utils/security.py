"""Security utilities for rate limiting, CSRF protection, and password reset"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
import secrets
import logging
from fastapi import HTTPException
import os

logger = logging.getLogger(__name__)

# ================= RATE LIMITING =================
login_attempts: Dict[str, list] = {}
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW = 300  # 5 minutes in seconds


def check_rate_limit(identifier: str, max_attempts: int = MAX_LOGIN_ATTEMPTS, window: int = LOGIN_ATTEMPT_WINDOW) -> Tuple[bool, str]:
    """
    Rate limiting function to prevent brute force attacks
    Returns: (is_allowed, message)
    """
    now = datetime.now()
    
    if identifier not in login_attempts:
        login_attempts[identifier] = []
    
    # Clean old attempts outside the window
    login_attempts[identifier] = [
        timestamp for timestamp in login_attempts[identifier]
        if (now - timestamp).total_seconds() < window
    ]
    
    # Check if max attempts exceeded
    if len(login_attempts[identifier]) >= max_attempts:
        return False, f"Too many attempts. Try again in {window // 60} minutes."
    
    # Record this attempt
    login_attempts[identifier].append(now)
    return True, "OK"


def record_failed_attempt(identifier: str):
    """Record a failed login attempt"""
    if identifier not in login_attempts:
        login_attempts[identifier] = []
    login_attempts[identifier].append(datetime.now())
    logger.warning(f"Failed login attempt for {identifier}")


def clear_attempts(identifier: str):
    """Clear attempts on successful login"""
    if identifier in login_attempts:
        del login_attempts[identifier]


# ================= PASSWORD RESET =================
password_reset_tokens: Dict[str, Dict] = {}
RESET_TOKEN_EXPIRY = 3600  # 1 hour


def generate_reset_token(user_id: int, user_email: str) -> str:
    """Generate a secure password reset token"""
    token = secrets.token_urlsafe(32)
    password_reset_tokens[token] = {
        "user_id": user_id,
        "email": user_email,
        "created_at": datetime.now(),
        "used": False
    }
    logger.info(f"Password reset token generated for user {user_id}")
    return token


def validate_reset_token(token: str) -> Tuple[bool, str, int]:
    """
    Validate a password reset token
    Returns: (is_valid, message, user_id)
    """
    if token not in password_reset_tokens:
        return False, "Invalid or expired token", -1
    
    token_data = password_reset_tokens[token]
    
    # Check if already used
    if token_data.get("used"):
        return False, "Token already used", -1
    
    # Check expiry
    created_at = token_data["created_at"]
    if (datetime.now() - created_at).total_seconds() > RESET_TOKEN_EXPIRY:
        del password_reset_tokens[token]
        return False, "Token expired", -1
    
    return True, "Valid token", token_data["user_id"]


def mark_reset_token_used(token: str):
    """Mark a reset token as used"""
    if token in password_reset_tokens:
        password_reset_tokens[token]["used"] = True
        logger.info(f"Password reset token marked as used")


def cleanup_expired_tokens():
    """Remove expired reset tokens (call periodically)"""
    now = datetime.now()
    expired_tokens = [
        token for token, data in password_reset_tokens.items()
        if (now - data["created_at"]).total_seconds() > RESET_TOKEN_EXPIRY
    ]
    
    for token in expired_tokens:
        del password_reset_tokens[token]
    
    if expired_tokens:
        logger.info(f"Cleaned up {len(expired_tokens)} expired reset tokens")


# ================= CSRF PROTECTION =================
def generate_csrf_token() -> str:
    """Generate a CSRF token"""
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, session_token: str) -> bool:
    """Verify CSRF token matches session token"""
    return token == session_token


# ================= SESSION SECURITY =================
def get_session_config():
    """Get secure session configuration"""
    env = os.getenv("ENVIRONMENT", "development")
    return {
        "secure": env == "production",  # HTTPS only in production
        "httponly": True,  # No JavaScript access
        "samesite": "strict"  # CSRF protection
    }


# ================= INPUT VALIDATION =================
def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, "Valid email"


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"
    
    return True, "Valid password"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number"""
    import re
    pattern = r'^[+]?[0-9]{7,15}$'
    if not re.match(pattern, phone.replace(" ", "").replace("-", "")):
        return False, "Invalid phone number format"
    return True, "Valid phone number"
