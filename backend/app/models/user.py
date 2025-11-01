from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, Index

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    score: Mapped[int] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

        # Create a regular btree index on score
    __table_args__ = (
        Index("ix_user_score", "score"),
        # If you insist on DESC (not necessary):
        # Index("ix_user_score_desc", score.desc()),
    )
