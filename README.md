# NoteHub

A FastAPI-based notes and daily plans management application with hierarchical data model.

## Project Structure

```
notehub/
├── .github/                    # GitHub workflows and AI coding instructions
│   └── copilot-instructions.md
├── backend/                    # FastAPI backend application
│   ├── app/                   # Main application code
│   │   ├── api/              # API route handlers
│   │   ├── core/             # Core functionality (security, config)
│   │   └── db/               # Database models and operations
│   ├── tests/                 # Test suite (37 atomic tests)
│   └── docker-compose.yml     # Docker configuration
├── web_frontend/              # React + TypeScript web frontend
│   ├── src/                  # React components and logic
│   │   ├── components/       # UI components
│   │   ├── api/              # API client
│   │   └── store/            # State management (Zustand)
│   └── docker-compose.yml    # Frontend Docker config
├── desktop/                   # Qt desktop application (NEW!)
│   ├── src/                  # Python + PySide6 code
│   │   ├── ui/               # Desktop UI windows
│   │   ├── api/              # API client
│   │   └── models/           # Data models
│   ├── requirements.txt      # Desktop dependencies
│   └── build.py              # Nuitka build script
├── docs/                      # Documentation
└── README.md                  # This file
```

## Tech Stack

### Backend
- **Framework**: FastAPI + Python 3.13
- **Database**: PostgreSQL (production) / SQLite (tests)
- **ORM**: SQLAlchemy 2.0 (async)
- **Authentication**: OAuth2 + JWT
- **Testing**: pytest with 37 atomic tests

### Web Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **State**: Zustand + React Query
- **Styling**: Tailwind CSS
- **Router**: React Router

### Desktop Application (NEW! 🎉)
- **Framework**: PySide6 (Qt for Python)
- **Build**: Nuitka (single executable)
- **Size**: ~20 MB standalone .exe
- **Platforms**: Windows, Linux, macOS

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Tunneling**: Cloudflare (for internet access)
- **CI/CD**: GitHub Actions

## Quick Start

### Backend (FastAPI)
```bash
cd backend
docker compose up --build
# Backend runs on http://localhost:8000
```

### Web Frontend (React)
```bash
cd web_frontend
docker compose up --build
# Frontend runs on http://localhost:5173
```

### Desktop Application (Qt)
```bash
cd desktop
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python src/main.py
```

**See individual README files for detailed instructions:**
- [backend/README.md](backend/README.md) - Backend setup and API docs
- [web_frontend/README.md](web_frontend/README.md) - Web frontend guide
- [desktop/README.md](desktop/README.md) - Desktop app development and building

## API Endpoints

- **Authentication**: /auth/register, /auth/login
- **Notes**: /notes (CRUD operations)  
- **Plans**: /notes/{note_id}/plans (CRUD operations)
- **Documentation**: /docs (Swagger UI)

## Testing

### Backend (Automated)
Run the complete test suite (37 atomic tests):
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend (Manual)
See [MANUAL_TESTING.md](MANUAL_TESTING.md) for complete testing scenarios and checklist.

## Data Model

- **User**  **Notes**  **Plans** (hierarchical structure)
- Full user isolation and authorization
- CRUD operations for all entities

## Deployment

### 🚀 Production Deployment (FREE)

#### Backend: Render.com
- **PostgreSQL database included**
- **Auto-deploy from GitHub**
- See [docs/RENDER_DEPLOY.md](docs/RENDER_DEPLOY.md) for step-by-step guide

```bash
# Generate production SECRET_KEY
cd backend
python generate_secret_key.py
```

#### Frontend: Vercel
- **Zero-config deployment**
- **Global CDN + Auto-HTTPS**
- **Auto-deploy from GitHub**
- See [docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md) or [Quick Start (2 min)](docs/VERCEL_QUICK_START.md)

#### Quick Deploy with Blueprint:
1. Push code to GitHub
2. Connect repository to Render
3. Render auto-detects `render.yaml` and deploys everything
4. Get your API URL: `https://notehub-backend.onrender.com`

**📚 Deployment Documentation:**

**Backend (Render):**
- 🚀 [Quick Deploy (5 min)](docs/QUICK_DEPLOY.md) - Fast start
- 📖 [Full Guide](docs/RENDER_DEPLOY.md) - Detailed instructions
- 🔖 [Quick Reference](docs/RENDER_QUICK_REFERENCE.md) - Commands cheat sheet

**Frontend (Vercel):**
- ⚡ [Quick Start (2 min)](docs/VERCEL_QUICK_START.md) - Super fast deploy
- � [Full Guide](docs/VERCEL_DEPLOY.md) - Complete instructions
- ⚙️ [Configuration](docs/VERCEL_CONFIG.md) - Advanced setup

**General:**
- ✅ [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) - Verification
- 📝 [Complete Summary](docs/RENDER_DEPLOYMENT_COMPLETE.md) - Everything configured

---

## Development

See backend/README.md for detailed development instructions and .github/copilot-instructions.md for AI coding guidelines.

## Git Ignore

The project includes comprehensive .gitignore files:
- **Root .gitignore**: General Python, Docker, IDE, and OS files
- **Backend .gitignore**: FastAPI/backend-specific ignores (test DBs, debug files)

Key ignored items:
- __pycache__/, *.pyc (Python bytecode)
- .env/, .env (Virtual environments and secrets)
- *.db, 	est*.db (Database files)
- .pytest_cache/, .coverage (Test artifacts)
- .vscode/, .idea/ (IDE configurations)
- docker-compose.override.yml (Local Docker overrides)
