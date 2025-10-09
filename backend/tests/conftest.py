import os
import sys
from pathlib import Path
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

# Ensure "app" package is importable inside container and locally
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

from app.main import app  # noqa: E402


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client

