# 🎬 Hackathon Demo Script

**Duration:** 5-7 minutes

---

## Setup Before Demo

- [ ] Backend running on localhost:8000
- [ ] Frontend running on localhost:5173
- [ ] Slack webhook configured
- [ ] Test payloads ready
- [ ] Browser tabs open:
  - Dashboard
  - Compliance view
  - Slack channel
  - webhook.site (for comparison)

---

## Act 1: The Problem (1 min)

**Show webhook.site:**
```
"This is what teams use today for webhook testing.
We discovered our own tests were using this..."
```

**Open browser dev tools → Network tab:**
```
"Every test creates a webhook.site URL.
Partner sends sensitive data.
Test completes... but look at this."
```

**Point to webhook.site URL in address bar:**
```
"This URL is public. For 30 days.
SSN: 123-45-6789
Credit Score: 720
Loan Amount: $35,000

Anyone with this URL can see it.
And it's in our CI logs, screenshots, Slack messages..."
```

**Pause for impact.** ⚠️

---

## Act 2: The Solution (3 min)

### Step 1: Create Compliant Bay

**Open Compliance Guardian dashboard:**
```
"We built Test Data Compliance Guardian.
Let me show you how it works."
```

**Click "Create Named Bay":**
- Name: `hmf-integration-demo`
- Owner: `mark.dunatov`
- Team: `QA`
- Repo: `DTN.PlaywrightTests`

**Click Create:**
```
"Notice we're tracking WHO created this.
Full ownership for compliance."
```

**Copy webhook URL:**
```
webhook-guardian.com/bay/hmf-integration-demo
```

---

### Step 2: Trigger PII Detection

**Have Slack channel visible on screen.**

**Send webhook with cURL:**
```bash
curl -X POST http://localhost:8000/bay/hmf-integration-demo \
  -H "Content-Type: application/json" \
  -d '{
    "dealId": "DEAL-12345",
    "customerSSN": "123-45-6789",
    "creditScore": 720,
    "loanAmount": 35000,
    "email": "customer@example.com"
  }'
```

**Watch the magic:**
1. ✅ Webhook appears in dashboard (real-time)
2. 🚨 **Slack alert fires immediately**
3. ⚠️ Badge shows "Contains PII"

**Point to Slack message:**
```
"Automatic alert. No manual checking needed.
It detected:
- SSN
- Credit Score  
- Email

This happens for EVERY webhook automatically."
```

---

### Step 3: Show Compliance Dashboard

**Click "Compliance" tab:**
```
"Here's where compliance teams get visibility."
```

**Point to stats:**
- Active Bays: 1
- With PII: 1  
- Recent Alerts: 1

**Scroll to alerts table:**
```
"Full audit trail:
- What PII was detected
- When
- Who owns the endpoint
- Which team"
```

**Filter by team:**
```
"Compliance can see: Which team has the most PII exposure?
Who needs to clean up?"
```

---

## Act 3: The Difference (1-2 min)

**Split screen: webhook.site vs. Compliance Guardian**

| webhook.site | Compliance Guardian |
|--------------|---------------------|
| ❌ No PII detection | ✅ Automatic detection |
| ❌ No alerts | ✅ Real-time Slack alerts |
| ❌ No ownership | ✅ Full tracking |
| ❌ 30 day retention | ✅ Configurable |
| ❌ $9/user/month | ✅ Self-hosted |

---

## Closing (1 min)

**"This isn't just a webhook tool."**

**"It's a compliance platform that:"**
- ✅ Protects sensitive data automatically
- ✅ Gives teams instant visibility
- ✅ Creates accountability
- ✅ Works for ANY temporary testing endpoint

**"We found the problem in our own tests."**

**"We built the solution for everyone."**

**🏁 Test at race speed, compliance guaranteed!**

---

## Backup Demos (If Time)

### Show Ownership Tracking
```bash
# Create bay with different owner
curl -X POST http://localhost:8000/api/bay/named \
  -d '{"bay_name": "team-dev-test", "owner_team": "Dev"}'

# Show filtering by team in UI
```

### Show Multiple PII Types
```bash
curl -X POST http://localhost:8000/bay/hmf-integration-demo \
  -d '{
    "ssn": "987-65-4321",
    "sin": "123-456-789",
    "phone": "(555) 123-4567",
    "vin": "1HGCM82633A123456"
  }'

# Watch Slack alert with all types
```

---

## Q&A Prep

**Q: What about false positives?**
A: Better safe than sorry for compliance. Patterns are configurable, whitelist support.

**Q: Does this scale?**
A: Async FastAPI, PostgreSQL, WebSocket pub/sub. Can add Redis for caching.

**Q: Integration with CI/CD?**
A: Full REST API. Pass owner metadata from pipeline. Auto-cleanup on job complete.

**Q: What about GDPR/data retention?**
A: Configurable expiration. Auto-delete after N days. Full audit log.

**Q: Cost to run?**
A: AWS: ~$15/month. Saves $900/year vs. webhook.site Pro.

---

## Technical Issues Fallback

**If live demo fails:**
- Have screenshots ready in HACKATHON.md
- Show Slack alert screenshots
- Walk through code in main.py (PII patterns)
- Show database schema
