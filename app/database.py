import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


def get_connection(path: Path = DATABASE_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(path: Path = DATABASE_PATH) -> None:
    with get_connection(path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS agent_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_request_summary TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                start_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                end_time TEXT,
                status TEXT NOT NULL,
                final_outcome TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                completion_tokens INTEGER NOT NULL,
                total_tokens INTEGER NOT NULL,
                estimated_cost REAL NOT NULL,
                retry_count INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                risk_flags_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tool_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                tool_name TEXT NOT NULL,
                input_summary TEXT NOT NULL,
                output_summary TEXT NOT NULL,
                status TEXT NOT NULL,
                latency_ms INTEGER NOT NULL,
                error_message TEXT NOT NULL,
                retry_count INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(run_id) REFERENCES agent_runs(id)
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                decision TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                notes TEXT NOT NULL,
                FOREIGN KEY(run_id) REFERENCES agent_runs(id)
            );
            """
        )


def reset_db(path: Path = DATABASE_PATH) -> None:
    with get_connection(path) as connection:
        connection.executescript(
            """
            DROP TABLE IF EXISTS audit_events;
            DROP TABLE IF EXISTS tool_calls;
            DROP TABLE IF EXISTS agent_runs;
            """
        )
    init_db(path)
