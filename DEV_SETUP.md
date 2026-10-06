# 🚀 Developer Setup - Get Running in 5 Minutes

**Test Data Compliance Guardian - Hackathon Project**

---

## ⚡ Fastest Way to Start (Recommended)

### Prerequisites
- **Docker Desktop** installed and running
- That's it!

### Start Everything
```bash
# 1. Clone the repo
git clone https://github.com/tdr-dealertrack/qa-testing-garage.git
cd qa-testing-garage

# 2. Checkout develop branch
git checkout develop

# 3. Start all services (PostgreSQL + Backend + Frontend)
cd docker
docker-compose up --build

# Wait ~2 minutes for build to complete
```

### Access the App
- 🌐 **Frontend**: http://localhost:8080
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

### Test It Works
```bash
# Send a test webhook
curl -X POST http://localhost:8000/bay/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from dev setup!"}'

# Open http://localhost:8080 and view the webhook
```

**✅ If you see the webhook in the UI, you're ready to develop!**

---

## 🎯 VS Code Users (Even Easier)

### One-Click Start

1. Open the project in VS Code
2. Press `Ctrl+Shift+B` (Windows) or `Cmd+Shift+B` (Mac)
3. Select: **"🐳 Start All (Docker)"**
4. Done! App is running at http://localhost:8080

### Available VS Code Tasks
- **🐳 Start All (Docker)** - Starts everything
- **🛑 Stop Docker** - Stops all containers
- **🔧 Backend (Poetry)** - Run backend only (manual dev)
- **🎨 Frontend (npm)** - Run frontend only (manual dev)
- **🧪 Test Webhook (Basic)** - Send test webhook
- **🚨 Test Webhook (With PII)** - Test PII detection

Press `Ctrl+Shift+P` → "Tasks: Run Task" to see all

---

## 🛠️ Manual Development (Without Docker)

**Only needed if you want to develop without Docker**

### Backend Setup
```bash
cd apps/webhook-inspector/api

# Install Poetry (if not installed)
pip install poetry

# Install dependencies
poetry install

# Run backend
poetry run uvicorn main:app --reload

# Backend running at: http://localhost:8000
```

### Frontend Setup (separate terminal)
```bash
cd apps/webhook-inspector/web

# Install dependencies
npm install

# Run frontend
npm run dev

# Frontend running at: http://localhost:5173
```

**Note:** Manual dev uses SQLite by default (no PostgreSQL needed)

---

## 🧪 Running Tests

### Backend Tests
```bash
cd apps/webhook-inspector/api

# Run all tests
poetry run pytest

# Run only unit tests (fast)
poetry run pytest -m unit

# Run with coverage
poetry run pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### Test Markers
- `pytest -m unit` - Unit tests only
- `pytest -m integration` - Integration tests
- `pytest -m compliance` - Compliance feature tests

---

## 🔍 Verifying Everything Works

### 1. Check Containers Running
```bash
docker ps

# Should see 3 containers:
# - compliance-guardian-db (PostgreSQL)
# - compliance-guardian-backend (FastAPI)
# - compliance-guardian-frontend (React)
```

### 2. Check Backend Health
```bash
curl http://localhost:8000/health

# Should return: {"status": "🏁 Ready to race!", "engine": "running"}
```

### 3. Check Database Connection
```bash
docker logs compliance-guardian-backend

# Should see "Connected to database" or similar (no errors)
```

### 4. Create a Bay
```bash
curl -X POST http://localhost:8000/api/bay/named \
  -H "Content-Type: application/json" \
  -d '{"bay_name": "dev-test", "description": "Testing setup"}'

# Should return bay details with URL
```

### 5. Send Webhook
```bash
curl -X POST http://localhost:8000/bay/dev-test \
  -H "Content-Type: application/json" \
  -d '{"test": "data", "timestamp": "2024-10-06T12:00:00Z"}'

# Open http://localhost:8080 and see the webhook
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Stop all containers
docker-compose down

# Check what's using port 8080
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Mac/Linux

