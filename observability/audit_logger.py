from app.schemas import AuditEventCreate
from app.storage import add_audit_event


def log_audit_event(run_id: int, payload: AuditEventCreate) -> dict | None:
    return add_audit_event(run_id, payload)
