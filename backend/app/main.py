from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.notes import router as notes_router
from app.api.plans import router as plans_router
from app.api.users import router as users_router
from app.core.config import settings
from app.db.base import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: F811, ARG001
    await init_db()
    yield


app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION, lifespan=lifespan)

# CORS configuration for frontend integration
# In production, replace origins with specific domains via CORS_ORIGINS environment variable
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.trycloudflare\.com",  # Allow all Cloudflare tunnels
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

app.include_router(users_router)
app.include_router(notes_router)
app.include_router(auth_router)
app.include_router(plans_router)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Welcome to NoteHub!"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "NoteHub API"}
