from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserCreate, UserPublic, UserLogin
from app.crud.user import create_user, get_user_by_username, authenticate_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    user = create_user(db, payload)
    return user

@router.post("/login", response_model=UserPublic)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
