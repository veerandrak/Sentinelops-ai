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
    t=DemoOpsTools(); s=state["service"]
    ev=[t.deployment(s),t.metrics(s),t.logs(s)]
    return {"evidence":[{"source":x.source,"detail":x.detail} for x in ev]}

def retrieve_context(state): return {"context":retrieve(f'{state["service"]} {state["question"]}')}

def reason(state):
    joined=" ".join(x["detail"] for x in state["evidence"])
    correlated=all(x in joined for x in ("v2.4.1","18%","DB_TIMEOUT"))
    if correlated:
        return {"hypothesis":"Deployment v2.4.1 correlates with database timeouts and elevated 5xx.","action":"rollback checkout-api to last known-good release"}
    return {"hypothesis":"Insufficient evidence; continue investigation.","action":"inspect logs and metrics"}

def gate(state): return {"requires_approval":classify_action(state["action"]).requires_approval}

def build_graph():
    g=StateGraph(IncidentState)
    for name,fn in [("collect",collect),("retrieve",retrieve_context),("reason",reason),("gate",gate)]: g.add_node(name,fn)
    g.set_entry_point("collect"); g.add_edge("collect","retrieve"); g.add_edge("retrieve","reason"); g.add_edge("reason","gate"); g.add_edge("gate",END)
    return g.compile()
