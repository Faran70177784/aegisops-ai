from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import settings


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine_kwargs = {"pool_pre_ping": True}

if not settings.database_url.startswith("sqlite"):
    engine_kwargs.update({"pool_size": 10, "max_overflow": 20})

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    **engine_kwargs,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
