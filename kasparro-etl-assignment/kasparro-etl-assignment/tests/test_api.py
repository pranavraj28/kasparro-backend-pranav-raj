"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import get_db
from app.core.models import Asset
from datetime import datetime


@pytest.fixture
def client(test_db):
    """Create test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_endpoint(client, test_db):
    """Test /health endpoint returns DB and ETL status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "etl" in data
    assert data["database"] == "healthy"


def test_data_endpoint_pagination(client, test_db):
    """Test /data endpoint pagination works."""
    # Create test data
    for i in range(10):
        asset = Asset(
            symbol=f"TEST{i}",
            name=f"Test Asset {i}",
            price_usd=100.0 + i,
            source="test",
            updated_at=datetime.utcnow()
        )
        test_db.add(asset)
    test_db.commit()
    
    # Test pagination
    response = client.get("/data?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert len(data["data"]) <= 5
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert "request_id" in data
    assert "api_latency_ms" in data


def test_data_endpoint_filtering(client, test_db):
    """Test /data endpoint filtering by symbol and source."""
    # Create test data
    asset1 = Asset(
        symbol="BTC",
        name="Bitcoin",
        price_usd=50000.0,
        source="coinpaprika",
        updated_at=datetime.utcnow()
    )
    asset2 = Asset(
        symbol="ETH",
        name="Ethereum",
        price_usd=3000.0,
        source="coingecko",
        updated_at=datetime.utcnow()
    )
    test_db.add(asset1)
    test_db.add(asset2)
    test_db.commit()
    
    # Test symbol filter
    response = client.get("/data?symbol=BTC")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 1
    assert all(item["symbol"] == "BTC" for item in data["data"])
    
    # Test source filter
    response = client.get("/data?source=coinpaprika")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) >= 1
    assert all(item["source"] == "coinpaprika" for item in data["data"])

