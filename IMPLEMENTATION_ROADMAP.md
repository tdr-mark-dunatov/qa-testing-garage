# 🚀 Implementation Roadmap - Test Data Compliance Guardian

**Hackathon Focus: Core Compliance Features**

---

## ✅ Already Implemented

### Backend (FastAPI)
- [x] WebSocket real-time updates
- [x] Named & Quick bays
- [x] Webhook capture & storage
- [x] PII masking patterns (SSN, credit cards, email, phone)
- [x] Database models (SQLAlchemy)
- [x] CORS & Docker setup

### Frontend (React)
- [x] Real-time dashboard with WebSockets
- [x] Bay creation UI
- [x] Webhook list view
- [x] Racing-themed design

---

## 🎯 Core Compliance Features (Hackathon MVP)

### Phase 1: PII Detection + Alerts (2-3 hours)

**Backend Tasks:**
- [ ] Create `pii_detector.py` module
  - Reuse existing regex patterns from `mask_sensitive_data()`
  - Return detection results: `{"has_pii": true, "types": ["ssn", "credit_score"]}`
- [ ] Add `slack_notifier.py` module
  - Send webhook to Slack when PII detected
  - Format alert message with bay name, PII types, timestamp
- [ ] Update `inspect_webhook()` in `main.py`
  - Call PII detector on incoming webhooks
  - Send Slack alert if PII found
  - Store PII detection result in database

**Database Tasks:**
- [ ] Add `has_pii` column to `PitLaneRequest` model
- [ ] Add `pii_types` JSON column to `PitLaneRequest` model
- [ ] Run migration

**API Tasks:**
- [ ] Add `/api/compliance/alerts` endpoint
  - Return recent PII detections
- [ ] Update WebSocket broadcast to include PII status

**Files to create/modify:**
- `apps/webhook-inspector/api/pii_detector.py` (NEW)
- `apps/webhook-inspector/api/slack_notifier.py` (NEW)
- `apps/webhook-inspector/api/models.py` (UPDATE)
- `apps/webhook-inspector/api/main.py` (UPDATE)

---

### Phase 2: Ownership Tracking (3-4 hours)

**Backend Tasks:**
- [ ] Update `ReceivingBay` model
  - Add `owner_user` column (string)
  - Add `owner_team` column (string)
  - Add `owner_repo` column (string, optional)
  - Add `owner_pipeline` column (string, optional)
- [ ] Update bay creation endpoints
  - Accept owner metadata in request body
  - Store owner info when creating bay
- [ ] Add `/api/bays/by-team/{team_name}` endpoint
  - Filter bays by team

**Frontend Tasks:**
- [ ] Add "Owner" fields to bay creation form
  - User (text input)
  - Team (dropdown or text)
  - Repo (optional)
  - Pipeline (optional)
- [ ] Display owner info in bay list

**Files to create/modify:**
- `apps/webhook-inspector/api/models.py` (UPDATE)
- `apps/webhook-inspector/api/schemas.py` (UPDATE)
- `apps/webhook-inspector/api/main.py` (UPDATE)
- `apps/webhook-inspector/web/src/components/CreateBayForm.jsx` (UPDATE)

---

### Phase 3: Compliance Dashboard (4-5 hours)

**Backend Tasks:**
- [ ] Add `/api/compliance/summary` endpoint
  - Total active bays
  - Bays with PII count
  - Recent PII alerts (last 24h)
  - Oldest bay age
- [ ] Add `/api/compliance/bays-with-pii` endpoint
  - List bays that have received PII
  - Include last PII detection timestamp

**Frontend Tasks:**
- [ ] Create `ComplianceDashboard.jsx` component
  - Stats cards (active bays, with PII, alerts)
  - Recent alerts table
  - Filter by team
- [ ] Add route `/compliance` to app
- [ ] Add navigation link to compliance dashboard

