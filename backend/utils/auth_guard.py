from fastapi import Request, HTTPException

def admin_required(request: Request):
    if "admin" not in request.session:
        raise HTTPException(status_code=401, detail="Not authorized")
    return True

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])  # bcrypt safe


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)