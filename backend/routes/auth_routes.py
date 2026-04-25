from utils.auth_guard import verify_password
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models import AdminUser
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

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
    print(f"Login attempt for user: {username}")

    user = db.query(AdminUser).filter(AdminUser.username == username).first()

    # ❌ INVALID LOGIN
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

    # ✅ SUCCESS LOGIN
    request.session["admin"] = user.username
    print("Admin logged in:", user.username)

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=302)