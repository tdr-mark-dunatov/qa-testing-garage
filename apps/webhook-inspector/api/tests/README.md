# 🧪 Tests - Webhook Inspector API

## Test Structure

```
tests/
├── conftest.py              # Fixtures (test DB, sample data)
├── test_pii_masking.py      # Unit: PII detection patterns
├── test_api_bays.py         # Integration: Bay CRUD operations
└── test_api_webhooks.py     # Integration: Webhook capture & retrieval
```

---

## Running Tests

### All Tests
```bash
cd apps/webhook-inspector/api
poetry run pytest
```

### With Coverage
```bash
poetry run pytest --cov=. --cov-report=html
```

### Specific Test Types

**Unit tests only (fast):**
```bash
poetry run pytest -m unit
```

**Integration tests:**
```bash
poetry run pytest -m integration
```

**Compliance tests:**
```bash
poetry run pytest -m compliance
```

### Specific Test File
```bash
poetry run pytest tests/test_pii_masking.py
```

### Specific Test
```bash
poetry run pytest tests/test_pii_masking.py::TestPIIMasking::test_ssn_masking
```

### Watch Mode (run tests on file change)
```bash
poetry run pytest-watch
```

---

## Test Coverage

Current test coverage:

| Module | Coverage | Status |
|--------|----------|--------|
| PII Masking | 100% | ✅ |
| Bay CRUD | 90% | ✅ |
| Webhook Capture | 85% | ✅ |
| PII Detection | 0% | ⚠️ Not implemented yet |
| Slack Alerts | 0% | ⚠️ Not implemented yet |

---

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast unit tests, no DB/external deps
- `@pytest.mark.integration` - Integration tests with test DB
- `@pytest.mark.compliance` - Compliance feature tests (PII, alerts)
- `@pytest.mark.slow` - Slow tests (can be skipped)

**Skip slow tests:**
```bash
pytest -m "not slow"
```

---

## Writing New Tests

### 1. Use Fixtures from conftest.py

```python
def test_example(client, created_bay, sample_webhook_payload):
    """client = FastAPI test client with test DB
       created_bay = Pre-created bay
       sample_webhook_payload = Sample data
    """
    response = client.post(f"/bay/{created_bay['pit_id']}", 
                           json=sample_webhook_payload)
    assert response.status_code == 200
```

### 2. Mark Your Tests

```python
@pytest.mark.unit
@pytest.mark.compliance
def test_pii_detection():
    # Your test here
    pass
```

### 3. Name Tests Descriptively

```python
def test_create_bay_with_valid_data():  # ✅ Good
def test_bay():                          # ❌ Too vague
```

---

## CI Integration

Tests run automatically in GitHub Actions:

**.github/workflows/ci.yml:**
- Runs on every push/PR
- Tests all Python versions
- Generates coverage report

**Local pre-commit hook (optional):**
```bash
# .git/hooks/pre-commit
#!/bin/bash
cd apps/webhook-inspector/api
poetry run pytest -m unit -x
```

---

## Debugging Tests

### Run with verbose output:
```bash
pytest -vv
```

### Show print statements:
```bash
pytest -s
```

### Drop into debugger on failure:
```bash
pytest --pdb
```

### Run last failed tests:
```bash
pytest --lf
```

---

## Test Data

**Sample fixtures in conftest.py:**

- `sample_bay_data` - Clean bay creation data
- `sample_webhook_payload` - Webhook without PII
- `sample_pii_payload` - Webhook with PII (SSN, email, credit score)
- `created_bay` - Pre-created bay for tests
- `test_db` - In-memory SQLite database
- `client` - FastAPI TestClient

---

## Common Test Patterns

### Test API Endpoint
```python
def test_endpoint(client):
    response = client.get("/api/endpoint")
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
```

### Test with Database
```python
def test_with_db(client, test_db):
    # Create record
    client.post("/api/bay/named", json={"bay_name": "test"})
    
    # Verify in DB
    from models import ReceivingBay
    bay = test_db.query(ReceivingBay).first()
    assert bay.bay_name == "test"
```

### Test PII Detection
```python
def test_pii_pattern():
    import re
    pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    assert re.search(pattern, "SSN: 123-45-6789")
```

---

## Adding Tests for New Features

### When Adding PII Detection Module:

**Create: `tests/test_pii_detector.py`**
```python
from pii_detector import detect_pii

@pytest.mark.unit
@pytest.mark.compliance
def test_detect_ssn():
    result = detect_pii("SSN: 123-45-6789")
    assert result["has_pii"] is True
    assert "ssn" in result["types"]
```

### When Adding Slack Alerts:

**Create: `tests/test_slack_notifier.py`**
```python
from unittest.mock import patch
from slack_notifier import send_pii_alert

@pytest.mark.unit
def test_slack_alert_format():
    with patch('requests.post') as mock_post:
        send_pii_alert("test-bay", "Test Bay", ["ssn"])
        
        # Verify Slack webhook was called
        assert mock_post.called
        call_args = mock_post.call_args
        assert "PII Detected" in str(call_args)
```

---

## Troubleshooting

**Tests fail with "ModuleNotFoundError":**
```bash
# Install dependencies
poetry install

# Ensure you're in correct directory
cd apps/webhook-inspector/api
```

**Database conflicts:**
```bash
# Tests use in-memory DB, but if issues persist:
rm -rf data/pitstop.db
```

**Async test warnings:**
```bash
# Add to test file:
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result
```

---

## Next Steps for Team

1. ✅ **Run baseline tests** - Make sure all pass
2. ⚠️ **Add PII detection tests** - When implementing feature
3. ⚠️ **Add Slack integration tests** - Mock the webhook calls
4. ⚠️ **Add ownership tracking tests** - Test new DB columns
5. ⚠️ **Add compliance dashboard tests** - Test new API endpoints

---

**Test coverage goal: 80%+ before hackathon demo!**
