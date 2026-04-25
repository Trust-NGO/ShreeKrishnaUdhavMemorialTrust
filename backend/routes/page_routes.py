from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import EmailStr
from datetime import datetime, timedelta
from sqlalchemy import and_

from database import get_db
from models import Event, News, TeamMember, Project, GalleryImage, Contact, Volunteer

router = APIRouter()
templates = Jinja2Templates(directory="templates")

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
    subject: str = Form(..., min_length=3, max_length=255),
    message: str = Form(..., min_length=10, max_length=5000),
    db: Session = Depends(get_db)
):
    try:
        # Check for spam/rate limiting (5 submissions per 5 minutes from same email)
        recent_contacts = db.query(Contact).filter(
            and_(
                Contact.email == email,
                Contact.submitted_at > datetime.utcnow() - timedelta(minutes=5)
            )
        ).count()
        
        if recent_contacts >= 3:
            raise HTTPException(429, "Too many submissions. Please try again later.")
        
        contact = Contact(
            name=name.strip(),
            email=email,
            subject=subject.strip(),
            message=message.strip(),
            read=False
        )

        db.add(contact)
        db.commit()
        return RedirectResponse("/contact?success=1", status_code=303)

    except Exception as e:
        db.rollback()
        print("ERROR:", e)
        return RedirectResponse("/contact?error=1", status_code=303)

    return RedirectResponse("/contact?success=1", status_code=303)

@router.get("/volunteer", response_class=HTMLResponse)
def join_us_page(request: Request):
    return templates.TemplateResponse("volunteer_registration.html", {"request": request})

@router.post("/submit-volunteer")
def submit_volunteer(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    skills: str = Form(...),
    availability: str = Form(...),
    db: Session = Depends(get_db)
):

    new_volunteer = Volunteer(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        availability=availability
    )

    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)

    return RedirectResponse(url="/?success=1", status_code=303)


@router.post("/admin/volunteers/api/update-status")
def update_status_api(
    volunteer_id: int = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    vol = db.query(Volunteer).get(volunteer_id)

    # 🚫 Prevent re-update
    if vol.status != "pending":
        return {
            "success": False,
            "message": "Action already taken"
        }

    if action == "approve":
        vol.status = "approved"
    elif action == "reject":
        vol.status = "rejected"

    db.commit()

    return {
        "success": True,
        "status": vol.status
    }