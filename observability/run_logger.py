from app.schemas import RunCreate, RunUpdate
from app.storage import create_run, finish_run


def log_run(payload: RunCreate) -> dict:
    return create_run(payload)


def complete_run(run_id: int, payload: RunUpdate) -> dict | None:
    return finish_run(run_id, payload)
