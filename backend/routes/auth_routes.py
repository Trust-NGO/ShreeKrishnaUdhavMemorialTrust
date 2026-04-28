from utils.auth_guard import verify_password, hash_password
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from utils.security import check_rate_limit, record_failed_attempt, clear_attempts, generate_reset_token, validate_reset_token, mark_reset_token_used, validate_email, validate_password

from database import get_db
from models import AdminUser
from fastapi.templating import Jinja2Templates
import logging
import os

logger = logging.getLogger(__name__)

# Get absolute path to templates directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BACKEND_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Admin login with rate limiting"""
    
    # ================= RATE LIMITING =================
    is_allowed, message = check_rate_limit(username)
    if not is_allowed:
        logger.warning(f"Rate limit exceeded for {username}")
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": message
        }, status_code=429)

    logger.info(f"Login attempt for user: {username}")

    user = db.query(AdminUser).filter(AdminUser.username == username).first()

    # ❌ INVALID LOGIN
    if not user or not verify_password(password, user.password):
        record_failed_attempt(username)
        logger.warning(f"Invalid credentials for {username}")
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

    # ✅ SUCCESS LOGIN
    clear_attempts(username)
    request.session["admin"] = user.username
    request.session["admin_id"] = user.id
    request.session["admin_role"] = user.role
    logger.info(f"Admin logged in: {user.username} (ID: {user.id})")

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.get("/logout")
def logout(request: Request):
    username = request.session.get("admin", "unknown")
    request.session.clear()
    logger.info(f"Admin logged out: {username}")
    return RedirectResponse(url="/admin/login", status_code=302)


# ================= PASSWORD RESET =================

@router.get("/forgot-password")
def forgot_password_page(request: Request):
    """Forgot password page"""
    return templates.TemplateResponse("admin/forgot_password.html", {"request": request})


@router.post("/forgot-password")
def forgot_password(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Send password reset email"""
    
    # Validate email format
    is_valid, msg = validate_email(email)
    if not is_valid:
        return templates.TemplateResponse("admin/forgot_password.html", {
            "request": request,
            "error": "Invalid email format"
        })
    
    # Find user
    user = db.query(AdminUser).filter(AdminUser.username == email).first()
    
    if not user:
        # Don't reveal if user exists (security best practice)
        logger.warning(f"Password reset request for non-existent user: {email}")
        return templates.TemplateResponse("admin/forgot_password.html", {
            "request": request,
            "message": "If the email exists, you will receive a password reset link"
        })
    
    # Generate reset token
    token = generate_reset_token(user.id, user.username)
    reset_url = f"{request.base_url}admin/reset-password?token={token}"
    
    # Send email
    from services.email_service import email_service
    subject = "Password Reset Request"
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">{reset_url}</a></p>
            <p style="color: #666; font-size: 12px;">This link will expire in 1 hour.</p>
        </div>
    </body>
    </html>
    """
    
    success = email_service.send_email(user.username, subject, html)
    
    if not success:
        logger.error("Failed to send reset email")
        return templates.TemplateResponse("admin/forgot_password.html", {
            "request": request,
            "error": "Failed to send reset email. Please try again."
        })
    
    logger.info(f"Password reset token generated for user: {user.username}")
    
    return templates.TemplateResponse("admin/forgot_password.html", {
        "request": request,
        "message": "Password reset link has been sent to your email"
    })


@router.get("/reset-password")
def reset_password_page(request: Request, token: str = None):
    """Reset password page"""
    if not token:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": "Invalid reset link"
        })
    
    # Validate token
    is_valid, msg, user_id = validate_reset_token(token)
    if not is_valid:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": msg
        })
    
    return templates.TemplateResponse("admin/reset_password.html", {
        "request": request,
        "token": token
    })


@router.post("/reset-password")
def reset_password(
    request: Request,
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Reset password with new password"""
    
    # Validate passwords match
    if new_password != confirm_password:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": "Passwords do not match",
            "token": token
        })
    
    # Validate password strength
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": msg,
            "token": token
        })
    
    # Validate token
    is_valid, msg, user_id = validate_reset_token(token)
    if not is_valid:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": msg,
            "token": token
        })
    
    # Update password
    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        return templates.TemplateResponse("admin/reset_password.html", {
            "request": request,
            "error": "User not found",
            "token": token
        })
    
    user.password = hash_password(new_password)
    db.commit()
    
    # Mark token as used
    mark_reset_token_used(token)
    
    logger.info(f"Password reset successful for user: {user.username}")
    
    return templates.TemplateResponse("admin/reset_password.html", {
        "request": request,
        "message": "Password has been reset successfully. You can now login with your new password.",
        "redirect_url": "/admin/login"
    })
