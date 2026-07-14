from fastapi.testclient import TestClient

from app.database import reset_db
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_trace_retrieval():
    reset_db()
    run_response = client.post(
        "/runs",
        json={"user_request_summary": "Review synthetic task notes", "agent_name": "api_agent", "prompt_tokens": 10, "completion_tokens": 5},
    )
    run_id = run_response.json()["id"]
    client.post(f"/runs/{run_id}/tool-call", json={"tool_name": "parser", "input_summary": "notes", "output_summary": "items", "latency_ms": 55})
    trace = client.get(f"/runs/{run_id}")
    assert trace.status_code == 200
    assert trace.json()["tool_calls"][0]["tool_name"] == "parser"


def test_dashboard_endpoint():
    reset_db()
    client.post("/synthetic/generate")
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert response.json()["total_agent_runs"] == 3
