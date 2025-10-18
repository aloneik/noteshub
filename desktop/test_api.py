"""Quick test script to verify API client works."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from api.client import NoteHubClient, APIError


def test_connection(backend_url: str = "http://localhost:8000"):
    """Test connection to backend."""
    print(f"🔌 Testing connection to {backend_url}")

    client = NoteHubClient(backend_url)

    try:
        # Try to access a public endpoint (should return 401 without auth)
        import requests
        response = requests.get(f"{backend_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is reachable!")
            print(f"   Swagger docs available at: {backend_url}/docs")
            return True
        else:
            print(f"⚠️  Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print(f"   Make sure backend is running: cd ../backend && docker compose up")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_registration(backend_url: str = "http://localhost:8000"):
    """Test user registration."""
    print("\n📝 Testing registration...")

    client = NoteHubClient(backend_url)

    try:
        import random
        username = f"testuser_{random.randint(1000, 9999)}"
        password = "test123456"

        user = client.register(username, password)
        print(f"✅ Registration successful!")
        print(f"   Username: {user.username}")
        print(f"   User ID: {user.id}")
        return user, password
    except APIError as e:
        print(f"❌ Registration failed: {e.message}")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None


def test_login(backend_url: str, username: str, password: str):
    """Test user login."""
    print("\n🔐 Testing login...")
    
    client = NoteHubClient(backend_url)
    
    try:
        token = client.login(username, password)
        print(f"✅ Login successful!")
        print(f"   Token: {token[:20]}...")
        return client
    except APIError as e:
        print(f"❌ Login failed: {e.message}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_notes(client: NoteHubClient):
    """Test notes operations."""
    print("\n📝 Testing notes...")
    
    try:
        # Create note
        note = client.create_note("Test Note", "This is a test note")
        print(f"✅ Created note: {note.title} (ID: {note.id})")
        
        # Get all notes
        notes = client.get_notes()
        print(f"✅ Retrieved {len(notes)} note(s)")
        
        # Update note
        updated = client.update_note(note.id, title="Updated Test Note")
        print(f"✅ Updated note: {updated.title}")
        
        # Delete note
        client.delete_note(note.id)
        print(f"✅ Deleted note")
        
        return True
    except APIError as e:
        print(f"❌ Notes test failed: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 NoteHub Desktop - API Client Test\n")
    
    backend_url = "http://localhost:8000"
    
    # Test 1: Connection
    if not test_connection(backend_url):
        print("\n⚠️  Backend is not running. Tests cannot continue.")
        print("\nTo start backend:")
        print("  cd ../backend")
        print("  docker compose up -d")
        return
    
    # Test 2: Registration
    user, password = test_registration(backend_url)
    if not user:
        print("\n❌ Registration test failed")
        return
    
    # Test 3: Login
    client = test_login(backend_url, user.username, password)
    if not client:
        print("\n❌ Login test failed")
        return
    
    # Test 4: Notes
    test_notes(client)
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()
