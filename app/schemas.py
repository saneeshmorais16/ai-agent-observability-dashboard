from typing import Literal

from pydantic import BaseModel, Field


RunStatus = Literal["running", "success", "failed", "blocked"]
RiskLevel = Literal["low", "medium", "high", "critical"]
ToolStatus = Literal["success", "failed"]


class RunCreate(BaseModel):
    user_request_summary: str = Field(..., min_length=3, max_length=500)
    agent_name: str = Field(..., min_length=2, max_length=80)
    status: RunStatus = "running"
    final_outcome: str = Field("", max_length=500)
    prompt_tokens: int = Field(0, ge=0)
    completion_tokens: int = Field(0, ge=0)
    retry_count: int = Field(0, ge=0)


class RunUpdate(BaseModel):
    status: RunStatus = "success"
    final_outcome: str = Field("", max_length=500)
    prompt_tokens: int = Field(0, ge=0)
    completion_tokens: int = Field(0, ge=0)
    retry_count: int = Field(0, ge=0)


class ToolCallCreate(BaseModel):
    tool_name: str = Field(..., min_length=2, max_length=120)
    input_summary: str = Field(..., min_length=1, max_length=500)
    output_summary: str = Field("", max_length=500)
    status: ToolStatus = "success"
    latency_ms: int = Field(0, ge=0)
    error_message: str = Field("", max_length=500)
    retry_count: int = Field(0, ge=0)


class AuditEventCreate(BaseModel):
    event_type: str = Field(..., min_length=2, max_length=120)
    actor: str = Field(..., min_length=2, max_length=120)
    decision: str = Field(..., min_length=2, max_length=120)
    # Keep risk levels predictable so dashboard filtering stays simple.
    risk_level: RiskLevel = "low"
    notes: str = Field("", max_length=500)


class RiskFlag(BaseModel):
    risk_type: str
    risk_level: RiskLevel
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
    risk_level: RiskLevel
    risk_flags: list[RiskFlag]