**Files to create/modify:**
- `apps/webhook-inspector/api/main.py` (UPDATE - add endpoints)
- `apps/webhook-inspector/web/src/components/ComplianceDashboard.jsx` (NEW)
- `apps/webhook-inspector/web/src/App.jsx` (UPDATE - add route)

---

## 🔮 Phase 4: Polish & Demo (2-3 hours)

- [ ] Add ENV variable for Slack webhook URL
- [ ] Test PII detection with sample payloads
- [ ] Update README with compliance features
- [ ] Create demo script for hackathon presentation
- [ ] Add screenshots to HACKATHON.md
- [ ] Deploy to AWS/Railway for live demo

---

## 📊 Effort Summary

| Phase | Features | Hours | Priority |
|-------|----------|-------|----------|
| Phase 1 | PII Detection + Slack Alerts | 2-3 | 🔴 Critical |
| Phase 2 | Ownership Tracking | 3-4 | 🔴 Critical |
| Phase 3 | Compliance Dashboard | 4-5 | 🟡 High |
| Phase 4 | Polish & Demo | 2-3 | 🟢 Medium |
| **Total** | **Core Compliance MVP** | **11-15 hours** | |

---

## 🎯 Minimum Viable Demo

**If time is tight, focus on Phase 1 + Phase 2:**
- PII detection working ✅
- Slack alerts sending ✅
- Ownership tracking ✅
- Basic compliance API ✅

**Phase 3 (Dashboard) can be shown as:**
- API responses (via Swagger UI)
- Or simple table view (no fancy charts needed)

---

## 📝 Development Order

**Day 1 (5-6 hours):**
1. PII detector module
2. Slack integration
3. Update database models
4. Test with sample webhooks

**Day 2 (5-6 hours):**
1. Ownership tracking
2. Compliance API endpoints
3. Frontend updates
4. Demo prep

---

## 🧪 Testing Checklist

- [ ] Send webhook with SSN → Slack alert fires
- [ ] Send webhook with credit score → Detected
- [ ] Send webhook with email → Detected
- [ ] Create bay with owner → Owner stored
- [ ] Call compliance API → Returns stats
- [ ] Dashboard shows correct counts
- [ ] WebSocket updates work with PII status

---

## 🚀 Quick Start Commands

```bash
# Backend development
cd apps/webhook-inspector/api
poetry install
poetry run uvicorn main:app --reload

# Frontend development
cd apps/webhook-inspector/web
npm install
npm run dev

# Test webhook with PII
curl -X POST http://localhost:8000/bay/test-bay \
  -H "Content-Type: application/json" \
  -d '{"ssn": "123-45-6789", "creditScore": 720}'

# Check Slack alert fired
# Check logs for PII detection

# View Swagger docs
open http://localhost:8000/docs
```

---

## 📚 Reference Files

- **Backend code**: `apps/webhook-inspector/api/`
- **Frontend code**: `apps/webhook-inspector/web/src/`
- **Existing PII patterns**: `apps/webhook-inspector/api/main.py:91-117`
- **Database models**: `apps/webhook-inspector/api/models.py`
- **Pitch document**: `PITCH.md`
- **Hackathon pitch**: `HACKATHON.md`

---

## ⚠️ Important Notes

1. **Reuse existing patterns**: Don't reinvent PII detection - copy from `mask_sensitive_data()`
2. **Keep it simple**: Hackathon MVP doesn't need ML or complex regex
3. **Test early**: Set up Slack webhook early to test alerts
4. **Demo-driven**: Focus on features that demo well
5. **Documentation**: Update READMEs as you build

---

## 🎬 Demo Script Outline

1. **Show the problem**
   - Existing test with webhook.site
   - Point out: data sits for 30 days

2. **Show the solution**
   - Create bay with ownership
   - Send webhook with SSN
   - Slack alert fires immediately
   - Show compliance dashboard
   - Show PII detected in UI

3. **Show the impact**
   - Cost savings
   - Compliance tracking
   - Ownership accountability

---

**Ready to build? Start with Phase 1!** 🚀
