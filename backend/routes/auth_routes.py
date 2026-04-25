from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

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
    if not user or not bcrypt.verify(password, user.password):
        print("Invalid login:", username)

        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "Invalid credentials"
        })

    # ✅ SUCCESS LOGIN
    request.session["admin"] = user.username
    print("Admin logged in:", user.username)

    # 🔥 FIXED REDIRECT (IMPORTANT)
    return RedirectResponse(url="/admin/dashboard", status_code=302)



@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)

    # clear session / cookie
    response.delete_cookie("access_token")

    return response