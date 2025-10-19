import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase


def get_database_url() -> str:
    """Get database URL and convert to asyncpg if needed."""
    url = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/notehub"
    )
    
    # Render.com provides postgresql:// but we need postgresql+asyncpg://
    # Automatically convert for compatibility with asyncpg driver
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    return url


def create_engine() -> AsyncEngine:
    return create_async_engine(get_database_url(), echo=True)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


# Global engine and session maker - will be recreated if DATABASE_URL changes
_engine: Optional[AsyncEngine] = None
_session_maker: Optional[async_sessionmaker[AsyncSession]] = None
_current_db_url: Optional[str] = None


def get_engine() -> AsyncEngine:
    global _engine, _current_db_url
    current_url = get_database_url()
    if _engine is None or _current_db_url != current_url:
        _engine = create_engine()
        _current_db_url = current_url
    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    global _session_maker, _current_db_url
    current_url = get_database_url()
    engine = get_engine()
    if _session_maker is None or _current_db_url != current_url:
        _session_maker = create_session_maker(engine)
        _current_db_url = current_url
    return _session_maker


# Initialize engine and session maker
engine = get_engine()
SessionLocal = get_session_maker()


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    # Import models so that metadata is populated before create_all
    from app.db import models as _models  # noqa: F401

    assert _models is not None  # reference to avoid unused-import warnings

    current_engine = get_engine()
    async with current_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
