from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_username, get_db
from app.db import crud
from app.db.schemas import PlanCreate, PlanOut, PlanUpdate

router = APIRouter(prefix="/notes/{note_id}/plans", tags=["plans"])


@router.get("", response_model=list[PlanOut])
async def get_plans(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
) -> Any:
    from app.db.crud import get_user_by_username

    user = await get_user_by_username(db, username)
    if not user:
        return []
    # ensure note belongs to user
    note = await crud.get_note(db, note_id=note_id, owner_id=int(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return await crud.list_plans(db, note_id=int(note.id))


@router.post("", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
async def create_plan(
    note_id: int,
    plan_in: PlanCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
) -> Any:
    from app.db.crud import get_user_by_username

    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    note = await crud.get_note(db, note_id=note_id, owner_id=int(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return await crud.create_plan(
        db, note_id=int(note.id), title=plan_in.title, is_done=plan_in.is_done
    )


@router.put("/{plan_id}", response_model=PlanOut)
async def update_plan(
    note_id: int,
    plan_id: int,
    plan_in: PlanUpdate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
) -> Any:
    from app.db.crud import get_user_by_username

    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    note = await crud.get_note(db, note_id=note_id, owner_id=int(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    plan = await crud.get_plan(db, plan_id=plan_id, note_id=int(note.id))
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    return await crud.update_plan(
        db, plan, title=plan_in.title, is_done=plan_in.is_done
    )


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    note_id: int,
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
) -> None:
    from app.db.crud import get_user_by_username

    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    note = await crud.get_note(db, note_id=note_id, owner_id=int(user.id))
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    plan = await crud.get_plan(db, plan_id=plan_id, note_id=int(note.id))
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    await crud.delete_plan(db, plan)
    return None
