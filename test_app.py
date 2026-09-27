import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_register_success(client):
    resp = client.post("/register/1")
    assert resp.status_code == 200
    assert resp.get_json()["seats_left"] == 49


def test_register_blocked_at_zero(client):
    resp = client.post("/register/2")  # AI Workshop, seats_left = 0
    assert resp.status_code == 400


def test_register_not_found(client):
    resp = client.post("/register/999")
    assert resp.status_code == 404
