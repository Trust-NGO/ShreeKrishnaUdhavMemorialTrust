from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Event
from utils.auth_guard import admin_required

router = APIRouter()

@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.post("/")
def create_event(event: dict, request: Request, db: Session = Depends(get_db)):
    admin_required(request)

    # Validate event date is not in the past
    event_date_str = event.get("date")
    if event_date_str:
        try:
            event_date = datetime.fromisoformat(event_date_str)
            # Compare dates only (not times) so same-day events are allowed
            if event_date.date() < datetime.utcnow().date():
                raise HTTPException(status_code=400, detail="Event date cannot be in the past")
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DDTHH:MM:SS")

    db_event = Event(**event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, request: Request, db: Session = Depends(get_db)):
    admin_required(request)
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": "Deleted"}