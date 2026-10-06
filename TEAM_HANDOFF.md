# 👥 Team Handoff - Getting Started

**Quick reference for team members joining the hackathon project**

---

## 🎯 What We're Building

**Test Data Compliance Guardian** - Platform that automatically detects PII in testing webhooks and sends Slack alerts.

**Problem:** Tests using webhook.site leak sensitive data (SSN, credit scores) for 30+ days.

**Solution:** Self-hosted with automatic PII detection, ownership tracking, compliance dashboard.

---

## 📚 Key Documents

1. **[HACKATHON.md](./HACKATHON.md)** - Full pitch & demo flow
2. **[IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)** - Development phases
3. **[PITCH.md](./PITCH.md)** - Detailed pitch for judges
4. **Backend spec:** `apps/webhook-inspector/api/COMPLIANCE_FEATURES.md`
5. **Frontend spec:** `apps/webhook-inspector/web/COMPLIANCE_UI.md`
6. **Demo script:** `apps/webhook-inspector/DEMO_SCRIPT.md`

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
cd c:/Test-Development/qa-testing-garage

# Backend
cd apps/webhook-inspector/api
poetry install
poetry run uvicorn main:app --reload

# Frontend (separate terminal)
cd apps/webhook-inspector/web
npm install
npm run dev
```

### 2. Access
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Test Webhook
```bash
curl -X POST http://localhost:8000/bay/test \
  -H "Content-Type: application/json" \
  -d '{"ssn": "123-45-6789", "creditScore": 720}'
```

---

## 👨‍💻 Team Roles

### Backend Developer
**Focus:** PII detection + Slack integration

**Tasks:**
- Create `pii_detector.py` module
- Create `slack_notifier.py` module
- Update database models (add PII columns)
- Add compliance API endpoints
- Test with sample payloads

**Reference:** `apps/webhook-inspector/api/COMPLIANCE_FEATURES.md`

---

### Frontend Developer
**Focus:** Compliance dashboard + UI updates

**Tasks:**
- Create `ComplianceDashboard.jsx` component
- Update `CreateBayForm.jsx` (add owner fields)
- Add PII badges to bay list
- Update WebSocket handler for PII alerts
- Add routing for compliance view

**Reference:** `apps/webhook-inspector/web/COMPLIANCE_UI.md`

---

### DevOps / Integration
**Focus:** Slack setup + deployment

**Tasks:**
- Create Slack webhook URL
- Set ENV variable `SLACK_WEBHOOK_URL`
- Test Slack alert formatting
- Docker compose updates if needed
- Prepare AWS/Railway deployment

**Reference:** `DEPLOYMENT.md`

---

### Demo / Presentation
**Focus:** Hackathon presentation

**Tasks:**
- Prepare demo script
- Create slide deck (optional)
- Test demo flow
- Prepare Q&A responses
- Record backup demo video

**Reference:** `apps/webhook-inspector/DEMO_SCRIPT.md`

---

## 🎯 MVP Features (Must Have)

- [x] Named webhook bays (already working)
- [x] Real-time WebSocket updates (already working)
- [ ] **PII detection** (SSN, credit scores, email, phone)
- [ ] **Slack alerts** when PII detected
- [ ] **Ownership tracking** (user, team, repo)
- [ ] **Compliance API** endpoints
- [ ] **Basic compliance dashboard**

---

## 🔮 Nice to Have (If Time)

- [ ] Auto-expiration policies
- [ ] Filter bays by team
- [ ] Compliance report export
- [ ] More PII patterns (VIN, SIN)
- [ ] Fancy charts in dashboard

---

## 🧪 Testing Checklist

- [ ] PII detection works (SSN, email, phone, credit score)
- [ ] Slack alert fires on PII
- [ ] Owner info saved on bay creation
- [ ] Compliance API returns correct stats
- [ ] Dashboard displays recent alerts
- [ ] WebSocket updates include PII status

---

## 📦 What's Already Built

**Backend (FastAPI):**
- ✅ Webhook capture endpoints
- ✅ Database models (SQLAlchemy)
- ✅ WebSocket real-time updates
- ✅ PII masking patterns (can reuse for detection)
- ✅ CORS & Docker setup

**Frontend (React + Vite):**
- ✅ Real-time dashboard
- ✅ Create bay form
- ✅ Bay list view
- ✅ WebSocket client
- ✅ Racing-themed UI

**Infrastructure:**
- ✅ Docker Compose
- ✅ SQLite database
- ✅ Nginx config

---

## 🐛 Known Issues

- None yet (fresh project!)

---

## 💡 Development Tips

1. **Reuse existing code:** PII masking patterns already exist in `main.py:91-117`
2. **Test with real Slack early:** Don't wait until last minute
3. **Use Swagger UI:** `http://localhost:8000/docs` for API testing
4. **Keep it simple:** Hackathon MVP doesn't need perfection
5. **Demo-driven:** Focus on features that show well

---

## 🆘 Need Help?

- Check existing code in `apps/webhook-inspector/api/main.py`
- See PII patterns: `mask_sensitive_data()` function
- Ask team lead for Slack webhook URL
- Review IMPLEMENTATION_ROADMAP.md for detailed steps

---

## 📞 Contact

**Project Lead:** [Your Name]
**Slack Channel:** #hackathon-compliance-guardian
**Repo:** https://github.com/your-org/qa-testing-garage

---

**Let's build something awesome! 🏁**
