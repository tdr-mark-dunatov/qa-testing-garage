# 🏎️ QA Testing Garage

**A monorepo of QA testing tools for automotive teams**

Collection of internal tools built to solve real QA testing problems - webhook inspection, API mocking, test data generation, and more.

---

## 🛠️ Tools in the Garage

### 🏁 [Webhook Inspector](./apps/webhook-inspector/) - **LIVE**

Real-time webhook testing with automatic PII masking.

**Features:**
- Named & quick receiving bays
- Real-time WebSocket updates
- Search & filter webhooks
- Export as JSON / Copy as cURL
- Automatic PII masking (SSN, credit cards, email, phone)
- Racing-themed dashboard

**Built for:** Testing partner webhooks (BMT, HYN, RBC) without exposing sensitive data

**[→ View Webhook Inspector Docs](./apps/webhook-inspector/README.md)**

---

### 🚧 API Mocker - **COMING SOON**

Mock API responses for testing without backend dependencies.

**Planned Features:**
- Define API endpoints with custom responses
- Latency simulation
- Error scenarios
- Response templating

---

### 🚧 Test Data Factory - **COMING SOON**

Generate realistic test data for automotive deals.

**Planned Features:**
- Customer profiles (with fake PII)
- Vehicle data (VIN, make, model)
- Deal structures
- Export as JSON/CSV/SQL

---

### 🚧 Contract Validator - **COMING SOON**

Validate API contracts between services.

**Planned Features:**
- OpenAPI spec validation
- Request/response schema checking
- Breaking change detection

---

## 🏗️ Monorepo Structure

```
qa-testing-garage/
├── apps/
│   ├── webhook-inspector/    # Webhook testing tool
│   │   ├── api/              # FastAPI backend
│   │   └── web/              # React frontend
│   │
│   ├── portal/               # Landing page (coming soon)
│   ├── api-mocker/           # Future tool
│   └── test-data-factory/    # Future tool
│
├── packages/
│   ├── shared-ui/            # Shared React components
│   └── types/                # Shared TypeScript types
│
├── docker/
│   └── docker-compose.yml    # All services
│
└── docs/
    ├── TOOLS.md              # Tool catalog
    ├── SECURITY.md           # Security guidelines
    └── CONTRIBUTING.md       # How to add tools
```

---

## 🚀 Quick Start

### Run Webhook Inspector

**Docker (Easiest):**
```bash
cd docker
docker-compose up --build
```

Access at **http://localhost:8080**

**Manual Development:**
```bash
# Backend
cd apps/webhook-inspector/api
poetry install
poetry run uvicorn main:app --reload

# Frontend
cd apps/webhook-inspector/web
npm install
npm run dev
```

---

## 📚 Documentation

- **[Webhook Inspector](./apps/webhook-inspector/README.md)** - Full docs for webhook tool
- **[Security Roadmap](./SECURITY_ROADMAP.md)** - Production security plan
- **[Pitch Document](./PITCH.md)** - QA team value proposition
- **[Tech Stack](./TECH_STACK.md)** - Technologies used
- **[Deployment Guide](./DEPLOYMENT.md)** - AWS/Railway deployment

---

## 🎯 Why a Monorepo?

**Benefits:**
- ✅ **Shared Components** - Reuse UI, auth, utilities across tools
- ✅ **Consistent Branding** - Same look and feel
- ✅ **Easier Development** - One repo, one workflow
- ✅ **Cross-Tool Features** - Tools can integrate with each other
- ✅ **Single Deployment** - Docker Compose orchestrates all services

---

## 🔒 Security

All tools follow these principles:
- **PII Masking** - Sensitive data masked before storage
- **Self-Hosted** - No third-party data exposure
- **Audit Ready** - Logs and access controls
- **Network Isolation** - Deploy on internal networks

See [SECURITY_ROADMAP.md](./SECURITY_ROADMAP.md) for production security requirements.

---

## 🏆 Built For

**AutoScout24 QA Team** - Solving real testing problems:

### The Problem:
Our QA tests for partner integrations were using webhook.site, leaving sensitive customer data (SSN, credit scores, loan amounts) exposed on external servers for 30+ days with no cleanup.

### The Solution:
Self-hosted testing tools with:
- Full data control
- Automatic PII protection
- Immediate cleanup
- Custom QA workflows

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11+** with **FastAPI**
- **Poetry** for dependency management
- **SQLAlchemy** ORM with SQLite/PostgreSQL
- **WebSockets** for real-time updates

### Frontend
- **React 18** with **Vite**
- **Tailwind CSS** for styling
- **Axios** for HTTP requests

### Infrastructure
- **Docker** & **Docker Compose**
- **Nginx** reverse proxy
- **AWS** / **Railway** deployment ready

---

## 📊 Project Status

| Tool | Status | Version | Last Updated |
|------|--------|---------|--------------|
| Webhook Inspector | ✅ Live | 1.0.0 | 2024-10-06 |
| Portal | 🚧 Planned | - | - |
| API Mocker | 🚧 Planned | - | - |
| Test Data Factory | 🚧 Planned | - | - |

---

## 🤝 Contributing

Want to add a new tool?

1. Create directory in `apps/your-tool/`
2. Build with any tech stack (FastAPI, React, CLI, etc.)
3. Add Dockerfile for containerization
4. Update `docker-compose.yml`
5. Add docs to `apps/your-tool/README.md`

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) (coming soon)

---

## 📝 License

MIT License - See [LICENSE](./LICENSE)

---

## 🎬 Hackathon Origin

Built during **Hackathon 2024** in response to the "Test Data Compliance Guardian" idea:

> "Teams use webhook.site, request bins, mock APIs... Sensitive payloads can remain exposed after tests complete."

We discovered this was a REAL problem in our Playwright tests. So we built the solution!

---

## 🏁 The Vision

**QA Testing Garage = One-stop shop for all QA testing tools**

Instead of cobbling together external services (webhook.site, mocky.io, faker.js, etc.), we build our own:
- ✅ **Secure** - Self-hosted, PII-protected
- ✅ **Integrated** - Tools work together
- ✅ **Custom** - Built for our workflows
- ✅ **Compliant** - Audit trails, access control

**Future:** Add API mockers, test data generators, contract validators, performance monitors, and more!

---

**Built with ❤️ by the QA Team**

🏎️ **Test at race speed!**
