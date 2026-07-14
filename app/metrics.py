from collections import Counter, defaultdict

from app.storage import list_audit_events, list_runs, list_tool_calls


def calculate_dashboard_metrics() -> dict:
    runs = list_runs()
    tools = list_tool_calls()
    total_runs = len(runs)
    successful_runs = sum(1 for run in runs if run["status"] == "success")
    failed_runs = sum(1 for run in runs if run["status"] == "failed")
    high_risk_prompts = sum(1 for run in runs if run["risk_level"] in {"high", "critical"})
    avg_latency = round(sum(tool["latency_ms"] for tool in tools) / len(tools), 2) if tools else 0
    total_cost = round(sum(run["estimated_cost"] for run in runs), 6)
    tool_counts = Counter(tool["tool_name"] for tool in tools)
    error_counts = Counter(tool["error_message"] or "unknown_error" for tool in tools if tool["status"] != "success")
    return {
        "total_agent_runs": total_runs,
        "successful_runs": successful_runs,
        "failed_runs": failed_runs,
        "average_tool_latency_ms": avg_latency,
        "estimated_total_cost": total_cost,
        "high_risk_prompts": high_risk_prompts,
        "most_used_tools": tool_counts.most_common(5),
        "most_common_errors": error_counts.most_common(5),
        "failure_rate": round(failed_runs / total_runs * 100, 2) if total_runs else 0,
    }


def cost_breakdown() -> dict:
    by_agent: dict[str, float] = defaultdict(float)
    by_run = []
    for run in list_runs():
        by_agent[run["agent_name"]] += run["estimated_cost"]
        by_run.append({"run_id": run["id"], "agent_name": run["agent_name"], "estimated_cost": run["estimated_cost"]})
    return {"cost_by_run": by_run, "cost_by_agent": {agent: round(cost, 6) for agent, cost in by_agent.items()}}


def risk_summary() -> list[dict]:
    rows = []
    for run in list_runs():
        for flag in run["risk_flags"]:
            rows.append({"run_id": run["id"], "agent_name": run["agent_name"], **flag})
    return rows


def error_summary() -> dict:
    tools = list_tool_calls()
    failed = [tool for tool in tools if tool["status"] != "success"]
    categories = Counter((tool["error_message"] or "unknown").split(":")[0].lower() for tool in failed)
    return {
        "failed_tool_calls": len(failed),
        "retry_count": sum(tool["retry_count"] for tool in tools),
        "error_categories": categories.most_common(),
    }


def audit_log() -> list[dict]:
    return list_audit_events()
