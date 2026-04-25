import os
from database import SessionLocal
from models import AdminUser
from utils.auth_guard import hash_password


def create_admin():
    db = SessionLocal()

    try:
        # 🔐 Get from environment (safe for production)
        username = os.getenv("ADMIN_USERNAME", "admin")
        password = os.getenv("ADMIN_PASSWORD", "admin123")

        # Check if admin already exists
        existing = db.query(AdminUser).filter(
            AdminUser.username == username
        ).first()

        if existing:
            print("⚠ Admin already exists")
            return

        # Hash password safely
        hashed_password = hash_password(password)

        # Create admin user
        admin = AdminUser(
            username=username,
            password=hashed_password
        )

        db.add(admin)
        db.commit()

        print("✅ Admin created successfully")
        print("Username:", username)

    finally:
        db.close()


# Run manually (optional)
if __name__ == "__main__":
    create_admin()