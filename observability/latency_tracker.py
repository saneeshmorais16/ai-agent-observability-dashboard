from app.storage import list_tool_calls


def slowest_tools(limit: int = 5) -> list[dict]:
    return sorted(list_tool_calls(), key=lambda item: item["latency_ms"], reverse=True)[:limit]
