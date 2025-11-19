from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "message" in data

def test_ask():
    r = client.post(
        "/ask/",
        json={"question": "Qual é o horário de atendimento?", "user_id": "rogerio"}
    )
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)

def test_train():
    r = client.post(
        "/train/",
        json={
            "dataset_path": "/data/faq.json",
            "params": {"epochs": 5, "learning_rate": 0.01}
        }
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "started"
    assert "run_id" in data
    assert "metrics" in data
    assert isinstance(data["metrics"], dict)

def test_metrics():
    r = client.get("/metrics/")
    assert r.status_code == 200
    data = r.json()
    assert "total_requests" in data
    assert "avg_latency_ms" in data
    assert isinstance(data["total_requests"], int)
    assert isinstance(data["avg_latency_ms"], float)
