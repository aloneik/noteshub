from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.notes import router as notes_router
from app.api.plans import router as plans_router
from app.api.users import router as users_router
from app.db.base import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):  # noqa: F811, ARG001
    await init_db()
    yield


app = FastAPI(title="NoteHub API", lifespan=lifespan)

app.include_router(users_router)
app.include_router(notes_router)
app.include_router(auth_router)
app.include_router(plans_router)


@app.get("/")
def root():
    return {"message": "Welcome to NoteHub!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "NoteHub API"}
