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
    And the SSN should be masked as "***-**-6789"

  Scenario: Detect Canadian SIN in webhook payload
    Given the webhook API is running
    And a named bay called "pii-sin-test" exists
    When I send a webhook with SIN "123-456-789"
    Then PII should be detected
    And the PII type should include "sin"
    And the risk level should be "critical"

  Scenario: Detect credit score in webhook payload
    Given the webhook API is running
    And a named bay called "pii-credit-test" exists
    When I send a webhook with credit score 720
    Then PII should be detected
    And the PII type should include "credit_score"
    And the risk level should be "high"
    And the credit score should be masked as "***"

  Scenario: Detect email address in webhook payload
    Given the webhook API is running
    And a named bay called "pii-email-test" exists
    When I send a webhook with email "customer@example.com"
    Then PII should be detected
    And the PII type should include "email"
    And the email should be masked as "***@example.com"

  Scenario: Detect phone number in webhook payload
    Given the webhook API is running
    And a named bay called "pii-phone-test" exists
    When I send a webhook with phone "(555) 123-4567"
    Then PII should be detected
    And the PII type should include "phone"
    And the phone should be masked as "***-***-4567"

  Scenario: Detect loan amount in webhook payload
    Given the webhook API is running
    And a named bay called "pii-loan-test" exists
    When I send a webhook with loan amount "$50,000"
    Then PII should be detected
    And the PII type should include "loan_amount"
    And the risk level should be "high"

  Scenario: Detect multiple PII types (critical risk)
    Given the webhook API is running
    And a named bay called "pii-multi-test" exists
    When I send a webhook with multiple PII:
      | type          | value            |
      | ssn           | 123-45-6789      |
      | email         | john@example.com |
      | credit_score  | 720              |
      | loan_amount   | $35,000          |
    Then PII should be detected
    And the risk level should be "critical"
    And 4 PII types should be detected

  Scenario: No PII detected in clean payload
    Given the webhook API is running
    And a named bay called "pii-clean-test" exists
    When I send a webhook with clean data:
      """
      {
        "order_id": "12345",
        "product": "Widget",
        "quantity": 10,
        "status": "pending"
      }
      """
    Then no PII should be detected
    And the risk level should be "low"

  Scenario: Reject invalid SSN patterns
    Given the webhook API is running
    And a named bay called "pii-invalid-ssn-test" exists
    When I send a webhook with SSN "000-00-0000"
    Then no PII should be detected
    And the SSN should be rejected as invalid

  Scenario: Detect PII in nested JSON
    Given the webhook API is running
    And a named bay called "pii-nested-test" exists
    When I send a webhook with nested PII:
      """
      {
        "application": {
          "customer": {
            "personal": {
              "ssn": "123-45-6789"
            }
          }
        }
      }
      """
    Then PII should be detected
    And the PII location should be "application.customer.personal.ssn"
