from database import get_db, SessionLocal
from models import AdminUser
from passlib.context import CryptContext

#python -m routes.create_admin_user # run this from backend path to create admin user 
# 🔐 Setup hashing (BEST PRACTICE)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()

    username = "admin"
    password = "admin123"   # 🔥 change this later

    # Check if already exists
    existing = db.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        print("⚠ Admin already exists")
        return

    hashed_password = pwd_context.hash(password)

    admin = AdminUser(
        username=username,
        password=hashed_password
    )

    db.add(admin)
    db.commit()

    print("✅ Admin created successfully")
    print("Username:", username)
    print("Password:", password)

if __name__ == "__main__":
    create_admin()