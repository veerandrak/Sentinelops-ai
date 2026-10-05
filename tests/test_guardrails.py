from sentinelops.guardrails import classify_action


def test_read_only_action_is_allowed():
    assert classify_action("inspect logs").requires_approval is False


def test_rollback_requires_approval():
    plan = classify_action("rollback checkout-api")
    assert plan.risk == "mutating"
    assert plan.requires_approval is True


def test_delete_is_destructive():
    assert classify_action("delete production namespace").risk == "destructive"
