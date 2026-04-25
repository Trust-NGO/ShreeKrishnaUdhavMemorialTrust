from fastapi import Request, HTTPException
from passlib.context import CryptContext

# ✅ DEFINE THIS (YOU MISSED THIS)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def admin_required(request: Request):
    if "admin" not in request.session:
        raise HTTPException(status_code=401, detail="Not authorized")
    return True

def hash_password(password: str) -> str:
    password = str(password).strip()[:72]   # 🔥 bcrypt limit fix
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        plain_password = str(plain_password).strip()[:72]
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False