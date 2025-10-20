from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_username, get_db
from app.db import crud, schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserOut)
async def get_current_user(
    username: str = Depends(get_current_username),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information."""
    user = await crud.get_user_by_username(db, username)
    return user
