from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_user(db: Session, user_in: UserCreate, is_superuser: bool = False):
    user = User(
        username=user_in.username,
        password_hash=hash_password(user_in.password),
        score=0,
        is_superuser=is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_top_users(db: Session, start_index: int, end_index: int) -> list[User]:
    # Calculate how many records to fetch
    limit = end_index - start_index + 1
    offset = start_index - 1  # start_index=1 means the top user

    stmt = (
        select(User)
        .order_by(User.score.desc())
        .offset(offset)
        .limit(limit)
    )

    return db.execute(stmt).scalars().all()
