from app.database import reset_db
from app.schemas import RunCreate, ToolCallCreate
from observability.run_logger import log_run
from observability.tool_logger import log_tool_call


def test_tool_call_logging():
    reset_db()
    run = log_run(RunCreate(user_request_summary="Use a safe tool", agent_name="tool_agent"))
    tool = log_tool_call(run["id"], ToolCallCreate(tool_name="search_docs", input_summary="query", output_summary="result", latency_ms=123))
    assert tool["tool_name"] == "search_docs"
    assert tool["latency_ms"] == 123
