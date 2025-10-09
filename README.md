# NoteHub

A FastAPI-based notes and daily plans management application with hierarchical data model.

## Project Structure

`
notehub/
 .github/                    # GitHub workflows and AI coding instructions
    copilot-instructions.md
 .gitignore                 # Main gitignore file
 README.md                  # This file
 backend/                   # FastAPI backend application
     .gitignore            # Backend-specific gitignore
     README.md             # Backend documentation
     requirements.txt      # Python dependencies
     docker-compose.yml    # Docker configuration
     Dockerfile           # Docker image definition
     app/                 # Main application code
        main.py         # FastAPI app initialization
        api/            # API route handlers
        core/           # Core functionality (security, config)
        db/             # Database models and operations
     tests/              # Test suite (37 atomic tests)
         test_auth_notes.py    # Authentication and basic notes
         test_notes_crud.py    # Complete CRUD for notes  
         test_plans.py         # Complete CRUD for plans
`

## Tech Stack

- **Backend**: FastAPI + Python 3.13
- **Database**: PostgreSQL (production) / SQLite (tests)
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: OAuth2 + JWT
- **Testing**: pytest with 37 atomic tests
- **Docker**: Full containerization support

## Quick Start

### Using Docker (Recommended)
`ash
cd backend
docker compose up --build
`

### Local Development
`ash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
$env:PYTHONPATH="$PWD"    # Critical for imports
uvicorn app.main:app --reload
`

## API Endpoints

- **Authentication**: /auth/register, /auth/login
- **Notes**: /notes (CRUD operations)  
- **Plans**: /notes/{note_id}/plans (CRUD operations)
- **Documentation**: /docs (Swagger UI)

## Testing

Run the complete test suite (37 atomic tests):
`ash
cd backend
python -m pytest tests/ -v
`

## Data Model

- **User**  **Notes**  **Plans** (hierarchical structure)
- Full user isolation and authorization
- CRUD operations for all entities

## Development

See ackend/README.md for detailed development instructions and .github/copilot-instructions.md for AI coding guidelines.

## Git Ignore

The project includes comprehensive .gitignore files:
- **Root .gitignore**: General Python, Docker, IDE, and OS files
- **Backend .gitignore**: FastAPI/backend-specific ignores (test DBs, debug files)

Key ignored items:
- __pycache__/, *.pyc (Python bytecode)
- env/, .env (Virtual environments and secrets)
- *.db, 	est*.db (Database files)
- .pytest_cache/, .coverage (Test artifacts)
- .vscode/, .idea/ (IDE configurations)
- docker-compose.override.yml (Local Docker overrides)
