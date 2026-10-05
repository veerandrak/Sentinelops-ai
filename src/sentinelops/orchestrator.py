from sentinelops.guardrails import classify_action
from sentinelops.models import Evidence, IncidentResponse
from sentinelops.retrieval import retrieve_runbooks
from sentinelops.tools import DemoOpsTools


def investigate(service: str, question: str) -> IncidentResponse:
    tools = DemoOpsTools()
    raw = [tools.deployment(service), tools.metrics(service), tools.logs(service)]
    evidence = [Evidence(source=e.source, detail=e.detail) for e in raw]
    context = retrieve_runbooks(f"{service} {question}")

    correlated = service == "checkout-api" and all(
        marker in " ".join(e.detail for e in raw)
        for marker in ("v2.4.1", "18%", "DB_TIMEOUT")
    )
    if correlated:
        hypothesis = "The v2.4.1 deployment likely introduced or exposed database timeout behavior."
        action = "rollback checkout-api to the last known-good release"
        severity = "high"
    else:
        hypothesis = "Evidence is insufficient for a confident root-cause hypothesis."
        action = "continue read-only investigation and gather deployment, metric, and log evidence"
        severity = "medium"

    gate = classify_action(action)
    return IncidentResponse(
        service=service,
        severity=severity,
        hypothesis=hypothesis,
        evidence=evidence,
        runbook_context=context,
        recommended_action=action,
        requires_approval=gate.requires_approval,
    )
