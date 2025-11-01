from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.user import UserCreate, UserPublic, UserLogin
from app.crud.user import create_user, get_user_by_username, authenticate_user, get_top_users

router = APIRouter(prefix="/users", tags=["users"])

MAX_PAGE = 100 # max top users pages

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = create_user(db, payload)
    return user

@router.post("/login", response_model=UserPublic)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@router.get("/list/{page}", response_model=list[UserPublic])
def list_users(page: int, db: Session = Depends(get_db)):
    if page < 1 or page > MAX_PAGE:
        raise HTTPException(status_code=400, detail="Page number out of range")
    return get_top_users(
        db,
        start_index=(page - 1) * 10 + 1,
        end_index=page * 10
    )
