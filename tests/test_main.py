from fastapi.testclient import TestClient
from app.main import app

def test_health_endpoint():
    """Verifies that the API base health check responds with 200 OK."""
    # Using 'with' forces FastAPI to run the @app.on_event("startup") function
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "HEALTHY"

def test_fraud_verification_flow():
    """Verifies that a high-risk crypto transaction triggers an anomaly detection response."""
    test_payload = {
        "transaction_id": "test-ci-cd-999",
        "account_id": "ACC-TEST",
        "amount": 1500.00,
        "merchant_category": "Crypto",
        "device_id": "device-ci",
        "timestamp": "2026-07-05T02:30:00Z"
    }
    
    # Using 'with' ensures the ML models are loaded into memory before the post request
    with TestClient(app) as client:
        response = client.post("/api/v1/transactions/verify", json=test_payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "risk_score" in data
        # The transaction should either be BLOCKED or routed to REVIEW
        assert data["status"] in ["BLOCKED", "REVIEW"]