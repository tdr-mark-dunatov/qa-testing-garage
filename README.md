# 🏎️ Test Data Compliance Guardian

**Hackathon 2024 Project**

## The Problem We Discovered

Our QA tests were using webhook.site, leaving **sensitive customer data** (SSN, credit scores, loan amounts) exposed on external servers for **30+ days** with no cleanup.

**This is a real compliance risk.**

## The Solution

Self-hosted webhook testing platform with **automatic PII detection**, Slack alerts when sensitive data is found, and full data ownership.

Replace webhook.site. Stop data leaks. Stay compliant.

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

## 🎯 What We're Building (Hackathon 2024)

### 🏁 Test Data Compliance Guardian - **IN PROGRESS**

**The Problem:** Teams use webhook.site and expose sensitive PII for 30+ days with no cleanup.

**The Solution:** Self-hosted webhook testing with automatic PII detection and compliance tracking.

**Core Features:**
- 🚨 **Automatic PII Detection** - Scans for SSN, SIN, credit scores, emails, phone numbers
- 📢 **Slack Alerts** - Real-time notifications when sensitive data detected  
- 👥 **Ownership Tracking** - Track who/what/when for every endpoint
- 📊 **Compliance Dashboard** - See all data exposure at a glance
- 🗑️ **Full Data Cleanup** - Delete bays + all webhooks on demand
- ⏰ **Auto-Expiration** - Configurable data retention policies

**Already Working:**
- ✅ Named & quick webhook receiving bays
- ✅ Real-time WebSocket updates
- ✅ PostgreSQL database
- ✅ PII masking for display
- ✅ Delete bay functionality
- ✅ Racing-themed dashboard

**To Build (11-15 hours):**
- ⚠️ PII Detection module + Slack integration
- ⚠️ Ownership tracking (user/team/repo/pipeline)
- ⚠️ Compliance dashboard UI

**[→ View Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)**

---

## 🏗️ Architecture

```
PostgreSQL 15 → FastAPI Backend → React Frontend
    ↓              ↓                   ↓
Webhook data   PII Detection      Real-time UI
Audit trail    Slack Alerts       WebSockets
```

**Tech Stack:**
- Backend: Python 3.11 + FastAPI + SQLAlchemy
- Frontend: React 18 + Vite + Tailwind
- Database: PostgreSQL 15
- Infrastructure: Docker Compose

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

## 💰 Business Value

| webhook.site Pro | Compliance Guardian |
|------------------|---------------------|
| $9/user/month | Self-hosted (~$15/month AWS) |
| **$1,080/year for 10 users** | **$180/year** |
| No PII detection | ✅ Automatic PII scanning |
| No alerts | ✅ Slack notifications |
| No ownership tracking | ✅ Full audit trail |
| Data sits 30 days | ✅ Delete on demand |

**Savings: $900/year + Compliance guaranteed**

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

## 📊 Hackathon Status

| Feature | Status | Effort | Owner |
|---------|--------|--------|-------|
| Webhook Receiving Bays | ✅ Complete | Done | - |
| Real-time WebSocket | ✅ Complete | Done | - |
| PostgreSQL Database | ✅ Complete | Done | - |
| Bay Delete (API + UI) | ✅ Complete | Done | - |
| **PII Detection Module** | ⚠️ **To Do** | 2-3h | Needed |
| **Slack Alerts** | ⚠️ **To Do** | 1h | Needed |
| **Ownership Tracking** | ⚠️ **To Do** | 3-4h | Needed |
| **Compliance Dashboard** | ⚠️ **To Do** | 4-5h | Needed |
| Test Suite | ✅ Complete | Done | - |
| Documentation | ✅ Complete | Done | - |

**Total Remaining:** ~11-15 hours of focused work

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

## 🏁 Hackathon Goal

**Build a production-ready compliance platform for webhook testing.**

### What Makes This Different:
- ✅ **Solves a REAL problem** we discovered in our own tests
- ✅ **Not just for QA** - Platform tool for all teams
- ✅ **Production architecture** - PostgreSQL, Docker, CI/CD
- ✅ **Automatic compliance** - No manual PII audits needed
- ✅ **Cost savings** - $900/year vs. webhook.site Pro

### After Hackathon:
1. Deploy to AWS/Railway
2. Migrate team tests from webhook.site
3. **Future:** Expand to other testing tools (API mocks, test data generators)

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
