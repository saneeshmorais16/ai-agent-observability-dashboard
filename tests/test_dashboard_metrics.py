from app.database import reset_db
from app.metrics import calculate_dashboard_metrics
from app.synthetic_data import generate_synthetic_data


def test_dashboard_metrics_from_synthetic_data():
    reset_db()
    generate_synthetic_data(reset=False)
    metrics = calculate_dashboard_metrics()
    assert metrics["total_agent_runs"] == 3
    assert metrics["failed_runs"] == 1
    assert metrics["high_risk_prompts"] == 1
    assert metrics["estimated_total_cost"] > 0
