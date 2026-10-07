Feature: Webhook Receiving Bays
  As a QA engineer
  I want to create webhook receiving bays
  So that I can capture webhook payloads for testing

  Scenario: Create a named webhook bay
    Given the webhook API is running
    When I create a named bay called "integration-test"
    Then the bay should be created successfully
    And the bay URL should be accessible
    And the bay should appear in the bays list

  Scenario: Create a quick webhook bay
    Given the webhook API is running
    When I create a quick bay
    Then the bay should be created with a random ID
    And the bay URL should be accessible

  Scenario: Prevent duplicate named bays
    Given the webhook API is running
    And a named bay called "duplicate-test" exists
    When I try to create another bay called "duplicate-test"
    Then the request should fail with a 400 error
    And the error message should mention "already exists"

  Scenario: Receive webhook in named bay
    Given the webhook API is running
    And a named bay called "webhook-test" exists
    When I send a POST request to the bay with JSON data
    Then the webhook should be captured
    And the webhook should have the correct method
    And the webhook should have the correct body

  Scenario: Capture different HTTP methods
    Given the webhook API is running
    And a named bay called "methods-test" exists
    When I send a GET request to the bay
    And I send a POST request to the bay
    And I send a PUT request to the bay
    And I send a DELETE request to the bay
    Then all 4 webhooks should be captured
    And each webhook should have its respective method

  Scenario: Delete a webhook bay
    Given the webhook API is running
    And a named bay called "delete-test" exists
    When I delete the bay
    Then the bay should be removed
    And the bay should not appear in the bays list
