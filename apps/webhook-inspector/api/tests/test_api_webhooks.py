"""
Integration tests for webhook capture endpoints
"""
import pytest
import json


@pytest.mark.integration
class TestWebhookCapture:
    """Test webhook capture functionality"""

    def test_capture_post_webhook(self, client, created_bay, sample_webhook_payload):
        """Test capturing a POST webhook"""
        bay_id = created_bay["pit_id"]

        # Send webhook
        response = client.post(
            f"/bay/{bay_id}",
            json=sample_webhook_payload
        )

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert data["pit_id"] == bay_id
        assert "lap_time_ms" in data
        assert data["lap_time_ms"] >= 0

    def test_capture_get_webhook(self, client, created_bay):
        """Test capturing a GET request"""
        bay_id = created_bay["pit_id"]

        response = client.get(f"/bay/{bay_id}?foo=bar&test=123")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_capture_various_methods(self, client, created_bay):
        """Test capturing different HTTP methods"""
        bay_id = created_bay["pit_id"]

        methods = [
            ("post", client.post),
            ("put", client.put),
            ("patch", client.patch),
            ("delete", client.delete),
        ]

        for method_name, method_func in methods:
            response = method_func(f"/bay/{bay_id}")
            assert response.status_code == 200, f"{method_name.upper()} failed"

    def test_webhook_with_headers(self, client, created_bay):
        """Test that webhook captures custom headers"""
        bay_id = created_bay["pit_id"]

        response = client.post(
            f"/bay/{bay_id}",
            headers={
                "X-Custom-Header": "test-value",
                "X-Event-Type": "deal.created"
            },
            json={"test": "data"}
        )

        assert response.status_code == 200

        # Get captured requests
        requests_response = client.get(f"/api/pit/{bay_id}/requests")
        assert requests_response.status_code == 200

        requests = requests_response.json()
        assert len(requests) == 1

        captured = requests[0]
        assert "x-custom-header" in captured["headers"]
        assert captured["headers"]["x-custom-header"] == "test-value"


@pytest.mark.integration
class TestWebhookRetrieval:
    """Test retrieving captured webhooks"""

    def test_get_requests_empty(self, client, created_bay):
        """Test getting requests when none captured"""
        bay_id = created_bay["pit_id"]

        response = client.get(f"/api/pit/{bay_id}/requests")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_requests_after_capture(self, client, created_bay, sample_webhook_payload):
        """Test getting requests after capturing webhooks"""
        bay_id = created_bay["pit_id"]

        # Send 3 webhooks
        for i in range(3):
            payload = {**sample_webhook_payload, "index": i}
            client.post(f"/bay/{bay_id}", json=payload)

        # Get captured requests
        response = client.get(f"/api/pit/{bay_id}/requests")

        assert response.status_code == 200
        requests = response.json()
        assert len(requests) == 3

        # Verify request structure
        req = requests[0]
        assert "id" in req
        assert "method" in req
        assert req["method"] == "POST"
        assert "headers" in req
        assert "body" in req
        assert "created_at" in req
        assert "lap_time_ms" in req

    def test_get_requests_with_limit(self, client, created_bay):
        """Test limiting number of requests returned"""
        bay_id = created_bay["pit_id"]

        # Send 10 webhooks
        for i in range(10):
            client.post(f"/bay/{bay_id}", json={"index": i})

        # Get only 5
        response = client.get(f"/api/pit/{bay_id}/requests?limit=5")

        assert response.status_code == 200
        requests = response.json()
        assert len(requests) == 5


@pytest.mark.integration
class TestWebhookCleanup:
    """Test webhook cleanup endpoints"""

    def test_clear_requests(self, client, created_bay):
        """Test clearing all requests from a bay"""
        bay_id = created_bay["pit_id"]

        # Send some webhooks
        for i in range(5):
            client.post(f"/bay/{bay_id}", json={"index": i})

        # Clear them
        response = client.delete(f"/api/pit/{bay_id}/requests")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "cleared"
        assert data["deleted_count"] == 5

        # Verify they're gone
        requests_response = client.get(f"/api/pit/{bay_id}/requests")
        assert requests_response.json() == []


@pytest.mark.integration
@pytest.mark.compliance
class TestWebhookPIIMasking:
    """Test PII masking in captured webhooks"""

    def test_webhook_with_pii_is_masked(self, client, created_bay, sample_pii_payload):
        """Test that PII in webhook payload is masked when stored"""
        bay_id = created_bay["pit_id"]

        # Send webhook with PII
        client.post(f"/bay/{bay_id}", json=sample_pii_payload)

        # Get captured request
        response = client.get(f"/api/pit/{bay_id}/requests")
        requests = response.json()

        assert len(requests) == 1
        captured = requests[0]

        # Check that body has masked PII
        body_text = captured["body"]

        # SSN should be masked
        assert "123-45-6789" not in body_text
        assert "***-**-6789" in body_text

        # Email should be masked
        assert "john.doe@example.com" not in body_text
        assert "j***@example.com" in body_text

        # Phone should be masked
        assert "(555) 123-4567" not in body_text
        assert "(***) ***-4567" in body_text

    def test_webhook_without_pii_unchanged(self, client, created_bay, sample_webhook_payload):
        """Test that webhooks without PII are not altered"""
        bay_id = created_bay["pit_id"]

        # Send webhook without PII
        client.post(f"/bay/{bay_id}", json=sample_webhook_payload)

        # Get captured request
        response = client.get(f"/api/pit/{bay_id}/requests")
        requests = response.json()

        body_text = requests[0]["body"]
        original_text = json.dumps(sample_webhook_payload)

        # Body should contain original data (after JSON parsing differences)
        assert "DEAL-12345" in body_text
        assert "deal.created" in body_text
