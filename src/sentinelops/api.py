from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from sentinelops.graph import build_graph
from sentinelops.guardrails import classify_action
from sentinelops.models import ActionPlan, ActionRequest, IncidentRequest
from sentinelops.observability import observe_incident

app = FastAPI(
    title="SentinelOps AI",
    version="0.2.0",
    description="Evidence-grounded agentic DevOps incident commander.",
)
graph = build_graph()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/v1/incidents/analyze")
def analyze(request: IncidentRequest) -> dict:
    with observe_incident(request.service):
        return graph.invoke({"service": request.service, "question": request.question})


@app.post("/v1/actions/plan", response_model=ActionPlan)
def plan_action(request: ActionRequest) -> ActionPlan:
    return classify_action(request.action)
