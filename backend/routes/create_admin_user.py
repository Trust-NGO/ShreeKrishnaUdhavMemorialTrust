import os
import secrets
from database import SessionLocal
from models import AdminUser
from utils.auth_guard import hash_password


def create_admin():
    db = SessionLocal()

    try:
        # 🔐 Get from environment (safe for production)
        username = os.getenv("ADMIN_USERNAME", "admin")
        password = os.getenv("ADMIN_PASSWORD")
        
        if not password:
            if os.getenv("ENVIRONMENT") == "production":
                raise ValueError("ADMIN_PASSWORD must be set in production!")
            # For dev/testing only - generate secure random password
            password = secrets.token_urlsafe(16)
            print(f"⚠️  Generated temporary admin password: {password}")
            print("Please set ADMIN_PASSWORD environment variable for production")

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
        print("Username:", username, "Password:", password)

    finally:
        db.close()


# Run manually (optional)
if __name__ == "__main__":
    create_admin()