from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import EmailStr, validator
from datetime import datetime, timedelta
from sqlalchemy import and_
import logging
import os

from database import get_db
from models import Event, News, TeamMember, Project, GalleryImage, Contact, Volunteer
from services.email_service import email_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Get absolute path to templates directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BACKEND_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ✅ HOME
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    events = db.query(Event).limit(3).all()
    news = db.query(News).filter(News.published == True).limit(2).all()
    team = db.query(TeamMember).limit(5).all()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "events": events,
        "news": news,
        "team": team
    })

# ✅ STATIC PAGES
@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/mission", response_class=HTMLResponse)
def mission(request: Request):
    return templates.TemplateResponse("mission.html", {"request": request})

@router.get("/objectives", response_class=HTMLResponse)
def objectives(request: Request):
    return templates.TemplateResponse("objective.html", {"request": request})

@router.get("/donate", response_class=HTMLResponse)
def donate(request: Request):
    return templates.TemplateResponse("donate.html", {"request": request})

@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@router.get("/terms", response_class=HTMLResponse)
def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@router.get("/refund", response_class=HTMLResponse)
def refund(request: Request):
    return templates.TemplateResponse("refund.html", {"request": request})

@router.get("/disclaimer", response_class=HTMLResponse)
def disclaimer(request: Request):
    return templates.TemplateResponse("disclaimer.html", {"request": request})

@router.get("/child-protection", response_class=HTMLResponse)
def child_protection(request: Request):
    return templates.TemplateResponse("child_protection.html", {"request": request})

@router.get("/financial-transparency", response_class=HTMLResponse)
def financial_transparency(request: Request):
    return templates.TemplateResponse("financial_transparency.html", {"request": request})

