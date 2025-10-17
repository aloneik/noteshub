from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# User schemas
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


# Note schemas
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteOut(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    plans: list["PlanOut"] = []


# Plan schemas
class PlanBase(BaseModel):
    title: str
    is_done: bool = False


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None


class PlanOut(PlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    note_id: int
    created_at: datetime
