from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token  # type: ignore[import]
from app.db.base import get_session_maker  # type: ignore[import]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session


async def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_token(token, secret_key="secret")
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return str(payload["sub"])


async def get_admin_user(
    username: str = Depends(get_current_username),
    db: AsyncSession = Depends(get_db)
) -> str:
    """Verify that the current user is an admin."""
    from app.db import crud
    
    user = await crud.get_user_by_username(db, username)
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return username
