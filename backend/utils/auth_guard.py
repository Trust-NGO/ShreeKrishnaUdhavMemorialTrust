from fastapi import Request, HTTPException

def admin_required(request: Request):
    if "admin" not in request.session:
        raise HTTPException(status_code=401, detail="Not authorized")
    return True