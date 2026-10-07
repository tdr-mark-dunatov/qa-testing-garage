# BDD Test Suite - Webhook Inspector

Behavior-Driven Development (BDD) tests for the Test Data Compliance Guardian webhook inspection features.

## 📋 What's Tested

### Webhook Receiving (`webhook_receiving.feature`)
- ✅ Create named webhook bays
- ✅ Create quick (random) webhook bays
- ✅ Prevent duplicate bay names
- ✅ Receive webhooks with different HTTP methods
- ✅ Delete webhook bays

### PII Detection (`pii_detection.feature`)
- ✅ Detect SSN (Social Security Numbers)
- ✅ Detect SIN (Canadian Social Insurance Numbers)
- ✅ Detect credit scores
- ✅ Detect email addresses
- ✅ Detect phone numbers
- ✅ Detect loan amounts
- ✅ Calculate risk levels (critical/high/medium/low)
- ✅ Mask sensitive data
- ✅ Reject invalid patterns
- ✅ Handle nested JSON

## 🚀 Running the Tests

### Prerequisites
1. **Start the application:**
   ```bash
   cd docker
   docker-compose up --build
   ```

2. **Install dependencies:**
   ```bash
   cd apps/webhook-inspector/api
   poetry install
   ```

### Run All BDD Tests
```bash
poetry run pytest tests/test_bdd_*.py -v
```

### Run Specific Feature
```bash
# Webhook receiving tests only
poetry run pytest tests/test_bdd_webhook_receiving.py -v

# PII detection tests only
poetry run pytest tests/test_bdd_pii_detection.py -v
```

### Run with Coverage
```bash
poetry run pytest tests/test_bdd_*.py --cov=. --cov-report=html
```

### Run Specific Scenario
```bash
poetry run pytest tests/test_bdd_pii_detection.py -k "Detect SSN" -v
```

## 📊 Test Output Example

```
tests/test_bdd_webhook_receiving.py::test_create_a_named_webhook_bay PASSED
tests/test_bdd_webhook_receiving.py::test_create_a_quick_webhook_bay PASSED
tests/test_bdd_webhook_receiving.py::test_prevent_duplicate_named_bays PASSED
tests/test_bdd_webhook_receiving.py::test_receive_webhook_in_named_bay PASSED
tests/test_bdd_webhook_receiving.py::test_capture_different_http_methods PASSED
tests/test_bdd_webhook_receiving.py::test_delete_a_webhook_bay PASSED

tests/test_bdd_pii_detection.py::test_detect_ssn_in_webhook_payload PASSED
tests/test_bdd_pii_detection.py::test_detect_credit_score_in_webhook_payload PASSED
tests/test_bdd_pii_detection.py::test_detect_multiple_pii_types PASSED
tests/test_bdd_pii_detection.py::test_no_pii_detected_in_clean_payload PASSED

======================== 10 passed in 5.23s ========================
```

## 📝 Feature File Format

Feature files use **Gherkin syntax** (Given/When/Then):

```gherkin
Feature: PII Detection in Webhooks
  As a compliance officer
  I want webhooks to be automatically scanned for PII
  So that we can prevent sensitive data exposure

  Scenario: Detect SSN in webhook payload
    Given the webhook API is running
    And a named bay called "pii-ssn-test" exists
    When I send a webhook with SSN "123-45-6789"
    Then PII should be detected
    And the PII type should include "ssn"
    And the risk level should be "critical"
```

## 🔧 Adding New Tests

### 1. Add a scenario to a feature file:
```gherkin
Scenario: Your new test case
  Given some precondition
  When some action
  Then some expected result
```

### 2. Implement step definitions in the corresponding test file:
```python
@when(parsers.parse('I do something with "{value}"'))
def do_something(context, value):
    # Implementation
    pass

@then("something should happen")
def verify_something(context):
    assert context["result"] == expected
```

## 📁 File Structure

```
tests/
├── features/
│   ├── webhook_receiving.feature    # Gherkin scenarios
│   └── pii_detection.feature        # Gherkin scenarios
├── test_bdd_webhook_receiving.py    # Step definitions
├── test_bdd_pii_detection.py        # Step definitions
└── BDD_TESTS_README.md              # This file
```

## 🐛 Troubleshooting

### Tests fail with "API is not running"
**Solution:** Start the app with `docker-compose up`

### Tests fail with connection errors
**Solution:** Verify API is accessible at http://localhost:8000/health

### Import errors for pytest-bdd
**Solution:** Run `poetry install` to install dependencies

### PII detection not working
**Solution:** Ensure latest code is running with `docker-compose up --build`

## 🎯 CI/CD Integration

These tests run automatically in GitHub Actions:

```yaml
- name: Run BDD Tests
  run: |
    cd apps/webhook-inspector/api
    poetry run pytest tests/test_bdd_*.py -v
```

## 📚 Learn More

- **pytest-bdd docs:** https://pytest-bdd.readthedocs.io/
- **Gherkin syntax:** https://cucumber.io/docs/gherkin/
- **BDD best practices:** https://cucumber.io/docs/bdd/
