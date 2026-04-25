from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    description = Column(Text)
    image_url = Column(String(500), nullable=True)
    date = Column(DateTime, default=func.now())
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    description = Column(Text)
    image_url = Column(String(500), nullable=True)
    category = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text, nullable=True)
    image_url = Column(String(500), unique=True, index=True)
    uploaded_at = Column(DateTime, default=func.now())

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    content = Column(Text)
    image_url = Column(String(500), nullable=True)
    published = Column(Boolean, default=True)
    published_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    subject = Column(String(255))
    message = Column(Text)
    read = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=func.now())

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, nullable=False)
    donor_email = Column(String, nullable=False)
    # 🔥 80G REQUIRED FIELD
    donor_pan = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String, unique=True, index=True)
    payment_status = Column(String, default="pending")
    purpose = Column(String, default="General Donation")
    receipt_no = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    position = Column(String(255))
    bio = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=func.now())


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    skills = Column(String)
    availability = Column(String)
    status = Column(String, default="pending")  # pending/approved/rejected
    created_at = Column(DateTime, default=datetime.utcnow)

# ================= DOCUMENT =================
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    file_url = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


# ================= AUDIT =================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)  # Type of action (Create, Update, Delete, etc.)
    action_details = Column(Text, nullable=True)  # Detailed description of what was changed
    user_id = Column(Integer, nullable=False)  # Reference to the User performing the action
    user = Column(String, nullable=False)  # Username or email of the user (use user_id as reference)
    ip_address = Column(String, nullable=True)  # IP address of the user
    user_agent = Column(String, nullable=True)  # User agent from the request headers
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp when the action occurred
    session_id = Column(String, nullable=True)  # Optional: track session ID for correlation between actions

# ================= ADMIN =================
class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="admin")
