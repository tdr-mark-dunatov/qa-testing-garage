"""
Integration tests for Bay API endpoints
"""
import pytest


@pytest.mark.integration
class TestBayCreation:
    """Test bay creation endpoints"""

    def test_create_named_bay(self, client, sample_bay_data):
        """Test creating a named bay"""
        response = client.post("/api/bay/named", json=sample_bay_data)

        assert response.status_code == 200
        data = response.json()

        assert data["pit_id"] == "test-integration-bay"
        assert "pit_lane_url" in data
        assert "/bay/test-integration-bay" in data["pit_lane_url"]
        assert "ready" in data["message"].lower()

    def test_create_quick_bay(self, client):
        """Test creating a quick (random) bay"""
        response = client.post("/api/bay/quick")

        assert response.status_code == 200
        data = response.json()

        assert "pit_id" in data
        assert len(data["pit_id"]) == 36  # UUID length
        assert "/bay/" in data["pit_lane_url"]

    def test_create_duplicate_named_bay_fails(self, client, sample_bay_data):
        """Test that creating duplicate named bay fails"""
        # Create first bay
        response1 = client.post("/api/bay/named", json=sample_bay_data)
        assert response1.status_code == 200

        # Try to create same bay again
        response2 = client.post("/api/bay/named", json=sample_bay_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"].lower()

    def test_bay_name_sanitization(self, client):
        """Test that bay names are sanitized to URL-safe format"""
        response = client.post("/api/bay/named", json={
            "bay_name": "Test Bay With Spaces!",
            "description": "Should be URL safe"
        })

        assert response.status_code == 200
        data = response.json()

        # Spaces and special chars should be replaced with dashes
        assert data["pit_id"] == "test-bay-with-spaces"


@pytest.mark.integration
class TestBayListing:
    """Test bay listing endpoints"""

    def test_list_empty_bays(self, client):
        """Test listing bays when none exist"""
        response = client.get("/api/bays")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_bays_with_stats(self, client, sample_bay_data):
        """Test listing bays shows statistics"""
        # Create a bay
        create_response = client.post("/api/bay/named", json=sample_bay_data)
        bay_id = create_response.json()["pit_id"]

        # List bays
        response = client.get("/api/bays")

        assert response.status_code == 200
        bays = response.json()
        assert len(bays) == 1

        bay = bays[0]
        assert bay["bay_id"] == bay_id
        assert bay["bay_name"] == sample_bay_data["bay_name"]
        assert bay["is_named"] is True
        assert bay["total_requests"] == 0  # No webhooks sent yet
        assert "created_at" in bay


@pytest.mark.integration
class TestBayDeletion:
    """Test bay deletion endpoints (compliance feature)"""

    def test_delete_bay(self, client, created_bay):
        """Test deleting a bay completely"""
        bay_id = created_bay["pit_id"]

        # Delete the bay
        response = client.delete(f"/api/bay/{bay_id}")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "deleted"
        assert data["bay_id"] == bay_id
        assert data["requests_deleted"] >= 0

        # Verify bay is gone
        list_response = client.get("/api/bays")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 0

    def test_delete_nonexistent_bay(self, client):
        """Test deleting a bay that doesn't exist"""
        response = client.delete("/api/bay/nonexistent-bay-id")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_bulk_cleanup_no_old_bays(self, client, created_bay):
        """Test bulk cleanup when no bays are old enough"""
        # Try to cleanup bays older than 30 days (our test bay is fresh)
        response = client.delete("/api/bays/cleanup?older_than_days=30")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "no_action"
        assert data["deleted_count"] == 0

        # Bay should still exist
        list_response = client.get("/api/bays")
        assert len(list_response.json()) == 1
