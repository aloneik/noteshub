# NoteHub Web Frontend

Modern React + TypeScript frontend for NoteHub notes and daily plans application.

## 🚀 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form + Zod** - Form handling and validation
- **Axios** - HTTP client
- **Heroicons** - Icon library

## 📋 Prerequisites

1. **Node.js** (v20 or later)
   - Download from: https://nodejs.org/
   - Verify installation:
     ```bash
     node --version
     npm --version
     ```

2. **Backend Running**
   - The FastAPI backend must be running on `http://localhost:8000`
   - See `../backend/README.md` for setup instructions

## 🛠️ Setup Instructions

### Option 1: Docker (Recommended - No Node.js Installation Required)

**Prerequisites**: Only Docker Desktop

#### Quick Start

```bash
# Use the startup script
.\start.ps1
```

Or manually:

```bash
docker compose up --build
```

Visit: **http://localhost:5173** 🌐

**Note**: Backend должен быть запущен отдельно на http://localhost:8000
(Смотри `../backend/README.md` для инструкций)

**Hot Reload**: All changes in `src/` will automatically reload! ♻️

**Управление контейнерами**:
```bash
# View logs
docker compose logs -f frontend

# Stop service
docker compose down

# Rebuild after dependency changes
docker compose up --build --force-recreate
```

### Option 2: Local Development (Requires Node.js)

**Prerequisites**: Node.js v20+

#### 1. Install Node.js

If you don't have Node.js installed:
1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer
4. Verify installation: `node --version`

#### 2. Install Dependencies

```bash
npm install
```

#### 3. Configure Environment Variables

Create `.env` file (already exists):
```env
VITE_API_URL=http://localhost:8000
```

#### 4. Start Development Server

```bash
npm run dev
```

Visit: `http://localhost:5173`

## 📁 Project Structure

```
web_frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   │   ├── client.ts  # Axios config & interceptors
│   │   ├── auth.ts    # Authentication API
│   │   ├── notes.ts   # Notes API
│   │   └── plans.ts   # Plans API
│   ├── components/     # React components
│   │   ├── auth/      # Login, Register
│   │   ├── notes/     # Note list, Note editor
│   │   ├── plans/     # Plan list, Plan item
│   │   ├── layout/    # Header, Footer, Sidebar
│   │   └── ui/        # Button, Input, Modal, etc.
│   ├── hooks/         # Custom React hooks
│   ├── pages/         # Page components
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── NotePage.tsx
│   ├── store/         # Zustand stores
│   │   └── authStore.ts
│   ├── types/         # TypeScript types
│   │   └── index.ts   # API types
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Main app with routing
│   ├── main.tsx       # Entry point
│   └── index.css      # Global styles
├── .env               # Environment variables
├── index.html         # HTML template
├── package.json       # Dependencies
├── tsconfig.json      # TypeScript config
├── vite.config.ts     # Vite config
├── tailwind.config.js # Tailwind config
└── README.md          # This file
```

## ✨ Features

### Already Implemented (Files Created)

✅ **Type Definitions** (`src/types/index.ts`)
- User, Note, Plan interfaces
- Request/Response types matching backend schemas
- Auth state types

✅ **API Client** (`src/api/client.ts`)
- Axios instance with base URL
- Auth token interceptor
- Error handling
- 401 auto-redirect to login

✅ **API Endpoints**
- `src/api/auth.ts` - Login, Register
- `src/api/notes.ts` - CRUD operations for notes
- `src/api/plans.ts` - CRUD operations for plans

✅ **State Management** (`src/store/authStore.ts`)
- Zustand store for authentication
- Persistent storage (localStorage)
- Login, Register, Logout actions

### To Be Implemented

🔲 **Components**
- Authentication forms (Login, Register)
- Notes list and editor
- Plans checklist
- Layout components (Header, Sidebar)
- UI primitives (Button, Input, Modal)

🔲 **Pages**
- Login page
- Register page
- Dashboard (notes list)
- Note detail page (with plans)

🔲 **Routing**
- Protected routes
- Public routes
- Navigation

🔲 **Styling**
- Tailwind utility classes
- Responsive design
- Dark mode (optional)

## 🔌 API Integration

The frontend is configured to work with the NoteHub FastAPI backend:

### Base URL
- Development: `http://localhost:8000`
- Production: Set via `VITE_API_URL` environment variable

### Authentication
- Login: `POST /auth/login` (form-data, OAuth2)
- Register: `POST /auth/register` (JSON)
- Token stored in localStorage
- Auto-attached to requests via interceptor

### Notes
- List: `GET /notes`
- Create: `POST /notes`
- Update: `PUT /notes/{id}`
- Delete: `DELETE /notes/{id}`

### Plans
- List: `GET /notes/{note_id}/plans`
- Create: `POST /notes/{note_id}/plans`
- Update: `PUT /notes/{note_id}/plans/{plan_id}`
- Delete: `DELETE /notes/{note_id}/plans/{plan_id}`

## 🧪 Testing

```bash
# Lint
npm run lint

# Type check
npx tsc --noEmit

# Build
npm run build

# Preview production build
npm run preview
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates optimized files in `dist/` directory.

### Environment Variables

Set production API URL:
```env
VITE_API_URL=https://api.notehub.com
```

### Hosting Options

- **Vercel**: `vercel deploy`
- **Netlify**: `netlify deploy`
- **GitHub Pages**: Use `vite-plugin-gh-pages`
- **Docker**: See `Dockerfile` (to be created)

## 📝 Next Steps

After Node.js installation:

1. **Run setup commands** (steps 2-7 above)
2. **Start backend**: `cd ../backend && uvicorn app.main:app --reload`
3. **Start frontend**: `npm run dev`
4. **I'll help you create**:
   - UI components
   - Pages and routing
   - Styling with Tailwind
   - Form validation
   - Error handling

## 🐛 Troubleshooting

### Port 5173 already in use
Vite will automatically try port 5174.

### CORS errors
Ensure backend is running and has CORS configured (already done).

### Type errors
Wait for `npm install` to complete before checking types.

### Backend connection failed
Check:
1. Backend is running: `http://localhost:8000/docs`
2. `.env` file has correct API URL
3. CORS is configured in backend

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://github.com/pmndrs/zustand)

---

**Ready to build! Install Node.js and run the setup commands above.** 🚀
