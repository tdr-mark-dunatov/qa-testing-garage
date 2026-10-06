# 🏁 Webhook Inspector

**Real-time webhook inspection tool with automatic PII masking**

Part of the [QA Testing Garage](../../README.md) monorepo.

---

## Overview

Webhook Inspector captures and displays HTTP webhooks in real-time with WebSocket-powered updates. Built specifically for QA teams testing partner integrations (BMT, HYN, RBC) where sensitive customer data needs protection.

**Key Problem Solved:** QA tests were using webhook.site, leaving sensitive data (SSN, credit scores, loan amounts) exposed on external servers for 30+ days. Webhook Inspector provides a secure, self-hosted alternative.

---

## Features

### Core
- 🏗️ **Named Receiving Bays** - Reusable webhook URLs (`/bay/hmf-integration`)
- ⚡ **Quick Bays** - Temporary random URLs for one-off testing
- 🔄 **Real-Time Updates** - WebSocket-powered live display
- 📋 **Dashboard** - View all bays with activity stats

### Search & Filter
- 🔍 **Universal Search** - Search body, headers, query params, IP
- 🎯 **Method Filters** - Filter by GET/POST/PUT/DELETE/PATCH
- 📊 **Live Filtering** - Results update as you type

### Export & Replay
- 📤 **Export JSON** - Download webhooks for test fixtures
- 📋 **Copy as cURL** - One-click replay in terminal
- 🔧 **Full Request Details** - Headers, body, timing, source IP

### Security
- 🔒 **Auto PII Masking** - SSN, credit cards, email, phone masked before storage
- 🏠 **Self-Hosted** - No third-party data exposure
- 🗑️ **Immediate Cleanup** - Delete data anytime

### Performance
- ⚡ **Response Tracking** - Millisecond-precision timing
- 📊 **Performance Metrics** - Fastest/slowest/average lap times
- 🎨 **Racing Theme** - Car-themed UI for automotive companies

---

## Quick Start

### Docker (Recommended)
```bash
cd ../../docker
docker-compose up --build
```

Access: **http://localhost:8080**

### Manual Development

**Backend:**
```bash
cd api
poetry install
poetry run uvicorn main:app --reload
```

**Frontend:**
```bash
cd web
npm install
npm run dev
```

---

## Usage

### 1. Create a Receiving Bay

**Named Bay** (reusable):
```bash
POST /api/bay/named
{
  "bay_name": "hmf-integration",
  "description": "HMF lender webhook testing"
}
```

**Quick Bay** (temporary):
```bash
POST /api/bay/quick
```

### 2. Send Webhooks

```bash
curl -X POST http://localhost:8000/bay/hmf-integration \
  -H "Content-Type: application/json" \
  -d '{
    "dealId": "DEAL-001",
    "status": "APPROVED",
    "ssn": "123-45-6789"
  }'
```

### 3. View in UI

Open **http://localhost:8080** - webhook appears instantly with SSN masked: `***-**-6789`

---

## API Endpoints

### Bay Management
- `POST /api/bay/named` - Create named bay
- `POST /api/bay/quick` - Create quick bay  
- `GET /api/bays` - List all bays with stats

### Webhook Capture
- `ANY /bay/{id}` - Receive webhook (all HTTP methods)

### Data Retrieval
- `GET /api/pit/{id}/requests` - Get webhooks (last 50)
- `GET /api/pit/{id}/diagnostics` - Performance metrics
- `DELETE /api/pit/{id}/requests` - Clear webhooks

### System
- `GET /health` - Health check
- `GET /docs` - Swagger API docs
- `WS /ws/{id}` - Real-time WebSocket

---

## Technology Stack

**Backend:**
- FastAPI (Python 3.11+)
- Poetry dependency management
- SQLAlchemy ORM
- SQLite (PostgreSQL-ready)
- WebSockets

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Axios
- Native WebSocket API

**Deployment:**
- Docker + Docker Compose
- Nginx reverse proxy
- Multi-stage builds

---

## Security Features

### PII Masking (Active)

Automatically masks before database storage:

| Data Type | Pattern | Masked Result |
|-----------|---------|---------------|
| SSN | `123-45-6789` | `***-**-6789` |
| Credit Card | `1234-5678-9012-3456` | `****-****-****-3456` |
| Email | `john.doe@example.com` | `j***@example.com` |
| Phone | `(555) 123-4567` | `(***) ***-4567` |

### Production Security Roadmap

For production deployment, see [../../SECURITY_ROADMAP.md](../../SECURITY_ROADMAP.md):
- SSO authentication
- Role-based access control
- Database encryption
- Audit logging
- 9-week implementation plan

---

## Development

### Project Structure

```
webhook-inspector/
├── api/                    # FastAPI backend
│   ├── main.py            # Main application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # DB configuration
│   ├── pyproject.toml     # Poetry dependencies
│   └── Dockerfile
│
└── web/                   # React frontend
    ├── src/
    │   ├── App.jsx        # Main component
    │   └── index.css      # Styles
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── Dockerfile
```

### Adding Features

1. **Backend**: Edit `api/main.py` for new endpoints
2. **Frontend**: Edit `web/src/App.jsx` for UI changes
3. **Database**: Add models in `api/models.py`
4. **Rebuild**: `cd ../../docker && docker-compose up --build`

---

## Testing

### Send Test Webhooks

Use included test scripts:

**Windows:**
```bash
../../test-webhooks.bat
```

**Mac/Linux:**
```bash
../../test-webhooks.sh
```

### With Postman

1. Create bay in UI
2. Copy webhook URL
3. POST to URL with JSON body
4. Watch appear in real-time

---

## Deployment

See [../../DEPLOYMENT.md](../../DEPLOYMENT.md) for:
- AWS Elastic Beanstalk
- Railway.app
- Render.com
- DigitalOcean App Platform

---

## Use Cases

### QA Testing
- Test lender integrations (HMF, TDC, RBC)
- Debug webhook delivery issues
- Capture exact payloads for test fixtures
- Validate partner webhook formats

### Development
- Develop against third-party webhooks locally
- No VPN/staging environment needed
- Share webhook URLs with external vendors

### Troubleshooting
- Reproduce production issues
- Compare working vs broken payloads
- Identify timing/latency problems
- Search by dealId for specific tests

---

## Configuration

### Environment Variables

**Backend (api/.env):**
```bash
DATABASE_URL=sqlite:///./data/pitstop.db
CORS_ALLOW_ALL=true
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Database

**Default**: SQLite at `api/data/pitstop.db`

**PostgreSQL**:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/webhooks
```

---

## Troubleshooting

### WebSocket not connecting
- Check browser console for errors
- Verify deployment supports WebSockets
- Ensure HTTPS → WSS protocol mapping

### CORS errors
- Set `CORS_ALLOW_ALL=true` environment variable
- Or add frontend domain to `ALLOWED_ORIGINS`

### Port conflicts
Edit `../../docker/docker-compose.yml`:
- Backend: `"8001:8000"`
- Frontend: `"8081:80"`

---

## Performance

- **Response Time**: <50ms average (local)
- **WebSocket Latency**: <10ms (local)
- **Frontend Build**: ~5-10 seconds (Vite)
- **Docker Build**: ~2-3 minutes (first time)

---

## License

MIT License - See [../../LICENSE](../../LICENSE)

---

## Part of QA Testing Garage

This tool is part of the **QA Testing Garage** monorepo - a collection of QA tools for automotive teams.

**[← Back to QA Testing Garage](../../README.md)**

---

**Built during Hackathon 2024** 🏆
