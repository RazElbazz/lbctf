from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user import Base
from app.crud.user import get_user_by_username, create_user
from app.schemas.user import UserCreate

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
        db.commit()        # commit if all went well
    except Exception:
        db.rollback()      # rollback on error
        raise
    finally:
        db.close()

def init_db():
    """Initialize the database and create the first superuser."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if superuser already exists
        superuser = get_user_by_username(db, settings.FIRST_SUPERUSER)
        if not superuser:
            print(f"Creating initial superuser: {settings.FIRST_SUPERUSER}")
            user_in = UserCreate(
                username=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
            )
            user = create_user(db, user_in, is_superuser=True)
    finally:
        db.close()
