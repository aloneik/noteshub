import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

# Ensure "app" package is importable inside container and locally
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Use in-memory SQLite database for tests
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app  # noqa: E402


@pytest_asyncio.fixture(scope="function")
async def async_client():
    """Create a new client for each test with isolated in-memory database."""
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://testserver"
        ) as client:
            yield client


@pytest.fixture(autouse=True)
def reset_database_state():
    """Reset database connections between tests."""
    # Reset global engine and session maker to force recreation
    from app.db import base

    base._engine = None
    base._session_maker = None
    base._current_db_url = None
