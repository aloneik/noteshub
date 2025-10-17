# Web Frontend Setup Guide

## Prerequisites

### 1. Install Node.js

Download and install Node.js LTS (v20 or later) from: https://nodejs.org/

After installation, verify:
```bash
node --version  # Should show v20.x.x or later
npm --version   # Should show 10.x.x or later
```

## Quick Start

### Step 1: Initialize Project

```bash
cd web_frontend
npm create vite@latest . -- --template react-ts
```

When prompted:
- Current directory is not empty. Remove existing files and continue? → **Yes**
- Package name: → **notehub-web** (or press Enter for default)

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Install Additional Packages

```bash
# UI Framework
npm install @headlessui/react @heroicons/react

# State Management & API
npm install @tanstack/react-query axios zustand

# Routing
npm install react-router-dom

# Forms & Validation
npm install react-hook-form zod @hookform/resolvers

# Utilities
npm install clsx tailwind-merge date-fns

# Development
npm install -D @types/node
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 4: Start Development Server

```bash
npm run dev
```

The app will be available at: `http://localhost:5173`

## Project Structure (After Setup)

```
web_frontend/
├── public/              # Static assets
├── src/
│   ├── api/            # API client and endpoints
│   ├── components/     # Reusable components
│   │   ├── auth/      # Authentication components
│   │   ├── notes/     # Notes components
│   │   └── ui/        # UI primitives
│   ├── hooks/         # Custom React hooks
│   ├── pages/         # Page components
│   ├── store/         # Zustand state management
│   ├── types/         # TypeScript types
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Main app component
│   ├── main.tsx       # Entry point
│   └── index.css      # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Backend Connection

The frontend is configured to connect to the backend API at:
- Development: `http://localhost:8000`
- Production: Set `VITE_API_URL` environment variable

CORS is already configured in the backend for:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React default)

## Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Next Steps

After Node.js installation and project setup:
1. Review the generated project structure
2. I'll help you create the components and API integration
3. We'll build the authentication system
4. Then implement notes and plans features

## Troubleshooting

### Port already in use
If port 5173 is busy, Vite will automatically use 5174.

### Backend not accessible
Make sure the FastAPI backend is running:
```bash
cd ../backend
uvicorn app.main:app --reload
```

### CORS errors
Verify backend is running and check `backend/app/main.py` CORS settings.
