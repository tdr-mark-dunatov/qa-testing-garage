# 🏎️ Test Data Compliance Guardian

**Compliance-aware testing platform with automatic PII detection**

Self-hosted testing tools that protect sensitive data with automatic PII scanning, ownership tracking, and real-time compliance alerts. Built for teams that can't afford data leaks in their testing workflows.

---

## 🚀 Quick Start for Developers

**Get running in 5 minutes:**

```bash
# 1. Start everything (PostgreSQL + Backend + Frontend)
cd docker
docker-compose up --build

# 2. Open your browser
http://localhost:8080
```

**That's it!** 

👉 **See [DEV_SETUP.md](./DEV_SETUP.md) for complete setup guide**

---

## 🛠️ Tools in the Garage

### 🏁 [Webhook Inspector](./apps/webhook-inspector/) - **LIVE**

Real-time webhook testing with **automatic PII detection and compliance alerts**.

**Core Compliance Features:**
- 🚨 **Automatic PII Detection** - Scans for SSN, SIN, credit scores, emails, phone numbers
- 📢 **Slack Alerts** - Real-time notifications when sensitive data detected
- 👥 **Ownership Tracking** - Know who/what/when for every endpoint
- 📊 **Compliance Dashboard** - See all data exposure at a glance
- ⏰ **Auto-Expiration** - Configurable data retention policies

**Testing Features:**
- Named & quick receiving bays
- Real-time WebSocket updates
- Search & filter webhooks
- Export as JSON / Copy as cURL
- PII masking for display
- Racing-themed dashboard

**Built for:** Testing partner webhooks (BMT, HYN, RBC) while **maintaining compliance**

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

## 🔒 Security & Compliance

All tools follow these principles:

### Automatic Protection
- **PII Detection** - Automatic scanning for SSN, SIN, credit scores, emails, phone
- **Real-time Alerts** - Slack notifications when sensitive data detected
- **PII Masking** - Display-level masking for sensitive data
- **Auto-Expiration** - Configurable data retention policies

### Accountability
- **Ownership Tracking** - Know who created every endpoint
- **Audit Trail** - Full compliance logs
- **Team Attribution** - Track by team/repo/pipeline

### Infrastructure
- **Self-Hosted** - No third-party data exposure
- **Network Isolation** - Deploy on internal networks
- **Access Controls** - Role-based permissions

See [SECURITY_ROADMAP.md](./SECURITY_ROADMAP.md) for production security requirements.

---

## 🏆 The Discovery

**We found a compliance risk in our own tests.**

### The Problem:
Our QA tests for partner integrations were using webhook.site, leaving sensitive customer data (SSN, credit scores, loan amounts) exposed on external servers for 30+ days. 

**This wasn't just a webhook problem** - it affects ANY team using temporary endpoints (RequestBin, mock APIs, etc.)

### The Solution:
**Test Data Compliance Guardian** - A platform that:
- ✅ **Detects PII automatically** (SSN, SIN, credit scores, emails, phone)
- ✅ **Sends Slack alerts** when sensitive data found
- ✅ **Tracks ownership** (team/repo/pipeline/user)
- ✅ **Compliance dashboard** for visibility
- ✅ **Full data control** (self-hosted)
- ✅ **Immediate cleanup** when tests complete
- ✅ **Audit trail** for compliance

**Not just for QA. A platform tool for every team.**

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
| Webhook Inspector (with PII detection) | ✅ Live | 1.0.0 | 2024-10-06 |
| Slack Alerts | 🚧 In Progress | 0.1.0 | 2024-10-06 |
| Compliance Dashboard | 🚧 In Progress | 0.1.0 | 2024-10-06 |
| Ownership Tracking | 🚧 Planned | - | - |
| Portal | 🚧 Planned | - | - |
| API Mocker (with compliance) | 🚧 Planned | - | - |
| Test Data Factory (PII-safe) | 🚧 Planned | - | - |

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

Built during **Hackathon 2024** to solve a real compliance risk:

### The Original Idea:
> "Build a service that registers temporary webhook endpoints, tracks ownership, scans payloads for PII, and sends alerts when sensitive data is detected."

### What We Discovered:
While testing, we found our own Playwright tests were leaving sensitive customer data (SSN, credit scores, loan amounts) on webhook.site for 30+ days with no cleanup.

### What We Built:
A production-ready compliance platform that:
- Automatically detects PII in real-time
- Sends Slack alerts immediately
- Tracks ownership for full accountability
- Provides compliance dashboard
- Replaces external services like webhook.site

**Not just a hackathon project. A real solution to a real problem.**

---

## 🏁 The Vision

**Test Data Compliance Guardian = Compliance layer for ALL testing tools**

Instead of cobbling together external services without compliance:
- ❌ webhook.site (no PII detection)
- ❌ RequestBin (no ownership tracking)
- ❌ mocky.io (no alerts)
- ❌ faker.js (generates real-looking PII)

We build a **compliance-first platform**:
- ✅ **Automatic PII Detection** - Scans everything
- ✅ **Real-time Alerts** - Slack notifications
- ✅ **Ownership Tracking** - Full accountability
- ✅ **Compliance Dashboard** - Visibility for all
- ✅ **Self-Hosted** - Complete control
- ✅ **Audit Ready** - Full compliance logs

**Future:** Expand to API mockers, test data generators, contract validators - all with built-in compliance.

🏁 **Test at race speed, compliance guaranteed!**

---

## 👥 Hackathon Team

**Project Lead:** Mark Dunatov (@mdunatov)

**Team Members:**
- Add your name here when you join!

**Roles:** See [TEAM_HANDOFF.md](./TEAM_HANDOFF.md) for role assignments

---

**Built with ❤️ by the QA Team**

🏎️ **Test at race speed!**
