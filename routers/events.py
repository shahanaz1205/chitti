from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.event
from database import get_db
from schemas.event import EventCreate, EventOut
from dependencies import admin_required

router = APIRouter(prefix="/events", tags=["Events"])


# ✅ Public
@router.get("/", response_model=list[EventOut])
def get_events(db: Session = Depends(get_db)):
    return db.query(models.event.Event).all()


# 🔒 Admin only
@router.post("/", response_model=EventOut)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    user = Depends(admin_required)
):
    new_event = models.event.Event(**event.dict())

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


# 🔒 Admin only
@router.put("/{event_id}")
def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(get_db),
    user = Depends(admin_required)
):
    db_event = db.query(models.event.Event).filter(
        models.event.Event.id == event_id
    ).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in event.dict().items():
        setattr(db_event, key, value)

    db.commit()
    return db_event


# 🔒 Admin only
@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user = Depends(admin_required)
):
    db_event = db.query(models.event.Event).filter(
        models.event.Event.id == event_id
    ).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)
    db.commit()

    return {"message": "Event deleted"}