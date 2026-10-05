from typing import TypedDict

from langgraph.graph import END, StateGraph

from sentinelops.guardrails import classify_action
from sentinelops.tools import DemoOpsTools
from sentinelops.vector_retrieval import retrieve


class IncidentState(TypedDict, total=False):
    service: str
    question: str
    evidence: list[dict]
    context: list[dict]
    hypothesis: str
    action: str
    requires_approval: bool


def collect(state: IncidentState):
    tools = DemoOpsTools()
    service = state["service"]
    evidence = [
        tools.deployment(service),
        tools.metrics(service),
        tools.logs(service),
    ]
    return {"evidence": [{"source": item.source, "detail": item.detail} for item in evidence]}


def retrieve_context(state: IncidentState):
    return {"context": retrieve(f'{state["service"]} {state["question"]}')}


def reason(state: IncidentState):
    joined = " ".join(item["detail"] for item in state["evidence"])
    correlated = all(marker in joined for marker in ("v2.4.1", "18%", "DB_TIMEOUT"))
    if correlated:
        return {
            "hypothesis": "Deployment v2.4.1 correlates with database timeouts and elevated 5xx.",
            "action": "rollback checkout-api to last known-good release",
        }
    return {
        "hypothesis": "Insufficient evidence; continue investigation.",
        "action": "inspect logs and metrics",
    }


def gate(state: IncidentState):
    return {"requires_approval": classify_action(state["action"]).requires_approval}


def build_graph():
    graph = StateGraph(IncidentState)
    graph.add_node("collect", collect)
    graph.add_node("retrieve", retrieve_context)
    graph.add_node("reason", reason)
    graph.add_node("gate", gate)
    graph.set_entry_point("collect")
    graph.add_edge("collect", "retrieve")
    graph.add_edge("retrieve", "reason")
    graph.add_edge("reason", "gate")
    graph.add_edge("gate", END)
    return graph.compile()
