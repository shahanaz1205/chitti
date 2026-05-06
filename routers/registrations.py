from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.registration
from database import get_db
from schemas.registration import RegistrationCreate, RegistrationOut
from dependencies import get_current_user, admin_required

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.get("/")
def get_events(db: Session = Depends(get_db), user = Depends(admin_required)):
    return db.query(models.registration.Registration).all()

@router.post("/", response_model=RegistrationOut)
def register_event(
    reg: RegistrationCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    new_reg = models.registration.Registration(
        event_id=reg.event_id,
        user_id=user.id
    )

    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)

    return new_reg


@router.get("/me", response_model=list[RegistrationOut])
def my_registrations(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(models.registration.Registration).filter(
        models.registration.Registration.user_id == user.id
    ).all()


@router.delete("/{reg_id}")
def cancel_registration(
    reg_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    reg = db.query(models.registration.Registration).filter(
        models.registration.Registration.id == reg_id
    ).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(reg)
    db.commit()

    return {"message": "Registration cancelled"}
