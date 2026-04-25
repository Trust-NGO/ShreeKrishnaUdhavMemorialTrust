from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    category: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GalleryImageBase(BaseModel):
    title: str
    description: Optional[str] = None

class GalleryImageCreate(GalleryImageBase):
    image_url: str

class GalleryImage(GalleryImageCreate):
    id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    published: bool = True

class NewsCreate(NewsBase):
    pass

class News(NewsBase):
    id: int
    published_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    read: bool
    submitted_at: datetime
    
    class Config:
        from_attributes = True

class DonationBase(BaseModel):
    donor_name: str
    donor_email: str
    amount: float
    transaction_id: str
    message: Optional[str] = None

class DonationCreate(DonationBase):
    pass

class Donation(DonationBase):
    id: int
    status: str
    donation_date: datetime
    
    class Config:
        from_attributes = True

class TeamMemberBase(BaseModel):
    name: str
    position: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
