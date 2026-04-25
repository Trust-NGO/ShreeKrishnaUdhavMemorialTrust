from fileinput import filename

from fastapi import APIRouter, Depends, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import *
import shutil
import os
from datetime import datetime
from fastapi import Query
from math import ceil
from fastapi.responses import RedirectResponse
from utils.auth_guard import admin_required

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# ================= Audit Log Helper =================

def log_audit_action(db: Session, action: str, action_details: str, user: str, user_id: int, request: Request):
    ip_address = request.client.host  # Get the IP address of the user
    user_agent = request.headers.get('User-Agent')  # Get the user agent
    session_id = request.cookies.get("session")  # Optional: session tracking, assuming you're using cookies

    audit_log = AuditLog(
        action=action,
        action_details=action_details,
        user=user,
        user_id=user_id,  # Assuming you have user IDs, if not, you may change this to something else like "admin"
        ip_address=ip_address,
        user_agent=user_agent,
        session_id=session_id,
    )

    db.add(audit_log)
    db.commit()

# ================= DASHBOARD =================

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    print("Redirecting to homepage")
    admin_required(request)
    print("Admin accessed dashboard")
    # ================= KPI COUNTS =================
    total_donation = db.query(Donation).count()
    total_contacts = db.query(Contact).count()
    total_volunteers = db.query(Volunteer).count()

    # ================= TOTAL AMOUNT (OPTIMIZED SQL) =================
    total_amount = db.query(
        func.coalesce(func.sum(Donation.amount), 0)
    ).scalar()

    # ================= RECENT DONATIONS =================
    recent_donations = (
        db.query(Donation)
        .order_by(Donation.id.desc())
        .limit(5)
        .all()
    )
    print("Recent Donations:", recent_donations)
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "donations": total_donation,
        "contacts": total_contacts,
        "volunteers": total_volunteers,
        "total_amount": total_amount,
        "recent_donations": recent_donations
    })

# ================= DONATIONS =================
@router.get("/donations")
def donations(request: Request, db: Session = Depends(get_db), page: int = Query(1, ge=1), page_size: int = 10):
    admin_required(request)
    
    # Pagination logic
    offset = (page - 1) * page_size
    total_donations = db.query(Donation).count()
    donations = db.query(Donation).offset(offset).limit(page_size).all()

    total_pages = (total_donations + page_size - 1) // page_size  # Calculate total pages

    return templates.TemplateResponse("admin/donations.html", {
        "request": request,
        "donations": donations,
        "page": page,
        "total_pages": total_pages,
        "page_size": page_size
    })


