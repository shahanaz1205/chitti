from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.registration
from database import get_db
from schemas.registration import RegistrationCreate, RegistrationOut
from dependencies import get_current_user

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)

# ✅ ADMIN → ALL REGISTRATIONS
# ✅ USER → OWN REGISTRATIONS
@router.get("/")
def get_registrations(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    # ✅ ADMIN
    if user.role == "admin":

        registrations = db.query(
            models.registration.Registration
        ).all()

    # ✅ NORMAL USER
    else:

        registrations = db.query(
            models.registration.Registration
        ).filter(
            models.registration.Registration.user_id == user.id
        ).all()

    # ✅ RESPONSE WITH USERNAME
    result = []

    for reg in registrations:

        result.append({
            "id": reg.id,
            "user_id": reg.user_id,
            "username": reg.user.username,
            "event_id": reg.event_id
        })

    return result


# ✅ REGISTER EVENT
@router.post("/", response_model=RegistrationOut)
def register_event(
    reg: RegistrationCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    # ❌ ADMIN CANNOT REGISTER
    if user.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin cannot register events"
        )

    new_reg = models.registration.Registration(
        event_id=reg.event_id,
        user_id=user.id
    )

    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)

    return new_reg


# ✅ USER OWN REGISTRATIONS
@router.get("/me", response_model=list[RegistrationOut])
def my_registrations(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return db.query(
        models.registration.Registration
    ).filter(
        models.registration.Registration.user_id == user.id
    ).all()


# ✅ CANCEL REGISTRATION
@router.delete("/{reg_id}")
def cancel_registration(
    reg_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    reg = db.query(
        models.registration.Registration
    ).filter(
        models.registration.Registration.id == reg_id
    ).first()

    if not reg:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    # ✅ USER CAN CANCEL ONLY OWN
    # ✅ ADMIN CAN CANCEL ANY
    if user.role != "admin" and reg.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    db.delete(reg)
    db.commit()

    return {
        "message": "Registration cancelled"
    }