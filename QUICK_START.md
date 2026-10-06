# 🚀 Quick Start - Test Data Compliance Guardian

## Option 1: Docker (Easiest) ✅

**Start everything with one command:**

```bash
cd docker
docker-compose up --build
```

**Access:**
- 🌐 Frontend: http://localhost:8080
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

**Stop:**
```bash
docker-compose down
```

**Clean restart (delete data):**
```bash
docker-compose down -v
docker-compose up --build
```

---

## Option 2: Manual Development

### Backend
```bash
cd apps/webhook-inspector/api

# Install dependencies
poetry install

# Run dev server
poetry run uvicorn main:app --reload

# Access: http://localhost:8000
```

### Frontend (separate terminal)
```bash
cd apps/webhook-inspector/web

# Install dependencies
npm install

# Run dev server
npm run dev

# Access: http://localhost:5173
```

---

## Test It Works

**Send a test webhook:**
```bash
curl -X POST http://localhost:8000/bay/test-bay \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from Compliance Guardian!"}'
```

**With PII (to trigger detection):**
```bash
curl -X POST http://localhost:8000/bay/test-bay \
  -H "Content-Type: application/json" \
  -d '{
    "ssn": "123-45-6789",
    "creditScore": 720,
    "email": "test@example.com"
  }'
```

---

## Environment Variables

**Optional - for Slack alerts:**

Create `apps/webhook-inspector/api/.env`:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
CORS_ALLOW_ALL=true
```

---

## Troubleshooting

**Port already in use?**
```bash
# Change ports in docker-compose.yml:
ports:
  - "8001:8000"  # Backend
  - "8081:80"    # Frontend
```

**Docker build fails?**
```bash
# Clear Docker cache
docker-compose down -v
docker system prune -a
docker-compose up --build
```

**Frontend can't reach backend?**
- Check backend is running: http://localhost:8000/health
- Check CORS settings in `api/main.py`

---

## What's Next?

1. **Explore the app:** Create a bay, send webhooks, watch real-time updates
2. **Read implementation docs:** See `IMPLEMENTATION_ROADMAP.md`
3. **Start building:** Pick a task from `TEAM_HANDOFF.md`
4. **Test compliance features:** Once PII detection is added

🏁 **Ready to race!**
