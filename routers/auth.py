from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models.user
from database import get_db
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token
from schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ Register (JSON)
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.user.User).filter(
        models.user.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.user.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ✅ Login (JSON - NO form, NO multipart)
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(
        models.user.User.username == user.username
    ).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }