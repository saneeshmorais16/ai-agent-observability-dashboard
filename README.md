# AI Agent Observability Dashboard

A portfolio-ready observability prototype for monitoring AI agent runs, tool calls, latency, cost estimates, errors, retries, prompt risks, approval decisions and audit logs.

## What This Project Does

The project records synthetic AI agent runs, logs tool calls, estimates token costs, detects risky prompts, stores audit events in SQLite and exposes dashboard metrics through FastAPI and a simple HTML/CSS/JavaScript frontend.

## Why It Matters

AI agents need operational visibility. Teams need to understand what an agent did, which tools were called, how long steps took, what failed, how much it may cost and whether prompts triggered safety or approval concerns.

## Problem Statement

Agent systems can become hard to inspect when planning, tool calls, retries and approvals happen across multiple steps. This dashboard creates a traceable record that supports debugging, review and governance.

## Tech Stack

- Python
- FastAPI
- SQLite
- pandas
- pydantic
- JavaScript, HTML and CSS
- pytest
- GitHub Actions

## Core Features

- Agent run tracking
- Tool-call tracing
- Token and cost estimation
- Latency monitoring
- Error and retry tracking
- Rule-based prompt risk detection
- Audit logging
- Dashboard metrics endpoint
- Trace view endpoint
- Synthetic data generator

## Agent Observability Architecture

```text
Agent run request
  -> Run logger
  -> Risk detector
  -> Tool logger
  -> Audit logger
  -> SQLite storage
  -> Metrics and trace services
  -> FastAPI dashboard/frontend
```

## Example Agent Trace

```json
{
  "run": {"agent_name": "safety_agent", "status": "failed", "risk_level": "critical"},
  "tool_calls": [{"tool_name": "approval_gate", "status": "failed", "latency_ms": 130}],
  "timeline": [{"type": "audit_event", "label": "tool_error", "risk_level": "medium"}]
}
```

## Example Dashboard Metrics

```json
{
  "total_agent_runs": 3,
  "successful_runs": 2,
  "failed_runs": 1,
  "high_risk_prompts": 1,
  "failure_rate": 33.33
}
```

## Example Risk Flags

- `prompt_injection`
- `credential_seeking`
- `data_exfiltration`
- `unsafe_instruction_override`
- `sensitive_data_warning`

## Setup Steps

```bash
pip install -r requirements.txt
```

## Run The API

```bash
python run.py
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard.

## Generate Synthetic Traces

```bash
python run.py
```

The generated SQLite database is local and ignored by Git.

## Run Tests

```bash
pytest
```

## Responsible AI / Privacy Limitations

This project uses only fake synthetic agent traces. It does not include real prompts, private conversations, real user data, customer data, private logs or API keys. It is a portfolio prototype and does not claim production use, real users, clients or enterprise deployment.

## Future Improvements

- Add OpenTelemetry-style export format.
- Add authentication for a real deployment scenario.
- Add charts for latency and cost trends.
- Add configurable risk rules.
- Add model/provider-specific cost tables.
- Add retention policies and audit export.

## No-Secrets Note

Do not commit `.env` files, API keys, tokens, credentials, passwords, private prompts, private conversations, real system logs, personal data, generated PDFs, application packets, databases or generated outputs.
