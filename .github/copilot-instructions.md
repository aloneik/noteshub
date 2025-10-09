# NoteHub AI Coding Instructions

## Architecture Overview
NoteHub is a FastAPI backend for notes and daily plans with a hierarchical data model: User → Notes → Plans. The app uses async SQLAlchemy 2.0 + PostgreSQL (or SQLite for tests) with OAuth2/JWT authentication.

## Key Structural Patterns

### Import Strategy & Module Resolution
- Use absolute imports with `app.*` prefix (e.g., `from app.db import crud`)
- Local imports within functions prevent circular dependencies: `from app.db.crud import get_user_by_username`
- Tests set `os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"` and add parent dir to sys.path for importability
- PYTHONPATH must include backend/ for local development without Docker

### Database Architecture
- **Base**: `app/db/base.py` - async engine, SessionLocal factory, declarative base
- **Models**: `app/db/models.py` - SQLAlchemy ORM with relationships (User.notes, Note.plans)
- **CRUD**: `app/db/crud.py` - async database operations grouped by entity
- **Schemas**: Pydantic models for request/response validation with Field constraints

### API Routing Pattern
Each API module (`app/api/`) follows this pattern:
- Router with prefix and tags: `router = APIRouter(prefix="/notes", tags=["notes"])`
- Dependency injection for DB sessions and auth: `db: AsyncSession = Depends(get_db)`
- User lookup via token: `username: str = Depends(get_current_username)`
- Resource ownership validation before operations

### Authentication Flow
- Register: JSON body `{"username", "password"}` → hash with bcrypt → store user
- Login: form-encoded `username=...&password=...` → verify → return JWT
- Protected endpoints: `Authorization: Bearer <token>` header → decode → extract username
- Secret key hardcoded as "secret" (not production-ready)

## Development Workflows

### Docker Development
```bash
# From backend/ directory
docker compose up --build
```
- Uses PostgreSQL service on port 5432
- App runs on port 8000 with volume mount for hot reload
- Database initialized on startup via `lifespan` in main.py

### Local Development  
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
$env:PYTHONPATH="$PWD"  # Critical for import resolution
uvicorn app.main:app --reload
```

### Testing
- Tests use SQLite + aiosqlite for speed
- `conftest.py` provides `async_client` fixture with lifespan management
- **Atomic test structure**: Each test function tests one specific behavior
- **Test files organized by functionality**:
  - `test_auth_notes.py`: Authentication and basic note operations
  - `test_notes_crud.py`: Complete CRUD operations for notes
  - `test_plans.py`: Complete CRUD operations for plans
- **Helper functions**: Reusable setup functions (register_user, login_user, create_note)
- **Isolation**: Each test uses unique usernames to avoid conflicts
- **Security testing**: Tests verify user isolation and authorization
- Run: `python -m pytest tests/ -v` (37 atomic tests)

## Project-Specific Conventions

### Error Handling
- Use FastAPI's HTTPException with appropriate status codes
- Resource not found: `HTTP_404_NOT_FOUND`
- Authorization failures: `HTTP_401_UNAUTHORIZED`
- Validation errors: `HTTP_400_BAD_REQUEST`

### Database Sessions
- Async context managers: `async with SessionLocal() as session:`
- Dependency injection via `get_db()` generator
- Always commit after modifications, refresh after updates

### Password Security
- bcrypt has 72-byte limit - truncate long passwords: `password[:72]`
- Apply consistently in both register and login flows
- Use passlib's CryptContext for hashing/verification

### Resource Ownership
Plans API uses nested routes (`/notes/{note_id}/plans`) requiring:
1. Verify user exists via token
2. Verify note belongs to user  
3. Then perform plan operations

## Critical Integration Points
- JWT secret key configuration (currently hardcoded)
- Database URL environment variable handling
- FastAPI lifespan events for schema initialization
- Docker volume mounts and service dependencies