from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_username, get_db  # type: ignore[import]
from app.db import crud  # type: ignore[import]
from app.db.schemas import NoteCreate, NoteOut, NoteUpdate  # type: ignore[import]

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteOut])
async def get_notes(
    db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)
):
    # In MVP we use username as identifier to fetch user and their notes
    from app.db.crud import (
        get_user_by_username,  # local import to avoid circulars in small files
    )

    user = await get_user_by_username(db, username)
    if not user:
        return []
    return await crud.list_notes(db, owner_id=int(user.id))


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_in: NoteCreate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
):
    from app.db.crud import get_user_by_username

    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return await crud.create_note(
        db, owner_id=int(user.id), title=note_in.title, content=note_in.content
    )


@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
):
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
    return await crud.update_note(
        db, note, title=note_in.title, content=note_in.content
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    username: str = Depends(get_current_username),
):
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
    await crud.delete_note(db, note)
    return None