# Kill the process or change ports in docker-compose.yml
```

### Docker Build Fails
```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Backend Won't Connect to PostgreSQL
```bash
# Check PostgreSQL is healthy
docker logs compliance-guardian-db

# Wait for: "database system is ready to accept connections"

# Backend waits for health check, so give it 30 seconds
```

### Frontend Shows "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:8000/health

# If backend is down, check logs
docker logs compliance-guardian-backend

# Common issue: PostgreSQL not ready yet, wait 30 seconds
```

### Tests Fail with "Module not found"
```bash
cd apps/webhook-inspector/api
poetry install  # Re-install dependencies
poetry run pytest
```

---

## 📁 Project Structure (What's Where)

```
qa-testing-garage/
├── apps/
│   └── webhook-inspector/
│       ├── api/              ← Backend (FastAPI + Python)
│       │   ├── main.py       ← Main API routes
│       │   ├── models.py     ← Database models
│       │   ├── tests/        ← Test suite
│       │   └── pyproject.toml
│       └── web/              ← Frontend (React + Vite)
│           └── src/
│               └── App.jsx   ← Main UI component
│
├── docker/
│   └── docker-compose.yml    ← All services definition
│
├── .github/workflows/        ← CI/CD
├── .vscode/                  ← VS Code tasks
│
├── HACKATHON.md              ← Hackathon pitch
├── IMPLEMENTATION_ROADMAP.md ← Development plan
├── TEAM_HANDOFF.md           ← Getting started guide
└── DEV_SETUP.md              ← This file
```

---

## 🎯 What to Work On

See **[IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)** for:
- Phase 1: PII Detection (2-3 hours)
- Phase 2: Ownership Tracking (3-4 hours)
- Phase 3: Compliance Dashboard (4-5 hours)

See **[TEAM_HANDOFF.md](./TEAM_HANDOFF.md)** for role assignments.

---

## 📚 Useful Links

**Documentation:**
- [Hackathon Pitch](./HACKATHON.md)
- [Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)
- [Quick Start](./QUICK_START.md)
- [Team Handoff](./TEAM_HANDOFF.md)

**API:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Code Locations:**
- Backend compliance spec: `apps/webhook-inspector/api/COMPLIANCE_FEATURES.md`
- Frontend compliance spec: `apps/webhook-inspector/web/COMPLIANCE_UI.md`
- Demo script: `apps/webhook-inspector/DEMO_SCRIPT.md`

---

## 🆘 Getting Help

**Common Issues:**
1. **Port conflicts** - Change ports in `docker-compose.yml`
2. **Docker not running** - Start Docker Desktop
3. **Build failures** - Run `docker system prune -a` and retry
4. **Database not ready** - Wait 30 seconds after `docker-compose up`

**Check Logs:**
```bash
docker logs compliance-guardian-backend    # Backend logs
docker logs compliance-guardian-frontend   # Frontend logs
docker logs compliance-guardian-db         # Database logs
```

**Still stuck?**
- Check `TEAM_HANDOFF.md` for detailed troubleshooting
- Ask in team Slack: #hackathon-compliance-guardian

---

## ✅ Quick Checklist

Before you start developing:

- [ ] Docker Desktop running
- [ ] Ran `docker-compose up --build`
- [ ] Can access http://localhost:8080
- [ ] Can access http://localhost:8000/docs
- [ ] Created a test bay successfully
- [ ] Sent a test webhook successfully
- [ ] Read `IMPLEMENTATION_ROADMAP.md`
- [ ] Know which phase you're working on

**All checked? You're ready to build! 🚀**

---

## 🏁 First Task Suggestions

**Easy warm-up tasks:**
1. Run the test suite: `cd apps/webhook-inspector/api && poetry run pytest`
2. Add your name to `TEAM_HANDOFF.md`
3. Create a test bay and send webhooks via Swagger UI
4. Read the compliance feature specs in `api/COMPLIANCE_FEATURES.md`

**Ready to code? Pick a phase:**
- **Phase 1**: Create `pii_detector.py` module
- **Phase 2**: Add owner fields to bay creation
- **Phase 3**: Build compliance dashboard

See `IMPLEMENTATION_ROADMAP.md` for detailed tasks!
