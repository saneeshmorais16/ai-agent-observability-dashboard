from app.database import reset_db
from app.schemas import RunCreate
from observability.run_logger import log_run


def test_run_creation_logs_cost_and_risk():
    reset_db()
    run = log_run(RunCreate(user_request_summary="Summarise safe synthetic notes", agent_name="demo_agent", prompt_tokens=100, completion_tokens=50))
    assert run["id"] == 1
    assert run["total_tokens"] == 150
    assert run["risk_level"] == "low"
