import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/api/v1/back_office/devoluciones/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}


test_websocket()