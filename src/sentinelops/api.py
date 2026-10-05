from fastapi import FastAPI
from sentinelops.guardrails import classify_action
from sentinelops.models import ActionPlan, ActionRequest, IncidentRequest, IncidentResponse
from sentinelops.orchestrator import investigate

app = FastAPI(
    title="SentinelOps AI",
    version="0.1.0",
    description="Evidence-grounded agentic DevOps incident commander.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/incidents/analyze", response_model=IncidentResponse)
def analyze(request: IncidentRequest) -> IncidentResponse:
    return investigate(request.service, request.question)


@app.post("/v1/actions/plan", response_model=ActionPlan)
def plan_action(request: ActionRequest) -> ActionPlan:
    return classify_action(request.action)
