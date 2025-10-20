"""
Additional tests for edge cases and error handlers to improve code coverage.
Tests focus on error paths, invalid inputs, and boundary conditions.
"""
import pytest


# Helper functions
async def register_and_login(client, username, password):
    """Register user and return access token."""
    await client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    r = await client.post(
        "/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return r.json()["access_token"]


async def create_note_helper(client, token, title="Test", content=""):
    """Create a note and return its ID."""
    r = await client.post(
        "/notes",
        json={"title": title, "content": content},
        headers={"Authorization": f"Bearer {token}"},
    )
    return r.json()["id"]


# ============================================================================
# AUTH API - Error handlers and edge cases
# ============================================================================


@pytest.mark.asyncio
async def test_register_duplicate_username(async_client):
    """Test registering with an already existing username."""
    username = "duplicate_user"
    password = "password123"
    
    # First registration should succeed
    r1 = await async_client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert r1.status_code == 200
    
    # Second registration with same username should fail
    r2 = await async_client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert r2.status_code == 400
    assert "username taken" in r2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client):
    """Test login with non-existent username."""
    r = await async_client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400
    assert "incorrect username or password" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    """Test login with correct username but wrong password."""
    username = "testuser_wrongpass"
    await async_client.post(
        "/auth/register", json={"username": username, "password": "correct123"}
    )
    
    r = await async_client.post(
        "/auth/login",
        data={"username": username, "password": "wrong123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400
    assert "incorrect username or password" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_empty_credentials(async_client):
    """Test login with empty credentials."""
    r = await async_client.post(
        "/auth/login",
        data={"username": "", "password": ""},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 400


# ============================================================================
# NOTES API - Error handlers and edge cases
# ============================================================================


@pytest.mark.asyncio
async def test_get_notes_empty_list_for_new_user(async_client):
    """Test that a new user gets empty notes list."""
    token = await register_and_login(async_client, "emptyuser", "pass123")
    
    r = await async_client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_update_note_nonexistent(async_client):
    """Test updating a note that doesn't exist."""
    token = await register_and_login(async_client, "updateuser", "pass123")
    
    r = await async_client.put(
        "/notes/99999",
        json={"title": "Updated", "content": "New content"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_note_other_user(async_client):
    """Test updating another user's note."""
    # User 1 creates a note
    token1 = await register_and_login(async_client, "owner1", "pass123")
    note_id = await create_note_helper(async_client, token1, "Owner's note")
    
    # User 2 tries to update it
    token2 = await register_and_login(async_client, "intruder1", "pass123")
    r = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "Hacked!", "content": "Malicious"},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_note_nonexistent(async_client):
    """Test deleting a note that doesn't exist."""
    token = await register_and_login(async_client, "deleteuser", "pass123")
    
    r = await async_client.delete(
        "/notes/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_note_other_user(async_client):
    """Test deleting another user's note."""
    # User 1 creates a note
    token1 = await register_and_login(async_client, "owner2", "pass123")
    note_id = await create_note_helper(async_client, token1, "Owner's note")
    
    # User 2 tries to delete it
    token2 = await register_and_login(async_client, "intruder2", "pass123")
    r = await async_client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_notes_without_auth(async_client):
    """Test accessing notes endpoints without authentication."""
    # GET notes
    r = await async_client.get("/notes")
    assert r.status_code == 401
    
    # POST note
    r = await async_client.post("/notes", json={"title": "Test", "content": ""})
    assert r.status_code == 401
    
    # PUT note
    r = await async_client.put("/notes/1", json={"title": "Test", "content": ""})
    assert r.status_code == 401
    
    # DELETE note
    r = await async_client.delete("/notes/1")
    assert r.status_code == 401


# ============================================================================
# PLANS API - Error handlers and edge cases
# ============================================================================


@pytest.mark.asyncio
async def test_get_plans_empty_list(async_client):
    """Test getting plans for a note with no plans."""
    token = await register_and_login(async_client, "emptyplans", "pass123")
    note_id = await create_note_helper(async_client, token, "Empty note")
    
    r = await async_client.get(
        f"/notes/{note_id}/plans",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_get_plans_nonexistent_note(async_client):
    """Test getting plans for a non-existent note."""
    token = await register_and_login(async_client, "planuser1", "pass123")
    
    r = await async_client.get(
        "/notes/99999/plans",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_plan_nonexistent(async_client):
    """Test updating a plan that doesn't exist."""
    token = await register_and_login(async_client, "planuser2", "pass123")
    note_id = await create_note_helper(async_client, token, "Test note")
    
    r = await async_client.put(
        f"/notes/{note_id}/plans/99999",
        json={"title": "Updated", "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_plan_wrong_note(async_client):
    """Test updating a plan via wrong note_id."""
    token = await register_and_login(async_client, "planuser3", "pass123")
    
    # Create note 1 with a plan
    note1_id = await create_note_helper(async_client, token, "Note 1")
    r = await async_client.post(
        f"/notes/{note1_id}/plans",
        json={"title": "Plan 1", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]
    
    # Create note 2
    note2_id = await create_note_helper(async_client, token, "Note 2")
    
    # Try to update plan via note2 (should fail - plan belongs to note1)
    r = await async_client.put(
        f"/notes/{note2_id}/plans/{plan_id}",
        json={"title": "Updated", "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_plan_nonexistent(async_client):
    """Test deleting a plan that doesn't exist."""
    token = await register_and_login(async_client, "planuser4", "pass123")
    note_id = await create_note_helper(async_client, token, "Test note")
    
    r = await async_client.delete(
        f"/notes/{note_id}/plans/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_delete_plan_wrong_note(async_client):
    """Test deleting a plan via wrong note_id."""
    token = await register_and_login(async_client, "planuser5", "pass123")
    
    # Create note 1 with a plan
    note1_id = await create_note_helper(async_client, token, "Note 1")
    r = await async_client.post(
        f"/notes/{note1_id}/plans",
        json={"title": "Plan 1", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]
    
    # Create note 2
    note2_id = await create_note_helper(async_client, token, "Note 2")
    
    # Try to delete plan via note2 (should fail)
    r = await async_client.delete(
        f"/notes/{note2_id}/plans/{plan_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_plans_other_users_note(async_client):
    """Test accessing plans for another user's note."""
    # User 1 creates note with plan
    token1 = await register_and_login(async_client, "owner3", "pass123")
    note_id = await create_note_helper(async_client, token1, "Owner's note")
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Secret plan", "is_done": False},
        headers={"Authorization": f"Bearer {token1}"},
    )
    plan_id = r.json()["id"]
    
    # User 2 tries to access plans
    token2 = await register_and_login(async_client, "intruder3", "pass123")
    
    # GET plans
    r = await async_client.get(
        f"/notes/{note_id}/plans",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    
    # POST plan
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Intruder plan", "is_done": False},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    
    # PUT plan
    r = await async_client.put(
        f"/notes/{note_id}/plans/{plan_id}",
        json={"title": "Hacked", "is_done": True},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    
    # DELETE plan
    r = await async_client.delete(
        f"/notes/{note_id}/plans/{plan_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_plans_without_auth(async_client):
    """Test accessing plans endpoints without authentication."""
    # GET plans
    r = await async_client.get("/notes/1/plans")
    assert r.status_code == 401
    
    # POST plan
    r = await async_client.post(
        "/notes/1/plans",
        json={"title": "Test", "is_done": False}
    )
    assert r.status_code == 401
    
    # PUT plan
    r = await async_client.put(
        "/notes/1/plans/1",
        json={"title": "Test", "is_done": False}
    )
    assert r.status_code == 401
    
    # DELETE plan
    r = await async_client.delete("/notes/1/plans/1")
    assert r.status_code == 401


# ============================================================================
# BOUNDARY CASES - Empty/null values
# ============================================================================


@pytest.mark.asyncio
async def test_create_note_empty_title(async_client):
    """Test creating a note with empty title."""
    token = await register_and_login(async_client, "emptytitle", "pass123")
    
    r = await async_client.post(
        "/notes",
        json={"title": "", "content": "Some content"},
        headers={"Authorization": f"Bearer {token}"},
    )
    # Should succeed - empty title is allowed
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_create_plan_empty_title(async_client):
    """Test creating a plan with empty title."""
    token = await register_and_login(async_client, "emptyplantitle", "pass123")
    note_id = await create_note_helper(async_client, token)
    
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    # Should succeed - empty title is allowed
    assert r.status_code == 201


@pytest.mark.asyncio
async def test_update_note_partial_fields(async_client):
    """Test updating note with only some fields."""
    token = await register_and_login(async_client, "partialupdate", "pass123")
    note_id = await create_note_helper(async_client, token, "Original", "Content")
    
    # Update only title
    r = await async_client.put(
        f"/notes/{note_id}",
        json={"title": "New Title", "content": None},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_update_plan_partial_fields(async_client):
    """Test updating plan with only some fields."""
    token = await register_and_login(async_client, "partialplanupdate", "pass123")
    note_id = await create_note_helper(async_client, token)
    
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Original Plan", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]
    
    # Update only is_done
    r = await async_client.put(
        f"/notes/{note_id}/plans/{plan_id}",
        json={"title": None, "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    assert r.json()["is_done"] is True
