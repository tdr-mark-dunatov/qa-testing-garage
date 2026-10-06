# 📁 Project Structure

**Webhook Pitstop** - Clean, focused structure with no unnecessary dependencies.

## Directory Layout

```
webhook-pitstop/
│
├── apps/
│   ├── api/                    # Python FastAPI Backend
│   │   ├── pyproject.toml      # Poetry dependencies
│   │   ├── Dockerfile          # Container definition
│   │   ├── main.py             # FastAPI app
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── database.py         # DB configuration
│   │   └── README.md           # API documentation
│   │
│   └── web/                    # React Frontend
│       ├── package.json        # npm dependencies
│       ├── Dockerfile          # Multi-stage build
│       ├── nginx.conf          # Nginx proxy config
│       ├── vite.config.js      # Vite configuration
│       ├── tailwind.config.js  # Tailwind CSS
│       └── src/
│           ├── App.jsx         # Main React component
│           ├── main.jsx        # Entry point
│           └── index.css       # Global styles
│
├── docker/
│   └── docker-compose.yml      # Orchestration
│
├── scripts/
│   ├── dev.sh                  # Unix development
│   └── dev.bat                 # Windows development
│
├── README.md                   # Main documentation
├── DEPLOYMENT.md               # Deployment guide
├── POETRY_MIGRATION.md         # Poetry setup guide
└── .gitignore                  # Git ignore rules
```

## Package Managers

### Backend: Poetry 🐍
**Location:** `apps/api/`
- Modern Python dependency management
- Lock file for reproducible builds
- Separation of dev/prod dependencies

```bash
cd apps/api
poetry install              # Install deps
poetry add package-name     # Add new package
poetry run uvicorn main:app # Run app
```

### Frontend: npm 📦
**Location:** `apps/web/`
- Standard JavaScript package manager
- React + Vite ecosystem
- Only place npm is used!

```bash
cd apps/web
npm install           # Install deps
npm run dev           # Dev server
npm run build         # Production build
```

### Root: None! ✨
**No package manager at root level**
- Scripts in `scripts/` handle multi-app dev
- Docker handles containerization
- Clean and simple!

## What We Removed

### ❌ Root package.json
- Was only for `concurrently` to run both apps
- `dev.sh`/`dev.bat` scripts handle this better
- No need for npm workspaces

### ❌ packages/shared/
- Shared constants directory
- Not imported anywhere
- Can add back later if needed

## Development Workflows

### Option 1: Quick Dev Scripts (Recommended)
```bash
# Windows
scripts\dev.bat

# Mac/Linux
./scripts/dev.sh
```

### Option 2: Manual (Full Control)
```bash
# Terminal 1 - Backend
cd apps/api
poetry install
poetry run uvicorn main:app --reload

# Terminal 2 - Frontend
cd apps/web
npm install
npm run dev
```

### Option 3: Docker (Production-like)
```bash
cd docker
docker-compose up --build
```

## Adding New Apps

The `apps/` directory is designed for easy expansion:

```bash
# Example: Add CLI tool
mkdir apps/cli
cd apps/cli
poetry init  # or npm init, or go mod init, etc.
```

Then add to `docker-compose.yml` if you want it containerized.

## Key Files

| File | Purpose |
|------|---------|
| `apps/api/pyproject.toml` | Python dependencies |
| `apps/web/package.json` | Frontend dependencies |
| `docker/docker-compose.yml` | Multi-container orchestration |
| `apps/api/Dockerfile` | Backend container |
| `apps/web/Dockerfile` | Frontend container (multi-stage) |
| `apps/web/nginx.conf` | Reverse proxy config |
| `.gitignore` | Ignore Python + Node artifacts |

## Why This Structure?

✅ **Clear Separation** - Each app is self-contained
✅ **Right Tool for Job** - Poetry for Python, npm for JS
✅ **No Overhead** - No unnecessary root dependencies
✅ **Docker Ready** - Each app builds independently
✅ **Extensible** - Easy to add CLI, mobile, admin apps

## Environment Variables

### Backend (apps/api)
```bash
DATABASE_URL=sqlite:///./data/pitstop.db  # Default
CORS_ALLOW_ALL=true                       # Optional
ALLOWED_ORIGINS=https://example.com       # Optional
```

### Frontend (apps/web)
No env vars needed! Auto-detects from `window.location`

## Port Configuration

| Service | Port | URL |
|---------|------|-----|
| Frontend | 80 | http://localhost |
| Backend | 8000 | http://localhost:8000 |
| Frontend Dev | 5173 | http://localhost:5173 |

## Tech Stack Summary

```
┌─────────────────────────────────────┐
│           FRONTEND                  │
│  React + Vite + Tailwind CSS       │
│  Package Manager: npm               │
│  Port: 5173 (dev) / 80 (prod)      │
└──────────────┬──────────────────────┘
               │
               │ WebSocket + HTTP
               │
┌──────────────▼──────────────────────┐
│           BACKEND                   │
│  FastAPI + SQLAlchemy + WebSockets │
│  Package Manager: Poetry            │
│  Port: 8000                         │
│  Database: SQLite (default)         │
└─────────────────────────────────────┘
```

---

🏁 **Simple, clean, and ready to scale!**
