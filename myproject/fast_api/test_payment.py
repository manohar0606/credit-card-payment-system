from fastapi.testclient import TestClient
from fast_api.main import app

client = TestClient(app)


def test_payment_without_token():
    response = client.post(
        "/payment/",
        json={
            "card_id": 1,
            "amount": 100.00
        }
    )

    assert response.status_code == 401


def test_payment_invalid_token():
    response = client.post(
        "/payment/",
        headers={
            "Authorization": "Bearer invalid-token"
        },
        json={
            "card_id": 1,
            "amount": 100.00
        }
    )

    assert response.status_code == 401