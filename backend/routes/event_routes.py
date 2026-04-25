from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Event

router = APIRouter()

@router.get("/")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.post("/")
def create_event(event: dict, db: Session = Depends(get_db)):
    db_event = Event(**event)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": "Deleted"}