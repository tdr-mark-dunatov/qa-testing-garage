# 🛡️ Compliance Features - Backend Implementation

## PII Detection Module

**File:** `pii_detector.py`

```python
# Core function signature
def detect_pii(text: str) -> dict:
    """
    Returns: {
        "has_pii": bool,
        "types": ["ssn", "credit_score", "email", "phone", "sin"],
        "details": [
            {"type": "ssn", "value": "***-**-6789", "position": 45}
        ]
    }
    """
```

**Patterns to detect:**
- SSN: `\b\d{3}-\d{2}-\d{4}\b`
- SIN: `\b\d{3}-\d{3}-\d{3}\b`
- Credit Score: `\b[3-8]\d{2}\b` (300-850)
- Loan Amount: `\$[\d,]+` (over $10,000)
- Email: Standard RFC 5322
- Phone: Various formats
- VIN: `[A-HJ-NPR-Z0-9]{17}`

---

## Slack Notifier Module

**File:** `slack_notifier.py`

```python
def send_pii_alert(bay_id: str, bay_name: str, pii_types: list, owner: dict = None):
    """
    POST to SLACK_WEBHOOK_URL with formatted message
    """
    
# Example message format:
{
    "text": "🚨 PII Detected",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Bay:* hmf-integration\n*Owner:* @mark.dunatov\n*PII Types:* SSN, Credit Score"
            }
        }
    ]
}
```

**ENV variable:** `SLACK_WEBHOOK_URL`

---

## Database Schema Updates

**Add to `ReceivingBay` model:**
```python
owner_user = Column(String(100), comment="Owner username")
owner_team = Column(String(100), comment="Team name")
owner_repo = Column(String(200), comment="Git repo (optional)")
owner_pipeline = Column(String(200), comment="CI pipeline ID (optional)")
```

**Add to `PitLaneRequest` model:**
```python
has_pii = Column(Integer, default=0, comment="1 if PII detected")
pii_types = Column(JSON, comment="List of PII types found")
pii_alert_sent = Column(Integer, default=0, comment="1 if Slack alert sent")
```

---

## New API Endpoints

### `/api/compliance/summary`
```json
{
  "active_bays": 12,
  "bays_with_pii": 3,
  "recent_alerts": 5,
  "oldest_bay_age_days": 4
}
```

### `/api/compliance/alerts`
```json
[
  {
    "bay_id": "hmf-integration",
    "bay_name": "HMF Integration Test",
    "pii_types": ["ssn", "credit_score"],
    "owner_user": "mark.dunatov",
    "owner_team": "QA",
    "detected_at": "2024-10-06T10:30:00Z"
  }
]
```

### `/api/compliance/bays-with-pii`
```json
[
  {
    "bay_id": "hmf-integration",
    "bay_name": "HMF Integration Test",
    "total_pii_detections": 5,
    "last_pii_at": "2024-10-06T10:30:00Z",
    "owner": {...}
  }
]
```

### `DELETE /api/bay/{bay_id}` ✅ IMPLEMENTED
Delete a bay completely (bay + all requests)
```json
{
  "status": "deleted",
  "message": "Bay 'hmf-integration' deleted completely",
  "bay_id": "hmf-integration",
  "requests_deleted": 45
}
```

### `DELETE /api/bays/cleanup?older_than_days=7` ✅ IMPLEMENTED
Bulk cleanup old bays for compliance
```json
{
  "status": "cleaned",
  "message": "Deleted 3 bays older than 7 days",
  "deleted_count": 3,
  "total_requests_deleted": 127,
  "bays": [...]
}
```

---

## Integration Points

**In `inspect_webhook()` function:**
```python
# After capturing request body
pii_result = detect_pii(body_text)

if pii_result["has_pii"]:
    # Update request record
    pit_request.has_pii = 1
    pit_request.pii_types = pii_result["types"]
    
    # Send Slack alert (async/background)
    bay = db.query(ReceivingBay).filter(...).first()
    send_pii_alert(
        bay_id=pit_id,
        bay_name=bay.bay_name if bay else pit_id,
        pii_types=pii_result["types"],
        owner={"user": bay.owner_user, "team": bay.owner_team}
    )
    
    pit_request.pii_alert_sent = 1
```

---

## Testing

```bash
# Test PII detection
curl -X POST http://localhost:8000/bay/test \
  -H "Content-Type: application/json" \
  -d '{
    "ssn": "123-45-6789",
    "creditScore": 720,
    "email": "test@example.com"
  }'

# Check logs for detection
# Check Slack for alert

# Query compliance API
curl http://localhost:8000/api/compliance/summary
```