# ✅ DYNAMIC PAGES
@router.get("/events", response_class=HTMLResponse)
def events_page(request: Request, db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return templates.TemplateResponse("events.html", {
        "request": request,
        "events": events
    })

@router.get("/team", response_class=HTMLResponse)
def team_page(request: Request, db: Session = Depends(get_db)):
    team = db.query(TeamMember).all()
    return templates.TemplateResponse("team.html", {
        "request": request,
        "team": team
    })

@router.get("/gallery", response_class=HTMLResponse)
def gallery_page(request: Request, db: Session = Depends(get_db)):
    images = db.query(GalleryImage).all()
    return templates.TemplateResponse("gallery.html", {
        "request": request,
        "images": images
    })

@router.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return templates.TemplateResponse("project.html", {
        "request": request,
        "projects": projects
    })


@router.post("/contact")
def submit_contact(
    name: str = Form(..., min_length=2, max_length=255),
    email: EmailStr = Form(...),
    phone: str = Form(""),
    subject: str = Form(..., min_length=3, max_length=255),
    message: str = Form(..., min_length=10, max_length=5000),
    db: Session = Depends(get_db)
):
    """Handle contact form submission with email notification"""
    try:
        # Check for spam/rate limiting (3 submissions per 5 minutes from same email)
        recent_contacts = db.query(Contact).filter(
            and_(
                Contact.email == email,
                Contact.submitted_at > datetime.utcnow() - timedelta(minutes=5)
            )
        ).count()
        
        if recent_contacts >= 3:
            logger.warning(f"Rate limit exceeded for contact form from {email}")
            raise HTTPException(status_code=429, detail="Too many submissions. Please try again later.")
        
        # Create contact record
        contact = Contact(
            name=name.strip(),
            email=email,
            phone=phone.strip() if phone else None,
            subject=subject.strip(),
            message=message.strip(),
            read=False
        )

        db.add(contact)
        db.commit()
        
        # Send acknowledgment email to user
        subject_text = "We Received Your Message"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2>Thank You for Contacting Us!</h2>
                <p>Dear {name},</p>
                <p>We have received your message and will get back to you as soon as possible.</p>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Your Message:</strong></p>
                    <p>{message}</p>
                </div>
                <p style="margin-top: 30px; color: #666;">
                    Best regards,<br>
                    <strong>Shri Krishna Udhav Memorial Trust Team</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        success, msg = email_service.send_email(email, subject_text, html_content)
        
        if not success:
            logger.error(f"Failed to send acknowledgment email: {msg}")
        
        logger.info(f"Contact form submitted by {name} ({email})")
        return RedirectResponse("/contact?success=1", status_code=303)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Contact form error: {str(e)}", exc_info=True)
        return RedirectResponse("/contact?error=1", status_code=303)

@router.get("/volunteer", response_class=HTMLResponse)
def join_us_page(request: Request):
    return templates.TemplateResponse("volunteer_registration.html", {"request": request})

@router.post("/submit-volunteer")
def submit_volunteer(
    request: Request,
    first_name: str = Form(..., min_length=1, max_length=255),
    last_name: str = Form(..., min_length=1, max_length=255),
    email: str = Form(...),
    phone: str = Form(...),
    date_of_birth: str = Form(""),
    address: str = Form(""),
    education: str = Form(""),
    skills: str = Form(""),
    preferred_area: str = Form(...),
    availability: str = Form("4-8"),
    motivation: str = Form(""),
    db: Session = Depends(get_db)
):
    """Submit volunteer application"""
    try:
        # Validate email format
        if "@" not in email or "." not in email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        name = f"{first_name.strip()} {last_name.strip()}"
        
        # Create volunteer record
        new_volunteer = Volunteer(
            name=name,
            email=email.strip(),
            phone=phone.strip(),
            date_of_birth=date_of_birth.strip() if date_of_birth else None,
            address=address.strip() if address else None,
            education=education.strip() if education else None,
            skills=skills.strip() if skills else None,
            preferred_area=preferred_area.strip() if preferred_area else None,
            availability=availability.strip() if availability else None,
            motivation=motivation.strip() if motivation else None,
            status="pending"
        )

        db.add(new_volunteer)
        db.commit()
        db.refresh(new_volunteer)
        
        # Send acknowledgment email
        subject_text = "Volunteer Application Received 🙏"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2>Thank You for Your Interest!</h2>
                <p>Dear {name},</p>
                <p>We have received your volunteer application. Our team will review it and get back to you soon.</p>
                <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <p><strong>Application Status:</strong> <span style="color: #28a745;">PENDING REVIEW</span></p>
                </div>
                <p>If you have any questions, feel free to reach out to us.</p>
                <p style="margin-top: 30px; color: #666;">
                    Best regards,<br>
                    <strong>Shri Krishna Udhav Memorial Trust</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        success, msg = email_service.send_email(email, subject_text, html_content)
        if not success:
            logger.error(f"Failed to send volunteer acknowledgment email: {msg}")
        
        logger.info(f"Volunteer application submitted: {name} ({email})")
        return RedirectResponse(url="/volunteer?success=1", status_code=303)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Volunteer submission error: {str(e)}", exc_info=True)
        return RedirectResponse(url="/volunteer?error=1", status_code=303)


@router.post("/admin/volunteers/api/update-status")
def update_status_api(
    volunteer_id: int = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    """Update volunteer status and send notification email"""
    try:
        vol = db.query(Volunteer).get(volunteer_id)
        
        if not vol:
            return {"success": False, "message": "Volunteer not found"}
        
        # Prevent re-update
        if vol.status != "pending":
            return {"success": False, "message": "Action already taken"}

        if action == "approve":
            vol.status = "approved"
            status_text = "APPROVED"
            status_color = "#28a745"
            message_html = "<p>We are excited to welcome you to our volunteer team!</p>"
        elif action == "reject":
            vol.status = "rejected"
            status_text = "REJECTED"
            status_color = "#dc3545"
            message_html = "<p>Thank you for your interest. Unfortunately, we cannot move forward at this time.</p>"
        else:
            return {"success": False, "message": "Invalid action"}

        db.commit()
        
        # Send status update email
        subject_text = f"Volunteer Application Update - {status_text}"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2>Application Status Update</h2>
                <p>Dear {vol.name},</p>
                <div style="background-color: {status_color}; color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 18px; font-weight: bold;">Your Application Status: {status_text}</p>
                </div>
                {message_html}
                <p style="margin-top: 30px; color: #666;">
                    Best regards,<br>
                    <strong>Shri Krishna Udhav Memorial Trust</strong>
                </p>
            </div>
        </body>
        </html>
        """
        
        success, msg = email_service.send_email(vol.email, subject_text, html_content)
        if not success:
            logger.error(f"Failed to send volunteer status email: {msg}")
        
        logger.info(f"Volunteer {volunteer_id} status updated to {vol.status}")

        return {"success": True, "status": vol.status}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Volunteer status update error: {str(e)}", exc_info=True)
        return {"success": False, "message": "An error occurred"}