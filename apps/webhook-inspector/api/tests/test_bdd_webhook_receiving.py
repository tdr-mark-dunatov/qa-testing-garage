"""
BDD Test Step Definitions - Webhook Receiving
"""

import pytest
import requests
import json
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('features/webhook_receiving.feature')

# Test context to share data between steps
@pytest.fixture
def context():
    return {
        "base_url": "http://localhost:8000",
        "bay_id": None,
        "bay_url": None,
        "response": None,
        "webhooks": []
    }


# ==================== GIVEN ====================

@given("the webhook API is running")
def api_is_running(context):
    """Verify the API is accessible"""
    try:
        response = requests.get(f"{context['base_url']}/health", timeout=5)
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("API is not running. Start with: docker-compose up")


@given(parsers.parse('a named bay called "{bay_name}" exists'))
def named_bay_exists(context, bay_name):
    """Create a named bay for testing"""
    response = requests.post(
        f"{context['base_url']}/api/bay/named",
        json={"bay_name": bay_name, "description": f"BDD test bay: {bay_name}"}
    )
    assert response.status_code == 200
    data = response.json()
    context["bay_id"] = data["pit_id"]
    context["bay_url"] = data["pit_lane_url"]


# ==================== WHEN ====================

@when(parsers.parse('I create a named bay called "{bay_name}"'))
def create_named_bay(context, bay_name):
    """Create a named webhook bay"""
    context["response"] = requests.post(
        f"{context['base_url']}/api/bay/named",
        json={"bay_name": bay_name, "description": f"BDD test: {bay_name}"}
    )
    if context["response"].status_code == 200:
        data = context["response"].json()
        context["bay_id"] = data["pit_id"]
        context["bay_url"] = data["pit_lane_url"]


@when("I create a quick bay")
def create_quick_bay(context):
    """Create a quick webhook bay with random ID"""
    context["response"] = requests.post(f"{context['base_url']}/api/bay/quick")
    if context["response"].status_code == 200:
        data = context["response"].json()
        context["bay_id"] = data["pit_id"]
        context["bay_url"] = data["pit_lane_url"]


@when(parsers.parse('I try to create another bay called "{bay_name}"'))
def try_create_duplicate_bay(context, bay_name):
    """Attempt to create a duplicate bay"""
    context["response"] = requests.post(
        f"{context['base_url']}/api/bay/named",
        json={"bay_name": bay_name, "description": "Duplicate test"}
    )


@when("I send a POST request to the bay with JSON data")
def send_post_request(context):
    """Send a POST webhook to the bay"""
    test_data = {"test": "data", "timestamp": "2024-10-06T12:00:00Z"}
    context["response"] = requests.post(
        f"{context['base_url']}/bay/{context['bay_id']}",
        json=test_data
    )
    context["test_data"] = test_data


@when("I send a GET request to the bay")
def send_get_request(context):
    """Send a GET request to the bay"""
    requests.get(f"{context['base_url']}/bay/{context['bay_id']}")


@when("I send a PUT request to the bay")
def send_put_request(context):
    """Send a PUT request to the bay"""
    requests.put(
        f"{context['base_url']}/bay/{context['bay_id']}",
        json={"action": "update"}
    )


@when("I send a DELETE request to the bay")
def send_delete_request_to_bay(context):
    """Send a DELETE request to the bay (not deleting the bay itself)"""
    requests.delete(f"{context['base_url']}/bay/{context['bay_id']}")


@when("I delete the bay")
def delete_bay(context):
    """Delete the webhook bay"""
    context["response"] = requests.delete(
        f"{context['base_url']}/api/bay/{context['bay_id']}"
    )


# ==================== THEN ====================

@then("the bay should be created successfully")
def bay_created_successfully(context):
    """Verify bay creation succeeded"""
    assert context["response"].status_code == 200
    data = context["response"].json()
    assert "pit_id" in data
    assert "pit_lane_url" in data


@then("the bay URL should be accessible")
def bay_url_accessible(context):
    """Verify the bay URL returns 200"""
    response = requests.get(f"{context['base_url']}/bay/{context['bay_id']}")
    assert response.status_code == 200


@then("the bay should appear in the bays list")
def bay_in_list(context):
    """Verify bay appears in GET /api/bays"""
    response = requests.get(f"{context['base_url']}/api/bays")
    assert response.status_code == 200
    bays = response.json()
    bay_ids = [bay["bay_id"] for bay in bays]
    assert context["bay_id"] in bay_ids


@then("the bay should be created with a random ID")
def bay_has_random_id(context):
    """Verify quick bay has a UUID"""
    assert context["bay_id"] is not None
    assert len(context["bay_id"]) == 36  # UUID format


@then(parsers.parse("the request should fail with a {status_code:d} error"))
def request_failed_with_status(context, status_code):
    """Verify request failed with specific status code"""
    assert context["response"].status_code == status_code


@then(parsers.parse('the error message should mention "{text}"'))
def error_message_contains(context, text):
    """Verify error message contains specific text"""
    error_data = context["response"].json()
    assert text.lower() in str(error_data).lower()


@then("the webhook should be captured")
def webhook_captured(context):
    """Verify webhook was captured in the database"""
    response = requests.get(f"{context['base_url']}/api/pit/{context['bay_id']}/requests")
    assert response.status_code == 200
    webhooks = response.json()
    assert len(webhooks) > 0


@then("the webhook should have the correct method")
def webhook_has_correct_method(context):
    """Verify captured webhook has correct HTTP method"""
    response = requests.get(f"{context['base_url']}/api/pit/{context['bay_id']}/requests")
    webhooks = response.json()
    assert webhooks[-1]["method"] == "POST"


@then("the webhook should have the correct body")
def webhook_has_correct_body(context):
    """Verify captured webhook has correct body"""
    response = requests.get(f"{context['base_url']}/api/pit/{context['bay_id']}/requests")
    webhooks = response.json()
    # Body might be masked, so check if it contains key elements
    body_str = str(webhooks[-1]["body"])
    assert "test" in body_str or "data" in body_str


@then(parsers.parse("all {count:d} webhooks should be captured"))
def all_webhooks_captured(context, count):
    """Verify all webhooks were captured"""
    response = requests.get(f"{context['base_url']}/api/pit/{context['bay_id']}/requests")
    webhooks = response.json()
    assert len(webhooks) >= count


@then("each webhook should have its respective method")
def each_webhook_has_method(context):
    """Verify each webhook has the correct method"""
    response = requests.get(f"{context['base_url']}/api/pit/{context['bay_id']}/requests")
    webhooks = response.json()
    methods = [w["method"] for w in webhooks[-4:]]  # Last 4 webhooks
    assert "GET" in methods
    assert "POST" in methods
    assert "PUT" in methods
    assert "DELETE" in methods


@then("the bay should be removed")
def bay_removed(context):
    """Verify bay was deleted"""
    assert context["response"].status_code == 200


@then("the bay should not appear in the bays list")
def bay_not_in_list(context):
    """Verify bay no longer appears in bays list"""
    response = requests.get(f"{context['base_url']}/api/bays")
    bays = response.json()
    bay_ids = [bay["bay_id"] for bay in bays]
    assert context["bay_id"] not in bay_ids
