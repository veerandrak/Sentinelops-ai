from sentinelops.models import ActionPlan

DESTRUCTIVE = {"delete", "destroy", "drop", "terminate"}
MUTATING = {"rollback", "restart", "scale", "apply", "deploy", "patch"}


def classify_action(action: str) -> ActionPlan:
    words = set(action.lower().replace("-", " ").split())
    if words & DESTRUCTIVE:
        return ActionPlan(risk="destructive", requires_approval=True,
                          reason="Destructive infrastructure actions always require human approval.")
    if words & MUTATING:
        return ActionPlan(risk="mutating", requires_approval=True,
                          reason="Infrastructure mutations require human approval.")
    return ActionPlan(risk="read_only", requires_approval=False,
                      reason="The requested operation is classified as read-only.")
