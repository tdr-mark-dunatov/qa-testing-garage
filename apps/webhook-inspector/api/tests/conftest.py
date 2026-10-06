"""
Test fixtures for Webhook Inspector API tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import get_db
from models import Base
from main import app


# ═══════════════════════════════════════════════════════════════════
# Database Fixtures
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def test_db():
    """
    Create a fresh in-memory SQLite database for each test
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(test_db):
    """
    FastAPI test client with test database
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════════
# Sample Data Fixtures
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def sample_bay_data():
    """Sample data for creating a named bay"""
    return {
        "bay_name": "test-integration-bay",
        "description": "Test bay for integration tests"
    }


@pytest.fixture
def sample_webhook_payload():
    """Sample webhook payload (no PII)"""
    return {
        "event": "deal.created",
        "dealId": "DEAL-12345",
        "status": "pending",
        "timestamp": "2024-10-06T10:30:00Z"
    }


@pytest.fixture
def sample_pii_payload():
    """Sample webhook payload WITH PII for compliance testing"""
    return {
        "event": "deal.approved",
        "dealId": "DEAL-67890",
        "customer": {
            "name": "John Doe",
            "ssn": "123-45-6789",
            "email": "john.doe@example.com",
            "phone": "(555) 123-4567"
        },
        "loan": {
            "creditScore": 720,
            "amount": 35000,
            "term": 60
        },
        "vehicle": {
            "vin": "1HGCM82633A123456",
            "make": "Honda",
            "model": "Accord"
        }
    }


@pytest.fixture
def created_bay(client, sample_bay_data):
    """
    Create a bay and return the response
    Useful for tests that need an existing bay
    """
    response = client.post("/api/bay/named", json=sample_bay_data)
    assert response.status_code == 200
    return response.json()
