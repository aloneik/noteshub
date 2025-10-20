import pytest


# Helper functions for test setup
async def create_authenticated_user(client, username="noteuser", password="secret123"):
    """Helper function to register and login a user, returning token."""
    await client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    r = await client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


async def create_note(client, token, title="Test Note", content="Test Content"):
    """Helper function to create a note and return the note data."""
    r = await client.post(
        "/notes",
        json={"title": title, "content": content},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    return r.json()


# Note update tests
@pytest.mark.asyncio
async def test_update_note(async_client):
    """Test updating a note."""
    token = await create_authenticated_user(async_client, "updateuser")
    note = await create_note(async_client, token, "Original Title", "Original Content")
    note_id = note["id"]

    # Update the note
    r = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Title", "content": "Updated Content"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    updated_note = r.json()
    assert updated_note["title"] == "Updated Title"
    assert updated_note["content"] == "Updated Content"
    assert updated_note["id"] == note_id


@pytest.mark.asyncio
async def test_update_note_partial(async_client):
    """Test partially updating a note (only title)."""
    token = await create_authenticated_user(async_client, "partialuser")
    note = await create_note(async_client, token, "Original Title", "Keep this content")
    note_id = note["id"]

    # Update only title
    r = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "New Title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    updated_note = r.json()
    assert updated_note["title"] == "New Title"
    assert updated_note["content"] == "Keep this content"  # Content unchanged


@pytest.mark.asyncio
async def test_update_note_unauthorized(async_client):
    """Test updating a note without authentication."""
    r = await async_client.put(
        "/notes/1",
        json={"title": "Unauthorized update"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_update_nonexistent_note(async_client):
    """Test updating a non-existent note."""
    token = await create_authenticated_user(async_client, "nonexistuser")

    r = await async_client.put(
        "/notes/99999",
        json={"title": "This won't work"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]


@pytest.mark.asyncio
async def test_update_other_users_note(async_client):
    """Test updating another user's note."""
    # Create first user with note
    token1 = await create_authenticated_user(async_client, "owner", "password123")
    note = await create_note(async_client, token1, "Owner's Note", "Private content")
    note_id = note["id"]

    # Create second user
    token2 = await create_authenticated_user(async_client, "intruder", "password123")

    # Try to update first user's note with second user's token
    r = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "Intruder's update"},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]


# Note deletion tests
@pytest.mark.asyncio
async def test_delete_note(async_client):
    """Test deleting a note."""
    token = await create_authenticated_user(async_client, "deleteuser")
    note = await create_note(async_client, token, "Note to delete", "Content to delete")
    note_id = note["id"]

    # Delete the note
    r = await async_client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 204

    # Verify note is deleted by trying to list notes
    r = await async_client.get("/notes", headers={"Authorization": f"Bearer {token}"})
    notes = r.json()
    assert len(notes) == 0


@pytest.mark.asyncio
async def test_delete_note_unauthorized(async_client):
    """Test deleting a note without authentication."""
    r = await async_client.delete("/notes/1")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_delete_nonexistent_note(async_client):
    """Test deleting a non-existent note."""
    token = await create_authenticated_user(async_client, "deletenonexistuser")

    r = await async_client.delete(
        "/notes/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]


@pytest.mark.asyncio
async def test_delete_other_users_note(async_client):
    """Test deleting another user's note."""
    # Create first user with note
    token1 = await create_authenticated_user(async_client, "noteowner", "password123")
    note = await create_note(async_client, token1, "Protected Note", "Private content")
    note_id = note["id"]

    # Create second user
    token2 = await create_authenticated_user(async_client, "notedeleter", "password123")

    # Try to delete first user's note with second user's token
    r = await async_client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]

    # Verify original note still exists
    r = await async_client.get("/notes", headers={"Authorization": f"Bearer {token1}"})
    notes = r.json()
    assert len(notes) == 1
    assert notes[0]["title"] == "Protected Note"


# Note validation tests
@pytest.mark.asyncio
async def test_create_note_empty_title(async_client):
    """Test creating a note with empty title (currently allowed)."""
    token = await create_authenticated_user(async_client, "validationuser")

    r = await async_client.post(
        "/notes",
        json={"title": "", "content": "Some content"},
        headers={"Authorization": f"Bearer {token}"},
    )
    # Empty title is currently allowed by the API
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == ""
    assert note["content"] == "Some content"


@pytest.mark.asyncio
async def test_create_note_no_title(async_client):
    """Test creating a note without title should fail."""
    token = await create_authenticated_user(async_client, "notitleuser")

    r = await async_client.post(
        "/notes",
        json={"content": "Content without title"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_create_note_with_null_content(async_client):
    """Test creating a note with null content (should be allowed)."""
    token = await create_authenticated_user(async_client, "nullcontentuser")

    r = await async_client.post(
        "/notes",
        json={"title": "Title only", "content": None},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "Title only"
    assert note["content"] is None


@pytest.mark.asyncio
async def test_create_note_without_content_field(async_client):
    """Test creating a note without content field (should be allowed)."""
    token = await create_authenticated_user(async_client, "nocontentfielduser")

    r = await async_client.post(
        "/notes",
        json={"title": "Title only"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "Title only"
    # Content should be None or empty based on schema default


# Get single note tests
@pytest.mark.asyncio
async def test_get_single_note(async_client):
    """Test getting a single note by ID."""
    token = await create_authenticated_user(async_client, "getsingleuser")
    note = await create_note(async_client, token, "My Note", "My Content")
    note_id = note["id"]

    r = await async_client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    fetched_note = r.json()
    assert fetched_note["id"] == note_id
    assert fetched_note["title"] == "My Note"
    assert fetched_note["content"] == "My Content"


@pytest.mark.asyncio
async def test_get_single_note_nonexistent(async_client):
    """Test getting a note that doesn't exist."""
    token = await create_authenticated_user(async_client, "getnonexistentuser")

    r = await async_client.get(
        "/notes/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_single_note_other_user(async_client):
    """Test getting another user's note."""
    # User 1 creates a note
    token1 = await create_authenticated_user(async_client, "noteowner1")
    note = await create_note(async_client, token1, "Private Note")
    note_id = note["id"]

    # User 2 tries to access it
    token2 = await create_authenticated_user(async_client, "intruder4")
    r = await async_client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_single_note_without_auth(async_client):
    """Test getting a note without authentication."""
    r = await async_client.get("/notes/1")
    assert r.status_code == 401
