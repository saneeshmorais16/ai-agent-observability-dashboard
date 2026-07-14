from app.schemas import ToolCallCreate
from app.storage import add_tool_call


def log_tool_call(run_id: int, payload: ToolCallCreate) -> dict | None:
    return add_tool_call(run_id, payload)
