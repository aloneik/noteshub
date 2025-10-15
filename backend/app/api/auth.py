from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db  # type: ignore[import]
from app.core.security import (  # type: ignore[import]
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db import crud  # type: ignore[import]
from app.db.schemas import Token, UserCreate, UserOut  # type: ignore[import]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> UserOut:
    existing = await crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username taken"
        )
    user = await crud.create_user(
        db, user_in.username, get_password_hash(user_in.password)
    )
    return UserOut.model_validate(user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> Token:
    user = await crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    token = create_access_token(
        subject=str(user.username), secret_key="secret", expires_minutes=60 * 24
    )
    return Token(access_token=token)
