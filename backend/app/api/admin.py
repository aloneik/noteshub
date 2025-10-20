from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_admin_user, get_db
from app.db import models, schemas

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[schemas.UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_admin_user)
):
    """Get all users (admin only)."""
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


@router.get("/notes", response_model=List[schemas.NoteOut])
async def get_all_notes(
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_admin_user)
):
    """Get all notes from all users (admin only)."""
    result = await db.execute(
        select(models.Note)
        .options(selectinload(models.Note.plans))
        .options(selectinload(models.Note.owner))
    )
    notes = result.scalars().all()
    return notes


@router.get("/users/{user_id}/notes", response_model=List[schemas.NoteOut])
async def get_user_notes(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(get_admin_user)
):
    """Get all notes for a specific user (admin only)."""
    result = await db.execute(
        select(models.Note)
        .where(models.Note.owner_id == user_id)
        .options(selectinload(models.Note.plans))
    )
    notes = result.scalars().all()
    return notes
