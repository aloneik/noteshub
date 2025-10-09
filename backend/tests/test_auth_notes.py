import pytest


# Helper functions for test setup
async def register_user(client, username="testuser", password="secret123"):
    """Helper function to register a user."""
    r = await client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert r.status_code == 200, r.text
    return r.json()


async def login_user(client, username="testuser", password="secret123"):
    """Helper function to login a user and return token."""
    r = await client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


async def create_authenticated_user(client, username="testuser", password="secret123"):
    """Helper function to register and login a user, returning token."""
    await register_user(client, username, password)
    return await login_user(client, username, password)


# Authentication tests
@pytest.mark.asyncio
async def test_user_registration(async_client):
    """Test user registration functionality."""
    user = await register_user(async_client, "newuser", "password123")
    assert user["username"] == "newuser"
    assert "id" in user
    assert user["id"] > 0


@pytest.mark.asyncio
async def test_user_registration_duplicate_username(async_client):
    """Test that duplicate usernames are rejected."""
    # Register first user
    await register_user(async_client, "duplicate", "password123")

    # Try to register same username again
    r = await async_client.post(
        "/auth/register", json={"username": "duplicate", "password": "password456"}
    )
    assert r.status_code == 400
    assert "Username taken" in r.json()["detail"]


@pytest.mark.asyncio
async def test_user_login_success(async_client):
    """Test successful user login."""
    await register_user(async_client, "loginuser", "password123")
    token = await login_user(async_client, "loginuser", "password123")
    assert token is not None
    assert len(token) > 0


@pytest.mark.asyncio
async def test_user_login_invalid_credentials(async_client):
    """Test login with invalid credentials."""
    await register_user(async_client, "validuser", "password123")

    # Try login with wrong password
    r = await async_client.post(
        "/auth/login",
        data={"username": "validuser", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400
    assert "Incorrect username or password" in r.json()["detail"]


@pytest.mark.asyncio
async def test_user_login_nonexistent_user(async_client):
    """Test login with non-existent user."""
    r = await async_client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400
    assert "Incorrect username or password" in r.json()["detail"]


# Notes tests
@pytest.mark.asyncio
async def test_create_note(async_client):
    """Test creating a note."""
    token = await create_authenticated_user(async_client, "noteuser", "password123")

    r = await async_client.post(
        "/notes",
        json={"title": "Test Note", "content": "This is a test note"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "Test Note"
    assert note["content"] == "This is a test note"
    assert "id" in note
    assert "owner_id" in note


@pytest.mark.asyncio
async def test_create_note_unauthorized(async_client):
    """Test creating a note without authentication."""
    r = await async_client.post(
        "/notes",
        json={"title": "Unauthorized Note", "content": "This should fail"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_list_notes_empty(async_client):
    """Test listing notes when user has no notes."""
    token = await create_authenticated_user(async_client, "emptyuser", "password123")

    r = await async_client.get("/notes", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    notes = r.json()
    assert isinstance(notes, list)
    assert len(notes) == 0


@pytest.mark.asyncio
async def test_list_notes_with_content(async_client):
    """Test listing notes when user has notes."""
    token = await create_authenticated_user(async_client, "listuser", "password123")

    # Create a note first
    await async_client.post(
        "/notes",
        json={"title": "Listed Note", "content": "Content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # List notes
    r = await async_client.get("/notes", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    notes = r.json()
    assert isinstance(notes, list)
    assert len(notes) == 1
    assert notes[0]["title"] == "Listed Note"


@pytest.mark.asyncio
async def test_list_notes_unauthorized(async_client):
    """Test listing notes without authentication."""
    r = await async_client.get("/notes")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_notes_isolation_between_users(async_client):
    """Test that users can only see their own notes."""
    # Create two users
    token1 = await create_authenticated_user(async_client, "user1", "password123")
    token2 = await create_authenticated_user(async_client, "user2", "password123")

    # User1 creates a note
    await async_client.post(
        "/notes",
        json={"title": "User1 Note", "content": "Private content"},
        headers={"Authorization": f"Bearer {token1}"},
    )

    # User2 creates a note
    await async_client.post(
        "/notes",
        json={"title": "User2 Note", "content": "Different content"},
        headers={"Authorization": f"Bearer {token2}"},
    )

    # User1 should only see their note
    r1 = await async_client.get("/notes", headers={"Authorization": f"Bearer {token1}"})
    notes1 = r1.json()
    assert len(notes1) == 1
    assert notes1[0]["title"] == "User1 Note"

    # User2 should only see their note
    r2 = await async_client.get("/notes", headers={"Authorization": f"Bearer {token2}"})
    notes2 = r2.json()
    assert len(notes2) == 1
    assert notes2[0]["title"] == "User2 Note"
