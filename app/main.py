from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR
from app.database import init_db
from app.metrics import audit_log, calculate_dashboard_metrics, cost_breakdown, error_summary, risk_summary
from app.schemas import AuditEventCreate, RunCreate, RunUpdate, ToolCallCreate
from app.storage import add_audit_event, add_tool_call, create_run, finish_run, list_runs
from app.synthetic_data import generate_synthetic_data
from app.trace_service import get_trace

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="AI Agent Observability Dashboard", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "app" / "static" / "index.html")


@app.get("/trace.html")
def trace_page():
    return FileResponse(BASE_DIR / "app" / "static" / "trace.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "synthetic-demo"}


@app.post("/runs")
def create_agent_run(payload: RunCreate) -> dict:
    return create_run(payload)


@app.patch("/runs/{run_id}")
def update_agent_run(run_id: int, payload: RunUpdate) -> dict:
    run = finish_run(run_id, payload)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.get("/runs")
def get_runs() -> list[dict]:
    return list_runs()


@app.get("/runs/{run_id}")
def get_run_trace(run_id: int) -> dict:
    trace = get_trace(run_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Run not found")
    return trace


@app.post("/runs/{run_id}/tool-call")
def log_tool_call(run_id: int, payload: ToolCallCreate) -> dict:
    tool_call = add_tool_call(run_id, payload)
    if not tool_call:
        raise HTTPException(status_code=404, detail="Run not found")
    return tool_call


@app.post("/runs/{run_id}/event")
def log_event(run_id: int, payload: AuditEventCreate) -> dict:
    event = add_audit_event(run_id, payload)
    if not event:
        raise HTTPException(status_code=404, detail="Run not found")
    return event


@app.post("/synthetic/generate")
def generate_synthetic() -> dict:
    return generate_synthetic_data(reset=True)


@app.get("/dashboard")
def dashboard() -> dict:
    return calculate_dashboard_metrics()


@app.get("/risks")
def risks() -> list[dict]:
    return risk_summary()


@app.get("/costs")
def costs() -> dict:
    return cost_breakdown()


@app.get("/errors")
def errors() -> dict:
    return error_summary()


@app.get("/audit")
def audit() -> list[dict]:
    return audit_log()