# ================= CONTACTS =================
@router.get("/contacts")
def contacts(request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    data = db.query(Contact).order_by(Contact.id.desc()).all()

    return templates.TemplateResponse("admin/contacts.html", {
        "request": request,
        "contacts": data
    })

@router.post("/contact/resolve/{id}")
def resolve_contact(id: int, request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    
    # Fetch the contact from the database
    contact = db.query(Contact).filter(Contact.id == id).first()
    
    # If the contact exists, update its status to 'resolved'
    if contact and contact.read is not True:
        contact.read = True
        db.commit()

        # Log the action in the audit log
        log_audit_action(
            db, 
            action=f"Contact {id} resolved", 
            action_details=f"Contact with ID {id} marked as resolved.",
            user="admin", 
            user_id=1,  # Change this to the actual logged-in user's ID
            request=request
        )

    return RedirectResponse("/admin/contacts", status_code=302)

# ================= VOLUNTEERS =================
@router.get("/volunteers")
def volunteers(request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    data = db.query(Volunteer).all()

    return templates.TemplateResponse("admin/volunteers.html", {
        "request": request,
        "volunteers": data
    })

@router.get("/volunteer/approve/{id}")
def approve_volunteer(id: int, request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    v = db.query(Volunteer).get(id)
    if v:
        v.status = "approved"
        db.commit()

        # Log the action in the audit log
        log_audit_action(db, action=f"Volunteer {id} approved", action_details=f"Volunteer with ID {id} has been approved.", user="admin", user_id=1, request=request)

    return {"status": "approved"}

# ================= DOCUMENTS =================
@router.get("/documents")
def documents(request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    data = db.query(Document).all()

    return templates.TemplateResponse("admin/documents.html", {
        "request": request,
        "documents": data
    })



# Define the upload directory
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= DOCUMENTS UPLOAD =================
@router.post("/documents/upload")
def upload_document(
    request: Request,  # Request object injected first
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)  # db is injected with Depends
):
    # Save the uploaded file
    filename = f"{datetime.now().timestamp()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save the document details in the database
    document = Document(
        title=title,
        file_url=f"/uploads/documents/{filename}",  # Assuming static files are served from /uploads
        uploaded_at=datetime.utcnow()
    )

    db.add(document)
    db.commit()

     # Log the action in the audit log
    log_audit_action(db, action="Uploaded new document", action_details=f"Document '{title}' uploaded.", user="admin", user_id=1, request=request)


    # Redirect back to the documents page after uploading
    return RedirectResponse("/admin/documents", status_code=302)




# ================= ADD EVENT =================
UPLOAD_DIR = "uploads/events"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/events/add")
def add_event(
    request: Request,  # Request should come first
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)  # db should come last
):
    # Save image
    filename = f"{datetime.now().timestamp()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Save DB
    event = Event(
        title=title,
        description=description,
        location=location,
        date=datetime.fromisoformat(date),
        image_url=f"/uploads/events/{filename}"
    )

    try:
        db.add(event)
        db.commit()

        # Log the action in the audit log
        log_audit_action(db, action="Created new event", action_details=f"Event '{title}' added to the system.", user="admin", user_id=1, request=request)
    except Exception as exc:
        db.rollback()
        return {"error": "Event could not be saved. Please check the data."}

    return RedirectResponse("/admin/events", status_code=302)
# ================= DELETE EVENT =================
@router.get("/events/delete/{id}")
def delete_event(id: int, request: Request, db: Session = Depends(get_db)):
    event = db.query(Event).get(id)

    if event:
        db.delete(event)
        db.commit()

        # Log deletion action in audit log
        log_audit_action(db, action="Deleted event", action_details=f"Event with ID {id} deleted from the system.", user="admin", user_id=1, request=request)
        db.commit()

    return RedirectResponse("/admin/events", status_code=302)

# ================= EVENTS PAGE =================
@router.get("/events")
def events_page(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = 6
):
    total = db.query(Event).count()

    events = (
        db.query(Event)
        .order_by(Event.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    total_pages = ceil(total / limit)

    return templates.TemplateResponse("admin/events.html", {
        "request": request,
        "events": events,
        "page": page,
        "total_pages": total_pages,
        "pages": list(range(1, total_pages + 1))
    })

# ================= SETUP TEAM MEMBERS UPLOAD DIR =================
TEAM_UPLOAD_DIR = "uploads/team_members"
os.makedirs(TEAM_UPLOAD_DIR, exist_ok=True)

# ================= AUDIT =================

@router.get("/audit")
def audit(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
    action: str = None,
    user: str = None,
    start_date: str = None,
    end_date: str = None
):
    admin_required(request)  # Ensure only admins can access
    
    query = db.query(AuditLog)

    # Apply filters if provided
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    if user:
        query = query.filter(AuditLog.user.ilike(f"%{user}%"))
    
    # Handle date range filtering with correct date parsing
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(AuditLog.created_at.between(start_date_obj, end_date_obj))
        except ValueError as e:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}  # Send error response if date format is incorrect
    
    # Pagination logic
    offset = (page - 1) * page_size
    logs = query.order_by(AuditLog.id.desc()).offset(offset).limit(page_size).all()

    # Get total logs count
    total_logs = db.query(AuditLog).count()
    total_pages = (total_logs + page_size - 1) // page_size
    
    return templates.TemplateResponse("admin/audit.html", {
        "request": request,
        "logs": logs,
        "page": page,
        "total_pages": total_pages
    })



# Team Member 

@router.get("/team_members")
async def get_team_members(request: Request, db: Session = Depends(get_db)):
    # Fetch all team members from the database
    team_members = db.query(TeamMember).all()
    
    # Ensure that team_members is not empty or None before passing to the template
    return templates.TemplateResponse("admin/team_members.html", {
        "request": request,
        "team_members": team_members
    })


# ================= ADD TEAM MEMBER =================
@router.post("/team/add")
async def add_team_member(
    request: Request,
    name: str = Form(...),
    position: str = Form(...),
    bio: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{int(datetime.now().timestamp())}_{photo.filename}"
    file_path = os.path.join(TEAM_UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    print(filename)
    new_member = TeamMember(
        name=name,
        position=position,
        bio=bio,
        email=email,
        phone=phone,
        photo_url=f"/uploads/team_members/{filename}"  # ✅ FIXED
    )

    db.add(new_member)
    db.commit()

    return RedirectResponse("/admin/team_members?success=1", status_code=303)

# ================= EDIT TEAM MEMBER =================
@router.post("/team/edit/{id}")
async def edit_team_member(
    id: int,
    name: str = Form(...),
    position: str = Form(...),
    bio: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    photo: UploadFile = File(None),  # ✅ optional
    db: Session = Depends(get_db)
):
    member = db.query(TeamMember).filter(TeamMember.id == id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Not found")

    member.name = name
    member.position = position
    member.bio = bio
    member.email = email
    member.phone = phone

    # ✅ update image only if new one uploaded
    if photo and photo.filename:
        filename = f"{int(datetime.now().timestamp())}_{photo.filename}"
        file_path = os.path.join(TEAM_UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        member.photo_url = f"/uploads/team_members/{filename}"

    db.commit()

    return RedirectResponse("/admin/team_members?success=1", status_code=303)

# ================= DELETE TEAM MEMBER =================
@router.delete("/team/{id}/delete")
async def delete_team_member(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    member = db.query(TeamMember).filter(TeamMember.id == id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    # Delete the member from database
    db.delete(member)
    db.commit()

    return {"status": "deleted"}