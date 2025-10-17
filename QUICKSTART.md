# NoteHub - Quick Start Guide 🚀

## Architecture

NoteHub consists of **two independent services**:
- 🔧 **Backend** - FastAPI + PostgreSQL (port 8000)
- 🌐 **Frontend** - React + Vite (port 5173)

Each service runs separately in its own Docker container.

## Quick Start

### 1️⃣ Start Backend (FastAPI + PostgreSQL)

```bash
cd backend
docker compose up --build
```

**Done!** Backend is available:
- 🔧 API: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs
- 🗄️ PostgreSQL: localhost:5432

### 2️⃣ Start Frontend (React + Vite)

```bash
cd web_frontend
docker compose up --build
```

Or use the script:
```bash
cd web_frontend
.\start.ps1
```

**Done!** Frontend is available:
- 🌐 App: http://localhost:5173

### Container Management

**Backend:**
```bash
cd backend
docker compose logs -f      # Logs
docker compose down          # Stop
docker compose ps            # Status
```

**Frontend:**
```bash
cd web_frontend
docker compose logs -f       # Logs
docker compose down          # Stop
docker compose ps            # Status
```

### Hot Reload ♻️

All code changes are applied automatically:
- ✅ `backend/app/` - backend reloads automatically
- ✅ `web_frontend/src/` - frontend updates instantly

## Docker Structure

```
backend/docker-compose.yml
├── backend    (Python + FastAPI)
└── db         (PostgreSQL)

web_frontend/docker-compose.yml
└── frontend   (Node.js + Vite + React)
```

**Important**: Services are independent and run separately!

## What's Ready ✅

### Backend ✅
- FastAPI with full documentation
- SQLAlchemy async + PostgreSQL  
- OAuth2/JWT authentication
- CRUD for Notes and Plans
- 37 tests (all passing)
- **Docker**: ready to run

### Frontend ✅
- React 18 + TypeScript
- Vite for development
- TailwindCSS configured
- API client with automatic authentication
- Zustand store for state management
- Basic routing
- **Docker**: ready to run
- **package.json**: created with all dependencies

### Infrastructure ✅
- Docker Compose for each service
- Hot reload for development
- PostgreSQL with persistent storage
- Proper CORS configuration
- Quick start scripts

## Next Steps

After running `docker compose up --build`:

1. **Check backend**:
   - Open http://localhost:8000/docs
   - Try `/auth/register` and `/auth/login`

2. **Check frontend**:
   - Open http://localhost:5173
   - You'll see the placeholder page

3. **I can help create**:
   - Login/Register forms
   - Notes list
   - Note editor
   - Daily plans checklist
   - Beautiful UI components

## Troubleshooting

### Port 5173 is busy
```bash
# Docker will automatically try 5174
# Or stop the other process
```

### CORS errors
```bash
# Backend is already configured for localhost:5173
# If using a different port, update backend/app/core/config.py
```

### Container won't start
```bash
# Check logs
docker compose logs

# Rebuild from scratch
docker compose down -v
docker compose up --build
```

## Alternative: Local Development

If you don't want to use Docker:

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH="$PWD"
uvicorn app.main:app --reload
```

### Frontend (requires Node.js v20+)
```bash
cd web_frontend
npm install
npm run dev
```
