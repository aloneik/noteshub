import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/notehub")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def init_db():
    # Import models so that metadata is populated before create_all
    from app.db import models as _models  # noqa: F401
    assert _models is not None  # reference to avoid unused-import warnings

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
