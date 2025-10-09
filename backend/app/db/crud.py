from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


# Users
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[models.User]:
    res = await db.execute(select(models.User).where(models.User.username == username))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password_hash: str) -> models.User:
    user = models.User(username=username, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Notes
async def list_notes(db: AsyncSession, owner_id: int) -> Sequence[models.Note]:
    res = await db.execute(select(models.Note).where(models.Note.owner_id == owner_id))
    return res.scalars().all()


async def get_note(db: AsyncSession, note_id: int, owner_id: int) -> Optional[models.Note]:
    res = await db.execute(
        select(models.Note).where(models.Note.id == note_id, models.Note.owner_id == owner_id)
    )
    return res.scalar_one_or_none()


async def create_note(db: AsyncSession, owner_id: int, title: str, content: Optional[str]) -> models.Note:
    note = models.Note(title=title, content=content, owner_id=owner_id)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def update_note(db: AsyncSession, note: models.Note, title: Optional[str], content: Optional[str]) -> models.Note:
    if title is not None:
        note.title = title  # type: ignore[assignment]
    if content is not None:
        note.content = content  # type: ignore[assignment]
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note: models.Note) -> None:
    await db.delete(note)
    await db.commit()


# Plans
async def list_plans(db: AsyncSession, note_id: int):
    res = await db.execute(select(models.Plan).where(models.Plan.note_id == note_id))
    return res.scalars().all()


async def get_plan(db: AsyncSession, plan_id: int, note_id: int):
    res = await db.execute(
        select(models.Plan).where(models.Plan.id == plan_id, models.Plan.note_id == note_id)
    )
    return res.scalar_one_or_none()


async def create_plan(db: AsyncSession, note_id: int, title: str, is_done: bool):
    plan = models.Plan(title=title, is_done=is_done, note_id=note_id)
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


async def update_plan(db: AsyncSession, plan: models.Plan, *, title=None, is_done=None):
    if title is not None:
        plan.title = title
    if is_done is not None:
        plan.is_done = is_done
    await db.commit()
    await db.refresh(plan)
    return plan


async def delete_plan(db: AsyncSession, plan: models.Plan) -> None:
    await db.delete(plan)
    await db.commit()


