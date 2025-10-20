import pytest


# Helper functions for test setup
async def create_authenticated_user(client, username="planner", password="secret123"):
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


async def create_note(client, token, title="Test Note", content=""):
    """Helper function to create a note and return note_id."""
    r = await client.post(
        "/notes",
        json={"title": title, "content": content},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


async def create_user_with_note(
    client, username="planuser", password="secret123", note_title="Daily"
):
    """Helper function to create user and note, returning token and note_id."""
    token = await create_authenticated_user(client, username, password)
    note_id = await create_note(client, token, note_title)
    return token, note_id


# Plan creation tests
@pytest.mark.asyncio
async def test_create_plan(async_client):
    """Test creating a plan for a note."""
    token, note_id = await create_user_with_note(async_client, "createplanuser")

    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Buy groceries", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201
    plan = r.json()
    assert plan["title"] == "Buy groceries"
    assert plan["is_done"] is False
    assert plan["note_id"] == note_id
    assert "id" in plan


@pytest.mark.asyncio
async def test_create_plan_unauthorized(async_client):
    """Test creating a plan without authentication."""
    r = await async_client.post(
        "/notes/1/plans",
        json={"title": "Unauthorized plan", "is_done": False},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_create_plan_nonexistent_note(async_client):
    """Test creating a plan for a non-existent note."""
    token = await create_authenticated_user(async_client, "nonexistentuser")

    r = await async_client.post(
        "/notes/99999/plans",
        json={"title": "Plan for missing note", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]


@pytest.mark.asyncio
async def test_create_plan_other_users_note(async_client):
    """Test creating a plan for another user's note."""
    # Create first user with note
    _, note_id = await create_user_with_note(async_client, "owner", "password123")

    # Create second user
    token2 = await create_authenticated_user(async_client, "intruder", "password123")

    # Try to create plan on first user's note with second user's token
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Intruder plan", "is_done": False},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r.status_code == 404
    assert "Note not found" in r.json()["detail"]


# Plan listing tests
@pytest.mark.asyncio
async def test_list_plans_empty(async_client):
    """Test listing plans when note has no plans."""
    token, note_id = await create_user_with_note(async_client, "emptyplansuser")

    r = await async_client.get(
        f"/notes/{note_id}/plans", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    plans = r.json()
    assert isinstance(plans, list)
    assert len(plans) == 0


@pytest.mark.asyncio
async def test_list_plans_with_content(async_client):
    """Test listing plans when note has plans."""
    token, note_id = await create_user_with_note(async_client, "listplansuser")

    # Create a plan
    await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Test plan", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    # List plans
    r = await async_client.get(
        f"/notes/{note_id}/plans", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    plans = r.json()
    assert isinstance(plans, list)
    assert len(plans) == 1
    assert plans[0]["title"] == "Test plan"


@pytest.mark.asyncio
async def test_list_plans_unauthorized(async_client):
    """Test listing plans without authentication."""
    r = await async_client.get("/notes/1/plans")
    assert r.status_code == 401


# Plan update tests
@pytest.mark.asyncio
async def test_update_plan(async_client):
    """Test updating a plan."""
    token, note_id = await create_user_with_note(async_client, "updateplanuser")

    # Create a plan
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Original title", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]

    # Update the plan
    r = await async_client.put(
        f"/notes/{note_id}/plans/{plan_id}",
        json={"title": "Updated title", "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    updated_plan = r.json()
    assert updated_plan["title"] == "Updated title"
    assert updated_plan["is_done"] is True
    assert updated_plan["id"] == plan_id


@pytest.mark.asyncio
async def test_update_plan_partial(async_client):
    """Test partially updating a plan (only is_done)."""
    token, note_id = await create_user_with_note(async_client, "partialupdateuser")

    # Create a plan
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Keep this title", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]

    # Update only is_done
    r = await async_client.put(
        f"/notes/{note_id}/plans/{plan_id}",
        json={"is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    updated_plan = r.json()
    assert updated_plan["title"] == "Keep this title"  # Title unchanged
    assert updated_plan["is_done"] is True  # Only is_done changed


@pytest.mark.asyncio
async def test_update_nonexistent_plan(async_client):
    """Test updating a non-existent plan."""
    token, note_id = await create_user_with_note(async_client, "updatenonexistentuser")

    r = await async_client.put(
        f"/notes/{note_id}/plans/99999",
        json={"title": "This won't work", "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "Plan not found" in r.json()["detail"]


# Plan deletion tests
@pytest.mark.asyncio
async def test_delete_plan(async_client):
    """Test deleting a plan."""
    token, note_id = await create_user_with_note(async_client, "deleteplanuser")

    # Create a plan
    r = await async_client.post(
        f"/notes/{note_id}/plans",
        json={"title": "Plan to delete", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    plan_id = r.json()["id"]

    # Delete the plan
    r = await async_client.delete(
        f"/notes/{note_id}/plans/{plan_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 204

    # Verify plan is deleted by listing plans
    r = await async_client.get(
        f"/notes/{note_id}/plans", headers={"Authorization": f"Bearer {token}"}
    )
    plans = r.json()
    assert len(plans) == 0


@pytest.mark.asyncio
async def test_delete_nonexistent_plan(async_client):
    """Test deleting a non-existent plan."""
    token, note_id = await create_user_with_note(async_client, "deletenonexistentuser")

    r = await async_client.delete(
        f"/notes/{note_id}/plans/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 404
    assert "Plan not found" in r.json()["detail"]


@pytest.mark.asyncio
async def test_plans_isolation_between_notes(async_client):
    """Test that plans are isolated between different notes."""
    token = await create_authenticated_user(async_client, "isolationuser")

    # Create two notes
    note1_id = await create_note(async_client, token, "Note 1")
    note2_id = await create_note(async_client, token, "Note 2")

    # Create plan for note1
    await async_client.post(
        f"/notes/{note1_id}/plans",
        json={"title": "Plan for note 1", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Create plan for note2
    await async_client.post(
        f"/notes/{note2_id}/plans",
        json={"title": "Plan for note 2", "is_done": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Note1 should only have its plan
    r1 = await async_client.get(
        f"/notes/{note1_id}/plans", headers={"Authorization": f"Bearer {token}"}
    )
    plans1 = r1.json()
    assert len(plans1) == 1
    assert plans1[0]["title"] == "Plan for note 1"

    # Note2 should only have its plan
    r2 = await async_client.get(
        f"/notes/{note2_id}/plans", headers={"Authorization": f"Bearer {token}"}
    )
    plans2 = r2.json()
    assert len(plans2) == 1
    assert plans2[0]["title"] == "Plan for note 2"


@pytest.mark.asyncio
async def test_plans_chronological_order(async_client):
    """Test that plans are returned in chronological order (by created_at)."""
    import asyncio
    
    token, note_id = await create_user_with_note(async_client, "orderuser")

    # Create plans with small delays to ensure different timestamps
    plan_titles = ["First plan", "Second plan", "Third plan", "Fourth plan"]
    created_plan_ids = []
    
    for title in plan_titles:
        r = await async_client.post(
            f"/notes/{note_id}/plans",
            json={"title": title, "is_done": False},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201
        created_plan_ids.append(r.json()["id"])
        await asyncio.sleep(0.01)  # Small delay to ensure different timestamps

    # Get all plans
    r = await async_client.get(
        f"/notes/{note_id}/plans",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    plans = r.json()
    
    # Verify plans are in chronological order
    assert len(plans) == 4
    for i, expected_title in enumerate(plan_titles):
        assert plans[i]["title"] == expected_title, f"Plan at index {i} should be '{expected_title}'"
    
    # Update the second plan (should not change order)
    second_plan_id = created_plan_ids[1]
    r = await async_client.put(
        f"/notes/{note_id}/plans/{second_plan_id}",
        json={"title": "Second plan (updated)", "is_done": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    
    # Get plans again - order should be preserved
    r = await async_client.get(
        f"/notes/{note_id}/plans",
        headers={"Authorization": f"Bearer {token}"},
    )
    plans_after_update = r.json()
    
    # Order should still be by creation time, not update time
    assert plans_after_update[0]["title"] == "First plan"
    assert plans_after_update[1]["title"] == "Second plan (updated)"
    assert plans_after_update[2]["title"] == "Third plan"
    assert plans_after_update[3]["title"] == "Fourth plan"
