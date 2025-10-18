"""Data models for NoteHub Desktop."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model."""
    
    id: int
    username: str
    created_at: Optional[datetime] = None


class Note(BaseModel):
    """Note model."""
    
    id: int
    title: str
    content: Optional[str] = ""
    owner_id: int  # Changed from user_id to match backend
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Plan(BaseModel):
    """Daily plan model."""
    
    id: int
    title: str  # Changed from content to match backend
    is_done: bool = False  # Changed from completed to match backend
    note_id: int
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class NoteWithPlans(Note):
    """Note with its plans."""
    
    plans: list[Plan] = []


class LoginRequest(BaseModel):
    """Login request."""
    
    username: str
    password: str


class RegisterRequest(BaseModel):
    """Registration request."""
    
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response after login."""
    
    access_token: str
    token_type: str = "bearer"


class NoteCreate(BaseModel):
    """Create note request."""
    
    title: str
    content: str = ""


class NoteUpdate(BaseModel):
    """Update note request."""
    
    title: Optional[str] = None
    content: Optional[str] = None


class PlanCreate(BaseModel):
    """Create plan request."""
    
    title: str  # Changed from content to match backend
    is_done: bool = False  # Changed from completed to match backend


class PlanUpdate(BaseModel):
    """Update plan request."""
    
    title: Optional[str] = None  # Changed from content to match backend
    is_done: Optional[bool] = None  # Changed from completed to match backend
