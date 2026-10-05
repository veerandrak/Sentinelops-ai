from typing import Literal

from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    service: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=3, max_length=1000)


class Evidence(BaseModel):
    source: str
    detail: str


class IncidentResponse(BaseModel):
    service: str
    severity: Literal["low", "medium", "high"]
    hypothesis: str
    evidence: list[Evidence]
    runbook_context: list[str]
    recommended_action: str
    requires_approval: bool


class ActionRequest(BaseModel):
    action: str = Field(min_length=1, max_length=300)


class ActionPlan(BaseModel):
    risk: Literal["read_only", "mutating", "destructive"]
    requires_approval: bool
    reason: str
