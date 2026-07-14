from app.storage import get_run, list_audit_events, list_tool_calls


def get_trace(run_id: int) -> dict | None:
    run = get_run(run_id)
    if not run:
        return None
    tools = list_tool_calls(run_id)
    events = list_audit_events(run_id)
    timeline = []
    timeline.append({"type": "run", "timestamp": run["start_time"], "label": "run_started", "status": run["status"]})
    for tool in tools:
        timeline.append(
            {
                "type": "tool_call",
                "timestamp": tool["created_at"],
                "label": tool["tool_name"],
                "status": tool["status"],
                "latency_ms": tool["latency_ms"],
                "error_message": tool["error_message"],
            }
        )
    for event in events:
        timeline.append(
            {
                "type": "audit_event",
                "timestamp": event["timestamp"],
                "label": event["event_type"],
                "status": event["decision"],
                "risk_level": event["risk_level"],
            }
        )
    timeline.sort(key=lambda item: item["timestamp"])
    return {"run": run, "tool_calls": tools, "audit_events": events, "timeline": timeline}
