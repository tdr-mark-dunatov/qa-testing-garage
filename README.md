# 🏁 Webhook Pitstop

**Real-time webhook inspection tool with race-speed diagnostics for QA testing**

Inspect webhooks at lightning speed with a racing-themed UI. Built for automotive QA teams who need to capture, analyze, and debug webhook integrations.

## Project Structure

```
webhook-pitstop/
├── apps/
│   ├── api/          FastAPI backend (Poetry)
│   └── web/          React + Vite frontend (npm)
├── docker/
│   └── docker-compose.yml
└── scripts/
    ├── dev.sh        Development script (Unix)
    └── dev.bat       Development script (Windows)
```

## Features

- 🏁 **Real-time Inspection** - See webhook requests as they arrive
- ⚡ **Race-Speed Performance** - WebSocket-powered live updates
- 🔧 **Diagnostic Dashboard** - Lap times, headers, payloads, and more
- 📊 **Performance Metrics** - Track fastest/slowest/average response times
- 🎨 **Racing Theme** - Car-themed UI for automotive companies
- 🐳 **Docker Ready** - One command deployment
- 📦 **Multi-App Ready** - Clean structure to add CLI, mobile, admin apps

## Quick Start

### Option 1: Quick Dev (Recommended for Hackathon)

**Windows:**
```bash
scripts\dev.bat
```

**Mac/Linux:**
```bash
./scripts/dev.sh
```

Access: http://localhost:5173

### Option 2: Manual Development

**Terminal 1 - API:**
```bash
cd apps/api
poetry install
poetry run uvicorn main:app --reload
```

**Terminal 2 - Web:**
```bash
cd apps/web
npm install
npm run dev
```

### Option 3: Docker

```bash
cd docker
docker-compose up --build
```

Access: http://localhost

## How It Works

1. **Open Pit Lane** - Generate a unique webhook URL
2. **Send Requests** - Send HTTP requests to your pit lane URL
3. **Watch Real-time** - See requests appear instantly via WebSocket
4. **Inspect Details** - Click any request to view headers, body, timing

## Use Cases

### QA Testing
- Test lender integrations (HMF, TDC, RBC external communications)
- Debug webhook delivery issues
- Capture exact payloads for test fixtures

### Development
- Develop against third-party webhooks locally
- No VPN/staging environment needed
- Share webhook URLs with external vendors

### Troubleshooting
- Reproduce production issues
- Compare working vs broken payloads
- Identify timing/latency problems

## Applications

### `apps/api` - FastAPI Backend
- WebSocket server for real-time updates
- SQLite/PostgreSQL support
- REST API with auto-generated docs
- Poetry for dependency management

### `apps/web` - React Frontend
- Racing-themed UI with Tailwind CSS
- Real-time WebSocket connection
- Responsive design
- Vite for blazing-fast dev server

### Future Apps (Easy to Add!)

The clean `apps/` structure makes it simple to add:

- **CLI Tool** - Watch requests in terminal, export data
- **Mobile App** - React Native for iOS/Android
- **Admin Dashboard** - User management and analytics

## Architecture

```
┌──────────────┐         ┌──────────────┐
│   apps/web   │ ◄─────► │   apps/api   │
│   (React)    │ WebSocket│  (FastAPI)   │
│   + Vite     │  + HTTP  │  + Poetry    │
└──────────────┘         └──────────────┘
```

## Technology Stack

**Backend (apps/api):**
- FastAPI (async Python)
- Poetry (dependency management)
- SQLAlchemy (ORM)
- WebSockets (real-time)
- SQLite/PostgreSQL

**Frontend (apps/web):**
- React + Vite
- Tailwind CSS
- Axios + WebSocket API

**Deployment:**
- Docker + Docker Compose
- Nginx (reverse proxy)
- Multi-stage builds for optimized images

## Configuration

### Environment Variables

```bash
# apps/api/.env
DATABASE_URL=sqlite:///./data/pitstop.db  # SQLite (default)
# or
DATABASE_URL=postgresql://user:pass@localhost:5432/webhooks
```

### Switch to PostgreSQL

Edit `docker/docker-compose.yml`:
```yaml
db:
  image: postgres:15-alpine
  environment:
    - POSTGRES_USER=pitstop
    - POSTGRES_PASSWORD=pitstop123
    - POSTGRES_DB=webhooks

backend:
  environment:
    - DATABASE_URL=postgresql://pitstop:pitstop123@db:5432/webhooks
```

## API Documentation

Once running:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Development Workflow

### Adding a New App

1. Create app directory:
```bash
mkdir apps/your-new-app
cd apps/your-new-app
```

2. Initialize your app (React, CLI, Python, etc.)

3. Add Dockerfile for containerization

4. Update `docker-compose.yml` to include the new service

### Testing

```bash
# API tests
cd apps/api
pytest

# Web tests
cd apps/web
npm test
```

### Building

```bash
# Build frontend
cd apps/web
npm run build

# Build with Docker
cd docker
docker-compose build
```

## Deployment

### Docker (Recommended)

```bash
cd docker
docker-compose up -d
```

### Cloud Providers
- **AWS ECS/Fargate**
- **Azure Container Instances**
- **Google Cloud Run**
- **DigitalOcean App Platform**
- **Railway.app** (easiest!)

## Racing Theme

The entire application uses automotive/racing metaphors:

- **Pit Lane** = Webhook URL
- **Lap Time** = Response time (ms)
- **Engine Type** = HTTP method
- **Diagnostic Report** = Request details
- **Pit Crew** = WebSocket connections
- **Service Bay** = Inspection interface

## Contributing

This is a hackathon project! Contributions welcome:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

## License

MIT License - See LICENSE file

## Built With

❤️ by Mark Dunatov for Hackathon 2024

---

🏁 **Inspect webhooks at race speed!**

**Clean architecture = Easy to scale. Add CLI tools, mobile apps, admin dashboards with the same patterns!**
