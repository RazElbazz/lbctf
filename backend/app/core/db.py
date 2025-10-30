from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from app.core.config import settings
from app.models.user import Base  # ensure models are imported before create_all

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:  # noqa: E722
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
