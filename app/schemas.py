from pydantic import BaseModel, Field


class RunCreate(BaseModel):
    user_request_summary: str = Field(..., min_length=3, max_length=500)
    agent_name: str = Field(..., min_length=2, max_length=80)
    status: str = "running"
    final_outcome: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    retry_count: int = 0


class RunUpdate(BaseModel):
    status: str = "success"
    final_outcome: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    retry_count: int = 0


class ToolCallCreate(BaseModel):
    tool_name: str
    input_summary: str
    output_summary: str = ""
    status: str = "success"
    latency_ms: int = 0
    error_message: str = ""
    retry_count: int = 0


class AuditEventCreate(BaseModel):
    event_type: str
    actor: str
    decision: str
    risk_level: str = "low"
    notes: str = ""


class RiskFlag(BaseModel):
    risk_type: str
    risk_level: str
    explanation: str


class RunResponse(BaseModel):
    id: int
    user_request_summary: str
    agent_name: str
    start_time: str
    end_time: str | None
    status: str
    final_outcome: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    retry_count: int
    risk_level: str
    risk_flags: list[RiskFlag]
