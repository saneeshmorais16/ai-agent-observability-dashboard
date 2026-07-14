import json

from app.cost_estimator import estimate_cost
from app.database import get_connection, init_db
from app.risk_detection import detect_prompt_risks, highest_risk_level


def create_run(payload) -> dict:
    init_db()
    cost = estimate_cost(payload.prompt_tokens, payload.completion_tokens)
    flags = detect_prompt_risks(payload.user_request_summary)
    risk_level = highest_risk_level(flags)
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO agent_runs (
                user_request_summary, agent_name, status, final_outcome, prompt_tokens, completion_tokens,
                total_tokens, estimated_cost, retry_count, risk_level, risk_flags_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.user_request_summary,
                payload.agent_name,
                payload.status,
                payload.final_outcome,
                cost["prompt_tokens"],
                cost["completion_tokens"],
                cost["total_tokens"],
                cost["estimated_cost"],
                payload.retry_count,
                risk_level,
                json.dumps(flags),
            ),
        )
        run_id = int(cursor.lastrowid)
        connection.execute(
            "INSERT INTO audit_events (run_id, event_type, actor, decision, risk_level, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, "run_created", "api", "recorded", risk_level, "Synthetic or user-provided demo run recorded."),
        )
    return get_run(run_id)


def finish_run(run_id: int, payload) -> dict | None:
    existing = get_run(run_id)
    if not existing:
        return None
    cost = estimate_cost(payload.prompt_tokens, payload.completion_tokens)
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE agent_runs
            SET status = ?, final_outcome = ?, prompt_tokens = ?, completion_tokens = ?, total_tokens = ?,
                estimated_cost = ?, retry_count = ?, end_time = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                payload.status,
                payload.final_outcome,
                cost["prompt_tokens"],
                cost["completion_tokens"],
                cost["total_tokens"],
                cost["estimated_cost"],
                payload.retry_count,
                run_id,
            ),
        )
        connection.execute(
            "INSERT INTO audit_events (run_id, event_type, actor, decision, risk_level, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, "run_finished", "api", payload.status, existing["risk_level"], payload.final_outcome),
        )
    return get_run(run_id)


def add_tool_call(run_id: int, payload) -> dict | None:
    if not get_run(run_id):
        return None
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tool_calls (run_id, tool_name, input_summary, output_summary, status, latency_ms, error_message, retry_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                payload.tool_name,
                payload.input_summary,
                payload.output_summary,
                payload.status,
                payload.latency_ms,
                payload.error_message,
                payload.retry_count,
            ),
        )
        tool_call_id = int(cursor.lastrowid)
        if payload.status != "success":
            connection.execute(
                "INSERT INTO audit_events (run_id, event_type, actor, decision, risk_level, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (run_id, "tool_error", payload.tool_name, "failed", "medium", payload.error_message),
            )
    return get_tool_call(tool_call_id)


def add_audit_event(run_id: int, payload) -> dict | None:
    if not get_run(run_id):
        return None
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO audit_events (run_id, event_type, actor, decision, risk_level, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, payload.event_type, payload.actor, payload.decision, payload.risk_level, payload.notes),
        )
        event_id = int(cursor.lastrowid)
    return get_audit_event(event_id)


def row_to_run(row) -> dict:
    result = dict(row)
    result["risk_flags"] = json.loads(result.pop("risk_flags_json"))
    return result


def get_run(run_id: int) -> dict | None:
    init_db()
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM agent_runs WHERE id = ?", (run_id,)).fetchone()
    return row_to_run(row) if row else None


def list_runs() -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM agent_runs ORDER BY id DESC").fetchall()
    return [row_to_run(row) for row in rows]


def get_tool_call(tool_call_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM tool_calls WHERE id = ?", (tool_call_id,)).fetchone()
    return dict(row) if row else None


def list_tool_calls(run_id: int | None = None) -> list[dict]:
    init_db()
    query = "SELECT * FROM tool_calls"
    params = ()
    if run_id is not None:
        query += " WHERE run_id = ?"
        params = (run_id,)
    query += " ORDER BY id"
    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def get_audit_event(event_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM audit_events WHERE id = ?", (event_id,)).fetchone()
    return dict(row) if row else None


def list_audit_events(run_id: int | None = None) -> list[dict]:
    init_db()
    query = "SELECT * FROM audit_events"
    params = ()
    if run_id is not None:
        query += " WHERE run_id = ?"
        params = (run_id,)
    query += " ORDER BY id"
    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
    return [dict(row) for row in rows]
